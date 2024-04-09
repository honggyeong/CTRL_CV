import streamlit as st
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

st.set_page_config(initial_sidebar_state="collapsed",page_title='구해줘용',
    page_icon='🚓')

token = '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'
st.session_state.token = token

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


st.title("구해줘용")
st.write('KOREA No.1 safety app.')
st.write("등록되어있지 않은 회원은 회원가입-로그인-홈 순서로 진행하여 주시기 바랍니다.")
st.write("기존에 등록된 회원은 로그인-홈 순서로 진행하여 주시면 됩니다.")
st.page_link("pages/signup.py", label='회원가입하기', icon='➕')
st.page_link("pages/login_map.py", label='로그인하기', icon='🔑')
st.page_link("pages/police.py", label='경찰서위치보기', icon='🚔')





