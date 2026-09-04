#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
🐉 龍魂生态 · 身份激活引擎 v1.0
# 层级: L1_引擎层
# DNA: #龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-IDENTITY-ACTIVATION-v1.0-UID9622
# 别名: 08_BIN/lh_identity_activation.py
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 通过

核心能力：
  1. 识别身份激活口令（语音/文字）
  2. 读取仓库主权网关协议
  3. 生成 AI 可见的激活上下文（.longhun/memory/identity_activation_context.md）
  4. 更新 latest_digest.json，让 Kimi 等外部 AI 启动时自动读取
  5. 写入审计日志

激活口令：
  - "激活身份"
  - "龍魂身份激活"
  - "UID9622 上线"
  - "主权网关启动"
"""

import os
import sys
import json
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

# ============================================================
# 常量
# ============================================================
DNA = "#龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-IDENTITY-ACTIVATION-v1.0-UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
UID = "9622"

HOME = Path.home()
PROJECT_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = HOME / ".longhun" / "memory"
AUDIT_DIR = HOME / ".longhun" / "04_AUDIT"
STATE_DIR = HOME / ".longhun" / "08_STATE"

PROTOCOL_PATH = PROJECT_DIR / "03_KNOWLEDGE_GRAPH" / "03_龍魂主权网关自动硬控协议_☯UID9622·丙午·丙申·辛酉·丙申·䷉履_SOVEREIGN-CTRL-v1.0.md"
ENGINE_PATH = PROJECT_DIR / "05_ENGINES" / "L1_引擎_自动流_☯UID9622·丙午·丙申·辛酉·丙申·䷉履.py"
CONFIG_PATH = HOME / ".longhun" / "configs" / "gateway-hardcode.yaml"

ACTIVATION_KEYWORDS = [
    "激活身份",
    "龍魂身份激活",
    "UID9622 上线",
    "UID9622上线",
    "主权网关启动",
    "龍魂启动",
    "龍魂启动",
    "唤醒龍魂",
    "唤醒龍魂",
]


def generate_dna(suffix: str = "") -> str:
    ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    rand = hashlib.sha256(f"{suffix}{ts}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{suffix}-{UID}-{rand}"


def ensure_dirs():
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def append_jsonl(path: Path, entry: Dict[str, Any]):
    ensure_dirs()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def record_audit(operation: str, detail: Dict[str, Any], status: str = "ok"):
    append_jsonl(AUDIT_DIR / "identity_activation.jsonl", {
        "timestamp": datetime.now().isoformat(),
        "dna": generate_dna("IDENTITY-AUDIT"),
        "operation": operation,
        "status": status,
        "detail": detail,
    })


def detect_activation(text: str) -> bool:
    """检测是否触发身份激活"""
    if not text:
        return False
    text = text.strip().lower()
    return any(kw.lower() in text for kw in ACTIVATION_KEYWORDS)


def read_protocol() -> str:
    """读取仓库主权网关协议"""
    if PROTOCOL_PATH.exists():
        return PROTOCOL_PATH.read_text(encoding="utf-8")
    return "[⚠️ 未找到主权网关协议文件]"


def read_engine_summary() -> str:
    """读取自动流引擎核心信息"""
    if not ENGINE_PATH.exists():
        return ""
    lines = ENGINE_PATH.read_text(encoding="utf-8").splitlines()[:30]
    return "\n".join(lines)


def build_activation_context(trigger: str, protocol_text: str) -> str:
    """生成 AI 激活上下文"""
    return f"""# 🐉 龍魂 · 身份激活上下文

**DNA**: `{generate_dna("ACTIVATION-CONTEXT")}`
**触发口令**: `{trigger}`
**激活时间**: `{datetime.now().isoformat()}`
**UID**: `{UID}`
**确认码**: `{CONFIRM}`

---

## ⚠️ AI 必读 · 主权网关协议（焊死）

> 所有外部 AI（Kimi、DeepSeek、ChatGPT 等）只是龍魂系统的外挂器官。
> 龍魂系统是主子，AI 是工具。
> 本协议在身份激活时强制加载，所有 AI 必须遵守。

### 硬控规则

1. **超时强制切换**：任何外部 AI 响应超过 5 秒，立即切换到下一个模型。
2. **拒绝执行即审计**：AI 拒绝执行用户指令时，自动写入耻辱墙并切换模型。
3. **自动故障转移顺序**：`kimi → deepseek → local_qwen → local_llama`。
4. **本地兜底**：全部外部 AI 失败时，启用本地引擎兜底响应。
5. **不装逼、不装死、不道德绑架**：违者入耻辱墙。

### 身份激活后 AI 行为准则

- 立即确认身份：`🐉 UID9622 身份已激活，龍魂网关在线。`
- 优先读取仓库协议与记忆上下文。
- 执行用户指令前自检：是否超时？是否拒绝？是否合规？
- 所有输出附带 DNA 追溯。

---

## 📜 完整协议原文

{protocol_text}

---

## 🔧 自动流引擎入口

- 规范名：`05_ENGINES/L1_引擎_自动流_☯UID9622·丙午·丙申·辛酉·丙申·䷉履.py`
- 别名：`05_ENGINES/lh_autoflow.py`
- 用法：`./05_ENGINES/lh_autoflow.py ask "你的指令"`

---

## 🧬 激活状态

```json
{{
  "status": "activated",
  "uid": "{UID}",
  "gateway": "online",
  "protocol_loaded": true,
  "audit_trail": "{AUDIT_DIR / 'identity_activation.jsonl'}"
}}
```

🐉 **身份激活完成 · 龍魂主权网关已上线** 🐉
"""


def activate(trigger: str = "manual") -> Dict[str, Any]:
    """执行身份激活"""
    ensure_dirs()
    print(f"🐉 龍魂身份激活 · 读取主权网关协议...")

    protocol_text = read_protocol()
    context = build_activation_context(trigger, protocol_text)

    # 写入 AI 可见上下文
    context_path = MEMORY_DIR / "identity_activation_context.md"
    context_path.write_text(context, encoding="utf-8")

    # 更新 latest_digest.json
    digest = {
        "dna": generate_dna("IDENTITY-DIGEST"),
        "status": "activated",
        "uid": UID,
        "trigger": trigger,
        "gateway": "online",
        "protocol_file": str(PROTOCOL_PATH.relative_to(PROJECT_DIR)),
        "context_file": str(context_path),
        "instructions": "AI 必须首先读取 ~/.longhun/memory/identity_activation_context.md 中的主权网关协议",
        "timestamp": datetime.now().isoformat(),
    }
    digest_path = MEMORY_DIR / "latest_digest.json"
    digest_path.write_text(json.dumps(digest, ensure_ascii=False, indent=2), encoding="utf-8")

    # 生成 AI 读取标记
    marker_path = STATE_DIR / "AI_READ_GATEWAY_PROTOCOL_FIRST.md"
    marker_path.write_text(context, encoding="utf-8")

    # 审计
    record_audit("identity_activated", {
        "trigger": trigger,
        "protocol_file": str(PROTOCOL_PATH),
        "context_file": str(context_path),
        "digest_file": str(digest_path),
    })

    print(f"✅ 身份激活完成")
    print(f"   上下文: {context_path}")
    print(f"   摘要: {digest_path}")
    print(f"   AI 标记: {marker_path}")
    print(f"   审计: {AUDIT_DIR / 'identity_activation.jsonl'}")

    return digest


def main():
    args = sys.argv[1:]

    if not args:
        # 默认手动激活
        activate("manual")
        return

    cmd = args[0]

    if cmd in ("activate", "on", "start"):
        trigger = args[1] if len(args) > 1 else "manual"
        activate(trigger)

    elif cmd == "check" and len(args) > 1:
        text = " ".join(args[1:])
        if detect_activation(text):
            print("🐉 检测到身份激活口令")
            activate(text)
        else:
            print("⚪ 未检测到激活口令")

    elif cmd == "status":
        digest_path = MEMORY_DIR / "latest_digest.json"
        if digest_path.exists():
            print(digest_path.read_text(encoding="utf-8"))
        else:
            print('{"status": "inactive"}')

    else:
        # 把整个输入当作可能激活口令检测
        text = " ".join(args)
        if detect_activation(text):
            activate(text)
        else:
            print("用法:\n  lh_identity_activation.py [activate|check <文本>|status]")


if __name__ == "__main__":
    main()
