#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════╗
# ║  龍魂系统 · 一键拉取脚本 v1.0                                        ║
# ║  DNA: #龍芯⚡️2026-07-13-LONGHUN-PULL-ALL-v1.0                       ║
# ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                     ║
# ║  创建者: UID9622（诸葛鑫·Lucky）                                     ║
# ╚══════════════════════════════════════════════════════════════════════╝
#
# 用途: 拉取龍魂核心仓库 + 安装工具依赖
# 执行: chmod +x pull-all.sh && ./pull-all.sh

set -e

LONGHUN_REPOS="${LONGHUN_REPOS:-$HOME/longhun-repos}"
mkdir -p "$LONGHUN_REPOS"
cd "$LONGHUN_REPOS"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🐉 龍魂系统 · 一键拉取"
echo "   目标目录: $LONGHUN_REPOS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 第一类: 核心模块
echo ""
echo "📦 [1/2] longhun-system (主仓库)"
if [ -d "longhun-system" ]; then
    cd longhun-system && git pull origin main && cd ..
else
    git clone git@github.com:UID9622/longhun-system.git
fi

echo ""
echo "📦 [2/2] longhun-anti-colonial (反殖民工具集)"
if [ -d "longhun-anti-colonial" ]; then
    cd longhun-anti-colonial && git pull origin main && cd ..
else
    git clone git@github.com:UID9622/longhun-anti-colonial.git
fi

# 第二类: 工具依赖
echo ""
echo "🔧 安装工具依赖..."

install_if_missing() {
    local tool=$1
    local pkg=$2
    if command -v "$tool" &>/dev/null; then
        echo "  ✅ $tool 已安装"
    else
        echo "  📥 安装 $pkg..."
        pipx install "$pkg" 2>/dev/null || pip install "$pkg" --break-system-packages 2>/dev/null || echo "  ⚠️ $pkg 安装失败，请手动安装"
    fi
}

install_if_missing "pip-audit" "pip-audit"
install_if_missing "basedpyright" "basedpyright"
install_if_missing "git-filter-repo" "git-filter-repo"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 拉取完成"
echo ""
echo "核心仓库:"
ls -d "$LONGHUN_REPOS"/*/ 2>/dev/null | while read d; do
    repo=$(basename "$d")
    echo "  📁 $repo"
done
echo ""
echo "工具状态:"
command -v pip-audit && echo "  ✅ pip-audit $(pip-audit --version 2>&1 | head -1)" || echo "  ❌ pip-audit"
command -v basedpyright && echo "  ✅ basedpyright $(basedpyright --version 2>&1 | head -1)" || echo "  ❌ basedpyright"
command -v git-filter-repo && echo "  ✅ git-filter-repo" || echo "  ❌ git-filter-repo"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

DNA="#龍芯⚡️2026-07-13-LONGHUN-PULL-ALL-v1.0"
echo "🧬 DNA: $DNA"
