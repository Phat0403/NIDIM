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
# client_qdrant.delete_collection(collection_name=collection_name)
create_qdrant(collection_name)


# clip_featurePath = 'D:/newPython/video_frame/clip-features'

# file_clip_feature = os.listdir(clip_featurePath)
# n=len(file_clip_feature)


def convert_name_file(s):
    s = s[0:8]
    return s
def encode_id(id_video,id_frame):
    l, v = id_video.split('_')
    l = int(l[1:])
    v = int(v[1:])
    return (l*32+v)*1000+id_frame
def decode_id(id):
    id_frame = id%1000
    v = int(((id - id_frame)/1000)%32)
    l = int(((id - id_frame)/1000-v)/32)
    return [f'L{l:02}_V{v:03}', id_frame]

file_clip_feature=os.listdir('./clip_h14_fixed')


def upload_data(n):
    for i in range(n):
        points = []
        clip_feature = np.load(f'./clip_h14_fixed/' + file_clip_feature[i])
        video = convert_name_file(file_clip_feature[i])
        sl_frame = clip_feature.shape[0]
        for j in range(sl_frame):
            idx = encode_id(video, j+1)
            vector = clip_feature[int(j)].tolist()
            point = PointStruct(id=int(idx), vector=vector,payload={"adr":idx})
            points.append(point)
        client_qdrant.upsert(collection_name=collection_name, points=points)

upload_data(len(file_clip_feature))
# print(len(file_clip_feature))

