#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·丙申·癸酉·乙卯·临-SEMANTIC-GUARD-SYNC-v∞-9F80C06F
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# CREATOR: UID9622
# PROTOCOL: 龍魂君子协议 · CC BY-NC-SA 4.0 · L0 世界老百姓最高
"""Sync semantic guard artifacts from project source to shared and skill directories."""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

BIN_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BIN_DIR.parent
PROTO_DIR = PROJECT_ROOT / "01_protocols" / "semantic_guard"

SHARED_DIR = Path.home() / ".longhun" / "config" / "semantic_guard"
SKILL_DIR = Path.home() / ".kimi-code" / "skills" / "longhun-tongxinyi" / "data"

SKILL_ROOT = Path.home() / ".kimi-code" / "skills" / "longhun-tongxinyi"

ARTIFACTS = [
    (PROTO_DIR / "tongxin_guard_rules.json", SHARED_DIR / "tongxin_guard_rules.json"),
    (PROTO_DIR / "tongxin_guard_rules.json", SKILL_DIR / "tongxin_guard_rules.json"),
    (PROTO_DIR / "rule_template_schema.json", SHARED_DIR / "rule_template_schema.json"),
    (PROTO_DIR / "rule_template_schema.json", SKILL_ROOT / "rule_template_schema.json"),
    (PROTO_DIR / "rule_template.example.json", SHARED_DIR / "rule_template.example.json"),
    (PROTO_DIR / "rule_template.example.json", SKILL_ROOT / "rule_template.example.json"),
]


def sync(audit: bool = True):
    ok = True
    for src, dst in ARTIFACTS:
        if not src.exists():
            print(f"🔴 Source missing: {src}")
            ok = False
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"✅ {src.name} -> {dst}")

    if audit:
        print("\n🔍 Running post-sync audit...")
        auditor = BIN_DIR / "lh_sg_auditor.py"
        for target in [PROTO_DIR / "tongxin_guard_rules.json", SHARED_DIR / "tongxin_guard_rules.json", SKILL_DIR / "tongxin_guard_rules.json"]:
            if not target.exists():
                continue
            ret = subprocess.run([sys.executable, str(auditor), str(target)], capture_output=True, text=True)
            if ret.returncode == 0:
                print(f"🟢 {target.name}: audit passed")
            else:
                print(f"🔴 {target.name}: audit failed")
                print(ret.stdout)
                ok = False
    return ok


def main():
    parser = argparse.ArgumentParser(description="Sync semantic guard artifacts.")
    parser.add_argument("--no-audit", action="store_true", help="Skip post-sync audit")
    args = parser.parse_args()

    if not sync(audit=not args.no_audit):
        sys.exit(1)
    print("\n🟢 Sync complete.")


if __name__ == "__main__":
    main()
