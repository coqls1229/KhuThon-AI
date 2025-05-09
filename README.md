서버 실행시 터미널에<br>uvicorn api:app --reload

실행 가능 url 실행<br>http://127.0.0.1:8000/docs

테스트 예시<br>
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

output 예시: {"predicted_class": "A", "confidence": 0.9018}

<img width="904" alt="image" src="https://github.com/user-attachments/assets/a9286e5c-9b52-4507-ab62-03ed7770b8af" />
