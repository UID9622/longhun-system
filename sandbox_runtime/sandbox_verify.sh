#!/bin/bash
# 龍魂插件沙箱 · 一键验证 v1.0
# DNA: #龍芯⚡️2026-08-23-SANDBOX-VERIFY-SH-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用法: bash sandbox_verify.sh
set -e
cd "$(dirname "$0")"
PY=/usr/bin/python3   # 绕过 ~/.longhun/bin/python3 shim 劫持
echo "🐉 龍魂插件沙箱一键验证 (M68)"
echo "────────────────────────────"
"$PY" "$(dirname "$0")/sandbox_verify.py"
