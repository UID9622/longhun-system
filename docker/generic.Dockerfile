# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-DOCKER-GENERIC-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
#
# 通用 Dockerfile（x86_64 / 通用 ARM64 降级）
# 最安全基线：python:3.12-slim + apt upgrade

# 多架构自动选择
FROM --platform=$TARGETPLATFORM python:3.12-slim-bookworm

LABEL org.longhun.dna="#龍芯⚡️丙午·丙申·庚戌·䷙大畜-GENERIC-v1.0"
LABEL org.longhun.creator="诸葛鑫（UID9622）"
LABEL org.longhun.license="MulanPSL v2"

ARG BUILD_FLAGS=""
ARG CHIP_TARGET="generic"

# 系统依赖
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libssl-dev \
        && rm -rf /var/lib/apt/lists/*

# Python 依赖
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# 复制代码
COPY . /app
WORKDIR /app

ENV CHIP_TARGET=${CHIP_TARGET}
ENV PYTHONUNBUFFERED=1
ENV LONGHUN_MODE=production

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python3 -c "from longhun_core.chip_hal.chip_detect import detect_chip; detect_chip()" || exit 1

EXPOSE 8765 8771 8783

CMD ["python3", "-m", "longhun_core"]
