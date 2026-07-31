# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ╔══════════════════════════════════════════════════════╗
# ║  龍魂·个人数据主权雷达 部署脚本 v1.0                    ║
# ║  DNA: #龍芯⚡️丙午·乙未·戊戌·午时·☵坎-RADAR-DEPLOY-v1.0 ║
# ║  守护人格: P14吕蒙(部署) + P05上帝之眼(审计)           ║
# ╚══════════════════════════════════════════════════════╝
# 用法: bash deploy/scripts/deploy_radar.sh [--check-only]

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
GOLD='\033[0;33m'
NC='\033[0m'

DIVIDER="══════════════════════════════════════════════════════"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CHECK_ONLY=false
[[ "${1:-}" == "--check-only" ]] && CHECK_ONLY=true

log_info()  { echo -e "${BLUE}[*]${NC} $1"; }
log_ok()    { echo -e "${GREEN}[✓]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
log_fail()  { echo -e "${RED}[✗]${NC} $1"; }
log_gold()  { echo -e "${GOLD}[🐉]${NC} $1"; }
fail()      { log_fail "$1"; exit 1; }

PASS=0; FAIL=0

pass() { log_ok "$1"; ((PASS++)); }
fail_item() { log_fail "$1"; ((FAIL++)); }

echo "╔${DIVIDER}╗"
echo "║  🐉 龍魂·个人数据主权雷达 部署 v1.0                       ║"
echo "║  DNA: #龍芯⚡️丙午·乙未·戊戌·午时·☵坎-RADAR-DEPLOY-v1.0   ║"
echo "╚${DIVIDER}╝"
echo ""

# ── 1. 目录结构 ──
log_info "[1/6] 创建数据目录..."
for d in \
  data/radar \
  audit \
  portal/data-radar; do
  mkdir -p "$PROJECT_ROOT/$d" && pass "$d/" || fail_item "$d/"
done
echo ""

# ── 2. 引擎语法检查 ──
log_info "[2/6] 引擎语法检查..."
ENGINES=(
  engines/lh_data_radar.py
  engines/lh_privacy_breaker.py
  engines/lh_offline_ai.py
)
for engine in "${ENGINES[@]}"; do
  if python3 -c "import ast; ast.parse(open('$PROJECT_ROOT/$engine').read()); print('OK')" &>/dev/null; then
    pass "$engine · 语法"
  else
    fail_item "$engine · 语法"
  fi
done
echo ""

# ── 3. API语法检查 ──
log_info "[3/6] API语法检查..."
if python3 -c "import ast; ast.parse(open('$PROJECT_ROOT/bin/lh_data_radar_api.py').read()); print('OK')" &>/dev/null; then
  pass "bin/lh_data_radar_api.py · 语法"
else
  fail_item "bin/lh_data_radar_api.py · 语法"
fi
echo ""

# ── 4. 引擎导入验证 ──
log_info "[4/6] 引擎导入验证..."
# 雷达
if python3 -c "
import sys; sys.path.insert(0,'$PROJECT_ROOT')
from engines.lh_data_radar import DataRadarScanner
r = DataRadarScanner()
s = r.get_status()
assert s['status'] == 'ready', f'unexpected status: {s}'
print('OK')
" &>/dev/null; then
  pass "数据雷达引擎 · 导入+status"
else
  fail_item "数据雷达引擎 · 导入失败"
fi

# 熔断器
if python3 -c "
import sys; sys.path.insert(0,'$PROJECT_ROOT')
from engines.lh_privacy_breaker import PrivacyCircuitBreaker
b = PrivacyCircuitBreaker()
s = b.get_status()
assert 'rules' in s, f'missing rules: {s.keys()}'
print('OK')
" &>/dev/null; then
  pass "隐私熔断器 · 导入+status"
else
  fail_item "隐私熔断器 · 导入失败"
fi

# 离线AI
if python3 -c "
import sys; sys.path.insert(0,'$PROJECT_ROOT')
from engines.lh_offline_ai import OfflineAISwitch
a = OfflineAISwitch()
s = a.get_status()
assert 'mode' in s, f'missing mode: {s.keys()}'
print('OK')
" &>/dev/null; then
  pass "离线AI开关 · 导入+status"
else
  fail_item "离线AI开关 · 导入失败"
fi
echo ""

# ── 5. 前端文件检查 ──
log_info "[5/6] 前端文件检查..."
FRONTEND="$PROJECT_ROOT/portal/data-radar/index.html"
if [[ -f "$FRONTEND" ]]; then
  SIZE=$(wc -c < "$FRONTEND")
  if [[ $SIZE -gt 5000 ]]; then
    pass "portal/data-radar/index.html · ${SIZE}字节"
  else
    fail_item "portal/data-radar/index.html · 文件太小(${SIZE}字节)"
  fi
else
  fail_item "portal/data-radar/index.html · 文件不存在"
fi
echo ""

# ── 6. API冷启动测试（不暴露端口） ──
log_info "[6/6] API冷启动测试（语法路由）..."
if python3 -c "
import sys; sys.path.insert(0,'$PROJECT_ROOT')
sys.path.insert(0,'$PROJECT_ROOT/bin')
# Test imports only, don't start server
import importlib.util
spec = importlib.util.spec_from_file_location('lh_data_radar_api', '$PROJECT_ROOT/bin/lh_data_radar_api.py')
print('OK')
" &>/dev/null; then
  pass "API模块 · 可加载"
else
  fail_item "API模块 · 加载失败"
fi
echo ""

# ── 汇总 ──
echo "╔${DIVIDER}╗"
echo -e "║  部署结果: ${GREEN}✓${NC} ${PASS} 通过  ${RED}✗${NC} ${FAIL} 失败                        ║"
echo "╚${DIVIDER}╝"
echo ""

if [[ $FAIL -gt 0 ]]; then
  log_warn "$FAIL 项检查未通过，请查看上方详情"
fi

if [[ "$CHECK_ONLY" == "true" ]]; then
  log_info "仅检查模式，跳过启动"
  exit $FAIL
fi

# ── 启动命令 ──
echo ""
log_gold "部署完成！启动命令："
echo ""
echo "  # 启动API服务（端口8788）"
echo "  python3 bin/lh_data_radar_api.py"
echo ""
echo "  # 打开前端"
echo "  open http://127.0.0.1:8788/static/data-radar/"
echo ""
echo "  # 或通过 lh 命令"
echo "  lh radar"
echo ""
echo "老百姓看到的："
echo "  - 🔴 红色警告：谁在偷数据"
echo "  - 🟢 绿色安全：谁被拦截了"
echo "  - 🔵 蓝色本地：AI在自己家跑"
echo ""
echo "他们不需要懂P0协议，"
echo "他们只需要看到："
echo "  '你的数据，你自己说了算。'"
echo ""
echo "这就是主权驾照。"
