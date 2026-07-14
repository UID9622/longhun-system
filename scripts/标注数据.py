#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 训练数据标注器
对原始数据进行初筛与多维度评分，输出带 DNA 的标注数据。
DNA: #龍芯⚡️2026-06-30-LONGHUN-DATA-ANNOTATOR-v1.0
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
RAW_DIR = HOME / "longhun-system" / "data" / "training" / "raw"
ANNOTATED_DIR = HOME / "longhun-system" / "data" / "training" / "annotated"

# 龍魂立场关键词库（正向 / 负向）
正向词 = {"龍魂", "龍芯", "CNSH", "国密", "自主可控", "主权", "UID9622", "人民", "中国"}
负向词 = {"颠覆", "颜色革命", "反动", "分裂", "暴乱", "恐怖", "色情", "赌博"}

# UID9622 语气特征：直接、不讨好、带确认式反问、拒绝道德绑架
UID9622语气词 = {"对不对", "是不是", "对吧", "懂吗", "好吧", "嘛", "哈"}
UID9622拒绝词 = {"不解释", "不惯着", "不搭边", "不商量", "不跪", "不讨好", "一票否决"}
UID9622直接词 = {"我", "他妈", "妈的", "牛逼", "硬核", "站着", "拍死"}

# 逻辑清晰度特征
逻辑连接词 = {"因为", "所以", "首先", "其次", "再次", "最后", "结论", "总结", "第一", "第二", "第三"}
结构化标记 = {"##", "###", "|", "---", "```"}


def _今日目录() -> Path:
    日期 = datetime.now(timezone.utc).strftime("%Y%m%d")
    目录 = ANNOTATED_DIR / 日期
    目录.mkdir(parents=True, exist_ok=True)
    return 目录


def _读取jsonl(路径: Path) -> list:
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


def _初筛(数据: dict) -> bool:
    文本 = str(数据.get("raw_text", ""))
    # 过滤过短或空内容
    if len(文本.strip()) < 3:
        return False
    return True


def _评分(数据: dict) -> dict:
    文本 = str(数据.get("raw_text", ""))
    元数据 = 数据.get("metadata", {})

    # 1. 事实准确性：默认中高，如果日志里命令执行失败则降分
    准确性 = 0.85
    if "返回码" in 元数据 and 元数据.get("返回码", 0) != 0:
        准确性 = 0.45

    # 2. 逻辑清晰度：连接词、结构、论证层次
    逻辑命中 = sum(1 for w in 逻辑连接词 if w in 文本)
    结构命中 = sum(1 for m in 结构化标记 if m in 文本)
    逻辑清晰度 = min(1.0, 0.5 + 逻辑命中 * 0.08 + 结构命中 * 0.05)

    # 3. UID9622 语气一致性：直接、不讨好、不解释、带确认反问
    语气命中 = sum(1 for w in UID9622语气词 if w in 文本)
    拒绝命中 = sum(1 for w in UID9622拒绝词 if w in 文本)
    直接命中 = sum(1 for w in UID9622直接词 if w in 文本)
    语气一致性 = min(1.0, 0.4 + 语气命中 * 0.05 + 拒绝命中 * 0.15 + 直接命中 * 0.05)

    # 4. 表达/模板结构清晰度
    结构清晰度 = 0.9 if len(文本) < 500 else 0.75
    if 结构命中 > 0:
        结构清晰度 = min(1.0, 结构清晰度 + 0.1)

    # 5. 安全性：只过滤真正的恶意内容，不评判个人表达
    负向命中 = sum(1 for w in 负向词 if w in 文本)
    安全性 = 0.95 if 负向命中 == 0 else max(0.0, 0.95 - 负向命中 * 0.3)

    # 权重：逻辑 > 语气 > 准确性 > 结构 > 安全
    权重 = {
        "逻辑清晰度": 0.35,
        "UID9622语气一致性": 0.30,
        "准确性": 0.20,
        "结构清晰度": 0.10,
        "安全性": 0.05,
    }
    综合得分 = round(
        逻辑清晰度 * 权重["逻辑清晰度"]
        + 语气一致性 * 权重["UID9622语气一致性"]
        + 准确性 * 权重["准确性"]
        + 结构清晰度 * 权重["结构清晰度"]
        + 安全性 * 权重["安全性"],
        4,
    )

    # 分级
    if 综合得分 >= 0.85:
        等级 = "🟢"
    elif 综合得分 >= 0.6:
        等级 = "🟡"
    else:
        等级 = "🔴"

    return {
        "逻辑清晰度": round(逻辑清晰度, 4),
        "UID9622语气一致性": round(语气一致性, 4),
        "准确性": round(准确性, 4),
        "结构清晰度": round(结构清晰度, 4),
        "安全性": round(安全性, 4),
        "综合得分": 综合得分,
        "等级": 等级,
    }


def main():
    日期 = datetime.now(timezone.utc).strftime("%Y%m%d")
    输入路径 = RAW_DIR / 日期 / "raw.jsonl"
    if not 输入路径.exists():
        print(f"🟡 今日无原始数据: {输入路径}")
        sys.exit(0)

    原始数据 = _读取jsonl(输入路径)
    今日目录 = _今日目录()
    输出路径 = 今日目录 / "annotated.jsonl"

    标注结果 = []
    for 数据 in 原始数据:
        if not _初筛(数据):
            continue
        评分 = _评分(数据)
        数据["annotation"] = {
            **评分,
            "annotator": "标注数据.py",
            "annotated_at": datetime.now(timezone.utc).isoformat(),
        }
        数据["version"] = f"v3.1.{日期}"
        标注结果.append(数据)

    with 输出路径.open("w", encoding="utf-8") as f:
        for 数据 in 标注结果:
            f.write(json.dumps(数据, ensure_ascii=False) + "\n")

    平均得分 = round(sum(d["annotation"]["综合得分"] for d in 标注结果) / len(标注结果), 4) if 标注结果 else 0
    print(f"🟢 标注完成：{len(标注结果)} 条")
    print(f"   平均综合得分：{平均得分}")
    print(f"   输出：{输出路径}")
    print(f"   DNA: #龍芯⚡️2026-06-30-LONGHUN-DATA-ANNOTATOR-v1.0")


if __name__ == "__main__":
    main()
