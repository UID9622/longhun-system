# 龍魂终端片段 · 真源（U+9F8D「龍」· 勿写成 U+9FB2/U+9F90）
# 用法: source ~/longhun-system/加载环境.sh
#   或: source ~/longhun-system/bin/zshrc_龍魂片段.sh
# 错字兼容: zshrc_龐魂片段.sh / zshrc_龍魂片段.sh 已软链到本文件

# >>> LONGHUN_ALIASES_BEGIN
[ -f "$HOME/longhun-system/bin/sovereignty_init.sh" ] && source "$HOME/longhun-system/bin/sovereignty_init.sh"
# 代码仓固定 ~/longhun-system（勿用 iCloud 龍魂主权库 当 bin 根）
export LONGHUN_REPO="$HOME/longhun-system"
export LONGHUN_ROOT="$LONGHUN_REPO"
export LONGHUN_DATA_ROOT="${LONGHUN_DATA_ROOT:-$HOME/Library/Mobile Documents/com~apple~CloudDocs/龍魂主权库}"
export PATH="$LONGHUN_ROOT/venv/bin:$LONGHUN_ROOT/bin:$PATH"
[ -f "$HOME/.longhun/secrets.env" ] && source "$HOME/.longhun/secrets.env"
[ -f "$LONGHUN_ROOT/engine/.env" ] && source "$LONGHUN_ROOT/engine/.env"
setopt INTERACTIVE_COMMENTS 2>/dev/null || true

alias 龍魂技能="bash \"$LONGHUN_ROOT/bin/龍魂技能.sh\""
alias 龐魂技能="bash \"$LONGHUN_ROOT/bin/龍魂技能.sh\""
alias Notion算力="bash \"$LONGHUN_ROOT/bin/Notion算力.sh\""
alias 显示dna="bash \"$LONGHUN_ROOT/bin/显示dna\""
alias 全检="bash \"$LONGHUN_ROOT/bin/主场全链路自检.sh\" --fix"
alias 指令="bash \"$LONGHUN_ROOT/bin/显示常用指令\""
alias 帮助="bash \"$LONGHUN_ROOT/bin/显示常用指令\""
alias api检测="bash \"$LONGHUN_ROOT/bin/api_check.sh\" --fix"

alias 开='bash "$LONGHUN_ROOT/bin/开龍魂9625"'
alias 收='bash "$LONGHUN_ROOT/bin/收龍魂" 2>/dev/null || true'
alias 全开='bash "$LONGHUN_ROOT/bin/爸爸一键全开.sh"'
alias 全收='bash "$LONGHUN_ROOT/bin/全日收工" 2>/dev/null || true'
alias 状态='bash "$LONGHUN_ROOT/bin/龍魂状态" 2>/dev/null || true'
alias 开机='bash "$LONGHUN_ROOT/bin/本机开机.sh"'
alias 开机全='bash "$LONGHUN_ROOT/bin/开机一条龙" 2>/dev/null || true'
alias 收工='bash "$LONGHUN_ROOT/bin/收工一条龙" 2>/dev/null || true'
alias lh-start='bash "$LONGHUN_ROOT/bin/爸爸一键全开.sh"'
alias lh-sync='bash "$LONGHUN_ROOT/bin/同步花名册" 2>/dev/null || true'
alias 同步花名册='bash "$LONGHUN_ROOT/bin/同步花名册" 2>/dev/null || true'

if [[ -f "$HOME/.longhun/显示指令.flag" ]]; then
  bash "$LONGHUN_ROOT/bin/显示常用指令"
  rm -f "$HOME/.longhun/显示指令.flag"
fi
# <<< LONGHUN_ALIASES_END
