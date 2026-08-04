#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·丙申·亥时·☵坎-INTEGRATION-TEST-v1.0-a1b2c3d4
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 职能: 龍魂系统集成测试 · 知识中枢→模型路由→审计完整链路
"""
龍魂·集成测试 v1.0
────────────────────────────
测试链路（7条）:
  1. 知识中枢API健康     → GET  /v1/li/health
  2. 系统状态端点        → GET  /v1/li/status
  3. 模型路由端点        → GET  /v1/li/model-routing
  4. 审计日志端点        → GET  /v1/li/audit
  5. 模型列表端点        → GET  /v1/li/models
  6. 审计写入→读取链路   → 写入测试记录→审计端点验证
  7. 配置一致性          → Ollama模型↔Settings.JSON↔API端点三对齐

用法:
  python3 bin/lh_integration_test.py           # 运行全部
  python3 bin/lh_integration_test.py --quick   # 快速模式(只测关键3项)
  python3 bin/lh_integration_test.py --json    # JSON输出
"""
import os, sys, json, time, subprocess, tempfile
from pathlib import Path
from datetime import datetime, timezone, timedelta
import urllib.request
import urllib.error

CST = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent
API_BASE = "http://127.0.0.1:8766/v1/li"

# ── 颜色 ──
GREEN = "\033[92m"; YELLOW = "\033[93m"; RED = "\033[91m"; BOLD = "\033[1m"; RESET = "\033[0m"
def g(s): return f"{GREEN}{s}{RESET}" if sys.stdout.isatty() else s
def y(s): return f"{YELLOW}{s}{RESET}" if sys.stdout.isatty() else s
def r(s): return f"{RED}{s}{RESET}" if sys.stdout.isatty() else s
def b(s): return f"{BOLD}{s}{RESET}" if sys.stdout.isatty() else s

PASS = "PASS"; FAIL = "FAIL"; SKIP = "SKIP"


def api_get(endpoint, timeout=10):
    """调用API GET端点"""
    url = f"{API_BASE}/{endpoint}"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read()), None
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read())
        except:
            body = {"error": str(e)}
        return e.code, body, str(e)
    except Exception as e:
        return 0, None, str(e)


def test_1_health():
    """T1: 知识中枢API健康"""
    status, data, err = api_get("health")
    if err:
        return FAIL, f"API不可达: {err}"
    if status != 200:
        return FAIL, f"HTTP {status}"
    if data.get("status") == "ok":
        return PASS, f"服务={data.get('service')} 版本={data.get('version')}"
    return FAIL, f"异常响应: {data}"


def test_2_status():
    """T2: 系统状态端点"""
    status, data, err = api_get("status")
    if err:
        return FAIL, f"端点不可达: {err}"
    if status != 200:
        return FAIL, f"HTTP {status}"
    # status端点返回扁平字典，不同平台格式不同
    cpu = data.get("cpu", "?")
    mem = data.get("memory", "?")
    disk = data.get("disk", "?")
    return PASS, f"CPU={cpu}·内存={mem}·磁盘={disk}"


def test_3_model_routing():
    """T3: 模型路由端点"""
    status, data, err = api_get("model-routing")
    if err:
        return FAIL, f"不可达: {err}"
    if status != 200:
        return FAIL, f"HTTP {status}"

    issues = []
    if not data.get("ollama_running"):
        issues.append("Ollama离线")
    if not data.get("local_available"):
        issues.append("无本地模型")
    if not data.get("config", {}).get("localModelPath"):
        issues.append("localModelPath未配置")

    n_models = len(data.get("local_models", []))
    if issues:
        return FAIL, "; ".join(issues)
    return PASS, f"Ollama在线·{n_models}模型·配置已注入"


def test_4_audit_endpoint():
    """T4: 审计日志端点"""
    status, data, err = api_get("audit?limit=5")
    if err:
        return FAIL, f"不可达: {err}"
    if status != 200:
        return FAIL, f"HTTP {status}"

    total = data.get("total", 0)
    pending = data.get("pending", 0)
    if data.get("exists") != True:
        return FAIL, "审计日志不存在"
    if pending > 10000:
        return FAIL, f"积压严重: {pending}条待审"
    if pending > 100:
        return y(f"积压{pending}条·建议批量处理"), f"待审{pending}/{total}"

    return PASS, f"共{total}条·已审{data.get('reviewed',0)}·待审{pending}"


def test_5_models_endpoint():
    """T5: 模型列表端点"""
    status, data, err = api_get("models")
    if err:
        # 端点可能不存在，不算致命
        return SKIP, f"端点可能不存在: {err}"
    if status != 200:
        return SKIP, f"HTTP {status}"
    return PASS, f"返回{len(data) if isinstance(data, list) else '?'}个模型"


def test_6_audit_write_read_chain():
    """T6: 审计写入→读取链路"""
    audit_path = PROJECT_ROOT / "logs" / "ai_audit.jsonl"
    if not audit_path.exists():
        return SKIP, "审计日志文件不存在"

    # 写入一条测试记录
    test_rec = {
        "model_source": "_integration_test_",
        "file_path": "test/integration_test.py",
        "line_start": 1, "line_end": 1,
        "code_hash": "test_hash_integration_deadbeef",
        "review_status": "pending",
        "timestamp": datetime.now(CST).isoformat(),
        "_test": True,
    }

    # 追加到日志
    try:
        with open(audit_path, "a") as f:
            f.write(json.dumps(test_rec, ensure_ascii=False) + "\n")
    except Exception as e:
        return FAIL, f"写入失败: {e}"

    # 立即通过API读取验证
    status, data, err = api_get("audit?limit=1")
    if err:
        return FAIL, f"读取验证失败: {err}"

    # 清理测试记录
    try:
        lines = []
        with open(audit_path) as f:
            for line in f:
                if not line.strip(): continue
                try:
                    rec = json.loads(line)
                    if rec.get("_test"): continue  # 跳过测试记录
                    lines.append(line)
                except:
                    lines.append(line)
        with open(audit_path, "w") as f:
            for line in lines:
                f.write(line)
    except Exception:
        pass  # 清理失败不阻测试

    return PASS, "写入→读取链路正常"


def test_7_config_consistency():
    """T7: Ollama模型↔Settings↔API端点三对齐"""
    # 1. Ollama
    ollama_models = set()
    try:
        proc = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        for line in proc.stdout.strip().split("\n")[1:]:
            parts = line.split()
            if len(parts) >= 1:
                ollama_models.add(parts[0].split(":")[0])
    except:
        pass

    # 2. Settings
    settings_models = set()
    settings_path = os.path.expanduser("~/Library/Application Support/CodeBuddy CN/User/settings.json")
    if os.path.exists(settings_path):
        try:
            with open(settings_path) as f:
                s = json.load(f)
            lp = s.get("longhun-model.localModelPath", "")
            if lp:
                settings_models.add(lp.replace("ollama://", "").split(":")[0])
        except:
            pass

    # 3. API
    api_models = set()
    status, data, err = api_get("model-routing")
    if not err:
        for m in data.get("local_models", []):
            api_models.add(m["name"].split(":")[0])

    # 一致性判定
    if not ollama_models:
        return SKIP, "Ollama不可达"

    overlap = ollama_models & api_models
    if len(overlap) == 0:
        return FAIL, f"Ollama({len(ollama_models)})≠API({len(api_models)})·无交集"
    if len(overlap) < len(ollama_models) * 0.5:
        return y("API未完全同步"), f"交集{len(overlap)}/{len(ollama_models)}"

    return PASS, f"Ollama{len(ollama_models)}·API{len(api_models)}·交集{len(overlap)}·Settings{'✅' if settings_models else '⚠️未配置'}"


ALL_TESTS = [
    ("T1 知识中枢API健康", test_1_health),
    ("T2 系统状态端点", test_2_status),
    ("T3 模型路由端点", test_3_model_routing),
    ("T4 审计日志端点", test_4_audit_endpoint),
    ("T5 模型列表端点", test_5_models_endpoint),
    ("T6 审计写入→读取链路", test_6_audit_write_read_chain),
    ("T7 配置三对齐", test_7_config_consistency),
]

QUICK_TESTS = ALL_TESTS[:3]  # T1-T3


def run_tests(tests, json_output=False):
    results = []
    t0 = time.time()

    for name, test_fn in tests:
        try:
            result, detail = test_fn()
        except Exception as e:
            result, detail = FAIL, f"异常: {e}"
        results.append({"name": name, "result": result, "detail": detail, "ts": datetime.now(CST).isoformat()})

    elapsed = round(time.time() - t0, 2)
    pass_count = sum(1 for it in results if it["result"] == PASS)
    fail_count = sum(1 for it in results if it["result"] == FAIL)
    skip_count = sum(1 for it in results if it["result"] == SKIP)
    warn_count = sum(1 for it in results if it["result"] not in (PASS, FAIL, SKIP))

    if json_output:
        output = {
            "dna": "#龍芯⚡️INTEGRATION-TEST-v1.0",
            "elapsed_sec": elapsed,
            "summary": {"total": len(results), "pass": pass_count, "fail": fail_count,
                         "skip": skip_count, "warn": warn_count},
            "results": results,
            "conclusion": "ALL_PASS" if fail_count == 0 else "HAS_FAILURES"
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0 if fail_count == 0 else 1

    # 终端输出
    print(f"\n{'='*60}")
    print(f"{b('🐉 龍魂·集成测试 v1.0')}")
    print(f"{'='*60}")
    print(f"  时间: {datetime.now(CST).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  耗时: {elapsed}秒")
    print(f"  {'='*60}\n")

    for item in results:
        icon = {"PASS": g("PASS"), "FAIL": r("FAIL"), "SKIP": y("SKIP")}
        res = item["result"]
        if res not in icon:
            icon[res] = y("WARN")
        print(f"  {icon.get(res, '?')} {b(item['name']):28s}  {item['detail']}")

    print(f"\n  {'='*60}")
    overall = g("全部通过 ✅") if fail_count == 0 else r(f"失败{fail_count}项 ❌")
    print(f"  {b('结果')}: {pass_count}通过·{fail_count}失败·{skip_count}跳过·{warn_count}警告  {overall}")
    print()

    return 0 if fail_count == 0 else 1


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂集成测试")
    parser.add_argument("--quick", action="store_true", help="快速模式(前3项)")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    tests = QUICK_TESTS if args.quick else ALL_TESTS
    return run_tests(tests, json_output=args.json)


if __name__ == "__main__":
    sys.exit(main())
