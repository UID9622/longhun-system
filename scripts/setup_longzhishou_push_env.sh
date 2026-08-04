#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# 龍智守飞书推送环境本地终端执行方案
# DNA: #龍芯⚡️2026-07-01-LONGZHISHOU-PUSH-SETUP-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# 用途：在本地终端一键检查/初始化龍智守飞书推送配置，并（可选）发送验证消息。
# 设计原则：
#   1. 真实配置与代码分离：敏感值只存在 ~/.longhun/config/ 或环境变量。
#   2. 默认 dry-run：不加 --run 不会真正发消息。
#   3. 扫描敏感信息时只列文件、不打印密钥本身。

set -euo pipefail

HOME_DIR="${HOME}"
CONFIG_DIR="${HOME_DIR}/.longhun/config"
CONFIG_FILE="${CONFIG_DIR}/龍智守_config.json"
CONFIG_EXAMPLE="${CONFIG_DIR}/龍智守_config.example.json"
SCRIPT_FILE="${HOME_DIR}/Downloads/龍智守_本地控制接口_v2.0.py"
SCAN_DIR="${HOME_DIR}/Downloads"

DRY_RUN=true
RUN_TEST=false
SHOW_HELP=false

usage() {
    cat <<EOF
用法: $0 [选项]

选项:
  --run        真正执行配置初始化和发送测试消息（默认 dry-run）
  --test       发送一条测试消息（需配合 --run）
  -h, --help   显示本帮助

示例:
  $0                           # 检查配置， dry-run
  $0 --run --test              # 初始化并发送测试消息
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --run) DRY_RUN=false ;;
        --test) RUN_TEST=true ;;
        -h|--help) SHOW_HELP=true ;;
        *) echo "🟡 未知参数: $1"; usage; exit 1 ;;
    esac
    shift
done

if $SHOW_HELP; then
    usage
    exit 0
fi

say() { echo "[龍智守] $*"; }
dna() { echo "#龍芯⚡️$(date -u +%Y%m%d%H%M%S%N | cut -c1-20)-$1-$(openssl rand -hex 4 2>/dev/null || head -c4 /dev/urandom | xxd -p)"; }

say "启动本地终端执行方案 | DNA: $(dna LONGZHISHOU-PUSH-SETUP)"
say "模式: $([ "$DRY_RUN" = false ] && echo "真实执行" || echo "干跑检查")"

# 1. 检查核心文件
say "检查核心文件..."
if [[ ! -f "$SCRIPT_FILE" ]]; then
    echo "🔴 未找到龍智守脚本: $SCRIPT_FILE"
    exit 1
fi
say "🟢 龍智守脚本已找到: $SCRIPT_FILE"

if [[ ! -f "$CONFIG_EXAMPLE" ]]; then
    echo "🟡 未找到配置模板: $CONFIG_EXAMPLE"
else
    say "🟢 配置模板已找到"
fi

# 2. 初始化配置文件（dry-run 时仅提示）
if [[ ! -f "$CONFIG_FILE" ]]; then
    if $DRY_RUN; then
        say "🟡 配置文件缺失: $CONFIG_FILE"
        say "    干跑模式下不会创建。请运行 '$0 --run' 从模板复制，或手动："
        say "    cp $CONFIG_EXAMPLE $CONFIG_FILE"
        say "    然后填入你的 Webhook 地址和密钥。"
    else
        mkdir -p "$CONFIG_DIR"
        cp "$CONFIG_EXAMPLE" "$CONFIG_FILE"
        say "🟢 已创建配置文件: $CONFIG_FILE"
        say "    请编辑该文件，把 YOUR_FEISHU_WEBHOOK_URL / YOUR_FEISHU_WEBHOOK_SECRET 替换成真实值。"
    fi
else
    say "🟢 配置文件已存在: $CONFIG_FILE"
fi

# 3. 检查环境变量或配置中的占位符
say "检查环境变量..."
if [[ -n "${FEISHU_WEBHOOK_URL:-}" && -n "${FEISHU_WEBHOOK_SECRET:-}" ]]; then
    say "🟢 环境变量 FEISHU_WEBHOOK_URL / FEISHU_WEBHOOK_SECRET 已设置"
else
    say "🟡 环境变量未设置，将依赖配置文件（可能会被脚本内的默认值覆盖，请检查）"
fi

# 4. 扫描硬编码秘密（只列文件路径，不打印内容；限定常见代码/配置类型）
say "扫描硬编码敏感信息（仅列文件，不打印密钥）..."
FOUND=0
if command -v grep >/dev/null 2>&1; then
    while IFS= read -r f; do
        [[ -z "$f" ]] && continue
        say "    发现潜在敏感文件: $f"
        FOUND=$((FOUND + 1))
    done < <(grep -R -l --include="*.py" --include="*.json" --include="*.sh" --include="*.md" \
        "open\.feishu\.cn" "$SCAN_DIR" 2>/dev/null | head -20 || true)
    while IFS= read -r f; do
        [[ -z "$f" ]] && continue
        say "    发现潜在密钥文件: $f"
        FOUND=$((FOUND + 1))
    done < <(grep -R -l --include="*.py" --include="*.json" --include="*.sh" --include="*.md" \
        "open-apis/bot/v2/hook/" "$SCAN_DIR" 2>/dev/null | head -20 || true)
fi
if [[ $FOUND -eq 0 ]]; then
    say "🟢 未发现明显硬编码飞书链接文件（或目录不可读）"
else
    say "🟡 发现 $FOUND 个文件可能包含硬编码敏感信息，请检查并外置到配置"
fi

# 5. 发送测试消息（dry-run 时仅打印命令）
if $RUN_TEST; then
    if $DRY_RUN; then
        say "🟡 干跑模式：以下命令不会真正执行"
        say "    python3 $SCRIPT_FILE 发送测试消息 \"🐉 龍智守环境验证\""
    else
        say "🟢 正在发送测试消息..."
        python3 "$SCRIPT_FILE" 发送测试消息 "🐉 龍智守环境验证"
    fi
else
    say "🟡 未请求发送测试消息。如需发送，请加 --run --test"
fi

say "本地终端执行方案完成。"
say "下一步建议："
say "  1. 编辑 $CONFIG_FILE 填入真实 Webhook 与密钥"
say "  2. 运行 '$0 --run --test' 验证推送"
say "  3. 开源前确保已移除所有硬编码 URL/密钥"
