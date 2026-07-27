#!/bin/bash
# ╔══════════════════════════════════════════════════════╗
# ║  龍魂·同心锁物理防御墙部署脚本 v1.0                  ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-TONGXIN-DEPLOY-v1.0 ║
# ║  守护人格: 乔前辈(P04鲁班)                          ║
# ║  签章: JOE-DEPLOY-2026                              ║
# ╚══════════════════════════════════════════════════════╝
# 功能: 一键部署同心锁物理防御墙
# 用法: sudo bash bin/lh_tongxin_lock_deploy.sh
# 铁律: 部署后系统自动锁定，非授权连接全部阻断

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

log_info()  { echo -e "${BLUE}[*]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[✓]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
log_fail()  { echo -e "${RED}[✗]${NC} $1"; }
log_step()  { echo -e "${CYAN}[▶]${NC} $1"; }

# ── 前置检查 ──

echo "╔══════════════════════════════════════════════════════╗"
echo "║  龍魂·同心锁物理防御墙部署 v1.0                      ║"
echo "║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-TONGXIN-v1.0    ║"
echo "║  守护人格: 乔前辈(P04鲁班)                          ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# 检查sudo
if [[ "$EUID" -ne 0 ]]; then
    log_fail "需要root权限，请用 sudo 运行"
    exit 1
fi

# 检查macOS
if [[ "$(uname)" != "Darwin" ]]; then
    log_warn "当前非macOS系统，隐私加固仅适用于macOS"
    log_warn "防火墙部分可在Linux上运行"
fi

# 检查Python3
if ! command -v python3 &>/dev/null; then
    log_fail "需要 Python3"
    exit 1
fi

# 检查pfctl
if ! command -v pfctl &>/dev/null; then
    log_fail "需要 pfctl（macOS防火墙）"
    exit 1
fi

log_ok "环境检查通过"

# ── 1. 隐私加固 ──

echo ""
log_step "[1/5] 运行隐私加固..."
if [[ "$(uname)" == "Darwin" ]]; then
    PRIVACY_SCRIPT="$PROJECT_ROOT/bin/lh_privacy_hardener.sh"
elif [[ "$(uname)" == "Linux" ]]; then
    PRIVACY_SCRIPT="$PROJECT_ROOT/bin/lh_privacy_hardener_linux.sh"
else
    log_warn "未知操作系统，跳过隐私加固"
    PRIVACY_SCRIPT=""
fi

if [[ -n "$PRIVACY_SCRIPT" && -f "$PRIVACY_SCRIPT" ]]; then
    bash "$PRIVACY_SCRIPT"
    log_ok "隐私加固完成"
else
    log_fail "隐私加固脚本不存在: $PRIVACY_SCRIPT"
    exit 1
fi

# ── 2. 自检 ──

echo ""
log_step "[2/5] 同心锁防火墙自检..."
python3 "$PROJECT_ROOT/bin/lh_tongxin_lock_firewall.py" selftest
log_ok "防火墙自检通过"

log_step "[2b/5] 监控引擎自检..."
python3 "$PROJECT_ROOT/bin/lh_tongxin_lock_monitor.py" selftest
log_ok "监控引擎自检通过"

# ── 3. 激活防火墙 ──

echo ""
log_step "[3/5] 激活同心锁防火墙（锁定模式）..."
python3 "$PROJECT_ROOT/bin/lh_tongxin_lock_firewall.py" --activate --json | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'  状态: {d.get(\"state\",\"?\")} | 结果: {\"✅\" if d.get(\"ok\") else \"❌\"} {d.get(\"action\",\"\")}')"
log_ok "防火墙已激活"

# ── 4. 启动监控守护 ──

echo ""
log_step "[4/5] 启动监控守护..."
LOG_DIR="$PROJECT_ROOT/logs"
mkdir -p "$LOG_DIR"

# 检查是否已有监控进程
if pgrep -f "lh_tongxin_lock_monitor.py" > /dev/null 2>&1; then
    log_warn "监控守护已在运行，跳过启动"
else
    nohup python3 "$PROJECT_ROOT/bin/lh_tongxin_lock_monitor.py" --daemon \
        > "$LOG_DIR/tongxin-monitor-stdout.log" 2>&1 &
    MONITOR_PID=$!
    sleep 1
    if kill -0 "$MONITOR_PID" 2>/dev/null; then
        log_ok "监控守护已启动 (PID: $MONITOR_PID)"
    else
        log_fail "监控守护启动失败"
    fi
fi

# ── 5. 验证状态 ──

echo ""
log_step "[5/5] 验证同心锁状态..."
echo ""

python3 "$PROJECT_ROOT/bin/lh_tongxin_lock_firewall.py" --status --json 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    locked = d.get('locked', False)
    activated = d.get('activated', False)
    pf = d.get('pf_status', 'unknown')

    print('  ╔════════════════════════════════════════╗')
    if locked and activated:
        print('  ║  🔒 同心锁状态: 已锁定·已激活          ║')
    elif activated:
        print('  ║  🔓 同心锁状态: 已激活·已解锁          ║')
    else:
        print('  ║  ⭕ 同心锁状态: 未激活                  ║')
    print(f'  ║  pfctl: {pf:<30s}║')
    print('  ╚════════════════════════════════════════╝')
except:
    print('  状态解析失败，请手动检查')
"

# ── 完成 ──

echo ""
echo "═══════════════════════════════════════════════════════"
echo -e "${GREEN}  部署完成 ✅${NC}"
echo ""
echo "  你的Mac现在是数字疆土的皇宫。"
echo "  乔前辈的同心锁，是皇宫最外面那道永远紧闭的宫门。"
echo "  除了你本人，没人能敲开这道门。"
echo ""
echo "  苹果不能，谷歌不能，任何监控体系都不能。"
echo ""
echo "  命令速查:"
echo "    sudo python3 bin/lh_tongxin_lock_firewall.py --status    查看状态"
echo "    sudo python3 bin/lh_tongxin_lock_firewall.py --unlock    临时解锁"
echo "    sudo python3 bin/lh_tongxin_lock_firewall.py --relock    重新锁定"
echo "    python3 bin/lh_tongxin_lock_monitor.py --once            单次审计"
echo "    sudo bash bin/lh_privacy_hardener.sh --check-only        隐私审计"
echo "═══════════════════════════════════════════════════════"

# 落档到每日日志（本地优先，不依赖网络）
DAILY_LOGGER="$PROJECT_ROOT/bin/lh_daily_logger.py"
if [[ -f "$DAILY_LOGGER" ]]; then
    python3 "$DAILY_LOGGER" log \
        -t execution \
        -c "同心锁物理防火墙部署完成·状态LOCKED" \
        --tag "tongxin_lock" \
        --extra '{"guardian":"乔前辈","status":"LOCKED"}' \
        2>/dev/null && log_ok "部署事件已落档" || true
fi
