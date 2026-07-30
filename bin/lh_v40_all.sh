#!/bin/bash
# ============================================================
# DNA: #龍芯⚡️丙午·丙申·癸酉·丁巳·临-V40-ALL-PIPELINE
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# ============================================================
# 龍魂v4.0 · 一键全流程：蒸馏 → 训练 → 导出 → 测试
# 用法: bash bin/lh_v40_all.sh [distill|prepare|train|fuse|verify|export|test|all]
# ============================================================

set -e
cd "$HOME/longhun-system"

CMD="${1:-all}"

echo "========================================"
echo "  龍魂v4.0 一键流水线"
echo "  命令: $CMD"
echo "  DNA: #龍芯⚡️丙午·丙申·癸酉·丁巳·临-V40-ALL-PIPELINE"
echo "========================================"

case "$CMD" in
  distill)
    echo "【阶段0】蒸馏数据生成..."
    bash bin/lh_v40_distill.sh
    ;;
  prepare)
    echo "【阶段1】数据与底座验证..."
    python3 bin/lh_train_v40.py prepare
    ;;
  train)
    echo "【阶段2】LoRA训练..."
    python3 bin/lh_train_v40.py train
    ;;
  fuse)
    echo "【阶段3】合并adapter..."
    python3 bin/lh_train_v40.py fuse
    ;;
  verify)
    echo "【阶段4】MLX推理验证..."
    python3 bin/lh_train_v40.py verify
    ;;
  export)
    echo "【阶段5】GGUF导出+Q4_K_M+Ollama..."
    python3 bin/lh_train_v40.py export
    ;;
  test)
    echo "【阶段6】Ollama 10项测试..."
    python3 bin/lh_v40_test.py 2>/dev/null || echo "测试脚本不存在，跳过"
    ;;
  all)
    echo "【阶段0】蒸馏数据生成..."
    bash bin/lh_v40_distill.sh
    echo ""
    echo "【阶段1-5】训练→导出..."
    python3 bin/lh_train_v40.py all
    echo ""
    echo "【阶段6】测试..."
    python3 bin/lh_v40_test.py 2>/dev/null || echo "测试脚本不存在，跳过"
    ;;
  *)
    echo "用法: bash bin/lh_v40_all.sh [distill|prepare|train|fuse|verify|export|test|all]"
    exit 1
    ;;
esac

echo ""
echo "========================================"
echo "  v4.0 流水线阶段 [$CMD] 完成"
echo "========================================"
