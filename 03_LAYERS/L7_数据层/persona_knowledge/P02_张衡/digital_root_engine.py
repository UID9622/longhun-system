#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""🐉 数字根引擎 v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
DNA: #龍芯⚡️丙午·乙未·甲寅·申时·䷆师-P02-DIGITAL-ROOT-v1.0

核心功能：
  1. 数字根计算（mod 9 算法）
  2. 数字根链生成（多值联动递推）
  3. 洛书369不动点校验
  4. 数字根→五行→八卦路由映射
  5. 跨模块权重一致性校验

数学锚：
  - 数字根 dr(n) = 1 + (n-1) % 9 (n>0), dr(0)=0
  - 369 = 三才算法不动点（L0宪法层·焊死）
  - 3·6·9 三数为洛书对角线核心，永不改
"""
from __future__ import annotations
import hashlib, json, math
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

ROOT = Path(__file__).resolve().parents[4]
def _sha8(s: str) -> str: return hashlib.sha256(s.encode()).hexdigest()[:8]

# —— 369不动点（L0宪法层·焊死）——
不动点_369 = (3, 6, 9)

# —— 数字根→五行映射（洛书矩阵推导）——
dr_五行 = {
    1: "水", 2: "土", 3: "木", 4: "木",
    5: "土", 6: "金", 7: "金", 8: "土", 9: "火"
}

# —— 数字根→八卦镜像——
dr_八卦 = {
    1: "坎☵", 2: "坤☷", 3: "震☳", 4: "巽☴",
    5: "中五☯", 6: "乾☰", 7: "兑☱", 8: "艮☶", 9: "离☲"
}

# —— 数字根范围色标 ——
def dr_range(dr: int) -> str:
    """数字根→范围归属"""
    if dr in (3, 6, 9): return "🟡 不动点"
    if dr in (1, 8): return "🟢 本源"
    if dr in (2, 7): return "🟢 稳定"
    if dr in (4, 5): return "🟡 中轴"
    return "🔴 异常"

class DRLevel(Enum):
    SINGLE = "单值"
    CHAIN = "链式"
    MATRIX = "矩阵"

@dataclass
class DRConfig:
    """数字根引擎配置"""
    mod_base: int = 9                    # 模基数（9=洛书模）
    chain_min_length: int = 3            # 链最小长度
    chain_max_length: int = 12           # 链最大长度
    immutables: Tuple[int, ...] = (3, 6, 9)  # 不动点·焊死
    verify_369: bool = True              # 是否校验收敛到369

@dataclass
class DRChain:
    """数字根链"""
    source_values: List[Union[int, float, str]]
    dr_values: List[int]
    chain_length: int
    hits_369: int                        # 命中369次数
    convergence_to_369: bool             # 是否收敛到369
    primary_wuxing: str = ""
    primary_bagua: str = ""
    anomaly_flag: bool = False           # 异常标记
    dna: str = ""

class DigitalRootEngine:
    """数字根计算引擎 · 洛书369不动点验证"""

    config: DRConfig

    def __init__(self, config: Optional[DRConfig] = None):
        self.config = config or DRConfig()

    # — 基础计算 —
    def dr(self, n: int) -> int:
        """单值数字根: dr(n) = 1 + (n-1) mod 9"""
        if n == 0: return 0
        r = 1 + (n - 1) % 9
        return r

    def dr_from_float(self, f: float, precision: int = 6) -> int:
        """浮点数→取整→数字根"""
        n = int(round(f * (10 ** precision)))
        return self.dr(n)

    def dr_from_str(self, s: str) -> int:
        """字符串→ASCII和→数字根"""
        total = sum(ord(c) for c in s)
        return self.dr(total)

    def dr_from_hex(self, hex_str: str) -> int:
        """十六进制→十进制→数字根"""
        return self.dr(int(hex_str, 16))

    # — 链式计算 —
    def chain(self, values: List[Union[int, float, str]],
              level: DRLevel = DRLevel.CHAIN) -> DRChain:
        """多值数字根链 → 递推+369判定"""
        dr_vals: List[int] = []
        for v in values:
            if isinstance(v, int):
                dr_vals.append(self.dr(v))
            elif isinstance(v, float):
                dr_vals.append(self.dr_from_float(v))
            elif isinstance(v, str):
                dr_vals.append(self.dr_from_str(v))
            else:
                dr_vals.append(0)

        hits = sum(1 for d in dr_vals if d in 不动点_369)
        chain_len = len(dr_vals)

        # 收敛判定：至少一个369 or 最后三个包含369
        last_3 = dr_vals[-3:] if chain_len >= 3 else dr_vals
        converged = bool(set(last_3) & set(不动点_369))

        # 主五行 = 链尾数字根映射
        wuxing = dr_五行.get(dr_vals[-1], "土") if dr_vals else "土"
        bagua = dr_八卦.get(dr_vals[-1], "中五☯") if dr_vals else "中五☯"

        # 异常检测：链长 < 3 或 无369命中
        anomaly = chain_len < 3 or (hits == 0 and self.config.verify_369)

        dna = _sha8(f"DR-CHAIN-{'-'.join(str(d) for d in dr_vals)}-{_sha8(str(values))}")

        return DRChain(
            source_values=values,
            dr_values=dr_vals,
            chain_length=chain_len,
            hits_369=hits,
            convergence_to_369=converged,
            primary_wuxing=wuxing,
            primary_bagua=bagua,
            anomaly_flag=anomaly,
            dna=f"#龍芯⚡️丙午·乙未·甲寅·申时·师-P02-DR-CHAIN-{dna}"
        )

    # — 数学一致性校验 —
    def verify_dr_consistency(self, weights: Dict[str, float]) -> Tuple[bool, List[str], Dict[str, Any]]:
        """
        校验权重集的一致性
        ① 每个权重转数字根
        ② 链收不收敛到369
        ③ 三才权重比例合理性
        """
        issues: List[str] = []
        dr_map: Dict[str, int] = {}
        for k, v in weights.items():
            dr_map[k] = self.dr_from_float(v)

        dr_chain = self.chain(list(weights.values()))

        if not dr_chain.convergence_to_369:
            issues.append(f"⚠️ 权重链未收敛到369: {dr_chain.dr_values}")

        if dr_chain.anomaly_flag:
            issues.append(f"⚠️ 数字根链异常标记激活")

        # check 三才 3·6·9 对应性
        if "天" in weights and self.dr_from_float(weights["天"]) != 3:
            issues.append(f"⚠️ 天权重dr≠3: {dr_map.get('天')}")

        if "地" in weights and self.dr_from_float(weights["地"]) != 6:
            issues.append(f"⚠️ 地权重dr≠6: {dr_map.get('地')}")

        if "人" in weights and self.dr_from_float(weights["人"]) != 9:
            issues.append(f"⚠️ 人权重dr≠9: {dr_map.get('人')}")

        passed = len(issues) == 0
        return passed, issues, {
            "dr_map": dr_map,
            "dr_chain": asdict(dr_chain),
            "convergence_to_369": dr_chain.convergence_to_369
        }

    # — IPA回调 —
    def ipa_callback(self, weights: Dict[str, float]) -> Dict[str, Any]:
        """
        IPA-L7-PER-KNOW-007 回调参数：
        output: { calibrated: bool, dr_chain, corrections }
        """
        passed, issues, detail = self.verify_dr_consistency(weights)
        return {
            "node_id": "IPA-L7-PER-KNOW-007",
            "calibrated": passed,
            "dr_chain": detail["dr_chain"],
            "dr_map": detail["dr_map"],
            "issues": issues,
            "corrections": [f"调整权重使dr链收敛到369" for _ in issues] if issues else [],
            "369_immutables_hit": detail["dr_chain"].get("hits_369", 0),
            "dna": detail["dr_chain"]["dna"]
        }

    # — S-004 关联：贡献值系数计算 —
    def contrib_dr_factor(self, dr_val: int) -> float:
        """数字根→贡献值系数 η_dr"""
        if dr_val in (3, 6, 9): return 1.0     # 不动点全能量
        if dr_val in (1, 5): return 0.8        # 中轴
        if dr_val in (2, 7): return 0.6        # 对角线
        if dr_val in (4, 8): return 0.4        # 边角
        return 0.0


# — 自验证 —
if __name__ == "__main__":
    dr_eng = DigitalRootEngine()
    # 测试369不动点
    for n in [3, 6, 9, 36, 69, 369, 963]:
        print(f"dr({n}) = {dr_eng.dr(n)}  [{dr_range(dr_eng.dr(n))}]")
    # 测试链
    chain = dr_eng.chain([0.35, 0.20, 0.45], DRLevel.CHAIN)
    print(f"三才权重链: dr={chain.dr_values} 369命中={chain.hits_369} 收敛={chain.convergence_to_369} 五行={chain.primary_wuxing}")
    # 测试一致性
    result = dr_eng.verify_dr_consistency({"天": 0.35, "地": 0.20, "人": 0.45})
    print(f"一致性: {'✅' if result[0] else '❌'} {' | '.join(result[1]) if result[1] else '完美'}")

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·申时·䷃蒙-CONFIRM-SEAL-digital_root_engine-34171242
