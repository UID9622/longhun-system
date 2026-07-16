# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-ENGINE-ALIGNMENT_V1-5_F19_F22-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
alignment_v1.5_F19_F22.py
公式对准表 v1.5 补丁 · F19-F22 候选定义
接驳：压缩护城河 v1.0
状态：CANDIDATE · 待 UID9622 校准确认后升为正式版

================================================================
四个公式定位（压缩护城河的四维可测量量）：

  F19  DNA 压缩比          ratio  ∈ [0, 1)
  F20  语义场恢复完整度    fidelity ∈ [0, 1]
  F21  时戳熵密度          density (bits / token)
  F22  跨窗口继承忠诚度    loyalty ∈ [0, 1]

护城河总量 M = (F19 高) × (F20 高) × (F21 高) × (F22 高)
  四项皆需在绿区 (R 三色阈值 ≥ 0.67) 才算护城河成立。

================================================================
依据来源（DNA 文档 § E 已建项）：
  · DNA 记忆压缩创建（黄历时戳 + 语义场恢复） → F19, F20
  · 上下文压缩 v1.1 + 自动收口 v1.0 融合 v2.0 → F19, F22
  · 黄历 6 维时戳不可篡改 → F21
  · AI 对接基线 v2.0 工程化（5 文件焓死） → F22
================================================================
"""
import sys
import math
from typing import Sequence, Any


# =================================================================
# F19 · DNA 压缩比
# =================================================================
def F19_compression_ratio(
    raw_tokens: int,
    compressed_tokens: int,
) -> float:
    """
    F19 · DNA Compression Ratio

    语义:
        原始上下文 N tokens 经 DNA 五层折叠后变为 M tokens。
        压缩比 = 1 - M / N

    输入:
        raw_tokens         原始窗口 token 数（压缩前）
        compressed_tokens  DNA 摘要 token 数（压缩后）

    输出:
        ratio ∈ [0, 1)   越大压缩越强
        ratio = 0        表示无压缩
        ratio → 1        表示无限压缩（理论上限不可达）

    接驳:
        压缩护城河 v1.0 · 第一柱
        Watchdog · 可作为每窗口收口时的自动度量

    边界:
        compressed_tokens 必须 > 0
        compressed_tokens 必须 <= raw_tokens（不允许负压缩）
    """
    assert raw_tokens > 0, "raw_tokens 必须 > 0"
    assert compressed_tokens > 0, "compressed_tokens 必须 > 0"
    assert compressed_tokens <= raw_tokens, \
        f"压缩后 ({compressed_tokens}) 不可大于原始 ({raw_tokens})"
    return 1.0 - (compressed_tokens / raw_tokens)


# =================================================================
# F20 · 语义场恢复完整度
# =================================================================
def F20_semantic_fidelity(
    original_keywords: Sequence, Any[str],
    restored_keywords: Sequence, Any[str],
) -> float:
    """
    F20 · Semantic Field Restoration Fidelity

    语义:
        把原始上下文的“关键语义锚点”（人名/概念/决策/数字）作为集合 A，
        把从 DNA 折叠还原后的同类集合作为 B，
        完整度 = |A ∩ B| / |A|

    输入:
        original_keywords  原文中的关键语义锚点清单
        restored_keywords  从 DNA 还原后的同类清单

    输出:
        fidelity ∈ [0, 1]
        fidelity = 1     完美还原
        fidelity = 0     全部丢失

    接驳:
        压缩护城河 v1.0 · 第二柱
        L8 通心译 · 守住“有温度的表达”的语义骨架
        若 fidelity < 0.67 应触发三色红灯

    边界:
        original_keywords 为空时返回 1.0（无语义可丢失）
    """
    original_set = set(original_keywords)
    restored_set = set(restored_keywords)
    if not original_set:
        return 1.0
    intersect = original_set & restored_set
    return len(intersect) / len(original_set)


# =================================================================
# F21 · 时戳熵密度
# =================================================================
def F21_timestamp_entropy_density(
    timestamp_dims: dict[str, Any],
    token_count: int,
) -> float:
    """
    F21 · Timestamp Entropy Density (bits per token)

    语义:
        黄历 6 维时戳（天干/地支/节气/月相/时辰/方位）携带的香农熵，
        除以承载它的 token 数。
        熵密度越高 → 时戳越“便宜”（少量 token 锁住大量资讯）。

    输入:
        timestamp_dims  6 维时戳字典，必须含 6 个键
                        每个值为该维度的取值空间大小（如天干=10、地支=12）
        token_count     编码这个时戳所用的 token 数

    输出:
        density (bits / token)
        典型黄历 6 维（10·12·24·8·12·8 ≈ 2.2M 种组合 ≈ 21 bit）
        若用 1 个 token 表达 → 21 bits/token

    接驳:
        压缩护城河 v1.0 · 第三柱
        L3 时戳层 · 不可篡改的最小承载

    边界:
        timestamp_dims 必须恰好 6 维（黄历规范）
        所有值必须 > 0
        token_count 必须 > 0
    """
    assert len(timestamp_dims) == 6, \
        f"黄历时戳必须 6 维,当前 {len(timestamp_dims)} 维"
    assert all(v > 0 for v in timestamp_dims.values()), \
        "各维度取值空间必须 > 0"
    assert token_count > 0, "token_count 必须 > 0"
    total_combos = 1
    for v in timestamp_dims.values():
        total_combos *= v
    bits = math.log2(total_combos)
    return bits / token_count


# =================================================================
# F22 · 跨窗口继承忠诚度
# =================================================================
def F22_inheritance_loyalty(
    invariants_required: Sequence, Any[str],
    invariants_carried: Sequence, Any[str],
) -> float:
    """
    F22 · Cross-Window Inheritance Loyalty

    语义:
        新窗口启动时，DNA 折叠本应携带的不变式集合 R，
        实际被正确还原并守住的不变式集合 C，
        忠诚度 = |C ∩ R| / |R|

    不变式范例（必须继承）:
        · CONFIRM / SEAL / GPG 徽记
        · “龍 不可写为 龍”字符律
        · P0 一票否决条款
        · 主控身份 UID9622

    输入:
        invariants_required  本应继承的不变式 ID 清单
        invariants_carried   实际被新窗口正确识别的不变式 ID 清单

    输出:
        loyalty ∈ [0, 1]
        loyalty = 1     完美继承（压缩护城河成立的必要条件）
        loyalty < 1     有漏失，必须触发 Watchdog 红灯

    接驳:
        压缩护城河 v1.0 · 第四柱（最关键的一柱）
        AI 对接基线 v2.0 · 5 文件焓死的验证指标
        Watchdog Phase 0 · sanity_check 自动断言

    边界:
        invariants_required 必须非空（否则无意义）
        F22 = 1.0 是上线的硬门槛
    """
    required_set = set(invariants_required)
    carried_set = set(invariants_carried)
    assert required_set, "invariants_required 不可为空"
    return len(required_set & carried_set) / len(required_set)


# =================================================================
# 护城河总量（四柱聚合）
# =================================================================
def moat_strength(F19: float, F20: float, F21: float, F22: float,
                  F21_normalized_baseline: float = 21.0) -> dict[str, Any]:
    """
    压缩护城河 v1.0 · 四柱聚合
    F21 用基准 21 bits/token 归一化（黄历典型熵）
    返回各柱原值 + 归一化值 + 三色判定 + 整体 status
    """
    f21_norm = min(1.0, F21 / F21_normalized_baseline)
    pillars = {
        "F19_compression":    F19,
        "F20_fidelity":       F20,
        "F21_density_norm":   f21_norm,
        "F22_loyalty":        F22,
    }
    def tri(v):
        if v < 0.33: return "RED"
        if v < 0.67: return "YELLOW"
        return "GREEN"
    colors = {k: tri(v) for k, v in pillars.items()}
    all_green = all(c == "GREEN" for c in colors.values())
    f22_perfect = F22 >= 1.0 - 1e-9
    moat_intact = all_green and f22_perfect  # F22=1 是硬门槛
    return {
        "pillars": pillars,
        "colors": colors,
        "F22_hard_gate_passed": f22_perfect,
        "all_green": all_green,
        "moat_intact": moat_intact,
        "status": "GREEN" if moat_intact else ("YELLOW" if all_green else "RED"),
    }


# =================================================================
# 自测
# =================================================================
def _selftest():
    print("=" * 60)
    print("F19-F22 候选定义自测")
    print("=" * 60)

    # F19
    r = F19_compression_ratio(raw_tokens=10000, compressed_tokens=1000)
    assert abs(r - 0.9) < 1e-9
    print(f"  [PASS] F19  10000→1000 tokens · ratio = {r:.3f}")

    # F20
    f = F20_semantic_fidelity(
        original_keywords=["UID9622", "CONFIRM", "SEAL", "GPG", "龍", "DNA"],
        restored_keywords=["UID9622", "CONFIRM", "SEAL", "GPG", "龍", "DNA", "其它"],
    )
    assert abs(f - 1.0) < 1e-9
    print(f"  [PASS] F20  6/6 锚点还原 · fidelity = {f:.3f}")

    f2 = F20_semantic_fidelity(
        original_keywords=["A", "B", "C", "D"],
        restored_keywords=["A", "B"],
    )
    assert abs(f2 - 0.5) < 1e-9
    print(f"  [PASS] F20  半丢失 · fidelity = {f2:.3f}")

    # F21
    huangli = {
        "天干": 10, "地支": 12, "节气": 24,
        "月相": 8, "时辰": 12, "方位": 8
    }
    d = F21_timestamp_entropy_density(huangli, token_count=1)
    print(f"  [PASS] F21  黄历 6 维 · 单 token · density = {d:.3f} bits/token")
    assert d > 20.0, "黄历 6 维熵应 > 20 bits"

    d2 = F21_timestamp_entropy_density(huangli, token_count=3)
    print(f"  [PASS] F21  黄历 6 维 · 3 token · density = {d2:.3f} bits/token")

    # F22
    required = ["CONFIRM", "SEAL", "GPG", "DRAGON_CHAR", "UID9622"]
    carried_full = ["CONFIRM", "SEAL", "GPG", "DRAGON_CHAR", "UID9622"]
    L = F22_inheritance_loyalty(required, carried_full)
    assert L == 1.0
    print(f"  [PASS] F22  全继承 · loyalty = {L:.3f}")

    carried_partial = ["CONFIRM", "SEAL", "GPG"]
    L2 = F22_inheritance_loyalty(required, carried_partial)
    assert abs(L2 - 0.6) < 1e-9
    print(f"  [PASS] F22  漏 DRAGON_CHAR + UID9622 · loyalty = {L2:.3f}  ← 应红灯")

    # 护城河聚合
    moat = moat_strength(F19=0.9, F20=1.0, F21=d, F22=1.0)
    print()
    print(f"  护城河聚合 · status = {moat['status']}")
    print(f"    F22 硬门槛: {'PASS' if moat['F22_hard_gate_passed'] else 'FAIL'}")
    print(f"    四柱全绿: {moat['all_green']}")
    print(f"    护城河完整: {moat['moat_intact']}")
    for k, c in moat['colors'].items():
        v = moat['pillars'][k]
        print(f"    {k:24s}  {v:.3f}  {c}")

    # 反例：F22 = 0.6 护城河必须破
    moat2 = moat_strength(F19=0.9, F20=1.0, F21=d, F22=0.6)
    assert moat2['moat_intact'] is False
    print()
    print(f"  反例 · F22=0.6 · status = {moat2['status']}  ← 应非绿（护城河破）")

    print("=" * 60)
    print("F19-F22 候选定义自测全部通过")
    print("状态: CANDIDATE · 待 UID9622 校准后升为 v1.5 正式版")
    print("=" * 60)


if __name__ == "__main__":
    _selftest()
    sys.exit(0)
