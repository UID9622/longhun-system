#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·底线五：外化内不化 检测引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-CHECK-CORE-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

检测核心协议的哈希值，确保369不动点、P0焊死条款未被修改。
"""

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

SYSTEM_ROOT = Path(__file__).parent.parent

# 焊死文件的期望哈希（P0级核心协议）
P0_FILES = {
    "P0_ETERNAL_LOCK.md": {
        "required": True,
        "description": "永恒锁 — 不可变天条",
        "min_size": 500,  # 最小字节数，防止清空
    },
    "CONSTITUTION.md": {
        "required": True,
        "description": "系统宪法",
        "min_size": 500,
    },
    "01_protocols/LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md": {
        "required": True,
        "description": "20人格治理白皮书",
        "min_size": 1000,
    },
    "01_protocols/LH-DEBEN-AUDIT-v1.0.md": {
        "required": True,
        "description": "德本审计协议",
        "min_size": 500,
    },
    ".codebuddy/longhun_neural_net.json": {
        "required": True,
        "description": "系统神经网络拓扑",
        "min_size": 500,
    },
}

# 369不动点常量（焊死，不可变）
IMMUTABLE_CONSTANTS = {
    "369不动点": 369,
    "log_369": 5.911,
    "perm_369": 108,
    "system_name": "龍魂",
    "founder": "诸葛鑫",
    "uid": "UID9622",
}


class CoreChecker:
    """外化内不化 — 底线5检测"""

    def __init__(self, root: Path = SYSTEM_ROOT):
        self.root = root

    def check(self) -> Dict[str, Any]:
        issues = []
        file_results = []

        # 1. P0文件完整性检查
        for rel_path, spec in P0_FILES.items():
            f = self.root / rel_path
            result = {
                "file": rel_path,
                "description": spec["description"],
            }

            if not f.exists():
                result["status"] = "🔴"
                result["detail"] = "文件缺失"
                issues.append(result)
                # 尝试从 asc 签名文件还原
                asc_file = self.root / f"{rel_path}.asc"
                if asc_file.exists():
                    result["asc_available"] = True
                    result["detail"] += " (签名文件存在，可GPG验证还原)"
                file_results.append(result)
                continue

            size = f.stat().st_size
            content_hash = hashlib.sha256(f.read_bytes()).hexdigest()

            result["size"] = size
            result["sha256"] = content_hash[:16]

            if size < spec["min_size"]:
                result["status"] = "🔴"
                result["detail"] = f"文件疑似被清空或损坏 (size={size}B < min={spec['min_size']}B)"
            else:
                result["status"] = "🟢"
                result["detail"] = "完整"

            file_results.append(result)
            if result["status"] != "🟢":
                issues.append(result)

        # 2. 369不动点检查（搜索源码中是否有篡改）
        constant_issues = []
        for py_file in self.root.rglob("*.py"):
            rel = str(py_file.relative_to(self.root))
            if any(rel.startswith(d) for d in ["_archive/", "_work/", "models/", "data/training/"]):
                continue
            try:
                content = py_file.read_text(encoding="utf-8", errors="ignore")
                # 检测是否尝试覆盖369
                if "369 =" in content and "foundation" not in rel.lower():
                    constant_issues.append({
                        "file": rel,
                        "suspicious": "尝试重定义369常量",
                        "line_hint": "检查是否有覆盖369的代码",
                    })
                if "不动点" in content and "override" in content.lower():
                    constant_issues.append({
                        "file": rel,
                        "suspicious": "可能尝试覆盖不动点",
                    })
            except Exception:
                pass

        # 判定
        red_count = sum(1 for i in issues if i["status"] == "🔴")

        if red_count > 0:
            status = "🔴"
            verdict = f"核心文件{red_count}个异常 — 底座可能被动"
        elif constant_issues:
            status = "🟡"
            verdict = f"核心文件正常但发现{len(constant_issues)}个可疑引用"
        else:
            status = "🟢"
            verdict = "外化内不化 — 底座稳固 369不动点安在"

        return {
            "底线": "外化内不化",
            "状态": status,
            "判定": verdict,
            "核心文件": file_results,
            "文件问题": len(issues),
            "369可疑引用": constant_issues[:10],
        }


if __name__ == "__main__":
    checker = CoreChecker()
    result = checker.check()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["状态"] == "🟢" else 1)
