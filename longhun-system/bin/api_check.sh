#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 龍魂API联动检测脚本
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
# Licensed under the Apache License, Version 2.0
#
# 作者：UID9622 诸葛鑫（龍芯北辰）
# 创作地：中华人民共和国
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导：曾仕强老师（永恒显示）
# DNA追溯码：#龍芯⚡️2026-03-10-API-CHECK-v1.3
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 共建致谢：Claude (Anthropic PBC) · Notion
#
# 献礼：新中国成立77周年（1949-2026）· 丙午马年
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#
# 用法: ~/longhun-system/bin/api_check.sh
# 或用于 /api-check 技能自动调用

# 读取 Notion Token（从 .env 文件）
ENV_FILE="$HOME/longhun-system/.env"
if [ -f "$ENV_FILE" ]; then
    NOTION_TOKEN=$(grep "NOTION_TOKEN" "$ENV_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'")
fi

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  🐉 龍魂API联动检测 v1.3                  ║"
echo "║  DNA: #龍芯⚡️2026-03-10-API-CHECK-v1.3   ║"
echo "╚══════════════════════════════════════════╝"
echo ""

PASS=0
FAIL=0
WARN=0

# ── 1. Notion API ─────────────────────────────────
echo "[1/5] 检测 Notion API..."
if [ -n "$NOTION_TOKEN" ]; then
    RESULT=$(curl -sf --max-time 5 https://api.notion.com/v1/users/me \
        -H "Authorization: Bearer $NOTION_TOKEN" \
        -H "Notion-Version: 2022-06-28" 2>/dev/null)
    NAME=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('name','unknown'))" 2>/dev/null)
    if [ -n "$NAME" ] && [ "$NAME" != "unknown" ]; then
        echo "  🟢 Notion API 正常 → 用户: $NAME"
        PASS=$((PASS+1))
    else
        echo "  🔴 Notion API 失败 → 检查Token是否有效"
        FAIL=$((FAIL+1))
    fi
else
    echo "  🟡 Notion Token 未配置 → 在 ~/longhun-system/.env 填入 NOTION_TOKEN"
    WARN=$((WARN+1))
fi

# ── 2. Ollama 本地 ────────────────────────────────
echo "[2/5] 检测 Ollama 本地服务..."
OLLAMA_RESULT=$(curl -sf --max-time 3 http://localhost:11434/api/tags 2>/dev/null)
if [ $? -eq 0 ] && [ -n "$OLLAMA_RESULT" ]; then
    MODEL_COUNT=$(echo "$OLLAMA_RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('models',[])))" 2>/dev/null || echo "?")
    echo "  🟢 Ollama 正常 → 已加载模型数: $MODEL_COUNT"
    PASS=$((PASS+1))
else
    echo "  🔴 Ollama 未启动 → 修复: ollama serve"
    FAIL=$((FAIL+1))
fi

# ── 3. MCP-mini Flask ─────────────────────────────
echo "[3/5] 检测 MCP-mini Flask (localhost:8787)..."
MCP_RESULT=$(curl -sf --max-time 3 http://localhost:8787/ 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "  🟢 MCP-mini 正常 → localhost:8787"
    PASS=$((PASS+1))
else
    echo "  🔴 MCP-mini 未启动 → 修复: cd ~/longhun-system && python3 app.py"
    FAIL=$((FAIL+1))
fi

# ── 4. GitHub API ─────────────────────────────────
echo "[4/5] 检测 GitHub API..."
GITHUB_TOKEN=$(grep "GITHUB_TOKEN\|GH_TOKEN" "$ENV_FILE" 2>/dev/null | head -1 | cut -d'=' -f2 | tr -d '"' | tr -d "'")
if [ -n "$GITHUB_TOKEN" ]; then
    GH_USER=$(curl -sf --max-time 5 https://api.github.com/user \
        -H "Authorization: token $GITHUB_TOKEN" 2>/dev/null | \
        python3 -c "import sys,json; print(json.load(sys.stdin).get('login','fail'))" 2>/dev/null)
    if [ -n "$GH_USER" ] && [ "$GH_USER" != "fail" ]; then
        echo "  🟢 GitHub API 正常 → 用户: $GH_USER"
        PASS=$((PASS+1))
    else
        echo "  🔴 GitHub API 失败 → Token无效或过期"
        FAIL=$((FAIL+1))
    fi
else
    echo "  🟡 GitHub Token 未配置 → 在 .env 填入 GITHUB_TOKEN"
    WARN=$((WARN+1))
fi

# ── 5. Gitee API ──────────────────────────────────
echo "[5/5] 检测 Gitee API..."
GITEE_TOKEN=$(grep "GITEE_TOKEN" "$ENV_FILE" 2>/dev/null | cut -d'=' -f2 | tr -d '"' | tr -d "'")
if [ -n "$GITEE_TOKEN" ]; then
    GITEE_USER=$(curl -sf --max-time 5 "https://gitee.com/api/v5/user?access_token=$GITEE_TOKEN" 2>/dev/null | \
        python3 -c "import sys,json; print(json.load(sys.stdin).get('login','fail'))" 2>/dev/null)
    if [ -n "$GITEE_USER" ] && [ "$GITEE_USER" != "fail" ]; then
        echo "  🟢 Gitee API 正常 → 用户: $GITEE_USER"
        PASS=$((PASS+1))
    else
        echo "  🔴 Gitee API 失败 → Token无效或过期"
        FAIL=$((FAIL+1))
    fi
else
    echo "  🟡 Gitee Token 未配置 → 在 .env 填入 GITEE_TOKEN"
    WARN=$((WARN+1))
fi

# ── 汇总 ──────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════╗"
if [ $FAIL -eq 0 ] && [ $WARN -eq 0 ]; then
    echo "║  🟢 所有API正常  PASS=$PASS              ║"
elif [ $FAIL -eq 0 ]; then
    echo "║  🟡 部分未配置  PASS=$PASS WARN=$WARN    ║"
else
    echo "║  🔴 有API故障  PASS=$PASS FAIL=$FAIL WARN=$WARN  ║"
fi
echo "║  DNA: #龍芯⚡️2026-03-10-API-CHECK-v1.3  ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# 降级策略提示
if [ $FAIL -gt 0 ]; then
    echo "⚡ 降级策略："
    echo "  Ollama 🔴 → 切换在线Claude，标记「未本地化」"
    echo "  MCP-mini 🔴 → 简化模式运行，不调用人格调度"
    echo "  GitHub/Gitee 🔴 → 本地暂存，补配置后发布"
fi
