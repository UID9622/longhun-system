# 🐉 龍魂系统 · 可交付容器镜像 Dockerfile
# DNA: #龍芯⚡️2026-09-03-ECOSYSTEM-DOCKERFILE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）· 龍芯北辰
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
#
# 用法:
#   docker build -t longhun:latest .
#   docker run --rm longhun:latest health          # 一键自检
#   docker run --rm longhun:latest topo verify 通心译
#   docker compose up -d                           # core/api/topo 三服务

# python:3.12-slim（较 3.11 更新 digest·规避镜像层已知高危告警；3.11→3.12 语法完全兼容）
FROM python:3.12-slim

# 最小运行时: curl(健康检查) + git(脚本兼容) · 其余零三方依赖(M77)
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

ENV PYTHONPATH=/app \
    LANG=C.UTF-8 \
    LONGHUN_UID=UID9622 \
    LONGHUN_OWNER="Zhuge-Xin-UID9622"

# 非 root 用户运行（安全基线）
RUN useradd -m -s /bin/bash longhun \
    && mkdir -p /home/longhun/.longhun \
    && chown -R longhun:longhun /app /home/longhun/.longhun
USER longhun
ENV HOME=/home/longhun

# 默认命令: docker run longhun → 一键健康自检；覆盖 CMD 即可执行任意 lh 子命令
CMD ["python3", "/app/08_BIN/lh.py", "health"]
