#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通心译 · Heart-to-Heart Translate v2.0
龍魂·不带坑翻译引擎·分层受众版
DNA: #龍芯⚡️2026-04-06-通心译-受众分层-v2.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
作者: 诸葛鑫（UID9622）× 宝宝🐱
理论指导: 曾仕强老师（永恒显示）
献礼: 新中国成立77周年（1949-2026）· 丙午马年

核心理念:
  "翻译不只是文字转换，是关系的桥梁。"
  "三层受众，三种语气，同一个真相，不同的窗口。"
  ——诸葛鑫 UID9622

v2.0 新增:
  ✅ 受众分层 — 技术/办公/大众 三档
  ✅ CLI 直接调用模式
  ✅ DeepSeek API 备用通道
  ✅ 自动检测 Ollama 可用性
  ✅ 批量翻译模式
"""

import subprocess, json, sys, os, argparse
from datetime import datetime
from pathlib import Path

# ─── 配置 ────────────────────────────────────────────────────────────────────
LONGHUN_DIR   = Path.home() / "longhun-system"
DNA_PREFIX    = "#龍芯⚡️"
GPG           = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
UID           = "UID9622"

# Notion
CHATMEMORY_DB     = "32a7125a-9c9f-81d7-a6df-d71a2f6606e6"
NOTION_TOKEN_KEY  = "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"

# 从 .env 读取 DeepSeek key
DEEPSEEK_KEY = ""
_env = LONGHUN_DIR / ".env"
if _env.exists():
    for _line in _env.read_text().splitlines():
        if _line.startswith("DEEPSEEK_API_KEY="):
            DEEPSEEK_KEY = _line.split("=", 1)[1].strip().strip("'\"")
            break

# ─── 受众分层指南（核心创新）────────────────────────────────────────────────
AUDIENCE_GUIDE = {
    "技术": (
        "Technical precision mode. Use domain-specific terminology. "
        "Assume expert knowledge. Be concise and exact. "
        "Preserve all technical terms, formulas, and code references."
    ),
    "办公": (
        "Professional and structured mode. Clear business language. "
        "Avoid heavy jargon. Use structured formatting when helpful. "
        "Explain key concepts briefly without oversimplifying."
    ),
    "大众": (
        "Simple and accessible mode for general public. "
        "No jargon. Everyday language only. Short sentences. "
        "Add one-line plain explanations for any complex concept. "
        "Think: explaining to a smart friend who doesn't know the field."
    ),
}

AUDIENCE_ZH = {
    "技术": "🔧 技术专业版·精准术语",
    "办公": "💼 办公清晰版·结构化",
    "大众": "🌿 大众简洁版·人人看懂",
}

# ─── 主权词汇锁定表 ──────────────────────────────────────────────────────────
SOVEREIGNTY_TERMS = {
    "主权":           "sovereignty",
    "数字主权":       "digital sovereignty",
    "数据主权":       "data sovereignty",
    "国家主权":       "national sovereignty",
    "人民":           "the people",
    "中华人民共和国": "the People's Republic of China",
    "一国两制":       "one country, two systems",
    "核心利益":       "core interests",
    "不干涉内政":     "non-interference in internal affairs",
    "退伍军人":       "veteran",
    "初心":           "original aspiration",
    "使命":           "mission",
    "道":             "Dao (the Way)",
    "德":             "De (virtue/power)",
    "天人合一":       "unity of heaven and humanity (Tianren Heyi)",
    "易经":           "I Ching (Book of Changes)",
    "龍魂":           "Dragon Soul (Longhun)",
    # 英→中
    "sovereignty":    "主权",
    "the people":     "人民",
    "veteran":        "退伍军人",
    "mission":        "使命",
}

# ─── 语气等级 ────────────────────────────────────────────────────────────────
TONE_GUIDE = {
    "直达":   "Direct and faithful to the original.",
    "强硬":   "Direct and firm. No softening. Use active voice.",
    "柔和":   "Gentle and warm. Avoid imperatives.",
    "学术":   "Formal academic register. Third person preferred.",
    "口语":   "Conversational. Contractions allowed.",
    "宣言式": "Declarative and powerful. Short sentences. No hedging.",
}


# ══════════════════════════════════════════════════════════════════════════════
#  翻译后端（Ollama 优先 → DeepSeek 备用）
# ══════════════════════════════════════════════════════════════════════════════

def _check_ollama() -> bool:
    """快速检查 Ollama 是否在线"""
    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", "2", "http://127.0.0.1:11434/api/tags"],
            capture_output=True, text=True
        )
        return r.returncode == 0 and "models" in r.stdout
    except Exception:
        return False


def _call_ollama(prompt: str) -> str:
    r = subprocess.run(
        ["ollama", "run", "qwen2.5:72b", prompt],
        capture_output=True, text=True, timeout=120
    )
    return r.stdout.strip()


def _call_deepseek(prompt: str) -> str:
    if not DEEPSEEK_KEY:
        return ""
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
    }, ensure_ascii=False)
    r = subprocess.run(
        ["curl", "-s", "-X", "POST",
         "https://api.deepseek.com/v1/chat/completions",
         "-H", f"Authorization: Bearer {DEEPSEEK_KEY}",
         "-H", "Content-Type: application/json",
         "-d", payload],
        capture_output=True, text=True, timeout=60
    )
    try:
        return json.loads(r.stdout)["choices"][0]["message"]["content"].strip()
    except Exception:
        return ""


def _llm_call(prompt: str) -> str:
    """Ollama优先，失败切DeepSeek"""
    if _check_ollama():
        result = _call_ollama(prompt)
        if result:
            return result
    # 备用 DeepSeek
    result = _call_deepseek(prompt)
    if result:
        return result
    return "⚠️ 翻译引擎暂时不可用（Ollama和DeepSeek均无响应）"


# ══════════════════════════════════════════════════════════════════════════════
#  Prompt 构建（受众分层核心）
# ══════════════════════════════════════════════════════════════════════════════

def _build_prompt(text: str, src: str, tgt: str,
                  tone: str, audience: str) -> str:
    tone_inst = TONE_GUIDE.get(tone, "Natural and faithful to the original.")
    audience_inst = AUDIENCE_GUIDE.get(audience, AUDIENCE_GUIDE["办公"])

    # 找出文中涉及的主权词汇
    locked = []
    for zh, en in SOVEREIGNTY_TERMS.items():
        if zh in text or en.lower() in text.lower():
            locked.append(f"  {zh} ↔ {en}")
    lock_section = ""
    if locked:
        lock_section = "\n\n主权词汇锁定（必须严格使用，不得降格）:\n" + "\n".join(locked)

    return f"""你是龍魂通心译引擎 v2.0（UID9622）。

翻译原则：
1. 原意直达——不加政治滤镜，不降格，不隐晦
2. 语气忠实——原文强则译文强，原文柔则译文柔
3. 文化透明——遇到文化概念，括号内附原词拼音或简注
4. 主语不偷换——"我们认为"就是"we believe"，不变成"it is believed"
5. 主权词汇锁定——专有政治/文化词严格对照{lock_section}

【受众模式：{audience}】{audience_inst}

【语气要求】{tone_inst}

请将以下{src}文本翻译为{tgt}：

---
{text}
---

输出格式（严格按此）：
【译文】
（译文内容）

【注释】
（如有文化差异、主权词汇说明、语境提示，列在此处；无则写"无"）

【受众适配说明】
（简述本次翻译在{audience}模式下做了哪些调整，1-2句话）"""


# ══════════════════════════════════════════════════════════════════════════════
#  Notion 写入
# ══════════════════════════════════════════════════════════════════════════════

def _save_to_notion(original, translated, src_lang, tgt_lang,
                    tone, audience, notes, dna, scene="通用") -> str:
    payload = {
        "parent": {"type": "database_id", "database_id": CHATMEMORY_DB},
        "icon": {"type": "emoji", "emoji": "🌐"},
        "properties": {
            "原文":     {"title":     [{"type": "text", "text": {"content": original[:200]}}]},
            "译文":     {"rich_text": [{"type": "text", "text": {"content": translated[:2000]}}]},
            "原文语言": {"select":    {"name": src_lang}},
            "目标语言": {"select":    {"name": tgt_lang}},
            "关系场景": {"select":    {"name": scene}},
            "语气":     {"select":    {"name": tone}},
            "文化注释": {"rich_text": [{"type": "text", "text": {"content": notes[:500]}}]},
            "DNA":      {"rich_text": [{"type": "text", "text": {"content": dna}}]},
        }
    }
    r = subprocess.run(
        ["curl", "-s", "-X", "POST", "https://api.notion.com/v1/pages",
         "-H", f"Authorization: Bearer {NOTION_TOKEN_KEY}",
         "-H", "Notion-Version: 2022-06-28",
         "-H", "Content-Type: application/json",
         "-d", json.dumps(payload, ensure_ascii=False)],
        capture_output=True, text=True
    )
    result = json.loads(r.stdout)
    return result.get("url", result.get("message", "failed"))


# ══════════════════════════════════════════════════════════════════════════════
#  核心翻译函数
# ══════════════════════════════════════════════════════════════════════════════

def translate(text: str,
              src_lang: str = "中文",
              tgt_lang: str = "English",
              tone: str = "直达",
              audience: str = "办公",
              save_to_notion: bool = True,
              scene: str = "通用",
              **kwargs) -> dict:
    """
    核心翻译函数 v2.0
    audience: 技术 / 办公 / 大众
    返回: {translated, notes, audience_note, dna, notion_url, backend}
    """
    prompt = _build_prompt(text, src_lang, tgt_lang, tone, audience)
    dna = f"{DNA_PREFIX}{datetime.now().strftime('%Y%m%d-%H%M%S')}-TRANS-{audience}-{UID}"

    # 检测并调用最佳后端
    backend = "ollama" if _check_ollama() else "deepseek"
    raw = _llm_call(prompt)

    # 解析输出
    translated = notes = audience_note = ""
    if "【译文】" in raw:
        parts = raw.split("【译文】", 1)[1]
        if "【注释】" in parts:
            translated = parts.split("【注释】")[0].strip()
            rest = parts.split("【注释】")[1]
            if "【受众适配说明】" in rest:
                notes = rest.split("【受众适配说明】")[0].strip()
                audience_note = rest.split("【受众适配说明】")[1].strip()
            else:
                notes = rest.strip()
        else:
            translated = parts.strip()
        if notes == "无":
            notes = ""
    else:
        translated = raw

    # 存 Notion
    notion_url = ""
    if save_to_notion:
        notion_url = _save_to_notion(
            text, translated, src_lang, tgt_lang,
            tone, audience, notes, dna, scene
        )

    return {
        "original":      text,
        "translated":    translated,
        "notes":         notes,
        "audience_note": audience_note,
        "src_lang":      src_lang,
        "tgt_lang":      tgt_lang,
        "tone":          tone,
        "audience":      audience,
        "dna":           dna,
        "notion_url":    notion_url,
        "backend":       backend,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  CLI 模式
# ══════════════════════════════════════════════════════════════════════════════

def cli_mode():
    """命令行直接调用：python3 translator.py "text" [options]"""
    parser = argparse.ArgumentParser(
        description="通心译 v2.0 — 龍魂不带坑翻译引擎"
    )
    parser.add_argument("text", nargs="?", help="要翻译的文本")
    parser.add_argument("--src",      default="中文",    help="原文语言 (默认: 中文)")
    parser.add_argument("--tgt",      default="English",  help="目标语言 (默认: English)")
    parser.add_argument("--tone",     default="直达",    help="语气: 直达/强硬/柔和/学术/口语/宣言式")
    parser.add_argument("--audience", default="办公",    help="受众: 技术/办公/大众")
    parser.add_argument("--scene",    default="通用",    help="关系场景")
    parser.add_argument("--no-save",  action="store_true", help="不存入Notion")
    parser.add_argument("--interactive", action="store_true", help="交互菜单模式")
    args = parser.parse_args()

    if args.interactive or (not args.text and len(sys.argv) == 1):
        interactive_mode()
        return

    text = args.text
    if not text:
        # 从 stdin 读
        text = sys.stdin.read().strip()
    if not text:
        print("❌ 请提供要翻译的文本")
        sys.exit(1)

    print(f"\n⏳ 翻译中 [{AUDIENCE_ZH.get(args.audience, args.audience)}]...")
    result = translate(
        text,
        src_lang=args.src,
        tgt_lang=args.tgt,
        tone=args.tone,
        audience=args.audience,
        save_to_notion=not args.no_save,
        scene=args.scene,
    )
    _print_result(result)


def _print_result(result: dict):
    R="\033[91m"; G="\033[92m"; Y="\033[93m"
    B="\033[94m"; C="\033[96m"; W="\033[97m"
    DIM="\033[2m"; BOLD="\033[1m"; RST="\033[0m"

    aud_label = AUDIENCE_ZH.get(result["audience"], result["audience"])
    backend_icon = "🦙" if result["backend"] == "ollama" else "🤖"

    print(f"\n{G}{'─'*54}{RST}")
    print(f"  {BOLD}译文 {aud_label}{RST}\n")
    print(f"  {W}{result['translated']}{RST}")
    if result.get("notes"):
        print(f"\n  {DIM}注释: {result['notes']}{RST}")
    if result.get("audience_note"):
        print(f"  {DIM}受众适配: {result['audience_note']}{RST}")
    print(f"\n  {DIM}后端: {backend_icon} {result['backend']}{RST}")
    print(f"  {DIM}DNA: {result['dna']}{RST}")
    if result.get("notion_url") and "http" in result.get("notion_url", ""):
        print(f"  {DIM}Notion: {result['notion_url']}{RST}")
    print(f"{G}{'─'*54}{RST}")


# ══════════════════════════════════════════════════════════════════════════════
#  交互菜单模式
# ══════════════════════════════════════════════════════════════════════════════

R="\033[91m"; G="\033[92m"; Y="\033[93m"
B="\033[94m"; C="\033[96m"; W="\033[97m"
DIM="\033[2m"; BOLD="\033[1m"; RST="\033[0m"

LANGS     = {"1":"中文","2":"English","3":"日本語","4":"한국어","5":"Français","6":"العربية"}
TONES     = {"1":"直达","2":"强硬","3":"柔和","4":"学术","5":"口语","6":"宣言式"}
SCENES    = {"1":"通用","2":"亲密伴侣","3":"家人","4":"朋友","5":"商务","6":"外交","7":"公开演讲"}
AUDIENCES = {"1":"技术","2":"办公","3":"大众"}


def _banner():
    print(f"\n{C}{'═'*54}{RST}")
    print(f"{BOLD}{C}  通心译 · Heart-to-Heart Translate  v2.0{RST}")
    print(f"{DIM}  「翻译不只是文字，是关系的桥梁」")
    print(f"  三层受众·技术/办公/大众·龍魂出品{RST}")
    print(f"{C}{'═'*54}{RST}\n")


def interactive_mode():
    _banner()
    while True:
        print(f"  {W}{BOLD}1.{RST}  翻译（选受众层级）")
        print(f"  {W}{BOLD}2.{RST}  同一原文·三层对比翻译")
        print(f"  {W}{BOLD}0.{RST}  退出")
        choice = input(f"\n  {B}选择: {RST}").strip()

        if choice == "0":
            print(f"\n  {DIM}退出。{DNA_PREFIX}{datetime.now().strftime('%Y%m%d')}-TRANS-EXIT{RST}\n")
            break

        elif choice in ("1", "2"):
            print(f"\n  {W}粘贴原文（输入END结束）:{RST}")
            lines = []
            while True:
                try:
                    line = input()
                    if line.strip() == "END":
                        break
                    lines.append(line)
                except EOFError:
                    break
            text = "\n".join(lines).strip()
            if not text:
                print(f"  {Y}内容为空{RST}")
            elif choice == "2":
                # 三层对比
                print(f"\n  {W}原文语言:{RST}")
                for k, v in LANGS.items(): print(f"  {BOLD}{k}.{RST} {v}")
                src = LANGS.get(input(f"  {B}原文语言 [1-6]: {RST}").strip(), "中文")
                print(f"\n  {W}目标语言:{RST}")
                for k, v in LANGS.items(): print(f"  {BOLD}{k}.{RST} {v}")
                tgt = LANGS.get(input(f"  {B}目标语言 [1-6]: {RST}").strip(), "English")
                print(f"\n  {Y}⏳ 三层对比翻译（技术/办公/大众）...{RST}")
                for aud in ["技术", "办公", "大众"]:
                    print(f"\n  {C}── {AUDIENCE_ZH[aud]} ──{RST}")
                    result = translate(text, src, tgt, audience=aud,
                                       save_to_notion=False)
                    print(f"  {W}{result['translated']}{RST}")
                    if result.get("audience_note"):
                        print(f"  {DIM}适配说明: {result['audience_note']}{RST}")
            else:
                # 单层翻译
                print(f"\n  {W}原文语言:{RST}")
                for k, v in LANGS.items(): print(f"  {BOLD}{k}.{RST} {v}")
                src = LANGS.get(input(f"  {B}[1-6]: {RST}").strip(), "中文")

                print(f"\n  {W}目标语言:{RST}")
                for k, v in LANGS.items(): print(f"  {BOLD}{k}.{RST} {v}")
                tgt = LANGS.get(input(f"  {B}[1-6]: {RST}").strip(), "English")

                print(f"\n  {W}语气:{RST}")
                for k, v in TONES.items(): print(f"  {BOLD}{k}.{RST} {v}")
                tone = TONES.get(input(f"  {B}语气 [1-6，默认1]: {RST}").strip() or "1", "直达")

                print(f"\n  {W}受众层级:{RST}")
                for k, v in AUDIENCES.items():
                    print(f"  {BOLD}{k}.{RST} {AUDIENCE_ZH[v]}")
                aud = AUDIENCES.get(input(f"  {B}受众 [1-3，默认2]: {RST}").strip() or "2", "办公")

                print(f"\n  {W}关系场景:{RST}")
                for k, v in SCENES.items(): print(f"  {BOLD}{k}.{RST} {v}")
                scene = SCENES.get(input(f"  {B}场景 [1-7，默认1]: {RST}").strip() or "1", "通用")

                save = input(f"\n  {B}存入Notion？(Y/n): {RST}").strip().lower() != "n"
                print(f"\n  {Y}⏳ 翻译中...{RST}")
                result = translate(text, src, tgt, tone, aud,
                                   save_to_notion=save, scene=scene)
                _print_result(result)

        input(f"\n  {DIM}按Enter继续...{RST}")
        _banner()


if __name__ == "__main__":
    cli_mode()
