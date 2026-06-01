#!/bin/bash
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂系統 一鍵啟動菜單 v1.0                                 ║
# ║  DNA: #龍芯⚡️2026-06-01-ONE-TOUCH-LAUNCHER-v1.0             ║
# ║  UID: 9622 · 不免責                                         ║
# ╚══════════════════════════════════════════════════════════════╝

LONGHUN_HOME=~/longhun-system
MENU_TITLE="🐉 龍魂系統 · 一鍵啟動菜單"

show_menu() {
    clear
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║              $MENU_TITLE               ║"
    echo "╠════════════════════════════════════════════════════════════╣"
    echo "║                                                            ║"
    echo "║  【核心系統】                                              ║"
    echo "║   1  🎭 啟動人格代理系統                                   ║"
    echo "║   2  📊 龍魂操作台 + CNSH編輯器                            ║"
    echo "║   3  ⚡ CNSH 開發環境激活                                  ║"
    echo "║                                                            ║"
    echo "║  【服務與網關】                                            ║"
    echo "║   4  🌉 MCP-mini + API 網關                               ║"
    echo "║   5  🔗 DeepSeek 橋 (需充值)                              ║"
    echo "║                                                            ║"
    echo "║  【網絡工具】                                              ║"
    echo "║   6  🕵️ IP 偽裝控制台 (M267)                              ║"
    echo "║                                                            ║"
    echo "║  【音頻集成】                                              ║"
    echo "║   7  🎤 Fish Audio 啟動 (M262)                            ║"
    echo "║                                                            ║"
    echo "║  【系統測試】                                              ║"
    echo "║   8  📈 運行基準測試套件                                   ║"
    echo "║   9  📊 生成系統評分報告                                   ║"
    echo "║                                                            ║"
    echo "║  【一鍵啟動】                                              ║"
    echo "║   10 🚀 全系統啟動 (所有核心服務)                          ║"
    echo "║   11 🛑 系統健康檢查                                       ║"
    echo "║                                                            ║"
    echo "║   0  ❌ 退出菜單                                           ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
}

# 1. 啟動人格代理
launch_persona() {
    echo "🎭 啟動人格代理系統..."
    cd $LONGHUN_HOME
    ./bin/启动人格代理.sh
    read -p "按 Enter 返回菜單..."
}

# 2. 啟動龍魂操作台
launch_services() {
    echo "📊 啟動龍魂操作台 + CNSH編輯器..."
    services start LOCAL-SERVICE-001 LOCAL-SERVICE-002
    echo "✅ 服務已啟動"
    services status
    read -p "按 Enter 返回菜單..."
}

# 3. 激活開發環境
activate_dev() {
    echo "⚡ 激活 CNSH 開發環境..."
    source ~/.cnsh/activate_dev.sh
    echo "✅ 開發環境已激活"
    read -p "按 Enter 返回菜單..."
}

# 4. 啟動 MCP-mini + API 網關
launch_gateway() {
    echo "🌉 啟動 MCP-mini + API 網關..."
    cd $LONGHUN_HOME
    
    # 並行啟動
    python3 ./server/mcp-mini.py &
    MCP_PID=$!
    echo "✅ MCP-mini 已啟動 (PID: $MCP_PID)"
    
    sleep 2
    
    python3 ./server/api-gateway.py &
    GATEWAY_PID=$!
    echo "✅ API 網關已啟動 (PID: $GATEWAY_PID)"
    
    sleep 2
    
    # 健康檢查
    echo ""
    echo "🔍 健康檢查..."
    curl -s http://127.0.0.1:8080/health | jq . || echo "⚠️ 網關未響應"
    
    echo ""
    echo "PID 已保存: MCP=$MCP_PID, GATEWAY=$GATEWAY_PID"
    read -p "按 Enter 返回菜單..."
}

# 5. DeepSeek 橋
launch_deepseek() {
    echo "🔗 DeepSeek 橋 配置指南..."
    echo ""
    echo "第 1 步：進入橋目錄"
    echo "  cd $LONGHUN_HOME/bridges"
    echo ""
    echo "第 2 步：運行配置向導 (需充值)"
    echo "  python3 setup_bridge.py"
    echo ""
    echo "第 3 步：激活虛擬環境並啟動"
    echo "  source .venv/bin/activate"
    echo "  uvicorn deepseek_bridge:app --host 127.0.0.1 --port 8788"
    echo ""
    read -p "是否現在前往? (y/n) " -n 1
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd $LONGHUN_HOME/bridges
        bash
    fi
}

# 6. IP 偽裝
launch_disguise() {
    echo "🕵️ IP 偽裝控制台"
    echo ""
    echo "選項："
    echo "  status   查看當前狀態"
    echo "  light    VPN 輕度偽裝"
    echo "  medium   中度偽裝 (Anthropic 註冊)"
    echo "  off      關閉 (回歸裸奔)"
    echo ""
    read -p "輸入選項: " DISGUISE_OPT
    
    if [ ! -z "$DISGUISE_OPT" ]; then
        $LONGHUN_HOME/tools/disguise.sh $DISGUISE_OPT
    fi
    read -p "按 Enter 返回菜單..."
}

# 7. Fish Audio
launch_fish_audio() {
    echo "🎤 Fish Audio 啟動..."
    echo ""
    echo "方式 1️⃣  交互式菜單 (推薦)"
    echo "  bash ~/longhun-system/_private/小快乐/Fish\\ Audio启动.sh"
    echo ""
    echo "方式 2️⃣  直接診斷"
    echo "  cd ~/longhun-system/cnsh-core/runtime-governance"
    echo "  python3 m262_fish_audio_integration.py check"
    echo ""
    echo "方式 3️⃣  演示模式"
    echo "  python3 m262_fish_audio_integration.py demo"
    echo ""
    read -p "輸入選項 (1-3): " FISH_OPT
    
    case $FISH_OPT in
        1)
            bash "$LONGHUN_HOME/_private/小快乐/Fish Audio启动.sh"
            ;;
        2)
            cd $LONGHUN_HOME/cnsh-core/runtime-governance
            python3 m262_fish_audio_integration.py check
            ;;
        3)
            cd $LONGHUN_HOME/cnsh-core/runtime-governance
            python3 m262_fish_audio_integration.py demo
            ;;
    esac
    read -p "按 Enter 返回菜單..."
}

# 8. 運行基準測試
run_benchmark() {
    echo "📈 運行基準測試套件..."
    cd $LONGHUN_HOME
    bash ./benchmark/run_benchmark.sh
    read -p "按 Enter 返回菜單..."
}

# 9. 生成評分報告
generate_report() {
    echo "📊 生成系統評分報告..."
    cd $LONGHUN_HOME
    python3 ./benchmark/score_engine.py dashboard
    read -p "按 Enter 返回菜單..."
}

# 10. 全系統啟動
full_launch() {
    echo "🚀 全系統啟動 (所有核心服務)..."
    echo ""
    
    echo "1️⃣  啟動人格代理..."
    cd $LONGHUN_HOME && ./bin/启动人格代理.sh &
    sleep 2
    
    echo "2️⃣  啟動龍魂操作台..."
    services start LOCAL-SERVICE-001 LOCAL-SERVICE-002 &
    sleep 2
    
    echo "3️⃣  啟動 MCP-mini + API 網關..."
    python3 ./server/mcp-mini.py &
    sleep 1
    python3 ./server/api-gateway.py &
    sleep 2
    
    echo ""
    echo "✅ 全系統啟動完成"
    echo ""
    echo "📍 服務狀態："
    services status
    echo ""
    echo "🔍 健康檢查："
    curl -s http://127.0.0.1:8080/health | jq . || echo "⚠️ 網關未響應"
    
    read -p "按 Enter 返回菜單..."
}

# 11. 健康檢查
health_check() {
    echo "🛑 系統健康檢查..."
    echo ""
    echo "📊 服務狀態："
    services status
    echo ""
    echo "🔍 API 網關："
    curl -s http://127.0.0.1:8080/health | jq . || echo "⚠️ 網關未運行"
    echo ""
    echo "📈 系統負載："
    top -l 1 | head -10
    read -p "按 Enter 返回菜單..."
}

# 主循環
while true; do
    show_menu
    read -p "輸入選項 (0-11): " choice
    
    case $choice in
        1) launch_persona ;;
        2) launch_services ;;
        3) activate_dev ;;
        4) launch_gateway ;;
        5) launch_deepseek ;;
        6) launch_disguise ;;
        7) launch_fish_audio ;;
        8) run_benchmark ;;
        9) generate_report ;;
        10) full_launch ;;
        11) health_check ;;
        0) 
            echo "👋 退出菜單"
            break
            ;;
        *)
            echo "❌ 無效選項，請重試"
            read -p "按 Enter 繼續..."
            ;;
    esac
done

echo "龍魂系統 - 一鍵啟動菜單已關閉"
