#!/usr/bin/env bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · 存储分离迁移脚本 v1.0
# 将冷数据迁移到移动硬盘，活跃数据保留本地，代码同步到服务器
# DNA: #龍芯⚡️2026-07-12-STORAGE-MIGRATE-v1.0
set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
log()  { echo -e "$(date '+%H:%M:%S') $*"; }
ok()   { log "${GREEN}✅${NC} $*"; }
warn() { log "${YELLOW}⚠️${NC}  $*"; }
fail() { log "${RED}🔴${NC} $*"; exit 1; }
info() { log "${CYAN}▶${NC}  $*"; }

LONGHUN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXTERNAL_DISK="/Volumes/LonghunDisk"
COLD_STORAGE="${EXTERNAL_DISK}/longhun-cold-storage"

# ── 检查移动硬盘 ──
check_disk() {
    info "检查移动硬盘..."
    if [[ ! -d "$EXTERNAL_DISK" ]]; then
        fail "移动硬盘未挂载！请插入硬盘后重试。"
    fi
    local avail
    avail=$(df -g "$EXTERNAL_DISK" | tail -1 | awk '{print $4}')
    ok "移动硬盘可用空间: ${avail} GB"
    mkdir -p "$COLD_STORAGE"
}

# ── 迁移单个目录到冷存储 ──
migrate_dir() {
    local src="$1"
    local name="$2"
    local dest="${COLD_STORAGE}/${name}"
    
    if [[ ! -e "$src" ]]; then
        warn "跳过不存在的目录: $src"
        return
    fi
    
    local size
    size=$(du -sh "$src" 2>/dev/null | cut -f1)
    
    if [[ -e "$dest" ]]; then
        warn "${name} 已存在于冷存储，跳过"
        return
    fi
    
    info "迁移 ${name} (${size}) → 移动硬盘..."
    cp -a "$src" "$dest" && ok "${name} 迁移完成 (${size})"
}

# ── 压缩日志并迁移 ──
compress_logs() {
    info "压缩历史日志..."
    cd "$LONGHUN_ROOT"
    
    local log_archive="${COLD_STORAGE}/logs_archive_$(date +%Y%m%d).tar.gz"
    
    # 只压缩7天前的日志
    find logs/ -type f -name "*.log" -mtime +7 2>/dev/null > /tmp/longhun_old_logs.txt || true
    find logs/ -type f -name "*.jsonl" -mtime +7 2>/dev/null >> /tmp/longhun_old_logs.txt || true
    
    local count
    count=$(wc -l < /tmp/longhun_old_logs.txt 2>/dev/null || echo 0)
    
    if [[ "$count" -gt 0 ]]; then
        tar -czf "$log_archive" -T /tmp/longhun_old_logs.txt 2>/dev/null && {
            ok "压缩了 ${count} 个旧日志文件 → $(du -sh "$log_archive" | cut -f1)"
            # 删除已压缩的旧日志
            while IFS= read -r f; do rm -f "$f"; done < /tmp/longhun_old_logs.txt
            ok "已清理旧日志"
        }
    else
        ok "无需压缩的旧日志"
    fi
    rm -f /tmp/longhun_old_logs.txt
}

# ── 清理 Python 缓存 ──
clean_pycache() {
    info "清理 __pycache__ 目录..."
    local count
    count=$(find "$LONGHUN_ROOT" -type d -name "__pycache__" 2>/dev/null | wc -l)
    if [[ "$count" -gt 0 ]]; then
        find "$LONGHUN_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        ok "清理了 ${count} 个 __pycache__ 目录"
    fi
    
    find "$LONGHUN_ROOT" -type f -name "*.pyc" -delete 2>/dev/null || true
}

# ── 创建本地软链接指向冷存储 ──
create_symlinks() {
    info "创建软链接..."
    cd "$LONGHUN_ROOT"
    
    # 只对已迁移的目录创建软链接
    for name in models backups_archive; do
        local dest="${COLD_STORAGE}/${name}"
        if [[ -d "$dest" ]] && [[ ! -L "$name" ]] && [[ ! -d "$name" ]]; then
            ln -sf "$dest" "$name" 2>/dev/null && ok "软链接: ${name} → ${dest}"
        fi
    done
}

# ── 主流程 ──
main() {
    echo "╔══════════════════════════════════════════╗"
    echo "║  🐉 龍魂存储分离迁移 v1.0              ║"
    echo "║  冷数据→移动硬盘 | 代码→服务器         ║"
    echo "╚══════════════════════════════════════════╝"
    echo ""
    
    check_disk
    
    # 1. 冷数据 → 移动硬盘
    info "=== 第一阶段：冷数据迁移到移动硬盘 ==="
    migrate_dir "$LONGHUN_ROOT/models" "models"
    migrate_dir "$LONGHUN_ROOT/.archive" "dot_archive"
    migrate_dir "$LONGHUN_ROOT/backups" "backups_archive"
    migrate_dir "$LONGHUN_ROOT/brain/editor_memory_archive" "editor_memory"
    migrate_dir "$LONGHUN_ROOT/data-hub" "data-hub"
    
    # 2. 压缩日志
    echo ""
    info "=== 第二阶段：日志压缩 ==="
    compress_logs
    
    # 3. 清理缓存
    clean_pycache
    
    # 4. 创建软链接
    echo ""
    info "=== 第三阶段：创建软链接 ==="
    create_symlinks
    
    # 5. 报告
    echo ""
    echo "╔══════════════════════════════════════════╗"
    echo "║  📊 迁移完成报告                       ║"
    echo "╠══════════════════════════════════════════╣"
    echo "║  冷存储路径: ${COLD_STORAGE}"
    echo "╚══════════════════════════════════════════╝"
    
    ok "存储分离迁移完成！"
    echo ""
    info "下一步：运行 bash deploy/sync-to-kunpeng.sh full 同步代码到服务器"
}

main "$@"
