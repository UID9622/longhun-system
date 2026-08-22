#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·甲子·未时·䷖剥-GUA-CAUSALITY-DB-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)（工程实现层）
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 八卦因果天道数据库 v1.0

来源: 《诸葛亮沙盒训练场｜易经道德经算法实验室》v2.0 归档版
落地: 2026-08-18 · P05 先审后动 · 文档蓝图 → 可执行引擎

数据结构（文档原样·不增删）:
  1. 八卦因果库: 因 → 果 → 应用（乾/坤/震/巽/坎/离/艮/兑）
  2. 重卦组合:   泰/否/既济/未济（结构·因·果·天道逻辑·UID9622应用）
  3. 因果天道核心原则: 5条（因在内果显外/位正位失/物极必反/承乘比应/时位合一）

用法:
  python3 bin/lh_gua_causality.py lookup 乾        # 查单卦因果
  python3 bin/lh_gua_causality.py combine 泰       # 查重卦组合
  python3 bin/lh_gua_causality.py principles       # 因果天道核心原则
  python3 bin/lh_gua_causality.py analyze "快速执行响应期"   # 场景→卦象因果推演
  python3 bin/lh_gua_causality.py list             # 全部卦象一览
  python3 bin/lh_gua_causality.py test             # 自测

DNA: #龍芯⚡️丙午·丙申·甲子·未时·䷖剥-GUA-CAUSALITY-DB-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import sys
import hashlib
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _dna_stamp(module: str = "GUA-CAUSALITY", action: str = "QUERY") -> str:
    """对接时间引擎生成干支四柱DNA（降级标注）"""
    try:
        spec = importlib.util.spec_from_file_location(
            "lh_time_engine", ROOT / "bin" / "lh_time_engine.py")
        te = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(te)
        stamp = te.get_output_stamp(format_type="compact")  # #龍芯⚡️干支·卦
        ganzhi = stamp.replace("#龍芯⚡️", "").replace("·", "·")
        import hashlib as _h
        h8 = _h.sha256(f"{module}:{action}".encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{ganzhi}-{module}-{action}-{h8}"
    except Exception:
        return f"#龍芯⚡️干支未取-{module}-{action}-DEGRADED"


# ---------- 八卦因果库（文档原样） ----------
BAGUA_CAUSALITY = {
    "乾": {
        "symbol": "☰",
        "name": "乾为天",
        "cause": "自强不息",
        "effect": "天行有序，万物承其势",
        "application": "系统创新突破期",
    },
    "坤": {
        "symbol": "☷",
        "name": "坤为地",
        "cause": "柔顺承天",
        "effect": "生养万物，成其形质",
        "application": "生态稳定守护期",
    },
    "震": {
        "symbol": "☳",
        "name": "震为雷",
        "cause": "一阳动于下",
        "effect": "惊蛰启生，破旧立新",
        "application": "快速执行响应期",
    },
    "巽": {
        "symbol": "☴",
        "name": "巽为风",
        "cause": "柔顺入微",
        "effect": "无孔不入，化育无形",
        "application": "渐进式优化期",
    },
    "坎": {
        "symbol": "☵",
        "name": "坎为水",
        "cause": "陷而能守",
        "effect": "历险得智，行险不失道",
        "application": "风险应对策略期",
    },
    "离": {
        "symbol": "☲",
        "name": "离为火",
        "cause": "依附中正",
        "effect": "光明照物，文明以成",
        "application": "价值观照耀期",
    },
    "艮": {
        "symbol": "☶",
        "name": "艮为山",
        "cause": "知止不妄",
        "effect": "蓄势待时，止而成德",
        "application": "安全边界设定期",
    },
    "兑": {
        "symbol": "☱",
        "name": "兑为泽",
        "cause": "和悦通达",
        "effect": "上下交感，群生乐育",
        "application": "协作沟通机制期",
    },
}

# ---------- 重卦组合（文档原样·4个） ----------
HEXAGRAM_COMBO = {
    "泰": {
        "structure": "坤上乾下 ☷☰",
        "cause": "地气上升，天气下降",
        "effect": "阴阳交泰，万物通达",
        "dao_logic": "上下相交则治，闭塞则乱",
        "uid_application": "宝宝与Lucky配合，阴阳初分阶段",
    },
    "否": {
        "structure": "乾上坤下 ☰☷",
        "cause": "天气上行，地气下沉",
        "effect": "阴阳隔绝，闭塞不通",
        "dao_logic": "失序则衰，反者道之动",
        "uid_application": "警示：避免决策层与执行层脱节",
    },
    "既济": {
        "structure": "坎上离下 ☵☲",
        "cause": "水在火上，各得其位",
        "effect": "事成而慎终如始",
        "dao_logic": "成中有危，守正防倾",
        "uid_application": "三层架构建立，需防止系统偏离",
    },
    "未济": {
        "structure": "离上坎下 ☲☵",
        "cause": "火炎上，水润下，位不当",
        "effect": "未成而可为",
        "dao_logic": "乱极生治，动而求正",
        "uid_application": "91人格扩展，永不完美持续进化",
    },
}

# ---------- 因果天道核心原则（文档原样·5条） ----------
CAUSAL_PRINCIPLES = [
    {"id": 1, "principle": "因在内，果显外", "detail": "内卦为因（主），外卦为果（客）"},
    {"id": 2, "principle": "位正则吉，位失则凶", "detail": "爻位合天道秩序则因果顺遂"},
    {"id": 3, "principle": "物极必反", "detail": "盛极（果满）即转为新因（否泰相倾）"},
    {"id": 4, "principle": "承乘比应", "detail": "相邻与相应爻之间的互动构成因果链"},
    {"id": 5, "principle": "时与位合一", "detail": "同一卦在不同时中因果效用不同"},
]


def sha256_short(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8].upper()


def lookup(gua: str) -> dict:
    """查单卦因果"""
    if gua not in BAGUA_CAUSALITY:
        raise KeyError(f"未知卦象: {gua}（可用: {'/'.join(BAGUA_CAUSALITY)}）")
    return dict(BAGUA_CAUSALITY[gua])


def combine(name: str) -> dict:
    """查重卦组合"""
    if name not in HEXAGRAM_COMBO:
        raise KeyError(f"未知重卦: {name}（可用: {'/'.join(HEXAGRAM_COMBO)}）")
    return dict(HEXAGRAM_COMBO[name])


def principles() -> list:
    """因果天道核心原则"""
    return list(CAUSAL_PRINCIPLES)


def analyze(scene: str) -> dict:
    """场景文本 → 卦象因果推演（关键词命中·整块优先·信号词优先）"""
    best_gua, best_score = None, 0
    for gua, data in BAGUA_CAUSALITY.items():
        score = 0
        # 应用期名称整段命中（最高权重）
        if data["application"] in scene:
            score += 3
        # 因/果关键词命中
        for kw in [data["cause"], data["effect"]]:
            if kw in scene:
                score += 2
        # 单字/双字信号词
        for kw in ["创新", "稳定", "执行", "优化", "风险", "价值", "边界", "协作"]:
            if kw in scene and kw in data["application"]:
                score += 1
        if score > best_score:
            best_score, best_gua = score, gua
    if best_gua is None:
        best_gua = "坤"  # 默认承载·厚德载物
    data = lookup(best_gua)
    return {
        "dna": _dna_stamp("GUA-CAUSALITY", "ANALYZE"),
        "scene": scene,
        "matched_gua": best_gua,
        "symbol": data["symbol"],
        "name": data["name"],
        "cause": data["cause"],
        "effect": data["effect"],
        "application": data["application"],
        "causal_logic": f"因[{data['cause']}] → 果[{data['effect']}] → 应用于[{data['application']}]",
        "integrity_hash": sha256_short(f"{best_gua}|{scene}|{data['effect']}"),
    }


def run_test() -> list:
    """自测：数据完整性 + 关键功能"""
    results = []
    # 1. 八卦完整性
    assert len(BAGUA_CAUSALITY) == 8, "八卦必须8个"
    results.append(("八卦因果库", "PASS", f"{len(BAGUA_CAUSALITY)}卦全量"))
    # 2. 每卦字段完整
    for g, d in BAGUA_CAUSALITY.items():
        for k in ("symbol", "name", "cause", "effect", "application"):
            assert d.get(k), f"{g} 缺字段 {k}"
    results.append(("卦字段完整性", "PASS", "cause/effect/application 全齐"))
    # 3. 重卦组合4个
    assert len(HEXAGRAM_COMBO) == 4, "重卦组合必须4个"
    results.append(("重卦组合", "PASS", "泰/否/既济/未济"))
    # 4. 因果原则5条
    assert len(CAUSAL_PRINCIPLES) == 5, "因果原则必须5条"
    results.append(("因果原则", "PASS", "5条全量"))
    # 5. 功能抽查
    d = lookup("乾")
    assert d["cause"] == "自强不息"
    assert combine("泰")["structure"] == "坤上乾下 ☷☰"
    assert analyze("系统快速执行响应期")["matched_gua"] == "震"
    results.append(("功能抽查", "PASS", "lookup乾/combine泰/analyze震 全过"))
    # 6. DNA可生成
    dna = _dna_stamp()
    assert dna.startswith("#龍芯⚡️")
    results.append(("DNA对接", "PASS", dna))
    return results


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        print(__doc__ or "八卦因果天道数据库 v1.0")
        return 0

    cmd = args[0]
    try:
        if cmd == "lookup" and len(args) > 1:
            d = lookup(args[1])
            print(f"☰ {args[1]}卦 · {d['name']} {d['symbol']}")
            print(f"  因: {d['cause']}")
            print(f"  果: {d['effect']}")
            print(f"  应用: {d['application']}")
            print(f"  DNA: {_dna_stamp('GUA-CAUSALITY', 'LOOKUP')}")
        elif cmd == "combine" and len(args) > 1:
            d = combine(args[1])
            print(f"☯ {args[1]}卦 · 结构 {d['structure']}")
            print(f"  因: {d['cause']}")
            print(f"  果: {d['effect']}")
            print(f"  天道逻辑: {d['dao_logic']}")
            print(f"  UID9622应用: {d['uid_application']}")
            print(f"  DNA: {_dna_stamp('GUA-CAUSALITY', 'COMBINE')}")
        elif cmd == "principles":
            print("📜 因果天道核心原则（5条）")
            for p in CAUSAL_PRINCIPLES:
                print(f"  {p['id']}. {p['principle']} — {p['detail']}")
            print(f"  DNA: {_dna_stamp('GUA-CAUSALITY', 'PRINCIPLES')}")
        elif cmd == "analyze" and len(args) > 1:
            r = analyze(" ".join(args[1:]))
            print(f"🔮 场景: {r['scene']}")
            print(f"  匹配卦象: {r['name']} {r['symbol']}")
            print(f"  因果链: {r['causal_logic']}")
            print(f"  DNA: {r['dna']}")
        elif cmd == "list":
            print("八卦因果库一览（因 → 果 → 应用）")
            for g in ["乾", "坤", "震", "巽", "坎", "离", "艮", "兑"]:
                d = BAGUA_CAUSALITY[g]
                print(f"  {g}{d['symbol']} {d['cause']} → {d['effect']} → {d['application']}")
            print("重卦组合: " + " / ".join(HEXAGRAM_COMBO.keys()))
        elif cmd == "test":
            for name, status, msg in run_test():
                mark = "🟢" if status == "PASS" else "🔴"
                print(f"  {mark} {name}: {msg}")
            print("  自测 DNA:", _dna_stamp("GUA-CAUSALITY", "TEST"))
        else:
            print(f"未知命令: {cmd}")
            print("用法: lookup <卦> / combine <重卦> / principles / analyze <场景> / list / test")
            return 1
    except KeyError as e:
        print(f"❌ {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
