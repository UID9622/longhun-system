# 🐉 longhun-cli 网关容器镜像
# DNA: #龍芯⚡️丙午·丁酉·乙亥·巳时·䷝离-DOCKERFILE-v1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 配套: docker-compose.yml（同目录）

FROM python:3.12-slim

# healthcheck 需要 curl
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 只复制运行网关所需的核心层（完整系统建议宿主机运行）
COPY bin/ /app/bin/
COPY 08_BIN/ /app/08_BIN/
COPY packaging/ /app/packaging/
COPY docs/ /app/docs/
COPY CHANGELOG.md /app/CHANGELOG.md

# 安装对外薄壳（可独立使用 lh flow/bazi/health）
RUN pip install --no-deps --quiet /app/packaging/longhun_cli || true

EXPOSE 9622

# 前台运行网关（容器内不要 --daemon，daemon 会让主进程退出）
# --host 0.0.0.0: 容器网络命名空间与宿主隔离，需开放才能被 -p 映射访问；
# 对外开放后外部调用自动写入 /root/.longhun/logs/external_calls.log（归一审计）
CMD ["python3", "/app/08_BIN/lh_api.py", "--host", "0.0.0.0"]
