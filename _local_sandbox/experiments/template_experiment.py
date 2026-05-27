#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
【本地實驗模板】UID9622私人沙盒

複製這個文件做你的實驗:
  cp template_experiment.py test_xxx.py
  然後改成你想做的

DNA: #龍芯⚡️2026-05-28-EXPERIMENT-TEMPLATE-UID9622-v1.0
創建者: UID9622
規則: 土方法·帶DNA·市場出現我認·出問題我承擔

【使用方式】
1. 複製這個文件: cp template_experiment.py test_xxx.py
2. 改你的想法和代碼
3. 運行: python3 test_xxx.py
4. 有收穫就記到 dna_log.md
"""

import sys
from datetime import datetime

# ============================================================================
# 【你的實驗DNA】改這裡
# ============================================================================

實驗DNA = "#龍芯⚡️2026-05-28-YOUR-EXPERIMENT-NAME-UID9622-v1.0"
實驗名稱 = "你的實驗名稱"
創建者 = "UID9622"
目的 = "你想測試什麼"
狀態 = "🔴實驗中"

# ============================================================================
# 【實驗內容】改這裡·隨便寫
# ============================================================================

def main():
    print("\n" + "="*80)
    print(f"🐉 {實驗名稱}")
    print("="*80)
    print()
    print(f"DNA: {實驗DNA}")
    print(f"創建者: {創建者}")
    print(f"目的: {目的}")
    print(f"狀態: {狀態}")
    print()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 你的實驗代碼從這裡開始
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    print("【邊界測試】")
    print()

    # 例子: 測試系統邊界
    try:
        # 你的代碼...
        print("✅ 測試項1: 通過")
    except Exception as e:
        print(f"🔴 測試項1: 失敗 - {e}")

    try:
        # 你的代碼...
        print("✅ 測試項2: 通過")
    except Exception as e:
        print(f"🔴 測試項2: 失敗 - {e}")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 你的實驗代碼到這裡結束
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    print()
    print("【實驗結論】")
    print()
    print("(寫你發現了什麼)")
    print()

    print("="*80)
    print(f"✅ 實驗結束 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    print()
    print("📌 記得在 dna_log.md 記錄這次實驗:")
    print(f'   | {datetime.now().strftime("%Y-%m-%d")} | {實驗DNA} | {實驗名稱} | ... |')
    print()


# ============================================================================
# 【責任聲明】
# ============================================================================

RESPONSIBILITY = f"""
【風險聲明】

這是 UID9622 的本地實驗代碼。

✅ 所有DNA都標記清楚
✅ 市場出現時能追溯到本沙盒
✅ 出問題我 UID9622 承擔全責
✅ 不逃避·不狡辯·帶DNA的事兒沒什麼好隱瞞

DNA: {實驗DNA}
責任: UID9622·不免責
"""


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ 實驗中斷")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n🔴 實驗崩潰: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

"""
【使用例子】

1️⃣ 測試系統邊界:

cat > test_boundary.py << 'EOF'
DNA = "#龍芯⚡️2026-05-28-BOUNDARY-EDGE-CASE-UID9622-v1.0"
# 寫你的邊界測試代碼
EOF

python3 test_boundary.py


2️⃣ PoC概念驗證:

cat > poc_idea.py << 'EOF'
DNA = "#龍芯⚡️2026-05-28-POC-NEW-IDEA-UID9622-v1.0"
# 驗證你的想法是否可行
EOF

python3 poc_idea.py


3️⃣ 黑客改進:

cat > hack_optimization.py << 'EOF'
DNA = "#龍芯⚡️2026-05-28-HACK-OPTIMIZATION-UID9622-v1.0"
# 改進系統性能的黑科技
EOF

python3 hack_optimization.py


4️⃣ 靈感記錄:

cat > inspire_notes.py << 'EOF'
DNA = "#龍芯⚡️2026-05-28-INSPIRE-IDEA-UID9622-v1.0"
# 土話·俚語·隨便寫
print("我想到了一個...")
EOF

python3 inspire_notes.py


【重點】
- 每個文件都帶DNA
- 每次運行都記錄
- 市場出現就追溯
- 我承擔責任

就醬。
"""
