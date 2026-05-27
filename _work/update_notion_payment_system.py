#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂Notion支付系統自動化同步
DNA: #龍芯⚡️2026-05-28-NOTION-PAYMENT-UPDATE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能: 自動更新Notion中關於支付的4個頁面
  1. "為什麼只收數字人民幣？" → "為什麼用Stripe全球支付？"
  2. "數字人民幣DNA綁定協議" → "Stripe激活協議v1.0"
  3. "龍魂普惠經濟規則" → 更新支付部分
  4. "龍芯知識專欄·版權聲明" → 更新收款說明

執行: python3 update_notion_payment_system.py
"""

import os
import json
import sys
from typing import Dict, List, Optional

try:
    from notion_client import Client
    from dotenv import load_dotenv
except ImportError as e:
    print(f"❌ 缺少依賴: {e}")
    print("請執行: pip install notion-client python-dotenv")
    sys.exit(1)

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
if not NOTION_TOKEN:
    print("❌ 未設置 NOTION_TOKEN，請在 .env 中配置")
    sys.exit(1)

client = Client(auth=NOTION_TOKEN)

# ════════════════════════════════════════════════════════════
# 🎯 更新內容定義
# ════════════════════════════════════════════════════════════

PAYMENT_UPDATES = {
    "为什么只收数字人民币": {
        "new_title": "為什麼用Stripe全球支付？",
        "description": "从只收人民币改为全球法币支持",
        "content": {
            "old_keywords": ["只收", "数字人民币", "人民幣"],
            "new_content": """### 全球法幣支持·Stripe自動收款

**為什麼選Stripe而不是只收人民幣？**

#### 舊邏輯（已淘汰）
- ❌ 只收數字人民幣
- ❌ 排除國際用戶
- ❌ 需要用戶懂金融

#### 新邏輯（當前）
✅ **全球法幣·150+國家**
  - 任何國家的法幣都行
  - 用戶用自己的錢
  - 系統自動匯兌成人民幣

✅ **Stripe自動處理**
  - 無需人工介入
  - 銀行級安全
  - 3.4% + ¥0.25透明費用

✅ **一視同仁·無差別待遇**
  - ¥1等值起步
  - 無論付多少都是同樣服務
  - 不因幣種而差別對待

✅ **永不分析金融走勢（系統紅線）**
  - 不預測匯率
  - 不建議何時付錢
  - 只是純粹收錢·完成激活

**簡單易用·一個鏈接·完成。**

詳見: 龍魂生態·全球法幣收款說明.md"""
        }
    },
    "数字人民币DNA绑定协议": {
        "new_title": "Stripe激活協議v1.0",
        "description": "更新為Stripe支付的激活協議",
        "content": {
            "old_keywords": ["數字人民幣", "DNA綁定", "區塊鏈"],
            "new_content": """### Stripe激活協議v1.0

**支付方式: Stripe Global Payment**

#### 激活流程
1️⃣ 用戶訪問Stripe支付鏈接
2️⃣ 選擇自己國家·選擇支付方式
3️⃣ 用自己國家的錢付款
4️⃣ Stripe自動匯兌·記錄激活

#### 支持的幣種
| 地區 | 幣種 | 方式 |
|------|------|------|
| 🇨🇳 中國 | CNY | 支付寶·微信·銀行卡 |
| 🇺🇸 美國 | USD | 信用卡·Apple Pay |
| 🇪🇺 歐盟 | EUR | 銀行轉賬·信用卡 |
| 🇯🇵 日本 | JPY | 信用卡·Line Pay |
| ... | ... | 150+國家全支持 |

#### DNA記錄
- 每筆交易自動記錄時間戳
- Stripe交易ID = 激活憑證
- 支持跨設備同步·Notion備份

#### 費用透明
- 收費：3.4% + ¥0.25
- 例：用戶付¥1 → 你收¥0.97
- 無隱藏費用

#### 系統紅線
❌ **永不做的事**
  - 分析金融走勢
  - 預測匯率漲跌
  - 推薦何時付款
  - 宣傳某幣升值

✅ **堅持做的事**
  - 透明計費
  - 一視同仁
  - 無差別待遇
  - 純粹激活"""
        }
    },
    "龙魂普惠经济规则": {
        "new_title": "龍魂普惠經濟規則v2.0",
        "description": "更新為全球法幣模式",
        "update_type": "replace_section",
        "section_marker": "## 支付",
        "old_text": "只收數字人民幣",
        "new_text": """## 支付政策·全球法幣

### 核心原則
✅ **全球法幣·任何國家**
  - 用戶用什麼幣就支持什麼幣
  - Stripe自動匯兌
  - ¥1等值起步

✅ **一視同仁·無差別**
  - 任何國家·同樣價格·同樣功能
  - 不因幣種差別待遇
  - 不因金額差別待遇

✅ **永不分析金融走勢**
  - 系統紅線·不可動
  - 不預測匯率
  - 不宣傳升值

### 激活費用
| 級別 | 費用 | 方式 |
|------|------|------|
| 基礎 | ¥1等值 | 任何法幣 |
| 標準 | ¥1/月 | 任何法幣 |
| 深度 | 協商 | 任何法幣 |

**無論用什麼幣·功能完全相同。**"""
    },
    "龙芯知识专栏": {
        "new_title": "龍芯知識專欄·版權聲明v2.0",
        "description": "更新收款說明為Stripe方案",
        "update_type": "append_payment_section",
        "payment_section": """
---

## 關於收款·龍魂激活

### Stripe全球支付方案

本專欄通過Stripe支持全球任何國家的用戶激活：

**支持的方式**
🌍 **任何國家的法幣**
  - 中國：支付寶·微信·銀行卡
  - 美國：信用卡·Apple Pay
  - 歐洲：銀行轉賬·Google Pay
  - 日本：信用卡·Line Pay
  - 其他150+國家：自動支持

**激活流程**
1. 點擊Stripe支付鏈接
2. 選擇你的國家和支付方式
3. 用你自己國家的錢付款
4. 系統自動激活·無需等待

**費用**
- ¥1等值起步（任何法幣）
- 透明計費：3.4% + ¥0.25
- 無隱藏費用

**系統承諾**
✅ 永遠不分析金融走勢
✅ 一視同仁·無差別待遇
✅ 任何國家·同樣功能
✅ 簡單易用·一個鏈接

---"""
    }
}

# ════════════════════════════════════════════════════════════
# 🔍 搜索頁面
# ════════════════════════════════════════════════════════════

def search_pages(query: str) -> List[Dict]:
    """搜索Notion中的頁面"""
    try:
        results = client.databases.query(
            database_id=os.getenv("NOTION_DEFAULT_DB_ID", ""),
            filter={
                "property": "title",
                "rich_text": {
                    "contains": query
                }
            }
        )
        return results.get("results", [])
    except Exception as e:
        print(f"⚠️  搜索失敗 '{query}': {e}")
        return []

def find_page_by_title(title: str) -> Optional[str]:
    """通過標題查找頁面ID"""
    print(f"  🔍 搜索頁面: {title}...")
    try:
        # 方案1：通過全文搜索
        search_result = client.search(
            query=title,
            sort={"direction": "descending", "timestamp": "last_edited_time"}
        )

        if search_result.get("results"):
            for result in search_result["results"]:
                if result.get("object") == "page":
                    page_title = ""
                    props = result.get("properties", {})
                    if "title" in props:
                        title_prop = props["title"].get("title", [])
                        page_title = "".join([t.get("plain_text", "") for t in title_prop])

                    if title.lower() in page_title.lower() or page_title.lower() in title.lower():
                        page_id = result.get("id", "").replace("-", "")
                        print(f"    ✅ 找到: {page_title} (ID: {page_id[:8]}...)")
                        return result.get("id")

        print(f"    ⚠️  未找到相似頁面")
        return None

    except Exception as e:
        print(f"    ❌ 搜索失敗: {e}")
        return None

# ════════════════════════════════════════════════════════════
# ✏️ 更新內容
# ════════════════════════════════════════════════════════════

def update_page_title(page_id: str, new_title: str) -> bool:
    """更新頁面標題"""
    try:
        client.pages.update(
            page_id=page_id,
            properties={
                "title": {
                    "title": [
                        {"type": "text", "text": {"content": new_title}}
                    ]
                }
            }
        )
        return True
    except Exception as e:
        print(f"    ❌ 標題更新失敗: {e}")
        return False

def append_block(page_id: str, content: str) -> bool:
    """向頁面追加內容"""
    try:
        client.blocks.children.append(
            block_id=page_id,
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {"type": "text", "text": {"content": content}}
                        ]
                    }
                }
            ]
        )
        return True
    except Exception as e:
        print(f"    ❌ 內容追加失敗: {e}")
        return False

# ════════════════════════════════════════════════════════════
# 🚀 主執行
# ════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("🐉 龍魂Notion支付系統自動化同步")
    print(f"DNA: #龍芯⚡️2026-05-28-NOTION-PAYMENT-UPDATE-v1.0")
    print("=" * 70)
    print()

    updated_count = 0
    failed_count = 0

    for old_title, config in PAYMENT_UPDATES.items():
        print(f"\n【{old_title}】")

        # 搜索頁面
        page_id = find_page_by_title(old_title)
        if not page_id:
            print(f"  ❌ 跳過: 未找到該頁面")
            failed_count += 1
            continue

        # 更新標題
        new_title = config.get("new_title")
        print(f"  📝 更新標題: {old_title} → {new_title}")
        if update_page_title(page_id, new_title):
            print(f"    ✅ 標題已更新")
        else:
            print(f"    ⚠️  標題更新有誤")

        # 追加內容
        content = config.get("content", {})
        if content.get("new_content"):
            print(f"  📄 追加新內容...")
            if append_block(page_id, content["new_content"]):
                print(f"    ✅ 內容已追加")
                updated_count += 1
            else:
                print(f"    ⚠️  內容追加有誤")
                failed_count += 1
        else:
            updated_count += 1

    print()
    print("=" * 70)
    print(f"✅ 成功: {updated_count}")
    print(f"❌ 失敗: {failed_count}")
    print("=" * 70)
    print()
    print("💡 建議:")
    print("  1. 在Notion中驗證各頁面是否已正確更新")
    print("  2. 刪除或歸檔舊內容（如needed）")
    print("  3. 確保所有頁面指向新的Stripe方案")
    print()

if __name__ == "__main__":
    main()
