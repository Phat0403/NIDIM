from pymongo import MongoClient
import json
import numpy as np
import pandas as pd
import os

map_keyframePath = 'D:/newPython/video_frame/map-keyframes-b1/map-keyframes'
metadataPath = 'D:/newPython/video_frame/media-info-b1/media-info'

file_map_keyframe = os.listdir(map_keyframePath)
file_metadata = os.listdir(metadataPath)
n = len(file_map_keyframe)


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
# # Kết nối tới MongoDB
client = MongoClient('mongodb://root:123456@localhost:27018/')
db = client.NIDIM
collection = db.data



def upload_data(n):
    for i in range(n):
        with open('./media-info-b1/media-info/' + file_metadata[i], 'r', encoding='utf-8') as file:
            metadata = json.load(file)
            url = metadata["watch_url"]
        df = pd.read_csv('./map-keyframes-b1/map-keyframes/'+ file_map_keyframe[i])
        video = convert_name_file(file_metadata[i])
        sl_frame = df.shape[0]
        frames = []
        for j in range(sl_frame):
            n, pts_time, fps, frame_idx =df.iloc[j]
            frame = {
                "id": int(n),
                "pts_time": pts_time,
                "fps": fps,
                "frame_idx": frame_idx,
            }
            frames.append(frame)
        document = {
            "_id": video,
            "url": url,
            "sl_frame": sl_frame,
            "frames": frames
        }
        collection.insert_one(document)
# upload_data(n)













document = collection.find_one({"_id": "L01_V001"})
id, pts_time, fps, frame_idx = document['frames'][int(100)-1]
print(frame_idx)

