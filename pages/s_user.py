import ssl
import folium
from streamlit_folium import st_folium
import firebase_admin
import streamlit as st
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd
import requests  # requests 라이브러리 추가

# SSL 인증서 문제 해결
ssl._create_default_https_context = ssl._create_unverified_context

# Streamlit 사이드바 축소 버튼 숨기기
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

# Firebase 초기화 함수
def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(st.secrets["repo_cert"])
        firebase_admin.initialize_app(cred, {
            'databaseURL': st.secrets["repo_url"]
        })
    return firebase_admin.get_app()

initialize_firebase()

# Firebase 앱 초기화
try:
    app = initialize_firebase()
    st.success("Firebase 초기화 성공")
except Exception as e:
    st.error(f"Firebase 초기화 오류: {e}")

# Firebase에서 사용자 데이터 가져오기
ref = db.reference("/users")  # 'users' 노드
data = ref.get()

# 데이터를 Pandas DataFrame으로 변환
if data:
    user_data = []
    for key, value in data.items():
        user_info = {
            "Name": value.get('name'),
            "Gender": value.get('gender'),
            "Age": value.get('age'),
            "Hobby": value.get('hobby'),
            "MBTI": value.get('mbti'),
            "Origin": value.get('origin'),
            "Favorite Travel": value.get('favorite_travel'),
            "Latitude": value.get('latitude'),
            "Longitude": value.get('longitude')
        }
        user_data.append(user_info)

    df = pd.DataFrame(user_data)

    # 나이대 선택
    age_group = st.selectbox("나이대를 선택하세요:", ["전체", "10대", "20대", "30대", "40대 이상"])

    # 나이대에 따라 데이터 필터링
    if age_group != "전체":
        age_ranges = {
            "10대": range(10, 20),
            "20대": range(20, 30),
            "30대": range(30, 40),
            "40대 이상": range(40, 150)
        }
        selected_age_range = age_ranges[age_group]
        df = df[df['Age'].between(selected_age_range.start, selected_age_range.stop - 1)]

    if not df.empty:
        # 사용자 선택
        selected_user = st.selectbox("사용자를 선택하세요", df['Name'])

        if selected_user:
            # 선택한 사용자의 정보 가져오기
            selected_user_info = df[df['Name'] == selected_user].iloc[0]

            # 사용자의 정보 표시
            st.write("### 사용자 정보")
            st.write(f"**이름:** {selected_user_info['Name']}")
            st.write(f"**성별:** {selected_user_info['Gender']}")
            st.write(f"**나이:** {selected_user_info['Age']}")
            st.write(f"**취미:** {selected_user_info['Hobby']}")
            st.write(f"**MBTI:** {selected_user_info['MBTI']}")
            st.write(f"**출신지:** {selected_user_info['Origin']}")
            st.write(f"**선호 여행지:** {selected_user_info['Favorite Travel']}")

            # 지도 생성 (한국 중심)
            korea_center = [36.5, 127.5]
            my_map = folium.Map(location=korea_center, zoom_start=7)

            # 선택한 사용자의 위치에 마커 추가
            if not pd.isna(selected_user_info['Latitude']) and not pd.isna(selected_user_info['Longitude']):

                lat = selected_user_info['Latitude']
                lon = selected_user_info['Longitude']
                name = selected_user_info['Name']

                def get_location_info(api_key, latitude, longitude):
                    # Kakao 지오코딩 API 요청 URL
                    url = "https://dapi.kakao.com/v2/local/geo/coord2address.json"
                    headers = {
                        "Authorization": f"KakaoAK {api_key}"
                    }
                    params = {
                        "x": longitude,  # 경도
                        "y": latitude  # 위도
                    }

                    try:
                        # API 요청
                        response = requests.get(url, headers=headers, params=params)
                        response.raise_for_status()  # HTTP 오류가 발생하면 예외를 발생시킵니다.
                        data = response.json()

                        # 행정구역 정보 추출
                        if data.get('documents'):
                            address = data['documents'][0]['address']
                            region_1depth_name = address['region_1depth_name']  # 시도 (예: 서울특별시)
                            region_2depth_name = address['region_2depth_name']  # 시군구 (예: 종로구)
                            region_3depth_name = address['region_3depth_name']  # 동/읍/면 (예: 청운효자동)
                            region_4depth_name = address.get('region_4depth_name', 'N/A')  # 세부 지역 (없을 경우 'N/A')

                            return {
                                'region_1depth_name': region_1depth_name,
                                'region_2depth_name': region_2depth_name,
                                'region_3depth_name': region_3depth_name,
                                'region_4depth_name': region_4depth_name
                            }
                        else:
                            return "주소를 찾을 수 없습니다."
                    except requests.exceptions.HTTPError as http_err:
                        return f"HTTP 오류 발생: {http_err}"
                    except requests.exceptions.RequestException as req_err:
                        return f"요청 오류 발생: {req_err}"
                    except Exception as e:
                        return f"알 수 없는 오류 발생: {e}"

                # 카카오 API 키
                api_key = st.secrets['kako_api']
                latitude = lat
                longitude = lon

                address_info = get_location_info(api_key, latitude, longitude)
                if isinstance(address_info, dict):
                    st.write(f"위도 {latitude}, 경도 {longitude}의 행정구역:")
                    st.write(f"  1단계 행정구역: {address_info['region_1depth_name']}")
                    st.write(f"  2단계 행정구역: {address_info['region_2depth_name']}")
                    st.write(f"  3단계 행정구역: {address_info['region_3depth_name']}")
                    st.write(f"  4단계 행정구역: {address_info['region_4depth_name']}")
                else:
                    st.write(address_info)

                # 팝업 내용 생성
                popup_content = f"""
                <div style="font-family: Arial, sans-serif; padding: 10px;">
                    <h4 style="margin-bottom: 5px;">{name}</h4>
                    <p><strong>출신지:</strong> {lat:.4f}, {lon:.4f}</p>
                </div>
                """

                # 마커 추가
                folium.Marker(
                    [lat, lon],
                    popup=folium.Popup(popup_content, max_width=300),
                    tooltip=f"{name}",
                    icon=folium.Icon(color='green', icon='user', prefix='fa')
                ).add_to(my_map)

                # 지도 표시
                st.write(f'{name}님의 출신지')
                st_folium(my_map, width=700, height=500)
            else:
                st.warning(f"{name}님의 위치 정보가 없습니다.")
    else:
        st.write(f"선택한 나이대({age_group})에 해당하는 사용자 데이터가 없습니다.")
else:
    st.write("등록된 사용자 데이터가 없습니다.")

# 홈으로 가기 버튼
if st.button('홈으로 가기'):
    st.switch_page('main.py')
