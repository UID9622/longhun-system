#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 水军显化补丁 v1.2 回归测试
# DNA: #龍芯⚡️丙午·乙未·甲午·庚午·䷳艮为山-SHUIJUN-DISCLOSE-V1.2-VERIFY
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
set -euo pipefail

cd "$(dirname "$0")/.."
export PYTHONPATH="${PYTHONPATH:-}:$(pwd)/bin"
PASS=0
FAIL=0

red() { echo -e "\033[31m$*\033[0m"; }
green() { echo -e "\033[32m$*\033[0m"; }
yellow() { echo -e "\033[33m$*\033[0m"; }

test_py() {
    local id="$1"; shift
    local desc="$1"; shift
    if python3 -c "$@" >/dev/null 2>&1; then
        green "✅ $id $desc"
        PASS=$((PASS+1))
    else
        red "❌ $id $desc"
        FAIL=$((FAIL+1))
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "水军显化补丁 v1.2 回归测试 (T13-T24)"
echo "PYTHONPATH=$PYTHONPATH"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_py T13 "七因子全0.9 → G0" "
from lh_shuijun_patch import CNSH_水军补丁内核
核=CNSH_水军补丁内核()
r=核.可信度({'设备':0.9,'关联簇':0.9,'地理IP':0.9,'时间':0.9,'兴趣':0.9,'社交图':0.9,'文本':0.9})
assert r['标注'] and abs(r['c']-0.9)<1e-9 and r['级别']=='G0', r
"

test_py T14 "四因子 → 不标注" "
from lh_shuijun_patch import CNSH_水军补丁内核
核=CNSH_水军补丁内核()
r=核.可信度({'设备':0.9,'关联簇':0.9,'地理IP':0.9,'时间':0.9})
assert not r['标注'] and '疑罪从无' in r['原因'], r
"

test_py T15 "冷启动权重≈0.11" "
from lh_shuijun_patch import CNSH_水军补丁内核
w=CNSH_水军补丁内核.冷启动权重(10,20)
assert abs(w-10/90)<1e-9, w
"

test_py T16 "自然簇豁免通过" "
from lh_shuijun_patch import CNSH_水军补丁内核
assert CNSH_水军补丁内核.自然簇豁免(0.8,0.1,0.1)
"

test_py T17 "同模板不豁免" "
from lh_shuijun_patch import CNSH_水军补丁内核
assert not CNSH_水军补丁内核.自然簇豁免(0.8,0.1,0.85)
"

test_py T18 "嫁祸保护性标签" "
from lh_shuijun_patch import CNSH_水军补丁内核
r=CNSH_水军补丁内核.水军雇主认定(False,False,False,False,False)
assert '被异常流量波及' in r, r
"

test_py T19 "自营水军认定" "
from lh_shuijun_patch import CNSH_水军补丁内核
r=CNSH_水军补丁内核.水军雇主认定(True,True,False,False,True)
assert '认定自营水军' in r, r
"

test_py T20 "误判补偿84000" "
from lh_shuijun_patch import CNSH_水军补丁内核
c=CNSH_水军补丁内核.误判补偿(10000,3000,10)
assert c==84000, c
"

test_py T21 "G1半衰90天W=0.5" "
from lh_shuijun_patch import CNSH_水军补丁内核
r=CNSH_水军补丁内核.标签衰减(1.0,90,'G1')
assert abs(r['W']-0.5)<1e-9 and not r['摘标'], r
"

test_py T22 "批评可见度0.5" "
from lh_shuijun_patch import CNSH_水军补丁内核
v=CNSH_水军补丁内核.批评可见度(5,20,100)
assert abs(v-0.5)<1e-9, v
"

test_py T23 "肯德尔τ=-1" "
from lh_shuijun_patch import CNSH_水军补丁内核
t=CNSH_水军补丁内核.肯德尔τ([1,2,3,4],[4,3,2,1])
assert abs(t+1.0)<1e-9, t
"

test_py T24 "标签哈希防篡改" "
from lh_shuijun_patch import CNSH_水军补丁内核
h1=CNSH_水军补丁内核.标签状态哈希('abc123','G1',0.65,'2026-07-19T12:00:00Z','system')
h2=CNSH_水军补丁内核.标签状态哈希('abc123','G1',0.66,'2026-07-19T12:00:00Z','system')
assert h1!=h2 and len(h1)==64
"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $FAIL -eq 0 ]; then
    green "🟢 水军补丁 T13-T24 全绿通过 ($PASS/12)"
else
    red "🔴 水军补丁失败 $FAIL 项，通过 $PASS 项"
fi

# 若道德经定锚测试脚本存在，合并跑 T01-T12
if [ -x bin/lh_daodejing_anchor_verify.sh ]; then
    echo ""
    echo "🔗 接力运行道德经定锚测试 (T01-T12)..."
    bash bin/lh_daodejing_anchor_verify.sh || true
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
exit $FAIL
