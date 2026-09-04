#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · 训练数据收集器
自动从本地日志、评估报告、集思广益、用户反馈目录中收集原始训练数据。
DNA: #龍芯⚡️丙午·甲午·乙亥·壬午·䷚颐-LONGHUN-FEEDBACK-COLLECTOR-v1.0
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
DATA_DIR = HOME / "longhun-system" / "data" / "training"
RAW_DIR = DATA_DIR / "raw"
LOGS = [
    HOME / "longhun-system" / "logs" / "bot_command.jsonl",
    HOME / ".longhun" / "audit" / "security.jsonl",
]
EVAL_DIR = HOME / ".longhun" / "evaluation"
FEEDBACK_DIR = HOME / "longhun-system" / "data" / "feedback"


def _今日目录() -> Path:
    日期 = datetime.now(timezone.utc).strftime("%Y%m%d")
    目录 = RAW_DIR / 日期
    目录.mkdir(parents=True, exist_ok=True)
    return 目录


def _生成DNA(来源: str, 内容摘要: str) -> str:
    种子 = f"{来源}-{内容摘要}-{datetime.now(timezone.utc).isoformat()}"
    哈希 = hashlib.sha256(种子.encode("utf-8")).hexdigest()[:8]
    日期 = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"#龍芯⚡️{日期}-{来源.upper()}-{哈希}"


def _读取jsonl(路径: Path) -> list[Any]:
    if not 路径.exists():
        return []
    结果 = []
    with 路径.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                结果.append(json.loads(line))
            except Exception:
                continue
    return 结果


def _收集机器人日志() -> list[Any]:
    条目 = []
    for 路径 in LOGS:
        for 记录 in _读取jsonl(路径):
            # 同时支持中文键名（龍智守日志）和英文键名
            内容 = 记录.get("原始消息") or 记录.get("消息内容") or 记录.get("message", "")
            if not 内容:
                continue
            时间戳 = 记录.get("时间") or 记录.get("timestamp", datetime.now(timezone.utc).isoformat())
            条目.append({
                "data_id": hashlib.sha256(f"bot-{时间戳}-{内容[:40]}".encode()).hexdigest()[:16],
                "source": "飞书机器人对话",
                "collector": "收集反馈.py",
                "timestamp": 时间戳,
                "raw_text": 内容,
                "metadata": {
                    "level": 记录.get("有效等级") or 记录.get("等级"),
                    "command": 记录.get("解析命令") or 记录.get("解析结果", {}).get("命令"),
                    "result": 记录.get("执行结果") or 记录.get("输出摘要", ""),
                },
                "dna": _生成DNA("bot", 内容[:40]),
            })
    return 条目


def _收集评估报告() -> list[Any]:
    条目 = []
    if not EVAL_DIR.exists():
        return 条目
    for 报告 in sorted(EVAL_DIR.glob("unified_evaluation_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:5]:
        内容 = 报告.read_text(encoding="utf-8")
        条目.append({
            "data_id": hashlib.sha256(f"eval-{报告.name}".encode()).hexdigest()[:16],
            "source": "系统评估报告",
            "collector": "收集反馈.py",
            "timestamp": datetime.fromtimestamp(报告.stat().st_mtime, tz=timezone.utc).isoformat(),
            "raw_text": 内容[:2000],
            "metadata": {"report_file": 报告.name},
            "dna": _生成DNA("eval", 报告.name),
        })
    return 条目


def _收集用户反馈目录() -> list[Any]:
    条目 = []
    if not FEEDBACK_DIR.exists():
        return 条目
    for 文件 in FEEDBACK_DIR.glob("*"):
        if not 文件.is_file():
            continue
        try:
            内容 = 文件.read_text(encoding="utf-8")
        except Exception:
            continue
        条目.append({
            "data_id": hashlib.sha256(f"fb-{文件.name}".encode()).hexdigest()[:16],
            "source": "用户直接反馈",
            "collector": "收集反馈.py",
            "timestamp": datetime.fromtimestamp(文件.stat().st_mtime, tz=timezone.utc).isoformat(),
            "raw_text": 内容,
            "metadata": {"filename": 文件.name},
            "dna": _生成DNA("fb", 文件.name),
        })
    return 条目


def main():
    今日目录 = _今日目录()
    输出路径 = 今日目录 / "raw.jsonl"

    所有数据 = []
    所有数据.extend(_收集机器人日志())
    所有数据.extend(_收集评估报告())
    所有数据.extend(_收集用户反馈目录())

    with 输出路径.open("w", encoding="utf-8") as f:
        for 数据 in 所有数据:
            f.write(json.dumps(数据, ensure_ascii=False) + "\n")

    print(f"🟢 共收集 {len(所有数据)} 条原始训练数据")
    print(f"   输出: {输出路径}")
    print(f"   DNA: #龍芯⚡️丙午·甲午·乙亥·壬午·䷚颐-LONGHUN-FEEDBACK-COLLECTOR-v1.0")


if __name__ == "__main__":
    main()
