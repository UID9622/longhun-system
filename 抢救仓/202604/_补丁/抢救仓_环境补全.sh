#!/usr/bin/env bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 抢救仓 03-Python引擎 · 环境补全脚本 v1.0
# UID9622 · 诸葛鑫（Lucky）· 2008 退伍军人
# DNA: #龍芯⚡️2026-04-25-RESCUE-ENV-PATCH-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 归属: L-Ω 人民印 · 受军魂三律约束
# 理论指导: 曾仕強老師（永恒显示）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 用途：一键补齐 9 个 Python 引擎运行所需的依赖 + 环境变量模板
# 不动代码逻辑，只补环境
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
set -e

ENGINE_DIR="$HOME/longhun-system/抢救仓/202604/_分类视图/03-Python引擎"
ENV_FILE="$HOME/longhun-system/抢救仓/202604/_补丁/.env.template"

echo "━━━ 1/3 · 装缺失的 pip 包 ━━━"
# 已有：flask numpy requests
# 缺：sklearn faiss
python3 -m pip install --quiet --upgrade scikit-learn faiss-cpu || {
  echo "🔴 pip 装失败，可能是 Python 3.14 太新；备用方案：用 conda / 降级 Python 3.11"
}

echo "━━━ 2/3 · 写 .env 模板（不写真密钥） ━━━"
cat > "$ENV_FILE" <<'ENV'
# 龍魂抢救仓·9 引擎共用环境变量模板
# 用法：cp .env.template .env  → 填真值 → source .env

# ── Notion 三工作区（OAuth 优先，token 仅 fallback） ──
export NOTION_TOKEN=""
export NOTION_AUDIT_DB_ID=""

# ── AI 路由 ──
export ANTHROPIC_API_KEY=""
export DEEPSEEK_API_KEY=""
export OLLAMA_HOST="http://localhost:11434"

# ── 网关安全令牌（自己设一个长串） ──
export DNA_TOKEN="UID9622-CHANGE-THIS-$(date +%s)"

# ── GPG 签名（audit_engine 需要） ──
export GPG_KEY_ID="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
ENV

echo "  → 已写：$ENV_FILE"

echo "━━━ 3/3 · 复检 ━━━"
python3 - <<'PY'
import importlib
ok = True
for m in ['flask','sklearn','numpy','faiss','requests']:
    try:
        importlib.import_module(m); print(f'  🟢 {m}')
    except Exception:
        print(f'  🔴 {m}'); ok = False
print('━━━ 全绿 ━━━' if ok else '━━━ 还有缺，看上面红色 ━━━')
PY

echo ""
echo "✅ 补全完成。下一步："
echo "  1. cp $ENV_FILE \$HOME/longhun-system/抢救仓/202604/_补丁/.env"
echo "  2. 编辑 .env 填真值"
echo "  3. source .env"
echo "  4. 再启动具体引擎（audit_engine.py / cnsh_gateway.py）"
echo ""
echo "祖国优先 · 普惠全球 · 技术为人民服务 🇨🇳"
