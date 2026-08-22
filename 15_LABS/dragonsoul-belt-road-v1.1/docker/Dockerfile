# 龍魂 · 一带一路入门包 · Docker镜像构建 v1.1
# DNA: #龍芯⚡️丙午·丙申·戊午·鼎卦-BELT-ROAD-PACK-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 许可: MulanPSL v2
# 用途: 多阶段构建，最小化镜像，支持 amd64/arm64
# 警告: 🟡 本Dockerfile为设计稿，未经过真实多架构构建验证

# ============================================
# 阶段一: 构建 llama.cpp (推理引擎)
# ============================================
FROM alpine:3.20 AS llama-builder

ARG TARGETARCH
ARG LLAMA_CPP_VERSION=b3578

RUN apk add --no-cache     git     build-base     cmake     linux-headers     && mkdir -p /build

WORKDIR /build

# 克隆 llama.cpp (特定版本，可复现)
RUN git clone --depth 1 --branch ${LLAMA_CPP_VERSION}     https://github.com/ggerganov/llama.cpp.git llama.cpp

WORKDIR /build/llama.cpp

# 架构检测与编译
RUN if [ "$TARGETARCH" = "arm64" ]; then         cmake -B build             -DLLAMA_NATIVE=OFF             -DCMAKE_C_FLAGS="-mcpu=apple-m1"             -DCMAKE_CXX_FLAGS="-mcpu=apple-m1"             -DLLAMA_AVX=OFF             -DLLAMA_AVX2=OFF             -DLLAMA_FMA=OFF             -DLLAMA_F16C=OFF;     elif [ "$TARGETARCH" = "amd64" ]; then         cmake -B build             -DLLAMA_NATIVE=OFF             -DLLAMA_AVX=ON             -DLLAMA_AVX2=ON             -DLLAMA_FMA=ON             -DLLAMA_F16C=ON;     else         cmake -B build -DLLAMA_NATIVE=OFF;     fi     && cmake --build build --config Release -j$(nproc)

# ============================================
# 阶段二: Python 依赖构建
# ============================================
FROM python:3.11-slim AS python-builder

WORKDIR /build

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends     gcc     g++     libffi-dev     libssl-dev     && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt /build/
RUN pip install --no-cache-dir --user -r /build/requirements.txt

# ============================================
# 阶段三: 最终运行镜像
# ============================================
FROM python:3.11-slim AS runtime

ARG TARGETARCH
ARG DRAGONSOUL_VERSION=1.1
ARG MODEL_SIZE=7b

LABEL maintainer="龍魂系统 <dev@dragonsoul.dev>"       org.opencontainers.image.title="DragonSoul Belt & Road Pack"       org.opencontainers.image.description="Sovereign AI localization framework for Belt & Road countries"       org.opencontainers.image.version="${DRAGONSOUL_VERSION}"       org.opencontainers.image.licenses="MulanPSL-2.0"       dragonsoul.dna="#龍芯⚡️丙午·丙申·戊午·鼎卦-BELT-ROAD-PACK-UID9622"

# 环境变量
ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PYTHONFAULTHANDLER=1     PIP_NO_CACHE_DIR=1     PIP_DISABLE_PIP_VERSION_CHECK=1     DRAGONSOUL_VERSION=${DRAGONSOUL_VERSION}     DRAGONSOUL_HOME=/app     MODEL_SIZE=${MODEL_SIZE}     DEFAULT_LANG=en     PORT=8080     HOST=0.0.0.0     DATA_DIR=/app/data     MODELS_DIR=/app/models     LOGS_DIR=/app/logs     CONFIGS_DIR=/app/configs     SCENARIOS_DIR=/app/scenarios     PATH=/app/.local/bin:$PATH

# 安装系统运行时依赖
RUN apt-get update && apt-get install -y --no-install-recommends     curl     ca-certificates     libgomp1     libopenblas0     fonts-noto-cjk     fonts-noto-arabic     fonts-noto-devanagari     fonts-noto-thai     && rm -rf /var/lib/apt/lists/*     && apt-get clean

# 创建工作目录
WORKDIR /app

# 复制 Python 依赖
COPY --from=python-builder /root/.local /app/.local

# 复制 llama.cpp 二进制
COPY --from=llama-builder /build/llama.cpp/build/bin/llama-server /usr/local/bin/llama-server
COPY --from=llama-builder /build/llama.cpp/build/bin/llama-cli /usr/local/bin/llama-cli

# 复制应用代码
COPY dragonsoul/ /app/dragonsoul/
COPY configs/ /app/configs/
COPY scenarios/ /app/scenarios/
COPY public/ /app/public/
COPY docker-entrypoint.sh /app/
COPY start.sh /app/

# 创建必要目录
RUN mkdir -p /app/data /app/models /app/logs /app/configs /app/scenarios /app/tmp     && chmod +x /app/docker-entrypoint.sh /app/start.sh

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3     CMD curl -fsSL http://localhost:8080/health || exit 1

# 暴露端口
EXPOSE 8080

# 入口脚本
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["start"]
