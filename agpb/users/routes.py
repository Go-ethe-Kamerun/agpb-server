import json

from flask import Blueprint, redirect, request, session, url_for
from flask_login import current_user, login_user, logout_user
import mwoauth

from agpb import app, db
from agpb.models import User
from agpb.main.utils import commit_changes_to_db, send_abort
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
        send_abort('OAuth callback failed. Are cookies disabled?', 404)

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
        send_abort('OAuth callback failed. Are cookies disabled?', 404)
    else:
        session['access_token'] = dict(zip(
            access_token._fields, access_token))
        session['username'] = identity['username']
        print(identity.keys())
        # In this case, handshake is finished and we redirect
        user = User.query.filter_by(username=session.get('username')).first()
        user.temp_token = generate_random_token()
        if commit_changes_to_db():
            return redirect("https://agpb.toolforge.org/oauth/callback?token=" + str(user.temp_token), code=302)
        # User token was not generated
        send_abort('Error adding user to database', 401)


@users.route('/logout')
def logout():
    """Log the user out by clearing their session."""
    logout_user()
    session.clear()
    send_abort('See you next time!', 200)


@users.route('/api/v1/verify_token', methods=['GET','POST'])
def get_current_user_info():
    token = request.args.get('token')

    user = User.query.filter_by(temp_token=token).first()
    if not user:
        send_abort("No user with token", 404)
    user_infomration = {}   
    user_info_obj = {}

    user_info_obj['username'] = user.username
    user_info_obj['lang'] = user.pref_lang
    user_info_obj['token'] = user.temp_token

    user_infomration['user'] = user_info_obj
    return json.dumps(user_infomration)
