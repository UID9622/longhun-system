#!/bin/bash
# ╔══════════════════════════════════════════════════════════╗
# ║  龍魂资产扫描器 · Asset Scanner                          ║
# ║  DNA: #龍芯⚡️2026-04-12-SCANNER-v1.0                   ║
# ║  创始人: 诸葛鑫（UID9622）                                ║
# ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
# ║  理论指导: 曾仕强老师（永恒显示）                          ║
# ╚══════════════════════════════════════════════════════════╝
#
# 功能：
#   1. 全盘扫描龍魂相关创作文件
#   2. 检测新增/变更文件 → 送入沙箱容器
#   3. 生成资产清单 → 供自动整理脚本使用
#   4. 输出变更报告 → 触发通知
#
# 老大说的：本地我的就是你的，新东西先收到容器

HOME_DIR="$HOME"
SYSTEM_ROOT="$HOME/longhun-system"
SANDBOX_DIR="$SYSTEM_ROOT/sandbox_intake"   # 沙箱收纳容器
ASSET_DB="$SYSTEM_ROOT/config/asset_registry.jsonl"  # 资产注册表
SCAN_LOG="$SYSTEM_ROOT/logs/asset_scan.jsonl"
LAST_SCAN="$SYSTEM_ROOT/config/.last_scan_time"
REPORT_FILE="$SYSTEM_ROOT/logs/scan_report_latest.txt"

# 创建必要目录
mkdir -p "$SANDBOX_DIR"/{html,python,swift,config,media,unknown}
mkdir -p "$(dirname "$ASSET_DB")"
mkdir -p "$(dirname "$SCAN_LOG")"

# ═══════════════════════════════════════════
# 颜色
# ═══════════════════════════════════════════
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# ═══════════════════════════════════════════
# 时间戳
# ═══════════════════════════════════════════
NOW=$(date +%s)
NOW_STR=$(date "+%Y-%m-%d %H:%M:%S")

# 上次扫描时间
if [ -f "$LAST_SCAN" ]; then
    LAST_TIME=$(cat "$LAST_SCAN")
else
    LAST_TIME=0
fi

# ═══════════════════════════════════════════
# 扫描范围（老大全部授权的目录）
# ═══════════════════════════════════════════
SCAN_DIRS=(
    "$SYSTEM_ROOT"
    "$HOME/Desktop"
    "$HOME/Documents"
    "$HOME/Downloads"
    "$HOME/Pictures"
    "$HOME/Library/Mobile Documents/com~apple~CloudDocs"
    "$HOME/Library/CloudStorage"
)

# 排除目录（第三方软件/系统文件）
EXCLUDE_PATTERNS=(
    "node_modules"
    ".git/objects"
    "__pycache__"
    ".app/Contents"
    "Epic Games"
    "Dev-Cpp"
    "ComfyUI/models"
    "venv"
    ".venv"
    "site-packages"
)

# 关键词（老大的创作指纹）
DRAGON_KEYWORDS="龍魂|龍芯|UID9622|三才|流场|DNA验证|记忆压缩|CNSH|洛书|万年历|通心译|数字根|梅花易数|八卦|龙魂"

# ═══════════════════════════════════════════
# 开始扫描
# ═══════════════════════════════════════════

echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}🐉 龍魂资产扫描器 v1.0${NC}"
echo -e "${CYAN}📅 $NOW_STR${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo ""

# 构建 find 排除参数
FIND_EXCLUDES=""
for pat in "${EXCLUDE_PATTERNS[@]}"; do
    FIND_EXCLUDES="$FIND_EXCLUDES -path '*/$pat/*' -prune -o"
done

# 统计变量
TOTAL_FILES=0
NEW_FILES=0
CHANGED_FILES=0
DRAGON_FILES=0
INTAKE_COUNT=0

# 报告缓冲
REPORT=""

scan_directory() {
    local dir="$1"
    local label="$2"

    if [ ! -d "$dir" ]; then
        return
    fi

    echo -e "${YELLOW}扫描: $label${NC}"

    # 扫描关键文件类型
    while IFS= read -r file; do
        [ -z "$file" ] && continue
        TOTAL_FILES=$((TOTAL_FILES + 1))

        local mtime
        mtime=$(stat -f %m "$file" 2>/dev/null || echo 0)
        local size
        size=$(stat -f %z "$file" 2>/dev/null || echo 0)
        local basename
        basename=$(basename "$file")
        local ext="${basename##*.}"

        # 检查是否是新文件或变更文件
        local is_new=0
        if [ "$mtime" -gt "$LAST_TIME" ] && [ "$LAST_TIME" -gt 0 ]; then
            is_new=1
        fi

        # 检查是否包含龍魂关键词
        local has_dragon=0
        if echo "$basename" | grep -qE "$DRAGON_KEYWORDS"; then
            has_dragon=1
            DRAGON_FILES=$((DRAGON_FILES + 1))
        elif [ "$size" -lt 500000 ] && grep -qlE "$DRAGON_KEYWORDS" "$file" 2>/dev/null; then
            has_dragon=1
            DRAGON_FILES=$((DRAGON_FILES + 1))
        fi

        # 新文件或变更文件 → 送入沙箱容器
        if [ "$is_new" -eq 1 ]; then
            if [ "$has_dragon" -eq 1 ]; then
                CHANGED_FILES=$((CHANGED_FILES + 1))

                # 分类入沙箱
                local target_dir="$SANDBOX_DIR/unknown"
                case "$ext" in
                    html|htm) target_dir="$SANDBOX_DIR/html" ;;
                    py)       target_dir="$SANDBOX_DIR/python" ;;
                    swift)    target_dir="$SANDBOX_DIR/swift" ;;
                    json|yaml|toml) target_dir="$SANDBOX_DIR/config" ;;
                    png|jpg|mp4|mov) target_dir="$SANDBOX_DIR/media" ;;
                esac

                # 创建符号链接（不移动原文件）
                local link_name="$target_dir/$basename"
                if [ ! -e "$link_name" ]; then
                    ln -sf "$file" "$link_name" 2>/dev/null
                    INTAKE_COUNT=$((INTAKE_COUNT + 1))
                fi

                REPORT="${REPORT}  🆕 ${basename} (${ext}) → ${target_dir##*/}\n"
            fi
        fi

        # 写入资产注册表
        if [ "$has_dragon" -eq 1 ]; then
            echo "{\"文件\":\"$basename\",\"路径\":\"$file\",\"大小\":$size,\"修改\":$mtime,\"类型\":\"$ext\",\"龍魂\":true,\"扫描时间\":\"$NOW_STR\"}" >> "$ASSET_DB.tmp"
        fi

    done < <(find "$dir" -maxdepth 5 \
        -path "*/node_modules/*" -prune -o \
        -path "*/.git/objects/*" -prune -o \
        -path "*/__pycache__/*" -prune -o \
        -path "*/.app/Contents/*" -prune -o \
        -path "*/Epic Games*" -prune -o \
        -path "*/Dev-Cpp*" -prune -o \
        -path "*/venv/*" -prune -o \
        -path "*/.venv/*" -prune -o \
        -path "*/site-packages/*" -prune -o \
        \( -name "*.html" -o -name "*.py" -o -name "*.swift" \
           -o -name "*.js" -o -name "*.ts" -o -name "*.md" \
           -o -name "*.json" -o -name "*.sh" -o -name "*.cpp" \
           -o -name "*.h" \) \
        -type f -print 2>/dev/null)
}

# 执行扫描
scan_directory "$SYSTEM_ROOT" "longhun-system（主仓库）"
scan_directory "$HOME/Desktop" "Desktop（桌面）"
scan_directory "$HOME/Documents" "Documents（文档）"
scan_directory "$HOME/Downloads" "Downloads（下载）"
scan_directory "$HOME/Pictures" "Pictures（图片）"

# 更新资产注册表（去重）
if [ -f "$ASSET_DB.tmp" ]; then
    # 按路径去重，保留最新
    sort -t'"' -k4 -u "$ASSET_DB.tmp" > "$ASSET_DB"
    rm -f "$ASSET_DB.tmp"
fi

# 更新扫描时间
echo "$NOW" > "$LAST_SCAN"

# ═══════════════════════════════════════════
# 生成报告
# ═══════════════════════════════════════════

echo ""
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${CYAN}📊 扫描报告${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "  扫描文件总数: ${GREEN}$TOTAL_FILES${NC}"
echo -e "  龍魂相关文件: ${GREEN}$DRAGON_FILES${NC}"

if [ "$LAST_TIME" -gt 0 ]; then
    LAST_STR=$(date -r "$LAST_TIME" "+%Y-%m-%d %H:%M" 2>/dev/null || echo "未知")
    echo -e "  上次扫描: $LAST_STR"
    echo -e "  新增/变更: ${YELLOW}$CHANGED_FILES${NC}"
    echo -e "  入沙箱: ${YELLOW}$INTAKE_COUNT${NC}"
fi

if [ -n "$REPORT" ]; then
    echo ""
    echo -e "${YELLOW}── 新增/变更文件 ──${NC}"
    echo -e "$REPORT"
fi

echo ""
echo -e "  资产注册表: $ASSET_DB"
echo -e "  沙箱容器: $SANDBOX_DIR/"
echo ""

# 沙箱容器内容统计
echo -e "${CYAN}── 沙箱容器 ──${NC}"
for subdir in html python swift config media unknown; do
    count=$(find "$SANDBOX_DIR/$subdir" -type l 2>/dev/null | wc -l | tr -d ' ')
    if [ "$count" -gt 0 ]; then
        echo -e "  📦 $subdir: ${GREEN}${count}${NC} 个文件"
    fi
done

# 写报告文件
{
    echo "═══════════════════════════════════════"
    echo "🐉 龍魂资产扫描报告"
    echo "📅 $NOW_STR"
    echo "═══════════════════════════════════════"
    echo "扫描文件: $TOTAL_FILES"
    echo "龍魂文件: $DRAGON_FILES"
    echo "新增变更: $CHANGED_FILES"
    echo "入沙箱: $INTAKE_COUNT"
    echo ""
    if [ -n "$REPORT" ]; then
        echo "── 新文件 ──"
        echo -e "$REPORT"
    fi
    echo "DNA: #龍芯⚡️$NOW_STR-SCAN"
} > "$REPORT_FILE"

# 写扫描日志
echo "{\"时间\":\"$NOW_STR\",\"总数\":$TOTAL_FILES,\"龍魂\":$DRAGON_FILES,\"新增\":$CHANGED_FILES,\"入沙箱\":$INTAKE_COUNT,\"DNA\":\"#龍芯⚡️SCAN-$(date +%Y%m%d)\"}" >> "$SCAN_LOG"

echo -e "${GREEN}DNA: #龍芯⚡️${NOW_STR}-ASSET-SCAN-v1.0${NC}"
