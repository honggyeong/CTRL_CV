
import requests
import streamlit as st
import pandas as pd
from github import Github
from io import StringIO
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def psh():
    repo_owner = 'honggyeong'
    repo_name = 'SAVEME'
    file_path = 'data/users.csv'
    token = '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'
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
    number = st.text_input('전화번호')
with st.container():
    age = st.slider('나이?', 0, 130, 25)
with st.container():
    sex = st.selectbox(
       '성별을 선택하세요',
       ('남', '여', '알수없음'))


if  st.button('입력완료/회원정보 등록'):
    df2 = pd.DataFrame({'이름': [name], '전화번호':[number], '나이':[age], '성별':[sex]})
    new_df = df._append(df2, ignore_index=True)
    df = new_df
    df.to_csv('users.csv', index=False)
    psh()
    st.write('등록이 완료되었습니다. 회원 정보 등록은 약 2분정도 소요되며, 2분 후 앱을 다시 실행하여 로그인 해주세요.')

st.page_link('main.py',label='홈화면으로', icon='🏠')





