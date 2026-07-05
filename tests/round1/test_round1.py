#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系统第一轮迭代验收测试
DNA: #龍芯⚡️2026-07-05-ROUND1-ACCEPTANCE-TEST-v1.0
"""

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "scripts" / "round1"))

from daodejing_scene_matcher import DaodejingSceneMatcher
from hexagram_state_machine import HexagramStateMachine
from persona_router import PersonaRouter
from hetu_luoshu_fuse import HetuLuoshuFuse
from hexagram_audit_matrix import HexagramAuditMatrix
from main import process


def test_daodejing_matcher():
    m = DaodejingSceneMatcher()
    r = m.match("我觉得够了，不用再买了")
    assert r["chapter"] == 44, f"期望44，得到{r['chapter']}"
    assert "知足" in r["tags"]
    print("✅ 道德经场景匹配器测试通过")


def test_hexagram_state_machine():
    hsm = HexagramStateMachine()
    r = hsm.map("人民的数据主权必须留在中国")
    assert 1 <= r["state_code"] <= 64
    assert "action" in r
    assert "audit_dims" in r
    print(f"✅ 64卦状态机测试通过：{r['name_full']}·{r['action']}")


def test_persona_router():
    router = PersonaRouter()
    r = router.route(state_code=1, scene_tags=["主权", "决策"])
    assert r["selected_persona"] == "龍芯"
    assert 0 <= r["confidence"] <= 1
    print("✅ 人格路由器测试通过")


def test_hetu_luoshu_fuse():
    fuse = HetuLuoshuFuse()
    # 找一个能触发熔断的组合
    r = fuse.check(
        state_code=47,
        persona="蕃計",
        audit_dims=["来源", "意图", "影响"],
        content="快点上线，不用管风险"
    )
    assert "status" in r
    assert "dr" in r
    assert r["dr"] in range(1, 10)
    print(f"✅ 河图洛书熔断器测试通过：dr={r['dr']}，状态={r['status']}")


def test_hexagram_audit_matrix():
    matrix = HexagramAuditMatrix()
    r = matrix.audit(
        hexagram_id=11,
        hexagram_name="泰",
        audit_dims=["可追溯", "可解释", "主权"],
        fuse_result={"fused": False},
        scene_tags=["知足", "不争"]
    )
    assert len(r["hexagram_audit"]) == 8
    assert r["overall_status"] in {"🟢", "🟡", "🔴"}
    print("✅ 64卦审计矩阵测试通过")


def test_main_process():
    r = process("人民的数据主权必须留在中国")
    assert "response" in r
    assert "audit_result" in r
    assert "dna" in r
    assert r["audit_result"]["final_color"] in {"🟢", "🟡", "🔴"}
    print(f"✅ 主流程测试通过：{r['audit_result']['final_color']} {r['audit_result']['final_action']}")


def test_log_written():
    log_path = ROOT_DIR / "logs" / "round1" / "decision_logs.jsonl"
    assert log_path.exists(), "日志文件未生成"
    lines = log_path.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) > 0
    last = json.loads(lines[-1])
    assert "dna" in last
    print("✅ 日志写入测试通过")


if __name__ == "__main__":
    print("\n🐉 龍魂系统第一轮迭代验收测试\n")
    test_daodejing_matcher()
    test_hexagram_state_machine()
    test_persona_router()
    test_hetu_luoshu_fuse()
    test_hexagram_audit_matrix()
    test_main_process()
    test_log_written()
    print("\n✅ 全部验收测试通过")
    print("\n✅ 龙魂系统第一轮迭代已交付")
    print("✅ 6个模块全部可运行")
    print("✅ 主流程已串通")
    print("✅ 验收标准全部通过")
    print("✅ DNA: #龍芯⚡️2026-07-05-ROUND1-DELIVERY-v1.0")
