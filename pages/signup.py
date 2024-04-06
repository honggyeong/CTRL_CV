import folium
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import pandas as pd
from git import repo


df = pd.read_csv("https://raw.githubusercontent.com/honggyeong/data/main/data/users.csv")
df
st.title("회원가입")

st.write('정보를 입력해주세요')

with st.container():
    name = st.text_input('이름')
with st.container():
    number = st.text_input('전화번호')
with st.container():
    age = st.slider('나이?', 0, 130, 25)
with st.container():
    sex = st.selectbox(
       '성별을 선택하세요',
       ('남', '여', '알수없음'))


if st.button('입력완료'):
    df2 = pd.DataFrame({'이름': [name], '전화번호':[number], '나이':[age], '성별':[sex]})
    new_df = df._append(df2, ignore_index=True)
    df = new_df
    df


