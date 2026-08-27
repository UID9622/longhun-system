# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·甲子·甲戌·䷍大有-CODE-补DNA-72dee294
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""test_audit.py — 史官审计日志测试（锚点7）。"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from longhun_trust.audit import AuditLog


@pytest.fixture
def audit(tmp_path, monkeypatch) -> AuditLog:
    """用 LONGHUN_HOME 隔离到 tmp_path，禁止污染真实 home。"""
    monkeypatch.setenv("LONGHUN_HOME", str(tmp_path))
    return AuditLog("test_audit")


class TestAuditLogBasics:
    def test_default_base_dir_uses_longhun_home(self, tmp_path, monkeypatch):
        monkeypatch.setenv("LONGHUN_HOME", str(tmp_path))
        log = AuditLog("x")
        assert log.base_dir == tmp_path / "04_AUDIT"
        assert log.path == tmp_path / "04_AUDIT" / "x.jsonl"
        assert log.base_dir.is_dir()

    def test_explicit_base_dir(self, tmp_path):
        log = AuditLog("y", base_dir=tmp_path / "custom")
        assert log.path == tmp_path / "custom" / "y.jsonl"

    def test_log_returns_entry_and_persists(self, audit: AuditLog):
        entry = audit.log("TEST_EVENT", {"k": "v"})
        assert entry["event"] == "TEST_EVENT"
        assert entry["details"] == {"k": "v"}
        assert "timestamp" in entry
        assert entry["dna"].startswith("#龍芯")
        # flush+fsync 生效：写入后立刻可从文件系统读到
        lines = audit.path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        assert json.loads(lines[0])["event"] == "TEST_EVENT"

    def test_read_all_empty(self, audit: AuditLog):
        assert audit.read_all() == []


class TestAppendOnly:
    """锚点7：只增不删 —— log→freeze→read_all 原行仍在且 FREEZE 在尾。"""

    def test_freeze_appends_and_never_deletes(self, audit: AuditLog):
        e1 = audit.log("FIRST", {"n": 1})
        e2 = audit.log("SECOND", {"n": 2})
        frozen = audit.freeze(reason="锚点7废止测试", target=e1)

        entries = audit.read_all()
        assert len(entries) == 3
        # 原行仍在
        assert entries[0] == e1
        assert entries[1] == e2
        # FREEZE 在尾
        assert entries[2]["event"] == "FREEZE"
        assert entries[2]["reason"] == "锚点7废止测试"
        assert entries[2]["target"] == e1
        assert frozen["event"] == "FREEZE"
        # 物理行数不变，未被删除
        assert len(audit.path.read_text(encoding="utf-8").splitlines()) == 3

    def test_freeze_without_target(self, audit: AuditLog):
        audit.log("A", {})
        audit.freeze(reason="整体冻结")
        entries = audit.read_all()
        assert entries[-1]["event"] == "FREEZE"
        assert entries[-1]["target"] is None

    def test_multiple_freezes_all_kept(self, audit: AuditLog):
        audit.log("A", {})
        audit.freeze(reason="r1")
        audit.freeze(reason="r2")
        events = [e["event"] for e in audit.read_all()]
        assert events == ["A", "FREEZE", "FREEZE"]

    def test_fsync_called(self, audit: AuditLog, monkeypatch):
        """实证 log() 路径确实 flush+fsync。"""
        import os

        calls = {"fsync": 0}
        real_fsync = os.fsync

        def spy(fd):
            calls["fsync"] += 1
            return real_fsync(fd)

        monkeypatch.setattr(os, "fsync", spy)
        audit.log("FSYNC_PROBE", {})
        assert calls["fsync"] >= 1
