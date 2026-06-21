# 龍魂體系 · 待融入包監控容器
# DNA:#龍芯⚡️2026-06-16-PACKAGE-WATCHER-CONTAINER-v1.0

FROM python:3.13-slim

LABEL maintainer="UID9622"
LABEL description="Longhun pending integration package watcher & classifier"

# 安裝基本工具（jq 用於報告查詢）
RUN apt-get update && apt-get install -y --no-install-recommends \
    jq \
    && rm -rf /var/lib/apt/lists/*

# 創建應用目錄
WORKDIR /app

# 複製監控腳本
COPY bin/package-watcher.py /app/package-watcher.py
RUN chmod +x /app/package-watcher.py

# 創建輸出目錄
RUN mkdir -p /app/output

# 容器以非 root 用戶運行（可選，但掛載 home 時可能需要 uid 映射）
# 此處保留 root 以便讀取掛載卷；生產環境建議配合 user namespaces

# 默認命令：循環監控，每 5 分鐘掃描一次
CMD ["python3", "/app/package-watcher.py", \
     "--watch-dir", "/host/Downloads", \
     "--watch-dir", "/host/home", \
     "--output-dir", "/app/output", \
     "--interval", "300", \
     "--prune"]
