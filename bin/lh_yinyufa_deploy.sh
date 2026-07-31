# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·隐语法部署脚本 v1.0                                   ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-YIN-YU-FA-DEPLOY-v1.0 ║
# ║  守护人格: 仓颉(P08符号语言) + 鲁班(P04技术执行)            ║
# ║  签章: CANGJIE-YINYUFA-DEPLOY-2026                         ║
# ╚══════════════════════════════════════════════════════════════╝
set -euo pipefail

# ═══ 颜色 ═══
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ═══ 函数 ═══
log_info()  { echo -e "${BLUE}[INFO]${NC}  $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_err()   { echo -e "${RED}[ERR]${NC}   $1"; }

# 获取项目根目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "============================================================"
echo "  龍魂·隐语法部署脚本 v1.0"
echo "  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-YIN-YU-FA-DEPLOY-v1.0"
echo "============================================================"
echo ""

# ═══ 第一步：翻译引擎自检 ═══
log_info "[1/5] 翻译层自检..."
cd "$PROJECT_ROOT"
if python3 engines/lh_translator.py selftest 2>&1; then
    log_ok "翻译层自检通过"
else
    log_err "翻译层自检失败，终止部署"
    exit 1
fi

# ═══ 第二步：命名检查器自检 ═══
log_info "[2/5] 命名检查器自检..."
if python3 bin/lh_naming_checker.py selftest 2>&1; then
    log_ok "命名检查器自检通过"
else
    log_err "命名检查器自检失败，终止部署"
    exit 1
fi

# ═══ 第三步：安装 Git Hook ═══
log_info "[3/5] 安装 Git pre-commit hook..."
HOOK_PATH="$PROJECT_ROOT/.git/hooks/pre-commit"

cat > "$HOOK_PATH" << 'HOOK_EOF'
#!/bin/bash
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·隐语法 pre-commit hook                                ║
# ║  每次提交前自动运行命名检查                                  ║
# ╚══════════════════════════════════════════════════════════════╝

echo ""
echo "============================================================"
echo "  龍魂·隐语法 pre-commit 检查"
echo "============================================================"

# 获取待提交文件（使用 -z 处理含空格/特殊字符文件名）
set --
while IFS= read -r -d '' f; do
    case "$f" in
        *.py|*.md|*.yaml|*.yml|*.json|*.html|*.js|*.sh)
            set -- "$@" "$f"
            ;;
    esac
done < <(git diff --cached --name-only --diff-filter=ACM -z 2>/dev/null || true)

if [ $# -eq 0 ]; then
    echo "  无待提交文件，跳过检查。"
    exit 0
fi

# 运行命名检查
python3 bin/lh_naming_checker.py "$@"

if [ $? -ne 0 ]; then
    echo ""
    echo "============================================================"
    echo "  提交被拒绝！对外文件中出现内部命名。"
    echo "  请使用隐语法翻译层修复后重试。"
    echo "============================================================"
    exit 1
fi

echo "  隐语法检查通过 ✅"
exit 0
HOOK_EOF

chmod +x "$HOOK_PATH"
log_ok "Git pre-commit hook 已安装"

# ═══ 第四步：全量扫描 ═══
log_info "[4/5] 全量隐语法扫描..."
if python3 bin/lh_naming_checker.py --all 2>&1; then
    log_ok "全量扫描通过"
else
    log_warn "全量扫描发现警告（非严重），仅对外文件CRITICAL会阻止提交"
fi

# ═══ 第五步：生成规范索引 ═══
log_info "[5/5] 生成隐语法规范索引..."
cd "$PROJECT_ROOT"

# 验证规范文档存在
if [ -f "01_protocols/LH-CODE-NAMING-STANDARD-v1.0.md" ]; then
    log_ok "隐语法规范文档已就位: 01_protocols/LH-CODE-NAMING-STANDARD-v1.0.md"
else
    log_err "隐语法规范文档缺失！"
    exit 1
fi

echo ""
echo "============================================================"
echo "  部署完成 ✅"
echo "============================================================"
echo ""
echo "  对外：标准英文，严谨正规。"
echo "  对内：拼音代号，玄铁壁垒。"
echo ""
echo "  老外打开核心代码，看到的全是："
echo "    jia_mi, jie_mi, yao_pai_sheng, she_bei_wen..."
echo ""
echo "  他们看不懂，但我们自己人门清。"
echo "  这就是「外正经，内玄铁」。"
echo ""
echo "  落地清单："
echo "    📄 规范文档:   01_protocols/LH-CODE-NAMING-STANDARD-v1.0.md"
echo "    🔧 翻译引擎:   engines/lh_translator.py"
echo "    🔍 命名检查器: bin/lh_naming_checker.py"
echo "    🪝 Git Hook:   .git/hooks/pre-commit"
echo ""
