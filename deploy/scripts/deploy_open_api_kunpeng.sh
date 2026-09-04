#!/bin/bash
# DNA: #龍芯⚡️2026-09-04-OPEN-API-DEPLOY-v1.0-9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# 🐉 龍魂开放 API 网关一键部署（剩余步骤 · 2026-09-04）
# 前置已完成(rsync): 代码+数据已推送 /apps/lh-api/（lh_api/lh_topo/lh_webhook + docs/topology + data 镜像）
# 本脚本: ①镜像改名 ②systemd lh-api.service:8761 ③admin keygen(首次)
#         ④nginx zone api_v1 10r/s ⑤/api/v1/ 反代(不剥前缀) ⑥外网验证
# 运行: bash deploy/scripts/deploy_open_api_kunpeng.sh   （需本机 ssh 批准）
set -euo pipefail

SSH_KEY=~/.ssh/longhun_kunpeng_ed25519
R=root@119.13.90.27
SSH() { ssh -i "$SSH_KEY" -o ConnectTimeout=15 "$R" "$@"; }

TMPD=$(mktemp -d)
trap 'rm -rf "$TMPD"' EXIT

cat > "$TMPD/lh-api.service" <<'UNIT'
[Unit]
Description=LongHun Open API Gateway (lh-api v4.2 /api/v1)
After=network.target

[Service]
WorkingDirectory=/apps/lh-api
ExecStart=/usr/bin/python3 /apps/lh-api/08_BIN/lh_api.py --port 8761 --host 127.0.0.1 --log-level info
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
UNIT

cat > "$TMPD/api-location.inc" <<'INC'
    # 龍魂开放 API 网关 v2.2 · /api/v1/ → 127.0.0.1:8761 (2026-09-04)
    location /api/v1/ {
        proxy_pass http://127.0.0.1:8761;
        limit_req zone=api_v1 burst=20 nodelay;
    }
INC

scp -q -i "$SSH_KEY" "$TMPD/lh-api.service" "$TMPD/api-location.inc" "$R":/tmp/

SSH 'bash -s' <<'REMOTE'
set -euo pipefail
echo "── 1/4 镜像改名"
mv -f /apps/lh-api/data/shame_wall_mirror.json /apps/lh-api/data/shame_wall.json 2>/dev/null || true
ls -la /apps/lh-api/data/

echo "── 2/4 systemd lh-api"
if ! systemctl is-active --quiet lh-api; then
  cp /tmp/lh-api.service /etc/systemd/system/lh-api.service
  systemctl daemon-reload
  systemctl enable --now lh-api
  sleep 2
fi
systemctl is-active lh-api

echo "── 3/4 admin API Key(首次)"
if [ ! -s /root/.longhun/api_keys.json ]; then
  python3 /apps/lh-api/08_BIN/lh_api.py --keygen --role admin --name UID9622-open-platform
else
  echo "api_keys.json 已存在，跳过签发"
fi
echo "── 内网自测"
curl -s http://127.0.0.1:8761/api/v1/health | head -c 220; echo
curl -s -o /dev/null -w 'topo:%{http_code} ' http://127.0.0.1:8761/api/v1/v1/topo
curl -s -o /dev/null -w 'shamewall:%{http_code} ' http://127.0.0.1:8761/api/v1/v1/judge/shamewall
curl -s -o /dev/null -w 'memorial:%{http_code} ' http://127.0.0.1:8761/api/v1/v1/memorial/verify
curl -s -X POST -o /dev/null -w 'scan-nokey:%{http_code}\n' http://127.0.0.1:8761/api/v1/v1/judge/scan

echo "── 4/4 nginx 反代+限流"
grep -q 'zone=api_v1' /etc/nginx/conf.d/00-limit-zones.conf \
  || echo 'limit_req_zone $binary_remote_addr zone=api_v1:10m rate=10r/s;' >> /etc/nginx/conf.d/00-limit-zones.conf
cp /tmp/api-location.inc /etc/nginx/conf.d/api-location.inc
grep -q 'api-location.inc' /etc/nginx/conf.d/nginx-uid9622.cn.conf \
  || sed -i '/topo-location.inc;/a\    include /etc/nginx/conf.d/api-location.inc;' /etc/nginx/conf.d/nginx-uid9622.cn.conf
cp /etc/nginx/conf.d/nginx-uid9622.cn.conf /etc/nginx/conf.d/nginx-uid9622.cn.conf.bak-api-20260904
nginx -t
systemctl reload nginx
echo "NGINX-OK"
REMOTE

echo "═══ 外网验证 ═══"
for p in health v1/topo v1/judge/shamewall v1/memorial/verify; do
  curl -s -o /dev/null -w "https://uid9622.cn/api/v1/$p → %{http_code}\n" "https://uid9622.cn/api/v1/$p"
done
curl -s -X POST -o /dev/null -w "scan 无key → %{http_code} (应 401)\n" https://uid9622.cn/api/v1/v1/judge/scan
echo "完成。详情见 docs/龙魂API集成指南-v1.0.md"
