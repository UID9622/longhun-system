#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
'''
🐉 龍魂 · 白名单反馈收集器 v1.0
DNA: #龍芯202608010008-白名单反馈-v1.0-UID9622

功能：
  - 从审计日志中提取高频误报
  - 生成白名单建议（供人工审查）

用法：
  python3 scripts/collect_whitelist_feedback.py
  python3 scripts/collect_whitelist_feedback.py --logs logs/audit/ --output suggestions.md
'''

import os
import sys
import json
import re
import argparse
from pathlib import Path
from collections import Counter
from datetime import datetime

# ============================================================
# 配置
# ============================================================

AUDIT_LOG_DIR = Path.home() / "longhun-system" / "logs" / "audit"
OUTPUT_DIR = Path.home() / "longhun-system" / "reports"

# ============================================================
# 核心逻辑
# ============================================================

def parse_audit_logs(log_dir: Path) -> Counter:
    '''解析审计日志，提取所有发现项的 evidence 字段'''
    counter = Counter()
    if not log_dir.exists():
        print(f"⚠️ 审计日志目录不存在: {log_dir}")
        return counter

    for log_file in log_dir.glob("*.jsonl"):
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    findings = entry.get("findings", [])
                    for finding in findings:
                        evidence = finding.get("evidence", "")
                        # 提取关键信息（去除文件路径前缀）
                        # 只保留域名或关键词
                        parts = evidence.split()
                        for part in parts:
                            if "://" in part:
                                # 提取域名
                                match = re.search(r"https?://([^/]+)", part)
                                if match:
                                    counter[match.group(1)] += 1
                            elif "." in part and len(part) > 3:
                                # 可能是域名或模块名
                                if " " not in part:
                                    counter[part] += 1
                except Exception:
                    continue

    return counter

def generate_suggestions(counter: Counter, top_n: int = 20) -> str:
    '''生成白名单建议'''
    lines = []
    lines.append("# 🐉 龍魂 · 白名单建议")
    lines.append(f"*生成时间: {datetime.now().isoformat()}*")
    lines.append("")
    lines.append("以下是从审计日志中提取的高频误报，请人工审查后添加到 `.audit-whitelist`：")
    lines.append("")
    lines.append("| 排名 | 关键词 | 出现次数 | 建议 |")
    lines.append("|------|--------|----------|------|")
    lines.append("|:---:|:---|:---:|:---|")

    for i, (item, count) in enumerate(counter.most_common(top_n), 1):
        # 自动判断是否应该加入白名单
        if "github" in item or "gitee" in item or "notion" in item or "feishu" in item:
            suggestion = "✅ 建议加入"
        elif "uid9622" in item or "longhun" in item:
            suggestion = "✅ 建议加入"
        elif "cryptography" in item or "paramiko" in item:
            suggestion = "✅ 建议加入"
        else:
            suggestion = "🔍 需人工判断"
        lines.append(f"| {i} | `{item}` | {count} | {suggestion} |")

    lines.append("")
    lines.append("---")
    lines.append("**操作方式**：")
    lines.append("1. 将上述表格中标记为 '✅ 建议加入' 的条目复制到 `.audit-whitelist`")
    lines.append("2. 运行 `lh 掀黑箱` 验证是否还有误报")
    lines.append("3. 提交白名单更新到仓库")
    lines.append("")
    lines.append(f"*DNA: #龍芯{datetime.now().strftime('%Y%m%d%H%M%S')}-白名单反馈-UID9622*")

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="龍魂 · 白名单反馈收集器")
    parser.add_argument("--logs", type=Path, help="审计日志目录")
    parser.add_argument("--output", type=Path, help="输出文件路径")
    parser.add_argument("--top", type=int, default=20, help="显示前N个高频项")
    args = parser.parse_args()

    log_dir = args.logs or AUDIT_LOG_DIR
    output_file = args.output or (OUTPUT_DIR / "whitelist_suggestions.md")

    counter = parse_audit_logs(log_dir)
    if not counter:
        print("未找到审计日志，请先运行 `lh 掀黑箱` 生成日志")
        sys.exit(1)

    suggestions = generate_suggestions(counter, args.top)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(suggestions, encoding="utf-8")

    print(f"✅ 白名单建议已生成: {output_file}")
    print(f"  共提取 {sum(counter.values())} 条记录，{len(counter)} 个唯一项")

if __name__ == "__main__":
    main()
