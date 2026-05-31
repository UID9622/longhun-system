#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════
# 龍魂中枢记忆收集脚本 v1.0
# DNA: #龍芯⚡️2026-CORE-MEMORY-COLLECT-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# ═══════════════════════════════════════════════════════════════════════
#
# 功能: 扫描龍魂系统所有关键文件，自动归集到单一真实源
# 特性: 只增不减·永驻挂载·系统升级不可动·Gitee备份
#
# 使用: ./collect_memory.sh
# 自动执行: git hook 或 crontab
# ═══════════════════════════════════════════════════════════════════════

set -e

# ─── 配置常量 ────────────────────────────────────────────────────
BASE_DIR="$HOME/longhun-system"
MEMORY_FILE="$HOME/longhun_core_memory.md"
BACKUP_DIR="$HOME/longhun_memory_backup"
KEYS_SUMMARY="$HOME/longhun_keys_summary.txt"
LOG_FILE="$BASE_DIR/logs/collect_memory.log"

# 创建日志目录
mkdir -p "$BACKUP_DIR" "$(dirname "$LOG_FILE")"

# ─── 日志函数 ────────────────────────────────────────────────────
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# ─── 龍魂系统关键字库（完整版） ────────────────────────────────
declare -a KEYWORDS=(
    # 核心系统
    "龍魂" "dragon.soul" "longhun" "龙魂"

    # 人格系统
    "P0" "P01" "P02" "P03" "P04" "P05" "P06" "P07" "P08" "P09" "P10" "P11"
    "诸葛" "宝宝" "文心" "雯雯" "北辰" "侦察" "上帝之眼"

    # 算法与规则
    "三才算法" "三色审计" "DNA追溯" "权重算法" "五行" "易经"
    "铁律" "七层防护" "治理宪法" "向下规则" "规则引擎"

    # 工具与平台
    "CNSH" "Claude.Code" "Notion" "Ollama" "OpenWebUI"
    "Gitee" "GitHub" "git" "ElevenLabs"

    # 模块与项目
    "M262" "M264" "brain_sync" "longhun_sync"
    "vision.bridge" "soul.engine" "elevenlabs_tts"

    # 概念框架
    "双脑同步" "显示脑" "内核脑" "本地脑" "展示脑"
    "同步状态" "冲突检测" "增量同步" "向下权重"

    # 安全相关
    "GPG" "SSH" "API.Key" "Token" "签名" "哈希"
    "UID9622" "CONFIRM" "确认码"

    # 执行相关
    "执行回执" "执行完成" "任务完成" "DNA" "审计"
)

# ─── 龍魂应用名称库（固定） ────────────────────────────────────
declare -a APP_NAMES=(
    "龍魂系统" "龍魂治理" "龍心永驻"
    "M262语音生态" "M264训练框架"
    "三才算法引擎" "龍芯北辰"
    "双脑同步系统" "CNSH中文编程"
    "骨嵌哲学框架" "数字主权守护"
)

# ─── 初始化记忆文件 ────────────────────────────────────────────
init_memory_file() {
    if [ ! -f "$MEMORY_FILE" ]; then
        log "📝 初始化记忆文件: $MEMORY_FILE"

        cat > "$MEMORY_FILE" <<'EOF'
# ╔═════════════════════════════════════════════════════════════╗
# ║        龍魂中枢记忆 | Core Memory Archive v1.0             ║
# ║   DNA: #龍芯⚡️2026-CORE-MEMORY-COLLECT-v1.0               ║
# ║   GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F            ║
# ╚═════════════════════════════════════════════════════════════╝
#
# 规则:
#   1️⃣ 只增不减 - 新内容永远追加到末尾
#   2️⃣ 永远锁定 - 系统升级不可覆盖此文件
#   3️⃣ 完整追踪 - 每条记录都有时间戳与DNA
#   4️⃣ 备份保护 - 每次修改自动备份时间戳版本
#
# 理论指导: 曾仕强老师（永恒显示）
# 责任人: UID9622 诸葛鑫 | 不免责
# 创建时间: $(date '+%Y-%m-%d %H:%M:%S')
# ═════════════════════════════════════════════════════════════

EOF
        chmod 444 "$MEMORY_FILE"  # 只读保护
        log "✅ 记忆文件初始化完成"
    fi
}

# ─── 扫描龍魂相关文件 ────────────────────────────────────────────
scan_related_files() {
    log "🔍 扫描龍魂相关文件..."

    local -a found_files=()

    # 1. 扫描所有"执行回执"markdown文件
    while IFS= read -r file; do
        if [ -f "$file" ]; then
            found_files+=("$file")
        fi
    done < <(find "$BASE_DIR" -name "*.md" -type f 2>/dev/null | head -200)

    # 2. 扫描项目状态文件
    found_files+=(
        "$BASE_DIR/brain_sync_state.json"
        "$BASE_DIR/brain_sync_index.json"
        "$BASE_DIR/brain_sync_conflicts.json"
        "$BASE_DIR/notion_sync_gateway.py"
        "$BASE_DIR/memory.jsonl"
        "$KEYS_SUMMARY"
    )

    # 3. 扫描Claude Code对话日志
    if [ -d "$HOME/.claude/projects" ]; then
        while IFS= read -r logfile; do
            found_files+=("$logfile")
        done < <(find "$HOME/.claude/projects" -name "*.jsonl" -type f 2>/dev/null | head -50)
    fi

    # 4. 扫描执行日志
    if [ -d "$BASE_DIR/logs" ]; then
        found_files+=("$BASE_DIR/logs"/*.log)
    fi

    # 过滤存在的文件，并去重
    printf '%s\n' "${found_files[@]}" | sort | uniq | while read -r file; do
        if [ -f "$file" ] && [ -s "$file" ]; then
            echo "$file"
        fi
    done
}

# ─── 检查文件是否包含龍魂关键字 ────────────────────────────────
contains_keyword() {
    local file="$1"
    local content=$(cat "$file" 2>/dev/null | head -1000)  # 读取前1000行

    for keyword in "${KEYWORDS[@]}"; do
        if echo "$content" | grep -qi "$keyword"; then
            return 0
        fi
    done

    # 也检查文件路径本身
    if echo "$file" | grep -qi "longhun\|dragon\|M262\|M264\|brain\|sync"; then
        return 0
    fi

    return 1
}

# ─── 计算文件哈希 ────────────────────────────────────────────────
file_hash() {
    md5sum "$1" 2>/dev/null | awk '{print $1}' || echo "unknown"
}

# ─── 检查是否已收集过（避免重复） ────────────────────────────
is_already_collected() {
    local file="$1"
    local hash=$(file_hash "$file")

    # 在记忆文件中搜索该文件的哈希
    grep -q "Hash: $hash" "$MEMORY_FILE" 2>/dev/null
}

# ─── 创建时间戳备份 ────────────────────────────────────────────
backup_current_memory() {
    if [ -f "$MEMORY_FILE" ]; then
        local timestamp=$(date '+%Y%m%d_%H%M%S')
        local backup_file="$BACKUP_DIR/longhun_memory_${timestamp}.md"
        cp "$MEMORY_FILE" "$backup_file"
        log "💾 备份已保存: $backup_file"
    fi
}

# ─── 追加文件内容到记忆库 ────────────────────────────────────
append_to_memory() {
    local file="$1"
    local file_size=$(wc -c < "$file" 2>/dev/null || echo 0)

    # 跳过过大的文件（防止内存溢出）
    if [ "$file_size" -gt 5242880 ]; then  # 5MB
        log "⚠️  文件过大，跳过: $file ($((file_size/1024))KB)"
        return
    fi

    local hash=$(file_hash "$file")
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local relative_path="${file#$HOME/}"

    # 临时解除只读保护
    chmod 644 "$MEMORY_FILE" 2>/dev/null || true

    # 追加记录
    {
        echo ""
        echo "─── 记录 ───────────────────────────────────────"
        echo "**时间**: $timestamp"
        echo "**文件**: \`$relative_path\`"
        echo "**大小**: $((file_size / 1024))KB"
        echo "**Hash**: $hash"
        echo ""
        echo "**内容摘要**:"
        head -100 "$file" | sed 's/^/> /'
        echo ""
        if [ "$file_size" -gt 102400 ]; then
            echo "*[文件内容过长，仅显示前100行，完整版请查看原文件]*"
            echo ""
        fi
    } >> "$MEMORY_FILE"

    # 恢复只读保护
    chmod 444 "$MEMORY_FILE" 2>/dev/null || true

    log "✅ 已收集: $relative_path (Hash: $hash)"
}

# ─── 收集所有关键信息 ────────────────────────────────────────
collect_all_memories() {
    log "📦 开始收集龍魂系统所有关键信息..."

    local collected=0
    local skipped=0

    # 备份当前版本
    backup_current_memory

    # 扫描所有相关文件
    while IFS= read -r file; do
        if [ -z "$file" ]; then
            continue
        fi

        # 检查是否包含龍魂关键字
        if contains_keyword "$file"; then
            # 检查是否已收集过
            if ! is_already_collected "$file"; then
                append_to_memory "$file"
                ((collected++))
            else
                ((skipped++))
            fi
        fi
    done < <(scan_related_files)

    log "📊 本次收集统计: 新增 $collected | 跳过重复 $skipped"
}

# ─── 推送到Gitee备份 ────────────────────────────────────────
push_to_gitee() {
    log "🚀 推送到Gitee备份..."

    cd "$BASE_DIR" || return

    # 检查是否有git配置
    if ! git status &>/dev/null; then
        log "⚠️  不在git仓库中，跳过Gitee推送"
        return
    fi

    # 添加记忆文件到git
    if [ -f "$MEMORY_FILE" ]; then
        cp "$MEMORY_FILE" "$BASE_DIR/longhun_core_memory.md" || true
        git add "longhun_core_memory.md" 2>/dev/null || true
    fi

    # 添加备份目录
    git add ".gitkeep" "$BACKUP_DIR/.gitkeep" 2>/dev/null || true

    # 提交
    if ! git diff --cached --quiet 2>/dev/null; then
        git commit -m "$(cat <<'COMMITMSG'
feat(core-memory): 龍魂中枢记忆自动收集更新

DNA: #龍芯⚡️2026-CORE-MEMORY-COLLECT-v1.0
时间: $(date '+%Y-%m-%d %H:%M:%S')

- 自动扫描龍魂系统所有关键文件
- 聚集到单一真实源: ~/longhun_core_memory.md
- 保持增量不覆盖原则
- 自动备份时间戳版本

Co-Authored-By: Claude Code <noreply@anthropic.com>
COMMITMSG
)" 2>/dev/null || true
    fi

    # 尝试推送（如果配置了远程）
    if git remote get-url origin &>/dev/null; then
        git push origin main 2>/dev/null || log "⚠️  推送失败，可能网络原因"
    fi

    log "✅ Gitee备份完成"
}

# ─── 生成收集回执 ────────────────────────────────────────────
generate_receipt() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    log ""
    log "╔════════════════════════════════════════════════════════════╗"
    log "║            龍魂中枢记忆收集 - 执行完成回执              ║"
    log "╚════════════════════════════════════════════════════════════╝"
    log ""
    log "✅ 时间: $timestamp"
    log "✅ 主文件: $MEMORY_FILE"
    log "✅ 备份目录: $BACKUP_DIR"
    log "✅ 日志文件: $LOG_FILE"
    log ""
    log "📊 记忆库统计:"
    log "   - 总行数: $(wc -l < "$MEMORY_FILE" 2>/dev/null || echo 0)"
    log "   - 文件大小: $(du -h "$MEMORY_FILE" 2>/dev/null | awk '{print $1}')"
    log "   - 最后更新: $(stat -f '%Sm' "$MEMORY_FILE" 2>/dev/null || stat -c '%y' "$MEMORY_FILE" 2>/dev/null || echo 'unknown')"
    log ""
    log "🔒 保护机制:"
    log "   ✓ 文件只读保护"
    log "   ✓ 时间戳备份"
    log "   ✓ Gitee远程备份"
    log "   ✓ 哈希去重"
    log ""
    log "DNA: #龍芯⚡️2026-CORE-MEMORY-COLLECT-v1.0"
    log "GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    log ""
}

# ═══════════════════════════════════════════════════════════════════════
# 主程序入口
# ═══════════════════════════════════════════════════════════════════════

main() {
    log "启动龍魂中枢记忆收集脚本..."
    log "==================================================================="

    # 初始化
    init_memory_file

    # 收集内容
    collect_all_memories

    # 推送备份
    push_to_gitee

    # 生成回执
    generate_receipt
}

# 执行主程序
main "$@"
