import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

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

my_map = folium.Map(location=[35.95, 128.25], zoom_start=6)
police = pd.read_csv('data/출동기관_경찰.csv')
policeposition = {
    '위도': police[['lat']],
    '경도': police[["lon"]],

}
icons_list = ["police"]
for i, row in police.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],

    ).add_to(my_map)
st.title('대한민국 경찰서의 모든 위치입니다.')
st_folium(my_map)
st.page_link("main.py", label='홈으로', icon='🏠')





