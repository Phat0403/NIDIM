import numpy as np
import json
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams
import os

from sentence_transformers import SentenceTransformer, util
from PIL import Image
import requests
from io import BytesIO

#Load CLIP model
model = SentenceTransformer('clip-ViT-B-32')
client_qdrant = QdrantClient(host='localhost', port=6333)
# Tạo collection
collection_name = 'clip-feature-3'

def decode_id(id):
    id_frame = id%1000
    v = int(((id - id_frame)/1000)%32)
    l = int(((id - id_frame)/1000-v)/32)
    return [f'L{l:02}_V{v:03}', id_frame]

def getData(video, id):
    with open('./media-info-b1/media-info/' + video + '.json', 'r', encoding='utf-8') as file:
            metadata = json.load(file)
            url = metadata["watch_url"]
    df = pd.read_csv('./map-keyframes-b1/map-keyframes/'+ video + '.csv')
    n, pts_time, fps, frame_idx =df.iloc[int(id)-1]
    return url, pts_time, fps, frame_idx

def find_index(arr, value):
    try:
        return arr.index(value) 
    except ValueError:
        return 1001
def join_arr(arr1, arr2):
    combined = arr1 + arr2
    unique_elements = {}
    unique_elements = {frozenset(item.items()): item for item in combined}
    unique_list = list(unique_elements.values())
    query = []
    result = []
    for el in unique_list:
        idx_1 = find_index(arr1, el) + 1
        idx_2 = find_index(arr2, el) + 1
        score = 2.0/(1.0/idx_1 + 1.0/idx_2)
        data = {'score': score, 'value': el}
        query.append(data)
    sorted_data = sorted(query, key=lambda x: x['score'])
    for el in sorted_data:
        result.append(el['value'])
    return result



def textQuery(data):
    n = len(data)
    query_more = []
    result = []
    count = 0
    for element in data:
        text = element['value']
        text_emb = model.encode([text])
        search_result = client_qdrant.search(collection_name=collection_name, query_vector=text_emb.tolist()[0], limit=1000)
        query = []
        for hit in search_result:
            video_frame, id_frame = decode_id(hit.id)
            data = {
             'video': video_frame, 
             'id': id_frame-count}
            query.append(data)
        query_more.append(query)
        count += 1
    ans = query_more[0]
    for i in range(1,count):
        ans = join_arr(ans, query_more[i])
    pd_video = []
    pd_frame = []
    for el in ans:
        video_frame = el['video']
        id_frame = el['id']
        url, pts_time, fps, frame_idx = getData(video_frame, id_frame)
        data = {
            'video': video_frame, 
            'id': id_frame,
            'url': url,
            'pts_time': pts_time,
            'frame_idx': frame_idx,
            'fps': fps,
            }
        result.append(data)
        pd_video.append(video_frame)
        pd_frame.append(int(frame_idx))
    
    pd_data = {
        'video': pd_video[0:100],
        'index': pd_frame[0:100]
    }
    df = pd.DataFrame(pd_data)
    df.to_csv('output.csv', index=False)
    return result[0:1000]



UPLOAD_FOLDER = 'uploads/'
def imageQuery():
    result = []
    img = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))][0]
    img_path = os.path.join(UPLOAD_FOLDER, img)
    img_emb = model.encode(Image.open(img_path))
    search_result = client_qdrant.search(collection_name=collection_name, query_vector=img_emb.tolist(), limit=500)
    for hit in search_result:
        video_frame, id_frame = decode_id(hit.id)
        url, pts_time, fps, frame_idx = getData(video_frame, id_frame)
        data = {
            'video': video_frame, 
            'id': id_frame,
            'url': url,
            'pts_time': pts_time,
            'frame_idx': frame_idx,
            'fps': fps}
        result.append(data)
    if os.path.exists(img_path):
        os.remove(img_path)
        print("File deleted successfully")
    else:
        print("File does not exist")
    return result


def similarQuery(url_img):
    result = []
    img_emb = model.encode(Image.open(url_img))
    search_result = client_qdrant.search(collection_name=collection_name, query_vector=img_emb.tolist(), limit=200)
    for hit in search_result:
        video_frame, id_frame = decode_id(hit.id)
        data = {
            'video': video_frame, 
            'id': id_frame,
            }
        result.append(data)
    return result