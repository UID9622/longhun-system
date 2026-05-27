#!/bin/bash

# 🐉 快速創建新實驗
# DNA: #龍芯⚡️2026-05-28-NEW-EXPERIMENT-TOOL-UID9622-v1.0

if [ -z "$1" ]; then
    echo "用法: ./new_experiment.sh <實驗名稱>"
    echo ""
    echo "例子:"
    echo "  ./new_experiment.sh boundary_test_01"
    echo "  ./new_experiment.sh poc_new_idea"
    echo "  ./new_experiment.sh hack_optimization"
    exit 1
fi

實驗名稱="$1"
日期=$(date +"%Y-%m-%d")
時間=$(date +"%Y-%m-%d %H:%M:%S")

# 創建文件
文件名="experiments/test_${實驗名稱}.py"

if [ -f "$文件名" ]; then
    echo "❌ 文件已存在: $文件名"
    exit 1
fi

cat > "$文件名" << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
【本地實驗】

DNA: #龍芯⚡️%DATE%-TEST-%EXPNAME%-UID9622-v1.0
創建時間: %TIME%
創建者: UID9622
狀態: 🔴實驗中

【目的】
寫你的目的...

【方法】
怎麼做...

【預期】
希望看到什麼...
"""

import sys
from datetime import datetime

def main():
    print("\n" + "="*80)
    print("🐉 實驗開始: %EXPNAME%")
    print("="*80)
    print()

    # 你的代碼寫這裡
    try:
        print("✅ 測試成功")
    except Exception as e:
        print(f"🔴 測試失敗: {e}")

    print()
    print("="*80)
    print(f"✅ 實驗結束 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    print()

if __name__ == '__main__':
    main()
EOF

# 替換佔位符
sed -i '' "s/%DATE%/$(date +%Y-%m-%d)/g" "$文件名"
sed -i '' "s/%TIME%/$時間/g" "$文件名"
sed -i '' "s/%EXPNAME%/$實驗名稱/g" "$文件名"

# 可執行權限
chmod +x "$文件名"

echo "✅ 創建成功!"
echo ""
echo "📍 文件: $文件名"
echo ""
echo "【下一步】"
echo "  1. 編輯: nano $文件名"
echo "  2. 運行: python3 $文件名"
echo "  3. 記錄: nano dna_log.md (添加一行)"
echo ""
