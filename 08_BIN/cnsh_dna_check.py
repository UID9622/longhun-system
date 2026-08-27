#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH DNA 完整性校验 v1.0
DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-CNSH-DNA-CHECK-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)  ← 工程实现层

功能：
  - 递归扫描 *.cnsh 文件
  - 文件级: 头部 5 行内必须有 DNA（#龍芯⚡️）
  - 函数级: 每个「功能」定义前 5 行内必须有 DNA
  - 严格模式(--strict): DNA 必须含 UID9622 或干支四柱+卦（公式计算痕迹）
  - 生成完整性报告 + 三色判定

DNA 合法格式（两种，v∞标准兼容）：
  - 干支式: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-模块-动作-哈希8
  - 日期式: #龍芯⚡️2026-07-30-模块-v1.0
"""

import re
import json
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent

# 宽松: 任何 #龍芯⚡️ 开头
DNA_LOOSE = re.compile(r'#龍芯⚡️[^\s\n]+')
# 严格: 干支式（含·与卦符）或日期式（YYYY-MM-DD）
DNA_STRICT = re.compile(
    r'#龍芯⚡️(?:'
    r'[^\s·⚡]+·[^\s·⚡]+·[^\s·⚡]+·[^\s·⚡]+·[䷀-䷿][^\s]+'
    r'|'
    r'[0-9]{4}-[0-9]{2}-[0-9]{2}[^\s]*'
    r')'
)
FUNCTION_PATTERN = re.compile(r'^\s*功能\s+(\w+)', re.MULTILINE)


class CNSHDNAChecker:
    """CNSH DNA 完整性校验器（Bug B1/B2 已修: 类名无空格）"""

    def __init__(self, strict: bool = True):
        self.strict = strict

    def scan_files(self) -> list:
        """扫描 *.cnsh，按 AI 扫描白名单排除黑名单目录（11_DATA/_work/archive 等）"""
        BLACK = (".venv", "node_modules", "11_DATA", "_work", "dist", "models",
                 "archive", "backups", "_archive", "backup_before", "旧镜像",
                 "tombstone", "_QUARANTINE", "_private")
        return sorted(
            p for p in ROOT.rglob("*.cnsh")
            if p.is_file()
            and not any(b in p.parts for b in BLACK)
        )

    def check_file(self, filepath: Path) -> dict:
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            return {"file": str(filepath), "error": str(e), "valid": False}

        lines = content.split("\n")
        pattern = DNA_STRICT if self.strict else DNA_LOOSE
        dnas = pattern.findall(content)
        functions = FUNCTION_PATTERN.findall(content)

        header = "\n".join(lines[:5])
        has_file_dna = bool(pattern.search(header))

        # 函数级 DNA 检查（仅严格模式强制；宽松模式只查文件级）
        missing_dna = []
        if self.strict:
            for func_name in functions:
                for i, line in enumerate(lines):
                    if re.search(r'功能\s+' + func_name, line):
                        context = "\n".join(lines[max(0, i - 5):i + 1])
                        if not pattern.search(context):
                            missing_dna.append("功能 %s (line %d)" % (func_name, i + 1))
                        break

        return {
            "file":           str(filepath.relative_to(ROOT)),
            "dna_count":      len(dnas),
            "function_count": len(functions),
            "has_file_dna":   has_file_dna,
            "missing_dna":    missing_dna,
            "valid":          has_file_dna and len(missing_dna) == 0,
            "dnas":           dnas[:3],
        }

    def run(self) -> dict:
        files = self.scan_files()
        results = [self.check_file(f) for f in files]

        valid_count = sum(1 for r in results if r.get("valid"))
        invalid_count = len(results) - valid_count
        tri_color = "🟢" if invalid_count == 0 else (
            "🟡" if invalid_count <= len(results) // 5 else "🔴")

        return {
            "timestamp":     datetime.now().isoformat(),
            "dna":           "#龍芯⚡️%s-DNA-CHECK-UID9622" % datetime.now().date(),
            "total_files":   len(files),
            "valid_files":   valid_count,
            "invalid_files": invalid_count,
            "tri_color":     tri_color,
            "results":       results,
        }


if __name__ == "__main__":
    strict = "--loose" not in sys.argv
    checker = CNSHDNAChecker(strict=strict)
    report = checker.run()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("\n三色: %s | 合法: %d/%d" % (report["tri_color"],
                                        report["valid_files"],
                                        report["total_files"]))
    sys.exit(0 if report["invalid_files"] == 0 else 1)
