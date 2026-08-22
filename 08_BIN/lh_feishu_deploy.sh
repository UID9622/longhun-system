#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════╗
# ║  🐉 龍魂系统 · 飞书通知网关部署脚本                          ║
# ║  🏷️  版本: v1.0 · 飞书主通道+Bark备用+终端兜底               ║
# ║  🧬  DNA: #龍芯⚡️丙午·乙未·辛丑·甲午·䷨损-FEISHU-DEPLOY-v1.0              ║
# ║  👤  适用: UID9622 · 诸葛鑫                                  ║
# ╚═══════════════════════════════════════════════════════════════╝

set -euo pipefail

DNA="#龍芯⚡️丙午·乙未·辛丑·甲午·䷨损-FEISHU-DEPLOY-v1.0"
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BIN_DIR="${BASE_DIR}/bin"
CONFIG_DIR="${BASE_DIR}/config"
LOG_DIR="${BASE_DIR}/logs/notify"

echo "=== 🐉 龍魂·飞书通知网关 部署 ==="
echo "DNA: ${DNA}"
echo ""

# ────────────────────────────────────────────────────────────────
# 1. 环境检查
# ────────────────────────────────────────────────────────────────
echo "[1/5] 环境检查..."

if ! command -v python3 &>/dev/null; then
    echo "🔴 python3 未安装"
    exit 1
fi

PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "  Python: ${PY_VER}"

# 检查 cryptography（用于AES加密）
if python3 -c "from cryptography.hazmat.primitives.ciphers.aead import AESGCM" 2>/dev/null; then
    echo "  ✅ cryptography 已安装"
else
    echo "  ⚠️  cryptography 未安装（加密降级·生产环境必须安装）"
    echo "     运行: pip3 install cryptography"
fi

# 检查飞书Webhook配置
if [ -z "${FEISHU_WEBHOOK_URL:-}" ]; then
    echo "  🟡 FEISHU_WEBHOOK_URL 未设置（飞书推送不可用·非致命）"
    echo "     配置: export FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
else
    echo "  ✅ FEISHU_WEBHOOK_URL 已配置"
fi

if [ -z "${FEISHU_WEBHOOK_SECRET:-}" ]; then
    echo "  🟡 FEISHU_WEBHOOK_SECRET 未设置（签名校验不可用）"
else
    echo "  ✅ FEISHU_WEBHOOK_SECRET 已配置"
fi

if [ -z "${BARK_KEY:-}" ] && [ -z "${BARK_SERVER:-}" ]; then
    echo "  🟡 BARK_KEY/BARK_SERVER 未设置（Bark备用通道不可用）"
else
    echo "  ✅ Bark备用通道已配置"
fi

# ────────────────────────────────────────────────────────────────
# 2. 创建目录结构
# ────────────────────────────────────────────────────────────────
echo ""
echo "[2/5] 创建目录结构..."

mkdir -p "${LOG_DIR}"
mkdir -p "${CONFIG_DIR}"
echo "  ✅ 日志目录: ${LOG_DIR}"
echo "  ✅ 配置目录: ${CONFIG_DIR}"

# ────────────────────────────────────────────────────────────────
# 3. 配置文件
# ────────────────────────────────────────────────────────────────
echo ""
echo "[3/5] 检查配置文件..."

if [ ! -f "${CONFIG_DIR}/feishu_bot.yaml" ]; then
    echo "  ⚠️  feishu_bot.yaml 不存在，请从模板创建"
    echo "  cp config/feishu_bot.yaml.example config/feishu_bot.yaml"
    echo "  编辑并填入飞书 Webhook URL 和 Secret"
else
    echo "  ✅ feishu_bot.yaml 已存在"
fi

# ────────────────────────────────────────────────────────────────
# 4. 自检
# ────────────────────────────────────────────────────────────────
echo ""
echo "[4/5] 运行自检..."

cd "${BASE_DIR}"
if python3 "${BIN_DIR}/lh_notify_gateway.py" selftest 2>&1; then
    echo "  ✅ 网关自检通过"
else
    echo "  🔴 网关自检失败，请检查上述错误"
    exit 1
fi

# ────────────────────────────────────────────────────────────────
# 5. 集成提示
# ────────────────────────────────────────────────────────────────
echo ""
echo "[5/5] 集成指南..."
echo ""

# 检查是否已有健康检查脚本
HEALTH_CHECK="${BASE_DIR}/deploy/scripts/health_check.sh"
if [ -f "${HEALTH_CHECK}" ]; then
    echo "  📋 建议在 ${HEALTH_CHECK} 中增加飞书通知替代Bark推送："
    echo ""
    echo "    # 在 health_check.sh 尾部添加："
    echo "    python3 ${BIN_DIR}/lh_notify_gateway.py send \\"
    echo "      --event daily_health_report \\"
    echo "      --title \"鲲鹏健康检查\" \\"
    echo "      --body \"\${HEALTH_SUMMARY}\" \\"
    echo "      --source 鲲鹏"
    echo ""
fi

echo "  📋 在其他引擎中集成通知："
echo ""
echo "    from bin.lh_notify_gateway import 龍魂通知网关"
echo "    gw = 龍魂通知网关()"
echo "    gw.发送("
echo "        event_type='video_generated',"
echo "        title='视频生成完成',"
echo "        body=f'《{article_title}》已生成·抖音+视频号+B站',"
echo "        source='本地'"
echo "    )"
echo ""

echo "  📋 通知规则定义在 config/feishu_bot.yaml → notify_rules"

# ────────────────────────────────────────────────────────────────
# 完成
# ────────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════════════"
echo "  🎉 龍魂·飞书通知网关部署完成"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "  三条推送通道:"
echo "    🥇 飞书 Webhook（主力·富文本卡片）"
echo "    🥈 Bark 推送（备用·iOS 通知）"
echo "    🥉 终端通知（兜底·桌面弹窗）"
echo ""
echo "  优先级路由:"
echo "    P0 → 三通道立即推送（飞书+Bark+终端）"
echo "    P1 → 飞书立即推送"
echo "    P2 → 飞书定期摘要（每小时）"
echo "    P3 → 仅归档日志"
echo ""
echo "  安全:"
echo "    P0事件 → AES-256-GCM 七因子强制加密"
echo "    每条通知 → DNA完整追溯"
echo "    飞书 → HMAC-SHA256 签名校验"
echo ""
echo "  使用:"
echo "    python3 bin/lh_notify_gateway.py selftest     # 自检"
echo "    python3 bin/lh_notify_gateway.py status        # 状态"
echo "    python3 bin/lh_notify_gateway.py send ...      # 发送"
echo "    python3 bin/lh_notify_gateway.py history       # 历史"
echo ""
echo "  DNA: ${DNA}"
echo ""

exit 0
