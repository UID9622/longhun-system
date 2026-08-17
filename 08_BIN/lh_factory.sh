#!/bin/bash
# 🐉 龍魂 · 全自动工厂总控 v2.1
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-FACTORY-CTRL-UID9622
# 创建者: 诸葛鑫（UID9622）
# 用法: lh factory [命令]

LH_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FACTORY_PY="$LH_ROOT/08_BIN/lh_auto_factory.py"

echo "🏭 龍魂 · 全自动工厂 v2.1"
echo "========================================"

case "${1:-help}" in
    run)
        echo "🔧 运行工厂流程..."
        python3 "$FACTORY_PY" --run "${2:-.}" ${3:+--version "$3"}
        ;;
    status)
        python3 "$FACTORY_PY" --status
        ;;
    artifacts)
        python3 "$FACTORY_PY" --artifacts
        ;;
    learn)
        python3 "$FACTORY_PY" --learn
        ;;
    monitor)
        echo "📊 实时监控..."
        python3 "$FACTORY_PY" --monitor
        ;;
    gate)
        echo "🚧 质量门禁规则..."
        python3 "$FACTORY_PY" --gate
        ;;
    release)
        echo "🚀 发布策略: ${2:-canary}"
        python3 "$LH_ROOT/08_BIN/lh_release_strategy.py" --run "${2:-canary}"
        ;;
    rollback)
        echo "⏪ 回滚到版本: ${2}"
        python3 "$LH_ROOT/08_BIN/lh_rollback.py" --version "${2}"
        ;;
    versions)
        echo "📚 可回滚版本..."
        python3 "$LH_ROOT/08_BIN/lh_rollback.py" --list
        ;;
    circuit)
        echo "🧯 熔断器状态..."
        python3 "$FACTORY_PY" --circuit
        ;;
    kunpeng)
        echo "🦅 鲲鹏健康检查..."
        python3 "$FACTORY_PY" --kunpeng-health
        ;;
    *)
        cat << EOF
🐉 龍魂 · 全自动工厂 v2.1

用法:
  lh factory run [PATH] [VERSION]    # 运行完整工厂流程
  lh factory status                  # 查看工厂状态
  lh factory artifacts               # 查看构建产物
  lh factory learn                   # 学习反馈模式
  lh factory monitor                 # 工厂自监控
  lh factory gate                    # 质量门禁规则
  lh factory release [STRATEGY]      # 发布 (canary|gray|full)
  lh factory rollback [VERSION]      # 回滚到指定版本
  lh factory versions                # 列出可回滚版本
  lh factory circuit                 # 熔断器状态
  lh factory kunpeng                 # 鲲鹏健康检查
EOF
        ;;
esac
