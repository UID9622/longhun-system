#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂多 Agent 协作工作流引擎 v1.0
P2 · 人格链式编排 · 事件驱动 · 审计归档
DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-WORKFLOW-ENGINE-v1.0-UID9622
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

HOME = Path.home()
LONGHUN_DIR = HOME / ".longhun"
WF_DIR = LONGHUN_DIR / "workflows"
WF_RUN_DIR = LONGHUN_DIR / "workflow_runs"

GOV_SCRIPT = Path(__file__).resolve().parent / "lh_governed_exec.py"
BUS_SCRIPT = Path(__file__).resolve().parent / "lh_event_bus.py"


def ensure_dirs():
    WF_DIR.mkdir(parents=True, exist_ok=True)
    WF_RUN_DIR.mkdir(parents=True, exist_ok=True)


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def load_json(path: Path) -> Any:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: Any):
    ensure_dirs()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def list_builtin_workflows() -> dict:
    """内置工作流模板"""
    return {
        "code-review": {
            "name": "代码审查链",
            "description": "代码提交前：铁律检查 → 君子协议记录 → 事件发布 → 审计归档",
            "dna": "#龍芯⚡️丙午·甲申·辛丑·坤卦-WF-CODE-REVIEW-v1.0-UID9622",
            "steps": [
                {
                    "name": "铁律自审",
                    "agent": "P05 上帝之眼",
                    "cmd": "lh iron --text '{{message}}' --json",
                    "on_fail": "abort",
                },
                {
                    "name": "君子协议记录",
                    "agent": "P15 韩非子",
                    "cmd": "lh trust contribute UID9622 code --note '{{message}}'",
                },
                {
                    "name": "发布事件",
                    "agent": "P06 张衡",
                    "cmd": "_event:workflow.code_review.completed",
                    "event_payload": {"workflow": "code-review", "message": "{{message}}"},
                },
            ],
        },
        "publish": {
            "name": "对外发布链",
            "description": "内容发布前：主权检查 →  workflow-transparent → 君子协议 → 发布事件",
            "dna": "#龍芯⚡️丙午·甲申·辛丑·坤卦-WF-PUBLISH-v1.0-UID9622",
            "steps": [
                {
                    "name": "内容主权检查",
                    "agent": "P13 姜子牙",
                    "cmd": "lh iron --text '{{message}}' --json",
                    "on_fail": "abort",
                },
                {
                    "name": "工作流程透明化",
                    "agent": "P12 司马迁",
                    "cmd": "lh workflow --message '{{message}}' --output-dir 12_DOCS/agent_reports/workflows",
                },
                {
                    "name": "诚信记录",
                    "agent": "P15 韩非子",
                    "cmd": "lh trust contribute UID9622 publish --note '{{message}}'",
                },
                {
                    "name": "发布完成事件",
                    "agent": "P06 张衡",
                    "cmd": "_event:workflow.publish.completed",
                    "event_payload": {"workflow": "publish", "message": "{{message}}"},
                },
            ],
        },
        "deploy": {
            "name": "部署审查链",
            "description": "部署前：技能路由 → 治理执行 → 健康检查 → 事件归档",
            "dna": "#龍芯⚡️丙午·甲申·辛丑·坤卦-WF-DEPLOY-v1.0-UID9622",
            "steps": [
                {
                    "name": "智能体路由",
                    "agent": "P04 鲁班",
                    "cmd": "lh orchestrator route --text '{{message}}' --json",
                },
                {
                    "name": "治理执行",
                    "agent": "P05 上帝之眼",
                    "cmd": "lh governed --cmd 'echo 执行部署: {{message}}' --desc '部署审查链' --uid UID9622 --topic skill.execution",
                },
                {
                    "name": "健康检查",
                    "agent": "P07 扁鹊",
                    "cmd": "lh event stats",
                },
            ],
        },
    }


def init_builtin_workflows():
    ensure_dirs()
    builtins = list_builtin_workflows()
    for wf_id, wf in builtins.items():
        path = WF_DIR / f"{wf_id}.json"
        if not path.exists():
            save_json(path, wf)
    return list(builtins.keys())


def render_cmd(cmd: str, context: dict) -> str:
    for k, v in context.items():
        cmd = cmd.replace(f"{{{{{k}}}}}", str(v))
    return cmd


def publish_event(topic: str, payload: dict, source: str = "workflow-engine"):
    cmd = [
        sys.executable, str(BUS_SCRIPT), "publish",
        "--topic", topic,
        "--source", source,
        "--type", "workflow_step_completed",
        "--payload", json.dumps(payload, ensure_ascii=False),
    ]
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")


def run_step(step: dict, context: dict, run_log: dict, dry_run: bool = False):
    name = step["name"]
    agent = step.get("agent", "龍魂")
    raw_cmd = step["cmd"]
    cmd = render_cmd(raw_cmd, context)

    print(f"\n[Step] {name} · {agent}")
    print(f"   cmd: {cmd[:120]}")

    if dry_run:
        run_log["steps"].append({"name": name, "agent": agent, "cmd": cmd, "status": "dry_run"})
        return {"status": "dry_run", "returncode": 0}

    # 特殊命令：发布事件
    if cmd.startswith("_event:"):
        topic = cmd.split(":", 1)[1]
        payload = step.get("event_payload", {})
        payload = {k: render_cmd(str(v), context) for k, v in payload.items()}
        r = publish_event(topic, payload)
        result = {
            "status": "event_published" if r.returncode == 0 else "event_failed",
            "returncode": r.returncode,
            "stdout": r.stdout.strip(),
            "stderr": r.stderr.strip(),
        }
        run_log["steps"].append({"name": name, "agent": agent, "cmd": cmd, **result})
        return result

    # 普通命令：优先走治理流水线
    if cmd.startswith("lh "):
        gov_cmd = [
            sys.executable, str(GOV_SCRIPT),
            "--cmd", cmd,
            "--desc", f"工作流[{context.get('workflow_id','?')}] {name} · {agent}",
            "--uid", context.get("uid", "UID9622"),
            "--topic", "workflow.execution",
        ]
        r = subprocess.run(gov_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    else:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8", errors="ignore")

    result = {
        "status": "success" if r.returncode == 0 else "failed",
        "returncode": r.returncode,
        "stdout": r.stdout.strip(),
        "stderr": r.stderr.strip(),
    }
    run_log["steps"].append({"name": name, "agent": agent, "cmd": cmd, **result})
    return result


def cmd_init(args):
    ids = init_builtin_workflows()
    print(f"🐉 已初始化 {len(ids)} 个内置工作流")
    for wf_id in ids:
        print(f"   · {wf_id}")
    return 0


def cmd_list(args):
    ensure_dirs()
    files = sorted(WF_DIR.glob("*.json"))
    print(f"🐉 工作流列表 ({len(files)} 个)")
    for f in files:
        wf = load_json(f)
        print(f"  · {f.stem} | {wf.get('name','未命名')} | {wf.get('description','')[:60]}...")
    return 0


def cmd_show(args):
    path = WF_DIR / f"{args.workflow}.json"
    if not path.exists():
        print(f"❌ 工作流不存在: {args.workflow}")
        return 1
    wf = load_json(path)
    print(json.dumps(wf, ensure_ascii=False, indent=2))
    return 0


def cmd_run(args):
    path = WF_DIR / f"{args.workflow}.json"
    if not path.exists():
        print(f"❌ 工作流不存在: {args.workflow}")
        return 1
    wf = load_json(path)
    steps = wf.get("steps", [])
    if not steps:
        print("🟡 工作流无步骤")
        return 0

    context = {
        "workflow_id": args.workflow,
        "message": args.message or "",
        "uid": args.uid or "UID9622",
        "started_at": now_iso(),
    }
    run_id = f"{args.workflow}_{time.strftime('%Y%m%d_%H%M%S')}"
    run_log = {
        "run_id": run_id,
        "workflow": args.workflow,
        "dna": wf.get("dna", ""),
        "context": context,
        "started_at": now_iso(),
        "steps": [],
    }

    print(f"🐉 启动工作流: {wf.get('name', args.workflow)} ({len(steps)} 步)")
    print(f"   DNA: {wf.get('dna', '无')}")
    print(f"   输入: {args.message or '(空)'}")
    if args.dry_run:
        print("   模式: dry-run（不执行）")

    aborted = False
    for step in steps:
        result = run_step(step, context, run_log, dry_run=args.dry_run)
        if result["returncode"] != 0 and step.get("on_fail") == "abort":
            print(f"   🔴 步骤失败且 on_fail=abort，工作流中止")
            aborted = True
            break

    run_log["ended_at"] = now_iso()
    run_log["status"] = "aborted" if aborted else ("dry_run" if args.dry_run else "completed")
    log_path = WF_RUN_DIR / f"{run_id}.json"
    save_json(log_path, run_log)

    print(f"\n✅ 工作流结束: {run_log['status']}")
    print(f"   运行日志: {log_path}")
    return 1 if aborted else 0


def cmd_history(args):
    ensure_dirs()
    files = sorted(WF_RUN_DIR.glob("*.json"), reverse=True)[: args.limit]
    print(f"🐉 最近 {len(files)} 次工作流运行")
    for f in files:
        r = load_json(f)
        print(f"  · {r.get('run_id')} | {r.get('status')} | {r.get('started_at')} | 步骤 {len(r.get('steps',[]))}")
    return 0


def build_parser():
    p = argparse.ArgumentParser(description="🐉 龍魂多 Agent 协作工作流引擎 v1.0")
    sub = p.add_subparsers(dest="command")

    sub.add_parser("init", help="初始化内置工作流模板")
    sub.add_parser("list", help="列出工作流")

    sh = sub.add_parser("show", help="查看工作流定义")
    sh.add_argument("workflow", help="工作流 ID")

    run = sub.add_parser("run", help="运行工作流")
    run.add_argument("workflow", help="工作流 ID")
    run.add_argument("--message", "-m", default="", help="传入消息/上下文")
    run.add_argument("--uid", default="UID9622", help="执行主体 UID")
    run.add_argument("--dry-run", action="store_true", help="只打印不执行")

    hist = sub.add_parser("history", help="查看运行历史")
    hist.add_argument("--limit", type=int, default=10)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0
    ensure_dirs()
    handlers = {
        "init": cmd_init,
        "list": cmd_list,
        "show": cmd_show,
        "run": cmd_run,
        "history": cmd_history,
    }
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
