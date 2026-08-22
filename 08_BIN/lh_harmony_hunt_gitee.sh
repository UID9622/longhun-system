#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷓观-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# 龍魂鸿蒙狩猎 · Gitee镜像版 v2
# GitHub不可达 → 走 Gitee mirrors

LH_ROOT="/Users/zuimeidedeyihan/longhun-system"
LOG="$LH_ROOT/L7_数据层/daoyin/harmony_hunt_gitee.log"
TMPDIR="/tmp/longhun_harmony_gitee"
mkdir -p "$TMPDIR"

echo "🏹 鸿蒙狩猎·Gitee镜像 · $(date)" | tee "$LOG"

repos=(
  "https://gitee.com/mirrors/ncnn|IPA-02,IPA-15"
  "https://gitee.com/mirrors/mnn|IPA-02,IPA-15"
  "https://gitee.com/mirrors/lvgl|IPA-15"
  "https://gitee.com/mirrors/wolfssl|IPA-77"
  "https://gitee.com/mirrors/optee_os|IPA-77,IPA-02"
)

done=0; fail=0; total=${#repos[@]}

for entry in "${repos[@]}"; do
  url="${entry%%|*}"; ipa="${entry##*|}"; name=$(basename "$url")
  dir="$TMPDIR/$name"
  rm -rf "$dir" 2>/dev/null
  
  echo "" | tee -a "$LOG"
  echo "📥 [$((done+fail+1))/$total] $name → $ipa" | tee -a "$LOG"
  
  echo "   clone..." | tee -a "$LOG"
  if git clone --depth 1 "$url" "$dir" >> "$LOG" 2>&1; then
    echo "   ✅ cloned" | tee -a "$LOG"
  else
    echo "   ❌ clone fail" | tee -a "$LOG"
    fail=$((fail+1)); continue
  fi

  echo "   absorb..." | tee -a "$LOG"
  if python3 "$LH_ROOT/bin/lh_daoyin.py" absorb "$dir" --ipa "$ipa" >> "$LOG" 2>&1; then
    echo "   ✅ absorbed" | tee -a "$LOG"
    done=$((done+1))
  else
    echo "   ❌ absorb fail" | tee -a "$LOG"
    fail=$((fail+1))
  fi
  rm -rf "$dir" 2>/dev/null
done

echo "" | tee -a "$LOG"
echo "🏁 $done/$total ok · $fail fail · $(date)" | tee -a "$LOG"
