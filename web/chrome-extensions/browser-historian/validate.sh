#!/bin/bash
# 龍魂·浏览器史官 — 自检脚本 v2.0
# 验证: manifest / 文件 / 图标 / 权限 / CSP / 底座痕迹
# 用法: bash validate.sh
set -euo pipefail

PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"
LONGHUN_ROOT="$(dirname "$(dirname "$(dirname "$PLUGIN_DIR")")")"
PASS=0; FAIL=0
GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; NC='\033[0m'

check()     { PASS=$((PASS+1)); echo -e "  ${GREEN}✅ $1${NC}"; }
fail()      { FAIL=$((FAIL+1)); echo -e "  ${RED}❌ $1${NC}"; }
warn()      { echo -e "  ${YELLOW}⚠️  $1${NC}"; }

echo "🔍 龍魂·浏览器史官 v2.0 自检"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ━━ Manifest ━━
echo "--- Manifest ---"
if [ -f "$PLUGIN_DIR/manifest.json" ]; then
    check "manifest.json 存在"
    
    if python3 -c "import json; m=json.load(open('$PLUGIN_DIR/manifest.json')); assert m['manifest_version']==3" 2>/dev/null; then
        check "Manifest V3"
    else
        fail "Manifest 版本不是 V3"
    fi
    
    VER=$(python3 -c "import json; print(json.load(open('$PLUGIN_DIR/manifest.json'))['version'])" 2>/dev/null || echo "?")
    if [ "$VER" = "2.0.0" ]; then
        check "版本号 v2.0.0 ✓"
    else
        warn "版本号: $VER (期望 2.0.0)"
    fi
    
    # 权限检查
    for perm in history storage downloads; do
        if python3 -c "import json; m=json.load(open('$PLUGIN_DIR/manifest.json')); assert '$perm' in m['permissions']" 2>/dev/null; then
            check "权限: $perm"
        else
            fail "缺少权限: $perm"
        fi
    done
    
    # host_permissions 检查 (v2.0)
    if python3 -c "import json; m=json.load(open('$PLUGIN_DIR/manifest.json')); hp=m.get('host_permissions',[]); assert 'http://127.0.0.1:18775/*' in hp" 2>/dev/null; then
        check "host_permissions: 本地采集API"
    else
        warn "host_permissions 未包含本地采集API"
    fi
    
    # CSP
    CSP=$(python3 -c "import json; m=json.load(open('$PLUGIN_DIR/manifest.json')); print(m.get('content_security_policy',{}).get('extension_pages',''))" 2>/dev/null)
    if echo "$CSP" | grep -q "script-src 'self'"; then
        check "CSP: script-src 'self'"
    else
        fail "CSP 不安全"
    fi
else
    fail "manifest.json 不存在"
fi

# ━━ 文件完整性 ━━
echo "--- 文件完整性 ---"
for f in popup.html popup.js styles.css background.js classifier.js README.md validate.sh; do
    if [ -f "$PLUGIN_DIR/$f" ]; then
        check "$f 存在"
    else
        fail "$f 缺失"
    fi
done

# ━━ 图标 ━━
echo "--- 图标 ---"
for size in 16 48 128; do
    if [ -f "$PLUGIN_DIR/icons/icon${size}.png" ]; then
        check "icon${size}.png"
    else
        fail "icon${size}.png 缺失"
    fi
done

# ━━ 底座痕迹功能 (v2.0) ━━
echo "--- 底座痕迹功能 (v2.0) ---"
if grep -q "底座痕迹" "$PLUGIN_DIR/popup.html" 2>/dev/null; then
    check "popup.html: 底座痕迹标签页"
else
    fail "popup.html: 缺少底座痕迹标签页"
fi

if grep -q "COLLECTOR_API" "$PLUGIN_DIR/popup.js" 2>/dev/null; then
    check "popup.js: 采集API集成"
else
    fail "popup.js: 缺少采集API代码"
fi

if grep -q "trace-timeline" "$PLUGIN_DIR/styles.css" 2>/dev/null; then
    check "styles.css: 时间线样式"
else
    fail "styles.css: 缺少时间线样式"
fi

# ━━ 采集引擎状态 ━━
echo "--- 底座采集引擎 ---"
COLLECTOR_BIN="$LONGHUN_ROOT/bin/lh_base_trace_collector.py"
if [ -f "$COLLECTOR_BIN" ]; then
    check "采集引擎脚本存在"
else
    warn "采集引擎脚本不存在: $COLLECTOR_BIN"
    warn "(不影响浏览器史官基本功能，但底座痕迹功能无法使用)"
fi

# 安装脚本
INSTALL_SCRIPT="$LONGHUN_ROOT/bin/lh_trace_install.sh"
if [ -f "$INSTALL_SCRIPT" ]; then
    check "一键安装脚本存在"
else
    warn "一键安装脚本不存在: $INSTALL_SCRIPT"
fi

# ━━ 导出功能 ━━
echo "--- 导出功能 ---"
if grep -q "chrome.downloads.download" "$PLUGIN_DIR/popup.js"; then
    check "导出: chrome.downloads API"
else
    fail "导出: 缺少 chrome.downloads"
fi

if grep -q "saveAs" "$PLUGIN_DIR/popup.js"; then
    check "导出: saveAs 系统对话框"
else
    warn "导出: 未使用 saveAs"
fi

# ━━ 分类引擎 ━━
echo "--- 分类引擎 ---"
if grep -q "DOMAIN_MAP" "$PLUGIN_DIR/classifier.js" 2>/dev/null; then
    check "分类器: DOMAIN_MAP"
else
    fail "分类器: 缺少 DOMAIN_MAP"
fi

# ━━ 结果 ━━
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
TOTAL=$((PASS+FAIL))
echo -e "通过: ${GREEN}${PASS}${NC} / 失败: ${RED}${FAIL}${NC} / 总计: ${TOTAL}"
if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}🎉 所有检查通过！插件可以加载。${NC}"
    exit 0
else
    echo -e "${RED}⚠️  有 ${FAIL} 项检查失败，请修复后重试。${NC}"
    exit 1
fi
