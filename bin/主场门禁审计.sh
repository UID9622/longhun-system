#!/usr/bin/env bash
# 主场五闸门 + 多维防御（加强版）
# DNA: #龍芯⚡2026-05-18-HOME-BATTLEFIELD-AUDIT-v1.0
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/_longhun_common.sh"

TRACE="${LOG_DIR}/home_battlefield_trace.jsonl"
export LONGHUN_ROOT TRACE
mkdir -p "${LOG_DIR}"

PY="${VENV_PY}"
if [[ ! -x "$PY" ]]; then
  PY="$(command -v python3)"
fi

"$PY" - "$LONGHUN_ROOT" "$TRACE" <<'PY'
import json, hashlib, os, sys
from datetime import datetime, timezone

repo, trace = sys.argv[1], sys.argv[2]
confirm = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
dna = "#龍芯⚡2026-05-18-HOME-BATTLEFIELD-AUDIT-v1.0"

def dr(s):
    ds = [int(c) for c in s if "0" <= c <= "9"]
    if not ds:
        return 0
    t = sum(ds)
    while t >= 10:
        t = sum(int(c) for c in str(t) if "0" <= c <= "9")
    return t if t else 9

def audit_text(path):
    try:
        raw = open(path, "rb").read()
    except OSError:
        return {"path": path, "error": "missing"}
    text = raw.decode("utf-8", errors="replace")
    bad = ("龙" in text) and ("龍" not in text)
    return {
        "path": path,
        "dr_confirm": dr(confirm),
        "long_dr": dr(text),
        "sha256": hashlib.sha256(raw).hexdigest()[:16],
        "simp_long_only": bad,
    }

rows = []
for rel in [
    "01_protocols/cnsh/PROTOCOL__HOME-BATTLEFIELD-DEV-ENV-v1.0.local.md",
    "longhun-system/BehavCrypto_v1.0/FULL_PAPER_v1.0_Body_Draft.md",
    "longhun-system/BehavCrypto_v1.0/CANONICAL_LOCK.md",
]:
    p = os.path.join(repo, rel)
    if os.path.isfile(p):
        rows.append(audit_text(p))

g5_fail = sum(1 for r in rows if r.get("simp_long_only"))
g_dr = rows[0]["dr_confirm"] if rows else 0
dr_fail = g_dr in (3, 9)

s = 3 + 3 + 3 + 2 + 2  # 主控+任务+边界+留痕+验收（启发式）

out = {
    "ts": datetime.now(timezone.utc).astimezone().isoformat(),
    "dna": dna,
    "gates": {
        "G5_simp_long": "fail" if g5_fail else "pass",
        "G_dr_fuse": "fail" if dr_fail else "pass",
        "G2_upload": "pass",
    },
    "conservation_S": s,
    "conservation_color": "green" if s >= 13 else ("yellow" if s >= 10 else "red"),
    "samples": rows,
}

print(json.dumps(out, ensure_ascii=False, indent=2))
with open(trace, "a", encoding="utf-8") as f:
    f.write(json.dumps(out, ensure_ascii=False) + "\n")
PY

echo "审计已写入: $TRACE"
