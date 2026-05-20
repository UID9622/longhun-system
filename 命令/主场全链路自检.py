#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主场全链路自检 · CNSH DNA 路由自动跑
DNA: #龍芯⚡2026-05-20-HOME-FULL-CHAIN-AUTO-v1.0

用法:
  python3 命令/主场全链路自检.py          # 只查
  python3 命令/主场全链路自检.py --fix   # 查 + 能修的自动起服务
  bash 命令/主场全链路自检.sh [--fix]
"""
from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Optional

TZ8 = timezone(timedelta(hours=8))
DNA_RUN = "#龍芯⚡2026-05-20-HOME-FULL-CHAIN-AUTO-v1.0"


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def ts_utc8() -> str:
    return datetime.now(TZ8).strftime("%Y-%m-%dT%H:%M:%S%z")


def dr_digits(text: str) -> int:
    digits = re.sub(r"\D", "", text)
    if not digits:
        return 0
    s = sum(int(c) for c in digits)
    while s >= 10:
        s = sum(int(c) for c in str(s))
    return 9 if s == 0 else s


@dataclass
class CheckItem:
    id: str
    name: str
    status: str  # green | yellow | red
    detail: str
    fix: str = ""


@dataclass
class RunReport:
    dna: str = DNA_RUN
    ts: str = field(default_factory=ts_utc8)
    items: List[CheckItem] = field(default_factory=list)
    fixes_applied: List[str] = field(default_factory=list)

    def add(self, item: CheckItem) -> None:
        self.items.append(item)

    @property
    def ok(self) -> bool:
        return not any(i.status == "red" for i in self.items)


def port_listen(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", port)) == 0


def http_ok(url: str, timeout: float = 2.0) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return 200 <= r.status < 400
    except (urllib.error.URLError, OSError):
        return False


def run_cmd(cmd: List[str], cwd: Optional[Path] = None, timeout: int = 120) -> tuple[int, str]:
    p = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    out = (p.stdout or "") + (p.stderr or "")
    return p.returncode, out.strip()


def ensure_engine_symlink(root: Path, report: RunReport) -> None:
    eng = root / "engine"
    target = root / "引擎"
    if eng.is_symlink() and eng.resolve() == target.resolve():
        report.add(CheckItem("path_engine", "engine→引擎 软链", "green", "已对齐"))
        return
    if eng.exists() and not eng.is_symlink():
        report.add(
            CheckItem(
                "path_engine",
                "engine 路径",
                "red",
                "存在 engine 但不是指向 引擎 的软链",
                f"rm -rf engine && ln -s 引擎 engine  （在 {root}）",
            )
        )
        return
    if target.is_dir():
        try:
            eng.symlink_to("引擎", target_is_directory=True)
            report.fixes_applied.append("ln -s 引擎 engine")
            report.add(CheckItem("path_engine", "engine→引擎 软链", "green", "已自动创建"))
        except OSError as e:
            report.add(CheckItem("path_engine", "engine→引擎 软链", "red", str(e)))
    else:
        report.add(CheckItem("path_engine", "引擎目录", "red", "缺少 引擎/"))


def _notion_token_ok(path: Path) -> bool:
    if not path.is_file():
        return False
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip().startswith("NOTION_TOKEN="):
            v = line.split("=", 1)[1].strip().strip('"').strip("'")
            return v.startswith("ntn_") and len(v) > 10
    return False


def check_secrets(root: Path, report: RunReport) -> None:
    home_sec = Path.home() / ".longhun" / "secrets.env"
    eng_env = root / "engine" / ".env"
    home_ok = _notion_token_ok(home_sec)
    eng_ok = _notion_token_ok(eng_env)
    if home_ok or eng_ok:
        where = []
        if home_ok:
            where.append("~/.longhun/secrets.env")
        if eng_ok:
            where.append("engine/.env")
        report.add(
            CheckItem("secrets_notion", "Notion 密钥", "green", "已填 · " + " · ".join(where))
        )
    else:
        report.add(
            CheckItem(
                "secrets_notion",
                "Notion 密钥",
                "yellow",
                "两处都未填 ntn_（接单台同步会卡）",
                "bash ~/longhun-system/bin/帮你打开密钥填写",
            )
        )
    if not home_sec.is_file():
        report.add(
            CheckItem(
                "secrets_home",
                "~/.longhun/secrets.env",
                "yellow" if eng_ok else "yellow",
                "文件不存在（可选·与 engine/.env 二选一）",
                "bash ~/longhun-system/bin/登记密钥说明.sh",
            )
        )
    elif not home_ok and eng_ok:
        report.add(
            CheckItem(
                "secrets_home",
                "~/.longhun/secrets.env",
                "green",
                "未填但 engine/.env 已有 · 本机够用",
            )
        )


def check_port(
    report: RunReport,
    pid: str,
    name: str,
    port: int,
    health_url: Optional[str],
    start_cmd: Optional[List[str]],
    do_fix: bool,
    root: Path,
) -> None:
    if port_listen(port):
        if health_url and not http_ok(health_url):
            report.add(
                CheckItem(pid, name, "yellow", f"端口 {port} 在听但 {health_url} 未 200")
            )
        else:
            report.add(CheckItem(pid, name, "green", f"端口 {port} OK"))
        return
    if do_fix and start_cmd:
        report.fixes_applied.append(" ".join(start_cmd))
        code, out = run_cmd(start_cmd, cwd=root)
        import time

        time.sleep(2)
        if port_listen(port):
            report.add(CheckItem(pid, name, "green", f"已自动启动 :{port}"))
            return
        report.add(
            CheckItem(pid, name, "red", f"启动失败 code={code}", out[-400:] if out else "")
        )
        return
    fix = ""
    if start_cmd:
        fix = "bash " + " ".join(str(x) for x in start_cmd[1:] if str(x).startswith("/") or "/" in str(x))
        if pid == "p9625":
            fix = f"bash {root}/bin/开龍魂9625"
        elif pid == "p8765":
            fix = f"bash {root}/bin/开操作台"
    report.add(CheckItem(pid, name, "yellow" if pid != "p9625" else "red", f"端口 {port} 未监听", fix))


def check_skills(root: Path, report: RunReport) -> None:
    sh = root / "命令" / "龍魂技能.sh"
    if not sh.is_file():
        report.add(CheckItem("skills", "v3 四 Skill", "red", "缺少 命令/龍魂技能.sh"))
        return
    code, out = run_cmd(["bash", str(sh), "all-test"], cwd=root, timeout=90)
    if code == 0 and "28/28" in out:
        report.add(CheckItem("skills", "v3 四 Skill", "green", "28/28 全过"))
    else:
        report.add(CheckItem("skills", "v3 四 Skill", "red", f"exit={code}", out[-500:]))


def check_cnsh_tests(root: Path, report: RunReport) -> None:
    py = root / "venv" / "bin" / "python"
    if not py.is_file():
        report.add(CheckItem("cnsh_pytest", "CNSH 单测", "red", "无 venv"))
        return
    tests = [
        "CNSH/gate_v3/tests",
        "CNSH/flow_field/tests",
        "CNSH/algorithms/tests",
        "CNSH/root_ratio/tests",
        "CNSH/sovereign/tests",
    ]
    existing = [t for t in tests if (root / t).is_dir()]
    if not existing:
        report.add(CheckItem("cnsh_pytest", "CNSH 单测", "red", "测试目录不存在"))
        return
    env = {**os.environ, "PYTHONPATH": str(root)}
    code, out = run_cmd(
        [str(py), "-m", "pytest", *existing, "-q"],
        cwd=root,
        timeout=180,
    )
    if code == 0:
        report.add(CheckItem("cnsh_pytest", "CNSH 单测", "green", f"{len(existing)} 包通过"))
    else:
        report.add(
            CheckItem(
                "cnsh_pytest",
                "CNSH 单测",
                "red",
                f"pytest exit={code}",
                f"bash {root}/bin/run_cnsh_tests.sh",
            )
        )


def check_region_sovereignty(root: Path, report: RunReport) -> None:
    py = root / "venv" / "bin" / "python"
    if not py.is_file():
        report.add(CheckItem("region_q0", "地区主权 Q0", "yellow", "无 venv"))
        return
    code, out = run_cmd([str(py), str(root / "命令" / "sanity_check.py")], cwd=root, timeout=60)
    if code == 0:
        report.add(CheckItem("region_q0", "地区主权 Q0", "green", "sanity_check PASS"))
    else:
        report.add(
            CheckItem(
                "region_q0",
                "地区主权 Q0",
                "red",
                "sanity_check FAIL",
                f"source {root}/bin/sovereignty_init.sh && {py} {root}/命令/sanity_check.py",
            )
        )


def check_semlayer(root: Path, report: RunReport) -> None:
    base = root / "cnsh-semlayer-runtime"
    mr = base / "core" / "mode_router.ts"
    spec = root / "CNSH核心" / "规范" / "CNSH-SEMLAYER-Runtime-v1.4-主权重写.md"
    if mr.is_file() and spec.is_file():
        report.add(CheckItem("semlayer", "SEMLAYER v1.4", "green", "总纲+mode_router 在仓"))
    elif mr.is_file():
        report.add(CheckItem("semlayer", "SEMLAYER v1.4", "green", "mode_router.ts 在仓"))
    else:
        report.add(CheckItem("semlayer", "SEMLAYER v1.4", "yellow", "骨架未落仓"))


def check_bin_aliases(root: Path, report: RunReport) -> None:
    """zshrc 里常引用的脚本是否存在（bin→命令）"""
    bin_dir = root / "bin"
    missing = []
    for name in (
        "开龍魂9625",
        "开操作台",
        "龍魂技能.sh",
        "主场全链路自检.sh",
        "api_check.sh",
        "帮你检查全部",
    ):
        p = bin_dir / name
        if not p.exists():
            missing.append(name)
    if missing:
        report.add(
            CheckItem(
                "bin_cmds",
                "命令入口",
                "yellow",
                "缺失: " + ", ".join(missing),
                f"检查 {bin_dir} 软链",
            )
        )
    else:
        report.add(CheckItem("bin_cmds", "命令入口", "green", "核心脚本齐全"))


def check_console_html(root: Path, report: RunReport) -> None:
    html = (
        root
        / "00_main_control"
        / "操作台v3"
        / "components"
        / "龍魂操作台_MVP_v1.html"
    )
    if html.is_file():
        report.add(CheckItem("console_html", "操作台 HTML", "green", str(html.relative_to(root))))
    else:
        report.add(
            CheckItem(
                "console_html",
                "操作台 HTML",
                "yellow",
                "MVP html 不在默认路径（8765 可能 404）",
                "恢复 00_main_control/操作台v3/components/ 或改 开操作台 URL",
            )
        )


def write_trace(root: Path, report: RunReport) -> Path:
    log_dir = root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / "home_full_chain_trace.jsonl"
    row = {
        "ts": report.ts,
        "dna": report.dna,
        "dr": dr_digits(report.dna),
        "ok": report.ok,
        "items": [asdict(i) for i in report.items],
        "fixes": report.fixes_applied,
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path


def print_cheatsheet(root: Path, report: RunReport) -> None:
    """老大只记三条 · 其余都归在这一条下面"""
    print("\n┌─ 老大只记三条（别的不用背）────────────────────")
    print("│  ① 全检     bash ~/longhun-system/bin/主场全链路自检.sh --fix")
    print("│  ② 看菜单   bash ~/longhun-system/bin/显示常用指令")
    print("│  ③ 全开     bash ~/longhun-system/bin/爸爸一键全开.sh")
    print("└──────────────────────────────────────────────")
    print("  终端省事: source ~/longhun-system/加载环境.sh  →  打「全检」「指令」")
    print("  浏览器:   http://127.0.0.1:9625/console  ·  操作台 :8765")
    yellows = [i for i in report.items if i.status == "yellow"]
    if yellows:
        print("\n  本次 🟡（可不管 / 按需）:")
        for it in yellows:
            print(f"    · {it.name}: {it.detail}")
            if it.fix:
                print(f"      → {it.fix}")


def print_report(report: RunReport) -> None:
    icon = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
    print("════════════════════════════════════════")
    print("  🐉 主场全链路自检")
    print(f"  时间: {report.ts}")
    print(f"  DNA:  {report.dna}")
    print(f"  dr:   {dr_digits(report.dna)}")
    print("════════════════════════════════════════")
    for it in report.items:
        print(f"{icon.get(it.status, '⚪')} [{it.id}] {it.name}")
        print(f"    {it.detail}")
        if it.fix and it.status != "green":
            print(f"    → {it.fix}")
    if report.fixes_applied:
        print("\n── 已自动修复 ──")
        for f in report.fixes_applied:
            print(f"  · {f}")
    print("════════════════════════════════════════")
    n_r = sum(1 for i in report.items if i.status == "red")
    n_y = sum(1 for i in report.items if i.status == "yellow")
    n_g = sum(1 for i in report.items if i.status == "green")
    print(f"合计: 🟢{n_g} 🟡{n_y} 🔴{n_r}")
    print("════════════════════════════════════════")


def main() -> int:
    do_fix = "--fix" in sys.argv
    root = repo_root()
    report = RunReport()

    ensure_engine_symlink(root, report)
    check_secrets(root, report)
    check_bin_aliases(root, report)
    check_console_html(root, report)

    bin_sh = root / "bin"
    check_port(
        report,
        "p9625",
        "龍魂引擎 9625",
        9625,
        "http://127.0.0.1:9625/api/health",
        ["bash", str(bin_sh / "开龍魂9625")] if (bin_sh / "开龍魂9625").exists() else None,
        do_fix,
        root,
    )
    check_port(
        report,
        "p8765",
        "操作台 8765",
        8765,
        "http://127.0.0.1:8765/",
        ["bash", str(bin_sh / "开操作台")] if (bin_sh / "开操作台").exists() else None,
        do_fix,
        root,
    )
    check_port(
        report,
        "p11434",
        "Ollama 11434",
        11434,
        "http://127.0.0.1:11434/api/tags",
        None,
        False,
        root,
    )
    check_port(report, "p9623", "Notion MCP 9623", 9623, "http://127.0.0.1:9623/health", None, do_fix, root)

    check_skills(root, report)
    check_cnsh_tests(root, report)
    check_region_sovereignty(root, report)
    check_semlayer(root, report)

    trace = write_trace(root, report)
    print_report(report)
    print_cheatsheet(root, report)
    print(f"\n留痕: {trace}")
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
