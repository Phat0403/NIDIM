import os
import database as db
from sentence_transformers import SentenceTransformer, util
from PIL import Image


#Load CLIP model
model = SentenceTransformer('clip-ViT-B-32')



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
    text = data[0]
    text = text['value']
    text_emb = model.encode(text)
    result = db.find_vector(text_emb)
    
    # query_more = []
    # result = []
    # count = 0
    # for i,_ in enumerate(data):
    #     text = preprocess_text(data[i].get('value'))
    #     result = []
    #     text_embs = model.encode(text)
    #     search_result=rf.rrf_pipeline(text_embs)
    #     query = []
    #     for hit in search_result:
    #         video_frame, id_frame = decode_id(hit)
    #         tmp = {
    #          'video': video_frame, 
    #          'id': id_frame-count
    #         }
    #         query.append(tmp)
    #     query_more.append(query)
    #     count += 1
    # ans = query_more[0]
    # for i in range(1,count):
    #     ans = join_arr(ans, query_more[i])
    # pd_video = []
    # pd_frame = []
    # for el in ans:
    #     video_frame = el['video']
    #     id_frame = el['id']
    #     url, pts_time, fps, frame_idx = getData(video_frame, id_frame)
    #     # print(video_frame,id_frame)
    #     data = {
    #         'video': video_frame, 
    #         'id': id_frame,
    #         'url': url,
    #         'pts_time': pts_time,
    #         'frame_idx': frame_idx,
    #         'fps': fps,
    #         }
    #     result.append(data)
    #     pd_video.append(video_frame)
    #     pd_frame.append(int(frame_idx))
    
    # pd_data = {
    #     'video': pd_video[0:100],
    #     'index': pd_frame[0:100]
    # }
    # df = pd.DataFrame(pd_data)
    # df.to_csv('output.csv', index=False)
    return result



UPLOAD_FOLDER = 'uploads/'
def imageQuery():
    # print('imageQuery')
    result=[]
    img = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))][0]
    img_path = os.path.join(UPLOAD_FOLDER, img)
    img = Image.open(img_path).resize((1280, 720)).crop((0,0,1280,645))
    img_emb = model.encode(img)
    result = db.find_vector(img_emb)
    
    if os.path.exists(img_path):
        os.remove(img_path)
        print("File deleted successfully")
    else:
        print("File does not exist")
    return result


def similarQuery(url_img):
    result = []
    local_file_path = 'C:/Users/tanph/OneDrive/Desktop/NIDIM/server/uploads'
    command = f"gsutil -m cp -r {url_img} {local_file_path}"
    exit_code = os.system(command)
    if exit_code == 0:
        print("File download successfully!")
    else:
        print(f"An error occurred. Exit code: {exit_code}")
    img = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))][0]
    img_path = os.path.join(UPLOAD_FOLDER, img)
    img = Image.open(img_path).resize((1280, 720)).crop((0,0,1280,645))
    img_emb = model.encode(img)
    result = db.find_vector(img_emb)
    
    if os.path.exists(img_path):
        os.remove(img_path)
        print("File deleted successfully")
    else:
        print("File does not exist")
    return result


