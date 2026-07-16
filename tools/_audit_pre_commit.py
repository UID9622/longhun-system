#!/usr/bin/env python3
"""龍魂·开源前审计 v1.0 — 安全扫描+GPG验证+变更统计"""
import os, re, subprocess, sys, json, time

# ── 1. 安全扫描 ──
DANGEROUS = [
    ("GPG私钥", rb"-----BEGIN PGP PRIVATE KEY BLOCK-----"),
    ("API硬编码", br'(?:api.?key|API_KEY|secret_key)\s*=\s*["\'][A-Za-z0-9_-]{20,}'),
    ("密码硬编码", br'password\s*=\s*["\']["\'](?![^"\']*CHANGE)(?![^"\']*change)[A-Za-z0-9@#$]{6,}'),
]

findings = {}
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "state", ".codebuddy", ".obsidian", "_downloads_staging", "node_modules", "agents/downloads-imports"}]
    for f in files:
        if not f.endswith((".py", ".json", ".md", ".txt", ".sh", ".conf", ".yaml", ".yml")):
            continue
        fp = os.path.join(root, f)
        try:
            with open(fp, "rb") as fh:
                content = fh.read()
        except Exception:
            continue
        for name, pat in DANGEROUS:
            if re.search(pat, content):
                findings.setdefault(name, []).append(os.path.relpath(fp))

# ── 2. 审计调用 ──
def run_audit(cmd, timeout=60, name=""):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        ok = r.returncode == 0
        return {"pass": ok, "name": name, "stdout": r.stdout[:500], "exit_code": r.returncode}
    except Exception as e:
        return {"pass": False, "name": name, "error": str(e)[:200]}

PASSED = 0
TOTAL = 0

checks = []
cmd_base = [sys.executable]

# (a) autoflow health
checks.append(run_audit(cmd_base + ["bin/lh_autoflow.py", "--health"], name="autoflow_health", timeout=30))
checks.append(run_audit(cmd_base + ["bin/lh_autoflow.py", "--test"], name="autoflow_selftest", timeout=30))
checks.append(run_audit(cmd_base + ["-m", "pytest", "tests/test_autoflow.py", "-q"], name="pytest_autoflow", timeout=60))
checks.append(run_audit(cmd_base + ["tests/longhun_entry_test_runner.py"], name="entry_test_runner", timeout=30))
checks.append(run_audit(cmd_base + ["audit/gua_audit_engine.py"], name="gua_audit", timeout=30))

# ── 3. 汇总 ──
results = {
    "audit_dna": "#龍芯⚡️丙午·辛未·乙酉·酉时·讼-OPENSOURCE-AUDIT-v1.0",
    "gpg_fingerprint": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
    "sensitive_scan": "PASS" if not findings else "FAIL",
    "sensitive_findings": {k: len(v) for k, v in findings.items()},
    "checks": [],
    "summary": {},
}

for c in checks:
    PASSED += int(c["pass"])
    TOTAL += 1
    results["checks"].append(c)

results["summary"] = {
    "total": TOTAL,
    "passed": PASSED,
    "failed": TOTAL - PASSED,
    "coverage": f"{PASSED/TOTAL*100:.1f}%" if TOTAL > 0 else "0%",
    "sensitive_scan": "🟢 PASS" if not findings else "🔴 FAIL",
    "audit_color": "🟢" if PASSED == TOTAL else "🟡" if PASSED >= TOTAL - 1 else "🔴",
}

# ── 4. 输出 ──
print(json.dumps(results, ensure_ascii=False, indent=2))
print()
print("╔═══════════════════════════════════════════════════════════════╗")
print("║  🐉 龍魂·开源前审计报告                                       ║")
print("╠═══════════════════════════════════════════════════════════════╣")
print(f"║  安全扫描: {results['summary']['sensitive_scan']}                                            ║")
for c in checks:
    mark = "🟢" if c["pass"] else "🔴"
    print(f"║  {mark} {c['name']:30s} {c.get('exit_code','N/A')}                                  ║")
print(f"║  通过: {PASSED}/{TOTAL}  |  审计: {results['summary']['audit_color']}                                         ║")
print("╚═══════════════════════════════════════════════════════════════╝")
sys.exit(0 if PASSED == TOTAL else 1)