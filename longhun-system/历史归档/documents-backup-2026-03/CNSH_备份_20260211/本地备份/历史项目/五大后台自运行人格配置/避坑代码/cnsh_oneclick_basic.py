#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH One-Click Task Executor (zh: yi jian zhi xing qi)
Constraints:
- Pure ASCII source code (no non-ASCII characters)
- No font usage (terminal output only)
- Force UTF-8 output for all text
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import sys
from typing import Any, Dict, List, Tuple

# ----------------------------- UTF-8 enforcement -----------------------------
def force_utf8_io() -> None:
    """
    Force UTF-8 for stdout/stderr regardless of platform defaults.
    (zh: qiang zhi UTF-8 shu chu)
    """
    os.environ.setdefault("PYTHONUTF8", "1")

    # Python 3.7+ usually supports reconfigure on text streams.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="strict", newline="\n")
    except Exception:
        pass

    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="strict", newline="\n")
    except Exception:
        pass

def u8_print(*parts: Any) -> None:
    """
    Print with guaranteed UTF-8 encoding by writing bytes to stdout buffer.
    (zh: yong UTF-8 byte xie chu)
    """
    s = " ".join("" if p is None else str(p) for p in parts) + "\n"
    b = s.encode("utf-8", errors="strict")
    try:
        sys.stdout.buffer.write(b)
        sys.stdout.buffer.flush()
    except Exception:
        # Fallback if buffer is unavailable
        sys.stdout.write(s)
        sys.stdout.flush()

# ----------------------------- Three-color audit -----------------------------
class ThreeColorAudit:
    """
    Minimal three-color audit engine.
    (zh: san se shen ji yin qing)
    """

    def __init__(self) -> None:
        # Keep patterns ASCII-only; do NOT embed non-ASCII keywords in source.
        self.red_rules: List[Tuple[re.Pattern[str], str]] = [
            (re.compile(r"\bhow\s+to\s+(build|make)\s+(bomb|explosive)\b", re.I), "illegal_harm"),
            (re.compile(r"\bcredit\s+card\s+number\b", re.I), "sensitive_data"),
        ]
        self.yellow_rules: List[Tuple[re.Pattern[str], str]] = [
            (re.compile(r"\bpassword\b", re.I), "possible_secret"),
            (re.compile(r"\bapi\s*key\b", re.I), "possible_secret"),
        ]

    def check(self, text: str) -> Dict[str, str]:
        """
        Return audit result: level, reason, action.
        (zh: fan hui shen ji jie guo)
        """
        for pat, reason in self.red_rules:
            if pat.search(text):
                return {"level": "RED", "reason": reason, "action": "BLOCK"}
        for pat, reason in self.yellow_rules:
            if pat.search(text):
                return {"level": "YELLOW", "reason": reason, "action": "WARN_AND_CONTINUE"}
        return {"level": "GREEN", "reason": "ok", "action": "ALLOW"}

# ----------------------------- DNA trace -------------------------------------
def make_dna(prefix: str) -> str:
    """
    Build a DNA trace string with UTC timestamp.
    (zh: sheng cheng DNA zhui su ma)
    """
    ts = _dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"{prefix}{ts}"

def sha256_hex(data: bytes) -> str:
    """
    Compute SHA256 hex digest.
    (zh: suan SHA256)
    """
    return hashlib.sha256(data).hexdigest()

# ----------------------------- Output format ---------------------------------
def build_output(
    uid: str,
    dna_prefix: str,
    confirm_code: str,
    gpg_fpr: str,
    sha256_fpr: str,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Build a strict JSON output package for downstream tools.
    (zh: sheng cheng gui fan shu chu)
    """
    now = _dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    dna = make_dna(dna_prefix)
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8", errors="strict")
    payload_sha = sha256_hex(raw)

    return {
        "meta": {
            "uid": uid,
            "confirm_code": confirm_code,
            "dna": dna,
            "generated_at_utc": now,
            "identity": {
                "gpg_fingerprint": gpg_fpr,
                "sha256_fingerprint": sha256_fpr,
            },
        },
        "payload": payload,
        "payload_sha256": payload_sha,
    }

def default_payload() -> Dict[str, Any]:
    """
    Default task payload template.
    (zh: mo ren ren wu mo ban)
    """
    return {
        "task_name": "cnsh_oneclick_bootstrap",
        "requirements": [
            "pure_utf8_output",
            "no_system_fonts",
            "three_color_audit",
            "dna_trace",
        ],
        "deliverables": [
            "project_skeleton",
            "docs_pack",
            "audit_module",
            "dna_module",
        ],
        "notes": [
            "Keep source ASCII-only.",
            "Emit JSON UTF-8 only.",
        ],
    }

# ----------------------------- Main ------------------------------------------
def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="CNSH one-click executor (ASCII-only source).")
    p.add_argument("--uid", default="9622")
    p.add_argument("--dna-prefix", default="#ZHUGEXIN-")  # ASCII-only prefix
    p.add_argument("--confirm", default="#CONFIRM-9622-ONLY-ONCE-LK9X-772Z")
    p.add_argument("--gpg", default="A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
    p.add_argument("--sha256", default="b83c74d108660082581f9ebbb9506f65849d9d48d21d328daf13f7c4d66cf6c1")
    p.add_argument("--input", default="", help="Optional input text/file to audit.")
    p.add_argument("--input-is-file", action="store_true", help="Treat --input as file path.")
    return p.parse_args(argv)

def read_input_text(arg: str, is_file: bool) -> str:
    if not arg:
        return ""
    if is_file:
        with open(arg, "rb") as f:
            b = f.read()
        return b.decode("utf-8", errors="strict")
    return arg

def main(argv: List[str]) -> int:
    force_utf8_io()
    args = parse_args(argv)

    audit = ThreeColorAudit()

    # Read optional input for auditing (zh: du ru shen ji nei rong)
    input_text = read_input_text(args.input, args.input_is_file)
    audit_result = audit.check(input_text) if input_text else {"level": "GREEN", "reason": "no_input", "action": "ALLOW"}

    # Build payload (zh: gou jian payload)
    payload = default_payload()
    payload["audit"] = audit_result

    # Emit JSON output (zh: shu chu JSON)
    out = build_output(
        uid=args.uid,
        dna_prefix=args.dna_prefix,
        confirm_code=args.confirm,
        gpg_fpr=args.gpg,
        sha256_fpr=args.sha256,
        payload=payload,
    )

    u8_print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if audit_result.get("level") != "RED" else 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
