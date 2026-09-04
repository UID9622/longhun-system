#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🛡️ 龍魂·轻量代码审计扫描器 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷔噬-CODE-AUDIT-v1.0

为 lh.py 交互菜单提供安全的文件级代码审计能力，
不经过 shell 拼接，直接接收 pathlib 路径。
"""

import json
import re
from pathlib import Path

# 高危模式：按行扫描即可发现的安全隐患
RISK_PATTERNS = [
    (r"os\.system\s*\(", "调用 os.system（存在命令注入风险）"),
    (r"subprocess\.\w+\s*\([^)]*shell\s*=\s*True", "subprocess shell=True（存在命令注入风险）"),
    (r"eval\s*\(", "eval 动态执行（存在代码注入风险）"),
    (r"exec\s*\(", "exec 动态执行（存在代码注入风险）"),
    (r"__import__\s*\(", "动态导入（需审查是否被滥用）"),
    (r"compile\s*\(", "compile 动态编译（需审查）"),
    (r"pickle\.loads?\s*\(", "pickle 反序列化（存在任意代码执行风险）"),
    (r"yaml\.load\s*\([^)]*Loader\s*=\s*yaml\.Loader", "yaml.load 使用不安全 Loader"),
]


def scan(path: str) -> dict:
    """扫描指定 Python 文件，返回审计结果字典并打印 JSON。"""
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = Path.cwd() / p
    p = p.resolve()

    result = {
        "path": str(p),
        "exists": False,
        "readable": False,
        "issues": [],
        "issue_count": 0,
        "status": "通过",
    }

    if not p.exists():
        result["status"] = "错误"
        result["error"] = f"路径不存在: {p}"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result

    result["exists"] = True

    if p.suffix.lower() != ".py":
        result["status"] = "跳过"
        result["error"] = "仅支持审计 .py 文件"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result

    try:
        source = p.read_text(encoding="utf-8", errors="ignore")
        result["readable"] = True
    except Exception as e:
        result["status"] = "错误"
        result["error"] = f"读取文件失败: {e}"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result

    for lineno, line in enumerate(source.splitlines(), 1):
        for pattern, desc in RISK_PATTERNS:
            if re.search(pattern, line):
                result["issues"].append({
                    "line": lineno,
                    "description": desc,
                    "snippet": line.strip()[:120],
                })

    result["issue_count"] = len(result["issues"])
    if result["issue_count"]:
        result["status"] = "需审查"

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="龍魂·轻量代码审计扫描器")
    parser.add_argument("--path", "-p", type=str, required=True, help="要审计的 Python 文件路径")
    args = parser.parse_args()
    scan(args.path)
