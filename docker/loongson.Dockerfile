# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-DOCKER-LOONGSON-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
#
# 龙芯 LoongArch Dockerfile
# - Loongnix Server 基础镜像
# - 龙芯 3A5000/3A6000 · LA464 微架构

FROM loongson/loongnix-server:latest

LABEL org.longhun.dna="#龍芯⚡️丙午·丙申·庚戌·䷙大畜-LOONGSON-v1.0"
LABEL org.longhun.creator="诸葛鑫（UID9622）"
LABEL org.longhun.license="MulanPSL v2"

ARG BUILD_FLAGS="-march=loongarch64 -mabi=lp64d"
ARG CHIP_TARGET="loongson"

# 系统依赖
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libssl-dev \
        python3 python3-pip python3-dev \
        && rm -rf /var/lib/apt/lists/*

# Python 依赖
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# 复制应用代码
COPY . /app
WORKDIR /app

ENV CHIP_TARGET=${CHIP_TARGET}
ENV BUILD_FLAGS=${BUILD_FLAGS}
ENV PYTHONUNBUFFERED=1
ENV LONGHUN_MODE=production

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python3 -c "from longhun_core.chip_hal.chip_detect import detect_chip; detect_chip()" || exit 1

EXPOSE 8765 8771 8783

CMD ["python3", "-m", "longhun_core"]
