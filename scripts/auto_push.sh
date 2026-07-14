#!/bin/bash
# 龍魂·自动推送 v1.0 · 密钥自检+四地推送
# DNA: #龍芯⚡️丙午·辛未·乙酉·亥-AUTO-PUSH-v1.0
# 用法: bash scripts/auto_push.sh

set -e
cd "$(dirname "$0")/.."

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() { echo -e "${GREEN}[+]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err() { echo -e "${RED}[x]${NC} $1"; }

echo "═══════════════════════════════════════"
echo "  龍魂·自动推送 · 密钥自检先行"
echo "═══════════════════════════════════════"

# ─── 阶段0: 密钥自检 ───
log "阶段0: 密钥自检..."
SECRETS_FOUND=0
for pattern in 'ntn_[0-9a-zA-Z]{20,}' 'sk-[A-Za-z0-9]{30,}' 'ghp_[A-Za-z0-9]{30,}' 'gho_[A-Za-z0-9]{30,}' 'AKIA[A-Za-z0-9]{16,}'; do
  HITS=$(git ls-files | xargs grep -lE "$pattern" 2>/dev/null | grep -v "ntn_xxxxxxxx\|ntn_\.\.\.\|ntn_test\|ntn_.*example\|scripts/auto_push" || true)
  if [ -n "$HITS" ]; then
    while IFS= read -r f; do
      # 检查是否是真实token还是占位符
      REAL=$(grep -cE "$pattern" "$f" 2>/dev/null | head -1)
      MATCHES=$(grep -nE "$pattern" "$f" 2>/dev/null | grep -v "ntn_xxxxxxxx\|ntn_\.\.\.\|ntn_test\|ntn_.*example\|placeholder\|redacted\|示例\|占位" || true)
      if [ -n "$MATCHES" ]; then
        err "疑似密钥泄露: $f"
        echo "$MATCHES" | while read line; do
          echo "  $line" | sed 's/ntn_[0-9a-zA-Z]\{10,\}/ntn_[REDACTED]/g'
        done
        SECRETS_FOUND=1
      fi
    done <<< "$HITS"
  fi
done

if [ "$SECRETS_FOUND" -eq 1 ]; then
  err "密钥自检未通过，已中止推送！"
  err "请用占位符替换真实token后重试"
  exit 1
fi
log "密钥自检通过 ✓"

# ─── 阶段1: 暂存并提交 ───
log "阶段1: 检查未提交变更..."
if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
  git add -A
  git commit -m "自動推送·變更同步·$(date '+%Y-%m-%d %H:%M')" 2>/dev/null || true
  log "已提交本地变更"
else
  log "无本地变更"
fi

# ─── 阶段2: 推送 ───
REMOTES=(
  "origin:git@github.com:UID9622/longhun-system.git"
  "gitcode:git@gitcode.com:UID9622/longhun-system.git"
  "gitee:git@gitee.com:uid9622_admin/longhun-system-core.git"
)

PUSH_OK=0
PUSH_FAIL=0

for remote_def in "${REMOTES[@]}"; do
  REMOTE_NAME="${remote_def%%:*}"
  REMOTE_URL="${remote_def#*:}"
  
  # 确保remote存在
  if ! git remote get-url "$REMOTE_NAME" &>/dev/null; then
    git remote add "$REMOTE_NAME" "$REMOTE_URL" 2>/dev/null || warn "无法添加远程: $REMOTE_NAME"
  fi
  
  echo ""
  log "推送 → $REMOTE_NAME ($REMOTE_URL)"
  
  if git push "$REMOTE_NAME" main --force 2>&1; then
    log "✓ $REMOTE_NAME 推送成功"
    PUSH_OK=$((PUSH_OK + 1))
  else
    err "✗ $REMOTE_NAME 推送失败"
    PUSH_FAIL=$((PUSH_FAIL + 1))
  fi
done

# ─── 汇总 ───
echo ""
echo "═══════════════════════════════════════"
echo "  推送汇总: ✓${PUSH_OK} ✗${PUSH_FAIL}"
echo "═══════════════════════════════════════"

if [ "$PUSH_FAIL" -gt 0 ]; then
  exit 1
fi
log "全部推送完成"
echo ""
echo "DNA: #龍芯⚡️丙午·辛未·乙酉·亥-AUTO-PUSH-v1.0"
echo "确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
