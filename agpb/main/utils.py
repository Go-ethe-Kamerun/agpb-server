import os
import sys
import json

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


def get_language_data():
    languages_data = {}
    language_data = []
    languages = Language.query.all()
    if languages is not None:
        for language in languages:
            language_data_entry = {}
            language_data_entry['id'] = language.id
            language_data_entry['label'] = language.label
            language_data_entry['lang_code'] = language.lang_code
            language_data.append(language_data_entry)
        languages_data['data'] = language_data
    return languages_data


def make_audio_id(translation_id, lang_code):
    if translation_id < 10:
        return 'cm_'+lang_code + '_00' + str(translation_id) + '.mp3'
    elif translation_id >= 10 and translation_id <= 99:
        return 'cm_' + lang_code + '_0' + str(translation_id) + '.mp3'
    else:
        return 'cm_'+lang_code + '_' +str(translation_id) + '.mp3'

def get_translation_data(category_number, language_code):
    translation_data = {}
    translations = []
    language = Language.query.filter_by(lang_code=language_code).first()
    category_id = Category.query.filter_by(id=category_number).first().id
    texts = Text.query.filter_by(category_id=category_id).all()
    # filter text in particular language
    for text in texts:
        translation_entry = {}
        if text.language_id == language.id:
            translation_entry['id'] = text.translation_id
            translation_entry['text'] = text.label.replace('"', '')
            translation_entry['audio_id'] = make_audio_id(text.translation_id, language.lang_code)
            translations.append(translation_entry)
    translation_data['translations'] = translations
    return translation_data