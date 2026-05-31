#!/bin/bash
# 🐉 CNSH 基准测试运行脚本 v1.0
# DNA: #龍芯⚇️2026-05-31-BENCHMARK-RUN-v1.0
# 功能：一键运行全套CNSH基准测试

set -e

BENCHMARK_DIR="$HOME/longhun-system/benchmark"
CONFIG_DIR="$HOME/.龍魂"

echo ""
echo "════════════════════════════════════════════════════════"
echo "🐉 CNSH 基准测试系统 v1.0"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📍 开始时间: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "📍 工作目录: $BENCHMARK_DIR"
echo "📍 配置目录: $CONFIG_DIR"
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 python3"
    exit 1
fi

echo "✅ Python3 环境就绪"
echo ""

# 步骤1：显示测试统计
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 第1步: 测试套件统计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd "$BENCHMARK_DIR"
python3 standard_test_suite.py stat

echo ""

# 步骤2：生成数据采集示例
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 第2步: 数据采集器状态"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 capture_output.py stat || echo "⚠️  暂无采集数据"

echo ""

# 步骤3: 尝试生成报告
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📈 第3步: 性能报告生成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 score_engine.py report || echo "⚠️  暂无评分数据"

echo ""

# 步骤4: 生成Markdown报告
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 第4步: 生成Markdown格式报告"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 score_engine.py markdown || echo "⚠️  暂无数据生成报告"

echo ""

# 步骤5: 生成仪表板
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 第5步: 生成仪表板JSON"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python3 score_engine.py dashboard || echo "⚠️  暂无数据生成仪表板"

echo ""

# 最终输出
echo "════════════════════════════════════════════════════════"
echo "✅ 基准测试系统初始化完成"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📁 文件位置:"
echo "  · 采集数据库: $CONFIG_DIR/benchmark.jsonl"
echo "  · 报告目录: $CONFIG_DIR/benchmark_reports/"
echo "  · 仪表板: $CONFIG_DIR/benchmark_dashboard.json"
echo "  · 日志: $CONFIG_DIR/capture.log, score_engine.log"
echo ""
echo "📖 使用指南:"
echo "  1. 运行测试: python3 $BENCHMARK_DIR/capture_output.py"
echo "  2. 查看报告: python3 $BENCHMARK_DIR/score_engine.py report"
echo "  3. 生成Markdown: python3 $BENCHMARK_DIR/score_engine.py markdown"
echo ""
echo "DNA: #龍芯⚡️$(date +%Y%m%d)-BENCHMARK-COMPLETE"
echo "🐉 龍魂系统·数字主权守护"
echo ""
