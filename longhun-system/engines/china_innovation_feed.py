#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
china_innovation_feed.py — 🇨🇳 中国科技自主创新专栏·注入器 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
签名人  : UID9622 · 诸葛鑫
DNA     : #龍芯⚡️20260424-CN-INNO-FEED-v1.0
目标库  : NOTION_INNOVATION_DB_ID (baf3b574023e49c987eee620a811e70d)
目的    : 一条命令把"中国自主创新内容"注入知识库·自动打 DNA 追溯码
═══════════════════════════════════════════

用法：
  中国创新 "标题" "一句话摘要"
  中国创新 "标题" "摘要" --domain AI --source 网络 --tags "半导体,光刻机"

可选参数：
  --domain    领域（AI/芯片/航天/能源/医疗/材料/制造/其他）
  --source    来源（网络/新闻/论文/会议/访谈/原创/其他）
  --tags      多标签（逗号分隔·最多 5 个）
  --logic     底层逻辑（一段话·深度分析）
  --yijing    易经锚点（某卦某爻）
  --level     重要程度（🔴高/🟡中/🟢低）
  --link      公开链接（URL）

无参数跑本脚本会打印本说明。
"""

import os, sys, json, hashlib, urllib.request, urllib.error
from datetime import datetime, timezone

# ═══════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════
NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
DB_ID = os.environ.get("NOTION_INNOVATION_DB_ID", "baf3b574023e49c987eee620a811e70d")
NOTION_VERSION = "2022-06-28"

C, G, Y, R, D, B, NC = ("\033[36m","\033[32m","\033[33m","\033[31m","\033[2m","\033[1m","\033[0m")


# ═══════════════════════════════════════════════
# 工具
# ═══════════════════════════════════════════════
def make_dna(title: str, summary: str) -> str:
    h = hashlib.sha256((title + "|" + summary).encode("utf-8")).hexdigest()[:8].upper()
    date = datetime.now().strftime("%Y%m%d")
    return f"#龍芯⚡️{date}-CN-INNO-{h}"


def rt(text: str) -> list:
    """Notion rich_text 字段的最小包装"""
    if not text: return []
    return [{"type": "text", "text": {"content": text[:2000]}}]


# ═══════════════════════════════════════════════
# 核心：写入 Notion
# ═══════════════════════════════════════════════
def create_page(title, summary, domain=None, source=None, tags=None,
                logic=None, yijing=None, level=None, link=None, status=None):
    if not NOTION_TOKEN:
        print(f"{R}🔴 NOTION_TOKEN 未配置·检查 ~/longhun-system/.env{NC}")
        return None

    dna = make_dna(title, summary)

    props = {
        "专栏标题": {"title": rt(title)},
        "DNA追溯码": {"rich_text": rt(dna)},
        "一句话摘要": {"rich_text": rt(summary)},
        "创作时间": {"date": {"start": datetime.now().date().isoformat()}},
    }
    if domain: props["领域分类"] = {"select": {"name": domain}}
    if source: props["来源"] = {"select": {"name": source}}
    if tags:
        tag_list = [t.strip() for t in tags.replace("，",",").split(",") if t.strip()]
        props["内容标签"] = {"multi_select": [{"name": t} for t in tag_list[:5]]}
    if logic: props["底层逻辑"] = {"rich_text": rt(logic)}
    if yijing: props["易经锚点"] = {"rich_text": rt(yijing)}
    if level: props["重要程度"] = {"select": {"name": level}}
    if link: props["公开链接"] = {"url": link}
    if status: props["状态"] = {"status": {"name": status}}

    payload = {
        "parent": {"database_id": DB_ID},
        "properties": props,
    }

    try:
        req = urllib.request.Request(
            "https://api.notion.com/v1/pages",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {NOTION_TOKEN}",
                "Notion-Version": NOTION_VERSION,
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            r = json.loads(resp.read().decode("utf-8"))

        if r.get("object") == "error":
            print(f"{R}🔴 写入失败: {r.get('message','?')[:200]}{NC}")
            return None

        url = r.get("url", "")
        pid = r.get("id", "")
        print()
        print(f"{G}━━━ 🐉 中国创新知识库·注入成功 ━━━{NC}")
        print(f"  标题   : {B}{title}{NC}")
        print(f"  摘要   : {summary[:60]}")
        print(f"  DNA    : {B}{dna}{NC}")
        print(f"  页 ID  : {D}{pid}{NC}")
        print(f"  链接   : {C}{url}{NC}")
        if domain: print(f"  领域   : {domain}")
        if source: print(f"  来源   : {source}")
        if tags: print(f"  标签   : {tags}")
        if level: print(f"  重要   : {level}")
        print()
        return {"id": pid, "url": url, "dna": dna}

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        print(f"{R}🔴 Notion HTTP {e.code}: {body[:300]}{NC}")
    except Exception as e:
        print(f"{R}🔴 异常: {e}{NC}")
    return None


# ═══════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════
def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        return

    title = args[0]
    summary = args[1]
    kwargs = {}
    i = 2
    while i < len(args):
        a = args[i]
        if a.startswith("--") and i + 1 < len(args):
            key = a[2:]
            val = args[i+1]
            kwargs[key] = val
            i += 2
        else:
            i += 1

    create_page(title, summary, **kwargs)


if __name__ == "__main__":
    main()
