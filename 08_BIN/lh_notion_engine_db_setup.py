#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 引擎数据库建表脚本 v2.0
DNA: #龍芯⚡️丙午·丙申·癸酉·庚申·䷒临-NOTION-ENGINE-DB-SETUP-v2.0-A1B2C3D4
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

基于 notion_db_schema_v2.json 自动生成 Notion Database 创建 Payload，
支持直接调用 Notion API 建库并返回 database_id。

用法:
  python3 bin/lh_notion_engine_db_setup.py              # 生成 payload + curl 命令
  python3 bin/lh_notion_engine_db_setup.py --create     # 调用 Notion API 建库

环境变量:
  NOTION_INTEGRATION_TOKEN  (必需，用于真实建库)
  NOTION_PARENT_PAGE_ID     (必需，数据库挂载到哪个页面)
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import urllib.request
import urllib.error

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·丙申·癸酉·庚申·䷒临-NOTION-ENGINE-DB-SETUP-v2.0-A1B2C3D4"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "data" / "notion_sync" / "engines"
SCHEMA_FILE = OUTPUT_DIR / "notion_db_schema_v2.json"
PAYLOAD_FILE = OUTPUT_DIR / "notion_db_create_payload.json"
CURL_FILE = OUTPUT_DIR / "notion_db_create_curl.sh"
RESULT_FILE = OUTPUT_DIR / "notion_db_create_result.json"

NOTION_API_VERSION = "2022-06-28"
NOTION_API_URL = "https://api.notion.com/v1/databases"

COLORS = [
    "default", "gray", "brown", "orange", "yellow", "green",
    "blue", "purple", "pink", "red",
]


def _now() -> str:
    return datetime.now(CST).isoformat()


def _log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴", "SKIP": "⏭️", "API": "🌐"}
    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] {markers.get(level, 'ℹ️')} {msg}")


def load_schema(path: Path) -> Dict[str, Any]:
    if not path.exists():
        _log(f"Schema 文件不存在: {path}", "ERROR")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _color_for(index: int) -> str:
    return COLORS[index % len(COLORS)]


def schema_property_to_notion(
    name: str,
    prop: Dict[str, Any],
    color_index: int,
) -> Dict[str, Any]:
    """把 Schema v2.0 里的属性定义转换为 Notion API property object。"""
    ptype = prop.get("type", "rich_text")

    if ptype == "title":
        return {"title": {}}

    if ptype == "rich_text":
        return {"rich_text": {}}

    if ptype == "url":
        return {"url": {}}

    if ptype == "date":
        return {"date": {}}

    if ptype == "checkbox":
        return {"checkbox": {}}

    if ptype == "number":
        fmt = prop.get("format", "number")
        return {"number": {"format": fmt}}

    if ptype == "select":
        options = prop.get("options", [])
        if not options:
            # 如果没有预定义选项，Notion API 也接受空 options 列表
            return {"select": {"options": []}}
        return {
            "select": {
                "options": [
                    {"name": opt, "color": _color_for(color_index + i)}
                    for i, opt in enumerate(options)
                ]
            }
        }

    if ptype == "multi_select":
        options = prop.get("options", [])
        if not options:
            return {"multi_select": {"options": []}}
        return {
            "multi_select": {
                "options": [
                    {"name": opt, "color": _color_for(color_index + i)}
                    for i, opt in enumerate(options)
                ]
            }
        }

    # 兜底
    _log(f"未知属性类型 '{ptype}'，按 rich_text 处理: {name}", "WARN")
    return {"rich_text": {}}


def build_notion_payload(schema: Dict[str, Any], parent_page_id: Optional[str]) -> Dict[str, Any]:
    """构建 Notion API 建库请求体。"""
    title_text = schema.get("database_title", "龍魂引擎注册表")
    description_text = schema.get("database_description", "")
    schema_props = schema.get("properties", {})

    # Notion 要求 properties 里必须有且仅有一个 title
    title_count = sum(1 for p in schema_props.values() if p.get("type") == "title")
    if title_count != 1:
        _log(f"Schema 中必须包含恰好 1 个 title 属性，当前 {title_count} 个", "ERROR")
        sys.exit(1)

    properties: Dict[str, Any] = {}
    color_index = 0
    for name, prop in schema_props.items():
        properties[name] = schema_property_to_notion(name, prop, color_index)
        if prop.get("type") in ("select", "multi_select"):
            color_index += len(prop.get("options", []))
        else:
            color_index += 1

    payload: Dict[str, Any] = {
        "title": [{"type": "text", "text": {"content": title_text}}],
        "description": [{"type": "text", "text": {"content": description_text}}],
        "properties": properties,
        "is_inline": False,
    }

    if parent_page_id:
        payload["parent"] = {"page_id": parent_page_id}

    return payload


def save_payload(payload: Dict[str, Any]):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(PAYLOAD_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    _log(f"Payload 已保存: {PAYLOAD_FILE}", "OK")


def save_curl(payload: Dict[str, Any], token: Optional[str], parent_page_id: Optional[str]):
    """保存可直接执行的 curl 命令（绝不写入真实 token，仅引用环境变量）。"""
    env_token = "$NOTION_INTEGRATION_TOKEN"
    env_parent = parent_page_id if parent_page_id else "$NOTION_PARENT_PAGE_ID"

    curl = f"""#!/usr/bin/env bash
# 龍魂 Notion 数据库建库命令
# DNA: {DNA}
# 生成时间: {_now()}

set -e

TOKEN="{env_token}"
PARENT_PAGE_ID="{env_parent}"

if [[ "$TOKEN" == \\$* ]]; then
  eval "TOKEN=$TOKEN"
fi
if [[ "$PARENT_PAGE_ID" == \\$* ]]; then
  eval "PARENT_PAGE_ID=$PARENT_PAGE_ID"
fi

curl -X POST "{NOTION_API_URL}" \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Notion-Version: {NOTION_API_VERSION}" \\
  -H "Content-Type: application/json" \\
  -d '{json.dumps(payload, ensure_ascii=False)}' \\
  | python3 -m json.tool
"""
    with open(CURL_FILE, "w", encoding="utf-8") as f:
        f.write(curl)
    os.chmod(CURL_FILE, 0o755)
    _log(f"curl 命令已保存: {CURL_FILE}", "OK")


def call_notion_api(payload: Dict[str, Any], token: str) -> Optional[Dict[str, Any]]:
    """直接调用 Notion API 创建数据库。"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json",
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(
        NOTION_API_URL,
        data=data,
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            result = json.loads(body)
            return result
    except urllib.error.HTTPError as e:
        _log(f"Notion API 错误: HTTP {e.code}", "ERROR")
        try:
            err_body = e.read().decode("utf-8")
            _log(err_body, "ERROR")
            return {"error": json.loads(err_body), "http_code": e.code}
        except Exception:
            return {"error": str(e), "http_code": e.code}
    except Exception as e:
        _log(f"请求失败: {e}", "ERROR")
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="龍魂 Notion 引擎数据库建表脚本 v2.0")
    parser.add_argument("--schema", type=Path, default=SCHEMA_FILE,
                        help="输入 Schema 文件路径")
    parser.add_argument("--create", action="store_true",
                        help="直接调用 Notion API 创建数据库（需环境变量）")
    parser.add_argument("--parent-page-id", type=str, default=os.environ.get("NOTION_PARENT_PAGE_ID", ""),
                        help="数据库挂载的父页面 ID")
    args = parser.parse_args()

    print(f"\n{DNA}")
    print(f"{CONFIRM}\n")

    schema = load_schema(args.schema)
    _log(f"已加载 Schema: {schema.get('title')} (v{schema.get('version')})", "OK")
    _log(f"属性数量: {len(schema.get('properties', {}))}", "INFO")

    token = os.environ.get("NOTION_INTEGRATION_TOKEN") or os.environ.get("NOTION_TOKEN")
    parent_page_id = args.parent_page_id or os.environ.get("NOTION_PARENT_PAGE_ID")

    payload = build_notion_payload(schema, parent_page_id)
    save_payload(payload)
    save_curl(payload, token, parent_page_id)

    print("\n📊 建库 Payload 概览:")
    print(f"  数据库标题: {schema.get('database_title')}")
    print(f"  属性数量: {len(payload['properties'])}")
    print(f"  父页面ID: {parent_page_id or '未设置（仅生成 curl）'}")
    print(f"  Token: {'已配置' if token else '未配置'}")

    print(f"\n🚀 curl 命令预览:")
    print(f"  bash {CURL_FILE}")

    if args.create:
        if not token:
            _log("未设置 NOTION_INTEGRATION_TOKEN，无法真实建库", "ERROR")
            sys.exit(1)
        if not parent_page_id:
            _log("未设置 NOTION_PARENT_PAGE_ID，无法真实建库", "ERROR")
            sys.exit(1)

        _log("正在调用 Notion API 创建数据库...", "API")
        result = call_notion_api(payload, token)

        with open(RESULT_FILE, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        _log(f"API 结果已保存: {RESULT_FILE}", "OK")

        if result and "id" in result:
            db_id = result["id"]
            url = result.get("url", "")
            _log(f"✅ 数据库创建成功", "OK")
            print(f"\n🎯 database_id: {db_id}")
            print(f"🔗 URL: {url}")
            print(f"\n后续同步命令:")
            print(f"  export NOTION_DATABASE_ID={db_id}")
            print(f"  export NOTION_INTEGRATION_TOKEN=<your-token>")
            print(f"  python3 bin/lh_notion_engine_status_syncer.py --execute")
        else:
            _log("数据库创建失败或未返回 id", "ERROR")
            sys.exit(1)
    else:
        _log("DRY-RUN 模式：已生成 payload 和 curl，未调用 Notion API", "OK")
        print("\n💡 如需真实建库:")
        print("  export NOTION_INTEGRATION_TOKEN=xxx")
        print("  export NOTION_PARENT_PAGE_ID=xxx")
        print("  python3 bin/lh_notion_engine_db_setup.py --create")

    _log("完成", "OK")


if __name__ == "__main__":
    main()
