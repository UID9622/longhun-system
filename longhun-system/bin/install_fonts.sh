#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────
# install_fonts.sh · Mac全套字体一键安装
# DNA: #龍芯⚡️2026-04-07-FONT-INSTALL-v1.0
# 作者: 诸葛鑫（UID9622）
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导: 曾仕强老师（永恒显示）
# 用途: 通心译完美显示·CNSH字元支持·世界无误解之根
# ─────────────────────────────────────────────────────────

set -e
FONT_DIR="$HOME/Library/Fonts"
mkdir -p "$FONT_DIR"

echo ""
echo "🐉 龍魂字体安装引擎 v1.0"
echo "DNA: #龍芯⚡️2026-04-07-FONT-INSTALL-v1.0"
echo "============================================"

# ── 检查Homebrew ──
if ! command -v brew &>/dev/null; then
  echo "⚠️  Homebrew未安装，先跑这个："
  echo '  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
  exit 1
fi

echo ""
echo "✅ Homebrew 已检测"
echo ""

# ── 添加字体tap ──
echo "📦 添加 homebrew/cask-fonts..."
brew tap homebrew/cask-fonts 2>/dev/null || true

# ════════════════════════════════════
# 第一层：CJK核心字体（通心译必备）
# ════════════════════════════════════
echo ""
echo "═══ 第一层：CJK核心·通心译必备 ═══"

CORE_FONTS=(
  "font-noto-sans-cjk"          # Google Noto 无衬线·6万+汉字·最全
  "font-noto-serif-cjk"         # Google Noto 衬线版
  "font-source-han-sans"        # Adobe 思源黑体·专业级
  "font-source-han-serif"       # Adobe 思源宋体
)

for f in "${CORE_FONTS[@]}"; do
  echo -n "  安装 $f ... "
  brew install --cask "$f" 2>/dev/null && echo "✅" || echo "⚠️ 跳过(可能已装)"
done

# ════════════════════════════════════
# 第二层：中文美学字体（通心译风格）
# ════════════════════════════════════
echo ""
echo "═══ 第二层：中文美学·CNSH风格 ═══"

STYLE_FONTS=(
  "font-lxgw-wenkai"            # 霞鹜文楷·手写风·最美中文
  "font-lxgw-wenkai-mono"       # 霞鹜文楷等宽版
  "font-ma-shan-zheng"          # 马善政楷体
  "font-zhi-mang-xing"          # 智芒星·书法感
)

for f in "${STYLE_FONTS[@]}"; do
  echo -n "  安装 $f ... "
  brew install --cask "$f" 2>/dev/null && echo "✅" || echo "⚠️ 跳过"
done

# ════════════════════════════════════
# 第三层：代码字体（CNSH编辑器）
# ════════════════════════════════════
echo ""
echo "═══ 第三层：代码字体·CNSH终端 ═══"

CODE_FONTS=(
  "font-jetbrains-mono"         # JetBrains·程序员最爱
  "font-fira-code"              # Fira Code·连字符
  "font-cascadia-code"          # 微软 Cascadia·现代感
  "font-monaspace"              # GitHub Monaspace·质感
  "font-sarasa-gothic"          # 更纱黑体·中英混排完美
)

for f in "${CODE_FONTS[@]}"; do
  echo -n "  安装 $f ... "
  brew install --cask "$f" 2>/dev/null && echo "✅" || echo "⚠️ 跳过"
done

# ════════════════════════════════════
# 第四层：覆盖Unicode私有区（CNSH字元）
# ════════════════════════════════════
echo ""
echo "═══ 第四层：Unicode全覆盖·兜底 ═══"

UNICODE_FONTS=(
  "font-noto-sans"              # Noto Sans·Latin/符号全集
  "font-unifont"                # GNU Unifont·Unicode全覆盖·兜底神器
)

for f in "${UNICODE_FONTS[@]}"; do
  echo -n "  安装 $f ... "
  brew install --cask "$f" 2>/dev/null && echo "✅" || echo "⚠️ 跳过"
done

# ════════════════════════════════════
# 第五层：CNSH自制字体（如果已生成）
# ════════════════════════════════════
echo ""
echo "═══ 第五层：CNSH龍魂自制字体 ═══"

CNSH_FONT_DIR="$HOME/longhun-system/CNSH引擎/CNSH_字体输出"
if [ -d "$CNSH_FONT_DIR" ]; then
  TTF_COUNT=$(find "$CNSH_FONT_DIR" -name "*.ttf" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$TTF_COUNT" -gt 0 ]; then
    echo "  发现 $TTF_COUNT 个自制TTF，安装中..."
    find "$CNSH_FONT_DIR" -name "*.ttf" -exec cp {} "$FONT_DIR/" \;
    echo "  ✅ CNSH龍魂字体已安装到系统"
  else
    echo "  ⏳ 自制TTF未生成，跑 cnsh_font_builder_v2_LU.py 后再装"
  fi
else
  echo "  ⏳ 字体输出目录不存在，先跑字体构建器"
fi

# ── 刷新字体缓存 ──
echo ""
echo "🔄 刷新字体缓存..."
atsutil databases -remove 2>/dev/null || true
echo "✅ 完成（可能需要重启应用生效）"

# ── 汇总 ──
echo ""
echo "════════════════════════════════════"
echo "🟢 安装完成 · 通心译字体全套就位"
echo ""
echo "字体位置: ~/Library/Fonts/"
TOTAL=$(ls "$FONT_DIR" | wc -l | tr -d ' ')
echo "当前字体总数: $TOTAL 个文件"
echo ""
echo "优先级叠加顺序:"
echo "  1. CNSH龍魂自制（私有区E001-EFFF）"
echo "  2. 霞鹜文楷（中文美学首选）"
echo "  3. 更纱黑体（中英混排）"
echo "  4. Noto CJK（6万字兜底）"
echo "  5. GNU Unifont（Unicode终极兜底）"
echo ""
echo "DNA: #龍芯⚡️2026-04-07-FONT-INSTALL-v1.0"
echo "🐉 世界无误解之根·字体就位"
