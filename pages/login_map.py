import pandas as pd
import streamlit as st
import ssl


ssl._create_default_https_context = ssl._create_unverified_context
df = pd.read_csv("https://raw.githubusercontent.com/honggyeong/SAVEME/main/data/users.csv")



placeholder = st.empty()
def n():
    global name
    name = st.text_input('이름', key="name")
    st.session_state.key = name




placeholder = st.empty()
oo = st.empty()


with placeholder.container():
    st.title('구해줘용 (KOREA No.1  SAFETY)')
    st.title('정보를 입력해주세요')
    n()
    result = df[df['이름'] == name]
    st.write('조회되는 회원님의 정보는 다음과 같습니다. 맞다면 확인을 눌러주세요. ', result)
    if st.button('확인'):
        if (df['이름'] == name).any() == True:
            st.write(name + '님', '로그인 되었습니다.')
        elif (df['이름'] == name).any() == False:
            st.write('로그인에 실패하였습니다.')



    if st.button('로그인 완료 / 홈으로'):
        placeholder.empty()
        with oo.container():
            st.title('구해줘용 (KOREA No.1  SAFETY)')
            st.write(name + '님', '반가워요')
            st.write("WELCOME")
            st.page_link("pages/needer.py", label='도움받기', icon='🤚')
            st.page_link("pages/helper.py", label='도와주기', icon='💪')



