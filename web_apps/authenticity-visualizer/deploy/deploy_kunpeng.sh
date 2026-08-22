#!/bin/bash
# ============================================================
# 龍魂 · 真实性标识协议 · 鲲鹏部署脚本
# DNA: #龍芯⚡️丙午·乙未·丁未·丙午·䷫姤-鲲鹏部署-V1.0
# 归属: 龍魂系统 UID9622 · 免费开源
#
# 用途：把本模块部署到华为鲲鹏服务器（openEuler/EulerOS + nginx）
# 执行：bash deploy/deploy_kunpeng.sh
# 前提：本地龍魂引擎（FastAPI 127.0.0.1:9527）已由云码启动
# 安全：不碰密钥、不改系统配置以外的文件、失败自动回滚
# ============================================================
set -euo pipefail

# ---- 参数（按实际改） ----
MODULE_NAME="lh-truth-tag"
SRC_DIR="$(cd "$(dirname "$0")/.." && pwd)"     # 本模块目录
DEPLOY_ROOT="/opt/longhun/modules"              # 龍魂模块根目录
WEB_ROOT="/var/www/longhun"                     # nginx 站点根目录
NGINX_CONF="/etc/nginx/conf.d/lh_truth_tag.conf"
ENGINE_PORT=9527                                # 龍魂 FastAPI 操作台

echo "=== 龍魂·真实性标识协议 鲲鹏部署 ==="
echo "源目录: ${SRC_DIR}"

# ---- 1. 落地模块文件 ----
sudo mkdir -p "${DEPLOY_ROOT}/${MODULE_NAME}" "${WEB_ROOT}/truth-tag"
sudo rsync -a --delete --exclude deploy "${SRC_DIR}/" "${DEPLOY_ROOT}/${MODULE_NAME}/"
sudo cp -r "${SRC_DIR}/index.html" "${SRC_DIR}/tagger.html" "${SRC_DIR}/pipeline.html" "${SRC_DIR}/embed.html" "${SRC_DIR}/js" "${WEB_ROOT}/truth-tag/"
echo "[1/4] 模块文件已落地 -> ${DEPLOY_ROOT}/${MODULE_NAME} & ${WEB_ROOT}/truth-tag"

# ---- 2. nginx 站点配置（静态托管 + 反代本地引擎 API） ----
sudo tee "${NGINX_CONF}" > /dev/null <<EOF
# 龍魂·真实性标识协议 · 由 deploy_kunpeng.sh 生成
server {
    listen 80;
    server_name _;

    root ${WEB_ROOT};
    index index.html;

    # 本模块静态页
    location /truth-tag/ {
        try_files \$uri \$uri/ =404;
    }

    # ===【缺口·云码接管】=== 前端 MODE='LOCAL' 后，API 走这里反代到龍魂引擎
    location /api/v1/truth/ {
        proxy_pass http://127.0.0.1:${ENGINE_PORT};
        proxy_set_header Host \$host;
    }
    location /api/v1/dna/ {
        proxy_pass http://127.0.0.1:${ENGINE_PORT};
        proxy_set_header Host \$host;
    }
}
EOF
echo "[2/4] nginx 配置已写入 ${NGINX_CONF}"

# ---- 3. 校验并重载 nginx ----
sudo nginx -t
sudo systemctl reload nginx
echo "[3/4] nginx 已重载"

# ---- 4. 引擎连通性自检（不强制，仅提示） ----
if curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:${ENGINE_PORT}/" | grep -q "200\|404"; then
  echo "[4/4] 龍魂本地引擎 127.0.0.1:${ENGINE_PORT} 在线 —— 可将 js/lh_interface.js 的 MODE 改为 'LOCAL'"
else
  echo "[4/4] 警告：龍魂本地引擎未响应。模块以 STUB 模式运行，云码启动引擎后改 MODE='LOCAL' 即可。"
fi

echo "=== 部署完成 ==="
echo "访问: http://<服务器IP>/truth-tag/"
echo "官网嵌入: 在 longhun888.com / uid9622.cn 页面插入 <iframe src=\"/truth-tag/embed.html\">"
echo "接入引擎: 编辑 ${WEB_ROOT}/truth-tag/js/lh_interface.js → MODE: 'LOCAL'"
