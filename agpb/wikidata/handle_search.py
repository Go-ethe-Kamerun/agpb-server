from agpb import app
from .utils import make_api_request, build_search_result
from wikidata.client import Client
from wikidata.commonsmedia import File


def make_wd_api_search(search_term, lang):
    """ Make request to Wikidata for Item suggestions.

        Parameters:
            suggest_prefix (str): suggest prefix entery.
            lang (obj): Language for the search.

        Returns:
            extend_results (obj): Result for the data extension request.
    """

    PARAMS = {
        "action": "wbsearchentities",
        "format": "json",
        "language": lang,
        "type": "item",
        "search": search_term
    }

    wd_search_results = make_api_request(app.config['API_URL'], PARAMS)
    search_result_data = build_search_result(wd_search_results['search'])

    return search_result_data


def get_wikidata_entity_data(wd_id, props, langs):
    """ Fetch the lable of a Wikidata entity.

        Parameters:
            wd_id (str): WD id of the entity.
            lang (str): language of the label.

        Returns:
            label (str): label of wikidata item with ID wd_id.
    """

    PARAMS = {
        "action": "wbgetentities",
        "format": "json",
        "props": props,
        "languages": langs,
        "ids": wd_id
    }


    entityies_data = make_api_request(app.config["API_URL"], PARAMS)

    if "entities" in entityies_data.keys():
        return entityies_data["entities"]
    else:
        return {}


def get_entity_data(wd_id):
    client = Client()
    entity_data = client.get(wd_id, load=True).data
    return entity_data

def get_item_label(wd_item, lang_code):

    entity_data = get_entity_data(wd_item)['labels']
    if lang_code not in entity_data.keys():
        return "Nan"
    else:
        return entity_data[lang_code]['value']


def  get_language_data(wd_lang_id):
    PARAMS = {
        "action": "wbgetclaims",
        "format": "json",
        "property": "P220",
        "entity": wd_lang_id
    }

    lang_data = make_api_request(app.config["API_URL"], PARAMS)
    return lang_data['claims']


def get_image_url(image):
    PARAMS = {
        "action": "query",
        "titles": "File:" + image,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    image_data = make_api_request(app.config["API_URL"], PARAMS)
    image_id = list(image_data["query"]["pages"].keys())[0]
    if image_id:
        return image_data["query"]["pages"][image_id]["imageinfo"][0]["url"]
    else:
        return None


def get_item_audio_data(wd_id):
    client = Client()
    base_url = 'File:'
    if "P443" in get_entity_data(wd_id)['claims'].keys():
        audio_records = get_entity_data(wd_id)['claims']['P443']
    else:
        audio_records = []

    image_url = 'https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png'
    entity_claims = get_entity_data(wd_id)['claims']
    if 'P18' in entity_claims.keys():
        image = entity_claims['P18'][0]['mainsnak']['datavalue']['value']
        image_url = get_image_url(image)

    audio_translations =  []

    for audio in audio_records:
        audio_content = base_url + audio['mainsnak']['datavalue']['value']
        audio_lang_id = audio['qualifiers']['P407'][0]['datavalue']['value']['id']

        trans_data  = {}
        trans_data['lang_wd_id'] = audio_lang_id
        trans_data['audio_file'] = File(client=client, title=audio_content).image_url
        audio_translations.append(trans_data)
    return audio_translations, image_url           


def get_search_data(text, lang_code, locale):
    PARAMS = {
        "action": "wbsearchentities",
        "search": text,
        "type": "item",
        "language": lang_code,
        "uselang": locale,
        "format": "json"
    }

    search_data = make_api_request(app.config["API_URL"], PARAMS)
    if len(search_data["search"]) > 0:
        search_data_entries = []
        for search in search_data["search"]:
            entry = {}
            entry["id"] = search["id"]
            entry["label"] = search["label"]
            if "description" in search.keys():
                entry["description"] = search["description"]
            else:
                entry["description"] = None

            search_data_entries.append(entry)
        return search_data_entries
    else:
        return []
