# DNA: #龍芯⚡️丙午·丙申·甲子·甲戌·䷍大有-CODE-补DNA-0527c250
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""test_selfheal.py — 自愈引擎测试（锚点9、锚点10 + 真实 git/pytest 行为测试）。

隔离铁律：全程 tmp_path / monkeypatch，不碰真实 home、不真执行 pip/launchctl；
快照与回滚逻辑用 tmp_path 内 git init 真建仓真测。
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

from longhun_trust.audit import AuditLog
from longhun_trust.dna import CONFIRM_CODE
from longhun_trust.exceptions import ConfirmCodeError
from longhun_trust.selfheal import (
    MAX_TAIL_BYTES,
    PACKAGE_NAME_RE,
    DetectedError,
    HealStatus,
    SelfHealEngine,
    _parse_ports,
    build_parser,
    main,
)


@pytest.fixture
def isolated_home(tmp_path, monkeypatch) -> object:
    """LONGHUN_HOME 隔离到 tmp_path，禁止污染真实 home。"""
    home = tmp_path / "longhun_home"
    monkeypatch.setenv("LONGHUN_HOME", str(home))
    return home


@pytest.fixture
def project(tmp_path) -> object:
    """空项目根（非 git 仓库，pytest 收集不到用例 → 退出码 5 不算错误）。"""
    root = tmp_path / "proj"
    root.mkdir()
    return root


@pytest.fixture
def engine(project, isolated_home, tmp_path) -> SelfHealEngine:
    """审计目录同样隔离到 tmp_path 的引擎实例。"""
    audit = AuditLog("self_heal", base_dir=tmp_path / "audit")
    return SelfHealEngine(project_root=project, audit=audit)


@pytest.fixture
def git_repo(tmp_path):
    """在 tmp_path 里 git init 真建仓：一个已提交文件，返回路径。"""

    def run(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *args],
            cwd=repo,
            capture_output=True,
            text=True,
            check=True,
        )

    repo = tmp_path / "gitproj"
    repo.mkdir()
    run("init")
    run("config", "user.email", "test@longhun.local")
    run("config", "user.name", "longhun-test")
    (repo / "app.py").write_text("VALUE = 1\n", encoding="utf-8")
    run("add", "-A")
    run("commit", "-m", "init")
    return repo


def make_error(type_: str, message: str, severity: str = "critical", **context):
    """构造 DetectedError 的测试辅助。"""
    return DetectedError(type=type_, message=message, severity=severity, context=context)


# --------------------------------------------------------------------- 锚点9


class TestAnchor9PlanAndDryRun:
    """锚点9：dry_run 默认 True；dep_missing → pip 策略；断言失败 → ESCALATE。"""

    def test_dry_run_default_true(self, engine: SelfHealEngine):
        """锚点9a：dry_run 默认 True（干跑，只记录不执行）。"""
        assert engine.dry_run is True
        assert engine.max_attempts == 3

    def test_plan_dep_missing_pip_install(self, engine: SelfHealEngine):
        """锚点9b：ModuleNotFoundError → pip install 策略，PIL 映射 pillow。"""
        err = make_error(
            "dep_missing", "ModuleNotFoundError: No module named 'PIL'"
        )
        (plan,) = engine.plan([err])
        assert plan["strategy"] == "pip_install"
        assert plan["safe"] is True
        assert plan["target"] == "pillow"
        assert plan["action"][:3] == [sys.executable, "-m", "pip"]
        assert plan["action"][-1] == "pillow"
        assert all(PACKAGE_NAME_RE.match(part) for part in plan["action"][-1:])

    def test_plan_alias_yaml_and_unknown_original(self, engine: SelfHealEngine):
        """锚点9c：别名表命中（yaml→pyyaml）；查不到映射用原名。"""
        (p1,) = engine.plan(
            [make_error("dep_missing", "ModuleNotFoundError: No module named 'yaml'")]
        )
        assert p1["target"] == "pyyaml"
        (p2,) = engine.plan(
            [make_error("dep_missing", "ModuleNotFoundError: No module named 'foo_bar'")]
        )
        assert p2["target"] == "foo_bar"
        assert p2["strategy"] == "pip_install"

    def test_plan_assertion_failure_escalates(self, engine: SelfHealEngine):
        """锚点9d：断言失败类 → ESCALATE 且无修复命令（绝不自动改代码）。"""
        err = make_error(
            "test_failure",
            "FAILED tests/test_x.py::test_y - AssertionError: assert 16 == 18",
        )
        (plan,) = engine.plan([err])
        assert plan["strategy"] == "ESCALATE"
        assert plan["action"] is None
        assert plan["safe"] is False
        assert "升级人工" in plan["reason"]

    def test_plan_malicious_package_rejected(self, engine: SelfHealEngine):
        """锚点9e：包名未过白名单正则 → 拒绝执行并 ESCALATE（防命令注入）。"""
        err = make_error(
            "dep_missing", "ModuleNotFoundError: No module named 'foo;id'", module="foo;id"
        )
        (plan,) = engine.plan([err])
        assert plan["strategy"] == "ESCALATE"
        assert plan["safe"] is False
        assert plan["action"] is None


# -------------------------------------------------------------------- 锚点10


class TestAnchor10RollbackGateAndExitCodes:
    """锚点10：rollback 无确认码 → ConfirmCodeError；退出码枚举值 0/1/2。"""

    def test_rollback_wrong_code_raises(self, engine: SelfHealEngine):
        """锚点10a：错误确认码 → ConfirmCodeError（闸门先于一切）。"""
        with pytest.raises(ConfirmCodeError):
            engine.rollback("lh-snapshot-20260818T000000", "wrong")

    def test_rollback_empty_code_raises(self, engine: SelfHealEngine):
        """锚点10b：空确认码同样被闸门拒绝。"""
        with pytest.raises(ConfirmCodeError):
            engine.rollback("lh-snapshot-20260818T000000", "")

    def test_heal_status_exit_code_values(self):
        """锚点10c：HealStatus 值严格为 0/1/2（即 CLI 退出码）。"""
        assert HealStatus.HEALTHY.value == 0
        assert HealStatus.PARTIAL.value == 1
        assert HealStatus.FAILED.value == 2


# ------------------------------------------------------- 真实 git 快照与回滚


class TestGitSnapshotAndRollback:
    """在 tmp_path 真建仓，真测快照打 tag 与 reset --hard 回滚。"""

    def test_snapshot_creates_tag(self, git_repo, isolated_home, tmp_path):
        """真打 lh-snapshot-<ts> tag；非 git 仓库记 SNAPSHOT_SKIPPED。"""
        audit = AuditLog("self_heal", base_dir=tmp_path / "audit")
        engine = SelfHealEngine(project_root=git_repo, audit=audit)
        tag = engine._create_snapshot()
        assert tag is not None and tag.startswith("lh-snapshot-")
        proc = subprocess.run(
            ["git", "tag", "--list", tag],
            cwd=git_repo,
            capture_output=True,
            text=True,
            check=True,
        )
        assert proc.stdout.strip() == tag

    def test_snapshot_skipped_non_git(self, engine: SelfHealEngine):
        """非 git 仓库 → 返回 None 且审计含 SNAPSHOT_SKIPPED。"""
        assert engine._create_snapshot() is None
        events = [e["event"] for e in engine.audit.read_all()]
        assert "SNAPSHOT_SKIPPED" in events

    def test_rollback_restores_snapshot(self, git_repo, isolated_home, tmp_path):
        """真回滚：快照后改文件并提交，rollback 后工作区与 HEAD 均回到快照。"""
        audit = AuditLog("self_heal", base_dir=tmp_path / "audit")
        engine = SelfHealEngine(project_root=git_repo, audit=audit)
        tag = engine._create_snapshot()
        assert tag is not None

        target = git_repo / "app.py"
        original = target.read_text(encoding="utf-8")
        target.write_text("VALUE = 999  # 被自愈改坏\n", encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=git_repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "break it"], cwd=git_repo, check=True,
            capture_output=True,
        )
        assert target.read_text(encoding="utf-8") != original

        assert engine.rollback(tag, CONFIRM_CODE) is True
        assert target.read_text(encoding="utf-8") == original
        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=git_repo,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        tagged = subprocess.run(
            ["git", "rev-parse", tag],
            cwd=git_repo,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        assert head == tagged
        events = [e["event"] for e in audit.read_all()]
        assert "ROLLBACK" in events

    def test_rollback_non_git_returns_false(self, engine: SelfHealEngine):
        """非 git 仓库回滚（确认码正确）→ False 且写审计。"""
        assert engine.rollback("lh-snapshot-x", CONFIRM_CODE) is False
        events = [e["event"] for e in engine.audit.read_all()]
        assert "ROLLBACK_FAILED" in events


# ------------------------------------------------------------- detect 行为


class TestDetect:
    """detect 各通道：残留锁、日志扫尾、超大日志、端口 warn 级。"""

    def test_detect_stale_lock(self, engine: SelfHealEngine, project):
        """project_root 顶层 *.lock → stale_lock（warn）。"""
        (project / "worker.lock").write_text("pid=1\n", encoding="utf-8")
        errors = engine.detect(run_tests=False)
        assert [e.type for e in errors] == ["stale_lock"]
        assert errors[0].severity == "warn"

    def test_detect_log_tail_and_severity(self, engine: SelfHealEngine, tmp_path):
        """日志扫尾 100 行：ERROR→warn，CRITICAL/FATAL/Traceback→critical。"""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()
        (log_dir / "svc.log").write_text(
            "INFO ok\n" * 200 + "ERROR boom\nCRITICAL meltdown\n", encoding="utf-8"
        )
        errors = engine.detect(run_tests=False, log_dir=log_dir)
        by_msg = {e.message.split(" ")[0]: e for e in errors if e.type == "log_error"}
        assert by_msg["ERROR"].severity == "warn"
        assert by_msg["CRITICAL"].severity == "critical"
        assert all(e.context["path"].endswith("svc.log") for e in errors)

    def test_detect_log_oversize(self, engine: SelfHealEngine, tmp_path):
        """日志 >50MB → log_oversize，plan 给 log_rotate 策略。"""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()
        big = log_dir / "big.log"
        big.write_bytes(b"x" * (50 * 1024 * 1024 + 1))
        errors = engine.detect(run_tests=False, log_dir=log_dir)
        oversize = [e for e in errors if e.type == "log_oversize"]
        assert len(oversize) == 1
        assert oversize[0].severity == "warn"
        (plan,) = engine.plan(oversize)
        assert plan["strategy"] == "log_rotate"
        assert plan["safe"] is True

    def test_detect_ports_warn_only(self, engine: SelfHealEngine, monkeypatch):
        """端口检测：lsof 不存在时 severity=warn，绝不 critical。"""
        monkeypatch.setattr("shutil.which", lambda name: None)
        errors = engine.detect(run_tests=False, ports=[8080, 9090])
        assert len(errors) == 2
        assert all(e.type == "service_down" for e in errors)
        assert all(e.severity == "warn" for e in errors)
        assert all(e.context["reason"] == "lsof_missing" for e in errors)


# ---------------------------------------------------------------- heal 流程


class TestHealFlow:
    """heal 主流程：干跑只记录、真执行安全策略、ESCALATE 上耻辱墙。"""

    def test_heal_healthy_empty_project(self, engine: SelfHealEngine):
        """空项目（pytest 退出码 5）→ HEALTHY，报告字段齐全。"""
        report = engine.heal()
        assert report["status"] == HealStatus.HEALTHY.value == 0
        assert report["found"] == 0
        assert report["dry_run"] is True
        assert report["rolled_back"] is False
        assert report["run_dna"].startswith("#龍芯")
        assert isinstance(report["details"], list)

    def test_heal_dry_run_records_but_keeps_lock(
        self, engine: SelfHealEngine, project
    ):
        """dry_run=True：stale_lock 计划只记录不执行，文件仍在，status=PARTIAL。"""
        lock = project / "worker.lock"
        lock.write_text("pid=1\n", encoding="utf-8")
        report = engine.heal()
        assert report["dry_run"] is True
        assert report["found"] >= 1
        assert report["fixed"] == 0
        assert report["status"] == HealStatus.PARTIAL.value
        assert lock.exists(), "干跑绝不真删"
        results = [d["result"] for d in report["details"]]
        assert "dry_run_recorded" in results

    def test_heal_execute_removes_stale_lock(
        self, project, isolated_home, tmp_path
    ):
        """dry_run=False：真删残留锁，复检干净 → HEALTHY。"""
        audit = AuditLog("self_heal", base_dir=tmp_path / "audit")
        engine = SelfHealEngine(project_root=project, audit=audit, dry_run=False)
        lock = project / "worker.lock"
        lock.write_text("pid=1\n", encoding="utf-8")
        report = engine.heal()
        assert report["fixed"] == 1
        assert report["status"] == HealStatus.HEALTHY.value
        assert not lock.exists()
        events = [e["event"] for e in audit.read_all()]
        assert "HEAL_FIX" in events
        assert "SNAPSHOT_SKIPPED" in events  # 非 git 仓库

    def test_heal_execute_log_rotate(self, engine: SelfHealEngine, tmp_path):
        """log_rotate 真执行：轮转为 .bak 并截断出空文件。"""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()
        big = log_dir / "big.log"
        payload = b"x" * (50 * 1024 * 1024 + 1)
        big.write_bytes(payload)
        err = make_error(
            "log_oversize", "日志超大", severity="warn", path=str(big)
        )
        (plan,) = engine.plan([err])
        engine._execute(plan)
        assert big.exists() and big.stat().st_size == 0
        backups = list(log_dir.glob("big.log.*.bak"))
        assert len(backups) == 1 and backups[0].stat().st_size == len(payload)

    def test_heal_escalates_real_failing_test(
        self, project, isolated_home, tmp_path
    ):
        """真跑 pytest 子进程：断言失败 → ESCALATE + 耻辱墙，绝不假装修复。"""
        (project / "test_broken.py").write_text(
            "def test_truth():\n    assert 16 == 18  # 断言失败\n",
            encoding="utf-8",
        )
        audit = AuditLog("self_heal", base_dir=tmp_path / "audit")
        engine = SelfHealEngine(project_root=project, audit=audit, dry_run=False)
        report = engine.heal(confirm_code=CONFIRM_CODE)
        assert report["found"] >= 1
        assert report["fixed"] == 0
        assert report["escalated"] >= 1
        assert report["rolled_back"] is False  # 非 git 仓库无快照可回滚
        assert report["status"] == HealStatus.PARTIAL.value
        strategies = [d["strategy"] for d in report["details"]]
        assert "ESCALATE" in strategies
        assert all(d["action"] is None for d in report["details"])

        shame = isolated_home / "08_STATE" / "shame_wall.jsonl"
        assert shame.exists(), "业务逻辑错误必须上耻辱墙"
        entries = [
            json.loads(line)
            for line in shame.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        assert any(e["event"] == "ESCALATE" for e in entries)
        events = [e["event"] for e in audit.read_all()]
        assert "ESCALATE" in events and "HEAL_REPORT" in events

    def test_heal_consecutive_failures_failed_status(
        self, engine: SelfHealEngine, isolated_home, monkeypatch
    ):
        """连续 max_attempts 次修复失败 → status=FAILED + 耻辱墙熔断记录。"""
        engine.max_attempts = 1
        err = make_error(
            "stale_lock",
            "残留锁文件",
            severity="warn",
            path=str(engine.project_root / "ghost.lock"),  # 不存在 → 执行必失败
        )
        monkeypatch.setattr(engine, "detect", lambda *a, **k: [err])
        engine.dry_run = False
        report = engine.heal()  # 锁文件不存在 → 执行失败 1 次 ≥ max_attempts=1
        assert report["status"] == HealStatus.FAILED.value == 2
        shame = isolated_home / "08_STATE" / "shame_wall.jsonl"
        entries = [
            json.loads(line)
            for line in shame.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        assert any(e["event"] == "CONSECUTIVE_FAILURES" for e in entries)


# ---------------------------------------------------------------------- CLI


class TestCli:
    """CLI：--once/--status 退出码 = HealStatus 值。"""

    def test_cli_once_healthy(self, project, isolated_home, capsys):
        """--once 在干净项目 → 退出码 0，输出报告 JSON。"""
        code = main(["--once", "--project-root", str(project)])
        assert code == 0
        out = capsys.readouterr().out
        assert "🟢" in out and "HEALTHY" in out

    def test_cli_once_partial_on_stale_lock(
        self, project, isolated_home, capsys
    ):
        """--once 干跑发现残留锁 → 退出码 1（🟡 待确认），文件保留。"""
        (project / "x.lock").write_text("pid=1\n", encoding="utf-8")
        code = main(["--once", "--project-root", str(project)])
        assert code == 1
        assert (project / "x.lock").exists()

    def test_cli_status_after_run(self, project, isolated_home, capsys):
        """--status 读最近一次 HEAL_REPORT，退出码对齐其状态。"""
        assert main(["--once", "--project-root", str(project)]) == 0
        assert main(["--status", "--project-root", str(project)]) == 0
        out = capsys.readouterr().out
        assert "最近一次自愈" in out


# ------------------------------------------------------- 审查修复回归（R1/Y2/Y4/Y6/Y7/Y8/O3/O4）


class TestR1RealSnapshotDirtyWorktree:
    """R1：dirty worktree（含未跟踪文件）必须进快照，rollback 完整恢复。"""

    def test_snapshot_commit_contains_worktree(self, git_repo, isolated_home, tmp_path):
        """打快照后快照 commit 包含未提交修改与未跟踪文件，HEAD 不被移动。"""
        audit = AuditLog("self_heal", base_dir=tmp_path / "audit")
        engine = SelfHealEngine(project_root=git_repo, audit=audit)
        head_before = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=git_repo,
            capture_output=True, text=True, check=True,
        ).stdout.strip()

        (git_repo / "app.py").write_text("VALUE = 2  # 未提交修改\n", encoding="utf-8")
        (git_repo / "untracked.py").write_text("X = 1\n", encoding="utf-8")
        tag = engine._create_snapshot()
        assert tag is not None

        tagged = subprocess.run(
            ["git", "rev-parse", tag], cwd=git_repo,
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        assert tagged != head_before, "dirty worktree 时 tag 不得只指向 HEAD"
        head_after = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=git_repo,
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        assert head_after == head_before, "打快照不得移动用户的 HEAD"

    def test_rollback_restores_uncommitted_and_untracked(
        self, git_repo, isolated_home, tmp_path
    ):
        """R1 主回归：快照→破坏（删未跟踪文件/改文件/提交）→回滚→全部恢复。"""
        audit = AuditLog("self_heal", base_dir=tmp_path / "audit")
        engine = SelfHealEngine(project_root=git_repo, audit=audit)
        dirty_content = "VALUE = 2  # 未提交修改\n"
        (git_repo / "app.py").write_text(dirty_content, encoding="utf-8")
        (git_repo / "untracked.py").write_text("X = 1\n", encoding="utf-8")
        tag = engine._create_snapshot()
        assert tag is not None

        # 模拟修复动作造成的破坏：删未跟踪文件、改坏已跟踪文件并提交。
        (git_repo / "untracked.py").unlink()
        (git_repo / "app.py").write_text("VALUE = 999  # 改坏\n", encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=git_repo, check=True)
        subprocess.run(
            ["git", "commit", "-m", "damage"], cwd=git_repo,
            check=True, capture_output=True,
        )
        assert not (git_repo / "untracked.py").exists()

        assert engine.rollback(tag, CONFIRM_CODE) is True
        assert (git_repo / "app.py").read_text(encoding="utf-8") == dirty_content
        assert (git_repo / "untracked.py").read_text(encoding="utf-8") == "X = 1\n"

    def test_heal_execute_rollback_restores_dirty_worktree(
        self, git_repo, isolated_home, tmp_path
    ):
        """R1+Y2 端到端：dirty worktree 下真执行修复→复检仍有错→回滚，
        未提交修改/未跟踪文件全恢复，报告 fixed 清零且带 rollback_note。"""
        dirty_content = "VALUE = 2  # 用户未提交的工作\n"
        (git_repo / "app.py").write_text(dirty_content, encoding="utf-8")
        (git_repo / "untracked_note.txt").write_text("草稿\n", encoding="utf-8")
        (git_repo / "worker.lock").write_text("pid=1\n", encoding="utf-8")
        (git_repo / "test_broken.py").write_text(
            "def test_truth():\n    assert 16 == 18\n", encoding="utf-8"
        )
        audit = AuditLog("self_heal", base_dir=tmp_path / "audit")
        engine = SelfHealEngine(project_root=git_repo, audit=audit, dry_run=False)
        report = engine.heal(confirm_code=CONFIRM_CODE)

        assert report["rolled_back"] is True
        assert report["fixed"] == 0, "回滚后 fixed 必须清零"
        assert report["rollback_note"]
        assert "无法自动撤销" in report["rollback_note"]
        assert "lock_remove" in report["rollback_note"]  # 已执行副作用逐条列出
        # 未提交修改与未跟踪文件（含被删的锁、草稿）全部恢复
        assert (git_repo / "app.py").read_text(encoding="utf-8") == dirty_content
        assert (git_repo / "untracked_note.txt").read_text("utf-8") == "草稿\n"
        assert (git_repo / "worker.lock").exists()

    def test_snapshot_failure_fail_closed(self, git_repo, isolated_home, tmp_path, monkeypatch):
        """R1 fail-closed：快照流程失败 → 拒绝执行修复动作，转 FAILED + 耻辱墙。"""
        (git_repo / "worker.lock").write_text("pid=1\n", encoding="utf-8")

        def boom(*args, **kwargs):
            raise RuntimeError("git tag 失败：模拟磁盘满")

        audit = AuditLog("self_heal", base_dir=tmp_path / "audit")
        engine = SelfHealEngine(project_root=git_repo, audit=audit, dry_run=False)
        monkeypatch.setattr(engine, "_create_snapshot", boom)
        report = engine.heal(confirm_code=CONFIRM_CODE)
        assert report["status"] == HealStatus.FAILED.value
        assert report["snapshot_failed"] is True
        assert report["fixed"] == 0
        assert (git_repo / "worker.lock").exists(), "快照失败绝不碰用户代码"
        results = [d["result"] for d in report["details"]]
        assert "aborted_snapshot_failed" in results
        events = [e["event"] for e in audit.read_all()]
        assert "HEAL_ABORTED" in events


class TestY4PackageWhitelist:
    """Y4：白名单收紧 + pip 命令加 -- 双保险。"""

    @pytest.mark.parametrize("bad", ["-e", "--user", "..", "", "-x"])
    def test_dash_and_dotdot_names_escalate(self, engine: SelfHealEngine, bad):
        """'-e'/'--user'/'..'/空串全部拒绝转 ESCALATE。"""
        err = make_error("dep_missing", "ModuleNotFoundError", module=bad)
        (plan,) = engine.plan([err])
        assert plan["strategy"] == "ESCALATE"
        assert plan["safe"] is False
        assert plan["action"] is None

    def test_whitelist_regex_shape(self):
        assert PACKAGE_NAME_RE.match("requests")
        assert PACKAGE_NAME_RE.match("foo_bar-1.2")
        for bad in ("-e", "--user", "..", "", ".hidden", "_leading"):
            assert PACKAGE_NAME_RE.match(bad) is None, bad

    def test_pip_action_has_double_dash(self, engine: SelfHealEngine):
        """生成的 pip 命令在包名前加 --：pip install -- <pkg>。"""
        err = make_error(
            "dep_missing", "ModuleNotFoundError: No module named 'requests'"
        )
        (plan,) = engine.plan([err])
        assert plan["action"][-2:] == ["--", "requests"]


class TestY8ServiceRestartWithoutCommand:
    """Y8：无重启命令的 service_down 不得标 safe，直接转 escalated。"""

    def test_no_command_not_safe(self, engine: SelfHealEngine):
        err = make_error("service_down", "端口 8080 无监听", severity="warn", port=8080)
        (plan,) = engine.plan([err])
        assert plan["strategy"] == "ESCALATE"
        assert plan["safe"] is False
        assert plan["action"] is None
        assert "升级人工" in plan["reason"]

    def test_with_command_still_safe(self, engine: SelfHealEngine):
        err = make_error(
            "service_down", "端口 8080 无监听", severity="warn",
            port=8080, restart_cmd=["true"],
        )
        (plan,) = engine.plan([err])
        assert plan["strategy"] == "service_restart"
        assert plan["safe"] is True
        assert plan["action"] == ["true"]


class TestO3TailRead:
    """O3：>1MB 日志真尾部读取，不整文件读入。"""

    def test_large_log_tail_only(self, engine: SelfHealEngine, tmp_path):
        log_dir = tmp_path / "logs"
        log_dir.mkdir()
        big = log_dir / "big.log"
        content = (
            "CRITICAL early-must-not-match\n"
            + "INFO filler line padding padding padding\n" * 40000
            + "ERROR tail-hit\n"
        )
        big.write_text(content, encoding="utf-8")
        assert big.stat().st_size > 1024 * 1024
        errors = engine.detect(run_tests=False, log_dir=log_dir)
        msgs = [e.message for e in errors if e.type == "log_error"]
        assert any("tail-hit" in m for m in msgs)
        assert not any("early-must-not-match" in m for m in msgs), "只许读尾部"


class TestTailReadHardCap:
    """复验残洞3：无换行/超长行病态输入下，尾读内存与耗时有硬上限。"""

    def test_60mb_single_line_bounded(self, tmp_path):
        """60MB 单行文件 → tracemalloc 峰值 <10MB 且耗时 <5s（宽松防 CI 抖动）。"""
        import time
        import tracemalloc

        big = tmp_path / "single.log"
        with big.open("wb") as fh:
            fh.write(b"ERROR " + b"x" * (60 * 1024 * 1024))  # 60MB 单行
        tracemalloc.start()
        started = time.monotonic()
        lines = SelfHealEngine._tail_lines(big, 100)
        elapsed = time.monotonic() - started
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        assert elapsed < 5.0, f"耗时越界：{elapsed:.2f}s"
        assert peak < 10 * 1024 * 1024, f"内存峰值越界：{peak / 1024 / 1024:.1f}MB"
        assert len(lines) == 1
        # 窗口只保留尾部：行首的 "ERROR" 在窗口外，绝不整文件读入
        assert set(lines[0]) == {"x"}
        assert len(lines[0]) <= MAX_TAIL_BYTES

    def test_60mb_multiline_reports_tail_only(self, engine: SelfHealEngine, tmp_path):
        """60MB 正常多行文件 → 只报尾部错误（回归既有行为），耗时同样有界。"""
        import time

        log_dir = tmp_path / "logs"
        log_dir.mkdir()
        big = log_dir / "huge.log"
        filler = b"INFO padding padding padding padding padding padding pad\n"
        with big.open("wb") as fh:
            fh.write(b"CRITICAL head-must-not-match\n")
            for _ in range((60 * 1024 * 1024) // len(filler)):
                fh.write(filler)
            fh.write(b"Traceback (most recent call last):\nCRITICAL tail-hit\n")
        assert big.stat().st_size > 60 * 1024 * 1024
        started = time.monotonic()
        errors = engine.detect(run_tests=False, log_dir=log_dir)
        elapsed = time.monotonic() - started
        assert elapsed < 5.0, f"耗时越界：{elapsed:.2f}s"
        msgs = [e.message for e in errors if e.type == "log_error"]
        assert any("tail-hit" in m for m in msgs)
        assert any("Traceback" in m for m in msgs)
        assert not any("head-must-not-match" in m for m in msgs), "只许读尾部窗口"


class TestGitMissingFailClosed:
    """复验残洞1：git 二进制不可用 + .git 存在 → 快照 fail-closed，
    heal 拒绝执行修复且 FAILED + 耻辱墙，用户代码零改动。"""

    @staticmethod
    def _patch_git_missing(monkeypatch):
        """monkeypatch subprocess.run：git 调用一律 FileNotFoundError（不在 PATH）。"""
        real_run = subprocess.run

        def fake_run(cmd, *args, **kwargs):
            if isinstance(cmd, (list, tuple)) and cmd and str(cmd[0]) == "git":
                raise FileNotFoundError("No such file or directory: 'git'")
            return real_run(cmd, *args, **kwargs)

        monkeypatch.setattr(subprocess, "run", fake_run)

    def test_is_git_repo_raises_when_git_missing_but_dotgit_exists(
        self, project, isolated_home, tmp_path, monkeypatch
    ):
        """有 .git 但 git 不可用 → _is_git_repo 抛 RuntimeError（不得返回 False）。"""
        (project / ".git").mkdir()
        audit = AuditLog("self_heal", base_dir=tmp_path / "audit")
        engine = SelfHealEngine(project_root=project, audit=audit)
        self._patch_git_missing(monkeypatch)
        with pytest.raises(RuntimeError):
            engine._is_git_repo()

    def test_is_git_repo_false_when_no_dotgit_and_git_missing(
        self, project, isolated_home, tmp_path, monkeypatch
    ):
        """无 .git 且 git 不可用 → False（真非 git 仓）。"""
        audit = AuditLog("self_heal", base_dir=tmp_path / "audit")
        engine = SelfHealEngine(project_root=project, audit=audit)
        self._patch_git_missing(monkeypatch)
        assert engine._is_git_repo() is False

    def test_heal_execute_fail_closed_when_git_missing(
        self, project, isolated_home, tmp_path, monkeypatch
    ):
        """对抗复现：PATH 剔除 git（FileNotFoundError）+ .git 存在 →
        heal 执行模式必须 FAILED、锁文件零改动、耻辱墙有 HEAL_ABORTED、
        审计含 SNAPSHOT_FAILED。"""
        (project / ".git").mkdir()
        lock = project / "worker.lock"
        lock.write_text("pid=1\n", encoding="utf-8")
        audit = AuditLog("self_heal", base_dir=tmp_path / "audit")
        engine = SelfHealEngine(project_root=project, audit=audit, dry_run=False)
        self._patch_git_missing(monkeypatch)
        report = engine.heal(confirm_code=CONFIRM_CODE)
        assert report["status"] == HealStatus.FAILED.value == 2
        assert report["snapshot_failed"] is True
        assert report["fixed"] == 0
        assert lock.exists(), "git 不可用不得误判跳过快照直接删锁"
        assert (project / "app.py").exists() is False  # 未产生任何新文件
        results = [d["result"] for d in report["details"]]
        assert "aborted_snapshot_failed" in results
        events = [e["event"] for e in audit.read_all()]
        assert "SNAPSHOT_FAILED" in events
        assert "HEAL_ABORTED" in events
        shame = isolated_home / "08_STATE" / "shame_wall.jsonl"
        entries = [
            json.loads(line)
            for line in shame.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        assert any(e["event"] == "HEAL_ABORTED" for e in entries)

    def test_rollback_git_missing_returns_false(
        self, project, isolated_home, tmp_path, monkeypatch
    ):
        """rollback：有 .git 但 git 不可用 → False + ROLLBACK_FAILED（不抛出）。"""
        (project / ".git").mkdir()
        audit = AuditLog("self_heal", base_dir=tmp_path / "audit")
        engine = SelfHealEngine(project_root=project, audit=audit)
        self._patch_git_missing(monkeypatch)
        assert engine.rollback("lh-snapshot-x", CONFIRM_CODE) is False
        events = [e["event"] for e in audit.read_all()]
        assert "ROLLBACK_FAILED" in events


class TestO4LogRotateNaming:
    """O4：备份名纳秒+pid 防同秒覆盖；保留原文件权限。"""

    def test_same_second_rotations_do_not_overwrite(
        self, engine: SelfHealEngine, tmp_path
    ):
        target = tmp_path / "svc.log"
        for payload in ("first", "second"):
            target.write_text(payload, encoding="utf-8")
            err = make_error("log_oversize", "超大", severity="warn", path=str(target))
            (plan,) = engine.plan([err])
            engine._execute(plan)
        backups = sorted(tmp_path.glob("svc.log.*.bak"))
        assert len(backups) == 2, "同秒两次轮转不得互相覆盖"
        contents = {b.read_text(encoding="utf-8") for b in backups}
        assert contents == {"first", "second"}

    def test_permissions_preserved(self, engine: SelfHealEngine, tmp_path):
        target = tmp_path / "svc.log"
        target.write_text("x", encoding="utf-8")
        os.chmod(target, 0o640)
        err = make_error("log_oversize", "超大", severity="warn", path=str(target))
        (plan,) = engine.plan([err])
        engine._execute(plan)
        assert (target.stat().st_mode & 0o777) == 0o640


class TestY6CliDetectParams:
    """Y6：CLI --log-dir/--ports 贯通到 engine.detect。"""

    def test_parser_accepts_log_dir_and_ports(self):
        args = build_parser().parse_args(
            ["--once", "--log-dir", "/tmp/x", "--ports", "8080, 9090", "--execute"]
        )
        assert args.log_dir == "/tmp/x"
        assert args.execute is True
        assert _parse_ports(args.ports) == [8080, 9090]

    def test_parse_ports_invalid(self):
        with pytest.raises(ValueError):
            _parse_ports("8080,abc")
        with pytest.raises(ValueError):
            _parse_ports("70000")
        assert _parse_ports(None) is None
        assert _parse_ports("") is None

    def test_heal_threads_log_dir_and_ports(
        self, project, isolated_home, tmp_path, monkeypatch
    ):
        log_dir = tmp_path / "logs"
        log_dir.mkdir()
        (log_dir / "svc.log").write_text("CRITICAL boom\n", encoding="utf-8")
        monkeypatch.setattr("shutil.which", lambda name: None)  # lsof 缺失 → warn
        audit = AuditLog("self_heal", base_dir=tmp_path / "audit")
        engine = SelfHealEngine(
            project_root=project, audit=audit, log_dir=log_dir, ports=[8080]
        )
        report = engine.heal()
        types = [d["error_type"] for d in report["details"]]
        assert "log_error" in types
        assert "service_down" in types


class TestY7ExitCodes:
    """Y7：--status 越界 clamp 到 2；未处理异常 → 摘要 + 2。"""

    def test_status_out_of_range_clamped_to_2(
        self, isolated_home, monkeypatch, capsys
    ):
        audit = AuditLog("self_heal")
        audit.log(
            "HEAL_REPORT",
            {
                "status": 99,
                "status_label": "BOGUS",
                "found": 0, "fixed": 0, "escalated": 0,
                "rolled_back": False, "dry_run": True,
            },
        )
        assert main(["--status"]) == 2
        assert "🔴" in capsys.readouterr().out

    def test_status_negative_clamped_to_2(self, isolated_home, capsys):
        audit = AuditLog("self_heal")
        audit.log(
            "HEAL_REPORT",
            {
                "status": -1,
                "status_label": "BOGUS",
                "found": 0, "fixed": 0, "escalated": 0,
                "rolled_back": False, "dry_run": True,
            },
        )
        assert main(["--status"]) == 2

    def test_main_unhandled_exception_returns_2(
        self, project, isolated_home, monkeypatch, capsys
    ):
        def boom(self, confirm_code=None):
            raise RuntimeError("爆炸")

        monkeypatch.setattr(SelfHealEngine, "heal", boom)
        assert main(["--once", "--project-root", str(project)]) == 2
        err = capsys.readouterr().err
        assert "未处理异常" in err and "爆炸" in err


class TestCorruptDotGitFailClosed:
    """集成审查补刀：.git 存在但损坏（rev-parse 返回非零）→ fail-closed，
    绝不误判为非 git 仓而无快照裸奔执行修复。"""

    def test_is_git_repo_raises_on_corrupt_dotgit(
        self, project, isolated_home, tmp_path
    ):
        """.git 损坏（rev-parse rc!=0）→ RuntimeError，不得返回 False。"""
        (project / ".git").mkdir()
        (project / ".git" / "HEAD").write_text("corrupt", encoding="utf-8")
        audit = AuditLog("self_heal", base_dir=tmp_path / "audit")
        engine = SelfHealEngine(project_root=project, audit=audit)
        with pytest.raises(RuntimeError):
            engine._is_git_repo()

    def test_heal_execute_fail_closed_on_corrupt_dotgit(
        self, project, isolated_home, tmp_path
    ):
        """对抗复现：.git 损坏 + dry_run=False → FAILED、锁文件零改动、
        耻辱墙有 HEAL_ABORTED、审计含 SNAPSHOT_FAILED。"""
        (project / ".git").mkdir()
        (project / ".git" / "HEAD").write_text("corrupt", encoding="utf-8")
        lock = project / "worker.lock"
        lock.write_text("pid=1\n", encoding="utf-8")
        audit = AuditLog("self_heal", base_dir=tmp_path / "audit")
        engine = SelfHealEngine(project_root=project, audit=audit, dry_run=False)
        report = engine.heal(confirm_code=CONFIRM_CODE)
        assert report["status"] == HealStatus.FAILED.value == 2
        assert report["snapshot_failed"] is True
        assert report["fixed"] == 0
        assert lock.exists(), ".git 损坏不得误判跳过快照直接删锁"
        events = [e["event"] for e in audit.read_all()]
        assert "SNAPSHOT_FAILED" in events
        assert "HEAL_ABORTED" in events
