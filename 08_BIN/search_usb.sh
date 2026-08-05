#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·观-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# 龍魂 USB 备份搜索引擎 — 本地一键搜索
# 用法: ./bin/search_usb.sh "关键词"

QUERY="$*"
if [ -z "$QUERY" ]; then
    echo "用法: ./bin/search_usb.sh \"关键词\""
    echo "示例: ./bin/search_usb.sh \"UID9622 龍魂\""
    exit 1
fi

ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27 \
  "python3 /usr/local/bin/lh_usb_search_index.py search \"$QUERY\" --db /data/usb_backup_index/search.db" \
  2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
for item in data:
    print(f\"📄 {item['name']}\")
    print(f\"   📍 {item['path']}\")
    print(f\"   📝 {item['snippet']}\")
    print()
print(f'共 {len(data)} 条结果')
"
