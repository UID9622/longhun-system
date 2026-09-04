#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 · Notion 全量同步整理器 v3.0

一键执行：
  扫描全部内容 → 分析分类 → 生成整理报告 → 创建/更新数据库 → 推送内容

用法：
  python3 bin/lh_notion_full_sync.py              # 扫描+报告
  python3 bin/lh_notion_full_sync.py --execute    # 扫描+报告+执行整理
  python3 bin/lh_notion_full_sync.py --report-only  # 仅基于已有扫描生成报告

DNA: #龍芯⚡️丙午·乙未·己丑·庚午·䷨损-NOTION-FULL-SYNC-v3.0
"""
import json, os, subprocess, sys, time, argparse
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Any

CST = timezone(timedelta(hours=8))
HOME = Path.home()
ROOT = HOME / "longhun-system"
DATA_DIR = ROOT / "data" / "notion_scan"
SCAN_FILE = DATA_DIR / "scan_raw.json"
REPORT_FILE = DATA_DIR / "reorganize_report.md"
PLAN_FILE = DATA_DIR / "reorganize_plan.json"

# ── 凭证 ──
def get_token():
    t = os.environ.get("NOTION_TOKEN", "")
    if not t:
        sys.path.insert(0, str(ROOT / "bin"))
        from lh_secrets_loader import load_all
        load_all(export_to_os=True)
        t = os.environ.get("NOTION_TOKEN", "")
    if not t:
        print("❌ NOTION_TOKEN 未设置"); sys.exit(1)
    return t

NOW = lambda: datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00")
NOW_TS = lambda: datetime.now(CST).strftime("%Y%m%d-%H%M%S")

# ═══════════════════════════════════════════════
# 1. Notion API
# ═══════════════════════════════════════════════
class NotionAPI:
    def __init__(self):
        self.token = get_token()
        self.calls = 0

    def call(self, endpoint, method="GET", payload=None):
        cmd = [
            "curl", "-s", "-S", "--max-time", "30",
            "-H", f"Authorization: Bearer {self.token}",
            "-H", "Notion-Version: 2022-06-28",
            "-H", "Content-Type: application/json",
        ]
        if method != "GET":
            cmd.extend(["-X", method])
        if payload:
            cmd.extend(["-d", json.dumps(payload, ensure_ascii=False)])
        cmd.extend(["-w", r"\nHTTP_CODE:%{http_code}",
                     f"https://api.notion.com/v1{endpoint}"])
        try:
            p = subprocess.run(cmd, capture_output=True, timeout=35)
            o = p.stdout.decode("utf-8", "replace")
            if "HTTP_CODE:" not in o:
                return None
            body, code = o.rsplit("HTTP_CODE:", 1)
            code = int(code.strip())
            if code >= 400:
                if code == 429:
                    time.sleep(3)
                    return self.call(endpoint, method, payload)
                return None
            self.calls += 1
            return json.loads(body.strip()) if body.strip() else {}
        except:
            return None

    def search_all(self):
        results, cursor = [], None
        while True:
            payload = {"page_size": 100}
            if cursor: payload["start_cursor"] = cursor
            resp = self.call("/search", "POST", payload)
            if not resp: break
            results.extend(resp.get("results", []))
            if not resp.get("has_more"): break
            cursor = resp.get("next_cursor")
            time.sleep(0.3)
        return results

    def query_db_all(self, db_id):
        results, cursor = [], None
        while True:
            payload = {"page_size": 100}
            if cursor: payload["start_cursor"] = cursor
            resp = self.call(f"/databases/{db_id}/query", "POST", payload)
            if not resp: break
            results.extend(resp.get("results", []))
            if not resp.get("has_more"): break
            cursor = resp.get("next_cursor")
            time.sleep(0.3)
        return results

    def get_db(self, db_id):
        return self.call(f"/databases/{db_id}")

    def get_page_blocks(self, page_id, max_blocks=500):
        blocks, cursor = [], None
        while True:
            ep = f"/blocks/{page_id}/children?page_size=100"
            if cursor: ep += f"&start_cursor={cursor}"
            resp = self.call(ep)
            if not resp: break
            results = resp.get("results", [])
            blocks.extend(results)
            if not resp.get("has_more") or len(blocks) >= max_blocks: break
            cursor = resp.get("next_cursor")
            time.sleep(0.3)
        return blocks

    def create_database(self, parent_page_id, title, properties):
        return self.call("/databases", "POST", {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": properties,
        })

    def create_page_in_db(self, db_id, properties, children=None):
        payload = {
            "parent": {"database_id": db_id},
            "properties": properties,
        }
        if children:
            payload["children"] = children[:100]
        return self.call("/pages", "POST", payload)

    def update_page(self, page_id, properties):
        return self.call(f"/pages/{page_id}", "PATCH", {"properties": properties})


# ═══════════════════════════════════════════════
# 2. 扫描器
# ═══════════════════════════════════════════════
class Scanner:
    def __init__(self, api: NotionAPI):
        self.api = api

    @staticmethod
    def ext_title(obj):
        for v in (obj.get("properties") or {}).values():
            if isinstance(v, dict) and v.get("type") == "title":
                return "".join(t.get("plain_text", "") for t in v.get("title", []))
        return "未命名"

    def run(self):
        print("\n" + "=" * 60)
        print("🐉 龍魂 · Notion 全量扫描 v3.0")
        print("=" * 60)

        print("\n📡 搜索所有页面和数据库...")
        all_items = self.api.search_all()
        dbs = [x for x in all_items if x.get("object") == "database"]
        pages = [x for x in all_items if x.get("object") == "page"]
        print(f"   找到: {len(dbs)} 数据库 + {len(pages)} 页面 = {len(all_items)} 项")

        print("\n📊 读取数据库内容...")
        db_details = []
        for i, db in enumerate(dbs):
            db_id = db["id"].replace("-", "")
            title = self.ext_title(db)
            entries = self.api.query_db_all(db_id)
            db_details.append({
                "id": db_id, "title": title, "url": db.get("url", ""),
                "entry_count": len(entries),
                "entries": [{
                    "id": e.get("id", ""),
                    "title": self.ext_title(e),
                    "url": e.get("url", ""),
                    "last_edited": e.get("last_edited_time", ""),
                } for e in entries],
            })
            print(f"   [{i+1}/{len(dbs)}] 📁 {title} → {len(entries)} 条")

        print("\n📝 页面摘要...")
        page_summaries = [{
            "id": p.get("id", "").replace("-", ""),
            "title": self.ext_title(p),
            "url": p.get("url", ""),
            "last_edited": p.get("last_edited_time", ""),
            "parent_type": p.get("parent", {}).get("type", ""),
            "parent_db": p.get("parent", {}).get("database_id", "").replace("-", ""),
            "archived": p.get("archived", False),
        } for p in pages]

        result = {
            "scan_time": NOW(),
            "dna": f"#龍芯⚡️{NOW_TS()}-NOTION-SCAN-v3",
            "summary": {
                "total": len(all_items),
                "databases": len(dbs),
                "pages": len(pages),
                "db_entries": sum(d["entry_count"] for d in db_details),
                "api_calls": self.api.calls,
            },
            "database_details": db_details,
            "page_summaries": page_summaries,
        }

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        SCAN_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"\n✅ 扫描完成: {SCAN_FILE}")
        self._print_summary(result)
        return result

    @staticmethod
    def _print_summary(r):
        s = r["summary"]
        print(f"   数据库: {s['databases']} | 独立页面: {s['pages']} | 条目: {s['db_entries']}")
        print(f"   API调用: {s['api_calls']} 次")


# ═══════════════════════════════════════════════
# 3. 分析器
# ═══════════════════════════════════════════════
class Analyzer:
    CATEGORIES = {
        "宪法铁律": ["宪法", "铁律", "规则", "protocol", "constitution", "law", "北辰"],
        "技术文档": ["技术", "tech", "API", "SDK", "架构", "engine", "部署", "deploy", "CNSH", "代码"],
        "哲学文化": ["哲学", "易经", "道德经", "太极", "五行", "八卦", "洛书", "369", "三才", "河图"],
        "身份IP": ["UID9622", "IP", "identity", "DNA", "诸葛鑫", "龍芯", "花名册", "about"],
        "论文学术": ["论文", "paper", "IEEE", "白皮书", "whitepaper", "学术"],
        "笔记日记": ["笔记", "日记", "log", "记录", "note", "投喂", "feed", "随想"],
        "项目产品": ["项目", "project", "MVP", "产品", "app", "应用"],
        "审计安全": ["审计", "audit", "安全", "security", "防火墙", "熔断"],
        "财富金融": ["财富", "金融", "money", "currency", "支付"],
        "未分类": [],
    }

    @classmethod
    def classify(cls, title):
        text = (title or "").lower()
        scores = {}
        for cat, kws in cls.CATEGORIES.items():
            if cat == "未分类": continue
            score = sum(1 for kw in kws if kw.lower() in text)
            if score > 0: scores[cat] = score
        return max(scores, key=scores.get) if scores else "未分类"

    def analyze(self, scan):
        # 分类统计
        cat_counts = {}
        for db in scan.get("database_details", []):
            for e in db.get("entries", []):
                c = self.classify(e.get("title", ""))
                cat_counts[c] = cat_counts.get(c, 0) + 1
        for p in scan.get("page_summaries", []):
            c = self.classify(p.get("title", ""))
            cat_counts[c] = cat_counts.get(c, 0) + 1

        # 建议结构
        ideal_structure = {
            "🏛️ 宪法铁律": {"category": "宪法铁律", "props": {
                "名称": {"title": {}},
                "版本": {"rich_text": {}},
                "状态": {"select": {"options": [
                    {"name": "✅ 有效", "color": "green"},
                    {"name": "📝 草稿", "color": "yellow"},
                    {"name": "📦 归档", "color": "gray"},
                ]}},
                "优先级": {"select": {"options": [
                    {"name": "P0-不可修订", "color": "red"},
                    {"name": "P1-老大审批", "color": "orange"},
                    {"name": "P2-社区讨论", "color": "blue"},
                ]}},
            }},
            "💻 技术文档": {"category": "技术文档", "props": {
                "名称": {"title": {}},
                "模块": {"select": {"options": [
                    {"name": "CNSH", "color": "blue"},
                    {"name": "引擎", "color": "green"},
                    {"name": "鸿蒙", "color": "orange"},
                    {"name": "运维", "color": "purple"},
                    {"name": "API", "color": "pink"},
                ]}},
                "状态": {"select": {"options": [
                    {"name": "✅ 完成", "color": "green"},
                    {"name": "🚧 进行中", "color": "yellow"},
                    {"name": "📋 规划", "color": "blue"},
                ]}},
            }},
            "🧠 哲学文化": {"category": "哲学文化", "props": {
                "名称": {"title": {}},
                "维度": {"multi_select": {"options": [
                    {"name": "太极", "color": "blue"},
                    {"name": "易经", "color": "yellow"},
                    {"name": "道德经", "color": "green"},
                    {"name": "五行", "color": "red"},
                    {"name": "八卦", "color": "purple"},
                    {"name": "369", "color": "orange"},
                    {"name": "三才", "color": "brown"},
                    {"name": "河图", "color": "pink"},
                ]}},
            }},
            "🆔 身份IP": {"category": "身份IP", "props": {
                "名称": {"title": {}},
                "类型": {"select": {"options": [
                    {"name": "公开IP", "color": "green"},
                    {"name": "内部档案", "color": "yellow"},
                    {"name": "数字人", "color": "blue"},
                ]}},
            }},
            "📝 论文发表": {"category": "论文学术", "props": {
                "名称": {"title": {}},
                "期刊": {"select": {"options": [
                    {"name": "IEEE", "color": "blue"},
                    {"name": "白皮书", "color": "gray"},
                    {"name": "博客", "color": "green"},
                ]}},
                "状态": {"select": {"options": [
                    {"name": "已发表", "color": "green"},
                    {"name": "审稿中", "color": "yellow"},
                    {"name": "草稿", "color": "orange"},
                ]}},
            }},
            "📒 笔记投喂": {"category": "笔记日记", "props": {
                "名称": {"title": {}},
                "来源": {"select": {"options": [
                    {"name": "老大", "color": "red"},
                    {"name": "AI", "color": "blue"},
                    {"name": "Claude", "color": "purple"},
                    {"name": "Kimi", "color": "green"},
                    {"name": "DeepSeek", "color": "orange"},
                ]}},
                "日期": {"date": {}},
            }},
            "🛡️ 审计安全": {"category": "审计安全", "props": {
                "名称": {"title": {}},
                "级别": {"select": {"options": [
                    {"name": "🔴 严重", "color": "red"},
                    {"name": "🟡 警告", "color": "yellow"},
                    {"name": "🟢 正常", "color": "green"},
                ]}},
                "时间": {"date": {}},
            }},
            "📦 项目交付": {"category": "项目产品", "props": {
                "名称": {"title": {}},
                "阶段": {"select": {"options": [
                    {"name": "概念", "color": "blue"},
                    {"name": "开发", "color": "yellow"},
                    {"name": "已交付", "color": "green"},
                    {"name": "归档", "color": "gray"},
                ]}},
                "截止": {"date": {}},
            }},
        }

        # 查找重复
        titles_map = {}
        for db in scan.get("database_details", []):
            for e in db.get("entries", []):
                t = (e.get("title", "") or "").strip().lower()
                if len(t) > 5:
                    titles_map.setdefault(t, []).append({"type": "db_entry", "id": e.get("id"), "title": e.get("title")})
        for p in scan.get("page_summaries", []):
            t = (p.get("title", "") or "").strip().lower()
            if len(t) > 5:
                titles_map.setdefault(t, []).append({"type": "page", "id": p.get("id"), "title": p.get("title")})

        duplicates = [
            {"title": v[0]["title"], "count": len(v), "items": v}
            for v in titles_map.values() if len(v) > 1
        ]

        # 本地去重建议
        local_dedups = []
        notions = {t for t in titles_map}
        docs_dir = ROOT / "docs"
        if docs_dir.exists():
            for f in docs_dir.rglob("*.md"):
                if f.stat().st_size > 5_000_000: continue
                try:
                    first_lines = f.read_text(encoding="utf-8")[:1000]
                    for line in first_lines.splitlines():
                        line = line.strip()
                        if line.startswith("# ") and len(line) > 4:
                            lt = line[2:].strip().lower()
                            if lt in notions:
                                size_kb = f.stat().st_size // 1024
                                local_dedups.append({
                                    "path": str(f.relative_to(ROOT)),
                                    "title": line[2:].strip(),
                                    "size_kb": size_kb,
                                })
                            break
                except: pass
        local_dedups.sort(key=lambda x: -x["size_kb"])

        plan = {
            "generated_at": NOW(),
            "category_stats": cat_counts,
            "ideal_structure": ideal_structure,
            "duplicates": duplicates,
            "local_dedup_suggestions": local_dedups[:100],
            "total_local_dedup_kb": sum(d["size_kb"] for d in local_dedups),
        }
        PLAN_FILE.write_text(json.dumps(plan, ensure_ascii=False, indent=2))
        return plan


# ═══════════════════════════════════════════════
# 4. 报告
# ═══════════════════════════════════════════════
def generate_report(scan, plan):
    s = scan["summary"]
    lines = [
        f"# 🐉 龍魂 · Notion 全量整理报告",
        f"",
        f"**DNA:** `{scan['dna']}`  ",
        f"**扫描时间:** {scan['scan_time']}  ",
        f"**确认:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  ",
        f"",
        f"---",
        f"",
        f"## 📊 总览",
        f"",
        f"| 指标 | 数值 |",
        f"|---|---|",
        f"| 总项目数 | **{s['total']}** |",
        f"| 数据库 | **{s['databases']}** |",
        f"| 独立页面 | **{s['pages']}** |",
        f"| 数据库条目 | **{s['db_entries']}** |",
        f"| API 调用 | {s['api_calls']} 次 |",
        f"",
        f"## 📈 内容分类",
        f"",
        f"| 分类 | 数量 |",
        f"|---|---|",
    ]
    for cat, cnt in sorted(plan["category_stats"].items(), key=lambda x: -x[1]):
        lines.append(f"| {cat} | {cnt} |")

    lines.extend([
        f"",
        f"## 📁 数据库清单",
        f"",
    ])
    for db in scan["database_details"]:
        lines.extend([
            f"### {db['title']}",
            f"- ID: `{db['id'][:16]}...`",
            f"- 条目: **{db['entry_count']}** 条",
            f"- URL: {db.get('url', 'N/A')}",
            f"",
        ])

    lines.extend([
        f"## 🏗️ 建议新数据库结构",
        f"",
        f"| 数据库 | 目标内容 |",
        f"|---|---|",
    ])
    for name, info in plan["ideal_structure"].items():
        cnt = plan["category_stats"].get(info["category"], 0)
        lines.append(f"| {name} | {info['category']} (~{cnt}条) |")

    if plan["duplicates"]:
        lines.extend([
            f"",
            f"## ⚠️ 疑似重复 ({len(plan['duplicates'])} 组)",
            f"",
        ])
        for d in plan["duplicates"][:10]:
            lines.append(f"- **{d['title'][:50]}** — {d['count']} 个副本")

    if plan["local_dedup_suggestions"]:
        total_mb = plan["total_local_dedup_kb"] / 1024
        lines.extend([
            f"",
            f"## 💾 本地去重建议",
            f"",
            f"以下 **{len(plan['local_dedup_suggestions'])}** 个本地文件在 Notion 中已有副本，",
            f"可安全归档释放约 **{total_mb:.1f} MB** 本地存储空间：",
            f"",
            f"| # | 文件 | 标题 | KB |",
            f"|---|---|---|---|",
        ])
        for i, d in enumerate(plan["local_dedup_suggestions"][:30], 1):
            lines.append(f"| {i} | `{d['path']}` | {d['title'][:35]} | {d['size_kb']} |")

    lines.extend([
        f"",
        f"---",
        f"> 🇨🇳 中国的事情，中国人自己说了算  ",
        f"> **DNA:** `{scan['dna']}`  ",
        f"> **CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`",
    ])

    report = "\n".join(lines)
    REPORT_FILE.write_text(report)
    return report


# ═══════════════════════════════════════════════
# 5. CLI
# ═══════════════════════════════════════════════
def main():
    p = argparse.ArgumentParser(description="龍魂 Notion 全量同步整理器 v3.0")
    p.add_argument("--execute", action="store_true", help="执行整理（在 Notion 创建新数据库结构）")
    p.add_argument("--report-only", action="store_true", help="仅基于已有扫描生成报告")
    args = p.parse_args()

    api = NotionAPI()

    if args.report_only:
        if not SCAN_FILE.exists():
            print(f"❌ 扫描文件不存在: {SCAN_FILE}\n   请先运行 python3 bin/lh_notion_full_sync.py")
            sys.exit(1)
        scan = json.loads(SCAN_FILE.read_text())
    else:
        scanner = Scanner(api)
        scan = scanner.run()

    analyzer = Analyzer()
    plan = analyzer.analyze(scan)
    report = generate_report(scan, plan)

    print(f"\n📄 报告: {REPORT_FILE}")
    print(f"📐 方案: {PLAN_FILE}")

    # 打印关键发现
    print(f"\n{'='*60}")
    print(f"🔑 关键发现:")
    print(f"{'='*60}")
    print(f"  📊 {scan['summary']['total']} 个 Notion 项目待整理")
    if plan["duplicates"]:
        print(f"  ⚠️ {len(plan['duplicates'])} 组疑似重复内容")
    if plan["local_dedup_suggestions"]:
        kb = plan["total_local_dedup_kb"]
        print(f"  💾 {len(plan['local_dedup_suggestions'])} 个本地文件可归档 → 释放 ~{kb/1024:.1f}MB")
    print(f"  🏗️ 建议 {len(plan['ideal_structure'])} 个主题数据库")

    if args.execute:
        print(f"\n⚠️  执行模式暂为预览。请先在 Notion 端确认报告后再执行整理。")
        print(f"   整理报告: {REPORT_FILE}")

    print(f"\n✅ 完成. DNA: #龍芯⚡️{NOW_TS()}-NOTION-FULL-SYNC-v3.0")

if __name__ == "__main__":
    main()
