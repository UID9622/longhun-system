#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-TEST-ORCHESTRATOR-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🐉 龍魂 · 测试流程调度器 v1.1
功能: 按依赖顺序执行测试，失败自动重试，生成调度报告

用法:
  python3 tests/test_orchestrator.py
"""

import subprocess
import json
import time
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent

TEST_PHASES = [
    {"name": "代码审计", "cmd": ["-m", "audit", "tests/test_code_audit.py"]},
    {"name": "功能评估", "cmd": ["-m", "functional", "tests/test_functional.py"]},
    {"name": "冒烟测试", "cmd": ["-m", "smoke", "tests/test_smoke.py"]},
    {"name": "自动迭代", "cmd": ["-m", "auto_iteration", "tests/test_auto_iteration.py"]}
]


def run_phase(phase, retry=2):
    """执行测试阶段，支持重试"""
    cmd = [sys.executable, "-m", "pytest", "-v", "-s"] + phase["cmd"]
    for attempt in range(retry):
        print(f"\n🔄 运行 {phase['name']} (尝试 {attempt+1}/{retry})")
        start = time.time()
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            timeout=600
        )
        elapsed = time.time() - start

        if result.returncode == 0:
            return {"passed": True, "output": result.stdout[-2000:], "elapsed": elapsed}
        print(f"⚠️ {phase['name']} 失败，重试中...")

    return {"passed": False, "output": result.stdout[-2000:], "elapsed": elapsed}


def main():
    results = {}
    all_passed = True

    print("""
╔══════════════════════════════════════════════════════════════╗
║  🐉 龍魂 · 测试流程调度器                                    ║
╠══════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-TEST-ORCHESTRATOR-UID9622║
╚══════════════════════════════════════════════════════════════╝
    """)

    for phase in TEST_PHASES:
        result = run_phase(phase)
        results[phase["name"]] = result
        if not result["passed"]:
            all_passed = False

    # 输出汇总
    print("\n" + "=" * 60)
    print("📊 测试汇总")
    print("=" * 60)
    for name, result in results.items():
        status = "✅" if result["passed"] else "❌"
        print(f"  {status} {name} ({result['elapsed']:.2f}s)")

    # 调度报告
    report_path = PROJECT_ROOT / "test_reports" / "orchestrator_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps({
            "dna": "#龍芯⚡️丙午·丙酉·丙寅·申时-TEST-ORCHESTRATOR-UID9622",
            "timestamp": datetime.now().isoformat(),
            "all_passed": all_passed,
            "phases": {k: {"passed": v["passed"], "elapsed": v["elapsed"]} for k, v in results.items()}
        }, indent=2, ensure_ascii=False),
        encoding='utf-8')
    print(f"📄 调度报告: {report_path}")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
