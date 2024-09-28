import numpy as np
import pandas as pd
import os 
from qdrant_client import QdrantClient
from qdrant_client import models
import json

import os

client_qdrant = QdrantClient(host='localhost', port=6333)
collection_name = 'clip-feature-3'
mapp={} #id->video
stt=[0,] #xác định xem frame đó ở video thứ mấy rồi sử dụng mapp để lấy ra địa chỉ video


def rrf(results: list[list], k=60):
    """ 
    Reciprocal_rank_fusion that takes multiple lists of ranked documents 
    and an optional parameter k used in the RRF formula 
    results: I[0] from faiss result    
    idx[0] is the id of the result
    """
    fused_scores = {}
    for result in results: # res1,res2,res...
        for rank,idx in enumerate(result):
            if idx not in fused_scores.keys():
                fused_scores[idx] = 0
            fused_scores[idx] += 1/(rank + k)
    reranked_results = [
        (doc,score)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True) # sort theo score
    ]
    return reranked_results # (id,score)


def vector_pipeline(embs,qfilter=None):
    rrf_input=[]
    mapp={}
    search_result=None
    for i in range(embs.shape[0]): ## rag_fusion
        emb=embs[i]
        # print(text_emb.tolist())
        search_result = client_qdrant.search(
            collection_name=collection_name,
            query_vector=emb.tolist(),
            query_filter= qfilter,
            with_payload=True,
            limit=500)
        rrf_input.append([hit.id for hit in search_result])
        for hit in search_result: ## khúc này để lưu lại score, lấy score trung bình nếu kết quả đó xuất hiện nhiều lần, do query nhiều lần
            tmp=hit.payload if len(hit.payload.keys()) else hit.id
            if hit.id not in mapp.keys():
                mapp[hit.id]=[0,tmp]
    res=rrf(rrf_input)
    tmp=[(a[0],a[1],mapp[a[0]][1]) for a in res] #a chỉ đơn giản là id, cái giữa là mean score, cái còn lại là payload
    res = tmp
    return res

def image_text_pipeline(img_emb,text_embs):
    '''
    input: image embed and a bunch of text embeds
    output: result from image_text query
    '''
    k=500
    curr=[]
    res=None
    img_search=client_qdrant.search(
        collection_name=collection_name,
        query_vector=img_emb.flatten().tolist(),
        limit=500,
    )
    curr= [hit.id for hit in img_search]
    qfilter = models.Filter(
        must=[
            models.FieldCondition(
                key='adr',
                match=models.MatchAny(any=curr),
            ),
        ]
    )
    res= vector_pipeline(text_embs,qfilter)
    return res


# from pprint import pprint
# if __name__=="__main__":
#     seed= np.random.default_rng(42)
#     a=seed.random((2,512))
#     c=seed.random((1,512))
#     b=image_text_pipeline(c,a)
#     pprint(b)
