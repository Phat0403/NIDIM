import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams

from sentence_transformers import SentenceTransformer, util
from PIL import Image

#Load CLIP model
model = SentenceTransformer('clip-ViT-B-32')
client_qdrant = QdrantClient(host='localhost', port=6333)
# Tạo collection
collection_name = 'clip-feature-2'

def decode_id(id):
    id_frame = id%1000
    v = int(((id - id_frame)/1000)%32)
    l = int(((id - id_frame)/1000-v)/32)
    return [f'L{l:02}_V{v:03}', id_frame]

def textQuery(text):
    result = []
    text_emb = model.encode([text])
    search_result = client_qdrant.search(collection_name=collection_name, query_vector=text_emb.tolist()[0], limit=100)
    for hit in search_result:
        video_frame, id_frame = decode_id(hit.id)
        data = {
            'video': video_frame, 
            'id': id_frame}
        result.append(data)
    return result