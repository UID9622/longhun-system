#!/usr/bin/env python3
"""
compress_session.py - 会话DNA压缩 · 龍魂记忆回流
用法:
  python3 compress_session.py [文件路径]
  cat session.txt | python3 compress_session.py
  python3 compress_session.py   ← 手动粘贴，Ctrl+D结束
"""
import json, hashlib, os, sys
from datetime import datetime
from pathlib import Path

HOME        = Path.home()
MEMORY_FILE = HOME / "longhun-system/memory.jsonl"
ENV_FILE    = HOME / "longhun-system/.env"
OBS_PAGE_ID = "32c7125a9c9f819aa8c3f5eb189f83b0"  # Claude観察层（温记忆库）

def load_env() -> dict:
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return {**env, **os.environ}

def compress(text: str, api_key: str) -> str:
    try:
        import anthropic
        c = anthropic.Anthropic(api_key=api_key)
        r = c.messages.create(
            model="claude-opus-4-5", max_tokens=400,
            messages=[{"role": "user", "content":
                "请将以下对话压缩为150字以内的DNA摘要。\n"
                "保留：关键决策·技术里程碑·用户情感锚点·系统状态变更。\n"
                "格式：[核心]→[技术]→[情感]\n\n" + text[:8000]}])
        return r.content[0].text.strip()
    except Exception as e:
        return f"[截断] {text[:250].replace(chr(10),' ')}... (压缩失败:{e})"

def make_dna(summary: str) -> str:
    ts = datetime.now().strftime("%Y%m%d%H%M")
    h  = hashlib.md5(summary.encode("utf-8")).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{h}"

def push_notion(summary: str, dna: str, token: str) -> bool:
    if not token:
        return False
    try:
        import urllib.request
        content = f"🧬 {dna}\n🕐 {datetime.now():%Y-%m-%d %H:%M}\n\n{summary}"
        body = json.dumps({"children": [{"object":"block","type":"paragraph",
            "paragraph":{"rich_text":[{"type":"text","text":{"content":content}}]}}]
        }).encode("utf-8")
        req = urllib.request.Request(
            f"https://api.notion.com/v1/blocks/{OBS_PAGE_ID}/children",
            data=body, method="PATCH",
            headers={"Authorization": f"Bearer {token}",
                     "Notion-Version": "2022-06-28",
                     "Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception as e:
        print(f"  ⚠️  Notion写入失败: {e}"); return False

def main():
    env = load_env()
    if len(sys.argv) > 1:
        text = Path(sys.argv[1]).read_text("utf-8")
    else:
        if sys.stdin.isatty():
            print("📥 粘贴会话内容，完成后 Ctrl+D：")
        text = sys.stdin.read()
    if not text.strip():
        sys.exit("❌ 无内容")

    print(f"📊 输入 {len(text):,} 字符 → 压缩中…")
    summary = compress(text, env.get("ANTHROPIC_API_KEY",""))
    dna     = make_dna(summary)

    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MEMORY_FILE,"a",encoding="utf-8") as f:
        f.write(json.dumps({
            "dna":dna,"ts":datetime.now().isoformat(),
            "uid":"UID9622","summary":summary,"chars_in":len(text)
        }, ensure_ascii=False) + "\n")

    token = (env.get("NOTION_TOKEN") or env.get("NOTION_TOKEN_1")
             or env.get("NOTION_API_KEY",""))
    notion_ok = push_notion(summary, dna, token)

    print(f"\n{'─'*52}")
    print(f"🧬 {dna}")
    print(f"📝 摘要：\n{summary}")
    print(f"{'─'*52}")
    print(f"✅ memory.jsonl  ← 已写入")
    print(f"{'✅' if notion_ok else '❌'} Notion観察层  {'← 已追加' if notion_ok else '← 失败（检查token）'}")
    print(f"\n💡 下次任何AI：读 memory.jsonl 最新5条 → 暖启动完成")

if __name__ == "__main__":
    main()
