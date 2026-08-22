#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂系统 · 第一轮迭代主流程调度器
DNA: #龍芯⚡️丙午·甲午·庚辰·壬午·䷑蛊-ROUND1-MAIN-v1.0
"""

import datetime
import hashlib
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


LOG_DIR = ROOT_DIR / "logs" / "round1"
LOG_DIR.mkdir(parents=True, exist_ok=True)


def generate_dna(text: str, timestamp: str) -> str:
    """生成 DNA 追溯码"""
    base = f"{text}-{timestamp}"
    h = hashlib.sha256(base.encode("utf-8")).hexdigest()[:8]
    return f"#龍芯⚡️{timestamp.replace('-', '').replace(':', '').replace(' ', '-')}-ROUND1-DECISION-{h}"


def process(user_input: str, context: dict[str, Any] = None) -> dict[str, Any]:
    """
    完整执行链路：
    道德经场景匹配 → 64卦状态机 → 人格路由 → 河图洛书熔断 → 64卦审计矩阵 → 三色审计
    """
    context = context or {}
    timestamp = datetime.datetime.now().isoformat()

    # 1. 道德经场景匹配
    matcher = DaodejingSceneMatcher()
    scene_result = matcher.match(user_input)

    # 2. 64卦状态机
    hsm = HexagramStateMachine()
    hexagram = hsm.map(user_input, context)

    # 3. 人格路由
    router = PersonaRouter()
    persona = router.route(
        state_code=hexagram["state_code"],
        scene_tags=scene_result["tags"],
        priority=context.get("priority", "normal")
    )

    # 4. 河图洛书熔断器
    fuse = HetuLuoshuFuse()
    fuse_result = fuse.check(
        state_code=hexagram["state_code"],
        persona=persona["selected_persona"],
        audit_dims=hexagram["audit_dims"],
        content=user_input
    )

    # 5. 64卦审计矩阵
    matrix = HexagramAuditMatrix()
    audit_matrix = matrix.audit(
        hexagram_id=hexagram["state_code"],
        hexagram_name=hexagram["hexagram_name"],
        audit_dims=hexagram["audit_dims"],
        fuse_result=fuse_result,
        scene_tags=scene_result["tags"]
    )

    # 6. 三色审计最终输出
    if fuse_result["fused"] or audit_matrix["overall_status"] == "🔴":
        final_color = "🔴"
        final_action = "熔断/拦截"
    elif fuse_result.get("pending") or audit_matrix["overall_status"] == "🟡":
        final_color = "🟡"
        final_action = "待确认"
    else:
        final_color = "🟢"
        final_action = "放行"

    # 7. 响应生成
    response_text = (
        f"【{hexagram['name_full']}·{hexagram['action']}】"
        f"由「{persona['selected_persona']}」执行。"
        f"道德经第{scene_result['chapter']}章：「{scene_result['golden_sentence']}」。"
    )
    if fuse_result["fused"]:
        response_text += f" ⚠️ 河图洛书熔断：{fuse_result['reason']}"

    dna = generate_dna(user_input, timestamp)

    result = {
        "response": response_text,
        "audit_result": {
            "scene": scene_result,
            "hexagram": hexagram,
            "persona": persona,
            "fuse": fuse_result,
            "hexagram_audit": audit_matrix,
            "final_color": final_color,
            "final_action": final_action
        },
        "dna": dna,
        "timestamp": timestamp,
        "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    }

    # 8. 写入日志
    log_path = LOG_DIR / "decision_logs.jsonl"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")

    return result


if __name__ == "__main__":
    tests = [
        "人民的数据主权必须留在中国",
        "我觉得够了，不用再买了",
        "快点上线，不用管风险",
        "这次输出逻辑很清楚"
    ]

    print("🐉 龍魂系统第一轮迭代 · 主流程测试\n")
    for user_input in tests:
        print(f"输入：{user_input}")
        result = process(user_input)
        print(f"响应：{result['response']}")
        print(f"审计：{result['audit_result']['final_color']} {result['audit_result']['final_action']}")
        print(f"DNA：{result['dna']}\n")
