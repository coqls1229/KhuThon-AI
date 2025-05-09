# api.py
from fastapi import FastAPI
from pydantic import BaseModel
import torch
from run.model import FertilizerClassifier
import torch.nn.functional as F

app = FastAPI()

# 모델 불러오기
model = FertilizerClassifier(input_size=9, num_classes=4)
model.load_state_dict(torch.load("run/fertilizer_model.pth", map_location=torch.device("cpu")))
model.eval()

# 입력 스키마 정의
class SensorInput(BaseModel):
    ph: float
    temperature: float
    humidity: float
    concentration: float
    homogeneity: str   # "A", "B", "C"
    odor: str          # "A", "B", "C"
    fermentation_days: int
    salinity: float
    e_coli: str        # "X", "O"

# 클래스 이름 매핑
class_names = ["A", "B", "C", "F"]

# 범주형 매핑
homogeneity_map = {"A": 2, "B": 1, "C": 0}
odor_map = {"A": 0, "B": 1, "C": 2}
e_coli_map = {"X": 0, "O": 1}

@app.post("/predict")
def predict(data: SensorInput):
    # 인코딩 처리
    h = homogeneity_map.get(data.homogeneity, 1)
    o = odor_map.get(data.odor, 1)
    e = e_coli_map.get(data.e_coli, 1)

    # 입력 텐서 구성
    input_tensor = torch.tensor([[
        data.ph,
        data.temperature,
        data.humidity,
        data.concentration,
        h,
        o,
        data.fermentation_days,
        data.salinity,
        e
    ]], dtype=torch.float32)

    # 예측
    with torch.no_grad():
        logits = model(input_tensor)
        probs = F.softmax(logits, dim=1)
        pred = probs.argmax().item()

    return {
        "predicted_class": class_names[pred],
        "confidence": round(probs[0][pred].item(), 4)
    }


"""
서버 실행시 터미널에 
uvicorn api:app --reload


테스트 예시
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '{
  "ph": 6.8,
  "temperature": 20.5,
  "humidity": 50.0,
  "concentration": 50.0,
  "homogeneity": "A",
  "odor": "A",
  "fermentation_days": 70,
  "salinity": 1.5,
  "e_coli": "X"
}'
"""