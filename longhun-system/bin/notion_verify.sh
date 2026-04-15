#!/bin/bash
# ╔══════════════════════════════════════════════════════════╗
# ║  龍魂Notion验证器 · Verify                               ║
# ║  DNA: #龍芯⚡️2026-04-13-NOTION-VERIFY-v1.0             ║
# ║  创始人: 诸葛鑫（UID9622）                                ║
# ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
# ║  理论指导: 曾仕强老师（永恒显示）                          ║
# ╚══════════════════════════════════════════════════════════╝
#
# 验证桌面清单和资料库清单是否一致
# SHA256哈希校验 · 一个都不能少

SYSTEM_ROOT="$HOME/longhun-system"
NOW_STR=$(date "+%Y-%m-%d %H:%M:%S")

echo "═══════════════════════════════════════"
echo "🐉 龍魂Notion验证器 v1.0"
echo "📅 $NOW_STR"
echo "═══════════════════════════════════════"
echo ""

PASS=0
FAIL=0

# ── 1. 桌面 vs 资料库清单一致性 ──
echo "── 1. 清单一致性验证 ──"

CATALOG_MAIN="$SYSTEM_ROOT/config/asset_catalog_auto.txt"
CATALOG_DESK=$(ls -t "$HOME/Desktop/龍魂资产清单_"*.txt 2>/dev/null | head -1)

if [ -f "$CATALOG_MAIN" ] && [ -f "$CATALOG_DESK" ]; then
    main_hash=$(shasum -a 256 "$CATALOG_MAIN" | cut -d' ' -f1)
    desk_hash=$(shasum -a 256 "$CATALOG_DESK" | cut -d' ' -f1)

    if [ "$main_hash" = "$desk_hash" ]; then
        echo "  ✅ 清单一致 (SHA256: ${main_hash:0:16}...)"
        PASS=$((PASS + 1))
    else
        echo "  ❌ 清单不一致！"
        echo "     资料库: ${main_hash:0:16}..."
        echo "     桌面:   ${desk_hash:0:16}..."
        echo "     💡 重新运行 notion_sync.sh 同步"
        FAIL=$((FAIL + 1))
    fi
else
    echo "  ⚠️  清单文件不完整"
    [ ! -f "$CATALOG_MAIN" ] && echo "     缺少: 资料库清单"
    [ -z "$CATALOG_DESK" ] && echo "     缺少: 桌面清单"
    FAIL=$((FAIL + 1))
fi

# ── 2. 核心文件完整性 ──
echo ""
echo "── 2. 核心文件完整性 ──"

CORE_FILES=(
    "core/baobao_dispatcher.py"
    "core/baobao_authority.py"
    "core/gentle_refusal.py"
    "core/page_helper.py"
    "core/dragon_stamp.py"
    "core/longhun_lang.py"
    "core/voice_reflux.py"
    "core/tail_sign.py"
    "core/inline_annotator.py"
    "config/baobao_master_key.json"
    "万年历/cpp-core/calendar/lunar_engine.cpp"
    "万年历/cpp-core/bagua/bagua_engine.cpp"
    "万年历/cpp-core/digital_root/sancai_engine.cpp"
    "万年历/cpp-core/dna/dna_activator.cpp"
)

for file in "${CORE_FILES[@]}"; do
    full="$SYSTEM_ROOT/$file"
    if [ -f "$full" ]; then
        # 检查龍字签到
        if grep -q "龍" "$full" 2>/dev/null; then
            echo "  ✅ $file (🐉签到)"
            PASS=$((PASS + 1))
        else
            echo "  ⚠️  $file (无龍字签到)"
            FAIL=$((FAIL + 1))
        fi
    else
        echo "  ❌ 缺失: $file"
        FAIL=$((FAIL + 1))
    fi
done

# ── 3. 服务配置验证 ──
echo ""
echo "── 3. 服务配置验证 ──"

# 检查钥匙文件
KEY_FILE="$SYSTEM_ROOT/config/baobao_master_key.json"
if [ -f "$KEY_FILE" ]; then
    if python3 -c "import json; json.load(open('$KEY_FILE'))" 2>/dev/null; then
        echo "  ✅ 钥匙文件 JSON合法"
        PASS=$((PASS + 1))
    else
        echo "  ❌ 钥匙文件 JSON损坏！"
        FAIL=$((FAIL + 1))
    fi
fi

# 检查自动化脚本可执行权限
for script in asset_scanner auto_organize notion_cleanup notion_deep_extract notion_sync notion_verify; do
    sfile="$SYSTEM_ROOT/bin/${script}.sh"
    if [ -x "$sfile" ]; then
        echo "  ✅ ${script}.sh 可执行"
        PASS=$((PASS + 1))
    elif [ -f "$sfile" ]; then
        echo "  ⚠️  ${script}.sh 无执行权限 → 修复中"
        chmod +x "$sfile"
        PASS=$((PASS + 1))
    else
        echo "  ❌ 缺失: ${script}.sh"
        FAIL=$((FAIL + 1))
    fi
done

# ── 4. C++17内核验证 ──
echo ""
echo "── 4. C++17内核验证 ──"

LIB="$SYSTEM_ROOT/万年历/cpp-core/liblonghun_calendar.a"
TEST="$SYSTEM_ROOT/万年历/cpp-core/test_calendar"

if [ -f "$LIB" ]; then
    lib_size=$(stat -f %z "$LIB" 2>/dev/null)
    echo "  ✅ 静态库存在 (${lib_size}B)"
    PASS=$((PASS + 1))
else
    echo "  ❌ 静态库缺失"
    FAIL=$((FAIL + 1))
fi

if [ -x "$TEST" ]; then
    # 快速运行测试
    test_result=$("$TEST" 2>/dev/null | tail -3 | head -1)
    if echo "$test_result" | grep -q "全部通过"; then
        echo "  ✅ C++17测试全部通过"
        PASS=$((PASS + 1))
    else
        echo "  ⚠️  C++17测试: $test_result"
        FAIL=$((FAIL + 1))
    fi
else
    echo "  ❌ 测试程序缺失·需要重新编译"
    FAIL=$((FAIL + 1))
fi

# ── 报告 ──
echo ""
echo "═══════════════════════════════════════"
TOTAL=$((PASS + FAIL))
echo "📊 验证结果: ✅ $PASS / $TOTAL"
if [ "$FAIL" -eq 0 ]; then
    echo "🏆 全部通过！系统完整！"
else
    echo "⚠️  有 $FAIL 项需要关注"
fi
echo "═══════════════════════════════════════"
echo ""
echo "DNA: #龍芯⚡️${NOW_STR}-NOTION-VERIFY-v1.0"
