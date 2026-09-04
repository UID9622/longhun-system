# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-DOCKER-KUNPENG-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
#
# 鲲鹏/飞腾 ARM64 Dockerfile
# - ARMv8+ · 国密SM3/SM4 · 鲲鹏加速库KAE
# - 编译标志: -march=armv8.2-a+fp16+rcpc+dotprod+sm3+sm4 (鲲鹏)
# - 编译标志: -march=armv8-a+crc+crypto (飞腾)

FROM arm64v8/python:3.12-slim-bookworm

LABEL org.longhun.dna="#龍芯⚡️丙午·丙申·庚戌·䷙大畜-KUNPENG-v1.0"
LABEL org.longhun.creator="诸葛鑫（UID9622）"
LABEL org.longhun.license="MulanPSL v2"

ARG BUILD_FLAGS="-march=armv8.2-a"
ARG CHIP_TARGET="kunpeng"

# 系统依赖 + 鲲鹏加速库 KAE
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libssl-dev \
        libgmp-dev \
        libsodium-dev \
        && rm -rf /var/lib/apt/lists/*

# 尝试安装鲲鹏加速引擎 KAE（如果可用则用于国密加速）
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libkae-dev 2>/dev/null || echo "KAE 不可用，使用软件国密" && \
    rm -rf /var/lib/apt/lists/*

# Python 依赖
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# 复制应用代码
COPY . /app
WORKDIR /app

# 设置架构感知环境变量
ENV CHIP_TARGET=${CHIP_TARGET}
ENV BUILD_FLAGS=${BUILD_FLAGS}
ENV PYTHONUNBUFFERED=1
ENV LONGHUN_MODE=production

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python3 -c "from longhun_core.chip_hal.chip_detect import detect_chip; detect_chip()" || exit 1

EXPOSE 8765 8771 8783

CMD ["python3", "-m", "longhun_core"]
