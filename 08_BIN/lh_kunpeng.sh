#!/usr/bin/env bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍芯·鲲鹏共生体快捷入口 v1.0
# DNA: #龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-KUNPENG-ENTRY-v1.0-UID9622
# 一句话：你在本地发号，20个人格在鲲鹏冲锋。

set -e

# 兼容符号链接：先解析真实路径
REAL_SCRIPT="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$0")"
SCRIPT_DIR="$(cd "$(dirname "$REAL_SCRIPT")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
AGENT="$ROOT/08_BIN/lh_agent_kunpeng.py"

show_help() {
    echo ""
    echo "🐉 龍芯·鲲鹏共生体快捷入口"
    echo "══════════════════════════════════════════════════"
    echo "用法: lh-kunpeng <command> [args...]"
    echo ""
    echo "命令:"
    echo "  status            查看共生体状态（鲲鹏在线/任务/人格）"
    echo "  check             完整自检（SSH+引擎+本地路由）"
    echo "  sync              同步最新代码到鲲鹏并验证引擎"
    echo "  demo              演示调度一次战略推演任务"
    echo "  task <指令>       向鲲鹏下发一句话任务"
    echo "  monitor <秒>      每隔N秒自动下发一次系统自检任务"
    echo "  help              显示本帮助"
    echo ""
    echo "示例:"
    echo "  lh-kunpeng status"
    echo "  lh-kunpeng sync"
    echo "  lh-kunpeng task \"评估当前系统状态\""
    echo "  lh-kunpeng task \"推演下季度战略方向\" --persona 诸葛亮"
    echo "  lh-kunpeng monitor 3600   # 每小时自动巡检一次"
    echo ""
    echo "等效调用:"
    echo "  python3 $AGENT status|check|sync|demo"
    echo "  python3 $AGENT --task \"指令\""
    echo ""
}

if [ $# -lt 1 ]; then
    show_help
    exit 0
fi

CMD="$1"
shift

case "$CMD" in
    status)
        python3 "$AGENT" status
        ;;
    check)
        python3 "$AGENT" check
        ;;
    sync|deploy)
        python3 "$AGENT" sync
        ;;
    demo)
        python3 "$AGENT" demo
        ;;
    task)
        if [ $# -lt 1 ]; then
            echo "❌ 请提供任务指令，例如: lh-kunpeng task \"评估系统状态\""
            exit 1
        fi
        # 支持 --persona 透传
        python3 "$AGENT" --task "$@"
        ;;
    monitor)
        INTERVAL="${1:-3600}"
        if ! [[ "$INTERVAL" =~ ^[0-9]+$ ]]; then
            echo "❌ monitor 参数需为秒数，例如: lh-kunpeng monitor 3600"
            exit 1
        fi
        echo "🐉 启动鲲鹏自动巡检（间隔 ${INTERVAL}秒）·按 Ctrl+C 停止"
        while true; do
            echo ""
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] 自动下发系统巡检任务..."
            python3 "$AGENT" --task "系统状态巡检·生成三色审计摘要" || true
            echo "   下次执行: ${INTERVAL}秒后"
            sleep "$INTERVAL"
        done
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ 未知命令: $CMD"
        show_help
        exit 1
        ;;
esac
