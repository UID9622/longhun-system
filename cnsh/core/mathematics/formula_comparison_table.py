#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  龍魂算法公式对照表生成器  |  Formula Comparison Table Generator  ║
║  DNA: #龍芯⚡️2026-06-21-FORMULA-COMPARISON-TABLE-v1.0          ║
║  用途: 生成“世界标准 vs 龍魂主权”双轨公式对照表，供论文/CSDN使用 ║
╚══════════════════════════════════════════════════════════════╝

设计原则:
  - 左栏: 世界标准公式 (数学表达 + 标准用途)
  - 右栏: 龍魂主权层扩展 (治理含义 + 三色审计 + DNA追溯)
  - 支持按论文关键词过滤相关公式
  - 输出 Markdown / LaTeX 两种格式
"""

from datetime import datetime
from typing import List, Dict, Optional


# ═══════════════════════════════════════════════════════════════
# 【公式数据库】世界标准 vs 龍魂主权
# ═══════════════════════════════════════════════════════════════

FORMULA_DB: List[Dict] = [
    {
        "id": "F01",
        "name": "数字根 Digital Root",
        "keywords": ["数字根", "dr", "洛书", "369", "数论"],
        "world_standard": {
            "formula": r"dr(n) = 1 + ((n-1) \bmod 9), \quad n > 0",
            "usage": "ISBN、Luhn 校验码、数论标准",
        },
        "longhun_layer": {
            "formula": r"dr \in \{3,9\} \to \textcolor{red}{\text{🔴 拒绝}};\ dr=6 \to \textcolor{yellow}{\text{🟡 警告}};\ \text{其余} \to \textcolor{green}{\text{🟢 通过}}",
            "usage": "把纯数论 dr 焊成三色治理判定，防止 3/9 极端值入侵决策",
        },
    },
    {
        "id": "F02",
        "name": "信息熵 Shannon Entropy",
        "keywords": ["熵", "entropy", "信息论", "压缩", "不确定性"],
        "world_standard": {
            "formula": r"H(X) = -\sum_{i} p_i \log_2 p_i",
            "usage": "衡量不确定性，压缩理论下界（Shannon 1948）",
        },
        "longhun_layer": {
            "formula": r"\rho = 1 - \frac{|compressed|}{|original|}, \quad \rho \geq 1 - 2^{-H} - \epsilon",
            "usage": "压缩护城河：超过香农下界的压缩视为非法/丢失主权信息",
        },
    },
    {
        "id": "F03",
        "name": "余弦相似度 Cosine Similarity",
        "keywords": ["余弦", "cosine", "相似度", "去重", "NLP", "水军"],
        "world_standard": {
            "formula": r"\cos(A,B) = \frac{A \cdot B}{\|A\| \cdot \|B\|}",
            "usage": "信息检索/NLP 标配，用于去重、聚类、推荐",
        },
        "longhun_layer": {
            "formula": r"\cos \geq 0.9 \to \textcolor{red}{\text{🔴 拒绝}};\ 0.7 \leq \cos < 0.9 \to \textcolor{yellow}{\text{🟡 警告}};\ \cos < 0.7 \to \textcolor{green}{\text{🟢 通过}}",
            "usage": "水军检测 + 去重路由，防止刷量与信息污染",
        },
    },
    {
        "id": "F04",
        "name": "权重归一化 Weight Normalization",
        "keywords": ["归一化", "normalize", "softmax", "权重", "概率"],
        "world_standard": {
            "formula": r"w_i = \frac{x_i}{\sum_j x_j}; \quad \text{softmax}(x_i) = \frac{e^{x_i}}{\sum_j e^{x_j}}",
            "usage": "线性归一与概率归一，ML 标配",
        },
        "longhun_layer": {
            "formula": r"\alpha_a: \sum |\alpha_i|^2 = 1; \quad \alpha_w: w_i \geq 0,\ \sum w_i = 1",
            "usage": "α 振幅量子归一 + α_w 凸组合约束，防止 α 混用与裸用",
        },
    },
    {
        "id": "F05",
        "name": "真实度评分 Truth Score",
        "keywords": ["真实度", "truth", "评分", "可信度", "一票否决"],
        "world_standard": {
            "formula": r"T = 0.4M + 0.3V + 0.3F",
            "usage": "加权置信度：M 有意义、V 可验证、F 格式安全",
        },
        "longhun_layer": {
            "formula": r"\exists i, F_i = 0 \Longrightarrow T_{total} = 0 \quad \text{(一票否决)}",
            "usage": "签章污染是绝对红线，任一 F=0 总分归零",
        },
    },
    {
        "id": "F06",
        "name": "七维 SOUL 评分",
        "keywords": ["SOUL", "评分", "多准则", "MCDA", "七维", "七因子", "身份", "EU HLEG", "Trustworthy AI"],
        "world_standard": {
            "formula": r"SOUL = \sum_{k} w_k \cdot E_k, \quad \sum_k w_k = 1",
            "usage": "多准则决策 MCDA：技术/语言/文化/数据/决策/知识/身份",
        },
        "longhun_layer": {
            "formula": r"w_{身份} = 0.05, \quad \alpha = 0 \text{ (永不衰减)}",
            "usage": "身份维作为不可让渡的主权底，权重永不衰减",
        },
    },
    {
        "id": "F07",
        "name": "哈希链 Hash Chain",
        "keywords": ["哈希", "hash", "DNA", "审计", "区块链"],
        "world_standard": {
            "formula": r"h_t = SHA256(h_{t-1} \| event_t)",
            "usage": "区块链/Git/Merkle 树标准，改一字全链变",
        },
        "longhun_layer": {
            "formula": r"DNA_t = SHA256(DNA_{t-1} \| event_t \| signer_t)",
            "usage": "审计哈希链，谁说话谁签名，追溯责任不可抵赖",
        },
    },
    {
        "id": "F08",
        "name": "洛书幻方守恒 Luoshu Magic Square",
        "keywords": ["洛书", "幻方", "守恒", "369", "中宫", "不动点"],
        "world_standard": {
            "formula": r"\sum row_i = \sum col_j = \sum diag = 15",
            "usage": "3 阶幻方组合数学经典，中宫 5 为不动点",
        },
        "longhun_layer": {
            "formula": r"\text{magic\_ok} \land center = 5 \to \textcolor{green}{\text{🟢 通过}}",
            "usage": "洛书双检：幻方守恒 + 中宫主权锚，判定系统是否平衡",
        },
    },
    {
        "id": "F09",
        "name": "黎曼函数方程 Riemann Functional Equation",
        "keywords": ["黎曼", "Riemann", "zeta", "函数方程", "临界线"],
        "world_standard": {
            "formula": r"\zeta(s) = 2^s \pi^{s-1} \sin\left(\frac{\pi s}{2}\right) \Gamma(1-s) \zeta(1-s)",
            "usage": "Riemann 1859，反射对称 s \\leftrightarrow 1-s",
        },
        "longhun_layer": {
            "formula": r"\Gamma = \left\{\frac{1}{2} + it \mid t \in \mathbb{R}\right\} \text{ 是 } s \leftrightarrow 1-s \text{ 的唯一不动集}",
            "usage": "临界线作为反射不动集，成为龍魂三视角（不动点/守恒/和谐）的交汇",
        },
    },
    {
        "id": "F10",
        "name": "三才权重 Three-Talent Weights",
        "keywords": ["三才", "权重", "天", "地", "人", "和谐"],
        "world_standard": {
            "formula": r"S = w_T \cdot T + w_E \cdot E + w_H \cdot H, \quad w_T + w_E + w_H = 1",
            "usage": "多维度加权求和，优化与决策通用",
        },
        "longhun_layer": {
            "formula": r"w_T = 0.35,\ w_E = 0.15,\ w_H = 0.50 \quad (\text{人} \geq 0.34)",
            "usage": "三才权重焊死：人场 ≥ 34%，防止系统脱离人的主导",
        },
    },
    {
        "id": "F11",
        "name": "EU 七因子可信 AI 合规评分",
        "keywords": ["七因子", "EU HLEG", "Trustworthy AI", "CNSH-64", "合规", "可信 AI"],
        "world_standard": {
            "formula": r"\text{TAIScore} = \sum_{j=1}^{7} \lambda_j \cdot r_j, \quad \lambda_j \geq 0,\ \sum_j \lambda_j = 1",
            "usage": "EU HLEG (2019) 七项可信 AI 要求：人本监督 / 鲁棒安全 / 隐私与数据治理 / 透明 / 公平非歧视 / 社会与环境福祉 / 问责",
        },
        "longhun_layer": {
            "formula": r"\text{CNSH-7F}(c) = \bigwedge_{j=1}^{7} \mathbb{I}\big[r_j(c) \geq \theta_j\big] \cdot \sum_j w_j r_j(c)",
            "usage": "把 EU 七因子映射到 CNSH-64 七属性；任一维度低于阈值即触发 🟡/🔴 三色审计，权重焊死确保问责与人本监督不可衰减",
        },
    },
]


# ═══════════════════════════════════════════════════════════════
# 【公式检索与生成】
# ═══════════════════════════════════════════════════════════════

def filter_formulas_by_keywords(keywords: List[str]) -> List[Dict]:
    """
    根据论文关键词过滤相关公式
    """
    if not keywords:
        return FORMULA_DB

    matched = []
    for formula in FORMULA_DB:
        score = 0
        for kw in keywords:
            kw_lower = kw.lower()
            # 匹配公式关键词
            for fk in formula["keywords"]:
                if kw_lower in fk.lower() or fk.lower() in kw_lower:
                    score += 1
            # 匹配公式名称
            if kw_lower in formula["name"].lower():
                score += 1

        if score > 0:
            formula_copy = formula.copy()
            formula_copy["relevance_score"] = score
            matched.append(formula_copy)

    # 按相关度排序
    matched.sort(key=lambda x: x["relevance_score"], reverse=True)
    return matched


def generate_markdown_table(formulas: List[Dict], title: str = "算法公式对照表") -> str:
    """
    生成 Markdown 格式对照表
    """
    lines = [
        f"## {title}",
        "",
        "| 编号 | 名称 | 世界标准 | 龍魂主权层 |",
        "|:----:|:-----|:---------|:-----------|",
    ]

    for f in formulas:
        name = f"**{f['id']}** · {f['name']}"
        std = f"{f['world_standard']['formula']}<br><small>{f['world_standard']['usage']}</small>"
        long = f"{f['longhun_layer']['formula']}<br><small>{f['longhun_layer']['usage']}</small>"
        lines.append(f"| {f['id']} | {name} | {std} | {long} |")

    lines.append("")
    lines.append(f"*表生成时间: {datetime.now().isoformat()} · DNA: #龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-FORMULA-TABLE-v1.0*")
    lines.append("")

    return "\n".join(lines)


def generate_compact_table(formulas: List[Dict]) -> str:
    """
    生成紧凑版 Markdown 表格（适合 CSDN 窄栏）
    """
    lines = [
        "| 公式 | 世界标准 | 龍魂扩展 |",
        "|:-----|:---------|:---------|",
    ]

    for f in formulas:
        lines.append(
            f"| **{f['id']}** {f['name']} | "
            f"{f['world_standard']['formula']} | "
            f"{f['longhun_layer']['formula']} |"
        )

    return "\n".join(lines)


def generate_formula_list(formulas: List[Dict]) -> str:
    """
    生成列表式公式说明（适合放在论文附录）
    """
    lines = ["### 公式说明", ""]

    for f in formulas:
        lines.append(f"**{f['id']} {f['name']}**")
        lines.append("")
        lines.append(f"- 世界标准: {f['world_standard']['formula']}")
        lines.append(f"  - 用途: {f['world_standard']['usage']}")
        lines.append(f"- 龍魂主权层: {f['longhun_layer']['formula']}")
        lines.append(f"  - 治理含义: {f['longhun_layer']['usage']}")
        lines.append("")

    return "\n".join(lines)


def get_formula_ids_for_paper(keywords: List[str], max_results: int = 6) -> List[str]:
    """
    为论文推荐相关公式ID列表
    """
    matched = filter_formulas_by_keywords(keywords)
    return [f["id"] for f in matched[:max_results]]


# ═══════════════════════════════════════════════════════════════
# 【演示代码】
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  龍魂算法公式对照表生成器 — 演示                             ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # 示例1: 全部公式
    print("\n【全部公式对照表】")
    print(generate_markdown_table(FORMULA_DB))

    # 示例2: 按关键词过滤
    print("\n【黎曼/数论相关公式】")
    matched = filter_formulas_by_keywords(["黎曼", "Riemann", "数字根", "洛书"])
    print(generate_compact_table(matched))

    # 示例3: 推荐公式ID
    print("\n【为 CNSH 治理论文推荐公式】")
    ids = get_formula_ids_for_paper(["CNSH", "AI治理", "真实度", "审计", "哈希"])
    print("推荐公式:", ", ".join(ids))
