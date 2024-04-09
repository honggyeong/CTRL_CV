import pandas as pd
import streamlit as st
import ssl


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


df = pd.read_csv("https://raw.githubusercontent.com/honggyeong/SAVEME/main/data/users.csv")


ynlog = 0


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


            pdf = df.loc[df.이름 == name, ['전화번호']]
            st.dataframe(pdf)

            phone = pdf.iloc[0,0]
            lati = df.loc[df.이름 == name, ['위도']]
            lat = lati.iloc[0,0]
            long = df.loc[df.이름 == name, ['경도']]
            lon = long.iloc[0, 0]




            st.session_state.phone = phone
            st.session_state.lat = lat
            st.session_state.lon = lon
            st.write(name + '님', '로그인 되었습니다.')

            st.page_link("pages/Y_log.py", label='홈으로', icon='🤚')
        elif (df['이름'] == name).any() == False:
            st.write('로그인에 실패하였습니다.')
            st.page_link("pages/signup.py", label='회원가입하기', icon='🤚')
    else:
        st.page_link("main.py", label='홈으로 가기', icon='🤚')
