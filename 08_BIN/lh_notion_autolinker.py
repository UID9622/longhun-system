#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 自动关联器 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-AUTOLINK-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

为 CodeBuddy 提供自主建立 Notion 页面关联的能力：
  1. 单对关联：在两个页面间建立双向关系链接
  2. 批量关联：将一个页面与多个目标页面建立关系
  3. 智能推荐：基于内容分析推荐应关联的页面
  4. 关系审计：查看某页面的所有关系链接
  5. 去重保护：已存在的关系不重复建立

用法：
  lh notion-link create --page1 <id> --page2 <id> --relation "关联"
  lh notion-link batch --from <id> --to <id1,id2,...> --relation "子任务"
  lh notion-link recommend --page <id> --limit 10
  lh notion-link audit --page <id>
  lh notion-link list-relations --db <database_id>
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ============================================================
# 配置
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LINK_CACHE_FILE = DATA_DIR / "notion_link_cache.json"
DATA_DIR.mkdir(parents=True, exist_ok=True)

NOTION_TOKEN = os.environ.get("NOTION_API_KEY", "")
NOTION_VERSION = "2022-06-28"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# ============================================================
# Notion API 客户端
# ============================================================

def notion_request(method: str, path: str, data: Dict = None) -> Dict:
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

def get_page(page_id: str) -> Dict:
    """获取页面信息（含属性）"""
    return notion_request("GET", f"pages/{page_id}")

def update_page(page_id: str, properties: Dict) -> Dict:
    """更新页面属性"""
    return notion_request("PATCH", f"pages/{page_id}", {"properties": properties})

def get_database(database_id: str) -> Dict:
    """获取数据库信息"""
    return notion_request("GET", f"databases/{database_id}")

def search_pages(query: str, limit: int = 20, start_cursor: str = None) -> Dict:
    """搜索 Notion 页面/数据库"""
    payload = {
        "query": query,
        "page_size": min(limit, 100),
        "filter": {"property": "object", "value": "page"}
    }
    if start_cursor:
        payload["start_cursor"] = start_cursor
    return notion_request("POST", "search", payload)

# ============================================================
# 辅助函数
# ============================================================

def extract_page_title(page: Dict) -> str:
    """从页面数据中提取标题文本"""
    for prop in page.get("properties", {}).values():
        if prop.get("type") == "title":
            parts = prop.get("title", [])
            return "".join([t.get("plain_text", "") for t in parts])
    return "未命名"

def find_relation_properties(page: Dict) -> Dict[str, Dict]:
    """找出页面中所有 relation 类型的属性"""
    relations = {}
    for name, prop in page.get("properties", {}).items():
        if prop.get("type") == "relation":
            relations[name] = {
                "db_id": prop.get("relation", {}).get("database_id", ""),
                "synced_property_name": prop.get("relation", {}).get("synced_property_name", ""),
            }
    return relations

# ============================================================
# 核心类：NotionAutoLinker
# ============================================================

class NotionAutoLinker:
    """Notion 页面自动关联器"""

    def __init__(self):
        self.link_cache = self._load_cache()

    def _load_cache(self) -> Dict:
        """加载本地缓存"""
        if LINK_CACHE_FILE.exists():
            try:
                with open(LINK_CACHE_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"links": {}}

    def _save_cache(self):
        """保存本地缓存"""
        with open(LINK_CACHE_FILE, 'w') as f:
            json.dump(self.link_cache, f, ensure_ascii=False, indent=2)

    def _cache_key(self, id1: str, id2: str) -> str:
        """生成排序后的缓存键（无向）"""
        parts = sorted([id1, id2])
        return f"{parts[0]}<>{parts[1]}"

    def _is_linked(self, id1: str, id2: str) -> bool:
        """检查本地缓存中是否已有链接记录"""
        return self._cache_key(id1, id2) in self.link_cache["links"]

    def _mark_linked(self, id1: str, id2: str, relation: str = ""):
        """标记链接到本地缓存"""
        key = self._cache_key(id1, id2)
        self.link_cache["links"][key] = {
            "page1": id1, "page2": id2,
            "relation": relation,
            "created_at": datetime.now().isoformat()
        }
        self._save_cache()

    def _get_relation_prop_name(self, page_id: str, target_db_id: str = None) -> Optional[str]:
        """找到页面中能关联到目标数据库的关系属性名"""
        page = get_page(page_id)
        if "error" in page:
            return None

        relations = find_relation_properties(page)
        if not relations:
            return None

        if target_db_id:
            # 精确匹配数据库
            for name, info in relations.items():
                if info["db_id"] == target_db_id:
                    return name
            # 模糊匹配（去掉连字符）
            target_clean = target_db_id.replace("-", "")
            for name, info in relations.items():
                if info["db_id"].replace("-", "") == target_clean:
                    return name

        # 返回第一个可用的关系属性
        return list(relations.keys())[0] if relations else None

    def link_pages(self, page_id_1: str, page_id_2: str, relation_type: str = "关联") -> Dict:
        """在两个页面之间建立双向关系链接"""
        # 1. 获取两个页面信息
        page1 = get_page(page_id_1)
        page2 = get_page(page_id_2)

        if "error" in page1:
            return {"error": f"页面1读取失败: {page1['error']}"}
        if "error" in page2:
            return {"error": f"页面2读取失败: {page2['error']}"}

        title1 = extract_page_title(page1)
        title2 = extract_page_title(page2)

        # 2. 检查是否已链接
        if self._is_linked(page_id_1, page_id_2):
            return {
                "status": "skipped",
                "message": f"'{title1}' 与 '{title2}' 已关联",
                "page1": page_id_1, "page2": page_id_2
            }

        # 3. 获取页面各自所属的数据库
        db1 = page1.get("parent", {}).get("database_id", "")
        db2 = page2.get("parent", {}).get("database_id", "")

        # 4. 找到合适的关系属性
        rel_prop1 = self._get_relation_prop_name(page_id_1, db2)
        rel_prop2 = self._get_relation_prop_name(page_id_2, db1)

        if not rel_prop1:
            return {"error": f"页面 '{title1}' 缺少 relation 类型属性。请先用 notion-architect 添加。"}
        if not rel_prop2:
            return {"error": f"页面 '{title2}' 缺少 relation 类型属性。请先用 notion-architect 添加。"}

        # 5. 获取现有关系列表
        current_rels1 = page1.get("properties", {}).get(rel_prop1, {}).get("relation", [])
        current_rels2 = page2.get("properties", {}).get(rel_prop2, {}).get("relation", [])

        linked_1 = {r.get("id", "") for r in current_rels1 if r.get("id")}
        linked_2 = {r.get("id", "") for r in current_rels2 if r.get("id")}

        errors = []

        # 6. 双向建立
        if page_id_2 not in linked_1:
            new_rels1 = list(current_rels1) + [{"id": page_id_2}]
            resp1 = update_page(page_id_1, {rel_prop1: {"relation": new_rels1}})
            if "error" in resp1:
                errors.append(f"页面1更新失败: {resp1['error']}")
        else:
            print(f"  ℹ️ {title1} → {title2} 已存在（跳过）")

        if page_id_1 not in linked_2:
            new_rels2 = list(current_rels2) + [{"id": page_id_1}]
            resp2 = update_page(page_id_2, {rel_prop2: {"relation": new_rels2}})
            if "error" in resp2:
                errors.append(f"页面2更新失败: {resp2['error']}")
        else:
            print(f"  ℹ️ {title2} → {title1} 已存在（跳过）")

        if errors:
            return {"error": "; ".join(errors)}

        # 7. 缓存
        self._mark_linked(page_id_1, page_id_2, relation_type)

        return {
            "status": "success",
            "action": "link",
            "page1": {"id": page_id_1, "title": title1},
            "page2": {"id": page_id_2, "title": title2},
            "relation": relation_type,
            "prop1": rel_prop1,
            "prop2": rel_prop2,
        }

    def batch_link(self, from_page_id: str, to_page_ids: List[str],
                   relation_type: str = "关联") -> Dict:
        """将一个页面批量关联到多个目标页面"""
        results = []
        for target_id in to_page_ids:
            r = self.link_pages(from_page_id, target_id, relation_type)
            results.append(r)

        success = sum(1 for r in results if r.get("status") in ("success", "skipped"))
        fail = sum(1 for r in results if "error" in r)

        return {
            "status": "done",
            "total": len(to_page_ids),
            "success": success,
            "fail": fail,
            "results": results
        }

    def recommend_pages(self, page_id: str, limit: int = 10) -> Dict:
        """基于页面内容推荐应关联的其他页面"""
        page = get_page(page_id)
        if "error" in page:
            return {"error": f"页面读取失败: {page['error']}"}

        title = extract_page_title(page)
        if not title:
            return {"error": "无法提取页面标题", "recommendations": []}

        # 提取关键词
        keywords = re.findall(r'[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}', title)
        if not keywords:
            keywords = [title]

        # 对每个关键词搜索
        all_results = []
        seen_ids = {page_id.replace("-", "")}

        for kw in keywords[:3]:  # 最多3个关键词
            resp = search_pages(kw, limit=min(limit, 10))
            if "error" in resp:
                continue
            for r in resp.get("results", []):
                rid = r.get("id", "").replace("-", "")
                if rid not in seen_ids:
                    seen_ids.add(rid)
                    all_results.append(r)

        # 精简输出
        recommendations = []
        for r in all_results[:limit]:
            recommendations.append({
                "id": r.get("id"),
                "title": extract_page_title(r),
                "url": r.get("url", ""),
                "last_edited": r.get("last_edited_time", ""),
            })

        return {
            "status": "success",
            "source_page": {"id": page_id, "title": title},
            "recommendations": recommendations,
            "count": len(recommendations),
            "keywords_used": keywords[:3]
        }

    def audit_links(self, page_id: str) -> Dict:
        """审计某页面的所有关系链接"""
        page = get_page(page_id)
        if "error" in page:
            return {"error": f"页面读取失败: {page['error']}"}

        title = extract_page_title(page)
        relations = find_relation_properties(page)

        if not relations:
            return {
                "status": "success",
                "page": {"id": page_id, "title": title},
                "relations": {},
                "total_links": 0,
                "message": "此页面没有关系属性"
            }

        link_details = {}
        total = 0

        for prop_name, prop_info in relations.items():
            rel_data = page.get("properties", {}).get(prop_name, {}).get("relation", [])
            linked_pages = []
            for rel in rel_data:
                linked_id = rel.get("id", "")
                if linked_id:
                    # 尝试获取链接页面的标题（可选，可能耗时）
                    linked_title = linked_id[:12] + "..."  # 默认用截断ID
                    linked_pages.append({"id": linked_id, "title": linked_title})
            link_details[prop_name] = {
                "target_db": prop_info["db_id"],
                "linked_pages": linked_pages,
                "count": len(linked_pages)
            }
            total += len(linked_pages)

        return {
            "status": "success",
            "page": {"id": page_id, "title": title},
            "relations": link_details,
            "total_links": total
        }

    def list_database_relations(self, database_id: str) -> Dict:
        """列出数据库中所有 relation 类型的属性"""
        db = get_database(database_id)
        if "error" in db:
            return {"error": f"数据库读取失败: {db['error']}"}

        title = ""
        title_list = db.get("title", [])
        if title_list:
            title = title_list[0].get("plain_text", "")

        relations = {}
        for name, prop in db.get("properties", {}).items():
            if prop.get("type") == "relation":
                relations[name] = {
                    "db_id": prop.get("relation", {}).get("database_id", ""),
                    "dual_property_name": prop.get("relation", {}).get("dual_property", {}).get("synced_property_name", ""),
                }

        # 尝试获取关联数据库的名称
        for rel_name, rel_info in relations.items():
            if rel_info["db_id"]:
                try:
                    target_db = get_database(rel_info["db_id"])
                    if "error" not in target_db:
                        t = target_db.get("title", [{}])
                        rel_info["target_db_name"] = t[0].get("plain_text", "") if t else ""
                except:
                    pass

        return {
            "status": "success",
            "database": {"id": database_id, "title": title},
            "relations": relations,
            "count": len(relations)
        }


# ============================================================
# CLI
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · Notion 自动关联器 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh notion-link create --page1 <id> --page2 <id> --relation "协作"
  lh notion-link batch --from <id> --to <id1,id2> --relation "子任务"
  lh notion-link recommend --page <id> --limit 10
  lh notion-link audit --page <id>
  lh notion-link list-relations --db <db_id>
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # create
    p_link = subparsers.add_parser("create", help="创建双向关联")
    p_link.add_argument("--page1", required=True, help="页面1 ID")
    p_link.add_argument("--page2", required=True, help="页面2 ID")
    p_link.add_argument("--relation", default="关联", help="关系类型描述")

    # batch
    p_batch = subparsers.add_parser("batch", help="批量关联")
    p_batch.add_argument("--from", dest="from_page", required=True, help="源页面ID")
    p_batch.add_argument("--to", required=True, help="目标页面ID列表（逗号分隔）")
    p_batch.add_argument("--relation", default="关联", help="关系类型描述")

    # recommend
    p_rec = subparsers.add_parser("recommend", help="智能推荐关联页面")
    p_rec.add_argument("--page", required=True, help="页面ID")
    p_rec.add_argument("--limit", type=int, default=10, help="推荐数量")

    # audit
    p_audit = subparsers.add_parser("audit", help="审计页面关系")
    p_audit.add_argument("--page", required=True, help="页面ID")

    # list-relations
    p_list = subparsers.add_parser("list-relations", help="列出数据库关系属性")
    p_list.add_argument("--db", required=True, help="数据库ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    linker = NotionAutoLinker()

    if args.command == "create":
        result = linker.link_pages(args.page1, args.page2, args.relation)
        if "error" in result:
            print(f"❌ {result['error']}")
            sys.exit(1)
        elif result.get("status") == "skipped":
            print(f"⏭️  {result['message']}")
        else:
            print(f"✅ 已关联: {result['page1']['title']} ↔ {result['page2']['title']}")
            print(f"   关系: {result['relation']} (属性: {result['prop1']}, {result['prop2']})")

    elif args.command == "batch":
        to_ids = [t.strip() for t in args.to.split(",") if t.strip()]
        if not to_ids:
            print("❌ --to 参数不能为空")
            sys.exit(1)
        result = linker.batch_link(args.from_page, to_ids, args.relation)
        print(f"📋 批量关联: {result['success']} 成功, {result['fail']} 失败 (共 {result['total']})")
        for r in result["results"]:
            if "error" in r:
                print(f"  ❌ {r['error'][:80]}")
            elif r.get("status") == "skipped":
                print(f"  ⏭️  {r.get('message', '')[:80]}")
            else:
                print(f"  ✅ {r.get('page1', {}).get('title', '?')} ↔ {r.get('page2', {}).get('title', '?')}")

    elif args.command == "recommend":
        result = linker.recommend_pages(args.page, args.limit)
        if "error" in result:
            print(f"❌ {result['error']}")
            sys.exit(1)
        print(f"\n🔍 为 '{result['source_page']['title']}' 推荐关联:")
        print(f"   关键词: {', '.join(result['keywords_used'])}")
        print(f"   推荐 {result['count']} 个页面:\n")
        for r in result["recommendations"]:
            print(f"  • {r['title']}")
            print(f"    ID: {r['id'][:24]}... | {r['url']}")
        print()

    elif args.command == "audit":
        result = linker.audit_links(args.page)
        if "error" in result:
            print(f"❌ {result['error']}")
            sys.exit(1)
        print(f"\n🔗 页面关系审计: {result['page']['title']}")
        print(f"   总链接数: {result['total_links']}")
        if not result["relations"]:
            print(f"   {result.get('message', '无关系属性')}")
        else:
            for prop_name, info in result["relations"].items():
                target = info.get("target_db", "")[:12]
                print(f"\n  📎 {prop_name} → 数据库 {target}...")
                print(f"     已链接 {info['count']} 个页面:")
                for lp in info["linked_pages"]:
                    print(f"       • {lp['title']}")
        print()

    elif args.command == "list-relations":
        result = linker.list_database_relations(args.db)
        if "error" in result:
            print(f"❌ {result['error']}")
            sys.exit(1)
        print(f"\n📊 数据库: {result['database']['title']}")
        print(f"   关系属性 ({result['count']} 个):\n")
        for name, info in result["relations"].items():
            target_name = info.get("target_db_name", info["db_id"][:12])
            print(f"  • {name} → {target_name}")
        print()


if __name__ == "__main__":
    main()
