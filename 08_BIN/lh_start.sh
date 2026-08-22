#!/usr/bin/env bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂系统一键启动入口 v1.0
# DNA: #龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-START-ENTRY-v1.0-UID9622
# 记不住命令？用这个。

set -e

REAL_SCRIPT="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$0")"
SCRIPT_DIR="$(cd "$(dirname "$REAL_SCRIPT")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LH="$ROOT/08_BIN/lh"

show_help() {
    echo ""
    echo "🐉 龍魂系统一键启动入口"
    echo "══════════════════════════════════════════════════"
    echo "用法: lh-start [选项]"
    echo ""
    echo "常用启动:"
    echo "  lh-start                 进入 lh 交互式控制台（33模块菜单）"
    echo "  lh-start --console       同上"
    echo "  lh-start --kunpeng       查看鲲鹏共生体状态"
    echo "  lh-start --status        全系统状态面板"
    echo "  lh-start --all           执行完整开机自启动脚本"
    echo "  lh-start --help          显示本帮助"
    echo ""
    echo "直接进入模块（等价于 lh 菜单选择）:"
    echo "  lh-start --core          轻量内核命令 (lh-core)"
    echo "  lh-start --time          时间引擎戳"
    echo "  lh-start --xpay          XPay支付"
    echo "  lh-start --hub           知识中枢"
    echo "  lh-start --valuation     估值报告"
    echo ""
    echo "鲲鹏自动AI:"
    echo "  lh-kunpeng status        状态"
    echo "  lh-kunpeng task \"指令\"  下发任务"
    echo "  lh-kunpeng monitor 3600  每小时自动巡检"
    echo ""
}

case "${1:-}" in
    ""|--console)
        exec "$LH"
        ;;
    --help|-h)
        show_help
        ;;
    --kunpeng)
        exec lh-kunpeng status
        ;;
    --status)
        python3 "$ROOT/bin/lh_unified_brain.py" status
        ;;
    --all)
        bash "$ROOT/08_BIN/lh_autostart.sh"
        ;;
    --core)
        shift || true
        exec lh-core "$@"
        ;;
    --time|--te)
        python3 "$ROOT/bin/lh_time_engine.py" --stamp
        ;;
    --xpay)
        shift || true
        "$LH" --xpay "${@:-balance}"
        ;;
    --hub)
        shift || true
        "$LH" --hub "${@:-status}"
        ;;
    --valuation)
        python3 "$ROOT/core/valuation/lh_valuation_template.py" --excel
        ;;
    *)
        echo "❌ 未知选项: $1"
        show_help
        exit 1
        ;;
esac
