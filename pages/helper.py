import ssl
import folium
from streamlit_folium import st_folium
import firebase_admin
import streamlit as st
from firebase_admin import credentials
from firebase_admin import db

ssl._create_default_https_context = ssl._create_unverified_context

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

st.markdown(container_style, unsafe_allow_html=True)



placeholder = st.empty()

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("report-5a738-firebase-adminsdk-2xgba-7458315dfe.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://report-5a738-default-rtdb.firebaseio.com/'
        })
    return firebase_admin.get_app()

initialize_firebase()

# Firebase 앱 초기화
try:
    app = initialize_firebase()
    st.success("Firebase 초기화 성공")
except Exception as e:
    st.error(f"Firebase 초기화 오류: {e}")

# Firebase에서 데이터 가져오기
ref = db.reference("/reports")  # needer.py에서 사용한 'reports' 노드
data = ref.get()

# 지도 생성 (한국 중심)
korea_center = [36.5, 127.5]
my_map = folium.Map(location=korea_center, zoom_start=7)

# 현재 사용자의 위치에 원 추가
user_lat = st.session_state.my_lat
user_lon = st.session_state.my_lon
folium.Circle([user_lat, user_lon], radius=50000, color="blue", fill=True, fillColor="blue", popup="내 위치").add_to(
    my_map)
if data:
    for key, value in data.items():
        lat = value['latitude']
        lon = value['longitude']
        name = value['name']
        incident_type = value['type']

        # 사고 유형에 따른 아이콘 설정
        icon_color = 'red'
        if incident_type == '납치':
            icon = 'car'
        elif incident_type == '화재':
            icon = 'fire'
        elif incident_type == '부상':
            icon = 'ambulance'
        else:
            icon = 'exclamation'

        # 팝업 내용 생성
        popup_content = f"""
        <div style="font-family: Arial, sans-serif; padding: 10px;">
            <h4 style="margin-bottom: 5px;">사용자 정보</h4>
            <p><strong>이름:</strong> {name}</p>
            <p><strong>사고 유형:</strong> {incident_type}</p>
            <p><strong>위치:</strong> {lat:.4f}, {lon:.4f}</p>
        </div>
        """

        # 마커 추가
        folium.Marker(
            [lat, lon],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=f"{name}: {incident_type}",
            icon=folium.Icon(color=icon_color, icon=icon, prefix='fa')
        ).add_to(my_map)

    # 지도 표시
    st.write('도움이 필요한 사용자들의 위치 지도')
    st_folium(my_map, width=700, height=500)
else:
    st.write("신고된 데이터가 없습니다.")

if st.button('홈으로 가기'):
    st.switch_page('main.py')
