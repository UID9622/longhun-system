# 龍魂体系 · 分布式节点容器 v2.0
# DNA: #龍芯⚡️丙午·辛未·乙酉·卯时·讼-NODE-DOCKER-v2.0

FROM python:3.11-slim

LABEL maintainer="UID9622 <longhun@uid9622.notion.site>"
LABEL version="2.0"
LABEL dna="#龍芯⚡️丙午·辛未·乙酉·卯时·讼-TRAIN-DATA-SOURCES-v2.0"
LABEL description="龍魂分布式节点 — 数据抓取+心跳上报+质量审计"

WORKDIR /app

# 安装依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates jq \
    && rm -rf /var/lib/apt/lists/*

# 复制节点核心
COPY deploy/longhun-node/node_heartbeat.py /app/node_heartbeat.py
COPY deploy/longhun-node/node_audit.py /app/node_audit.py

# 复制数据引擎
COPY data/sources/lh_fetch_engine.py /app/lh_fetch_engine.py
COPY data/sources/lh_data_cleaner.py /app/lh_data_cleaner.py
COPY data/sources/lh_source_manager.py /app/lh_source_manager.py
COPY data/sources/sources.json /app/sources.json

# 复制训练桥接
COPY bin/lh_data_to_train_bridge.py /app/lh_data_to_train_bridge.py

# 创建数据目录
RUN mkdir -p /data/logs /data/fetched /data/cleaned /data/train /data/audit

# 环境变量
ENV LONGHUN_NODE_ID=""
ENV LONGHUN_REGISTRY_URL="http://localhost:9623"
ENV LONGHUN_DNA_ANCHOR="#龍芯⚡️丙午·辛未·乙酉·卯时·讼-TRAIN-DATA-SOURCES-v2.0"
ENV LONGHUN_CONFIRM="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Shanghai

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:9622/health', timeout=3)" || exit 1

EXPOSE 9622

# 启动：静态文件服务 + 心跳 + 审计
CMD ["sh", "-c", "\
    echo '🐉 龍魂节点容器启动 v2.0' && \
    echo '🐉 节点ID:' $LONGHUN_NODE_ID && \
    echo '🐉 注册中心:' $LONGHUN_REGISTRY_URL && \
    python3 -m http.server 9622 --directory /data & \
    python3 /app/node_heartbeat.py --registry $LONGHUN_REGISTRY_URL --node-id $LONGHUN_NODE_ID & \
    wait"]
