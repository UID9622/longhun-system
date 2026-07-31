# DNA: #龍芯⚡️丙午·乙未·乙丑·泰-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
创建 CNSH 三层论文数据库（workspace 级别）
"""

import os
import json
import urllib.request
from datetime import datetime

token = os.getenv("NOTION_TOKEN")

def create_db(title: str, description: str, properties: dict[str, Any]) -> str:
    """创建数据库"""
    url = "https://api.notion.com/v1/databases"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    payload = {
        "parent": {"type": "workspace", "workspace": True},
        "title": [{"type": "text", "text": {"content": title}}],
        "description": [{"type": "text", "text": {"content": description}}],
        "properties": properties
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
            db_id = result['id']
            print(f"✅ {title}")
            print(f"   ID: {db_id}\n")
            return db_id
    except Exception as e:
        print(f"❌ {title}: {e}\n")
        return ""

print("\n🐉 CNSH 论文形式化系统 · 创建三层数据库\n")
print("=" * 60)

# THEORY_DB
theory_props = {
    "名称": {"title": {}},
    "定理号": {"rich_text": {}},
    "分类": {"select": {"options": [
        {"name": "核心定理", "color": "blue"},
        {"name": "引理", "color": "purple"},
        {"name": "推论", "color": "pink"},
        {"name": "定义", "color": "gray"}
    ]}},
    "状态": {"select": {"options": [
        {"name": "✅ 已形式化", "color": "green"},
        {"name": "🟡 部分完成", "color": "yellow"},
        {"name": "⏳ 待完成", "color": "red"}
    ]}},
    "Given": {"rich_text": {}},
    "When": {"rich_text": {}},
    "Then": {"rich_text": {}},
    "Proof": {"rich_text": {}},
    "LaTeX": {"rich_text": {}},
    "DNA": {"rich_text": {}}
}

theory_id = create_db(
    "📚 CNSH Unified Theory Layer",
    "龍魂核心定理库 - 所有定理、引理、推论的形式化"
    , theory_props
)

# AXIOM_DB
axiom_props = {
    "名称": {"title": {}},
    "公理号": {"rich_text": {}},
    "原理": {"rich_text": {}},
    "形式化": {"rich_text": {}},
    "应用范围": {"rich_text": {}},
    "DNA": {"rich_text": {}}
}

axiom_id = create_db(
    "⚖️ CNSH Axiom System",
    "龍魂不可动规则库 - 所有公理基础",
    axiom_props
)

# FORMULA_DB
formula_props = {
    "名称": {"title": {}},
    "类型": {"select": {"options": [
        {"name": "核心公式"},
        {"name": "推导公式"},
        {"name": "辅助公式"},
        {"name": "运行时公式"}
    ]}},
    "公式": {"rich_text": {}},
    "LaTeX": {"rich_text": {}},
    "解释": {"rich_text": {}},
    "应用": {"rich_text": {}},
    "DNA": {"rich_text": {}}
}

formula_id = create_db(
    "🧮 CNSH Runtime Formula Index",
    "龍魂数学公式库 - 所有形式化表达",
    formula_props
)

print("=" * 60)
print("\n📊 三个核心数据库已创建！\n")

config = {
    "timestamp": datetime.now().isoformat(),
    "theory_db": theory_id,
    "axiom_db": axiom_id,
    "formula_db": formula_id,
    "dna": "#龍芯⚇️2026-05-30-CNSH-THEORY-DBS-CREATED-v1.0"
}

# 保存配置
import os
config_path = os.path.expanduser("~/.龍魂_config/cnsh_theory_dbs.json")
with open(config_path, 'w') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print(f"✅ 配置已保存: {config_path}\n")

# 输出可直接使用的 ID
print("🔗 后续使用：\n")
print(f"export CNSH_THEORY_DB={theory_id}")
print(f"export CNSH_AXIOM_DB={axiom_id}")
print(f"export CNSH_FORMULA_DB={formula_id}")
