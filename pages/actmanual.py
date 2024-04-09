

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

act = st.session_state.sit
st.title('행동강령')

st.write('접수 신청이 완료되었습니다. 신고 등록은 약 5분정도 소요됩니다.')


if act ==1:
    st.title('현재 납치 상황으로 신고가 접수되었습니다.')
    st.write('납치를 당하였을 때는 가장 먼저 침착하는 것이 중요합니다. 용의자의 인상착의 등을 기억해놓으십시오. ')
elif act ==2:
    st.title('현재 화재 상황으로 신고가 접수되었습니다.')
    st.write('화재가 났을 때는 119에 신고하고 작은 불은 소화기로 끄십시오. 소화기로 진압되지 않는 불일 경우 대피하십시오.')
elif act ==3:
    st.title('현재 부상 상황으로 신고가 접수되었습니다.')
    st.write('부상을 당하였을 때는 움직이지 마시고 가만히 계십시오. 119에 전화를 하고 긴급처치가 가능한 경우 긴급처치를 하십시오.')
elif act ==4:
    st.title('현재 기타 상황으로 신고가 접수되었습니다.')
    st.write(' 필요한 도움이 무엇인지 정리해놓으시고, 다른 앱 사용자에게 도움의 전화가 오면 자세히 상황을 설명해주십시오. ')

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
st.title('주변 경찰서의 위치입니다. 확인해보시기 바랍니다. ')
st_folium(my_map)
st.page_link("main.py", label='홈으로', icon='🏠')




