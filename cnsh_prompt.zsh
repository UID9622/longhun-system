# ==========================================================
# CNSH ZSH 提示符
# VERSION: v2.0.0
# ==========================================================

# 引入环境变量
source ~/longhun-system/cnsh_env.sh

# 动态标题（含卦象）
precmd() {
    local CURRENT_PATH=${PWD/#$HOME/~}
    local SHORT_PATH=$(echo $CURRENT_PATH | awk -F/ '{OFS="·"; n=NF; if(n>3) print $(n-2),$(n-1),$n; else print $0}')

    local HOUR=$(date +%H)
    local GUA_SYMBOL

    case $HOUR in
        23|00|01) GUA_SYMBOL="☷" ;;
        02|03|04) GUA_SYMBOL="☳" ;;
        05|06|07) GUA_SYMBOL="☲" ;;
        08|09|10) GUA_SYMBOL="☴" ;;
        11|12|13) GUA_SYMBOL="☰" ;;
        14|15|16) GUA_SYMBOL="☵" ;;
        17|18|19) GUA_SYMBOL="☶" ;;
        20|21|22) GUA_SYMBOL="☱" ;;
        *) GUA_SYMBOL="$CNSH_SYMBOL_TAIJI" ;;
    esac

    echo -ne "\e]0;${CNSH_SYMBOL_DRAGON} ${SHORT_PATH} ${GUA_SYMBOL} ${CNSH_AUDIT_STATUS}\a"
}

# 提示符
PROMPT="%F{red}${CNSH_SYMBOL_DRAGON}%f %F{cyan}%~%f ${CNSH_SYMBOL_TAIJI} ${CNSH_AUDIT_STATUS} %# "
