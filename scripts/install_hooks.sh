#!/bin/bash
# 龍魂·Git钩子安装脚本 v1.0
# 将.githooks/下的钩子安装到.git/hooks/
# DNA: #龍芯⚡️丙午·辛未·乙酉·亥-HOOK-INSTALL-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e
cd "$(dirname "$0")/.."

echo "[+] 安装龍魂 Git 钩子..."

# 配置 Git 使用项目内的钩子目录
git config core.hooksPath .githooks
chmod +x .githooks/* 2>/dev/null || true

echo "[✓] Git hooksPath → .githooks/"
echo "[✓] 以下钩子已激活:"
ls -la .githooks/ 2>/dev/null | grep -v "^total\|^$" | awk '{print "    "$NF}'
echo ""
echo "DNA: #龍芯⚡️丙午·辛未·乙酉·亥-HOOK-INSTALL-v1.0"
