import os
import sys
import json

from flask import Blueprint, request

from agpb.main.utils import (get_category_data, get_language_data, get_translation_data,
                            get_audio_file)

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return '<h2> Welcome to African German Phrasebook Server</h2>'

@main.route('/api/v1/categories')
def getCategories():
    '''
    Get application categories
    '''

    # section_name = request.args.get('section')
    category_data = get_category_data()
    if category_data:
        return category_data
    else:
        return '<h2> Unable to get Category data at the moment</h2>'

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
