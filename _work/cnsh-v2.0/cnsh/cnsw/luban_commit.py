# -*- coding: utf-8 -*-
"""
鲁班绿闸本地提交 — CNSW（暂存补丁正文）× gate_v3（提交说明 dr）× 涉密路径拦截。

仅当汇总为 🟢 且允许提交时执行 `git commit`，不 push。
DNA: #龍芯⚡️2026-05-16-LUBAN-GREEN-COMMIT-v1.0

用法（仓库根目录）：
  python3 -m cnsh.cnsw.luban_commit -m "feat(x): 说明"
  LUBAN_DRY_RUN=1 python3 -m cnsh.cnsw.luban_commit -m "..."
  LUBAN_SKIP_CNSW=1 python3 -m cnsh.cnsw.luban_commit -m "..."   # 仅 dr+秘钥（急救）
  LUBAN_NO_GPG=1  → 追加 git commit --no-gpg-sign

规范：不写 git config；失败非零退出。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

from cnsh.gate_v3.engine import digital_root_from_text, gate_color

from .hook_scanner import scan_output
from .pseudocode_audit import audit_pseudocode_in_text, incremental_added_text_from_patch
from .system_tricolor import aggregate_engineering_from_rows, combine_gate_dr

_PATCH_MAX = 512_000
_SECRET_PATH_RE = re.compile(
    r"(^|/)("
    r"\.env[^/]*|\.pem$|id_rsa|id_ed25519|\.key$|credentials\.json|"
    r"secrets\.|token\.json|\.pfx$|\.p12$"
    r")",
    re.I,
)


def _repo_root() -> Path:
    r = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(r.stdout.strip())


def _staged_paths(root: Path) -> List[str]:
    r = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "-z"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return [p for p in r.stdout.split("\0") if p]


def _check_secret_paths(paths: List[str]) -> Tuple[bool, str]:
    for p in paths:
        if _SECRET_PATH_RE.search(p.replace("\\", "/")):
            return False, f"涉密路径命中 staged：{p}"
    return True, ""


def _staged_patch(root: Path) -> str:
    r = subprocess.run(
        ["git", "diff", "--cached", "--binary"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return r.stdout[:_PATCH_MAX]


def _aggregate_from_patch(patch: str) -> dict:
    if os.environ.get("LUBAN_SKIP_CNSW", "").strip() in ("1", "true", "yes"):
        return aggregate_engineering_from_rows(
            [{"drift_level": "L0", "sovereignty_score": 100}]
        )
    scan = scan_output(patch or "(empty)", include_supplemental=True, pseudocode_scan=False)
    return aggregate_engineering_from_rows(
        [
            {
                "drift_level": scan["drift_level"],
                "sovereignty_score": int(scan["sovereignty_score"]),
            }
        ]
    )


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="鲁班绿闸：CNSW+dr 通过后 git commit")
    ap.add_argument(
        "-m",
        "--message",
        required=True,
        help="提交说明（参与 gate_v3 数字根判定）",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印 JSON 审计，不执行 commit",
    )
    args = ap.parse_args(argv)

    root = _repo_root()
    dry = args.dry_run or os.environ.get("LUBAN_DRY_RUN", "").strip() in ("1", "true")

    paths = _staged_paths(root)
    if not paths:
        sys.stderr.write("🔴 无 staged 变更，跳过提交\n")
        return 5

    ok, err = _check_secret_paths(paths)
    if not ok:
        sys.stderr.write(f"🔴 {err}\n")
        return 6

    patch = _staged_patch(root)
    agg = _aggregate_from_patch(patch)
    dr = digital_root_from_text(args.message)
    gc = gate_color(dr)
    combined, dual_green = combine_gate_dr(
        flow=agg["flow_tricolor"], gate_dr_color=gc
    )
    commit_ok = bool(agg.get("commit_allowed")) and dual_green and combined == "🟢"

    out = {
        "flow_tricolor": combined,
        "cnsw_aggregate": {k: v for k, v in agg.items() if k != "p05_lane"},
        "gate": {"dr": dr, "gate_color": gc},
        "commit_allowed": commit_ok,
        "staged_files": len(paths),
        "pseudocode_on_added_lines": audit_pseudocode_in_text(
            incremental_added_text_from_patch(patch)
        ),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

    if not commit_ok:
        sys.stderr.write(
            f"🔴 鲁班绿闸未通过：合并三色={combined} "
            f"(CNSW worst={agg.get('worst_drift_level')}, "
            f"提交说明 dr={dr}→{gc})\n"
        )
        return 7 if combined == "🔴" else 8

    if dry:
        sys.stderr.write("🟡 DRY_RUN：本可提交，未执行 git commit\n")
        return 0

    cmd = ["git", "commit"]
    if os.environ.get("LUBAN_NO_GPG", "").strip() in ("1", "true", "yes"):
        cmd.append("--no-gpg-sign")
    cmd.extend(["-m", args.message])
    subprocess.run(
        cmd,
        cwd=root,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
