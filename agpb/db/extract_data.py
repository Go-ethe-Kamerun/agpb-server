import fnmatch
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
        category['label'] = row[0].split(',')[1]
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


def extract_languages(folder_dir_list):
    languages = []
    for folder in folder_dir_list:
        language = {}
        language['label'] = folder.split('_')[1]
        language['lang_code'] = folder.split('_')[0]
        languages.append(language)
    languages = [Language(label=lang['label'], lang_code=lang['lang_code']) for lang in languages]
    return languages


def get_text_category(index_number):
    category_data = pd.read_csv('agpb/db/data/category_list.csv', sep='\t').values
    for data in category_data:
        category_number = int(data[0].split(',')[0])
        category_start = int(data[0].split(',')[2].split('-')[0])
        category_end = int(data[0].split(',')[2].split('-')[1])
        if index_number in list(range(category_start, category_end)):
            return category_number


def extract_text_data(content_folder):
    text_data_files = []
    text_data = []
    root = content_folder
    folder_content_list = naviagate_folder(content_folder)
    folder_content_list = [root + '/' + folder for folder in folder_content_list]
    for folder_content in folder_content_list:
        for text_file in os.listdir(folder_content):
            if text_file.endswith('.csv'):
                text_data_files.append(folder_content + '/' + text_file)
    # Read the data files now and get the data
    for lang_data_file in text_data_files:
        file_data = pd.read_csv(lang_data_file, sep='\t').values
        
        file_lang_code = lang_data_file.split('/')[-1].split('_')[1].split('.')[0]
        text_lang_id = Language.query.filter_by(lang_code=file_lang_code).first().id

        for row in file_data:
            text_cateogry_index = int(row[0].split(',')[0])
            text_label = row[0].split(',')[1].replace('"', '')
            text = Text(label=text_label,
                        category_id=get_text_category(text_cateogry_index),
                        language_id=text_lang_id,
                        translation_id=text_cateogry_index)
            text_data.append(text)
    return text_data
