from elasticsearch import Elasticsearch
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

username = 'elastic'
password = 'uH2*KwJ9HqdAq7-SRaR6'

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=(username, password),
    ca_certs=False,
    verify_certs=False
)

index_name = 'aic_ocr'

def fuzzy_search(query, max_results=20): 
    response = es.search(
        index=index_name,
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


def search_all(max_results=1000):
    response = es.search(
        index=index_name,
        body={
            "query": {
                "match_all": {}
            },
            "size": max_results
        }
    )
    return response['hits']['hits']


if __name__ == '__main__':
    query = "Đậu mùa khỉ"  
    results = fuzzy_search(query)
    # results = search_all()
    for result in results:
        print(result['_source']['frame_id'], "| Score:", result['_score'])
