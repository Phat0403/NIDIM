from elasticsearch import Elasticsearch
import json

username = 'elastic'
password = '' # Dien password vao day

es_client = Elasticsearch(
    "https://localhost:9200",
    basic_auth=(username, password),
    ca_certs=False,
    verify_certs=False
)

index_name = 'aic_ocr'

with open("tokenizer.json", "r", encoding="utf-8") as f:
    tokenizer = json.load(f)

with open("filter.json", "r", encoding="utf-8") as f:
    filterr = json.load(f)

with open("analyzer.json", "r", encoding="utf-8") as f:
    analyzer = json.load(f)

index_config = {
    "settings": {
        "analysis": {
            "tokenizer": tokenizer["tokenizer"],
            "filter": filterr,
            "analyzer": analyzer
        }
    },
    "mappings": {
        "properties": {
            "frame_id": {
                "type": "keyword"
            },
            "text": {
                "type": "text",
                "analyzer": "custom_analyzer"
            }
        }
    }
}

def create_index(index_name,config):
    if es_client.indices.exists(index=index_name):
        es_client.indices.delete(index=index_name)
    es_client.indices.create(index=index_name, body=config)
    # Check
    if es_client.indices.exists(index=index_name):
        print(f"Index {index_name} created")
    else:
        print("Some thing went wrong")

if __name__ == '__main__':
    create_index(index_name, index_config)
