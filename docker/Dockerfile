# 龍魂体系 · 待融入包监控容器
# DNA:#龍芯⚡️2026-06-16-PACKAGE-WATCHER-CONTAINER-v1.0

FROM python:3.13-slim

LABEL maintainer="UID9622"
LABEL description="Longhun pending integration package watcher & classifier"

# 安装基本工具（jq 用于报告查询）
RUN apt-get update && apt-get install -y --no-install-recommends \
    jq \
    && rm -rf /var/lib/apt/lists/*

# 创建应用目录
WORKDIR /app

# 复制监控脚本
COPY bin/package-watcher.py /app/package-watcher.py
RUN chmod +x /app/package-watcher.py

# 创建输出目录
RUN mkdir -p /app/output

# 容器以非 root 用户运行（可选，但挂载 home 时可能需要 uid 映射）
# 此处保留 root 以便读取挂载卷；生产环境建议配合 user namespaces

# 默认命令：循环监控，每 5 分钟扫描一次
CMD ["python3", "/app/package-watcher.py", \
     "--watch-dir", "/host/Downloads", \
     "--watch-dir", "/host/home", \
     "--output-dir", "/app/output", \
     "--interval", "300", \
     "--prune"]
