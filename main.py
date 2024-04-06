import folium
import streamlit as st
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import pandas as pd




st.set_page_config(
    page_title='구해줘용',
    page_icon='🚓')



def main1():
    a = 0
    st.title("구해줘용")
    st.write('KOREA No.1 safety app.')
    st.page_link("pages/signup.py", label='회원가입하기', icon='➕')
    st.page_link("pages/login.py", label='로그인하기', icon='🔑')
    st.page_link("pages/needer.py", label='도움받기', icon='🤚')
    st.page_link("pages/helper.py", label='도와주기', icon='💪')

def main2(a):
    st.title("구해줘용")
    st.write('KOREA No.1 safety app.')

    st.page_link("pages/needer.py", label='도움받기', icon='🤚')
    st.page_link("pages/helper.py", label='도와주기', icon='💪')



main1()




