#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·壬戌·戌时·䷬萃-ALIGN-FIX-BATCH-v1.0-UID9622-6A1CDB2A
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂对齐批量修复脚本 v1.0
按 LONGHUN_ALIGN.md 协议，为活跃文件补 DNA/CONFIRM，为临时/历史文件归档。

用法:
    python3 08_BIN/lh_align_fix_batch.py [--dry-run]
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 让脚本能找到 core.longhun_core.dna_trace
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.longhun_core.dna_trace import generate_dna

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"
ARCHIVE_DIR = BASE_DIR / "archive" / "frozen"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 视为历史/临时/第三方的路径关键词
# 注意：只匹配作为目录/历史区出现的标识，不因为文件名含 archive/backup 就归档
ARCHIVE_KEYWORDS = [
    "/_archive/", "/archive/", "/backups/", "/downloads_archive/",
    "/venv/", "/site-packages/", "/tmp/", "/temp/",
    "code_with_dna_", "demo_vulnerable",
]


def is_archive_path(path: str) -> bool:
    p = path.lower()
    return any(kw in p for kw in ARCHIVE_KEYWORDS)


def module_name_from_path(path: str) -> str:
    """从文件路径推导 DNA module 名"""
    rel = Path(path)
    name = rel.stem
    # 去掉 lh_ 前缀
    if name.startswith("lh_"):
        name = name[3:]
    # 路径部分
    parts = list(rel.parent.parts)
    # 忽略顶层目录如 08_BIN, 05_ENGINES，保留功能名
    filtered = []
    for part in parts:
        part = part.lower()
        if part in {"users", "zuimeidedeyihan", "longhun-system"}:
            continue
        # 去掉数字前缀如 08_BIN, 05_ENGINES, 13_TESTS
        part = re.sub(r'^(\d+[_-])', '', part)
        if part in {"bin", "engines", "tests", "tools", "layers", "protocols", "skills"}:
            continue
        filtered.append(part)
    # 组合
    tokens = filtered + [name]
    module = "-".join(tokens).upper()
    # 清理
    module = re.sub(r'[^A-Z0-9_\-]', '-', module)
    module = re.sub(r'-+', '-', module).strip('-')
    if len(module) > 60:
        module = module[:60]
    return module or "MODULE"


def add_seal_to_python(filepath: Path, module: str, dry_run: bool) -> dict:
    """为 Python 文件添加 DNA + CONFIRM"""
    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)

    has_dna = "DNA:" in content
    has_confirm = CONFIRM_MARK in content

    if has_dna and has_confirm:
        return {"file": str(filepath), "status": "skip", "reason": "already sealed"}

    # 找到插入位置：shebang 之后、第一个 docstring/注释之后
    insert_idx = 0
    if lines and lines[0].startswith("#!"):
        insert_idx = 1
    # 跳过紧接的编码声明
    if insert_idx < len(lines) and "coding" in lines[insert_idx]:
        insert_idx += 1

    additions = []
    if not has_dna:
        dna = generate_dna(module=module, action="UID9622")
        additions.append(f"# DNA: {dna}\n")
    if not has_confirm:
        additions.append(f"# CONFIRM: {CONFIRM_MARK}\n")

    if not additions:
        return {"file": str(filepath), "status": "skip", "reason": "no additions"}

    if dry_run:
        return {"file": str(filepath), "status": "dry-run", "additions": additions}

    # 插入到 shebang/编码声明之后
    new_lines = lines[:insert_idx] + additions + lines[insert_idx:]
    filepath.write_text("".join(new_lines), encoding="utf-8")
    return {"file": str(filepath), "status": "ok", "additions": additions}


def add_seal_to_shell(filepath: Path, module: str, dry_run: bool) -> dict:
    """为 Shell 文件添加 DNA + CONFIRM"""
    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)

    has_dna = "DNA:" in content
    has_confirm = CONFIRM_MARK in content

    if has_dna and has_confirm:
        return {"file": str(filepath), "status": "skip", "reason": "already sealed"}

    insert_idx = 0
    if lines and lines[0].startswith("#!"):
        insert_idx = 1

    additions = []
    if not has_dna:
        dna = generate_dna(module=module, action="UID9622")
        additions.append(f"# DNA: {dna}\n")
    if not has_confirm:
        additions.append(f"# CONFIRM: {CONFIRM_MARK}\n")

    if not additions:
        return {"file": str(filepath), "status": "skip", "reason": "no additions"}

    if dry_run:
        return {"file": str(filepath), "status": "dry-run", "additions": additions}

    new_lines = lines[:insert_idx] + additions + lines[insert_idx:]
    filepath.write_text("".join(new_lines), encoding="utf-8")
    return {"file": str(filepath), "status": "ok", "additions": additions}


def archive_file(filepath: Path, dry_run: bool) -> dict:
    """移动文件到 archive/frozen/，保持相对目录结构"""
    rel = filepath.relative_to(BASE_DIR)
    dest = ARCHIVE_DIR / rel
    if dry_run:
        return {"file": str(filepath), "status": "dry-run-archive", "dest": str(dest)}

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(filepath), str(dest))
    return {"file": str(filepath), "status": "archived", "dest": str(dest)}


def gpg_sign_file(filepath: Path, force: bool = False, dry_run: bool = False) -> dict:
    """为文件生成 GPG 分离签名"""
    asc = filepath.with_suffix(filepath.suffix + ".asc")
    if asc.exists() and not force:
        return {"file": str(filepath), "status": "skip", "reason": "asc exists"}
    if dry_run:
        return {"file": str(filepath), "status": "dry-run-signed"}

    cmd = [
        "gpg", "--local-user", GPG_KEY, "--armor", "--detach-sign",
        "--batch", "--yes", "--no-tty",
        "-o", str(asc), str(filepath)
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0:
        return {"file": str(filepath), "status": "signed"}
    return {"file": str(filepath), "status": "fail", "error": r.stderr.strip()[:200]}


def load_latest_report() -> dict:
    reports = sorted(REPORT_DIR.glob("align_*.json"), reverse=True)
    if not reports:
        print("❌ 找不到对齐报告，先运行: python3 08_BIN/lh_align.py check --refresh", file=sys.stderr)
        sys.exit(2)
    with open(reports[0], "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="龍魂对齐批量修复")
    parser.add_argument("--dry-run", action="store_true", help="只检测建议，不修改文件")
    args = parser.parse_args()

    report = load_latest_report()
    missing_dna = report.get("missing_dna", [])
    missing_confirm = report.get("missing_confirm", [])
    missing_gpg = report.get("missing_gpg", [])

    # 合并需要处理的文件集合
    files_to_fix = set(missing_dna) | set(missing_confirm)

    results = []
    archived = []
    signed = []

    print(f"🐉 开始对齐修复（dry-run={args.dry_run}）")
    print(f"   待处理文件: {len(files_to_fix)}  缺GPG: {len(missing_gpg)}")

    for f in sorted(files_to_fix):
        filepath = BASE_DIR / f
        if not filepath.exists():
            results.append({"file": f, "status": "skip", "reason": "not found"})
            continue

        if is_archive_path(f):
            archived.append(archive_file(filepath, args.dry_run))
            continue

        module = module_name_from_path(f)
        if f.endswith(".py"):
            results.append(add_seal_to_python(filepath, module, args.dry_run))
        elif f.endswith(".sh"):
            results.append(add_seal_to_shell(filepath, module, args.dry_run))
        else:
            results.append({"file": f, "status": "skip", "reason": "unsupported type"})

    # GPG 签名（仅对存在的文件）
    for f in missing_gpg:
        filepath = BASE_DIR / f
        if not filepath.exists():
            continue
        if is_archive_path(f):
            continue
        signed.append(gpg_sign_file(filepath, force=False, dry_run=args.dry_run))

    # 输出摘要
    ok = [r for r in results if r["status"] == "ok"]
    dry = [r for r in results if r["status"].startswith("dry-run")]
    skipped = [r for r in results if r["status"] == "skip"]
    archived_ok = [r for r in archived if r["status"] in ("archived", "dry-run-archive")]
    signed_ok = [r for r in signed if r["status"] in ("signed",)]

    print(f"\n📊 修复摘要:")
    print(f"   已补签章: {len(ok)}")
    print(f"   已归档: {len(archived_ok)}")
    print(f"   已GPG签名: {len(signed_ok)}")
    print(f"   跳过: {len(skipped)}")
    if args.dry_run:
        print(f"   干跑模式: {len(dry)} 个文件待修改")

    if ok:
        print(f"\n🟢 已补签章文件示例（前10）:")
        for r in ok[:10]:
            print(f"   {r['file']}")

    if archived_ok:
        print(f"\n🟡 已归档文件示例（前10）:")
        for r in archived_ok[:10]:
            print(f"   {r['file']} -> {r.get('dest', '')}")

    # 保存操作日志
    log = {
        "timestamp": datetime.now().isoformat(),
        "dry_run": args.dry_run,
        "report": str(load_latest_report()),
        "results": results,
        "archived": archived,
        "signed": signed,
    }
    log_path = BASE_DIR / "archive" / f"align_fix_{datetime.now():%Y%m%d_%H%M%S}.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n💾 操作日志: {log_path}")


if __name__ == "__main__":
    main()
