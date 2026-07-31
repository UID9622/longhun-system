#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════╗
# ║  🐉 龙魂·Git推送通知 v1.0 — 本地Git Hook · 并入库知识矩阵      ║
# ║  Git Push Notify · commit → DNA → audit → store → Bark       ║
# ╠═══════════════════════════════════════════════════════════════╣
# ║  DNA: #龍芯⚡️2026-07-12-BARK-GIT-HOOK-v1.0                  ║
# ║  安装: ln -s executors/bark/git_push_hook.sh .git/hooks/post-push ║
# ╚═══════════════════════════════════════════════════════════════╝

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "$(cd "$(dirname "$0")/../.." && pwd)")
DISPATCHER="${REPO_ROOT}/bin/lh_bark_dispatcher.py"

# ── 获取Git信息 ──
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
COMMIT_HASH=$(git rev-parse HEAD 2>/dev/null || echo "unknown")
COMMIT_SHORT=$(echo "${COMMIT_HASH}" | cut -c1-8)
COMMIT_MSG=$(git log -1 --pretty=%B 2>/dev/null | head -3 || echo "no message")
COMMIT_AUTHOR=$(git log -1 --pretty=%an 2>/dev/null || echo "unknown")
COMMIT_TIME=$(git log -1 --pretty=%ci 2>/dev/null | cut -d' ' -f1-2 || echo "unknown")

# ── 变更文件 ──
CHANGED_FILES=$(git diff --name-status HEAD~1 HEAD 2>/dev/null | head -20 || echo "")
ADDED=$(echo "${CHANGED_FILES}" | grep "^A" | wc -l | xargs)
MODIFIED=$(echo "${CHANGED_FILES}" | grep "^M" | wc -l | xargs)
DELETED=$(echo "${CHANGED_FILES}" | grep "^D" | wc -l | xargs)
ADDED=${ADDED:-0}
MODIFIED=${MODIFIED:-0}
DELETED=${DELETED:-0}

# ── 构造消息 ──
TITLE="📦 Git Push · [${BRANCH}] ${COMMIT_SHORT}"

CONTENT="分支: ${BRANCH}
提交: ${COMMIT_SHORT}
作者: ${COMMIT_AUTHOR}
时间: ${COMMIT_TIME}

提交信息:
${COMMIT_MSG}

变更统计: +${ADDED} ~${MODIFIED} -${DELETED}"

if [ -n "${CHANGED_FILES}" ]; then
    CONTENT="${CONTENT}

变更文件:
${CHANGED_FILES}"
fi

CONTENT="${CONTENT}

仓库: longhun-system
来源: $(hostname)"

# ── 通过调度器走完整管道（DNA→审计→入库→推送）──
if [ -f "${DISPATCHER}" ]; then
    python3 "${DISPATCHER}" \
        --type git \
        --title "${TITLE}" \
        --content "${CONTENT}" \
        --source "Git:$(hostname)" \
        --json 2>&1
else
    echo "⚠️ 调度器未找到: ${DISPATCHER}"
    # fallback: 直接Bark推送
    python3 "${REPO_ROOT}/executors/bark/bark_send.py" "${TITLE}" "${CONTENT}"
fi
