# 龍魂·自描述子系统 ADS · 容器镜像
# DNA: #龍芯⚡️丙午·丙申·丙寅·乙未·䷣明夷-ADS-DOCKER-v4.0
# License: MulanPSL v2
# 注意: ADS 依赖同目录 lh_dna_generator.py + lh_time_engine.py（复用不重造）

FROM python:3.13-slim

LABEL maintainer="UID9622"
LABEL description="龍魂自描述子系统 ADS v4.0 · 四层递归自指认知 · Port 9626"
LABEL dna="#龍芯⚡️2026-08-20-ADS-DOCKER-v4.0"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 引擎 + 复用依赖（同一目录，PYTHONPATH 覆盖）
COPY bin/lh_self_describing.py /app/lh_self_describing.py
COPY bin/lh_dna_generator.py /app/lh_dna_generator.py
COPY bin/lh_time_engine.py /app/lh_time_engine.py

RUN pip install --no-cache-dir psutil cryptography pyyaml

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Shanghai

# 健康检查（零 curl 依赖也行，但保留 curl 便于排障）
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:9626/api/v1/health', timeout=5).read()" || exit 1

EXPOSE 9626

CMD ["python3", "/app/lh_self_describing.py", "--api", "--port", "9626"]
