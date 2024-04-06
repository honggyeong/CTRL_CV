import folium
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_folium import st_folium

st.set_page_config(
    page_title='구해줘용',
    page_icon='🚓')
def needer():
    st.title('도움받기')

    with st.container():
        # Starting variables
        center = [35.95, 128.25]
        zoom = 6
        use_time = False
        colormap = plt.cm.YlOrRd
        padding_geo_factor = 1 / 111111
        interpolation_algo_dict = {
            'idw': 'Inverse Distance Weighting (IDW)',
            'tin': 'Triangular Irregular Network (TIN)'
        }
        is_extended_graph = True

        # State variables
        if 'center' not in st.session_state:
            st.session_state.center = center

        if 'source' not in st.session_state:
            st.session_state.source = center

        if 'zoom' not in st.session_state:
            st.session_state.zoom = zoom

        if "cost_type" not in st.session_state:
            st.session_state.cost_type = 'distance'

        # Map
        m = folium.Map(location=center, zoom_start=zoom)

        with st.form("map_form"):

            # Map Controls
            st.subheader('위치 선택')
            st.caption('지도를 움직여 위치를 바꿔주세요')

            # Create the map
            with st.container():

                # When the user pans the map ...
                map_state_change = st_folium(
                    m,
                    key="new",
                    height=300,
                    width='100%',
                    returned_objects=['center', 'zoom'],
                )

                st.write('⌖')

                if 'center' in map_state_change:
                    st.session_state.center = [map_state_change['center']['lat'], map_state_change['center']['lng']]

                if 'zoom' in map_state_change:
                    st.session_state.zoom = map_state_change['zoom']

            with st.container():
                col1, col2 = st.columns([2, 1])

                with col1:
                    dec = 10
                    st.write(round(st.session_state.center[0], dec), ', ', round(st.session_state.center[1], dec))

                with col2:
                    submitted = st.form_submit_button("Set location")
                    if submitted:
                        st.session_state.source = st.session_state.center
                        st.title('입력되었습니다')


def helper():

    st.map()






def login():
    st.title('구해줘용 (No.1 KOREA SAFETY)')
    st.title('정보를 입력해주세요')

    container = st.container(border=True)
    name = container.text_input('이름')

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


    if st.button("입력 완료"):
        if st.button('니더(도움받기)'):
            needer()
        if st.button('헬퍼(도와주기)'):
            helper()


def main():
    st.title("구해줘용")
    st.write('No.1 korea safety app.')
    if st.button('로그인하기'):
        login()






main()



