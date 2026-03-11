#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# digital_archive_toolkit.sh
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：#龍芯⚡️20260310-digital_archive_toolkit-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 共建致谢：Claude (Anthropic PBC) · Notion
# 创作地：中华人民共和国
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ============================================================
# 数字创作归集 & 去重工具包
# 作者: 为 龙芯北辰 诸葛鑫 定制
# 适用: macOS + iCloud + 本地硬盘备份
# ============================================================

set -e
LANG=zh_CN.UTF-8

# ── 颜色输出 ──────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; NC='\033[0m' # 无颜色

log()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
info() { echo -e "${CYAN}[i]${NC} $1"; }
err()  { echo -e "${RED}[✗]${NC} $1"; }

# ── 配置区（按需修改）─────────────────────────────────────
# 你的创作根目录（扫描来源）
SCAN_DIRS=(
    "$HOME/Desktop"
    "$HOME/Documents"
    "$HOME/Downloads"
    "$HOME/Movies"
    "$HOME/Pictures"
    "$HOME/Music"
    "/Volumes"                     # 外接硬盘自动挂载点
)

# iCloud Drive 路径（Mac标准路径）
ICLOUD_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs"

# 整理后统一归档目录
ARCHIVE_ROOT="$HOME/CreativeArchive"

# 去重报告输出目录
REPORT_DIR="$HOME/CreativeArchive/_reports"

# ── 目录初始化 ────────────────────────────────────────────
init_dirs() {
    mkdir -p "$ARCHIVE_ROOT"/{文字创作,图像设计,音频视频,代码脚本,压缩包原始,_reports,_待分类,_重复文件回收站}
    mkdir -p "$REPORT_DIR"
    log "归档目录结构已创建: $ARCHIVE_ROOT"
}

# ================================================================
# 模块1: 解压 .gz / .tar.gz 并扫描内容
# ================================================================
unpack_gz() {
    local target_dir="${1:-$HOME/Downloads}"
    info "开始扫描 .gz 压缩包: $target_dir"

    local unpack_base="$ARCHIVE_ROOT/压缩包原始/_已解压"
    mkdir -p "$unpack_base"

    find "$target_dir" -name "*.gz" -o -name "*.tar.gz" 2>/dev/null | while read -r gz_file; do
        local basename
        basename=$(basename "$gz_file" .gz)
        basename=$(basename "$basename" .tar)
        local dest="$unpack_base/$basename"
        mkdir -p "$dest"

        info "解压: $gz_file → $dest"
        if tar -xzf "$gz_file" -C "$dest" 2>/dev/null; then
            log "解压成功: $basename"
            # 备份原始gz到专区，不删除
            cp "$gz_file" "$ARCHIVE_ROOT/压缩包原始/" 2>/dev/null || true
        else
            # 单文件 .gz
            gunzip -c "$gz_file" > "$dest/$basename" 2>/dev/null && log "单文件解压: $basename" || warn "解压失败: $gz_file"
        fi
    done
    log "解压完成，原始gz已备份至: $ARCHIVE_ROOT/压缩包原始/"
}

# ================================================================
# 模块2: 按文件类型自动归类
# ================================================================
classify_files() {
    local source_dir="${1:-$HOME/Downloads}"
    info "开始按类型归类文件: $source_dir"

    # 定义类型映射（兼容 bash 和 zsh）
    typeset -A TYPE_MAP
    TYPE_MAP[文字创作]="txt md doc docx pdf rtf pages odt"
    TYPE_MAP[图像设计]="jpg jpeg png gif bmp tiff psd ai svg webp heic raw cr2 nef"
    TYPE_MAP[音频视频]="mp3 wav flac aac ogg mp4 mov avi mkv m4v m4a"
    TYPE_MAP[代码脚本]="sh py js ts html css json xml yaml yml rb go rs c cpp java"

    find "$source_dir" -type f 2>/dev/null | while read -r f; do
        ext="${f##*.}"
        ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
        classified=false  # 是否已分类标记

        for category in "${!TYPE_MAP[@]}"; do
            if echo "${TYPE_MAP[$category]}" | grep -qw "$ext_lower"; then
                dest_dir="$ARCHIVE_ROOT/$category"
                mkdir -p "$dest_dir"
                # 避免覆盖：若同名文件存在则加时间戳
                dest_file="$dest_dir/$(basename "$f")"
                if [ -e "$dest_file" ]; then
                    ts=$(date +%Y%m%d_%H%M%S)
                    dest_file="$dest_dir/${ts}_$(basename "$f")"
                fi
                cp "$f" "$dest_file" 2>/dev/null && classified=true
                break
            fi
        done

        if [ "$classified" = false ]; then
            cp "$f" "$ARCHIVE_ROOT/_待分类/" 2>/dev/null || true
        fi
    done
    log "文件归类完成"
}

# ================================================================
# 模块3: SHA256 去重（核心功能）
# ================================================================
find_duplicates() {
    local scan_dir="${1:-$ARCHIVE_ROOT}"
    local report="$REPORT_DIR/duplicates_$(date +%Y%m%d_%H%M%S).txt"
    local dup_list="$REPORT_DIR/dup_list_$(date +%Y%m%d_%H%M%S).csv"

    info "开始 SHA256 去重扫描: $scan_dir"
    info "这可能需要几分钟，请耐心等待..."

    echo "# 重复文件报告 - $(date)" > "$report"
    echo "# SHA256哈希值,文件路径" > "$dup_list"

    # 计算所有文件的哈希值，找出重复项
    local tmp_hash="$REPORT_DIR/.tmp_hashes"
    > "$tmp_hash"

    find "$scan_dir" -type f ! -path "*/.git/*" 2>/dev/null | while read -r f; do
        hash=$(shasum -a 256 "$f" 2>/dev/null | awk '{print $1}')
        [ -n "$hash" ] && echo "$hash|$f" >> "$tmp_hash"
    done

    # 找出重复的哈希值
    local dup_count=0  # 重复计数
    sort "$tmp_hash" | awk -F'|' '{print $1}' | sort | uniq -d | while read -r dup_hash; do
        echo "" >> "$report"
        echo "## 重复组 [哈希: $dup_hash]" >> "$report"
        grep "^$dup_hash|" "$tmp_hash" | awk -F'|' '{print $2}' | while read -r fpath; do
            fsize=$(du -sh "$fpath" 2>/dev/null | cut -f1)
            echo "  $fsize  $fpath" >> "$report"
            echo "$dup_hash,$fpath" >> "$dup_list"
        done
        dup_count=$((dup_count+1))
    done

    rm -f "$tmp_hash"
    log "去重扫描完成！"
    log "报告文件: $report"
    log "重复列表: $dup_list"
    echo ""
    warn "⚠️  请先查看报告，确认后再选择「移除重复文件」功能（选项5）进行删除"
}

# ================================================================
# 模块4: 安全删除重复文件（保留第一个，其余移入回收站）
# ================================================================
remove_duplicates() {
    local dup_csv="${1:-}"
    if [ -z "$dup_csv" ]; then
        # 自动找最新的去重列表
        dup_csv=$(ls -t "$REPORT_DIR"/dup_list_*.csv 2>/dev/null | head -1)
    fi

    if [ -z "$dup_csv" ] || [ ! -f "$dup_csv" ]; then
        err "未找到去重列表，请先运行「查找重复文件」功能（选项4）"
        return 1
    fi

    info "从列表中移除重复文件: $dup_csv"
    local trash="$ARCHIVE_ROOT/_重复文件回收站/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$trash"

    local prev_hash=""   # 上一个哈希值
    local kept=0         # 保留计数
    local moved=0        # 移动计数

    # 按哈希值分组，每组只保留第一个
    sort "$dup_csv" | while IFS=',' read -r hash fpath; do
        if [ "$hash" = "$prev_hash" ]; then
            # 重复，移入回收站
            mv "$fpath" "$trash/" 2>/dev/null && {
                warn "已移入回收站: $fpath"
                moved=$((moved+1))
            }
        else
            log "保留: $fpath"
            kept=$((kept+1))
        fi
        prev_hash="$hash"
    done

    log "操作完成 → 回收站: $trash"
    warn "确认无误后可手动清空回收站目录"
}

# ================================================================
# 模块5: iCloud 同步状态检查
# ================================================================
check_icloud() {
    if [ ! -d "$ICLOUD_DIR" ]; then
        warn "未找到 iCloud Drive 目录: $ICLOUD_DIR"
        return
    fi

    info "检查 iCloud Drive 文件状态..."
    local report="$REPORT_DIR/icloud_status_$(date +%Y%m%d_%H%M%S).txt"

    echo "# iCloud 文件状态报告 - $(date)" > "$report"
    echo "" >> "$report"

    # 找出未下载到本地的文件（.icloud 是占位文件）
    echo "## 仅在云端（未下载到本地）:" >> "$report"
    find "$ICLOUD_DIR" -name "*.icloud" 2>/dev/null | while read -r f; do
        echo "  $f" >> "$report"
    done

    # 统计已下载文件
    echo "" >> "$report"
    echo "## 已下载文件数量:" >> "$report"
    find "$ICLOUD_DIR" -type f ! -name "*.icloud" 2>/dev/null | wc -l >> "$report"

    echo "" >> "$report"
    echo "## iCloud Drive 总占用:" >> "$report"
    du -sh "$ICLOUD_DIR" 2>/dev/null >> "$report"

    log "iCloud 报告: $report"
    cat "$report"
}

# ================================================================
# 模块6: 版本归集 — 将整理好的档案纳入版本控制管理
# ================================================================
git_archive_init() {
    local repo_dir="${1:-$ARCHIVE_ROOT}"
    info "初始化版本仓库: $repo_dir"

    cd "$repo_dir"

    if [ ! -d ".git" ]; then
        git init
        log "版本仓库已初始化"
    else
        log "版本仓库已存在，跳过初始化"
    fi

    # 创建 .gitignore
    cat > .gitignore << 'EOF'
# 系统文件
.DS_Store
Thumbs.db
*.tmp

# 大文件（超过100MB建议用 git-lfs 管理）
*.dmg
*.iso

# 回收站不纳入版本控制
_重复文件回收站/

# 临时报告（可选择是否追踪）
# _reports/
EOF

    git add -A
    git commit -m "🐉 初始归档 - $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || warn "无新文件需要提交"
    log "首次版本提交完成"
}
git_snapshot() {
    local repo_dir="${1:-$ARCHIVE_ROOT}"
    cd "$repo_dir"
    git add -A
    git commit -m "📦 快照归档 - $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || info "无变更需要提交"
    log "版本快照已保存"
}

# ================================================================
# 模块7: 生成磁盘空间分析报告
# ================================================================
disk_report() {
    local report="$REPORT_DIR/disk_report_$(date +%Y%m%d_%H%M%S).txt"
    info "生成磁盘分析报告..."

    {
        echo "# 磁盘空间分析报告 - $(date)"
        echo ""
        echo "## 整体磁盘使用"
        df -h /
        echo ""
        echo "## 各挂载磁盘"
        df -h
        echo ""
        echo "## 创作归档目录占用"
        du -sh "$ARCHIVE_ROOT"/* 2>/dev/null
        echo ""
        echo "## 前20大文件"
        find "$HOME" -type f -exec du -sh {} \; 2>/dev/null | sort -rh | head -20
        echo ""
        echo "## 前10大目录"
        du -sh "$HOME"/*/  2>/dev/null | sort -rh | head -10
    } > "$report"

    log "磁盘报告: $report"
    cat "$report"
}

# ================================================================
# 主菜单
# ================================================================
main_menu() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   🐉 数字创作归集工具包 v1.0             ║${NC}"
    echo -e "${BLUE}║   龙芯北辰 诸葛鑫 专属版                 ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
    echo ""
    echo "  1) 初始化归档目录结构"
    echo "  2) 解压 .gz 压缩包"
    echo "  3) 按类型归类文件"
    echo "  4) SHA256 查找重复文件"
    echo "  5) 移除重复文件（到回收站）"
    echo "  6) 检查 iCloud 状态"
    echo "  7) 版本控制初始化"
    echo "  8) 版本快照提交"
    echo "  9) 磁盘空间分析"
    echo "  0) 一键全流程（1→2→3→4→6→7）"
    echo ""
    read -r -p "请选择操作 [0-9]: " choice

    case "$choice" in
        1) init_dirs ;;
        2) read -r -p "指定目录（回车默认 ~/Downloads）: " d; unpack_gz "${d:-$HOME/Downloads}" ;;
        3) read -r -p "指定目录（回车默认 ~/Downloads）: " d; classify_files "${d:-$HOME/Downloads}" ;;
        4) read -r -p "扫描目录（回车默认归档目录）: " d; find_duplicates "${d:-$ARCHIVE_ROOT}" ;;
        5) remove_duplicates ;;
        6) check_icloud ;;
        7) git_archive_init ;;
        8) git_snapshot ;;
        9) disk_report ;;
        0)
            log "开始全流程..."
            init_dirs
            unpack_gz "$HOME/Downloads"
            classify_files "$HOME/Downloads"
            find_duplicates "$ARCHIVE_ROOT"
            check_icloud
            git_archive_init
            log "🎉 全流程完成！请查看报告: $REPORT_DIR"
            ;;
        *) err "无效选项" ;;
    esac
}

# ── 入口 ──────────────────────────────────────────────────
# 如果直接运行则显示菜单；也可以直接调用函数
# 例如: source digital_archive_toolkit.sh && find_duplicates ~/Downloads
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main_menu
fi
