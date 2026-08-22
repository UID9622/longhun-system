#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷈小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# 龍魂·全远端推送脚本
# 用法: bash bin/lh_push_all.sh
echo "🐉 龍魂推送到所有远端..."
cd "$(dirname "$0")/.."
for remote in origin gitee gitcode; do
    echo "   → $remote..."
    git push $remote main 2>&1
done
echo "✅ 推送完成"
