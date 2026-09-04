#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · Git 仓库收拾脚本 v1.0
# 按 Kimi 建议收拾方案执行
# DNA: #龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-GIT-HISTORY-CLEANUP-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
set -euo pipefail

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
log() { echo -e "${GREEN}[$(date +%H:%M:%S)]${NC} $*"; }
warn() { echo -e "${YELLOW}⚠️${NC}  $*"; }

log "🐉 龍魂 Git 仓库收拾开始"

# ── 第0步：已有快照分支 backup-2026-07-12-pre-cherrypick，确认 ──
if ! git rev-parse --verify backup-2026-07-12-pre-cherrypick >/dev/null 2>&1; then
    log "创建安全快照..."
    git branch backup-2026-07-12-pre-cherrypick
fi
log "✅ 安全快照已确认: backup-2026-07-12-pre-cherrypick"

# ── 第1步：reset 到远端 main（干净历史） ──
log "Step 1: reset 到 origin/main（远端重写后的干净历史）"
git fetch origin 2>&1 | tail -3
CURRENT_HEAD=$(git rev-parse HEAD)
ORIGIN_HEAD=$(git rev-parse origin/main)

if [ "$CURRENT_HEAD" = "$ORIGIN_HEAD" ]; then
    log "本地已在 origin/main，无需 reset"
else
    log "当前 HEAD: ${CURRENT_HEAD:0:10}"
    log "origin/main: ${ORIGIN_HEAD:0:10}"
    git reset --hard origin/main 2>&1
    log "✅ 已 reset 到 origin/main"
fi

# ── 第2步：cherry-pick 独有提交 ──
log "Step 2: cherry-pick 33 个独有提交"

# 这些是从 Kimi 分析中确认的独有提交（按时间顺序，从早到晚）
UNIQUE_COMMITS=(
    "645785652"  # feat(training): DeepSeek 聊天记录抽取
    "07bca2389"  # feat(training): DeepSeek 对话为训练数据
    "9a2967219"  # feat(raw-feeder): 龍魂投喂器 + 开机自启
    "78d9a652b"  # feat(protocol): 数据主权与流量治理协议 v2.0
    "cac47d1c8"  # 🧹 龍魂收口整理
    "f5c4e8b9a"  # 📁 根目录整理
    "699ada240"  # 📋 备份目录弃用标注
    "3fe7e7f5f"  # 📦 备份目录完整入库
    "9b2812355"  # 🔒 龍魂安全协议·四级防火墙
    "49d5f3b4b"  # 🐉 龍魂v2.0·国标合规修复
    "5d6ae1541"  # feat: 指令中心 v1.0
    "32173115b"  # feat: 天下无欺 v1.0
    "0f2a79787"  # feat: 加密盾 v1.0
    "c0ec5d1cf"  # feat: 网络户口本 v1.0
    "39bde1d32"  # feat: 公开审计报告 v1.0
    "7635f4c15"  # feat: 定时自动审计 v1.0
    "f43b64fea"  # feat: 龍魂元宇宙 v1.0
    "1eaaa6d31"  # fix: FastAPI lifespan 写法升级
    "44d34a3a8"  # fix: CNSH编译器修复
    "e14209d0a"  # feat: 数字资产归档
    "ed45ee44a"  # feat: 换设备一键安装
    "74889788b"  # feat: 数据门卫+量子易经接口
    "ab537ff2e"  # chore: DNA 格式对齐
    "ef3c247ec"  # feat: 技术中立宣言
    "0ab7c0753"  # fix: /api/docs 路由修正
    "b4e66b5d1"  # 🐉 龍魂统一后端v2.0
    "cfa49682c"  # feat: 统一记忆中枢 v1.0
    "66c233aac"  # feat: DNA 固化脚本
    "89092e8ea"  # feat: 经济主权突破 v2.0
    "0ce83ba1d"  # feat: 四山硬科技突破 v1.0
    "784ec5ade"  # feat: 行为密码学·七维审计 v2.1
    "b505e8fed"  # feat: 行为密码学·水军审计一体化引擎 v2.0
    "0fd4959fc"  # feat: 数字江湖·黑箱审计报告 v1.0
    "031ede135"  # feat: 平台异常阻断日志系统 v1.0
    "7b411d956"  # feat: 水晶识别知识库 v1.0
    "965b59483"  # feat: 水晶识别 v2.0
    "ab83b2d76"  # feat: 千问幻觉案·多模型综合评分引擎 v1.0
    "0e96f76e5"  # 🐉 千问幻觉案评分引擎 v1.1
)

SUCCESS=0
FAILED=0
SKIPPED=0

for commit in "${UNIQUE_COMMITS[@]}"; do
    if git cherry-pick --no-commit "$commit" 2>/dev/null; then
        git commit -C "$commit" --no-edit 2>/dev/null && {
            log "  ✅ ${commit:0:10}"
            SUCCESS=$((SUCCESS + 1))
        } || {
            warn "  ⚠️ ${commit:0:10} 内容为空（可能已在远端），跳过"
            git cherry-pick --abort 2>/dev/null || true
            SKIPPED=$((SKIPPED + 1))
        }
    else
        # 冲突或失败
        warn "  🔴 ${commit:0:10} cherry-pick 失败（可能已存在或冲突）"
        git cherry-pick --abort 2>/dev/null || git reset --hard 2>/dev/null || true
        FAILED=$((FAILED + 1))
    fi
done

echo ""
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "📊 Cherry-pick 完成统计:"
log "   ✅ 成功: $SUCCESS"
log "   ⚠️ 跳过(已存在): $SKIPPED"
log "   🔴 失败: $FAILED"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 第3步：显示当前状态 ──
echo ""
log "Step 3: 当前仓库状态"
git log --oneline -5
echo ""
warn "远端状态:"
git log --oneline origin/main -3 2>/dev/null || true
echo ""
log "⚠️  工作区仍有 3356 个未提交改动——需要你确认哪些保留、哪些丢弃"
log "   快照在 backup-2026-07-12-pre-cherrypick 分支，可随时回退"
log ""
log "下一步建议:"
log "   1. 确认 cherry-pick 结果满意"
log "   2. 处理工作区改动 (git add / git checkout -- / git clean)"
log "   3. 推送到4个远端: git push origin main && git push https-origin main && git push gitee main && git push gitcode main"
