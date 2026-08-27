#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·甲戌·卯时·䷐随-QUAD-SYNC-v1.0-ATTRIBUTION-8c26d5f
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# ╔══════════════════════════════════════════════════════════════╗
# ║   龍魂数字创作归集工具包 v2.0                               ║
# ║   龍芯北辰 诸葛鑫 (Zhuge Xin) 专属定制版                   ║
# ║                                                              ║
# ║   DNA前缀   : #ZHUGEXIN                                     ║
# ║   UID       : 96 / uid9622                                  ║
# ║   GPG指纹   : A2D0092CEE2E5BA87035600924C3704A8CC26D5F      ║
# ║   确认码    : #CONFIRM-9622-ONLY-ONCE-LK9X-77               ║
# ║   GitHub    : uid9622/cnsh                                  ║
# ╚══════════════════════════════════════════════════════════════╝

set -e
export LANG=zh_CN.UTF-8

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; PURPLE='\033[0;35m'; NC='\033[0m'

log()    { echo -e "${GREEN}[✓]${NC} $1"; }
warn()   { echo -e "${YELLOW}[!]${NC} $1"; }
info()   { echo -e "${CYAN}[i]${NC} $1"; }
err()    { echo -e "${RED}[✗]${NC} $1"; }
dragon() { echo -e "${PURPLE}[龍]${NC} $1"; }

# ══════════════════════════════════════════════════════════════
# 身份配置（固定）
# ══════════════════════════════════════════════════════════════
DNA_PREFIX="#ZHUGEXIN"
UID_CODE="9622"
GPG_FINGERPRINT="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
AUTHOR_NAME="龍芯北辰 诸葛鑫"

GITHUB_USER="uid9622"
GITHUB_REPO="cnsh"
GITHUB_PROXY="https://mirror.ghproxy.com"
GITHUB_URL="${GITHUB_PROXY}/https://github.com/${GITHUB_USER}/${GITHUB_REPO}.git"

LONGHUN_ROOT="$HOME/longhun-system/CNSH-整理版"
ARCHIVE_ROOT="$LONGHUN_ROOT"
REPORT_DIR="$LONGHUN_ROOT/_reports"
SHA256_DB="$REPORT_DIR/sha256_database.tsv"

ICLOUD_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs"

# ══════════════════════════════════════════════════════════════
# 模块0: 初始化目录
# ══════════════════════════════════════════════════════════════
init_dirs() {
    mkdir -p "$LONGHUN_ROOT"/{文字创作,图像设计,音频视频,代码脚本,压缩包原始,_待分类,_重复文件回收站}
    mkdir -p "$REPORT_DIR"
    if [ ! -f "$SHA256_DB" ]; then
        printf "DNA前缀\tUID\tSHA256\t文件名\t文件路径\t文件大小\t时间戳\tGPG签名状态\n" > "$SHA256_DB"
        log "SHA256 数据库已建立: $SHA256_DB"
    fi
    log "龍魂归档目录已就绪: $LONGHUN_ROOT"
}

# ══════════════════════════════════════════════════════════════
# 模块1: 解压 .gz / .tar.gz
# ══════════════════════════════════════════════════════════════
unpack_gz() {
    local target_dir="${1:-$HOME/Downloads}"
    info "扫描 .gz 压缩包: $target_dir"
    local unpack_base="$ARCHIVE_ROOT/压缩包原始/_已解压"
    mkdir -p "$unpack_base"

    find "$target_dir" \( -name "*.gz" -o -name "*.tar.gz" \) 2>/dev/null | while read -r gz_file; do
        local bname
        bname=$(basename "$gz_file" .gz)
        bname=$(basename "$bname" .tar)
        local dest="$unpack_base/$bname"
        mkdir -p "$dest"
        info "解压: $(basename "$gz_file")"
        if tar -xzf "$gz_file" -C "$dest" 2>/dev/null; then
            log "解压成功: $bname"
        else
            gunzip -c "$gz_file" > "$dest/$bname" 2>/dev/null \
                && log "单文件解压: $bname" \
                || warn "解压失败: $gz_file"
        fi
        cp "$gz_file" "$ARCHIVE_ROOT/压缩包原始/" 2>/dev/null || true
    done
    log "解压完成，原始gz已备份"
}

# ══════════════════════════════════════════════════════════════
# 模块2: 按类型归类
# ══════════════════════════════════════════════════════════════
classify_files() {
    local source_dir="${1:-$HOME/Downloads}"
    info "按类型归类: $source_dir"

    declare -A TYPE_MAP
    TYPE_MAP["文字创作"]="txt md doc docx pdf rtf pages odt"
    TYPE_MAP["图像设计"]="jpg jpeg png gif bmp tiff psd ai svg webp heic raw cr2 nef"
    TYPE_MAP["音频视频"]="mp3 wav flac aac ogg mp4 mov avi mkv m4v m4a"
    TYPE_MAP["代码脚本"]="sh py js ts html css json xml yaml yml rb go rs c cpp java h"

    find "$source_dir" -type f 2>/dev/null | while read -r f; do
        ext=$(echo "${f##*.}" | tr '[:upper:]' '[:lower:]')
        classified=false
        for category in "${!TYPE_MAP[@]}"; do
            if echo "${TYPE_MAP[$category]}" | grep -qw "$ext"; then
                dest_dir="$ARCHIVE_ROOT/$category"
                mkdir -p "$dest_dir"
                dest_file="$dest_dir/$(basename "$f")"
                [ -e "$dest_file" ] && dest_file="$dest_dir/$(date +%Y%m%d_%H%M%S)_$(basename "$f")"
                cp "$f" "$dest_file" 2>/dev/null && classified=true
                break
            fi
        done
        $classified || cp "$f" "$ARCHIVE_ROOT/_待分类/" 2>/dev/null || true
    done
    log "归类完成"
}

# ══════════════════════════════════════════════════════════════
# 模块3: SHA256 数字指纹归集 + 查重
# ══════════════════════════════════════════════════════════════
build_sha256_db() {
    local scan_dir="${1:-$ARCHIVE_ROOT}"
    info "构建 SHA256 数字指纹数据库..."
    info "DNA前缀: $DNA_PREFIX | UID: $UID_CODE"
    info "扫描: $scan_dir"

    local tmp="$REPORT_DIR/.tmp_sha256_$$"
    > "$tmp"
    local count=0

    find "$scan_dir" -type f \
        ! -path "*/.git/*" \
        ! -name "*.icloud" \
        ! -name ".DS_Store" \
        ! -name "*.sig" \
        ! -name "*.asc" \
        2>/dev/null | while read -r f; do

        local sha256
        sha256=$(shasum -a 256 "$f" 2>/dev/null | awk '{print $1}')
        [ -z "$sha256" ] && continue

        local fsize ts fname gpg_status
        fsize=$(du -sh "$f" 2>/dev/null | cut -f1)
        ts=$(date '+%Y-%m-%dT%H:%M:%S')
        fname=$(basename "$f")
        gpg_status="未签名"
        { [ -f "${f}.sig" ] || [ -f "${f}.asc" ]; } && gpg_status="已签名"

        # 写入数据库（新增才写，避免重复）
        if ! grep -qF "$sha256" "$SHA256_DB" 2>/dev/null; then
            printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
                "$DNA_PREFIX" "$UID_CODE" "$sha256" "$fname" "$f" "$fsize" "$ts" "$gpg_status" \
                >> "$SHA256_DB"
        fi

        echo "$sha256|$f" >> "$tmp"
        count=$((count+1))
        [ $((count % 100)) -eq 0 ] && info "已扫描 $count 个文件..."
    done

    log "SHA256 指纹归集完成 → $SHA256_DB"

    # 生成重复报告
    local dup_report="$REPORT_DIR/duplicates_$(date +%Y%m%d_%H%M%S).txt"
    local dup_csv="$REPORT_DIR/dup_list_$(date +%Y%m%d_%H%M%S).csv"

    echo "# 重复文件报告 - $(date)" > "$dup_report"
    echo "# DNA: $DNA_PREFIX | UID: $UID_CODE" >> "$dup_report"
    echo "SHA256,文件路径" > "$dup_csv"

    local dup_groups=0
    sort "$tmp" | awk -F'|' '{print $1}' | sort | uniq -d | while read -r dup_hash; do
        echo "" >> "$dup_report"
        echo "## [重复] $dup_hash" >> "$dup_report"
        grep "^${dup_hash}|" "$tmp" | awk -F'|' '{print $2}' | while read -r fp; do
            sz=$(du -sh "$fp" 2>/dev/null | cut -f1)
            echo "  [$sz] $fp" >> "$dup_report"
            echo "$dup_hash,$fp" >> "$dup_csv"
        done
        dup_groups=$((dup_groups+1))
    done

    rm -f "$tmp"
    log "重复报告: $dup_report"
    log "重复列表: $dup_csv"
    warn "确认后选菜单5移除重复文件"
}

# ══════════════════════════════════════════════════════════════
# 模块4: 安全移除重复文件
# ══════════════════════════════════════════════════════════════
remove_duplicates() {
    local dup_csv
    dup_csv=$(ls -t "$REPORT_DIR"/dup_list_*.csv 2>/dev/null | head -1)
    if [ -z "$dup_csv" ] || [ ! -f "$dup_csv" ]; then
        err "未找到去重列表，请先运行模块3"
        return 1
    fi
    local trash="$ARCHIVE_ROOT/_重复文件回收站/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$trash"
    info "重复文件移入: $trash"

    local prev_hash=""
    sort "$dup_csv" | while IFS=',' read -r hash fpath; do
        if [ "$hash" = "$prev_hash" ]; then
            mv "$fpath" "$trash/" 2>/dev/null && warn "已移入回收站: $(basename "$fpath")"
        else
            log "保留: $fpath"
        fi
        prev_hash="$hash"
    done
    log "完成 → 回收站: $trash"
    warn "确认无误后可手动清空回收站"
}

# ══════════════════════════════════════════════════════════════
# 模块5: GPG 签名
# ══════════════════════════════════════════════════════════════
gpg_sign_files() {
    local target_dir="${1:-$ARCHIVE_ROOT}"
    if ! command -v gpg &>/dev/null; then
        err "未找到 gpg，请安装: brew install gnupg"
        return 1
    fi
    if ! gpg --list-secret-keys "$GPG_FINGERPRINT" &>/dev/null; then
        warn "未找到私钥: $GPG_FINGERPRINT"
        warn "导入私钥: gpg --import 你的私钥.asc"
        return 1
    fi
    info "GPG 签名目录: $target_dir"
    info "使用指纹: $GPG_FINGERPRINT"

    find "$target_dir" -type f \
        ! -name "*.sig" ! -name "*.asc" \
        ! -name ".DS_Store" ! -path "*/.git/*" \
        2>/dev/null | while read -r f; do
        [ -f "${f}.sig" ] && continue
        gpg --batch --yes \
            --local-user "$GPG_FINGERPRINT" \
            --detach-sign \
            --output "${f}.sig" \
            "$f" 2>/dev/null \
            && log "已签名: $(basename "$f")" \
            || warn "签名失败: $(basename "$f")"
    done
    log "GPG 签名完成，指纹: $GPG_FINGERPRINT"
}

gpg_verify_files() {
    local target_dir="${1:-$ARCHIVE_ROOT}"
    info "验证 GPG 签名: $target_dir"
    local report="$REPORT_DIR/gpg_verify_$(date +%Y%m%d_%H%M%S).txt"
    echo "# GPG 验证报告 - $(date)" > "$report"
    echo "# 指纹: $GPG_FINGERPRINT" >> "$report"
    echo "" >> "$report"
    find "$target_dir" -name "*.sig" 2>/dev/null | while read -r sig; do
        original="${sig%.sig}"
        [ -f "$original" ] || continue
        if gpg --verify "$sig" "$original" 2>/dev/null; then
            echo "[✓ 有效] $(basename "$original")" >> "$report"
        else
            echo "[✗ 无效] $(basename "$original")" >> "$report"
        fi
    done
    log "验证报告: $report"
    cat "$report"
}

# ══════════════════════════════════════════════════════════════
# 模块6: iCloud 状态检查
# ══════════════════════════════════════════════════════════════
check_icloud() {
    if [ ! -d "$ICLOUD_DIR" ]; then
        warn "未找到 iCloud Drive: $ICLOUD_DIR"
        return
    fi
    info "检查 iCloud Drive..."
    local report="$REPORT_DIR/icloud_$(date +%Y%m%d_%H%M%S).txt"
    {
        echo "# iCloud 状态报告 - $(date)"
        echo "# DNA: $DNA_PREFIX | UID: $UID_CODE"
        echo ""
        echo "## 仅在云端（未下载的占位文件）:"
        find "$ICLOUD_DIR" -name "*.icloud" 2>/dev/null | sed 's/^/  /'
        echo ""
        echo "## 已在本地的文件数:"
        find "$ICLOUD_DIR" -type f ! -name "*.icloud" 2>/dev/null | wc -l | tr -d ' '
        echo ""
        echo "## iCloud 总占用:"
        du -sh "$ICLOUD_DIR" 2>/dev/null
    } > "$report"
    log "iCloud 报告: $report"
    cat "$report"
}

# ══════════════════════════════════════════════════════════════
# 模块7: Git 归集推送
# ══════════════════════════════════════════════════════════════
git_archive_init() {
    local repo_dir="${1:-$LONGHUN_ROOT}"
    info "初始化 Git: $repo_dir"
    cd "$repo_dir"
    if [ ! -d ".git" ]; then
        git init
        git remote add origin "$GITHUB_URL"
    else
        git remote set-url origin "$GITHUB_URL"
    fi
    cat > .gitignore << 'GITEOF'
.DS_Store
Thumbs.db
*.tmp
*.dmg
*.iso
_重复文件回收站/
.tmp_*
GITEOF
    git add -A
    git commit -m "龍 ${DNA_PREFIX} 龍魂归档初始化 - $(date '+%Y-%m-%d %H:%M')" 2>/dev/null \
        || warn "无新文件"
    log "Git 初始化完成 → uid9622/cnsh"
}

git_snapshot() {
    local repo_dir="${1:-$LONGHUN_ROOT}"
    cd "$repo_dir"
    git remote set-url origin "$GITHUB_URL"
    git add -A
    git commit -m "龍 ${DNA_PREFIX} 快照 - $(date '+%Y-%m-%d %H:%M')" 2>/dev/null \
        || { info "无变更"; return 0; }
    info "推送到 uid9622/cnsh（贵州代理加速）..."
    git push origin main \
        && log "推送成功！" \
        || warn "推送失败，稍后重试"
}

# ══════════════════════════════════════════════════════════════
# 模块8: 磁盘分析
# ══════════════════════════════════════════════════════════════
disk_report() {
    local report="$REPORT_DIR/disk_$(date +%Y%m%d_%H%M%S).txt"
    info "生成磁盘报告..."
    {
        echo "# 磁盘报告 - $(date)"
        echo "# $DNA_PREFIX | UID: $UID_CODE"
        echo ""
        echo "## 磁盘整体"
        df -h
        echo ""
        echo "## 龍魂归档目录分布"
        du -sh "$ARCHIVE_ROOT"/* 2>/dev/null
        echo ""
        echo "## 前20大文件"
        find "$HOME" -type f ! -path "*/.git/*" \
            -exec du -sh {} \; 2>/dev/null | sort -rh | head -20
        echo ""
        echo "## 前10大目录"
        du -sh "$HOME"/*/ 2>/dev/null | sort -rh | head -10
    } > "$report"
    log "磁盘报告: $report"
    cat "$report"
}

# ══════════════════════════════════════════════════════════════
# 主菜单
# ══════════════════════════════════════════════════════════════
main_menu() {
    clear
    echo ""
    echo -e "${PURPLE}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║  龍  龍魂数字创作归集工具包 v2.0                      ║${NC}"
    echo -e "${PURPLE}║  ${AUTHOR_NAME}  专属版              ║${NC}"
    echo -e "${PURPLE}║  DNA: ${DNA_PREFIX}  UID: ${UID_CODE}                            ║${NC}"
    echo -e "${PURPLE}║  GPG: ${GPG_FINGERPRINT:0:20}...            ║${NC}"
    echo -e "${PURPLE}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "  1) 初始化龍魂归档目录"
    echo "  2) 解压 .gz 压缩包"
    echo "  3) 按类型归类文件"
    echo "  4) SHA256 数字指纹归集 + 查重"
    echo "  5) 移除重复文件（到回收站）"
    echo "  6) GPG 签名文件（私钥: $GPG_FINGERPRINT）"
    echo "  7) GPG 验证已签名文件"
    echo "  8) 检查 iCloud 状态"
    echo "  9) Git 初始化归集"
    echo "  a) Git 快照推送到 uid9622/cnsh"
    echo "  b) 磁盘空间分析"
    echo ""
    echo "  0) 一键全流程（1→2→3→4→8→9）"
    echo ""
    read -r -p "请选择 [0-9/a/b]: " choice

    case "$choice" in
        1) init_dirs ;;
        2) read -r -p "目录（回车=~/Downloads）: " d; unpack_gz "${d:-$HOME/Downloads}" ;;
        3) read -r -p "目录（回车=~/Downloads）: " d; classify_files "${d:-$HOME/Downloads}" ;;
        4) read -r -p "扫描目录（回车=归档目录）: " d; build_sha256_db "${d:-$ARCHIVE_ROOT}" ;;
        5) remove_duplicates ;;
        6) read -r -p "签名目录（回车=归档目录）: " d; gpg_sign_files "${d:-$ARCHIVE_ROOT}" ;;
        7) read -r -p "验证目录（回车=归档目录）: " d; gpg_verify_files "${d:-$ARCHIVE_ROOT}" ;;
        8) check_icloud ;;
        9) git_archive_init ;;
        a) git_snapshot ;;
        b) disk_report ;;
        0)
            dragon "启动全流程..."
            init_dirs
            unpack_gz "$HOME/Downloads"
            classify_files "$HOME/Downloads"
            build_sha256_db "$ARCHIVE_ROOT"
            check_icloud
            git_archive_init
            dragon "全流程完成！报告在: $REPORT_DIR"
            ;;
        *) err "无效选项" ;;
    esac

    echo ""
    read -r -p "按回车返回菜单..." _
    main_menu
}

# 入口
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    init_dirs 2>/dev/null || true
    main_menu
fi
