#!/usr/bin/env python3
"""
从已归档的 VSCode/Cursor 编辑器聊天 JSONL 中提取可读的 Markdown，
放入 Obsidian vault 供第二大脑索引。
DNA: #龍芯⚡️2026-06-29-EDITOR-CHAT-PROCESSOR-UID9622
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

DNA = "#龍芯⚡️2026-06-29-EDITOR-CHAT-PROCESSOR-UID9622"
ARCHIVE = Path("/Users/zuimeidedeyihan/longhun-system/brain/editor_memory_archive")
VAULT = Path.home() / "Obsidian" / "龍魂系統"
OUT_DIR = VAULT / "EditorChats"

def safe_text(val: Any) -> str:
    if val is None:
        return ""
    if isinstance(val, str):
        return val
    try:
        return json.dumps(val, ensure_ascii=False, indent=2)
    except Exception:
        return str(val)

def extract_vscode_copilot_transcript(path: Path) -> str:
    """解析 GitHub.copilot-chat transcripts jsonl"""
    lines: List[str] = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = obj.get("type")
                data = obj.get("data", {})
                if t == "user.message":
                    text = data.get("text") or ""
                    if text:
                        lines.append(f"**User**: {text}")
                elif t == "assistant.message":
                    content = data.get("content") or ""
                    if content:
                        lines.append(f"**Assistant**: {content}")
                    # tool results / file edits
                    for tr in data.get("toolRequests", []):
                        name = tr.get("name", "")
                        args = tr.get("arguments", "")
                        lines.append(f"- Tool `{name}`: `{args[:500]}`")
                elif t == "session.start":
                    lines.append(f"_Session {data.get('sessionId')} started {data.get('startTime')}_")
    except Exception as e:
        lines.append(f"_解析错误: {e}_")
    return "\n\n".join(lines)

def extract_vscode_chat_session(path: Path) -> str:
    """解析 VSCode chatSessions jsonl (kind-based)"""
    lines: List[str] = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                kind = obj.get("kind")
                v = obj.get("v")
                k = obj.get("k")
                if kind == 0 and isinstance(v, dict):
                    meta = v
                    lines.append(f"_Session {meta.get('sessionId')} 创建于 {meta.get('creationDate')}_")
                elif kind == 1:
                    lines.append(f"**属性变更** `{k}`: `{safe_text(v)[:500]}`")
                elif kind == 2 and isinstance(v, list):
                    for req in v:
                        message = req.get("message", {})
                        text = message.get("text") or message.get("parts") or ""
                        if text:
                            lines.append(f"**User**: {safe_text(text)}")
                        for resp in req.get("response", []) or []:
                            content = resp.get("content") or resp.get("text") or ""
                            if content:
                                lines.append(f"**Assistant**: {safe_text(content)}")
                        # tool calls
                        for tc in req.get("toolCalls", []) or []:
                            lines.append(f"- Tool `{tc.get('name')}`: `{safe_text(tc.get('arguments'))[:500]}`")
    except Exception as e:
        lines.append(f"_解析错误: {e}_")
    return "\n\n".join(lines)

def make_filename(path: Path) -> str:
    name = re.sub(r"[^\w\-]", "_", path.stem)[:60]
    return name or "chat"

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # VSCode Copilot transcripts
    for p in ARCHIVE.rglob("GitHub.copilot-chat/transcripts/*.jsonl"):
        text = extract_vscode_copilot_transcript(p)
        if not text.strip():
            continue
        out = OUT_DIR / f"vscode_copilot_{make_filename(p)}.md"
        md = f"---\ntitle: VSCode Copilot Chat {p.stem}\ntags: [VSCode, Copilot, Chat, 编辑器记忆]\ndna: {DNA}\n---\n\n# VSCode Copilot Chat `{p.stem}`\n\n{text}\n"
        out.write_text(md, encoding="utf-8")
        print("wrote", out, len(md))
    # VSCode chatSessions
    for p in ARCHIVE.rglob("chatSessions/*.jsonl"):
        text = extract_vscode_chat_session(p)
        if not text.strip():
            continue
        out = OUT_DIR / f"vscode_chat_{make_filename(p)}.md"
        md = f"---\ntitle: VSCode Chat Session {p.stem}\ntags: [VSCode, Chat, 编辑器记忆]\ndna: {DNA}\n---\n\n# VSCode Chat Session `{p.stem}`\n\n{text}\n"
        out.write_text(md, encoding="utf-8")
        print("wrote", out, len(md))

if __name__ == "__main__":
    main()
