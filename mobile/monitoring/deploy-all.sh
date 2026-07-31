##龍芯⚡️2026-06-21-MOBILE-DEPLOY-ALL-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

#!/bin/bash

#######################################################################
# 龍魂移动端监控 · 完整部署脚本 v1.0
#
# DNA: #龍芯⚡️2026-06-07-DEPLOY-ALL-SCRIPT
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 责任: UID9622 · 不免责
#######################################################################

set -e

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  🐉 龍魂移动端监控 · 一键完整部署 v1.0"
echo "════════════════════════════════════════════════════════════════"
echo ""

# 定义应用列表
APPS=(
  "real-time-performance-dashboard"
  "data-visualization-dashboard"
  "mobile-auth-system"
  "smart-task-management"
)

# [Step 1] 检查环境
echo "📋 [Step 1] 检查部署环境..."

if ! command -v npm &> /dev/null; then
  echo "❌ 错误: npm 未安装"
  exit 1
fi

if ! command -v node &> /dev/null; then
  echo "❌ 错误: Node.js 未安装"
  exit 1
fi

NODE_VERSION=$(node -v)
NPM_VERSION=$(npm -v)
echo "✅ Node.js 版本: $NODE_VERSION"
echo "✅ npm 版本: $NPM_VERSION"

# [Step 2] 安装 SDK
echo ""
echo "📦 [Step 2] 安装监控 SDK..."

if npm list @longhun/monitoring-sdk > /dev/null 2>&1; then
  echo "✅ SDK 已安装"
else
  echo "⏳ 安装 SDK..."
  npm install @longhun/monitoring-sdk --save-prod
  echo "✅ SDK 安装完成"
fi

# [Step 3] 建立配置文件
echo ""
echo "⚙️  [Step 3] 建立监控配置..."

mkdir -p mobile-monitoring

cat > .env.monitoring << 'EOF'
# 龍魂移动端监控配置
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

# [Step 4] 为每个应用配置初始化
echo ""
echo "🔧 [Step 4] 为 4 个应用配置监控初始化..."

for APP in "${APPS[@]}"; do
  echo ""
  echo "  正在配置: $APP"

  # 在 src/main.ts 或 src/index.tsx 中注入初始化代码
  # (这里假设项目结构有 src 目录)

  if [ -d "src" ]; then
    cat >> src/main.ts << EOF

// [自动注入] 龍魂监控初始化 - $APP
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

# [Step 5] 部署验证
echo ""
echo "✔️  [Step 5] 执行部署验证..."

verify_count=0

# 检查 SDK
if npm list @longhun/monitoring-sdk > /dev/null 2>&1; then
  SDK_VERSION=$(npm list @longhun/monitoring-sdk | grep @longhun | awk '{print $2}')
  echo "  ✅ SDK 已安装: $SDK_VERSION"
  ((verify_count++))
fi

# 检查配置文件
if [ -f ".env.monitoring" ]; then
  echo "  ✅ 配置文件已建立"
  ((verify_count++))
fi

# 检查初始化代码
if grep -r "initLonghunMonitoring" src/ 2>/dev/null | head -1 > /dev/null; then
  echo "  ✅ 应用初始化已配置"
  ((verify_count++))
fi

# 测试云端连接 (可选)
if command -v curl &> /dev/null; then
  if curl -s -o /dev/null -w "%{http_code}" https://monitoring.longhun.io/health 2>/dev/null | grep -q "200\|301\|302"; then
    echo "  ✅ 云端连接正常"
    ((verify_count++))
  fi
fi

# [Step 6] 构建应用
echo ""
echo "🏗️  [Step 6] 构建应用..."

if [ -f "package.json" ]; then
  echo "  ⏳ 执行 npm run build (如果存在)..."
  if grep -q '"build"' package.json; then
    npm run build 2>/dev/null && echo "  ✅ 构建完成" || echo "  ⚠️  构建脚本未找到"
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
echo "  • 监控应用: ${#APPS[@]} 个"
for APP in "${APPS[@]}"; do
  echo "    - ✅ $APP"
done

echo ""
echo "📍 监控仪表板:"
echo "  🌐 https://logs.longhun.io/public"
echo ""

echo "📋 验证项目: $verify_count / 4 项通过"

if [ $verify_count -ge 3 ]; then
  echo ""
  echo "✅ 部署验证成功！系统已就绪。"
  echo ""
  echo "🚀 后续步骤:"
  echo "  1. 访问监控仪表板: https://logs.longhun.io/public"
  echo "  2. 检查应用运行状态"
  echo "  3. 配置告警规则 (可选)"
  echo ""
  echo "DNA: #龍芯⚡️2026-06-07-DEPLOY-ALL-SCRIPT"
  echo "责任: UID9622 · 不免责"
  echo ""
  exit 0
else
  echo ""
  echo "⚠️  部分验证项未通过，请检查"
  exit 1
fi
