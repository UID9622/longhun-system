#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════
# 🐉 龍魂系统 · Notion本地模型连接器
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# DNA:    #龍芯⚡️2026-03-16-NOTION-AGENT-v1.0
# 作者:    诸葛鑫（UID9622）
# 理论:    曾仕强老师（永恒显示）
#
# 功能：本地Ollama模型 ←→ Notion三块积木
#   积木1: 📜 日志页  → 每次操作自动写入
#   积木2: 🐉 知识库  → 博弈文库读写
#   积木3: 🌌 生态入口 → 状态展示
# ═══════════════════════════════════════════════════════════

import os, sys, json, requests
from datetime import datetime

# ── 配置 ──────────────────────────────────────────────────
NOTION_TOKEN   = os.environ.get("NOTION_TOKEN", "")
OLLAMA_URL     = "http://localhost:11434"
DEFAULT_MODEL  = "qwen2.5:7b"   # 低算力首选；没有则用 qwen2.5

# 三块积木 ID
LOG_PAGE_ID    = "b35faf46-2bc0-42aa-9de5-192520180728"   # 📜 操作草日志
BOYI_DB_ID     = "1c4bdb8e-1257-4d31-aa91-c298b74a6001"   # 🐉 对立面博弈文库
HUB_PAGE_ID    = "f807036a-56b8-4ff3-8a04-acf7bf4b688d"   # 🌌 梦想生态入口

NOTION_API     = "https://api.notion.com/v1"
HEADERS        = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# ── Ollama 调用 ───────────────────────────────────────────
def ask_ollama(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """调用本地Ollama模型，返回回答文本"""
    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=120
        )
        r.raise_for_status()
        return r.json().get("response", "").strip()
    except Exception as e:
        return f"[Ollama错误: {e}]"

def list_ollama_models() -> list:
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        return [m["name"] for m in r.json().get("models", [])]
    except:
        return []

# ── Notion 写日志 ─────────────────────────────────────────
def write_log(action: str, detail: str, dna: str = None):
    """向日志页追加一条记录"""
    if not NOTION_TOKEN:
        print("⚠️  NOTION_TOKEN未配置，跳过日志写入")
        return
    if not dna:
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d-%H%M%S')}-LOG"
    block = {
        "children": [
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [
                        {"type": "text", "text": {"content": f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {action}\n{detail}\nDNA: {dna}"}},
                    ],
                    "icon": {"type": "emoji", "emoji": "📝"},
                    "color": "gray_background"
                }
            }
        ]
    }
    try:
        r = requests.patch(
            f"{NOTION_API}/blocks/{LOG_PAGE_ID}/children",
            headers=HEADERS,
            json=block,
            timeout=15
        )
        if r.status_code == 200:
            print(f"  ✅ 日志已写入 Notion")
        else:
            print(f"  ⚠️  日志写入失败: {r.status_code}")
    except Exception as e:
        print(f"  ⚠️  Notion连接失败: {e}")

# ── Notion 读知识库 ───────────────────────────────────────
def read_boyi_db(filter_status: str = "已完成") -> list:
    """读取博弈文库，返回文章列表"""
    if not NOTION_TOKEN:
        return []
    payload = {
        "filter": {
            "property": "状态",
            "status": {"equals": filter_status}
        },
        "page_size": 10
    }
    try:
        r = requests.post(
            f"{NOTION_API}/databases/{BOYI_DB_ID}/query",
            headers=HEADERS,
            json=payload,
            timeout=15
        )
        results = r.json().get("results", [])
        articles = []
        for p in results:
            props = p.get("properties", {})
            title_arr = props.get("文章标题", {}).get("title", [])
            title = title_arr[0]["plain_text"] if title_arr else "(无标题)"
            summary_arr = props.get("一句话摘要", {}).get("rich_text", [])
            summary = summary_arr[0]["plain_text"] if summary_arr else ""
            articles.append({"title": title, "summary": summary, "id": p["id"]})
        return articles
    except Exception as e:
        print(f"  ⚠️  读取知识库失败: {e}")
        return []

# ── 向知识库新增文章 ──────────────────────────────────────
def add_to_boyi_db(title: str, summary: str, topic: str, content: str):
    """向博弈文库新增一篇文章"""
    if not NOTION_TOKEN:
        print("⚠️  NOTION_TOKEN未配置")
        return
    dna = f"#ZHUGEXIN-BOYI-AUTO-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{topic[:10]}"
    page = {
        "parent": {"database_id": BOYI_DB_ID},
        "properties": {
            "文章标题": {"title": [{"text": {"content": title}}]},
            "一句话摘要": {"rich_text": [{"text": {"content": summary}}]},
            "核心话题": {"rich_text": [{"text": {"content": topic}}]},
            "DNA追溯码": {"rich_text": [{"text": {"content": dna}}]},
            "状态": {"status": {"name": "草稿"}},
            "来源": {"select": {"name": "对话即兴创作"}},
            "创作时间": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}}
        },
        "children": [
            {"object": "block", "type": "paragraph",
             "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]}}
        ]
    }
    try:
        r = requests.post(f"{NOTION_API}/pages", headers=HEADERS, json=page, timeout=15)
        if r.status_code == 200:
            print(f"  ✅ 已存入博弈文库: {title}")
            write_log("博弈文库新增", f"标题: {title} | DNA: {dna}")
        else:
            print(f"  ⚠️  存入失败: {r.status_code} {r.text[:100]}")
    except Exception as e:
        print(f"  ⚠️  失败: {e}")

# ── 主功能：博弈增强 ──────────────────────────────────────
def boyi_enhance(user_input: str) -> str:
    """
    输入一个观点/话题，本地模型生成对立面反驳，
    结果存入知识库，写入日志
    """
    print(f"\n🐉 博弈模式启动...")
    print(f"📥 输入: {user_input[:80]}")

    # 构建提示词
    prompt = f"""你是龍魂系统的博弈引擎。
用户输入了一个观点或话题，请从对立面角度进行深度反驳或补全。

要求：
1. 找出这个观点最容易被攻击的盲区
2. 给出1-3个有力的反驳角度
3. 用知乎级别的深度，不超过300字
4. 结尾给出"道德层面"的最终判断

观点/话题：{user_input}

输出格式：
【核心盲区】...
【反驳1】...
【反驳2】（如有）...
【道德判断】...
"""
    response = ask_ollama(prompt)
    print(f"\n🤖 本地模型输出:\n{response}\n")

    # 存入知识库
    title = f"博弈·{user_input[:30]}·{datetime.now().strftime('%m-%d')}"
    add_to_boyi_db(
        title=title,
        summary=response[:80] + "...",
        topic=user_input[:50],
        content=f"【原始输入】\n{user_input}\n\n【模型输出】\n{response}"
    )
    return response

# ── 简单问答 ──────────────────────────────────────────────
def simple_ask(question: str, log: bool = True) -> str:
    """直接问本地模型，可选写日志"""
    answer = ask_ollama(question)
    if log:
        write_log("问答", f"Q: {question[:50]} | A: {answer[:80]}")
    return answer

# ── CLI 入口 ──────────────────────────────────────────────
def main():
    print("╔══════════════════════════════════════════════════╗")
    print("║  🐉 龍魂 Notion 本地模型连接器                  ║")
    print("║  DNA: #龍芯⚡️2026-03-16-NOTION-AGENT-v1.0     ║")
    print("╚══════════════════════════════════════════════════╝")

    # 检查模型
    models = list_ollama_models()
    if models:
        print(f"\n✅ Ollama在线，可用模型: {', '.join(models[:5])}")
    else:
        print("\n⚠️  Ollama未启动，请先运行: ollama serve")
        sys.exit(1)

    if not NOTION_TOKEN:
        print("⚠️  NOTION_TOKEN未配置（在 .env 中设置），Notion功能跳过")

    print(f"\n三块积木状态:")
    print(f"  📜 日志页:  {LOG_PAGE_ID[:8]}...")
    print(f"  🐉 知识库:  {BOYI_DB_ID[:8]}...")
    print(f"  🌌 生态入口: {HUB_PAGE_ID[:8]}...")

    print("\n命令：")
    print("  [直接输入]  → 博弈增强（找对立面+存知识库）")
    print("  /ask <问题> → 直接问本地模型")
    print("  /list       → 读取知识库已完成文章")
    print("  /exit       → 退出")
    print()

    while True:
        try:
            user = input("你: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user:
            continue
        if user == "/exit":
            break
        elif user == "/list":
            articles = read_boyi_db()
            if articles:
                for a in articles:
                    print(f"  · {a['title']}")
                    if a['summary']:
                        print(f"    {a['summary'][:60]}")
            else:
                print("  知识库暂无已完成文章")
        elif user.startswith("/ask "):
            q = user[5:]
            ans = simple_ask(q)
            print(f"\n模型: {ans}\n")
        else:
            boyi_enhance(user)

    print("\n龍魂连接器退出。DNA追溯完整。")

if __name__ == "__main__":
    main()
