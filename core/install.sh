#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 🐉 龍魂低算力内核 · 一键安装脚本
# longhun-core v1.0.0
# DNA: #龍芯⚡️丙午·丙申·丁巳·恒卦-INSTALL-UID9622
# License: MulanPSL v2

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="${HOME}/.longhun-core"
VENV_DIR="${INSTALL_DIR}/venv"
BIN_DIR="${HOME}/.local/bin"
PYTHON_CMD=""

echo ""
echo -e "${BOLD}══════════════════════════════════════════════════${NC}"
echo -e "${BOLD}🐉 龍魂低算力内核 · longhun-core v1.0.0${NC}"
echo -e "${BOLD}══════════════════════════════════════════════════${NC}"
echo -e "治大国若烹小鲜。——《道德经》第60章"
echo ""

# === 检测 Python ===
for cmd in python3 python; do
    if command -v $cmd &>/dev/null; then
        ver=$($cmd --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        major=$(echo "$ver" | cut -d. -f1)
        minor=$(echo "$ver" | cut -d. -f2)
        if [ "$major" -ge 3 ] && [ "$minor" -ge 8 ]; then
            PYTHON_CMD=$cmd
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${RED}❌ 需要 Python 3.8+，未找到或版本过低${NC}"
    exit 1
fi

echo -e "✅ Python: $($PYTHON_CMD --version)"

# === 无需 pip install（纯标准库），直接复制文件 ===
echo ""
echo "📦 安装内核模块..."

mkdir -p "${INSTALL_DIR}"
mkdir -p "${BIN_DIR}"

# 复制 longhun_core 包
rm -rf "${INSTALL_DIR}/longhun_core"
cp -r "${SCRIPT_DIR}/longhun_core" "${INSTALL_DIR}/"

# 复制 CLI
cp "${SCRIPT_DIR}/lh.py" "${INSTALL_DIR}/lh"

# 复制工具
mkdir -p "${INSTALL_DIR}/tools"
for f in "${SCRIPT_DIR}/tools/"*; do
    if [ -f "$f" ]; then
        cp "$f" "${INSTALL_DIR}/tools/"
    fi
done

# 复制文档
mkdir -p "${INSTALL_DIR}/docs"
for f in "${SCRIPT_DIR}/docs/"*; do
    if [ -f "$f" ]; then
        cp "$f" "${INSTALL_DIR}/docs/"
    fi
done

# 复制 web
mkdir -p "${INSTALL_DIR}/web"
for f in "${SCRIPT_DIR}/web/"*; do
    if [ -f "$f" ]; then
        cp "$f" "${INSTALL_DIR}/web/"
    fi
done

# 创建 lh-core 可执行入口（与完整版 lh 区分）
cat > "${BIN_DIR}/lh-core" << 'LHENTRY'
#!/bin/bash
exec python3 "${HOME}/.longhun-core/lh" "$@"
LHENTRY
chmod +x "${BIN_DIR}/lh-core"

echo -e "✅ 内核模块安装到: ${INSTALL_DIR}"
echo -e "✅ CLI 安装到:     ${BIN_DIR}/lh-core"

# === 检查 PATH ===
if ! echo "$PATH" | grep -q "${BIN_DIR}"; then
    echo ""
    echo -e "${YELLOW}⚠️  ${BIN_DIR} 不在 PATH 中${NC}"
    echo ""
    echo "请将以下行添加到你的 shell 配置文件中:"
    echo ""
    echo -e "  ${BOLD}export PATH=\"${BIN_DIR}:\$PATH\"${NC}"
    echo ""
    echo "或者运行:"
    echo ""
    echo -e "  ${BOLD}export PATH=\"${BIN_DIR}:\$PATH\"${NC}"
    echo ""
    # 尝试自动添加到常用配置
    for rc in "${HOME}/.zshrc" "${HOME}/.bashrc" "${HOME}/.bash_profile"; do
        if [ -f "$rc" ]; then
            if ! grep -q "${BIN_DIR}" "$rc" 2>/dev/null; then
                echo "export PATH=\"${BIN_DIR}:\$PATH\"" >> "$rc"
                echo -e "✅ 已自动添加到 $rc"
            fi
        fi
    done
else
    echo -e "✅ ${BIN_DIR} 已在 PATH 中"
fi

# === 自测 ===
echo ""
echo -e "${BOLD}══════════════════════════════════════════════════${NC}"
echo -e "${BOLD}🔬 运行自检...${NC}"
echo -e "${BOLD}══════════════════════════════════════════════════${NC}"
echo ""

PASS=0
FAIL=0

# 测试1: CLI 可用
if "${BIN_DIR}/lh-core" version > /dev/null 2>&1; then
    echo -e "  ${GREEN}✅${NC} CLI 启动正常"
    PASS=$((PASS + 1))
else
    echo -e "  ${RED}❌${NC} CLI 启动失败"
    FAIL=$((FAIL + 1))
fi

# 测试2: DNA 签发
DNA_OUT=$("${BIN_DIR}/lh-core" dna "自测" 2>&1)
if echo "$DNA_OUT" | grep -q "#龍芯"; then
    echo -e "  ${GREEN}✅${NC} DNA 签发正常"
    PASS=$((PASS + 1))
else
    echo -e "  ${RED}❌${NC} DNA 签发失败"
    FAIL=$((FAIL + 1))
fi

# 测试3: 三色审计
AUDIT_OUT=$("${BIN_DIR}/lh-core" audit --json '{"阻塞率":0.02}' 2>&1)
if echo "$AUDIT_OUT" | grep -q "🟢"; then
    echo -e "  ${GREEN}✅${NC} 三色审计正常"
    PASS=$((PASS + 1))
else
    echo -e "  ${RED}❌${NC} 三色审计失败"
    FAIL=$((FAIL + 1))
fi

# 测试4: 数字根
ROOT_OUT=$("${BIN_DIR}/lh-core" root 369 2>&1)
if echo "$ROOT_OUT" | grep -q "9"; then
    echo -e "  ${GREEN}✅${NC} 数字根正常"
    PASS=$((PASS + 1))
else
    echo -e "  ${RED}❌${NC} 数字根失败"
    FAIL=$((FAIL + 1))
fi

# 测试5: 年轮链
CHAIN_OUT=$("${BIN_DIR}/lh-core" chain write '{"test":true}' 2>&1)
if echo "$CHAIN_OUT" | grep -q "写入"; then
    echo -e "  ${GREEN}✅${NC} 年轮链正常"
    PASS=$((PASS + 1))
else
    echo -e "  ${RED}❌${NC} 年轮链失败"
    FAIL=$((FAIL + 1))
fi

echo ""

# === 结果 ===
echo -e "${BOLD}══════════════════════════════════════════════════${NC}"
if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}${BOLD}🎉 安装成功！${NC} ${PASS}/${PASS} 自检通过"
    echo ""
    echo -e "现在试试:"
    echo -e "  ${BOLD}lh-core version${NC}      — 查看版本"
    echo -e "  ${BOLD}lh-core bench${NC}        — 跑基准测试"
    echo -e "  ${BOLD}lh-core dna 你好世界${NC}  — 签发DNA"
    echo -e "  ${BOLD}lh-core info${NC}         — 系统信息"
else
    echo -e "${RED}❌ 安装检测到 ${FAIL} 个失败项${NC}"
    echo -e "请检查 Python 环境是否满足要求 (>=3.8)"
fi
echo -e "${BOLD}══════════════════════════════════════════════════${NC}"
echo ""
echo -e "🐉 #龍芯⚡️丙午·丙申·丁巳·恒卦-LOW-POWER-BENCH-UID9622"
echo ""
