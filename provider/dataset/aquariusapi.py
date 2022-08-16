import requests
import pandas as pd

def query(search_term:str,
        response_size:int=5
):
    base_url = "https://v4.aquarius.oceanprotocol.com/api/aquarius/assets/"
    endpoint = 'query'
    link = base_url + endpoint


    query = {"from":0,"size":response_size,"query":{"bool":{"must":[{"bool":{"should":
                                                      [{"query_string":{"query":search_term,"fields":["id","nft.owner","datatokens.address","datatokens.name"
                                                      ,"datatokens.symbol","metadata.name^10",
                                                      "metadata.author","metadata.description","metadata.tags"],
                                                                        "minimum_should_match":"2<75%","phrase_slop":2,"boost":5}},


                                                       {"query_string":{"query":f"{search_term}*","fields":["id","nft.owner","datatokens.address","datatokens.name","datatokens.symbol",
                                                                        "metadata.name^10","metadata.author","metadata.description","metadata.tags"],"boost":5,"lenient":True}},{"match_phrase":{"content":{"query":"Testing","boost":10}}},




                                                       {"query_string":{"query":f"*{search_term}*","fields":["id","nft.owner","datatokens.address","datatokens.name","datatokens.symbol","metadata.name^10","metadata.author","metadata.description",
                                                                                                      "metadata.tags"],"default_operator":"AND"}}]}}],"filter":[{"terms":{"chainId":[4]}},{"term":{"_index":"aquarius"}},
                                                                                                      {"term":{"purgatory.state":False}}]}},"sort":{"_score":"desc"}}

    response = requests.post(link,json=query)

    if len(response.json()["hits"]["hits"]) > 0:

        df_payload = pd.DataFrame(response.json()["hits"]["hits"])

        df_source = pd.json_normalize(df_payload["_source"])

        return df_payload,df_source

    else:
        return None,None


def get_asset_metadata(dids:list):

    base_url = "https://v4.aquarius.oceanprotocol.com/api/aquarius/assets/"


    metadata_list = list()

    for did in dids:

        endpoint = f'metadata/{did}'
        query = base_url+endpoint
        response = requests.get(query)

        metadata_list.append(response.json())

    return metadata_list
