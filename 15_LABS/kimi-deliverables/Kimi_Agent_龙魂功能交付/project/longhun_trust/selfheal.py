# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-9db154d1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""龍魂信任核心 · 自愈引擎（检测→分析→修复→验证→回滚→耻辱墙）。

诚实边界焊死：
- 安全策略（dep_missing/service_down/log_oversize/stale_lock）才可自动执行，
  且 ``dry_run=True``（默认）只记录不执行；
- 断言失败/业务逻辑错误一律 ``strategy="ESCALATE"``，绝不自动生成代码补丁、
  绝不假装修复，升级人工 + 耻辱墙；
- 回滚必须先过确认码闸门（``verify_confirm_code``），快照用
  ``git tag lh-snapshot-<ts>``，回滚用 ``git reset --hard <tag>``，禁用 HEAD^。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from .audit import AuditLog
from .dna import generate_dna, verify_confirm_code
from .exceptions import ConfirmCodeError

PYTEST_TIMEOUT_SECONDS: int = 120
"""pytest 子进程超时（秒）。"""

LOG_TAIL_LINES: int = 100
"""日志扫尾行数。"""

MAX_TAIL_BYTES: int = 2 * 1024 * 1024
"""日志尾读字节窗口硬上限 2MB：任何病态输入（无换行/超长行）下
内存与耗时都有界，缓冲只保留最后一个窗口，更早内容直接丢弃。"""

LOG_MAX_BYTES: int = 50 * 1024 * 1024
"""日志超大阈值：50MB。"""

MODULE_NOT_FOUND_RE = re.compile(r"No module named '([^']+)'")
"""从 ModuleNotFoundError 提取模块名。"""

PACKAGE_NAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_.-]*$")
"""pip 包名白名单正则（防命令注入/选项注入：首字符必须是字母数字，
拒绝 ``-e``/``--user``/``..``/空串；pip 命令另行加 ``--`` 双保险）。"""

LOG_ERROR_RE = re.compile(r"\b(ERROR|CRITICAL|FATAL)\b|Traceback")
"""日志错误行匹配。"""

MODULE_ALIAS: dict[str, str] = {
    "PIL": "pillow",
    "yaml": "pyyaml",
    "cv2": "opencv-python",
    "bs4": "beautifulsoup4",
    "skimage": "scikit-image",
    "dotenv": "python-dotenv",
    "dateutil": "python-dateutil",
    "Crypto": "pycryptodome",
}
"""常见 import 名 → pip 包名映射；查不到映射就用原名。"""

SAFE_STRATEGIES: frozenset[str] = frozenset(
    {"pip_install", "service_restart", "log_rotate", "lock_remove"}
)
"""允许自动执行的安全策略；其余一律 ESCALATE。"""


class HealStatus(Enum):
    """自愈结果状态；值即 CLI 退出码（0/1/2，三色语义）。"""

    HEALTHY = 0  # 🟢 通过
    PARTIAL = 1  # 🟡 待确认或部分修复
    FAILED = 2  # 🔴 失败或熔断


@dataclass
class DetectedError:
    """一次检测到的问题。"""

    type: str  # test_failure | log_error | service_down | dep_missing | log_oversize | stale_lock
    message: str
    severity: str  # critical | warn（端口/lsof 缺失只许 warn）
    context: dict = field(default_factory=dict)


class SelfHealEngine:
    """自愈引擎：detect → plan → heal（快照→执行→复检→回滚）→ 耻辱墙。"""

    def __init__(
        self,
        project_root: Path,
        audit: AuditLog | None = None,
        dry_run: bool = True,
        max_attempts: int = 3,
        log_dir: Path | None = None,
        ports: list[int] | None = None,
    ) -> None:
        """初始化自愈引擎。

        :param project_root: 项目根目录（检测/快照/回滚的作用范围）。
        :param audit: 审计日志，默认 ``AuditLog("self_heal")``。
        :param dry_run: 干跑开关，默认 True（只记录不执行）；显式传 False 才执行修复。
        :param max_attempts: 连续失败阈值，达到即上耻辱墙并 status=FAILED。
        :param log_dir: 日志目录；heal 每轮 detect/复检都会扫描（默认 None 不扫）。
        :param ports: 待检测端口列表；heal 每轮 detect/复检都会探测（默认 None）。
        """
        self.project_root: Path = Path(project_root).resolve()
        self.audit: AuditLog = audit if audit is not None else AuditLog("self_heal")
        self.dry_run: bool = bool(dry_run)
        self.max_attempts: int = int(max_attempts)
        self.log_dir: Path | None = Path(log_dir) if log_dir is not None else None
        self.ports: list[int] | None = list(ports) if ports else None
        self._state_dir: Path = (
            Path(os.environ.get("LONGHUN_HOME", Path.home() / ".longhun")) / "08_STATE"
        )
        self._shame_wall_path: Path = self._state_dir / "shame_wall.jsonl"

    # ------------------------------------------------------------------ detect

    def detect(
        self,
        run_tests: bool = True,
        log_dir: Path | None = None,
        ports: list[int] | None = None,
    ) -> list[DetectedError]:
        """检测问题：pytest 子进程 + 日志扫尾 + 超大日志 + 残留锁 + 端口监听。

        :param run_tests: 是否在 project_root 下运行 pytest（超时 120s）。
        :param log_dir: 日志目录；扫描其中 ``*.log`` 尾部 100 行与文件体积。
        :param ports: 待检测端口列表；lsof 缺失或无监听一律 severity=warn。
        :return: 检测到的问题列表（可能为空）。
        """
        errors: list[DetectedError] = []
        if run_tests:
            errors.extend(self._detect_tests())
        if log_dir is not None:
            errors.extend(self._detect_logs(Path(log_dir)))
        errors.extend(self._detect_stale_locks(Path(log_dir) if log_dir else None))
        if ports:
            errors.extend(self._detect_ports(ports))
        self.audit.log(
            "DETECT",
            {
                "run_tests": run_tests,
                "log_dir": str(log_dir) if log_dir else None,
                "ports": ports,
                "found": len(errors),
                "types": [e.type for e in errors],
            },
        )
        return errors

    def _detect_tests(self) -> list[DetectedError]:
        """运行 pytest 子进程并解析失败（超时 120s，list 传参禁 shell）。

        :return: test_failure / dep_missing 问题列表。
        """
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "--tb=short"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=PYTEST_TIMEOUT_SECONDS,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return [
                DetectedError(
                    type="test_failure",
                    message=f"pytest 运行超时（{PYTEST_TIMEOUT_SECONDS}s）",
                    severity="critical",
                    context={"reason": "timeout"},
                )
            ]
        except OSError as exc:
            return [
                DetectedError(
                    type="test_failure",
                    message=f"pytest 无法运行：{exc}",
                    severity="critical",
                    context={"reason": str(exc)},
                )
            ]
        if proc.returncode in (0, 5):  # 0=全绿；5=未收集到测试（空项目不算错误）
            return []
        output = (proc.stdout or "") + "\n" + (proc.stderr or "")
        errors: list[DetectedError] = []
        seen_modules: set[str] = set()
        for match in MODULE_NOT_FOUND_RE.finditer(output):
            module = match.group(1)
            if module in seen_modules:
                continue
            seen_modules.add(module)
            errors.append(
                DetectedError(
                    type="dep_missing",
                    message=f"ModuleNotFoundError: No module named '{module}'",
                    severity="critical",
                    context={"module": module},
                )
            )
        seen_tests: set[str] = set()
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("FAILED "):
                node = line.split(" ", 1)[1].split(" - ")[0].strip()
                if node and node not in seen_tests:
                    seen_tests.add(node)
                    errors.append(
                        DetectedError(
                            type="test_failure",
                            message=line,
                            severity="critical",
                            context={"test": node},
                        )
                    )
        if not errors:
            errors.append(
                DetectedError(
                    type="test_failure",
                    message=f"pytest 退出码 {proc.returncode}（未解析出具体失败）",
                    severity="critical",
                    context={"returncode": proc.returncode},
                )
            )
        return errors

    def _detect_logs(self, log_dir: Path) -> list[DetectedError]:
        """扫描日志目录：超大日志（>50MB）与尾部 100 行错误关键字。

        :param log_dir: 日志目录。
        :return: log_oversize / log_error 问题列表。
        """
        errors: list[DetectedError] = []
        if not log_dir.is_dir():
            return errors
        for log_file in sorted(log_dir.glob("*.log")):
            if not log_file.is_file():
                continue
            try:
                size = log_file.stat().st_size
            except OSError:
                continue
            if size > LOG_MAX_BYTES:
                errors.append(
                    DetectedError(
                        type="log_oversize",
                        message=f"日志超大：{log_file.name} {size} 字节 > 50MB",
                        severity="warn",
                        context={"path": str(log_file), "size_bytes": size},
                    )
                )
            try:
                lines = self._tail_lines(log_file, LOG_TAIL_LINES)
            except OSError:
                continue
            matched = 0
            for line in lines:
                if matched >= 20:  # 单文件最多记 20 条，防爆量
                    break
                hit = LOG_ERROR_RE.search(line)
                if not hit:
                    continue
                matched += 1
                keyword = hit.group(0)
                severity = (
                    "critical"
                    if keyword in ("CRITICAL", "FATAL", "Traceback")
                    else "warn"
                )
                errors.append(
                    DetectedError(
                        type="log_error",
                        message=line.strip()[:500],
                        severity=severity,
                        context={"path": str(log_file), "keyword": keyword},
                    )
                )
        return errors

    @staticmethod
    def _tail_lines(
        path: Path, max_lines: int, block_size: int = 65536
    ) -> list[str]:
        """真正的尾部读取：seek 到末尾按块倒读，绝不整文件读入内存。

        字节窗口硬封顶 ``MAX_TAIL_BYTES``：倒读累计达到上限即停，
        缓冲只保留最后一个窗口（更早内容直接丢弃），在窗口内取最后
        ``max_lines`` 行。60MB 单行/超长行等病态输入下内存与耗时有界。

        :param path: 日志文件路径。
        :param max_lines: 最多返回的尾行数。
        :param block_size: 每次倒读的块字节数。
        :return: 尾部窗口内至多 max_lines 行（utf-8 解码，errors=replace）。
        """
        with path.open("rb") as fh:
            fh.seek(0, os.SEEK_END)
            remaining = fh.tell()
            window = min(remaining, MAX_TAIL_BYTES)
            buf = b""
            while window > 0 and buf.count(b"\n") <= max_lines:
                read_size = min(block_size, window)
                window -= read_size
                remaining -= read_size
                fh.seek(remaining)
                buf = fh.read(read_size) + buf
        return [
            chunk.decode("utf-8", errors="replace")
            for chunk in buf.splitlines()[-max_lines:]
        ]

    def _detect_stale_locks(self, log_dir: Path | None) -> list[DetectedError]:
        """检测残留锁文件（log_dir 与 project_root 顶层 ``*.lock``）。

        :param log_dir: 日志目录（可选）。
        :return: stale_lock 问题列表。
        """
        errors: list[DetectedError] = []
        dirs: list[Path] = []
        for candidate in (log_dir, self.project_root):
            if candidate is not None and candidate.is_dir() and candidate not in dirs:
                dirs.append(candidate)
        for directory in dirs:
            for lock in sorted(directory.glob("*.lock")):
                if lock.is_file():
                    errors.append(
                        DetectedError(
                            type="stale_lock",
                            message=f"残留锁文件：{lock}",
                            severity="warn",
                            context={"path": str(lock)},
                        )
                    )
        return errors

    def _detect_ports(self, ports: list[int]) -> list[DetectedError]:
        """检测端口监听。lsof 不存在或端口无监听一律 severity=warn（沙盒友好）。

        :param ports: 端口列表。
        :return: service_down 问题列表（仅 warn 级，永不 critical）。
        """
        errors: list[DetectedError] = []
        lsof = shutil.which("lsof")
        for port in ports:
            if lsof is None:
                errors.append(
                    DetectedError(
                        type="service_down",
                        message=f"端口 {port} 无法检测：lsof 不可用（沙盒环境）",
                        severity="warn",
                        context={"port": port, "reason": "lsof_missing"},
                    )
                )
                continue
            try:
                proc = subprocess.run(
                    [lsof, "-nP", "-i", f"TCP:{int(port)}", "-sTCP:LISTEN"],
                    capture_output=True,
                    text=True,
                    timeout=15,
                    check=False,
                )
            except (subprocess.TimeoutExpired, OSError) as exc:
                errors.append(
                    DetectedError(
                        type="service_down",
                        message=f"端口 {port} 检测失败：{exc}",
                        severity="warn",
                        context={"port": port, "reason": "detect_failed"},
                    )
                )
                continue
            if proc.returncode != 0 or not proc.stdout.strip():
                errors.append(
                    DetectedError(
                        type="service_down",
                        message=f"端口 {port} 无监听",
                        severity="warn",
                        context={"port": port, "reason": "no_listener"},
                    )
                )
        return errors

    # -------------------------------------------------------------------- plan

    def plan(self, errors: list[DetectedError]) -> list[dict]:
        """根据检测到的问题生成修复计划（真实可执行动作，非 echo 空壳）。

        策略表：dep_missing → pip install（白名单 + 别名映射）；
        service_down → 重启命令（仅记录，执行需 dry_run=False）；
        log_oversize → 轮转截断；stale_lock → 删除；
        其余（断言失败/业务逻辑）→ strategy="ESCALATE"，不生成修复动作。

        :param errors: detect 返回的问题列表。
        :return: 计划字典列表，每项含 strategy/action/safe/reason 等键。
        """
        plans = [self._plan_one(err) for err in errors]
        self.audit.log(
            "PLAN",
            {
                "count": len(plans),
                "strategies": [p["strategy"] for p in plans],
                "escalated": sum(1 for p in plans if p["strategy"] == "ESCALATE"),
            },
        )
        return plans

    def _plan_one(self, err: DetectedError) -> dict:
        """为单个问题生成计划。

        :param err: 检测到的问题。
        :return: 计划字典。
        """
        plan: dict[str, Any] = {
            "error_type": err.type,
            "message": err.message,
            "severity": err.severity,
            "context": dict(err.context),
            "strategy": "ESCALATE",
            "action": None,
            "target": None,
            "safe": False,
            "reason": "",
        }
        if err.type == "dep_missing":
            module = err.context.get("module") or self._extract_module(err.message)
            if not module:
                plan["reason"] = "无法从错误信息提取模块名，升级人工"
                return plan
            package = (
                MODULE_ALIAS.get(module)
                or MODULE_ALIAS.get(module.split(".", 1)[0])
                or module
            )
            if not PACKAGE_NAME_RE.match(package):
                plan["reason"] = f"包名 {package!r} 未过白名单校验，拒绝执行并升级人工"
                plan["context"]["rejected_package"] = package
                return plan
            plan.update(
                strategy="pip_install",
                action=[sys.executable, "-m", "pip", "install", "--", package],
                target=package,
                safe=True,
                reason=f"缺依赖 {module} → pip install {package}",
            )
        elif err.type == "service_down":
            restart_cmd = err.context.get("restart_cmd")
            if not restart_cmd:
                # 无命令却标 safe 等于假装可修：不计入可执行修复，直接升级人工。
                plan["reason"] = "未提供重启命令，无可执行修复动作，升级人工"
                plan["context"]["port"] = err.context.get("port")
                return plan
            plan.update(
                strategy="service_restart",
                action=list(restart_cmd),
                target=str(err.context.get("port", "")),
                safe=True,
                reason="记录重启命令，执行需 dry_run=False",
            )
        elif err.type == "log_oversize":
            plan.update(
                strategy="log_rotate",
                action=None,  # 进程内轮转截断，非子进程
                target=err.context.get("path"),
                safe=True,
                reason="日志超 50MB → 轮转为 .bak 并截断",
            )
        elif err.type == "stale_lock":
            plan.update(
                strategy="lock_remove",
                action=None,  # 进程内删除，非子进程
                target=err.context.get("path"),
                safe=True,
                reason="残留锁文件 → 删除",
            )
        else:
            plan["reason"] = (
                "断言失败/业务逻辑错误：绝不自动生成代码补丁，升级人工 + 耻辱墙"
            )
        return plan

    @staticmethod
    def _extract_module(message: str) -> str | None:
        """从 "ModuleNotFoundError: No module named 'X'" 提取 X。

        :param message: 错误信息。
        :return: 模块名或 None。
        """
        match = MODULE_NOT_FOUND_RE.search(message)
        return match.group(1) if match else None

    # -------------------------------------------------------------------- heal

    def heal(self, confirm_code: str | None = None) -> dict:
        """自愈主流程：detect → plan → 快照 → 执行安全策略 → 复检 → 报告。

        快照：project_root 是 git 仓库且将要真执行时，先打
        ``git tag lh-snapshot-<ts>``；非 git 仓库记审计 SNAPSHOT_SKIPPED。
        修复后仍有错 → 回滚到快照（必须 verify_confirm_code(confirm_code)，
        否则 PARTIAL 并保持现状）。连续 max_attempts 失败 → 耻辱墙 + FAILED。

        :param confirm_code: 确认码；仅当需要回滚时使用，缺失/错误则保持现状。
        :return: 报告 dict：{status, found, fixed, escalated, rolled_back,
            dry_run, details[], run_dna}。
        """
        run_dna = generate_dna("SELFHEAL")
        errors = self.detect(log_dir=self.log_dir, ports=self.ports)
        plans = self.plan(errors)
        executable = [p for p in plans if p["safe"]]
        will_execute = bool(executable) and not self.dry_run

        snapshot_tag: str | None = None
        snapshot_failed = False
        if will_execute:
            try:
                snapshot_tag = self._create_snapshot()
            except RuntimeError as exc:
                # fail-closed：快照打不出来就绝不碰用户代码，全部转升级人工。
                snapshot_failed = True
                self.audit.log(
                    "HEAL_ABORTED",
                    {"reason": f"快照失败，fail-closed 拒绝执行修复动作：{exc}"},
                )
                self._to_shame_wall(
                    "HEAL_ABORTED",
                    {
                        "error_type": "engine",
                        "message": f"快照失败，fail-closed 拒绝执行：{exc}",
                        "severity": "critical",
                        "context": {"executable": len(executable)},
                        "strategy": "ESCALATE",
                        "reason": "快照失败 fail-closed",
                    },
                    run_dna,
                )

        details: list[dict] = []
        fixed = 0
        escalated = 0
        failures = 0
        for plan in plans:
            if plan["strategy"] == "ESCALATE":
                escalated += 1
                self.audit.log(
                    "ESCALATE",
                    {"message": plan["message"], "reason": plan["reason"]},
                )
                self._to_shame_wall("ESCALATE", plan, run_dna)
                details.append({**plan, "executed": False, "result": "escalated"})
                continue
            if snapshot_failed:
                escalated += 1
                details.append(
                    {
                        **plan,
                        "executed": False,
                        "result": "aborted_snapshot_failed",
                        "reason": plan["reason"] + "；快照失败 fail-closed，拒绝执行",
                    }
                )
                continue
            if self.dry_run:
                details.append(
                    {**plan, "executed": False, "result": "dry_run_recorded"}
                )
                continue
            try:
                self._execute(plan)
            except Exception as exc:  # noqa: BLE001 修复失败必须记录而非中断整轮
                failures += 1
                self.audit.log(
                    "HEAL_FIX_FAILED",
                    {"strategy": plan["strategy"], "error": str(exc)},
                )
                details.append(
                    {**plan, "executed": True, "result": f"failed: {exc}"}
                )
            else:
                fixed += 1
                self.audit.log(
                    "HEAL_FIX",
                    {"strategy": plan["strategy"], "target": plan["target"]},
                )
                details.append({**plan, "executed": True, "result": "fixed"})

        rolled_back = False
        remaining_count: int | None = None
        if will_execute and not snapshot_failed:
            remaining = self.detect(log_dir=self.log_dir, ports=self.ports)
            remaining_count = len(remaining)
            if remaining:
                if confirm_code is not None and snapshot_tag is not None:
                    try:
                        rolled_back = self.rollback(snapshot_tag, confirm_code)
                    except ConfirmCodeError as exc:
                        self.audit.log("ROLLBACK_DENIED", {"reason": str(exc)})
                else:
                    self.audit.log(
                        "ROLLBACK_SKIPPED",
                        {
                            "reason": (
                                "未提供确认码或无快照，保持现状并升级人工"
                            ),
                            "remaining": remaining_count,
                        },
                    )

        rollback_note: str | None = None
        if rolled_back:
            side_effects = [
                f"{d['strategy']}({d.get('target')})"
                for d in details
                if d.get("executed") and d.get("result") == "fixed"
            ]
            rollback_note = (
                "回滚已恢复 git 工作区；但 git 之外的副作用"
                "（已装包/已轮转日志/已删未跟踪文件）无法自动撤销"
            )
            if side_effects:
                rollback_note += "；本轮已执行动作：" + "、".join(side_effects)
            fixed = 0  # 回滚发生后报告 fixed 必须清零，绝不自相矛盾

        if snapshot_failed:
            status = HealStatus.FAILED
        elif not errors:
            status = HealStatus.HEALTHY
        elif failures >= self.max_attempts:
            status = HealStatus.FAILED
            self._to_shame_wall(
                "CONSECUTIVE_FAILURES",
                {
                    "error_type": "engine",
                    "message": f"单轮修复连续失败 {failures} 次，达到阈值 "
                    f"{self.max_attempts}，熔断并升级人工",
                    "severity": "critical",
                    "context": {"failures": failures},
                    "strategy": "ESCALATE",
                    "reason": "连续失败熔断",
                },
                run_dna,
            )
        elif (
            remaining_count == 0
            and escalated == 0
            and failures == 0
            and not rolled_back
        ):
            status = HealStatus.HEALTHY  # 真执行后复检干净且全部修复
        else:
            status = HealStatus.PARTIAL

        report: dict[str, Any] = {
            "status": status.value,
            "status_label": status.name,
            "found": len(errors),
            "fixed": fixed,
            "escalated": escalated,
            "rolled_back": rolled_back,
            "rollback_note": rollback_note,
            "dry_run": self.dry_run,
            "snapshot_tag": snapshot_tag,
            "snapshot_failed": snapshot_failed,
            "details": details,
            "run_dna": run_dna,
            "timestamp": datetime.now().isoformat(),
        }
        self.audit.log(
            "HEAL_REPORT",
            {
                "status": status.value,
                "status_label": status.name,
                "found": report["found"],
                "fixed": fixed,
                "escalated": escalated,
                "rolled_back": rolled_back,
                "rollback_note": rollback_note,
                "dry_run": self.dry_run,
                "snapshot_tag": snapshot_tag,
                "run_dna": run_dna,
            },
        )
        return report

    def _execute(self, plan: dict) -> None:
        """执行单个安全策略（仅 dry_run=False 时由 heal 调用）。

        :param plan: 计划字典（strategy 必须在 SAFE_STRATEGIES 内）。
        :raises RuntimeError: 执行失败或策略不在安全白名单。
        """
        strategy = plan["strategy"]
        if strategy not in SAFE_STRATEGIES:
            raise RuntimeError(f"策略 {strategy} 不在安全白名单，拒绝执行")
        if strategy == "pip_install":
            package = plan["target"] or ""
            if not PACKAGE_NAME_RE.match(package):
                raise RuntimeError(f"包名 {package!r} 未过白名单校验，拒绝执行")
            proc = subprocess.run(
                list(plan["action"]),
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )
            if proc.returncode != 0:
                raise RuntimeError(
                    f"pip install {package} 失败：{(proc.stderr or '').strip()[-300:]}"
                )
        elif strategy == "service_restart":
            if not plan["action"]:
                raise RuntimeError("service_down 未提供重启命令，无法执行")
            proc = subprocess.run(
                list(plan["action"]),
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            if proc.returncode != 0:
                raise RuntimeError(
                    f"重启命令失败：{(proc.stderr or '').strip()[-300:]}"
                )
        elif strategy == "log_rotate":
            target = Path(plan["target"] or "")
            if not target.is_file():
                raise RuntimeError(f"日志文件不存在：{target}")
            # 备份名加纳秒 + pid，防同秒两次轮转互相覆盖。
            backup = target.with_name(
                f"{target.name}.{datetime.now().strftime('%Y%m%dT%H%M%S')}"
                f".{time.time_ns()}.{os.getpid()}.bak"
            )
            target.rename(backup)
            target.touch()
            shutil.copystat(backup, target)  # 保留原文件权限/时间戳
        elif strategy == "lock_remove":
            target = Path(plan["target"] or "")
            if target.suffix != ".lock":
                raise RuntimeError(f"目标不是 .lock 文件，拒绝删除：{target}")
            if not target.is_file():
                raise RuntimeError(f"锁文件不存在：{target}")
            target.unlink()

    # ---------------------------------------------------------- snapshot/rollback

    def _is_git_repo(self) -> bool:
        """判断 project_root 是否为 git 仓库（区分两类失败，fail-closed）。

        先文件系统探测 ``.git`` 存在性：
        - 无 ``.git`` → False（真非 git 仓，与 git 是否可用无关）；
        - 有 ``.git`` 且 rev-parse 确认在工作树内 → True；
        - 有 ``.git`` 但 git 子进程 OSError（不在 PATH）/超时/返回非零（如 .git
          损坏）→ 状态不确定，**绝不**返回 False（那会让真 git 仓被误判跳过快照、
          无快照裸奔执行修复），抛 RuntimeError（fail-closed）。

        :return: 确认是 git 仓库返回 True，确认不是返回 False。
        :raises RuntimeError: 存在 .git 但仓库状态无法确认（git 不可用/超时/损坏）。
        """
        has_git_dir = (self.project_root / ".git").exists()
        if not has_git_dir:
            return False
        try:
            proc = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
        except (subprocess.TimeoutExpired, OSError) as exc:
            raise RuntimeError(
                f"检测到 .git 目录但 git 不可用/超时（{exc}）："
                "仓库状态不确定，fail-closed 拒绝按非 git 仓处理"
            ) from exc
        if proc.returncode != 0:
            raise RuntimeError(
                f"检测到 .git 目录但 rev-parse 失败（rc={proc.returncode}）："
                f"{proc.stderr.strip()[:200]}。仓库可能损坏，"
                "fail-closed 拒绝按非 git 仓处理"
            )
        return proc.stdout.strip() == "true"

    def _git_checked(self, args: list[str], step: str) -> str:
        """运行 git 子命令，失败即 raise RuntimeError（快照流程 fail-closed）。

        :param args: git 参数列表（list 传参禁 shell）。
        :param step: 步骤名（用于错误信息）。
        :return: stdout。
        :raises RuntimeError: 命令超时/无法执行/退出码非零。
        """
        try:
            proc = subprocess.run(
                ["git", *args],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
        except (subprocess.TimeoutExpired, OSError) as exc:
            raise RuntimeError(f"{step} 无法执行：{exc}") from exc
        if proc.returncode != 0:
            raise RuntimeError(f"{step} 失败：{(proc.stderr or '').strip()}")
        return proc.stdout

    def _create_snapshot(self) -> str | None:
        """打真快照 tag ``lh-snapshot-<ts>``；非 git 仓库记 SNAPSHOT_SKIPPED。

        dirty worktree（含未跟踪文件）时先把工作区全部内容提交为快照 commit
        （``git add -A`` → ``write-tree`` → ``commit-tree``，不移动 HEAD），
        tag 指向该 commit——rollback 的 ``git reset --hard <tag>`` 才能完整
        恢复未提交修改与未跟踪文件。任何一步失败立即 raise（fail-closed），
        由 heal 拒绝执行修复动作，绝不碰用户代码。

        :return: 快照 tag 名；非 git 仓库返回 None。
        :raises RuntimeError: git 仓库内快照流程任一步失败，
            或检测到 .git 但 git 不可用（fail-closed，绝不误判跳过）。
        """
        try:
            is_repo = self._is_git_repo()
        except RuntimeError as exc:
            self.audit.log("SNAPSHOT_FAILED", {"reason": str(exc)})
            raise
        if not is_repo:
            self.audit.log(
                "SNAPSHOT_SKIPPED",
                {"reason": "project_root 非 git 仓库，跳过快照"},
            )
            return None
        tag = f"lh-snapshot-{datetime.now().strftime('%Y%m%dT%H%M%S%f')}"
        try:
            dirty = self._git_checked(
                ["status", "--porcelain"], "git status"
            ).strip()
            if dirty:
                # 真快照：工作区全部内容（含未跟踪文件）→ 快照 commit。
                self._git_checked(["add", "-A"], "git add -A")
                tree = self._git_checked(["write-tree"], "git write-tree").strip()
                commit_args = ["commit-tree", tree, "-m", "lh-snapshot"]
                head = subprocess.run(
                    ["git", "rev-parse", "--verify", "HEAD"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=15,
                    check=False,
                )
                if head.returncode == 0:
                    commit_args += ["-p", "HEAD"]
                commit = self._git_checked(
                    commit_args, "git commit-tree"
                ).strip()
                self._git_checked(["tag", tag, commit], "git tag")
            else:
                self._git_checked(["tag", tag], "git tag")
                commit = None
        except RuntimeError as exc:
            self.audit.log("SNAPSHOT_FAILED", {"reason": str(exc), "tag": tag})
            raise
        self.audit.log(
            "SNAPSHOT_CREATED",
            {"tag": tag, "dirty_worktree": bool(dirty), "snapshot_commit": commit},
        )
        return tag

    def rollback(self, snapshot_tag: str, confirm_code: str) -> bool:
        """回滚到快照：先过确认码闸门，再 ``git reset --hard <tag>``，写审计。

        禁用 HEAD^ 之类相对引用，只允许显式快照 tag。

        :param snapshot_tag: 快照 tag（lh-snapshot-<ts>）。
        :param confirm_code: 确认码，不匹配即抛 ConfirmCodeError。
        :return: 回滚成功返回 True。
        :raises ConfirmCodeError: 确认码错误（闸门拒绝）。
        """
        verify_confirm_code(confirm_code)
        try:
            is_repo = self._is_git_repo()
        except RuntimeError as exc:
            self.audit.log(
                "ROLLBACK_FAILED", {"tag": snapshot_tag, "reason": str(exc)}
            )
            return False
        if not is_repo:
            self.audit.log(
                "ROLLBACK_FAILED",
                {"tag": snapshot_tag, "reason": "project_root 非 git 仓库"},
            )
            return False
        proc = subprocess.run(
            ["git", "reset", "--hard", snapshot_tag],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if proc.returncode != 0:
            self.audit.log(
                "ROLLBACK_FAILED",
                {"tag": snapshot_tag, "reason": (proc.stderr or "").strip()},
            )
            return False
        self.audit.log("ROLLBACK", {"tag": snapshot_tag})
        return True

    # ------------------------------------------------------------ shame wall

    def _to_shame_wall(self, event: str, plan: dict, run_dna: str) -> dict:
        """耻辱墙：append-only 记录升级人工事项（绝不自动改业务代码）。

        :param event: 事件名（ESCALATE / CONSECUTIVE_FAILURES）。
        :param plan: 触发升级的计划字典。
        :param run_dna: 本轮自愈的 DNA 追溯码。
        :return: 写入的条目。
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "error_type": plan.get("error_type"),
            "message": plan.get("message"),
            "severity": plan.get("severity"),
            "reason": plan.get("reason"),
            "context": plan.get("context"),
            "run_dna": run_dna,
        }
        self._state_dir.mkdir(parents=True, exist_ok=True)
        with self._shame_wall_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        return entry


# ----------------------------------------------------------------------- CLI

_STATUS_EMOJI = {0: "🟢", 1: "🟡", 2: "🔴"}


def build_parser() -> argparse.ArgumentParser:
    """构建 CLI 参数解析器。

    :return: ArgumentParser。
    """
    parser = argparse.ArgumentParser(
        prog="python3 -m longhun_trust.selfheal",
        description="龍魂自愈引擎：检测→分析→修复→验证→回滚→耻辱墙。"
        "退出码 = HealStatus 值（🟢0 / 🟡1 / 🔴2）。",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--once", action="store_true", help="运行一轮自愈并出报告")
    mode.add_argument("--status", action="store_true", help="查看最近一次自愈报告状态")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="真执行安全策略（默认 dry_run 只记录不执行）",
    )
    parser.add_argument("--confirm-code", default=None, help="回滚确认码")
    parser.add_argument(
        "--project-root",
        default=None,
        help="项目根目录（默认当前目录）",
    )
    parser.add_argument(
        "--log-dir",
        default=None,
        help="日志目录：扫描其中 *.log 尾部 100 行错误关键字与超大日志",
    )
    parser.add_argument(
        "--ports",
        default=None,
        help="待检测端口，逗号分隔（如 8080,9090）；仅 warn 级",
    )
    return parser


def _parse_ports(raw: str | None) -> list[int] | None:
    """解析逗号分隔端口列表。

    :param raw: 形如 "8080,9090" 的字符串或 None。
    :return: 端口列表；未提供返回 None。
    :raises ValueError: 含非法端口（非数字或越界 1..65535）。
    """
    if not raw:
        return None
    ports: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        port = int(part)
        if not (1 <= port <= 65535):
            raise ValueError(f"端口越界（1..65535）：{port}")
        ports.append(port)
    return ports or None


def _clamp_exit_code(value: object) -> int:
    """退出码只允许 0/1/2；越界一律 clamp 到 2（🔴 失败语义）。

    :param value: 原始状态值。
    :return: 0/1/2 之一。
    """
    try:
        code = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return HealStatus.FAILED.value
    return code if code in (0, 1, 2) else HealStatus.FAILED.value


def _main(argv: list[str] | None = None) -> int:
    """CLI 主逻辑。退出码 = HealStatus 值（0/1/2）。

    :param argv: 参数列表（默认 sys.argv[1:]）。
    :return: 退出码。
    """
    args = build_parser().parse_args(argv)
    project_root = Path(args.project_root) if args.project_root else Path.cwd()

    if args.status:
        audit = AuditLog("self_heal")
        reports = [
            entry
            for entry in audit.read_all()
            if entry.get("event") == "HEAL_REPORT"
        ]
        if not reports:
            print("🟢 尚无自愈运行记录")
            return HealStatus.HEALTHY.value
        last = reports[-1]["details"]
        status_value = _clamp_exit_code(last.get("status", HealStatus.HEALTHY.value))
        emoji = _STATUS_EMOJI.get(status_value, "🔴")
        print(
            f"{emoji} 最近一次自愈：{last.get('status_label')} "
            f"found={last.get('found')} fixed={last.get('fixed')} "
            f"escalated={last.get('escalated')} rolled_back={last.get('rolled_back')} "
            f"dry_run={last.get('dry_run')} @ {reports[-1].get('timestamp')}"
        )
        return status_value

    engine = SelfHealEngine(
        project_root=project_root,
        dry_run=not args.execute,
        log_dir=Path(args.log_dir) if args.log_dir else None,
        ports=_parse_ports(args.ports),
    )
    report = engine.heal(confirm_code=args.confirm_code)
    emoji = _STATUS_EMOJI.get(report["status"], "🟡")
    print(
        f"{emoji} 自愈报告 status={report['status_label']}({report['status']}) "
        f"found={report['found']} fixed={report['fixed']} "
        f"escalated={report['escalated']} rolled_back={report['rolled_back']} "
        f"dry_run={report['dry_run']} snapshot={report['snapshot_tag']}"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return _clamp_exit_code(report["status"])


def main(argv: list[str] | None = None) -> int:
    """CLI 入口（兜底 guard）：未处理异常 → 打印错误摘要 + 退出码 2。

    :param argv: 参数列表（默认 sys.argv[1:]）。
    :return: 退出码（严格 0/1/2）。
    """
    try:
        return _main(argv)
    except Exception as exc:  # noqa: BLE001 CLI 边界兜底，绝不泄漏越界退出码
        print(
            f"🔴 自愈 CLI 未处理异常：{type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        return HealStatus.FAILED.value


if __name__ == "__main__":
    sys.exit(main())
