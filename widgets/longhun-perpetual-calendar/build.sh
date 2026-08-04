#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂万年历构建脚本
# DNA: #龍芯⚡️2026-06-27-LONGHUN-CALENDAR-BUILD-v1.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

WIDGET_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🐉 龍魂万年历构建开始"

# 1. 生成 LonghunFont 实用字体（基于 Noto Sans SC，保留 Longhun 品牌名）
echo "🔤 正在构建 LonghunFont 字体..."
python3 "$WIDGET_DIR/build-font.py"

# 2. 计算文件哈希并写入清单
MANIFEST="$WIDGET_DIR/manifest.json"
echo "{" > "$MANIFEST"
echo "  \"dna\": \"#龍芯⚡️$(date +%Y%m%d%H%M%S)-LONGHUN-CALENDAR-MANIFEST-$(shasum -a 256 "$WIDGET_DIR/index.html" | cut -c1-8 | tr 'a-z' 'A-Z')\"," >> "$MANIFEST"
echo "  \"files\": {" >> "$MANIFEST"

FIRST=true
for f in index.html styles.css calendar.js sovereignty.js build-font.py README.md; do
    if [ "$FIRST" = true ]; then
        FIRST=false
    else
        echo "," >> "$MANIFEST"
    fi
    HASH=$(shasum -a 256 "$WIDGET_DIR/$f" | cut -c1-64 | tr 'a-z' 'A-Z')
    echo -n "    \"$f\": \"$HASH\"" >> "$MANIFEST"
done

echo "" >> "$MANIFEST"
echo "  }," >> "$MANIFEST"

# 字体文件单独列出（二进制，每次构建可能变化）
echo "  \"fonts\": {" >> "$MANIFEST"
FIRST=true
for f in LonghunFont-Regular.ttf LonghunFont-Regular.woff2; do
    if [ "$FIRST" = true ]; then
        FIRST=false
    else
        echo "," >> "$MANIFEST"
    fi
    HASH=$(shasum -a 256 "$WIDGET_DIR/$f" | cut -c1-64 | tr 'a-z' 'A-Z')
    echo -n "    \"$f\": \"$HASH\"" >> "$MANIFEST"
done
echo "" >> "$MANIFEST"
echo "  }," >> "$MANIFEST"
echo "  \"built_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"," >> "$MANIFEST"
echo "  \"builder\": \"UID9622\"" >> "$MANIFEST"
echo "}" >> "$MANIFEST"

echo "✅ 清单已生成: $MANIFEST"
echo "🎉 构建完成"
