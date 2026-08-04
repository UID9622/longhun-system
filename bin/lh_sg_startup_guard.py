#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·丙申·癸酉·丙辰·临-SEMANTIC-GUARD-STARTUP-GUARD-v∞-494EF148
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# CREATOR: UID9622
# PROTOCOL: 龍魂君子协议 · CC BY-NC-SA 4.0 · L0 世界老百姓最高
"""Startup guard: any Agent/ASI must pass semantic guard audit before loading."""
import subprocess
import sys
from pathlib import Path

BIN_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BIN_DIR.parent
AUDITOR = BIN_DIR / "lh_sg_auditor.py"

# Search order: project source -> shared config
RULE_PATHS = [
    PROJECT_ROOT / "01_protocols" / "semantic_guard" / "tongxin_guard_rules.json",
    Path.home() / ".longhun" / "config" / "semantic_guard" / "tongxin_guard_rules.json",
]

TIMEOUT_SECONDS = 5


def _find_rule_file() -> Path | None:
    for path in RULE_PATHS:
        if path.exists():
            return path
    return None


def enforce() -> None:
    """Enforce semantic guard audit at Agent/ASI startup.

    If tongxin_guard_rules.json exists, run lh_sg_auditor.py with a 5-second
    timeout. Exit code 0 allows startup; any non-zero exit or timeout terminates
    the process with Exit 1. No silent degradation or skip is permitted.
    """
    rule_file = _find_rule_file()
    if rule_file is None:
        print("[lh_sg_startup_guard] tongxin_guard_rules.json not found; skipping guard.")
        return

    if not AUDITOR.exists():
        print(f"[lh_sg_startup_guard] 🔴 Auditor missing: {AUDITOR}")
        sys.exit(1)

    print(f"[lh_sg_startup_guard] Running audit on {rule_file} ...")
    try:
        result = subprocess.run(
            [sys.executable, str(AUDITOR), str(rule_file)],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        print(f"[lh_sg_startup_guard] 🔴 Audit timed out after {TIMEOUT_SECONDS}s")
        sys.exit(1)
    except Exception as e:
        print(f"[lh_sg_startup_guard] 🔴 Audit failed to run: {e}")
        sys.exit(1)

    if result.returncode != 0:
        print(f"[lh_sg_startup_guard] 🔴 Audit failed (exit {result.returncode}). Startup aborted.")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(1)

    print("[lh_sg_startup_guard] 🟢 Audit passed. Startup allowed.")


def main():
    enforce()


if __name__ == "__main__":
    main()
