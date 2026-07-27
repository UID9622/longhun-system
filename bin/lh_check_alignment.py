#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·底线二：路径对齐 检测引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-CHECK-ALIGNMENT-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

扫描全项目，检测同名文件是否出现在不同路径，防止混乱和自毁。
"""

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

SYSTEM_ROOT = Path(__file__).parent.parent

# 同名不同路径是允许的关键目录（同一文件的合法别名或符号链接）
WHITELIST_PAIRS = {
    ("engines/lh_team_orchestrator.py", "engines/collaboration/lh_team_orchestrator.py"),
}

FORBIDDEN_DIRS = [
    "~/Downloads/", "~/Desktop/", "~/tmp/", "/tmp/",
]


class AlignmentChecker:
    """路径对齐 — 底线2检测"""

    def __init__(self, root: Path = SYSTEM_ROOT):
        self.root = root

    def check(self) -> Dict[str, Any]:
        # 1. 同名不同路径检测
        name_to_paths: Dict[str, List[str]] = defaultdict(list)
        exts = {".py", ".md", ".sh", ".js", ".html", ".json", ".cnsh"}

        for f in self.root.rglob("*"):
            if f.is_file() and f.suffix in exts:
                rel = str(f.relative_to(self.root))
                name_to_paths[f.name].append(rel)

        duplicates = []
        for name, paths in name_to_paths.items():
            if len(paths) > 1:
                # 排除白名单
                non_whitelist = [
                    (a, b) for i, a in enumerate(paths)
                    for b in paths[i+1:]
                    if (a, b) not in WHITELIST_PAIRS and (b, a) not in WHITELIST_PAIRS
                ]
                if non_whitelist:
                    duplicates.append({
                        "name": name,
                        "paths": paths,
                        "count": len(paths),
                    })

        # 2. 禁止目录检测
        forbidden = []
        for f in self.root.rglob("*"):
            if f.is_file():
                abs_path = str(f)
                for fdir in FORBIDDEN_DIRS:
                    exp = Path(fdir).expanduser()
                    if str(exp) in abs_path:
                        forbidden.append({
                            "file": str(f.relative_to(self.root)),
                            "forbidden_in": fdir,
                        })

        # 3. 产出路径合规检测
        path_violations = []
        expected_dirs = {
            "01_protocols/": ["协议", "规范", "规则"],
            "bin/": ["脚本", "CLI", "工具"],
            "web/": ["前端", "HTML", "JS"],
            "portal/": ["门户", "仪表盘"],
            "engines/": ["引擎", "核心"],
            "deploy/": ["部署"],
            "data/": ["数据"],
            "logs/": ["日志"],
            "models/": ["模型"],
        }

        # 判定
        dup_count = len(duplicates)
        forb_count = len(forbidden)

        if forb_count > 0:
            status = "🔴"
            verdict = f"发现{forb_count}个文件位于禁止目录"
        elif dup_count > 3:
            status = "🟡"
            verdict = f"发现{dup_count}组同名不同路径 — 建议清理"
        elif dup_count > 0:
            status = "🟡"
            verdict = f"发现{dup_count}组同名不同路径 — 已排除白名单"
        else:
            status = "🟢"
            verdict = "路径对齐 — 通过"

        return {
            "底线": "路径对齐",
            "状态": status,
            "判定": verdict,
            "同名冲突": dup_count,
            "禁止目录": forb_count,
            "同名详情": duplicates[:10],
            "禁止详情": forbidden[:10],
        }


if __name__ == "__main__":
    checker = AlignmentChecker()
    result = checker.check()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["状态"] == "🟢" else 1)
