#!/bin/bash
# 龍魂插件沙箱 · 部署验证 v1.1
# DNA: #龍芯⚡️2026-08-22-SANDBOX-VERIFY-v1.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）| 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2
# 用法: bash scripts/sandbox_verify.sh [plugin_id]
# v1.1: 增加安全断言（越权必须 denied，任一项失败脚本退出非 0）

cd "$(dirname "$0")/.."
PLUGIN="${1:-demo_plugin}"
FAILED=0

echo "🐉 龍魂插件沙箱 · 部署验证"
echo "== 1. 目录结构 =="
for d in sandbox_runtime plugins/$PLUGIN/sandbox plugins/$PLUGIN/logs logs; do
  [ -d "$d" ] && echo "  ✓ $d" || { echo "  ✗ 缺失 $d"; FAILED=1; }
done
echo "== 2. 核心模块 =="
for f in sandbox_runtime/capability_gate.py sandbox_runtime/audit_hook.py sandbox_runtime/sandbox_api.py sandbox_runtime/plugin_loader.py sandbox_runtime/runner.py; do
  [ -f "$f" ] && echo "  ✓ $f" || { echo "  ✗ 缺失 $f"; FAILED=1; }
done
echo "== 3. 运行插件 ($PLUGIN) =="
OUT=$(python3 -m sandbox_runtime.runner "$PLUGIN" 2>&1)
echo "$OUT"

echo "== 4. 安全断言 =="
# 越权读沙箱外必须 denied
if echo "$OUT" | grep -q "越权读沙箱外.*denied"; then
  echo "  ✓ 路径越权被拒"
else
  echo "  ✗ 路径越权未被拒（严重）"; FAILED=1
fi
# 未授权能力必须 denied
if echo "$OUT" | grep -q "违规请求.*denied"; then
  echo "  ✓ 未授权能力被拒"
else
  echo "  ✗ 未授权能力未被拒（严重）"; FAILED=1
fi
# DNA 必须真生成（干支卦格式 #龍芯⚡️）
if echo "$OUT" | grep -q "生成 DNA.*#龍芯⚡️"; then
  echo "  ✓ DNA 真生成"
else
  echo "  ✗ DNA 未真生成（假成功）"; FAILED=1
fi
# MEMORY 必须真写入
if echo "$OUT" | grep -q "MEMORY 写入.*已写入"; then
  echo "  ✓ MEMORY 真写入"
else
  echo "  ✗ MEMORY 未真写入（假成功）"; FAILED=1
fi

echo "== 5. 审计日志 =="
tail -8 logs/sandbox_audit.jsonl
echo "== 6. 违规统计 =="
python3 -c "
import sys; sys.path.insert(0, '.')
from sandbox_runtime.audit_hook import AuditHook
h = AuditHook()
print(f'  $PLUGIN 违规次数(🔴):', h.count_violations('$PLUGIN'))
"

if [ $FAILED -eq 0 ]; then
  echo "✅ 验证通过 · 三色: 🟢"
else
  echo "❌ 验证失败 · 三色: 🔴"
  exit 1
fi
