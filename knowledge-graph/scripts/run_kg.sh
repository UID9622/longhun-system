#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 龙魂知识图谱 · 本地 Kimi 执行指令
# DNA: #龍芯⚡️2026-06-27-LHKG-RUN-v1.0
# ═══════════════════════════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KG_DIR="${HOME}/.龍魂/knowledge-graph"
PYTHON="${LHKG_PYTHON:-python3}"

color() { echo -e "\033[${1}m${2}\033[0m"; }

# ── 安装 ──────────────────────────────────────────
cmd_install() {
    color "94" "📦 安装龙魂知识图谱到 ~/.龍魂/knowledge-graph/"
    
    mkdir -p "${KG_DIR}"
    
    # 复制数据
    cp -r "${SCRIPT_DIR}/../nodes" "${KG_DIR}/"
    cp -r "${SCRIPT_DIR}/../edges" "${KG_DIR}/"
    cp -r "${SCRIPT_DIR}/../states" "${KG_DIR}/"
    cp -r "${SCRIPT_DIR}/../queries" "${KG_DIR}/"
    cp -r "${SCRIPT_DIR}/../visual" "${KG_DIR}/"
    
    # 创建state_history.json（空）
    echo '{}' > "${KG_DIR}/states/state_history.json"
    
    # 安装kg命令
    if [ -d "${HOME}/bin" ]; then
        cp "${SCRIPT_DIR}/kg" "${HOME}/bin/kg"
        chmod +x "${HOME}/bin/kg"
        export PATH="${HOME}/bin:${PATH}"
    fi
    
    color "92" "✅ 安装完成！"
    color "96" "   数据目录: ${KG_DIR}"
    color "96" "   命令: kg list | kg show | kg path | kg state | kg export"
}

# ── 验证 ──────────────────────────────────────────
cmd_verify() {
    color "94" "🔍 验证知识图谱完整性..."
    
    local errors=0
    
    [ -f "${KG_DIR}/nodes/all_nodes.json" ] || { color "91" "❌ nodes/all_nodes.json 缺失"; errors=$((errors+1)); }
    [ -f "${KG_DIR}/edges/all_edges.json" ] || { color "91" "❌ edges/all_edges.json 缺失"; errors=$((errors+1)); }
    [ -f "${KG_DIR}/states/state_machine.json" ] || { color "91" "❌ states/state_machine.json 缺失"; errors=$((errors+1)); }
    [ -f "${KG_DIR}/queries/longhun_kg.py" ] || { color "91" "❌ queries/longhun_kg.py 缺失"; errors=$((errors+1)); }
    
    if [ $errors -eq 0 ]; then
        color "92" "✅ 所有文件完整！"
        
        # 运行Python验证
        ${PYTHON} -c "
import sys
sys.path.insert(0, '${KG_DIR}/queries')
from longhun_kg import LongHunGraph

g = LongHunGraph('${KG_DIR}')
print(f'📊 节点: {len(g.nodes)} | 边: {len(g.edges)}')

# 类型分布
types = {}
for n in g.nodes.values():
    t = n.get('type', 'unknown')
    types[t] = types.get(t, 0) + 1
print('📋 类型分布:')
for t, c in sorted(types.items(), key=lambda x: -x[1]):
    print(f'   {t}: {c}')

# 层级分布
layers = {}
for n in g.nodes.values():
    l = n.get('layer', 'unknown')
    layers[l] = layers.get(l, 0) + 1
print('📊 层级分布:')
for l, c in sorted(layers.items(), key=lambda x: -x[1]):
    print(f'   {l}: {c}')

print('✅ 验证通过！')
" || { color "91" "❌ Python验证失败"; exit 1; }
    else
        color "91" "❌ ${errors}个文件缺失，请重新安装"
        exit 1
    fi
}

# ── 运行 ──────────────────────────────────────────
cmd_run() {
    local cmd="$1"
    shift
    
    ${PYTHON} "${KG_DIR}/queries/longhun_kg.py" "${cmd}" --data-dir "${KG_DIR}" "$@"
}

# ── 主入口 ────────────────────────────────────────
case "${1:-}" in
    install)
        cmd_install
        ;;
    verify)
        cmd_verify
        ;;
    run)
        shift
        cmd_run "$@"
        ;;
    *)
        echo "龙魂知识图谱 · 本地执行器"
        echo ""
        echo "用法: $0 <命令>"
        echo ""
        echo "命令:"
        echo "  install    安装知识图谱到 ~/.龍魂/knowledge-graph/"
        echo "  verify     验证安装完整性"
        echo "  run <cmd>  运行kg命令 (list/show/path/state/export)"
        echo ""
        echo "环境变量:"
        echo "  LHKG_DIR     数据目录 (默认: ~/.龍魂/knowledge-graph)"
        echo "  LHKG_PYTHON  Python路径 (默认: python3)"
        ;;
esac
