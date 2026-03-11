#!/bin/bash

# ══════════════════════════════════════════════════════
#    🇨🇳  UID9622 CNSH 系统 | Made in China • By 诸葛鑫
#    中国创新 · 世界共享 · 铜墙铁壁
# ══════════════════════════════════════════════════════

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# 清屏
clear

# 显示横幅
echo -e "${CYAN}"
echo "═══════════════════════════════════════════════════════"
echo "   🇨🇳  UID9622 CNSH 系统 | Made in China          "
echo "   中国创新 · 世界共享 · 铜墙铁壁                  "
echo "═══════════════════════════════════════════════════════"
echo -e "${NC}"
echo ""

# 项目目录
CNSH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$CNSH_DIR/logs/cnsh-unified.log"
PID_FILE="$CNSH_DIR/logs/cnsh-unified.pid"

# 创建日志目录
mkdir -p "$CNSH_DIR/logs"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo -e "$1"
}

# 检查进程状态
check_status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            return 0  # 运行中
        else
            rm -f "$PID_FILE"  # 清理无效的PID文件
            return 1  # 已停止
        fi
    else
        return 1  # 已停止
    fi
}

# 启动CNSH核心服务器
start_cnsh() {
    if [ -f "$CNSH_DIR/logs/cnsh-server.pid" ]; then
        SERVER_PID=$(cat "$CNSH_DIR/logs/cnsh-server.pid")
        if ps -p "$SERVER_PID" > /dev/null 2>&1; then
            log "${GREEN}✅ CNSH核心服务器已在运行 (PID: $SERVER_PID)${NC}"
            return 0
        fi
    fi
    
    log "${YELLOW}🚀 启动CNSH核心服务器...${NC}"
    cd "$CNSH_DIR"
    
    # 检查依赖
    if [ ! -d "node_modules" ]; then
        log "${YELLOW}📦 正在安装依赖...${NC}"
        npm install
    fi
    
    # 启动服务器
    nohup npm start > "$CNSH_DIR/logs/cnsh-server.log" 2>&1 &
    SERVER_PID=$!
    echo "$SERVER_PID" > "$CNSH_DIR/logs/cnsh-server.pid"
    
    sleep 2
    if ps -p "$SERVER_PID" > /dev/null 2>&1; then
        log "${GREEN}✅ CNSH核心服务器已启动 (PID: $SERVER_PID)${NC}"
        log "${CYAN}📋 服务器日志: $CNSH_DIR/logs/cnsh-server.log${NC}"
        log "${CYAN}🌐 服务器地址: http://localhost:8080${NC}"
    else
        log "${RED}❌ CNSH核心服务器启动失败${NC}"
        return 1
    fi
}

# 启动Notion监控器
start_notion_monitor() {
    if [ -f "$CNSH_DIR/.notion-monitor.pid" ]; then
        MONITOR_PID=$(cat "$CNSH_DIR/.notion-monitor.pid")
        if ps -p "$MONITOR_PID" > /dev/null 2>&1; then
            log "${GREEN}✅ Notion监控器已在运行 (PID: $MONITOR_PID)${NC}"
            return 0
        fi
    fi
    
    log "${YELLOW}🔍 启动Notion页面监控器...${NC}"
    
    # 启动监控器
    nohup node "$CNSH_DIR/notion-monitor.js" > "$CNSH_DIR/logs/notion-monitor.log" 2>&1 &
    MONITOR_PID=$!
    echo "$MONITOR_PID" > "$CNSH_DIR/.notion-monitor.pid"
    
    sleep 2
    if ps -p "$MONITOR_PID" > /dev/null 2>&1; then
        log "${GREEN}✅ Notion监控器已启动 (PID: $MONITOR_PID)${NC}"
        log "${CYAN}📝 监控器日志: $CNSH_DIR/logs/notion-monitor.log${NC}"
        log "${CYAN}🔗 监控页面: $CNSH_DIR/notion-monitor-daemon.sh logs${NC}"
    else
        log "${RED}❌ Notion监控器启动失败${NC}"
        return 1
    fi
}

# 显示系统状态
show_status() {
    echo -e "${BLUE}══════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}📊 CNSH系统状态总览${NC}"
    echo -e "${BLUE}══════════════════════════════════════════════════════${NC}"
    echo ""
    
    # CNSH核心服务器状态
    if [ -f "$CNSH_DIR/logs/cnsh-server.pid" ]; then
        SERVER_PID=$(cat "$CNSH_DIR/logs/cnsh-server.pid")
        if ps -p "$SERVER_PID" > /dev/null 2>&1; then
            echo -e "🌐 CNSH核心服务器: ${GREEN}运行中${NC} (PID: $SERVER_PID)"
        else
            echo -e "🌐 CNSH核心服务器: ${RED}已停止${NC}"
        fi
    else
        echo -e "🌐 CNSH核心服务器: ${RED}未启动${NC}"
    fi
    
    # Notion监控器状态
    if [ -f "$CNSH_DIR/.notion-monitor.pid" ]; then
        MONITOR_PID=$(cat "$CNSH_DIR/.notion-monitor.pid")
        if ps -p "$MONITOR_PID" > /dev/null 2>&1; then
            echo -e "🔍 Notion监控器: ${GREEN}运行中${NC} (PID: $MONITOR_PID)"
        else
            echo -e "🔍 Notion监控器: ${RED}已停止${NC}"
        fi
    else
        echo -e "🔍 Notion监控器: ${RED}未启动${NC}"
    fi
    
    # 法律知识库状态
    if [ -d "$CNSH_DIR/legal-knowledge" ]; then
        echo -e "⚖️ 全球法律知识库: ${GREEN}已集成${NC}"
    else
        echo -e "⚖️ 全球法律知识库: ${RED}未集成${NC}"
    fi
    
    echo ""
    echo -e "${BLUE}══════════════════════════════════════════════════════${NC}"
}

# 停止所有服务
stop_all() {
    log "${YELLOW}🛑 正在停止所有CNSH服务...${NC}"
    
    # 停止CNSH核心服务器
    if [ -f "$CNSH_DIR/logs/cnsh-server.pid" ]; then
        SERVER_PID=$(cat "$CNSH_DIR/logs/cnsh-server.pid")
        if ps -p "$SERVER_PID" > /dev/null 2>&1; then
            kill "$SERVER_PID"
            rm -f "$CNSH_DIR/logs/cnsh-server.pid"
            log "${GREEN}✅ CNSH核心服务器已停止${NC}"
        fi
    fi
    
    # 停止Notion监控器
    if [ -f "$CNSH_DIR/.notion-monitor.pid" ]; then
        MONITOR_PID=$(cat "$CNSH_DIR/.notion-monitor.pid")
        if ps -p "$MONITOR_PID" > /dev/null 2>&1; then
            kill "$MONITOR_PID"
            rm -f "$CNSH_DIR/.notion-monitor.pid"
            log "${GREEN}✅ Notion监控器已停止${NC}"
        fi
    fi
    
    log "${GREEN}✅ 所有CNSH服务已停止${NC}"
}

# 显示帮助信息
show_help() {
    echo -e "${WHITE}CNSH统一管理系统 - 帮助${NC}"
    echo ""
    echo -e "${CYAN}用法: $0 [命令]${NC}"
    echo ""
    echo -e "${WHITE}命令:${NC}"
    echo -e "  start         ${GREEN}启动所有服务${NC}"
    echo -e "  stop          ${RED}停止所有服务${NC}"
    echo -e "  restart       ${YELLOW}重启所有服务${NC}"
    echo -e "  status        ${BLUE}显示服务状态${NC}"
    echo -e "  server        ${GREEN}仅启动CNSH核心服务器${NC}"
    echo -e "  monitor       ${GREEN}仅启动Notion监控器${NC}"
    echo -e "  logs          ${CYAN}查看所有日志${NC}"
    echo -e "  transparency  ${PURPLE}查看UID9622透明声明${NC}"
    echo -e "  update        ${PURPLE}更新系统${NC}"
    echo -e "  help          ${WHITE}显示此帮助信息${NC}"
    echo ""
    echo -e "${YELLOW}示例:${NC}"
    echo -e "  $0 start      ${GREEN}# 启动所有CNSH服务${NC}"
    echo -e "  $0 status     ${BLUE}# 查看服务状态${NC}"
    echo -e "  $0 logs       ${CYAN}# 查看日志${NC}"
    echo -e "  $0 transparency${PURPLE}# 查看透明声明${NC}"
    echo ""
}

# 查看日志
show_logs() {
    echo -e "${CYAN}══════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}📝 CNSH系统日志${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════════${NC}"
    echo ""
    
    if [ -f "$CNSH_DIR/logs/cnsh-server.log" ]; then
        echo -e "${YELLOW}🌐 CNSH核心服务器日志 (最近20行):${NC}"
        tail -n 20 "$CNSH_DIR/logs/cnsh-server.log"
        echo ""
    fi
    
    if [ -f "$CNSH_DIR/logs/notion-monitor.log" ]; then
        echo -e "${YELLOW}🔍 Notion监控器日志 (最近20行):${NC}"
        tail -n 20 "$CNSH_DIR/logs/notion-monitor.log"
        echo ""
    fi
    
    if [ -f "$LOG_FILE" ]; then
        echo -e "${YELLOW}📋 统一管理系统日志 (最近20行):${NC}"
        tail -n 20 "$LOG_FILE"
        echo ""
    fi
    
    echo -e "${CYAN}══════════════════════════════════════════════════════${NC}"
    echo -e "${WHITE}💡 实时查看日志: tail -f $LOG_FILE${NC}"
    echo -e "${WHITE}💡 查看服务器日志: tail -f $CNSH_DIR/logs/cnsh-server.log${NC}"
    echo -e "${WHITE}💡 查看监控器日志: tail -f $CNSH_DIR/logs/notion-monitor.log${NC}"
}

# 显示透明声明
show_transparency() {
    TRANSPARENCY_FILE="$CNSH_DIR/UID9622_TRANSPARENCY.md"
    
    if [ -f "$TRANSPARENCY_FILE" ]; then
        # 检查是否安装了less或more命令
        if command -v less &>/dev/null; then
            less "$TRANSPARENCY_FILE"
        elif command -v more &>/dev/null; then
            more "$TRANSPARENCY_FILE"
        else
            # 如果没有分页器，则显示前50行
            echo -e "${CYAN}══════════════════════════════════════════════════════${NC}"
            echo -e "${WHITE}💎 UID9622 透明声明${NC}"
            echo -e "${CYAN}══════════════════════════════════════════════════════${NC}"
            echo ""
            head -n 50 "$TRANSPARENCY_FILE"
            echo ""
            echo -e "${WHITE}💡 完整声明位于: $TRANSPARENCY_FILE${NC}"
        fi
    else
        echo -e "${RED}❌ 透明声明文件不存在${NC}"
        echo -e "${WHITE}文件路径: $TRANSPARENCY_FILE${NC}"
    fi
}

# 更新系统
update_system() {
    log "${PURPLE}🔄 更新CNSH系统...${NC}"
    
    cd "$CNSH_DIR"
    git pull origin main
    npm install
    
    log "${GREEN}✅ 系统更新完成${NC}"
    log "${YELLOW}💡 建议重启服务以应用更新${NC}"
}

# 主菜单
show_menu() {
    while true; do
        clear
        echo -e "${CYAN}"
        echo "═══════════════════════════════════════════════════════"
        echo "   🇨🇳  UID9622 CNSH 系统 | Made in China          "
        echo "   中国创新 · 世界共享 · 铜墙铁壁                  "
        echo "═══════════════════════════════════════════════════════"
        echo -e "${NC}"
        echo ""
        
        show_status
        
        echo ""
        echo -e "${WHITE}请选择操作:${NC}"
        echo -e "  ${GREEN}1)${NC} 启动所有服务"
        echo -e "  ${RED}2)${NC} 停止所有服务"
        echo -e "  ${YELLOW}3)${NC} 重启所有服务"
        echo -e "  ${BLUE}4)${NC} 仅启动CNSH核心服务器"
        echo -e "  ${BLUE}5)${NC} 仅启动Notion监控器"
        echo -e "  ${CYAN}6)${NC} 查看服务状态"
        echo -e "  ${CYAN}7)${NC} 查看日志"
        echo -e "  ${PURPLE}8)${NC} 查看UID9622透明声明"
        echo -e "  ${PURPLE}9)${NC} 更新系统"
        echo -e "  ${WHITE}10)${NC} 退出"
        echo ""
        read -p "请输入选项 [1-10]: " choice
        
        case $choice in
            1)
                start_cnsh
                start_notion_monitor
                read -p "按回车键继续..."
                ;;
            2)
                stop_all
                read -p "按回车键继续..."
                ;;
            3)
                stop_all
                sleep 2
                start_cnsh
                start_notion_monitor
                read -p "按回车键继续..."
                ;;
            4)
                start_cnsh
                read -p "按回车键继续..."
                ;;
            5)
                start_notion_monitor
                read -p "按回车键继续..."
                ;;
            6)
                show_status
                read -p "按回车键继续..."
                ;;
            7)
                show_logs
                read -p "按回车键继续..."
                ;;
            8)
                show_transparency
                read -p "按回车键继续..."
                ;;
            9)
                update_system
                read -p "按回车键继续..."
                ;;
            10)
                echo -e "${GREEN}再见！${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}无效选项，请重新选择${NC}"
                sleep 1
                ;;
        esac
    done
}

# 主逻辑
case "${1:-menu}" in
    start)
        start_cnsh
        start_notion_monitor
        ;;
    stop)
        stop_all
        ;;
    restart)
        stop_all
        sleep 2
        start_cnsh
        start_notion_monitor
        ;;
    status)
        show_status
        ;;
    server)
        start_cnsh
        ;;
    monitor)
        start_notion_monitor
        ;;
    logs)
        show_logs
        ;;
    transparency)
        show_transparency
        ;;
    update)
        update_system
        ;;
    help)
        show_help
        ;;
    menu)
        show_menu
        ;;
    *)
        echo -e "${RED}未知命令: $1${NC}"
        show_help
        exit 1
        ;;
esac
# Notion数据库管理
notion_menu() {
    clear
    echo "📋 Notion数据库管理"
    echo "===================="
    echo "1) 配置Notion API"
    echo "2) 测试DNA注册"
    echo "3) 测试举报处理"
    echo "4) 完整集成测试"
        5) 
            notion_menu 
            ;;
    echo "5) 查看集成指南"
    echo "6) 返回主菜单"
    echo ""
    read -p "请选择操作 [1-6]: " notion_choice
    
    case $notion_choice in
        1)
            echo "📝 配置Notion API..."
            if [ ! -f ".env" ]; then
                cp .env.notion.template .env
                echo "✅ 已创建.env文件，请编辑并填入正确的API密钥和数据库ID"
                echo "🔗 获取API密钥: https://www.notion.so/my-integrations"
                echo "📋 数据库ID在Notion宝宝创建的数据库URL中"
                echo "💡 编辑命令: nano .env"
            else
                echo "✅ .env文件已存在"
                echo "💡 编辑命令: nano .env"
            fi
            read -p "按回车键继续..."
            ;;
        2)
            echo "🧪 测试DNA注册..."
            python test-notion-integration.py | grep -A 10 "测试DNA注册功能"
            read -p "按回车键继续..."
            ;;
        3)
            echo "🧪 测试举报处理..."
            python test-notion-integration.py | grep -A 10 "测试举报处理功能"
            read -p "按回车键继续..."
            ;;
        4)
            echo "🚀 完整集成测试..."
            python test-notion-integration.py
            read -p "按回车键继续..."
            ;;
        5)
            echo "📖 查看集成指南..."
            if command -v less > /dev/null; then
                less notion-databases-integration.md
            else
                cat notion-databases-integration.md
            fi
            ;;
        6)
            return
            ;;
        *)
            echo "❌ 无效选择，请重新输入"
            sleep 1
            notion_menu
            ;;
    esac
}
