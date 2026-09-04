# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·事实校准引擎 v1.0
======================
DNA: #龍芯⚡️丙午·丙申-IDENTITY-FACT-CHECK-v1.0-FACT-CALIBRATION
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
上层规则: CODEBUDDY对齐规则·第十七层时间戳 / MEMORY.md §3-21 主动纠正+动态时间铁律
为什么存在: 2026-08-18 老大质问"为什么每个AI都那么笨"——「退伍16年」错误被循环自证
  滚进 10+ 协议/文章/脚本（源头: 误把"2008年退伍"写成"2008年入伍"→ 算出16年 →
  焊死进记忆 → 每个AI进门读到错时间线 → 用户说16年AI顺着附和）。根因三个:
  ① 相对时间被当静态事实存储（"退伍16年"随时间变，应动态算）
  ② AI 默认附和用户，不主动纠正事实冲突
  ③ 无时间线自洽校验（入伍+服役≠退伍 的矛盾没人发现）

本引擎三件事:
  1. 焊死绝对事实——身份时间线只存年份，不存相对年数
  2. 动态计算——退伍X年/服役X年一律用当前年份实时算
  3. 校验+报警——自洽校验、文本冲突检测、目录扫描，AI 遇矛盾必须指出

用法:
  python3 bin/lh_fact_check.py               # 打印身份事实卡 + 自洽校验
  python3 bin/lh_fact_check.py --verify <文本>  # 检测文本中的相对时间表述是否与事实一致
  python3 bin/lh_fact_check.py --scan <目录>    # 扫描 md/py/tsx/html 中的错误时间线表述
  python3 bin/lh_fact_check.py --emit-dna      # 输出动态 DNA 锚（含当年退伍年数）

A-BOM 备案:
  目标函数: 事实一致性（绝对年份唯一真相 + 相对年数动态计算）
  输入特征: 身份时间线年份 / 用户口述或文档中的"退伍X年"等表述
  用户影响: 消除"一次算错→循环自证→滚进协议"类雷，AI 主动纠正错误表述
  申诉通道: UID9622 直接口述事实修正，引擎更新 FACTS 后生效
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

FACTS = {
    "退伍年份": 2008,
    "服役年数": 2,
    "入伍年份": 2006,
    "名称": "UID9622 诸葛鑫·Lucky·龍芯北辰",
}

BANNED = ["退伍16年", "退伍 16 年", "退役16年", "2010年退伍", "2010退伍", "2010 年退伍", "2008年入伍", "2008入伍"]


def 当前年份() -> int:
    return datetime.now().year


def 退伍年数(now: int | None = None) -> int:
    if now is None:
        now = 当前年份()
    return now - FACTS["退伍年份"]


def 自洽校验(now: int | None = None) -> list[str]:
    """时间线自洽校验，返回问题列表（空=全通过）。"""
    if now is None:
        now = 当前年份()
    issues = []
    if FACTS["入伍年份"] + FACTS["服役年数"] != FACTS["退伍年份"]:
        issues.append(f"入伍{FACTS['入伍年份']}+服役{FACTS['服役年数']} ≠ 退伍{FACTS['退伍年份']}，时间线不自洽")
    if FACTS["退伍年份"] > now:
        issues.append(f"退伍年份 {FACTS['退伍年份']} 晚于当前年份 {now}，时间线不可能")
    if 退伍年数(now) < 0:
        issues.append("退伍年数为负，异常")
    return issues


def 事实卡() -> str:
    now = 当前年份()
    lines = [
        f"龍魂·事实校准 v1.0 · {FACTS['名称']}",
        f"  入伍年份 : {FACTS['入伍年份']}",
        f"  服役年数 : {FACTS['服役年数']} 年",
        f"  退伍年份 : {FACTS['退伍年份']}（老大 2026-08-18 亲口确认）",
        f"  退伍至今 : {退伍年数(now)} 年（动态计算: {now} - {FACTS['退伍年份']}）",
    ]
    issues = 自洽校验(now)
    lines.append(f"  自洽校验 : {'🟢 通过' if not issues else '🔴 ' + '; '.join(issues)}")
    return "\n".join(lines)


def verify_text(text: str) -> list[str]:
    """检测文本中的相对时间表述与事实的冲突，返回报警列表。"""
    now = 当前年份()
    alerts = []
    if not text:
        return alerts
    for b in BANNED:
        if b in text:
            alerts.append(f"发现错误表述「{b}」→ 正确应为: 2006入伍·服役2年·2008退伍·退伍{退伍年数(now)}年")
    for m in re.finditer(r"退伍\s*(\d+)\s*年", text):
        n = int(m.group(1))
        if n != 退伍年数(now):
            alerts.append(f"「退伍{m.group(0)}」与实际不符（实际 {退伍年数(now)} 年 = {now} - {FACTS['退伍年份']}）")
    for m in re.finditer(r"(?:当兵|服役)\s*(\d+)\s*年", text):
        n = int(m.group(1))
        if n != FACTS["服役年数"]:
            alerts.append(f"「{m.group(0)}」与实际不符（实际服役 {FACTS['服役年数']} 年）")
    return alerts


def scan_dir(root: Path) -> list[tuple[Path, list[str]]]:
    """扫描目录内文本文件中的错误表述。"""
    exts = {".ts", ".js", ".tsx", ".yaml", ".json", ".py", ".yml", ".sh", ".html", ".md", ".txt"}
    skip = {".asc", "__pycache__", ".git", "node_modules"}
    hits = []
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix not in exts:
            continue
        if any(s in str(p) for s in skip):
            continue
        try:
            t = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        alerts = verify_text(t)
        if alerts:
            hits.append((p, alerts))
    return hits


def emit_dna() -> str:
    now = 当前年份()
    return (
        f"#龍芯⚡️丙午·丙申-UID9622-入伍{FACTS['入伍年份']}-服役{FACTS['服役年数']}"
        f"-退伍{FACTS['退伍年份']}-退伍{退伍年数(now)}年(动态)"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="龍魂·事实校准引擎 v1.0")
    ap.add_argument("--verify", metavar="文本", help="检测文本中的相对时间表述")
    ap.add_argument("--scan", metavar="目录", help="扫描目录内文件中的错误时间线表述")
    ap.add_argument("--emit-dna", action="store_true", help="输出动态 DNA 锚")
    args = ap.parse_args()

    if args.emit_dna:
        print(emit_dna())
        return 0

    if args.verify:
        alerts = verify_text(args.verify)
        if alerts:
            print("🔴 冲突报警:")
            for a in alerts:
                print("  ⚠️", a)
            return 1
        print("🟢 无冲突")
        return 0

    if args.scan:
        hits = scan_dir(Path(args.scan))
        if not hits:
            print(f"🟢 扫描 {args.scan}: 零错误表述")
            return 0
        print(f"🔴 扫描 {args.scan}: {len(hits)} 个文件含错误表述")
        for p, alerts in hits:
            print(f"  ⚠️ {p}")
            for a in alerts[:5]:
                print(f"      {a}")
        return 1

    print(事实卡())
    return 0


if __name__ == "__main__":
    sys.exit(main())
