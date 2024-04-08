



import folium
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import requests
import streamlit as st
import pandas as pd
from github import Github
from io import StringIO
import ssl




ssl._create_default_https_context = ssl._create_unverified_context
df = pd.read_csv("https://raw.githubusercontent.com/honggyeong/SAVEME/main/data/emergency.csv")


a = st.session_state.key

st.write(a+'님', '안녕하세요')



st.title('도움받기')
def psh():
    repo_owner = 'honggyeong'
    repo_name = 'SAVEME'
    file_path = 'data/emergency.csv'
    token = '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'
    commit_message = 'Update CSV file'

    github = Github(token)
    repo = github.get_user(repo_owner).get_repo(repo_name)

    url = f'https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{file_path}'
    response = requests.get(url)


    df = pd.read_csv(StringIO(response.text))
    df['test_col'] = "new_test_val"

    content = repo.get_contents(file_path)
    with open('emergency.csv', 'rb') as f:
        contents = f.read()


    repo.update_file(file_path, commit_message, contents, content.sha)




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




with st.container():
    col1, col2 = st.columns([2,1])
    with col1:
        if st.button("납치🚓"):
            uni = '납치'
            eme = 4
            df2 = pd.DataFrame({'이름': [a], '위도': [round(st.session_state.center[0], dec)], '경도': [round(st.session_state.center[1], dec)], '유형': [uni], '위급정도': [eme]})
            new_df = df._append(df2, ignore_index=True)
            df = new_df
            df.to_csv('emergency.csv', index=False)
            psh()
            st.write('접수신청을 하였습니다. 접수까지는 2분 정도 소요됩니다. ')
        if st.button("화재🔥"):
            uni = '화재'
            eme = 3
            df2 = pd.DataFrame({'이름': [a], '위도': [round(st.session_state.center[0], dec)], '경도': [round(st.session_state.center[1], dec)], '유형': [uni], '위급정도': [eme]})
            new_df = df._append(df2, ignore_index=True)
            df = new_df
            df.to_csv('emergency.csv', index=False)
            psh()
            st.write('접수신청을 하였습니다. 접수까지는 2분 정도 소요됩니다. ')
    with col2:
        if st.button("부상🚑"):
            uni = '부상'
            eme = 2
            df2 = pd.DataFrame({'이름': [a],'위도': [round(st.session_state.center[0], dec)], '경도': [round(st.session_state.center[1], dec)], '유형': [uni], '위급정도': [eme]})
            new_df = df._append(df2, ignore_index=True)
            df = new_df
            df.to_csv('emergency.csv', index=False)
            psh()
            st.write('접수신청을 하였습니다. 접수까지는 2분 정도 소요됩니다. ')
        if st.button("기타➕"):
            uni = '기타'
            eme = 1
            df2 = pd.DataFrame({'이름': [a], '위도': [round(st.session_state.center[0], dec)], '경도': [round(st.session_state.center[1], dec)], '유형': [uni], '위급정도': [eme]})
            new_df = df._append(df2, ignore_index=True)
            df = new_df
            df.to_csv('emergency.csv', index=False)
            psh()
            st.write('접수신청을 하였습니다. 접수까지는 2분 정도 소요됩니다. ')



