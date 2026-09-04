# DNA: #龍芯⚡️丙午·壬辰·乙亥·壬午·䷚颐-SYNC-COMPLIANCE-20260827-7A2C9F3D
#!/bin/bash
#龍芯⚡️丙午·乙未·丁酉·子时·䷀乾-KUNPENG-TOP-TUNE-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# 龍魂·鲲鹏服务器顶配调优脚本 v1.0
# 适用: Ubuntu 24.04 (x86_64 2vCPU/7.4G/99G 实测基线) + systemd
# 用法: bash kunpeng_top_tune.sh [clean|limits|swap|sysctl|all]  (默认 all)
# 安全: 全程容错·单项失败不中断·备份只留最新·可重复执行(幂等)

set -u
MODE="${1:-all}"
LOG="/var/log/longhun-top-tune.log"
mkdir -p /var/log

log() { echo "[$(date '+%F %T')] $*" | tee -a "$LOG"; }
die() { log "🔴 $*"; }

# ━━━━━━━━━━━ 模块1: 磁盘腾空间(保守·只清安全项) ━━━━━━━━━━━
do_clean() {
    log "== [clean] 磁盘腾空间 =="
    # 1. 备份只留最新一份(删最旧 tar.gz)
    BK_DIR=/backup/longhun
    if [ -d "$BK_DIR" ]; then
        OLD=$(ls -t "$BK_DIR"/*.tar.gz 2>/dev/null | tail -n +2)
        if [ -n "$OLD" ]; then
            for f in $OLD; do
                log "  删旧备份: $f ($(du -sh "$f" 2>/dev/null | cut -f1))"
                rm -f "$f"
            done
        else
            log "  备份≤1份·跳过"
        fi
    fi
    # 2. journal 上限 500M
    journalctl --vacuum-size=500M 2>/dev/null | tail -1 | tee -a "$LOG"
    # 3. 30 天前 .gz 旧日志
    find /var/log -name '*.gz' -mtime +30 -delete 2>/dev/null
    # 4. truncate 失控错误日志(>50M)
    for f in $(find /var/log -type f -size +50M -name '*.log' 2>/dev/null); do
        log "  truncate: $f ($(du -sh "$f" 2>/dev/null | cut -f1))"
        : > "$f"
    done
    # 5. apt 缓存
    apt-get clean 2>/dev/null
    df -h / | tail -1 | tee -a "$LOG"
}

# ━━━━━━━━━━━ 模块2: systemd + limits 顶配(服务级 nofile) ━━━━━━━━━━━
do_limits() {
    log "== [limits] systemd 级限额顶配 =="
    # systemd 全局: nofile 1024→1048576·nproc→65536 (72服务默认撞1024墙=病根)
    if ! grep -q '^DefaultLimitNOFILE=' /etc/systemd/system.conf; then
        sed -i 's/^#DefaultLimitNOFILE=.*/DefaultLimitNOFILE=1048576/' /etc/systemd/system.conf
        sed -i 's/^DefaultLimitNOFILE=.*/DefaultLimitNOFILE=1048576/' /etc/systemd/system.conf 2>/dev/null
    fi
    if ! grep -q '^DefaultLimitNPROC=' /etc/systemd/system.conf; then
        sed -i 's/^#DefaultLimitNPROC=.*/DefaultLimitNPROC=65536/' /etc/systemd/system.conf
        sed -i 's/^DefaultLimitNPROC=.*/DefaultLimitNPROC=65536/' /etc/systemd/system.conf 2>/dev/null
    fi
    # 兜底: 若 sed 未命中注释行则追加
    grep -q '^DefaultLimitNOFILE=' /etc/systemd/system.conf || \
        echo 'DefaultLimitNOFILE=1048576' >> /etc/systemd/system.conf
    grep -q '^DefaultLimitNPROC=' /etc/systemd/system.conf || \
        echo 'DefaultLimitNPROC=65536' >> /etc/systemd/system.conf
    # limits.d 顶配
    cat > /etc/security/limits.d/99-longhun.conf << 'EOF'
# 龍魂·顶配资源限制 (v1.0)
* soft nofile 1048576
* hard nofile 1048576
* soft nproc 65536
* hard nproc 65536
* soft memlock unlimited
* hard memlock unlimited
www-data soft nofile 1048576
www-data hard nofile 1048576
EOF
    systemctl daemon-reload
    grep -E 'DefaultLimit' /etc/systemd/system.conf | tee -a "$LOG"
    log "  重启所有服务后生效(可下轮开机统一重启)"
}

# ━━━━━━━━━━━ 模块3: swap 顶配(防 OOM·ZRAM优先·零磁盘占用) ━━━━━━━━━━━
do_swap() {
    log "== [swap] 顶配: ZRAM 4G 压缩交换区 + 保留原磁盘swapfile =="
    # 1. 清理旧 8G 磁盘 swapfile(占盘·不顶配)
    if [ -f /swapfile_top ]; then
        swapoff /swapfile_top 2>/dev/null
        rm -f /swapfile_top
        sed -i '/swapfile_top/d' /etc/fstab
        log "  已撤旧磁盘swapfile_top"
    fi
    # 2. ZRAM 模块装载
    echo 'zram' > /etc/modules-load.d/zram.conf
    # 3. ZRAM systemd 服务(持久化·开机自启)
    cat > /etc/systemd/system/zram-swap.service << 'SERVEOF'
[Unit]
Description=ZRAM 压缩交换区(顶配·零磁盘占用)
After=systemd-modules-load.service
[Service]
Type=oneshot
ExecStart=/bin/bash -c 'echo 4G > /sys/block/zram0/disksize && mkswap /dev/zram0 && swapon -p 100 /dev/zram0'
RemainAfterExit=yes
[Install]
WantedBy=multi-user.target
SERVEOF
    # 4. 立即生效(已挂则跳过)
    if ! swapon --show | grep -q zram0; then
        modprobe zram 2>/dev/null
        echo 4G > /sys/block/zram0/disksize 2>/dev/null
        mkswap /dev/zram0 >/dev/null 2>&1
        swapon -p 100 /dev/zram0 2>/dev/null
    fi
    systemctl daemon-reload
    systemctl enable zram-swap >/dev/null 2>&1
    swapon --show | tee -a "$LOG"
}

# ━━━━━━━━━━━ 模块4: sysctl 内核顶配(服务型·全部幂等) ━━━━━━━━━━━
do_sysctl() {
    log "== [sysctl] 内核顶配 =="
    # 0. 修复覆盖源: /etc/sysctl.conf 最后加载会压过 sysctl.d 的值
    sed -i 's/^vm.swappiness=0$/vm.swappiness=10/' /etc/sysctl.conf
    sed -i 's/^net.ipv4.tcp_max_syn_backlog=1024$/net.ipv4.tcp_max_syn_backlog=8192/' /etc/sysctl.conf
    CONF=/etc/sysctl.d/99-longhun.conf
    cat > "$CONF" << 'EOF'
# 龍魂·鲲鹏顶配内核参数 v1.0 (服务型·幂等)
# 连接队列
net.core.somaxconn = 65535
net.core.netdev_max_backlog = 65535
# TIME_WAIT 复用
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 30
# SYN 防护
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 8192
# 大吞吐缓冲(16M)
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.core.rmem_default = 1048576
net.core.wmem_default = 1048576
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
# 连接保活
net.ipv4.tcp_keepalive_time = 600
net.ipv4.tcp_keepalive_intvl = 30
net.ipv4.tcp_keepalive_probes = 5
# 内存压力(小内存机平衡: 留swap兜底·保inode缓存)
vm.swappiness = 10
vm.vfs_cache_pressure = 50
vm.max_map_count = 1048576
# 文件/监控上限(72服务+多引擎)
fs.file-max = 2097152
fs.inotify.max_user_watches = 524288
fs.inotify.max_user_instances = 1024
# 连接追踪(容错·不可写则跳过)
net.netfilter.nf_conntrack_max = 655360
net.netfilter.nf_conntrack_tcp_timeout_established = 3600
net.netfilter.nf_conntrack_tcp_timeout_time_wait = 60
EOF
    sysctl --system >/dev/null 2>&1 || sysctl -p "$CONF" 2>/dev/null
    log "  已应用关键项:"
    for k in vm.swappiness vm.vfs_cache_pressure net.core.somaxconn net.ipv4.tcp_max_syn_backlog net.core.rmem_max fs.inotify.max_user_watches; do
        log "    $k = $(sysctl -n "$k" 2>/dev/null)"
    done
}

# ━━━━━━━━━━━ 执行 ━━━━━━━━━━━
case "$MODE" in
    clean)  do_clean ;;
    limits) do_limits ;;
    swap)   do_swap ;;
    sysctl) do_sysctl ;;
    all|*)  do_clean; do_limits; do_swap; do_sysctl ;;
esac
log "🟢 顶配模块[$MODE]完成·日志: $LOG"
