#!/bin/bash
# 龍魂环境加载脚本 · 在 .zshrc 或 .bashrc 中 source 此文件
# DNA: #龍芯⚡️2026-05-20-环境加载-v1.0

# §主仓库路径
export LONGHUN_ROOT="${HOME}/longhun-system"

# §命令路径·加入 PATH
export PATH="${LONGHUN_ROOT}/命令:${PATH}"

# §别名·方便操作
alias lh="cd ${LONGHUN_ROOT}"
alias lhlog="cd ${LONGHUN_ROOT}/日志"
alias lhcmd="cd ${LONGHUN_ROOT}/命令"

# §提示加载成功
echo "🐲 龍魂环境已加载 · UID9622"
