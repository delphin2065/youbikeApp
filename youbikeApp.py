import pandas as pd
import numpy as np
import folium
from dataDownload import data
import streamlit as st
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import os
import time

import datetime as dt
import pytz
tz = pytz.timezone('Asia/Taipei')

st.header('北市YouBike查詢 App')
st.write('資料來源: YouBike2.0臺北市公共自行車即時資訊(每分鐘更新一次), from https://data.gov.tw/dataset/137993')



# 初始化 session state
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'selected_location' not in st.session_state:
    st.session_state.selected_location = None

dfq = data()
locations = np.unique(dfq['sarea'])
location = st.selectbox('選擇項目', locations)

btn = st.button('資料查詢')

# 處理按鈕點擊
if btn:
    st.session_state.auto_refresh = True
    st.session_state.selected_location = location

# 顯示資料和地圖
if st.session_state.auto_refresh:
    location_to_show = st.session_state.selected_location
    
    # 抓取最新資料
    dfq = data()
    df = dfq[dfq['sarea'] == location_to_show].copy()
    df.reset_index(inplace=True, drop=True)
    
    # 顯示更新時間
    st.info(f"🔄 自動更新中... 最後更新: {dt.datetime.now(tz).strftime('%H:%M:%S')}")
    
    
    
    # 計算中心點
    latitude_mean = df['latitude'].mean()
    longitude_mean = df['longitude'].mean()
    
    # 繪製地圖
    m = folium.Map(location=[latitude_mean, longitude_mean], zoom_start=16)
    
    # 加入標記
    arr = df[['sna', 'sarea', 'ar', 'available_return_bikes', 'updateTime', 'latitude', 'longitude']].to_numpy()
    
    for i in arr:
        popup_content = f"""
            <div style='width: 250px;'>
            {i[0]} ( {i[2]} )
            <br>
            <i class="fa-solid fa-bicycle"></i> 
            {i[3]}輛可租用, {i[4]}</div>"""
        folium.Marker(
            location=[i[-2], i[-1]], 
            popup=popup_content,
            icon=folium.Icon(color='green') 
        ).add_to(m)
    
    # folium_static(m)
    st_folium(m, width=None, height=400, use_container_width=True)
    # 每60秒自動更新
    time.sleep(60)
    st.rerun()