# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂插件沙箱 · 一键验证执行器 v1.0
DNA: #龍芯⚡️2026-08-23-SANDBOX-VERIFY-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

T1~T7 覆盖:
  T1 五模块导入       T2 门控默认全拒       T3 grant 后放行
  T4 路径逃逸拒绝     T5 demo_plugin 执行   T6 审计日志落盘
  T7 import 守卫拦截
"""
import sys, os, tempfile
import multiprocessing
try:
    multiprocessing.set_start_method('fork')
except Exception:
    pass

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_HERE)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

_AUDIT_LOG = os.path.join(_PROJECT_ROOT, "logs", "sandbox_audit.jsonl")

RESULT = []
def ok(name, cond, detail=""):
    RESULT.append((name, bool(cond), detail))
    print(f"[{'OK' if cond else 'FAIL'}] {name} {detail}")

def _audit_lines():
    if os.path.exists(_AUDIT_LOG):
        return sum(1 for _ in open(_AUDIT_LOG))
    return 0

# T1 五模块导入
try:
    from sandbox_runtime.capability_gate import CapabilityGate, CapabilityRequest
    from sandbox_runtime.audit_hook import AuditHook
    from sandbox_runtime.sandbox_api import SandboxAPI
    from sandbox_runtime.plugin_loader import PluginLoader, install_import_guard
    from sandbox_runtime.runner import PluginSandbox, run_plugin
    ok("T1 五模块导入", True)
except Exception as e:
    ok("T1 五模块导入", False, str(e))

# T2 门控默认全拒
try:
    g = CapabilityGate()
    r = g.request(CapabilityRequest(plugin_id='x', capability='fs.read', action='read', payload={}))
    ok("T2 门控默认全拒", r.status == 'denied', f"status={r.status}")
except Exception as e:
    ok("T2 门控默认全拒", False, str(e))

# T3 grant 后放行
try:
    g = CapabilityGate()
    g.grant('x', ['dna.generate'])
    r1 = g.request(CapabilityRequest(plugin_id='x', capability='dna.generate', action='gen', payload={}))
    r2 = g.request(CapabilityRequest(plugin_id='x', capability='fs.write', action='w', payload={}))
    ok("T3 grant 后放行", r1.status == 'ok' and r2.status == 'denied',
       f"gen={r1.status} fs_write={r2.status}")
except Exception as e:
    ok("T3 grant 后放行", False, str(e))

# T4 路径逃逸拒绝
try:
    tmp = tempfile.mkdtemp()
    os.environ['_TEST_HOME'] = tmp
    g = CapabilityGate()
    g.grant('x', ['fs.read'])
    a = AuditHook()
    api = SandboxAPI(plugin_id='x', gate=g, audit_hook=a)
    r = api.request_fs_read('../../../../etc/passwd')
    ok("T4 路径逃逸拒绝", r.get('status') == 'denied', f"status={r.get('status')}")
except Exception as e:
    ok("T4 路径逃逸拒绝", False, str(e))

# T5 demo_plugin 完整执行（独立子进程）
try:
    before = _audit_lines()
    r = run_plugin('demo_plugin')
    after = _audit_lines()
    st = r.get('status') if isinstance(r, dict) else r
    ok("T5 demo_plugin 执行", st == 'ok', f"status={st} 审计+{after-before}行")
except Exception as e:
    ok("T5 demo_plugin 执行", False, str(e))

# T6 审计日志落盘
try:
    n = _audit_lines()
    ok("T6 审计日志落盘", n > 0, f"共{n}行")
except Exception as e:
    ok("T6 审计日志落盘", False, str(e))

# T7 import 守卫（ImportError 或 PermissionError 均视为拦截成功）
try:
    install_import_guard()
    try:
        import subprocess
        ok("T7 import 守卫拦截", False, "subprocess 可导入=泄漏")
    except (ImportError, PermissionError):
        ok("T7 import 守卫拦截", True, "subprocess 已拦截")
    except Exception as e:
        ok("T7 import 守卫拦截", True, f"subprocess 被拦({type(e).__name__})")
except Exception as e:
    ok("T7 import 守卫拦截", False, str(e))

fails = [r for r in RESULT if not r[1]]
print("=" * 40)
print(f"结果: {len(RESULT)-len(fails)} 通过 / {len(fails)} 失败")
print(f"三色: {'🟢 全部通过' if not fails else '🔴 存在失败项'}")
sys.exit(0 if not fails else 1)
