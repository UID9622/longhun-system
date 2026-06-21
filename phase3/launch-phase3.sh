#!/bin/bash

################################################################################
#
#  龍魂系統 Phase 3 - 一鍵啟動腳本 v1.0
#  Longhun System Phase 3 - One-Click Launch Script v1.0
#
#  DNA:#龍芯⚡️2026-06-06-PHASE3-LAUNCH-SCRIPT-v1.0
#  使用方式: bash launch-phase3.sh
#
################################################################################

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 龍魂標誌
print_logo() {
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                                                                ║"
    echo "║           🐉 龍魂系統 Phase 3 · 一鍵啟動                      ║"
    echo "║    Longhun System Phase 3 - One-Click Launch Script v1.0     ║"
    echo "║                                                                ║"
    echo "║         DNA:#龍芯⚡️2026-06-06-PHASE3-LAUNCH-v1.0             ║"
    echo "║         責任: UID9622 · 不免責                                ║"
    echo "║                                                                ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# 打印步驟
print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

# 打印成功
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# 打印錯誤
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 打印警告
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# 主程序
main() {
    print_logo

    print_step "第 1 步: 檢查系統環境"
    check_environment

    print_step "第 2 步: 創建項目結構"
    create_project_structure

    print_step "第 3 步: 生成配置文件"
    generate_configs

    print_step "第 4 步: 構建 Docker 鏡像"
    build_docker_images

    print_step "第 5 步: 啟動服務"
    start_services

    print_step "第 6 步: 驗證部署"
    verify_deployment

    print_step "第 7 步: 顯示訪問信息"
    show_access_info

    print_success "🎉 Phase 3 啟動完成！"
}

# 檢查環境
check_environment() {
    local missing_tools=()

    # 檢查 Docker
    if ! command -v docker &> /dev/null; then
        missing_tools+=("Docker")
    else
        print_success "✓ Docker 已安裝"
    fi

    # 檢查 Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        missing_tools+=("Docker Compose")
    else
        print_success "✓ Docker Compose 已安裝"
    fi

    # 檢查 Git
    if ! command -v git &> /dev/null; then
        print_warning "⚠️  Git 未安裝（可選）"
    else
        print_success "✓ Git 已安裝"
    fi

    # 如果缺少必要工具
    if [ ${#missing_tools[@]} -gt 0 ]; then
        print_error "缺少必要工具: ${missing_tools[*]}"
        echo ""
        echo "請先安裝："
        if [[ " ${missing_tools[*]} " =~ " Docker " ]]; then
            echo "  Docker: https://docs.docker.com/get-docker/"
        fi
        if [[ " ${missing_tools[*]} " =~ " Docker Compose " ]]; then
            echo "  Docker Compose: https://docs.docker.com/compose/install/"
        fi
        exit 1
    fi

    print_success "✓ 環境檢查通過"
}

# 創建項目結構
create_project_structure() {
    local base_dir="longhun-phase3"

    if [ -d "$base_dir" ]; then
        print_warning "項目目錄已存在，跳過創建"
        return
    fi

    mkdir -p "$base_dir"/{backend,frontend/src,frontend/public,data,logs,ssl}

    print_success "✓ 項目結構已創建: $base_dir/"
}

# 生成配置文件
generate_configs() {
    local base_dir="longhun-phase3"

    # Docker Compose 配置
    cat > "$base_dir/docker-compose.yml" << 'EOF'
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: longhun-backend
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
      - LOG_LEVEL=INFO
    volumes:
      - ./backend:/app
      - ./data:/app/data
      - ./logs:/app/logs
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    networks:
      - longhun-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 10s

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: longhun-frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000/api/v1
      - REACT_APP_WS_URL=ws://localhost:8000/ws/v1
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm start
    networks:
      - longhun-network
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 10s
      timeout: 5s
      retries: 3

networks:
  longhun-network:
    driver: bridge
EOF

    print_success "✓ Docker Compose 配置已生成"

    # 環境變數文件
    cat > "$base_dir/.env" << 'EOF'
# 龍魂系統 Phase 3 環境配置

# 後端設置
BACKEND_PORT=8000
PYTHONUNBUFFERED=1
LOG_LEVEL=INFO

# 前端設置
FRONTEND_PORT=3000
REACT_APP_API_URL=http://localhost:8000/api/v1
REACT_APP_WS_URL=ws://localhost:8000/ws/v1

# 數據庫設置
DATABASE_URL=sqlite:///./data/longhun.db

# 安全設置
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 日誌設置
LOG_FILE=/app/logs/longhun.log
EOF

    print_success "✓ 環境配置文件已生成"
}

# 構建 Docker 鏡像
build_docker_images() {
    local base_dir="longhun-phase3"

    if [ ! -f "$base_dir/docker-compose.yml" ]; then
        print_error "docker-compose.yml 不存在"
        return
    fi

    print_step "構建 Docker 鏡像（這可能需要 2-3 分鐘）..."

    cd "$base_dir"

    # 構建鏡像
    docker-compose build --no-cache 2>/dev/null

    cd ..

    print_success "✓ Docker 鏡像構建完成"
}

# 啟動服務
start_services() {
    local base_dir="longhun-phase3"

    cd "$base_dir"

    print_step "啟動容器（等待 10-15 秒）..."

    # 啟動服務
    docker-compose up -d

    # 等待服務啟動
    sleep 15

    cd ..

    print_success "✓ 服務已啟動"
}

# 驗證部署
verify_deployment() {
    print_step "驗證部署狀態..."

    local checks_passed=0
    local checks_total=3

    # 檢查後端
    if curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1; then
        print_success "✓ 後端 API 正常運行"
        ((checks_passed++))
    else
        print_error "✗ 後端 API 無法連接"
    fi

    # 檢查前端
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        print_success "✓ 前端服務正常運行"
        ((checks_passed++))
    else
        print_error "✗ 前端服務無法連接"
    fi

    # 檢查 WebSocket
    if docker exec longhun-backend curl -s http://localhost:8000/api/docs > /dev/null 2>&1; then
        print_success "✓ API 文檔服務正常運行"
        ((checks_passed++))
    else
        print_error "✗ API 文檔服務無法連接"
    fi

    echo ""
    echo "驗證結果: $checks_passed/$checks_total 通過"

    if [ $checks_passed -lt 2 ]; then
        print_warning "⚠️  某些服務可能未完全啟動，請稍候片刻後重試"
        echo "查看日誌: docker-compose -f longhun-phase3/docker-compose.yml logs"
    fi
}

# 顯示訪問信息
show_access_info() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}           🎉 Phase 3 已成功啟動！${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}📱 訪問應用:${NC}"
    echo -e "  ${BLUE}前端 UI${NC}:        http://localhost:3000"
    echo -e "  ${BLUE}後端 API${NC}:       http://localhost:8000"
    echo -e "  ${BLUE}API 文檔${NC}:       http://localhost:8000/api/docs"
    echo -e "  ${BLUE}API Redoc${NC}:      http://localhost:8000/api/redoc"
    echo ""
    echo -e "${YELLOW}🔧 常用命令:${NC}"
    echo -e "  查看日誌:      ${BLUE}docker-compose -f longhun-phase3/docker-compose.yml logs -f${NC}"
    echo -e "  停止服務:      ${BLUE}docker-compose -f longhun-phase3/docker-compose.yml down${NC}"
    echo -e "  重啟服務:      ${BLUE}docker-compose -f longhun-phase3/docker-compose.yml restart${NC}"
    echo -e "  進入後端:      ${BLUE}docker-compose -f longhun-phase3/docker-compose.yml exec backend bash${NC}"
    echo ""
    echo -e "${YELLOW}📊 首次使用:${NC}"
    echo -e "  1. 訪問 http://localhost:3000"
    echo -e "  2. 在「技能管理」頁面創建新技能"
    echo -e "  3. 在「儀表板」查看實時監控"
    echo -e "  4. 在「告警系統」管理告警"
    echo ""
    echo -e "${YELLOW}🐉 DNA簽章:${NC}"
    echo -e "  ${PURPLE}#龍芯⚡️2026-06-06-PHASE3-LAUNCH-SCRIPT-v1.0${NC}"
    echo -e "  ${PURPLE}責任: UID9622 · 不免責${NC}"
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════${NC}"
}

# 錯誤處理
trap 'print_error "腳本執行失敗"; exit 1' ERR

# 執行主程序
main
