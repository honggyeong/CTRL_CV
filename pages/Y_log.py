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

name = st.session_state.key




st.title('구해줘용 (KOREA No.1  SAFETY)')
st.write(name + '님', '반가워요')
st.write("WELCOME")
st.page_link("pages/needer.py", label='도움받기', icon='🤚')
st.page_link("pages/helper.py", label='도와주기', icon='💪')
