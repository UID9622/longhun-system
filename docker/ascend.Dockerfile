# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-DOCKER-ASCEND-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
#
# 昇腾 NPU Dockerfile
# - 基于华为昇腾官方镜像
# - CANN Toolkit + torch_npu
# - AI 推理加速

FROM ascendhub/ascend-pytorch:latest

LABEL org.longhun.dna="#龍芯⚡️丙午·丙申·庚戌·䷙大畜-ASCEND-v1.0"
LABEL org.longhun.creator="诸葛鑫（UID9622）"
LABEL org.longhun.license="MulanPSL v2"

ARG CANN_VERSION="8.0.RC1"
ARG CHIP_TARGET="ascend"

# 系统依赖
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libssl-dev \
        && rm -rf /var/lib/apt/lists/*

# 验证 CANN 环境
RUN test -d /usr/local/Ascend && echo "CANN 驱动就绪" || echo "警告: CANN 未找到"

# Python 依赖
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt 2>/dev/null; exit 0

# 复制代码
COPY . /app
WORKDIR /app

ENV ASCEND_HOME=/usr/local/Ascend
ENV CHIP_TARGET=${CHIP_TARGET}
ENV CANN_VERSION=${CANN_VERSION}
ENV LD_LIBRARY_PATH=/usr/local/Ascend/driver/lib64:/usr/local/Ascend/nnae/latest/lib64:${LD_LIBRARY_PATH}
ENV PYTHONUNBUFFERED=1
ENV LONGHUN_MODE=production

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD npu-smi info || python3 -c "from longhun_core.chip_hal.chip_detect import detect_chip; detect_chip()" || exit 1

EXPOSE 8765 8771 8783

CMD ["python3", "-m", "longhun_core"]
