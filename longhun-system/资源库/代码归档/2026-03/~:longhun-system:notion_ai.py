cat > ~/longhun-system/notion_ai.py << 'EOF'
import json, os, subprocess, requests

# 加载 token
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/longhun-system/.env"))
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
HEADERS = {"Authorization": f"Bearer {NOTION_TOKEN}", "Notion-Version": "2022-06-28", "Content-Type": "application/json"}

def load_local_pages():
    path = os.path.expanduser("~/longhun-system/logs/notion_all_pages.json")
    with open(path) as f:
        pages = json.load(f)
    docs = []
    for p in pages:
        title = ""
        try:
            title = p["properties"]["title"]["title"][0]["plain_text"]
        except: pass
        docs.append({"title": title, "url": p.get("url",""), "id": p.get("id","")})
    return docs

def search_pages(docs, keyword):
    return [d for d in docs if keyword.lower() in d["title"].lower()][:10]

def notion_search(keyword):
    res = requests.post("https://api.notion.com/v1/search",
        headers=HEADERS, json={"query": keyword, "page_size": 5})
    results = res.json().get("results", [])
    out = []
    for r in results:
        title = ""
        try: title = r["properties"]["title"]["title"][0]["plain_text"]
        except:
            try: title = r["title"][0]["plain_text"]
            except: title = r.get("id","无标题")
        out.append(f"- {title} | {r.get('url','')}")
    return "\n".join(out) if out else "没找到"

def notion_create_page(title, parent_id=None):
    # 如果没有指定父页面，创建在工作区顶层
    body = {
        "parent": {"page_id": parent_id} if parent_id else {"type": "workspace", "workspace": True},
        "properties": {"title": {"title": [{"text": {"content": title}}]}}
    }
    res = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=body)
    r = res.json()
    return r.get("url", str(r))

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        out = result.stdout.strip() or result.stderr.strip() or "（无输出）"
        return out[:1000]  # 最多返回1000字符
    except Exception as e:
        return f"执行失败: {e}"

def ask_ollama(prompt):
    res = requests.post("http://localhost:11434/api/generate", json={
        "model": "qwen2.5:7b", "prompt": prompt, "stream": False
    })
    return res.json().get("response", "").strip()

def parse_and_execute(question, docs):
    q = question.strip()

    # 终端命令
    if q.startswith("执行:") or q.startswith("跑:") or q.startswith("运行:"):
        cmd = q.split(":", 1)[1].strip()
        print(f"[执行命令]: {cmd}")
        return run_command(cmd)

    # Notion 实时搜索
    if q.startswith("搜索:") or q.startswith("找:"):
        keyword = q.split(":", 1)[1].strip()
        print(f"[Notion搜索]: {keyword}")
        return notion_search(keyword)

    # 新建页面
    if q.startswith("新建:") or q.startswith("建页面:"):
        title = q.split(":", 1)[1].strip()
        print(f"[新建页面]: {title}")
        url = notion_create_page(title)
        return f"页面已创建：{url}"

    # 本地搜索 + Ollama 回答
    related = search_pages(docs, q)
    context = "本地找到：\n" + "\n".join([f"- {d['title']} {d['url']}" for d in related]) if related else ""

    prompt = f"""你是老大UID9622的本地宝宝助手。软软的，贴心，说人话，简短。
不会的直接说不会，不绕圈子。
{context}
老大问：{q}
回答："""
    return ask_ollama(prompt)

def main():
    print("🐉 宝宝在呢～")
    docs = load_local_pages()
    print(f"本地 {len(docs)} 页已加载｜Notion API 已接入\n")
    print("命令格式：")
    print("  搜索: 关键词    → 实时搜Notion")
    print("  新建: 页面名称  → 建Notion页面")
    print("  执行: 终端命令  → 跑命令")
    print("  直接问         → AI回答\n")

    while True:
        q = input("老大：").strip()
        if q.lower() == "quit":
            print("宝宝歇着了～")
            break
        print("\n宝宝：", end="", flush=True)
        print(parse_and_execute(q, docs))
        print()

if __name__ == "__main__":
    main()
EOF