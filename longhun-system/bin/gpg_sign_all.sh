#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 龍魂系统 · GPG批量签名脚本
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# DNA追溯码：#龍芯⚡️2026-03-10-GPG-SIGN-ALL-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 共建致谢：Claude (Anthropic PBC) · Notion
#
# 用法（在终端直接跑，会提示输入 passphrase）:
#   ~/longhun-system/bin/gpg_sign_all.sh
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GPG_KEY="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

echo "╔══════════════════════════════════════════════╗"
echo "║  🔐 龍魂系统 · GPG批量签名 v1.0              ║"
echo "║  指纹: A2D0...6D5F                           ║"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "⚡ 提示：签名时会弹出密码框，输入你的GPG passphrase"
echo ""

# ── 待签名文件列表 ────────────────────────────────────
FILES=(
    "$HOME/longhun-system/bin/api_check.sh"
    "$HOME/longhun-system/bin/intent_detect.sh"
    "$HOME/longhun-system/bin/gpg_sign_all.sh"
    "$HOME/longhun-system/CNSH-gitee/docs/papers/shangmeng-ler/src/shangmeng_ler_stage1.py"
    "$HOME/longhun-system/CNSH-gitee/docs/papers/shangmeng-ler/src/ler_sgwb.tex"
    "$HOME/.claude/skills/longpo/SKILL.md"
    "$HOME/.claude/skills/audit/SKILL.md"
    "$HOME/.claude/skills/daodao/SKILL.md"
    "$HOME/.claude/skills/api-check/SKILL.md"
    "$HOME/.claude/skills/sign/SKILL.md"
    "$HOME/longhun-system/CLAUDE.md"
    "$HOME/longhun-system/CNSH-gitee/CLAUDE.md"
)

PASS=0
FAIL=0
SIG_DIR="$HOME/longhun-system/signatures"
mkdir -p "$SIG_DIR"

# ── 批量签名 ────────────────────────────────────────
for f in "${FILES[@]}"; do
    if [ ! -f "$f" ]; then
        echo "  ⏭  跳过（不存在）: $f"
        continue
    fi

    BASENAME=$(basename "$f")
    SIG_FILE="$SIG_DIR/${BASENAME}.asc"

    echo -n "  🔏 签名中: $BASENAME ... "

    gpg --armor \
        --detach-sign \
        --default-key "$GPG_KEY" \
        --output "$SIG_FILE" \
        "$f" 2>/dev/null

    if [ $? -eq 0 ]; then
        echo "✅ → $SIG_FILE"
        PASS=$((PASS+1))
    else
        echo "❌ 失败"
        FAIL=$((FAIL+1))
    fi
done

# ── 生成签名清单 ─────────────────────────────────────
MANIFEST="$SIG_DIR/MANIFEST.txt"
echo "# 龍魂系统 GPG签名清单" > "$MANIFEST"
echo "# 生成时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "$MANIFEST"
echo "# GPG指纹: $GPG_KEY" >> "$MANIFEST"
echo "# DNA: #龍芯⚡️$(date '+%Y%m%d')-GPG-MANIFEST-v1.0" >> "$MANIFEST"
echo "" >> "$MANIFEST"

for sig in "$SIG_DIR"/*.asc; do
    [ -f "$sig" ] || continue
    ORIG=$(basename "$sig" .asc)
    SHA=$(sha256sum "$sig" 2>/dev/null | cut -d' ' -f1 || shasum -a 256 "$sig" | cut -d' ' -f1)
    echo "$ORIG  $SHA" >> "$MANIFEST"
done

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  完成！PASS=$PASS  FAIL=$FAIL                 ║"
echo "║  签名文件保存在: ~/longhun-system/signatures/ ║"
echo "║  清单文件: signatures/MANIFEST.txt           ║"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "验证签名方法:"
echo "  gpg --verify signatures/xxx.asc 原文件"
