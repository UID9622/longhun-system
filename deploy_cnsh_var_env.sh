#!/bin/bash
# 🐉 CNSH 通用符号变量环境 · 一键部署 v1.2
# DNA: #龍芯⚡️2026-08-31-CNSH-DEPLOY-v1.2-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# v1.2: 兼容 DeepSeek 参考版 API（CNSSHLexer 别名·eval_expr·OP_MAP）·lh cnsh-var 入口

set -e

echo "🐉 CNSH 通用符号变量环境 · 集成部署 v1.2"
echo "确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

LONGHUN_ROOT=~/longhun-system
CNSH_BIN=$LONGHUN_ROOT/08_BIN/cnsh

# ── 1. 创建目录 ────────────────────────────────
echo "[1/5] 创建目录结构..."
mkdir -p $CNSH_BIN
mkdir -p $LONGHUN_ROOT/13_TESTS
mkdir -p $LONGHUN_ROOT/20_CONFIG

# ── 2. 生成 __init__.py（若缺失） ──────────────
echo "[2/5] 检查模块入口..."
if [ ! -f "$CNSH_BIN/__init__.py" ]; then
    cat > $CNSH_BIN/__init__.py << 'PYEOF'
# 🐉 CNSH 模块入口
# DNA: #龍芯⚡️2026-08-31-CNSH-INIT-v1.3-UID9622
from .lexer import CNSHLexer, CNSSHLexer, CNSHToken
from .var_env import CNSHVarEnv
from .interpreter import CNSHInterpreter
from .dna_verify import verify_dna_header, verify_dna_file, batch_verify

__version__ = '1.3'
__dna__ = '#龍芯⚡️2026-08-31-CNSH-INIT-v1.3-UID9622'
__all__ = ['CNSHLexer', 'CNSSHLexer', 'CNSHVarEnv', 'CNSHInterpreter',
           'verify_dna_header', 'verify_dna_file', 'batch_verify']
PYEOF
    echo "  ✅ 已生成 __init__.py"
else
    echo "  ℹ️  已存在: __init__.py（跳过）"
fi

# ── 3. 注入系统环境变量 ────────────────────────
echo "[3/5] 注入系统环境变量..."
PROFILE_SNIPPET='\n# 🐉 龍魂 CNSH 环境变量\nexport CNSH_ENV_ALLOW_SYMBOLS=true\nexport CNSH_STRICT_DNA=true\nexport CNSH_UID=UID9622\nexport CNSH_GPG=A2D0092CEE2E5BA87035600924C3704A8CC26D5F\nexport LONGHUN_ROOT=~/longhun-system\nexport PYTHONPATH="$LONGHUN_ROOT/08_BIN:$PYTHONPATH"'

for PROFILE in ~/.zshrc ~/.bashrc ~/.bash_profile; do
    if [ -f "$PROFILE" ]; then
        if ! grep -q 'CNSH_ENV_ALLOW_SYMBOLS' "$PROFILE"; then
            echo -e "$PROFILE_SNIPPET" >> "$PROFILE"
            echo "  ✅ 已注入: $PROFILE"
        else
            echo "  ℹ️  已存在: $PROFILE（跳过）"
        fi
    fi
done

# ── 4. 生成配置文件（若缺失） ──────────────────
echo "[4/5] 检查配置文件..."
if [ ! -f "$LONGHUN_ROOT/20_CONFIG/cnsh_config.yaml" ]; then
    cat > $LONGHUN_ROOT/20_CONFIG/cnsh_config.yaml << 'YAMLEOF'
cnsh:
  variables:
    allow_any_symbols: true
    allow_chinese_operators: true
    long_form_delimiter: "${...}"
    scope_stack: true
  comments:
    line: "//"
    block_start: "/*"
    block_end: "*/"
  dna:
    strict_mode: true
    gpg_fingerprint: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    check_header_lines: 30
    on_fail: reject
  debug: false
YAMLEOF
    echo "  ✅ 已生成 cnsh_config.yaml"
else
    echo "  ℹ️  已存在: cnsh_config.yaml（跳过）"
fi

# ── 5. 验证 ────────────────────────────────────
echo "[5/5] 运行验证测试..."
cd $LONGHUN_ROOT
python3 - << 'PYEOF'
import sys
sys.path.insert(0, '08_BIN')
from cnsh import CNSHLexer, CNSSHLexer, CNSHVarEnv, CNSHInterpreter, verify_dna_header

# 测试1: 词法分析（含 DeepSeek 参考版三S别名）
lex = CNSHLexer('$#var = 100')
toks = lex.tokenize()
var_names = [t.value for t in toks if t.type == 'VAR']
assert '#var' in var_names, '词法分析失败'
assert CNSSHLexer is CNSHLexer, 'CNSSHLexer 别名兼容失败'
print('✅ 词法分析通过（含 CNSSHLexer 别名）')

# 测试2: 变量环境
interp = CNSHInterpreter({'strict_dna': False})
interp.execute('$#var = 100')
assert interp.env.get_var('#var') == 100
print('✅ 变量环境通过')

# 测试3: 中文运算符
interp.execute('$a = 10\n$b = 5\n$c = $a 加 $b')
assert interp.env.get_var('c') == 15
print('✅ 中文运算符通过')

# 测试3b: 参考版 eval_expr 兼容 API
val, _ = interp.env.eval_expr([('NUMBER', '10'), ('PLUS', '加'), ('NUMBER', '5')])
assert val == 15, 'eval_expr 兼容失败'
assert '加' in CNSHVarEnv.OP_MAP, 'OP_MAP 兼容失败'
print('✅ eval_expr/OP_MAP 兼容通过')

# 测试4: DNA验证
assert verify_dna_header('// #龍芯⚡️2026-08-31-TEST-v1.0-UID9622')
assert not verify_dna_header('// #龙芯⚡️2026-08-31-TEST-v1.0-UID9622')  # 简体不合法
print('✅ DNA签名校验通过')

print('🎉 全部测试通过！CNSH 环境已就绪。')
PYEOF

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 部署完成"
echo ""
echo "运行测试:    python3 $LONGHUN_ROOT/13_TESTS/test_cnsh_var_env.py"
echo "交互模式:    python3 $LONGHUN_ROOT/08_BIN/cnsh/interpreter.py"
echo "DNA批量验证: python3 $LONGHUN_ROOT/08_BIN/cnsh/dna_verify.py $LONGHUN_ROOT --suffix .py"
echo "主系统入口:  lh cnsh-var run <文件.cnsh>   (已集成到 lh 主命令)"
echo ""
echo "DNA:   #龍芯⚡️2026-08-31-CNSH-DEPLOY-v1.2-UID9622"
echo "三色:  🟢 全部通过 · 🟡 0 · 🔴 0"
