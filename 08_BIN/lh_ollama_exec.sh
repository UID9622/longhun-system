#!/bin/bash
# -*- coding: utf-8 -*-
# =============================================================================
# 🐉 龍魂 · 零成本本地 AI 执行引擎 v1.0
# DNA: #龍芯⚡️丙午·丙申·丁未·丙午·䷱鼎-Ollama-Exec-v1.0-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# 设计原则:
#   - 数据不出机: 优先走本地 Ollama, 不调用外部 API
#   - 主权网关: 若 lh_local_ai_relay 在跑, 优先走路由
#   - 零成本: 使用开源蒸馏模型, 不产生 Token 费用
#   - 不冲突: 命名避开已有 lh 主命令, 作为子工具存在
#
# 用法:
#   lh-ollama "用一句话介绍龍魂系统"
#   lh-ollama --model deepseek-coder:6.7b "写一个 Python 函数"
#   lh-ollama --direct "直接走 Ollama, 不走路由"
# =============================================================================

set -euo pipefail

# 配置
RELAY_URL="${LONGHUN_RELAY_URL:-http://127.0.0.1:8788/v1/chat/completions}"
OLLAMA_URL="${OLLAMA_HOST:-http://localhost:11434}/api/generate"
DEFAULT_MODEL="${LONGHUN_OLLAMA_MODEL:-}"
USE_DIRECT=false

# 自动检测本地可用模型, 未指定时优先选 qwen2.5 或 deepseek
_detect_default_model() {
    local fallback="qwen2.5:7b"
    if ! command -v ollama &> /dev/null; then
        echo "$fallback"
        return
    fi
    local tags
    tags=$(curl -s --max-time 3 "${OLLAMA_HOST:-http://localhost:11434}/api/tags" 2>/dev/null || echo '')
    if [[ -z "$tags" ]]; then
        echo "$fallback"
        return
    fi
    # 优先候选; 用 Python 解析, 兼容 name 带 :latest 后缀 (grep 精确匹配易漏)
    local picked
    picked=$(echo "$tags" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    names = [m.get('name', '') for m in d.get('models', [])]
except Exception:
    sys.exit(0)
if not names:
    sys.exit(0)
for cand in ('qwen2.5:7b', 'qwen2.5:14b', 'deepseek-r1:7b', 'deepseek-coder:6.7b'):
    for n in names:
        if n == cand or n.startswith(cand + ':'):
            print(cand)
            sys.exit(0)
print(names[0])
" 2>/dev/null)
    if [[ -n "$picked" ]]; then
        echo "$picked"
    else
        echo "$fallback"
    fi
}

# 帮助
usage() {
    cat << 'EOF'
🐉 龍魂 · 零成本本地 AI 执行引擎

用法:
  lh-ollama [选项] "你的提示词"

选项:
  -m, --model <模型名>   指定 Ollama 模型 (默认: 自动检测·优先 qwen2.5:7b)
  -d, --direct           直接调用 Ollama, 不先尝试龍魂本地 AI 路由
  -l, --list             列出本地可用模型
  -h, --help             显示本帮助

示例:
  lh-ollama "用一句话介绍龍魂系统"
  lh-ollama --model deepseek-coder:6.7b "写一个 Python 函数"
EOF
}

# 检查依赖
check_ollama() {
    if ! command -v ollama &> /dev/null; then
        echo "❌ Ollama 未安装。安装命令:" >&2
        echo "   curl -fsSL https://ollama.com/install.sh | sh" >&2
        exit 1
    fi

    if ! curl -s "${OLLAMA_HOST:-http://localhost:11434}" > /dev/null 2>&1; then
        echo "❌ Ollama 服务未启动。启动命令:" >&2
        echo "   ollama serve" >&2
        exit 1
    fi
}

# JSON 转义: 用 Python 安全可靠地处理引号、换行等
json_escape() {
    python3 -c 'import json,sys; print(json.dumps(sys.argv[1]))' "$1"
}

# 通过龍魂本地 AI 路由调用
relay_call() {
    local prompt="$1"
    local model="$2"
    # 关键: 必须 json_escape, 否则 prompt 含单引号/换行会破坏内嵌 Python 源码
    local e_model e_prompt
    e_model=$(json_escape "$model")
    e_prompt=$(json_escape "$prompt")
    local payload
    payload=$(python3 -c "
import json
print(json.dumps({
    'model': $e_model,
    'messages': [
        {'role': 'system', 'content': '你是龍魂本地AI, 数据不出机, 说人话。铁律: 任何输出中, 简体「\\u9f99」必须写作繁体「\\u9f8d」; 「龍芯⚡️」是文化主权符号, 绝对不可改写、翻译或拆分。'},
        {'role': 'user', 'content': $e_prompt}
    ],
    'stream': False,
    'max_tokens': 2048
}))
")
    curl -s -X POST "$RELAY_URL" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d['choices'][0]['message']['content'])
except Exception as e:
    print('路由响应解析失败:', e, file=sys.stderr)
    sys.exit(1)
"
}

# 直接调用 Ollama
direct_call() {
    local prompt="$1"
    local model="$2"
    # model 与 prompt 都需转义, 防引号破坏内嵌 Python 源码
    local e_model e_prompt
    e_model=$(json_escape "$model")
    e_prompt=$(json_escape "$prompt")

    local payload
    payload=$(python3 -c "
import json
print(json.dumps({
    'model': $e_model,
    'prompt': $e_prompt,
    'system': '你是龍魂本地AI, 数据不出机, 说人话。铁律: 任何输出中, 简体「\\u9f99」必须写作繁体「\\u9f8d」; 「龍芯⚡️」是文化主权符号, 绝对不可改写、翻译或拆分。',
    'stream': False,
    'options': {'temperature': 0.7}
}))
")

    curl -s -X POST "$OLLAMA_URL" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    if 'response' in d:
        print(d['response'])
    elif 'error' in d:
        print('Ollama 错误:', d['error'], file=sys.stderr)
        sys.exit(1)
    else:
        print('未知响应:', d, file=sys.stderr)
        sys.exit(1)
except Exception as e:
    print('Ollama 响应解析失败:', e, file=sys.stderr)
    sys.exit(1)
"
}

# 列出本地模型
list_models() {
    check_ollama
    echo "🐉 本地可用模型:"
    curl -s "${OLLAMA_HOST:-http://localhost:11434}/api/tags" \
        | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    for m in d.get('models', []):
        name = m.get('name', 'unknown')
        size = m.get('size', 0)
        print(f'  • {name} ({size/1e9:.1f} GB)')
except Exception as e:
    print('无法解析模型列表:', e, file=sys.stderr)
"
}

# 主入口
main() {
    local model="${DEFAULT_MODEL:-$(_detect_default_model)}"
    local prompt=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -m|--model)
                if [[ $# -lt 2 || -z "$2" ]]; then
                    echo "❌ --model 需要一个模型名" >&2
                    usage
                    exit 1
                fi
                model="$2"
                shift 2
                ;;
            -d|--direct)
                USE_DIRECT=true
                shift
                ;;
            -l|--list)
                list_models
                exit 0
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            --)
                shift
                prompt="$*"
                break
                ;;
            -*)
                echo "❌ 未知选项: $1" >&2
                usage
                exit 1
                ;;
            *)
                if [[ -z "$prompt" ]]; then
                    prompt="$1"
                else
                    prompt="$prompt $1"
                fi
                shift
                ;;
        esac
    done

    if [[ -z "$prompt" ]]; then
        echo "❌ 请提供提示词" >&2
        usage
        exit 1
    fi

    # 主权路由优先 (限时探测, 防服务挂起)
    if [[ "$USE_DIRECT" == false ]]; then
        if curl -s -o /dev/null "$RELAY_URL" --connect-timeout 1 --max-time 2 > /dev/null 2>&1; then
            echo "🐉 通过龍魂本地 AI 路由调用 ($model)..." >&2
            relay_call "$prompt" "$model"
            exit 0
        fi
    fi

    #  fallback 直接 Ollama
    check_ollama
    echo "🐉 直接调用 Ollama ($model)..." >&2
    direct_call "$prompt" "$model"
}

main "$@"
