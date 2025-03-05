import requests as re
import json
import pandas as pd
import numpy as np
import streamlit as st

st.cache_data(ttl=30)
def data():
    url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
    res_j = re.get(url)
    res = json.loads(res_j.text)
    dfq = pd.DataFrame(res)
    dfq['sna'] = dfq['sna'].str.split('_').str[-1]
    return dfq


