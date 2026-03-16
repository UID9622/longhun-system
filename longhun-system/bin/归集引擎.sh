#!/bin/bash
# ═══════════════════════════════════════════════════════════
# 🐉 龙魂系统 · P0伦理锚点
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# DNA:    #龍芯⚡️2026-03-16-ETHICS-STAMP-v1.0
# 作者:    诸葛鑫（UID9622）
# 理论:    曾仕强老师（永恒显示）
#
# P0铁律: 守正·稳态·永恒锚·零毁伤·三色监测
# ═══════════════════════════════════════════════════════════
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🐉 龍魂数据归集引擎 v1.0
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DNA追溯码: #龍芯⚡️
# GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 共建致谢：Claude (Anthropic PBC) · Notion
# 创建者: UID9622
# 版本: 1.0
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# 功能:
#   - 扫描本地所有AI导出文件 (ChatGPT、Claude、Notion)
#   - 自动识别类型并分类
#   - SHA256去重
#   - 生成带DNA追溯码的完整清单
#
# 用法:
#   ./归集引擎.sh [选项]
#
# 选项:
#   -s, --scan     仅扫描，不移动文件
#   -m, --move     扫描并移动到归集目录
#   -d, --dedup    执行去重
#   -a, --all      执行全部操作
#   -h, --help     显示帮助
#
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# set -e  # 禁用自动退出，改用手动错误处理
set +e

# ═══════════════════════════════════════════════════════════════════
# 配置区
# ═══════════════════════════════════════════════════════════════════

# DNA追溯信息
DNA_CODE="#龍芯⚡️"
GPG_FP="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
UID_CODE="9622"
VERSION="1.0"

# 扫描目录
SCAN_DIRS=(
    "$HOME/Downloads"
    "$HOME/Desktop"
    "$HOME/Documents"
    "$HOME/longhun-system"
    "/Volumes/LonghunDisk"
)

# 输出目录
OUTPUT_DIR="$HOME/longhun-system/数据归集"
ARCHIVE_DIR="$OUTPUT_DIR/归档"
DEDUP_DIR="$OUTPUT_DIR/去重备份"
LOG_DIR="$OUTPUT_DIR/logs"

# 清单文件
MANIFEST_FILE="$OUTPUT_DIR/归集清单_$(date +%Y%m%d_%H%M%S).md"
JSON_MANIFEST="$OUTPUT_DIR/归集清单_$(date +%Y%m%d_%H%M%S).json"
HASH_DB="$OUTPUT_DIR/.hash_database.json"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# ═══════════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════════

print_banner() {
    echo -e "${CYAN}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🐉 龍魂数据归集引擎 v${VERSION}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "  DNA: ${GREEN}${DNA_CODE}${CYAN}"
    echo -e "  GPG: ${YELLOW}${GPG_FP}${CYAN}"
    echo -e "  UID: ${MAGENTA}${UID_CODE}${CYAN}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${NC}"
}

print_section() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}\n"
}

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 计算SHA256
calc_sha256() {
    local file="$1"
    if [[ -f "$file" ]]; then
        shasum -a 256 "$file" 2>/dev/null | awk '{print $1}'
    fi
}

# 格式化文件大小
format_size() {
    local size=$1
    if (( size >= 1073741824 )); then
        printf "%.2f GB" $(echo "scale=2; $size/1073741824" | bc)
    elif (( size >= 1048576 )); then
        printf "%.2f MB" $(echo "scale=2; $size/1048576" | bc)
    elif (( size >= 1024 )); then
        printf "%.2f KB" $(echo "scale=2; $size/1024" | bc)
    else
        printf "%d B" $size
    fi
}

# ═══════════════════════════════════════════════════════════════════
# 导出包识别模式
# ═══════════════════════════════════════════════════════════════════

# ChatGPT 导出特征
identify_chatgpt() {
    local path="$1"
    local name=$(basename "$path")

    # ChatGPT导出通常包含 conversations.json
    if [[ -d "$path" ]]; then
        if [[ -f "$path/conversations.json" ]] || [[ -f "$path/chat.html" ]]; then
            echo "ChatGPT导出包"
            return 0
        fi
    fi

    # ZIP包检测
    if [[ "$name" =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}.*\.zip$ ]]; then
        echo "ChatGPT导出ZIP"
        return 0
    fi

    if [[ "$name" =~ chatgpt|openai|gpt-export ]]; then
        echo "ChatGPT相关"
        return 0
    fi

    return 1
}

# Claude 导出特征
identify_claude() {
    local path="$1"
    local name=$(basename "$path")

    # Claude导出JSON
    if [[ "$name" =~ ^[0-9a-f]{64}-.*\.json$ ]]; then
        echo "Claude对话导出"
        return 0
    fi

    if [[ "$name" =~ claude|anthropic ]]; then
        echo "Claude相关"
        return 0
    fi

    # Claude Code会话
    if [[ -d "$path/.claude" ]]; then
        echo "Claude Code项目"
        return 0
    fi

    return 1
}

# Notion 导出特征
identify_notion() {
    local path="$1"
    local name=$(basename "$path")

    # Notion导出ZIP
    if [[ "$name" =~ ^Export-[0-9a-f]{8}-.*\.zip$ ]]; then
        echo "Notion导出ZIP"
        return 0
    fi

    # Notion导出目录
    if [[ -d "$path" ]]; then
        if [[ "$name" =~ ^Export-[0-9a-f]{8} ]]; then
            echo "Notion导出目录"
            return 0
        fi
        # 检查是否包含Notion特征文件
        if ls "$path"/*.md 2>/dev/null | head -1 | grep -q "[0-9a-f]\{32\}"; then
            echo "Notion页面集"
            return 0
        fi
    fi

    if [[ "$name" =~ notion|Notion ]]; then
        echo "Notion相关"
        return 0
    fi

    return 1
}

# 其他导出类型识别
identify_other_exports() {
    local path="$1"
    local name=$(basename "$path")

    # GitHub导出
    if [[ "$name" =~ \.git$ ]] || [[ -d "$path/.git" ]]; then
        echo "Git仓库"
        return 0
    fi

    # Obsidian
    if [[ -d "$path/.obsidian" ]]; then
        echo "Obsidian库"
        return 0
    fi

    # 各种备份
    if [[ "$name" =~ backup|备份|Backup ]]; then
        echo "备份文件"
        return 0
    fi

    return 1
}

# 综合识别
identify_export_type() {
    local path="$1"
    local result=""

    result=$(identify_chatgpt "$path") && echo "$result" && return 0
    result=$(identify_claude "$path") && echo "$result" && return 0
    result=$(identify_notion "$path") && echo "$result" && return 0
    result=$(identify_other_exports "$path") && echo "$result" && return 0

    # 按扩展名分类
    local ext="${path##*.}"
    case "$ext" in
        json) echo "JSON数据" ;;
        md) echo "Markdown文档" ;;
        zip|tar|gz|7z) echo "压缩包" ;;
        pdf) echo "PDF文档" ;;
        py|js|sh) echo "代码文件" ;;
        *) echo "其他文件" ;;
    esac
}

# ═══════════════════════════════════════════════════════════════════
# 核心功能
# ═══════════════════════════════════════════════════════════════════

# 初始化目录
init_directories() {
    log_info "初始化归集目录..."

    mkdir -p "$OUTPUT_DIR"
    mkdir -p "$ARCHIVE_DIR"/{ChatGPT,Claude,Notion,Git,Obsidian,备份,其他}
    mkdir -p "$DEDUP_DIR"
    mkdir -p "$LOG_DIR"

    log_info "目录结构已创建: $OUTPUT_DIR"
}

# 扫描导出文件
scan_exports() {
    print_section "📂 扫描导出文件"

    local total_files=0
    local chatgpt_count=0
    local claude_count=0
    local notion_count=0
    local other_count=0

    # 临时文件存储扫描结果
    local scan_result="/tmp/龙魂归集_scan_$$.json"
    echo "[]" > "$scan_result"

    for scan_dir in "${SCAN_DIRS[@]}"; do
        if [[ ! -d "$scan_dir" ]]; then
            log_warn "目录不存在，跳过: $scan_dir"
            continue
        fi

        log_info "扫描: $scan_dir"

        # 查找潜在的导出文件
        while IFS= read -r -d '' file; do
            local filename=$(basename "$file")
            local export_type=$(identify_export_type "$file")
            local file_size=$(stat -f%z "$file" 2>/dev/null || echo 0)
            local file_hash=""

            # 快速扫描模式不计算哈希
            # file_hash=$(calc_sha256 "$file")  # 在清单生成时再计算

            # 分类计数
            case "$export_type" in
                *ChatGPT*) ((chatgpt_count++)) ;;
                *Claude*) ((claude_count++)) ;;
                *Notion*) ((notion_count++)) ;;
                *) ((other_count++)) ;;
            esac

            ((total_files++))

            # 输出进度
            if (( total_files % 100 == 0 )); then
                echo -ne "\r   已扫描: $total_files 个文件..."
            fi

        done < <(find "$scan_dir" -maxdepth 4 \( \
            -name "*.json" -o \
            -name "*.zip" -o \
            -name "*.md" -o \
            -name "conversations.json" -o \
            -name "Export-*" -o \
            -name "*chatgpt*" -o \
            -name "*claude*" -o \
            -name "*notion*" -o \
            -name "*backup*" -o \
            -name "*备份*" \
        \) -print0 2>/dev/null)
    done

    echo ""
    log_info "扫描完成!"
    echo ""
    echo -e "  ${GREEN}ChatGPT 导出:${NC} $chatgpt_count"
    echo -e "  ${BLUE}Claude 导出:${NC} $claude_count"
    echo -e "  ${YELLOW}Notion 导出:${NC} $notion_count"
    echo -e "  ${MAGENTA}其他文件:${NC} $other_count"
    echo -e "  ${CYAN}总计:${NC} $total_files"

    # 返回统计
    echo "$chatgpt_count:$claude_count:$notion_count:$other_count:$total_files"
}

# 深度扫描并生成清单
deep_scan_and_manifest() {
    print_section "📋 生成归集清单"

    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local scan_id=$(date +%Y%m%d%H%M%S)

    # 初始化清单
    cat > "$MANIFEST_FILE" << MANIFEST_HEADER
# 🐉 龍魂数据归集清单

\`\`\`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DNA追溯码: ${DNA_CODE}
GPG指纹: ${GPG_FP}
UID: ${UID_CODE}
扫描ID: ${scan_id}
生成时间: ${timestamp}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
\`\`\`

## 扫描范围

MANIFEST_HEADER

    for dir in "${SCAN_DIRS[@]}"; do
        echo "- \`$dir\`" >> "$MANIFEST_FILE"
    done

    echo "" >> "$MANIFEST_FILE"

    # JSON清单初始化
    cat > "$JSON_MANIFEST" << JSON_HEADER
{
  "meta": {
    "dna": "${DNA_CODE}",
    "gpg": "${GPG_FP}",
    "uid": "${UID_CODE}",
    "scan_id": "${scan_id}",
    "generated_at": "${timestamp}",
    "version": "${VERSION}"
  },
  "statistics": {},
  "files": []
}
JSON_HEADER

    # 分类统计
    declare -A type_counts
    declare -A type_sizes
    declare -A hash_index
    local duplicates=0
    local unique_files=0
    local total_size=0

    echo "## 文件清单" >> "$MANIFEST_FILE"
    echo "" >> "$MANIFEST_FILE"

    # 按类型分组
    local current_type=""

    for scan_dir in "${SCAN_DIRS[@]}"; do
        [[ ! -d "$scan_dir" ]] && continue

        log_info "深度扫描: $scan_dir"

        while IFS= read -r -d '' file; do
            local filename=$(basename "$file")
            local export_type=$(identify_export_type "$file")
            local file_size=$(stat -f%z "$file" 2>/dev/null || echo 0)
            local file_mtime=$(stat -f%m "$file" 2>/dev/null || echo 0)
            local file_date=$(date -r "$file_mtime" '+%Y-%m-%d %H:%M' 2>/dev/null || echo "未知")
            local file_hash=""
            local is_dup="否"

            # 计算哈希 (文件<100MB)
            if [[ -f "$file" ]] && (( file_size < 104857600 )); then
                file_hash=$(calc_sha256 "$file")

                # 检查重复
                if [[ -n "$file_hash" ]] && [[ -n "${hash_index[$file_hash]}" ]]; then
                    is_dup="是"
                    ((duplicates++))
                else
                    hash_index[$file_hash]="$file"
                    ((unique_files++))
                fi
            else
                file_hash="[文件过大]"
                ((unique_files++))
            fi

            # 统计
            ((type_counts[$export_type]++))
            ((type_sizes[$export_type]+=$file_size))
            ((total_size+=$file_size))

            # 输出到清单 (按类型分组)
            if [[ "$export_type" != "$current_type" ]]; then
                current_type="$export_type"
                echo "" >> "$MANIFEST_FILE"
                echo "### $export_type" >> "$MANIFEST_FILE"
                echo "" >> "$MANIFEST_FILE"
                echo "| 文件名 | 大小 | 修改时间 | SHA256 | 重复 |" >> "$MANIFEST_FILE"
                echo "|--------|------|----------|--------|------|" >> "$MANIFEST_FILE"
            fi

            local size_str=$(format_size $file_size)
            local short_hash="${file_hash:0:16}..."
            local short_name="${filename:0:40}"
            [[ ${#filename} -gt 40 ]] && short_name="${short_name}..."

            echo "| $short_name | $size_str | $file_date | \`$short_hash\` | $is_dup |" >> "$MANIFEST_FILE"

        done < <(find "$scan_dir" -maxdepth 5 \( \
            -name "*.json" -o \
            -name "*.zip" -o \
            -name "*.md" -o \
            -name "*.tar.gz" -o \
            -name "Export-*" -o \
            -iname "*chatgpt*" -o \
            -iname "*claude*" -o \
            -iname "*notion*" -o \
            -iname "*backup*" -o \
            -iname "*备份*" -o \
            -iname "*导出*" -o \
            -iname "*export*" \
        \) -type f -print0 2>/dev/null)
    done

    # 添加统计摘要
    echo "" >> "$MANIFEST_FILE"
    echo "## 统计摘要" >> "$MANIFEST_FILE"
    echo "" >> "$MANIFEST_FILE"
    echo "| 类型 | 数量 | 总大小 |" >> "$MANIFEST_FILE"
    echo "|------|------|--------|" >> "$MANIFEST_FILE"

    for type in "${!type_counts[@]}"; do
        local count=${type_counts[$type]}
        local size=${type_sizes[$type]}
        local size_str=$(format_size $size)
        echo "| $type | $count | $size_str |" >> "$MANIFEST_FILE"
    done

    local total_size_str=$(format_size $total_size)
    echo "" >> "$MANIFEST_FILE"
    echo "**总计:** $unique_files 个唯一文件, $duplicates 个重复文件, 总大小 $total_size_str" >> "$MANIFEST_FILE"

    # 添加DNA签名
    echo "" >> "$MANIFEST_FILE"
    echo "---" >> "$MANIFEST_FILE"
    echo "" >> "$MANIFEST_FILE"
    echo "**DNA追溯码:** \`${DNA_CODE}\`" >> "$MANIFEST_FILE"
    echo "" >> "$MANIFEST_FILE"
    echo "**GPG指纹:** \`${GPG_FP}\`" >> "$MANIFEST_FILE"
    echo "" >> "$MANIFEST_FILE"
    echo "*由龍魂数据归集引擎 v${VERSION} 生成*" >> "$MANIFEST_FILE"

    log_info "清单已生成: $MANIFEST_FILE"

    echo ""
    echo -e "  ${GREEN}唯一文件:${NC} $unique_files"
    echo -e "  ${YELLOW}重复文件:${NC} $duplicates"
    echo -e "  ${CYAN}总大小:${NC} $total_size_str"
}

# 执行去重
dedup_files() {
    print_section "🔄 SHA256 去重"

    log_info "分析重复文件..."

    declare -A hash_files
    local dup_count=0
    local saved_size=0

    for scan_dir in "${SCAN_DIRS[@]}"; do
        [[ ! -d "$scan_dir" ]] && continue

        while IFS= read -r -d '' file; do
            local file_size=$(stat -f%z "$file" 2>/dev/null || echo 0)

            # 只处理小于100MB的文件
            (( file_size >= 104857600 )) && continue

            local file_hash=$(calc_sha256 "$file")
            [[ -z "$file_hash" ]] && continue

            if [[ -n "${hash_files[$file_hash]}" ]]; then
                # 发现重复
                local original="${hash_files[$file_hash]}"
                log_warn "重复: $(basename "$file")"
                log_info "  原始: $original"

                # 移动到去重目录
                local dup_name="$(basename "$file")_dup_$(date +%s)"
                mv "$file" "$DEDUP_DIR/$dup_name" 2>/dev/null && {
                    ((dup_count++))
                    ((saved_size+=$file_size))
                }
            else
                hash_files[$file_hash]="$file"
            fi

        done < <(find "$scan_dir" -maxdepth 5 -type f \( \
            -name "*.json" -o \
            -name "*.zip" -o \
            -name "*.md" \
        \) -print0 2>/dev/null)
    done

    local saved_str=$(format_size $saved_size)

    echo ""
    log_info "去重完成!"
    echo -e "  ${GREEN}移除重复:${NC} $dup_count 个文件"
    echo -e "  ${CYAN}节省空间:${NC} $saved_str"
    echo -e "  ${YELLOW}备份位置:${NC} $DEDUP_DIR"
}

# 显示帮助
show_help() {
    print_banner
    echo "用法: $(basename "$0") [选项]"
    echo ""
    echo "选项:"
    echo "  -s, --scan     仅扫描，统计导出文件"
    echo "  -m, --manifest 生成详细清单"
    echo "  -d, --dedup    执行SHA256去重"
    echo "  -a, --all      执行全部操作"
    echo "  -h, --help     显示帮助"
    echo ""
    echo "示例:"
    echo "  $(basename "$0") -s        # 快速扫描"
    echo "  $(basename "$0") -m        # 生成清单"
    echo "  $(basename "$0") -a        # 完整归集"
    echo ""
}

# ═══════════════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════════════

main() {
    local do_scan=false
    local do_manifest=false
    local do_dedup=false

    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -s|--scan)
                do_scan=true
                shift
                ;;
            -m|--manifest)
                do_manifest=true
                shift
                ;;
            -d|--dedup)
                do_dedup=true
                shift
                ;;
            -a|--all)
                do_scan=true
                do_manifest=true
                do_dedup=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                log_error "未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done

    # 默认执行扫描和清单
    if ! $do_scan && ! $do_manifest && ! $do_dedup; then
        do_scan=true
        do_manifest=true
    fi

    print_banner

    # 初始化
    init_directories

    # 执行操作
    if $do_scan; then
        scan_exports
    fi

    if $do_manifest; then
        deep_scan_and_manifest
    fi

    if $do_dedup; then
        dedup_files
    fi

    # 完成
    print_section "✅ 归集完成"

    echo -e "输出目录: ${GREEN}$OUTPUT_DIR${NC}"
    echo -e "清单文件: ${CYAN}$MANIFEST_FILE${NC}"
    echo ""
    echo -e "${YELLOW}DNA追溯码:${NC} ${DNA_CODE}"
    echo -e "${YELLOW}GPG指纹:${NC} ${GPG_FP}"
    echo ""
}

# 运行
main "$@"
