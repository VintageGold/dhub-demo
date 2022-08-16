import streamlit as st
import requests
import pandas as pd
from aquariusapi import query, get_asset_metadata
import os

def load_hf_ds():

    metadata = "https://huggingface.co/datasets/imdb/raw/main/README.md"

    md =requests.get(metadata)

    return md

def hf_ui():
    st.title("Hugging Face")
    tiles= st.columns(3)
    for i in range(2):
        for tile in tiles:
            with tile.expander("Data",expanded=False):
                md = load_hf_ds()
                st.markdown(md.text[md.text.find("#"):],unsafe_allow_html=True)


def ocean_ui(metadata):
    st.title("Ocean")
    cols = 3
    init_tile = 0
    tiles= st.columns(cols)
    for i,data in enumerate(metadata):

            if i % cols == 0:
                init_tile = 0

            with tiles[init_tile].expander("Dataset",expanded=False):
                st.image("https://cryptologos.cc/logos/ocean-protocol-ocean-logo.png?v=023",width=100)
                st.write(data)

            init_tile +=1


def main():


    st.set_page_config(layout="wide")

    search_field = st.text_input("Search Ocean. Hugging Face and Active Loop will be added soon!",value="Test")


    df_payload,df_source = query(search_field,response_size=21)

    if isinstance(df_source,pd.DataFrame):

        metadata = get_asset_metadata(df_source["id"].to_list())

        ocean_ui(metadata)
        st.dataframe(df_payload)

    else:
        st.write("No Datasets Returned")





if __name__ == "__main__":

    main()
