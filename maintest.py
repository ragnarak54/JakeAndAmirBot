from elasticsearch import Elasticsearch
import json
import config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

es = Elasticsearch()
current_index = "ja-test_index"

GOOGLE_API_KEY = config.google_api_key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(query):
    try:
        youtube = build(serviceName=YOUTUBE_API_SERVICE_NAME, version=YOUTUBE_API_VERSION, developerKey=GOOGLE_API_KEY)
        search_response = youtube.search().list(q=query, type="video", maxResults=1, part="id").execute()

        return "https://www.youtube.com/watch?v=" + search_response['items'][0]['id']['videoId']

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))


def create_script(script_file, link):
    doc = {'link': link}

    with open(script_file, 'r', encoding="utf8") as script:
        doc['script'] = script.read()

    return json.dumps(doc)


def save_script(doc):
    return es.index(index=current_index, doc_type="script", body=doc)


def search_script(query):
    # search for a script + link
    search_res = es.search(index=current_index, body={"query": {"match": {"script": {"query": query}}}})
    for hit in search_res['hits']['hits']:
        print(hit)


def match_all_scripts():
    search_res = es.search(index=current_index, body={"query": {"match_all": {}}})
    for hit in search_res['hits']['hits']:
        print(hit)


def clear_index():
    es.indices.delete(index='ja-test_index', ignore=[400, 404])

# save_script(create_script("triathlon.txt", youtube_search("Jake and Amir Triathlon")))
# save_script(create_script("corduroy_pants.txt", youtube_search("Jake and Amir Corduroy Pants")))
