#!/bin/bash
# ══════════════════════════════════════════════
# 龍魂系统 · 目录结构初始化脚本
# UID9622 · 诸葛鑫 · #龍芯⚡️20260422-SH-INIT01
# 执行: bash init_cnsh_structure.sh
# ══════════════════════════════════════════════

set -e
CNSH="$HOME/cnsh"
LS="$HOME/longhun-system"

echo "╔══════════════════════════════════════╗"
echo "║  龍魂目录结构初始化 · UID9622        ║"
echo "╚══════════════════════════════════════╝"

# ──────────────────────────────────────────────
# ~/cnsh/ — CNSH语义引擎工作区 (你截图里看到的)
# ──────────────────────────────────────────────
# 已存在的: 入口/ rules/ input/ logs/ output/
# 新增补全:
mkdir -p "$CNSH/入口/DNA"           # 流场密钥 + GPG签名DNA
mkdir -p "$CNSH/入口/auth"          # 令牌/证书 (不同步云端)
mkdir -p "$CNSH/入口/manifest"      # 系统状态快照
mkdir -p "$CNSH/rules"              # CNSH语法规则文件
mkdir -p "$CNSH/input"              # 入站请求原文
mkdir -p "$CNSH/output"             # 处理后输出
mkdir -p "$CNSH/logs/signed"        # GPG签名后的日志导出
mkdir -p "$CNSH/logs/archive"       # 历史归档
mkdir -p "$CNSH/sandbox"            # 沙盒推演临时区

echo "✅ ~/cnsh/ 结构完成"

# ──────────────────────────────────────────────
# ~/longhun-system/ — 本地引擎区 (20+工具)
# ──────────────────────────────────────────────
mkdir -p "$LS/engines"              # Python引擎 (audit_engine.py等)
mkdir -p "$LS/personas"             # 五大后台人格代码
mkdir -p "$LS/web"                  # Chrome Extension HTML工具
mkdir -p "$LS/config"               # 配置文件 (不含密钥)
mkdir -p "$LS/scripts"              # 启动/维护脚本
mkdir -p "$LS/data/sqlite"          # SQLite数据库
mkdir -p "$LS/data/snapshots"       # 快照存档

echo "✅ ~/longhun-system/ 结构完成"

# ──────────────────────────────────────────────
# 把 audit_engine.py 复制到正确位置
# ──────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -f "$SCRIPT_DIR/audit_engine.py" ]; then
    cp "$SCRIPT_DIR/audit_engine.py" "$LS/engines/audit_engine.py"
    echo "✅ audit_engine.py → $LS/engines/"
fi

# ──────────────────────────────────────────────
# 权限锁定 (auth目录只有自己能读)
# ──────────────────────────────────────────────
chmod 700 "$CNSH/入口/auth"
echo "✅ auth/ 权限锁 700"

# ──────────────────────────────────────────────
# 生成目录清单 → 写入 Notion 同步点
# ──────────────────────────────────────────────
MANIFEST="$CNSH/入口/manifest/structure_$(date +%Y%m%d).json"
cat > "$MANIFEST" << EOF
{
  "uid": "UID9622",
  "dna": "#龍芯⚡️$(date +%Y%m%d)-SH-INIT01",
  "generated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "cnsh_root": "$CNSH",
  "longhun_root": "$LS",
  "directories": {
    "cnsh": {
      "入口/DNA":       "流场混沌密钥 + GPG签名DNA文件",
      "入口/auth":      "本地令牌证书 [chmod700 · 不上云]",
      "入口/manifest":  "系统状态快照 JSON",
      "rules":          "CNSH语法规则",
      "input":          "入站请求原文",
      "output":         "处理结果输出",
      "logs/signed":    "GPG签名日志导出",
      "logs/archive":   "历史归档",
      "sandbox":        "沙盒推演临时区"
    },
    "longhun_system": {
      "engines":        "Python核心引擎 (audit/shield/gua/bone...)",
      "personas":       "五大后台人格 (wenwen/scout/guardian/builder/syncer)",
      "web":            "Chrome Extension 9大工具HTML",
      "config":         "配置文件 (不含密钥)",
      "scripts":        "启停维护脚本",
      "data/sqlite":    "SQLite数据库 (audit.db等)",
      "data/snapshots": "系统状态快照归档"
    }
  },
  "ports": {
    "3000": "OpenWebUI (Ollama前端)",
    "8765": "主服务 (CNSH网关)",
    "9622": "龍魂审计引擎 (audit_engine.py)",
    "11434": "Ollama本地模型"
  },
  "signature": "UID9622 · GPG:A2D0092C · 不黑箱·审计即主权"
}
EOF

echo "✅ 系统清单 → $MANIFEST"

# ──────────────────────────────────────────────
# 生成 .env 模板 (需要自己填值)
# ──────────────────────────────────────────────
ENV_TEMPLATE="$LS/config/env.template"
cat > "$ENV_TEMPLATE" << 'EOF'
# 龍魂系统环境变量模板
# cp env.template .env && nano .env
# source .env 或加入 ~/.zshrc

# Notion集成
export NOTION_TOKEN="secret_你的Notion令牌"
export NOTION_AUDIT_DB_ID="你的审计数据库ID"

# 本地安全令牌 (自己设一个强密码)
export DNA_TOKEN="UID9622-你的本地密码"

# GPG密钥ID
export GPG_KEY="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# Ollama配置
export OLLAMA_HOST="http://localhost:11434"
EOF

echo "✅ 环境变量模板 → $ENV_TEMPLATE"
echo ""

# ──────────────────────────────────────────────
# 打印完整结构树
# ──────────────────────────────────────────────
echo "════════════════════════════════════════"
echo "📂 ~/cnsh/"
echo "   ├── 入口/"
echo "   │   ├── DNA/        ← 流场密钥 + DNA签名"
echo "   │   ├── auth/       ← 令牌证书 [700 仅本机]"
echo "   │   └── manifest/   ← 系统状态快照"
echo "   ├── rules/          ← CNSH语法规则"
echo "   ├── input/          ← 入站请求"
echo "   ├── output/         ← 处理结果"
echo "   ├── logs/"
echo "   │   ├── audit.db    ← SQLite追加只读"
echo "   │   ├── signed/     ← GPG签名日志"
echo "   │   └── archive/    ← 历史归档"
echo "   └── sandbox/        ← 沙盒推演"
echo ""
echo "📂 ~/longhun-system/"
echo "   ├── engines/        ← audit_engine.py 等"
echo "   ├── personas/       ← 五大后台人格"
echo "   ├── web/            ← Chrome工具9件"
echo "   ├── config/         ← 配置(无密钥)"
echo "   ├── scripts/        ← 启停脚本"
echo "   └── data/"
echo "       ├── sqlite/     ← audit.db"
echo "       └── snapshots/  ← 快照归档"
echo "════════════════════════════════════════"
echo ""
echo "🚀 下一步:"
echo "   1. cd $LS/config && cp env.template .env && nano .env"
echo "   2. source .env"
echo "   3. pip install flask requests --break-system-packages"
echo "   4. python $LS/engines/audit_engine.py"
echo "   5. curl -H 'X-DNA-Token: \$DNA_TOKEN' http://localhost:9622/stats"
echo ""
echo "✅ 龍魂目录初始化完成 · DNA:#龍芯⚡️$(date +%Y%m%d)-SH-INIT01"
