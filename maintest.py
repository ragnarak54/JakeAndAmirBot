from elasticsearch import Elasticsearch
import json

es = Elasticsearch()

triathlon_doc = {'link': "https://www.youtube.com/watch?v=INVdbXTuPVI"}

with open('triathlon.txt', 'r', encoding="utf8") as triathlon_script:
    triathlon_doc['script'] = triathlon_script.read()

doc_json = json.dumps(triathlon_doc)

index_response = es.index(index="ja-test_index", doc_type="script", body=doc_json, id=1)

search_res = es.search(index="ja-test_index", body={"query": {"match": {"script": {"query": "cash money", "fuzziness": "AUTO"}}}})
for hit in search_res['hits']['hits']:
    print(hit['_source']['link'])
