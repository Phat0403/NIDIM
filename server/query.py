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
    return result

UPLOAD_FOLDER = 'uploads/'
def imageQuery():
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


def ocrQuery(ocr):
    text = ocr[0]
    text = text['value']
    result = db.findOcr(text)
    return result
