#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 行业痛点治理系统测试
DNA: #龍芯⚡️丙午·丙申·丁酉·丑时-INDUSTRY-GOVERNANCE-TEST-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
License: MulanPSL v2
"""

import json
import os
import shutil
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

TEST_STATE = PROJECT_ROOT / ".state_test_industry_governance"
if TEST_STATE.exists():
    shutil.rmtree(TEST_STATE)
TEST_STATE.mkdir(parents=True, exist_ok=True)

from engines import lh_industry_governance

lh_industry_governance.STATE_DIR = TEST_STATE
lh_industry_governance.DB_PATH = TEST_STATE / "governance.sqlite"

from engines.lh_industry_governance import (
    GovernanceOrchestrator,
    SUBSYSTEMS,
    PAIN_POINT_MAP,
    tricolor_audit,
)


@pytest.fixture
def orch():
    return GovernanceOrchestrator()


# ============================================================
# 基础结构
# ============================================================

def test_subsystems_cover_8_pain_points():
    assert len(SUBSYSTEMS) == 8
    names = set(PAIN_POINT_MAP.values())
    assert names == set(SUBSYSTEMS.keys())


def test_tricolor_audit():
    assert tricolor_audit({"errors": ["x"], "warnings": []}) == "🔴"
    assert tricolor_audit({"warnings": ["x"], "gaps": []}) == "🟡"
    assert tricolor_audit({"checks": {"a": True}}) == "🟢"


# ============================================================
# 子系统功能
# ============================================================

def test_auto_factory_assess(orch):
    r = orch.dispatch("auto_factory", "assess", {"stage_build": True})
    assert r["pain_point"] == "auto_factory"
    assert r["tricolor"] in ("🟢", "🟡", "🔴")
    assert "gaps" in r["result"]


def test_agent_control_bind_and_trace(orch):
    bind = orch.dispatch("agent_control", "act", {"bind": True, "agent_id": "agent-1", "owner": "UID9622"})
    assert bind["result"]["owner"] == "UID9622"
    trace = orch.dispatch("agent_control", "assess", {"agent_id": "agent-1", "action": "deploy"})
    assert trace["result"]["status"] == "bound"


def test_data_sovereignty_act(orch):
    r = orch.dispatch("data_sovereignty", "act", {"local_storage": True, "encrypted": True})
    assert "sovereignty_score" in r["result"]
    assert r["result"]["sovereignty_score"] >= 0.5


def test_context_assess(orch):
    r = orch.dispatch("context", "assess", {"kg_connected": True})
    assert 0 <= r["result"]["ready_score"] <= 1


def test_open_source_honor(orch):
    r = orch.dispatch("open_source", "act", {"honor": True, "contributor": "tester", "contribution": "修复bug"})
    assert r["result"]["honored"]["contributor"] == "tester"


def test_sovereign_gateway_assess(orch):
    r = orch.dispatch("sovereign_gateway", "assess", {
        "providers": [{"name": "ollama", "domestic": True}, {"name": "openai", "domestic": False}]
    })
    assert r["result"]["domestic_ratio"] == 0.5


def test_rule_engine_shame(orch):
    r = orch.dispatch("rule_engine", "act", {"shame": True, "actor": "bad_agent", "reason": "越权操作"})
    assert r["result"]["shamed"]["actor"] == "bad_agent"


def test_shadow_ai_detect(orch):
    r = orch.dispatch("shadow_ai", "act", {"tool_name": "chatgpt_web", "user": "employee"})
    assert r["result"]["detection"]["blocked"] is True
    r2 = orch.dispatch("shadow_ai", "act", {"tool_name": "lh_terminal_writer", "user": "employee"})
    assert r2["result"]["detection"]["blocked"] is False


# ============================================================
# 编排器高级功能
# ============================================================

def test_dashboard(orch):
    board = orch.dashboard()
    assert "pain_points" in board
    assert "shame_count" in board
    assert "honor_count" in board


def test_all_assess(orch):
    results = orch.all_assess()
    assert len(results) == 8
    for k in SUBSYSTEMS:
        assert k in results


def test_unknown_pain_point(orch):
    r = orch.dispatch("not_exists", "assess")
    assert "error" in r


# ============================================================
# API 集成测试
# ============================================================

def test_api_endpoints():
    try:
        from fastapi.testclient import TestClient
        from engines.lh_governance_api import app
    except Exception:
        pytest.skip("未安装 fastapi / testclient")

    client = TestClient(app)

    r = client.get("/")
    assert r.status_code == 200
    assert "dna" in r.json()

    r = client.get("/pain-points")
    assert r.status_code == 200
    assert len(r.json()["pain_points"]) == 8

    r = client.post("/assess", json={"pain_point": "auto_factory", "context": {"stage_build": True}})
    assert r.status_code == 200
    assert r.json()["pain_point"] == "auto_factory"

    r = client.post("/act", json={"pain_point": "agent_control", "context": {"bind": True, "agent_id": "api-agent", "owner": "UID9622"}})
    assert r.status_code == 200

    r = client.get("/dashboard")
    assert r.status_code == 200
    assert "event_colors" in r.json()


# ============================================================
# 中英双语命令路由
# ============================================================

def test_bilingual_router():
    sys.path.insert(0, str(PROJECT_ROOT / "08_BIN"))
    from lh_bilingual_router import BilingualCommandRouter
    router = BilingualCommandRouter()
    assert router.resolve_command("assess") == "assess"
    assert router.resolve_command("评估") == "assess"
    assert router.resolve_pain_point("数据主权") == "data_sovereignty"
    assert router.resolve_pain_point("shadow_ai") == "shadow_ai"
    assert router.resolve_pain_point("AI ROI") == "auto_factory"


def test_dispatch_bilingual_pain_point(orch):
    r = orch.dispatch("数据主权", "assess", {"local_storage": True})
    assert r["pain_point"] == "data_sovereignty"


def test_dispatch_bilingual_action(orch):
    r = orch.dispatch("auto_factory", "评估", {"stage_build": True})
    assert r["pain_point"] == "auto_factory"
    assert r["action"] == "assess"


def test_api_bilingual_pain_point():
    try:
        from fastapi.testclient import TestClient
        from engines.lh_governance_api import app
    except Exception:
        pytest.skip("未安装 fastapi / testclient")

    client = TestClient(app)
    r = client.post("/assess", json={"pain_point": "影子AI", "context": {"gateway_enabled": True}})
    assert r.status_code == 200
    assert r.json()["pain_point"] == "shadow_ai"


# ============================================================
# 清理
# ============================================================

def teardown_module():
    if TEST_STATE.exists():
        shutil.rmtree(TEST_STATE)

# ⛓️ 龍魂DNA接龙链 ──────────────────────────────
# DNA:V1|丙午·丙申·癸亥·辰时·䷗复|P04鲁班|创建|治理测试封装|bhash:1f2e456a|chash:d1afe344|←GENESIS
# ⛓️ 龍魂DNA接龙末端 ──────────────────────────────
