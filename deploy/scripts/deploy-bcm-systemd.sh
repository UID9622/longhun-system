#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丁未·戊申·戊午·巳时·䷀乾-BCM-SYSTEMD-DEPLOY-v1.0
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2
# 部署行為密碼學 API systemd 服務到鲲鹏

set -e

KUNPENG="root@119.13.90.27"
SERVICE_NAME="longhun-bcm-api"
SERVICE_FILE="deploy/systemd/${SERVICE_NAME}.service"
SSH_KEY="${HOME}/.ssh/longhun_kunpeng_ed25519"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🔬 部署行為密碼學API systemd服務"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. 複製服務文件到鲲鹏
echo "📋 複製 systemd 服務文件..."
scp -i "$SSH_KEY" "$SERVICE_FILE" "${KUNPENG}:/etc/systemd/system/${SERVICE_NAME}.service"

# 2. 重載 systemd 配置
echo "🔄 重載 systemd..."
ssh -i "$SSH_KEY" "$KUNPENG" "systemctl daemon-reload"

# 3. 啟用開機自啟
echo "🚀 啟用開機自啟..."
ssh -i "$SSH_KEY" "$KUNPENG" "systemctl enable ${SERVICE_NAME}"

# 4. 啟動服務
echo "▶️  啟動服務..."
ssh -i "$SSH_KEY" "$KUNPENG" "systemctl restart ${SERVICE_NAME}"

# 5. 狀態檢查
echo "📡 狀態檢查..."
sleep 2
ssh -i "$SSH_KEY" "$KUNPENG" "systemctl status ${SERVICE_NAME} --no-pager" || true

# 6. API 測試
echo "🧪 API測試..."
sleep 2
curl -s http://119.13.90.27:8775/api/v2/bcm/health 2>&1 || echo "⚠️ API 尚未響應（可能需要等待啟動）"

echo ""
echo "✅ 部署完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
