import os
import json
from elasticsearch import Elasticsearch, helpers
from concurrent.futures import ThreadPoolExecutor

username = 'elastic'
password = '' # Dien password vao day

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=(username, password),
    ca_certs=False,
    verify_certs=False
)

index_name = 'aic_ocr'

def index_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    print(f"Indexing {file_path}") # theo doi
    data_text = " ".join([entry["text"] for entry in json_data])
    parent_dir = os.path.basename(os.path.dirname(file_path))
    file_name = os.path.basename(file_path).replace('.json', '')
    frame_id = f"{parent_dir}, {file_name}"
    return {
        "_index": index_name,
        "_source": {
            "frame_id": frame_id,
            "text": data_text
        }
    }


def index_data(root, batch_size=1000):
    actions = []  
    with ThreadPoolExecutor() as executor:
        for subdir, dirs, files in os.walk(root):
            json_files = [os.path.join(subdir, file) for file in files if file.endswith(".json")]
            results = list(executor.map(index_file, json_files))
            for action in results:
                actions.append(action)
                if len(actions) >= batch_size:
                    helpers.bulk(es, actions)
                    print(f"Indexed {len(actions)} documents")
                    actions = []
        if actions:
            helpers.bulk(es, actions)
            print(f"Indexed {len(actions)} documents")


if __name__ == '__main__':
    root = "OCR"
    index_data(root)

# def test(root):
#     print("start")
#     length = 0
#     for subdir, dirs, files in os.walk(root):
#         for file in files:
#             if file.endswith(".json"):
#                 file_path = os.path.join(subdir, file)
#                 length += 1
#                 print(file_path)
#     print(length)
# test("OCR")