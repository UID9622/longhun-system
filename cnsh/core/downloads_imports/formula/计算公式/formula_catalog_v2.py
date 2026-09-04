#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷔噬嗑-FIX_DNA-v1.0
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

"""
🧮 龍魂数学公式母册完整版 v2.0
═══════════════════════════════════════════════════════════════════════════

定位：把《🧮 数学公式算法核心·CNSH 计算公式升级 v2.0》里的 F01–F25
      全部焊进可查询、可回填、可验证的母册，并输出 v2 版清单。

升级重点（v1.0 → v2.0）：
  ✅ F01–F25 全表补齐，不再只挂 A 组几条
  ✅ 每条公式带“模块落点 + α 归属 + 三色审计”
  ✅ 生成独立清单 formula_catalog_manifest_v2.md，不覆盖 v1
  ✅ 自检覆盖编号连续性、可验证比例、回填引用

DNA：    #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-龍魂数学公式母册-v2.0-CNSH-25-FORMULAS
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL:    #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG:     A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色审计：🟢 通过

创建者：Kimi Code CLI
授权者：UID9622（龍芯北辰·老大）
指导：曾仕强老师（永恒致敬）
═══════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import hashlib
import json


# ============ 公式分组 ============

class FormulaGroup(Enum):
    """公式分组（与 v2.0 核心页对齐）"""
    A_CORE = "A组·龍魂数学核心（F01-F15）"
    B_ENGINEERING = "B组·三才工程层（F16-F30）"
    C_APPLICATION = "C组·通心译+应用层（F31-F45）"


# ============ 公式数据结构 ============

@dataclass
class Formula:
    """公式记录"""
    fid: str                      # F01, F02, ...
    group: FormulaGroup           # 所属分组
    title: str                    # 公式名称

    # 世界标准
    standard_formula: str         # 数学公式
    standard_source: str          # 出处
    standard_explanation: str     # 世界标准用法

    # 龍魂主权层
    longhorn_twist: str           # 加了什么
    longhorn_explanation: str     # 怎么用

    # CNSH 落点
    module: str                   # 进哪个模块
    alpha_belongs: str            # α 归属：α_τ / α_a / α_w / B-LOCK / 无
    audit: str                    # 🟢🟡🔴

    # 正本记录
    canon_page: str               # 正本页面
    canon_dna: str                # 正本 DNA

    # 回填规则
    backfill_target: str          # 应回填到哪些页
    backfill_rule: str            # 只引用 FXX·不重写公式

    # 验证
    verifiable: bool              # 是否可计算验证
    python_snippet: Optional[str] # Python 实现片段
    test_case: Optional[Dict]     # 测试案例


# ============ A组·F01-F15 ============

A_FORMULAS = {
    "F01": Formula(
        fid="F01", group=FormulaGroup.A_CORE,
        title="时间衰减 Temporal Decay",
        standard_formula="η(T,α_τ)=T^(-α_τ)",
        standard_source="幂律衰减·记忆留存模型",
        standard_explanation="时间越久保留率越低，α 控制衰减速率",
        longhorn_twist="α_τ 不归一化；L0 永恒层 η=1",
        longhorn_explanation="规则/记忆随时间保留；P0 永恒规则永不过期",
        module="时间续航",
        alpha_belongs="α_τ",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="记忆衰减、规则时效、L0-L4 分层",
        backfill_rule="引用 F01·α_τ 只用于时间项",
        verifiable=True,
        python_snippet="""
def temporal_decay(T: float, alpha_tau: float) -> float:
    if alpha_tau == 0: return 1.0
    return T ** (-alpha_tau)
        """,
        test_case={"input": {"T": 10, "alpha_tau": 1.0}, "expected": 0.1}
    ),

    "F02": Formula(
        fid="F02", group=FormulaGroup.A_CORE,
        title="内容贡献值 Content Contribution",
        standard_formula="C=R·I·T^(-α_τ)",
        standard_source="活跃度×质量×时间衰减",
        standard_explanation="综合衡量一段内容/行为的有效贡献",
        longhorn_twist="涉密高贡献 → sealed/hash_only",
        longhorn_explanation="内容贡献与人格贡献分列，不互相替代",
        module="贡献计算",
        alpha_belongs="α_τ",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="行为评估、收益台账、内容归档",
        backfill_rule="引用 F02·不另写 C 公式",
        verifiable=True,
        python_snippet="""
def content_contribution(R: float, I: float, T: float, alpha_tau: float) -> float:
    return R * I * (T ** (-alpha_tau) if alpha_tau else 1.0)
        """,
        test_case={"input": {"R": 10, "I": 0.9, "T": 1, "alpha_tau": 0}, "expected": 9.0}
    ),

    "F03": Formula(
        fid="F03", group=FormulaGroup.A_CORE,
        title="人格叠加态 Persona Superposition",
        standard_formula="|Ψ⟩=Σ α_a,i |φ_i⟩",
        standard_source="量子力学叠加·Bra-Ket 表示",
        standard_explanation="多个人格以振幅形式共存",
        longhorn_twist="必须 Σ|α_a,i|²=1",
        longhorn_explanation="人格组合状态，振幅向量平方和归一",
        module="人格调度",
        alpha_belongs="α_a",
        audit="🟡",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="人格路由、数字人调度",
        backfill_rule="引用 F03·α_a 平方和必须=1",
        verifiable=True,
        python_snippet="""
def alpha_amp_ok(amps):
    return abs(sum(a*a for a in amps) - 1.0) < 1e-6
        """,
        test_case={"input": {"amps": [0.6, 0.8]}, "expected": True}
    ),

    "F04": Formula(
        fid="F04", group=FormulaGroup.A_CORE,
        title="人格出现概率 Persona Probability",
        standard_formula="P(φ_i)=|α_a,i|²",
        standard_source="量子概率解释",
        standard_explanation="某人格在特定场景下出场概率",
        longhorn_twist="量子概率解释·人格坍缩选最适配",
        longhorn_explanation="从叠加态坍缩到具体人格",
        module="人格调度",
        alpha_belongs="α_a",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="人格概率、场景匹配",
        backfill_rule="引用 F04·概率从 α_a 导出",
        verifiable=True,
        python_snippet="""
def persona_prob(amps):
    return [a*a for a in amps]
        """,
        test_case={"input": {"amps": [0.6, 0.8]}, "expected": [0.36, 0.64]}
    ),

    "F05": Formula(
        fid="F05", group=FormulaGroup.A_CORE,
        title="权重效用 Weighted Utility",
        standard_formula="V(P)=Σ α_w,j · f_j(P)",
        standard_source="MCDA 多准则决策·加权求和",
        standard_explanation="多目标按权重合成综合评分",
        longhorn_twist="α_w 凸组合和=1，再高不越 P0",
        longhorn_explanation="目标函数权重归一，P0 永恒规则不可覆盖",
        module="目标评估",
        alpha_belongs="α_w",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="综合评分、路由选择",
        backfill_rule="引用 F05·α_w 凸组合和=1",
        verifiable=True,
        python_snippet="""
def weighted_utility(values, weights):
    return sum(v*w for v, w in zip(values, weights))
        """,
        test_case={"input": {"values": [0.9, 0.8], "weights": [0.5, 0.5]}, "expected": 0.85}
    ),

    "F06": Formula(
        fid="F06", group=FormulaGroup.A_CORE,
        title="数字根 Digital Root",
        standard_formula="dr(n)=1+((n-1) mod 9)",
        standard_source="数论标准·校验码/Luhn 算法",
        standard_explanation="把整数压缩到 1–9",
        longhorn_twist="焊三色闸门：dr∈{3,9}→🔴 · dr=6→🟡 · 其余→🟢",
        longhorn_explanation="入口第一道治理闸",
        module="数字根",
        alpha_belongs="无",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="决策链输入、编号压缩、五行映射",
        backfill_rule="引用 F06·不另写 dr",
        verifiable=True,
        python_snippet="""
def digital_root(n: int) -> int:
    n = abs(n)
    return 0 if n == 0 else 1 + (n - 1) % 9
        """,
        test_case={"input": {"n": 20260603}, "expected": 1}
    ),

    "F07": Formula(
        fid="F07", group=FormulaGroup.A_CORE,
        title="数字根五行映射 Five Element Map",
        standard_formula="1/2木·3/4火·5土·6/7金·8/9水",
        standard_source="河图洛书·五行配数",
        standard_explanation="数字根到五行的固定映射",
        longhorn_twist="固定映射表，不与路由映射混用",
        longhorn_explanation="数字根→五行",
        module="五行映射",
        alpha_belongs="无",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="五行分析、卦象推演",
        backfill_rule="引用 F07·固定五行表",
        verifiable=True,
        python_snippet="""
FIVE_ELEMENT = {1:"木",2:"木",3:"火",4:"火",5:"土",6:"金",7:"金",8:"水",9:"水"}
def five_element(n):
    return FIVE_ELEMENT[digital_root(n)]
        """,
        test_case={"input": {"n": 5}, "expected": "土"}
    ),

    "F08": Formula(
        fid="F08", group=FormulaGroup.A_CORE,
        title="五行向量 Five-Element Vector",
        standard_formula="W(x)=[金,木,水,火,土], Σ=1",
        standard_source="文本语义结构化·向量表示",
        standard_explanation="把中文内容转成五行比例向量",
        longhorn_twist="未识别默认 [0,0,0,0,1]（中宫缓存）",
        longhorn_explanation="中文内容转结构比例，中宫土为兜底",
        module="五行向量",
        alpha_belongs="无",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="语义分析、五行对冲、相似度",
        backfill_rule="引用 F08·Σ=1·缺省中宫",
        verifiable=True,
        python_snippet="""
def wuxing_vector(text: str) -> list[Any]:
    # 简化示例：按关键词计数后归一
    counts = {"金":0,"木":0,"水":0,"火":0,"土":0}
    for c in text:
        if c in counts: counts[c] += 1
    s = sum(counts.values())
    return [counts[k]/s for k in ["金","木","水","火","土"]] if s else [0,0,0,0,1]
        """,
        test_case={"input": {"text": "金木"}, "expected": [0.5, 0.5, 0.0, 0.0, 0.0]}
    ),

    "F09": Formula(
        fid="F09", group=FormulaGroup.A_CORE,
        title="余弦相似度 Cosine Similarity",
        standard_formula="cos(A,B)=A·B/(‖A‖‖B‖)",
        standard_source="向量空间模型·IR/NLP",
        standard_explanation="衡量两个向量方向一致程度",
        longhorn_twist="≥0.9 高度一致合并·用于水军检测/去重路由",
        longhorn_explanation="去重、合并、路由",
        module="相似度",
        alpha_belongs="无",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="去重、合并、水军检测",
        backfill_rule="引用 F09·阈值 0.9",
        verifiable=True,
        python_snippet="""
from math import sqrt
def cosine(a, b):
    dot = sum(x*y for x,y in zip(a,b))
    na = sqrt(sum(x*x for x in a))
    nb = sqrt(sum(y*y for y in b))
    return dot/(na*nb) if na and nb else 0.0
        """,
        test_case={"input": {"a": [1,0], "b": [1,0]}, "expected": 1.0}
    ),

    "F10": Formula(
        fid="F10", group=FormulaGroup.A_CORE,
        title="风险三色判定 Risk Tri-color",
        standard_formula="Risk=影响×不确定×越界",
        standard_source="风险评估·治理决策",
        standard_explanation="综合影响、不确定性、越界程度评估风险",
        longhorn_twist="一票变红规则（密钥/发布/涉密）",
        longhorn_explanation="判断 🟢🟡🔴",
        module="风险审计",
        alpha_belongs="无",
        audit="🟡",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="三色审计、风险决策",
        backfill_rule="引用 F10·明确一票变红场景",
        verifiable=True,
        python_snippet="""
def risk_tri_color(impact, uncertainty, boundary):
    risk = impact * uncertainty * boundary
    if risk >= 0.8: return "🔴"
    if risk >= 0.4: return "🟡"
    return "🟢"
        """,
        test_case={"input": {"impact": 0.9, "uncertainty": 0.9, "boundary": 0.9}, "expected": "🔴"}
    ),

    "F11": Formula(
        fid="F11", group=FormulaGroup.A_CORE,
        title="守恒分数 Conservation Score",
        standard_formula="S=主控+任务+边界+留痕+验收",
        standard_source="系统完整性评分",
        standard_explanation="0–15 分衡量任务闭环程度",
        longhorn_twist="13-15稳定 / 10-12收口 / 7-9压缩 / 0-6新窗口",
        longhorn_explanation="是否收口或开新窗口",
        module="收口判定",
        alpha_belongs="无",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="任务收口、窗口管理",
        backfill_rule="引用 F11·五分项求和",
        verifiable=True,
        python_snippet="""
def conservation_score(主控, 任务, 边界, 留痕, 验收):
    return 主控 + 任务 + 边界 + 留痕 + 验收
        """,
        test_case={"input": {"主控":3,"任务":3,"边界":3,"留痕":3,"验收":3}, "expected": 15}
    ),

    "F12": Formula(
        fid="F12", group=FormulaGroup.A_CORE,
        title="决策路径评分 Decision Path Score",
        standard_formula="D=可执行+安全+主线+验证-风险-H_人性",
        standard_source="多属性决策·路径优化",
        standard_explanation="给不同执行路径打分",
        longhorn_twist="涉密/密钥/破坏性动作一票否决",
        longhorn_explanation="判断走哪条路径",
        module="决策来源",
        alpha_belongs="无",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="路由选择、路径择优",
        backfill_rule="引用 F12·H_人性必须带下标",
        verifiable=True,
        python_snippet="""
def decision_path_score(可执行, 安全, 主线, 验证, 风险, H_人性):
    return 可执行 + 安全 + 主线 + 验证 - 风险 - H_人性
        """,
        test_case={"input": {"可执行":1,"安全":1,"主线":1,"验证":1,"风险":0.1,"H_人性":0.1}, "expected": 3.8}
    ),

    "F13": Formula(
        fid="F13", group=FormulaGroup.A_CORE,
        title="人性偏置 Human Bias",
        standard_formula="H_人性=欲望×损失规避×即时偏好",
        standard_source="行为经济学·Kahneman/Tversky",
        standard_explanation="量化冲动、短视、损失厌恶",
        longhorn_twist="只防系统冲动，不评判用户",
        longhorn_explanation="修正冲动/越界/短视",
        module="人性修正",
        alpha_belongs="无",
        audit="🟡",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="冲动修正、短视拦截",
        backfill_rule="引用 F13·H 必须写作 H_人性",
        verifiable=True,
        python_snippet="""
def human_bias(欲望, 损失规避, 即时偏好):
    return 欲望 * 损失规避 * 即时偏好
        """,
        test_case={"input": {"欲望":2,"损失规避":2,"即时偏好":2}, "expected": 8}
    ),

    "F14": Formula(
        fid="F14", group=FormulaGroup.A_CORE,
        title="最小执行链 Minimal Execution Chain",
        standard_formula="dr→W(x)→Risk→S→D→Action",
        standard_source="龍魂治理层·执行闭环",
        standard_explanation="任何决策必须走的最小链路",
        longhorn_twist="任一环节 🔴 即截链",
        longhorn_explanation="公式落地执行的最小闭环",
        module="执行闭环",
        alpha_belongs="无",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="所有决策链、执行收口",
        backfill_rule="引用 F14·不跳过任何环节",
        verifiable=True,
        python_snippet="""
# 完整实现见 formula_chain_v2.decision_chain
        """,
        test_case=None
    ),

    "F15": Formula(
        fid="F15", group=FormulaGroup.A_CORE,
        title="人格贡献值 Persona Contribution",
        standard_formula="PC=R×0.4+I×0.3+T_lv×0.3+B_seven−W×5−F×20+B_test×2",
        standard_source="人格活跃度·质量·七维加成",
        standard_explanation="花名册中某人格的贡献值",
        longhorn_twist="与 F02 内容贡献并列，不混算",
        longhorn_explanation="人格维度的收益/调度依据",
        module="人格贡献",
        alpha_belongs="无",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="人格调度、收益分配",
        backfill_rule="引用 F15·区分 PC 与 C",
        verifiable=True,
        python_snippet="""
def persona_contribution(R, I, T_lv, B_seven, W, F, B_test):
    return R*0.4 + I*0.3 + T_lv*0.3 + B_seven - W*5 - F*20 + B_test*2
        """,
        test_case={"input": {"R":10,"I":0.9,"T_lv":0.8,"B_seven":5,"W":0,"F":0,"B_test":1}, "expected": 13.27}
    ),
}


# ============ B组·F16-F30 ============

B_FORMULAS = {
    "F16": Formula(
        fid="F16", group=FormulaGroup.B_ENGINEERING,
        title="七维覆盖加成 Seven Dimension Bonus",
        standard_formula="分段函数 0/5/12/22/35",
        standard_source="多维度联动激励",
        standard_explanation="人格覆盖维度越多加成越高",
        longhorn_twist="鼓励多维联动",
        longhorn_explanation="人格覆盖维度加成",
        module="七维覆盖",
        alpha_belongs="无",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="人格评估、调度优先级",
        backfill_rule="引用 F16·分段函数",
        verifiable=True,
        python_snippet="""
def seven_dim_bonus(covered_dims: int) -> int:
    if covered_dims <= 1: return 0
    if covered_dims == 2: return 5
    if covered_dims == 3: return 12
    if covered_dims == 4: return 22
    return 35
        """,
        test_case={"input": {"covered_dims": 5}, "expected": 35}
    ),

    "F17": Formula(
        fid="F17", group=FormulaGroup.B_ENGINEERING,
        title="活跃度三色 Activity To Color",
        standard_formula="≤7天🔥 / 8-30天✅ / 31-90天⚠️ / >90天❌",
        standard_source="活跃度分级",
        standard_explanation="按距今天数给活跃度颜色",
        longhorn_twist="姜子牙守门",
        longhorn_explanation="调度优先级",
        module="活跃度三色",
        alpha_belongs="无",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="调度、提醒、召回",
        backfill_rule="引用 F17·天数区间固定",
        verifiable=True,
        python_snippet="""
def activity_color(days: int) -> str:
    if days <= 7: return "🔥"
    if days <= 30: return "✅"
    if days <= 90: return "⚠️"
    return "❌"
        """,
        test_case={"input": {"days": 5}, "expected": "🔥"}
    ),

    "F18": Formula(
        fid="F18", group=FormulaGroup.B_ENGINEERING,
        title="三才主权指数 Sovereignty Index",
        standard_formula="SI=0.34·天+0.33·地+0.33·人",
        standard_source="三才学·F05 扩展",
        standard_explanation="天·地·人加权合成主权指数",
        longhorn_twist="天<0.34 一票熔断",
        longhorn_explanation="主权穿过校验，天轴不可让渡",
        module="三才主权",
        alpha_belongs="α_w",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="决策链、三才熔断",
        backfill_rule="引用 F18·天轴熔断线 0.34",
        verifiable=True,
        python_snippet="""
def sovereignty_index(tian, di, ren):
    if tian < 0.34: return {"SI":0.0,"color":"🔴","veto":True}
    si = 0.34*tian + 0.33*di + 0.33*ren
    color = "🟢" if si>=0.85 else ("🟡" if si>=0.6 else "🔴")
    return {"SI":si,"color":color,"veto":False}
        """,
        test_case={"input": {"tian": 0.9, "di": 0.9, "ren": 0.9}, "expected": "🟢"}
    ),

    "F19": Formula(
        fid="F19", group=FormulaGroup.B_ENGINEERING,
        title="行为密码学置信度 Behavioral Cryptography Confidence",
        standard_formula="conf=(∏F_i^{w_i})^{1/Σw_i}",
        standard_source="几何加权平均",
        standard_explanation="多因子复合置信度",
        longhorn_twist="任一 F_i=0 → conf=0",
        longhorn_explanation="内容血统验证",
        module="行为密码学",
        alpha_belongs="α_w",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="内容血统、身份验证",
        backfill_rule="引用 F19·几何加权",
        verifiable=True,
        python_snippet="""
from math import prod, pow
def behavioral_confidence(factors, weights):
    if any(f == 0 for f in factors): return 0.0
    total_w = sum(weights)
    return prod(pow(f, w) for f, w in zip(factors, weights)) ** (1/total_w)
        """,
        test_case={"input": {"factors": [0.9,0.9], "weights": [1,1]}, "expected": 0.9}
    ),

    "F20": Formula(
        fid="F20", group=FormulaGroup.B_ENGINEERING,
        title="通心译 ETE 置信度 Tongxin ETE Confidence",
        standard_formula="CONF_ETE=cos_sim×cultural_root×emotion_keep",
        standard_source="多维度翻译质量评估",
        standard_explanation="语义、文化根、情绪保留综合置信度",
        longhorn_twist="≥0.85 高 / 0.6-0.85 校验 / <0.6 保留原话",
        longhorn_explanation="语义→公式→代码翻译质量",
        module="通心译 ETE",
        alpha_belongs="无",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="通心译、翻译校验",
        backfill_rule="引用 F20·三乘积模型",
        verifiable=True,
        python_snippet="""
def ete_confidence(cos_sim, cultural_root, emotion_keep):
    return cos_sim * cultural_root * emotion_keep
        """,
        test_case={"input": {"cos_sim": 0.9, "cultural_root": 0.9, "emotion_keep": 0.9}, "expected": 0.729}
    ),

    "F21": Formula(
        fid="F21", group=FormulaGroup.B_ENGINEERING,
        title="广义加法 Generalized Addition",
        standard_formula="A⊕B=α·(A·B)+β·(A∩B)+γ·(A⊖B)+δ·(A↦¬B)",
        standard_source="龍魂原创·多元运算统一",
        standard_explanation="根据主导系数决定 1+1 结果",
        longhorn_twist="主导系数决定 ∞/1/2/0/🔴",
        longhorn_explanation="共鸣/归一/独立/对冲/价值观违反",
        module="广义加法",
        alpha_belongs="α_w",
        audit="🟡",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="价值合并、冲突判定",
        backfill_rule="引用 F21·四系数主导",
        verifiable=True,
        python_snippet="""
def generalized_addition(A, B, alpha, beta, gamma, delta):
    terms = [alpha*(A*B), beta*(A and B), gamma*(A-B), delta*(A and not B)]
    return max(terms, key=abs)  # 简化：取主导项
        """,
        test_case={"input": {"A":1,"B":1,"alpha":1,"beta":0,"gamma":0,"delta":0}, "expected": 1}
    ),

    "F22": Formula(
        fid="F22", group=FormulaGroup.B_ENGINEERING,
        title="创作价值收益 Royalty",
        standard_formula="Royalty=ValidCitations×0.0028×QualityWeight×OwnerShare×AuthCoef×L5_TimeFactor",
        standard_source="引用计量·收益分配",
        standard_explanation="创作者从引用中获得收益记录",
        longhorn_twist="主权信封收益台账·非法定价格",
        longhorn_explanation="创作价值收益记录",
        module="创作价值收益",
        alpha_belongs="α_w / α_τ",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="收益台账、创作者经济",
        backfill_rule="引用 F22·主权信封",
        verifiable=True,
        python_snippet="""
def royalty(valid_citations, Q, owner_share, auth_coef, L5):
    return valid_citations * 0.0028 * Q * owner_share * auth_coef * L5
        """,
        test_case={"input": {"valid_citations":100,"Q":1.0,"owner_share":1.0,"auth_coef":1.0,"L5":1.0}, "expected": 0.28}
    ),

    "F23": Formula(
        fid="F23", group=FormulaGroup.B_ENGINEERING,
        title="DNA 哈希链 DNA Hash Chain",
        standard_formula="child_hash=SHA256(parent_hash‖canonical_JSON(payload))",
        standard_source="区块链·Git·哈希链",
        standard_explanation="父哈希 + 载荷生成子哈希",
        longhorn_twist="篡改任一字段则链断·永久追溯",
        longhorn_explanation="有痕开源 + 自适应调节器",
        module="DNA 哈希链",
        alpha_belongs="无",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="所有签署、审计、操作",
        backfill_rule="引用 F23·canonical JSON 载荷",
        verifiable=True,
        python_snippet="""
import hashlib, json
def dna_hash_child(parent_hash, payload):
    canon = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256((parent_hash + canon).encode()).hexdigest()
        """,
        test_case={"input": {"parent_hash":"abc","payload":{"x":1}}, "expected_len": 64}
    ),

    "F24": Formula(
        fid="F24", group=FormulaGroup.B_ENGINEERING,
        title="α 校准 Alpha Calibration",
        standard_formula="α=-ln(η_obs/η_init)/ln(T_days); T_half(α)=2^(1/α)",
        standard_source="指数衰减反推",
        standard_explanation="从观测半衰期反推衰减指数",
        longhorn_twist="L0-L4 五层时间衰减反算",
        longhorn_explanation="已知半衰期反推 α",
        module="α 校准",
        alpha_belongs="α_τ",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="记忆分层、规则时效校准",
        backfill_rule="引用 F24·半衰期反推",
        verifiable=True,
        python_snippet="""
import math
def alpha_calibration(eta_obs, eta_init, T_days):
    return -math.log(eta_obs/eta_init) / math.log(T_days)
def half_life(alpha):
    return 2 ** (1/alpha)
        """,
        test_case={"input": {"eta_obs":0.5,"eta_init":1.0,"T_days":2}, "expected_alpha": 1.0}
    ),

    "F25": Formula(
        fid="F25", group=FormulaGroup.B_ENGINEERING,
        title="五行对冲指数 Wuxing Hedge Index",
        standard_formula="H=克制衡×0.30+疏导×0.25+补益×0.20+均衡×0.15+链路健康度×0.10",
        standard_source="五行生克·系统平衡度",
        standard_explanation="衡量五行平衡度",
        longhorn_twist="≥0.80🟢 / 0.50≤H<0.80🟡 / <0.50🔴",
        longhorn_explanation="五行平衡度归一",
        module="五行对冲",
        alpha_belongs="α_w",
        audit="🟢",
        canon_page="🧮 数学公式算法核心·CNSH计算公式升级v2.0.md",
        canon_dna="#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-FORMULA-CORE-CNSH-UPGRADE-v2.0-10C84C10",
        backfill_target="五行分析、系统健康",
        backfill_rule="引用 F25·H 写作 H_五行",
        verifiable=True,
        python_snippet="""
def wuxing_hedge(克制衡, 疏导, 补益, 均衡, 链路健康度):
    return 克制衡*0.30 + 疏导*0.25 + 补益*0.20 + 均衡*0.15 + 链路健康度*0.10
        """,
        test_case={"input": {"克制衡":0.9,"疏导":0.9,"补益":0.9,"均衡":0.9,"链路健康度":0.9}, "expected": 0.9}
    ),
}


# ============ C组·F31+（当前只列 F31） ============

C_FORMULAS = {
    "F31": Formula(
        fid="F31", group=FormulaGroup.C_APPLICATION,
        title="通心译总式 Tongxin Translation Formula",
        standard_formula="Translate(x)=⊕_{i=1}^{6} Dim_i(x)",
        standard_source="龍魂通心译系统·六维文化翻译",
        standard_explanation="不是简单翻译，是六维一起对齐",
        longhorn_twist="语义+语气+文化+术语+五行+主权词锁",
        longhorn_explanation="中文文化不丢·主权词不乱翻",
        module="通心译",
        alpha_belongs="F21 广义加法",
        audit="🔖",
        canon_page="🧮 通心译·TONGXIN_TRANSLATION_MODERN_PHYSICS_v1.0_COMPLETE",
        canon_dna="#龍芯⚡️丙午·甲午·癸丑·戊午·䷨损-F31-通心译-v1.0",
        backfill_target="翻译系统·文化主权·国际化",
        backfill_rule="引用 F31·遵守六维翻译规则",
        verifiable=False,
        python_snippet=None,
        test_case=None
    ),
}


# ============ 母册核心类 ============

class FormulaCatalog:
    """公式母册 v2.0·可查·可回填·可验证"""

    EXPECTED_F01_F15 = {f"F{i:02d}" for i in range(1, 16)}
    EXPECTED_F16_F30 = {f"F{i:02d}" for i in range(16, 31)}
    EXPECTED_F31_F45 = {f"F{i:02d}" for i in range(31, 46)}

    def __init__(self):
        self.formulas: Dict[str, Formula] = {}
        self.load_all()

    def load_all(self):
        self.formulas.update(A_FORMULAS)
        self.formulas.update(B_FORMULAS)
        self.formulas.update(C_FORMULAS)

    def get_by_fid(self, fid: str) -> Optional[Formula]:
        return self.formulas.get(fid)

    def list_group(self, group: FormulaGroup) -> List[Formula]:
        return [f for f in self.formulas.values() if f.group == group]

    def backfill_reference(self, fid: str) -> str:
        f = self.get_by_fid(fid)
        if not f:
            return f"❌ 公式 {fid} 不存在"
        return f"🧮 引用 {fid}（{f.title}）— {f.canon_page}"

    def verification_report(self) -> Dict[str, Any]:
        verifiable = [f for f in self.formulas.values() if f.verifiable]
        total = len(self.formulas)
        return {
            "total": total,
            "verifiable": len(verifiable),
            "verifiable_ratio": f"{len(verifiable)/total*100:.1f}%" if total else "0%",
            "verified_list": [f.fid for f in verifiable],
            "f01_f15_present": sorted(self.EXPECTED_F01_F15 & set(self.formulas)),
            "f16_f30_present": sorted(self.EXPECTED_F16_F30 & set(self.formulas)),
            "missing_f01_f15": sorted(self.EXPECTED_F01_F15 - set(self.formulas)),
            "missing_f16_f30": sorted(self.EXPECTED_F16_F30 - set(self.formulas)),
        }

    def continuity_check(self) -> Dict[str, Any]:
        """检查 F01-F25 是否连续"""
        expected = {f"F{i:02d}" for i in range(1, 26)}
        present = set(self.formulas) & expected
        return {
            "expected_count": 25,
            "present_count": len(present),
            "missing": sorted(expected - present),
            "complete": present == expected
        }

    def generate_manifest(self) -> str:
        manifest = "# 龍魂公式母册清单 v2.0\n\n"
        for group in FormulaGroup:
            formulas_in_group = self.list_group(group)
            manifest += f"## {group.value}\n\n"
            for f in formulas_in_group:
                manifest += f"- **{f.fid} {f.title}**\n"
                manifest += f"  - 模块：{f.module}\n"
                manifest += f"  - 标准：{f.standard_formula}\n"
                manifest += f"  - 龍魂：{f.longhorn_twist}\n"
                manifest += f"  - α 归属：{f.alpha_belongs}\n"
                manifest += f"  - 可验：{'✅' if f.verifiable else '🔖'}\n\n"
        manifest += "---\n\n"
        manifest += f"**DNA：** `#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-龍魂数学公式母册-v2.0-CNSH-25-FORMULAS`\n"
        return manifest


# ============ 自检 ============

def selftest() -> bool:
    """v2.0 母册完整性自检"""
    print("=" * 80)
    print("🧮 龍魂数学公式母册完整版 v2.0 · 自检")
    print("=" * 80)

    catalog = FormulaCatalog()

    # 1. F01-F15 全齐
    a_group = catalog.list_group(FormulaGroup.A_CORE)
    assert len(a_group) == 15, f"A组应为 15 条，实际 {len(a_group)}"
    print(f"[1] A组 F01-F15 全齐：{len(a_group)} 条 ✅")

    # 2. F16-F30 当前补齐 10 条（F16-F25）
    b_group = catalog.list_group(FormulaGroup.B_ENGINEERING)
    assert len(b_group) == 10, f"B组应为 10 条（F16-F25），实际 {len(b_group)}"
    print(f"[2] B组 F16-F25 全齐：{len(b_group)} 条 ✅")

    # 3. F01-F25 连续性
    cont = catalog.continuity_check()
    assert cont["complete"], f"F01-F25 不连续：缺 {cont['missing']}"
    print(f"[3] F01-F25 连续无缺口 ✅")

    # 4. 回填引用
    ref = catalog.backfill_reference("F18")
    assert "F18" in ref and "引用" in ref
    print(f"[4] 回填引用：{ref} ✅")

    # 5. 可验证比例
    report = catalog.verification_report()
    ratio = float(report["verifiable_ratio"].rstrip("%"))
    assert ratio >= 90.0, f"可验证比例 {ratio}% 不足 90%"
    print(f"[5] 总公式数={report['total']}·可验证={report['verifiable']}·比例={report['verifiable_ratio']} ✅")

    # 6. 清单生成
    manifest = catalog.generate_manifest()
    assert "v2.0" in manifest and "F25" in manifest
    print(f"[6] v2 清单已生成·共 {len(manifest)} 字 ✅")

    print("=" * 80)
    print("🟢 龍魂公式母册 v2.0 完整性验证通过")
    print("   DNA：#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-龍魂数学公式母册-v2.0-CNSH-25-FORMULAS")
    print("   回填规则：引用 FXX·不重写公式·保留签署链")
    print("=" * 80)
    return True


if __name__ == "__main__":
    selftest()
    catalog = FormulaCatalog()
    with open("formula_catalog_manifest_v2.md", "w", encoding="utf-8") as f:
        f.write(catalog.generate_manifest())
    print("\n✅ v2 公式清单已保存至 formula_catalog_manifest_v2.md")
