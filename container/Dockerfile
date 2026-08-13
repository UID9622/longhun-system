# 🐉 龍魂系统 · 容器化底座
# DNA: #龍芯⚡️丙午·丙酉·壬戌·亥时·䷬萃-LONGHUN-CONTAINER-v1.0-UID9622
# 用途：把 longhun-system 核心能力打包为可运行容器
#       完整功能放 /app，不完整/实验性功能放 /app/sandbox

FROM python:3.12-slim

LABEL maintainer="UID9622"
LABEL dna="#龍芯⚡️丙午·丙酉·壬戌·亥时·䷬萃-LONGHUN-CONTAINER-v1.0-UID9622"
LABEL confirm="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gnupg \
    sqlite3 \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 工作目录
WORKDIR /app

# 先复制依赖清单，利用 Docker 缓存层
COPY container/requirements.txt /app/container/requirements.txt
RUN pip install --no-cache-dir -r /app/container/requirements.txt

# 复制核心代码（.dockerignore 控制不复制大目录）
COPY . /app

# 创建沙盒目录，用于隔离不完整/实验性功能
RUN mkdir -p /app/sandbox /app/data /app/logs

# 设置环境变量
ENV PYTHONPATH=/app
ENV LONGHUN_ROOT=/app
ENV LONGHUN_DATA=/app/data
ENV LONGHUN_LOGS=/app/logs
ENV LONGHUN_SANDBOX=/app/sandbox

# 健康检查
HEALTHCHECK --interval=60s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.path.insert(0,'/app'); from core.longhun_core.dna_trace import generate_dna; print(generate_dna('HEALTHCHECK','UID9622'))" || exit 1

# 默认入口：展示帮助
CMD ["python3", "/app/08_BIN/lh_notion.py", "--help"]
