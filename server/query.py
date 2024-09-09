import numpy as np
import json
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams
import os
import rag_fusion as rf
from sentence_transformers import SentenceTransformer, util
from PIL import Image

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
    with open('./data/media-info-b1/media-info/' + video + '.json', 'r', encoding='utf-8') as file:
            metadata = json.load(file)
            url = metadata["watch_url"]
    df = pd.read_csv('./data/map-keyframes-b1/map-keyframes/'+ video + '.csv')
    _, pts_time, fps, frame_idx =df.iloc[int(id)-1]
    return url, pts_time, fps, frame_idx

def textQuery(data):
    print(data)
    text = data[0]['value']
    result = []
    rrf_input=[]
    text=text.split("\n")
    text= [a for a in text if a != " "]
    # print(text)
    text_embs = model.encode(text)
    print(text_embs.shape)
    search_result=None
    for i in range(text_embs.shape[0]): ## rag_fusion
        text_emb=text_embs[i]
        # print(text_emb.tolist())
        search_result = client_qdrant.search(collection_name=collection_name, query_vector=text_emb.tolist(), limit=100)
        rrf_input.append([hit.id for hit in search_result])
    search_result=rf.rrf(rrf_input)
    for hit in search_result:
        video_frame, id_frame = decode_id(hit)
        url, pts_time, fps, frame_idx = getData(video_frame, id_frame)
        # print(video_frame,id_frame)
        data = {
            'video': video_frame, 
            'id': id_frame,
            'url': url,
            'pts_time': pts_time,
            'frame_idx': frame_idx,
            'fps': fps}
        result.append(data)
    return result


UPLOAD_FOLDER = 'uploads/'
def imageQuery(text):
    result=[]
    # return None
    img = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))][0]
    img_path = os.path.join(UPLOAD_FOLDER, img)
    img_emb = model.encode(Image.open(img_path))
    search_result = client_qdrant.search(collection_name=collection_name, query_vector=img_emb.tolist(), limit=500)
    
    # search_result=rf.image_text_pipeline_qdrant(np.vstack([img_emb]))
    # search_result=rf.image_text_pipeline_qdrant([img_emb])
    print(search_result)
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