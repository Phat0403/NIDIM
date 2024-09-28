import json
import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams
from qdrant_client import models

import os

client_qdrant = QdrantClient(host='localhost', port=6333)

# Tạo collection
collection_name = 'clip-feature-3'

def create_qdrant(collection_name):
    client_qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=512, distance="Cosine") # Cung cấp cấu hình vector
    )

def convert_name_file(s):
    s = s[0:8]
    return s
def encode_id(id_video,id_frame):
    l, v = id_video.split('_')
    l = int(l[1:])
    v = int(v[1:])
    return (l*32+v)*1000+id_frame

def decode_id(res):
    return res['video_id'],res['keyframe_id']




def upload_data(n=None):
    cnt=0
    file_clip_feature=os.listdir('./data/clip-features')
    n=len(file_clip_feature)
    # print(n)
    for i in range(n):
        points = []
        clip_feature = np.load(f'./data/clip-features/' + file_clip_feature[i])
        video = convert_name_file(file_clip_feature[i])
        sl_frame = clip_feature.shape[0]
        for j in range(sl_frame):
            idx = cnt
            # print(idx)
            cnt+=1
            vector = clip_feature[int(j)].tolist()
            # print(video,j)
            point = PointStruct(id=int(idx), vector=vector,payload={
                "adr":idx,
                'video_id':video,
                "keyframe_id":j+1,
            })
            points.append(point)
        client_qdrant.upsert(collection_name=collection_name, points=points)


if __name__=="__main__":
    print(client_qdrant.get_collection(collection_name=collection_name))
    # client_qdrant.update_collection(
    # collection_name=collection_name,
    #     hnsw_config=models.HnswConfigDiff(
    #         m=36,
    #         ef_construct=250, 
    #     )
    # )
    # while True:
    #     collection_info = client_qdrant.get_collection(collection_name=collection_name)
    #     if collection_info.status == models.CollectionStatus.GREEN:
    #         # Collection status is green, which means the indexing is finished
    #         break
