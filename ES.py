from elasticsearch import Elasticsearch
import csv
import json
import youtubeapi as youtube
import redditapi as reddit
import os

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
            reddit_link = row[2]

            script_doc = create_script(title, script, youtube_link, reddit_link)
            save_script(script_doc)
            print("Saved doc " + str(doc_count) + ": " + script_doc)
            doc_count = doc_count + 1


def create_script(title, script, youtube_link, reddit_link):
    doc = {'title': title, 'script': script, 'youtube_link': youtube_link, 'reddit_link': reddit_link}
    return json.dumps(doc)


def save_script(doc):
    return es.index(index=current_index, doc_type="script", body=doc)


def search_script(query):
    # search for a script + link
    search_res = es.search(index=current_index, body={"query": {"span_near": {"clauses": create_fuzzy_clauses(query),
                                                                            "slop": 3, "in_order": "true"}}})
    if not search_res['hits']['hits']:
        return None

    return search_res['hits']['hits'][0]


def search_script_debug(query):
    search_res = es.search(index=current_index, body={"query": {"span_near": {"clauses": create_fuzzy_clauses(query),
                                                                            "slop": 3, "in_order": "true"}}})
    for hit in search_res['hits']['hits']:
        print(hit)


# https://stackoverflow.com/questions/38816955/elasticsearch-fuzzy-phrases
def create_fuzzy_clauses(query):
    tokens = query.split(" ")
    clauses = []

    for token in tokens:
        span_multi_query = {
            "span_multi": {
                "match": {
                    "fuzzy": {
                        # field to search in here
                        "script": {
                            "fuzziness": "3",
                            "value": token
                        }
                    }
                }
            }
        }
        clauses.append(span_multi_query)

    return clauses


def print_all_scripts():
    search_res = es.search(index=current_index, body={"query": {"match_all": {}}})
    # TODO: Print all scripts, not just the first 10
    for hit in search_res['hits']['hits']:
        print(hit)


def search_script_by_title(title):
    search_res = es.search(index=current_index, body={"query": {"match_phrase": { "title": title}}})

    for hit in search_res['hits']['hits']:
        print(hit)


def delete_doc_by_id(id):
    res = es.delete(index=current_index, doc_type="script", id=id)


def clear_index():
    es.indices.delete(index=current_index, ignore=[400, 404])


def add_script_with_text_file(title, filepath, youtube_link, reddit_link):
    # https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python
    script_dir = os.path.dirname(__file__)  # <-- absolute dir this script is in
    rel_path = filepath
    abs_file_path = script_dir + rel_path

    with open(abs_file_path, 'r', encoding="utf-8") as script_file:
        script_text = script_file.read()

    save_script(create_script(title, script_text, youtube_link, reddit_link))
