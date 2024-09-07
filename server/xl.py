import json
import pandas as pd
def get_link_from_json(file):
    file+=".json"
    path_metadata='C:/Users/LAPTOP/Downloads/media-info-b1/media-info'
    with open(path_metadata+'/'+file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['watch_url']
def get_time(dict):
    path="C:/Users/LAPTOP/Downloads/map-keyframes-b1/map-keyframes"
    file_path = path+'/'+dict['video']+'.csv'
    df = pd.read_csv(file_path)
    row=(df[df['n']==int(dict['id'])])
    return row['pts_time']
def gom_laij(url):
    parts = url.split('/')
    folder_video = parts[-2]
    id_video = parts[-1].replace(".jpg","")
    time=int(get_time({'video':folder_video,'id':id_video}))
    link=get_link_from_json(folder_video)
    return link+'&t='+str(time)
def get_title(url):
    parts = url.split('/')
    folder_video = parts[-2]
    id_video = parts[-1].replace(".jpg","")
    time=int(get_time({'video':folder_video,'id':id_video}))
    return folder_video+" "+str(time)