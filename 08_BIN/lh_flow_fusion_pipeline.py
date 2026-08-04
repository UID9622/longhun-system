#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 流场融合管道 v1.0（一键全量注入）
DNA: #龍芯⚡️丙午·乙巳·壬申·未时·☰乾-FLOW-FUSION-PIPELINE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  运行所有可观测性引擎 → 翻译结果 → 注入流场融合桥接层 :8777/event

用法：
  python3 bin/lh_flow_fusion_pipeline.py                    # 全量注入一次
  python3 bin/lh_flow_fusion_pipeline.py --watch            # 守护模式 每5分钟
  python3 bin/lh_flow_fusion_pipeline.py --dry-run          # 只翻译不注入
  python3 bin/lh_flow_fusion_pipeline.py --self-audit       # 只注入自我审计
  python3 bin/lh_flow_fusion_pipeline.py --health           # 只注入健康检查
  python3 bin/lh_flow_fusion_pipeline.py --fuse             # 只注入熔断状态
  python3 bin/lh_flow_fusion_pipeline.py --status           # 查看管道状态

管线：
  [自我审计] → [健康检查] → [熔断控制] → [主动观察] → [资源监控]
       ↓            ↓            ↓            ↓            ↓
       └──────────────────┬──────────────────────────────┘
                          ↓
               [融合桥接层 :8777] → [流场 :8776]
"""

import os
import sys
import json
import time
import subprocess
import argparse
import urllib.request
import urllib.error
import sqlite3
import hashlib
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import deque

# ============================================================
# 锚点
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
PROJECT_ROOT = Path.home() / "longhun-system"
BIN = PROJECT_ROOT / "bin"
FUSION_BRIDGE_URL = "http://127.0.0.1:8777"
DATA_DIR = PROJECT_ROOT / "data"
PIPE_DB = DATA_DIR / "fusion_pipeline.db"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 管线数据库
# ============================================================

def init_pipe_db():
    conn = sqlite3.connect(str(PIPE_DB))
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pipe_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stage TEXT NOT NULL,
            status TEXT,
            events_injected INTEGER DEFAULT 0,
            errors TEXT,
            duration_ms REAL,
            dna_trace TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# ============================================================
# 注入助手
# ============================================================

def inject_event(source: str, event_type: str, severity: str = "info",
                 data: Optional[Dict] = None,
                 bridge_url: str = FUSION_BRIDGE_URL,
                 dry_run: bool = False) -> Dict:
    """注入单个事件到融合桥接层"""
    if dry_run:
        return {"injected": False, "reason": "dry_run", "event": event_type}

    payload = {
        "source": source,
        "event_type": event_type,
        "severity": severity,
        "data": data or {}
    }

    try:
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{bridge_url}/event",
            data=body,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        return {"injected": False, "error": f"bridge_unreachable: {e}", "event": event_type}
    except Exception as e:
        return {"injected": False, "error": str(e), "event": event_type}

def bridge_available(bridge_url: str = FUSION_BRIDGE_URL) -> bool:
    try:
        req = urllib.request.Request(f"{bridge_url}/ping")
        with urllib.request.urlopen(req, timeout=2) as resp:
            return json.loads(resp.read().decode()).get("pong") is True
    except Exception:
        return False

# ============================================================
# 观测阶段
# ============================================================

def stage_self_audit(bridge_url: str, dry_run: bool) -> Dict:
    """阶段1: 自我审计 → 流场注入"""
    results = {"stage": "self_audit", "events": []}

    try:
        proc = subprocess.run(
            [sys.executable, str(BIN / "lh_self_reflexivity_audit.py"), "--full", "--json"],
            capture_output=True, text=True, timeout=30, cwd=str(PROJECT_ROOT)
        )
        audit = json.loads(proc.stdout)

        # 按三个风险维度注入
        for rtype in ["dna_risk", "p0_risk", "protocol_risk"]:
            risk = audit.get(rtype, {})
            score = risk.get("risk_score", 0)
            status_char = risk.get("status", "🟡")
            severity = "critical" if score > 0.7 else ("medium" if score > 0.4 else "low")

            # 精细事件名
            level = "high" if score > 0.7 else ("medium" if score > 0.4 else "low")
            event_type = f"{rtype.replace('_risk','')}_risk_{level}"

            r = inject_event("self_audit", event_type, severity,
                           {"risk_score": score, "status": status_char,
                            "recommendation": risk.get("recommendation", "")},
                           bridge_url, dry_run)
            results["events"].append(r)

        results["status"] = "ok"
    except Exception as e:
        results["status"] = "error"
        results["error"] = str(e)
        # 兜底：至少报告自审失败
        inject_event("self_audit", "audit_failed", "high", {"error": str(e)},
                    bridge_url, dry_run)

    return results

def stage_health_check(bridge_url: str, dry_run: bool) -> Dict:
    """阶段2: 健康检查 → 流场注入"""
    results = {"stage": "health_check", "events": []}

    try:
        # 快速健康检查
        proc = subprocess.run(
            [sys.executable, str(BIN / "lh_health_check_quick.py")],
            capture_output=True, text=True, timeout=20, cwd=str(PROJECT_ROOT)
        )
        output = proc.stdout + proc.stderr

        # 解析健康状态
        if "P0" in output or "critical" in output.lower() or "CRITICAL" in output:
            severity, event_type = "critical", "critical"
        elif "WARNING" in output or "warning" in output.lower() or "⚠" in output:
            severity, event_type = "medium", "warning"
        elif "OK" in output or "健康" in output or "✅" in output:
            severity, event_type = "low", "ok"
        else:
            severity, event_type = "info", "unknown"

        r = inject_event("health_check", event_type, severity,
                       {"summary": output[:500]}, bridge_url, dry_run)
        results["events"].append(r)
        results["status"] = "ok"
    except Exception as e:
        results["status"] = "error"
        results["error"] = str(e)
        inject_event("health_check", "check_failed", "high", {"error": str(e)},
                    bridge_url, dry_run)

    return results

def stage_fuse_status(bridge_url: str, dry_run: bool) -> Dict:
    """阶段3: 熔断状态 → 流场注入"""
    results = {"stage": "fuse_control", "events": []}

    try:
        proc = subprocess.run(
            [sys.executable, str(BIN / "fuse_control.py"), "status"],
            capture_output=True, text=True, timeout=10, cwd=str(PROJECT_ROOT)
        )
        output = proc.stdout

        # 解析熔断状态
        if "🔴" in output or "TRIPPED" in output or "硬阻断" in output:
            severity, event_type = "critical", "tripped"
        elif "🟡" in output or "软阻断" in output:
            severity, event_type = "medium", "soft_block"
        elif "🟢" in output or "NORMAL" in output:
            severity, event_type = "low", "normal"
        else:
            severity, event_type = "info", "unknown"

        r = inject_event("fuse_control", event_type, severity,
                       {"summary": output[:500]}, bridge_url, dry_run)
        results["events"].append(r)
        results["status"] = "ok"
    except Exception as e:
        results["status"] = "error"
        results["error"] = str(e)
        inject_event("fuse_control", "status_failed", "medium", {"error": str(e)},
                    bridge_url, dry_run)

    return results

def stage_active_observation(bridge_url: str, dry_run: bool) -> Dict:
    """阶段4: 主动观察 → 流场注入"""
    results = {"stage": "active_observation", "events": []}

    try:
        # 检查最近的系统变化
        recent_files = []
        bin_dir = BIN
        for f in sorted(bin_dir.glob("*.py"), key=lambda p: p.stat().st_mtime, reverse=True)[:3]:
            mtime = datetime.datetime.fromtimestamp(f.stat().st_mtime)
            if (datetime.datetime.now() - mtime).seconds < 3600:  # 1小时内
                recent_files.append(str(f.name))

        if recent_files:
            r = inject_event("active_observe", "file_change", "low",
                           {"recent_files": recent_files}, bridge_url, dry_run)
            results["events"].append(r)

        results["status"] = "ok"
    except Exception as e:
        results["status"] = "error"
        results["error"] = str(e)

    return results

def stage_resource_monitor(bridge_url: str, dry_run: bool) -> Dict:
    """阶段5: 资源监控 → 流场注入"""
    results = {"stage": "resource_monitor", "events": []}

    try:
        import psutil

        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent

        # CPU
        if cpu > 90:
            r = inject_event("resource_monitor", "cpu_high", "critical",
                           {"cpu_percent": cpu}, bridge_url, dry_run)
        elif cpu > 70:
            r = inject_event("resource_monitor", "cpu_high", "medium",
                           {"cpu_percent": cpu}, bridge_url, dry_run)
        else:
            r = inject_event("resource_monitor", "cpu_normal", "low",
                           {"cpu_percent": cpu}, bridge_url, dry_run)
        results["events"].append(r)

        # Memory
        if mem > 90:
            r = inject_event("resource_monitor", "mem_high", "critical",
                           {"mem_percent": mem}, bridge_url, dry_run)
        elif mem > 75:
            r = inject_event("resource_monitor", "mem_high", "medium",
                           {"mem_percent": mem}, bridge_url, dry_run)
        else:
            r = inject_event("resource_monitor", "mem_normal", "low",
                           {"mem_percent": mem}, bridge_url, dry_run)
        results["events"].append(r)

        results["status"] = "ok"
    except ImportError:
        results["status"] = "skipped"
        results["reason"] = "psutil not installed"
    except Exception as e:
        results["status"] = "error"
        results["error"] = str(e)

    return results

# ============================================================
# 管线编排
# ============================================================

def run_pipeline(bridge_url: str = FUSION_BRIDGE_URL,
                 stages: Optional[List[str]] = None,
                 dry_run: bool = False) -> Dict:
    """运行完整融合管线"""
    all_stages = ["self_audit", "health_check", "fuse_control",
                  "active_observation", "resource_monitor"]
    stages = stages or all_stages

    # 先检查桥接层
    bridge_ok = bridge_available(bridge_url) if not dry_run else False
    if not dry_run and not bridge_ok:
        print("⚠️ 融合桥接层 (8777) 未运行，注入不会生效。")
        print("   请先启动: python3 bin/lh_flow_fusion_bridge.py &")

    start_time = time.time()
    results = {
        "pipeline": "flow_fusion_v1.0",
        "bridge_available": bridge_ok,
        "dry_run": dry_run,
        "stages": {},
        "total_events": 0,
    }

    stage_map = {
        "self_audit": stage_self_audit,
        "health_check": stage_health_check,
        "fuse_control": stage_fuse_status,
        "active_observation": stage_active_observation,
        "resource_monitor": stage_resource_monitor,
    }

    for stage_name in stages:
        if stage_name not in stage_map:
            continue
        print(f"  🚀 {stage_name}...", end=" ", flush=True)
        stage_start = time.time()
        stage_result = stage_map[stage_name](bridge_url, dry_run)
        duration = round((time.time() - stage_start) * 1000)
        stage_result["duration_ms"] = duration

        events_count = len(stage_result.get("events", []))
        injected = sum(1 for e in stage_result.get("events", [])
                      if e.get("injected") or (dry_run and e.get("event")))

        status_icon = "✅" if stage_result.get("status") == "ok" else "❌"
        print(f"{status_icon} {events_count}事件/{injected}注入 ({duration}ms)")

        results["stages"][stage_name] = stage_result
        results["total_events"] += injected

    results["duration_ms"] = round((time.time() - start_time) * 1000)

    # 记录管线运行
    conn = sqlite3.connect(str(PIPE_DB))
    dna = f"#龍芯⚡️{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-PIPELINE-FUSION"
    for stage_name, sr in results["stages"].items():
        conn.execute(
            "INSERT INTO pipe_runs (stage, status, events_injected, errors, duration_ms, dna_trace) VALUES (?,?,?,?,?,?)",
            (stage_name, sr.get("status"),
             sum(1 for e in sr.get("events", []) if e.get("injected") or (dry_run and e.get("event"))),
             sr.get("error", ""), sr.get("duration_ms", 0), dna)
        )
    conn.commit()
    conn.close()

    return results

# ============================================================
# CLI
# ============================================================

def print_banner():
    print(f"""
╔══════════════════════════════════════════════════╗
║  🐉 龍魂 · 流场融合管道 v1.0                       ║
║  一键注入 · 全引擎观测 · 统一物理映射                ║
║  CONFIRM: {CONFIRM}  ║
╚══════════════════════════════════════════════════╝
""")

def main():
    init_pipe_db()

    parser = argparse.ArgumentParser(description="🐉 龍魂 · 流场融合管道")
    parser.add_argument("--watch", "-w", action="store_true", help="守护模式·每5分钟注入")
    parser.add_argument("--interval", type=int, default=300, help="守护模式间隔(秒) 默认300")
    parser.add_argument("--dry-run", action="store_true", help="只翻译不注入")
    parser.add_argument("--self-audit", action="store_true", help="只注入自我审计")
    parser.add_argument("--health", action="store_true", help="只注入健康检查")
    parser.add_argument("--fuse", action="store_true", help="只注入熔断状态")
    parser.add_argument("--observe", action="store_true", help="只注入主动观察")
    parser.add_argument("--resource", action="store_true", help="只注入资源监控")
    parser.add_argument("--status", action="store_true", help="查看管道运行历史")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--bridge-url", type=str, default=FUSION_BRIDGE_URL, help="融合桥接地址")
    args = parser.parse_args()

    if args.status:
        conn = sqlite3.connect(str(PIPE_DB))
        rows = conn.execute(
            "SELECT * FROM pipe_runs ORDER BY id DESC LIMIT 50"
        ).fetchall()
        conn.close()
        print(f"融合管道运行历史 ({len(rows)}条):")
        for r in rows:
            icon = "✅" if r[2] == "ok" else "❌"
            print(f"  {r[6][:19]} {icon} {r[1]:20s} 注入{r[3]} 耗时{r[5]:.0f}ms")
        return

    # 确定要运行的阶段
    stages = []
    if args.self_audit: stages.append("self_audit")
    if args.health: stages.append("health_check")
    if args.fuse: stages.append("fuse_control")
    if args.observe: stages.append("active_observation")
    if args.resource: stages.append("resource_monitor")
    if not stages:
        stages = None  # 全部

    # 守护模式
    if args.watch:
        print_banner()
        print(f"🔄 守护模式 · 每{args.interval}秒注入一次 · Ctrl+C 退出\n")
        try:
            while True:
                results = run_pipeline(args.bridge_url, stages, args.dry_run)
                print(f"\n  📊 注入{results['total_events']}事件 · "
                      f"耗时{results['duration_ms']}ms · "
                      f"桥接{'✅' if results['bridge_available'] else '❌'}")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n👋 融合管道 · 龙魂不息")
    else:
        print_banner()
        results = run_pipeline(args.bridge_url, stages, args.dry_run)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"\n📊 管线完成: {results['total_events']}事件注入 · "
                  f"耗时{results['duration_ms']}ms · "
                  f"桥接{'✅在线' if results['bridge_available'] else '❌离线'}")
            for sname, sr in results["stages"].items():
                icon = "✅" if sr.get("status") == "ok" else "⚠️"
                print(f"  {icon} {sname}: {sr.get('duration_ms',0)}ms")

if __name__ == "__main__":
    main()
