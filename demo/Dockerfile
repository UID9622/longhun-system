FROM python:3.11-slim

WORKDIR /app

# 复制 requirements 并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app.py .

# 复制三色审计引擎
COPY engine/ /app/engine/
RUN mkdir -p /app/engine

EXPOSE 9622

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9622"]
