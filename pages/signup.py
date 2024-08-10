import firebase_admin
import folium
import matplotlib.pyplot as plt
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from firebase_admin import credentials
from firebase_admin import db
from streamlit_authenticator.utilities.exceptions import (RegisterError,
                                                          UpdateError)
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
from yaml.loader import SafeLoader

# 세션 상태 초기화
if 'latitude' not in st.session_state:
    st.session_state.latitude = None
if 'longitude' not in st.session_state:
    st.session_state.longitude = None

def initialize_firebase():
    try:
        # 이미 초기화된 앱이 있는지 확인
        app = firebase_admin.get_app()
    except ValueError:
        # 앱이 초기화되지 않았다면 초기화
        cred = credentials.Certificate(st.secrets['app_todo_cert'])
        firebase_admin.initialize_app(cred, {
            'databaseURL': st.secrets['app_todo_url']
        })

    return firebase_admin.get_app()

app = initialize_firebase()

# 데이터 저장 함수
def save_user_data(name, latitude, longitude, gender, age, hobby, mbti, origin, favorite_travel):
    ref.child("{}".format(name)).set({
        'name' : name,
        'latitude': latitude,
        'longitude': longitude,
        'gender': gender,
        'age': age,
        'hobby': hobby,
        'mbti': mbti,
        'origin': origin,
        'favorite_travel': favorite_travel
    })
    print(f"Data saved for {name}")

# 데이터베이스 레퍼런스 가져오기
ref = db.reference('users', app=app)  # 'users'는 사용자 데이터를 저장할 노드 이름입니다.

# Loading config file
with open('config/config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Creating the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Creating a new user registration widget
try:
    gps = st.checkbox("나의 GPS위치 정보 사용하기")
    if gps:
        location = streamlit_geolocation()
        st.write(location)
        st.session_state.latitude = location['latitude']
        st.session_state.longitude = location['longitude']
    elif not gps:
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

    # 사용자 추가 정보 입력 받기
    gender = st.selectbox('성별', ['남성', '여성', '기타'])
    age = st.number_input('나이', min_value=0, max_value=120, step=1)
    hobby = st.text_input('취미')

    # MBTI 선택 드롭다운 추가
    mbti = st.selectbox('MBTI', [
        'ISFP', 'INFP', 'INTP', 'ISTP', 'ISFJ', 'INFJ', 'INTJ', 'ISTJ',
        'ESFP', 'ENFP', 'ENTP', 'ESTP', 'ESFJ', 'ENFJ', 'ENTJ', 'ESTJ'
    ])

    origin = st.text_input('출신지')
    favorite_travel = st.text_area('만족스러웠던 여행지')

    # 사용자 등록 처리
    (email_of_registered_user,
     username_of_registered_user,
     name_of_registered_user) = authenticator.register_user(pre_authorization=False)

    if email_of_registered_user:
        st.success('계정 생성이 완료되었습니다.')
        st.session_state["name"] = name_of_registered_user
        st.write(st.session_state["name"])
        if st.session_state.latitude is not None and st.session_state.longitude is not None:
            save_user_data(name_of_registered_user, st.session_state.latitude, st.session_state.longitude,
                           gender, age, hobby, mbti, origin, favorite_travel)
        else:
            st.error("위치 정보가 설정되지 않았습니다. 위치를 선택해주세요.")

        st.page_link("pages/login_map.py", label='로그인하러가기', icon='🔑')

except RegisterError as e:
    st.error(e)

# Creating an update user details widget
if st.session_state["authentication_status"]:
    try:
        if authenticator.update_user_details(st.session_state["username"]):
            st.success('항목이 업데이트 되었습니다.')
    except UpdateError as e:
        st.error(e)


# Saving config file
with open("config/config.yaml", 'w', encoding='utf-8') as file:
    yaml.dump(config, file, default_flow_style=False)

# 홈으로 가기 버튼
if st.button('홈으로 가기'):
    st.switch_page('main.py')
