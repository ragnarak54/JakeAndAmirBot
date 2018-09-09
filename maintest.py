from elasticsearch import Elasticsearch
import json

es = Elasticsearch()


def create_script(script_file, link):
    doc = {'link': link}

    with open(script_file, 'r', encoding="utf8") as script:
        doc['script'] = script.read()

    return json.dumps(doc)


def save_script(doc):
    return es.index(index="ja-test_index", doc_type="script", body=doc)


def search_script(query):
    # search for a script + link
    search_res = es.search(index="ja-test_index", body={"query": {"match": {"script": {"query": query}}}})
    for hit in search_res['hits']['hits']:
        print(hit)


def main():
    # triathlon = create_script("triathlon.txt", "https://www.youtube.com/watch?v=INVdbXTuPVI")
    # save_script(triathlon)
    # corduroy = create_script("corduroy_pants.txt", "https://www.youtube.com/watch?v=ao2xLlxiaNo")
    # save_script(corduroy)

    search_script("if you're the trunk, then you got punked")


if __name__ == "__main__":
    main()
