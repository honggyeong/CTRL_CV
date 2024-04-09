import folium
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import requests
import streamlit as st
from github import Github
from io import StringIO
import ssl
import pandas as pd

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



def psh():
    repo_owner = 'honggyeong'
    repo_name = 'SAVEME'
    file_path = 'data/users.csv'
    token = st.secret["GIT_TOKEN"]
    commit_message = 'Update CSV file'

    github = Github(token)
    repo = github.get_user(repo_owner).get_repo(repo_name)

    url = f'https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{file_path}'
    response = requests.get(url)


    df = pd.read_csv(StringIO(response.text))
    df['test_col'] = "new_test_val"

    content = repo.get_contents(file_path)
    with open('users.csv', 'rb') as f:
        contents = f.read()


    repo.update_file(file_path, commit_message, contents, content.sha)


df = pd.read_csv("https://raw.githubusercontent.com/honggyeong/SAVEME/main/data/users.csv")
st.title("회원가입")

st.write('정보를 입력해주세요')

with st.container():
    name = st.text_input('이름')
with st.container():
    number = st.text_input('전화번호(010을 제외한 8자리 숫자 그대로 입력)(ex010-1234-5678 = 12345678)')
with st.container():
    age = st.slider('나이?', 0, 130, 25)
with st.container():
    sex = st.selectbox(
       '성별을 선택하세요',
       ('남', '여', '알수없음'))
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

if  st.button('입력완료/회원정보 등록'):
    df2 = pd.DataFrame({'이름': [name], '전화번호':[number], '나이':[age], '성별':[sex],'위도': [round(st.session_state.center[0], dec)], '경도': [round(st.session_state.center[1], dec)]})
    new_df = df._append(df2, ignore_index=True)
    df = new_df
    df.to_csv('users.csv', index=False)
    psh()
    st.write('등록이 완료되었습니다. 회원 정보 등록은 약 2분정도 소요되며, 2분 후 앱을 다시 실행하여 로그인 해주세요.')

st.page_link('main.py',label='홈화면으로', icon='🏠')





