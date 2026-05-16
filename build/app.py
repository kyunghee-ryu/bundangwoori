import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import plotly.graph_objects as go

# 1. BigQuery 클라이언트 설정
# 1. Secrets에서 인증 정보 읽어오기
if "gcp_service_account" in st.secrets:
    info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(info)
    client = bigquery.Client(credentials=credentials, project=info["bundangwoori-492711"])
else:
    st.error("Secrets 설정에서 gcp_service_account를 찾을 수 없습니다.")
    st.stop()

@st.cache_data
def load_data():
    # 쿼리 작성: a, b, c 부서의 주일예배 출석 데이터를 날짜별로 가져옴
    query = """
    SELECT 
        CAST(date AS DATE) as date,
        department,
        value
    FROM `your_project.your_dataset.bq_all`
    WHERE category = '주일예배' 
      AND department IN ('서현', '송림', '청년')
      AND metric = '출석'
    ORDER BY date ASC
    """
    return client.query(query).to_dataframe()

st.title("⛪ 주일예배 부서별 출석 통계")

try:
    df = load_data()

    # 2. Plotly 누적 세로 막대그래프 생성
    fig = go.Figure()

    for dept in ['서현', '송림', '청년']:
        dept_data = df[df['department'] == dept]
        fig.add_trace(go.Bar(
            x=dept_data['date'],
            y=dept_data['value'],
            name=f'{dept.upper()} 부서'
        ))

    # 누적 설정 (stack) 및 디자인
    fig.update_layout(
        barmode='stack',
        xaxis_title="날짜 (매주 일요일)",
        yaxis_title="참석 인원수",
        hovermode="x unified",
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")