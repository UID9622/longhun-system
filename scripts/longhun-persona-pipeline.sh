#!/bin/bash
# ============================================================================
# longhun-persona-pipeline.sh — 四步一键执行：挖掘 → 训练 → 可视化 → 模型训练
# DNA: #龍芯⚡️丙午·辛未·PERSONA-PIPELINE-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# 用法:
#   ./scripts/longhun-persona-pipeline.sh               # 完整四步
#   ./scripts/longhun-persona-pipeline.sh --no-model    # 前三步（不触发模型训练）
#   ./scripts/longhun-persona-pipeline.sh --mine        # 仅挖掘
#   ./scripts/longhun-persona-pipeline.sh --train       # 仅训练
#   ./scripts/longhun-persona-pipeline.sh --view        # 仅可视化
#   ./scripts/longhun-persona-pipeline.sh --bridge      # 仅桥接+模型训练
#   ./scripts/longhun-persona-pipeline.sh --open        # 完整四步 + 打开浏览器
#   ./scripts/longhun-persona-pipeline.sh --serve       # 完整四步 + 启动HTTP服务
# ============================================================================

set -e

LONGHUN_ROOT="${HOME}/longhun-system"
cd "$LONGHUN_ROOT"

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

banner() {
    echo ""
    echo -e "${BOLD}🐉 龍魂人格IP固化流水线 v2.0${NC}"
    echo "═══════════════════════════════════════════════════════"
    echo -e "  DNA: ${CYAN}UID9622-ONLY-ONCE🧬LK9X-772Z${NC}"
    echo "═══════════════════════════════════════════════════════"
    echo ""
}

step_header() {
    echo ""
    echo -e "${CYAN}【步骤 $1/$2】$3${NC}"
    echo "───────────────────────────────────────────────────────"
}

done_banner() {
    echo ""
    echo "═══════════════════════════════════════════════════════"
    echo -e "${GREEN}✅ 人格IP固化完成${NC}"
    echo ""
    echo "  输出文件:"
    echo "    挖掘数据: ~/longhun-system/.data-miner/"
    echo "    人格链:   ~/longhun-system/persona-chain/"
    echo "    可视化:   ~/longhun-system/persona-visual/persona-report.html"
    echo "    训练数据: ~/longhun-system/models/persona_training_data.jsonl"
    echo ""
    echo -e "  查看报告: ${CYAN}open ~/longhun-system/persona-visual/persona-report.html${NC}"
    echo -e "  本地服务: ${CYAN}python3 scripts/longhun-persona-visualizer.py --serve${NC}"
    echo "═══════════════════════════════════════════════════════"
}

# 解析模式
MODE="full"
OPEN_REPORT=false
SERVE_REPORT=false
SKIP_MODEL=false

for arg in "$@"; do
    case "$arg" in
        --mine)       MODE="mine" ;;
        --train)      MODE="train" ;;
        --view)       MODE="view" ;;
        --bridge)     MODE="bridge" ;;
        --no-model)   SKIP_MODEL=true ;;
        --open)       OPEN_REPORT=true ;;
        --serve)      SERVE_REPORT=true ;;
        --help|-h)
            echo "用法: ./scripts/longhun-persona-pipeline.sh [选项]"
            echo ""
            echo "选项:"
            echo "  (无参数)  完整四步：挖掘 → 训练 → 可视化 → 桥接模型训练"
            echo "  --mine    仅数据挖掘"
            echo "  --train   仅人格链训练"
            echo "  --view    仅可视化还原"
            echo "  --bridge  仅桥接+模型训练"
            echo "  --no-model 跳过模型训练（仅前三步）"
            echo "  --open    完整流程 + 自动打开浏览器"
            echo "  --serve   完整流程 + 启动HTTP服务"
            exit 0
            ;;
    esac
done

TOTAL_STEPS=4
if $SKIP_MODEL; then TOTAL_STEPS=3; fi

banner
CURRENT=0

# ═══════════════════════════════════════════════════════
# 步骤1: 数据挖掘
# ═══════════════════════════════════════════════════════
if [[ "$MODE" == "full" || "$MODE" == "mine" ]]; then
    CURRENT=$((CURRENT + 1))
    step_header "$CURRENT" "$TOTAL_STEPS" "数据挖掘"
    bash "${LONGHUN_ROOT}/scripts/longhun-data-miner.sh"
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}❌ 挖掘失败${NC}"
        exit 1
    fi
fi

# ═══════════════════════════════════════════════════════
# 步骤2: 人格链训练
# ═══════════════════════════════════════════════════════
if [[ "$MODE" == "full" || "$MODE" == "train" ]]; then
    CURRENT=$((CURRENT + 1))
    step_header "$CURRENT" "$TOTAL_STEPS" "人格链训练"
    python3 "${LONGHUN_ROOT}/scripts/longhun-persona-trainer.py"
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}❌ 训练失败${NC}"
        exit 1
    fi
fi

# ═══════════════════════════════════════════════════════
# 步骤3: 可视化还原
# ═══════════════════════════════════════════════════════
if [[ "$MODE" == "full" || "$MODE" == "view" ]]; then
    CURRENT=$((CURRENT + 1))
    step_header "$CURRENT" "$TOTAL_STEPS" "可视化还原"
    python3 "${LONGHUN_ROOT}/scripts/longhun-persona-visualizer.py"
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}❌ 可视化失败${NC}"
        exit 1
    fi
fi

# ═══════════════════════════════════════════════════════
# 步骤4: 桥接 → 模型训练
# ═══════════════════════════════════════════════════════
if [[ "$MODE" == "full" || "$MODE" == "bridge" ]]; then
    if ! $SKIP_MODEL; then
        CURRENT=$((CURRENT + 1))
        step_header "$CURRENT" "$TOTAL_STEPS" "桥接 → 模型训练"
        python3 "${LONGHUN_ROOT}/scripts/longhun-persona-to-model-bridge.py" --export-only
        if [[ $? -ne 0 ]]; then
            echo -e "${YELLOW:-}⚠️  桥接导出完成，训练需手动触发${NC}"
        else
            echo -e "${GREEN}✅ 训练数据已导出到 models/persona_training_data.jsonl${NC}"
            echo -e "  手动训练: ${CYAN}python3 scripts/longhun-persona-to-model-bridge.py --train${NC}"
        fi
    fi
fi

done_banner

# 自动打开浏览器
if $OPEN_REPORT; then
    open "${HOME}/longhun-system/persona-visual/persona-report.html"
fi

# 启动HTTP服务
if $SERVE_REPORT; then
    echo ""
    python3 "${LONGHUN_ROOT}/scripts/longhun-persona-visualizer.py" --serve &
    sleep 1
    open "http://localhost:8765"
    echo "按 Ctrl+C 停止服务"
    wait
fi
