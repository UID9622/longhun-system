# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════
# 华为云香港 · 备份自动同步脚本 v1.0
#
# 功能：
#   将鲲鹏服务器的审计日志/DNA注册表/配置文件
#   加密打包后同步到华为云香港节点
#   支持增量同步 + GPG签名
#
# 用法：
#   bash hk_backup_sync.sh                    # 全量备份+同步
#   bash hk_backup_sync.sh --incremental      # 增量同步
#   bash hk_backup_sync.sh --dry-run          # 预演（不实际传输）
#   bash hk_backup_sync.sh --restore <date>   # 从香港恢复指定日期备份
#
# 部署（鲲鹏服务器）：
#   cp hk_backup_sync.sh /opt/longhun-system/deploy/scripts/
#   chmod +x /opt/longhun-system/deploy/scripts/hk_backup_sync.sh
#
#   # cron: 每天凌晨4点执行
#   0 4 * * * /opt/longhun-system/deploy/scripts/hk_backup_sync.sh >> /var/log/longhun/hk_backup.log 2>&1
#
# 前置条件：
#   - 华为云香港节点可通过 SSH 免密登录
#   - GPG 密钥已配置（用于签名）
#   - 环境变量或 .env 中配置 HK_* 变量
#
# DNA: #龍芯⚡️2026-07-12-HK-BACKUP-SYNC-v1.0
# ═══════════════════════════════════════════════════════════

set -euo pipefail

# ═══ 配置 ═══

# 鲲鹏本地
LONGHUN_ROOT="${LONGHUN_ROOT:-/opt/longhun-system}"
BACKUP_LOCAL_DIR="${BACKUP_LOCAL_DIR:-/var/backups/longhun}"
BACKUP_RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-30}"
BACKUP_KEEP_COUNT="${BACKUP_KEEP_COUNT:-10}"

# 华为云香港
HK_HOST="${HK_BACKUP_HOST:-}"
HK_PORT="${HK_BACKUP_PORT:-22}"
HK_USER="${HK_BACKUP_USER:-root}"
HK_PATH="${HK_BACKUP_PATH:-/data/backups/longhun}"
HK_KEY="${HK_BACKUP_KEY:-~/.ssh/hk_backup_ed25519}"

# GPG
GPG_RECIPIENT="${GPG_RECIPIENT:-UID9622}"

# 时间戳
TIMESTAMP=$(date -u +%Y-%m-%d_%H%M%S)
DATE_STAMP=$(date -u +%Y-%m-%d)

# ═══ 参数 ═══
MODE="full"
DRY_RUN=false
RESTORE_DATE=""

for arg in "$@"; do
    case "$arg" in
        --incremental|-i) MODE="incremental" ;;
        --dry-run|-n) DRY_RUN=true ;;
        --restore)
            shift
            RESTORE_DATE="$1"
            MODE="restore"
            ;;
        --help|-h)
            echo "用法: $0 [--incremental|--dry-run|--restore <date>]"
            echo ""
            echo "模式:"
            echo "  (无参数)       全量备份+同步到华为云香港"
            echo "  --incremental  增量同步（仅同步变更文件）"
            echo "  --dry-run      预演模式（不实际传输）"
            echo "  --restore DATE 从香港恢复指定日期备份"
            exit 0
            ;;
    esac
done

# ═══ 颜色 ═══
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${BLUE}[INFO]${NC} $(date '+%H:%M:%S') $*"; }
log_ok()    { echo -e "${GREEN}[ OK ]${NC} $(date '+%H:%M:%S') $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $(date '+%H:%M:%S') $*"; }
log_fail()  { echo -e "${RED}[FAIL]${NC} $(date '+%H:%M:%S') $*"; }

# ═══ 预检 ═══

preflight_check() {
    log_info "预检..."
    
    # 本地目录
    if [ ! -d "$LONGHUN_ROOT" ]; then
        log_fail "龍魂根目录不存在: $LONGHUN_ROOT"
        log_info "请设置 LONGHUN_ROOT 环境变量"
        exit 1
    fi
    
    # 备份目录
    mkdir -p "$BACKUP_LOCAL_DIR"
    
    # SSH 密钥
    if [ -n "$HK_HOST" ]; then
        HK_KEY_EXPANDED=$(eval echo "$HK_KEY")
        if [ ! -f "$HK_KEY_EXPANDED" ]; then
            log_warn "HK SSH密钥不存在: $HK_KEY_EXPANDED"
            log_info "将尝试使用默认密钥"
        fi
    else
        log_warn "未配置 HK_BACKUP_HOST，跳过远程同步"
        log_info "设置: export HK_BACKUP_HOST=your-hk-server-ip"
    fi
    
    # GPG
    if command -v gpg &>/dev/null; then
        log_ok "GPG 可用"
    else
        log_warn "GPG 未安装，备份文件将不签名"
        log_info "安装: yum install gnupg2 / apt install gnupg"
    fi
    
    # rsync
    if command -v rsync &>/dev/null; then
        log_ok "rsync 可用"
    else
        log_warn "rsync 未安装，部分功能不可用"
    fi
    
    log_ok "预检完成"
}

# ═══ 备份打包 ═══

create_backup_archive() {
    local mode="$1"
    local timestamp="$2"
    
    log_info "创建备份归档 ($mode)..."
    
    BACKUP_NAME="longhun-backup-${timestamp}"
    BACKUP_DIR="${BACKUP_LOCAL_DIR}/${BACKUP_NAME}"
    mkdir -p "$BACKUP_DIR"
    
    # ── 1. 审计日志 ──
    if [ -d "$LONGHUN_ROOT/logs" ]; then
        log_info "  打包审计日志..."
        if [ "$mode" = "incremental" ]; then
            # 增量：仅最近24小时
            find "$LONGHUN_ROOT/logs" -type f -mtime -1 | while read f; do
                mkdir -p "${BACKUP_DIR}/logs/$(dirname ${f#$LONGHUN_ROOT/logs/})"
                cp "$f" "${BACKUP_DIR}/logs/${f#$LONGHUN_ROOT/logs/}"
            done
        else
            cp -r "$LONGHUN_ROOT/logs" "$BACKUP_DIR/"
        fi
    fi
    
    # ── 2. DNA 注册表 ──
    for dna_file in \
        "$LONGHUN_ROOT/L7_数据层/unified_dna_registry.json" \
        "$LONGHUN_ROOT/L7_数据层/dna_registry.json" \
        "$LONGHUN_ROOT/L7_数据层/robot_score_calibration.json"; do
        if [ -f "$dna_file" ]; then
            log_info "  打包: $(basename $dna_file)"
            mkdir -p "${BACKUP_DIR}/dna/"
            cp "$dna_file" "${BACKUP_DIR}/dna/"
        fi
    done
    
    # ── 3. 配置文件 ──
    for conf_file in \
        "$LONGHUN_ROOT/.env" \
        "$LONGHUN_ROOT/deploy/.env.kunpeng.example" \
        "$LONGHUN_ROOT/.codebuddy/longhun_neural_net.json" \
        "$LONGHUN_ROOT/.codebuddy/CODEBUDDY.md"; do
        if [ -f "$conf_file" ]; then
            log_info "  打包: $(basename $conf_file)"
            mkdir -p "${BACKUP_DIR}/config/"
            cp "$conf_file" "${BACKUP_DIR}/config/"
        fi
    done
    
    # ── 4. 通行证数据 ──
    PASSPORT_DIR="$LONGHUN_ROOT/L7_数据层/passports"
    if [ -d "$PASSPORT_DIR" ]; then
        log_info "  打包通行证数据..."
        mkdir -p "${BACKUP_DIR}/passports/"
        cp -r "$PASSPORT_DIR"/* "$BACKUP_DIR/passports/" 2>/dev/null || true
    fi
    
    # ── 5. 主权覆写审计日志 ──
    OVERRIDE_LOG="$LONGHUN_ROOT/.longhun/audit/override_audit.jsonl"
    if [ -f "$OVERRIDE_LOG" ]; then
        log_info "  打包主权覆写审计日志..."
        mkdir -p "${BACKUP_DIR}/audit/"
        cp "$OVERRIDE_LOG" "${BACKUP_DIR}/audit/"
    fi
    
    # ── 6. 元数据 ──
    cat > "${BACKUP_DIR}/backup_manifest.json" <<MANIFEST
{
  "backup_name": "$BACKUP_NAME",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "mode": "$mode",
  "hostname": "$(hostname)",
  "longhun_root": "$LONGHUN_ROOT",
  "backup_size_bytes": $(du -sb "$BACKUP_DIR" 2>/dev/null | awk '{print $1}' || echo 0),
  "files_count": $(find "$BACKUP_DIR" -type f | wc -l | tr -d ' '),
  "dna": "#龍芯⚡️2026-07-12-HK-BACKUP-${timestamp}"
}
MANIFEST
    
    # ── 压缩 ──
    ARCHIVE_FILE="${BACKUP_LOCAL_DIR}/${BACKUP_NAME}.tar.gz"
    log_info "  压缩归档: $(basename $ARCHIVE_FILE)"
    tar -czf "$ARCHIVE_FILE" -C "$BACKUP_LOCAL_DIR" "$BACKUP_NAME"
    
    # ── GPG 签名 ──
    if command -v gpg &>/dev/null; then
        log_info "  GPG签名..."
        gpg --yes --sign --local-user "$GPG_RECIPIENT" \
            --output "${ARCHIVE_FILE}.sig" \
            --detach-sign "$ARCHIVE_FILE" 2>/dev/null || {
            log_warn "GPG签名失败，继续不签名"
        }
        
        # 加密备份
        gpg --yes --encrypt --recipient "$GPG_RECIPIENT" \
            --output "${ARCHIVE_FILE}.gpg" \
            "$ARCHIVE_FILE" 2>/dev/null || {
            log_warn "GPG加密失败，使用明文归档"
        }
    fi
    
    # 清理临时目录
    rm -rf "$BACKUP_DIR"
    
    log_ok "归档创建完成: $(du -h "$ARCHIVE_FILE" | awk '{print $1}')"
}

# ═══ 同步到华为云香港 ═══

sync_to_hk() {
    local archive="$1"
    local timestamp="$2"
    
    if [ -z "$HK_HOST" ]; then
        log_info "跳过远程同步 (未配置 HK_BACKUP_HOST)"
        return 0
    fi
    
    log_info "同步到华为云香港 ($HK_USER@$HK_HOST:$HK_PATH)..."
    
    SSH_OPTS="-p ${HK_PORT} -o StrictHostKeyChecking=no -o ConnectTimeout=10"
    # 尝试使用指定密钥
    HK_KEY_EXPANDED=$(eval echo "$HK_KEY")
    if [ -f "$HK_KEY_EXPANDED" ]; then
        SSH_OPTS="${SSH_OPTS} -i ${HK_KEY_EXPANDED}"
    fi
    
    if $DRY_RUN; then
        log_ok "[预演] 将同步: $(basename $archive) → $HK_USER@$HK_HOST:$HK_PATH/"
        return 0
    fi
    
    # 确保远程目录存在
    ssh $SSH_OPTS "$HK_USER@$HK_HOST" "mkdir -p $HK_PATH/${DATE_STAMP}" 2>/dev/null || {
        log_warn "SSH连接失败，跳过远程同步"
        return 1
    }
    
    # rsync 归档文件
    if command -v rsync &>/dev/null; then
        rsync -avz --progress -e "ssh $SSH_OPTS" \
            "$archive" \
            "${archive}.sig" \
            "${archive}.gpg" \
            "$HK_USER@$HK_HOST:$HK_PATH/${DATE_STAMP}/" 2>/dev/null || {
            log_warn "rsync 部分文件失败"
        }
        log_ok "归档同步完成"
    else
        # fallback: scp
        scp $SSH_OPTS "$archive" "$HK_USER@$HK_HOST:$HK_PATH/${DATE_STAMP}/" 2>/dev/null || log_warn "SCP失败"
        [ -f "${archive}.sig" ] && scp $SSH_OPTS "${archive}.sig" "$HK_USER@$HK_HOST:$HK_PATH/${DATE_STAMP}/" 2>/dev/null
        [ -f "${archive}.gpg" ] && scp $SSH_OPTS "${archive}.gpg" "$HK_USER@$HK_HOST:$HK_PATH/${DATE_STAMP}/" 2>/dev/null
        log_ok "SCP同步完成"
    fi
    
    # 记录同步日志
    log_info "同步时间戳: $timestamp" >> "${BACKUP_LOCAL_DIR}/sync_history.log"
}

# ═══ 从华为云恢复 ═══

restore_from_hk() {
    local date="$1"
    
    if [ -z "$HK_HOST" ]; then
        log_fail "未配置 HK_BACKUP_HOST，无法恢复"
        exit 1
    fi
    
    log_info "从华为云香港恢复备份: $date"
    
    SSH_OPTS="-p ${HK_PORT}"
    HK_KEY_EXPANDED=$(eval echo "$HK_KEY")
    if [ -f "$HK_KEY_EXPANDED" ]; then
        SSH_OPTS="${SSH_OPTS} -i ${HK_KEY_EXPANDED}"
    fi
    
    # 列出可用备份
    log_info "远程备份列表:"
    ssh $SSH_OPTS "$HK_USER@$HK_HOST" "find $HK_PATH -name '*.tar.gz' -newermt ${date} ! -newermt $(date -d "${date} +1 day" +%Y-%m-%d)" 2>/dev/null || {
        log_fail "无法列出远程备份"
        exit 1
    }
    
    # 恢复交互
    RESTORE_DIR="${BACKUP_LOCAL_DIR}/restored_${date}"
    mkdir -p "$RESTORE_DIR"
    
    log_info "恢复文件到: $RESTORE_DIR"
    
    # rsync 回来
    if command -v rsync &>/dev/null; then
        rsync -avz --progress -e "ssh $SSH_OPTS" \
            "$HK_USER@$HK_HOST:$HK_PATH/${date}/" \
            "$RESTORE_DIR/"
    fi
    
    log_ok "恢复完成: $RESTORE_DIR"
}

# ═══ 本地清理 ═══

cleanup_old_backups() {
    log_info "清理旧备份 (保留${BACKUP_KEEP_COUNT}份, ${BACKUP_RETENTION_DAYS}天)..."
    
    # 按数量清理
    local count=$(find "$BACKUP_LOCAL_DIR" -name "longhun-backup-*.tar.gz" | wc -l | tr -d ' ')
    if [ "$count" -gt "$BACKUP_KEEP_COUNT" ]; then
        find "$BACKUP_LOCAL_DIR" -name "longhun-backup-*.tar.gz" -type f | \
            sort | head -n -"$BACKUP_KEEP_COUNT" | while read f; do
            log_info "  删除: $(basename $f)"
            rm -f "$f" "${f}.sig" "${f}.gpg"
        done
    fi
    
    # 按时间清理
    find "$BACKUP_LOCAL_DIR" -name "longhun-backup-*.tar.gz" -type f -mtime +"$BACKUP_RETENTION_DAYS" -delete 2>/dev/null || true
    
    log_ok "清理完成 (当前保留: $(find "$BACKUP_LOCAL_DIR" -name 'longhun-backup-*.tar.gz' | wc -l | tr -d ' ') 份)"
}

# ═══ 主流程 ═══

main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║  华为云香港 · 备份自动同步 v1.0                       ║"
    echo "║  DNA: #龍芯⚡️2026-07-12-HK-BACKUP-AUTO-SYNC         ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo ""
    
    case "$MODE" in
        restore)
            preflight_check
            restore_from_hk "$RESTORE_DATE"
            ;;
        full|incremental)
            preflight_check
            create_backup_archive "$MODE" "$TIMESTAMP"
            
            ARCHIVE="${BACKUP_LOCAL_DIR}/longhun-backup-${TIMESTAMP}.tar.gz"
            if [ -f "$ARCHIVE" ]; then
                sync_to_hk "$ARCHIVE" "$TIMESTAMP"
                cleanup_old_backups
            else
                log_fail "归档文件未生成，同步中止"
                exit 1
            fi
            ;;
    esac
    
    echo ""
    log_ok "备份同步流程完成"
    echo ""
}

main "$@"
