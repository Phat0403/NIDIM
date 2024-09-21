import json
import numpy as np
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams

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
                "keyframe_id":j,
            })
            points.append(point)
        client_qdrant.upsert(collection_name=collection_name, points=points)


if __name__=="__main__":
    from pprint import pprint
    client_qdrant.delete_collection(collection_name=collection_name)
    create_qdrant(collection_name) 
    upload_data()
    # res= client_qdrant.search(collection_name=collection_name,
    #                      query_vector=np.random.rand(512).tolist(),
    #                      limit=2,
    #                      with_payload=True)
    # for a in res:
    #     print(a.payload['video_id'],a.payload['keyframe_id'])
        