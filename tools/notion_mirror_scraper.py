#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · Notion 公開頁面瀏覽器鏡像爬蟲 v1.0

用途：
  當 Notion API integration 未被共享到頁面時，用 Playwright 瀏覽器兜底抓取
  公開 Notion 頁面的純文本內容，轉為本地 Markdown/JSON 鏡像。

用法：
  # 同步單頁
  python3 notion_mirror_scraper.py --url "https://uid9622.notion.site/xxx"

  # 按配置批量同步（預設）
  python3 notion_mirror_scraper.py --config config/notion_sync.json

  # 僅同步 Top N 個優先頁面
  python3 notion_mirror_scraper.py --top 10

DNA: #龍芯⚡️2026-07-05-NOTION-MIRROR-SCRAPER-v1.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# ═══════════════════════════════════════════
# 0. 路徑與配置
# ═══════════════════════════════════════════
HOME = Path.home()
LONGHUN_ROOT = Path(__file__).resolve().parent.parent
MIRROR_DIR = LONGHUN_ROOT / "docs" / "notion_mirror" / "pages"
STATUS_FILE = LONGHUN_ROOT / "docs" / "notion_mirror" / "mirror_status.json"
PRIORITY_FILE = LONGHUN_ROOT / "docs" / "notion_mirror" / "uid9622_todo_priority_top50.json"
TODO_FILE = LONGHUN_ROOT / "docs" / "notion_mirror" / "uid9622_todo_index.json"
DEFAULT_CONFIG = LONGHUN_ROOT / "config" / "notion_sync.json"

MIRROR_DIR.mkdir(parents=True, exist_ok=True)

DNA_PREFIX = "#龍芯⚡️"


def now_iso() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat()


def make_dna(op: str) -> str:
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    raw = f"{op}-{ts}-{uuid.uuid4().hex[:8]}"
    h = hashlib.sha256(raw.encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{ts}-NOTION-MIRROR-{op}-{h}"


def page_id_from_url(url: str) -> str:
    """從 uid9622.notion.site/<page_id>?... 提取 page_id"""
    m = re.search(r"notion\.site/([a-f0-9]+)", url)
    if m:
        return m.group(1)
    m = re.search(r"([a-f0-9]{32})", url)
    if m:
        return m.group(1)
    raise ValueError(f"無法從 URL 提取 page_id: {url}")


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


# ═══════════════════════════════════════════
# 1. Playwright 抓取
# ═══════════════════════════════════════════
def scrape_page(url: str, headless: bool = True, timeout_ms: int = 60000) -> Dict[str, Any]:
    """返回 {page_id, title, url, text, blocks, scraped_at, dna, ok, error}
    
    Notion 會攔截 Chromium 無頭瀏覽器（導向 unsupported-browser.html），
    因此預設使用 WebKit，失敗再回退 Chromium。
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        return {"url": url, "ok": False, "error": f"未安裝 playwright: {e}"}

    result = {
        "page_id": page_id_from_url(url),
        "url": url,
        "scraped_at": now_iso(),
        "dna": make_dna("SCRAPE"),
        "ok": False,
        "title": None,
        "text": "",
        "blocks": [],
        "error": None,
    }

    engines = [("webkit", lambda p: p.webkit.launch(headless=headless)),
               ("chromium", lambda p: p.chromium.launch(headless=headless))]

    with sync_playwright() as p:
        for engine_name, launch in engines:
            browser = None
            try:
                browser = launch(p)
                context = browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
                    )
                )
                page = context.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
                page.wait_for_selector("[data-block-id]", timeout=timeout_ms)
                # 滾動觸發懶加載
                page.evaluate("() => { window.scrollTo(0, document.body.scrollHeight); }")
                page.wait_for_timeout(1500)

                title = page.title()
                # Notion 在 WebKit 下 title 常為 "Notion"，改從首個內容塊取標題
                blocks = page.evaluate("""() => {
                    const out = [];
                    document.querySelectorAll('[data-block-id]').forEach(b => {
                        const t = b.innerText.replace(/\\s+/g, ' ').trim();
                        if (t && t.length > 1) out.push(t);
                    });
                    return out;
                }""")
                if title in ("Notion", "", None) and blocks:
                    title = blocks[0][:120]
                result["title"] = title
                result["blocks"] = blocks
                result["text"] = "\n\n".join(blocks)
                result["ok"] = True
                result["engine"] = engine_name
                break
            except Exception as e:
                result["error"] = f"[{engine_name}] {e}"
            finally:
                if browser:
                    browser.close()

    return result


# ═══════════════════════════════════════════
# 2. Markdown / JSON 輸出
# ═══════════════════════════════════════════
def save_mirror(result: Dict[str, Any]) -> Path:
    pid = result["page_id"]
    safe_title = re.sub(r"[^\\w\\u4e00-\\u9fff]+", "_", result.get("title") or pid)[:60]

    # JSON
    json_path = MIRROR_DIR / f"{pid}.json"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    # Markdown
    md_path = MIRROR_DIR / f"{pid}.md"
    lines = [
        f"<!-- {result['dna']} -->",
        f"# {result.get('title') or 'Untitled'}",
        "",
        f"- **URL**: {result['url']}",
        f"- **Page ID**: {result['page_id']}",
        f"- **Scraped At**: {result['scraped_at']}",
        f"- **Blocks**: {len(result['blocks'])}",
        f"- **DNA**: {result['dna']}",
        "",
        "---",
        "",
        result["text"],
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")

    return md_path


# ═══════════════════════════════════════════
# 3. 配置與批量
# ═══════════════════════════════════════════
def load_config(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_priority_list(path: Path = PRIORITY_FILE) -> List[Dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("recommendations", [])


def load_todo_list(path: Path = TODO_FILE) -> List[Dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("links", [])


def run_batch(urls: List[str], headless: bool = True, delay: float = 2.0) -> List[Dict[str, Any]]:
    results = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] 抓取 {url}")
        r = scrape_page(url, headless=headless)
        if r["ok"]:
            md_path = save_mirror(r)
            print(f"       ✅ 已保存 {md_path}")
        else:
            print(f"       🔴 失敗: {r['error']}")
        results.append(r)
        if i < len(urls):
            import time
            time.sleep(delay)
    return results


def save_status(results: List[Dict[str, Any]], run_dna: str):
    ok_count = sum(1 for r in results if r["ok"])
    status = {
        "run_dna": run_dna,
        "run_at": now_iso(),
        "total": len(results),
        "ok": ok_count,
        "failed": len(results) - ok_count,
        "pages": [
            {
                "page_id": r["page_id"],
                "title": r.get("title"),
                "url": r["url"],
                "ok": r["ok"],
                "error": r.get("error"),
                "blocks": len(r.get("blocks", [])),
                "dna": r.get("dna"),
            }
            for r in results
        ],
    }
    STATUS_FILE.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n鏡像狀態已保存: {STATUS_FILE}")
    print(f"成功: {ok_count} / {len(results)}")


# ═══════════════════════════════════════════
# 4. CLI
# ═══════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(description="龍魂 Notion 公開頁面瀏覽器鏡像爬蟲")
    parser.add_argument("--url", help="同步單個 Notion 公開頁面 URL")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="批量配置文件")
    parser.add_argument("--top", type=int, default=0, help="只同步優先級 Top N 頁面")
    parser.add_argument("--headless", type=lambda x: x.lower() in ("1", "true", "yes"), default=True, help="是否無頭模式")
    parser.add_argument("--delay", type=float, default=2.0, help="頁面間延遲秒數")
    args = parser.parse_args()

    run_dna = make_dna("BATCH")
    print(f"=== 龍魂 Notion 鏡像爬蟲 ===")
    print(f"Run DNA: {run_dna}")
    print(f"Time: {now_iso()}")

    urls: List[str] = []

    if args.url:
        urls = [args.url]
    elif args.top > 0:
        items = load_priority_list()[: args.top]
        urls = [item["href"] for item in items]
        print(f"從優先級列表載入 Top {len(urls)} 頁面")
    else:
        cfg = load_config(args.config)
        for m in cfg.get("mappings", []):
            if m.get("direction") in ("pull", "sync"):
                pid = m.get("notion_page_id")
                if pid:
                    urls.append(f"https://uid9622.notion.site/{pid}")
        if not urls:
            # 預設從待辦頁 + Top 6 開始
            urls = ["https://uid9622.notion.site/34f7125a9c9f80b9951cee661375dd09"]
            urls += [item["href"] for item in load_priority_list()[:6]]
            urls = list(dict.fromkeys(urls))
            print(f"未找到配置映射，使用默認：待辦頁 + Top {len(urls) - 1} 頁面")
        else:
            print(f"從配置載入 {len(urls)} 個頁面")

    if not urls:
        print("沒有需要同步的 URL")
        sys.exit(1)

    results = run_batch(urls, headless=args.headless, delay=args.delay)
    save_status(results, run_dna)


if __name__ == "__main__":
    main()
