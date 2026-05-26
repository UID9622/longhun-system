#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂批量签名系统 · 自动DNA/三色/GPG签名流水线
DNA: #龍芯⚡️2026-05-26-batch-sign-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
UID: 9622 · 诸葛鑫
理论指导: 曾仕强老师·永恒显示
献礼: 龍魂系统·中华文化传承

【公式】
数字根 dr = 1 + ((N - 1) mod 9), where N = Σ ord(char_i)
三色判定: dr∈{1,2}→🟢 | dr∈{3,4,5,6}→🟡 | dr∈{7,8,9}→🔴
"""

import os
import sys
import json
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime

def digital_root(n):
    """递归数字根：Σ digits → 单个digit"""
    return 1 + ((n - 1) % 9) if n > 0 else 0

def get_file_color(dr):
    """dr → 三色"""
    if dr in [1, 2]:
        return "🟢"
    elif dr in [3, 4, 5, 6]:
        return "🟡"
    else:
        return "🔴"

def compute_dna_color(filepath):
    """
    计算文件的DNA签名（数字根 + 三色）
    返回: (dr, color, file_hash)
    """
    with open(filepath, 'rb') as f:
        content = f.read()

    # 字节和 → 数字根
    byte_sum = sum(content)
    dr = digital_root(byte_sum)
    color = get_file_color(dr)

    # SHA256文件哈希
    file_hash = hashlib.sha256(content).hexdigest()[:8]

    return dr, color, file_hash

def gpg_sign_file(filepath, gpg_key_id="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"):
    """
    用GPG签名文件，生成 .sig
    返回: (success, sig_filepath, error_msg)
    """
    sig_path = f"{filepath}.sig"
    try:
        result = subprocess.run(
            ["gpg", "--default-key", gpg_key_id, "--output", sig_path, "--detach-sign", filepath],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, sig_path, None
        else:
            return False, None, result.stderr
    except Exception as e:
        return False, None, str(e)

def batch_sign_directory(root_dir="~/longhun-system", gpg_key_id="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"):
    """
    批量扫描 + 签名 + 审计日志
    返回: (files_processed, audit_records)
    """
    root_path = Path(root_dir).expanduser()
    audit_records = []

    # 排除目录：.venv, node_modules, .git等
    exclude_dirs = {'.venv', 'node_modules', '.git', '__pycache__', '.pytest_cache',
                    '.vscode', 'dist', 'build', '.idea', 'venv', 'env'}

    # 递归扫描所有.md文件，排除不必要的目录
    md_files = [f for f in root_path.rglob("*.md")
                if not any(part in exclude_dirs for part in f.parts)]
    md_files = sorted(md_files)

    print(f"[📋] 扫描完成: {len(md_files)} 个.md文件")
    print(f"[🔐] GPG密钥: {gpg_key_id[:16]}...")
    print()

    for idx, md_file in enumerate(md_files, 1):
        rel_path = md_file.relative_to(root_path)

        # Step 1: 计算DNA/三色
        dr, color, file_hash = compute_dna_color(str(md_file))

        # Step 2: GPG签名
        success, sig_path, error = gpg_sign_file(str(md_file), gpg_key_id)

        # Step 3: 构建审计记录
        record = {
            "timestamp": datetime.now().isoformat(),
            "file_path": str(rel_path),
            "abs_path": str(md_file),
            "dr": dr,
            "color": color,
            "file_hash": file_hash,
            "gpg_sign": {
                "success": success,
                "sig_file": sig_path,
                "error": error
            }
        }
        audit_records.append(record)

        # 实时输出
        status = "✅" if success else "❌"
        print(f"[{idx:3d}] {status} {color} dr={dr} | {rel_path}")
        if error:
            print(f"      ⚠️  ERROR: {error[:80]}")

    return len(md_files), audit_records

def save_audit_log(audit_records, log_dir="~/longhun-system/logs"):
    """
    保存审计日志为JSONL格式
    返回: log_filepath
    """
    log_path = Path(log_dir).expanduser()
    log_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_path / f"batch_audit_{timestamp}.jsonl"

    with open(log_file, 'w', encoding='utf-8') as f:
        for record in audit_records:
            f.write(json.dumps(record, ensure_ascii=False, separators=(',', ':')) + '\n')

    return str(log_file)

def main():
    import sys

    output_lines = []

    output_lines.append("=" * 70)
    output_lines.append("龍魂批量签名系统 · DNA自动化流水线 v1.0")
    output_lines.append("=" * 70)
    output_lines.append("")

    root_dir = "~/longhun-system"
    gpg_key_id = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

    # 执行批量签名
    total_files, audit_records = batch_sign_directory(root_dir, gpg_key_id)

    output_lines.append("")
    output_lines.append("=" * 70)

    # 统计三色分布
    dr_stats = {}
    color_stats = {"🟢": 0, "🟡": 0, "🔴": 0}
    success_count = sum(1 for r in audit_records if r["gpg_sign"]["success"])

    for record in audit_records:
        dr = record["dr"]
        dr_stats[dr] = dr_stats.get(dr, 0) + 1
        color_stats[record["color"]] += 1

    # 保存审计日志
    log_file = save_audit_log(audit_records, "~/longhun-system/logs")

    output_lines.append(f"[📊] 统计结果")
    output_lines.append(f"    总文件数: {total_files}")
    output_lines.append(f"    签名成功: {success_count}/{total_files}")
    output_lines.append(f"    三色分布: 🟢={color_stats['🟢']} 🟡={color_stats['🟡']} 🔴={color_stats['🔴']}")
    output_lines.append(f"    数字根分布: {dict(sorted(dr_stats.items()))}")
    output_lines.append("")
    output_lines.append(f"[💾] 审计日志: {log_file}")
    output_lines.append("")
    output_lines.append("=" * 70)

    # 输出到stdout和文件
    output_text = "\n".join(output_lines)
    print(output_text, flush=True)
    sys.stdout.flush()

if __name__ == "__main__":
    main()
