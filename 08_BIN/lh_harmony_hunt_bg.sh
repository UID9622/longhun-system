#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 · 鸿蒙生态后台狩猎脚本 v2
# DNA: #龍芯⚡️丙午·乙未·丁巳·亥时·需-LH-HARMONY-HUNT-BG-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
set -e
PROJECT_ROOT="/Users/zuimeidedeyihan/longhun-system"
DAOYIN="$PROJECT_ROOT/bin/lh_daoyin.py"
TMPDIR="/tmp/longhun_harmony_hunt"
LOG="$PROJECT_ROOT/L7_数据层/daoyin/harmony_hunt_bg.log"
mkdir -p "$TMPDIR"
echo "🚀 鸿蒙狩猎后台启动 $(date)" | tee "$LOG"

# 格式: URL|IPA
REPOS=(
  "https://github.com/Tencent/ncnn|IPA-02,IPA-15"
  "https://github.com/alibaba/MNN|IPA-02,IPA-15"
  "https://github.com/lvgl/lvgl|IPA-15"
  "https://github.com/wolfSSL/wolfssl|IPA-77"
  "https://github.com/OP-TEE/optee_os|IPA-77,IPA-02"
)

for entry in "${REPOS[@]}"; do
  URL="${entry%|*}"
  IPA="${entry#*|}"
  NAME=$(basename "$URL")
  echo "" | tee -a "$LOG"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG"
  echo "📥 [$NAME] → $IPA" | tee -a "$LOG"
  
  CLONE_DIR="$TMPDIR/$NAME"
  if [ -d "$CLONE_DIR/.git" ]; then
    echo "   已克隆，跳过" | tee -a "$LOG"
  else
    rm -rf "$CLONE_DIR" 2>/dev/null || true
    echo "   git clone --depth 1..." | tee -a "$LOG"
    git clone --depth 1 "$URL" "$CLONE_DIR" 2>&1 | tail -3 | tee -a "$LOG"
  fi
  
  echo "   daoyin absorb..." | tee -a "$LOG"
  python3 "$DAOYIN" absorb "$CLONE_DIR" --ipa "$IPA" 2>&1 | tee -a "$LOG"
  
  echo "✅ [$NAME] 完成" | tee -a "$LOG"
done

echo "" | tee -a "$LOG"
echo "🏁 鸿蒙狩猎后台完成 $(date)" | tee -a "$LOG"
python3 "$DAOYIN" report 2>&1 | tee -a "$LOG"
