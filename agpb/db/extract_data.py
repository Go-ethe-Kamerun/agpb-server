import os
import sys
import json
import pandas as pd

from agpb.models import Category, Language, Text
from agpb.main.utils import commit_changes_to_db


def extract_category_data(category_list_file):
    ''' Extract category data from CSV file
        category_list_file: csv file containing categories
        return: category_list: list of categories to be added
    '''

    category_data = []
    data = pd.read_csv(category_list_file, sep='\t').values
    for row in data:
        category = {}
        
        category['label'] = row[0]
        category_data.append(category)
    category_data = [Category(label=category['label']) for category in category_data]
    return category_data


def write_data(data):
    ''' Write data to the database
        data: The data to be inserted into the database
    '''
    if commit_changes_to_db(data=data):
        print('Something is Wrong:(')
    else:
        print('Data Added!', file=sys.stderr)


def naviagate_folder(folder):
    folder_content = os.listdir(folder)
    return folder_content


def get_country_code(language):
    pass

def extract_languages(folder_dir_list):
    languages = []
    for folder in folder_dir_list:
        
        language = {}
        language['label'] = folder.split('_')[1]
        language['lang_code'] = folder.split('_')[0]
        languages.append(language)
    languages = [ Language(label=lang['label'], lang_code=lang['lang_code']) for lang in languages]
    return languages
