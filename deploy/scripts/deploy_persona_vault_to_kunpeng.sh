#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂·人格路由 + 保险柜 API 鲲鹏部署脚本
# DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-DEPLOY-PERSONA-VAULT-KUNPENG-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
set -e

echo "=== 部署龍魂人格路由 + 保险柜 API 到鲲鹏 ==="

# 复制服务文件
sudo cp /opt/longhun-system/deploy/scripts/longhun-persona-api.service /etc/systemd/system/
sudo cp /opt/longhun-system/deploy/scripts/longhun-vault-api.service /etc/systemd/system/

# 重载 systemd
sudo systemctl daemon-reload

# 启动并启用
sudo systemctl enable longhun-persona-api longhun-vault-api
sudo systemctl restart longhun-persona-api longhun-vault-api

sleep 2

# 健康检查
echo ""
echo "健康检查:"
curl -s http://127.0.0.1:8779/health | python3 -m json.tool || echo "persona-api 未响应"
curl -s http://127.0.0.1:8780/health | python3 -m json.tool || echo "vault-api 未响应"

echo ""
echo "=== 部署完成 ==="
