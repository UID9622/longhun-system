#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·壬戌·亥时·䷬萃-NOTION-CLI-v1.0-UID9622-B18B81B3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂 · Notion 统一入口 v1.0

把散落在 50+ 脚本里的 Notion 能力统一成一个主控台。

用法:
    python3 08_BIN/lh_notion.py scan            # 扫描 Notion 全量页面/数据库
    python3 08_BIN/lh_notion.py health          # Notion 健康度检查
    python3 08_BIN/lh_notion.py list            # 列出所有页面标题
    python3 08_BIN/lh_notion.py pull --page-id <id>  # 拉取单页面为 Markdown

配置来源:
    config/notion_config.json

协议: CC BY-NC-SA 4.0 (思想层) · MulanPSL v2 (工程层)
"""

import argparse
import json
import os
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 让导入能找到 core.longhun_core.dna_trace
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.longhun_core.dna_trace import generate_dna

# ═══════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "notion_config.json"
MIRROR_DIR = PROJECT_ROOT / "12_DOCS" / "notion_mirror"
REPORT_DIR = PROJECT_ROOT / "12_DOCS" / "notion_mirror"
CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
DNA_ANY_RE = re.compile(r'#龍芯⚡️\S+')


# ═══════════════════════════════════════════════════════
# Notion API 客户端
# ═══════════════════════════════════════════════════════
class NotionClient:
    def __init__(self, token: str):
        self.token = token
        self.base = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }
        # 带重试的会话：连接错误/429/5xx 自动重试 3 次
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session = requests.Session()
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def search(self, query: str = "", page_size: int = 100) -> List[Dict[str, Any]]:
        """分页搜索所有可访问页面和数据库"""
        results = []
        cursor = None
        while True:
            payload = {"page_size": page_size, "query": query}
            if cursor:
                payload["start_cursor"] = cursor
            resp = self.session.post(
                f"{self.base}/search",
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            results.extend(data.get("results", []))
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
        return results

    def get_page(self, page_id: str) -> Dict[str, Any]:
        resp = self.session.get(
            f"{self.base}/pages/{page_id}",
            headers=self.headers,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def get_block_children(self, block_id: str) -> List[Dict[str, Any]]:
        results = []
        cursor = None
        while True:
            payload = {"page_size": 100}
            if cursor:
                payload["start_cursor"] = cursor
            resp = self.session.get(
                f"{self.base}/blocks/{block_id}/children",
                headers=self.headers,
                params=payload,
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            results.extend(data.get("results", []))
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
        return results


# ═══════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════
def load_config() -> Dict[str, str]:
    if not CONFIG_PATH.exists():
        print(f"❌ 找不到 Notion 配置: {CONFIG_PATH}", file=sys.stderr)
        print("   请创建 config/notion_config.json，包含 notion_token", file=sys.stderr)
        sys.exit(2)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_title(item: Dict[str, Any]) -> str:
    """从页面或数据库中提取标题"""
    obj = item.get("object")
    if obj == "page":
        props = item.get("properties", {})
        # title 类型
        title_prop = props.get("title", {})
        if "title" in title_prop:
            return "".join(t.get("plain_text", "") for t in title_prop["title"])
        # 其他可能的标题属性名
        for key, val in props.items():
            if val.get("type") == "title":
                return "".join(t.get("plain_text", "") for t in val.get("title", []))
    elif obj == "database":
        return "".join(t.get("plain_text", "") for t in item.get("title", []))
    return ""


def extract_url(item: Dict[str, Any]) -> str:
    return item.get("url", "")


def extract_last_edited(item: Dict[str, Any]) -> str:
    return item.get("last_edited_time", "")


def has_dna(title: str, item: Dict[str, Any]) -> bool:
    """检查标题或任何属性中是否含 DNA"""
    if DNA_ANY_RE.search(title):
        return True
    text = json.dumps(item, ensure_ascii=False)
    return bool(DNA_ANY_RE.search(text))


def mirror_path_for_page(page_id: str, title: str, base_dir: Path = MIRROR_DIR) -> Path:
    """本地镜像路径"""
    safe_title = re.sub(r'[^\w\u4e00-\u9fff\-]+', '_', title).strip('_')[:60]
    name = f"{safe_title or 'untitled'}_{page_id.replace('-', '')}.md"
    return base_dir / name


# ═══════════════════════════════════════════════════════
# 命令实现
# ═══════════════════════════════════════════════════════
def cmd_scan(args: argparse.Namespace):
    config = load_config()
    client = NotionClient(config["notion_token"])

    print("🔍 正在扫描 Notion 工作区...")
    results = client.search()

    pages = [r for r in results if r.get("object") == "page"]
    databases = [r for r in results if r.get("object") == "database"]

    report = {
        "dna": generate_dna("NOTION-SCAN", "UID9622"),
        "confirm": CONFIRM_MARK,
        "timestamp": datetime.now().isoformat(),
        "workspace": config.get("workspace", "unknown"),
        "total": len(results),
        "pages": [
            {
                "id": p.get("id"),
                "title": extract_title(p),
                "url": extract_url(p),
                "last_edited": extract_last_edited(p),
            }
            for p in pages
        ],
        "databases": [
            {
                "id": d.get("id"),
                "title": extract_title(d),
                "url": extract_url(d),
            }
            for d in databases
        ],
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = REPORT_DIR / f"notion_scan_{datetime.now():%Y%m%d_%H%M%S}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n📊 扫描完成")
    print(f"   总条目: {len(results)}")
    print(f"   页面: {len(pages)}")
    print(f"   数据库: {len(databases)}")
    print(f"💾 报告: {out_path}")
    return out_path


def cmd_health(args: argparse.Namespace):
    config = load_config()
    client = NotionClient(config["notion_token"])

    print("🏥 正在检查 Notion 健康度...")
    results = client.search()
    pages = [r for r in results if r.get("object") == "page"]

    issues = {
        "untitled": [],
        "missing_dna": [],
        "missing_mirror": [],
        "duplicated_titles": defaultdict(list),
    }

    title_counts = Counter()
    for p in pages:
        title = extract_title(p)
        page_id = p.get("id", "")
        url = extract_url(p)
        title_counts[title] += 1

        if not title or title == "无标题":
            issues["untitled"].append({"id": page_id, "url": url})
        elif not has_dna(title, p):
            issues["missing_dna"].append({"id": page_id, "title": title, "url": url})

        mirror_path = mirror_path_for_page(page_id, title)
        if not mirror_path.exists():
            issues["missing_mirror"].append({
                "id": page_id,
                "title": title,
                "url": url,
                "expected_path": str(mirror_path.relative_to(PROJECT_ROOT)),
            })

    for title, count in title_counts.items():
        if count > 1 and title:
            issues["duplicated_titles"][title] = count

    total_pages = len(pages)
    untitled_rate = len(issues["untitled"]) / total_pages if total_pages else 0
    missing_dna_rate = len(issues["missing_dna"]) / total_pages if total_pages else 0
    missing_mirror_rate = len(issues["missing_mirror"]) / total_pages if total_pages else 0
    duplicate_rate = len(issues["duplicated_titles"]) / total_pages if total_pages else 0

    # 基于百分比扣分，避免页面多就归零
    health_score = max(
        0,
        100
        - int(untitled_rate * 30)
        - int(missing_dna_rate * 30)
        - int(missing_mirror_rate * 20)
        - int(duplicate_rate * 20),
    )

    report = {
        "dna": generate_dna("NOTION-HEALTH", "UID9622"),
        "confirm": CONFIRM_MARK,
        "timestamp": datetime.now().isoformat(),
        "workspace": config.get("workspace", "unknown"),
        "total_pages": len(pages),
        "health_score": health_score,
        "issues": {
            "untitled_count": len(issues["untitled"]),
            "missing_dna_count": len(issues["missing_dna"]),
            "missing_mirror_count": len(issues["missing_mirror"]),
            "duplicated_title_count": len(issues["duplicated_titles"]),
            "untitled": issues["untitled"][:20],
            "missing_dna": issues["missing_dna"][:20],
            "missing_mirror": issues["missing_mirror"][:20],
            "duplicated_titles": dict(issues["duplicated_titles"]),
        },
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = REPORT_DIR / f"notion_health_{datetime.now():%Y%m%d_%H%M%S}.json"
    md_path = REPORT_DIR / f"notion_health_{datetime.now():%Y%m%d_%H%M%S}.md"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    md = _build_health_markdown(report)
    md_path.write_text(md, encoding="utf-8")

    print(f"\n🏥 Notion 健康度检查完成")
    print(f"   页面总数: {len(pages)}")
    print(f"   健康评分: {health_score}/100")
    print(f"   🔴 无标题: {len(issues['untitled'])}")
    print(f"   🔴 缺 DNA: {len(issues['missing_dna'])}")
    print(f"   🟡 缺本地镜像: {len(issues['missing_mirror'])}")
    print(f"   🟡 重复标题: {len(issues['duplicated_titles'])}")
    print(f"💾 JSON: {json_path}")
    print(f"📄 Markdown: {md_path}")
    return json_path, md_path


def _build_health_markdown(report: Dict[str, Any]) -> str:
    issues = report["issues"]
    md = f"""# 🐉 龍魂 · Notion 健康度报告

**DNA:** `{report['dna']}`  
**确认码:** `{report['confirm']}`  
**生成时间:** {report['timestamp']}  
**工作区:** {report['workspace']}

---

## 📊 总览

| 指标 | 数值 |
|:---|---:|
| 页面总数 | **{report['total_pages']}** |
| 健康评分 | **{report['health_score']}/100** |
| 🔴 无标题页面 | **{issues['untitled_count']}** |
| 🔴 缺 DNA 页面 | **{issues['missing_dna_count']}** |
| 🟡 缺本地镜像 | **{issues['missing_mirror_count']}** |
| 🟡 重复标题 | **{issues['duplicated_title_count']}** |

---

## 🔴 无标题页面（前20）

"""
    if issues["untitled"]:
        for item in issues["untitled"]:
            md += f"- [{item['id']}]({item['url']})\n"
    else:
        md += "✅ 无\n"

    md += "\n## 🔴 缺 DNA 页面（前20）\n\n"
    if issues["missing_dna"]:
        for item in issues["missing_dna"]:
            md += f"- **{item['title']}** — [{item['id']}]({item['url']})\n"
    else:
        md += "✅ 无\n"

    md += "\n## 🟡 缺本地镜像（前20）\n\n"
    if issues["missing_mirror"]:
        for item in issues["missing_mirror"]:
            md += f"- **{item['title']}** — 应镜像到 `{item['expected_path']}`\n"
    else:
        md += "✅ 无\n"

    md += "\n## 🟡 重复标题\n\n"
    if issues["duplicated_titles"]:
        for title, count in issues["duplicated_titles"].items():
            md += f"- **{title}**: {count} 个页面\n"
    else:
        md += "✅ 无\n"

    md += f"""
---

## 🚀 下一步建议

```bash
# 全量拉取 Notion 到本地镜像
python3 08_BIN/lh_notion.py pull-all

# 给缺 DNA 的页面批量补签章
python3 08_BIN/lh_notion.py seal-missing-dna

# 导出无标题页面清单
python3 08_BIN/lh_notion.py export-untitled
```

---

**DNA:** `{report['dna']}`  
**确认码:** `{report['confirm']}`
"""
    return md


def cmd_list(args: argparse.Namespace):
    config = load_config()
    client = NotionClient(config["notion_token"])
    results = client.search()
    pages = [r for r in results if r.get("object") == "page"]

    print(f"\n📄 Notion 页面列表 ({len(pages)} 个)\n")
    print(f"{'#':<4} {'标题':<50} {'ID':<36}")
    print("-" * 90)
    for i, p in enumerate(pages, 1):
        title = extract_title(p) or "(无标题)"
        print(f"{i:<4} {title[:48]:<50} {p.get('id', '')}")


def cmd_pull(args: argparse.Namespace):
    config = load_config()
    client = NotionClient(config["notion_token"])

    page_id = args.page_id
    print(f"📥 拉取页面: {page_id}")
    page = client.get_page(page_id)
    title = extract_title(page)
    blocks = client.get_block_children(page_id)

    MIRROR_DIR.mkdir(parents=True, exist_ok=True)
    out_path = mirror_path_for_page(page_id, title)

    lines = [f"# {title or '无标题'}\n", f"\n> Notion URL: {page.get('url', '')}\n"]
    for b in blocks:
        block_type = b.get("type", "")
        text = _block_to_markdown(b)
        if text:
            lines.append(text + "\n")

    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"💾 已保存: {out_path}")


def cmd_pull_all(args: argparse.Namespace):
    """全量拉取 Notion 页面到本地镜像"""
    import time

    config = load_config()
    client = NotionClient(config["notion_token"])
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    progress_path = output_dir / ".pull_all_progress.json"

    progress: Dict[str, Any] = {
        "done_ids": [],
        "errors": [],
        "skipped": [],
        "total": 0,
        "processed": 0,
        "last_updated": datetime.now().isoformat(),
    }
    if args.resume and progress_path.exists():
        try:
            progress = json.loads(progress_path.read_text(encoding="utf-8"))
            print(f"🔄 从进度文件恢复：已处理 {len(progress.get('done_ids', []))} 个页面")
        except Exception as e:
            print(f"⚠️ 进度文件损坏，重新开始: {e}", file=sys.stderr)

    done_ids: set = set(progress.get("done_ids", []))
    errors: List[Dict[str, Any]] = list(progress.get("errors", []))
    skipped: List[Dict[str, Any]] = list(progress.get("skipped", []))

    print("🔍 正在搜索 Notion 工作区...")
    results = client.search()
    pages = [r for r in results if r.get("object") == "page"]
    total = len(pages)
    progress["total"] = total
    print(f"📄 共发现 {total} 个页面")

    start_time = datetime.now()
    processed_this_run = 0
    limit = args.limit or total

    for i, page_meta in enumerate(pages, 1):
        page_id = page_meta.get("id")
        if not page_id or page_id in done_ids:
            continue
        if processed_this_run >= limit:
            print(f"⏹️ 已达到 --limit {limit}，停止")
            break

        try:
            # 复用 search 结果中的页面元数据，避免额外 get_page 请求
            title = extract_title(page_meta)
            blocks = client.get_block_children(page_id)

            out_path = mirror_path_for_page(page_id, title, base_dir=output_dir)
            lines = [
                f"# {title or '无标题'}\n",
                f"\n> Notion URL: {extract_url(page_meta)}\n",
                f"> Last edited: {extract_last_edited(page_meta)}\n",
            ]
            for b in blocks:
                text = _block_to_markdown(b)
                if text:
                    lines.append(text + "\n")

            out_path.write_text("".join(lines), encoding="utf-8")
            done_ids.add(page_id)
            processed_this_run += 1
            print(f"[{i:>5}/{total}] ✅ {title or '无标题'}")
        except KeyboardInterrupt:
            print("\n🛑 用户中断，保存进度...")
            break
        except Exception as e:
            err_info = {"id": page_id, "error": str(e), "time": datetime.now().isoformat()}
            errors.append(err_info)
            print(f"[{i:>5}/{total}] ❌ {page_id}: {e}", file=sys.stderr)

        # 每处理一页保存一次进度
        progress.update({
            "done_ids": list(done_ids),
            "errors": errors,
            "skipped": skipped,
            "processed": len(done_ids),
            "last_updated": datetime.now().isoformat(),
        })
        progress_path.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")

        time.sleep(args.delay)

    elapsed = (datetime.now() - start_time).total_seconds()
    report = {
        "dna": generate_dna("NOTION-PULL-ALL", "UID9622"),
        "confirm": CONFIRM_MARK,
        "timestamp": datetime.now().isoformat(),
        "workspace": config.get("workspace", "unknown"),
        "total_pages": total,
        "processed": len(done_ids),
        "errors": len(errors),
        "elapsed_seconds": elapsed,
        "output_dir": str(output_dir),
        "progress_file": str(progress_path),
    }
    report_path = output_dir / f"pull_all_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n📊 Notion 全量镜像报告")
    print(f"   总页面: {total}")
    print(f"   已处理: {len(done_ids)}")
    print(f"   本次处理: {processed_this_run}")
    print(f"   错误: {len(errors)}")
    print(f"   耗时: {elapsed:.1f}s")
    print(f"💾 进度: {progress_path}")
    print(f"📄 报告: {report_path}")


def _block_to_markdown(block: Dict[str, Any]) -> str:
    """简单把 Notion block 转成 Markdown"""
    bt = block.get("type", "")
    if bt in ("paragraph", "heading_1", "heading_2", "heading_3",
              "bulleted_list_item", "numbered_list_item", "quote"):
        rich = block.get(bt, {}).get("rich_text", [])
        text = "".join(t.get("plain_text", "") for t in rich)
        if bt == "heading_1":
            return f"# {text}"
        elif bt == "heading_2":
            return f"## {text}"
        elif bt == "heading_3":
            return f"### {text}"
        elif bt == "bulleted_list_item":
            return f"- {text}"
        elif bt == "numbered_list_item":
            return f"1. {text}"
        elif bt == "quote":
            return f"> {text}"
        return text
    elif bt == "code":
        rich = block.get("code", {}).get("rich_text", [])
        text = "".join(t.get("plain_text", "") for t in rich)
        lang = block.get("code", {}).get("language", "")
        return f"```{lang}\n{text}\n```"
    elif bt == "divider":
        return "---"
    return ""


# ═══════════════════════════════════════════════════════
# Notion 归档数据库
# ═══════════════════════════════════════════════════════

ARCHIVE_DB_PATH = MIRROR_DIR / "notion_archive.db"


DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS archive_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna TEXT,
    confirm TEXT,
    started_at TEXT,
    completed_at TEXT,
    workspace TEXT,
    pages_total INTEGER,
    pages_updated INTEGER,
    blocks_total INTEGER,
    errors_count INTEGER
);

CREATE TABLE IF NOT EXISTS pages (
    id TEXT PRIMARY KEY,
    title TEXT,
    url TEXT,
    created_time TEXT,
    last_edited_time TEXT,
    archived_at TEXT,
    markdown_path TEXT,
    json_blob TEXT
);

CREATE TABLE IF NOT EXISTS blocks (
    id TEXT PRIMARY KEY,
    page_id TEXT NOT NULL,
    block_type TEXT,
    content TEXT,
    json_blob TEXT,
    archived_at TEXT,
    FOREIGN KEY (page_id) REFERENCES pages(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_blocks_page_id ON blocks(page_id);
CREATE INDEX IF NOT EXISTS idx_pages_last_edited ON pages(last_edited_time);
"""


def _init_archive_db(db_path: Path) -> sqlite3.Connection:
    """初始化归档数据库"""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.executescript(DB_SCHEMA)
    conn.commit()
    return conn


def _get_db_last_edited(conn: sqlite3.Connection) -> Dict[str, str]:
    """获取数据库中所有页面最后的 last_edited_time"""
    cursor = conn.execute("SELECT id, last_edited_time FROM pages")
    return {row[0]: row[1] or "" for row in cursor.fetchall()}


def _save_page(conn: sqlite3.Connection, page: Dict[str, Any], blocks: List[Dict[str, Any]],
               output_dir: Path, archived_at: str) -> Path:
    """保存单个页面到数据库和 Markdown"""
    page_id = page.get("id", "")
    title = extract_title(page)
    url = extract_url(page)
    created_time = page.get("created_time", "")
    last_edited_time = page.get("last_edited_time", "")

    # Markdown 文件
    out_path = mirror_path_for_page(page_id, title, base_dir=output_dir)
    lines = [
        f"# {title or '无标题'}\n",
        f"\n> Notion URL: {url}\n",
        f"> Created: {created_time}\n",
        f"> Last edited: {last_edited_time}\n",
        f"> Archived at: {archived_at}\n",
    ]
    for b in blocks:
        text = _block_to_markdown(b)
        if text:
            lines.append(text + "\n")
    out_path.write_text("".join(lines), encoding="utf-8")

    # 写入/更新 pages 表
    conn.execute(
        """INSERT INTO pages (id, title, url, created_time, last_edited_time,
                            archived_at, markdown_path, json_blob)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(id) DO UPDATE SET
               title=excluded.title,
               url=excluded.url,
               created_time=excluded.created_time,
               last_edited_time=excluded.last_edited_time,
               archived_at=excluded.archived_at,
               markdown_path=excluded.markdown_path,
               json_blob=excluded.json_blob""",
        (page_id, title, url, created_time, last_edited_time,
         archived_at, str(out_path.relative_to(PROJECT_ROOT)),
         json.dumps(page, ensure_ascii=False)),
    )

    # 删除旧 blocks，写入新 blocks
    conn.execute("DELETE FROM blocks WHERE page_id = ?", (page_id,))
    for b in blocks:
        block_id = b.get("id", "")
        block_type = b.get("type", "")
        content = _block_to_markdown(b)
        conn.execute(
            """INSERT INTO blocks (id, page_id, block_type, content, json_blob, archived_at)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                   page_id=excluded.page_id,
                   block_type=excluded.block_type,
                   content=excluded.content,
                   json_blob=excluded.json_blob,
                   archived_at=excluded.archived_at""",
            (block_id, page_id, block_type, content,
             json.dumps(b, ensure_ascii=False), archived_at),
        )

    conn.commit()
    return out_path


def cmd_archive(args: argparse.Namespace):
    """把 Notion 页面增量归档到 SQLite 数据库"""
    import time

    config = load_config()
    client = NotionClient(config["notion_token"])
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    db_path = Path(args.db_path).resolve() if args.db_path else ARCHIVE_DB_PATH

    conn = _init_archive_db(db_path)
    db_last_edited = _get_db_last_edited(conn)

    started_at = datetime.now().isoformat()
    archived_at = started_at
    dna = generate_dna("NOTION-ARCHIVE", "UID9622")

    print("🔍 正在搜索 Notion 工作区...")
    results = client.search()
    pages = [r for r in results if r.get("object") == "page"]
    total = len(pages)
    print(f"📄 共发现 {total} 个页面")

    updated = 0
    skipped = 0
    blocks_total = 0
    errors: List[Dict[str, Any]] = []

    for i, page in enumerate(pages, 1):
        page_id = page.get("id", "")
        title = extract_title(page)
        notion_edited = page.get("last_edited_time", "")
        db_edited = db_last_edited.get(page_id, "")

        # 增量判断：数据库中已存在且 last_edited_time 未变则跳过
        if db_edited and notion_edited <= db_edited:
            skipped += 1
            if i % 100 == 0 or i == total:
                print(f"[{i:>5}/{total}] ⏭️ 跳过未变化页面 ({skipped} 已跳过)")
            continue

        try:
            blocks = client.get_block_children(page_id)
            _save_page(conn, page, blocks, output_dir, archived_at)
            blocks_total += len(blocks)
            updated += 1
            print(f"[{i:>5}/{total}] ✅ {title or '无标题'}")
        except Exception as e:
            errors.append({"id": page_id, "error": str(e), "time": datetime.now().isoformat()})
            print(f"[{i:>5}/{total}] ❌ {page_id}: {e}", file=sys.stderr)

        time.sleep(args.delay)

    completed_at = datetime.now().isoformat()
    conn.execute(
        """INSERT INTO archive_runs
           (dna, confirm, started_at, completed_at, workspace,
            pages_total, pages_updated, blocks_total, errors_count)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (dna, CONFIRM_MARK, started_at, completed_at,
         config.get("workspace", "unknown"), total, updated,
         blocks_total, len(errors)),
    )
    conn.commit()
    conn.close()

    print(f"\n📊 Notion 归档完成")
    print(f"   总页面: {total}")
    print(f"   本次更新: {updated}")
    print(f"   跳过未变化: {skipped}")
    print(f"   Blocks 总数: {blocks_total}")
    print(f"   错误: {len(errors)}")
    print(f"💾 数据库: {db_path}")
    print(f"🧬 DNA: {dna}")


def cmd_install_cron(args: argparse.Namespace):
    """安装 Notion 归档定时任务"""
    cron_line = (
        f"0 2 * * * cd {PROJECT_ROOT} && "
        f"/usr/bin/python3 08_BIN/lh_notion.py archive "
        f"--output-dir {args.output_dir} "
        f">> 12_DOCS/notion_mirror/archive_cron.log 2>&1"
    )

    # 读取现有 crontab
    result = os.popen("crontab -l 2>/dev/null").read()
    existing_lines = result.splitlines() if result else []

    # 去重：如果已有 lh_notion.py archive，先移除旧条目
    marker = "lh_notion.py archive"
    new_lines = [line for line in existing_lines if marker not in line]
    new_lines.append(cron_line)

    new_crontab = "\n".join(new_lines) + "\n"
    proc = os.popen("crontab -", "w")
    proc.write(new_crontab)
    proc.close()

    print("✅ Notion 归档定时任务已安装")
    print(f"   规则: {cron_line}")
    print("   每天 02:00 自动增量归档")


# ═══════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · Notion 统一入口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 08_BIN/lh_notion.py scan
  python3 08_BIN/lh_notion.py health
  python3 08_BIN/lh_notion.py list
  python3 08_BIN/lh_notion.py pull --page-id <uuid>
  python3 08_BIN/lh_notion.py pull-all
  python3 08_BIN/lh_notion.py pull-all --resume --limit 100
  python3 08_BIN/lh_notion.py archive
  python3 08_BIN/lh_notion.py archive --install-cron
        """,
    )
    sub = parser.add_subparsers(dest="command", help="子命令")

    sub.add_parser("scan", help="扫描 Notion 工作区所有页面和数据库")
    sub.add_parser("health", help="Notion 健康度检查")
    sub.add_parser("list", help="列出所有页面")

    p_pull = sub.add_parser("pull", help="拉取单页面到本地镜像")
    p_pull.add_argument("--page-id", required=True, help="Notion 页面 ID")

    p_pull_all = sub.add_parser("pull-all", help="全量拉取 Notion 页面到本地镜像")
    p_pull_all.add_argument("--output-dir", type=str, default=str(MIRROR_DIR),
                            help=f"镜像输出目录 (默认: {MIRROR_DIR})")
    p_pull_all.add_argument("--resume", action="store_true",
                            help="从进度文件断点续传")
    p_pull_all.add_argument("--delay", type=float, default=0.35,
                            help="请求间隔秒数，避免触发 Notion rate limit (默认: 0.35)")
    p_pull_all.add_argument("--limit", type=int, default=0,
                            help="限制本次处理页面数 (0=无限制)")

    p_archive = sub.add_parser("archive", help="把 Notion 页面增量归档到 SQLite 数据库")
    p_archive.add_argument("--output-dir", type=str, default=str(MIRROR_DIR),
                           help=f"Markdown 输出目录 (默认: {MIRROR_DIR})")
    p_archive.add_argument("--db-path", type=str, default=str(ARCHIVE_DB_PATH),
                           help=f"SQLite 数据库路径 (默认: {ARCHIVE_DB_PATH})")
    p_archive.add_argument("--delay", type=float, default=0.35,
                           help="请求间隔秒数 (默认: 0.35)")
    p_archive.add_argument("--install-cron", action="store_true",
                           help="安装每天 02:00 自动归档的 crontab 任务")

    args = parser.parse_args()

    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "health":
        cmd_health(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "pull":
        cmd_pull(args)
    elif args.command == "pull-all":
        cmd_pull_all(args)
    elif args.command == "archive":
        if args.install_cron:
            cmd_install_cron(args)
        else:
            cmd_archive(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
