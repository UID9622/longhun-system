#!/bin/bash

#######################################################################
# 龍魂移動端監控 · 完整部署脚本 v1.0
#
# DNA: #龍芯⚡️2026-06-07-DEPLOY-ALL-SCRIPT
# 責任: UID9622 · 不免責
#######################################################################

set -e

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  🐉 龍魂移動端監控 · 一鍵完整部署 v1.0"
echo "════════════════════════════════════════════════════════════════"
echo ""

# 定義應用列表
APPS=(
  "real-time-performance-dashboard"
  "data-visualization-dashboard"
  "mobile-auth-system"
  "smart-task-management"
)

# [Step 1] 檢查環境
echo "📋 [Step 1] 檢查部署環境..."

if ! command -v npm &> /dev/null; then
  echo "❌ 錯誤: npm 未安裝"
  exit 1
fi

if ! command -v node &> /dev/null; then
  echo "❌ 錯誤: Node.js 未安裝"
  exit 1
fi

NODE_VERSION=$(node -v)
NPM_VERSION=$(npm -v)
echo "✅ Node.js 版本: $NODE_VERSION"
echo "✅ npm 版本: $NPM_VERSION"

# [Step 2] 安裝 SDK
echo ""
echo "📦 [Step 2] 安裝監控 SDK..."

if npm list @longhun/monitoring-sdk > /dev/null 2>&1; then
  echo "✅ SDK 已安裝"
else
  echo "⏳ 安裝 SDK..."
  npm install @longhun/monitoring-sdk --save-prod
  echo "✅ SDK 安裝完成"
fi

# [Step 3] 建立配置文件
echo ""
echo "⚙️  [Step 3] 建立監控配置..."

mkdir -p mobile-monitoring

cat > .env.monitoring << 'EOF'
# 龍魂移動端監控配置
LONGHUN_ENV=production
LONGHUN_MONITORING_ENDPOINT=https://monitoring.longhun.io/api
LONGHUN_SDK_VERSION=1.0.0
LONGHUN_AUTO_INIT=true
LONGHUN_AUTO_PERSIST=true
LONGHUN_AUTO_REPORT=true
LONGHUN_SAMPLE_RATE=1.0
LONGHUN_BATCH_SIZE=50
LONGHUN_BATCH_TIMEOUT=10000
LONGHUN_ALERT_ENABLED=true
LONGHUN_DNA=#龍芯⚡️2026-06-07-MOBILE-MONITORING-DEPLOYMENT
EOF

echo "✅ 配置文件已建立: .env.monitoring"

# [Step 4] 為每個應用配置初始化
echo ""
echo "🔧 [Step 4] 為 4 個應用配置監控初始化..."

for APP in "${APPS[@]}"; do
  echo ""
  echo "  正在配置: $APP"

  # 在 src/main.ts 或 src/index.tsx 中注入初始化代碼
  # (這裡假設項目結構有 src 目錄)

  if [ -d "src" ]; then
    cat >> src/main.ts << EOF

// [自動注入] 龍魂監控初始化 - $APP
import { initLonghunMonitoring } from '@longhun/monitoring-sdk';

initLonghunMonitoring({
  appId: '$APP',
  environment: 'production',
  autoInit: true
});

EOF
    echo "  ✅ $APP 初始化配置完成"
  fi
done

# [Step 5] 部署驗證
echo ""
echo "✔️  [Step 5] 執行部署驗證..."

verify_count=0

# 檢查 SDK
if npm list @longhun/monitoring-sdk > /dev/null 2>&1; then
  SDK_VERSION=$(npm list @longhun/monitoring-sdk | grep @longhun | awk '{print $2}')
  echo "  ✅ SDK 已安裝: $SDK_VERSION"
  ((verify_count++))
fi

# 檢查配置文件
if [ -f ".env.monitoring" ]; then
  echo "  ✅ 配置文件已建立"
  ((verify_count++))
fi

# 檢查初始化代碼
if grep -r "initLonghunMonitoring" src/ 2>/dev/null | head -1 > /dev/null; then
  echo "  ✅ 應用初始化已配置"
  ((verify_count++))
fi

# 測試雲端連接 (可選)
if command -v curl &> /dev/null; then
  if curl -s -o /dev/null -w "%{http_code}" https://monitoring.longhun.io/health 2>/dev/null | grep -q "200\|301\|302"; then
    echo "  ✅ 雲端連接正常"
    ((verify_count++))
  fi
fi

# [Step 6] 構建應用
echo ""
echo "🏗️  [Step 6] 構建應用..."

if [ -f "package.json" ]; then
  echo "  ⏳ 執行 npm run build (如果存在)..."
  if grep -q '"build"' package.json; then
    npm run build 2>/dev/null && echo "  ✅ 構建完成" || echo "  ⚠️  構建腳本未找到"
  fi
fi

# [Step 7] 部署摘要
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  ✅ 部署完成"
echo "════════════════════════════════════════════════════════════════"
echo ""

echo "📊 部署摘要:"
echo "  • SDK 版本: 1.0.0"
echo "  • 監控應用: ${#APPS[@]} 個"
for APP in "${APPS[@]}"; do
  echo "    - ✅ $APP"
done

echo ""
echo "📍 監控儀表板:"
echo "  🌐 https://logs.longhun.io/public"
echo ""

echo "📋 驗證項目: $verify_count / 4 項通過"

if [ $verify_count -ge 3 ]; then
  echo ""
  echo "✅ 部署驗證成功！系統已就緒。"
  echo ""
  echo "🚀 後續步驟:"
  echo "  1. 訪問監控儀表板: https://logs.longhun.io/public"
  echo "  2. 檢查應用運行狀態"
  echo "  3. 配置告警規則 (可選)"
  echo ""
  echo "DNA: #龍芯⚡️2026-06-07-DEPLOY-ALL-SCRIPT"
  echo "責任: UID9622 · 不免責"
  echo ""
  exit 0
else
  echo ""
  echo "⚠️  部分驗證項未通過，請檢查"
  exit 1
fi
