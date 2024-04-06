import folium
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
from git import repo
import pandas as pd

df = pd.read_csv("users/유저.csv")

st.dataframe(df)

st.title('구해줘용 (KOREA No.1  SAFETY)')
st.title('정보를 입력해주세요')
with st.container():
    name = st.text_input('이름')







st.page_link('main.py', label= "입력완료")

