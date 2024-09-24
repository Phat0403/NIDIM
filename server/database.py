import numpy as np
import json
import pandas as pd
import os 
from qdrant_client import QdrantClient
from qdrant_client import models

import os

client_qdrant = QdrantClient(host='localhost', port=6333, timeout=60)
collection_name = 'clip-feature-4'

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