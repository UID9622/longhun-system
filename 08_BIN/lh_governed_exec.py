#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙戌·乙丑·卯时·䷯井-GOVERNED-EXEC-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂治理流水线执行器 v1.0

任何可能产生对外影响的命令，通过本包装器执行时会自动：
  1. 生成 workflow-transparent 工作流记录
  2. 过 iron-laws 自审闸
  3. 执行原命令并捕获结果
  4. 用 trust-protocol 记录贡献/违约
  5. 向事件总线发布 execution 事件
  6. 归档到审计目录

用法:
    python3 08_BIN/lh_governed_exec.py --cmd "lh iron --text '龍魂' --json" --desc "铁律检查"
    python3 08_BIN/lh_governed_exec.py --cmd "make deploy" --desc "部署到鲲鹏" --topic deploy.kunpeng

协议: CC BY-NC-SA 4.0 (思想层) · MulanPSL v2 (工程层)
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.longhun_core.dna_trace import generate_dna

CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUDIT_DIR = PROJECT_ROOT / "12_DOCS" / "agent_reports" / "governed_exec"


def _now() -> str:
    return datetime.now().isoformat()


def _run(cmd: str, cwd: Path = PROJECT_ROOT, timeout: int = 300) -> Dict[str, Any]:
    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "command": cmd,
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    except subprocess.TimeoutExpired:
        return {"command": cmd, "returncode": -1, "stdout": "", "stderr": "超时"}
    except Exception as e:
        return {"command": cmd, "returncode": -1, "stdout": "", "stderr": str(e)}


def _workflow_record(desc: str) -> Dict[str, Any]:
    wf_script = PROJECT_ROOT / "08_BIN" / "lh_workflow_transparent.py"
    cmd = f"python3 {wf_script} --message {json.dumps(desc)} --output-dir /tmp --json"
    res = _run(cmd)
    if res["returncode"] == 0:
        try:
            return json.loads(res["stdout"])
        except Exception:
            pass
    return {"error": res.get("stderr", ""), "dna": generate_dna("WORKFLOW", "UID9622")}


def _iron_gate(text: str) -> Dict[str, Any]:
    iron_script = PROJECT_ROOT / "08_BIN" / "lh_iron_law_gate.py"
    cmd = f"python3 {iron_script} --text {json.dumps(text)} --json"
    res = _run(cmd)
    if res["returncode"] == 0 or res["stdout"]:
        try:
            return json.loads(res["stdout"])
        except Exception:
            pass
    return {"verdict": "🟡", "error": res.get("stderr", "")}


def _trust_record(uid: str, event_type: str, desc: str):
    trust_script = PROJECT_ROOT / "08_BIN" / "lh_trust_protocol.py"
    if event_type == "contribute":
        cmd = f"python3 {trust_script} contribute {uid} code --desc {json.dumps(desc[:80])}"
    else:
        cmd = f"python3 {trust_script} violate {uid} --desc {json.dumps(desc[:80])}"
    _run(cmd)


def _publish_event(source: str, event_type: str, payload: Dict[str, Any], topic: str):
    bus_script = PROJECT_ROOT / "08_BIN" / "lh_event_bus.py"
    payload_json = json.dumps(payload, ensure_ascii=False)
    cmd = f"python3 {bus_script} publish --topic {topic} --source {source} --type {event_type} --payload {json.dumps(payload_json)}"
    _run(cmd)


def _save_audit(record: Dict[str, Any]):
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    ph = hashlib.sha256(json.dumps(record, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:8]
    path = AUDIT_DIR / f"governed_exec_{ts}_{ph}.json"
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂治理流水线执行器")
    parser.add_argument("--cmd", required=True, help="要执行的 shell 命令")
    parser.add_argument("--desc", required=True, help="操作描述，用于工作流与审计")
    parser.add_argument("--topic", default="governed.execution", help="事件总线 topic")
    parser.add_argument("--uid", default="UID9622", help="执行主体 UID")
    parser.add_argument("--skip-iron", action="store_true", help="跳过铁律自审（不推荐）")
    args = parser.parse_args()

    print("🐉 治理流水线执行器启动")
    print(f"   命令: {args.cmd}")
    print(f"   描述: {args.desc}\n")

    # 1. workflow transparent
    print("[1/5] 生成工作流透明化记录...")
    wf = _workflow_record(args.desc)

    # 2. iron law gate
    iron = {"verdict": "🟢", "findings": []}
    if not args.skip_iron:
        print("[2/5] 铁律自审闸...")
        iron = _iron_gate(args.desc + " " + args.cmd)
        if iron.get("verdict") == "🔴":
            print("🔴 铁律自审熔断，停止执行。")
            print(json.dumps(iron, ensure_ascii=False, indent=2))
            sys.exit(1)
    else:
        print("[2/5] 跳过铁律自审")

    # 3. execute command
    print("[3/5] 执行原命令...")
    result = _run(args.cmd)
    success = result["returncode"] == 0
    print(f"   退出码: {result['returncode']}")

    # 4. trust protocol
    print("[4/5] 记录君子协议事件...")
    trust_event = "contribute" if success else "violate"
    _trust_record(args.uid, trust_event, args.desc)

    # 5. event bus + audit
    print("[5/5] 发布事件并归档审计...")
    event_payload = {
        "uid": args.uid,
        "command": args.cmd,
        "description": args.desc,
        "returncode": result["returncode"],
        "success": success,
        "iron_verdict": iron.get("verdict"),
        "workflow_dna": wf.get("dna"),
    }
    _publish_event("lh-governed-exec", "command_executed", event_payload, args.topic)

    audit_record = {
        "dna": generate_dna("GOVERNED-EXEC", "UID9622"),
        "confirm": CONFIRM_MARK,
        "timestamp": _now(),
        "uid": args.uid,
        "command": args.cmd,
        "description": args.desc,
        "workflow": wf,
        "iron_law": iron,
        "execution": result,
        "trust_event": trust_event,
        "event_topic": args.topic,
    }
    audit_path = _save_audit(audit_record)

    print(f"\n✅ 治理流水线完成")
    print(f"   铁律: {iron.get('verdict')}")
    print(f"   执行: {'成功' if success else '失败'}")
    print(f"   君子协议: {trust_event}")
    print(f"   审计归档: {audit_path}")

    if result["stdout"]:
        print("\n--- 命令输出 ---")
        print(result["stdout"])
    if result["stderr"]:
        print("\n--- 命令错误 ---")
        print(result["stderr"])

    sys.exit(result["returncode"])


if __name__ == "__main__":
    main()
