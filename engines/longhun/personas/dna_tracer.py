#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# DNA: #龍芯⚡️2026-06-24-LONGHUN-DNA-TRACER-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""
龍魂 DNA 追本溯源器 · LongHun DNA Tracer v1.0

功能:
- 扫描指定目录下的 DNA 追溯码
- 根据 DNA 码查找相关文件与操作链
- 显示某个模块/关键词的完整溯源路径

用法:
    python3 dna_tracer.py --scan persona/
    python3 dna_tracer.py --query "LONGHUN-PERSONA-HUB"
    python3 dna_tracer.py --query "#龍芯⚡️2026-06-24"
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any


class 龍魂DNA追溯器:
    DNA = "#龍芯⚡️2026-06-24-LONGHUN-DNA-TRACER-v1.0"

    # DNA 码格式: #龍芯⚡️<时间戳>-<操作类型>[-v<版本>][-<哈希>]
    # 时间戳可能是 2026-06-24 或 20260624130125
    DNA_PATTERN = re.compile(
        r"#龍芯⚡️(?P<timestamp>\d{4}(?:-\d{2}){2}|\d{14,})-(?P<type>[A-Z0-9_]+(?:-[A-Z0-9_]+)*)(?:-v(?P<version>\d+\.\d+))?(?:-(?P<hash>[A-Fa-f0-9]{4,}))?",
        re.UNICODE,
    )

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.results: List[Dict] = []

    def 扫描(self, target_dir: Optional[str] = None, glob: str = "**/*", max_size_mb: float = 10.0) -> List[Dict]:
        """扫描目录中的 DNA 码（跳过超大/二进制文件）"""
        scan_dir = Path(target_dir) if target_dir else self.base_dir
        max_bytes = int(max_size_mb * 1024 * 1024)
        findings = []
        for path in scan_dir.glob(glob):
            if not path.is_file():
                continue
            try:
                if path.stat().st_size > max_bytes:
                    continue
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for lineno, line in enumerate(text.splitlines(), 1):
                for match in self.DNA_PATTERN.finditer(line):
                    findings.append({
                        "file": str(path.relative_to(scan_dir)),
                        "line": lineno,
                        "dna": match.group(0),
                        "type": match.group("type") or "unknown",
                        "timestamp": match.group("timestamp") or "",
                        "version": match.group("version") or "",
                        "hash": match.group("hash") or "",
                        "context": line.strip()[:200],
                    })
        self.results = findings
        return findings

    def 查询(self, keyword: str, target_dir: Optional[str] = None, glob: str = "**/*") -> List[Dict]:
        """根据关键词查询 DNA 和相关上下文"""
        findings = self.扫描(target_dir, glob)
        keyword_lower = keyword.lower()
        matched = []
        for item in findings:
            if keyword_lower in item["dna"].lower() or keyword_lower in item["type"].lower():
                matched.append(item)
        return matched

    def 模块溯源(self, module_name: str, target_dir: Optional[str] = None) -> Dict[str, Any]:
        """追溯某个模块的所有 DNA 记录（支持模块名、文件名、关键词）"""
        scan_dir = Path(target_dir) if target_dir else self.base_dir
        findings = self.扫描(scan_dir)
        module_map = {}
        map_path = scan_dir / "module_map.json"
        if map_path.exists():
            try:
                module_map = json.loads(map_path.read_text(encoding="utf-8")).get("modules", {})
            except Exception:
                pass

        # 收集该模块关联的关键词
        keywords = {module_name.lower()}
        info = module_map.get(module_name, {})
        keywords.add(info.get("file", "").lower())
        keywords.update(k.lower() for k in info.get("keywords", []))
        keywords.discard("")

        matched = []
        for item in findings:
            hay = f"{item['file']} {item['dna']} {item['type']} {item['context']}".lower()
            if any(k in hay for k in keywords):
                matched.append(item)

        # 按时间排序
        matched.sort(key=lambda x: x.get("timestamp", ""))
        return {
            "DNA": self.DNA,
            "模块": module_name,
            "记录数": len(matched),
            "时间范围": {
                "最早": matched[0]["timestamp"] if matched else "",
                "最晚": matched[-1]["timestamp"] if matched else "",
            },
            "溯源链": matched,
        }

    def 链路图(self, keyword: str, target_dir: Optional[str] = None) -> str:
        """生成 Mermaid 溯源图"""
        matched = self.查询(keyword, target_dir)
        if not matched:
            return "未找到相关 DNA 记录"
        lines = ["graph TD"]
        prev = None
        for i, item in enumerate(matched):
            node = f"D{i}[{item['type']}<br/>{item['file']}:{item['line']}]"
            lines.append(f"    {node}")
            if prev:
                lines.append(f"    {prev} --> {node}")
            prev = node
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="龍魂 DNA 追本溯源器")
    parser.add_argument("--scan", "-s", type=str, help="扫描目录")
    parser.add_argument("--query", "-q", type=str, help="查询关键词/DNA前缀")
    parser.add_argument("--module", "-m", type=str, help="模块溯源")
    parser.add_argument("--graph", "-g", action="store_true", help="输出 Mermaid 链路图")
    parser.add_argument("--base", "-b", type=str, default=".", help="基准目录")
    args = parser.parse_args()

    tracer = 龍魂DNA追溯器(args.base)

    if args.scan:
        results = tracer.扫描(args.scan)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.query:
        results = tracer.查询(args.query)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif args.module:
        result = tracer.模块溯源(args.module)
        if args.graph:
            print(tracer.链路图(args.module))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("用法: python3 dna_tracer.py --scan <dir> | --query <keyword> | --module <name>")


if __name__ == "__main__":
    main()
