#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通心译 · 一键初始化脚本
在你自己的Notion里建好全部数据库，然后生成MCP配置。
你的数据在你自己的Notion，作者不在中间。

DNA: #龍芯⚡️2026-03-21-通心译-SETUP-v1.0
作者: 诸葛鑫（Lucky · UID9622）
"""

import json, subprocess, sys, os
from pathlib import Path

R="\033[91m"; G="\033[92m"; Y="\033[93m"; C="\033[96m"
W="\033[97m"; DIM="\033[2m"; BOLD="\033[1m"; RST="\033[0m"

MCP_SCRIPT = Path(__file__).parent / "tongxinyi_mcp.py"


def _post(token, endpoint, payload):
    r = subprocess.run(
        ["curl", "-s", "-X", "POST", f"https://api.notion.com/v1/{endpoint}",
         "-H", f"Authorization: Bearer {token}",
         "-H", "Notion-Version: 2022-06-28",
         "-H", "Content-Type: application/json",
         "-d", json.dumps(payload, ensure_ascii=False)],
        capture_output=True, text=True
    )
    return json.loads(r.stdout)


def _create_page(token, title, emoji):
    """在workspace根级建页面（需要public integration权限）"""
    r = _post(token, "pages", {
        "parent": {"type": "workspace", "workspace": True},
        "icon": {"type": "emoji", "emoji": emoji},
        "properties": {"title": {"title": [{"type": "text", "text": {"content": title}}]}}
    })
    if r.get("id"):
        return r["id"], r.get("url", "")
    # 如果workspace级不行，提示用户选择父页面
    return None, r.get("message", "")


def _create_database(token, parent_page_id, title, emoji, properties):
    r = _post(token, "databases", {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "icon": {"type": "emoji", "emoji": emoji},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": properties
    })
    if r.get("id"):
        return r["id"], r.get("url", "")
    return None, r.get("message", "")


def setup(token: str, parent_page_id: str = None):
    print(f"\n{C}{'═'*52}{RST}")
    print(f"{BOLD}{C}  通心译 · 初始化你的Notion翻译生态{RST}")
    print(f"{DIM}  数据归你，作者不在中间{RST}")
    print(f"{C}{'═'*52}{RST}\n")

    # ── 1. 建主页面 ──────────────────────────────────────────────────────────
    if not parent_page_id:
        print(f"  {Y}[1/7] 创建通心译主页面...{RST}")
        page_id, page_url = _create_page(token, "💰 通心译 · Heart-to-Heart Translate", "💰")
        if not page_id:
            print(f"  {R}❌ 无法在workspace根级建页面。")
            print(f"  请在Notion里手动建一个页面，把页面ID粘贴在这里:{RST}")
            raw = input(f"  {W}页面ID（32位，去掉-也行）: {RST}").strip().replace("-","")
            page_id = f"{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}" if len(raw)==32 else raw
            page_url = ""
        print(f"  {G}✅ 主页面: {page_url or page_id}{RST}")
    else:
        page_id = parent_page_id
        print(f"  {G}[1/7] 使用指定父页面: {page_id}{RST}")

    db_ids = {}

    # ── 2. 对话记忆库 ChatMemory ─────────────────────────────────────────────
    print(f"\n  {Y}[2/7] 建「③ 对话记忆库 · ChatMemory」...{RST}")
    db_id, url = _create_database(token, page_id,
        "③ 对话记忆库 · ChatMemory", "🧠", {
        "原文":     {"title": {}},
        "译文":     {"rich_text": {}},
        "原文语言": {"select": {"options": [
            {"name": "中文","color":"red"},{"name":"English","color":"blue"},
            {"name":"日本語","color":"pink"},{"name":"한국어","color":"purple"},
            {"name":"Français","color":"yellow"},{"name":"العربية","color":"orange"}
        ]}},
        "目标语言": {"select": {"options": [
            {"name": "中文","color":"red"},{"name":"English","color":"blue"},
            {"name":"日本語","color":"pink"},{"name":"한국어","color":"purple"},
            {"name":"Français","color":"yellow"},{"name":"العربية","color":"orange"}
        ]}},
        "关系场景": {"select": {"options": [
            {"name":"通用","color":"default"},{"name":"亲密伴侣","color":"red"},
            {"name":"家人","color":"orange"},{"name":"朋友","color":"green"},
            {"name":"商务","color":"blue"},{"name":"外交","color":"purple"},
            {"name":"公开演讲","color":"yellow"}
        ]}},
        "语气":     {"select": {"options": [
            {"name":"直达","color":"default"},{"name":"温柔","color":"pink"},
            {"name":"强硬","color":"red"},{"name":"学术","color":"blue"},
            {"name":"宣言式","color":"purple"},{"name":"口语","color":"green"}
        ]}},
        "文化注释": {"rich_text": {}},
        "DNA":      {"rich_text": {}},
        "创建时间": {"created_time": {}}
    })
    db_ids["CHATMEMORY_DB"] = db_id
    print(f"  {G if db_id else R}{'✅' if db_id else '❌'} {url or db_id}{RST}")

    # ── 3. 文化词典库 CulturalDict ───────────────────────────────────────────
    print(f"\n  {Y}[3/7] 建「① 文化词典库 · CulturalDict」...{RST}")
    db_id, url = _create_database(token, page_id,
        "① 文化词典库 · CulturalDict", "📖", {
        "词条原文": {"title": {}},
        "标准译文": {"rich_text": {}},
        "语言对":   {"select": {"options": [
            {"name":"中→英","color":"blue"},{"name":"英→中","color":"red"},
            {"name":"中→日","color":"pink"},{"name":"通用","color":"default"}
        ]}},
        "类型":     {"select": {"options": [
            {"name":"主权词汇","color":"red"},{"name":"文化成语","color":"orange"},
            {"name":"亲昵称呼","color":"pink"},{"name":"商务术语","color":"blue"},
            {"name":"哲学概念","color":"purple"}
        ]}},
        "禁止译法": {"rich_text": {}},
        "原因注释": {"rich_text": {}},
    })
    db_ids["CULTURALDICT_DB"] = db_id
    print(f"  {G if db_id else R}{'✅' if db_id else '❌'} {url or db_id}{RST}")

    # ── 4. 习惯偏好库 UserStyle ──────────────────────────────────────────────
    print(f"\n  {Y}[4/7] 建「④ 习惯偏好库 · UserStyle」...{RST}")
    db_id, url = _create_database(token, page_id,
        "④ 习惯偏好库 · UserStyle", "🎨", {
        "偏好项":   {"title": {}},
        "偏好值":   {"rich_text": {}},
        "类别":     {"select": {"options": [
            {"name":"表情风格","color":"yellow"},{"name":"语气偏好","color":"blue"},
            {"name":"禁忌词","color":"red"},{"name":"常用场景","color":"green"},
            {"name":"语言习惯","color":"purple"}
        ]}},
        "示例":     {"rich_text": {}},
    })
    db_ids["USERSTYLE_DB"] = db_id
    print(f"  {G if db_id else R}{'✅' if db_id else '❌'} {url or db_id}{RST}")

    # ── 5. 关系图谱库 RelationMap ────────────────────────────────────────────
    print(f"\n  {Y}[5/7] 建「② 关系图谱库 · RelationMap」...{RST}")
    db_id, url = _create_database(token, page_id,
        "② 关系图谱库 · RelationMap", "🕸️", {
        "关系名称": {"title": {}},
        "关系类型": {"select": {"options": [
            {"name":"伴侣","color":"red"},{"name":"家人","color":"orange"},
            {"name":"朋友","color":"green"},{"name":"同事","color":"blue"},
            {"name":"陌生人","color":"default"}
        ]}},
        "惯用称呼": {"rich_text": {}},
        "语气偏好": {"rich_text": {}},
        "文化背景": {"rich_text": {}},
    })
    db_ids["RELATIONMAP_DB"] = db_id
    print(f"  {G if db_id else R}{'✅' if db_id else '❌'} {url or db_id}{RST}")

    # ── 6. 易经语义映射库 YiJingMap ──────────────────────────────────────────
    print(f"\n  {Y}[6/7] 建「⑤ 易经语义映射库 · YiJingMap」...{RST}")
    db_id, url = _create_database(token, page_id,
        "⑤ 易经语义映射库 · YiJingMap", "☯️", {
        "卦名":     {"title": {}},
        "卦象编号": {"number": {}},
        "对应场景": {"rich_text": {}},
        "翻译策略": {"rich_text": {}},
        "语气建议": {"rich_text": {}},
    })
    db_ids["YIJINGMAP_DB"] = db_id
    print(f"  {G if db_id else R}{'✅' if db_id else '❌'} {url or db_id}{RST}")

    # ── 7. 生成MCP配置 ───────────────────────────────────────────────────────
    print(f"\n  {Y}[7/7] 生成Claude MCP配置...{RST}")

    mcp_config = {
        "tongxinyi": {
            "type": "stdio",
            "command": "python3",
            "args": [str(MCP_SCRIPT)],
            "env": {
                "NOTION_TOKEN":    token,
                "CHATMEMORY_DB":   db_ids.get("CHATMEMORY_DB", ""),
                "CULTURALDICT_DB": db_ids.get("CULTURALDICT_DB", ""),
                "USERSTYLE_DB":    db_ids.get("USERSTYLE_DB", ""),
                "RELATIONMAP_DB":  db_ids.get("RELATIONMAP_DB", ""),
                "YIJINGMAP_DB":    db_ids.get("YIJINGMAP_DB", ""),
            }
        }
    }

    # 写入用户claude.json
    claude_json = Path.home() / ".claude.json"
    if claude_json.exists():
        cfg = json.loads(claude_json.read_text())
        cfg.setdefault("mcpServers", {}).update(mcp_config)
        claude_json.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
        print(f"  {G}✅ 已写入 ~/.claude.json{RST}")

    # 也输出配置供手动复制
    config_out = Path.home() / ".tongxinyi_mcp_config.json"
    config_out.write_text(json.dumps(mcp_config, indent=2, ensure_ascii=False))
    print(f"  {G}✅ 配置已保存到 {config_out}{RST}")

    # ── 完成 ─────────────────────────────────────────────────────────────────
    print(f"\n{C}{'═'*52}{RST}")
    print(f"{BOLD}{G}  🎉 通心译初始化完成！{RST}")
    print(f"\n  你的Notion里已建好5个数据库：")
    print(f"  ① 文化词典库  ② 关系图谱库  ③ 对话记忆库")
    print(f"  ④ 习惯偏好库  ⑤ 易经语义映射库")
    print(f"\n  {DIM}作者（UID9622）不在中间。")
    print(f"  你的翻译记忆，在你自己的Notion。{RST}")
    print(f"\n  重启Claude Code后，直接说：")
    print(f"  {W}「帮我翻译这句话：小傻瓜」{RST}")
    print(f"  通心译会自动调用。")
    print(f"{C}{'═'*52}{RST}\n")

    return db_ids


if __name__ == "__main__":
    print(f"\n{C}通心译 · 初始化向导{RST}")
    print(f"{DIM}你的Notion token（去 notion.so/my-integrations 创建integration取得）{RST}")
    token = input(f"{W}Notion Token: {RST}").strip()
    if not token.startswith("ntn_") and not token.startswith("secret_"):
        print(f"{R}❌ token格式不对，应以 ntn_ 或 secret_ 开头{RST}")
        sys.exit(1)

    parent = input(f"{W}父页面ID（留空则自动创建，或粘贴你已有的页面ID）: {RST}").strip()
    if parent:
        parent = parent.replace("-","")
        parent = f"{parent[:8]}-{parent[8:12]}-{parent[12:16]}-{parent[16:20]}-{parent[20:]}"

    setup(token, parent or None)
