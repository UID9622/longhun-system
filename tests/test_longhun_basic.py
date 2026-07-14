#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂基础回归测试
DNA: #龍芯⚡️2026-06-21-LONGHUN-BASIC-TESTS-v1.0
"""

from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_project_root_exists():
    assert PROJECT_ROOT.exists()


def test_core_files_present():
    core_files = [
        PROJECT_ROOT / "cnsh-terminal" / "cnsh_terminal_v5.py",
        PROJECT_ROOT / "control-panel" / "api_gateway_8443.py",
        PROJECT_ROOT / "brain" / "brain_notion_sync.py",
        PROJECT_ROOT / "agents" / "longhun_notion_sync_auto.py",
    ]
    for path in core_files:
        assert path.exists(), f"核心文件缺失: {path}"


def test_action_log_exists():
    log_path = PROJECT_ROOT / "logs" / "action_log.jsonl"
    assert log_path.exists()


def test_dna_marker_format():
    dna = "#龍芯⚡️2026-06-21-LONGHUN-BASIC-TESTS-v1.0"
    assert dna.startswith("#龍芯")
    assert "⚡️" in dna
    assert len(dna) > 10
