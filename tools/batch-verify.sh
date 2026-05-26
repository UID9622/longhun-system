#!/bin/bash
# 龍魂批量验签系统 · GPG签名验证流水线
# DNA: #龍芯⚡️2026-05-26-batch-verify-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# UID: 9622 · 诸葛鑫

set -e

ROOT_DIR="${1:-.}"
LOG_FILE="batch_verify_$(date +%Y%m%d_%H%M%S).log"

echo "========================================================================"
echo "龍魂批量验签系统 · GPG签名验证流水线 v1.0"
echo "========================================================================"
echo ""
echo "[📂] 扫描范围: $ROOT_DIR"
echo "[📝] 日志文件: $LOG_FILE"
echo ""

total=0
success=0
failed=0

# 递归扫描所有.sig文件
while IFS= read -r sig_file; do
    md_file="${sig_file%.sig}"

    if [[ ! -f "$md_file" ]]; then
        echo "[❌] 原文件缺失: $md_file" | tee -a "$LOG_FILE"
        ((failed++))
        continue
    fi

    # 验签
    if gpg --verify "$sig_file" "$md_file" &>/dev/null; then
        rel_path=$(echo "$md_file" | sed "s|^$ROOT_DIR/||")
        echo "[✅] 验签通过: $rel_path" | tee -a "$LOG_FILE"
        ((success++))
    else
        echo "[❌] 验签失败: $md_file" | tee -a "$LOG_FILE"
        ((failed++))
    fi

    ((total++))
done < <(find "$ROOT_DIR" -name "*.sig" -type f | sort)

echo ""
echo "========================================================================"
echo "[📊] 验签统计"
echo "    总签名数: $total"
echo "    验签成功: $success"
echo "    验签失败: $failed"
echo "========================================================================"
