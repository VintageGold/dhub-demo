import streamlit as st
import requests
import pandas as pd
from provider.dataset.aquariusapi import query, get_asset_metadata
import os

# def load_hf_ds():

#     metadata = "https://huggingface.co/datasets/imdb/raw/main/README.md"

#     md =requests.get(metadata)

#     return md

import re
import string

def _get_hits(search_term,data):

    new_string = data.translate(str.maketrans(' ', ' ', string.punctuation))

    return len(re.findall(search_term,new_string))


def metahub_ui(metadata,title):
    cols = 3
    init_tile = 0
    tiles= st.columns(cols)
    for i,data in enumerate(metadata):

            with tiles[init_tile].expander("Dataset",expanded=False):

                if title == "Metahub-Metadata":
                    st.write(title)
                    st.image("https://cryptologos.cc/logos/ocean-protocol-ocean-logo.png?v=023",width=100)
                    st.write("Metadata")
                    st.write(data)

                if title == "Metahub-DDO":
                    st.write(title)
                    st.image("https://cryptologos.cc/logos/ocean-protocol-ocean-logo.png?v=023",width=100)
                    st.write("DDO")
                    st.write(data)


def main():
    st.set_page_config(layout="wide")

    search_field = st.text_input("Search Ocean. Hugging Face and Active Loop will be added soon!",value="glue")

    df_payload,df_source = query(search_field,response_size=21)

    if isinstance(df_source,pd.DataFrame):

        st.write("DIDs from hits found by ES")
        st.write(df_source["id"].to_list())

        metadata = get_asset_metadata(df_source["id"].to_list())

        metahub_ui(metadata,"Metahub-Metadata")

        ddo_data = get_asset_metadata(df_source["id"].to_list())

        metahub_ui(ddo_data,"Metahub-DDO")

    else:
        st.write("No Datasets Returned")

if __name__ == "__main__":

    main()
