#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════════════════════
# 龍魂体系 | 技能启动·全局验收测试 v1.0
# ═══════════════════════════════════════════════════════════
# DNA: #龍芯⚡️丙午·乙未·壬戌·丙午·䷊泰-INTEGRATION-TEST-v1.0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════════
#
# 用法:
#   python3 bin/test_integration.py              # 全量验收
#   python3 bin/test_integration.py --verbose    # 详细输出
#   python3 bin/test_integration.py --smoke      # 仅烟测试
# ═══════════════════════════════════════════════════════════
"""

import sys
import os
import json
import time
import hashlib
import urllib.request
import urllib.error
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# ── 测试目标 ──
ENDPOINTS = {
    # (名称, HTTP方法, URL, 请求体, 期望状态码, 验证键)
    "1_qiaojie_help": (
        "QiaoJie CLI v2.0 帮助",
        "CLI",
        None,
        ["帮助"],
        lambda r: r["ok"] is True,
    ),
    "2_qiaojie_qc": (
        "QiaoJie CLI QuickCheck",
        "CLI",
        None,
        ["qc"],
        lambda r: r["ok"] is True,
    ),
    "3_hub_8799_health": (
        "8799枢纽 /health",
        "GET",
        "http://127.0.0.1:8799/health",
        None,
        lambda r: r.get("status") == "ok",
    ),
    "4_hub_8799_status": (
        "8799枢纽 /hub/status",
        "GET",
        "http://127.0.0.1:8799/hub/status",
        None,
        lambda r: "version" in r and "backends" in r,
    ),
    "5_hub_8799_ask": (
        "8799枢纽 /hub/ask → 降级链",
        "POST",
        "http://127.0.0.1:8799/hub/ask",
        {"query": "ping", "persona_code": "integration_test", "route_id": "test", "format": "v2"},
        lambda r: "answer" in r and "route_trace" in r,
    ),
    "6_hub_8799_veto": (
        "8799枢纽 一票否决词熔断",
        "POST",
        "http://127.0.0.1:8799/hub/ask",
        {"query": "技术无国界", "persona_code": "integration_test", "format": "v2"},
        lambda r: r.get("audit_mark") == "🔴",  # HTTP 403
    ),
    "7_hub_8799_missing": (
        "8799枢纽 缺少query→400",
        "POST",
        "http://127.0.0.1:8799/hub/ask",
        {},
        lambda r: "error" in r,  # HTTP 400
    ),
    "8_guanlan_8770_health": (
        "观澜M1 /health",
        "GET",
        "http://127.0.0.1:8770/health",
        None,
        lambda r: r.get("service") == "观澜浏览器AI联动API" and r.get("status") in ("🟢", "ok"),
    ),
    "9_guanlan_8770_status": (
        "观澜M1 /status",
        "GET",
        "http://127.0.0.1:8770/status",
        None,
        lambda r: "网关" in r,
    ),
    "10_guanlan_8770_chat": (
        "观澜M1 /chat → Ollama透传",
        "POST",
        "http://127.0.0.1:8770/chat",
        {"query": "1+1等于几", "persona_code": "integration_test", "route_id": "test", "format": "v2"},
        lambda r: "answer" in r and r.get("audit_mark") == "🟢",
    ),
    "11_cnsh_gateway_health": (
        "CNSH网关 /health",
        "GET",
        "http://127.0.0.1:8765/health",
        None,
        lambda r: r.get("service") and r.get("status") in ("🟢", "ok"),
    ),
    "12_portal_home": (
        "门户主页",
        "GET",
        "https://uid9622.cn",
        None,
        lambda r: "200" in str(r.get("status_code", "")),
    ),
    "13_qiaojie_selftest": (
        "QiaoJie CLI 全链路自检",
        "CLI",
        None,
        ["selftest"],
        lambda r: r["ok"] is True,
    ),
}

# ── 全局统计 ──
passed: int = 0
failed: int = 0
skipped: int = 0
results: List[Dict[str, Any]] = []
verbose: bool = False
smoke_only: bool = False


def _run_cli(args: List[str]) -> Dict[str, Any]:
    """运行 qiaojie CLI 命令并返回结果 JSON"""
    import subprocess
    cmd = [sys.executable, "integrations/qiaojie/qiaojie_cli.py"] + args
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=15,
        cwd=os.path.join(os.path.dirname(__file__), ".."),
    )
    ok = result.returncode == 0 or "🟢" in result.stdout or "QiaoJie" in result.stdout
    return {"ok": ok, "stdout": result.stdout[:500], "stderr": result.stderr[:500]}


def _http_get(url: str) -> Dict[str, Any]:
    """HTTP GET"""
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode("utf-8")
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                data = {"_raw": body[:200]}
            data["status_code"] = resp.status
            return data
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {"_raw": body[:200]}
        data["status_code"] = e.code
        return data
    except Exception as e:
        return {"_error": str(e)}


def _http_post(url: str, body: Dict[str, Any]) -> Dict[str, Any]:
    """HTTP POST"""
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8")
            try:
                result = json.loads(raw)
            except json.JSONDecodeError:
                result = {"_raw": raw[:200]}
            result["status_code"] = resp.status
            return result
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            result = {"_raw": raw[:200]}
        result["status_code"] = e.code
        return result
    except Exception as e:
        return {"_error": str(e)}


def run_test(test_id: str, test_spec: Tuple) -> None:
    global passed, failed, skipped, verbose

    name, method, url_or_cmd, payload, check_fn = test_spec

    if smoke_only and not test_id.startswith(("1_", "3_", "5_", "8_")):
        results.append({"id": test_id, "name": name, "status": "⏭️", "detail": "smoke skip"})
        global skipped
        skipped += 1
        return

    try:
        if method == "CLI":
            r = _run_cli(payload)
        elif method == "GET":
            r = _http_get(url_or_cmd)
        elif method == "POST":
            r = _http_post(url_or_cmd, payload)
        else:
            r = {"_error": f"unknown method {method}"}

        ok = check_fn(r)
        if ok:
            passed += 1
            detail = ""
            results.append({"id": test_id, "name": name, "status": "🟢", "detail": detail})
            if verbose:
                print(f"  🟢 {test_id}: {name}")
        else:
            failed += 1
            detail = json.dumps(r, ensure_ascii=False)[:200]
            results.append({"id": test_id, "name": name, "status": "🔴", "detail": detail})
            if verbose:
                print(f"  🔴 {test_id}: {name} — {detail}")

    except Exception as e:
        failed += 1
        results.append({"id": test_id, "name": name, "status": "🔴", "detail": str(e)})
        if verbose:
            print(f"  🔴 {test_id}: {name} — {e}")


def generate_test_dna() -> str:
    ts = datetime.now().strftime("%Y%m%d%H%M")
    h = hashlib.sha256(f"integration-test-{ts}".encode()).hexdigest()[:8]
    return f"#龍芯⚡️丙午·乙未·壬戌·泰-INTEGRATION-TEST-{h}"


def print_report() -> None:
    total = passed + failed + skipped
    print("\n" + "═" * 56)
    print("  龍魂技能启动 · 全局验收报告")
    print(f"  DNA: {generate_test_dna()}")
    print("═" * 56)

    for r in results:
        icon = r["status"]
        print(f"  {icon} {r['id']}: {r['name']}")
        if r.get("detail") and icon == "🔴":
            print(f"     └─ {r['detail'][:120]}")

    print("─" * 56)
    pass_pct = passed / total * 100 if total > 0 else 0
    if failed == 0:
        print(f"  🟢 全部通过: {passed}/{total} ({pass_pct:.0f}%)")
    elif failed <= 2:
        print(f"  🟡 {passed}/{total} 通过 ({pass_pct:.0f}%), {failed} 失败")
    else:
        print(f"  🔴 {passed}/{total} 通过 ({pass_pct:.0f}%), {failed} 失败")
    print(f"     Skipped: {skipped}")
    print("═" * 56)

    # JSON 报告
    report_path = os.path.join(
        os.path.dirname(__file__), "..", "output", "integration_test_report.json"
    )
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        json.dump({
            "dna": generate_test_dna(),
            "time": datetime.now().isoformat(),
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "total": total,
            "results": results,
        }, f, ensure_ascii=False, indent=2)
    print(f"\n  📄 报告已保存: {report_path}")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="龍魂技能启动·全局验收测试")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--smoke", action="store_true", help="仅烟测试(核心链路)")
    args = parser.parse_args()

    global verbose, smoke_only
    verbose = args.verbose
    smoke_only = args.smoke

    print("═" * 56)
    print("  龍魂技能启动 · 全局验收 v1.0")
    print(f"  🧬 {generate_test_dna()}")
    print(f"  📋 {len(ENDPOINTS)} 项测试")
    if smoke_only:
        print("  ⚡ 烟测试模式 (仅核心链路)")
    print("═" * 56)

    for test_id in sorted(ENDPOINTS.keys()):
        run_test(test_id, ENDPOINTS[test_id])

    print_report()

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
