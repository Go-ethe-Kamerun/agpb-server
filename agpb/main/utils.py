import os
import shutil
import sys
import json
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
            category_data_entry['created_at'] = category.created_at
            category_data.append(category_data_entry)
        categories_data['categories'] = category_data
    return categories_data


def build_lang_url(lang_code):
    coountry_ext = 'cm'
    base_url = request.url.split('/api')[0]
    api_route = '/api/v1/translations?lang_code='

    if lang_code == 'de':
        coountry_ext = 'de'

    url = base_url + api_route + coountry_ext + '_' + lang_code
    return url


def get_language_data():
    languages_data = {}
    language_data = []
    languages = Language.query.all()
    if languages is not None:
        for language in languages:
            language_data_entry = {}
            language_data_entry['name'] = language.label
            language_data_entry['lang_code'] = language.lang_code
            language_data_entry['url'] = build_lang_url(language.lang_code)
            language_data.append(language_data_entry)
        languages_data['data'] = language_data
    return languages_data


def make_audio_id(translation_id, lang_code):
    coountry_ext = 'cm'

    if lang_code == 'de':
        coountry_ext = 'de'

    if translation_id < 10:
        return coountry_ext + "_" + lang_code + "_00" + str(translation_id) + ".mp3"
    elif translation_id >= 10 and translation_id <= 99:
        return coountry_ext + "_" + lang_code + "_0" + str(translation_id) + ".mp3"
    else:
        return coountry_ext + "_" + lang_code + "_" + str(translation_id) + ".mp3"

def create_translation_text_file(trans_text, lang_code):
    coountry_ext = 'cm'

    if lang_code == 'de':
        coountry_ext = 'de'

    root_dir = './agpb/db/data/trans/' + coountry_ext + '_' + lang_code
    file_name = root_dir + "/" +coountry_ext + "_" + lang_code + ".json"

    # Remove old file in case of update
    if os.path.isfile(file_name):
        os.remove(file_name)

    with open(file_name, 'a') as file:
        file.write(trans_text.strip())

    return root_dir


def create_zip_file(directory):
    shutil.make_archive(directory, 'zip', directory)
    return directory.split('/')[-1]


def convert_encoded_text(text):
    norm_data = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
    return norm_data.decode('ascii')


def get_translation_data(language_code):
    translation_data = {}
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
    trans_directory = create_translation_text_file(translations, language.lang_code)
    # create zip of the directory
    zip_file = create_zip_file(trans_directory)

    # Send a Zip file of the content to the user
    return send_file(app.config['UPLOADS'] + zip_file + '.zip', as_attachment=True)
