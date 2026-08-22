#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# lh_cnsh_run.sh
# 龍魂 · CNSH 全语言终端直跑
# DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

FILE=$1
LANG=${2:-auto}

# 语言扩展名映射
case "${FILE##*.}" in
    cnsh)    LANG=zh ;;
    km)      LANG=km ;;
    ru)      LANG=ru ;;
    ar)      LANG=ar ;;
    fa)      LANG=fa ;;
    th)      LANG=th ;;
    pt)      LANG=pt ;;
    vi)      LANG=vi ;;
esac

echo "🐉 龍魂 CNSH 全语言编译器 v0.2"
echo "源文件: $FILE"
echo "检测语言: $LANG"
echo "DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️"

# 编译
python3 "$(dirname "$0")/lh_cnsh_compiler.py" \
    --input "$FILE" \
    --lang "$LANG" \
    --output /tmp/longhun_exec.py

# 执行
python3 /tmp/longhun_exec.py
