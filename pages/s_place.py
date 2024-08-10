import csv
import random
import requests
import pandas as pd
import streamlit as st
import folium
import firebase_admin
from firebase_admin import credentials, db
from streamlit_folium import st_folium

# Firebase initialization
def initialize_firebase():
    try:
        app = firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate(st.secrets['app_todo_cert'])
        firebase_admin.initialize_app(cred, {
            'databaseURL': st.secrets["app_todo_url"]
        })
    return firebase_admin.get_app()

initialize_firebase()

# Function to get location information
def get_location_info(api_key, latitude, longitude):
    url = "https://dapi.kakao.com/v2/local/geo/coord2address.json"
    headers = {
        "Authorization": f"KakaoAK {api_key}"
    }
    params = {
        "x": longitude,
        "y": latitude
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get('documents'):
            address = data['documents'][0]['address']
            return {
                'region_1depth_name': address['region_1depth_name'],
                'region_2depth_name': address['region_2depth_name'],
                'region_3depth_name': address['region_3depth_name'],
                'region_4depth_name': address.get('region_4depth_name', 'N/A')
            }
        else:
            return "주소를 찾을 수 없습니다."
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP 오류 발생: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"요청 오류 발생: {req_err}"
    except Exception as e:
        return f"알 수 없는 오류 발생: {e}"

# Function to get tourist spots from Naver API
def get_tourist_spots(location, display=20):
    CLIENT_ID = st.secrets["KAKO_ID"]
    CLIENT_SECRET = st.secrets["KAKAO_SECRET"]
    url = 'https://openapi.naver.com/v1/search/local.json'
    headers = {
        'X-Naver-Client-Id': CLIENT_ID,
        'X-Naver-Client-Secret': CLIENT_SECRET
    }
    params = {
        'query': location + ' 가볼만한 곳',
        'display': display,
        'sort': 'random'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        st.error(f"Error: {response.status_code}")
        return []

# Function to recommend tourist spots
def recommend_spots(tourist_spots, num_recommendations=5):
    if len(tourist_spots) > num_recommendations:
        return random.sample(tourist_spots, num_recommendations)
    return tourist_spots

# Function to get image from Naver Image Search API
def get_image(query):
    CLIENT_ID = st.secrets["NAVER_ID"]
    CLIENT_SECRET = st.secrets["NAVER_SECRET"]
    url = 'https://openapi.naver.com/v1/search/image'
    headers = {
        'X-Naver-Client-Id': CLIENT_ID,
        'X-Naver-Client-Secret': CLIENT_SECRET
    }
    params = {
        'query': query,
        'display': 1,
        'sort': 'sim'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        items = response.json().get('items', [])
        if items:
            return items[0].get('link')
    return None

# Function to save tourist spots to a CSV file
def save_to_csv(tourist_spots, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Address', 'Category', 'Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for spot in tourist_spots:
            writer.writerow({
                'Name': spot.get('title', 'N/A').replace('<b>', '').replace('</b>', ''),
                'Address': spot.get('address', 'N/A'),
                'Category': spot.get('category', 'N/A'),
                'Link': spot.get('link', 'N/A')
            })

# Function to handle travel spot recommendations and display
def loc(selected_travel):
    location = selected_travel
    tourist_spots = get_tourist_spots(location)

    if tourist_spots:

        recommended_spots = recommend_spots(tourist_spots, num_recommendations)

        st.subheader(f"{location}에서 추천하는 여행지:")
        for idx, spot in enumerate(recommended_spots, start=1):
            name = spot.get('title', 'N/A').replace('<b>', '').replace('</b>', '')
            address = spot.get('address', 'N/A')
            category = spot.get('category', 'N/A')
            link = spot.get('link', 'N/A')
            st.markdown(f"**{idx}. {name}**")
            st.write(f"- 주소: {address}")
            st.write(f"- 카테고리: {category}")
            st.write(f"[더보기]({link})")

            image_url = get_image(name)
            if image_url:
                st.image(image_url, caption=name, use_column_width=True)
            else:
                st.write("이미지를 찾을 수 없습니다.")

        save_to_csv(recommended_spots, 'recommended_tourist_spots.csv')
        st.write("추천된 여행지 정보를 `recommended_tourist_spots.csv`에 저장했습니다.")
        st.download_button(label="CSV 파일 다운로드", data=open('recommended_tourist_spots.csv', 'rb').read(), file_name='recommended_tourist_spots.csv')

    else:
        st.write("관광지 정보를 찾을 수 없습니다.")

# Streamlit app layout
st.title("여행지 추천")

# Firebase 데이터베이스 참조 가져오기
ref = db.reference('users')

try:
    data = ref.get()
    if data:
        df = pd.DataFrame.from_dict(data, orient='index')
        grouped = df.groupby('favorite_travel')['name'].apply(list).reset_index(name='users')
        grouped['user_count'] = grouped['users'].apply(len)

        selected_travel = st.selectbox("만족한 여행지를 선택하세요:", grouped['favorite_travel'])

        if selected_travel:
            user_list = grouped[grouped['favorite_travel'] == selected_travel]['users'].values[0]
            user_count = grouped[grouped['favorite_travel'] == selected_travel]['user_count'].values[0]

            st.write(f"**{selected_travel}**에 만족한 사용자들:")
            st.write(f"**총 {user_count}명**")
            st.write(", ".join(user_list))

            user_info = df[df['favorite_travel'] == selected_travel].iloc[0]
            lat, lon = user_info['latitude'], user_info['longitude']

            api_key = st.secrets["loc"]
            address_info = get_location_info(api_key, lat, lon)
            if isinstance(address_info, dict):
                st.write(f"출신지: {lat}, {lon}", address_info['region_1depth_name'], address_info['region_2depth_name'])
            else:
                st.write()

            map = folium.Map(location=[lat, lon], zoom_start=12)
            folium.Marker([lat, lon], popup=f"{selected_travel}").add_to(map)
            st.header(f"의견을 제시해주신 사용자의 출신지입니다.")
            st_folium(map, width=700, height=500)
            num_recommendations = st.slider("추천할 여행지의 수를 선택하세요", 1, 5, 5)
            if st.button("선택된 여행지 기반으로 여행지 추천"):
                loc(selected_travel)

    else:
        st.write("등록된 만족스러운 여행지가 없습니다.")

except Exception as e:
    st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")


# 홈으로 가기 버튼
if st.button('홈으로 가기'):
    st.switch_page('main.py')
