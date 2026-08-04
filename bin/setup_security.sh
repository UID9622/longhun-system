#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════╗
# ║  龍魂·安全协议安装脚本                                            ║
# ║  DNA: #龍芯⚡️2026-07-06-SECURITY-SETUP-v1.0                      ║
# ║                                                                      ║
# ║  在新克隆的仓库中执行此脚本来安装安全协议：                          ║
# ║    chmod +x bin/setup_security.sh && bash bin/setup_security.sh      ║
# ║                                                                      ║
# ║  安装内容：                                                          ║
# ║    1. pre-commit hook → 5层密钥/凭证/敏感文件扫描                   ║
# ║    2. pre-push hook → GitHub永久阻断 + 主权令牌控制                ║
# ║    3. 熔断控制器 → 主权人唯一开关（trip/reset/lock）               ║
# ║    4. 初始化熔断状态                                                ║
# ╚══════════════════════════════════════════════════════════════════════╝

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOKS_DIR="${PROJECT_ROOT}/.git/hooks"

echo "🐉 龍魂·安全协议安装"
echo "━━━━━━━━━━━━━━━━━━━━"
echo ""

# 确保 hooks 目录存在
mkdir -p "${HOOKS_DIR}"

# ── 1. 安装 pre-commit 审计防火墙 ──
echo "  [1/4] 安装 pre-commit 审计防火墙..."
cat > "${HOOKS_DIR}/pre-commit" << 'PRECOMMIT_EOF'
#!/bin/bash
# 龍魂 pre-commit 审计防火墙 v2.0
# DNA: #龍芯⚡️2026-07-06-PRECOMMIT-AUDIT-v2.0
# 5层扫描：私钥/凭证/敏感文件/内网IP/大文件

export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/opt/homebrew/bin:$PATH"
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${PROJECT_ROOT}"

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'
VIOLATIONS=0
WARNINGS=0

echo "🐉 pre-commit · 龍魂审计防火墙 v2.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM 2>/dev/null || true)
if [[ -z "${STAGED_FILES}" ]]; then
    echo "🟢 无暂存文件，跳过审计"
    exit 0
fi

# 1. 私钥扫描
echo "  [1/5] 私钥扫描..."
if echo "${STAGED_FILES}" | xargs grep -l --no-messages \
    -e "BEGIN RSA PRIVATE KEY" \
    -e "BEGIN DSA PRIVATE KEY" \
    -e "BEGIN EC PRIVATE KEY" \
    -e "BEGIN OPENSSH PRIVATE KEY" \
    -e "BEGIN PGP PRIVATE KEY" \
    -e "BEGIN GPG PRIVATE KEY" \
    2>/dev/null; then
    echo -e "  ${RED}🔴 发现私钥明文！提交已阻断${NC}"
    VIOLATIONS=$((VIOLATIONS + 1))
fi

# 2. 硬编码凭证扫描
echo "  [2/5] 硬编码凭证扫描..."
CRED_PATTERNS=(
    'api_key\s*=\s*["'"'"'][A-Za-z0-9_\-]{8,}'
    'apiKey\s*[:=]\s*["'"'"'][A-Za-z0-9_\-]{8,}'
    'secret\s*=\s*["'"'"'][A-Za-z0-9_\-]{8,}'
    'password\s*=\s*["'"'"'][^"'"'"'\s]{3,}'
    'token\s*=\s*["'"'"'][A-Za-z0-9_\-\.]{16,}'
    'SECRET_KEY\s*=\s*["'"'"']'
    'ghp_[A-Za-z0-9]{36}'
    'sk-[A-Za-z0-9]{32,}'
    'DATABASE_URL\s*=\s*["'"'"'][^"'"'"']*://[^"'"'"']*@'
)
for pattern in "${CRED_PATTERNS[@]}"; do
    if matched=$(echo "${STAGED_FILES}" | xargs grep -l -E --no-messages "${pattern}" 2>/dev/null || true); then
        if [[ -n "${matched}" ]]; then
            echo -e "  ${RED}🔴 硬编码凭证: ${pattern}${NC}"
            echo "     文件: ${matched}"
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
    fi
done

# 3. 敏感文件检测
echo "  [3/5] 敏感文件检测..."
SENSITIVE_PATTERNS=('\.env$' 'secrets\.env' 'credentials' '\.pem$' '\.key$' 'id_rsa' 'id_ed25519')
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    while IFS= read -r file; do
        if echo "${file}" | grep -q '\.env\.example$'; then continue; fi
        if git check-ignore -q "${file}" 2>/dev/null; then continue; fi
        echo -e "  ${RED}🔴 敏感文件: ${file}${NC}"
        VIOLATIONS=$((VIOLATIONS + 1))
    done < <(echo "${STAGED_FILES}" | grep -E "${pattern}" || true)
done

# 4. 内网IP泄漏
echo "  [4/5] 内网地址泄漏扫描..."
for pattern in '10\.\d{1,3}\.\d{1,3}\.\d{1,3}' '192\.168\.\d{1,3}\.\d{1,3}'; do
    if matched=$(echo "${STAGED_FILES}" | xargs grep -l -E --no-messages "${pattern}" 2>/dev/null | \
        grep -v -E '(\.md$|\.txt$|test_|/test/|/tests/)' || true); then
        if [[ -n "${matched}" ]]; then
            echo -e "  ${YELLOW}🟡 内网IP引用: ${matched}${NC}"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
done

# 5. 大文件检测
echo "  [5/5] 大文件检测..."
while IFS= read -r file; do
    if [[ -f "${file}" ]]; then
        size=$(wc -c < "${file}" 2>/dev/null || echo 0)
        if [[ ${size} -gt 10485760 ]]; then
            echo -e "  ${YELLOW}🟡 大文件 (>10MB): ${file}${NC}"
            WARNINGS=$((WARNINGS + 1))
        fi
    fi
done < <(echo "${STAGED_FILES}")

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [[ ${VIOLATIONS} -gt 0 ]]; then
    echo ""
    echo -e "${RED}🔴 审计失败 · ${VIOLATIONS} 项红线违规 · 提交已阻断${NC}"
    exit 1
fi
if [[ ${WARNINGS} -gt 0 ]]; then
    echo -e "${YELLOW}⚠️  审计通过 · ${WARNINGS} 项警告${NC}"
else
    echo -e "${GREEN}🟢 审计通过${NC}"
fi
echo "🟢 pre-commit 全通，允许提交"
exit 0
PRECOMMIT_EOF
chmod +x "${HOOKS_DIR}/pre-commit"
echo "     ✅ pre-commit hook 已安装"

# ── 2. 安装 pre-push 熔断防火墙 ──
echo "  [2/4] 安装 pre-push 熔断防火墙..."
cat > "${HOOKS_DIR}/pre-push" << 'PREPUSH_EOF'
#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════════╗
# ║  龍魂·熔断防火墙 — Git Pre-Push Hook                              ║
# ║  DNA: #龍芯⚡️2026-07-06-PREPUSH-FIREWALL-v1.0                     ║
# ║  GitHub: 永久阻断 · gitcode/gitee: 主权令牌 · 全局熔断: 全阻断     ║
# ╚══════════════════════════════════════════════════════════════════════╝

export PATH="/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/opt/homebrew/bin:$PATH"
set -euo pipefail

REMOTE_NAME="$1"
REMOTE_URL=""
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FUSE_FILE="${PROJECT_ROOT}/.longhun/fuse_state.json"
CONFIRM_FILE="${PROJECT_ROOT}/.longhun/sovereign_push_confirm.txt"
LOG_DIR="${PROJECT_ROOT}/logs"
AUDIT_LOG="${LOG_DIR}/push_audit.log"

mkdir -p "${LOG_DIR}" 2>/dev/null || true

REMOTE_URL=$(git remote get-url "${REMOTE_NAME}" 2>/dev/null || echo "UNKNOWN")

# 读取熔断状态
FUSE_STATUS="ACTIVE"
if [[ -f "${FUSE_FILE}" ]]; then
    FUSE_STATUS=$(python3 -c "
import json
with open('${FUSE_FILE}') as f:
    d = json.load(f)
print(d.get('status', 'ACTIVE'))
" 2>/dev/null || echo "ACTIVE")
fi

# 全局熔断
if [[ "${FUSE_STATUS}" == "CIRCUIT_TRIPPED" ]]; then
    echo ""
    echo "🔴 龍魂熔断防火墙 · 电路已熔断 · ALL PUSHES BLOCKED"
    echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") | BLOCKED | CIRCUIT_TRIPPED | ${REMOTE_NAME}" >> "${AUDIT_LOG}"
    exit 1
fi

# GitHub 永久阻断
if echo "${REMOTE_URL}" | grep -qi "github\.com"; then
    echo ""
    echo "🔴 龍魂熔断防火墙 · GitHub 永久阻断"
    echo "   Remote: ${REMOTE_NAME} → ${REMOTE_URL}"
    echo "   龍魂系统代码不得上公开平台"
    echo "   连手动发布开源都做不到"
    echo "   黑客就算拿到 SSH Key，也只能黑了寂寞"
    echo ""
    echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") | BLOCKED | GITHUB | ${REMOTE_NAME}" >> "${AUDIT_LOG}"
    exit 1
fi

# gitcode/gitee → 需主权令牌
if echo "${REMOTE_URL}" | grep -qi "gitcode\.com\|gitee\.com"; then
    if [[ ! -f "${CONFIRM_FILE}" ]]; then
        echo ""
        echo "🟡 龍魂主权令牌 · 需确认"
        echo "   执行: python3 bin/fuse_control.py push-confirm"
        echo ""
        echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") | BLOCKED | NO_TOKEN | ${REMOTE_NAME}" >> "${AUDIT_LOG}"
        exit 1
    fi
    
    TOKEN_TIME=$(head -1 "${CONFIRM_FILE}" 2>/dev/null | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z' || echo "1970-01-01T00:00:00Z")
    
    if date --version >/dev/null 2>&1; then
        TOKEN_EPOCH=$(date -u -d "${TOKEN_TIME}" "+%s" 2>/dev/null || echo 0)
        NOW_EPOCH=$(date -u "+%s")
    else
        TOKEN_EPOCH=$(date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "${TOKEN_TIME}" "+%s" 2>/dev/null || echo 0)
        NOW_EPOCH=$(date -u "+%s")
    fi
    
    AGE=$((NOW_EPOCH - TOKEN_EPOCH))
    
    if [[ ${AGE} -gt 300 ]]; then
        echo "🟡 龍魂主权令牌 · 已过期（${AGE}s > 300s）"
        echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") | BLOCKED | TOKEN_EXPIRED | ${AGE}s" >> "${AUDIT_LOG}"
        exit 1
    fi
    
    echo "🟢 熔断防火墙 · 主权令牌有效（${AGE}s）· 放行 ${REMOTE_NAME}"
    echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") | ALLOWED | TOKEN_VALID | ${REMOTE_NAME}" >> "${AUDIT_LOG}"
    exit 0
fi

# 其他远程 → 放行
echo "🟢 熔断防火墙 · ${REMOTE_NAME} 非公开平台 · 放行"
echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") | ALLOWED | LOCAL | ${REMOTE_NAME}" >> "${AUDIT_LOG}"
exit 0
PREPUSH_EOF
chmod +x "${HOOKS_DIR}/pre-push"
echo "     ✅ pre-push hook 已安装"

# ── 3. 初始化熔断状态 ──
echo "  [3/4] 初始化熔断控制..."
mkdir -p "${PROJECT_ROOT}/.longhun"
python3 -c "
import json, os
from datetime import datetime, timezone
fuse_file = '${PROJECT_ROOT}/.longhun/fuse_state.json'
if not os.path.exists(fuse_file):
    state = {
        'status': 'ACTIVE',
        'github_locked': True,
        'trip_count': 0,
        'last_trip': None,
        'last_reset': datetime.now(timezone.utc).isoformat(),
        'sovereign_uid': 'UID9622',
        'sovereign_name': '💎 龍芯北辰·诸葛鑫·Lucky',
        'created': datetime.now(timezone.utc).isoformat(),
        'dna': '#龍芯⚡️2026-07-06-FUSE-CONTROL-v1.0',
    }
    with open(fuse_file, 'w') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    print('     ✅ 熔断状态已初始化（GitHub锁定·ACTIVE）')
else:
    print('     ⓘ  熔断状态已存在，跳过初始化')
"
echo "     ✅ 熔断控制完成"

# ── 4. 验证 ──
echo "  [4/4] 验证安装..."
ERRORS=0
if [[ ! -x "${HOOKS_DIR}/pre-commit" ]]; then echo "     ❌ pre-commit 不可执行"; ERRORS=$((ERRORS+1)); fi
if [[ ! -x "${HOOKS_DIR}/pre-push" ]]; then echo "     ❌ pre-push 不可执行"; ERRORS=$((ERRORS+1)); fi
if [[ ! -f "${PROJECT_ROOT}/bin/fuse_control.py" ]]; then echo "     ❌ fuse_control.py 不存在"; ERRORS=$((ERRORS+1)); fi

if [[ ${ERRORS} -eq 0 ]]; then
    echo "     ✅ 全部验证通过"
else
    echo "     ⚠️  ${ERRORS} 项验证失败"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  🐉 龍魂·安全协议安装完成                                  ║"
echo "╠═══════════════════════════════════════════════════════════╣"
echo "║  🔒 GitHub 推送:     永久阻断                              ║"
echo "║  🔑 gitcode/gitee:   需主权确认令牌                        ║"
echo "║  🔴 全局熔断:        阻断一切                              ║"
echo "║  🛡️  密钥扫描:        提交时自动检测                        ║"
echo "║                                                             ║"
echo "║  主权人命令:                                                ║"
echo "║    python3 bin/fuse_control.py status       查看状态       ║"
echo "║    python3 bin/fuse_control.py trip         全局熔断       ║"
echo "║    python3 bin/fuse_control.py reset        重置熔断       ║"
echo "║    python3 bin/fuse_control.py push-confirm 生成令牌       ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "  DNA: #龍芯⚡️2026-07-06-SECURITY-SETUP-v1.0"
