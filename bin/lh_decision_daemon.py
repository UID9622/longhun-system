#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙申·甲寅·庚午·大壮-DECISION-DAEMON-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 来源: 龍魂/核心/龍魂守护进程.py → 吸收对齐后嵌入 longhun-system
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 路径标准化·DNA嵌入完成

"""
龍魂守护进程 — 决策卡片自动生成钩子 v1.0
==========================================

行为规则：
  1) 模块目录出现新文件时分流
  2) ☯龍🧬_xxx.cnsh → 🟢 允许执行 + 生成决策卡片
  3) xxx.cnsh（无前缀）→ 🟡 仅记录 + 生成决策卡片（建议补前缀）
  4) 非 .cnsh → 🔴 只记录风险，不执行，不生成卡片
  5) 只新增，不覆盖

对齐说明：
  - 路径从硬编码 /Users/zuimeidedeyihan/龍魂 → 统一使用基于项目根的标准路径
  - 守护进程路径: longhun-system/bin/lh_decision_daemon.py
  - 决策卡片输出: longhun-system/logs/decision_cards/
  - 模块目录: longhun-system/04_決策日誌/modules/
  - 日志: longhun-system/logs/decision_daemon.log
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import argparse
import os
import sys
import time
import unicodedata

# 确保项目根在 Python path 中
_项目根 = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_项目根))

from bin.lh_decision_tracer import 决策追溯引擎, 决策事件


# ── 路径配置（基于 longhun-system 标准目录结构）──
根目录 = _项目根
日志目录 = 根目录 / "logs"
决策卡目录 = 根目录 / "04_決策日誌" / "decision_cards"
模块目录 = 根目录 / "04_決策日誌" / "modules"
日志文件 = 日志目录 / "decision_daemon.log"


def 写日志(内容: str) -> None:
    日志目录.mkdir(parents=True, exist_ok=True)
    时间戳 = datetime.now().isoformat(timespec="seconds")
    with 日志文件.open("a", encoding="utf-8") as f:
        f.write(f"[{时间戳}] {内容}\n")


def 归一文件名(name: str) -> str:
    return unicodedata.normalize("NFKC", name).strip()


def 判断分类(path: Path) -> str:
    """🟢绿=标准前缀 / 🟡黄=缺前缀 / 🔴红=非cnsh"""
    name = 归一文件名(path.name)
    lower = name.lower()
    if not lower.endswith(".cnsh"):
        return "红"

    前缀候选 = (
        "☯龍🧬_",
        "☯龍🧬",
        "龍🧬_",
        "龍🧬_",
    )
    if any(name.startswith(p) for p in 前缀候选):
        return "绿"
    return "黄"


def 构造事件(path: Path, 分类: str) -> 决策事件:
    if 分类 == "绿":
        return 决策事件(
            执行文件=path.name,
            触发原因="检测到标准前缀 ☯龍🧬 且后缀为 .cnsh，允许执行并留痕。",
            审计颜色="🟢",
            三才天="命中规则：标准文件命名与 .cnsh 执行规则。",
            三才地=f"输入来源：{path}",
            三才人="执行动作：允许进入执行链并生成决策卡片。",
            风险说明="低风险：命名规范，格式符合。",
            下一步动作="继续执行该 .cnsh，并保持审计链追加。",
        )
    if 分类 == "黄":
        return 决策事件(
            执行文件=path.name,
            触发原因="检测到 .cnsh 但缺少 ☯龍🧬 前缀，记录并建议修正命名。",
            审计颜色="🟡",
            三才天="命中规则：.cnsh 可记录，前缀不规范需提醒。",
            三才地=f"输入来源：{path}",
            三才人="执行动作：记录事件并生成决策卡片，不阻断。",
            风险说明="中风险：命名不规范可能导致后续路由歧义。",
            下一步动作="建议改名为 ☯龍🧬_*.cnsh 后再纳入标准执行流。",
        )
    raise ValueError("红色事件不生成决策卡片")


def 处理文件(path: Path, 引擎: 决策追溯引擎) -> None:
    分类 = 判断分类(path)

    if 分类 == "红":
        写日志(f"🔴 非 .cnsh 文件：{path.name} | 不执行，只记录风险")
        return

    事件 = 构造事件(path, 分类)
    卡片路径 = 引擎.生成决策卡片(事件)
    写日志(f"{事件.审计颜色} 文件处理：{path.name}")
    写日志(f"已生成决策卡片：{卡片路径}")


def 单次扫描(引擎: 决策追溯引擎, 已处理集合: set[str]) -> None:
    模块目录.mkdir(parents=True, exist_ok=True)
    for path in sorted(模块目录.iterdir()):
        if not path.is_file():
            continue
        文件标识 = f"{path.name}|{int(path.stat().st_mtime)}|{path.stat().st_size}"
        if 文件标识 in 已处理集合:
            continue
        处理文件(path, 引擎)
        已处理集合.add(文件标识)


def main() -> None:
    parser = argparse.ArgumentParser(description="龍魂守护进程：决策卡片自动钩子")
    parser.add_argument("--once", action="store_true", help="只扫描一次后退出")
    parser.add_argument("--interval", type=int, default=2, help="循环扫描秒数，预设2秒")
    args = parser.parse_args()

    引擎 = 决策追溯引擎(决策卡目录)
    已处理集合: set[str] = set()
    写日志("守护进程启动：决策卡片自动生成钩子已激活")

    if args.once:
        单次扫描(引擎, 已处理集合)
        写日志("守护进程退出：单次扫描完成")
        return

    while True:
        单次扫描(引擎, 已处理集合)
        time.sleep(max(1, args.interval))


if __name__ == "__main__":
    main()
