#!/usr/bin/env bash
# ============================================================
# 龍魂 · 视频工坊 / 引擎主控仪表盘 · 鲲鹏服务器一键部署
# DNA: #龍芯⚡️丙午·辛未·DEPLOY-VIDEO-STUDIO-KUNPENG-v1.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 目标: 119.13.90.27 (华为云 / 鲲鹏节点)
# 功能: 把按钮版视频工坊和数据大屏部署到公网，直接用网页生成视频
# 变更: v1.1 严格白名单同步，防止敏感目录外传；nginx 改为修改 00-default-ip.conf
# ============================================================

set -euo pipefail

DNA="#龍芯⚡️丙午·辛未·DEPLOY-VIDEO-STUDIO-KUNPENG-v1.0"
SERVER="root@119.13.90.27"
SSH_KEY="${HOME}/.ssh/longhun_kunpeng_ed25519"
REMOTE_ROOT="/opt/longhun"
NGINX_CONF="/etc/nginx/conf.d/longhun.conf"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log(){ echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $1"; }
warn(){ echo -e "${YELLOW}[WARN]${NC} $1"; }
error(){ echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

[ -f "$SSH_KEY" ] || error "SSH 密钥不存在: $SSH_KEY"
command -v rsync >/dev/null 2>&1 || error "本机需要安装 rsync"

log "开始部署: $SERVER"

# ── 1. 同步代码到服务器（严格白名单，防止敏感/大目录外传） ──
log "同步项目文件到 ${REMOTE_ROOT} ..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=accept-new "$SERVER" "mkdir -p ${REMOTE_ROOT}"

# 只同步视频工坊/仪表盘运行必需的最小集合
rsync -avz --delete \
  -e "ssh -i ${SSH_KEY} -o StrictHostKeyChecking=accept-new" \
  --include='/bin/' \
  --include='/bin/***' \
  --include='/portal/' \
  --include='/portal/***' \
  --include='/engines/' \
  --include='/engines/***' \
  --include='/requirements.txt' \
  --include='/requirements-base.txt' \
  --include='/pyproject.toml' \
  --exclude='*' \
  "$(pwd)/" "${SERVER}:${REMOTE_ROOT}/"

# ── 2. 服务器端安装依赖、配置、启动服务 ────────────────────
log "在服务器上安装依赖并配置服务..."
ssh -i "$SSH_KEY" "$SERVER" bash -s <<'REMOTE'
set -euo pipefail
REMOTE_ROOT="/opt/longhun"
VENV="${REMOTE_ROOT}/venv"

# 创建虚拟环境并安装依赖
if [ ! -d "$VENV" ]; then
    python3 -m venv "$VENV"
fi
"$VENV/bin/pip" install --upgrade pip
"$VENV/bin/pip" install -q \
    edge-tts moviepy pillow numpy \
    flask pyyaml click rich apscheduler requests

# 创建视频输出目录
mkdir -p "${REMOTE_ROOT}/videos"
mkdir -p "${REMOTE_ROOT}/data/3d_forge"

# 创建服务器端统一配置
mkdir -p /root/.longhun
cat > /root/.longhun/config.yaml <<'CFG'
# 龍魂引擎主控 · 服务器配置
# DNA: #龍芯⚡️丙午·丙申·癸酉·庚申·临-LH-CTL-CONFIG-SERVER-v1.0

longhun:
  root: /opt/longhun
  logs_dir: /opt/longhun/logs/lh_ctl
  state_dir: /opt/longhun/state

notion:
  integration_token: ""
  engine_registry_db_id: ""

engines:
  search:
    script: bin/lh_search_engine.py
    description: 龍魂搜索引擎
    output_dir: data/search_results
    default_args:
      query: ""
  video:
    script: bin/lh_video_studio.py
    description: 龍魂视频工坊
    output_dir: videos
    default_args:
      script: ""
      style: 龍魂
      name: output
  distill:
    script: bin/lh_k3_distill_v39.py
    description: K3 教师模型蒸馏
    output_dir: models/longhun-v1.0/lora_output/k3_distill_v39
    default_args:
      mock: false
      local: false
  audit:
    script: bin/lh_sg_auditor.py
    description: 语义安全闸审计
    output_dir: data/audit
    default_args:
      target: ""
  3d:
    script: bin/lh_3d_pipeline.py
    description: 龍魂图生三维引擎
    output_dir: data/3d_forge
    default_args:
      input: ""
      category: object
      style: realistic

web:
  host: 127.0.0.1
  port: 9630
  dashboard_html: portal/dashboard/index.html

schedule:
  db_path: /opt/longhun/state/scheduler.sqlite
CFG

# 写入 systemd 服务
for svc in longhun-video-gallery longhun-ctl-web; do
    systemctl stop "$svc" 2>/dev/null || true
done

cat > /etc/systemd/system/longhun-video-gallery.service <<'SVC'
[Unit]
Description=龍魂视频工坊画廊服务
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/longhun
ExecStart=/opt/longhun/venv/bin/python3 bin/lh_video_index.py --serve :8788
Restart=always
RestartSec=5
Environment=PATH=/opt/longhun/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

[Install]
WantedBy=multi-user.target
SVC

cat > /etc/systemd/system/longhun-ctl-web.service <<'SVC'
[Unit]
Description=龍魂引擎主控仪表盘
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/longhun
ExecStart=/opt/longhun/venv/bin/python3 bin/lh_ctl_web.py --host 127.0.0.1 --port 9630
Restart=always
RestartSec=5
Environment=PATH=/opt/longhun/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

[Install]
WantedBy=multi-user.target
SVC

systemctl daemon-reload
systemctl enable longhun-video-gallery longhun-ctl-web
systemctl start longhun-video-gallery longhun-ctl-web

# 等待服务启动
sleep 3
REMOTE

# ── 3. 配置 nginx ──────────────────────────────────────────
log "配置 nginx 反向代理..."
# IP 直连/默认站点使用专门配置，避免与 uid9622.cn.conf 冲突
ssh -i "$SSH_KEY" "$SERVER" bash -s <<'REMOTE'
set -euo pipefail
SRC="/opt/longhun/portal/nginx/00-default-ip-video-studio.conf"
DST="/etc/nginx/sites-enabled/00-default-ip.conf"
BAK="/etc/nginx/sites-enabled/00-default-ip.conf.bak.$(date +%Y%m%d%H%M%S)"

if [ -f "$DST" ]; then
    cp "$DST" "$BAK"
fi
cp "$SRC" "$DST"

# 清理可能冲突的备份文件
rm -f /etc/nginx/sites-enabled/*.bak

nginx -t && systemctl reload nginx
REMOTE

# ── 4. 健康检查 ────────────────────────────────────────────
log "执行公网健康检查..."
sleep 2
for url in \
  "http://119.13.90.27/video-studio/" \
  "http://119.13.90.27/api/videos" \
  "http://119.13.90.27/api/video-metrics" \
  "http://119.13.90.27/dashboard/" \
  "http://119.13.90.27/api/health"; do
    code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$url" || true)
    if [ "$code" = "200" ]; then
        log "  ✅ ${url} -> ${code}"
    else
        warn "  🟡 ${url} -> ${code:-失败}"
    fi
done

log "部署完成！"
echo ""
echo "🎬 视频工坊: http://119.13.90.27/video-studio/"
echo "📊 数据大屏: http://119.13.90.27/dashboard/"
echo ""
echo "后续管理服务："
echo "  systemctl status longhun-video-gallery"
echo "  systemctl status longhun-ctl-web"
echo "  journalctl -u longhun-video-gallery -f"
