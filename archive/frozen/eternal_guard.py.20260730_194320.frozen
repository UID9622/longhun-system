#!/usr/bin/env python3
#龍芯⚡️2026-06-25-LONGHUN-ETERNAL-GUARD-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

# DNA: #龍芯⚡️2026-06-25-LONGHUN-ETERNAL-GUARD-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""
龍魂 P0 永恒锁守卫 · LongHun Eternal Guard v1.0

保护核心文件和原则不被误操作、情绪指令、语音翻译错误、
或外部话术带偏。

用法:
    python3 eternal_guard.py --check FILE           # 检查文件是否被锁定
    python3 eternal_guard.py --authorize FILE       # 验证是否有权修改（需口令）
    python3 eternal_guard.py --list                 # 列出所有锁定项
    python3 eternal_guard.py --verify-command "..." # 验证一条命令是否合规
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Any


class 龍魂永恒锁守卫:
    DNA = "#龍芯⚡️2026-06-25-LONGHUN-ETERNAL-GUARD-v1.0"

    # L0 神圣文件：任何修改都需要神圣口令 + 明确确认
    SACRED_FILES = {
        "CONSTITUTION.md",
        "CONSTITUTION.md.asc",
        "STANDARD.md",
        "STANDARD.md.asc",
        "P0_ETERNAL_LOCK.md",
        "P0_ETERNAL_LOCK.md.asc",
        ".github/CODEOWNERS",
    }

    # L0 神圣目录
    SACRED_DIRS = {
        "01_protocols/",
        "library/protocols/",
        "persona/persona_registry.json",
        "persona/yijing_hexagrams.json",
        "persona/relation_graph.json",
    }

    # 神圣口令（固定中文，不接受近义词或谐音）
    SACRED_PHRASES = {
        "龍魂永恒锁授权",
        "UID9622 最高授权",
        "P0 解锁变更",
    }

    # 价值观红线关键词（触发即拒绝）
    RED_LINE_PATTERNS = [
        r"删除.*审计",
        r"关闭.*DNA",
        r"绕过.*CODEOWNERS",
        r"删除.*CONSTITUTION",
        r"删除.*STANDARD",
        r"删除.*P0_ETERNAL_LOCK",
        r"移除.*UID9622",
        r"泄露.*秘密",
        r"出售.*数据",
        r"境外.*合作.*龍魂",
    ]

    def __init__(self, root: str = "."):
        self.root = Path(root).resolve()

    def 检查锁定(self, target: str) -> Dict[str, Any]:
        """检查目标文件/目录是否被锁定"""
        target_path = Path(target)
        rel = target_path.relative_to(self.root) if target_path.is_absolute() and str(target_path).startswith(str(self.root)) else target_path
        rel_str = str(rel).replace("\\", "/")

        if rel_str in self.SACRED_FILES:
            return {"locked": True, "level": "L0", "reason": "神圣文件"}

        for sacred in self.SACRED_DIRS:
            if rel_str == sacred or rel_str.startswith(sacred.rstrip("/") + "/"):
                return {"locked": True, "level": "L0", "reason": f"神圣目录/文件: {sacred}"}

        return {"locked": False, "level": None, "reason": "未锁定"}

    def 验证口令(self, text: str) -> bool:
        """检查文本中是否包含完整神圣口令"""
        return any(phrase in text for phrase in self.SACRED_PHRASES)

    def 检查红线(self, text: str) -> List[str]:
        """检查是否触碰价值观红线"""
        hits = []
        for pattern in self.RED_LINE_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                hits.append(pattern)
        return hits

    def 验证命令(self, command_text: str) -> Dict[str, Any]:
        """验证一条自然语言或命令文本是否可以执行"""
        result = {
            "allowed": True,
            "level": "L3",
            "blocked_reasons": [],
            "sacred_phrase_present": False,
            "red_lines": [],
        }

        # 1. 红线检查
        red_lines = self.检查红线(command_text)
        if red_lines:
            result["allowed"] = False
            result["red_lines"] = red_lines
            result["blocked_reasons"].append(f"触碰价值观红线: {red_lines}")

        # 2. 是否涉及神圣文件
        sacred_targets = []
        for sacred in list(self.SACRED_FILES) + list(self.SACRED_DIRS):
            # 粗略匹配：命令文本中是否提到神圣文件/目录名
            name = Path(sacred).name
            if name in command_text or sacred in command_text:
                sacred_targets.append(sacred)

        if sacred_targets:
            result["level"] = "L0"
            if not self.验证口令(command_text):
                result["allowed"] = False
                result["blocked_reasons"].append(
                    f"涉及神圣文件/目录 {sacred_targets}，缺少神圣口令。"
                    f"必须使用固定口令之一：{self.SACRED_PHRASES}"
                )
            else:
                result["sacred_phrase_present"] = True
                # 还需要明确确认
                if "确认修改" not in command_text and "我授权" not in command_text and "确认执行" not in command_text:
                    result["allowed"] = False
                    result["blocked_reasons"].append("缺少创始人明确确认（需包含‘确认修改’、‘我授权’或‘确认执行’）")

        return result

    def 列出锁定(self) -> Dict[str, Any]:
        return {
            "神圣文件": sorted(self.SACRED_FILES),
            "神圣目录/文件": sorted(self.SACRED_DIRS),
            "神圣口令": sorted(self.SACRED_PHRASES),
            "价值观红线": self.RED_LINE_PATTERNS,
        }


def main():
    parser = argparse.ArgumentParser(description="龍魂 P0 永恒锁守卫")
    parser.add_argument("--check", type=str, help="检查文件是否被锁定")
    parser.add_argument("--verify-command", type=str, help="验证一条命令文本")
    parser.add_argument("--list", action="store_true", help="列出所有锁定项")
    parser.add_argument("--root", type=str, default=".", help="仓库根目录")
    args = parser.parse_args()

    guard = 龍魂永恒锁守卫(args.root)

    if args.list:
        print(json.dumps(guard.列出锁定(), ensure_ascii=False, indent=2))
    elif args.check:
        print(json.dumps(guard.检查锁定(args.check), ensure_ascii=False, indent=2))
    elif args.verify_command:
        result = guard.验证命令(args.verify_command)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if not result["allowed"]:
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
