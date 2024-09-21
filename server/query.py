import numpy as np
import json
import pandas as pd
from qdrant_client import QdrantClient
import os
import rag_fusion as rf
from PIL import Image
from sentence_transformers import SentenceTransformer, util
#Load CLIP model
import torch
# from  

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)
# import open_clip

model = SentenceTransformer('clip-ViT-B-32',device=device)

client_qdrant = QdrantClient(host='localhost', port=6333)
# Tạo collection
collection_name = 'clip-feature-3'



def decode_id(payload):
    return payload['video_id'],payload['keyframe_id']

def getData(video, id):
    with open('./data/media-info-b1/media-info/' + video + '.json', 'r', encoding='utf-8') as file:
            metadata = json.load(file)
            url = metadata["watch_url"]
    df = pd.read_csv('./data/map-keyframes-b1/map-keyframes/'+ video + '.csv')
    _, pts_time, fps, frame_idx =df.iloc[int(id)-1]
    return url, pts_time, fps, frame_idx

def searchResult_to_json(search_result):
    result=[]
    pd_video = []
    pd_frame = []
    for hit in search_result:
        video_id, keyframe_id = decode_id(hit)
        url, pts_time, fps, frame_idx = getData(video_id, keyframe_id)
        # print(video_frame,id_frame)
        data = {
            'video': video_id, 
            'id': keyframe_id,
            'url': url,
            'pts_time': pts_time,
            'frame_idx': frame_idx,
            'fps': fps}
        result.append(data)
        pd_video.append(video_id)
        pd_frame.append(int(frame_idx))
    pd_data = {
        'video': pd_video[0:100],
        'index': pd_frame[0:100]
    }
    df = pd.DataFrame(pd_data)
    df.to_csv('output.csv', index=False)
    return result


def find_index(arr, value):
    try:
        return arr.index(value) 
    except ValueError:
        return 1001
        
def join_arr(arr1, arr2):
    '''
    each element in arr1 and arr2 is a dictionary with two keys: video,id
    arr1 and arr2 are ranked results
    '''
    combined = arr1 + arr2
    unique_elements = {frozenset(item.items()): item for item in combined}
    # print(unique_elements)
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


def join_arr1(curr,nexxt,cnt_scene,rateNum):
    for rank,ele in enumerate(nexxt): 
        video_id=ele['video_id']
        if (cnt_scene>1 and ele < rateNum): continue
        if curr[video_id]['cnt'] == cnt_scene: # có 1 frame giống hơn đã được cập nhật
            #Trường hợp frame_id cái này lớn hơn cái đã cập nhật -> khỏi lấy
            #Trường hợp frame_id cái này nhỏ hơn cái đã cập nhật ? (ưu tiên rank hay độ lớn của frame_id)
            #Đang theo hướng ưu tiên độ lớn của frame_id
            curr[video_id]['curr_keyframe']=min(curr[video_id]['curr_keyframe'],ele['keyframe_id'])
        elif curr[video_id]['curr_keyframe'] is None or ele['keyframe_id'] < curr[video_id]['curr_keyframe']+5 : # xét xem có cùng bảng tin ko
            curr[video_id]['cnt']+=1
            curr[video_id]['score']+= cnt_scene*5/(rank+60)
            curr[video_id]['curr_keyframe']=ele['keyframe_id']
        if cnt_scene==1:
            curr[video_id]['initial_keyframe']=curr[video_id]['curr_keyframe']
    return curr
        

def preprocess_text(text):
    text=text.split("\n")
    text= [a for a in text if a != " " and a!= ""]
    return text

## Code của Phát
# def textQuery1(data):
#     query_more = []
#     result = []
#     count = 0
#     for i,_ in enumerate(data):
#         text = preprocess_text(data[i].get('value'))
#         result = []
#         text_embs = model.encode(text)
#         search_result=rf.rrf_pipeline(text_embs)
#         query = []
#         for hit in search_result:
#             video_frame, id_frame = decode_id(hit)
#             tmp = {
#              'video': video_frame, 
#              'id': id_frame-count
#             }
#             query.append(tmp)
#         query_more.append(query)
#         count += 1
#     ans = query_more[0]
#     for i in range(1,count):
#         ans = join_arr(ans, query_more[i])
#     pd_video = []
#     pd_frame = []
#     for el in ans:
#         video_frame = el['video']
#         id_frame = el['id']
#         url, pts_time, fps, frame_idx = getData(video_frame, id_frame)
#         # print(video_frame,id_frame)
#         data = {
#             'video': video_frame, 
#             'id': id_frame,
#             'url': url,
#             'pts_time': pts_time,
#             'frame_idx': frame_idx,
#             'fps': fps,
#             }
#         result.append(data)
#         pd_video.append(video_frame)
#         pd_frame.append(int(frame_idx))
    
#     pd_data = {
#         'video': pd_video[0:100],
#         'index': pd_frame[0:100]
#     }
#     df = pd.DataFrame(pd_data)
#     df.to_csv('output.csv', index=False)
#     return result[0:1000]
## hết code của Phát

def textQuery1(data,rateNum):
    '''
    Assumming that it is very unlikely to have the same content of a series of scenes in one video
    '''
    scenes = []
    result = []
    count = len(data)
    print(count)
    for i,_ in enumerate(data):
        text=preprocess_text(data[i].get('value'))
        result = []
        text_embs = model.encode(text)
        # print(text_embs.shape)
        search_result=rf.rrf_pipeline(text_embs)# search_result có [0]id vector, [1]score, [2]payload
        query = []
        for hit in search_result: 
            video_id, keyframe_id = decode_id(hit[2]) #decode cái payload
            tmp = {
                'video_id':video_id,
                'keyframe_id': keyframe_id,
                'score': hit[1]
            }
            query.append(tmp)
        scenes.append(query)
    
    names= os.listdir('./data/clip-features') # để lấy tên file
    ans={}
    for name in names:
        name=name.split('.')[0] # Chỉ lấy phần L01_V001
        ans[name]={
            'video_id':name,
            'initial_keyframe':None,
            'curr_keyframe':None,
            'cnt':0,
            'score':0
        }
    for i in range(count):
        ans = join_arr1(ans, scenes[i],i+1,rateNum)
    # for name in ans.keys():
    #     print(ans[name]['initial_keyframe'])
    ans= [
        value
        for _,value in sorted(ans.items(), key=lambda x: x[1]['score'], reverse=True) if value['initial_keyframe']!=None
    ]
    pd_video = []
    pd_frame = []
    for el in ans: 
        video_id = el['video_id']
        keyframe_id = el['initial_keyframe']
        url, pts_time, fps, frame_idx = getData(video_id, keyframe_id)
        # print(video_frame,id_frame)
        data = {
            'video': video_id, 
            'id': keyframe_id,
            'url': url,
            'pts_time': pts_time,
            'frame_idx': frame_idx,
            'fps': fps, 
            }
        result.append(data)
        pd_video.append(video_id)
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
    print('imageQuery')
    result=[]
    img = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))][0]
    img_path = os.path.join(UPLOAD_FOLDER, img)
    img_emb = model.encode(Image.open(img_path))
    # print(len(img_emb.tolist()))
    search_result=rf.rrf_pipeline(img_emb)
    search_result =[hit.id for hit in search_result]
    result= searchResult_to_json(search_result)
    if os.path.exists(img_path):
        os.remove(img_path)
        print("File deleted successfully")
    else:
        print("File does not exist")
    return result


def similarQuery(url_img):
    result = []
    img_emb = model.encode(Image.open(url_img))
    search_result = client_qdrant.search(collection_name=collection_name,
                                        query_vector=img_emb.tolist(),
                                        with_payload=True,
                                        limit=200)
    for hit in search_result:
        video_frame, id_frame = decode_id(hit.payload)
        data = {
            'video': video_frame, 
            'id': id_frame,
            }
        result.append(data)
    return result


def image_textQuery(data):
    # print('image_textQuery')
    result=[]   
    text = data[0]['value']
    result = []
    text=text.split("\n")
    text= [a for a in text if a != " "]
    text_embs = model.encode(text)
    img = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))][0]
    img_path = os.path.join(UPLOAD_FOLDER, img)
    img_emb = model.encode(Image.open(img_path))
    # print(img_emb.shape,123)
    # search_result = client_qdrant.search(collection_name=collection_name, query_vector=img_emb.tolist(), limit=500)
    
    search_result=rf.image_text_pipeline(img_emb,text_embs)
    result= searchResult_to_json(search_result)
    if os.path.exists(img_path):
        os.remove(img_path)
        print("File deleted successfully")
    else:
        print("File does not exist")
    return result

# if __name__ == '__main__':
#     seed= np.random.default_rng(42)
#     vec1,vec2={},{}
#     vec1['value']="dog"
#     vec2['value']="cat"
#     a = []
#     a.extend([vec1,vec2])
#     # print(a[0]['value'].shape)
#     print(textQuery1(a))
