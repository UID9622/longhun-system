#!/usr/bin/env bash
# Regenerate CANONICAL_SHA256 for FULL_PAPER_v1.0_Body_Draft.md (see CANONICAL_LOCK.md).
# WORKTREE = directory that contains BehavCrypto_v1.0/ and scripts/ (repo root when longhun-system is the Git root).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKTREE="$(cd "$SCRIPT_DIR/../.." && pwd)"
BODY_REL="BehavCrypto_v1.0/FULL_PAPER_v1.0_Body_Draft.md"
OUT_REL="BehavCrypto_v1.0/CANONICAL_SHA256"
BODY="$WORKTREE/$BODY_REL"
OUT="$WORKTREE/$OUT_REL"
if [[ ! -f "$BODY" ]]; then
  echo "update.sh: missing $BODY_REL under $WORKTREE" >&2
  exit 1
fi
cd "$WORKTREE"
if command -v shasum >/dev/null 2>&1; then
  shasum -a 256 "$BODY_REL" >"$OUT"
elif command -v sha256sum >/dev/null 2>&1; then
  sha256sum "$BODY_REL" >"$OUT"
else
  echo "update.sh: need shasum (BSD/macOS) or sha256sum (Linux)" >&2
  exit 1
fi
echo "Wrote $OUT_REL (under $WORKTREE)"
cat "$OUT"
