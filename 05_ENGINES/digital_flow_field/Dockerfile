# 龍魂系统 · 工程实现层
# License: MulanPSL v2
# DNA: #龍芯⚡️丙午·癸未·甲申-DIGITAL-FLOW-FIELD-DOCKER-v2.0-UID9622
# 署名: UID9622（诸葛鑫·Lucky）

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
