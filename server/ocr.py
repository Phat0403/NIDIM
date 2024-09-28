
from elasticsearch import Elasticsearch
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = 'elastic'
password = 'Mn*mMi=L2ceq+oEC4Ovm'#'-LMpeY1XX13uwH95CuWP' # Dien password vao day

es = Elasticsearch(
    "https://104.214.176.14:9200",
    basic_auth=(username, password),
    ca_certs=False,
    verify_certs=False
)
##########################################################################################################################################

##########################################################################################################################################
def find_ocr(query, max_results=1000): 
    if es.indices.exists(index='aic_ocr'):
        print('co')
    else:
        print('khong')
    response = es.search(
        index='aic_ocr',
        body={
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "text": {
                                    "query": query,
                                    "fuzziness": "AUTO",  
                                    "operator": "or"  
                                }
                            }
                        }
                    ],
                    "minimum_should_match": 1  
                }
            },
            "size": max_results,
            "sort": [
                {
                    "_score": {
                        "order": "desc"  
                    }
                }
            ]
        }
    )
    return response['hits']['hits']

##########################################################################################################################################
