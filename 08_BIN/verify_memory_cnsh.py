#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·乙巳·庚辰·☴巽-VERIFY-MEMORY-CNSH-v2.0-UID9622
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

"""🐉 龍魂引擎：verify_memory_cnsh.py
验证：记忆服务 + CNSH v2.1 解释器 + 执行器链路全部可运行。
"""
import os as _os
import sys as _sys
_module_dir = _os.path.dirname(_os.path.abspath(__file__))
if _module_dir not in _sys.path:
    _sys.path.insert(0, _module_dir)

import json
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(_module_dir).parent
STATE_DIR = PROJECT_ROOT / "state"
STATE_DIR.mkdir(parents=True, exist_ok=True)


def _run(cmd: list, cwd=PROJECT_ROOT, timeout=60) -> dict:
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "ok": proc.returncode == 0,
            "exit_code": proc.returncode,
            "stdout": proc.stdout[-500:] if proc.stdout else "",
            "stderr": proc.stderr[-500:] if proc.stderr else "",
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "exit_code": -1, "stdout": "", "stderr": "timeout"}
    except Exception as e:
        return {"ok": False, "exit_code": -1, "stdout": "", "stderr": str(e)}


def _health_check(host="127.0.0.1", port=8771) -> dict:
    try:
        with urllib.request.urlopen(f"http://{host}:{port}/v1/memory/health", timeout=3) as resp:
            return {"ok": True, "data": json.loads(resp.read().decode("utf-8"))}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def main():
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "DNA": "#龍芯⚡️丙午·丙申·乙巳·庚辰·☴巽-VERIFY-MEMORY-CNSH-v2.0-UID9622",
        "memory_services": {},
        "cnsht_examples": {},
        "executor": {},
        "overall_ok": True,
    }

    # 1. 记忆服务状态
    services = [
        ("CNSH_国密工具", ["python3", "bin/CNSH_国密工具.py"]),
        ("CNSH_透明语义治理内核", ["python3", "bin/CNSH_透明语义治理内核.py"]),
        ("lh_memory_load", ["python3", "bin/lh_memory_load.py"]),
        ("lh_memory_indexer", ["python3", "bin/lh_memory_indexer.py", "--force"]),
        ("CNSH_知识库", ["python3", "bin/CNSH_知识库.py"]),
        ("CNSH_颜色历史", ["python3", "bin/CNSH_颜色历史.py"]),
        ("dna_memory_layer", ["python3", "bin/dna_memory_layer.py", "--offline", "summary"]),
    ]

    for name, cmd in services:
        result = _run(cmd)
        report["memory_services"][name] = result
        if not result["ok"]:
            report["overall_ok"] = False

    # 记忆 API 健康检查（可能已启动）
    health = _health_check()
    report["memory_services"]["lh_memory_api"] = health

    # 2. CNSH v2.1 examples
    examples = [
        "cnsh/core/cnsh_v2.1/examples/hello.cnsh",
        "cnsh/core/cnsh_v2.1/examples/fib.cnsh",
        "cnsh/core/cnsh_v2.1/examples/types.cnsh",
        "cnsh/core/cnsh_v2.1/examples/file_io.cnsh",
        "cnsh/core/cnsh_v2.1/examples/crypto.cnsh",
        "cnsh/core/cnsh_v2.1/examples/audit.cnsh",
        "cnsh/core/cnsh_v2.1/examples/ffi.cnsh",
    ]

    for ex in examples:
        cmd = ["python3", "cnsh/core/cnsh_v2.1/run.py", ex]
        if "types.cnsh" in ex:
            cmd.append("--no-type-check")
        result = _run(cmd)
        report["cnsht_examples"][ex] = result
        if not result["ok"]:
            report["overall_ok"] = False

    # 3. 执行器链路
    executor_result = _run([
        "python3", "bin/CNSH_执行器.py",
        "cnsh/core/cnsh_v2.1/examples/hello.cnsh",
    ])
    report["executor"] = executor_result
    if not executor_result["ok"]:
        report["overall_ok"] = False

    # 4. 写入报告
    report_path = STATE_DIR / "verification_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # 5. 终端摘要
    print("=" * 60)
    print("🐉 龍魂 · 记忆 + CNSH 落地验证报告")
    print("=" * 60)
    print(f"生成时间: {report['generated_at']}")
    print(f"整体状态: {'✅ 全部通过' if report['overall_ok'] else '🔴 存在失败'}")
    print()

    print("【记忆服务】")
    for name, result in report["memory_services"].items():
        mark = "✅" if result.get("ok") else "🔴"
        print(f"  {mark} {name}")
    print()

    print("【CNSH v2.1 Examples】")
    for ex, result in report["cnsht_examples"].items():
        mark = "✅" if result.get("ok") else "🔴"
        print(f"  {mark} {Path(ex).name}")
    print()

    print("【执行器链路】")
    mark = "✅" if report["executor"].get("ok") else "🔴"
    print(f"  {mark} CNSH_执行器.py 执行 hello.cnsh")
    print()

    print(f"报告已写入: {report_path}")
    print(f"DNA: {report['DNA']}")

    return 0 if report["overall_ok"] else 1


import sys as _sys_real

if __name__ == "__main__":
    _sys_real.exit(main())
