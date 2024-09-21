import numpy as np
import pandas as pd
import os 
from qdrant_client import QdrantClient
from qdrant_client import models

import os

client_qdrant = QdrantClient(host='localhost', port=6333)
collection_name = 'clip-feature-3'
mapp={} #id->video
stt=[0,] #xác định xem frame đó ở video thứ mấy rồi sử dụng mapp để lấy ra địa chỉ video

# def normalize(embeds):
#     return embeds/ np.linalg.norm(embeds,axis=1,keepdims=True)

def rrf(results: list[list], k=60):
    """ 
    Reciprocal_rank_fusion that takes multiple lists of ranked documents 
    and an optional parameter k used in the RRF formula 
    results: I[0] from faiss result    
    idx[0] is the id of the result
    """
    fused_scores = {}
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




def get_points(points):
    '''
        input: json from qdrant.search
    '''
    res=[]
    for p in points['result']:
        res.append((p['id'],p['payload'],p['vector']))
    return res



def rrf_pipeline(embs,qfilter=None):
    rrf_input=[]
    mapp={}
    for i in range(embs.shape[0]): ## rag_fusion
        emb=embs[i]
        # print(text_emb.tolist())
        search_result = client_qdrant.search(
            collection_name=collection_name,
            query_vector=emb.tolist(),
            query_filter= qfilter,
            limit=200)
        rrf_input.append([hit.id for hit in search_result])
        for hit in search_result:
            if hit.id not in mapp.keys():
                mapp[hit.id]=hit.score
            mapp[hit.id]= (mapp[hit.id]+hit.score)/2
    res=rrf(rrf_input)
    res=[(a,mapp[a]) for a in res]
    return  res


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
    res= rrf_pipeline(text_embs,qfilter)
    return res


# from pprint import pprint
# if __name__=="__main__":
#     seed= np.random.default_rng(42)
#     a=seed.random((2,512))
#     c=seed.random((1,512))
#     b=image_text_pipeline(c,a)
#     pprint(b)
