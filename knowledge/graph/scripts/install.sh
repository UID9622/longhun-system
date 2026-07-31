#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# 龍魂知识图谱安装脚本
# DNA: #龍芯⚡️2026-06-27-LHKG-INSTALL-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════════════

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_DIR="${HOME}/.龍魂/knowledge-graph"
BIN_DIR="${HOME}/bin"
FORCE=0

usage() {
    echo "安装龍魂知识图谱"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --system    安装到 /usr/local/bin (需要 sudo)"
    echo "  --force     强制覆盖现有安装"
    echo "  --help      显示帮助"
    exit 0
}

color() { echo -e "\033[${1}m${2}\033[0m"; }

while [ $# -gt 0 ]; do
    case "$1" in
        --system) BIN_DIR="/usr/local/bin" ;;
        --force) FORCE=1 ;;
        --help) usage ;;
        *) echo "未知选项: $1"; usage ;;
    esac
    shift
done

# 检查Python
color "94" "🔍 检查 Python..."
if ! command -v python3 &> /dev/null; then
    color "91" "❌ 未找到 python3，请先安装 Python 3.8+"
    exit 1
fi
PYVER=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
color "92" "✅ Python ${PYVER}"

# 创建安装目录
color "94" "📁 创建安装目录..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${INSTALL_DIR}/nodes"
mkdir -p "${INSTALL_DIR}/edges"
mkdir -p "${INSTALL_DIR}/states"
mkdir -p "${INSTALL_DIR}/queries"
mkdir -p "${INSTALL_DIR}/visual"

# 复制文件
color "94" "📦 复制文件..."
cp "${REPO_DIR}/nodes/all_nodes.json" "${INSTALL_DIR}/nodes/"
cp "${REPO_DIR}/nodes/schema.json" "${INSTALL_DIR}/nodes/" 2>/dev/null || true
cp "${REPO_DIR}/edges/all_edges.json" "${INSTALL_DIR}/edges/"
cp "${REPO_DIR}/edges/schema.json" "${INSTALL_DIR}/edges/" 2>/dev/null || true
cp "${REPO_DIR}/states/state_machine.json" "${INSTALL_DIR}/states/"
cp "${REPO_DIR}/states/penetration_rules.json" "${INSTALL_DIR}/states/"
cp "${REPO_DIR}/queries/longhun_kg.py" "${INSTALL_DIR}/queries/"
cp "${REPO_DIR}/visual/"*.mermaid "${INSTALL_DIR}/visual/" 2>/dev/null || true

# 创建空的state_history.json
echo '{}' > "${INSTALL_DIR}/states/state_history.json"

# 安装kg命令
color "94" "🔧 安装 kg 命令..."
mkdir -p "${BIN_DIR}"
cp "${REPO_DIR}/scripts/kg" "${BIN_DIR}/kg"
chmod +x "${BIN_DIR}/kg"

# 验证
color "94" "✅ 验证安装..."
if [ -f "${INSTALL_DIR}/nodes/all_nodes.json" ]; then
    NODE_COUNT=$(python3 -c "import json; d=json.load(open('${INSTALL_DIR}/nodes/all_nodes.json')); print(len(d.get('nodes', d)))")
    color "92" "✅ 节点: ${NODE_COUNT}"
fi
if [ -f "${INSTALL_DIR}/edges/all_edges.json" ]; then
    EDGE_COUNT=$(python3 -c "import json; d=json.load(open('${INSTALL_DIR}/edges/all_edges.json')); print(len(d.get('edges', d)))")
    color "92" "✅ 边: ${EDGE_COUNT}"
fi

color "92" ""
color "92" "🎉 龍魂知识图谱安装完成！"
color "96" "   数据目录: ${INSTALL_DIR}"
color "96" "   命令: kg list | kg show | kg path | kg state | kg export"
color "96" ""
color "93" "   提示: 确保 ${BIN_DIR} 在 PATH 中"

if [ "${BIN_DIR}" = "${HOME}/bin" ] && [[ ":$PATH:" != *":${HOME}/bin:"* ]]; then
    color "93" "   执行以下命令添加 PATH:"
    color "93" '   export PATH="${HOME}/bin:${PATH}"'
    color "93" '   echo '"'"'export PATH="${HOME}/bin:${PATH}"'"'" >> ~/.bashrc'
fi
