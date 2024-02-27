import json

from flask import Blueprint, redirect, request, session, url_for, make_response, jsonify
from flask_login import current_user, login_user, logout_user
import mwoauth

from agpb import app, db
from agpb.models import User
from agpb.main.utils import commit_changes_to_db, send_response, manage_session
from agpb.users.utils import generate_random_token
from agpb.require_token import token_required

import jwt
import datetime

users = Blueprint('users', __name__)


@users.route('/login')
def login():
    """Initiate an OAuth login.

    Call the MediaWiki server to get request secrets and then redirect the
    user to the MediaWiki server to sign the request.
    """
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        return jsonify({'token': user.temp_token})
    else:
        consumer_token = mwoauth.ConsumerToken(
            app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
        try:
            redirect_string, request_token = mwoauth.initiate(
                app.config['OAUTH_MWURI'], consumer_token)
        except Exception:
            app.logger.exception('mwoauth.initiate failed')
            return redirect(url_for('main.home'))
        else:
            session['request_token'] = dict(zip(
                request_token._fields, request_token))
            if session.get('username'):
                user = User.query.filter_by(username=session.get('username')).first()
                if not user:
                    user = User(username=session.get('username'), pref_lang='en', temp_token = generate_random_token())
                    db.session.add(user)

                    if commit_changes_to_db():
                        pass
            return redirect(redirect_string)


@users.route('/oauth-callback')
def oauth_callback():
    """OAuth handshake callback."""
    if 'request_token' not in session:
        send_response('OAuth callback failed. Are cookies disabled?', 404)

    consumer_token = mwoauth.ConsumerToken(
        app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])

    try:
        access_token = mwoauth.complete(
            app.config['OAUTH_MWURI'],
            consumer_token,
            mwoauth.RequestToken(**session['request_token']),
            request.query_string)
        identity = mwoauth.identify(
            app.config['OAUTH_MWURI'], consumer_token, access_token)
    except Exception:
        app.logger.exception('OAuth authentication failed')
        send_response('OAuth callback failed. Are cookies disabled?', 404)
    else:
        session['access_token'] = dict(zip(
            access_token._fields, access_token))
        session['username'] = identity['username']
        # In this case, handshake is finished and we redirect
        user = User.query.filter_by(username=session.get('username')).first()
        user.temp_token = generate_random_token()

        token = jwt.encode({
                'token' : user.temp_token,
                'access_token': session.get('access_token', None),
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
                app.config['SECRET_KEY'], "HS256")

        if commit_changes_to_db():
            login_user(user)
            redirect_base_url = app.config['DEV_FE_URL'] if app.config['IS_DEV'] else app.config['PROD_FE_URL']
            response = redirect(redirect_base_url + "/oauth/callback?token=" + str(token), code=302)
            return response

        # User token was not generated
        send_response('Error adding user to database', 401)


@users.route('/logout')
def logout():
    """Log the user out by clearing their session."""
    logout_user()
    session.clear()
    send_response('See you next time!', 200)


@users.route('/api/v1/current_user', methods=['GET','POST'])
@token_required
def get_current_user_info(current_user, data):
    user_infomration = {}
    user_info_obj = {}

    user_info_obj['username'] = current_user.username
    user_info_obj['lang'] = current_user.pref_lang
    user_info_obj['token'] = current_user.temp_token
    user_infomration['user'] = user_info_obj

    response = make_response(user_infomration)
    return response
