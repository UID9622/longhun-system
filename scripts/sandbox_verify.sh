#!/bin/bash
# 龍魂插件沙箱 · 部署验证 v1.0
# DNA: #龍芯⚡️2026-08-22-SANDBOX-VERIFY-v1.0
# 创建者: 诸葛鑫（UID9622）| 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2
# 用法: bash scripts/sandbox_verify.sh [plugin_id]

cd "$(dirname "$0")/.."
PLUGIN="${1:-demo_plugin}"

echo "🐉 龍魂插件沙箱 · 部署验证"
echo "== 1. 目录结构 =="
for d in sandbox_runtime plugins/$PLUGIN/sandbox plugins/$PLUGIN/logs logs; do
  [ -d "$d" ] && echo "  ✓ $d" || echo "  ✗ 缺失 $d"
done
echo "== 2. 核心模块 =="
for f in sandbox_runtime/capability_gate.py sandbox_runtime/audit_hook.py sandbox_runtime/sandbox_api.py sandbox_runtime/plugin_loader.py sandbox_runtime/runner.py; do
  [ -f "$f" ] && echo "  ✓ $f" || echo "  ✗ 缺失 $f"
done
echo "== 3. 运行插件 ($PLUGIN) =="
python3 -m sandbox_runtime.runner "$PLUGIN"
echo "== 4. 审计日志 =="
tail -5 logs/sandbox_audit.jsonl
echo "== 5. 违规统计 =="
python3 -c "
import sys; sys.path.insert(0, '.')
from sandbox_runtime.audit_hook import AuditHook
h = AuditHook()
print(f'  {PLUGIN} 违规次数(🔴):', h.count_violations('$PLUGIN'))
"
echo "✅ 验证完成"
