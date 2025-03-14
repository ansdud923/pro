import streamlit as st
import pandas as pd
import json
import plotly.express as px

# 📌 JSON 파일 로드
with open("graph_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 📌 CSV 파일 로드 (최신 데이터)
df = pd.read_csv("Updated_Recycling_Campaign_Data.csv")

# 📌 Streamlit 대시보드 UI 설정
st.set_page_config(page_title="재활용 캠페인 AI 분석", layout="wide")
st.title("♻️ AI 기반 재활용 캠페인 데이터 분석")

# 🔹 1. 지역별 평균 참여율
st.subheader("📍 지역별 분리수거 참여율")
region_df = pd.DataFrame(data["region_participation"])
fig1 = px.bar(region_df, x="지역", y="분리수거 참여율 (%)", color="지역", text="분리수거 참여율 (%)")
st.plotly_chart(fig1)

# 🔹 2. 캠페인 홍보 방식별 참여율 변화 (꺾은선 그래프 수정)
st.subheader("📢 캠페인 홍보 방식별 참여율 변화")
promo_df = pd.DataFrame(data["promo_participation"])
promo_df_long = promo_df.melt(id_vars=["캠페인 홍보 방식"], value_vars=["캠페인 전 참여율 (%)", "캠페인 후 참여율 (%)"], 
                              var_name="참여율 구분", value_name="참여율 (%)")
fig2 = px.line(promo_df_long, x="캠페인 홍보 방식", y="참여율 (%)", color="참여율 구분", markers=True)
st.plotly_chart(fig2)

# 🔹 3. 지역별 폐기물 수거량 비교
st.subheader("🗑️ 지역별 폐기물 종류별 수거량 비교")
waste_df = df.groupby("지역")[["플라스틱 (kg)", "종이 (kg)", "캔 (kg)", "기타 폐기물 (kg)"]].sum().reset_index()
fig3 = px.bar(waste_df, x="지역", y=["플라스틱 (kg)", "종이 (kg)", "캔 (kg)", "기타 폐기물 (kg)"], barmode="group")
st.plotly_chart(fig3)

# 🔹 4. 연령대별 평균 참여율 분석 (파이 차트)
st.subheader("📊 연령대별 평균 분리수거 참여율")
age_df = df.groupby("참여 연령대")["분리수거 참여율 (%)"].mean().reset_index()
fig4 = px.pie(age_df, names="참여 연령대", values="분리수거 참여율 (%)", title="연령대별 평균 참여율")
st.plotly_chart(fig4)

# 🔹 5. 성별별 평균 분리수거 참여율 (막대 그래프 추가)
st.subheader("🚻 성별별 평균 분리수거 참여율")
gender_df = df.groupby("성별")["분리수거 참여율 (%)"].mean().reset_index()
fig5 = px.bar(gender_df, x="성별", y="분리수거 참여율 (%)", color="성별", text="분리수거 참여율 (%)", title="성별별 평균 분리수거 참여율")
st.plotly_chart(fig5)

# 🔹 6. 날짜별 참여율 트렌드 (히스토그램 → 시계열 변경)
# 🔹 날짜 데이터를 변환하여 월별 합계로 집계
df["날짜"] = pd.to_datetime(df["날짜"])
df["년월"] = df["날짜"].dt.to_period("M")  # 'YYYY-MM' 형식으로 변환

# 🔹 월별 합계 계산
monthly_df = df.groupby("년월")["분리수거 참여율 (%)"].sum().reset_index()
monthly_df["년월"] = monthly_df["년월"].astype(str)  # 스트림릿에서 문자열 변환

# 🔹 월별 합계 시계열 그래프 (선 그래프)
st.subheader("📅 월별 분리수거 참여율 합계 (시계열)")
fig6 = px.line(monthly_df, x="년월", y="분리수거 참여율 (%)", title="월별 분리수거 참여율 합계", markers=True)

# 🔹 그래프 표시
st.plotly_chart(fig6)



# 🔹 7. AI 예측 기능 (캠페인 홍보 방식 선택)
st.subheader("🔮 AI 예측: 캠페인 방식에 따른 예상 참여율")
selected_campaign = st.selectbox("분석할 캠페인 방식 선택", promo_df["캠페인 홍보 방식"].unique())

if selected_campaign:
    predicted_participation = promo_df[promo_df["캠페인 홍보 방식"] == selected_campaign]["캠페인 후 참여율 (%)"].values[0]
    st.success(f"✅ 예상 참여율: {predicted_participation:.2f}%")
