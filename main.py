import ssl

import streamlit as st

ssl._create_default_https_context = ssl._create_unverified_context

st.set_page_config(initial_sidebar_state="collapsed",page_title='TRIP_PELGANGER',
    page_icon='✈️')

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://img.freepik.com/premium-photo/black-abstract-background-white-dots-black-background_73152-5632.jpg");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}


st.markdown(page_bg_img, unsafe_allow_html=True)

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
st.image("data/dasdlkashdlasdhlasd.png", caption="LET'S GO TRIP", use_column_width=True)
st.write('여행 & 사용자 공유시스템')
st.write("등록되어있지 않은 회원은 회원가입-로그인-홈 순서로 진행하여 주시기 바랍니다.")
st.write("기존에 등록된 회원은 로그인-홈 순서로 진행하여 주시면 됩니다.")
st.page_link("pages/signup.py", label='회원가입하기', icon='➕')
st.page_link("pages/login_map.py", label='로그인하기', icon='🔑')











