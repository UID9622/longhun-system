#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·壬午·戌时·䷘无妄-CSDN-CRAWLER-v1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · CSDN 资料抓取工具 v1.0（Playwright + 本机 Chrome）

功能:
  1. 从任意 CSDN 页面开始（用户主页 / 文章列表 / 专栏 / 单篇详情）
  2. 自动提取列表下全部文章链接（支持静态分页 + 滚动/按钮懒加载）
  3. 逐篇抓取 标题 / 正文 / 发布时间 / 阅读量 / 标签
  4. 输出结构化 JSON（UTF-8 无乱码）
  5. 断点续传（--resume 跳过已抓）+ 中途落盘 checkpoint
  6. 内置防封策略：随机延时 / UA 轮换 / 失败重试 / 退避

用法:
  python3 08_BIN/csdn_crawler.py --url https://blog.csdn.net/UID9622 --output /tmp/csdn.json --max-pages 5
  python3 08_BIN/csdn_crawler.py --url <单篇详情页> --output one.json        # 单篇模式
  python3 08_BIN/csdn_crawler.py --url <url> --resume --output data.json      # 断点续传
  python3 08_BIN/csdn_crawler.py --url <url> --headed --max-articles 3        # 有头调试

依赖:
  pip install playwright      # 复用本机 Chrome，无需下载 chromium
  若要用 playwright 自带 chromium: playwright install chromium

注意:
  - 阅读量字段 CSDN 常需登录才渲染，缺失时为 null（非故障）
  - 请合理控制频率（默认随机延时 2-5s），尊重站点服务条款
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError
except ImportError:
    print("❌ 缺少 playwright，请先安装：python3 -m pip install playwright", file=sys.stderr)
    sys.exit(2)

# ============================================================
# 常量
# ============================================================
ARTICLE_RE = re.compile(r"https?://blog\.csdn\.net/[^/]+/article/details/(\d+)")
UA_POOL = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
]

DEFAULT_DELAY = 2.5          # 每次页面动作后的基础延时(秒)，实际 ±随机抖动
RETRIES = 3
CHECKPOINT_EVERY = 5         # 每抓 N 篇落盘一次（断点续传友好）


# ============================================================
# 工具函数
# ============================================================
def _sleep(delay: float = DEFAULT_DELAY) -> None:
    """随机抖动延时，防固定节奏。"""
    time.sleep(max(0.3, delay + random.uniform(-0.8, 1.2)))


def _goto(page, url: str, retries: int = 3) -> None:
    """
    带风控容错的页面导航。

    CSDN 全站有 JS 反爬：首次访问常返回 403/521 并注入 challenge，
    数秒后 JS 自动刷新为 200 正常内容。故:
      1. domcontentloaded 到达即可（内容由 JS 续渲染）
      2. 状态码 403/521 时等 3s 再 reload（最多 retries 次）
    """
    for attempt in range(1, retries + 1):
        try:
            resp = page.goto(url, wait_until="domcontentloaded", timeout=40000)
        except PWTimeoutError:
            resp = None
        if resp is not None and resp.status in (403, 521):
            time.sleep(3.0)
            continue  # reload 再试
        page.wait_for_timeout(2500)
        return
    # 最后一次兜底：不抛错，让后续 DOM 提取自行判断
    try:
        page.wait_for_timeout(2500)
    except Exception:
        pass


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def canonical_article_url(url: str) -> str:
    """归一化文章链接：补协议 + 去 query/#，支持主域与子域(uid9622-01.blog.csdn.net)形态。"""
    url = url.strip()
    if url.startswith("//"):
        url = "https:" + url
    url = url.split("#")[0]
    m = re.search(r"(https?://[^/?#]+/article/details/\d+)", url)
    return m.group(1) if m else url.split("?")[0]


def load_done(output_file: Path) -> Dict[str, dict]:
    """断点续传：读已有输出文件的已抓记录 {canonical_url: data}。"""
    if output_file.exists():
        try:
            data = json.loads(output_file.read_text(encoding="utf-8"))
            items = data.get("articles", data) if isinstance(data, dict) else data
            if isinstance(items, list):
                return {it.get("url"): it for it in items if it.get("url")}
        except Exception:
            pass
    return {}


def save_results(results: Dict[str, dict], output_file: Path, start_url: str) -> None:
    """保存结构化 JSON：全部已抓记录 + 元数据。"""
    payload = {
        "meta": {
            "tool": "csdn_crawler v1.0",
            "dna": "#龍芯⚡️丙午·丁酉·壬午·戌时·䷘无妄-CSDN-CRAWLER-v1.0",
            "归属名": "诸葛鑫 | UID9622 · 龍芯北辰",
            "start_url": start_url,
            "crawled_at": now_iso(),
            "count": len(results),
        },
        "articles": list(results.values()),
    }
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


# ============================================================
# 核心抓取函数
# ============================================================
def get_article_links(page, url: str) -> List[str]:
    """
    提取当前列表页所有文章链接（返回归一化 URL，去重保序）。

    兼容多种 CSDN 布局：
      - 文章列表页 /article/list/N   (.article-list / .blog-list-box ...)
      - 专栏列表页 /column/<id>       (动态渲染)
      - 用户主页（未规范为列表时）    (懒加载容器)
    通用策略：页面内所有 a[href*=/article/details/]，按数字 id 去重。
    """
    _goto(page, url)

    hrefs: List[str] = []
    for _ in range(6):  # 滚动 6 轮，触发懒加载（若页面本来就有全部链接也不影响）
        page.mouse.wheel(0, 6000)
        page.wait_for_timeout(500)

    # 点击"加载更多"类按钮（存在则点，最多 3 次）
    for _ in range(3):
        btns = page.locator(
            "text=加载更多,text=点击加载,text=查看更多,text=load more"
        )
        if btns.count() == 0:
            break
        try:
            btns.first.click(timeout=2000)
            page.wait_for_timeout(1800)
        except Exception:
            break

    # 兼容绝对 / 相对 / 无协议 / 子域(xxx.blog.csdn.net) 四种 href 形态
    # 统一以 urljoin 补全为绝对 URL，再截取到 /article/details/<id> 保留真实 host
    anchors = page.locator('a[href*="/article/details/"]')
    n = anchors.count()
    for i in range(n):
        try:
            href = anchors.nth(i).get_attribute("href")
        except Exception:
            continue
        if not href:
            continue
        abs_href = urljoin(url, href.strip())
        m = re.search(r"(https?://[^/?#]+/article/details/\d+)", abs_href)
        if m:
            hrefs.append(m.group(1))
    return list(dict.fromkeys(canonical_article_url(h) for h in hrefs))


def _first_text(page, selectors: List[str]) -> Optional[str]:
    for sel in selectors:
        try:
            loc = page.locator(sel).first
            if loc.count() > 0:
                txt = loc.inner_text(timeout=1500).strip()
                if txt:
                    return txt
        except Exception:
            continue
    return None


def _first_attr(page, selectors: List[str], attr: str) -> Optional[str]:
    for sel in selectors:
        try:
            loc = page.locator(sel).first
            if loc.count() > 0:
                val = loc.get_attribute(attr, timeout=1500)
                if val and val.strip():
                    return val.strip()
        except Exception:
            continue
    return None


def _clean_time(raw: Optional[str]) -> Optional[str]:
    """把「于 2026-08-31 23:03:04 发布」等包裹清洗成 ISO 时间；ISO 原样返回。"""
    if not raw:
        return None
    m = re.search(r"(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(?::\d{2})?)", raw)
    if m:
        return m.group(1).replace(" ", "T")
    return None  # 无法解析为干净时间则不输出


def _extract_tags(page) -> List[str]:
    tags: List[str] = []
    try:
        loc = page.locator("a.tag-link")
        if loc.count() == 0:
            loc = page.locator(".tags-box a, .article-tags a")
        for i in range(loc.count()):
            t = loc.nth(i).inner_text(timeout=800).strip()
            if t and t not in tags:
                tags.append(t)
    except Exception:
        pass
    if not tags:  # fallback: meta keywords
        kw = _first_attr(page, ["meta[name='keywords']"], "content")
        if kw:
            tags = [t.strip() for t in kw.split(",") if t.strip()][:10]
    return tags


def scrape_article(page, url: str) -> dict:
    """
    抓取单篇文章详细内容。

    返回字段: url / title / publish_time / read_count / tags / excerpt / content / crawled_at
    多套 CSS 选择器 fallback，抵御 CSDN 改版。
    """
    _goto(page, url)

    title = _first_text(page, [
        "h1.title-article",
        "h1#articleContentId",
        ".article_title h1",
        "h1",
    ]) or _first_attr(page, ["meta[property='og:title']"], "content")

    publish_time = _first_text(page, [
        "#barrierTime",
        ".barriertitle .time",
        ".article-header-box .time",
        ".article-info-box .time",
    ]) or _first_attr(page, ["meta[property='article:published_time']"], "content")
    publish_time = _clean_time(publish_time)

    read_count = _first_text(page, [
        ".read-count",
        ".read-num",
        ".article-header-box .read",
        ".view-time-box .read-count",
    ])
    # 阅读量常被 CSDN 以非数字占位/需登录，清洗成纯数字或 None
    if read_count:
        nums = re.findall(r"\d+", read_count)
        read_count = int(nums[0]) if nums else None

    tags = _extract_tags(page)

    # 正文：多容器 fallback
    content = ""
    for sel in ["#content_views", ".markdown_views", "article", ".article_content"]:
        try:
            loc = page.locator(sel).first
            if loc.count() > 0:
                content = loc.inner_text(timeout=3000).strip()
                if content:
                    break
        except Exception:
            continue
    excerpt = content[:200]

    return {
        "url": canonical_article_url(url),
        "title": title or "(未捕获标题)",
        "publish_time": publish_time,
        "read_count": read_count,
        "tags": tags,
        "excerpt": excerpt,
        "content": content,
        "crawled_at": now_iso(),
    }


# ============================================================
# 主流程
# ============================================================
def run(start_url: str, output: str, max_pages: int, headless: bool,
        delay: float, max_articles: Optional[int], resume: bool, channel: str) -> int:
    output_file = Path(output).expanduser()

    # 用户主页规范化为文章列表页（最稳的静态分页结构）
    m = re.match(r"https?://blog\.csdn\.net/([A-Za-z0-9_-]+)/?$", start_url.strip())
    if m:
        start_url = f"https://blog.csdn.net/{m.group(1)}/article/list/1"

    is_single = "/article/details/" in start_url
    done: Dict[str, dict] = load_done(output_file) if resume else {}
    if resume and done:
        print(f"♻️ 断点续传：已跳过 {len(done)} 篇已抓记录")

    # 复用本机 Chrome / 或 playwright 自带 chromium
    if channel == "chrome":
        channel_cfg = {"channel": "chrome"}
    else:
        channel_cfg = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
            **channel_cfg,
        )
        ctx = browser.new_context(
            user_agent=random.choice(UA_POOL),
            viewport={"width": 1440, "height": 900},
            locale="zh-CN",
        )
        page = ctx.new_page()

        # 静默：把 navigator.webdriver 抹掉，降低被识别为自动化的概率
        page.add_init_script(
            "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
        )

        try:
            # ---------- 单篇模式 ----------
            if is_single:
                print(f"📄 单篇模式: {start_url}")
                rec = scrape_article(page, start_url)
                done[rec["url"]] = rec
                save_results(done, output_file, start_url)
                print(f"✅ 完成 1 篇 → {output_file}")
                return 0

            # ---------- 列表模式：翻页收集链接 ----------
            print(f"🔗 列表模式: {start_url}  (上限 {max_pages} 页)")
            all_links: List[str] = []
            current_url = start_url
            for pg in range(1, max_pages + 1):
                links = get_article_links(page, current_url)
                new = [u for u in links if u not in all_links]
                all_links.extend(new)
                print(f"   第{pg}页: 本页{len(links)}条 · 累计{len(all_links)}条")
                if not new:
                    break

                # 找"下一页"
                next_found = False
                # ① 静态分页器
                try:
                    next_btn = page.locator(".ui-pager .ui-pager-next")
                    if next_btn.count() and next_btn.is_visible():
                        next_btn.first.click(timeout=2500)
                        next_found = True
                        page.wait_for_timeout(1800)
                except Exception:
                    pass
                # ② URL 翻页: /article/list/N → N+1
                if not next_found:
                    m2 = re.match(r"(.*/article/list/)(\d+)(.*)", current_url)
                    if m2:
                        nxt = int(m2.group(2)) + 1
                        current_url = f"{m2.group(1)}{nxt}{m2.group(3)}"
                        next_found = True
                if not next_found:
                    break  # 没有翻页入口 → 结束
                _sleep(delay)

            # 去重（保序）
            all_links = list(dict.fromkeys(all_links))
            # 过滤已抓
            pending = [u for u in all_links if u not in done]
            print(f"📚 共发现 {len(all_links)} 篇，待抓 {len(pending)} 篇")
            if max_articles:
                pending = pending[: max_articles]

            # ---------- 逐篇抓详情 ----------
            ok = fail = 0
            for idx, art_url in enumerate(pending, 1):
                for attempt in range(1, RETRIES + 1):
                    try:
                        rec = scrape_article(page, art_url)
                        done[rec["url"]] = rec
                        ok += 1
                        title_show = (rec.get("title") or "?")[:40]
                        print(f"   [{idx}/{len(pending)}] ✅ {title_show}")
                        break
                    except PWTimeoutError:
                        print(f"   [{idx}/{len(pending)}] ⏱️ 超时(尝试{attempt}/{RETRIES}) {art_url}")
                    except Exception as e:
                        print(f"   [{idx}/{len(pending)}] ⚠️ 失败(尝试{attempt}/{RETRIES}): {e}")
                    if attempt < RETRIES:
                        _sleep(delay * 2)
                else:
                    fail += 1
                    print(f"   [{idx}/{len(pending)}] ❌ 放弃: {art_url}")

                # 中途 checkpoint
                if ok % CHECKPOINT_EVERY == 0 or idx == len(pending):
                    save_results(done, output_file, start_url)
                _sleep(delay)

            save_results(done, output_file, start_url)
            print(f"\n📦 完成: 成功{ok} · 失败{fail} · 累计{len(done)} → {output_file}")
            return 0 if fail == 0 else 1
        finally:
            try:
                browser.close()
            except Exception:
                pass


def main() -> int:
    ap = argparse.ArgumentParser(
        description="🐉 龍魂 · CSDN 资料抓取工具 v1.0（Playwright + Chrome）",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    ap.add_argument("--url", required=True, help="起始 URL：用户主页/列表/专栏/单篇")
    ap.add_argument("--output", default="csdn_crawl_output.json", help="输出 JSON 文件路径")
    ap.add_argument("--max-pages", type=int, default=5, help="列表翻页上限")
    ap.add_argument("--max-articles", type=int, default=None, help="最多抓取文章数")
    ap.add_argument("--headed", action="store_true", help="有头模式(调试可见·默认无头)")
    ap.add_argument("--delay", type=float, default=DEFAULT_DELAY, help="页面动作基础延时(秒)")
    ap.add_argument("--resume", action="store_true", help="断点续传：跳过输出文件中已抓文章")
    ap.add_argument("--channel", choices=["chrome", "chromium"], default="chrome",
                    help="浏览器引擎: chrome=复用本机Chrome(默认) / chromium=playwright自带")
    args = ap.parse_args()

    return run(args.url, args.output, args.max_pages, not args.headed,
               args.delay, args.max_articles, args.resume, args.channel)


if __name__ == "__main__":
    sys.exit(main())
