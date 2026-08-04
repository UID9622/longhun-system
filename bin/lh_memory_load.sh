#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ═══════════════════════════════════════════════
# 龍魂·记忆加载 (Shell版) — 给没有Python的AI用
# DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-MEMORY-LOAD-SHELL-v1.1-SECURE
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════
# 用法:
#   source bin/lh_memory_load.sh                    # 加载完整记忆
#   source bin/lh_memory_load.sh --identity         # 只身份块
#   source bin/lh_memory_load.sh --raw              # 原始MD全文
#   source bin/lh_memory_load.sh --search "训练"     # 搜索
#
# Token（远程访问自动加载，优先级递减）:
#   1. 环境变量 $LH_MEMORY_TOKEN
#   2. ~/.longhun/.memory_token 文件
#   3. .codebuddy/memory/.api_token 文件
#   🔴 禁止在命令行明文出示 Token
# ═══════════════════════════════════════════════

LH_MEMORY_HOST="${LH_MEMORY_HOST:-127.0.0.1}"
LH_MEMORY_PORT="${LH_MEMORY_PORT:-8771}"
LH_MEMORY_URL="http://${LH_MEMORY_HOST}:${LH_MEMORY_PORT}"

# 🔥 v1.1 Token 静默加载
_lh_load_token() {
    # 1. 环境变量
    [ -n "$LH_MEMORY_TOKEN" ] && echo "$LH_MEMORY_TOKEN" && return 0
    # 2. ~/.longhun/.memory_token
    [ -f "$HOME/.longhun/.memory_token" ] && head -1 "$HOME/.longhun/.memory_token" && return 0
    # 3. 项目内
    local proj_token="$(dirname "$0")/../.codebuddy/memory/.api_token"
    [ -f "$proj_token" ] && head -1 "$proj_token" && return 0
    return 1
}

_lh_curl() {
    local LH_TOKEN
    # 仅远程请求加 Token 头
    case "$LH_MEMORY_HOST" in
        127.0.0.1|localhost|::1) curl -s "$@" 2>/dev/null ;;
        *) LH_TOKEN=$(_lh_load_token)
           if [ -n "$LH_TOKEN" ]; then
               curl -s -H "X-API-Token: $LH_TOKEN" "$@" 2>/dev/null
           else
               echo '{"status":"🔴 未配置 Token，远程访问需要认证"}'
               echo "# 设置方式: export LH_MEMORY_TOKEN=<your_token>"
           fi ;;
    esac
}

_lh_memory_health() {
    _lh_curl "${LH_MEMORY_URL}/v1/memory/health" || echo '{"status":"🔴 记忆API未连接"}'
}

_lh_memory_load() {
    echo "══════════════════════════════════════════════"
    echo "🐉 龍魂统一记忆 · Shell客户端"
    echo "   API: ${LH_MEMORY_URL}"
    echo "══════════════════════════════════════════════"
    _lh_curl "${LH_MEMORY_URL}/v1/memory/raw" | head -200
    echo ""
    echo "══════════════════════════════════════════════"
    echo "🐉 记忆已注入上下文。详细: GET ${LH_MEMORY_URL}/v1/memory"
    echo "══════════════════════════════════════════════"
}

_lh_memory_identity() {
    echo "══════════════════════════════════════════════"
    echo "🔥 龍魂·身份焊死块"
    echo "══════════════════════════════════════════════"
    _lh_curl "${LH_MEMORY_URL}/v1/memory/identity" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for k,v in d.items():
    if k!='raw': print(f'  {k}: {v}')
" 2>/dev/null || _lh_curl "${LH_MEMORY_URL}/v1/memory/identity"
    echo "══════════════════════════════════════════════"
}

_lh_memory_search() {
    local q="$1"
    echo "🔍 搜索: $q"
    _lh_curl "${LH_MEMORY_URL}/v1/memory/search?q=${q}" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print(f\"  找到 {d.get('total_hits',0)} 条\")
for r in d.get('results',[]):
    print(f\"  [{r['section']}] L{r['line_num']}: {r['match_line'][:100]}\")
" 2>/dev/null || _lh_curl "${LH_MEMORY_URL}/v1/memory/search?q=${q}"
    echo ""
}

# 主入口
case "${1:-}" in
    --health|health)
        _lh_memory_health
        ;;
    --identity|identity)
        _lh_memory_identity
        ;;
    --search|search)
        shift
        _lh_memory_search "${1:-}"
        ;;
    --raw|raw)
        _lh_curl "${LH_MEMORY_URL}/v1/memory/raw"
        ;;
    *)
        _lh_memory_load
        ;;
esac
