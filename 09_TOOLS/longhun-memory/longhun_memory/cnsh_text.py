#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·乙未·壬子·丙午·䷙大畜-MEMORY-CNSH-TEXT-v1.0
# License: MulanPSL v2
"""
CNSH 文本转换引擎
═════════════════
对话记忆 → CNSH 通用文本格式（人类可读 + 机器可解析）

CNSH 是数据流通的通用格式——让 longhun-memory / longhun-save / 鸿蒙插件
说同一种话。DNA 是追溯凭证，三色审计是状态语言。

格式:
  龍憶·對話 v1.0
  DNA: #龍芯⚡️...
  時間: ISO8601
  條數: N
  ═══════════
  [用户] ...
  [助手] ...
  ═══════════
  關鍵詞: k1, k2, k3
  審計: 🟢/🟡/🔴
"""

import json
import re
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple

from .dna import dna_now
from .audit import AuditColor, AuditMark


# ═══════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════

CNSH_HEADER = "龍憶·對話"
CNSH_VERSION = "v1.0"
CNSH_SEPARATOR = "═══════════"
CNSH_ROLE_MAP = {
    "user": "用户",
    "assistant": "助手",
    "system": "系统",
}


# ═══════════════════════════════════════════
# JSON → CNSH
# ═══════════════════════════════════════════

def json_to_cnsh(messages: List[Dict[str, str]],
                 dna: Optional[str] = None,
                 audit: Optional[str] = "🟢",
                 keywords: Optional[List[str]] = None) -> str:
    """将对话 JSON 列表转换为 CNSH 文本格式

    Args:
        messages: [{"role":"user","content":"..."}, ...]
        dna: DNA 追溯码（自动生成如果为 None）
        audit: 三色审计 emoji
        keywords: 关键词列表

    Returns:
        CNSH 格式文本
    """
    dna = dna or dna_now("MEMORY", "CNTX")
    ts = datetime.now(timezone.utc).isoformat()
    lines = []

    # 头部
    lines.append(f"{CNSH_HEADER} {CNSH_VERSION}")
    lines.append(f"DNA: {dna}")
    lines.append(f"時間: {ts}")
    lines.append(f"條數: {len(messages)}")
    lines.append(CNSH_SEPARATOR)

    # 对话体
    for msg in messages:
        role = msg.get("role", "unknown")
        cn_role = CNSH_ROLE_MAP.get(role, role)
        content = msg.get("content", "").strip()
        lines.append(f"[{cn_role}] {content}")

    # 尾部
    lines.append(CNSH_SEPARATOR)
    if keywords:
        lines.append(f"關鍵詞: {', '.join(keywords[:20])}")
    else:
        kw = _extract_all_keywords(messages)
        if kw:
            lines.append(f"關鍵詞: {', '.join(kw[:20])}")
    lines.append(f"審計: {audit}")

    return "\n".join(lines) + "\n"


# ═══════════════════════════════════════════
# CNSH → JSON
# ═══════════════════════════════════════════

def cnsh_to_json(text: str) -> Tuple[List[Dict[str, str]], dict]:
    """将 CNSH 文本解析回对话 JSON + 元数据

    Args:
        text: CNSH 格式文本

    Returns:
        (messages, metadata)
        messages: [{"role":"user","content":"..."}, ...]
        metadata: {"dna","time","msg_count","keywords","audit"}
    """
    lines = text.strip().split("\n")
    metadata = {}
    messages = []
    in_body = False

    cn_role_rev = {v: k for k, v in CNSH_ROLE_MAP.items()}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 头部解析
        if line.startswith("DNA:"):
            metadata["dna"] = line[4:].strip()
        elif line.startswith("時間:"):
            metadata["time"] = line[3:].strip()
        elif line.startswith("條數:"):
            metadata["msg_count"] = int(line[3:].strip())
        elif line.startswith("關鍵詞:"):
            metadata["keywords"] = [k.strip() for k in line[4:].split(",")]
        elif line.startswith("審計:"):
            metadata["audit"] = line[3:].strip()
        elif line == CNSH_SEPARATOR:
            in_body = not in_body
            continue

        # 消息体解析
        elif in_body and line.startswith("[") and "]" in line:
            bracket_end = line.index("]")
            cn_role = line[1:bracket_end]
            role = cn_role_rev.get(cn_role, cn_role.lower())
            content = line[bracket_end + 1:].strip()
            messages.append({"role": role, "content": content})

    return messages, metadata


# ═══════════════════════════════════════════
# 关键词提取
# ═══════════════════════════════════════════

def _extract_all_keywords(messages: List[Dict[str, str]]) -> List[str]:
    """从消息中提取关键词（中英文混合词频）"""
    all_text = " ".join(m.get("content", "") for m in messages)
    tokens = re.findall(r'[\u4e00-\u9fff]{2,}|[a-zA-Z]{3,}', all_text.lower())

    stop_words = {
        "这个","那个","我们","他们","什么","怎么","为什么","可以","一个",
        "没有","已经","还是","因为","所以","但是","不过","然后","就是",
        "the","and","for","that","this","with","was","are","not","but",
        "you","can","has","have","will","from","all","its",
    }
    filtered = [t for t in tokens if t.lower() not in stop_words]

    freq: dict = {}
    for t in filtered:
        freq[t] = freq.get(t, 0) + 1

    return sorted(freq.keys(), key=lambda k: freq[k], reverse=True)


# ═══════════════════════════════════════════
# 格式检测
# ═══════════════════════════════════════════

def is_cnsh_text(text: str) -> bool:
    """检测文本是否为 CNSH 格式"""
    return text.strip().startswith(f"{CNSH_HEADER} ")


def is_cnsh_json(text: str) -> bool:
    """检测文本是否为 JSON 格式"""
    try:
        json.loads(text)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def detect_format(text: str) -> str:
    """自动检测格式 → 'cnsh' | 'json' | 'unknown'"""
    if is_cnsh_text(text):
        return "cnsh"
    if is_cnsh_json(text):
        return "json"
    return "unknown"


# ═══════════════════════════════════════════
# 批量转换
# ═══════════════════════════════════════════

def batch_json_to_cnsh(input_path: str, output_path: str,
                       dna: Optional[str] = None) -> dict:
    """批量转换 JSON 对话文件 → CNSH 文本文件"""
    with open(input_path, "r", encoding="utf-8") as f:
        messages = json.load(f)

    cnsh = json_to_cnsh(messages, dna=dna)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cnsh)

    return {
        "input": input_path,
        "output": output_path,
        "messages": len(messages),
        "chars": len(cnsh),
    }


# ═══════════════════════════════════════════
# 自检
# ═══════════════════════════════════════════

if __name__ == "__main__":
    # 测试 JSON → CNSH → JSON 往返
    messages = [
        {"role": "user", "content": "你好，帮我记住：项目代号'龍魂'"},
        {"role": "assistant", "content": "已记住：项目代号'龍魂'"},
        {"role": "user", "content": "目标是保护数据主权"},
        {"role": "assistant", "content": "了解：目标是保护数据主权"},
    ]

    # 编码
    cnsh = json_to_cnsh(messages, keywords=["龍魂","数据主权"])
    print("=== CNSH 文本 ===")
    print(cnsh)

    # 格式检测
    assert is_cnsh_text(cnsh), "CNSH检测失败"
    assert detect_format(cnsh) == "cnsh", "格式检测失败"
    print(f"🟢 格式检测: {detect_format(cnsh)}")

    # 解码
    decoded, meta = cnsh_to_json(cnsh)
    assert len(decoded) == len(messages), f"消息数不一致: {len(decoded)} vs {len(messages)}"
    assert decoded[0]["content"] == messages[0]["content"], "内容不一致"
    print(f"🟢 往返解码: {len(decoded)} 条消息, 元数据: {list(meta.keys())}")

    # 测试 JSON 检测
    assert detect_format(json.dumps(messages)) == "json", "JSON检测失败"
    print("🟢 JSON格式检测通过")

    print("🟢 CNSH文本引擎自检通过")
