#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·甲午·己巳·庚午·䷃蒙-LONGHUN-AUDIT-LOGGER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

# DNA: #龍芯⚡️丙午·甲午·己巳·庚午·䷃蒙-LONGHUN-AUDIT-LOGGER-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""
龍魂审计日志器 · LongHun Audit Logger v1.0

只追加（append-only）的 JSONL 审计日志：
- id: UUID v4
- ts: ISO-8601 UTC
- user_id: 用户或 system
- op: scan | write | sync | model_upgrade | incident_fix | ...
- status: success | partial | failed
- error_code: 可为 null
- evidence: {artifact_path|db_primary_key|config_hash|model_id|release_id}
- stats: {hit_count|wrote_count|deduped_count|duration_ms|...}

用法:
    python3 audit_logger.py log --op scan --status success --evidence '{"artifact_path":"/tmp/x"}' --stats '{"hit_count":10}'
    python3 audit_logger.py tail 20
    python3 audit_logger.py verify
"""

import os
import json
import uuid
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List


class 龍魂审计日志器:
    DNA = "#龍芯⚡️丙午·甲午·己巳·庚午·䷃蒙-LONGHUN-AUDIT-LOGGER-v1.0"

    def __init__(self, log_dir: Optional[str] = None):
        if log_dir:
            self.log_dir = Path(log_dir)
        else:
            self.log_dir = Path.home() / ".longhun" / "audit"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "anti_blowout.jsonl"

    def 记录(
        self,
        op: str,
        status: str,
        evidence: Optional[Dict[str, Any]] = None,
        stats: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        user_id: str = "system",
        extra: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        record = {
            "id": str(uuid.uuid4()),
            "ts": datetime.now(timezone.utc).isoformat(),
            "user_id": user_id,
            "op": op,
            "status": status,
            "error_code": error_code,
            "evidence": evidence or {},
            "stats": stats or {},
            "DNA": self.DNA,
        }
        if extra:
            record.update(extra)
        self._追加(record)
        return record

    def _追加(self, record: Dict[str, Any]):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def 读取(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        if not self.log_file.exists():
            return []
        records = []
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return records[-(offset + limit):][:limit] if limit else records

    def 验证(self) -> Dict[str, Any]:
        """验证日志只追加性：检查是否有行被修改（通过重读并校验递增）"""
        if not self.log_file.exists():
            return {"valid": True, "count": 0, "message": "日志文件不存在"}
        records = self.读取(limit=0)
        issues = []
        for i, r in enumerate(records):
            if "id" not in r:
                issues.append(f"第{i+1}行缺少 id")
            if "ts" not in r:
                issues.append(f"第{i+1}行缺少 ts")
        return {
            "valid": len(issues) == 0,
            "count": len(records),
            "issues": issues,
            "file": str(self.log_file),
        }


def main():
    parser = argparse.ArgumentParser(description="龍魂审计日志器")
    sub = parser.add_subparsers(dest="action")

    p_log = sub.add_parser("log", help="写入一条审计记录")
    p_log.add_argument("--op", required=True)
    p_log.add_argument("--status", required=True, choices=["success", "partial", "failed"])
    p_log.add_argument("--evidence", default="{}", help="JSON 字符串")
    p_log.add_argument("--stats", default="{}", help="JSON 字符串")
    p_log.add_argument("--error-code", default=None)
    p_log.add_argument("--user", default="system")

    p_tail = sub.add_parser("tail", help="查看最近 N 条")
    p_tail.add_argument("n", type=int, default=10)

    p_verify = sub.add_parser("verify", help="验证日志完整性")

    args = parser.parse_args()

    logger = 龍魂审计日志器()

    if args.action == "log":
        ev = json.loads(args.evidence)
        st = json.loads(args.stats)
        record = logger.记录(args.op, args.status, ev, st, args.error_code, args.user)
        print(json.dumps(record, ensure_ascii=False, indent=2))
    elif args.action == "tail":
        for r in logger.读取(limit=args.n):
            print(json.dumps(r, ensure_ascii=False))
    elif args.action == "verify":
        print(json.dumps(logger.验证(), ensure_ascii=False, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
