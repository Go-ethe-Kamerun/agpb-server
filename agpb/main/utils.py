import os

from agpb import db

from agpb.models import Category, Language


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
