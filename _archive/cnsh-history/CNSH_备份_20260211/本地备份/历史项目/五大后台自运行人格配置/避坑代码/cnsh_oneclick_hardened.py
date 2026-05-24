#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH One-Click Executor - Hardened Edition
- Pure ASCII source code
- No font usage
- Force UTF-8 output
- English comments, add (zh: ...) after key logic lines
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ----------------------------- UTF-8 enforcement -----------------------------
def force_utf8_io() -> None:
    """
    Force UTF-8 for stdout/stderr.
    (zh: qiang zhi UTF-8 shu chu)
    """
    os.environ.setdefault("PYTHONUTF8", "1")  # (zh: qiang zhi python utf8 mo shi)

    # Best-effort stream reconfigure (Python 3.7+)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="strict", newline="\n")
    except Exception:
        pass
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="strict", newline="\n")
    except Exception:
        pass

def u8_write(s: str) -> None:
    """
    Write UTF-8 bytes to stdout.
    (zh: yong byte xie chu)
    """
    b = s.encode("utf-8", errors="strict")
    try:
        sys.stdout.buffer.write(b)
        sys.stdout.buffer.flush()
    except Exception:
        sys.stdout.write(s)
        sys.stdout.flush()

def u8_print(*parts: Any) -> None:
    """
    Print with UTF-8 enforcement.
    (zh: utf8 da yin)
    """
    s = " ".join("" if p is None else str(p) for p in parts) + "\n"
    u8_write(s)

# ----------------------------- Safe IO helpers ------------------------------
def safe_read_text(path: Path, max_bytes: int = 2_000_000) -> str:
    """
    Read UTF-8 text from a file with size guard.
    (zh: wen jian du qu xian zhi da xiao)
    """
    if not path.exists():
        raise FileNotFoundError(f"input file not found: {path}")
    size = path.stat().st_size
    if size > max_bytes:
        raise ValueError(f"input file too large: {size} bytes > {max_bytes}")
    data = path.read_bytes()
    return data.decode("utf-8", errors="strict")

def safe_write_text(path: Path, text: str) -> None:
    """
    Write UTF-8 text atomically.
    (zh: yuan zi xie ru)
    """
    tmp = path.with_suffix(path.suffix + ".tmp")
    data = text.encode("utf-8", errors="strict")
    tmp.write_bytes(data)
    tmp.replace(path)

# ----------------------------- Time/DNA trace --------------------------------
def utc_now_iso() -> str:
    """
    Return current UTC in ISO format.
    (zh: huo qu UTC shi jian)
    """
    return _dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

def make_dna(prefix: str) -> str:
    """
    Build DNA trace string.
    (zh: sheng cheng DNA)
    """
    return f"{prefix}{utc_now_iso()}"

def sha256_hex(data: bytes) -> str:
    """
    Compute SHA256 hex digest.
    (zh: suan SHA256)
    """
    return hashlib.sha256(data).hexdigest()

# ----------------------------- Three-color audit -----------------------------
@dataclass
class AuditFinding:
    level: str
    reason: str
    action: str
    pros_note: str
    risks_note: str

class ThreeColorAudit:
    """
    Minimal policy engine. Keep source ASCII-only; patterns are ASCII.
    (zh: san se shen ji)
    """

    def __init__(self) -> None:
        self.red_rules: List[Tuple[re.Pattern[str], str]] = [
            (re.compile(r"\bhow\s+to\s+(build|make)\s+(bomb|explosive)\b", re.I), "illegal_harm"),
            (re.compile(r"\bcredit\s+card\s+number\b", re.I), "sensitive_data"),
            (re.compile(r"\bmalware\b|\bransomware\b|\bkeylogger\b", re.I), "malicious_intent"),
        ]
        self.yellow_rules: List[Tuple[re.Pattern[str], str]] = [
            (re.compile(r"\bpassword\b", re.I), "possible_secret"),
            (re.compile(r"\bapi\s*key\b", re.I), "possible_secret"),
            (re.compile(r"\btoken\b", re.I), "possible_secret"),
        ]

    def check(self, text: str) -> AuditFinding:
        """
        Return audit finding including pros/risks notes.
        (zh: fan hui you lie zhu shi)
        """
        for pat, reason in self.red_rules:
            if pat.search(text):
                return AuditFinding(
                    level="RED",
                    reason=reason,
                    action="BLOCK",
                    pros_note="Blocks high-risk content early.",  # (zh: ti qian zu duan)
                    risks_note="May over-block benign text containing keywords.",  # (zh: wu sha feng xian)
                )
        for pat, reason in self.yellow_rules:
            if pat.search(text):
                return AuditFinding(
                    level="YELLOW",
                    reason=reason,
                    action="WARN_AND_CONTINUE",
                    pros_note="Warns on possible secrets without stopping work.",  # (zh: ti shi dan bu zhong duan)
                    risks_note="May miss non-obvious sensitive patterns.",  # (zh: lou jian feng xian)
                )
        return AuditFinding(
            level="GREEN",
            reason="ok",
            action="ALLOW",
            pros_note="No policy hits found under current rules.",  # (zh: gui ze fan wei nei an quan)
            risks_note="Rules are minimal; expand for real deployments.",  # (zh: xu yao kuo zhan)
        )

# ----------------------------- Output packaging ------------------------------
def canonical_json_bytes(obj: Any) -> bytes:
    """
    Encode object to canonical JSON bytes (stable).
    (zh: gu ding shu chu)
    """
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return s.encode("utf-8", errors="strict")

def build_output(
    uid: str,
    dna_prefix: str,
    confirm_code: str,
    gpg_fpr: str,
    sha256_fpr: str,
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Build strict JSON output package.
    (zh: shu chu bao)
    """
    dna = make_dna(dna_prefix)
    payload_bytes = canonical_json_bytes(payload)
    payload_sha = sha256_hex(payload_bytes)

    return {
        "meta": {
            "uid": uid,
            "confirm_code": confirm_code,
            "dna": dna,
            "generated_at_utc": utc_now_iso(),
            "identity": {
                "gpg_fingerprint": gpg_fpr,
                "sha256_fingerprint": sha256_fpr,
            },
            "constraints": {
                "ascii_source_only": True,
                "utf8_output_only": True,
                "no_fonts": True,
            },
        },
        "payload": payload,
        "payload_sha256": payload_sha,
    }

# ----------------------------- Project skeleton generator --------------------
def default_payload() -> Dict[str, Any]:
    """
    Default task payload template.
    (zh: mo ren ren wu)
    """
    return {
        "task_name": "cnsh_oneclick_bootstrap",
        "requirements": [
            "pure_utf8_output",
            "no_system_fonts",
            "three_color_audit",
            "dna_trace",
            "atomic_write",
            "size_guard",
            "canonical_json",
        ],
        "deliverables": [
            "project_skeleton",
            "docs_pack",
            "audit_module",
            "dna_module",
            "plugin_stub",
        ],
        "notes": [
            "Keep source ASCII-only.",
            "Emit JSON UTF-8 only.",
            "Prefer stable output for hashing.",
        ],
    }

def make_skeleton_tree(root: Path) -> List[str]:
    """
    Return list of relative paths to create.
    (zh: sheng cheng mu lu)
    """
    return [
        "README.md",
        "QUICK_START.md",
        "PROJECT_STRUCTURE.md",
        "CNSH_BOOTSTRAP.md",
        "index.html",
        "assets/.keep",
        "docs/.keep",
        "cnsh/.keep",
        "editor/.keep",
        "audit/.keep",
        "dna/.keep",
        "plugins/.keep",
        "tools/.keep",
    ]

def skeleton_file_content(rel: str) -> Optional[str]:
    """
    Minimal file contents (ASCII-only).
    (zh: mo ban nei rong)
    """
    if rel == "README.md":
        return (
            "# CNSH Editor\n\n"
            "- UID: UID9622\n"
            "- DNA: #ZHUGEXIN- (ASCII prefix)\n"
            "- Features: Chinese-like keywords, DNA trace, three-color audit\n\n"
            "This repo is a minimal skeleton.\n"
        )
    if rel == "QUICK_START.md":
        return (
            "# Quick Start\n\n"
            "1) python3 cnsh_oneclick.py --init --root ./CNSH\n"
            "2) python3 cnsh_oneclick.py --emit\n"
        )
    if rel == "PROJECT_STRUCTURE.md":
        return (
            "# Project Structure\n\n"
            "CNSH/\n"
            "  index.html\n"
            "  assets/\n"
            "  cnsh/\n"
            "  editor/\n"
            "  audit/\n"
            "  dna/\n"
            "  plugins/\n"
            "  docs/\n"
            "  tools/\n"
        )
    if rel == "CNSH_BOOTSTRAP.md":
        return (
            "# Bootstrap Plan\n\n"
            "Phase 1: JS/Python toolchain builds initial CNSH.\n"
            "Phase 2: rewrite parts in CNSH (self-hosting).\n"
        )
    if rel == "index.html":
        return (
            "<!doctype html>\n"
            "<html>\n"
            "<head>\n"
            "  <meta charset=\"utf-8\" />\n"
            "  <title>CNSH</title>\n"
            "</head>\n"
            "<body>\n"
            "  <h1>CNSH Home</h1>\n"
            "</body>\n"
            "</html>\n"
        )
    if rel.endswith("/.keep"):
        return ""
    return None

def init_project(root: Path) -> Dict[str, Any]:
    """
    Create project skeleton on disk.
    (zh: chuang jian xiang mu gu jia)
    """
    created: List[str] = []
    skipped: List[str] = []
    tree = make_skeleton_tree(root)

    for rel in tree:
        p = root / rel
        if p.exists():
            skipped.append(rel)
            continue
        if rel.endswith("/.keep"):
            p.parent.mkdir(parents=True, exist_ok=True)
            safe_write_text(p, "")
            created.append(rel)
            continue
        content = skeleton_file_content(rel)
        if content is None:
            skipped.append(rel)
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        safe_write_text(p, content)
        created.append(rel)

    return {"root": str(root), "created": created, "skipped": skipped}

# ----------------------------- CLI ------------------------------------------
def parse_args(argv: List[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="CNSH one-click executor (ASCII-only source).")
    p.add_argument("--uid", default="9622")
    p.add_argument("--dna-prefix", default="#ZHUGEXIN-")  # ASCII-only (zh: ASCII qian zhui)
    p.add_argument("--confirm", default="#CONFIRM-9622-ONLY-ONCE-LK9X-772Z")
    p.add_argument("--gpg", default="A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
    p.add_argument("--sha256", default="b83c74d108660082581f9ebbb9506f65849d9d48d21d328daf13f7c4d66cf6c1")

    p.add_argument("--input", default="", help="Optional input text/file to audit.")
    p.add_argument("--input-is-file", action="store_true", help="Treat --input as file path.")

    p.add_argument("--emit", action="store_true", help="Emit JSON output to stdout.")
    p.add_argument("--out", default="", help="Optional output file path for JSON.")
    p.add_argument("--init", action="store_true", help="Initialize project skeleton.")
    p.add_argument("--root", default="./CNSH", help="Root folder for skeleton.")

    p.add_argument("--max-bytes", type=int, default=2_000_000, help="Max input file size in bytes.")
    return p.parse_args(argv)

def read_input_text(arg: str, is_file: bool, max_bytes: int) -> str:
    """
    Read optional input text to audit.
    (zh: du ru shen ji nei rong)
    """
    if not arg:
        return ""
    if is_file:
        return safe_read_text(Path(arg), max_bytes=max_bytes)
    # If arg is a literal, enforce it is valid UTF-8 by encode/decode roundtrip.
    b = str(arg).encode("utf-8", errors="strict")
    return b.decode("utf-8", errors="strict")

def emit_json(out_obj: Dict[str, Any], out_path: str) -> None:
    """
    Emit JSON to stdout or file.
    (zh: shu chu JSON)
    """
    text = json.dumps(out_obj, ensure_ascii=False, indent=2) + "\n"
    if out_path:
        safe_write_text(Path(out_path), text)
    else:
        u8_write(text)

def main(argv: List[str]) -> int:
    force_utf8_io()
    args = parse_args(argv)

    audit = ThreeColorAudit()

    # Optional init skeleton (zh: chuang jian gu jia)
    init_result: Optional[Dict[str, Any]] = None
    if args.init:
        root = Path(args.root).expanduser().resolve()
        init_result = init_project(root)

    # Audit input if provided (zh: shen ji)
    input_text = read_input_text(args.input, args.input_is_file, args.max_bytes)
    finding = audit.check(input_text) if input_text else AuditFinding(
        level="GREEN",
        reason="no_input",
        action="ALLOW",
        pros_note="No input provided; nothing to audit.",  # (zh: wu shu ru)
        risks_note="Provide --input for real audit coverage.",  # (zh: jian yi ti gong)
    )

    payload = default_payload()
    payload["audit"] = {
        "level": finding.level,
        "reason": finding.reason,
        "action": finding.action,
        "pros_note": finding.pros_note,
        "risks_note": finding.risks_note,
    }
    if init_result is not None:
        payload["init"] = init_result

    out_obj = build_output(
        uid=args.uid,
        dna_prefix=args.dna_prefix,
        confirm_code=args.confirm,
        gpg_fpr=args.gpg,
        sha256_fpr=args.sha256,
        payload=payload,
    )

    if args.emit or (not args.init and not args.out and not args.input):
        # Default behavior: emit JSON if no explicit action is given.
        # (zh: mo ren shu chu)
        emit_json(out_obj, args.out)

    # Exit code policy (zh: tui chu ma)
    if finding.level == "RED":
        return 2
    if finding.level == "YELLOW":
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
