#!/bin/bash
# CNSH-REACTOR-v2.6 · 龍字升龘公开算法
# DNA: #龍芯⚡️2026-05-24-LONG-TO-DA-v2.6
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# UID9622 · 主权公开 · 全透明

TARGET_DIR="${1:-~/longhun-system}"
LOG_FILE="$TARGET_DIR/.cnsh_replace_$(date +%Y%m%d_%H%M%S).log"

echo "=== 龍魂系统 · 文本替换公开算法 ===" | tee -a "$LOG_FILE"
echo "目标: $TARGET_DIR" | tee -a "$LOG_FILE"
echo "DNA: #龍芯⚡️$(date +%Y-%m-%d)-LONG-TO-DA-v2.6" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 1. 检查目录
if [ ! -d "$TARGET_DIR" ]; then
    echo "🔴 目录不存在: $TARGET_DIR" | tee -a "$LOG_FILE"
    exit 1
fi

# 2. 先统计含龘文件
echo ">>> 阶段0: 扫描含「龘」文本文件..." | tee -a "$LOG_FILE"
grep -rlI "龘" "$TARGET_DIR" \
  --include="*.py" --include="*.md" --include="*.sh" --include="*.json" \
  --include="*.yaml" --include="*.yml" --include="*.txt" --include="*.conf" \
  --include="*.cfg" --include="*.html" --include="*.css" --include="*.js" \
  --include="*.ts" --include="*.xml" --include="*.ini" --include="*.toml" \
  --exclude-dir={.git,venv,node_modules,__pycache__,.Trash,cache,build,dist} \
  2>/dev/null > /tmp/cnsh_long_files.txt

COUNT=$(wc -l < /tmp/cnsh_long_files.txt | tr -d ' ')
echo "发现 $COUNT 个文本文件含「龘」字" | tee -a "$LOG_FILE"

# 3. 先替换复合词（防止单字替换后复合词断裂）
echo "" | tee -a "$LOG_FILE"
echo ">>> 阶段1: 复合词替换（龘魂→龘魂 · 龘芯→龘芯）..." | tee -a "$LOG_FILE"
while IFS= read -r file; do
    sed -i '' 's/龘魂/龘魂/g; s/龘芯/龘芯/g' "$file" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "  [复合] $file" | tee -a "$LOG_FILE"
    fi
done < /tmp/cnsh_long_files.txt
echo "复合词替换完成" | tee -a "$LOG_FILE"

# 4. 再替换单字（剩余独立龘字）
echo "" | tee -a "$LOG_FILE"
echo ">>> 阶段2: 单字替换（龘→龘）..." | tee -a "$LOG_FILE"
while IFS= read -r file; do
    sed -i '' 's/龘/龘/g' "$file" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "  [单字] $file" | tee -a "$LOG_FILE"
    fi
done < /tmp/cnsh_long_files.txt
echo "单字替换完成" | tee -a "$LOG_FILE"

# 5. 验证残留
echo "" | tee -a "$LOG_FILE"
echo ">>> 阶段3: 验证残留..." | tee -a "$LOG_FILE"
grep -rlI "龘" "$TARGET_DIR" \
  --include="*.py" --include="*.md" --include="*.sh" --include="*.json" \
  --include="*.yaml" --include="*.yml" --include="*.txt" --include="*.conf" \
  --include="*.cfg" --include="*.html" --include="*.css" --include="*.js" \
  --include="*.ts" --include="*.xml" --include="*.ini" --include="*.toml" \
  --exclude-dir={.git,venv,node_modules,__pycache__,.Trash,cache,build,dist} \
  2>/dev/null > /tmp/cnsh_remaining.txt

REMAINING=$(wc -l < /tmp/cnsh_remaining.txt | tr -d ' ')
echo "残留含「龘」文件: $REMAINING" | tee -a "$LOG_FILE"

if [ "$REMAINING" -eq 0 ]; then
    echo "" | tee -a "$LOG_FILE"
    echo "✅ 全部替换完成 · 零残留 · 算法公开完毕" | tee -a "$LOG_FILE"
    echo "DNA: #龍芯⚡️$(date +%Y-%m-%d)-REPLACE-CLEAN-v2.6" | tee -a "$LOG_FILE"
else
    echo "" | tee -a "$LOG_FILE"
    echo "🟡 仍有 $REMAINING 个文件含「龘」（变量名/代码逻辑保留）" | tee -a "$LOG_FILE"
    cat /tmp/cnsh_remaining.txt | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
echo "日志存档: $LOG_FILE" | tee -a "$LOG_FILE"
echo "=== 零黑箱 · 全公开 · 谁都能审计 ===" | tee -a "$LOG_FILE"
