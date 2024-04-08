import streamlit as st
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

st.set_page_config(initial_sidebar_state="collapsed",page_title='구해줘용',
    page_icon='🚓')

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

st.page_link("pages/signup.py", label='회원가입하기', icon='➕')
st.page_link("pages/login_map.py", label='로그인하기', icon='🔑')
st.page_link("pages/needer.py", label='도움받기', icon='🤚')
st.page_link("pages/helper.py", label='도와주기', icon='💪')











