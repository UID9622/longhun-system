#!/bin/bash
# ╔══════════════════════════════════════════════════════════╗
# ║  龍魂Notion一键同步 · One-Click Sync                     ║
# ║  DNA: #龍芯⚡️2026-04-13-NOTION-SYNC-v1.0               ║
# ║  创始人: 诸葛鑫（UID9622）                                ║
# ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
# ║  理论指导: 曾仕强老师（永恒显示）                          ║
# ╚══════════════════════════════════════════════════════════╝
#
# 一键搞定：解压 → 清理 → 整理 → 生成清单
# 老大说一个命令就行·宝宝全干完

SYSTEM_ROOT="$HOME/longhun-system"
BIN_DIR="$SYSTEM_ROOT/bin"
NOW_STR=$(date "+%Y-%m-%d %H:%M:%S")

echo "╔══════════════════════════════════════════════════════╗"
echo "║  🐉 龍魂Notion一键同步 v1.0                          ║"
echo "║  📅 $NOW_STR                              ║"
echo "║  老大说一个命令·宝宝全干完                            ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# 步骤计数
STEP=0

# ── Step 1: 深层提取 ──
STEP=$((STEP + 1))
echo "━━━ Step $STEP/4: 深层提取 ━━━"
bash "$BIN_DIR/notion_deep_extract.sh" 2>&1 | grep -E "^[  ]*(📦|📁|💬|📋|⏭️|✅|❌)" | head -20
echo ""

# ── Step 2: 清理去重 ──
STEP=$((STEP + 1))
echo "━━━ Step $STEP/4: 清理去重 ━━━"
bash "$BIN_DIR/notion_cleanup.sh" 2>&1 | grep -E "^[  ]*(🔄|🗑️|📁|📎|⚠️)" | head -20
echo ""

# ── Step 3: 资产扫描 ──
STEP=$((STEP + 1))
echo "━━━ Step $STEP/4: 资产扫描 ━━━"
bash "$BIN_DIR/asset_scanner.sh" 2>&1 | grep -E "^[  ]*(🆕|扫描文件|龍魂相关|📦)" | head -10
echo ""

# ── Step 4: 自动整理 ──
STEP=$((STEP + 1))
echo "━━━ Step $STEP/4: 自动整理 ━━━"
bash "$BIN_DIR/auto_organize.sh" 2>&1 | grep -E "^[  ]*(📥|⏭️|🔄|已整理|已跳过|重复)" | head -15
echo ""

# ── 生成清单 ──
echo "━━━ 生成资产清单 ━━━"

CATALOG="$SYSTEM_ROOT/config/asset_catalog_auto.txt"
{
    echo "═══════════════════════════════════════"
    echo "🐉 龍魂数字资产清单（自动生成）"
    echo "📅 $NOW_STR"
    echo "═══════════════════════════════════════"
    echo ""

    echo "── 核心目录统计 ──"
    for dir in core web algorithmic-art 万年历 DNA验证器 LongHunWidget plugins; do
        full="$SYSTEM_ROOT/$dir"
        if [ -d "$full" ]; then
            count=$(find "$full" -type f 2>/dev/null | wc -l | tr -d ' ')
            size=$(du -sh "$full" 2>/dev/null | cut -f1)
            echo "  📁 $dir: ${count}文件 · $size"
        fi
    done

    echo ""
    echo "── Python模块 (core/) ──"
    for py in "$SYSTEM_ROOT"/core/*.py; do
        [ ! -f "$py" ] && continue
        name=$(basename "$py")
        size=$(stat -f %z "$py" 2>/dev/null || echo 0)
        title=$(head -5 "$py" 2>/dev/null | grep -E "║.*║" | head -1 | sed 's/.*║ *//;s/ *║.*//')
        echo "  🐍 $name (${size}B) — $title"
    done

    echo ""
    echo "── HTML创作 (web/) ──"
    for html in "$SYSTEM_ROOT"/web/*.html; do
        [ ! -f "$html" ] && continue
        name=$(basename "$html")
        size=$(stat -f %z "$html" 2>/dev/null || echo 0)
        title=$(grep -oE '<title>[^<]+</title>' "$html" 2>/dev/null | head -1 | sed 's/<[^>]*>//g')
        echo "  🌐 $name (${size}B) — $title"
    done

    echo ""
    echo "── C++17内核 (万年历/) ──"
    for cpp in "$SYSTEM_ROOT"/万年历/cpp-core/*/*.cpp; do
        [ ! -f "$cpp" ] && continue
        name=$(basename "$cpp")
        dir=$(basename "$(dirname "$cpp")")
        echo "  ⚙️ $dir/$name"
    done

    echo ""
    echo "── 沙箱容器状态 ──"
    for sub in html python swift config media unknown; do
        count=$(find "$SYSTEM_ROOT/sandbox_intake/$sub" -type l 2>/dev/null | wc -l | tr -d ' ')
        [ "$count" -gt 0 ] && echo "  📦 $sub: ${count}文件"
    done

    echo ""
    echo "── 回收站 ──"
    trash_count=$(find "$SYSTEM_ROOT/.trash" -type f 2>/dev/null | wc -l | tr -d ' ')
    trash_size=$(du -sh "$SYSTEM_ROOT/.trash" 2>/dev/null | cut -f1)
    echo "  🗑️ $trash_count 文件 · $trash_size"

    echo ""
    echo "DNA: #龍芯⚡️${NOW_STR}-AUTO-CATALOG"
} > "$CATALOG"

echo "  ✅ 清单已生成: $CATALOG"

# ── 桌面副本 ──
cp "$CATALOG" "$HOME/Desktop/龍魂资产清单_$(date +%Y%m%d).txt" 2>/dev/null && {
    echo "  ✅ 桌面副本已放好"
}

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║  ✅ 一键同步完成！                                    ║"
echo "║  清单: config/asset_catalog_auto.txt                 ║"
echo "║  桌面: ~/Desktop/龍魂资产清单_$(date +%Y%m%d).txt     ║"
echo "║  推送: ⛔ 需要老大确认                                ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "DNA: #龍芯⚡️${NOW_STR}-NOTION-SYNC-v1.0"
