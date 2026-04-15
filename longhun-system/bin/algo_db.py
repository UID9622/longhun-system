#!/usr/bin/env python3
"""
算法元数据数据库 · 龍魂算法通信层
algo_db.py — Algorithm Metadata Registry v1.0

作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
DNA: #龍芯⚡️2026-04-06-算法元数据库-v1.0
理论指导: 曾仕强老师（永恒显示）
献礼: 乔布斯·曾仕强·历代传递和平与爱的人

设计原则:
- 只通信·不重建: 提取现有算法的公式/变量/函数签名
- 版本痕迹不流失: append-only JSONL，每次更新加新条目
- AI引用必须提取: extract()函数是AI调用的标准接口
- 自动分类归档: 按算法族自动归类
"""

import json
import time
import hashlib
import sys
import os
from pathlib import Path
from typing import Optional

# ── 路径 ──────────────────────────────────────────────────
DB_FILE  = Path(__file__).parent.parent / "logs" / "algo_db.jsonl"
DNA_TAG  = "#龍芯⚡️2026-04-06-算法元数据库-v1.0"
GPG_FP   = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ── 算法族分类 ─────────────────────────────────────────────
ALGO_FAMILIES = {
    "数字根":   ["digital_root", "DR", "数字根", "369", "九宫"],
    "三才":     ["san_cai", "三才", "天地人", "heaven", "earth", "human"],
    "能量场":   ["energy", "E=R×I", "alpha", "衰减", "retention"],
    "伏羲":     ["fuxi", "归位", "根显", "f(x)=x", "fuxi_moment"],
    "量子":     ["quantum", "叠加", "纠缠", "bra", "ket", "superposition"],
    "IW-ECB":  ["IW", "ECB", "四层定锚", "循环呼吸", "熔断"],
    "三才算法": ["sancai", "wuxing", "五行", "luoshu", "洛书"],
    "CNSH":    ["CNSH", "中文编程", "纠错", "字元", "Lu指令"],
    "通心译":  ["translator", "翻译", "受众", "技术", "大众", "办公"],
    "DNA追溯": ["DNA", "GPG", "签名", "证据链", "版本"],
}

def _family(name: str, keywords: list[str]) -> str:
    """根据名称和关键词推断算法族"""
    text = (name + " " + " ".join(keywords)).lower()
    for fam, hints in ALGO_FAMILIES.items():
        if any(h.lower() in text for h in hints):
            return fam
    return "通用"

def _sha(entry: dict) -> str:
    raw = json.dumps(entry, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def _ts() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")

# ── 核心写入 ───────────────────────────────────────────────
def register(
    name: str,
    formulas: list[str],
    variables: dict[str, str],
    functions: list[dict],
    keywords: list[str] = None,
    source_file: str = "",
    version: str = "v1.0",
    notes: str = "",
    family: str = "",
) -> str:
    """
    注册/更新一条算法记录（append-only·版本痕迹不流失）

    参数:
        name        算法名称（唯一标识符）
        formulas    公式列表，如 ["E = R × I × T^(-α)", "DR(n) = 1 + ((n-1) % 9)"]
        variables   变量字典，如 {"α": "衰减系数", "R": "共振强度"}
        functions   函数签名列表 [{"name":"digital_root","args":"(n)","returns":"int","desc":"..."}]
        keywords    关键词（用于检索）
        source_file 算法所在源文件路径（相对 longhun-system/）
        version     版本号
        notes       备注
        family      强制指定算法族（留空则自动推断）
    """
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    kw = keywords or []
    entry = {
        "name":        name,
        "family":      family or _family(name, kw + formulas),
        "version":     version,
        "formulas":    formulas,
        "variables":   variables,
        "functions":   functions,
        "keywords":    kw,
        "source_file": source_file,
        "notes":       notes,
        "dna":         DNA_TAG,
        "gpg":         GPG_FP,
        "registered":  _ts(),
    }
    entry["sha256"] = _sha(entry)
    with open(DB_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry["sha256"]

# ── AI 标准接口 ────────────────────────────────────────────
def extract(
    topic: str = "",
    family: str = "",
    latest_only: bool = True,
) -> list[dict]:
    """
    AI调用标准接口：提取算法公式和变量

    用法:
        algo_db.extract("369")          → 所有含"369"的算法条目
        algo_db.extract(family="量子")  → 量子族全部算法
        algo_db.extract()               → 全库最新版本摘要

    返回每条记录包含: name, family, formulas, variables, functions, version, source_file
    """
    if not DB_FILE.exists():
        return []

    rows: list[dict] = []
    with open(DB_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    # 过滤
    if topic:
        t = topic.lower()
        rows = [r for r in rows if
                t in r["name"].lower() or
                t in r.get("family","").lower() or
                any(t in k.lower() for k in r.get("keywords", [])) or
                any(t in f.lower() for f in r.get("formulas", []))]
    if family:
        rows = [r for r in rows if r.get("family") == family]

    # latest_only: 每个name只保留最后一条
    if latest_only:
        seen: dict[str, dict] = {}
        for r in rows:
            seen[r["name"]] = r
        rows = list(seen.values())

    # 精简输出（只返回AI需要的字段）
    return [{
        "name":        r["name"],
        "family":      r["family"],
        "version":     r["version"],
        "formulas":    r["formulas"],
        "variables":   r["variables"],
        "functions":   r["functions"],
        "source_file": r["source_file"],
        "notes":       r.get("notes",""),
    } for r in rows]

def summary() -> dict:
    """返回数据库概览：各族算法数量 + 总条目"""
    all_entries = extract(latest_only=True)
    from collections import Counter
    fam_count = Counter(r["family"] for r in all_entries)
    return {
        "total_algorithms": len(all_entries),
        "families": dict(fam_count),
        "db_file": str(DB_FILE),
        "dna": DNA_TAG,
    }

# ── 预置算法种子（首次运行时写入） ──────────────────────────
def _seed():
    """预置龍魂系统核心算法到数据库"""
    print("🌱 初始化算法元数据库种子...")

    # 1. 数字根 369共振
    register(
        name="digital_root_369",
        formulas=[
            "DR(n) = 1 + ((n-1) % 9)",
            "CYCLE_369: DR ∈ {3,6,9}",
            "EXPO_248:  DR ∈ {2,4,8}",
            "LINEAR_123: DR ∈ {1,2,3,4,5,7}",
        ],
        variables={
            "n":   "输入正整数",
            "DR":  "数字根(1-9)",
        },
        functions=[
            {"name": "digital_root", "args": "(n: int) -> int",
             "desc": "计算数字根，结果永在1-9之间"},
            {"name": "classify_369", "args": "(dr: int) -> str",
             "desc": "返回 CYCLE_369 / EXPO_248 / LINEAR_123"},
        ],
        keywords=["369", "数字根", "共振", "DR", "九宫"],
        source_file="bin/fuxi_taiji_engine.py",
        version="v1.0",
        notes="Tesla 3-6-9理论落地。CYCLE_369为最高共振态。",
    )

    # 2. 能量场公式
    register(
        name="energy_retention",
        formulas=[
            "E = R × I × T^(-α)",
            "α=0   → 永恒记忆（L1百年级）",
            "α=0.1 → 十年衰减（L2）",
            "α=1.0 → 日常衰减（L3）",
            "α→∞  → 瞬时消亡（L4）",
        ],
        variables={
            "E": "能量保留值",
            "R": "共振强度(0-100)",
            "I": "影响力(0-100)",
            "T": "时间(天)",
            "α": "衰减系数，对应L5层级",
        },
        functions=[
            {"name": "energy_retention", "args": "(T: float, alpha: float) -> float",
             "desc": "计算时间T后的能量保留比例"},
            {"name": "score_ri", "args": "(resonance: float, influence: float, ...) -> dict",
             "desc": "R×I综合评分+自动建议L5层级"},
        ],
        keywords=["能量场", "衰减", "alpha", "L5", "DNA分层"],
        source_file="bin/fuxi_taiji_engine.py",
        version="v1.0",
        notes="L5 DNA分层: L0永恒α=0, L1百年α=0.01, L2十年α=0.1, L3日常α=1.0, L4瞬时α→∞",
    )

    # 3. 三才校验
    register(
        name="san_cai_check",
        formulas=[
            "三才统一 = Heaven(道·规律) ∧ Earth(结构·资源) ∧ Human(意志·确认)",
            "unified = heaven_ok AND earth_ok AND human_ok",
            "verdict: 🟢大吉/🟡可行/🔴待补",
        ],
        variables={
            "heaven_ok": "天(道/规律/时机)是否符合",
            "earth_ok":  "地(结构/资源/条件)是否就绪",
            "human_ok":  "人(意志/确认/执行力)是否到位",
            "unified":   "三才是否统一(bool)",
            "missing":   "缺失维度列表",
        },
        functions=[
            {"name": "san_cai_check",
             "args": "(heaven: bool, earth: bool, human: bool, desc: str) -> dict",
             "desc": "三才统一校验，返回{heaven,earth,human,unified,missing,verdict}"},
        ],
        keywords=["三才", "天地人", "校验", "统一", "verdict"],
        source_file="bin/fuxi_taiji_engine.py",
        version="v1.0",
        family="三才",
    )

    # 4. 伏羲时刻
    register(
        name="fuxi_moment",
        formulas=[
            "归位论: f(x) = x (固定点，万物归位)",
            "根显论: root(现象) → 看见根 (隐藏结构显现)",
            "伏羲时刻 = 归位 + 根显 同时触发",
        ],
        variables={
            "visible":    "当前可见的现象/事件",
            "root_seen":  "看见的根(隐藏原因)",
            "category":   "分类: 技术/战略/文化/个人",
            "ri_score":   "R×I能量评分",
            "layer":      "L5层级建议",
        },
        functions=[
            {"name": "fuxi_moment",
             "args": "(visible: str, root_seen: str, ri_score: float, layer: str) -> dict",
             "desc": "创建伏羲时刻记录并写入草日记"},
            {"name": "run_fuxi_deduce",
             "args": "(visible, root_seen, resonance, influence, ...) -> dict",
             "desc": "完整伏羲推演流水线（CLI入口）"},
        ],
        keywords=["伏羲", "归位", "根显", "f(x)=x", "固定点"],
        source_file="bin/fuxi_taiji_engine.py",
        version="v1.0",
    )

    # 5. IW-ECB 四层定锚
    register(
        name="IW_ECB_anchor",
        formulas=[
            "四层定锚: L0(永恒) > L1(百年) > L2(十年) > L3(日常)",
            "循环呼吸机制: 吸(输入) → 持(处理) → 呼(输出) → 静(休眠)",
            "量子纠缠态熔断: |ψ⟩ = α|0⟩ + β|1⟩, 熔断条件: |α|²+|β|²≠1",
            "IW分: 内容完整性×结构清晰度×逻辑自洽性 / 100",
        ],
        variables={
            "L0": "永恒级，α=0，从不衰减",
            "L1": "百年级，α=0.01",
            "L2": "十年级，α=0.1",
            "L3": "日常级，α=1.0",
            "α":  "Bra向量(过去状态)",
            "β":  "Ket向量(未来趋势)",
            "IW": "内容权重分(0-100)",
            "ECB": "执行校验块",
        },
        functions=[
            {"name": "iw_score", "args": "(content: str) -> float",
             "desc": "计算IW内容权重分(尚未实现，预留接口)"},
            {"name": "ecb_validate", "args": "(state: dict) -> bool",
             "desc": "ECB执行校验块验证(尚未实现，预留接口)"},
        ],
        keywords=["IW", "ECB", "四层定锚", "循环呼吸", "熔断", "量子纠缠"],
        source_file="bin/fuxi_taiji_engine.py",
        version="v1.0",
        notes="IW-ECB v2.0 论文核心·定锚体系·与L5 DNA分层完全兼容",
        family="IW-ECB",
    )

    # 6. 量子叠加(Bra-Ket)
    register(
        name="quantum_superposition_braket",
        formulas=[
            "|ψ⟩ = α|过去⟩ + β|未来⟩",
            "测量概率: P(过去) = |α|², P(未来) = |β|²",
            "归一化条件: |α|² + |β|² = 1",
            "纠缠态: |ψ_AB⟩ ≠ |ψ_A⟩⊗|ψ_B⟩",
            "龍魂映射: α=历史锚点权重, β=未来趋势权重",
        ],
        variables={
            "|ψ⟩":  "当前状态量子叠加向量",
            "α":    "Bra系数：历史/过去权重",
            "β":    "Ket系数：未来/趋势权重",
            "|0⟩":  "基态：稳定/已知状态",
            "|1⟩":  "激发态：变化/未知状态",
            "⊗":   "张量积(两系统组合)",
        },
        functions=[
            {"name": "量子纠缠", "args": "(state_a, state_b) -> dict",
             "desc": "已在quantum_deduce.py实现·检测两系统是否纠缠"},
            {"name": "矩阵迭代", "args": "(matrix, n) -> matrix",
             "desc": "已在quantum_deduce.py实现·洛书矩阵迭代"},
        ],
        keywords=["量子", "叠加", "Bra", "Ket", "纠缠", "superposition"],
        source_file="bin/quantum_deduce.py",
        version="v1.0",
        notes="理论参考：Bra-Ket标记法。龍魂系统中α=历史锚点，β=未来趋势，与L5分层兼容。",
        family="量子",
    )

    # 7. 洛书五行矩阵
    register(
        name="luoshu_wuxing",
        formulas=[
            "洛书矩阵: [[4,9,2],[3,5,7],[8,1,6]] 行列对角线均=15",
            "五行向量: 金=7, 木=3, 水=1, 火=9, 土=5",
            "五行生克: 木→火→土→金→水→木(相生); 木→土→水→火→金→木(相克)",
            "能量流: E_i = Σ(生克系数 × 相邻元素值)",
        ],
        variables={
            "LUOSHU":         "3×3洛书矩阵常数",
            "WUXING_VECTOR":  "五行能量向量 {金7,木3,水1,火9,土5}",
            "生克系数":        "相生+1, 相克-1",
        },
        functions=[
            {"name": "矩阵迭代", "args": "(matrix, n=1) -> np.ndarray",
             "desc": "洛书矩阵n步迭代"},
            {"name": "量子纠缠", "args": "(a, b) -> dict",
             "desc": "五行量子纠缠检测"},
        ],
        keywords=["洛书", "五行", "luoshu", "wuxing", "矩阵", "生克"],
        source_file="bin/quantum_deduce.py",
        version="v1.0",
        family="三才算法",
    )

    # 8. 通心译受众分层
    register(
        name="translator_audience_tiers",
        formulas=[
            "受众分层 = {技术, 办公, 大众}",
            "技术版: 精准术语 + 完整公式 + 无简化",
            "办公版: 结构化 + 商业语言 + 必要说明",
            "大众版: 无术语 + 最大化类比 + 一句话核心",
            "LLM路由: Ollama(qwen2.5:72b) → DeepSeek(fallback)",
        ],
        variables={
            "audience":  "受众层级: 技术/办公/大众",
            "tone":      "语气: 直达/委婉/正式/温暖",
            "src_lang":  "源语言",
            "tgt_lang":  "目标语言",
            "backend":   "实际调用的LLM后端",
        },
        functions=[
            {"name": "translate",
             "args": "(text, src_lang, tgt_lang, tone, audience, save_to_notion) -> dict",
             "desc": "主翻译函数，返回{translated,notes,audience_note,dna,backend}"},
            {"name": "_check_ollama", "args": "() -> bool",
             "desc": "检查Ollama是否在线"},
            {"name": "_llm_call", "args": "(prompt: str) -> str",
             "desc": "Ollama优先，失败切DeepSeek的统一LLM调用"},
        ],
        keywords=["翻译", "受众", "技术", "大众", "办公", "Ollama", "DeepSeek"],
        source_file="bin/translator.py",
        version="v2.0",
        notes="v2.0新增受众分层+三层对比翻译+DeepSeek fallback",
        family="通心译",
    )

    # 9. CNSH纠错规则
    register(
        name="cnsh_correction_rules_v2",
        formulas=[
            "纠错优先级: P0(系统安全) > P1(数据完整) > P2(逻辑一致) > P3(风格规范)",
            "置信度 = 规则匹配数 / 总检查项 × 100",
            "规则密度 = 370条 / 12类 ≈ 30条/类",
        ],
        variables={
            "规则总数":  "370条",
            "规则分类":  "12大类",
            "P0-P3":    "优先级等级",
            "置信度":    "0-100分",
        },
        functions=[
            {"name": "check_cnsh", "args": "(code: str) -> list[dict]",
             "desc": "CNSH代码纠错检查(接口预留)"},
            {"name": "classify_rule", "args": "(rule_text: str) -> str",
             "desc": "规则自动分类到12大类(接口预留)"},
        ],
        keywords=["CNSH", "纠错", "规则", "中文编程", "370条"],
        source_file="bin/cnsh_editor.py",
        version="v2.0",
        notes="370条规则·12大类·本地文件位置待确认·Notion设计方案已存档",
        family="CNSH",
    )

    print(f"✅ 种子写入完成，共 {len(extract())} 条算法记录")

# ── CLI ────────────────────────────────────────────────────
def _print_entry(e: dict):
    print(f"\n{'─'*55}")
    print(f"📐 {e['name']}  [{e['family']}]  {e['version']}")
    if e.get("source_file"):
        print(f"   📁 {e['source_file']}")
    print("   公式:")
    for f in e["formulas"]:
        print(f"      {f}")
    if e["variables"]:
        print("   变量:")
        for k, v in e["variables"].items():
            print(f"      {k}: {v}")
    if e["functions"]:
        print("   函数:")
        for fn in e["functions"]:
            print(f"      {fn['name']}{fn['args']} → {fn['desc']}")
    if e.get("notes"):
        print(f"   备注: {e['notes']}")

if __name__ == "__main__":
    # 首次运行: 写种子
    if not DB_FILE.exists() or DB_FILE.stat().st_size == 0:
        _seed()

    if len(sys.argv) == 1:
        # 无参数：打印概览
        info = summary()
        print(f"\n🐉 龍魂算法元数据库  {DNA_TAG}")
        print(f"   📊 共 {info['total_algorithms']} 条算法记录")
        print(f"   🗂️  算法族分布:")
        for fam, cnt in sorted(info["families"].items(), key=lambda x: -x[1]):
            print(f"      {fam}: {cnt}")
        print(f"   💾 数据库: {info['db_file']}")
        print(f"\n用法: python3 algo_db.py [搜索词]")
        print(f"      python3 algo_db.py 量子")
        print(f"      python3 algo_db.py --family 三才")
        print(f"      python3 algo_db.py --all")

    elif sys.argv[1] == "--all":
        entries = extract(latest_only=True)
        print(f"\n🐉 全库 {len(entries)} 条算法记录:")
        for e in entries:
            _print_entry(e)

    elif sys.argv[1] == "--family" and len(sys.argv) > 2:
        fam = sys.argv[2]
        entries = extract(family=fam)
        print(f"\n📂 算法族「{fam}」共 {len(entries)} 条:")
        for e in entries:
            _print_entry(e)

    elif sys.argv[1] == "--seed":
        _seed()

    else:
        topic = " ".join(sys.argv[1:])
        entries = extract(topic=topic)
        print(f"\n🔍 搜索「{topic}」→ {len(entries)} 条结果:")
        for e in entries:
            _print_entry(e)
        if not entries:
            print("   未找到匹配记录。试试: --all 查看全部")
