#!/bin/bash
# 龍魂環境加載腳本 · 在 .zshrc 或 .bashrc 中 source 此文件
# DNA: #龍芯⚡️2026-05-20-環境加載-v1.0

# §主倉庫路徑
export LONGHUN_ROOT="${HOME}/longhun-system"

# §命令路徑·加入 PATH
export PATH="${LONGHUN_ROOT}/命令:${PATH}"

# §別名·方便操作
alias lh="cd ${LONGHUN_ROOT}"
alias lhlog="cd ${LONGHUN_ROOT}/日志"
alias lhcmd="cd ${LONGHUN_ROOT}/命令"

# §提示加載成功
echo "🐲 龍魂環境已加載 · UID9622"
