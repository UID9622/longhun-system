# DNA: #龍芯⚡️丙午·乙未·乙丑·观-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ═══════════════════════════════════════════════════════════
# 龍魂系统 · 服务异常排查清单 v1.0
# 目标: gatekeeper / longzhishou 反复崩溃根因定位
# UID: 9622 | 主权人格: ZHUGEXIN⚡️ | 时间: 2026-07-13
# ═══════════════════════════════════════════════════════════

# ─── 配置 ───
LOG_DIR="${LOG_DIR:-$HOME/.longhun/logs}"
REPORT_FILE="$LOG_DIR/crash_report_$(date +%Y%m%d_%H%M%S).txt"
mkdir -p "$LOG_DIR"

# ─── 颜色 ───
R='\033[0;31m'; G='\033[0;32m'; Y='\033[0;33m'; C='\033[0;36m'; X='\033[0m'

# ─── 输出函数 ───
section() { echo -e "\n${C}═══ $1 ═══${X}" | tee -a "$REPORT_FILE"; }
pass() { echo -e "${G}[✓]${X} $1" | tee -a "$REPORT_FILE"; }
fail() { echo -e "${R}[✗]${X} $1" | tee -a "$REPORT_FILE"; }
warn() { echo -e "${Y}[!]${X} $1" | tee -a "$REPORT_FILE"; }
info() { echo -e "  $1" | tee -a "$REPORT_FILE"; }

# ─── 开始 ───
section "龍魂系统 · 崩溃排查报告 · $(date '+%Y-%m-%d %H:%M:%S')"
echo "目标服务: gatekeeper, longzhishou" | tee -a "$REPORT_FILE"
echo "排查主机: $(hostname)" | tee -a "$REPORT_FILE"

# ═══ 1. 进程状态 ═══
section "1. 进程存活状态"
for svc in gatekeeper longzhishou; do
    pid=$(pgrep -f "$svc" | head -1)
    if [[ -n "$pid" ]]; then
        pass "$svc 运行中 (PID: $pid)"
        info "启动时间: $(ps -o lstart= -p $pid 2>/dev/null || echo '未知')"
        info "CPU/内存: $(ps -o pcpu,pmem= -p $pid 2>/dev/null || echo '未知')"
    else
        fail "$svc 未运行"
    fi
done

# ═══ 2. 最近崩溃记录 ═══
section "2. 系统崩溃日志 (最近10条)"
if command -v journalctl >/dev/null 2>&1; then
    journalctl --since "1 hour ago" -p err --no-pager | grep -E "(gatekeeper|longzhishou|failed|killed|segfault)" | tail -10 | tee -a "$REPORT_FILE"
else
    warn "journalctl 不可用，跳过系统日志"
fi

# ═══ 3. 服务日志 ═══
section "3. 应用日志最后20行"
for svc in gatekeeper longzhishou; do
    logfile="$LOG_DIR/${svc}.log"
    if [[ -f "$logfile" ]]; then
        info "--- $svc 日志 ---"
        tail -20 "$logfile" | tee -a "$REPORT_FILE"
    else
        warn "$svc 日志文件未找到: $logfile"
    fi
done

# ═══ 4. 资源检查 ═══
section "4. 系统资源"
# 磁盘
disk_usage=$(df -h / | awk 'NR==2{print $5}' | tr -d '%')
if [[ "$disk_usage" -gt 90 ]]; then
    fail "磁盘使用率 ${disk_usage}% (>90%)"
elif [[ "$disk_usage" -gt 80 ]]; then
    warn "磁盘使用率 ${disk_usage}% (>80%)"
else
    pass "磁盘使用率 ${disk_usage}%"
fi

# 内存
mem_info=$(free -m | awk 'NR==2{printf "%.1f", $3*100/$2}')
if (( $(echo "$mem_info > 90" | bc -l 2>/dev/null || echo "0") )); then
    fail "内存使用率 ${mem_info}% (>90%)"
else
    pass "内存使用率 ${mem_info}%"
fi

# 端口占用
section "5. 端口冲突检查"
for port in 8080 3000 5000; do
    pid=$(lsof -ti:$port 2>/dev/null)
    if [[ -n "$pid" ]]; then
        info "端口 $port 被 PID $pid 占用"
    fi
done

# ═══ 6. 依赖服务 ═══
section "6. 依赖服务状态"
# 检查常见依赖
deps=("docker" "nginx" "redis" "mysql" "postgresql")
for dep in "${deps[@]}"; do
    if pgrep -x "$dep" >/dev/null || pgrep -f "$dep" >/dev/null; then
        pass "$dep 运行中"
    else
        info "$dep 未运行 (如不需要可忽略)"
    fi
done

# ═══ 7. 配置校验 ═══
section "7. 配置文件检查"
for svc in gatekeeper longzhishou; do
    cfg="$HOME/.longhun/config/${svc}.conf"
    if [[ -f "$cfg" ]]; then
        pass "$cfg 存在"
        # 检查语法错误标记
        if grep -q "ERROR\|syntax\|invalid" "$cfg" 2>/dev/null; then
            fail "$cfg 包含错误标记"
        fi
    else
        warn "$cfg 不存在"
    fi
done

# ═══ 8. 自动修复建议 ═══
section "8. 修复建议"
cat << 'EOF' | tee -a "$REPORT_FILE"

常见修复路径:
1. 磁盘满 → 清理日志: find /var/log -name "*.log" -mtime +7 -delete
2. 内存溢出 → 检查是否有内存泄漏, 或增加swap
3. 端口冲突 → 修改配置文件中的端口, 或停止占用进程
4. 配置错误 → 恢复上一次备份配置, 逐步回滚
5. 依赖缺失 → 重新安装依赖包或重启依赖服务
6. 权限问题 → 检查服务运行用户是否有目录读写权限

紧急止血:
  systemctl stop gatekeeper longzhishou  # 停止死循环
  # 修复根因后
  systemctl start gatekeeper longzhishou

EOF

section "排查完成"
echo "报告已保存: $REPORT_FILE"
echo "执行: cat $REPORT_FILE 查看完整报告"
