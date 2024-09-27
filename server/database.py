import numpy as np
import json
import pandas as pd
import os 
from qdrant_client import QdrantClient
from qdrant_client import models
from elasticsearch import Elasticsearch
import urllib3
import os

client_qdrant = QdrantClient(host='104.214.176.14', port=6333, timeout=60)
collection_name = 'clip-feature-4'
##########################################################################################################################################
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = 'elastic'
password = 'Mn*mMi=L2ceq+oEC4Ovm'#'-LMpeY1XX13uwH95CuWP' # Dien password vao day

es = Elasticsearch(
    "https://104.214.176.14:9200",
    basic_auth=(username, password),
    ca_certs=False,
    verify_certs=False
)
##########################################################################################################################################
def decode_id(id):
    id_frame = id%3000
    v = int(((id - id_frame)/3000)%50)
    l = int(((id - id_frame)/3000-v)/50)
    return [f'L{l:02}_V{v:03}', id_frame]

def getData(video, id):
    with open('C:/Users/tanph/OneDrive/Desktop/NIDIM/server/media-info-b1/media-info/' + video + '.json', 'r', encoding='utf-8') as file:
            metadata = json.load(file)
            url = metadata["watch_url"]
    df = pd.read_csv('C:/Users/tanph/OneDrive/Desktop/NIDIM/server/map-keyframes/'+ video + '.csv')
    n , pts_time, fps, frame_idx =df.iloc[int(id)-1]
    return url, pts_time, fps, frame_idx
##########################################################################################################################################
def fuzzy_search(query, max_results=1000): 
    if es.indices.exists(index='aic_ocr'):
        print('co')
    else:
        print('khong')
    response = es.search(
        index='aic_ocr',
        body={
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "text": {
                                    "query": query,
                                    "fuzziness": "AUTO",  
                                    "operator": "or"  
                                }
                            }
                        }
                    ],
                    "minimum_should_match": 1  
                }
            },
            "size": max_results,
            "sort": [
                {
                    "_score": {
                        "order": "desc"  
                    }
                }
            ]
        }
    )
    return response['hits']['hits']

##########################################################################################################################################
def find_vector(emb):
    result = []
    search_result = client_qdrant.search(
        collection_name=collection_name,
        query_vector=emb.tolist(), 
        limit=1000)
    search_result =[hit.id for hit in search_result]
    for hit in search_result:
        video_frame, id_frame = decode_id(hit)
        url, pts_time, fps, frame_idx = getData(video_frame, id_frame)
        data = {
            'video': video_frame, 
            'id': id_frame,
            'url': url,
            'pts_time': pts_time,
            'frame_idx': frame_idx,
            'fps': fps}
        result.append(data)
    return result


def findOcr(ocr):
    result = []
    search_result = fuzzy_search(ocr)
    search_result = [result['_source']['frame_id'].split(', ') for result in search_result]
    for hit in search_result:
        video_frame = hit[0]
        id_frame = hit[1]
        url, pts_time, fps, frame_idx = getData(video_frame, id_frame)
        data = {
            'video': video_frame, 
            'id': id_frame,
            'url': url,
            'pts_time': pts_time,
            'frame_idx': frame_idx,
            'fps': fps}
        result.append(data)
    return result
