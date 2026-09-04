#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷊泰-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
Task 5: 批量导入到 Notion 数据库
"""

import os
import json
import urllib.request
from datetime import datetime

token = os.getenv("NOTION_TOKEN")

# 从配置文件读取数据
config_path = os.path.expanduser("~/.龍魂_config/cnsh_formalization_data.json")
with open(config_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

THEORY_DB = data['databases']['theory']
AXIOM_DB = data['databases']['axiom']
FORMULA_DB = data['databases']['formula']
THEOREMS = data['theorems']
AXIOMS = data['axioms']

headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def create_page(db_id: str, title: str, properties: dict[str, Any]) -> str:
    """在数据库中创建页面"""
    url = f"https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": db_id},
        "properties": {
            "名称": {"title": [{"type": "text", "text": {"content": title}}]},
            **properties
        }
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result.get('id', '')
    except Exception as e:
        print(f"❌ 创建失败: {title}")
        print(f"   {str(e)[:100]}")
        return ""

print("\n🐉 Task 5: 批量导入到 Notion\n")
print("=" * 70)

# 导入定理
print(f"\n📚 导入 {len(THEOREMS)} 个定理...")
theorem_count = 0
for thm in THEOREMS:
    props = {
        "定理号": {"rich_text": [{"type": "text", "text": {"content": thm.get('number', '')}}]},
        "分类": {"select": {"name": thm.get('category', '')}},
        "Given": {"rich_text": [{"type": "text", "text": {"content": thm.get('given', '')[:100]}}]},
        "LaTeX": {"rich_text": [{"type": "text", "text": {"content": thm.get('latex', '')}}]},
        "DNA": {"rich_text": [{"type": "text", "text": {"content": thm.get('dna', '')}}]},
    }
    page_id = create_page(THEORY_DB, thm['name'], props)
    if page_id:
        theorem_count += 1
        print(f"  ✅ {thm['name']}")

print(f"\n✅ 导入 {theorem_count}/{len(THEOREMS)} 个定理")

# 导入公理
print(f"\n⚖️  导入 {len(AXIOMS)} 个公理...")
axiom_count = 0
for ax in AXIOMS:
    props = {
        "公理号": {"rich_text": [{"type": "text", "text": {"content": ax.get('number', '')}}]},
        "原理": {"rich_text": [{"type": "text", "text": {"content": ax.get('principle', '')[:100]}}]},
        "DNA": {"rich_text": [{"type": "text", "text": {"content": ax.get('dna', '')}}]},
    }
    page_id = create_page(AXIOM_DB, ax['name'], props)
    if page_id:
        axiom_count += 1
        print(f"  ✅ {ax['name']}")

print(f"\n✅ 导入 {axiom_count}/{len(AXIOMS)} 个公理")

print("\n" + "=" * 70)
print(f"✅ Task 5 完成: {theorem_count} 定理 + {axiom_count} 公理")
print("=" * 70)
