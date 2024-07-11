import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

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

plt.rcParams['font.family'] = 'Malgun Gothic'
# Firebase 초기화
def initialize_firebase():
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate("report-5a738-firebase-adminsdk-2xgba-7458315dfe.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://report-5a738-default-rtdb.firebaseio.com/'
        })

initialize_firebase()

# 데이터 가져오기
def get_report_data():
    ref = db.reference('reports')
    data = ref.get()
    if data:
        df = pd.DataFrame.from_dict(data, orient='index')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    return pd.DataFrame()

st.title("신고 분석 대시보드")

if st.button('홈으로 가기'):
    st.switch_page('main.py')

# 여기서 데이터를 가져옵니다
df = get_report_data()

if df.empty:
    st.write("데이터가 없습니다.")
else:
    st.write(f"총 신고 건수: {len(df)}")

    # 시간대별 신고량
    st.subheader("시간대별 신고량")
    df['hour'] = df['timestamp'].dt.hour
    hourly_reports = df['hour'].value_counts().sort_index()
    st.bar_chart(hourly_reports)

    # 유형별 신고량
    st.subheader("유형별 신고량")
    type_counts = df['type'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    st.pyplot(fig)

    # 최근 7일간 일별 신고량 추이
    st.subheader("최근 7일간 일별 신고량 추이")
    df['date'] = df['timestamp'].dt.date
    last_7_days = pd.date_range(end=datetime.now(), periods=7).date
    daily_reports = df['date'].value_counts().sort_index()
    daily_reports = daily_reports.reindex(last_7_days, fill_value=0)
    st.line_chart(daily_reports)

    # 지도에 신고 위치 표시
    st.subheader("신고 위치 지도")
    st.map(df[['latitude', 'longitude']])

    # 상세 데이터 테이블
    st.subheader("상세 신고 데이터")
    st.dataframe(df[['name', 'type', 'timestamp', 'latitude', 'longitude']])

    # 시간대별 신고 유형 분포
    st.subheader("시간대별 신고 유형 분포")
    plt.figure(figsize=(12, 6))
    sns.countplot(x='hour', hue='type', data=df)
    plt.title("시간대별 신고 유형 분포")
    plt.xlabel("시간")
    plt.ylabel("신고 건수")
    st.pyplot(plt)

    # 최근 24시간 동안의 신고량 추이
    st.subheader("최근 24시간 동안의 신고량 추이")
    now = datetime.now()
    last_24_hours = df[df['timestamp'] > (now - timedelta(hours=24))]
    hourly_trend = last_24_hours.groupby(last_24_hours['timestamp'].dt.floor('H')).size()
    st.line_chart(hourly_trend)