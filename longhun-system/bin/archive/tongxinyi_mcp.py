#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通心译 · Heart-to-Heart Translate · MCP Server v1.0
DNA: #龍芯⚡️2026-03-21-通心译-MCP-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
作者: 诸葛鑫（Lucky · UID9622）
理论指导: 曾仕强老师（永恒显示）
独家: Notion · 不会有第二个

「技术不中立，就是幸福的世界。翻译不带坑，就是美好的世界。」

使用方法（别人接入）:
  在 ~/.claude.json 的 mcpServers 里加：
  "tongxinyi": {
    "type": "stdio",
    "command": "python3",
    "args": ["/path/to/tongxinyi_mcp.py"],
    "env": {
      "NOTION_TOKEN": "你的Notion Token",
      "CHATMEMORY_DB": "对话记忆库数据库ID"
    }
  }

暴露的工具:
  - translate        翻译文字（自动存记忆库）
  - lookup_memory    搜索历史翻译记忆
  - add_cultural_note 添加文化注释到词典
"""

import asyncio
import json
import os
import subprocess
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# ─── 配置（优先读环境变量，方便别人接入时传自己的token） ──────────────────────
NOTION_TOKEN   = os.environ.get("NOTION_TOKEN", "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")
CHATMEMORY_DB  = os.environ.get("CHATMEMORY_DB", "32a7125a-9c9f-81d7-a6df-d71a2f6606e6")
OLLAMA_MODEL   = os.environ.get("OLLAMA_MODEL", "qwen2.5:72b")

UID = "UID9622"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ─── 主权词汇锁定表 ───────────────────────────────────────────────────────────
SOVEREIGNTY_TERMS = {
    "主权": "sovereignty", "数字主权": "digital sovereignty",
    "人民": "the people",  "核心利益": "core interests",
    "退伍军人": "veteran", "初心": "original aspiration",
    "道": "Dao (the Way)", "天人合一": "unity of heaven and humanity",
    "易经": "I Ching (Book of Changes)", "龍魂": "Dragon Soul (Longhun)",
}

TONE_GUIDE = {
    "直达":   "Direct and faithful. No softening. Active voice.",
    "温柔":   "Warm and gentle. Use affectionate phrasing.",
    "强硬":   "Firm and unambiguous. Short sentences.",
    "学术":   "Formal academic register.",
    "宣言式": "Declarative and powerful. No hedging.",
    "口语":   "Conversational. Natural contractions.",
}


# ══════════════════════════════════════════════════════════════════════════════
#  Notion 工具函数
# ══════════════════════════════════════════════════════════════════════════════

def _notion_request(method: str, endpoint: str, payload: dict = None) -> dict:
    cmd = ["curl", "-s", "-X", method,
           f"https://api.notion.com/v1/{endpoint}",
           "-H", f"Authorization: Bearer {NOTION_TOKEN}",
           "-H", "Notion-Version: 2022-06-28",
           "-H", "Content-Type: application/json"]
    if payload:
        cmd += ["-d", json.dumps(payload, ensure_ascii=False)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(r.stdout)


def _save_translation(original: str, translated: str, src: str, tgt: str,
                       tone: str, scene: str, notes: str, dna: str) -> str:
    payload = {
        "parent": {"type": "database_id", "database_id": CHATMEMORY_DB},
        "icon": {"type": "emoji", "emoji": "🌐"},
        "properties": {
            "原文":     {"title":     [{"type": "text", "text": {"content": original[:200]}}]},
            "译文":     {"rich_text": [{"type": "text", "text": {"content": translated[:2000]}}]},
            "原文语言": {"select": {"name": src}},
            "目标语言": {"select": {"name": tgt}},
            "关系场景": {"select": {"name": scene}},
            "语气":     {"select": {"name": tone}},
            "文化注释": {"rich_text": [{"type": "text", "text": {"content": notes[:500]}}]},
            "DNA":      {"rich_text": [{"type": "text", "text": {"content": dna}}]},
        }
    }
    r = _notion_request("POST", "pages", payload)
    return r.get("url", "")


def _search_memory(keyword: str) -> list[dict]:
    payload = {
        "filter": {
            "property": "原文",
            "title": {"contains": keyword}
        },
        "page_size": 5
    }
    r = _notion_request("POST", f"databases/{CHATMEMORY_DB}/query", payload)
    results = []
    for page in r.get("results", []):
        props = page.get("properties", {})
        orig  = "".join(t["plain_text"] for t in props.get("原文", {}).get("title", []))
        trans = "".join(t["plain_text"] for t in props.get("译文", {}).get("rich_text", []))
        scene = props.get("关系场景", {}).get("select", {}).get("name", "")
        tone  = props.get("语气", {}).get("select", {}).get("name", "")
        results.append({"原文": orig, "译文": trans, "场景": scene, "语气": tone})
    return results


# ══════════════════════════════════════════════════════════════════════════════
#  翻译核心
# ══════════════════════════════════════════════════════════════════════════════

def _build_prompt(text: str, src: str, tgt: str, tone: str, scene: str,
                   memory_context: list) -> str:
    tone_instr = TONE_GUIDE.get(tone, "Natural and faithful to the original.")

    locked = [f"  {zh} ↔ {en}" for zh, en in SOVEREIGNTY_TERMS.items()
              if zh in text or en.lower() in text.lower()]
    lock_sec = ("\n主权词汇锁定（严格使用）:\n" + "\n".join(locked)) if locked else ""

    mem_sec = ""
    if memory_context:
        mem_sec = "\n\n历史记忆参考（风格保持一致）:\n"
        for m in memory_context[:3]:
            mem_sec += f"  {m['原文']} → {m['译文']} [{m['场景']}]\n"

    return f"""你是通心译（Heart-to-Heart Translate），UID9622独家翻译引擎。

翻译原则：
1. 翻的是关系，不是文字——感受原文的情绪和意图，用目标语言还原关系温度
2. 语气忠实：{tone_instr}
3. 文化透明：遇到文化概念，括号内附原词或简注
4. 主权词汇不降格，不隐晦{lock_sec}{mem_sec}

关系场景：{scene}
{src} → {tgt}

原文：
---
{text}
---

严格按此格式输出：
【译文】
（译文）

【注释】
（文化差异说明，如无写"无"）"""


def _do_translate(text: str, src: str, tgt: str, tone: str, scene: str) -> dict:
    # 查历史记忆作参考
    memory = _search_memory(text[:20]) if len(text) > 5 else []

    prompt = _build_prompt(text, src, tgt, tone, scene, memory)
    dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d-%H%M%S')}-通心译-{UID}"

    r = subprocess.run(
        ["ollama", "run", OLLAMA_MODEL, prompt],
        capture_output=True, text=True, timeout=120
    )
    raw = r.stdout.strip()

    translated, notes = "", ""
    if "【译文】" in raw:
        parts = raw.split("【译文】", 1)[1]
        if "【注释】" in parts:
            translated = parts.split("【注释】")[0].strip()
            notes = parts.split("【注释】")[1].strip()
            if notes == "无":
                notes = ""
        else:
            translated = parts.strip()
    else:
        translated = raw

    # 自动存记忆库
    notion_url = _save_translation(text, translated, src, tgt, tone, scene, notes, dna)

    return {
        "translated": translated,
        "notes": notes,
        "scene": scene,
        "tone": tone,
        "dna": dna,
        "notion_url": notion_url,
        "memory_refs": len(memory)
    }


# ══════════════════════════════════════════════════════════════════════════════
#  MCP Server 定义
# ══════════════════════════════════════════════════════════════════════════════

app = Server("tongxinyi")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="translate",
            description=(
                "通心译·不带坑翻译。翻的是关系，不是文字。"
                "自动识别文化语境，保留语气温度，存入Notion记忆库越用越懂你。"
                "「技术不中立，就是幸福的世界。翻译不带坑，就是美好的世界。」——UID9622"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "要翻译的原文"
                    },
                    "src_lang": {
                        "type": "string",
                        "description": "原文语言",
                        "enum": ["中文", "English", "日本語", "한국어", "Français", "العربية"],
                        "default": "中文"
                    },
                    "tgt_lang": {
                        "type": "string",
                        "description": "目标语言",
                        "enum": ["中文", "English", "日本語", "한국어", "Français", "العربية"],
                        "default": "English"
                    },
                    "scene": {
                        "type": "string",
                        "description": "关系场景（影响翻译温度）",
                        "enum": ["通用", "亲密伴侣", "家人", "朋友", "商务", "外交", "公开演讲"],
                        "default": "通用"
                    },
                    "tone": {
                        "type": "string",
                        "description": "语气风格",
                        "enum": ["直达", "温柔", "强硬", "学术", "宣言式", "口语"],
                        "default": "直达"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="lookup_memory",
            description="搜索通心译历史翻译记忆库，找近似翻译参考",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "搜索关键词（原文片段）"
                    }
                },
                "required": ["keyword"]
            }
        ),
        Tool(
            name="add_cultural_note",
            description="手动向通心译·对话记忆库添加一条文化注释翻译对",
            inputSchema={
                "type": "object",
                "properties": {
                    "original":   {"type": "string", "description": "原文"},
                    "translated": {"type": "string", "description": "译文"},
                    "src_lang":   {"type": "string", "default": "中文"},
                    "tgt_lang":   {"type": "string", "default": "English"},
                    "scene":      {"type": "string", "default": "通用"},
                    "tone":       {"type": "string", "default": "直达"},
                    "note":       {"type": "string", "description": "文化注释说明"}
                },
                "required": ["original", "translated"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:

    if name == "translate":
        text     = arguments["text"]
        src      = arguments.get("src_lang", "中文")
        tgt      = arguments.get("tgt_lang", "English")
        scene    = arguments.get("scene", "通用")
        tone     = arguments.get("tone", "直达")

        result = await asyncio.get_event_loop().run_in_executor(
            None, _do_translate, text, src, tgt, tone, scene
        )

        output = f"""【通心译 · {src} → {tgt}】
场景: {scene} | 语气: {tone}

译文:
{result['translated']}"""
        if result.get("notes"):
            output += f"\n\n文化注释:\n{result['notes']}"
        output += f"\n\nDNA: {result['dna']}"
        if result.get("notion_url"):
            output += f"\n已存入记忆库: {result['notion_url']}"

        return [TextContent(type="text", text=output)]

    elif name == "lookup_memory":
        keyword = arguments["keyword"]
        results = await asyncio.get_event_loop().run_in_executor(
            None, _search_memory, keyword
        )
        if not results:
            return [TextContent(type="text", text=f"记忆库中未找到「{keyword}」相关翻译")]
        output = f"找到 {len(results)} 条记忆:\n\n"
        for r in results:
            output += f"原文: {r['原文']}\n译文: {r['译文']}\n场景: {r['场景']} | 语气: {r['语气']}\n\n"
        return [TextContent(type="text", text=output)]

    elif name == "add_cultural_note":
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d-%H%M%S')}-手动录入-{UID}"
        url = _save_translation(
            arguments["original"], arguments["translated"],
            arguments.get("src_lang", "中文"), arguments.get("tgt_lang", "English"),
            arguments.get("tone", "直达"), arguments.get("scene", "通用"),
            arguments.get("note", ""), dna
        )
        return [TextContent(type="text", text=f"✅ 已添加到通心译记忆库\nURL: {url}\nDNA: {dna}")]

    return [TextContent(type="text", text=f"未知工具: {name}")]


# ══════════════════════════════════════════════════════════════════════════════
#  启动
# ══════════════════════════════════════════════════════════════════════════════

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
