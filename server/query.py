import json
import pandas as pd
import os
import vecQuery as vec
from PIL import Image
from sentence_transformers import SentenceTransformer
#Load CLIP model
import torch
import ocr
# from  

device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)


model = SentenceTransformer('clip-ViT-B-32',device=device)

# def decode_id(id): # Fat
#     id_frame = id%3000
#     v = int(((id - id_frame)/3000)%50)
#     l = int(((id - id_frame)/3000-v)/50)
#     return [f'L{l:02}_V{v:03}', id_frame]

def decode_id(payload):
    return payload['video_id'],payload['keyframe_id']

def getData(video, id):
    with open('./data/media-info-b1/media-info/' + video + '.json', 'r', encoding='utf-8') as file:
            metadata = json.load(file)
            url = metadata["watch_url"]
    df = pd.read_csv('./data/map-key-frames/'+ video + '.csv')
    _, pts_time, fps, frame_idx =df.iloc[int(id)-1]
    return url, pts_time, fps, frame_idx

def searchResult_to_json(search_result):
    result=[] #hit as payload
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

def find_ocr(data):
    text = data[0]
    text = text['value']
    search_result= ocr.find_ocr(text)
    tmp = [result['_source']['frame_id'].split(', ') for result in search_result]
    search_result=[{'video_id':a[0][0],'keyframe_id':a[0][1]} for a in tmp]
    result = searchResult_to_json(search_result)
    # print('This is ocr')
    return result


def find_index(arr, value):
    try:
        return arr.index(value) 
    except ValueError:
        return 1001

def bi_search(arr,x,k):
    curr=list(arr.items())
    l,r=0,len(curr)-1
    mid=int((l+r)/2)
    # print(curr[0][0][0],curr[0][0][1])
    x_v,x_kf=x['video_id'],max(1,x['keyframe_id']-k)
    while mid != l and mid != r:
        m_v,m_kf=curr[mid][0][0],curr[mid][0][1] # lấy vị trí, lấy key, lấy [0]video_id,[1]keyframe_id
        if x_v>m_v or\
           x_v==m_v and x_kf>m_kf:
            l=mid
        else: r=mid
        mid=int((l+r)/2)
    for i in range(l,r+1):
        m_v,m_kf=curr[i][0][0],curr[i][0][1]
        if x_v==m_v and m_kf>=x_kf:
            return i  
    return None

def temporal_merge(curr,nexxt,cnt_scene,span):
    k=4*int(span) 
    adr= list(curr.keys()) # adr là list các key 
    for rank,ele in enumerate(nexxt): 
        idx= bi_search(curr,ele,k) #idx thứ tự của scene[0] có chung video và số thứ tự keyframe nhỏ hơn số thứ tự keyframe của ảnh đang xét
        if idx==None: 
            continue
        key= adr[idx] 
        while ele['keyframe_id']>curr[key]['curr_keyframe'] \
            and ele['keyframe_id'] <= curr[key]['curr_keyframe']+k: # xét xem có cùng bảng tin ko
            if curr[key]['cnt']==cnt_scene-1:
                curr[key]['cnt']=cnt_scene
                curr[key]['score']+=ele['score']*cnt_scene*2/3
                curr[key]['curr_keyframe']=ele['keyframe_id']
            if idx == len(curr)-1: break
            idx+=1
            key=adr[idx]
    return curr
        

def preprocess_text(text):
    text=text.split("\n")
    text= [a for a in text if a != " " and a!= ""]
    return text

def initial(scene):
    res={}
    for i,a in enumerate(scene):
        video_id,keyframe_id=a['video_id'],a['keyframe_id']
    
        res[(video_id,keyframe_id)]={ #cấu trúc phần tử trong ans
            'score':a['score'],
            'curr_keyframe':scene[i]['keyframe_id'],
            'cnt':1,
            'id':a['id'],
        }
    return res
            

def textQuery1(data,rateNum):
    scenes = []
    result = []
    search_result=[]
    data = [a for a in data if a['value']!='']
    count = len(data)
    # print(count)
    for i,_ in enumerate(data):
        text=preprocess_text(data[i].get('value'))
        result = []
        text_embs = model.encode(text)
        search_result=vec.vector_pipeline(text_embs)# search_result có [0]id vector, [1]score, [2]payload
        query = []
        for hit in search_result: 
            video_id, keyframe_id = decode_id(hit[2]) #decode cái payload
            tmp = { #cấu trúc của các phần tử trong scene
                'id':hit[0],
                'video_id':video_id,
                'keyframe_id': keyframe_id,
                'score': hit[1]
            }
            query.append(tmp)
        scenes.append(query)
    scenes[0].sort(key=lambda x: (x['video_id'],x['keyframe_id']))
    ans= initial(scenes[0])
    # Merge các scene
    for i in range(1,count):
        ans = temporal_merge(ans, scenes[i],i+1,rateNum)
    # sort lại theo score
    ans= [
        (key,value)
        for key,value in sorted(ans.items(), key=lambda x: x[1]['score'], reverse=True)
    ]
    #Xuất top 10
    for i in range(10):
        print(f"Top {i+1}: ",ans[i])
    ans=[{'video_id':a[0][0],'keyframe_id':a[0][1]} for a in ans]
    # ans=[a[1]['id'] for a in ans] # Fat
    result=searchResult_to_json(ans)
    return result


UPLOAD_FOLDER = 'uploads/'
def imageQuery():
    result=[]
    img = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))][0]
    img_path = os.path.join(UPLOAD_FOLDER, img)
    img_emb = model.encode(Image.open(img_path).crop((0,0,1280,645))).reshape(1,-1)
    search_result=vec.vector_pipeline(img_emb)
    search_result =[hit[2] for hit in search_result]
    result= searchResult_to_json(search_result)
    if os.path.exists(img_path):
        os.remove(img_path)
        print("File deleted successfully")
    else:
        print("File does not exist")
    return result


def similarQuery(url_img):
    result = []
    img_emb = model.encode(Image.open(url_img).crop((0,0,1280,645))).reshape(1,-1)
    search_result=vec.vector_pipeline(img_emb)
    search_result =[hit[2] for hit in search_result]
    result= searchResult_to_json(search_result)
    for hit in search_result:
        video_frame, id_frame = decode_id(hit.payload)
        data = {
            'video': video_frame, 
            'id': id_frame,
            }
        result.append(data)
    return result


def image_textQuery(data):
    result=[]   
    text = data[0]['value']
    result = []
    text=text.split("\n")
    text= [a for a in text if a != " "]
    text_embs = model.encode(text)
    img = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))][0]
    img_path = os.path.join(UPLOAD_FOLDER, img)
    img_emb = model.encode(Image.open(img_path))
    
    search_result=vec.image_vector_pipeline(img_emb,text_embs)
    # search_result=sorted(search_result,key=lambda x: x[1],reverse=True)
    tmp = [a[2] for a in search_result]
    result= searchResult_to_json(tmp)
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
