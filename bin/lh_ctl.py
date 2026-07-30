#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂引擎主控（lh-ctl）v1.0
DNA: #龍芯⚡️丙午·丙申·癸酉·庚申·临-LH-CTL-v1.0-7A3B9C2D
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

统一入口：一个 `lh` 命令调度所有引擎、统一日志、统一状态、统一输出。

用法:
  lh --help
  lh search "关键词"
  lh video --script 解说稿.txt --name demo
  lh distill --mock
  lh audit
  lh status
  lh logs --tail 20
  lh web
  lh schedule --help
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

from lh_ctl_config import load_config, logs_dir, state_dir, project_root

# 兼容直接运行与作为包导入
sys.path.insert(0, str(Path(__file__).resolve().parent))

CST = timezone(timedelta(hours=8))
DNA = "#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH-CTL-v1.0-7A3B9C2D"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

console = Console()


def _now() -> str:
    return datetime.now(CST).isoformat()


def _today_file() -> str:
    return datetime.now(CST).strftime("%Y-%m-%d")


def _job_id() -> str:
    return f"lh-{_today_file()}-{datetime.now(CST).strftime('%H%M%S')}-{uuid.uuid4().hex[:6]}"


def _ensure_dirs(cfg: Dict[str, Any]):
    logs_dir(cfg).mkdir(parents=True, exist_ok=True)
    state_dir(cfg).mkdir(parents=True, exist_ok=True)


# ═══════════════════════════════════════════════════════════
# 记忆层集成 — 每次执行自动写入当日记忆日志
# ═══════════════════════════════════════════════════════════

def _memory_dir(cfg: Dict[str, Any]) -> Path:
    """记忆层目录: longhun-system/.codebuddy/memory/"""
    return project_root(cfg) / ".codebuddy" / "memory"


def _memory_today(cfg: Dict[str, Any]) -> Path:
    """当日记忆日志: memory/YYYY-MM-DD.md"""
    return _memory_dir(cfg) / f"{_today_file()}.md"


def _log_to_memory(cfg: Dict[str, Any], job: Dict[str, Any]):
    """每次引擎执行后，自动追加一条记录到当日记忆日志。"""
    mem_file = _memory_today(cfg)
    mem_file.parent.mkdir(parents=True, exist_ok=True)

    started = job.get("started_at", "")[:19]
    cmd = job.get("command", "?")
    exit_code = job.get("exit_code", "?")
    summary = job.get("summary", "")
    job_id = job.get("job_id", "")
    mark = "✅" if exit_code == 0 else "❌"

    entry = f"\n| {started} | `lh {cmd}` | {mark} 退出{exit_code} | {summary[:80]} | `{job_id}` |"

    # 如果是当天第一次写入，先写表头
    write_header = not mem_file.exists()
    with open(mem_file, "a", encoding="utf-8") as f:
        if write_header:
            f.write(f"# 龍魂·执行日志 {_today_file()}\n\n")
            f.write("> 由 lh-ctl 自动生成。人工备注请在下方追加。\n\n")
            f.write("| 时间 | 命令 | 结果 | 摘要 | Job ID |\n")
            f.write("|:---|:---|:---:|:---|:---|\n")
        f.write(entry + "\n")


def _engine_map(cfg: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return cfg.get("engines", {})


def _engine_script_path(cfg: Dict[str, Any], name: str) -> Optional[Path]:
    engines = _engine_map(cfg)
    if name not in engines:
        return None
    rel = engines[name].get("script", f"bin/lh_{name}.py")
    return project_root(cfg) / rel


def _append_log(cfg: Dict[str, Any], record: Dict[str, Any]):
    d = logs_dir(cfg)
    f = d / f"{_today_file()}.log"
    with open(f, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def _append_job(cfg: Dict[str, Any], record: Dict[str, Any]):
    d = state_dir(cfg)
    f = d / "job_history.jsonl"
    with open(f, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def _read_job_history(cfg: Dict[str, Any], limit: int = 100, command: Optional[str] = None) -> List[Dict[str, Any]]:
    d = state_dir(cfg)
    f = d / "job_history.jsonl"
    if not f.exists():
        return []
    jobs: List[Dict[str, Any]] = []
    with open(f, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if command and rec.get("command") != command:
                continue
            jobs.append(rec)
    return jobs[-limit:]


def _build_args(name: str, kwargs: Dict[str, Any]) -> List[str]:
    """根据引擎类型构造命令行参数。"""
    args: List[str] = []
    if name == "search":
        query = kwargs.get("query", "")
        args = ["search", query]
        if kwargs.get("n"):
            args += ["--n", str(kwargs["n"])]
        if kwargs.get("deep"):
            args += ["--deep", str(kwargs["deep"])]
        if kwargs.get("output"):
            args += ["--output", kwargs["output"]]
    elif name == "video":
        if kwargs.get("script"):
            args += ["--script", kwargs["script"]]
        if kwargs.get("style"):
            args += ["--style", kwargs["style"]]
        if kwargs.get("name"):
            args += ["--name", kwargs["name"]]
    elif name == "distill":
        if kwargs.get("mock"):
            args.append("--mock")
        if kwargs.get("local"):
            args.append("--local")
    elif name == "audit":
        target = kwargs.get("target", "")
        if target:
            args.append(target)
    elif name == "3d":
        if kwargs.get("input"):
            args += ["--input", kwargs["input"]]
        if kwargs.get("category"):
            args += ["--category", kwargs["category"]]
        if kwargs.get("style"):
            args += ["--style", kwargs["style"]]
    return args


def _extract_summary(name: str, stdout: str, stderr: str, exit_code: int) -> str:
    """从输出中提取一句运行摘要。"""
    if exit_code != 0:
        err = (stderr or stdout).strip().split("\n")[-1]
        return f"运行失败: {err[:120]}"

    lines = [l.strip() for l in (stdout or "").split("\n") if l.strip()]
    if name == "search":
        for l in lines:
            if "找到" in l and "结果" in l:
                return l[:120]
            if "命中" in l:
                return l[:120]
        return "搜索完成"
    if name == "video":
        for l in lines:
            if "输出" in l or "完成" in l:
                return l[:120]
        return "视频处理完成"
    if name == "distill":
        for l in lines:
            if "完成" in l or "蒸馏" in l:
                return l[:120]
        return "蒸馏完成"
    if name == "audit":
        for l in lines:
            if "通过" in l or "失败" in l or "error" in l.lower():
                return l[:120]
        return "审计完成"
    return "运行完成"


def _run_engine(name: str, cfg: Dict[str, Any], **kwargs) -> int:
    """执行引擎脚本并记录日志。返回退出码。"""
    script = _engine_script_path(cfg, name)
    if not script or not script.exists():
        console.print(f"[red]未知引擎或脚本不存在: {name}[/red]")
        return 1

    args = _build_args(name, kwargs)
    cmd = [sys.executable, str(script)] + args
    cmd_str = " ".join(cmd)

    job = {
        "job_id": _job_id(),
        "command": name,
        "args": kwargs,
        "cmd": cmd_str,
        "started_at": _now(),
        "engine_id": f"ENG-{name.upper()}",
    }

    console.print(f"[dim]执行: {cmd_str}[/dim]")
    proc = subprocess.run(cmd, cwd=project_root(cfg), capture_output=True, text=True)

    finished_at = _now()
    summary = _extract_summary(name, proc.stdout, proc.stderr, proc.returncode)

    job.update({
        "finished_at": finished_at,
        "exit_code": proc.returncode,
        "summary": summary,
        "stdout_lines": len(proc.stdout.splitlines()) if proc.stdout else 0,
        "stderr_lines": len(proc.stderr.splitlines()) if proc.stderr else 0,
    })

    _append_log(cfg, job)
    _append_job(cfg, job)
    _log_to_memory(cfg, job)

    # 终端输出原引擎输出
    if proc.stdout:
        console.print(proc.stdout)
    if proc.stderr:
        console.print(proc.stderr, style="red")

    status = "[green]✅[/green]" if proc.returncode == 0 else "[red]❌[/red]"
    console.print(f"{status} {name} · {summary} · job_id={job['job_id']}")
    return proc.returncode


# ═══════════════════════════════════════════════════════════
# Click CLI
# ═══════════════════════════════════════════════════════════

@click.group(invoke_without_command=True)
@click.option("--version", is_flag=True, help="显示版本信息")
@click.pass_context
def cli(ctx, version):
    """🐉 龍魂引擎主控 — 一个入口，统一调度。"""
    if version:
        console.print(f"[gold1]{DNA}[/gold1]")
        return
    if ctx.invoked_subcommand is None:
        console.print(f"[gold1]{DNA}[/gold1]")
        console.print("\n[dim]输入 `lh --help` 查看所有命令[/dim]")


@cli.command()
@click.argument("query")
@click.option("--n", type=int, default=10, help="返回结果数")
@click.option("--deep", type=int, default=0, help="深度提取前N个页面")
@click.option("--output", type=click.Choice(["text", "json", "csv"]), default="text")
def search(query, n, deep, output):
    """龍魂搜索引擎。"""
    cfg = load_config()
    _ensure_dirs(cfg)
    sys.exit(_run_engine("search", cfg, query=query, n=n, deep=deep, output=output))


@cli.command()
@click.option("--script", required=True, help="解说稿文件路径")
@click.option("--style", default="龍魂", help="视频风格")
@click.option("--name", default="output", help="输出文件名")
def video(script, style, name):
    """龍魂视频工坊。"""
    cfg = load_config()
    _ensure_dirs(cfg)
    sys.exit(_run_engine("video", cfg, script=script, style=style, name=name))


@cli.command()
@click.option("--mock", is_flag=True, help="Mock 模式")
@click.option("--local", is_flag=True, help="使用本地模型")
def distill(mock, local):
    """K3 教师模型蒸馏。"""
    cfg = load_config()
    _ensure_dirs(cfg)
    sys.exit(_run_engine("distill", cfg, mock=mock, local=local))


def _audit_memory_self(cfg: Dict[str, Any]) -> int:
    """审计 MEMORY.md 完整性：DNA头·铁律·确认码·文件路径。"""
    mem_path = _memory_dir(cfg) / "MEMORY.md"
    if not mem_path.exists():
        console.print("[red]🔴 MEMORY.md 不存在！[/red]")
        return 1

    with open(mem_path, "r", encoding="utf-8") as f:
        content = f.read()

    checks = {
        "DNA头 #龍芯⚡️": "#龍芯⚡️" in content,
        "确认码 #CONFIRM": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z" in content,
        "UID9622身份": "UID9622" in content and "诸葛鑫" in content,
        "GPG指纹": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F" in content,
        "操作铁律表": "| # | 铁律 |" in content and "不删除只冻结" in content,
        "德本审计五问": "德在技术前" in content,
        "lh CLI统一入口": "lh search" in content and "lh web" in content,
        "核心协议引用": "P0_ETERNAL_LOCK" in content or "CONSTITUTION" in content,
        "人格矩阵": "P00" in content and "P72" in content,
        "底座369锚点": "369" in content and "sn=369" in content,
        "文件无恶意代码": "rm -rf" not in content.split("```")[::2] if "```" in content else True,
    }

    table = Table(title="🔍 记忆层自检 · MEMORY.md 完整性")
    table.add_column("检查项", style="cyan")
    table.add_column("结果", justify="center")

    all_pass = True
    for check, passed in checks.items():
        mark = "[green]✅[/green]" if passed else "[red]🔴[/red]"
        if not passed:
            all_pass = False
        table.add_row(check, mark)

    console.print(table)

    # 额外统计
    line_count = len(content.splitlines())
    file_size = mem_path.stat().st_size
    sections = content.count("## §")
    console.print(f"\n[dim]{line_count} 行 · {file_size}B · {sections} 节 · MEMORY.md v39.0[/dim]")

    if all_pass:
        console.print("\n[green]✅ 记忆层完整 · 全部检查通过[/green]")
        return 0
    else:
        console.print("\n[red]🔴 记忆层存在缺口 · 请修复后重新审计[/red]")
        return 1


@cli.command()
@click.argument("target", required=False, default="")
@click.option("--self", "audit_self", is_flag=True, help="审计记忆层本身 (MEMORY.md)")
def audit(target, audit_self):
    """语义安全闸审计。--self 审计记忆层本身。"""
    cfg = load_config()
    _ensure_dirs(cfg)

    if audit_self:
        sys.exit(_audit_memory_self(cfg))

    sys.exit(_run_engine("audit", cfg, target=target))


@cli.command(name="3d")
@click.option("--input", required=True, help="输入图像路径")
@click.option("--category", default="object", help="分类: object/character/building/nature/military")
@click.option("--style", default="realistic", help="风格: realistic/stylized")
def three_d(input, category, style):
    """龍魂图生三维引擎。"""
    cfg = load_config()
    _ensure_dirs(cfg)
    sys.exit(_run_engine("3d", cfg, input=input, category=category, style=style))


def _read_state_quick_card(cfg: Dict[str, Any]) -> Optional[List[Dict[str, str]]]:
    """从 STATE.md 读取快速状态卡（前30行表格）。返回行列表。"""
    state_path = project_root(cfg) / "STATE.md"
    if not state_path.exists():
        return None
    rows: List[Dict[str, str]] = []
    in_table = False
    with open(state_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            if line.startswith("## 快速状态卡"):
                in_table = True
                continue
            if in_table:
                if line.startswith("## "):
                    break
                if line.startswith("| ") and "---" not in line:
                    parts = [p.strip() for p in line.split("|") if p.strip()]
                    if len(parts) >= 2:
                        rows.append({"item": parts[0], "status": parts[1]})
    return rows if rows else None


@cli.command()
@click.option("--refresh", is_flag=True, help="从 Notion API 刷新数据")
@click.option("--limit", type=int, default=20, help="显示条数")
def status(refresh, limit):
    """查看系统状态与引擎注册表。先从 STATE.md 读取。"""
    cfg = load_config()
    _ensure_dirs(cfg)

    # ── 1. STATE.md 快速状态卡 ──
    quick = _read_state_quick_card(cfg)
    if quick:
        table = Table(title="🐉 龍魂 · STATE.md 快速状态卡")
        table.add_column("项目", style="cyan")
        table.add_column("状态")
        for row in quick[:20]:
            table.add_row(row["item"], row["status"])
        console.print(table)
        console.print()
    else:
        console.print("[dim]未找到 STATE.md 快速状态卡[/dim]")
        console.print()

    if refresh:
        console.print("[yellow]🔄 从 Notion 刷新状态...[/yellow]")
        # 调用 status_syncer 重新生成本地注册表
        syncer = project_root(cfg) / "bin" / "lh_notion_engine_status_syncer.py"
        subprocess.run([sys.executable, str(syncer)], cwd=project_root(cfg))

    registry_path = project_root(cfg) / "data" / "notion_sync" / "engines" / "engine_registry.json"
    integrity_path = project_root(cfg) / "data" / "notion_sync" / "engines" / "integrity_report.json"

    if not registry_path.exists():
        console.print("[red]注册表不存在，请先运行 `lh status --refresh`[/red]")
        return

    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    # 建立 path -> integrity result 索引
    health_index: Dict[str, int] = {}
    if integrity_path.exists():
        with open(integrity_path, "r", encoding="utf-8") as f:
            integrity = json.load(f)
        for r in integrity.get("results", []):
            path = r.get("path", "")
            if path:
                health_index[path] = _calc_health(r)

    table = Table(title=f"🐉 龍魂引擎注册表 · {registry.get('total_engines', 0)} 个引擎")
    table.add_column("引擎ID", style="cyan", no_wrap=True)
    table.add_column("名称")
    table.add_column("分类")
    table.add_column("子分类")
    table.add_column("类型")
    table.add_column("健康分", justify="right")
    table.add_column("状态", justify="center")

    engines = registry.get("engines", [])[:limit]
    for eng in engines:
        health = health_index.get(eng.get("path", ""), "-")
        health_str = str(health) if isinstance(health, int) else health
        table.add_row(
            eng.get("id", "")[:12],
            eng.get("name", "")[:20],
            eng.get("category", "")[:12],
            eng.get("subcategory", "")[:12],
            eng.get("type", ""),
            health_str,
            "[green]active[/green]" if eng.get("status") == "active" else eng.get("status", ""),
        )

    console.print(table)


def _calc_health(result: Dict[str, Any]) -> int:
    """根据 integrity_report 计算健康分（与 syncer 一致）。"""
    passed = result.get("passed", False)
    issues = result.get("issues", [])
    severity = result.get("severity", "unknown")
    score = 100
    if not passed:
        if severity == "critical":
            score -= 30
        elif severity == "high":
            score -= 20
        else:
            score -= 10
    score -= len(issues) * 5
    return max(0, min(100, score))


@cli.command()
@click.option("--tail", type=int, default=20, help="最近 N 条")
@click.option("--engine", type=click.Choice(["search", "video", "distill", "audit", "3d"]), help="按引擎过滤")
def logs(tail, engine):
    """查看聚合运行日志。"""
    cfg = load_config()
    _ensure_dirs(cfg)
    jobs = _read_job_history(cfg, limit=tail, command=engine)

    if not jobs:
        console.print("[dim]暂无运行日志[/dim]")
        return

    table = Table(title=f"📜 最近运行日志 · {len(jobs)} 条")
    table.add_column("时间", style="dim", no_wrap=True)
    table.add_column("命令", style="cyan")
    table.add_column("退出码", justify="center")
    table.add_column("摘要")

    for job in jobs:
        started = job.get("started_at", "")[11:19]
        cmd = job.get("command", "")
        code = job.get("exit_code", "")
        summary = job.get("summary", "")[:60]
        code_str = f"[green]{code}[/green]" if code == 0 else f"[red]{code}[/red]"
        table.add_row(started, cmd, code_str, summary)

    console.print(table)


@cli.command()
@click.option("--host", default=None, help="监听地址")
@click.option("--port", type=int, default=None, help="监听端口")
def web(host, port):
    """启动 Web 仪表盘。"""
    cfg = load_config()
    web_cfg = cfg.get("web", {})
    h = host or web_cfg.get("host", "127.0.0.1")
    p = port or web_cfg.get("port", 9630)

    web_script = Path(__file__).resolve().parent / "lh_ctl_web.py"
    if not web_script.exists():
        console.print("[red]Web 仪表盘脚本不存在: lh_ctl_web.py[/red]")
        return

    console.print(f"[green]启动 Web 仪表盘: http://{h}:{p}[/green]")
    subprocess.run([sys.executable, str(web_script), "--host", h, "--port", str(p)], cwd=project_root(cfg))


@cli.command()
@click.option("--today", "show_today", is_flag=True, help="查看今日执行日志")
@click.option("--tail", type=int, default=30, help="最近 N 天")
@click.option("--summary", is_flag=True, help="仅显示摘要统计")
def memory(show_today, tail, summary):
    """龍魂记忆层 — 查看/审计执行日志。"""
    cfg = load_config()
    mem_dir = _memory_dir(cfg)

    if show_today:
        today_path = _memory_today(cfg)
        if not today_path.exists():
            console.print(f"[dim]今日尚无执行日志: {today_path}[/dim]")
            return
        console.print(f"[gold1]📜 今日记忆 · {_today_file()}[/gold1]\n")
        with open(today_path, "r", encoding="utf-8") as f:
            console.print(f.read())
        return

    if summary:
        # 统计最近 N 天的执行情况
        if not mem_dir.exists():
            console.print("[dim]记忆目录不存在[/dim]")
            return
        logs = sorted(mem_dir.glob("202?-??-??.md"), reverse=True)[:tail]
        table = Table(title=f"📊 记忆层统计 · 最近 {len(logs)} 天")
        table.add_column("日期", style="cyan")
        table.add_column("条目数", justify="right")
        table.add_column("成功", justify="right")
        table.add_column("失败", justify="right")
        for log_file in logs:
            date_str = log_file.stem
            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read()
            total = content.count("| `lh ")
            success = content.count("✅")
            fail = content.count("❌")
            table.add_row(date_str, str(total), f"[green]{success}[/green]", f"[red]{fail}[/red]" if fail else "0")
        console.print(table)
        return

    # 默认：列出最近记忆文件
    if not mem_dir.exists():
        console.print("[dim]记忆目录不存在[/dim]")
        return
    logs = sorted(mem_dir.glob("202?-??-??.md"), reverse=True)[:tail]
    if not logs:
        console.print("[dim]暂无记忆日志[/dim]")
        return

    console.print(f"[gold1]📂 记忆层 · 最近 {len(logs)} 天[/gold1]\n")
    for log_file in logs:
        date_str = log_file.stem
        size = log_file.stat().st_size
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        entries = sum(1 for l in lines if l.startswith("| "))
        console.print(f"  [cyan]{date_str}[/cyan]  {entries} 条  {size}B")


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), add_help_option=False)
@click.pass_context
def schedule(ctx):
    """定时任务管理：add / list / remove / daemon。"""
    cfg = load_config()
    scheduler = Path(__file__).resolve().parent / "lh_ctl_scheduler.py"
    if not scheduler.exists():
        console.print("[red]调度器脚本不存在: lh_ctl_scheduler.py[/red]")
        return

    extra = [a for a in ctx.args if a not in ("schedule",)]
    subprocess.run([sys.executable, str(scheduler)] + extra, cwd=project_root(cfg))


def main():
    print(f"{DNA}\n{CONFIRM}\n")
    cli()


if __name__ == "__main__":
    main()
