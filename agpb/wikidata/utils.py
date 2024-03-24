
import requests
from . import handle_search

def make_api_request(url, PARAMS):
    """ Makes request to an end point to get data

        Parameters:
            url (str): The Api url end point
            PARAMS (obj): The parameters to be used as arguments

        Returns:
            data (obj): Json object of the recieved data.
    """

    S = requests.Session()
    r = S.get(url=url, params=PARAMS)
    data = r.json()

    if data is None:
        return {}
    else:
        return data


def build_search_result(search_result):
    search_result_data = []

    for data in search_result:
        search_entity = {}
        if "id" in data.keys():
            search_entity["wd_id"] = data["id"]
        else:
            search_entity["wd_id"] = None
        if "label" in data.keys():
            search_entity["label"] = data["label"]
        else:
            search_entity["label"] = None
        if "description" in data.keys():
            search_entity["description"] = data["description"]
        else:
            search_entity["description"] = None

        search_result_data.append(search_entity)

    return search_result_data


def process_translations_data(translations_data, descriptions_data, wd_id, langs):
    translations_data_list = {}
    translations_data_list['translations'] = []
    lang_list = langs.split('|')

    for lang in lang_list:
        translation = {}
        translation["lang_code"] = lang

        if lang in translations_data[wd_id]["labels"].keys():
            translation["label"] = translations_data[wd_id]["labels"][lang]["value"]
        else:
            translation["label"] = None

        if lang in descriptions_data[wd_id]["descriptions"].keys():
            translation["description"] = descriptions_data[wd_id]["descriptions"][lang]["value"]
        else:
            translation["description"] = None

        translations_data_list['translations'].append(translation)
    translations_data_list["audios"], image_url = handle_search.get_item_audio_data(wd_id)
    translations_data_list["image_url"] = image_url

    return translations_data_list