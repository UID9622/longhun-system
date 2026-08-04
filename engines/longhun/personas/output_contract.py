#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️2026-06-24-LONGHUN-OUTPUT-CONTRACT-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

# DNA: #龍芯⚡️2026-06-24-LONGHUN-OUTPUT-CONTRACT-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""
龍魂输出契约 · LongHun Output Contract v1.0

规则：任何声明「完成/已修复/已升级/已写入/已扫描」的输出，
     必须附带可验证的 evidence + stats，否则系统禁止输出完成声明。

用法:
    python3 output_contract.py validate --op scan --status success --evidence '{"artifact_path":"/tmp/x"}' --stats '{"hit_count":10}'
    python3 output_contract.py demo-fail
"""

import json
import argparse
from typing import Dict, Any, Optional, List


class 龍魂输出契约:
    DNA = "#龍芯⚡️2026-06-24-LONGHUN-OUTPUT-CONTRACT-v1.0"

    VALID_OPS = {
        "scan", "write", "sync", "model_upgrade", "incident_fix",
        "deploy", "audit", "compress", "sign", "check",
        "daily_review", "autostart", "heal", "status", "memory",
        "persona", "skill", "cnsh", "review", "cleanup",
    }

    EVIDENCE_KEYS = {
        "artifact_path", "db_primary_key", "config_hash", "build_hash",
        "model_id", "release_id", "commit_hash", "file_path",
    }

    STAT_KEYS = {
        "hit_count", "wrote_count", "deduped_count", "duration_ms",
        "status", "error_code", "records_scanned", "records_deduped",
    }

    COMPLETION_KEYWORDS = {
        "完成", "已修复", "已升级", "已写入", "已扫描", "已同步",
        "completed", "fixed", "upgraded", "written", "done", "synced",
        "full scan done", "resolved",
    }

    def __init__(self):
        self.violations: List[str] = []

    def 验证(
        self,
        op: str,
        status: str,
        evidence: Optional[Dict[str, Any]] = None,
        stats: Optional[Dict[str, Any]] = None,
        output_text: str = "",
    ) -> Dict[str, Any]:
        violations = []

        if op not in self.VALID_OPS:
            violations.append(f"未知 op: {op}，必须是 {self.VALID_OPS}")

        if status not in {"success", "partial", "failed"}:
            violations.append(f"status 必须是 success/partial/failed，当前: {status}")

        ev = evidence or {}
        if not any(k in ev for k in self.EVIDENCE_KEYS):
            violations.append("缺少可验证 evidence（artifact_path/db_primary_key/config_hash/build_hash/model_id/release_id/commit_hash/file_path 至少一个）")

        st = stats or {}
        if "duration_ms" not in st:
            violations.append("stats 缺少 duration_ms")

        # 如果输出文本包含完成声明，但未通过契约，加重错误
        has_completion_claim = any(kw in output_text.lower() for kw in self.COMPLETION_KEYWORDS)

        return {
            "valid": len(violations) == 0,
            "violations": violations,
            "has_completion_claim": has_completion_claim,
            "blocked": has_completion_claim and len(violations) > 0,
            "DNA": self.DNA,
        }

    def 安全输出(self, result: Dict[str, Any]) -> str:
        if result.get("blocked"):
            return f"[契约拦截] 输出被阻止：{'; '.join(result['violations'])}"
        if not result.get("valid"):
            return f"[契约警告] {'; '.join(result['violations'])}"
        return "[契约通过] 输出可被验证"


def main():
    parser = argparse.ArgumentParser(description="龍魂输出契约校验")
    sub = parser.add_subparsers(dest="action")

    p_val = sub.add_parser("validate", help="校验一次操作")
    p_val.add_argument("--op", required=True)
    p_val.add_argument("--status", required=True)
    p_val.add_argument("--evidence", default="{}")
    p_val.add_argument("--stats", default="{}")
    p_val.add_argument("--output", default="", help="模拟输出文本")

    p_demo = sub.add_parser("demo-fail", help="演示一次失败拦截")

    args = parser.parse_args()

    contract = 龍魂输出契约()

    if args.action == "validate":
        ev = json.loads(args.evidence)
        st = json.loads(args.stats)
        result = contract.验证(args.op, args.status, ev, st, args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(contract.安全输出(result))
    elif args.action == "demo-fail":
        result = contract.验证(
            op="scan",
            status="success",
            evidence={},
            stats={},
            output_text="full scan done",
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(contract.安全输出(result))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
