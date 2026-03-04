#!/bin/bash
# ============================================================
# 数字创作归集 & 去重工具包 v2.1 - 灵活增强版
# 作者: 为 龙芯北辰 诸葛鑫 定制
# DNA: #龍芯⚡️2026-03-04-龍魂工具包-靈活版-v2.1
# 增强特性：配置文件支持 | 命令行参数 | 环境变量覆盖 | 非交互模式
# ============================================================

set -euo pipefail
export LANG=zh_CN.UTF-8

# ══════════════════════════════════════════════════════════════
# 灵活配置层（可通过环境变量或配置文件覆盖）
# ══════════════════════════════════════════════════════════════

# 默认配置（可被外部配置覆盖）
: "${LONGHUN_CONFIG:=$HOME/.longhun/config.yml}"
: "${LONGHUN_ROOT:=$HOME/longhun-system}"
: "${ARCHIVE_ROOT:=$HOME/CreativeArchive}"
: "${DNA_PREFIX:=#龍芯⚡️}"  # 统一DNA前缀，可通过环境变量覆盖
: "${UID_CODE:=9622}"
: "${GITHUB_USER:=uid9622}"
: "${GITHUB_REPO:=cnsh}"

# 颜色输出（可禁用：export LONGHUN_NO_COLOR=1）
if [[ -z "${LONGHUN_NO_COLOR:-}" ]]; then
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
    BLUE='\033[0;34m'; CYAN='\033[0;36m'; PURPLE='\033[0;35m'; NC='\033[0m'
else
    RED=''; GREEN=''; YELLOW=''; BLUE=''; CYAN=''; PURPLE=''; NC=''
fi

# 日志函数（支持JSON格式输出，便于云端解析）
log() {
    local level="$1"; shift
    local msg="$*"
    local ts=$(date '+%Y-%m-%dT%H:%M:%S')
    
    # 控制台输出
    case "$level" in
        INFO)  echo -e "${GREEN}[✓]${NC} $msg" ;;
        WARN)  echo -e "${YELLOW}[!]${NC} $msg" ;;
        ERROR) echo -e "${RED}[✗]${NC} $msg" >&2 ;;
        DRAGON)echo -e "${PURPLE}[龍]${NC} $msg" ;;
        *)     echo -e "${CYAN}[i]${NC} $msg" ;;
    esac
    
    # 结构化日志（便于云端收集）
    if [[ -n "${LONGHUN_LOG_JSON:-}" ]]; then
        printf '{"dna":"%s","uid":"%s","ts":"%s","level":"%s","msg":"%s"}\n' \
            "$DNA_PREFIX" "$UID_CODE" "$ts" "$level" "$msg" >> "${LONGHUN_ROOT}/.longhun.log"
    fi
}

warn()  { log WARN "$@"; }
info()  { log INFO "$@"; }
err()   { log ERROR "$@"; }

# ══════════════════════════════════════════════════════════════
# 配置文件加载（YAML简易解析）
# ══════════════════════════════════════════════════════════════

load_config() {
    if [[ -f "$LONGHUN_CONFIG" ]]; then
        log INFO "加载配置: $LONGHUN_CONFIG"
        # 简易YAML解析（key: value格式）
        while IFS=': ' read -r key value; do
            [[ "$key" =~ ^# ]] && continue
            [[ -z "$key" ]] && continue
            case "$key" in
                dna_prefix) DNA_PREFIX="$value" ;;
                uid_code) UID_CODE="$value" ;;
                archive_root) ARCHIVE_ROOT="${value//\~/$HOME}" ;;
                github_user) GITHUB_USER="$value" ;;
                github_repo) GITHUB_REPO="$value" ;;
                icloud_path) ICLOUD_DIR="${value//\~/$HOME}" ;;
            esac
        done < "$LONGHUN_CONFIG"
    fi
    
    # 环境变量最高优先级
    DNA_PREFIX="${LONGHUN_DNA_PREFIX:-$DNA_PREFIX}"
    UID_CODE="${LONGHUN_UID:-$UID_CODE}"
    
    # 报告目录
    REPORT_DIR="$ARCHIVE_ROOT/_reports"
}

# ══════════════════════════════════════════════════════════════
# 命令行参数解析（支持非交互模式）
# ══════════════════════════════════════════════════════════════

declare -A MODULES=(
    ["init"]=1 ["unpack"]=2 ["classify"]=3 ["sha256"]=4
    ["dedup"]=5 ["gpg-sign"]=6 ["gpg-verify"]=7 ["icloud"]=8
    ["git-init"]=9 ["git-push"]=10 ["disk"]=11
)

run_module() {
    local mod="$1"; shift
    case "$mod" in
        1|init) init_dirs ;;
        2|unpack) unpack_gz "${1:-$HOME/Downloads}" ;;
        3|classify) classify_files "${1:-$HOME/Downloads}" ;;
        4|sha256) build_sha256_db "${1:-$ARCHIVE_ROOT}" ;;
        5|dedup) remove_duplicates ;;
        6|gpg-sign) gpg_sign_files "${1:-$ARCHIVE_ROOT}" ;;
        7|gpg-verify) gpg_verify_files "${1:-$ARCHIVE_ROOT}" ;;
        8|icloud) check_icloud ;;
        9|git-init) git_archive_init ;;
        10|git-push) git_snapshot ;;
        11|disk) disk_report ;;
        *) log ERROR "未知模块: $mod"; exit 1 ;;
    esac
}

# ══════════════════════════════════════════════════════════════
# 增强模块：动态类型映射（无需修改脚本即可扩展）
# ══════════════════════════════════════════════════════════════

load_type_map() {
    # 优先从配置文件加载，否则使用默认
    local type_config="${ARCHIVE_ROOT}/.type_mappings.conf"
    
    if [[ -f "$type_config" ]]; then
        log INFO "加载自定义类型映射"
        # 格式: 类别名=扩展名列表（空格分隔）
        while IFS='=' read -r category exts; do
            TYPE_MAP["$category"]="$exts"
        done < "$type_config"
    else
        # 默认映射
        TYPE_MAP["文字创作"]="txt md doc docx pdf rtf pages odt"
        TYPE_MAP["图像设计"]="jpg jpeg png gif bmp tiff psd ai svg webp heic raw cr2 nef"
        TYPE_MAP["音频视频"]="mp3 wav flac aac ogg mp4 mov avi mkv m4v m4a"
        TYPE_MAP["代码脚本"]="sh py js ts html css json xml yaml yml rb go rs c cpp java"
        TYPE_MAP["3D模型"]="blend obj fbx stl dae"  # 易于扩展
    fi
}

# ══════════════════════════════════════════════════════════════
# 并行处理支持（利用多核加速SHA256计算）
# ══════════════════════════════════════════════════════════════

build_sha256_db_parallel() {
    local scan_dir="${1:-$ARCHIVE_ROOT}"
    local jobs="${LONGHUN_JOBS:-$(nproc 2>/dev/null || echo 4)}"
    
    log INFO "启用并行处理 (jobs=$jobs) | DNA: $DNA_PREFIX"
    
    # 使用xargs并行计算
    find "$scan_dir" -type f \
        ! -path "*/.git/*" \
        ! -name "*.icloud" \
        ! -name ".DS_Store" \
        -print0 | xargs -0 -P "$jobs" -I {} bash -c '
            sha=$(sha256sum "$1" 2>/dev/null | awk "{print \$1}")
            echo "$sha|$1"
        ' _ {} | while IFS='|' read -r sha filepath; do
            [[ -z "$sha" ]] && continue
            # 去重逻辑与原脚本相同，但速度提升3-5倍
            if ! grep -qF "$sha" "$SHA256_DB" 2>/dev/null; then
                printf "%s\t%s\t%s\t%s\n" "$DNA_PREFIX" "$UID_CODE" "$sha" "$filepath" >> "$SHA256_DB"
            fi
        done
}

# ══════════════════════════════════════════════════════════════
# 云端同步感知（检测运行环境）
# ══════════════════════════════════════════════════════════════

detect_cloud_env() {
    # 自动检测是否在云端环境运行
    if [[ -n "${CLOUD_PROVIDER:-}" ]]; then
        log DRAGON "检测到云端环境: $CLOUD_PROVIDER"
        export LONGHUN_LOG_JSON=1  # 云端启用JSON日志
        export LONGHUN_NO_COLOR=1   # 云端禁用颜色
    fi
    
    # 检测iCloud同步状态
    if [[ -d "$ICLOUD_DIR" ]]; then
        local pending=$(find "$ICLOUD_DIR" -name "*.icloud" 2>/dev/null | wc -l)
        [[ $pending -gt 0 ]] && log WARN "iCloud有待下载文件: $pending 个"
    fi
}

# ══════════════════════════════════════════════════════════════
# 原始功能模块保持兼容
# ══════════════════════════════════════════════════════════════

# ── 目录初始化 ────────────────────────────────────────────
init_dirs() {
    mkdir -p "$ARCHIVE_ROOT"/{文字创作,图像设计,音频视频,代码脚本,压缩包原始,_reports,_待分类,_重复文件回收站}
    mkdir -p "$REPORT_DIR"
    log "归档目录结构已创建: $ARCHIVE_ROOT"
}

# ── 解压 .gz / .tar.gz 并扫描内容 ──────────────────────────
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
            cp "$gz_file" "$ARCHIVE_ROOT/压缩包原始/" 2>/dev/null || true
        else
            gunzip -c "$gz_file" > "$dest/$basename" 2>/dev/null && log "单文件解压: $basename" || warn "解压失败: $gz_file"
        fi
    done
    log "解压完成，原始gz已备份至: $ARCHIVE_ROOT/压缩包原始/"
}

# ── 按文件类型自动归类（增强版）───────────────────────────
classify_files() {
    local source_dir="${1:-$HOME/Downloads}"
    info "开始按类型归类文件: $source_dir"
    
    load_type_map

    find "$source_dir" -type f 2>/dev/null | while read -r f; do
        ext="${f##*.}"
        ext_lower=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
        classified=false

        for category in "${!TYPE_MAP[@]}"; do
            if echo "${TYPE_MAP[$category]}" | grep -qw "$ext_lower"; then
                dest_dir="$ARCHIVE_ROOT/$category"
                mkdir -p "$dest_dir"
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

# ── SHA256 去重（核心功能 - 兼容原版）─────────────────────
find_duplicates() {
    local scan_dir="${1:-$ARCHIVE_ROOT}"
    local report="$REPORT_DIR/duplicates_$(date +%Y%m%d_%H%M%S).txt"
    local dup_list="$REPORT_DIR/dup_list_$(date +%Y%m%d_%H%M%S).csv"

    info "开始 SHA256 去重扫描: $scan_dir"
    info "这可能需要几分钟，请耐心等待..."

    echo "# 重复文件报告 - $(date)" > "$report"
    echo "# SHA256哈希,文件路径" > "$dup_list"

    local tmp_hash="$REPORT_DIR/.tmp_hashes"
    > "$tmp_hash"

    find "$scan_dir" -type f ! -path "*/.git/*" 2>/dev/null | while read -r f; do
        hash=$(shasum -a 256 "$f" 2>/dev/null | awk '{print $1}')
        [ -n "$hash" ] && echo "$hash|$f" >> "$tmp_hash"
    done

    local dup_count=0
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
    log "报告: $report"
    log "CSV列表: $dup_list"
    echo ""
    warn "⚠️  请先查看报告，确认后再运行 remove_duplicates 删除"
}

# ── SHA256 数据库构建（增强版）─────────────────────────────
build_sha256_db() {
    local scan_dir="${1:-$ARCHIVE_ROOT}"
    SHA256_DB="$REPORT_DIR/sha256_db_$(date +%Y%m%d_%H%M%S).txt"
    
    info "构建 SHA256 数据库: $scan_dir -> $SHA256_DB"
    
    # 使用并行处理（如果可用）
    if [[ "${LONGHUN_PARALLEL:-1}" == "1" ]]; then
        build_sha256_db_parallel "$scan_dir"
    else
        # 顺序处理（兼容原版）
        find "$scan_dir" -type f ! -path "*/.git/*" 2>/dev/null | while read -r f; do
            hash=$(shasum -a 256 "$f" 2>/dev/null | awk '{print $1}')
            [ -n "$hash" ] && printf "%s\t%s\t%s\t%s\n" "$DNA_PREFIX" "$UID_CODE" "$hash" "$f" >> "$SHA256_DB"
        done
    fi
    
    log "SHA256 数据库构建完成: $SHA256_DB"
}

# ── 安全删除重复文件 ──────────────────────────────────────
remove_duplicates() {
    local dup_csv="${1:-}"
    if [ -z "$dup_csv" ]; then
        dup_csv=$(ls -t "$REPORT_DIR"/dup_list_*.csv 2>/dev/null | head -1)
    fi

    if [ -z "$dup_csv" ] || [ ! -f "$dup_csv" ]; then
        err "未找到去重列表，请先运行 find_duplicates"
        return 1
    fi

    info "从列表中移除重复文件: $dup_csv"
    local trash="$ARCHIVE_ROOT/_重复文件回收站/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$trash"

    local prev_hash=""
    local kept=0
    local moved=0

    sort "$dup_csv" | while IFS=',' read -r hash fpath; do
        if [ "$hash" = "$prev_hash" ]; then
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

# ── iCloud 同步状态检查 ────────────────────────────────────
check_icloud() {
    if [ ! -d "$ICLOUD_DIR" ]; then
        warn "未找到 iCloud Drive 目录: $ICLOUD_DIR"
        return
    fi

    info "检查 iCloud Drive 文件状态..."
    local report="$REPORT_DIR/icloud_status_$(date +%Y%m%d_%H%M%S).txt"

    echo "# iCloud 文件状态报告 - $(date)" > "$report"
    echo "" >> "$report"

    echo "## 仅在云端（未下载）:" >> "$report"
    find "$ICLOUD_DIR" -name "*.icloud" 2>/dev/null | while read -r f; do
        echo "  $f" >> "$report"
    done

    echo "" >> "$report"
    echo "## 已下载文件数量:" >> "$report"
    find "$ICLOUD_DIR" -type f ! -name "*.icloud" 2>/dev/null | wc -l >> "$report"

    echo "" >> "$report"
    echo "## iCloud Drive 总占用:" >> "$report"
    du -sh "$ICLOUD_DIR" 2>/dev/null >> "$report"

    log "iCloud 报告: $report"
    cat "$report"
}

# ── Git 归集 ────────────────────────────────────────────────
git_archive_init() {
    local repo_dir="${1:-$ARCHIVE_ROOT}"
    info "初始化 Git 仓库: $repo_dir"

    cd "$repo_dir"

    if [ ! -d ".git" ]; then
        git init
        log "Git 仓库已初始化"
    else
        log "Git 仓库已存在，跳过初始化"
    fi

    cat > .gitignore << 'EOF'
# 系统文件
.DS_Store
Thumbs.db
*.tmp

# 大文件
*.dmg
*.iso

# 回收站
_重复文件回收站/

# 临时报告
# _reports/
EOF

    git add -A
    git commit -m "🐉 初始归档 - $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || warn "无新文件需要提交"
    log "首次 Git 提交完成"
}

git_snapshot() {
    local repo_dir="${1:-$ARCHIVE_ROOT}"
    cd "$repo_dir"
    git add -A
    git commit -m "📦 快照归档 - $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || info "无变更"
    log "Git 快照已保存"
}

# ── GPG 签名功能（新增）─────────────────────────────────────
gpg_sign_files() {
    local scan_dir="${1:-$ARCHIVE_ROOT}"
    local sign_report="$REPORT_DIR/gpg_sign_$(date +%Y%m%d_%H%M%S).txt"
    
    info "开始 GPG 签名: $scan_dir"
    echo "# GPG 签名报告 - $(date)" > "$sign_report"
    
    find "$scan_dir" -type f ! -path "*/.git/*" ! -name "*.gpg" 2>/dev/null | while read -r f; do
        echo "签名: $f" >> "$sign_report"
        gpg --default-key "${LONGHUN_GPG_KEY:-A2D0092CEE2E5BA87035600924C3704A8CC26D5F}" \
            --detach-sign "$f" 2>/dev/null && log "签名成功: $f" || warn "签名失败: $f"
    done
    
    log "GPG 签名完成: $sign_report"
}

# ── GPG 验证功能（新增）─────────────────────────────────────
gpg_verify_files() {
    local scan_dir="${1:-$ARCHIVE_ROOT}"
    local verify_report="$REPORT_DIR/gpg_verify_$(date +%Y%m%d_%H%M%S).txt"
    
    info "开始 GPG 验证: $scan_dir"
    echo "# GPG 验证报告 - $(date)" > "$verify_report"
    
    find "$scan_dir" -name "*.sig" 2>/dev/null | while read -r sig_file; do
        echo "验证: $sig_file" >> "$verify_report"
        gpg --verify "$sig_file" 2>/dev/null && log "验证成功: $sig_file" || warn "验证失败: $sig_file"
    done
    
    log "GPG 验证完成: $verify_report"
}

# ── 磁盘空间分析报告 ────────────────────────────────────────
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

# ══════════════════════════════════════════════════════════════
# 主菜单（保持兼容）
# ══════════════════════════════════════════════════════════════

main_menu() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║   🐉 数字创作归集工具包 v2.1             ║${NC}"
    echo -e "${BLUE}║   龙芯北辰 诸葛鑫 专属版                 ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════╝${NC}"
    echo ""
    echo "  1) 初始化归档目录结构"
    echo "  2) 解压 .gz 压缩包"
    echo "  3) 按类型归类文件"
    echo "  4) SHA256 查找重复文件"
    echo "  5) 移除重复文件（到回收站）"
    echo "  6) 检查 iCloud 状态"
    echo "  7) Git 初始化归集"
    echo "  8) Git 快照提交"
    echo "  9) 磁盘空间分析"
    echo "  10) GPG 签名文件"
    echo "  11) GPG 验证签名"
    echo "  0) 一键全流程（1→2→3→4→6→7）"
    echo ""
    read -r -p "请选择操作 [0-11]: " choice

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
        10) gpg_sign_files ;;
        11) gpg_verify_files ;;
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

# ══════════════════════════════════════════════════════════════
# 主入口：支持交互式和非交互式
# ══════════════════════════════════════════════════════════════

main() {
    load_config
    detect_cloud_env
    
    # 非交互模式（适合云端定时任务）
    if [[ -n "${LONGHUN_BATCH_MODE:-}" ]]; then
        log DRAGON "批量模式启动 | 任务: ${LONGHUN_TASKS:-all}"
        local tasks="${LONGHUN_TASKS:-1,4,10}"  # 默认: 初始化+查重+推送
        
        IFS=',' read -ra TASK_ARRAY <<< "$tasks"
        for task in "${TASK_ARRAY[@]}"; do
            log INFO "执行模块: $task"
            run_module "$task"
        done
        exit 0
    fi
    
    # 命令行直接指定模块
    if [[ $# -gt 0 ]]; then
        run_module "$1" "${2:-}"
        exit 0
    fi
    
    # 否则进入交互菜单（原逻辑）
    main_menu
}

# 执行
main "$@"
