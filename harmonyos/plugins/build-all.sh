#!/bin/bash
# 🐉 龍魂·鸿蒙插件生态·全量一键构建
# DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-BUILD-ALL-HARMONYOS-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 主权锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="${SCRIPT_DIR}/output"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

echo "🐉 龍魂·鴻蒙插件生態·全量構建"
echo "DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-BUILD-ALL-HARMONYOS-UID9622"
echo "時間: ${TIMESTAMP}"
echo ""

mkdir -p "${OUTPUT_DIR}"

PLUGINS=(
  "01-core-service"
  "02-memory-browser"
  "03-supervision-dashboard"
  "04-evolution-monitor"
  "05-sovereignty-verifier"
  "06-cross-device-sync"
  "07-one-click-migrate"
  "08-widget-pack"
  "09-notification-service"
  "10-settings"
)

BUILD_COUNT=0
FAIL_COUNT=0
declare -A BUILD_RESULTS

for plugin in "${PLUGINS[@]}"; do
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "🔨 構建: ${plugin}"
  echo ""

  PLUGIN_DIR="${SCRIPT_DIR}/${plugin}"

  if [ ! -d "${PLUGIN_DIR}" ]; then
    echo "❌ ${plugin} 目錄不存在，跳過"
    FAIL_COUNT=$((FAIL_COUNT + 1))
    BUILD_RESULTS[${plugin}]="❌ 目錄缺失"
    continue
  fi

  cd "${PLUGIN_DIR}"

  # 检查是否有 hvigorw (鸿蒙构建工具)
  if [ -f "hvigorw" ] || command -v hvigorw &> /dev/null; then
    echo "  運行 hvigorw assembleHap..."
    if hvigorw assembleHap --mode module -p product=default 2>&1; then
      echo "  ✅ ${plugin} 構建成功"
      BUILD_COUNT=$((BUILD_COUNT + 1))
      BUILD_RESULTS[${plugin}]="✅ 成功"

      # 复制产物
      if ls build/outputs/default/*.hap 1> /dev/null 2>&1; then
        cp build/outputs/default/*.hap "${OUTPUT_DIR}/"
        echo "  📦 HAP已複製到 output/"
      fi
    else
      echo "  ❌ ${plugin} 構建失敗"
      FAIL_COUNT=$((FAIL_COUNT + 1))
      BUILD_RESULTS[${plugin}]="❌ 構建失敗"
    fi
  else
    echo "  🟡 hvigorw 未找到，跳過構建（源碼已就緒）"
    BUILD_RESULTS[${plugin}]="🟡 源碼模式"
  fi

  echo ""
done

cd "${SCRIPT_DIR}"

echo "═══════════════════════════════════════"
echo "📊 構建結果匯總"
echo "═══════════════════════════════════════"
for plugin in "${PLUGINS[@]}"; do
  printf "  %-35s %s\n" "${plugin}" "${BUILD_RESULTS[${plugin}]:-未執行}"
done
echo ""
echo "✅ 構建: ${BUILD_COUNT} | ❌ 失敗: ${FAIL_COUNT} | 🟡 源碼: $((10 - BUILD_COUNT - FAIL_COUNT))"
echo "📦 產物目錄: ${OUTPUT_DIR}"
echo ""

if [ ${FAIL_COUNT} -gt 0 ]; then
  echo "⚠️ 有插件構建失敗，請檢查日誌"
  exit 1
else
  echo "🐉 鴻蒙龍魂生態·全量構建完成 🟢"
fi
