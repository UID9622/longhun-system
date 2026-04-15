#!/usr/bin/env python3
"""
龍魂系统·全模块自检·开机自检入口
health_check.py v1.0

作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
DNA: #龍芯⚡️2026-04-06-系统自检-v1.0
理论指导: 曾仕强老师（永恒显示）
献礼: 乔布斯·曾仕强·历代传递和平与爱的人

用法:
  python3 bin/health_check.py          # 全检
  python3 bin/health_check.py --fast   # 只检文件/端口（跳过模块导入）
  python3 bin/health_check.py --json   # JSON输出（供其他脚本调用）
"""

import sys
import json
import time
import subprocess
import importlib.util
from pathlib import Path
from typing import Optional

BASE    = Path.home() / "longhun-system"
BIN     = BASE / "bin"
LOGS    = BASE / "logs"
DNA_TAG = "#龍芯⚡️2026-04-06-系统自检-v1.0"

# ─────────────────────────────────────────────────────────
# 检查项定义
# ─────────────────────────────────────────────────────────

CACHE = BASE / "cache"

FILE_CHECKS = [
    # (标签, 路径, 期望存在)
    ("CLAUDE.md",           BASE / "CLAUDE.md",                          True),
    ("algo_db.py",          BIN  / "algo_db.py",                         True),
    ("algo_db.jsonl",       LOGS / "algo_db.jsonl",                      True),
    ("fuxi_taiji_engine",   BIN  / "fuxi_taiji_engine.py",               True),
    ("translator.py",       BIN  / "translator.py",                      True),
    ("persona_router.py",   BIN  / "persona_router.py",                  True),
    ("quantum_deduce.py",   BIN  / "quantum_deduce.py",                  True),
    ("identity_engine.py",  BIN  / "identity_engine.py",                 True),
    ("cnsh_editor.py",      BIN  / "cnsh_editor.py",                     True),
    ("auto_audit.py",       BIN  / "auto_audit.py",                      True),
    ("immutable_ledger",    LOGS / "immutable_ledger.jsonl",              True),
    ("emotion_log",         LOGS / "emotion_log.jsonl",                  True),
    (".env",                BASE / ".env",                                True),
    # 时光机
    ("time_machine.py",     BASE / "time_machine.py",                    True),
    ("time_machine 密钥",   BASE / ".dna_key",                           True),
    ("time_machine cache",  CACHE,                                        True),
]

PORT_CHECKS = [
    # (标签, host, port, 描述)
    ("Local Engine",  "127.0.0.1", 8000, "app.py 主服务"),
    ("Ollama",        "127.0.0.1", 11434, "Ollama LLM服务"),
    ("Open WebUI",    "127.0.0.1", 8080, "Open WebUI界面"),
    ("龍魂API",        "127.0.0.1", 9622, "龍魂API服务"),
    ("longhun_local", "127.0.0.1", 8765, "longhun_local_service"),
    ("MCP-mini",      "127.0.0.1", 8787, "MCP人格调度心脏"),
]

MODULE_CHECKS = [
    # (标签, 文件路径, 导入名, 测试函数)
    ("algo_db·extract",     BIN/"algo_db.py",           "algo_db",
     lambda m: len(m.extract()) > 0),
    ("fuxi·digital_root",   BIN/"fuxi_taiji_engine.py", "fuxi_taiji_engine",
     lambda m: m.digital_root(369) == 9),
    ("persona_router",      BIN/"persona_router.py",    "persona_router",
     lambda m: isinstance(m.route("测试代码"), str)),
]

# ─────────────────────────────────────────────────────────
# 检查函数
# ─────────────────────────────────────────────────────────

def _icon(ok: bool, warn: bool = False) -> str:
    if ok:    return "✅"
    if warn:  return "⏳"
    return "❌"

def check_files() -> list[dict]:
    results = []
    for label, path, should_exist in FILE_CHECKS:
        exists = path.exists()
        ok = exists == should_exist
        size = path.stat().st_size if exists else 0
        results.append({
            "check": "file", "label": label, "ok": ok,
            "path": str(path.relative_to(Path.home())),
            "size": size,
            "detail": f"{size} bytes" if exists else "文件不存在",
        })
    return results

def check_ports() -> list[dict]:
    results = []
    for label, host, port, desc in PORT_CHECKS:
        try:
            r = subprocess.run(
                ["nc", "-z", "-w1", host, str(port)],
                capture_output=True, timeout=2
            )
            ok = r.returncode == 0
        except Exception:
            ok = False
        results.append({
            "check": "port", "label": label, "ok": ok,
            "port": port, "desc": desc,
            "detail": f":{port} {'在线' if ok else '未启动'}",
        })
    return results

def check_modules() -> list[dict]:
    results = []
    for label, filepath, modname, test_fn in MODULE_CHECKS:
        if not filepath.exists():
            results.append({"check": "module", "label": label, "ok": False,
                            "detail": "文件不存在"})
            continue
        try:
            spec = importlib.util.spec_from_file_location(modname, filepath)
            mod  = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            ok   = test_fn(mod)
            results.append({"check": "module", "label": label, "ok": ok,
                            "detail": "导入+测试通过" if ok else "测试失败"})
        except Exception as e:
            results.append({"check": "module", "label": label, "ok": False,
                            "detail": str(e)[:80]})
    return results

def check_time_machine() -> dict:
    """时光机快照专项检查"""
    cache = BASE / "cache"
    key   = BASE / ".dna_key"
    if not cache.exists():
        return {"ok": False, "snap_count": 0, "detail": "cache目录不存在·运行 time_machine.py 初始化"}
    snaps = list(cache.glob("*.dna"))
    key_ok = key.exists() and key.stat().st_size == 32
    return {
        "ok":         len(snaps) >= 0 and key_ok,
        "snap_count": len(snaps),
        "key_ok":     key_ok,
        "detail":     f"{len(snaps)}个加密快照  密钥{'✅' if key_ok else '❌未初始化'}",
    }

def check_algo_db_counts() -> dict:
    """algo_db 族数量快速验证"""
    db = LOGS / "algo_db.jsonl"
    if not db.exists():
        return {"ok": False, "count": 0, "families": {}}
    families: dict[str, int] = {}
    seen: set[str] = set()
    with open(db, encoding="utf-8") as f:
        for line in f:
            try:
                e = json.loads(line.strip())
                name = e.get("name","")
                if name not in seen:
                    seen.add(name)
                    fam = e.get("family","?")
                    families[fam] = families.get(fam, 0) + 1
            except Exception:
                continue
    return {"ok": len(seen) >= 9, "count": len(seen), "families": families}

# ─────────────────────────────────────────────────────────
# 主函数
# ─────────────────────────────────────────────────────────

def run_all(fast: bool = False) -> dict:
    t0 = time.time()
    report: dict = {
        "dna": DNA_TAG,
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "files": check_files(),
        "ports": check_ports(),
        "modules": [] if fast else check_modules(),
        "algo_db": check_algo_db_counts(),
        "time_machine": check_time_machine(),
        "elapsed_ms": 0,
    }
    report["elapsed_ms"] = round((time.time() - t0) * 1000)
    return report

def print_report(report: dict):
    print(f"\n🐉 龍魂系统·全模块自检报告")
    print(f"   {report['dna']}")
    print(f"   检测时间: {report['ts']}  耗时: {report['elapsed_ms']}ms")

    # ── 文件检查
    print(f"\n── 文件模块 ─{'─'*40}")
    for r in report["files"]:
        icon = _icon(r["ok"])
        print(f"  {icon} {r['label']:<22} {r['detail']}")

    # ── 端口检查
    print(f"\n── 端口/服务 ─{'─'*39}")
    for r in report["ports"]:
        icon = _icon(r["ok"], warn=not r["ok"])
        print(f"  {icon} {r['label']:<16} {r['detail']:<20} {r['desc']}")

    # ── 模块功能检查
    if report["modules"]:
        print(f"\n── 模块功能测试 ─{'─'*36}")
        for r in report["modules"]:
            icon = _icon(r["ok"])
            print(f"  {icon} {r['label']:<24} {r['detail']}")

    # ── algo_db 专项
    adb = report["algo_db"]
    icon = _icon(adb["ok"])
    print(f"\n── 算法元数据库 ─{'─'*36}")
    print(f"  {icon} 算法总数: {adb['count']} 条  {'✅ 9族完整' if adb['ok'] else '❌ 不足9族'}")
    for fam, cnt in adb.get("families", {}).items():
        print(f"      • {fam}: {cnt}")

    # ── 时光机专项
    tm = report["time_machine"]
    icon = _icon(tm["ok"])
    print(f"\n── 时光机·设备容器 ─{'─'*34}")
    print(f"  {icon} {tm['detail']}")

    # ── 总结
    all_items = report["files"] + report["ports"] + report["modules"]
    ok_count  = sum(1 for r in all_items if r["ok"])
    bad       = [r["label"] for r in all_items if not r["ok"]]
    total     = len(all_items)
    color     = "🟢" if len(bad) == 0 else ("🟡" if len(bad) <= 3 else "🔴")
    print(f"\n{color} 总结: {ok_count}/{total} 通过")
    if bad:
        print(f"   ❌ 需要关注: {', '.join(bad)}")
    print()

if __name__ == "__main__":
    fast = "--fast" in sys.argv
    as_json = "--json" in sys.argv
    report = run_all(fast=fast)
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(report)
