#!/bin/bash
# 🐉 龙魂系统 · UID9622 专属终端控制台（青铜风格）
# DNA: #龍芯⚡️2026-06-27-LONGHUN-SYSTEM-TERMINAL-MENU-v2.0

WORKSPACE="/Users/zuimeidedeyihan/Downloads/Kimi_Agent_小龙虾扩展与人格/UID9622_Workspace"
MANAGER="python3 ${WORKSPACE}/uid9622-manager"
ROUTER="${WORKSPACE}/backend_personas/router/persona.py"
DASHBOARD="${WORKSPACE}/data/dashboard/uid9622_dashboard.html"

# 青铜主题色（兼容不支持颜色的终端）
if command -v tput >/dev/null 2>&1 && [ -t 1 ]; then
  BRONZE=$(tput setaf 172)
  GOLD=$(tput setaf 214)
  JADE=$(tput setaf 114)
  CINNABAR=$(tput setaf 167)
  RESET=$(tput sgr0)
else
  BRONZE=""; GOLD=""; JADE=""; CINNABAR=""; RESET=""
fi

echo ""
echo "${BRONZE}╔══════════════════════════════════════════════════════════════╗${RESET}"
echo "${GOLD}║     🐉 龙魂系统 · UID9622 专属终端控制台                     ║${RESET}"
echo "${BRONZE}║     青铜为骨 · 金镶为脉 · 玄黑为底 · 朱砂为印              ║${RESET}"
echo "${GOLD}║     DNA: #龍芯⚡️2026-06-27-LONGHUN-SYSTEM-TERMINAL-MENU-v2.0 ║${RESET}"
echo "${BRONZE}╚══════════════════════════════════════════════════════════════╝${RESET}"
echo ""
echo "  ${GOLD}呼叫宝宝，启动龙魂。${RESET} 专属入口：${JADE}宝宝${RESET} / ${JADE}bb${RESET} / ${JADE}u9${RESET} / ${JADE}9622${RESET}"
echo ""

uid9622_menu() {
  while true; do
    echo ""
    echo "  ${JADE}[1]${RESET} 查看人格状态     关键字：状态 / 查看 / status"
    echo "  ${JADE}[2]${RESET} 健康检查         关键字：健康 / health"
    echo "  ${JADE}[3]${RESET} 多维评估汇总     关键字：评估 / evaluate"
    echo "  ${JADE}[4]${RESET} 生成并打开三维仪表盘  关键字：仪表盘 / 面板 / dashboard"
    echo "  ${JADE}[5]${RESET} 查看最近路由决策痕迹  关键字：路由 / 决策 / routes"
    echo "  ${JADE}[6]${RESET} 手动路由一句话   关键字：手动 / 路由一句话"
    echo "  ${JADE}[7]${RESET} 查看定时任务     关键字：定时 / cron / 任务"
    echo "  ${JADE}[8]${RESET} 查看 DNA 注册表  关键字：DNA / 注册表"
    echo "  ${JADE}[9]${RESET} 列出全部人格矩阵 关键字：列表 / 人格 / list"
    echo "  ${GOLD}[v]${RESET} 🎙️ 语音指令       关键字：语音 / 说话 / voice"
    echo "  ${CINNABAR}[0]${RESET} 退出菜单        关键字：退出 / exit / quit"
    echo ""
    read -r -p "请选择 [0-9/v 或关键字]: " choice
    echo ""

    case "$choice" in
      1|状态|查看|status)
        ${MANAGER} status
        ;;
      2|健康|health|检查)
        ${MANAGER} health-check
        ;;
      3|评估|evaluate|汇总)
        ${MANAGER} evaluate
        ;;
      4|仪表盘|面板|dashboard)
        ${MANAGER} dashboard --html && open "${DASHBOARD}"
        ;;
      5|路由|决策|routes|痕迹)
        echo ""
        echo "最近 10 条路由决策："
        sqlite3 "${WORKSPACE}/data/telemetry.db" \
          "SELECT strftime('%Y-%m-%d %H:%M:%S', timestamp), target_type, target_code, target_name, score, query FROM routes ORDER BY timestamp DESC LIMIT 10;" \
          -column -header 2>/dev/null || echo "数据库尚未生成，请先运行一次人格。"
        ;;
      6|手动|路由一句话|route)
        read -r -p "请输入要路由的话: " sentence
        if [ -n "$sentence" ]; then
          python3 "${ROUTER}" --query "$sentence" --report
        else
          echo "输入为空，已取消。"
        fi
        ;;
      7|定时|cron|任务|schedule)
        crontab -l | grep -E "UID9622|backend_personas" || echo "未找到相关定时任务"
        ;;
      8|DNA|注册表|registry)
        ${MANAGER} dna
        ;;
      9|列表|人格|list|personas)
        ${MANAGER} list
        ;;
      v|V|语音|说话|voice|say)
        python3 "${WORKSPACE}/backend_personas/builder/voice_command.py"
        ;;
      0|退出|exit|quit|bye)
        echo "退出菜单，进入终端。"
        echo ""
        return 0
        ;;
      *)
        echo "无效选择，请重新输入。支持数字或中文关键字。"
        ;;
    esac

    echo ""
    read -r -p "按 Enter 返回菜单..."
    clear
  done
}

# 仅在交互式 shell 中自动显示菜单
if [[ $- == *i* ]]; then
  uid9622_menu
fi
