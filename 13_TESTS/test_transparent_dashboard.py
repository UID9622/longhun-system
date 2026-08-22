#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 透明看板测试
DNA: #龍芯⚡️丙午·丙申·丁酉·甲辰·䷼中孚-TRANSPARENT-DASHBOARD-TEST-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
License: MulanPSL v2
"""

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "08_BIN"))

from lh_transparent_dashboard import collect_data, DNA


def test_collect_data_structure():
    data = collect_data()
    assert data["dna"] == DNA
    assert "timestamp" in data
    assert "governance" in data
    assert "historian" in data
    assert "knowledge_graph" in data
    assert "sources" in data


def test_governance_data_fields():
    data = collect_data()
    gov = data["governance"]
    assert "available" in gov
    if gov["available"]:
        assert "counts" in gov
        assert "recent_events" in gov
        assert "recent_shame" in gov
        assert "recent_honor" in gov
        assert "recent_shadow_ai" in gov
        assert "agent_bindings" in gov


def test_api_endpoints():
    try:
        from fastapi.testclient import TestClient
        from lh_transparent_dashboard import app
    except Exception:
        pytest.skip("未安装 fastapi / testclient")

    client = TestClient(app)

    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["dna"] == DNA

    r = client.get("/api/data")
    assert r.status_code == 200
    body = r.json()
    assert body["dna"] == DNA
    assert "governance" in body

    r = client.get("/")
    assert r.status_code == 200
    assert "龍魂 · 透明看板" in r.text

# ⛓️ 龍魂DNA接龍链 ──────────────────────────────
# DNA:V1|丙午·丙申·癸亥·辰时·䷗复|P04鲁班|创建|透明看板落地-君子协议可视化契约|bhash:f44ac024|chash:b0cc3a19|←GENESIS
# DNA:V2|丙午·丙申·癸亥·辰时·䷗复|P04鲁班|修改|透明看板+双语路由封装|bhash:002ae1d4|chash:2d613d10|←b0cc3a19
# ⛓️ 龍魂DNA接龍末端 ──────────────────────────────
