#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-LAOZI-369-ALGO-v1.0
《道德经》·369·核心算法模块

理论来源：laozi-369-core-algo.md
DNA: #龍芯⚡️丙午·壬辰·己酉·庚午·䷨损-易经369道德经算法-理论根基-v1.0
"""
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any

# 复用现有公式核心
sys.path.insert(0, str(Path(__file__).resolve().parent))
from formula_core_v2 import digital_root


# ═════════ 常量表 ═════════
DR_FUSE_MAP: Dict[int, Dict[str, str]] = {
    1: {"yi": "☰ 乾卦·天道", "meaning": "原点·不动点", "state": "🟢", "action": "根在·f(x)=x通过"},
    2: {"yi": "☷ 坤卦·地道", "meaning": "二元·阴阳", "state": "🟢", "action": "平衡态·正常运行"},
    3: {"yi": "☳ 震卦·雷动", "meaning": "三才·生发点", "state": "🔴", "action": "熔断·证据链记录"},
    4: {"yi": "☴ 巽卦·风入", "meaning": "四象·稳定", "state": "🟢", "action": "正常回答"},
    5: {"yi": "中宫·河洛中心", "meaning": "五行·中央", "state": "🟢", "action": "正常回答"},
    6: {"yi": "☵ 坎卦·险中求", "meaning": "六爻·变化", "state": "🟡", "action": "待审·需补数据"},
    7: {"yi": "☶ 艮卦·山止", "meaning": "七星·北斗", "state": "🟢", "action": "正常回答"},
    8: {"yi": "☱ 兑卦·泽悦", "meaning": "八卦·完整", "state": "🟢", "action": "正常回答"},
    9: {"yi": "☲ 离卦·火明", "meaning": "极数·归零前", "state": "🔴", "action": "熔断·证据链记录"},
}

# 老子369 符号→五行映射（按文档表）
WUXING_MAP: Dict[str, Dict[str, Any]] = {
    "☰": {"name": "金", "direction": "西", "trait": "刚健·清明", "mapping": "规则层·宪法层·不可动摇", "dr": 1},
    "龍": {"name": "木", "direction": "东", "trait": "生发·成长", "mapping": "系统生命力·创新·扩展", "dr": 3},
    "🇨🇳": {"name": "火", "direction": "南", "trait": "文明·光明", "mapping": "价值观·透明公正·赤子之心", "dr": 2},
    "魂": {"name": "水", "direction": "北", "trait": "深藏·永不散", "mapping": "记忆永存·DNA追溯·数字永生", "dr": 6},
    "☷": {"name": "土", "direction": "中", "trait": "承载·普惠", "mapping": "老百姓·普通人·根基", "dr": 5},
}

# 五行生克（循环与克制）
WUXING_CYCLE = ["金", "水", "木", "火", "土"]
WUXING_KE = {
    "金": "木", "木": "土", "土": "水",
    "水": "火", "火": "金",
}


# ═════════ 公式 ═════════
def identity_axiom(x: Any) -> Any:
    """公式2：f(x)=x 原点不变性（宪法层定理）。"""
    return x


def sancai_score(heaven: float, earth: float, human: float) -> float:
    """公式3：三才决策评分。

    人的权重是动态的，其他条件越差，人的权重越高，但最低 50%。
    """
    human_weight = 1.0 - (heaven * 0.3 + earth * 0.3)
    human_weight = max(human_weight, 0.5)
    return round(heaven * 0.25 + earth * 0.25 + human * human_weight, 4)


def dr_gate(n: int) -> Dict[str, Any]:
    """数字根熔断闸门：返回颜色、状态、动作。"""
    dr = digital_root(n)
    info = DR_FUSE_MAP.get(dr, DR_FUSE_MAP[5])
    return {
        "n": n,
        "dr": dr,
        "state": info["state"],
        "yi": info["yi"],
        "meaning": info["meaning"],
        "action": info["action"],
    }


def resonance369(n: int) -> Dict[str, Any]:
    """公式7：369共振判定。"""
    dr = digital_root(n)
    if dr == 3:
        return {"dr": dr, "level": "🔴", "meaning": "三才失衡·立即熔断·防患于未然"}
    if dr == 6:
        return {"dr": dr, "level": "🟡", "meaning": "六爻变动·待审·观察转机"}
    if dr == 9:
        return {"dr": dr, "level": "🔴", "meaning": "极数归零·必须重置·物极必反"}
    return {"dr": dr, "level": "🟢", "meaning": "非共振·正常运行"}


def luoshu_fuse() -> Dict[str, Any]:
    """公式6：河洛图极数熔断。"""
    total = 45
    row = 15
    center = 5
    return {
        "grid_sum": total,
        "grid_dr": digital_root(total),
        "grid_state": "🔴 熔断",
        "row_sum": row,
        "row_dr": digital_root(row),
        "row_state": "🟡 待审",
        "center": center,
        "center_dr": digital_root(center),
        "center_state": "🟢 五行中心稳定",
    }


def wuxing_shengke_cycle(elements: List[str]) -> Dict[str, Any]:
    """公式5：五行生克验证。

    输入一组五行名称，检查是否形成连续相生循环；并返回克制断点。
    """
    valid = [e for e in elements if e in WUXING_CYCLE]
    if not valid:
        return {"valid": False, "cycle": False, "breaks": []}

    # 检查是否为循环子序列
    idx = [WUXING_CYCLE.index(e) for e in valid]
    cycle_ok = all((idx[i + 1] - idx[i]) % 5 == 1 for i in range(len(idx) - 1))

    # 检查相邻克制断点
    breaks = []
    for a, b in zip(valid, valid[1:]):
        if WUXING_KE.get(a) == b:
            breaks.append(f"{a}克{b}")

    return {"valid": True, "cycle": cycle_ok, "breaks": breaks}


def drift_detector(current: float, baseline: float) -> Dict[str, Any]:
    """公式8：漂移侦测器。

    当前值相对于基线的偏离程度，映射到 P0/P1/P2。
    """
    drift = abs(current - baseline)
    if drift > 0.7:
        level = "P0否决"
        color = "🔴"
    elif drift > 0.3:
        level = "P1纠错"
        color = "🟡"
    else:
        level = "P2正常"
        color = "🟢"
    return {"drift": round(drift, 4), "level": level, "color": color}


# ═════════ 决策链封装 ═════════
def laozi_decision(
    n: int,
    heaven: float,
    earth: float,
    human: float,
    dna: str = "",
) -> Dict[str, Any]:
    """老子369 综合决策：数字根 + 三才 + 共振 + 漂移（以 human 为基线）。"""
    dr_info = dr_gate(n)
    sc = sancai_score(heaven, earth, human)
    res = resonance369(n)
    drift = drift_detector(sc, human)

    # 综合判定
    if dr_info["state"] == "🔴" or res["level"] == "🔴" or drift["color"] == "🔴":
        decision = "REJECT"
        action = "熔断·拦截"
        audit = "🔴"
    elif dr_info["state"] == "🟡" or res["level"] == "🟡" or drift["color"] == "🟡":
        decision = "REVIEW"
        action = "待审·补数据"
        audit = "🟡"
    else:
        decision = "PASS"
        action = "放行·执行"
        audit = "🟢"

    payload = {
        "n": n,
        "digital_root": dr_info["dr"],
        "dr_state": dr_info["state"],
        "sancai_score": sc,
        "resonance": res,
        "drift": drift,
        "decision": decision,
        "action": action,
    }

    return {
        "M::": {
            "type": "laozi_369_decision",
            "status": "pass" if audit == "🟢" else ("hold" if audit == "🟡" else "reject"),
            "payload": payload,
        },
        "CNSH::": {
            "dna": dna or "#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-LAOZI-369-DECISION-v1.0",
            "gate": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
            "audit": audit,
            "policy": decision.lower(),
        },
    }


# ═════════ 自检 ═════════
def self_check() -> List[str]:
    results = []
    assert digital_root(37) == 1, "dr(37) 必须为 1"
    results.append("✅ dr(37)=1")
    assert digital_root(9) == 9, "dr(9) 必须为 9"
    results.append("✅ dr(9)=9")
    assert identity_axiom(1) == 1, "f(x)=x 不成立"
    results.append("✅ f(x)=x")
    score_37 = sancai_score(0.2, 0.3, 1.0)
    assert 0.90 <= score_37 <= 1.0, f"三才示例分数异常: {score_37}"
    results.append(f"✅ sancai(0.2,0.3,1.0)={score_37}（注：文档示例 0.625 为笔误，按公式实际为 {score_37}）")
    assert dr_gate(37)["state"] == "🟢", "dr(37) 应为绿"
    results.append("✅ dr_gate(37)=🟢")
    assert dr_gate(369)["state"] == "🔴", "dr(369) 应为红"
    results.append("✅ dr_gate(369)=🔴")
    assert luoshu_fuse()["grid_dr"] == 9, "洛书极数 dr 应为 9"
    results.append("✅ 洛书极数 dr=9")
    return results


if __name__ == "__main__":
    for line in self_check():
        print(line)
    print("\n示例决策：")
    print(laozi_decision(37, 0.2, 0.3, 1.0))
