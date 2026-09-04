#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 · Notion 全面整理引擎 v1.0

功能：
  1. 搜索 Notion 中所有页面和数据库
  2. 读取所有数据库的结构和内容
  3. 分析内容分类和重复
  4. 重新组织数据库结构
  5. 输出整理报告和推荐操作

用法：
  python3 bin/lh_notion_reorganizer.py --scan        # 扫描所有内容
  python3 bin/lh_notion_reorganizer.py --report      # 生成整理报告
  python3 bin/lh_notion_reorganizer.py --reorganize  # 执行整理（需确认）

DNA: #龍芯⚡️丙午·乙未·己丑·庚午·䷨损-NOTION-REORGANIZER-v1.0
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════
# 0. 配置
# ═══════════════════════════════════════════════
CST = timezone(timedelta(hours=8))
HOME = Path.home()
LONGHUN_ROOT = Path(os.environ.get("LONGHUN_ROOT", HOME / "longhun-system"))
OUTPUT_DIR = LONGHUN_ROOT / "data" / "notion_scan"
STATE_FILE = HOME / ".longhun" / "notion_reorganizer_state.json"

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
NOTION_VERSION = "2022-06-28"
NOTION_API = "https://api.notion.com/v1"

# 从环境变量加载数据库 ID
KNOWN_DBS = {}
for k, v in os.environ.items():
    if k.startswith("NOTION_") and k.endswith("_DB") and v:
        KNOWN_DBS[k.replace("NOTION_", "").replace("_DB", "")] = v

for d in (OUTPUT_DIR,):
    d.mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    return datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def now_ts() -> str:
    return datetime.now(CST).strftime("%Y%m%d-%H%M%S")


# ═══════════════════════════════════════════════
# 1. Notion API 客户端
# ═══════════════════════════════════════════════
class NotionClient:
    def __init__(self, token: str = ""):
        self.token = token or NOTION_TOKEN
        if not self.token:
            raise RuntimeError("NOTION_TOKEN 未设置")
        self.call_count = 0
        self.last_call = 0

    def _rate_limit(self):
        elapsed = time.time() - self.last_call
        if elapsed < 0.34:
            time.sleep(0.34 - elapsed)

    def _call(self, method: str, endpoint: str, payload: Optional[Dict] = None,
              timeout: int = 60) -> Dict[str, Any]:
        self._rate_limit()
        self.last_call = time.time()

        url = f"{NOTION_API}{endpoint}"
        cmd = [
            "curl", "-s", "-S", "-L", "--max-time", str(timeout),
            "-X", method,
            "-H", f"Authorization: Bearer {self.token}",
            "-H", f"Notion-Version: {NOTION_VERSION}",
            "-H", "Content-Type: application/json",
            "-w", "\nHTTP_CODE:%{http_code}",
            url,
        ]

        data_file = None
        try:
            if payload is not None:
                data_file = Path(f"/tmp/.lh_notion_{os.getpid()}.json")
                data_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
                # 插入到 -w 之前: -d @file 必须在 -w 前面
                cmd.insert(-3, "-d")
                cmd.insert(-3, f"@{data_file}")

            proc = subprocess.run(cmd, capture_output=True, timeout=timeout + 10)
            out = proc.stdout.decode("utf-8", errors="replace")

            if "HTTP_CODE:" not in out:
                return {"ok": False, "error": f"curl异常: {out[:200]}"}

            body_str, code_str = out.rsplit("HTTP_CODE:", 1)
            code = int(code_str.strip())
            body_str = body_str.strip()

            self.call_count += 1

            if code >= 400:
                try:
                    err = json.loads(body_str)
                    msg = err.get("message", body_str[:200])
                except Exception:
                    msg = body_str[:200]
                if code == 429:
                    time.sleep(3)
                    return self._call(method, endpoint, payload, timeout)
                return {"ok": False, "status": code, "error": msg}

            if not body_str:
                return {"ok": True, "data": {}}

            return {"ok": True, "data": json.loads(body_str)}

        except subprocess.TimeoutExpired:
            return {"ok": False, "error": f"超时: {method} {endpoint}"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
        finally:
            if data_file and data_file.exists():
                data_file.unlink()

    def search(self, query: str = "", page_size: int = 100,
               start_cursor: Optional[str] = None,
               filter_type: Optional[str] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"page_size": page_size}
        if query:
            payload["query"] = query
        if filter_type:
            payload["filter"] = {"property": "object", "value": filter_type}
        if start_cursor:
            payload["start_cursor"] = start_cursor
        return self._call("POST", "/search", payload)

    def search_all(self, filter_type: Optional[str] = None) -> List[Dict]:
        """搜索所有页面/数据库"""
        results = []
        cursor = None
        page = 1
        while True:
            print(f"  🔍 搜索第{page}页... (已找到{len(results)}项)", end="\r")
            resp = self.search(query="", page_size=100, start_cursor=cursor,
                              filter_type=filter_type)
            if not resp.get("ok"):
                print(f"\n  ⚠️ 搜索出错: {resp.get('error', '')}")
                break
            data = resp["data"]
            batch = data.get("results", [])
            results.extend(batch)
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
            page += 1
            time.sleep(0.2)
        print(f"  🔍 搜索完成: 共{len(results)}项" + " " * 30)
        return results

    def get_page(self, page_id: str) -> Dict[str, Any]:
        page_id = page_id.replace("-", "")
        return self._call("GET", f"/pages/{page_id}")

    def get_block_children(self, block_id: str, page_size: int = 100) -> Dict[str, Any]:
        block_id = block_id.replace("-", "")
        return self._call("GET",
                         f"/blocks/{block_id}/children?page_size={page_size}")

    def get_all_blocks(self, block_id: str) -> List[Dict]:
        """获取所有子块"""
        all_blocks = []
        cursor = None
        while True:
            endpoint = f"/blocks/{block_id}/children?page_size=100"
            if cursor:
                endpoint += f"&start_cursor={cursor}"
            resp = self._call("GET", endpoint)
            if not resp.get("ok"):
                break
            data = resp["data"]
            batch = data.get("results", [])
            all_blocks.extend(batch)
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
        return all_blocks

    def query_database(self, db_id: str) -> Dict[str, Any]:
        db_id = db_id.replace("-", "")
        return self._call("POST", f"/databases/{db_id}/query",
                         {"page_size": 100})

    def query_database_all(self, db_id: str) -> List[Dict]:
        """查询数据库所有条目"""
        db_id = db_id.replace("-", "")
        results = []
        cursor = None
        while True:
            payload: Dict[str, Any] = {"page_size": 100}
            if cursor:
                payload["start_cursor"] = cursor
            resp = self._call("POST", f"/databases/{db_id}/query", payload)
            if not resp.get("ok"):
                print(f"  ⚠️ 查询数据库 {db_id[:8]} 出错: {resp.get('error', '')}")
                break
            data = resp["data"]
            batch = data.get("results", [])
            results.extend(batch)
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
        return results

    def get_database(self, db_id: str) -> Dict[str, Any]:
        db_id = db_id.replace("-", "")
        return self._call("GET", f"/databases/{db_id}")

    def create_database(self, parent_page_id: str, title: str,
                        properties: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": properties,
        }
        return self._call("POST", "/databases", payload)

    def list_databases(self) -> List[Dict]:
        """列出所有数据库"""
        return [r for r in self.search_all()
                if r.get("object") == "database"]

    def list_pages(self) -> List[Dict]:
        """列出所有页面（不含数据库）"""
        return [r for r in self.search_all()
                if r.get("object") == "page"]


# ═══════════════════════════════════════════════
# 2. 内容分析器
# ═══════════════════════════════════════════════
class ContentAnalyzer:
    """分析 Notion 内容，分类、去重、推荐整理方案"""

    CATEGORIES = {
        "宪法/铁律": ["宪法", "铁律", "规则", "宪法", "铁律", "protocol",
                     "constitution", "law", "rule", "铁律·北辰"],
        "技术文档": ["技术文档", "tech", "API", "SDK", "架构", "engine",
                    "部署", "deploy", "代码", "CNSH", "算法", "开发"],
        "哲学/文化": ["哲学", "philosophy", "易经", "道德经", "太极", "五行",
                    "八卦", "洛书", "三才", "369", "文化"],
        "身份/IP": ["UID9622", "IP", "身份", "identity", "DNA", "诸葛鑫",
                   "龍芯北辰", "花名册", "profile", "about"],
        "论文/学术": ["论文", "paper", "IEEE", "白皮书", "whitepaper",
                    "学术", "academic", "发表"],
        "笔记/日记": ["笔记", "日记", "log", "记录", "note", "memo",
                    "随想", "投喂", "feed"],
        "项目/产品": ["项目", "product", "project", "MVP", "产品",
                    "app", "应用", "小程序"],
        "审计/安全": ["审计", "audit", "安全", "security", "firewall",
                    "防火墙", "熔断", "violation", "违规"],
        "财富/金融": ["财富", "金融", "money", "finance", "币", "currency",
                    "支付", "pay", "经济"],
        "未分类": [],
    }

    @classmethod
    def classify(cls, title: str, properties: Optional[Dict] = None) -> str:
        """根据标题和属性分类"""
        text = (title or "").lower()
        if properties:
            for prop_name, prop_val in (properties or {}).items():
                if isinstance(prop_val, dict):
                    if prop_val.get("type") == "select":
                        sel = prop_val.get("select")
                        if sel:
                            text += " " + sel.get("name", "").lower()
                    elif prop_val.get("type") == "multi_select":
                        for s in prop_val.get("multi_select", []):
                            text += " " + s.get("name", "").lower()

        scores = {}
        for cat, keywords in cls.CATEGORIES.items():
            if cat == "未分类":
                continue
            score = 0
            for kw in keywords:
                if kw.lower() in text:
                    score += 1
            if score > 0:
                scores[cat] = score

        if scores:
            return max(scores, key=scores.get)
        return "未分类"

    @staticmethod
    def extract_title(page: Dict[str, Any]) -> str:
        """从页面提取标题"""
        props = page.get("properties", {})
        for prop_val in props.values():
            if isinstance(prop_val, dict) and prop_val.get("type") == "title":
                titles = prop_val.get("title", [])
                return "".join(t.get("plain_text", "") for t in titles)
        # fallback: 从页面对象本身
        for key in ["title", "Name", "名称", "标题"]:
            p = props.get(key, {})
            if isinstance(p, dict) and p.get("title"):
                return "".join(t.get("plain_text", "") for t in p["title"])
        return "未命名"

    @staticmethod
    def extract_tags(page: Dict[str, Any]) -> List[str]:
        """提取标签"""
        tags = []
        props = page.get("properties", {})
        for prop_val in props.values():
            if isinstance(prop_val, dict):
                if prop_val.get("type") == "multi_select":
                    for s in prop_val.get("multi_select", []):
                        tags.append(s.get("name", ""))
        return tags

    @staticmethod
    def estimate_size(page: Dict[str, Any]) -> int:
        """估算页面大小（字符数）"""
        total = 0
        props = page.get("properties", {})
        for prop_val in props.values():
            if isinstance(prop_val, dict):
                for rt_field in ["title", "rich_text"]:
                    for rt in prop_val.get(rt_field, []):
                        total += len(rt.get("plain_text", ""))
        return total


# ═══════════════════════════════════════════════
# 3. Notion 扫描器
# ═══════════════════════════════════════════════
class NotionScanner:
    """扫描 Notion 全部内容并建立索引"""

    def __init__(self, client: NotionClient):
        self.client = client
        self.databases: List[Dict] = []
        self.pages: List[Dict] = []
        self.db_entries: Dict[str, List[Dict]] = {}  # db_id -> entries
        self.scan_result: Dict[str, Any] = {}

    def scan_all(self) -> Dict[str, Any]:
        """执行全量扫描"""
        print("\n" + "=" * 60)
        print("🐉 龍魂 · Notion 全量扫描")
        print("=" * 60)

        # Step 1: 获取所有数据库
        print("\n📊 Step 1/4: 搜索所有数据库...")
        self.databases = self.client.list_databases()
        print(f"  找到 {len(self.databases)} 个数据库")

        # Step 2: 获取所有页面
        print("\n📄 Step 2/4: 搜索所有页面...")
        self.pages = self.client.list_pages()
        print(f"  找到 {len(self.pages)} 个页面")

        # Step 3: 读取每个数据库的结构和内容
        print("\n📋 Step 3/4: 读取数据库内容...")
        db_summaries = []
        for i, db in enumerate(self.databases):
            db_id = db.get("id", "").replace("-", "")
            db_title = ContentAnalyzer.extract_title(db) or "未命名数据库"
            print(f"  [{i+1}/{len(self.databases)}] 📁 {db_title} ({db_id[:8]}...)")

            # 获取数据库 schema
            db_detail_resp = self.client.get_database(db_id)
            db_detail = {}
            if db_detail_resp.get("ok"):
                db_detail = db_detail_resp["data"]

            # 查询所有条目
            entries = self.client.query_database_all(db_id)
            self.db_entries[db_id] = entries

            # 摘要
            entry_summaries = []
            for e in entries:
                title = ContentAnalyzer.extract_title(e)
                category = ContentAnalyzer.classify(title, e.get("properties"))
                entry_summaries.append({
                    "id": e.get("id", ""),
                    "title": title,
                    "category": category,
                    "url": e.get("url", ""),
                    "last_edited": e.get("last_edited_time", ""),
                    "created": e.get("created_time", ""),
                })

            db_summaries.append({
                "id": db_id,
                "title": db_title,
                "entry_count": len(entries),
                "schema": {k: v.get("type", "unknown")
                          for k, v in db_detail.get("properties", {}).items()
                          if k not in ("Name", "title")} if db_detail else {},
                "entries": entry_summaries,
                "url": db.get("url", ""),
                "last_edited": db.get("last_edited_time", ""),
            })

        # Step 4: 分析页面
        print("\n🔬 Step 4/4: 分析页面内容...")
        page_summaries = []
        for i, page in enumerate(self.pages):
            page_id = page.get("id", "").replace("-", "")
            title = ContentAnalyzer.extract_title(page)
            category = ContentAnalyzer.classify(title, page.get("properties"))
            parent = page.get("parent", {})

            page_summaries.append({
                "id": page_id,
                "title": title,
                "category": category,
                "parent_type": parent.get("type", ""),
                "parent_id": parent.get("page_id", parent.get("database_id", "")),
                "url": page.get("url", ""),
                "last_edited": page.get("last_edited_time", ""),
                "created": page.get("created_time", ""),
                "archived": page.get("archived", False),
            })

            if (i + 1) % 50 == 0:
                print(f"  分析中... {i+1}/{len(self.pages)}", end="\r")
        print(f"  分析完成: {len(page_summaries)} 个页面" + " " * 20)

        # 汇总
        self.scan_result = {
            "scan_time": now_iso(),
            "dna": f"#龍芯⚡️{now_ts()}-NOTION-SCAN-v1.0",
            "summary": {
                "total_databases": len(self.databases),
                "total_pages": len(self.pages),
                "total_db_entries": sum(len(v) for v in self.db_entries.values()),
                "api_calls": self.client.call_count,
            },
            "databases": db_summaries,
            "pages": page_summaries,
        }

        # 分类统计
        cat_counts = {}
        for p in page_summaries:
            c = p["category"]
            cat_counts[c] = cat_counts.get(c, 0) + 1
        for db_s in db_summaries:
            for e in db_s["entries"]:
                c = e["category"]
                cat_counts[c] = cat_counts.get(c, 0) + 1

        self.scan_result["category_stats"] = cat_counts

        # 保存
        scan_path = OUTPUT_DIR / f"notion_full_scan_{now_ts()}.json"
        scan_path.write_text(
            json.dumps(self.scan_result, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"\n💾 扫描结果已保存: {scan_path}")

        return self.scan_result


# ═══════════════════════════════════════════════
# 4. 整理方案生成器
# ═══════════════════════════════════════════════
class ReorganizerPlanner:
    """生成 Notion 整理方案"""

    def __init__(self, scan_result: Dict[str, Any]):
        self.scan = scan_result

    def generate_plan(self) -> Dict[str, Any]:
        """生成整理计划"""
        print("\n" + "=" * 60)
        print("📐 生成整理方案")
        print("=" * 60)

        plan = {
            "generated_at": now_iso(),
            "dna": f"#龍芯⚡️{now_ts()}-NOTION-REORG-PLAN-v1.0",
            "suggested_structure": self._suggest_structure(),
            "orphan_pages": self._find_orphans(),
            "duplicates": self._find_duplicates(),
            "archive_candidates": self._find_archive_candidates(),
            "local_dedup_suggestions": self._local_dedup_suggestions(),
            "recommended_actions": [],
        }

        # 生成推荐操作
        plan["recommended_actions"] = self._generate_actions(plan)

        # 保存
        plan_path = OUTPUT_DIR / f"reorganize_plan_{now_ts()}.json"
        plan_path.write_text(
            json.dumps(plan, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"💾 整理方案已保存: {plan_path}")

        return plan

    def _suggest_structure(self) -> Dict[str, Any]:
        """建议理想的 Notion 数据库结构"""
        cat_stats = self.scan.get("category_stats", {})

        suggested = {
            "🏛️ 核心宪法与铁律": {
                "description": "系统宪法、铁律、不可修订条款、协议",
                "target_category": "宪法/铁律",
                "suggested_properties": {
                    "名称": {"title": {}},
                    "版本": {"rich_text": {}},
                    "状态": {"select": {
                        "options": [
                            {"name": "有效", "color": "green"},
                            {"name": "草稿", "color": "yellow"},
                            {"name": "已修订", "color": "orange"},
                            {"name": "归档", "color": "gray"},
                        ]
                    }},
                    "优先级": {"select": {
                        "options": [
                            {"name": "P0-不可修订", "color": "red"},
                            {"name": "P1-需老大审批", "color": "orange"},
                            {"name": "P2-社区讨论", "color": "blue"},
                        ]
                    }},
                    "DNA": {"rich_text": {}},
                    "标签": {"multi_select": {
                        "options": [
                            {"name": "北辰协议", "color": "purple"},
                            {"name": "三色审计", "color": "green"},
                            {"name": "DNA追溯", "color": "blue"},
                            {"name": "三道闸门", "color": "red"},
                            {"name": "主权", "color": "orange"},
                        ]
                    }},
                },
                "estimated_entries": cat_stats.get("宪法/铁律", 0),
            },
            "💻 技术文档与架构": {
                "description": "CNSH、API、引擎、部署等所有技术文档",
                "target_category": "技术文档",
                "suggested_properties": {
                    "名称": {"title": {}},
                    "模块": {"select": {
                        "options": [
                            {"name": "CNSH语言", "color": "blue"},
                            {"name": "引擎", "color": "green"},
                            {"name": "鸿蒙", "color": "orange"},
                            {"name": "部署运维", "color": "purple"},
                            {"name": "API网关", "color": "pink"},
                            {"name": "安全", "color": "red"},
                            {"name": "其他", "color": "gray"},
                        ]
                    }},
                    "状态": {"select": {
                        "options": [
                            {"name": "已完成", "color": "green"},
                            {"name": "开发中", "color": "yellow"},
                            {"name": "规划中", "color": "blue"},
                            {"name": "归档", "color": "gray"},
                        ]
                    }},
                    "DNA": {"rich_text": {}},
                },
                "estimated_entries": cat_stats.get("技术文档", 0),
            },
            "🧠 哲学与文化库": {
                "description": "易经、道德经、太极、五行、369等哲学资产",
                "target_category": "哲学/文化",
                "suggested_properties": {
                    "名称": {"title": {}},
                    "维度": {"multi_select": {
                        "options": [
                            {"name": "太极", "color": "blue"},
                            {"name": "易经", "color": "yellow"},
                            {"name": "道德经", "color": "green"},
                            {"name": "五行", "color": "red"},
                            {"name": "八卦", "color": "purple"},
                            {"name": "洛书369", "color": "orange"},
                            {"name": "三才算法", "color": "brown"},
                            {"name": "河图", "color": "pink"},
                            {"name": "七因子", "color": "gray"},
                        ]
                    }},
                    "形式": {"select": {
                        "options": [
                            {"name": "论文", "color": "blue"},
                            {"name": "引擎代码", "color": "green"},
                            {"name": "解读", "color": "yellow"},
                            {"name": "图谱", "color": "purple"},
                            {"name": "其他", "color": "gray"},
                        ]
                    }},
                },
                "estimated_entries": cat_stats.get("哲学/文化", 0),
            },
            "🆔 身份与IP资产": {
                "description": "UID9622身份、IP展示、花名册、DNA体系",
                "target_category": "身份/IP",
                "suggested_properties": {
                    "名称": {"title": {}},
                    "类型": {"select": {
                        "options": [
                            {"name": "公开IP", "color": "green"},
                            {"name": "内部档案", "color": "yellow"},
                            {"name": "数字人", "color": "blue"},
                            {"name": "DNA登记", "color": "purple"},
                        ]
                    }},
                },
                "estimated_entries": cat_stats.get("身份/IP", 0),
            },
            "📝 论文与学术": {
                "description": "IEEE论文、白皮书、学术发表",
                "target_category": "论文/学术",
                "suggested_properties": {
                    "名称": {"title": {}},
                    "期刊": {"select": {
                        "options": [
                            {"name": "IEEE", "color": "blue"},
                            {"name": "白皮书", "color": "gray"},
                            {"name": "arXiv", "color": "red"},
                            {"name": "博客", "color": "green"},
                        ]
                    }},
                    "版本": {"rich_text": {}},
                    "状态": {"select": {
                        "options": [
                            {"name": "已发表", "color": "green"},
                            {"name": "审稿中", "color": "yellow"},
                            {"name": "草稿", "color": "orange"},
                        ]
                    }},
                },
                "estimated_entries": cat_stats.get("论文/学术", 0),
            },
            "📒 笔记与投喂": {
                "description": "日常笔记、投喂记录、日志",
                "target_category": "笔记/日记",
                "suggested_properties": {
                    "名称": {"title": {}},
                    "来源": {"select": {
                        "options": [
                            {"name": "老大投喂", "color": "red"},
                            {"name": "AI生成", "color": "blue"},
                            {"name": "Claude", "color": "purple"},
                            {"name": "Kimi", "color": "green"},
                            {"name": "DeepSeek", "color": "orange"},
                            {"name": "其他", "color": "gray"},
                        ]
                    }},
                    "日期": {"date": {}},
                },
                "estimated_entries": cat_stats.get("笔记/日记", 0),
            },
            "🛡️ 审计与安全": {
                "description": "安全审计、违规记录、熔断日志",
                "target_category": "审计/安全",
                "suggested_properties": {
                    "名称": {"title": {}},
                    "级别": {"select": {
                        "options": [
                            {"name": "🔴 严重", "color": "red"},
                            {"name": "🟡 警告", "color": "yellow"},
                            {"name": "🟢 正常", "color": "green"},
                            {"name": "⚪ 信息", "color": "gray"},
                        ]
                    }},
                    "时间": {"date": {}},
                },
                "estimated_entries": cat_stats.get("审计/安全", 0),
            },
            "📦 项目与交付": {
                "description": "项目计划、交付物、产品迭代",
                "target_category": "项目/产品",
                "suggested_properties": {
                    "名称": {"title": {}},
                    "阶段": {"select": {
                        "options": [
                            {"name": "概念", "color": "blue"},
                            {"name": "开发", "color": "yellow"},
                            {"name": "测试", "color": "orange"},
                            {"name": "已交付", "color": "green"},
                            {"name": "归档", "color": "gray"},
                        ]
                    }},
                    "截止日期": {"date": {}},
                },
                "estimated_entries": cat_stats.get("项目/产品", 0),
            },
        }
        return suggested

    def _find_orphans(self) -> List[Dict]:
        """找出孤立的页面（不在任何数据库中）"""
        orphans = []
        db_ids = {db["id"] for db in self.scan.get("databases", [])}
        for page in self.scan.get("pages", []):
            parent_db = page.get("parent_id", "")
            if parent_db and parent_db in db_ids:
                continue  # 在数据库中，不是孤儿
            if page.get("parent_type") == "database_id":
                continue
            orphans.append({
                "id": page["id"],
                "title": page["title"],
                "category": page["category"],
                "url": page.get("url", ""),
            })
        return orphans

    def _find_duplicates(self) -> List[Dict]:
        """找出疑似重复的页面"""
        titles: Dict[str, List[Dict]] = {}
        for db in self.scan.get("databases", []):
            for e in db.get("entries", []):
                t = (e.get("title", "") or "").lower().strip()
                if len(t) > 5:
                    titles.setdefault(t, []).append(e)
        for page in self.scan.get("pages", []):
            t = (page.get("title", "") or "").lower().strip()
            if len(t) > 5:
                titles.setdefault(t, []).append(page)

        # 相似度匹配（模糊）
        duplicates = []
        processed = set()
        items = list(titles.items())

        for i, (t1, entries1) in enumerate(items):
            if t1 in processed or len(entries1) <= 1:
                continue
            dups = []
            for j, (t2, entries2) in enumerate(items):
                if j <= i or t2 in processed:
                    continue
                # 简单相似度：一个包含另一个 或 共同词≥80%
                if t1 in t2 or t2 in t1:
                    dups.append({"title": t2, "entries": entries2})
                    processed.add(t2)
            if dups:
                processed.add(t1)
                duplicates.append({
                    "title": t1,
                    "entries": entries1,
                    "duplicates": dups,
                })

        return duplicates

    def _find_archive_candidates(self) -> List[Dict]:
        """找出90天没动的页面（候选归档）"""
        ninety_days_ago = (datetime.now(CST) - timedelta(days=90)).isoformat()
        candidates = []

        for page in self.scan.get("pages", []):
            last_edited = page.get("last_edited", "")
            if last_edited and last_edited < ninety_days_ago:
                candidates.append({
                    "id": page["id"],
                    "title": page["title"],
                    "category": page["category"],
                    "last_edited": last_edited,
                    "url": page.get("url", ""),
                })

        for db in self.scan.get("databases", []):
            for e in db.get("entries", []):
                last_edited = e.get("last_edited", "")
                if last_edited and last_edited < ninety_days_ago:
                    candidates.append({
                        "id": e.get("id", ""),
                        "title": e.get("title", ""),
                        "category": e.get("category", ""),
                        "last_edited": last_edited,
                        "url": e.get("url", ""),
                    })

        return sorted(candidates, key=lambda x: x["last_edited"])

    def _local_dedup_suggestions(self) -> List[Dict]:
        """建议哪些本地文件可以归档（因为已存在于 Notion）"""
        suggestions = []
        notion_titles = set()

        # 收集 Notion 中的所有标题
        for db in self.scan.get("databases", []):
            for e in db.get("entries", []):
                t = (e.get("title", "") or "").strip().lower()
                if len(t) > 3:
                    notion_titles.add(t)
        for page in self.scan.get("pages", []):
            t = (page.get("title", "") or "").strip().lower()
            if len(t) > 3:
                notion_titles.add(t)

        # 扫描本地 docs/ 目录
        docs_dir = LONGHUN_ROOT / "docs"
        if docs_dir.exists():
            for md_file in docs_dir.rglob("*.md"):
                if md_file.stat().st_size > 1000000:  # 跳过超大文件
                    continue
                try:
                    content = md_file.read_text(encoding="utf-8")[:500]
                    # 提取第一个 # 标题
                    for line in content.splitlines():
                        line = line.strip()
                        if line.startswith("# ") and len(line) > 4:
                            local_title = line[2:].strip().lower()
                            if local_title in notion_titles:
                                suggestions.append({
                                    "local_path": str(md_file.relative_to(LONGHUN_ROOT)),
                                    "title": line[2:].strip(),
                                    "size_kb": md_file.stat().st_size // 1024,
                                    "action": "可归档（Notion已有副本）",
                                })
                            break
                except Exception:
                    pass

        return sorted(suggestions, key=lambda x: x["size_kb"], reverse=True)

    def _generate_actions(self, plan: Dict[str, Any]) -> List[str]:
        """生成推荐操作列表"""
        actions = []

        # 1. 孤儿页面
        orphans = plan.get("orphan_pages", [])
        if orphans:
            actions.append(
                f"📌 找到 {len(orphans)} 个孤立页面，建议归入对应数据库"
            )

        # 2. 重复
        dups = plan.get("duplicates", [])
        if dups:
            actions.append(
                f"🔄 发现 {len(dups)} 组疑似重复内容，建议去重合并"
            )

        # 3. 归档候选
        archives = plan.get("archive_candidates", [])
        if archives:
            actions.append(
                f"📦 {len(archives)} 个页面超过90天未更新，建议归档"
            )

        # 4. 本地去重
        local_dedups = plan.get("local_dedup_suggestions", [])
        if local_dedups:
            total_kb = sum(d["size_kb"] for d in local_dedups)
            actions.append(
                f"💾 {len(local_dedups)} 个本地文件({total_kb}KB)已在Notion有副本，可归档本地释放空间"
            )

        # 5. 数据库建议
        suggested = plan.get("suggested_structure", {})
        db_count = self.scan.get("summary", {}).get("total_databases", 0)
        actions.append(
            f"🏗️ 建议整理为 {len(suggested)} 个主题数据库（当前有 {db_count} 个数据库）"
        )

        return actions


# ═══════════════════════════════════════════════
# 5. 报告生成
# ═══════════════════════════════════════════════
def generate_markdown_report(scan: Dict[str, Any], plan: Dict[str, Any]) -> str:
    """生成可读的 Markdown 报告"""
    s = scan.get("summary", {})
    cat_stats = scan.get("category_stats", {})

    lines = [
        f"# 龍魂 · Notion 全量整理报告",
        f"",
        f"**DNA:** `{scan.get('dna', '')}`",
        f"**扫描时间:** {scan.get('scan_time', '')}",
        f"**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`",
        f"",
        f"---",
        f"",
        f"## 一、总览",
        f"",
        f"| 指标 | 数值 |",
        f"|---|---|",
        f"| 数据库数量 | **{s.get('total_databases', 0)}** |",
        f"| 独立页面数量 | **{s.get('total_pages', 0)}** |",
        f"| 数据库条目总数 | **{s.get('total_db_entries', 0)}** |",
        f"| API 调用次数 | {s.get('api_calls', 0)} |",
        f"",
        f"## 二、内容分类统计",
        f"",
        f"| 分类 | 数量 |",
        f"|---|---|",
    ]
    for cat, count in sorted(cat_stats.items(), key=lambda x: -x[1]):
        lines.append(f"| {cat} | {count} |")

    lines.extend([
        f"",
        f"## 三、数据库清单",
        f"",
    ])
    for db in scan.get("databases", []):
        lines.extend([
            f"### 📁 {db['title']}",
            f"- ID: `{db['id'][:16]}...`",
            f"- 条目数: **{db['entry_count']}**",
            f"- URL: {db.get('url', 'N/A')}",
            f"",
        ])

    lines.extend([
        f"",
        f"## 四、整理方案",
        f"",
        f"### 建议数据库结构",
        f"",
    ])
    suggested = plan.get("suggested_structure", {})
    for name, info in suggested.items():
        lines.extend([
            f"#### {name}",
            f"- 说明: {info.get('description', '')}",
            f"- 预估条目: {info.get('estimated_entries', 0)}",
            f"",
        ])

    lines.extend([
        f"### 推荐操作",
        f"",
    ])
    for i, action in enumerate(plan.get("recommended_actions", []), 1):
        lines.append(f"{i}. {action}")

    lines.extend([
        f"",
        f"---",
        f"",
        f"## 五、本地去重建议",
        f"",
        f"以下本地文件在 Notion 已有副本，可安全归档以释放本地存储：",
        f"",
        f"| 文件 | 标题 | 大小(KB) | 操作 |",
        f"|---|---|---|---|",
    ])
    for d in plan.get("local_dedup_suggestions", [])[:50]:
        lines.append(
            f"| `{d['local_path']}` | {d['title'][:40]} | {d['size_kb']} | {d['action']} |"
        )

    lines.extend([
        f"",
        f"> 中国的事情，中国人自己说了算",
        f"> **DNA:** `{scan.get('dna', '')}`",
        f"> **CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`",
        f"",
    ])

    return "\n".join(lines)


# ═══════════════════════════════════════════════
# 6. CLI
# ═══════════════════════════════════════════════
def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · Notion 全面整理引擎 v1.0"
    )
    parser.add_argument("--scan", action="store_true",
                       help="扫描 Notion 全部内容")
    parser.add_argument("--report", action="store_true",
                       help="生成整理报告")
    parser.add_argument("--reorganize", action="store_true",
                       help="执行整理操作")
    parser.add_argument("--dry-run", action="store_true",
                       help="试运行（不实际修改 Notion）")
    parser.add_argument("--list-dbs", action="store_true",
                       help="列出所有数据库")

    args = parser.parse_args()

    if not any([args.scan, args.report, args.reorganize, args.list_dbs]):
        parser.print_help()
        print("\n💡 常用: python3 bin/lh_notion_reorganizer.py --scan --report")
        return

    # 加载 Token
    token = NOTION_TOKEN or os.environ.get("NOTION_TOKEN", "")
    if not token:
        # 尝试从 secrets loader 加载
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "lh_secrets_loader",
            LONGHUN_ROOT / "bin" / "lh_secrets_loader.py"
        )
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.load_all(export_to_os=True)
            token = os.environ.get("NOTION_TOKEN", "")

    if not token:
        print("❌ NOTION_TOKEN 未设置，请先运行 python3 bin/lh_secrets_loader.py")
        sys.exit(1)

    client = NotionClient(token)

    # --list-dbs
    if args.list_dbs:
        dbs = client.list_databases()
        print(f"\n📊 Notion 数据库列表 ({len(dbs)} 个):\n")
        for db in dbs:
            title = ContentAnalyzer.extract_title(db) or "未命名"
            db_id = db.get("id", "").replace("-", "")
            print(f"  📁 {title}")
            print(f"     ID: {db_id}")
            print(f"     URL: {db.get('url', 'N/A')}")
            print()
        return

    scan_result = None

    # --scan
    if args.scan:
        scanner = NotionScanner(client)
        scan_result = scanner.scan_all()

    # --report
    if args.report:
        if scan_result is None:
            latest = sorted(OUTPUT_DIR.glob("notion_full_scan_*.json"), reverse=True)
            if latest:
                scan_result = json.loads(latest[0].read_text(encoding="utf-8"))
                print(f"📂 加载已有扫描: {latest[0]}")
            else:
                print("⚠️ 没有扫描结果，先执行 --scan")
                scanner = NotionScanner(client)
                scan_result = scanner.scan_all()

        planner = ReorganizerPlanner(scan_result)
        plan = planner.generate_plan()

        report = generate_markdown_report(scan_result, plan)
        report_path = OUTPUT_DIR / f"notion_reorganize_report_{now_ts()}.md"
        report_path.write_text(report, encoding="utf-8")
        print(f"\n📄 整理报告已生成: {report_path}")

        # 打印摘要
        print("\n" + "=" * 60)
        print("📊 整理摘要")
        print("=" * 60)
        for action in plan.get("recommended_actions", []):
            print(f"  {action}")

        local_dedups = plan.get("local_dedup_suggestions", [])
        if local_dedups:
            total_kb = sum(d["size_kb"] for d in local_dedups)
            total_mb = total_kb / 1024
            print(f"\n  💾 可释放本地空间: ~{total_mb:.1f}MB ({len(local_dedups)}个文件)")

    # --reorganize
    if args.reorganize:
        if args.dry_run:
            print("\n🔍 [试运行模式] 不会实际修改 Notion")
        else:
            print("\n⚠️  --reorganize 需要 #CONFIRM 码确认后再执行")
            print("   请先在 Notion 中查看报告后再确认执行")

    # 总结
    print(f"\n✅ 完成。所有产物在: {OUTPUT_DIR}")
    print(f"   DNA: #龍芯⚡️{now_ts()}-NOTION-REORGANIZER-v1.0")


if __name__ == "__main__":
    main()
