#!/usr/bin/env python3
"""
龍魂 · CSDN 外部引用工具 v1.0
让系统内任何组件都能引用已发布的CSDN博客文章

用法:
  python3 bin/lh_csdn_ref.py sources        — 列出两个博客源
  python3 bin/lh_csdn_ref.py article <id>    — 按article_id查文章
  python3 bin/lh_csdn_ref.py search <kw>     — 搜索
  python3 bin/lh_csdn_ref.py url <title>     — 生成CSDN文章URL引用
  python3 bin/lh_csdn_ref.py status          — 状态概览

DNA: #龍芯⚡️2026-07-12-CSDN-REF-TOOL-v1.0
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXTERNAL_SOURCES = PROJECT_ROOT / "articles/csdn/external_sources.json"
ARTICLES_JSON = PROJECT_ROOT / "L5_服务层/services/portal/portal/data/csdn_articles.json"

# 两个博客源
SOURCES = {
    "legacy": {
        "name": "主账号·历史全量",
        "url": "https://uid9622.blog.csdn.net",
        "articles": 360,
        "status": "archive"
    },
    "active": {
        "name": "第二账号·当前活跃",
        "url": "https://blog.csdn.net/UID9622?type=blog",
        "articles": 147,
        "status": "active"
    }
}


def get_sources():
    """获取两个博客源信息"""
    if EXTERNAL_SOURCES.exists():
        with open(EXTERNAL_SOURCES, "r") as f:
            data = json.load(f)
        return data
    return {"sources": [
        {"id": "csdn-main-legacy", "url": SOURCES["legacy"]["url"], "articles_total": 360},
        {"id": "csdn-second-active", "url": SOURCES["active"]["url"], "articles_total": 147},
    ]}


def get_published_articles():
    """获取已同步的文章列表"""
    if ARTICLES_JSON.exists():
        with open(ARTICLES_JSON, "r") as f:
            raw = f.read()
        # csdn_articles.json 末尾有注释行，截取纯JSON部分
        comment_pos = raw.find("\n//")
        if comment_pos > 0:
            raw = raw[:comment_pos]
        return json.loads(raw)
    return {"articles": []}


def search_article(keyword: str):
    """搜索文章"""
    from integrations.csdn import get_csdn_client
    client = get_csdn_client()
    return client.search_articles(keyword)


def generate_url_ref(title: str, article_id: str = None, source: str = "active"):
    """生成CSDN文章引用URL"""
    if source == "legacy":
        base = "https://uid9622.blog.csdn.net/article/details"
    else:
        base = "https://blog.csdn.net/UID9622/article/details"

    if article_id:
        return f"{base}/{article_id}"
    return None


def get_status():
    """状态概览"""
    published = get_published_articles()
    sources_data = get_sources()

    return {
        "sources": [
            {"id": "legacy", "url": "https://uid9622.blog.csdn.net", "articles": 360, "status": "archive"},
            {"id": "active", "url": "https://blog.csdn.net/UID9622?type=blog", "articles": 147, "status": "active"},
        ],
        "total_published": 507,
        "synced_locally": len(published.get("articles", [])),
        "sync_engine": "integrations/csdn/csdn_sync_engine.py",
        "api_client": "integrations/csdn/csdn_api_client.py",
        "external_ref_registry": "articles/csdn/external_sources.json",
        "how_to_ref": "from integrations.csdn import get_csdn_client",
    }


def main():
    if len(sys.argv) < 2:
        print("用法: python3 bin/lh_csdn_ref.py <command> [args]")
        print("命令:")
        print("  sources        - 两个博客源URL")
        print("  search <kw>    - 搜索文章")
        print("  status         - 引用状态")
        print("  url <article_id> [active|legacy] - 生成引用URL")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "sources":
        data = get_sources()
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif cmd == "search":
        kw = sys.argv[2] if len(sys.argv) > 2 else ""
        result = search_article(kw)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif cmd == "status":
        result = get_status()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif cmd == "url":
        article_id = sys.argv[2] if len(sys.argv) > 2 else None
        source = sys.argv[3] if len(sys.argv) > 3 else "active"
        if article_id:
            url = generate_url_ref("", article_id, source)
            print(url)
        else:
            print("需要 article_id")
    else:
        print(json.dumps({"error": f"未知命令: {cmd}"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
