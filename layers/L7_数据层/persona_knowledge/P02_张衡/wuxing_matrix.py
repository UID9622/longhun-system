#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""🐉 五行矩阵评分引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·甲寅·申时·师-P02-WUXING-MATRIX-v1.0

核心功能：
  1. 五行常量定义（金木水火土 + 生克关系）
  2. WBI（五行平衡指数）+ GRS（生克动态）+ SBC（三才平衡系数）
  3. 五行向量计算 W(x) = [金,木,水,火,土]
  4. 五行矩阵乘变换 + 量子叠加态投影
  5. 多维权重→五行诊断→优化建议

数学锚：
  - 公式06: WBI = 100 - (σ/avg × 100)
  - 公式07: GRS = 生强度 - 克强度
  - 公式08: SBC = 天×0.35 + 地×0.20 + 人×0.45
"""
from __future__ import annotations
import hashlib, json, math
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
def _sha8(s: str) -> str: return hashlib.sha256(s.encode()).hexdigest()[:8]

# ═══════════════════════════════════════════════
# 五行常量（L0焊死）
# ═══════════════════════════════════════════════
五行 = ["金", "木", "水", "火", "土"]
五行索引 = {"金": 0, "木": 1, "水": 2, "火": 3, "土": 4}

# 相生矩阵: M[i][j] = 1 if i生j
# 金生水·水生木·木生火·火生土·土生金
五行相生 = {
    ("金", "水"): 1.0, ("水", "木"): 1.0, ("木", "火"): 1.0,
    ("火", "土"): 1.0, ("土", "金"): 1.0,
}

# 相克矩阵: M[i][j] = -1 if i克j
# 金克木·木克土·土克水·水克火·火克金
五行相克 = {
    ("金", "木"): -1.0, ("木", "土"): -1.0, ("土", "水"): -1.0,
    ("水", "火"): -1.0, ("火", "金"): -1.0,
}

# 反克（侮·乘）
五行反克 = {
    ("木", "金"): -0.5, ("土", "木"): -0.5, ("水", "土"): -0.5,
    ("火", "水"): -0.5, ("金", "火"): -0.5,
}

# 数字根→五行
dr_五行 = {
    1: "水", 2: "土", 3: "木", 4: "木",
    5: "土", 6: "金", 7: "金", 8: "土", 9: "火"
}

@dataclass
class MatrixConfig:
    """五行矩阵配置"""
    enable_anti_ke: bool = True          # 是否检查反克
    enable_stealth_ke: bool = True       # 是否检查暗克（势弱时）
    balance_weight: float = 0.3          # 平衡权重（历史vs当前）
    entropy_floor: float = 0.05          # 熵底限
    three_talents: Dict[str, float] = field(default_factory=lambda: {"天": 0.35, "地": 0.20, "人": 0.45})

@dataclass
class MatrixScore:
    """五行矩阵评分结果"""
    wuxing_vector: Dict[str, float]      # [金,木,水,火,土]
    WBI: float                            # 五行平衡指数 (0-100)
    GRS: float                            # 生克动态 (-1 to 1)
    SBC: float                            # 三才平衡系数
    dominant_element: str                 # 主五行
    deficiency_element: str               # 缺五行
    anomaly_alert: bool                   # 异常预警
    optimization_suggestions: List[str] = field(default_factory=list)
    historical_trend: List[Dict[str, float]] = field(default_factory=list)
    dna: str = ""

def _pad_wuxing_vec(vec: List[float]) -> List[float]:
    """确保五行向量长度为5"""
    return (vec + [0.0] * 5)[:5]

class WuxingMatrix:
    """五行矩阵引擎 · 多维诊断 + 生克动态"""

    config: MatrixConfig

    def __init__(self, config: Optional[MatrixConfig] = None):
        self.config = config or MatrixConfig()

    # — 基础向量计算 —
    def compute_vector(self, scores: Dict[str, float]) -> Dict[str, float]:
        """
        多维分数 → 五行向量 W = [金,木,水,火,土]
        算法：每个维度名/值的数字根→五行映射→累加
        """
        vec = [0.0] * 5
        for name, score in scores.items():
            # 数字根→五行
            n = int(hash(name) % 100)
            dr = 1 + (n - 1) % 9 if n > 0 else 9
            wx = dr_五行.get(dr, "土")
            idx = 五行索引.get(wx, 4)
            vec[idx] += score
        # 归一化
        total = sum(vec)
        if total > 0:
            vec = [v / total for v in vec]
        return {五行[i]: round(v, 4) for i, v in enumerate(vec)}

    # — 从权重直接算W向量（数字根映射）—
    def vector_from_weights(self, weights: Dict[str, float]) -> Dict[str, float]:
        """权重值 → 数字根 → 五行向量"""
        vec = [0.0] * 5
        for name, w in weights.items():
            n = int(w * 1000)  # 放大取整
            dr = 1 + (n - 1) % 9 if n > 0 else 9
            wx = dr_五行.get(dr, "土")
            vec[五行索引[wx]] += abs(w)
        total = sum(vec)
        if total > 0:
            vec = [v / total for v in vec]
        return {五行[i]: round(v, 4) for i, v in enumerate(vec)}

    # — WBI 五行平衡指数 —
    def wbi(self, wuxing_vec: Dict[str, float]) -> float:
        """WBI = 100 - (σ/avg × 100)"""
        values = [wuxing_vec.get(w, 0.0) for w in 五行]
        avg = sum(values) / 5
        if avg == 0: return 0.0
        variance = sum((v - avg) ** 2 for v in values) / 5
        sigma = math.sqrt(variance)
        wbi = 100 - (sigma / avg * 100)
        return round(max(0, min(100, wbi)), 2)

    # — GRS 生克动态 —
    def grs(self, wuxing_vec: Dict[str, float]) -> float:
        """GRS = Σ(相生力度) - Σ(相克力度)"""
        sheng = 0.0
        ke = 0.0
        for i, wi in enumerate(五行):
            vi = wuxing_vec.get(wi, 0.0)
            for j, wj in enumerate(五行):
                if i == j: continue
                vj = wuxing_vec.get(wj, 0.0)
                if (wi, wj) in 五行相生:
                    sheng += vi * vj * 五行相生[(wi, wj)]
                if (wi, wj) in 五行相克:
                    ke += vi * vj * abs(五行相克[(wi, wj)])
                if self.config.enable_anti_ke and (wi, wj) in 五行反克:
                    ke += vi * vj * abs(五行反克[(wi, wj)]) * 0.5
        total = sheng + ke
        grs_val = (sheng - ke) / (total + 1e-9)
        return round(grs_val, 4)

    # — SBC 三才平衡系数 —
    def sbc(self, talent_scores: Dict[str, float]) -> float:
        """SBC = 天×0.35 + 地×0.20 + 人×0.45"""
        t = self.config.three_talents
        return round(
            talent_scores.get("天", 0) * t["天"] +
            talent_scores.get("地", 0) * t["地"] +
            talent_scores.get("人", 0) * t["人"],
            4
        )

    # — 完整评分 —
    def score(self, scores: Dict[str, float],
              talent_scores: Optional[Dict[str, float]] = None) -> MatrixScore:
        """
        完整五行矩阵评分
        scores: 各维度分数字典
        talent_scores: 三才分（可选）
        """
        wx_vec = self.compute_vector(scores)

        # WBI
        wbi_val = self.wbi(wx_vec)

        # GRS
        grs_val = self.grs(wx_vec)

        # SBC
        sbc_val = self.sbc(talent_scores or {})

        # 主五行 & 缺五行
        max_wx_item = max(wx_vec.items(), key=lambda x: x[1])
        min_wx_item = min(wx_vec.items(), key=lambda x: x[1])
        dominant = max_wx_item[0]
        deficiency = min_wx_item[0] if min_wx_item[1] < 0.05 else "无"

        # 异常检测
        anomaly = wbi_val < 30 or grs_val < -0.5

        # 优化建议
        suggestions = []
        if wbi_val < 50:
            suggestions.append(f"五行失衡(偏{dominant})，WBI={wbi_val}→建议补{deficiency}行")
        if grs_val < -0.3:
            suggestions.append(f"生克动态偏克(GRS={grs_val})→检查克制链")
        if wbi_val < 30:
            suggestions.append(f"🔴 WBI<30 严重失衡→立即调整权重")
        if anomaly:
            suggestions.append(f"⚠️ 异常标记激活")

        dna = _sha8(f"WX-MATRIX-{_sha8(json.dumps(wx_vec))}")

        return MatrixScore(
            wuxing_vector=wx_vec,
            WBI=wbi_val,
            GRS=grs_val,
            SBC=sbc_val,
            dominant_element=dominant,
            deficiency_element=deficiency,
            anomaly_alert=anomaly,
            optimization_suggestions=suggestions,
            dna=f"#龍芯⚡️丙午·乙未·甲寅·申时·师-P02-WX-SCORE-{dna}"
        )

    # — 五行矩阵变换（量子叠加投影）—
    def matrix_transform(self, wuxing_vec: Dict[str, float],
                          transform_type: str = "quantum") -> Dict[str, float]:
        """
        五行向量 → 矩阵变换 → 投影
        quantum: 量子叠加态（每个五行=一个量子态）
        luoshu: 洛书映射变换
        """
        vec = [wuxing_vec.get(w, 0.0) for w in 五行]

        if transform_type == "quantum":
            # 量子叠加：每个元素概率振幅 → 归一化
            sq = [v ** 2 for v in vec]
            s = sum(sq) + 1e-9
            transformed = [math.sqrt(vq / s) for vq in sq]
        elif transform_type == "luoshu":
            # 洛书映射：3×3 → 展开 → 取前5
            luoshu = [4, 9, 2, 3, 5, 7, 8, 1, 6]
            ls_norm = [lv / 45 for lv in luoshu[:5]]
            transformed = [ls_norm[i] * vec[i] for i in range(5)]
        else:
            transformed = vec

        total = sum(transformed) + 1e-9
        return {五行[i]: round(transformed[i] / total, 4) for i in range(5)}

    # — 跨模块五行协调 —
    def harmonize_across_modules(self, module_vectors: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """多模块五行向量调和"""
        module_scores = {}
        all_warnings = []
        for mod, vec in module_vectors.items():
            s = self.score(vec)
            module_scores[mod] = asdict(s)
            if s.anomaly_alert:
                all_warnings.append(f"{mod}: {s.optimization_suggestions[0] if s.optimization_suggestions else '异常'}")

        # 跨模块总体WBI
        avg_vec = {w: 0.0 for w in 五行}
        for vec in module_vectors.values():
            for w in 五行:
                avg_vec[w] += vec.get(w, 0)
        n = max(len(module_vectors), 1)
        avg_vec = {w: round(v / n, 4) for w, v in avg_vec.items()}
        overall_wbi = self.wbi(avg_vec)

        return {
            "module_scores": module_scores,
            "average_vector": avg_vec,
            "overall_wbi": overall_wbi,
            "cross_module_warnings": all_warnings,
            "is_stable": overall_wbi >= 60 and len(all_warnings) == 0
        }

    # — IPA回调 —
    def ipa_callback(self, scores: Dict[str, float],
                     talent_scores: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        """
        IPA-L7-PER-KNOW-007 回调（五行矩阵子模块）
        """
        result = self.score(scores, talent_scores)
        return {
            "wuxing_matrix": asdict(result),
            "WBI": result.WBI,
            "GRS": result.GRS,
            "SBC": result.SBC,
            "anomaly": result.anomaly_alert,
            "dna": result.dna
        }


# ═══════════════════════════════════════════════
# 五行常量对外接口
# ═══════════════════════════════════════════════
五行常量 = {
    "金": {"数字根": [6, 7], "方向": "西北·西", "季节": "秋", "脏腑": "肺", "味": "辛", "色": "白"},
    "木": {"数字根": [3, 4], "方向": "东·东南", "季节": "春", "脏腑": "肝", "味": "酸", "色": "青"},
    "水": {"数字根": [1], "方向": "北", "季节": "冬", "脏腑": "肾", "味": "咸", "色": "黑"},
    "火": {"数字根": [9], "方向": "南", "季节": "夏", "脏腑": "心", "味": "苦", "色": "赤"},
    "土": {"数字根": [2, 5, 8], "方向": "中·西南·东北", "季节": "长夏", "脏腑": "脾", "味": "甘", "色": "黄"},
}

# — 自验证 —
if __name__ == "__main__":
    wx = WuxingMatrix()
    # 测试从分数→五行向量
    test_scores = {"证据链": 8.5, "法律适用": 7.2, "执行可行": 6.8, "时机成熟": 5.5, "舆论": 4.0, "反扑": 7.0, "保护": 9.0}
    result = wx.score(test_scores)
    print(f"五行向量: {result.wuxing_vector}")
    print(f"WBI={result.WBI}, GRS={result.GRS}, SBC={result.SBC}")
    print(f"主五行={result.dominant_element}, 缺={result.deficiency_element}")
    print(f"异常={result.anomaly_alert}")
    for s in result.optimization_suggestions: print(f"  → {s}")
    # 量子变换
    qt = wx.matrix_transform(result.wuxing_vector, "quantum")
    print(f"量子变换: {qt}")

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·申时·小畜-CONFIRM-SEAL-wuxing_matrix-B9D248A8
