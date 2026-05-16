# 龍魂终端片段 · source ~/longhun-system/bin/zshrc_龍魂片段.sh
# 别名真源维护: bin/常用指令_真源.txt · 改别名跑 bin/同步指令别名.sh

# >>> LONGHUN_ALIASES_BEGIN（由 bin/同步指令别名.sh 生成 · 勿手改）
export PATH="$HOME/longhun-system/bin:$PATH"
[ -f "$HOME/longhun-system/.env" ] && source "$HOME/longhun-system/.env"
setopt INTERACTIVE_COMMENTS 2>/dev/null || true

alias 开='~/longhun-system/bin/开龙魂'
alias 收='~/longhun-system/bin/收龙魂'
alias 全开='bash ~/longhun-system/bin/全日开机'
alias 全收='bash ~/longhun-system/bin/全日收工'
alias 状态='bash ~/longhun-system/bin/龍魂状态'
alias 指令='bash ~/longhun-system/bin/显示常用指令'
alias 帮助='bash ~/longhun-system/bin/显示常用指令'
alias 开机='bash ~/longhun-system/bin/开机一条龙'
alias 收工='bash ~/longhun-system/bin/收工一条龙'
alias lh-start='bash ~/longhun-system/bin/启动所有服务.sh'
alias lh-sync='bash ~/longhun-system/bin/一键同步.sh'
alias 同步花名册='bash ~/longhun-system/bin/同步花名册'

# 开机一条龙后下一次 source ~/.zshrc 会再印一遍常用指令
if [[ -f "$HOME/.longhun/显示指令.flag" ]]; then
  bash "$HOME/longhun-system/bin/显示常用指令"
  rm -f "$HOME/.longhun/显示指令.flag"
fi
# <<< LONGHUN_ALIASES_END
