#!/bin/bash
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂系統 快速啟動 v1.0 (無菜單直接啟動)                   ║
# ║  用法: ./快速启动.sh [服務名]                               ║
# ║  或使用別名: 人格启动 / 全启 / 体检 / IP伪装 / 鱼音          ║
# ╚══════════════════════════════════════════════════════════════╝

LONGHUN_HOME=~/longhun-system
SERVICE=$1

if [ -z "$SERVICE" ]; then
    echo "❌ 請指定服務"
    echo ""
    echo "用法: ./快速启动.sh [service]"
    echo ""
    echo "可用服務:"
    echo "  persona      人格代理"
    echo "  services     龍魂操作台 + CNSH編輯器"
    echo "  gateway      MCP-mini + API 網關"
    echo "  benchmark    基準測試"
    echo "  report       生成評分報告"
    echo "  full         全系統啟動"
    echo "  health       系統健康檢查"
    echo ""
    exit 1
fi

case $SERVICE in
    persona|人格)
        echo "🎭 啟動人格代理系統..."
        cd $LONGHUN_HOME
        ./bin/启动人格代理.sh
        ;;
    
    services|服务)
        echo "📊 啟動龍魂操作台..."
        services start-all
        services status
        ;;
    
    gateway|网关)
        echo "🌉 啟動 MCP-mini + API 網關..."
        cd $LONGHUN_HOME
        python3 ./server/mcp-mini.py &
        sleep 1
        python3 ./server/api-gateway.py &
        sleep 2
        curl -s http://127.0.0.1:8080/health | jq .
        ;;
    
    benchmark|测试)
        echo "📈 運行基準測試..."
        cd $LONGHUN_HOME
        bash ./benchmark/run_benchmark.sh
        ;;
    
    report|报告)
        echo "📊 生成評分報告..."
        cd $LONGHUN_HOME
        python3 ./benchmark/score_engine.py dashboard
        ;;
    
    full|全启)
        echo "🚀 全系統啟動..."
        cd $LONGHUN_HOME
        ./bin/启动人格代理.sh &
        sleep 2
        services start-all &
        sleep 2
        python3 ./server/mcp-mini.py &
        sleep 1
        python3 ./server/api-gateway.py &
        sleep 2
        echo "✅ 全系統已啟動"
        services status
        curl -s http://127.0.0.1:8080/health | jq .
        ;;
    
    health|检查)
        echo "🛑 系統健康檢查..."
        services status
        echo ""
        curl -s http://127.0.0.1:8080/health | jq . || echo "⚠️ 網關未運行"
        ;;
    
    *)
        echo "❌ 未知服務: $SERVICE"
        exit 1
        ;;
esac
