from elasticsearch import Elasticsearch
import csv
import json
import youtubeapi as youtube
import redditapi as reddit

es = Elasticsearch()
current_index = "ja-test_index"


def auto_index_scripts():
    with open('JakeAndAmir_spreadsheet.csv', encoding="utf8") as scripts_spreadsheet:
        csv_reader = csv.reader(scripts_spreadsheet)
        doc_count = 0

        for row in csv_reader:
            script = reddit.read_script(row[2])
            title = row[0]
            youtube_link = youtube.search("Jake and Amir " + title)

            script_doc = create_script(script, youtube_link, title)
            save_script(script_doc)
            print("Saved doc " + str(doc_count) + ": " + script_doc)
            doc_count = doc_count + 1


def create_script(script_text, link, title):
    doc = {'link': link, 'title': title, 'script': script_text}
    return json.dumps(doc)


def save_script(doc):
    return es.index(index=current_index, doc_type="script", body=doc)


def search_script(query):
    # search for a script + link
    search_res = es.search(index=current_index, body={"query": {"match": {"script":
                                                                              {"query": query}}}})
    for hit in search_res['hits']['hits']:
        print(hit)


def match_all_scripts():
    search_res = es.search(index=current_index, body={"query": {"match_all": {}}})
    for hit in search_res['hits']['hits']:
        print(hit)


def clear_index():
    es.indices.delete(index=current_index, ignore=[400, 404])

