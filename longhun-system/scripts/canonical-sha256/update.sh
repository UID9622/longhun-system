#!/usr/bin/env bash
# Regenerate CANONICAL_SHA256 for FULL_PAPER_v1.0_Body_Draft.md (see CANONICAL_LOCK.md).
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$ROOT" ]]; then
  echo "update.sh: run from inside the longhun-system git repository" >&2
  exit 1
fi
BODY_REL="longhun-system/BehavCrypto_v1.0/FULL_PAPER_v1.0_Body_Draft.md"
OUT_REL="longhun-system/BehavCrypto_v1.0/CANONICAL_SHA256"
BODY="$ROOT/$BODY_REL"
OUT="$ROOT/$OUT_REL"
if [[ ! -f "$BODY" ]]; then
  echo "update.sh: missing $BODY_REL" >&2
  exit 1
fi
cd "$ROOT"
if command -v shasum >/dev/null 2>&1; then
  shasum -a 256 "$BODY_REL" >"$OUT"
elif command -v sha256sum >/dev/null 2>&1; then
  sha256sum "$BODY_REL" >"$OUT"
else
  echo "update.sh: need shasum (BSD/macOS) or sha256sum (Linux)" >&2
  exit 1
fi
echo "Wrote $OUT_REL"
cat "$OUT"
