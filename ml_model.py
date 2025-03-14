import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import json

# 📌 1. 데이터 로드
df = pd.read_csv("Updated_Recycling_Campaign_Data.csv")

# 📌 2. 데이터 전처리
df = df.dropna()

# 🔹 범주형 데이터를 숫자로 변환
label_encoders = {}
for column in ["지역", "캠페인 홍보 방식", "참여 연령대", "성별"]:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# 🔹 특성과 타겟 변수 설정
X = df[["지역", "플라스틱 (%)", "종이 (%)", "캔 (%)", "캠페인 홍보 방식", "참여 연령대", "성별"]]
y = df["분리수거 참여율 (%)"]

# 🔹 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 📌 3. 랜덤 포레스트 모델 학습
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 🔹 모델 성능 평가
print(f"모델 R^2 점수: {model.score(X_test, y_test):.2f}")

# 🔹 특성 중요도 분석
feature_importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
}).sort_values(by="importance", ascending=False)

# 📌 4. 시각화용 데이터 생성
# 🔹 지역별 평균 참여율
region_participation = df.groupby("지역")["분리수거 참여율 (%)"].mean().reset_index()
region_participation["지역"] = label_encoders["지역"].inverse_transform(region_participation["지역"])

# 🔹 홍보 방식별 평균 참여율
promo_participation = df.groupby("캠페인 홍보 방식")[["캠페인 전 참여율 (%)", "캠페인 후 참여율 (%)"]].mean().reset_index()
promo_participation["캠페인 홍보 방식"] = label_encoders["캠페인 홍보 방식"].inverse_transform(promo_participation["캠페인 홍보 방식"])

# 🔹 JSON 파일 저장
graph_data = {
    "region_participation": region_participation.to_dict(orient="records"),
    "promo_participation": promo_participation.to_dict(orient="records"),
    "feature_importance": feature_importance.to_dict(orient="records")
}

with open("graph_data.json", "w", encoding="utf-8") as f:
    json.dump(graph_data, f, ensure_ascii=False, indent=2)

print("✅ JSON 파일 'graph_data.json'이 생성되었습니다.")
