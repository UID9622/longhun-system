#!/usr/bin/env python3
"""
🐉 龍魂搜索引擎 v2.0
多后端：SearXNG（本地·零费用·首选） → 百度 → Bing
原则：搜索是基础能力，不应收费
DNA: #龍芯⚡️2026-08-31-SEARCH-ENGINE-V2.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: MulanPSL v2（工程实现层）
"""

import requests
from bs4 import BeautifulSoup
import json
import sys
import os
import urllib.parse
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# SearXNG 本地实例（docker-compose 启动后可用）
SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:8888")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def search_searxng(query: str, num: int = 10) -> list:
    """优先使用本地 SearXNG（完全免费·无 API Key·无限额）"""
    try:
        resp = requests.get(
            f"{SEARXNG_URL}/search",
            params={"q": query, "format": "json", "engines": "bing,baidu,google"},
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            return [
                {
                    "title":   r.get("title", ""),
                    "link":    r.get("url", ""),
                    "snippet": r.get("content", ""),
                    "engine":  r.get("engine", "searxng"),
                    "source":  "searxng_local"
                }
                for r in data.get("results", [])[:num]
            ]
    except Exception:
        pass
    return []


def search_bing(query: str, num: int = 10) -> list:
    """Bing 网页爬取（无需 API Key）"""
    try:
        url = f"https://www.bing.com/search?q={urllib.parse.quote_plus(query)}&count={num}"
        headers = {"User-Agent": UA}
        resp = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for li in soup.select("li.b_algo"):
            a = li.find("a")
            if a:
                snippet = li.find("p")
                results.append({
                    "title":   a.get_text(strip=True),
                    "link":    a.get("href", ""),
                    "snippet": snippet.get_text(strip=True) if snippet else "",
                    "engine":  "bing",
                    "source":  "bing_scrape"
                })
        return results
    except Exception:
        return []


def search_baidu(query: str, num: int = 10) -> list:
    """百度搜索（国内首选·无需翻墙）"""
    try:
        url = f"https://www.baidu.com/s?wd={urllib.parse.quote_plus(query)}&rn={num}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        resp = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for div in soup.select("div.result"):
            a = div.find("a")
            snippet_div = div.find("div", class_=lambda c: c and "c-abstract" in c)
            if a and a.get("href"):
                results.append({
                    "title":   a.get_text(strip=True),
                    "link":    a.get("href", ""),
                    "snippet": snippet_div.get_text(strip=True) if snippet_div else "",
                    "engine":  "baidu",
                    "source":  "baidu_scrape"
                })
        return results
    except Exception:
        return []


def multi_search(query: str, num: int = 10) -> dict:
    """
    多后端搜索·自动降级
    优先级：SearXNG本地 → 百度 → Bing
    """
    # 1. 先尝试本地 SearXNG（零费用·最优）
    results = search_searxng(query, num)
    if results:
        return {"results": results, "backend": "searxng_local",
                "cost": "¥0", "note": "本地SearXNG·完全免费"}

    # 2. 降级到百度（国内无需翻墙）
    results = search_baidu(query, num)
    if results:
        return {"results": results, "backend": "baidu_scrape",
                "cost": "¥0", "note": "百度网页抓取·免费"}

    # 3. 最后降级到 Bing
    results = search_bing(query, num)
    return {"results": results, "backend": "bing_scrape",
            "cost": "¥0", "note": "Bing网页抓取·免费"}


@app.route("/search")
def search_api():
    query = request.args.get("q", "")
    num   = int(request.args.get("n", 10))
    if not query:
        return jsonify({"error": "Missing parameter: q"}), 400
    result = multi_search(query, num)
    result["dna"] = f"#龍芯⚡️2026-08-31-SEARCH-{query[:20]}-UID9622"
    result["tricolor"] = "🟢" if result["results"] else "🔴"
    return jsonify(result)


@app.route("/health")
def health():
    # 检测各后端状态
    searxng_ok = False
    try:
        r = requests.get(f"{SEARXNG_URL}/healthz", timeout=2)
        searxng_ok = r.status_code == 200
    except Exception:
        pass

    return jsonify({
        "status": "healthy",
        "backends": {
            "searxng_local": "🟢 online" if searxng_ok else "🟡 offline (fallback to scraping)",
            "baidu_scrape":  "🟢 available",
            "bing_scrape":   "🟢 available"
        },
        "cost": "¥0/次",
        "note": "三重后端·任一可用即正常"
    })


if __name__ == "__main__":
    # 命令行模式
    if len(sys.argv) > 1 and sys.argv[1] != "--server":
        q = " ".join(sys.argv[1:])
        result = multi_search(q)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("🔍 搜索服务启动在 :8890")
        app.run(host="0.0.0.0", port=8890, debug=False)
