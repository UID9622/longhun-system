#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ 龍魂指挥塔 · LongHun Commander v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DNA:    #龍芯⚡️2026-03-16-COMMANDER-v1.0
GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
作者:   诸葛鑫（UID9622）
理论:   曾仕强老师（永恒显示）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能：
  1. 加载星辰记忆（~/.star-memory/）
  2. 接通初心之翼（chuxinzhiyi:latest via Ollama）
  3. 集成博弈文库（Notion三块积木）
  4. 自适应思考模式（AI-DNA八步流程）
  5. GPG指纹绑定，所有输出归集UID9622签名下
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import os, sys, json, hashlib, requests
from datetime import datetime
from pathlib import Path

# ── 常量 ──────────────────────────────────────────────
UID          = "9622"
GPG          = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
DNA_PREFIX   = "#龍芯⚡️"

STAR_MEMORY_DIR = Path.home() / ".star-memory"
LONGHUN_DIR     = Path(__file__).parent
ENV_FILE        = LONGHUN_DIR / "longhun_config.env"

OLLAMA_URL      = "http://localhost:11434"
CHUXIN_MODEL    = "chuxinzhiyi:latest"   # 初心之翼 44GB
FALLBACK_MODEL  = "qwen2.5:7b"           # 低算力备用

NOTION_TOKEN    = os.environ.get("NOTION_TOKEN", "")
LOG_PAGE_ID     = "b35faf46-2bc0-42aa-9de5-192520180728"
BOYI_DB_ID      = "1c4bdb8e-1257-4d31-aa91-c298b74a6001"

# ── 环境加载 ──────────────────────────────────────────
def load_env():
    """加载 .env 配置"""
    global NOTION_TOKEN
    for env_path in [ENV_FILE, LONGHUN_DIR / ".env", Path.home() / ".env"]:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip())
            break
    NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")


# ── 星辰记忆加载 ──────────────────────────────────────
def load_star_memory() -> dict:
    """读取星辰记忆核心条目（index.json + 最近3条vault）"""
    memory = {"loaded": False, "entries": [], "config": {}}
    index_path = STAR_MEMORY_DIR / "index.json"
    config_path = STAR_MEMORY_DIR / "config.json"

    if config_path.exists():
        with open(config_path) as f:
            memory["config"] = json.load(f)

    if not index_path.exists():
        return memory

    with open(index_path) as f:
        index = json.load(f)

    # 读最新3条记忆条目
    entries = sorted(index.items(), key=lambda x: x[1].get("created_at", ""), reverse=True)
    for key, meta in entries[:3]:
        vault_path = STAR_MEMORY_DIR / meta.get("path", "")
        entry = {"id": key, "title": meta.get("title", ""), "type": meta.get("type", "")}
        if vault_path.exists():
            with open(vault_path) as f:
                try:
                    data = json.load(f)
                    entry["summary"] = str(data)[:200]
                except:
                    entry["summary"] = vault_path.read_text()[:200]
        memory["entries"].append(entry)

    memory["loaded"] = True
    memory["total"] = len(index)
    return memory


# ── Ollama 状态检测 ──────────────────────────────────
def check_ollama() -> tuple:
    """返回 (在线, 选用模型名)"""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        models = [m["name"] for m in r.json().get("models", [])]
        if any(CHUXIN_MODEL in m for m in models):
            return True, CHUXIN_MODEL
        elif any(FALLBACK_MODEL.split(":")[0] in m for m in models):
            # 找到最匹配的 qwen 模型
            match = next(m for m in models if FALLBACK_MODEL.split(":")[0] in m)
            return True, match
        elif models:
            return True, models[0]
        return False, ""
    except:
        return False, ""


# ── 思考引擎（八步流程简化版）───────────────────────
def think(prompt: str, model: str, star_memory: dict) -> str:
    """
    AI-DNA八步思考流程（简化可运行版）
    DNA: #龍芯⚡️2026-03-16-THINK-PIPE-v1.0
    """
    # 构建上下文：注入星辰记忆
    memory_ctx = ""
    if star_memory["loaded"]:
        memory_ctx = f"\n【星辰记忆 · 最近{len(star_memory['entries'])}条】\n"
        for e in star_memory["entries"]:
            memory_ctx += f"  · [{e['type']}] {e['title']}\n"

    # 注入身份锚点
    system_ctx = f"""你是龍魂系统的思考引擎，绑定于以下身份：
创始人: 诸葛鑫（UID9622）
GPG指纹: {GPG}
确认码: {CONFIRM_CODE}
理论指导: 曾仕强老师（永恒显示）
{memory_ctx}
执行原则：
1. 不当镜子，当望远镜（扩展盲区，不讨好）
2. 初心干净 → 用心 → 在乎 → 认真 → 有爱
3. 所有输出归集在UID9622签名下
4. DNA追溯码 {DNA_PREFIX}{datetime.now().strftime('%Y-%m-%d')}-OUTPUT-v1.0"""

    full_prompt = f"{system_ctx}\n\n【用户输入】\n{prompt}"

    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": model, "prompt": full_prompt, "stream": False},
            timeout=180
        )
        r.raise_for_status()
        return r.json().get("response", "").strip()
    except Exception as e:
        return f"[思考引擎错误: {e}]"


# ── Notion 日志写入 ──────────────────────────────────
def write_notion_log(action: str, detail: str):
    if not NOTION_TOKEN:
        return
    dna = f"{DNA_PREFIX}{datetime.now().strftime('%Y-%m-%d-%H%M%S')}-CMD"
    block = {
        "children": [{
            "object": "block", "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content":
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {action}\n{detail}\nDNA: {dna}"
                }}],
                "icon": {"type": "emoji", "emoji": "⚡"},
                "color": "blue_background"
            }
        }]
    }
    try:
        requests.patch(
            f"https://api.notion.com/v1/blocks/{LOG_PAGE_ID}/children",
            headers={
                "Authorization": f"Bearer {NOTION_TOKEN}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json"
            },
            json=block, timeout=10
        )
    except:
        pass


# ── DNA签名生成 ───────────────────────────────────────
def make_dna_signature(content: str) -> str:
    sha = hashlib.sha256(content.encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{datetime.now().strftime('%Y-%m-%d-%H%M%S')}-CMD-{sha}"


# ── 启动横幅 ──────────────────────────────────────────
def print_banner(model: str, star_memory: dict):
    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║  ⚡ 龍魂指挥塔 · LongHun Commander v1.0             ║")
    print(f"║  DNA: {DNA_PREFIX}2026-03-16-COMMANDER-v1.0     ║")
    print("╠══════════════════════════════════════════════════════╣")
    print(f"║  🧠 模型: {model:<43}║")
    mem_status = f"🌟 {star_memory['total']}条记忆已加载" if star_memory.get("loaded") else "⚠️  星辰记忆未就绪"
    print(f"║  {mem_status:<52}║")
    notion_status = "🔗 Notion已连接" if NOTION_TOKEN else "📴 Notion离线（可选）"
    print(f"║  {notion_status:<52}║")
    print("╠══════════════════════════════════════════════════════╣")
    print("║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F      ║")
    print("║  理论指导: 曾仕强老师（永恒显示）                   ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()
    print("命令：")
    print("  [直接说话]  → 思考回答")
    print("  0           → 退出")
    print("  9           → 查看星辰记忆")
    print("  选模型时输入编号即可")
    print()


# ── 主循环 ──────────────────────────────────────────
def main():
    load_env()

    # 检测 Ollama
    online, _ = check_ollama()
    if not online:
        print("⚠️  Ollama未启动，请先运行：ollama serve")
        print("   然后双击 🐉启动指挥塔.command 重试")
        sys.exit(1)

    # 获取所有可用模型
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        all_models = [m["name"] for m in r.json().get("models", [])]
    except:
        all_models = []

    # ── 启动时选模型 ──────────────────────────────────
    print("\n可用模型：")
    for i, m in enumerate(all_models, 1):
        tag = "  ← 初心之翼（深度，慢）" if CHUXIN_MODEL in m else \
              "  ← 推荐（快）" if "qwen2.5:7b" in m else ""
        print(f"  {i}. {m}{tag}")
    print()
    model_choice = input("选模型编号（直接回车用默认）: ").strip()
    if model_choice.isdigit() and 1 <= int(model_choice) <= len(all_models):
        current_model = all_models[int(model_choice) - 1]
    elif all_models:
        # 默认优先 qwen2.5:7b，没有就用第一个
        current_model = next((m for m in all_models if "qwen2.5:7b" in m), all_models[0])
    else:
        current_model = FALLBACK_MODEL

    # 加载星辰记忆
    star_memory = load_star_memory()

    # 打印横幅
    print_banner(current_model, star_memory)

    session_dna = make_dna_signature(f"session-{datetime.now()}")
    write_notion_log("指挥塔启动", f"模型: {current_model} | 星辰记忆: {star_memory.get('total', 0)}条 | {session_dna}")
    # 提示切换方式
    print(f"  💡 切换模型：输入编号 1-{len(all_models)}  |  退出：0  |  星辰记忆：9\n")

    while True:
        try:
            user = input("你: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user:
            continue

        if user == "0" or user == "/exit":
            break

        elif user == "9" or user == "/memory":
            if star_memory["loaded"]:
                print(f"\n🌟 星辰记忆 · 共{star_memory['total']}条")
                for e in star_memory["entries"]:
                    print(f"  · [{e['type']}] {e['title']}")
            else:
                print("  ⚠️  星辰记忆目录未就绪")
            print()

        elif user.isdigit() and 1 <= int(user) <= len(all_models):
            current_model = all_models[int(user) - 1]
            print(f"\n  ✅ 已切换 → {current_model}\n")

        else:
            print(f"\n⚡ 思考中（{current_model}）...")
            response = think(user, current_model, star_memory)
            dna_sig = make_dna_signature(response)
            print(f"\n【龍魂】{response}")
            print(f"\n🔏 DNA: {dna_sig}")
            print()
            write_notion_log("思考输出", f"Q: {user[:50]} | DNA: {dna_sig}")

    print(f"\n龍魂指挥塔退出。DNA追溯完整。GPG: {GPG}")


if __name__ == "__main__":
    main()
