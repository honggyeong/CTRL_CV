import firebase_admin
import streamlit as st
from firebase_admin import credentials
from firebase_admin import db
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.exceptions import (CredentialsError,
                                                          ForgotError,
                                                          LoginError,
                                                          RegisterError,
                                                          ResetError,
                                                          UpdateError)




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



def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(st.secrets["app_todo_cert"])
        firebase_admin.initialize_app(cred, {
            'databaseURL': st.secrets["app_todo_url"]
        })
    return firebase_admin.get_app()

# Firebase 앱 초기화
try:
    app = initialize_firebase()
    st.success("Firebase 초기화 성공")
except Exception as e:
    st.error(f"Firebase 초기화 오류: {e}")



# Loading config file
with open(st.secrets["yam"], 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Creating the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Creating a login widget
try:
    authenticator.login()
except LoginError as e:
    st.error(e)
if st.session_state["authentication_status"] == True:
    authenticator.logout()
    st.write(f'반갑습니다 *{st.session_state["name"]}*님')

    # Firebase에서 데이터 가져오기
    if "name" in st.session_state:
        ref = db.reference("/locations/{}".format(st.session_state["name"]))
        data = ref.get()
        if data:
            st.write("사용자 데이터:", data)
            lat = data["latitude"]
            lon = data["longitude"]
            st.session_state.my_lat = lat
            st.session_state.my_lon = lon
        else:
            st.write("해당 사용자의 데이터가 없습니다.")
    else:
        st.warning("사용자 이름이 설정되지 않았습니다.")


    st.title('무엇을 할까요?')
    if st.button("도움받기🤚"):
        st.switch_page("pages/needer.py")
    if st.button("도와주기💪"):
        st.switch_page("pages/helper.py")
    if st.button("경찰서위치보기🚔"):
        st.switch_page("pages/police.py")
    if st.button('홈으로 가기'):
        st.switch_page('main.py')

elif st.session_state["authentication_status"] is False:
    st.error('아이디/비밀번호가 맞지 않습니다.')
elif st.session_state["authentication_status"] is None:
    st.warning('아이디와 비밀번호를 입력해주세요.')

# Creating a password reset widget
if st.session_state["authentication_status"] == False:
    try:
        if authenticator.reset_password(st.session_state["username"]):
            st.success('비밀번호가 변경되었습니다.')
    except ResetError as e:
        st.error(e)
    except CredentialsError as e:
        st.error(e)

# # Creating a forgot password widget
if st.session_state["authentication_status"] == False:
    try:
        (username_of_forgotten_password,
            email_of_forgotten_password,
            new_random_password) = authenticator.forgot_password()
        if username_of_forgotten_password:
            st.success('새로운 비밀번호를 전송했습니다.')
            # Random password to be transferred to the user securely
        elif not username_of_forgotten_password:
            st.error('아이디를 찾을 수 없습니다. ')
    except ForgotError as e:
        st.error(e)

# # Creating a forgot username widget
if st.session_state["authentication_status"] == False:
    try:
        (username_of_forgotten_username,
            email_of_forgotten_username) = authenticator.forgot_username()
        if username_of_forgotten_username:
            st.success('Username sent securely')
            # Username to be transferred to the user securely
        elif not username_of_forgotten_username:
            st.error('Email not found')
    except ForgotError as e:
        st.error(e)

# # Creating an update user details widget
if st.session_state["authentication_status"] == False:
    try:
        if authenticator.update_user_details(st.session_state["username"]):
            st.success('항목이 업데이트 되었습니다. ')
    except UpdateError as e:
        st.error(e)

# Saving config file
with open(st.secrets["yam"], 'w', encoding='utf-8') as file:
    yaml.dump(config, file, default_flow_style=False)
