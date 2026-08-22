#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂道引器 · Gitee 批量吸收桥接脚本 v1.0

作用：将 gitee.com 仓库 clone 到临时目录，然后调用 lh_daoyin.py absorb 道引吸收。
原因：lh_daoyin.py v2.0 只支持 GitHub tarball 和本地路径，需此桥接层处理 Gitee。

用法：
  python3 bin/lh_daoyin_gitee_batch.py batch <repos.txt> [--workers 2] [--dry-run]

DNA: #龍芯⚡️丙午·丙申·丙辰·戊子·䷜坎-DAOYIN-GITEE-BRIDGE-v1.0
"""

import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional, Tuple, Any

# ── 路径 ──
SCRIPT_DIR = Path(__file__).resolve().parent
LONGHUN_ROOT = SCRIPT_DIR.parent
DAOYIN_SCRIPT = SCRIPT_DIR / "lh_daoyin.py"

# ── 17 个 Gitee 目标仓库（按5梯队排列）──
DEFAULT_REPOS = [
    # 第一梯队：鸿蒙底层与内核（权重:10）
    "https://gitee.com/openharmony/kernel_linux_5.10",
    "https://gitee.com/openharmony/drivers_peripheral",
    "https://gitee.com/openharmony/distributed_hardware",
    "https://gitee.com/openharmony/ability_base",
    # 第二梯队：鲲鹏/昇腾底层算力适配（权重:10）
    "https://gitee.com/kunpengcompute/KunpengBoostKit",
    "https://gitee.com/ascend/ascend-cann-toolkit",
    "https://gitee.com/openeuler/kernel",
    "https://gitee.com/mindspore/mindspore",
    # 第三梯队：国产安全与国密算法（权重:10）
    "https://gitee.com/gmssl/GmSSL",
    "https://gitee.com/openeuler/openssl",
    "https://gitee.com/openharmony/security_huks",
    # 第四梯队：方舟编译器与工具链（权重:9）
    "https://gitee.com/openarkcompiler/OpenArkCompiler",
    "https://gitee.com/openharmony-tpc/ohos_build",
    # 第五梯队：鸿蒙 UI 框架与图形渲染（权重:8）
    "https://gitee.com/openharmony/ui",
    "https://gitee.com/openharmony/graphic_2d",
    "https://gitee.com/openharmony/graphic_3d",
]

TIER_MAP = {
    "kernel_linux_5.10": 1, "drivers_peripheral": 1, "distributed_hardware": 1, "ability_base": 1,
    "KunpengBoostKit": 2, "ascend-cann-toolkit": 2, "openeuler/kernel": 2, "mindspore": 2,
    "GmSSL": 3, "openeuler/openssl": 3, "security_huks": 3,
    "OpenArkCompiler": 4, "ohos_build": 4,
    "ui": 5, "graphic_2d": 5, "graphic_3d": 5,
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_gitee_url(url: str) -> Optional[Tuple[str, str]]:
    """从 gitee.com URL 提取 owner/repo（支持 HTTPS 和 SSH 格式）"""
    # SSH 格式: git@gitee.com:owner/repo.git
    m = re.match(r"git@gitee\.com:([^/]+/[^/]+)", url.rstrip(".git"))
    if m:
        parts = m.group(1).split("/")
        return parts[0], parts[1]
    # HTTPS 格式: https://gitee.com/owner/repo
    m = re.match(r"https?://gitee\.com/([^/]+/[^/]+)", url.rstrip("/").rstrip(".git"))
    if m:
        parts = m.group(1).split("/")
        return parts[0], parts[1]
    return None


def to_ssh_clone_url(url: str) -> str:
    """将 HTTPS Gitee URL 转为 SSH clone 地址"""
    parsed = parse_gitee_url(url)
    if parsed:
        return f"git@gitee.com:{parsed[0]}/{parsed[1]}.git"
    return url


def read_repos(filepath: str) -> List[str]:
    repos = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            repos.append(line)
    return repos


class CloneResult(NamedTuple):
    source: str
    success: bool
    local_path: str
    error: str
    clone_elapsed: float


def clone_repo(source: str, clone_dir: Path) -> CloneResult:
    """浅克隆一个 Gitee 仓库，返回本地路径"""
    parsed = parse_gitee_url(source)
    if not parsed:
        return CloneResult(source, False, "", f"无法解析 Gitee URL: {source}", 0)

    owner, repo = parsed
    dest = clone_dir / repo
    t0 = time.time()

    try:
        ssh_url = to_ssh_clone_url(source)
        cmd = ["git", "clone", "--depth=1", "--single-branch", ssh_url, str(dest)]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5分钟超时
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_LFS_SKIP_SMUDGE": "1"},
        )
        elapsed = time.time() - t0
        if result.returncode != 0:
            err = result.stderr.strip()[-200:] if result.stderr else "未知错误"
            return CloneResult(source, False, "", f"clone 失败: {err}", elapsed)

        size = sum(f.stat().st_size for f in dest.rglob("*") if f.is_file())
        print(f"   📥 clone 完成 · {size/1024/1024:.1f}MB · {elapsed:.1f}s")
        return CloneResult(source, True, str(dest), "", elapsed)

    except subprocess.TimeoutExpired:
        return CloneResult(source, False, "", "clone 超时 (5分钟)", time.time() - t0)
    except Exception as e:
        return CloneResult(source, False, "", str(e), time.time() - t0)


def absorb_local(path: str, dry_run: bool = False) -> Dict[str, Any]:
    """调用 lh_daoyin.py absorb 吸收本地路径"""
    cmd = [sys.executable, str(DAOYIN_SCRIPT), "absorb", path]
    if dry_run:
        cmd.append("--dry-run")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(LONGHUN_ROOT),
        )
        stdout_text = result.stdout
        stderr_text = result.stderr

        # 尝试从 stdout 解析 DNA
        dna_match = re.search(r"DNA:\s*(#龍芯[^\s]+)", stdout_text + stderr_text)
        dna = dna_match.group(1) if dna_match else ""

        return {
            "success": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": stdout_text[-500:] if stdout_text else "",
            "stderr": stderr_text[-500:] if stderr_text else "",
            "dna": dna,
        }

    except subprocess.TimeoutExpired:
        return {"success": False, "exit_code": -1, "dna": "", "stderr": "absorb 超时"}
    except Exception as e:
        return {"success": False, "exit_code": -1, "dna": "", "stderr": str(e)}


def process_single(url: str, dry_run: bool = False) -> Dict[str, Any]:
    """
    单个 Gitee 仓库处理流程：
    1. clone → 2. daoyin absorb → 3. 清理 clone
    """
    parsed = parse_gitee_url(url)
    owner_repo = f"{parsed[0]}/{parsed[1]}" if parsed else url
    result = {
        "source": url,
        "owner_repo": owner_repo,
        "success": False,
        "clone_ok": False,
        "absorb_ok": False,
        "dna": "",
        "error": "",
        "elapsed_total": 0,
    }

    t0 = time.time()

    with tempfile.TemporaryDirectory(prefix="daoyin_gitee_") as tmp:
        clone_dir = Path(tmp)

        # Step 1: Clone
        print(f"\n{'='*60}")
        print(f"📥 [{owner_repo}] 道引开始")
        print(f"   URL: {url}")

        clone_result = clone_repo(url, clone_dir)
        result["clone_ok"] = clone_result.success
        result["elapsed_clone"] = clone_result.clone_elapsed

        if not clone_result.success:
            result["error"] = f"clone: {clone_result.error}"
            print(f"   ❌ {result['error']}")
            return result

        # Step 2: Absorb
        print(f"   🔄 道引吸收中...")
        absorb_result = absorb_local(clone_result.local_path, dry_run=dry_run)
        result["absorb_ok"] = absorb_result["success"]
        result["dna"] = absorb_result.get("dna", "")

        if absorb_result["success"]:
            print(f"   ✅ DNA: {result['dna']}")
        elif dry_run:
            print(f"   🧪 试运行完成（未入链）")
        else:
            err = absorb_result.get("stderr", "") or absorb_result.get("stdout", "")
            result["error"] = f"absorb: {err[:200]}"
            print(f"   ❌ {result['error']}")

        result["success"] = absorb_result["success"]
        result["elapsed_total"] = time.time() - t0

        if result["success"]:
            print(f"   ⏱️ 总耗时 {result['elapsed_total']:.1f}s")

    return result


def batch_process(repos: List[str], workers: int = 2, dry_run: bool = False) -> List[Dict]:
    """批量处理 Gitee 仓库列表"""
    total = len(repos)
    print(f"\n🔰 龍魂道引 · Gitee 批量吸收桥接")
    print(f"   仓库数: {total}")
    print(f"   并发数: {workers}")
    print(f"   模式: {'🧪 试运行' if dry_run else '🔒 正式入链'}")
    print(f"   {'='*60}")

    results: List[Dict] = []
    start = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(process_single, repo, dry_run): repo for repo in repos}
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                source = futures[future]
                results.append({
                    "source": source, "owner_repo": source,
                    "success": False, "error": str(e),
                })

    elapsed = time.time() - start
    success = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    # ── 汇总 ──
    print(f"\n{'='*60}")
    print(f"📊 Gitee 批量吸收完成 · 耗时 {elapsed:.1f}s ({elapsed/60:.1f}min)")
    print(f"   ✅ 成功: {len(success)}/{total}")
    print(f"   ❌ 失败: {len(failed)}/{total}")

    if success:
        print(f"\n   成功清单:")
        for r in success:
            print(f"   ✅ {r['owner_repo']} → {r['dna']}")

    if failed:
        print(f"\n   失败清单:")
        for r in failed:
            err = r.get("error", "未知")[:100]
            print(f"   ❌ {r['owner_repo']} — {err}")

    # ── 保存批次日志 ──
    log_dir = LONGHUN_ROOT / "L7_数据层" / "daoyin"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"gitee_batch_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    log = {
        "batch_type": "gitee_clone_bridge",
        "total": total,
        "success_count": len(success),
        "failed_count": len(failed),
        "elapsed_seconds": elapsed,
        "dry_run": dry_run,
        "results": results,
    }
    log_file.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n📄 批次日志: {log_file}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="龍魂道引器 · Gitee 批量吸收桥接",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_daoyin_gitee_batch.py batch repos.txt
  python3 bin/lh_daoyin_gitee_batch.py batch repos.txt --dry-run
  python3 bin/lh_daoyin_gitee_batch.py default   # 使用内建默认名单
  python3 bin/lh_daoyin_gitee_batch.py default --dry-run
        """,
    )

    sub = parser.add_subparsers(dest="command", help="命令")

    # default 命令
    cmd_default = sub.add_parser("default", help="使用内建默认17仓库名单吸收")

    # batch 命令
    cmd_batch = sub.add_parser("batch", help="从文件读取仓库名单批量吸收")
    cmd_batch.add_argument("repo_file", help="仓库名单文件（每行一个URL）")
    cmd_batch.add_argument("--workers", type=int, default=2, help="并发数（默认2，Gitee限速）")
    cmd_batch.add_argument("--dry-run", action="store_true", help="试运行，不入链")

    # default 命令参数
    cmd_default.add_argument("--workers", type=int, default=2, help="并发数（默认2）")
    cmd_default.add_argument("--dry-run", action="store_true", help="试运行，不入链")

    args = parser.parse_args()

    if args.command == "default":
        repos = DEFAULT_REPOS
        batch_process(repos, workers=args.workers, dry_run=args.dry_run)

    elif args.command == "batch":
        repos = read_repos(args.repo_file)
        if not repos:
            print(f"❌ 名单为空: {args.repo_file}")
            sys.exit(1)
        print(f"📋 从文件读取: {args.repo_file} ({len(repos)} 个仓库)")
        batch_process(repos, workers=args.workers, dry_run=args.dry_run)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
