#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 架构管理器 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-ARCHITECT-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

为 CodeBuddy 提供自主操作 Notion 数据库架构的能力：
  1. 读取数据库当前属性架构
  2. 添加/修改/删除属性（列）
  3. 支持多种属性类型: title, rich_text, number, select, multi_select,
     date, people, relation, checkbox, url, email, phone_number, status
  4. 自动备份当前架构（JSON·滚存5份）
  5. 批量操作（从JSON描述文件批量添加属性）

用法：
  lh notion-architect list --db <database_id>
  lh notion-architect add --db <database_id> --name "活跃度" --type number
  lh notion-architect add --db <database_id> --name "优先级" --type select --options "高,中,低"
  lh notion-architect rename --db <database_id> --old "状态" --new "审核状态"
  lh notion-architect delete --db <database_id> --name "临时字段"
  lh notion-architect backup --db <database_id>
  lh notion-architect batch --db <database_id> --file schema.json
"""

import os
import sys
import json
import shutil
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# ============================================================
# 配置
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
BACKUP_DIR = DATA_DIR / "notion_schemas"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)
MAX_BACKUPS = 5  # 滚存保留份数

NOTION_TOKEN = os.environ.get("NOTION_API_KEY", "")
NOTION_VERSION = "2022-06-28"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

VALID_PROP_TYPES = [
    "title", "rich_text", "number", "select", "multi_select",
    "date", "people", "files", "checkbox", "url", "email", "phone_number",
    "formula", "relation", "rollup", "created_time", "created_by",
    "last_edited_time", "last_edited_by", "status", "unique_id"
]

# ============================================================
# Notion API 客户端（零依赖·自包含）
# ============================================================

def notion_request(method: str, path: str, data: Dict = None) -> Dict:
    """调用 Notion API"""
    if not NOTION_TOKEN:
        return {"error": "NOTION_API_KEY 未设置。请在环境变量中设置后重试。"}

    url = f"https://api.notion.com/v1/{path.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(url, method=method, headers=headers)
    if data:
        req.data = json.dumps(data).encode('utf-8')

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8') if e.fp else "{}"
        return {"error": f"HTTP {e.code}", "details": body}
    except Exception as e:
        return {"error": str(e)}

def get_database(database_id: str) -> Dict:
    """获取数据库完整信息"""
    return notion_request("GET", f"databases/{database_id}")

def update_database(database_id: str, properties: Dict) -> Dict:
    """PATCH 更新数据库属性架构"""
    return notion_request("PATCH", f"databases/{database_id}", {"properties": properties})

# ============================================================
# 核心类：NotionArchitect
# ============================================================

class NotionArchitect:
    """Notion 数据库架构管理器"""

    def __init__(self):
        self.backup_dir = BACKUP_DIR

    def get_schema(self, database_id: str) -> Dict:
        """获取当前数据库架构（人类可读）"""
        resp = get_database(database_id)
        if "error" in resp:
            return resp

        title = ""
        title_list = resp.get("title", [])
        if title_list:
            title = title_list[0].get("plain_text", "")

        properties = {}
        for name, prop in resp.get("properties", {}).items():
            prop_type = prop.get("type", "unknown")
            prop_info = {"type": prop_type}

            # 提取 select/multi_select 选项
            if prop_type in ("select", "multi_select") and prop_type in prop:
                options = prop[prop_type].get("options", [])
                prop_info["options"] = [o.get("name", "") for o in options]

            # 提取 relation 数据库ID
            if prop_type == "relation" and prop_type in prop:
                prop_info["db_id"] = prop[prop_type].get("database_id", "")
                prop_info["dual_property"] = prop[prop_type].get("dual_property", {})

            # 提取 number format
            if prop_type == "number" and prop_type in prop:
                prop_info["format"] = prop[prop_type].get("format", "number")

            # 提取 formula
            if prop_type == "formula" and prop_type in prop:
                prop_info["expression"] = str(prop[prop_type].get("expression", ""))

            properties[name] = prop_info

        return {
            "title": title,
            "properties": properties,
            "id": resp.get("id"),
            "url": resp.get("url"),
            "created_time": resp.get("created_time", ""),
            "last_edited_time": resp.get("last_edited_time", ""),
        }

    def backup_schema(self, database_id: str) -> str:
        """备份当前架构到 JSON 文件（滚存保留最近5份）"""
        schema = self.get_schema(database_id)
        if "error" in schema:
            print(f"  ⚠️ 备份失败: {schema['error']}")
            return ""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        short_id = database_id.replace("-", "")[:8]
        backup_file = self.backup_dir / f"schema_{short_id}_{timestamp}.json"

        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(schema, f, ensure_ascii=False, indent=2, default=str)

        # 滚存：保留最近 MAX_BACKUPS 份
        pattern = f"schema_{short_id}_*.json"
        existing = sorted(self.backup_dir.glob(pattern))
        if len(existing) > MAX_BACKUPS:
            for old in existing[:-MAX_BACKUPS]:
                old.unlink()

        return str(backup_file)

    def add_property(self, database_id: str, name: str, prop_type: str,
                     options: List[str] = None, relation_db: str = None) -> Dict:
        """添加新属性到数据库"""
        if prop_type not in VALID_PROP_TYPES:
            return {
                "error": f"无效属性类型: {prop_type}",
                "valid_types": VALID_PROP_TYPES
            }

        # 先检查是否已存在同名属性
        schema = self.get_schema(database_id)
        if "error" not in schema and name in schema.get("properties", {}):
            return {"error": f"属性 '{name}' 已存在（类型: {schema['properties'][name]['type']}）"}

        # 构建属性定义
        prop_def = {name: {}}

        if prop_type == "select":
            opts = options or ["默认"]
            prop_def[name]["select"] = {
                "options": [{"name": o.strip(), "color": "default"} for o in opts]
            }
        elif prop_type == "multi_select":
            opts = options or ["默认"]
            prop_def[name]["multi_select"] = {
                "options": [{"name": o.strip(), "color": "default"} for o in opts]
            }
        elif prop_type == "number":
            prop_def[name]["number"] = {"format": "number"}
        elif prop_type == "relation":
            target_db = relation_db or database_id
            prop_def[name]["relation"] = {
                "database_id": target_db,
                "type": "dual_property"
            }
        elif prop_type == "status":
            opts = options or ["未开始", "进行中", "已完成"]
            groups = [{"name": o.strip(), "color": "default"} for o in opts]
            prop_def[name]["status"] = {
                "options": groups,
                "groups": [{"name": o.strip(), "color": "default", "option_ids": []} for o in opts]
            }
        elif prop_type == "formula":
            prop_def[name]["formula"] = {
                "expression": options[0] if options else "prop(\"Name\")"
            }
        else:
            prop_def[name][prop_type] = {}

        resp = update_database(database_id, prop_def)

        if "error" in resp:
            detail = resp.get("details", "")
            # 尝试提取 Notion 的错误消息
            try:
                detail_json = json.loads(detail) if isinstance(detail, str) else detail
                detail = detail_json.get("message", str(detail_json))
            except:
                pass
            return {"error": f"添加失败: {resp['error']}", "detail": str(detail)[:300]}

        # 备份更新后的架构
        self.backup_schema(database_id)

        return {
            "status": "success",
            "action": "add",
            "property": name,
            "type": prop_type,
            "database_id": database_id
        }

    def delete_property(self, database_id: str, name: str) -> Dict:
        """删除属性（将属性设为 null）"""
        schema = self.get_schema(database_id)
        if "error" in schema:
            return schema

        if name not in schema["properties"]:
            return {"error": f"属性 '{name}' 不存在", "existing": list(schema["properties"].keys())}

        # 获取旧类型用于确认信息
        old_type = schema["properties"][name].get("type", "unknown")

        # Notion API: 删除属性 = 设为 null
        resp = update_database(database_id, {name: None})
        if "error" in resp:
            return {"error": f"删除失败: {resp['error']}"}

        self.backup_schema(database_id)
        return {
            "status": "success",
            "action": "delete",
            "deleted": name,
            "old_type": old_type,
            "database_id": database_id
        }

    def rename_property(self, database_id: str, old_name: str, new_name: str) -> Dict:
        """重命名属性"""
        if old_name == new_name:
            return {"error": "新旧名称相同，无需操作"}

        schema = self.get_schema(database_id)
        if "error" in schema:
            return schema

        if old_name not in schema["properties"]:
            return {"error": f"属性 '{old_name}' 不存在", "existing": list(schema["properties"].keys())}

        if new_name in schema["properties"]:
            return {"error": f"目标名称 '{new_name}' 已存在"}

        # 复制旧属性定义到新名称
        old_prop = schema["properties"][old_name]
        # 需要还原为完整的 Notion API 属性格式
        prop_type = old_prop.get("type", "rich_text")
        full_prop = _rebuild_notion_prop(prop_type, old_prop)

        # 先创建新属性
        resp = update_database(database_id, {new_name: full_prop})
        if "error" in resp:
            return {"error": f"创建新属性失败: {resp['error']}"}

        # 再删除旧属性
        del_resp = update_database(database_id, {old_name: None})
        if "error" in del_resp:
            # 回滚：删除已创建的新属性
            update_database(database_id, {new_name: None})
            return {"error": f"删除旧属性失败（已回滚）: {del_resp['error']}"}

        self.backup_schema(database_id)
        return {
            "status": "success",
            "action": "rename",
            "old_name": old_name,
            "new_name": new_name,
            "old_type": prop_type,
            "database_id": database_id
        }

    def batch_add(self, database_id: str, prop_list: List[Dict]) -> Dict:
        """批量添加属性（从一个定义列表）"""
        results = []
        for prop in prop_list:
            name = prop.get("name", "")
            prop_type = prop.get("type", "rich_text")
            options = prop.get("options", None)
            relation_db = prop.get("relation_db", None)
            if not name:
                results.append({"error": "缺少属性名称", "prop": prop})
                continue
            r = self.add_property(database_id, name, prop_type, options, relation_db)
            results.append(r)
        return {"status": "done", "total": len(prop_list), "results": results}


def _rebuild_notion_prop(prop_type: str, prop_info: Dict) -> Dict:
    """从精简的 prop_info 重建 Notion API 格式的属性定义"""
    prop = {}

    if prop_type == "select":
        options = prop_info.get("options", ["默认"])
        prop["select"] = {"options": [{"name": o, "color": "default"} for o in options]}
    elif prop_type == "multi_select":
        options = prop_info.get("options", ["默认"])
        prop["multi_select"] = {"options": [{"name": o, "color": "default"} for o in options]}
    elif prop_type == "number":
        fmt = prop_info.get("format", "number")
        prop["number"] = {"format": fmt}
    elif prop_type == "relation":
        db_id = prop_info.get("db_id", "")
        dual = prop_info.get("dual_property", {})
        prop["relation"] = {"database_id": db_id, "type": "dual_property", "dual_property": dual}
    elif prop_type == "formula":
        expr = prop_info.get("expression", "")
        prop["formula"] = {"expression": expr}
    elif prop_type == "status":
        options = prop_info.get("options", ["未开始", "进行中", "已完成"])
        prop["status"] = {
            "options": [{"name": o, "color": "default"} for o in options],
            "groups": [{"name": o, "color": "default", "option_ids": []} for o in options]
        }
    else:
        prop[prop_type] = {}

    return prop


# ============================================================
# CLI
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · Notion 架构管理器 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh notion-architect list --db <db_id>
  lh notion-architect add --db <db_id> --name "优先级" --type select --options "高,中,低"
  lh notion-architect rename --db <db_id> --old "状态" --new "审核状态"
  lh notion-architect delete --db <db_id> --name "临时字段"
  lh notion-architect backup --db <db_id>
  lh notion-architect batch --db <db_id> --file props.json
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # list
    p_list = subparsers.add_parser("list", help="列出数据库所有属性")
    p_list.add_argument("--db", required=True, help="数据库ID")

    # add
    p_add = subparsers.add_parser("add", help="添加新属性")
    p_add.add_argument("--db", required=True, help="数据库ID")
    p_add.add_argument("--name", required=True, help="属性名称")
    p_add.add_argument("--type", required=True, help=f"属性类型: {', '.join(VALID_PROP_TYPES[:12])}...")
    p_add.add_argument("--options", help="选项（逗号分隔，用于select/multi_select/status）")
    p_add.add_argument("--relation-db", help="关联的目标数据库ID（用于relation类型）")

    # delete
    p_del = subparsers.add_parser("delete", help="删除属性")
    p_del.add_argument("--db", required=True, help="数据库ID")
    p_del.add_argument("--name", required=True, help="要删除的属性名称")

    # rename
    p_rename = subparsers.add_parser("rename", help="重命名属性")
    p_rename.add_argument("--db", required=True, help="数据库ID")
    p_rename.add_argument("--old", required=True, help="旧属性名称")
    p_rename.add_argument("--new", required=True, help="新属性名称")

    # backup
    p_backup = subparsers.add_parser("backup", help="备份当前架构")
    p_backup.add_argument("--db", required=True, help="数据库ID")

    # batch
    p_batch = subparsers.add_parser("batch", help="从JSON文件批量添加属性")
    p_batch.add_argument("--db", required=True, help="数据库ID")
    p_batch.add_argument("--file", required=True, help="JSON定义文件路径")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    arch = NotionArchitect()

    if args.command == "list":
        schema = arch.get_schema(args.db)
        if "error" in schema:
            print(f"❌ {schema['error']}")
            sys.exit(1)

        print(f"\n📊 数据库: {schema['title']} ({schema['id'][:12]}...)")
        print(f"🔗 URL: {schema['url']}")
        print(f"📋 属性 ({len(schema['properties'])} 个):\n")
        for name, prop in schema["properties"].items():
            prop_type = prop.get("type", "?")
            extras = ""
            if prop_type in ("select", "multi_select", "status"):
                opts = prop.get("options", [])
                extras = f" → {', '.join(opts[:5])}"
            if prop_type == "relation":
                extras = f" → {prop.get('db_id', '?')[:12]}..."
            print(f"  • {name}")
            print(f"    类型: {prop_type}{extras}")
        print()

    elif args.command == "add":
        options = args.options.split(",") if args.options else None
        result = arch.add_property(args.db, args.name, args.type, options, args.relation_db)
        if "error" in result:
            print(f"❌ {result['error']}")
            if "valid_types" in result:
                print(f"   支持的类型: {', '.join(result['valid_types'][:12])}...")
            sys.exit(1)
        print(f"✅ 已添加属性: {result['property']} ({result['type']})")

    elif args.command == "delete":
        result = arch.delete_property(args.db, args.name)
        if "error" in result:
            print(f"❌ {result['error']}")
            if "existing" in result:
                print(f"   现有属性: {', '.join(result['existing'][:10])}")
            sys.exit(1)
        print(f"✅ 已删除: {result['deleted']} (原类型: {result['old_type']})")

    elif args.command == "rename":
        result = arch.rename_property(args.db, args.old, args.new)
        if "error" in result:
            print(f"❌ {result['error']}")
            sys.exit(1)
        print(f"✅ 已重命名: {result['old_name']} → {result['new_name']} ({result['old_type']})")

    elif args.command == "backup":
        path = arch.backup_schema(args.db)
        if not path:
            print("❌ 备份失败")
            sys.exit(1)
        print(f"📦 已备份: {path}")

    elif args.command == "batch":
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                prop_list = json.load(f)
        except FileNotFoundError:
            print(f"❌ 文件不存在: {args.file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ JSON 格式错误: {e}")
            sys.exit(1)

        if not isinstance(prop_list, list):
            prop_list = prop_list.get("properties", []) if isinstance(prop_list, dict) else []

        result = arch.batch_add(args.db, prop_list)
        success = sum(1 for r in result["results"] if "error" not in r)
        fail = len(result["results"]) - success
        print(f"📋 批量操作完成: {success} 成功, {fail} 失败 (共 {result['total']})")
        for r in result["results"]:
            if "error" in r:
                print(f"  ❌ {r.get('error', '未知错误')}")
            else:
                print(f"  ✅ {r.get('property', '?')} ({r.get('type', '?')})")


if __name__ == "__main__":
    main()
