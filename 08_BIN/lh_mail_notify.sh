#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ╔═══════════════════════════════════════════════════════════════╗
# ║  🐉 龍魂系统 · Apple Mail 通知引擎                          ║
# ║  🏷️  版本: v1.0                                              ║
# ║  🧬  DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-MAIL-NOTIFY-v1.0 ║
# ║  👤  创建者: 诸葛鑫（UID9622）                               ║
# ║  📧  通过: Apple Mail.app (osascript)                       ║
# ╚═══════════════════════════════════════════════════════════════╝
#
# 用法:
#   lh_mail_notify.sh "标题" "正文" [level]
#   level: info(默认) | warn | critical
#
# 或直接管道:
#   echo "正文内容" | lh_mail_notify.sh "标题" -
#
# 环境变量:
#   MAIL_TO: 收件人 (默认: ahaojiaqi520@icloud.com)
#   MAIL_FROM: 发件人 (默认: ahaojiaqi520@icloud.com)

set -e

TITLE="${1:-龍魂系统通知}"
BODY="${2:-}"
LEVEL="${3:-info}"

# 从stdin读取正文（如果第二个参数是 - 或为空）
if [ "$BODY" = "-" ] || [ -z "$BODY" ]; then
    BODY=$(cat)
fi

# 收件人配置
MAIL_TO="${MAIL_TO:-ahaojiaqi520@icloud.com}"
MAIL_FROM="${MAIL_FROM:-ahaojiaqi520@icloud.com}"
TS=$(date '+%Y-%m-%d %H:%M:%S')

# ── 按级别选样式 ──
case "$LEVEL" in
    critical|🔴|red)
        EMOJI="🔴"
        SOUND="Basso"
        ;;
    warn|🟡|yellow)
        EMOJI="🟡"
        SOUND="Glass"
        ;;
    *)
        EMOJI="🟢"
        SOUND="Pop"
        LEVEL="info"
        ;;
esac

FULL_TITLE="${EMOJI} ${TITLE}"

# 构造HTML正文（Apple Mail支持基础HTML）
HTML_BODY=$(cat <<HTMLEOF
<html><body style="font-family: -apple-system, Helvetica, sans-serif; padding: 10px;">
<div style="background: #1a1a2e; border-left: 4px solid #d4a574; padding: 15px; border-radius: 4px;">
  <h3 style="color: #d4a574; margin: 0 0 10px 0;">🐉 ${TITLE}</h3>
  <pre style="color: #e0e0e0; font-size: 13px; line-height: 1.5; white-space: pre-wrap; margin: 0; font-family: -apple-system, monospace;">${BODY}</pre>
  <hr style="border-color: #333; margin: 12px 0;">
  <p style="color: #888; font-size: 11px; margin: 0;">
    龍魂系统 · ${TS} · 级别: ${LEVEL}
  </p>
</div>
</body></html>
HTMLEOF
)

# ── 通过 osascript 用 Apple Mail 发送 ──
osascript -e "
tell application \"Mail\"
  set newMessage to make new outgoing message with properties {subject:\"${FULL_TITLE}\", content:\"$(echo "$HTML_BODY" | sed 's/"/\\"/g')\"}
  tell newMessage
    set visible to false
    set sender to \"${MAIL_FROM}\"
    make new to recipient at end of to recipients with properties {address:\"${MAIL_TO}\"}
  end tell
  send newMessage
end tell
" 2>&1

echo "[MAIL] ${TS} ✅ 已发送: ${FULL_TITLE}" >&2
