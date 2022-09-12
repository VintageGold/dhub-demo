import requests
import pandas as pd
import streamlit as st

def query(search_term:str,
        response_size:int=5,
        chain_id:int=4
):
    base_url = "https://aquarius.algovera.ai/api/aquarius/assets/"
    endpoint = 'query'
    link = base_url + endpoint

    #simple query
    query = {"from":0,"size":response_size,"query":{"bool":{"must":[{"bool":{"should":
                                                      [{"query_string":{"query":search_term,"fields":["id","metadata.name"],
                                                                        "minimum_should_match":"2<75%","phrase_slop":2,"boost":5}}]}}]}}}

                                                       #
                                                       # {"query_string":{"query":f"{search_term}*","fields":["id","metadata.name"],"boost":5,"lenient":True}},{"match_phrase":{"content":{"query":"Testing","boost":10}}},
                                                       #
                                                       #
                                                       #
                                                       #
                                                       # {"query_string":{"query":f"*{search_term}*","fields":["id","metadata.name"],"default_operator":"AND"}}]}}],"filter":[{"terms":{"chainId":[chain_id]}},{"term":{"_index":"aquarius"}},
                                                       #                                                {"term":{"purgatory.state":False}}]}},"sort":{"_score":"desc"}}

    response = requests.post(link,json=query)

    if len(response.json()["hits"]["hits"]) > 0:

        df_payload = pd.DataFrame(response.json()["hits"]["hits"])

        df_source = pd.json_normalize(df_payload["_source"])

        return df_payload,df_source

    else:
        return None,None


def get_asset_metadata(dids:list):

    base_url = "https://aquarius.algovera.ai/api/aquarius/assets/"


    metadata_list = list()

    for did in dids:

        endpoint = f'metadata/{did}'
        query = base_url+endpoint
        response = requests.get(query)

        metadata_list.append(response.json())

    return metadata_list


def get_asset_ddo(dids:list):

    base_url = "https://aquarius.algovera.ai/api/aquarius/assets/"


    metadata_list = list()

    for did in dids:

        endpoint = f'ddo/{did}'
        query = base_url+endpoint
        response = requests.get(query)

        metadata_list.append(response.json())

    return metadata_list
