import json

from flask import Blueprint, request, jsonify
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
def getContributions(current_user, data):
    '''
    Get contributions
    '''
    token_data = data
    contributions = get_serialized_data(Contribution.query.all())
    username = request.args.get('username')
    if username:
        return get_serialized_data(Contribution.query.filter_by(username=username).all())
    return contributions


@main.route('/api/v1/post-contribution', methods=['POST'])
@token_required
def postContribution(current_user, data):
    latest_base_rev_id = 0

    wd_item = request.form.get('wd_item')
    edit_type = request.form.get('edit_type')
    language = request.form.get('lang_code')
    lang_label = request.form.get('lang_label')
    upload_file = request.files['data'].read() if request.files else b''

    file_name = request.files['data'].filename if request.files else None
    contrib_data = upload_file if edit_type == 'wbsetclaim' else request.form.get('data')

    valid_actions = [
        'wbsetclaim',
        'wbsetlabel',
        'wbsetdescription'
    ]
    print('edit_type', edit_type)
    if edit_type not in valid_actions:
        send_response('Incorrect edit type', 401)
    try:
        contribution = Contribution(username=current_user.username,
                                    wd_item=wd_item,
                                    lang_code=language,
                                    edit_type=edit_type,
                                    data=contrib_data)
    except Exception as e:
        return jsonify(str(e))

    auth_obj = {
        "consumer_key": app.config['CONSUMER_KEY'],
        "consumer_secret": app.config['CONSUMER_SECRET'],
        "access_token": data.get('access_token')['key'],
        "access_secret": data.get('access_token')['secret'],
    }

    lastrevid = make_edit_api_call(edit_type, current_user.username,language, lang_label,
                                    contrib_data, wd_item, auth_obj, file_name=file_name)
    
    if not lastrevid:
        send_response('Edit failed', 401)

    db.session.add(contribution)
    latest_base_rev_id = lastrevid

    if not commit_changes_to_db():
        send_response('Contribution not saved', 403)

    return send_response(str(latest_base_rev_id), 200)
