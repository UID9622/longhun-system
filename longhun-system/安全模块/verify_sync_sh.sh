#!/bin/bash
# 一键校验 sync_to_icloud.sh 完整性
TARGET="$HOME/Desktop/龍魂操作日志/sync_to_icloud.sh"
BASELINE="$HOME/longhun-system/security/checksums/sync_to_icloud.sha256"
EXPECTED=$(head -1 "$BASELINE" | awk '{print $1}')
ACTUAL=$(shasum -a 256 "$TARGET" | awk '{print $1}')

if [ "$EXPECTED" = "$ACTUAL" ]; then
    echo "✅ 完整性校验通过"
    echo "   SHA256: $ACTUAL"
else
    echo "🔴 警告！文件已被篡改"
    echo "   期望: $EXPECTED"
    echo "   实际: $ACTUAL"
fi
