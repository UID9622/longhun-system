# 龍魂 CNSH Editor API · Dockerfile
# DNA: #龍芯⚡️2026-07-04-CNSH-API-DOCKER-v1.0
#
# 构建（x86）：
#   docker build -t cnsh-editor-api:latest -f Dockerfile ../..
# 构建（华为鲲鹏 ARM64）：
#   docker buildx build --platform linux/arm64 -t cnsh-editor-api:arm64 -f Dockerfile ../..
#
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制 CNSH 编辑器后端包与 API 服务
COPY dev-env/chinese-editor /app/chinese-editor
COPY integrated-modules/cnsh_editor_api /app/cnsh_editor_api

# 安装 Python 依赖
RUN pip install --no-cache-dir -e /app/chinese-editor \
    && pip install --no-cache-dir fastapi uvicorn pydantic

# 默认免费 tier；华为云完整版请在运行容器时设置为 paid
ENV CNSH_API_TIER=free
ENV CNSH_API_HOST=0.0.0.0
ENV CNSH_API_PORT=8000
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["python3", "-m", "cnsh_editor_api.main"]
