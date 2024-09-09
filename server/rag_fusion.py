import faiss
import numpy as np
import pandas as pd
import os 
from bisect import bisect_left
from qdrant_client import QdrantClient
from qdrant_client import models

import os

client_qdrant = QdrantClient(host='localhost', port=6333)

mapp={} #id->video
stt=[0,] #xác định xem frame đó ở video thứ mấy rồi sử dụng mapp để lấy ra địa chỉ video

# def normalize(embeds):
#     return embeds/ np.linalg.norm(embeds,axis=1,keepdims=True)

def data_init():
    index = faiss.IndexFlatIP(512)
    file_path= './data'
    file_clip_features=file_path+'/'+'clip-features'
    # file_clip_features= file_path+'/'+'clip-features-32-b1'+'/'+'clip-features-32'
    clip_features = os.listdir(file_clip_features)
    for i in range(len(clip_features)):
        data=np.load(file_clip_features+'/'+clip_features[i])
        stt.append(stt[i]+data.shape[0]) #số vector trong L01_V001
        tmp=clip_features[i].split('.')[0]
        mapp[i]=tmp
        faiss.normalize_L2(data)
        index.add(data)
    return index

def data_altering(ids):
    embeddings= index.reconstruct(*ids)
    index = faiss.IndexFlatIP(512)
    index.add_with_ids(embeddings,ids)
    return index

def rrf(results: list[list], k=60):
    """ 
    Reciprocal_rank_fusion that takes multiple lists of ranked documents 
    and an optional parameter k used in the RRF formula 
    results: I[0] from faiss result    
    """
    fused_scores = {}
    # print(1234566)
    for result in results:
        for rank,idx in enumerate(result):
            if idx not in fused_scores.keys():
                fused_scores[idx] = 0
            fused_scores[idx] += 1/(rank + k)
    reranked_results = [
        doc
        for doc, _ in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]
    return reranked_results

def findd(embed,index,k=50):
    faiss.normalize_L2(embed)
    _,I= index.search(embed,k)
    return I[0]


def BinarySearch(a, xs):
    i = [bisect_left(a, x) for x in xs]
    res = [y-1 if y else -1 for y in i]
    return res

def to_address(idx):
    # print(idx)
    pos= BinarySearch(stt,idx)
    # print(pos)
    k=[(i-stt[po]).item() for i,po in zip(idx,pos)]
    # # print(mapp[pos]+'/'+f'{k:03}'+'.jpg')
    videos= [mapp[po] for po in pos]
    return videos,k

index=data_init()

def rrf_pipeline(embeds):
    results=[]
    for i in range(embeds.shape[0]):
        results.append(findd(embeds[i].reshape(1,-1),index))
    return rrf(results)
    
def image_text_pipeline(embeds):
    tmp=data_init()
    for embed in embeds:
        result= findd(embed,tmp)
        tmp= data_altering(result)
    return result

def get_points(points):
    '''
        input: json from qdrant.search
    '''
    res=[]
    for p in points['result']:
        res.append((p['id'],p['payload'],p['vector']))
    return res

collection_name = 'clip-feature-3'


def image_text_pipeline_qdrant(embeds):
    # print(embeds[0].shape,embeds[1].shape)
    k=500
    curr=[]
    res=None
    for i in range(embeds.shape[0]):
        embed=embeds[i]
        query_filter = None
        if curr:
            query_filter = models.Filter(
                should=[
                    models.FieldCondition(
                        key='adr',
                        match=models.MatchAny(any=curr),
                    ),
                ]
            )
        # print(type(query_filter))
        res= client_qdrant.search(
            collection_name=collection_name,
            query_vector= embed.tolist(),
            limit=k,
            with_payload=True,
            query_filter=query_filter
        )
        k=max(100,k-75)
        curr.extend([b.payload['adr'] for b in res])
        print(curr)
    return res

# from pprint import pprint
# if __name__=="__main__":
#     seed= np.random.default_rng(42)
#     a=seed.random((2,512))
#     b=image_text_pipeline_qdrant(a)
#     pprint(b)
    # for aa in b:
    #     print(aa.payload['adr'])
    # pprint(client_qdrant.get_collection(collection_name=collection_name))
    # pprint(client_qdrant.retrieve(collection_name=collection_name,ids=[235113]))
    # print(b)
