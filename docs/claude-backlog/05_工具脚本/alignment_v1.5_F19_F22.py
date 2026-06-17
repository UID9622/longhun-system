#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
alignment_v1.5_F19_F22.py
公式對準表 v1.5 補丁 · F19-F22 候選定義
接駁：壓縮護城河 v1.0
狀態：CANDIDATE · 待 UID9622 校準確認後升為正式版

================================================================
四個公式定位（壓縮護城河的四維可測量量）：

  F19  DNA 壓縮比          ratio  ∈ [0, 1)
  F20  語義場恢復完整度    fidelity ∈ [0, 1]
  F21  時戳熵密度          density (bits / token)
  F22  跨窗口繼承忠誠度    loyalty ∈ [0, 1]

護城河總量 M = (F19 高) × (F20 高) × (F21 高) × (F22 高)
  四項皆需在綠區 (R 三色閾值 ≥ 0.67) 才算護城河成立。

================================================================
依據來源（DNA 文檔 § E 已建項）：
  · DNA 記憶壓縮創建（黃曆時戳 + 語義場恢復） → F19, F20
  · 上下文壓縮 v1.1 + 自動收口 v1.0 融合 v2.0 → F19, F22
  · 黃曆 6 維時戳不可篡改 → F21
  · AI 對接基線 v2.0 工程化（5 文件焓死） → F22
================================================================
"""
import sys
import math
from typing import Sequence


# =================================================================
# F19 · DNA 壓縮比
# =================================================================
def F19_compression_ratio(
    raw_tokens: int,
    compressed_tokens: int,
) -> float:
    """
    F19 · DNA Compression Ratio

    語義:
        原始上下文 N tokens 經 DNA 五層摺疊後變為 M tokens。
        壓縮比 = 1 - M / N

    輸入:
        raw_tokens         原始窗口 token 數（壓縮前）
        compressed_tokens  DNA 摘要 token 數（壓縮後）

    輸出:
        ratio ∈ [0, 1)   越大壓縮越強
        ratio = 0        表示無壓縮
        ratio → 1        表示無限壓縮（理論上限不可達）

    接駁:
        壓縮護城河 v1.0 · 第一柱
        Watchdog · 可作為每窗口收口時的自動度量

    邊界:
        compressed_tokens 必須 > 0
        compressed_tokens 必須 <= raw_tokens（不允許負壓縮）
    """
    assert raw_tokens > 0, "raw_tokens 必須 > 0"
    assert compressed_tokens > 0, "compressed_tokens 必須 > 0"
    assert compressed_tokens <= raw_tokens, \
        f"壓縮後 ({compressed_tokens}) 不可大於原始 ({raw_tokens})"
    return 1.0 - (compressed_tokens / raw_tokens)


# =================================================================
# F20 · 語義場恢復完整度
# =================================================================
def F20_semantic_fidelity(
    original_keywords: Sequence[str],
    restored_keywords: Sequence[str],
) -> float:
    """
    F20 · Semantic Field Restoration Fidelity

    語義:
        把原始上下文的「關鍵語義錨點」（人名/概念/決策/數字）作為集合 A，
        把從 DNA 摺疊還原後的同類集合作為 B，
        完整度 = |A ∩ B| / |A|

    輸入:
        original_keywords  原文中的關鍵語義錨點清單
        restored_keywords  從 DNA 還原後的同類清單

    輸出:
        fidelity ∈ [0, 1]
        fidelity = 1     完美還原
        fidelity = 0     全部丟失

    接駁:
        壓縮護城河 v1.0 · 第二柱
        L8 通心譯 · 守住「有溫度的表達」的語義骨架
        若 fidelity < 0.67 應觸發三色紅燈

    邊界:
        original_keywords 為空時返回 1.0（無語義可丟失）
    """
    original_set = set(original_keywords)
    restored_set = set(restored_keywords)
    if not original_set:
        return 1.0
    intersect = original_set & restored_set
    return len(intersect) / len(original_set)


# =================================================================
# F21 · 時戳熵密度
# =================================================================
def F21_timestamp_entropy_density(
    timestamp_dims: dict,
    token_count: int,
) -> float:
    """
    F21 · Timestamp Entropy Density (bits per token)

    語義:
        黃曆 6 維時戳（天干/地支/節氣/月相/時辰/方位）攜帶的香農熵，
        除以承載它的 token 數。
        熵密度越高 → 時戳越「便宜」（少量 token 鎖住大量資訊）。

    輸入:
        timestamp_dims  6 維時戳字典，必須含 6 個鍵
                        每個值為該維度的取值空間大小（如天干=10、地支=12）
        token_count     編碼這個時戳所用的 token 數

    輸出:
        density (bits / token)
        典型黃曆 6 維（10·12·24·8·12·8 ≈ 2.2M 種組合 ≈ 21 bit）
        若用 1 個 token 表達 → 21 bits/token

    接駁:
        壓縮護城河 v1.0 · 第三柱
        L3 時戳層 · 不可篡改的最小承載

    邊界:
        timestamp_dims 必須恰好 6 維（黃曆規範）
        所有值必須 > 0
        token_count 必須 > 0
    """
    assert len(timestamp_dims) == 6, \
        f"黃曆時戳必須 6 維,當前 {len(timestamp_dims)} 維"
    assert all(v > 0 for v in timestamp_dims.values()), \
        "各維度取值空間必須 > 0"
    assert token_count > 0, "token_count 必須 > 0"
    total_combos = 1
    for v in timestamp_dims.values():
        total_combos *= v
    bits = math.log2(total_combos)
    return bits / token_count


# =================================================================
# F22 · 跨窗口繼承忠誠度
# =================================================================
def F22_inheritance_loyalty(
    invariants_required: Sequence[str],
    invariants_carried: Sequence[str],
) -> float:
    """
    F22 · Cross-Window Inheritance Loyalty

    語義:
        新窗口啟動時，DNA 摺疊本應攜帶的不變式集合 R，
        實際被正確還原並守住的不變式集合 C，
        忠誠度 = |C ∩ R| / |R|

    不變式範例（必須繼承）:
        · CONFIRM / SEAL / GPG 徽記
        · 「龍 不可寫為 龙」字符律
        · P0 一票否決條款
        · 主控身份 UID9622

    輸入:
        invariants_required  本應繼承的不變式 ID 清單
        invariants_carried   實際被新窗口正確識別的不變式 ID 清單

    輸出:
        loyalty ∈ [0, 1]
        loyalty = 1     完美繼承（壓縮護城河成立的必要條件）
        loyalty < 1     有漏失，必須觸發 Watchdog 紅燈

    接駁:
        壓縮護城河 v1.0 · 第四柱（最關鍵的一柱）
        AI 對接基線 v2.0 · 5 文件焓死的驗證指標
        Watchdog Phase 0 · sanity_check 自動斷言

    邊界:
        invariants_required 必須非空（否則無意義）
        F22 = 1.0 是上線的硬門檻
    """
    required_set = set(invariants_required)
    carried_set = set(invariants_carried)
    assert required_set, "invariants_required 不可為空"
    return len(required_set & carried_set) / len(required_set)


# =================================================================
# 護城河總量（四柱聚合）
# =================================================================
def moat_strength(F19: float, F20: float, F21: float, F22: float,
                  F21_normalized_baseline: float = 21.0) -> dict:
    """
    壓縮護城河 v1.0 · 四柱聚合
    F21 用基準 21 bits/token 歸一化（黃曆典型熵）
    返回各柱原值 + 歸一化值 + 三色判定 + 整體 status
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
    moat_intact = all_green and f22_perfect  # F22=1 是硬門檻
    return {
        "pillars": pillars,
        "colors": colors,
        "F22_hard_gate_passed": f22_perfect,
        "all_green": all_green,
        "moat_intact": moat_intact,
        "status": "GREEN" if moat_intact else ("YELLOW" if all_green else "RED"),
    }


# =================================================================
# 自測
# =================================================================
def _selftest():
    print("=" * 60)
    print("F19-F22 候選定義自測")
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
    print(f"  [PASS] F20  6/6 錨點還原 · fidelity = {f:.3f}")

    f2 = F20_semantic_fidelity(
        original_keywords=["A", "B", "C", "D"],
        restored_keywords=["A", "B"],
    )
    assert abs(f2 - 0.5) < 1e-9
    print(f"  [PASS] F20  半丟失 · fidelity = {f2:.3f}")

    # F21
    huangli = {
        "天干": 10, "地支": 12, "節氣": 24,
        "月相": 8, "時辰": 12, "方位": 8
    }
    d = F21_timestamp_entropy_density(huangli, token_count=1)
    print(f"  [PASS] F21  黃曆 6 維 · 單 token · density = {d:.3f} bits/token")
    assert d > 20.0, "黃曆 6 維熵應 > 20 bits"

    d2 = F21_timestamp_entropy_density(huangli, token_count=3)
    print(f"  [PASS] F21  黃曆 6 維 · 3 token · density = {d2:.3f} bits/token")

    # F22
    required = ["CONFIRM", "SEAL", "GPG", "DRAGON_CHAR", "UID9622"]
    carried_full = ["CONFIRM", "SEAL", "GPG", "DRAGON_CHAR", "UID9622"]
    L = F22_inheritance_loyalty(required, carried_full)
    assert L == 1.0
    print(f"  [PASS] F22  全繼承 · loyalty = {L:.3f}")

    carried_partial = ["CONFIRM", "SEAL", "GPG"]
    L2 = F22_inheritance_loyalty(required, carried_partial)
    assert abs(L2 - 0.6) < 1e-9
    print(f"  [PASS] F22  漏 DRAGON_CHAR + UID9622 · loyalty = {L2:.3f}  ← 應紅燈")

    # 護城河聚合
    moat = moat_strength(F19=0.9, F20=1.0, F21=d, F22=1.0)
    print()
    print(f"  護城河聚合 · status = {moat['status']}")
    print(f"    F22 硬門檻: {'PASS' if moat['F22_hard_gate_passed'] else 'FAIL'}")
    print(f"    四柱全綠: {moat['all_green']}")
    print(f"    護城河完整: {moat['moat_intact']}")
    for k, c in moat['colors'].items():
        v = moat['pillars'][k]
        print(f"    {k:24s}  {v:.3f}  {c}")

    # 反例：F22 = 0.6 護城河必須破
    moat2 = moat_strength(F19=0.9, F20=1.0, F21=d, F22=0.6)
    assert moat2['moat_intact'] is False
    print()
    print(f"  反例 · F22=0.6 · status = {moat2['status']}  ← 應非綠（護城河破）")

    print("=" * 60)
    print("F19-F22 候選定義自測全部通過")
    print("狀態: CANDIDATE · 待 UID9622 校準後升為 v1.5 正式版")
    print("=" * 60)


if __name__ == "__main__":
    _selftest()
    sys.exit(0)
