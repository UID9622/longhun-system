#!/bin/bash
# deploy.sh · 龍魂审计链 · 数字人民币跨境结算桥 · 一键部署
# DNA: #龍芯⚡️2026-08-23-ECNY-DEPLOY-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 设计原则: 老大什么都不用懂，粘贴执行一键搞定
set -e

EXCHANGE=~/longhun-system/exchange
echo ""
echo "💴 龍魂审计链 · 数字人民币跨境结算桥 v1.0"
echo "============================================"
echo ""

# ─── Step 1: 创建目录 ───
echo "1️⃣  创建目录结构..."
mkdir -p $EXCHANGE/{db,api}
touch $EXCHANGE/api/__init__.py
echo "   ✅ 目录就绪"

# ─── Step 2: 安装 Python 依赖 ───
echo "2️⃣  安装依赖..."
which python3 || { echo "❌ 需要 python3"; exit 1; }
# 系统 Homebrew Python 受 PEP 668 保护，自动加 --break-system-packages（龍魂官方流程 lh_install_deps.py 同款）
python3 -m pip install flask pyyaml --quiet --break-system-packages 2>/dev/null \
  || python3 -m pip install flask pyyaml --quiet 2>/dev/null \
  || echo "   ⚠️ 依赖已存在或安装跳过（继续）"
python3 -c "import flask, yaml" 2>/dev/null && echo "   ✅ flask + pyyaml 就绪" \
  || { echo "   ❌ 依赖安装失败"; exit 1; }

# ─── Step 3: 检查各文件是否就位 ───
echo "3️⃣  检查文件..."
FILES=(
  "config.yaml"
  "dna_utils.py"
  "rate_fetcher.py"
  "converter.py"
  "ecny_channel.py"
  "api/app.py"
)
ALL_OK=true
for f in "${FILES[@]}"; do
  if [ -f "$EXCHANGE/$f" ]; then
    echo "   ✅ $f"
  else
    echo "   ❌ $f 缺失"
    ALL_OK=false
  fi
done
if [ "$ALL_OK" = false ]; then
  echo ""
  echo "⚠️  有文件缺失，请确认所有 .py 和 .yaml 文件已保存到 $EXCHANGE/"
  exit 1
fi

# ─── Step 4: 初始化数据库 ───
echo "4️⃣  初始化 SQLite 账本..."
cd $EXCHANGE
python3 -c "
import sys; sys.path.insert(0,'.')
from converter import CurrencyConverter
print('   ✅ 数据库表创建完成')
"

# ─── Step 5: 测试汇率获取（联网） ───
echo "5️⃣  测试汇率获取（联网）..."
python3 -c "
import sys; sys.path.insert(0,'.')
from rate_fetcher import get_rate_to_cny
for c in ['USD', 'EUR', 'JPY', 'BTC']:
    r = get_rate_to_cny(c)
    flag = '🟡 兜底' if r['is_fallback'] else '🟢 实时'
    print(f'   {flag} 1 {c} = {r[\"rate\"]:.4f} CNY ({r[\"source\"]})')
"

# ─── Step 6: 测试汇兑 ───
echo "6️⃣  测试汇兑模块..."
python3 -c "
import sys; sys.path.insert(0,'.')
from converter import CurrencyConverter
c = CurrencyConverter()
r = c.convert(100, 'USD', 'test_user')
print(f'   ✅ 100 USD → {r[\"converted\"][\"amount\"]} eCNY')
print(f'   DNA: {r[\"dna\"]}')
"

# ─── Step 7: 启动 API 服务（后台） ───
echo "7️⃣  启动 API 服务..."
cd $EXCHANGE
# 先杀掉旧进程
lsof -ti:8899 | xargs kill -9 2>/dev/null || true
sleep 0.5
# 后台启动
nohup python3 api/app.py > $EXCHANGE/api.log 2>&1 &
echo $! > $EXCHANGE/api.pid
sleep 2

# ─── Step 8: 健康检查 ───
echo "8️⃣  健康检查..."
HEALTH=$(python3 -c "
import urllib.request, json
try:
    r = urllib.request.urlopen('http://localhost:8899/dna/health', timeout=5)
    d = json.loads(r.read())
    print(d['status'])
except: print('fail')
")
if [ "$HEALTH" = "ok" ]; then
  echo "   ✅ 服务运行正常"
else
  echo "   ⚠️  服务未响应，查看日志: tail -f $EXCHANGE/api.log"
fi

# ─── Step 9: 冒烟测试三个接口 ───
echo "9️⃣  冒烟测试接口..."
python3 - <<'PYEOF'
import urllib.request, urllib.error, json

def post(url, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data,
          headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"error": str(e)}

base = "http://localhost:8899"

# /dna/pay
p = post(f"{base}/dna/pay",
         {"amount": 100, "currency": "USD", "user_id": "test_uid"})
print(f"   /dna/pay  → {p.get('received','')} → {p.get('converted','')} {p.get('tri_color','')}")

# /dna/audit
a = post(f"{base}/dna/audit",
         {"caller_id": "test_uid", "service": "calibration_check", "calls": 5})
print(f"   /dna/audit → 扣费 {a.get('charged','')} {a.get('tri_color','')}")

# /dna/settle
import urllib.request as ur
with ur.urlopen(f"{base}/dna/settle?limit=3", timeout=5) as r:
    s = json.loads(r.read())
print(f"   /dna/settle → 共 {s['summary']['total_transactions']} 笔 {s['summary']['total_ecny_settled']} eCNY {s.get('tri_color','')}")
PYEOF

echo ""
echo "✅ 龍魂审计链部署完成！"
echo ""
echo "📡 API 地址:"
echo "   POST http://localhost:8899/dna/pay"
echo "   POST http://localhost:8899/dna/audit"
echo "   GET  http://localhost:8899/dna/settle"
echo "   GET  http://localhost:8899/dna/health"
echo ""
echo "📒 账本位置: $EXCHANGE/db/ledger.db"
echo "📄 服务日志: tail -f $EXCHANGE/api.log"
echo "🛑 停止服务: kill \$(cat $EXCHANGE/api.pid)"
echo ""
echo "💡 切换到 live 模式: 在 config.yaml 填入 ecny.api_key 即可自动升级"
echo ""
echo "DNA: #龍芯⚡️2026-08-23-ECNY-BRIDGE-v1.0-UID9622"
echo "SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
