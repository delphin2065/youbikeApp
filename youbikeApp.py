import pandas as pd
import numpy as np
import folium
from dataDownload import data
import streamlit as st
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import os
import time



st.header('北市YouBike查詢 App')
st.write('資料來源: YouBike2.0臺北市公共自行車即時資訊, from https://data.gov.tw/dataset/137993')
image_url = os.path.join(os.getcwd(), 'YouBike.png')


dfq = data()
locations = np.unique(dfq['sarea'])
location = st.selectbox('選擇項目', locations)
btn = st.button('資料查詢')





if btn:
    maps = st.empty()
    # texts = st.empty()
    

    dfq = data()
    df = dfq[dfq['sarea']==location].copy()
    df.reset_index(inplace=True, drop=True)
    latitude_mean = df[['latitude']].to_numpy()[:, 0].mean()
    longitude_mean = df[['longitude']].to_numpy()[:, 0].mean()

    # # 繪製中心點
    m = folium.Map(location=[latitude_mean, longitude_mean], zoom_start=16)


    # # 加入標記
    arr = df[['sna', 'sarea', 'ar', 'available_return_bikes', 'updateTime', 'latitude', 'longitude']].to_numpy()

    for i in arr:
        popup_content = f"""
            <div style='width: 200px;'>
            {i[0]} ( {i[2]} )
            <br> 
            <img src='{image_url}' style='width: auto; height: 15px;' alt='youbike'> 
            {i[3]}輛可租用</div>"""
        folium.Marker(
        location = [i[-2], i[-1]], 
        popup = popup_content,
        icon=folium.Icon(color='green') 
        ).add_to(m)

    maps = folium_static(m)

        
    # texts.write(df)
    # time.sleep(10)