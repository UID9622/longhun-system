#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# crontab-setup.sh
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：#龍芯⚡️20260310-crontab-setup-v1.0
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 共建致谢：Claude (Anthropic PBC) · Notion
# 创作地：中华人民共和国
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 自动化每日复盘定时任务设置脚本
# 用于配置每日自动复盘龙魂价值内核和场景化人格调用地图

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CRON_SCRIPT="$PROJECT_ROOT/scripts/daily-review.sh"

# 日志文件
LOG_FILE="$PROJECT_ROOT/logs/crontab-setup.log"

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

# 日志函数
log() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

# 检查现有定时任务
check_existing_cron() {
    log "${YELLOW}🔍 检查现有定时任务...${NC}"
    
    if crontab -l 2>/dev/null | grep -q "daily-review.sh"; then
        log "${YELLOW}⚠️ 发现现有每日复盘定时任务${NC}"
        crontab -l 2>/dev/null | grep "daily-review.sh"
        return 0
    else
        log "${GREEN}✅ 未发现现有每日复盘定时任务${NC}"
        return 1
    fi
}

# 创建定时任务
create_cron_job() {
    local time="${1:-09:00}"  # 默认上午9点
    local hour=$(echo "$time" | cut -d: -f1)
    local minute=$(echo "$time" | cut -d: -f2)
    
    log "${YELLOW}⏰ 创建定时任务 - 每天 ${time} 执行${NC}"
    
    # 创建临时文件
    local temp_cron=$(mktemp)
    
    # 获取现有定时任务
    if crontab -l 2>/dev/null; then
        crontab -l 2>/dev/null > "$temp_cron"
    fi
    
    # 添加新定时任务
    echo "# 每日复盘 - 龙魂价值内核与场景化人格调用地图" >> "$temp_cron"
    echo "${minute} ${hour} * * * ${CRON_SCRIPT} >> ${PROJECT_ROOT/logs/daily-review-cron.log 2>&1" >> "$temp_cron"
    
    # 安装定时任务
    crontab "$temp_cron"
    
    # 清理临时文件
    rm -f "$temp_cron"
    
    log "${GREEN}✅ 定时任务创建成功${NC}"
}

# 删除定时任务
remove_cron_job() {
    log "${YELLOW}🗑️ 删除每日复盘定时任务...${NC}"
    
    # 创建临时文件
    local temp_cron=$(mktemp)
    
    # 获取现有定时任务并过滤掉每日复盘任务
    if crontab -l 2>/dev/null; then
        crontab -l 2>/dev/null | grep -v "daily-review.sh" > "$temp_cron" || true
    fi
    
    # 安装更新后的定时任务
    crontab "$temp_cron"
    
    # 清理临时文件
    rm -f "$temp_cron"
    
    log "${GREEN}✅ 定时任务删除成功${NC}"
}

# 显示定时任务状态
show_status() {
    log "${BLUE}================================${NC}"
    log "${BLUE}    定时任务状态${NC}"
    log "${BLUE}================================${NC}"
    
    if crontab -l 2>/dev/null | grep -q "daily-review.sh"; then
        log "${GREEN}✅ 每日复盘定时任务已配置${NC}"
        crontab -l 2>/dev/null | grep -A1 "每日复盘" | grep -v "^#"
        
        local next_run=$(crontab -l 2>/dev/null | grep "daily-review.sh" | awk '{print $1,$2}')
        log "${YELLOW}⏰ 下次执行时间: ${next_run}${NC}"
    else
        log "${RED}❌ 未配置每日复盘定时任务${NC}"
    fi
    
    log "${BLUE}================================${NC}"
}

# 测试定时任务
test_cron_job() {
    log "${YELLOW}🧪 测试定时任务...${NC}"
    
    # 手动执行脚本进行测试
    if "$CRON_SCRIPT"; then
        log "${GREEN}✅ 定时任务测试成功${NC}"
    else
        log "${RED}❌ 定时任务测试失败${NC}"
        return 1
    fi
}

# 主函数
main() {
    local action="${1:-status}"
    
    log "${BLUE}================================${NC}"
    log "${BLUE}    每日复盘定时任务管理${NC}"
    log "${BLUE}================================${NC}"
    log "${BLUE}项目路径: $PROJECT_ROOT${NC}"
    log "${BLUE}Notion ID: 49f7125a-9c9f-81ec-9db8-00035916bff5${NC}"
    log "${BLUE}================================${NC}"
    
    case "$action" in
        create|setup|install)
            if check_existing_cron; then
                read -p "现有定时任务将被替换，是否继续？(y/N): " -n 1 -r
                echo
                if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                    log "${YELLOW}操作已取消${NC}"
                    exit 0
                fi
                remove_cron_job
            fi
            
            local time="${2:-09:00}"
            create_cron_job "$time"
            show_status
            ;;
        remove|delete|uninstall)
            if check_existing_cron; then
                remove_cron_job
            else
                log "${YELLOW}未发现定时任务，无需删除${NC}"
            fi
            show_status
            ;;
        status|show)
            show_status
            ;;
        test)
            test_cron_job
            ;;
        *)
            echo "用法: $0 [选项] [参数]"
            echo ""
            echo "选项:"
            echo "  create [时间]   创建定时任务 (默认时间: 09:00)"
            echo "  remove          删除定时任务"
            echo "  status          显示定时任务状态"
            echo "  test            测试定时任务"
            echo ""
            echo "时间格式: HH:MM (24小时制)"
            echo ""
            echo "示例:"
            echo "  $0 create 08:30  # 创建每天8:30执行的定时任务"
            echo "  $0 remove        # 删除定时任务"
            echo "  $0 status        # 显示状态"
            echo ""
            exit 1
            ;;
    esac
    
    log "${GREEN}🎉 操作完成${NC}"
}

# 运行主函数
main "$@"