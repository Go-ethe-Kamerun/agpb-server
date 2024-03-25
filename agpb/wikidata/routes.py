import json

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from .handle_languages import getLanguages
from .handle_search import get_wikidata_entity_data, get_search_data
from .utils import process_translations_data
from agpb.require_token import token_required

wikidata = Blueprint('wikidata', __name__)


@wikidata.route('/languages', methods=['GET', 'POST'])
def get_languages():
    languages = getLanguages()
    return jsonify(languages)


@wikidata.route('/text-search', methods=['GET', 'POST'])
def get_search_Items():
    text = request.args.get('text')
    lang_code = request.args.get('lang_code')
    search_data = get_search_data(text, lang_code)
    return jsonify(search_data)


@wikidata.route('/search', methods=['GET', 'POST'])
@token_required
def make_search(current_user, data):
    wd_id = request.args.get('wd_id')
    base_language = request.args.get('base_lang')
    dest_language_one = request.args.get('dest_lang_one')
    dest_language_two = request.args.get('dest_lang_two')
    langs = base_language + '|' + dest_language_one + '|' + dest_language_two

    translation_label_data = get_wikidata_entity_data(wd_id, "labels", langs)
    translation_description_data = get_wikidata_entity_data(wd_id, "descriptions", langs)
    translations = process_translations_data(translation_label_data, translation_description_data, wd_id, langs)

    return jsonify(translations)
