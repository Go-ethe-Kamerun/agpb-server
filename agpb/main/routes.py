import json

from flask import Blueprint, request, session
from agpb import db, app
import requests
from agpb.models import Contribution, User
from agpb.require_token import token_required
from agpb.main.utils import (get_category_data, get_language_data, get_translation_data,
                             get_audio_file, get_serialized_data, commit_changes_to_db,
                             manage_session, send_response, generate_csrf_token,
                             make_edit_api_call)

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return '<h2> Welcome to African German Phrasebook Server</h2>'


@manage_session
@main.route('/api/v1/categories')
def getCategories():
    '''
    Get application categories
    '''

    category_data = get_category_data()
    if category_data:
        return category_data
    else:
        return '<h2> Unable to get Category data at the moment</h2>'


@manage_session
@main.route('/api/v1/languages')
def getLanguages():
    '''
    Get application categories
    '''

    # section_name = request.args.get('section')
    language_data = get_language_data()
    if language_data:
        return language_data
    else:
        return '<h2> Unable to get Category data at the moment</h2>'


@main.route('/api/v1/play')
def playAudioFile():
    '''
    Get application categories
    '''
    lang_code = request.args.get('lang')
    audio_file = request.args.get('file')
    audio = get_audio_file(lang_code, audio_file)
    if audio:
        return audio
    else:
        return 'Audio not found'


@manage_session
@main.route('/api/v1/translations')
def getTranslations():
    '''
    Get translations by category
    '''
    # category_number = int(request.args.get('category'))
    language_code = request.args.get('lang_code').split('_')[1]
    return_type = request.args.get('return_type')
    translation_data = get_translation_data(language_code, return_type)
    if translation_data:
        return translation_data
    else:
        return '<h2> Unable to get Translation data at the moment</h2>'



@manage_session
@main.route('/api/v1/contributions')
@token_required
def getContributions(current_user):
    '''
    Get contributions
    '''
    contributions = get_serialized_data(Contribution.query.all())
    username = request.args.get('username')
    if username:
        return get_serialized_data(Contribution.query.filter_by(username=username).all())
    return contributions


@main.route('/api/v1/post-contribution', methods=['POST'])
def postContribution():
    contribution_data = request.json
    session_bearer = session.get('bearer', None)
    bearer = request.headers.get('bearer', None)
    user_v_token = request.headers.get('vtoken', None)
    latest_base_rev_id = 0

    if session_bearer != bearer:
        send_response('User cannot be verified', 401)

    username = User.query.filter_by(temp_token=user_v_token).first()

    if not username:
        send_response('User does not exist: please try to login', 401)

    valid_actions = [
        'wbsetclaim',
        'wbsetlabel',
        'wbsetdescription'
    ]
    if contribution_data['edit_type'] not in valid_actions:
        send_response('Incorrect edit type', 401)

    contribution = Contribution(username=username,
                                wd_item=contribution_data['wd_item'],
                                lang_code=contribution_data['lang_code'],
                                edit_type=contribution_data['edit_type'],
                                data=contribution_data['data'])

    csrf_token, api_auth_token = generate_csrf_token(
                app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'],
                session.get('access_token')['key'],
                session.get('access_token')['secret']
            )

    lastrevid = make_edit_api_call(csrf_token,
                                   api_auth_token,
                                   contribution_data,
                                   username)
    
    if not lastrevid:
        send_response('Edit failed', 401)

    db.session.add(contribution)
    latest_base_rev_id = lastrevid

    if not commit_changes_to_db():
        send_response('Contribution not saved', 403)

    return send_response(str(latest_base_rev_id), 200)


@main.route('/api/v1/upload-file', methods=['POST'])
def postUploadFile():
    upload_data = request.json
    user_v_token = request.headers.get('vtoken', None)
    session_bearer = session.get('bearer', None)
    header_bearer = request.headers.get('bearer', None)

    if session_bearer != header_bearer:
        send_response('User cannot be verified', 401)

    username = User.query.filter_by(temp_token=user_v_token).first()

    if not username:
        send_response('User does not exist: please try to login', 401)

    username = session.get('username', None)
    if not username:
        send_response('User does not exist', 401)

    csrf_token, api_auth_token = generate_csrf_token(
        app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'],
        session.get('access_token')['key'],
        session.get('access_token')['secret']
    )

    params = {}
    params['action'] = 'upload'
    params['format'] = 'json'
    params['filename'] = upload_data['filename']
    params['token'] = csrf_token
    params['text'] = "[[Category:African German Phrasebook " + upload_data['country'] + "]]"
    params['file'] = open(upload_data['file'], 'rb')

    response = requests.post(app.config['UPLOAD_API_URL'], data=params, auth=api_auth_token)

    if response.status_code != 200:
        send_response('File was not uploaded', 401)

    result = response.json()
    return result
