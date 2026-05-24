#!/usr/bin/env bash
# Exit 0 iff CANONICAL_SHA256 matches FULL_PAPER_v1.0_Body_Draft.md on disk.
# Paths in CANONICAL_SHA256 are relative to WORKTREE (BehavCrypto_v1.0/...).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKTREE="$(cd "$SCRIPT_DIR/../.." && pwd)"
BODY_REL="BehavCrypto_v1.0/FULL_PAPER_v1.0_Body_Draft.md"
SUM_REL="BehavCrypto_v1.0/CANONICAL_SHA256"
BODY="$WORKTREE/$BODY_REL"
SUM="$WORKTREE/$SUM_REL"
if [[ ! -f "$BODY" ]]; then
  echo "verify.sh: missing $BODY_REL under $WORKTREE" >&2
  exit 1
fi
if [[ ! -f "$SUM" ]]; then
  echo "verify.sh: missing $SUM_REL — run scripts/canonical-sha256/update.sh" >&2
  exit 1
fi
cd "$WORKTREE"
if command -v shasum >/dev/null 2>&1; then
  actual="$(shasum -a 256 "$BODY_REL" | awk '{print $1}')"
elif command -v sha256sum >/dev/null 2>&1; then
  actual="$(sha256sum "$BODY_REL" | awk '{print $1}')"
else
  echo "verify.sh: need shasum or sha256sum" >&2
  exit 1
fi
expected="$(awk 'NF>=2 && $1 ~ /^[a-f0-9]{64}$/ {print $1; exit}' "$SUM")"
if [[ -z "$expected" ]]; then
  echo "verify.sh: could not parse hash from $SUM_REL" >&2
  exit 1
fi
if [[ "$actual" != "$expected" ]]; then
  echo "verify.sh: CANONICAL_SHA256 mismatch for $BODY_REL" >&2
  echo "  expected (file): $expected" >&2
  echo "  actual   (disk): $actual" >&2
  echo "  run: (cd \"\$REPO_ROOT\") bash scripts/canonical-sha256/update.sh && git add <prefix>BehavCrypto_v1.0/CANONICAL_SHA256" >&2
  exit 1
fi
echo "verify.sh: OK — $BODY_REL matches CANONICAL_SHA256"
