import json

from flask import Blueprint, redirect, request, session, url_for
from flask_login import current_user, login_user, logout_user
import mwoauth

from agpb import app, db
from agpb.models import User
from agpb.main.utils import commit_changes_to_db, send_response, manage_session
from agpb.users.utils import generate_random_token


users = Blueprint('users', __name__)


@users.route('/login')
def login():
    """Initiate an OAuth login.

    Call the MediaWiki server to get request secrets and then redirect the
    user to the MediaWiki server to sign the request.
    """
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        return redirect("https://agpb.toolforge.org/oauth/callback?token=" + str(user.temp_token), code=302)
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
        bearer_token = request.args.get('oauth_token')
        redirect_base_url = app.config['DEV_FE_URL'] if app.config['IS_DEV'] else app.config['PROD_FE_URL']
        response = redirect(redirect_base_url + "/oauth/callback?token=" + str(user.temp_token), code=302)
        session['bearer'] = bearer_token
        if commit_changes_to_db():
            login_user(user)
            return response
        # User token was not generated
        send_response('Error adding user to database', 401)


@users.route('/logout')
def logout():
    """Log the user out by clearing their session."""
    logout_user()
    session.clear()
    send_response('See you next time!', 200)


@manage_session
@users.route('/api/v1/verify_token', methods=['GET','POST'])
def get_current_user_info():
    token = request.args.get('token')

    user = User.query.filter_by(temp_token=token).first()
    if not user:
        send_response("No user with token", 404)
    user_infomration = {}
    user_info_obj = {}

    user_info_obj['username'] = user.username
    user_info_obj['lang'] = user.pref_lang
    user_info_obj['token'] = user.temp_token
    user_info_obj['bearer'] = session.get('bearer', None)

    user_infomration['user'] = user_info_obj
    return json.dumps(user_infomration)
