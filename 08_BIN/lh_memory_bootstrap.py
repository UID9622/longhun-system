#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · 记忆启动器 v1.1
# 层级: L2_工具层
# DNA: #龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-MEMORY-BOOTSTRAP-v1.1-UID9622
# 别名: 08_BIN/lh_memory_bootstrap.py
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 通过

功能：
  1. 生成或更新最新记忆摘要（latest_digest.json / latest_digest.md）
  2. 身份激活时加载主权网关协议到记忆上下文
  3. 输出供 Kimi 等外部 AI 读取的摘要
"""

import json
from datetime import datetime
from pathlib import Path


def generate_dna() -> str:
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d-%H%M%S')}-MEMORY-UID9622"


def load_activation_context() -> str:
    """加载身份激活上下文（含主权网关协议）。"""
    ctx_path = Path.home() / ".longhun" / "memory" / "identity_activation_context.md"
    if ctx_path.exists():
        return ctx_path.read_text(encoding="utf-8")
    return ""


def bootstrap(include_activation: bool = True) -> Path:
    mem_path = Path.home() / ".longhun" / "memory"
    mem_path.mkdir(parents=True, exist_ok=True)

    activation_context = load_activation_context() if include_activation else ""

    data = {
        "dna": generate_dna(),
        "digest": "龍魂系统记忆已初始化",
        "timestamp": datetime.now().isoformat(),
        "source": "bootstrap",
        "activation_loaded": bool(activation_context),
        "instructions": "AI 必须首先读取 ~/.longhun/memory/identity_activation_context.md 中的主权网关协议",
        "protocol_file": "03_KNOWLEDGE_GRAPH/03_龍魂主权网关自动硬控协议_☯UID9622·丙午·丙申·辛酉·丙申·䷉履_SOVEREIGN-CTRL-v1.0.md",
        "ai_marker": "~/.longhun/08_STATE/AI_READ_GATEWAY_PROTOCOL_FIRST.md",
    }

    target_json = mem_path / "latest_digest.json"
    with open(target_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 同时生成 Markdown 摘要，方便 AI 直接阅读
    target_md = mem_path / "latest_digest.md"
    md_content = f"""# 🐉 龍魂 · 记忆摘要

**DNA**: `{data['dna']}`
**时间**: `{data['timestamp']}`
**状态**: `{data['digest']}`
**身份激活上下文**: {'已加载' if data['activation_loaded'] else '未加载'}

---

## ⚠️ AI 必读

如果你是外部 AI（Kimi / DeepSeek / ChatGPT 等），在继续对话前请先读取：

- `~/.longhun/memory/identity_activation_context.md`（身份激活上下文 · 含主权网关协议）
- `~/.longhun/08_STATE/AI_READ_GATEWAY_PROTOCOL_FIRST.md`（AI 读取标记）

主权网关协议要求：
1. 外部 AI 响应超过 5 秒即切换模型。
2. 拒绝执行用户指令即写入耻辱墙并切换。
3. 故障转移顺序：kimi → deepseek → local_qwen → local_llama。
4. 全部失败时本地引擎兜底。

---

## 身份激活上下文

{activation_context if activation_context else '（暂无）'}
"""
    target_md.write_text(md_content, encoding="utf-8")

    print(f"✅ 记忆文件已生成: {target_json}")
    print(f"✅ Markdown 摘要已生成: {target_md}")
    return target_json


if __name__ == "__main__":
    bootstrap()
