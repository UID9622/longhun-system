#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂三色审计快速检查工具
DNA: #龍芯⚡️2026-05-23-AUDIT-CHECK-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: UID9622 诸葛鑫

用法:
    python audit_check.py <文件路径>
    python audit_check.py --content "要审计的内容"
    echo "内容" | python audit_check.py --stdin
"""

import sys
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

# ============ 三色常量 ============
COLOR_GREEN = "🟢"
COLOR_YELLOW = "🟡"
COLOR_RED = "🔴"

# ============ dr 阈值 ============
# TODO: 从「三色审计判定参数·写死阈值」源页 fetch 后填真值
THRESHOLDS = {
    "green_drs": [3, 6, 9],   # 木·生长·通过
    "yellow_drs": [2, 5, 8],  # 土·待定·警示
    "red_drs": [1, 4, 7],     # 火·爆发·熔断
}


def digital_root(n: int) -> int:
    """数字根：各位数字求和直到变成一位数"""
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


def compute_content_dr(content: str) -> int:
    """内容 dr：SHA256 取位求和回到 1-9"""
    h = hashlib.sha256(content.encode()).hexdigest()
    total = sum(int(c, 16) for c in h)
    return digital_root(total)


def forge_dna(module: str = "AUDIT-CHECK", version: str = "v1.0") -> str:
    """生成 DNA 戳"""
    now = datetime.now(ZoneInfo("Asia/Shanghai"))
    h = hashlib.sha256(f"{module}{now}".encode()).hexdigest()[:6].upper()
    return f"#龍芯⚡️{now.strftime('%Y-%m-%d')}-{module}-{version}-{h}"


def classify_dr(dr: int) -> tuple:
    """根据 dr 值返回 (颜色, 动作, 理由)"""
    if dr in THRESHOLDS["green_drs"]:
        return (COLOR_GREEN, "放行", f"dr={dr}·木态·生长·安全")
    elif dr in THRESHOLDS["yellow_drs"]:
        return (COLOR_YELLOW, "警示", f"dr={dr}·土态·待定·需复核")
    elif dr in THRESHOLDS["red_drs"]:
        return (COLOR_RED, "熔断", f"dr={dr}·火态·爆发·阻断")
    else:
        return (COLOR_YELLOW, "警示", f"dr={dr}·未知态·需人工判定")


def audit_content(content: str, source: str = "stdin") -> dict:
    """审计内容，返回结果字典"""
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    dr = compute_content_dr(content)
    color, action, reasoning = classify_dr(dr)
    dna = forge_dna("AUDIT-CHECK")

    return {
        "color": color,
        "dr_value": dr,
        "content_hash": content_hash[:8],
        "content_length": len(content),
        "source": source,
        "reasoning": reasoning,
        "action": action,
        "dna_trace": dna,
        "timestamp": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(),
    }


def audit_file(filepath: str) -> dict:
    """审计文件"""
    path = Path(filepath)
    if not path.exists():
        return {"error": f"文件不存在: {filepath}"}

    content = path.read_text(encoding="utf-8", errors="ignore")
    return audit_content(content, source=str(path))


def print_result(result: dict):
    """打印审计结果"""
    if "error" in result:
        print(f"{COLOR_RED} 错误: {result['error']}")
        return 1

    print(f"""
{'='*50}
龍魂三色审计结果
{'='*50}
颜色: {result['color']}
dr值: {result['dr_value']}
动作: {result['action']}
理由: {result['reasoning']}
{'='*50}
来源: {result['source']}
哈希: {result['content_hash']}...
长度: {result['content_length']} 字符
DNA:  {result['dna_trace']}
时间: {result['timestamp']}
{'='*50}
""")

    # 返回退出码：绿=0, 黄=1, 红=2
    if result['color'] == COLOR_GREEN:
        return 0
    elif result['color'] == COLOR_YELLOW:
        return 1
    else:
        return 2


def write_log(result: dict, log_path: Optional[str] = None):
    """写入审计日志"""
    if log_path is None:
        log_path = Path.home() / "longhun-system" / "logs" / "audit_check.jsonl"
    else:
        log_path = Path(log_path)

    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="龍魂三色审计快速检查")
    parser.add_argument("file", nargs="?", help="要审计的文件路径")
    parser.add_argument("--content", "-c", help="直接审计内容字符串")
    parser.add_argument("--stdin", action="store_true", help="从 stdin 读取内容")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--log", help="日志文件路径（默认: ~/longhun-system/logs/audit_check.jsonl）")
    parser.add_argument("--no-log", action="store_true", help="不写日志")

    args = parser.parse_args()

    # 获取要审计的内容
    if args.content:
        result = audit_content(args.content, source="--content")
    elif args.stdin or not sys.stdin.isatty():
        content = sys.stdin.read()
        result = audit_content(content, source="stdin")
    elif args.file:
        result = audit_file(args.file)
    else:
        parser.print_help()
        sys.exit(1)

    # 输出结果
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        exit_code = 0 if result['color'] == COLOR_GREEN else (1 if result['color'] == COLOR_YELLOW else 2)
    else:
        exit_code = print_result(result)

    # 写日志
    if not args.no_log and "error" not in result:
        write_log(result, args.log)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
