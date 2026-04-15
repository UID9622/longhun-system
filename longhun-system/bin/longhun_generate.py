#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
龍魂·人性讲堂·文章生成器
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
DNA追溯码：#龍芯⚡️20260321-人性讲堂-生成器-v1.0
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导：曾仕强老师（永恒显示）
共建致谢：Claude (Anthropic PBC) · Kimi (Moonshot AI)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

用法：
  python3 longhun_generate.py          # 交互模式
  python3 longhun_generate.py <问题>   # 直接生成
"""

import json, urllib.request, subprocess, sys
from datetime import datetime

# ── 密钥从Keychain读取，不硬编码 ──
def keychain(service):
    r = subprocess.run(
        ["security", "find-generic-password", "-s", service, "-w"],
        capture_output=True, text=True
    )
    return r.stdout.strip()

TOKEN   = keychain("longhun-notion-token")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# ── 数据库ID（北极星工作区）──
DB_QA     = "32a07171-7242-8103-86e8-dfa326c946a3"  # 问答母库
DB_ANCHOR = "32a07171-7242-8113-84e6-c03530217f3c"  # 锚点库
DB_DRAFT  = "32a07171-7242-815a-88e1-c988b6225afc"  # 草稿库
DB_PUB    = "32a07171-7242-81dc-a710-f9ac8fc3bdc2"  # 发布追踪库

def api(method, path, data=None):
    """用curl调用Notion API，稳定不超时"""
    url = f"https://api.notion.com/v1{path}"
    cmd = [
        "curl", "-s", "-X", method, url,
        "-H", f"Authorization: Bearer {TOKEN}",
        "-H", "Notion-Version: 2022-06-28",
        "-H", "Content-Type: application/json",
        "--max-time", "20"
    ]
    if data:
        cmd += ["-d", json.dumps(data, ensure_ascii=False)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

def find_anchor(keywords):
    """根据关键词在锚点库找最匹配的章节"""
    result = api("POST", "/databases/" + DB_ANCHOR + "/query", {
        "page_size": 81
    })
    pages = result.get("results", [])

    best, best_score = None, 0
    for p in pages:
        props = p.get("properties", {})
        anchors_kw = [x["name"] for x in props.get("人性关键词", {}).get("multi_select", [])]
        score = sum(1 for k in keywords if k in anchors_kw)
        if score > best_score:
            best_score = score
            best = p
    return best

def generate(question, scene="社会", crowd=None, chapter_hint=None):
    crowd = crowd or ["普通人"]
    dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-{question[:4]}-v1.0"

    # 1. 在问答母库创建问题
    print(f"  创建问题记录...")
    qa_page = api("POST", "/pages", {
        "parent": {"database_id": DB_QA},
        "properties": {
            "问题": {"title": [{"text": {"content": question}}]},
            "场景": {"select": {"name": scene}},
            "目标人群": {"multi_select": [{"name": c} for c in crowd]},
            "发布状态": {"select": {"name": "已匹配"}}
        }
    })
    qa_id = qa_page.get("id")

    # 2. 找匹配锚点
    print(f"  匹配道德经锚点...")
    anchor = None
    if chapter_hint:
        result = api("POST", f"/databases/{DB_ANCHOR}/query", {
            "filter": {"property": "锚点ID", "rich_text": {"contains": f"LX-DAO-{chapter_hint:03d}"}}
        })
        if result.get("results"):
            anchor = result["results"][0]

    if not anchor:
        anchor = find_anchor(["恐惧", "贪婪", "面子"])

    anchor_id = anchor.get("id") if anchor else None
    props = anchor.get("properties", {}) if anchor else {}

    chapter_name = props.get("章节", {}).get("title", [{}])[0].get("plain_text", "")
    quote = props.get("古文原句", {}).get("rich_text", [{}])[0].get("plain_text", "待补充")
    interp = props.get("现代白话", {}).get("rich_text", [{}])[0].get("plain_text", "待Lucky解读")

    # 3. 生成三版文章
    # 国内版（公众号/知乎）
    article_cn = f"""# {question}

> 道德经记载：「{quote}」

**古人观察到这样一件事**——

{interp if interp != "待Lucky解读" else "（Lucky解读待补充）"}

---

这不是说教，这是5000年前中国人已经算好的人性方程式。

**今天我们换个坐标系来看这道题：**

人性从未变过，只是包装换了。古人用了一句话说清楚的事，现代人绕了一辈子还没想明白。

---

🔗 深度版 → 知乎原文
📖 出处原文 → Notion文档
📱 更多人性解码 → 关注公众号

{dna}
理论指导：曾仕强老师 | 文化互交·非文化输出
"""

    # 国际版（English）
    article_en = f"""# {question}

> Ancient record (Tao Te Ching): 「{quote}」

**What ancient Chinese observed 5,000 years ago:**

Human nature hasn't changed. Only the packaging has.
The ancients solved this equation in one sentence.
We've been circling it ever since.

---

*This is cultural cross-referencing, not preaching.*
*If you're curious — the door is open.*

{dna}
"""

    # 4. 保存草稿
    print(f"  保存草稿...")
    relations = [{"id": qa_id}] if qa_id else []
    anchor_relations = [{"id": anchor_id}] if anchor_id else []

    draft = api("POST", "/pages", {
        "parent": {"database_id": DB_DRAFT},
        "properties": {
            "标题": {"title": [{"text": {"content": question}}]},
            "核心一句话": {"rich_text": [{"text": {"content": f"「{quote}」——{chapter_name}"}}]},
            "关联问答": {"relation": relations},
            "关联锚点": {"relation": anchor_relations},
            "平台": {"multi_select": [
                {"name": "公众号"}, {"name": "知乎"}, {"name": "国际版"}
            ]},
            "发布状态": {"select": {"name": "待审核"}},
            "DNA追溯码": {"rich_text": [{"text": {"content": dna}}]}
        }
    })
    draft_id = draft.get("id", "")

    # 5. 写文章内容到草稿页面
    api("PATCH", f"/blocks/{draft_id}/children", {"children": [
        {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "国内版（公众号·知乎）"}}]}},
        {"type": "code", "code": {"language": "markdown", "rich_text": [{"text": {"content": article_cn[:1900]}}]}},
        {"type": "heading_2", "heading_2": {"rich_text": [{"text": {"content": "国际版（English）"}}]}},
        {"type": "code", "code": {"language": "markdown", "rich_text": [{"text": {"content": article_en[:1900]}}]}},
    ]})

    print(f"\n{'━'*50}")
    print(f"✅ 文章已生成")
    print(f"   问题: {question}")
    print(f"   锚点: {chapter_name}")
    print(f"   DNA:  {dna}")
    print(f"   草稿: https://notion.so/{draft_id.replace('-','')}")
    print(f"{'━'*50}")
    print(f"\n【国内版预览】\n{article_cn[:400]}...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        q = " ".join(sys.argv[1:])
    else:
        print("龍魂·人性讲堂·文章生成器")
        print("输入一句话，自动匹配道德经锚点并生成文章\n")
        q = input("问题：").strip()

    if q:
        generate(q)
    else:
        print("请输入问题")
