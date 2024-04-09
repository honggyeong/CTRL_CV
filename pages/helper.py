import ssl
import pandas as pd
ssl._create_default_https_context = ssl._create_unverified_context
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.map import Icon



st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

container_style = """
    <style>
        .container1 {
            border: 2px solid #3498db;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 20px;
        }
        </style>
"""

lat = st.session_state.lat
lon = st.session_state.lon
st.markdown(container_style, unsafe_allow_html=True)


df = pd.read_csv("https://raw.githubusercontent.com/honggyeong/SAVEME/main/data/emergency.csv")

placeholder = st.empty()

st.dataframe(df)
my_map = folium.Map(location=[lat, lon], zoom_start=6)



for i, row in df.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=row['이름']

    ).add_to(my_map)
with st.container() as container1:
    st.write('도움이 필요한 사용자들의 위치 지도, 원의 반경 = 회원가입 시의 내 위치로부터 50KM')
    folium.Circle([lat, lon], radius=50000,).add_to(my_map)
    st_folium(my_map)





if st.button('홈으로 가기'):
    st.switch_page('main.py')
