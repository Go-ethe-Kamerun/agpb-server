import os
import shutil
import sys
import json
import ast
import unicodedata

from agpb import app
from flask import send_file, request
from agpb import db

from agpb.models import Category, Language, Text


def commit_changes_to_db(data=None):
    """
    Test for the success of a database commit operation.

    """
    if data is not None:
        for d in data:
            db.session.add(d)
    try:
        db.session.commit()
    except Exception as e:
        # TODO: We could add a try catch here for the error
        print('-------------->>>>>', file=sys.stderr)
        print(str(e), file=sys.stderr)
        db.session.rollback()
        # for resetting non-commited .add()
        db.session.flush()
        return True
    return False


def get_category_data():
    categories_data = {}
    category_data = []
    categories = Category.query.all()
    if categories is not None:
        for category in categories:
            category_data_entry = {}
            category_data_entry['id'] = category.id
            category_data_entry['label'] = category.label
            category_data.append(category_data_entry)
        categories_data['categories'] = category_data
    return categories_data


def build_country_lang_code(lang_code):
    country_ext = 'cm'
    if lang_code == 'de':
        country_ext = 'de'
    return country_ext + '_' + lang_code


def build_lang_url(lang_code, url_type):
    country_ext = 'cm'
    ip_address = app.config['SERVER_ADDRESS']
    api_route = '/api/v1/translations?lang_code='

    if lang_code == 'de':
        country_ext = 'de'

    url = ip_address + api_route + country_ext + '_' + lang_code
    if url_type == 'zip':
        url += '&return_type=zip'
    else:
        url += '&return_type=json'
    return url


def check_lang_support(lang_code):
    root_dir = './agpb/db/data/trans/'
    lang_dirs = os.listdir(root_dir)
    if lang_code in lang_dirs:
        return 'true'
    else:
        return 'false'


def get_language_data():
    languages_data = {}
    language_data = []
    languages = Language.query.all()
    if languages is not None:
        for language in languages:
            language_data_entry = {}
            language_data_entry['name'] = language.label
            language_data_entry['lang_code'] = build_country_lang_code(language.lang_code)
            language_data_entry['zip_url'] = build_lang_url(language.lang_code, 'zip')
            language_data_entry['json_url'] = build_lang_url(language.lang_code, 'json')
            language_data_entry['supported'] = check_lang_support(build_country_lang_code(
                                                                  language.lang_code))
            language_data.append(language_data_entry)
        languages_data['data'] = language_data
    return languages_data


def make_audio_id(translation_id, lang_code):
    country_ext = 'cm'

    if lang_code == 'de':
        country_ext = 'de'

    if translation_id < 10:
        return country_ext + "_" + lang_code + "_00" + str(translation_id) + ".mp3"
    elif translation_id >= 10 and translation_id <= 99:
        return country_ext + "_" + lang_code + "_0" + str(translation_id) + ".mp3"
    else:
        return country_ext + "_" + lang_code + "_" + str(translation_id) + ".mp3"


def create_translation_text_file(trans_text, lang_code):
    country_ext = 'cm'

    if lang_code == 'de':
        country_ext = 'de'
    root_dir = './agpb/db/data/trans/' + country_ext + '_' + lang_code
    file_name = root_dir + "/" + country_ext + "_" + lang_code + ".json"

    # Remove old file in case of update
    if os.path.isfile(file_name):
        os.remove(file_name)

    with open(file_name, 'a') as file:
        file.write(trans_text.strip())

    return root_dir


def create_zip_file(directory, lang_code):
    archived_file = shutil.make_archive(directory, 'zip', directory)
    return archived_file


def convert_encoded_text(text):
    # norm_data = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
    return text


def get_audio_file_path(audio):
    country_code = audio.split('_')[0] + '_' + audio.split('_')[1]
    audio_full_path = app.config['SERVER_ADDRESS'] + \
        app.config['PLAY_AUDIO_ROUTE'] + 'lang=' + \
        country_code + '&file=' + audio
    return audio_full_path


def get_audio_file(lang_code, audio_number):
    download_directory = app.config['UPLOADS_DIR'] + \
        lang_code + '/' + audio_number
    return send_file(download_directory, as_attachment=True)


def get_translation_data(language_code, return_type):
    translations = []
    language = Language.query.filter_by(lang_code=language_code).first()
    # category_id = Category.query.filter_by(id=category_number).first().id
    texts = Text.query.filter_by(language_id=language.id).all()

    # filter text in particular language
    for text in texts:
        translation_entry = {}
        translation_entry['No'] = str(text.translation_id)
        translation_entry['text'] = convert_encoded_text(text.label)
        if text.category_id is None:
            translation_entry['category'] = 'none'
        else:
            translation_entry['category'] = Category.query.filter_by(id=text.category_id).first().label
        translation_entry['audio'] = make_audio_id(text.translation_id,
                                                   language.lang_code)
        translations.append(translation_entry)

    # translation_data['export default'] = translations
    translations = json.dumps(translations)
    if return_type == 'json':
        translations = ast.literal_eval(translations)
        for translation in translations:
            translation['audio'] = get_audio_file_path(translation['audio'])

        return json.dumps(translations, ensure_ascii=False).encode('utf8')
    elif return_type == 'zip':
        trans_directory = create_translation_text_file(translations, language.lang_code)
        # create zip of the directory
        zip_file = create_zip_file(trans_directory, language_code)
        # Send a Zip file of the content to the user
        return send_file(zip_file, as_attachment=True)
    else:
        return 'return_type may be missing: How do you want to get the data? zip or json'
