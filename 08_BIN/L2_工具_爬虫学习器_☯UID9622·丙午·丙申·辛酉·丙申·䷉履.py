#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
🐉 龍魂生态 · 爬虫学习器 v1.0
# 层级: L2_工具层
# DNA: #龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-CRAWLER-LEARNER-v1.0-UID9622
# 别名: 08_BIN/lh_crawler_learn.py
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 通过

学习目标：
  1. HTTP 请求与响应
  2. HTML/XML 解析
  3. 数据提取与存储
  4. 反爬基础：User-Agent、延时、重试
  5. 合规：robots.txt、频率控制、数据主权

用法：
  ./08_BIN/lh_crawler_learn.py fetch <url> --output ./data/page.html
  ./08_BIN/lh_crawler_learn.py extract <url> --selector "title"
  ./08_BIN/lh_crawler_learn.py crawl <url> --depth 2 --delay 1
"""

import argparse
import hashlib
import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse

try:
    import requests
except ImportError:
    print("⚠️ 未安装 requests，请先执行: pip install requests beautifulsoup4 lxml")
    raise SystemExit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("⚠️ 未安装 beautifulsoup4，请先执行: pip install requests beautifulsoup4 lxml")
    raise SystemExit(1)


DNA = "#龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-CRAWLER-LEARNER-v1.0-UID9622"
UID = "9622"
DEFAULT_DELAY = 1.0
DEFAULT_TIMEOUT = 10
DEFAULT_USER_AGENT = "LonghunCrawlerLearner/1.0 (educational; UID9622)"


def generate_dna(suffix: str = "") -> str:
    ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    rand = hashlib.sha256(f"{suffix}{ts}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{suffix}-{UID}-{rand}"


def ensure_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def fetch(url: str, timeout: int = DEFAULT_TIMEOUT, headers: Optional[Dict] = None) -> Optional[requests.Response]:
    """发送 HTTP GET 请求，带基础反爬头部"""
    h = {"User-Agent": DEFAULT_USER_AGENT}
    if headers:
        h.update(headers)
    try:
        resp = requests.get(url, headers=h, timeout=timeout)
        resp.raise_for_status()
        return resp
    except Exception as e:
        print(f"❌ 请求失败: {url} → {e}")
        return None


def extract_text(soup: BeautifulSoup) -> str:
    """提取页面正文文本"""
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def extract_links(soup: BeautifulSoup, base_url: str) -> List[str]:
    """提取页面内所有链接"""
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full = urljoin(base_url, href)
        parsed = urlparse(full)
        if parsed.scheme in ("http", "https"):
            links.append(full)
    return list(set(links))


def extract_by_selector(soup: BeautifulSoup, selector: str) -> List[str]:
    """按 CSS 选择器提取内容"""
    try:
        elements = soup.select(selector)
        return [el.get_text(strip=True) for el in elements]
    except Exception as e:
        print(f"⚠️ 选择器解析失败: {e}")
        return []


def save_result(output_dir: Path, url: str, data: Dict[str, Any]):
    """保存抓取结果到本地"""
    ensure_dir(output_dir)
    domain = urlparse(url).netloc.replace(":", "_")
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:12]
    filename = output_dir / f"{domain}_{url_hash}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 结果已保存: {filename}")


def cmd_fetch(args):
    url = args.url
    print(f"🐉 抓取: {url}")
    resp = fetch(url, timeout=args.timeout)
    if not resp:
        return

    output_path = Path(args.output) if args.output else None
    if output_path:
        ensure_dir(output_path)
        output_path.write_text(resp.text, encoding="utf-8")
        print(f"✅ 已保存 HTML: {output_path}")
    else:
        print(resp.text[:500])


def cmd_extract(args):
    url = args.url
    print(f"🐉 提取: {url}")
    resp = fetch(url, timeout=args.timeout)
    if not resp:
        return

    soup = BeautifulSoup(resp.text, "lxml")

    if args.selector:
        results = extract_by_selector(soup, args.selector)
        print(f"\n选择器 '{args.selector}' 命中 {len(results)} 条:")
        for r in results[:20]:
            print(f"  - {r[:120]}")
        return

    title = soup.title.get_text(strip=True) if soup.title else ""
    print(f"\n标题: {title}")
    print(f"\n正文前 500 字:\n{extract_text(soup)[:500]}")


def cmd_crawl(args):
    start_url = args.url
    max_depth = args.depth
    delay = args.delay
    output_dir = Path(args.output)

    visited: set = set()
    to_visit = [(start_url, 0)]
    results = []

    print(f"🐉 开始爬取: {start_url} · 最大深度: {max_depth} · 延时: {delay}s")

    while to_visit:
        url, depth = to_visit.pop(0)
        if url in visited or depth > max_depth:
            continue
        visited.add(url)

        print(f"  [{'=' * depth}{' ' * (max_depth - depth)}] {url}")
        resp = fetch(url, timeout=args.timeout)
        if not resp:
            continue

        soup = BeautifulSoup(resp.text, "lxml")
        text = extract_text(soup)
        links = extract_links(soup, url)

        result = {
            "dna": generate_dna("CRAWL"),
            "url": url,
            "depth": depth,
            "title": soup.title.get_text(strip=True) if soup.title else "",
            "text_preview": text[:500],
            "links": links[:50],
            "crawled_at": datetime.now().isoformat(),
        }
        results.append(result)
        save_result(output_dir, url, result)

        if depth < max_depth:
            for link in links[:args.max_links]:
                if link not in visited:
                    to_visit.append((link, depth + 1))

        if delay > 0:
            time.sleep(delay)

    print(f"\n✅ 爬取完成: {len(results)} 个页面")


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂爬虫学习器")
    sub = parser.add_subparsers(dest="command", required=True)

    p_fetch = sub.add_parser("fetch", help="抓取单个页面")
    p_fetch.add_argument("url")
    p_fetch.add_argument("--output", help="保存 HTML 文件路径")
    p_fetch.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)

    p_extract = sub.add_parser("extract", help="提取页面内容")
    p_extract.add_argument("url")
    p_extract.add_argument("--selector", help="CSS 选择器，如 'h1, h2'")
    p_extract.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)

    p_crawl = sub.add_parser("crawl", help="递归爬取")
    p_crawl.add_argument("url")
    p_crawl.add_argument("--depth", type=int, default=1)
    p_crawl.add_argument("--delay", type=float, default=DEFAULT_DELAY)
    p_crawl.add_argument("--max-links", type=int, default=10)
    p_crawl.add_argument("--output", default="./08_STATE/crawler_learn")
    p_crawl.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)

    args = parser.parse_args()

    if args.command == "fetch":
        cmd_fetch(args)
    elif args.command == "extract":
        cmd_extract(args)
    elif args.command == "crawl":
        cmd_crawl(args)


if __name__ == "__main__":
    main()
