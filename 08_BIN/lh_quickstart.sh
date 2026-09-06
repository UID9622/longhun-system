#!/usr/bin/env bash
# 🐉 lh_quickstart.sh — 龍魂引擎一键巡检（开工 30 秒知道所有引擎还活着）
# DNA: #龍芯⚡️丙午·丁酉·癸未·LH-QUICKSTART-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# 用法: bash 08_BIN/lh_quickstart.sh
# 全过返回 0 · 任意失败返回 1 并报出哪个挂了
# 探活原则（老大棒令）: 引擎没有 selfcheck 就用 --help/裸跑，能执行不崩溃=活着；不为巡检造假。

# 自动 cd 到仓库根（脚本在 08_BIN/ 下）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.." || exit 1

PASS=0
FAIL=0

chk() {
    local name="$1"; shift
    if "$@" &>/dev/null; then
        echo "  🟢 $name"
        ((PASS++))
    else
        echo "  🔴 $name 挂了"
        ((FAIL++))
    fi
}

echo "=== 龍魂引擎巡检 $(date '+%Y-%m-%d %H:%M') ==="

echo "— L2 自研引擎 —"
# 台账引擎（summary=真读台账，exit0 即活）
chk "台账引擎"       python3 08_BIN/lh_asi_ledger.py summary
# 量化引擎（summary=GGUF/AWQ 探测汇总）
chk "量化引擎"       python3 08_BIN/lh_quant_engine.py summary
# 白盒探针（summary 子命令·无参 exit0 亦活）
chk "白盒探针"       python3 08_BIN/lh_whitebox_probe.py summary
# 白盒前向（argparse --help 即活；--selfcheck 会挂载模型勿用）
chk "白盒前向"       python3 08_BIN/lh_mlx_forward_probe.py --help
# tokenizer builder（test 轨对 AWQ 词表单测·真信号）
chk "tokenizer"     python3 08_BIN/lh_tokenizer_builder.py test --file models/qwen2.5-0.5b-instruct-awq/tokenizer.json
# 行为密码学（裸跑=自测演示）
chk "行为密码学"     python3 12_DOCS/knowledge-matrix-src/04_三色审计与决策/behavioral_crypto.py
# 幻觉检测（裸跑=验收基线复现·0.06s）
chk "幻觉检测"       python3 08_BIN/lh_hallucination_metrics.py
# 蚁群引擎（import 心跳·engine 包别名桥接已持久化）
chk "蚁群引擎"       env PYTHONPATH=05_ENGINES python3 -c "import engine.ant_colony.antenna_bus, engine.ant_colony.antenna_signal"

echo "— L4 基础设施 —"
# lh CLI / 五检健康看板
chk "lh hboard"     lh hboard
# memory-sync 健康端点（鲲鹏 443）
chk "memory-sync"   curl -sfk --max-time 8 https://119.13.90.27/sync/health

echo ""
echo "=== 结果：🟢$PASS 通过  🔴$FAIL 失败 ==="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
