import pandas as pd
import ssl

import firebase_admin
import folium
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from firebase_admin import credentials
from firebase_admin import db
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation


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



if st.button('홈으로 가기'):
    st.switch_page('main.py')


def initialize_firebase_report():
    try:
        # 이미 초기화된 앱이 있는지 확인
        app = firebase_admin.get_app()
    except ValueError:
        # 앱이 초기화되지 않았다면 초기화
        cred = credentials.Certificate(st.secrets["repo_cert"])
        firebase_admin.initialize_app(cred, {
            'databaseURL': st.secrets["repo_url"]
        })

    return firebase_admin.get_app()

app2 = initialize_firebase_report()

# 데이터 저장 함수
def save_report(name, lat, lon, type):
    ref_report.child("{}".format(name)).set({
        'name': name,
        'latitude': lat,
        'longitude': lon,
        'type': type
    })
    print(f"Report saved for {name}")

# 데이터베이스 레퍼런스 가져오기
ref_report = db.reference('reports', app=app2) # 'reports'는 데이터를 저장할 노드 이름입니다.
ref_repo = db.reference('repo', app=app2) # 'reports'는 데이터를 저장할 노드 이름입니다.

def save_repo(name, lat, lon, type):
    ref_repo.child("users").set({
        'name': name,
        'latitude': lat,
        'longitude': lon,
        'type': type
    })
    print(f"Report saved for {name}")







ssl._create_default_https_context = ssl._create_unverified_context
mydata = st.checkbox('회원가입시 작성한 나의 위치 사용하기')
geo = st.checkbox("나의 GPS위치 정보 사용하기")
nam = st.session_state["name"]
if mydata:
    lon = st.session_state.my_lon
    lat = st.session_state.my_lat
    st.write(lat,lon)

    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("납치🚓"):
                uni = '납치'
                save_report(nam,lat,lon,uni)
                save_repo(nam, lat, lon, uni)
                st.switch_page("pages/actmanual.py")
            if st.button("화재🔥"):
                uni = '화재'
                save_report(nam, lat, lon, uni)
                save_repo(nam, lat, lon, uni)
                st.switch_page("pages/actmanual.py")
        with col2:
            if st.button("부상🚑"):
                uni = '부상'
                save_report(nam, lat, lon, uni)
                save_repo(nam, lat, lon, uni)
                st.switch_page("pages/actmanual.py")
            if st.button("기타➕"):
                uni = '기타'
                save_report(nam, lat, lon, uni)
                save_repo(nam, lat, lon, uni)
                st.switch_page("pages/actmanual.py")

elif geo:


    location = streamlit_geolocation()
    st.write(location)
    lat = location['latitude']
    lon = location['longitude']

    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("납치🚓"):
                uni = '납치'
                save_report(nam,lat,lon,uni)
                save_repo(nam, lat, lon, uni)
                st.switch_page("pages/actmanual.py")
            if st.button("화재🔥"):
                uni = '화재'
                save_report(nam, lat, lon, uni)
                save_repo(nam, lat, lon, uni)
                st.switch_page("pages/actmanual.py")
        with col2:
            if st.button("부상🚑"):
                uni = '부상'
                save_report(nam, lat, lon, uni)
                save_repo(nam, lat, lon, uni)
                st.switch_page("pages/actmanual.py")
            if st.button("기타➕"):
                uni = '기타'
                save_report(nam, lat, lon, uni)
                save_repo(nam, lat, lon, uni)
                st.switch_page("pages/actmanual.py")
else:
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

        # 위치가 설정되면 lat와 lon 변수를 정의합니다.
        lat, lon = st.session_state.center

    with st.container():
        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("납치🚓"):
                uni = '납치'
                save_report(nam, lat, lon, uni)
                save_repo(nam, lat, lon, uni)
                st.switch_page("pages/actmanual.py")
            if st.button("화재🔥"):
                uni = '화재'
                save_report(nam, lat, lon, uni)
                save_repo(nam, lat, lon, uni)
                st.switch_page("pages/actmanual.py")
        with col2:
            if st.button("부상🚑"):
                uni = '부상'
                save_report(nam, lat, lon, uni)
                save_repo(nam, lat, lon, uni)
                st.switch_page("pages/actmanual.py")
            if st.button("기타➕"):
                uni = '기타'
                save_report(nam, lat, lon, uni)
                save_repo(nam, lat, lon, uni)
                st.switch_page("pages/actmanual.py")





