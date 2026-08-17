# 龍魂·云浏览器 Dockerfile
# DNA: #龍芯⚡️丙午-乙巳-癸酉-亥时-☰乾-CLOUD-BROWSER-DOCKER-v1.0-BUILD
# License: MulanPSL v2
# 官方 Playwright 镜像自带 Chromium + 全部系统依赖（免编译）
FROM mcr.microsoft.com/playwright:v1.53.0-jammy

WORKDIR /app

COPY backend/requirements.txt .
# 官方镜像不带 pip：apt 补装；playwright install chromium 把浏览器固化进镜像层
# （镜像内置 chromium-1178 完整版，但 1.53.0 的 headless 需 headless_shell-1179 → 补装对齐）
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-pip \
    && python3 -m pip install --no-cache-dir -r requirements.txt \
    && python3 -m playwright install chromium \
    && rm -rf /var/lib/apt/lists/*

COPY backend/ .

ENV BROWSER_DATA_DIR=/data/browser
ENV HEADLESS=1
ENV BROWSER_API_PORT=8899
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

EXPOSE 8899

CMD ["python3", "-m", "uvicorn", "browser_service:app", "--host", "0.0.0.0", "--port", "8899"]
