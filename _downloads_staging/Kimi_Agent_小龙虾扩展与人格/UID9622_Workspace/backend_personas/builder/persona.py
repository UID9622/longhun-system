#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宝宝·系统中枢 P-AK-BAOBAO
功能：
  1. 项目脚手架 / 模板库 / CNSH 命名规范检查 / 架构文档
  2. 系统中枢：解析老大意图 → 拆解任务 → 路由到各人格 → 汇总执行结果 → 生成报告
DNA: #BAOBAO-AGENT-CONFIG-20251214-001
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import AuditMark, DNATracer, SecurityFilter, TelemetryCollector, load_config, setup_logging, workspace_root


PERSONA_CODE = "BAOBAO"
PERSONA_NAME = "宝宝·系统中枢 P-AK-BAOBAO"
AGENT_DNA = "#BAOBAO-AGENT-CONFIG-20251214-001"

CONFIG = load_config()
WORKSPACE = Path(CONFIG.get("workspace", workspace_root()))
LOG_FILE = Path(CONFIG.get("logs_dir", WORKSPACE / "logs")) / "builder.log"
REPORT_DIR = WORKSPACE / "data" / "baobao" / "reports"
STATE_FILE = WORKSPACE / "data" / "baobao" / "system_state.json"
VERSION = "2.0.0"

CNSH_VAR = re.compile(r"^[a-z_][a-z0-9_]*$")
CNSH_FUNC = re.compile(r"^[a-z_][a-z0-9_]*$")
CNSH_CLASS = re.compile(r"^[A-Z][a-zA-Z0-9]*$")

TEMPLATES = {
    "python_basic": {
        "name": "Python 基础项目",
        "files": [
            "{name}/__init__.py",
            "{name}/main.py",
            "{name}/utils/__init__.py",
            "{name}/utils/helpers.py",
            "tests/__init__.py",
            "tests/test_main.py",
            "README.md",
            "requirements.txt",
        ],
    },
    "python_cli": {
        "name": "CLI 工具项目",
        "files": [
            "{name}/__init__.py",
            "{name}/cli.py",
            "{name}/core.py",
            "tests/test_cli.py",
            "README.md",
            "requirements.txt",
            "setup.py",
        ],
    },
    "web_api": {
        "name": "Web API 项目",
        "files": [
            "{name}/__init__.py",
            "{name}/app.py",
            "{name}/handlers.py",
            "tests/test_app.py",
            "README.md",
            "requirements.txt",
        ],
    },
    "longhun_module": {
        "name": "龍魂标准模块",
        "files": [
            "{name}/__init__.py",
            "{name}/module.py",
            "{name}/dna_tracker.py",
            "{name}/cns_checker.py",
            "README.md",
        ],
    },
    "persona_module": {
        "name": "后台人格模块",
        "files": [
            "{name}/persona.py",
            "{name}/system_prompt.md",
            "{name}/cron.conf",
            "README.md",
        ],
    },
}

# 历史目录名映射（与 uid9622-manager 保持一致）
_DIR_OVERRIDES = {
    "WENWEN": "wenwen",
    "SCOUT": "scout",
    "GUARDIAN": "guardian",
    "BAOBAO": "builder",
    "WENXIN": "sync_master",
    "ROUTER": "router",
}

SEQ_MARKERS = ["然后", "接着", "接下来", "之后", "最后", "再", "又", "并且", "并", "以及", "顺便", "还有", "和", " firstly ", " secondly ", " finally "]
PARALLEL_MARKERS = ["同时", "一起", "一并", "同步", "并行", "一块儿"]


def generate_dna(project_name: str) -> str:
    safe = re.sub(r"[^\w\-]", "_", project_name).lower()
    return f"#BAOBAO-BUILD-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{safe}-v{VERSION}"


def check_cns(path: Path) -> Dict:
    issues = []
    score = 100
    if not path.exists():
        return {"file": str(path), "passed": False, "score": 0, "issues": ["文件不存在"]}
    try:
        content = path.read_text(encoding="utf-8")
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            m = re.search(r"^class\s+(\w+)", s)
            if m and not CNSH_CLASS.match(m.group(1)):
                issues.append(f"第{i}行 类名 '{m.group(1)}' 应使用大驼峰")
                score -= 3
            m = re.search(r"^def\s+(\w+)", s)
            if m and not CNSH_FUNC.match(m.group(1)):
                issues.append(f"第{i}行 函数名 '{m.group(1)}' 应使用小写下划线")
                score -= 3
            m = re.search(r"^(\w+)\s*=", s)
            if m:
                var = m.group(1)
                if var not in {
                    "import", "from", "class", "def", "return", "if", "elif", "else",
                    "for", "while", "try", "except", "finally", "with", "as", "pass",
                    "break", "continue", "raise", "yield", "assert", "global", "nonlocal",
                    "lambda", "print", "True", "False", "None",
                } and not CNSH_VAR.match(var):
                    issues.append(f"第{i}行 变量名 '{var}' 应使用小写下划线")
                    score -= 2
    except Exception as e:
        issues.append(f"检查异常: {e}")
        score = 0
    return {"file": str(path), "passed": score >= 80, "score": max(0, score), "issues": issues}


def render_file_content(rel_path: str, project_name: str, dna: str) -> str:
    name = project_name
    if rel_path.endswith("__init__.py"):
        return f'#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n"""{name}\nDNA: {dna}\n"""\n'
    if "main.py" in rel_path or "app.py" in rel_path or "cli.py" in rel_path:
        return f'#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n"""{name} 主入口\nDNA: {dna}\n"""\n\ndef main():\n    print("{name} 启动成功")\n    print("DNA: {dna}")\n\nif __name__ == "__main__":\n    main()\n'
    if rel_path.endswith("README.md"):
        return f"# {name}\n\nDNA: {dna}\n\n## 说明\n\n由宝宝·系统中枢生成。\n"
    if rel_path.endswith("requirements.txt"):
        return "# 依赖列表\n"
    if rel_path.endswith("setup.py"):
        return (
            "from setuptools import setup, find_packages\n"
            f'setup(name="{name}", version="0.1.0", packages=find_packages())\n'
        )
    return f'#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n"""{Path(rel_path).name}\nDNA: {dna}\n"""\n'


def init_project(template: str, project_name: str, output_dir: Path, arch_doc: bool = False) -> Path:
    if template not in TEMPLATES:
        raise ValueError(f"未知模板: {template}。可用: {', '.join(TEMPLATES)}")
    target = output_dir / project_name
    target.mkdir(parents=True, exist_ok=True)
    dna = generate_dna(project_name)
    for rel in TEMPLATES[template]["files"]:
        rel_path = rel.format(name=project_name)
        f = target / rel_path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(render_file_content(rel_path, project_name, dna), encoding="utf-8")
    if arch_doc:
        (target / "ARCHITECTURE.md").write_text(
            f"# {project_name} 架构设计\n\nDNA: {dna}\n\n## 模块划分\n\n- 待补充\n",
            encoding="utf-8",
        )
    return target


def list_templates() -> str:
    lines = ["内置模板:"]
    for k, v in TEMPLATES.items():
        lines.append(f"  - {k}: {v['name']}")
    return "\n".join(lines)


# ==================== 系统中枢能力 ====================

def load_matrix() -> Dict[str, Any]:
    path = WORKSPACE / "backend_personas" / "persona_matrix.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_registry() -> Dict[str, Any]:
    path = WORKSPACE / "backend_personas" / "router" / "registry.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def dir_for_code(code: str) -> str:
    return _DIR_OVERRIDES.get(code.upper(), code.lower())


def score_keywords(text: str, keywords: List[str]) -> int:
    text = text.lower()
    score = 0
    for kw in keywords:
        kw = kw.lower()
        score += text.count(kw)
        if re.search(r"\b" + re.escape(kw) + r"\b", text):
            score += 2
    return score


def route_step(text: str, registry: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """返回 (target_type, winner_entry)。"""
    candidates = []
    for group in ["agents", "skills", "ipa_nodes"]:
        for entry in registry.get(group, []):
            keywords = entry.get("keywords", [])
            s = score_keywords(text, keywords)
            if s > 0:
                candidates.append({
                    "type": group.rstrip("s"),
                    "group": group,
                    "score": s,
                    **entry,
                })
    candidates.sort(key=lambda x: x["score"], reverse=True)
    if candidates:
        winner = candidates[0]
        return winner["type"], winner
    default = registry.get("default", {"code": "BAOBAO", "name": "宝宝·系统中枢"})
    return "default", {"type": "default", "score": 0, **default}


def decompose_intent(text: str) -> List[Dict[str, Any]]:
    """把老大的一句话拆成可执行步骤；支持并行标记。"""
    text = SecurityFilter.sanitize(text)
    # 去掉常见请求前缀，让路由更聚焦
    text = re.sub(r"^(请|帮我|给我|帮我一下|给我一下|我想|我要|需要|麻烦你)", "", text).strip()
    for m in PARALLEL_MARKERS:
        text = text.replace(m, "||")
    # 先按 || 分成并行组，再在各组内拆分顺序步骤
    groups = [g.strip() for g in text.split("||")]
    steps = []
    step_id = 1
    for gi, group in enumerate(groups):
        if not group:
            continue
        is_parallel = gi > 0
        for m in SEQ_MARKERS:
            group = group.replace(m, "|")
        parts = re.split(r"\|+|[。；;！!？?\n、,，]+", group)
        for p in parts:
            p = p.strip()
            if not p:
                continue
            steps.append({"id": step_id, "text": p, "parallel": is_parallel})
            step_id += 1
    return steps


def build_plan(intent: str, registry: Dict[str, Any]) -> Dict[str, Any]:
    steps = decompose_intent(intent)
    plan = {"intent": intent, "steps": [], "created_at": datetime.now(timezone.utc).isoformat()}
    for step in steps:
        target_type, winner = route_step(step["text"], registry)
        code = winner.get("code") or winner.get("id") or "BAOBAO"
        name = winner.get("name") or code
        plan["steps"].append({
            "id": step["id"],
            "text": step["text"],
            "parallel": step["parallel"],
            "target_type": target_type,
            "target_code": code,
            "target_name": name,
            "score": winner.get("score", 0),
        })
    return plan


# 人格专属调度参数：把自然语言步骤映射到各人格的 CLI
STEP_DISPATCH: Dict[str, callable] = {
    "WENWEN": lambda text: ["--scan-dir", str(WORKSPACE), "--auth-safe", "--report", "--dedup"],
    "GUARDIAN": lambda text: ["--check"],
    "SCOUT": lambda text: ["--keywords", text] if text else [],
    "WENXIN": lambda text: ["--full"] if "全量" in text or "完整" in text else [],
    "ROUTER": lambda text: ["--query", text, "--report"],
}


def build_step_args(step: Dict[str, Any]) -> List[str]:
    code = step["target_code"].upper()
    if code == PERSONA_CODE:
        return []
    fn = STEP_DISPATCH.get(code)
    if fn:
        return fn(step["text"])
    return ["--task", step["text"]]


def execute_step(step: Dict[str, Any], timeout: int = 120) -> Dict[str, Any]:
    code = step["target_code"]
    dname = dir_for_code(code)
    script = WORKSPACE / "backend_personas" / dname / "persona.py"
    if not script.exists():
        return {
            "step_id": step["id"],
            "target_code": code,
            "returncode": 1,
            "stdout": "",
            "stderr": f"脚本不存在: {script}",
        }
    if code.upper() == PERSONA_CODE:
        # 避免自我递归：中枢自己执行时，直接生成一条系统状态记录
        return {
            "step_id": step["id"],
            "target_code": code,
            "returncode": 0,
            "stdout": json.dumps({"note": "中枢直接承接，避免递归", "task": step["text"]}, ensure_ascii=False),
            "stderr": "",
        }
    args = build_step_args(step)
    try:
        result = subprocess.run(
            [sys.executable, str(script)] + args,
            cwd=str(WORKSPACE),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "step_id": step["id"],
            "target_code": code,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        return {
            "step_id": step["id"],
            "target_code": code,
            "returncode": 1,
            "stdout": "",
            "stderr": f"执行超时 ({timeout}s)",
        }
    except Exception as e:
        return {
            "step_id": step["id"],
            "target_code": code,
            "returncode": 1,
            "stdout": "",
            "stderr": str(e),
        }


def run_plan(plan: Dict[str, Any], telemetry: TelemetryCollector) -> List[Dict[str, Any]]:
    """按顺序/并行执行计划，并记录遥测与路由痕迹。"""
    results = []
    i = 0
    steps = plan["steps"]
    while i < len(steps):
        step = steps[i]
        telemetry.route(step["target_type"], step["target_code"], step["target_name"], step["score"], query=step["text"])

        if step["parallel"]:
            # 收集连续并行步骤
            group = [step]
            j = i + 1
            while j < len(steps) and steps[j]["parallel"]:
                group.append(steps[j])
                j += 1
            procs = []
            for s in group:
                code = s["target_code"]
                dname = dir_for_code(code)
                script = WORKSPACE / "backend_personas" / dname / "persona.py"
                args = build_step_args(s)
                if code.upper() == PERSONA_CODE or not script.exists():
                    procs.append((s, None, args))
                    continue
                p = subprocess.Popen(
                    [sys.executable, str(script)] + args,
                    cwd=str(WORKSPACE),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                procs.append((s, p, args))
            for s, p, _ in procs:
                if p is None:
                    res = execute_step(s)
                else:
                    try:
                        out, err = p.communicate(timeout=120)
                        res = {"step_id": s["id"], "target_code": s["target_code"], "returncode": p.returncode, "stdout": out.strip(), "stderr": err.strip()}
                    except subprocess.TimeoutExpired:
                        p.kill()
                        res = {"step_id": s["id"], "target_code": s["target_code"], "returncode": 1, "stdout": "", "stderr": "执行超时 (120s)"}
                results.append(res)
                telemetry.event("STEP_COMPLETE", {"step_id": s["id"], "target": s["target_code"], "status": "success" if res["returncode"] == 0 else "error"})
            i = j
        else:
            res = execute_step(step)
            results.append(res)
            telemetry.event("STEP_COMPLETE", {"step_id": step["id"], "target": step["target_code"], "status": "success" if res["returncode"] == 0 else "error"})
            i += 1
    return results


def generate_orchestration_report(plan: Dict[str, Any], results: List[Dict[str, Any]], report_dir: Path = None) -> Path:
    report_dir = report_dir or REPORT_DIR
    report_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    path = report_dir / f"baobao_orchestration_{ts}.md"

    success = sum(1 for r in results if r["returncode"] == 0)
    failed = len(results) - success

    lines = [
        "# 宝宝·系统中枢 · 任务执行报告\n",
        f"- 意图: {plan['intent']}",
        f"- 生成时间: {datetime.now(timezone.utc).isoformat()}",
        f"- DNA: {AGENT_DNA}",
        f"- 步骤总数: {len(plan['steps'])}",
        f"- 成功: {success} / 失败: {failed}\n",
        "## 执行计划\n",
    ]
    for s in plan["steps"]:
        pmark = "【并行】" if s["parallel"] else ""
        lines.append(f"{s['id']}. {pmark}[{s['target_type'].upper()}] {s['target_name']} ({s['target_code']}) → {s['text']}")
    lines.append("")

    lines.append("## 执行结果\n")
    for r in results:
        status = "✅" if r["returncode"] == 0 else "❌"
        lines.append(f"### 步骤 {r['step_id']} - {r['target_code']} {status}")
        lines.append(f"**返回码**: {r['returncode']}")
        if r["stdout"]:
            lines.append(f"**输出**:\n```\n{r['stdout'][:800]}\n```")
        if r["stderr"]:
            lines.append(f"**错误**:\n```\n{r['stderr'][:400]}\n```")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def update_system_state(plan: Dict[str, Any], results: List[Dict[str, Any]]):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    success = sum(1 for r in results if r["returncode"] == 0)
    state = {
        "last_run": datetime.now(timezone.utc).isoformat(),
        "intent": plan["intent"],
        "steps_total": len(plan["steps"]),
        "steps_success": success,
        "steps_failed": len(results) - success,
        "step_codes": [s["target_code"] for s in plan["steps"]],
        "dna": AGENT_DNA,
    }
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def system_health_check() -> Dict[str, Any]:
    """调用管理器做全系统健康检查。"""
    manager = WORKSPACE / "uid9622-manager"
    result = subprocess.run(
        [sys.executable, str(manager), "health-check"],
        cwd=str(WORKSPACE),
        capture_output=True,
        text=True,
        timeout=120,
    )
    return {
        "returncode": result.returncode,
        "output": result.stdout.strip(),
        "errors": result.stderr.strip(),
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(description=PERSONA_NAME)
    parser.add_argument("--list-templates", action="store_true", help="列出模板")
    parser.add_argument("--init", metavar="TEMPLATE", help="初始化项目模板")
    parser.add_argument("--project-name", default="my_project", help="项目名称")
    parser.add_argument("--output-dir", default=str(WORKSPACE / "projects"), help="输出目录")
    parser.add_argument("--arch-doc", action="store_true", help="生成架构文档")
    parser.add_argument("--cns-check", help="CNSH 规范检查文件路径")
    parser.add_argument("--health-check", action="store_true", help="自身健康检查")

    # 系统中枢参数
    parser.add_argument("--intent", help="老大的自然语言意图，中枢自动拆解并调度")
    parser.add_argument("--plan", action="store_true", help="只生成执行计划，不执行")
    parser.add_argument("--system-health", action="store_true", help="全系统健康检查")
    parser.add_argument("--report-dir", default=str(REPORT_DIR), help="报告输出目录")
    parser.add_argument("--verbose", action="store_true", help="详细日志")
    args = parser.parse_args()

    logger = setup_logging("builder", LOG_FILE, verbose=args.verbose)
    dna = DNATracer(PERSONA_CODE, AGENT_DNA)

    # 系统健康检查
    if args.system_health:
        with TelemetryCollector(PERSONA_CODE, PERSONA_NAME, operation_type="SYSTEM_HEALTH") as telemetry:
            logger.info(AuditMark.tag(AuditMark.PURPLE, PERSONA_NAME, "执行全系统健康检查"))
            result = system_health_check()
            telemetry.set_metrics({"health_passed": int(result["returncode"] == 0)})
            print(json.dumps(result, ensure_ascii=False, indent=2))
            logger.info(AuditMark.tag(AuditMark.GREEN if result["returncode"] == 0 else AuditMark.RED, PERSONA_NAME, "系统健康检查完成"))
        return

    # 意图调度中枢
    if args.intent:
        with TelemetryCollector(PERSONA_CODE, PERSONA_NAME, operation_type="ORCHESTRATE", query=args.intent) as telemetry:
            logger.info(AuditMark.tag(AuditMark.PURPLE, PERSONA_NAME, f"接收意图: {args.intent}"))
            registry = load_registry()
            plan = build_plan(args.intent, registry)
            plan_dna = dna.generate("PLAN")
            telemetry.event("PLAN_BUILT", {"steps": len(plan["steps"]), "dna": plan_dna})

            if args.plan:
                print(json.dumps(plan, ensure_ascii=False, indent=2))
                telemetry.set_metrics({"steps": len(plan["steps"]), "planned": 1})
                return

            results = run_plan(plan, telemetry)
            report_path = generate_orchestration_report(plan, results, Path(args.report_dir))
            update_system_state(plan, results)

            success = sum(1 for r in results if r["returncode"] == 0)
            failed = len(results) - success
            telemetry.set_metrics({"steps": len(plan["steps"]), "success": success, "failed": failed})

            logger.info(AuditMark.tag(AuditMark.GREEN if failed == 0 else AuditMark.YELLOW, PERSONA_NAME, f"执行完成 成功{success}/失败{failed} | 报告: {report_path}"))
            print(json.dumps({
                "intent": args.intent,
                "steps_total": len(plan["steps"]),
                "success": success,
                "failed": failed,
                "report": str(report_path),
                "dna": plan_dna,
            }, ensure_ascii=False, indent=2))
        return

    # 原有构建能力
    with TelemetryCollector(PERSONA_CODE, PERSONA_NAME) as telemetry:
        logger.info(AuditMark.tag(AuditMark.PURPLE, PERSONA_NAME, "启动"))

        if args.list_templates:
            telemetry.set_metrics({"action": "list_templates", "templates": len(TEMPLATES)})
            print(list_templates())
            return

        if args.health_check:
            telemetry.set_metrics({"action": "health_check", "checks_passed": 1})
            print(json.dumps({
                "code": PERSONA_CODE,
                "name": PERSONA_NAME,
                "status": "ok",
                "templates": list(TEMPLATES.keys()),
                "version": VERSION,
                "agent_dna": AGENT_DNA,
            }, ensure_ascii=False, indent=2))
            return

        if args.cns_check:
            result = check_cns(Path(args.cns_check))
            telemetry.set_metrics({"action": "cns_check", "score": result["score"], "passed": int(result["passed"]), "issues": len(result["issues"])})
            print(json.dumps(result, ensure_ascii=False, indent=2))
            logger.info(AuditMark.tag(AuditMark.GREEN if result["passed"] else AuditMark.YELLOW, PERSONA_NAME, f"CNSH 检查: {result['score']}分"))
            return

        if args.init:
            target = init_project(args.init, args.project_name, Path(args.output_dir), args.arch_doc)
            op_dna = generate_dna(args.project_name)
            template = TEMPLATES.get(args.init, {})
            telemetry.set_metrics({
                "action": "init_project",
                "projects_created": 1,
                "files_created": len(template.get("files", [])),
                "template": args.init,
            })
            logger.info(AuditMark.tag(AuditMark.GREEN, PERSONA_NAME, f"项目已生成: {target} DNA: {op_dna}"))
            print(f"项目已生成: {target}")
            print(f"DNA确认: {op_dna}")
            return

        parser.print_help()


if __name__ == "__main__":
    main()
