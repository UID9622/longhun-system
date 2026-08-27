#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 数字根引擎 v1.0
369洛书数字根 · 三六九不动点 · 纯标准库零依赖

核心不动点: sn=369, log369=5.911, perm369=108
数字根算法: 各位数字反复求和直至一位数

DNA: #龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-DIGITAL-ROOT-UID9622
License: MulanPSL v2
"""

import math
from typing import Dict, List, Tuple, Any


# ═══════════════════════════════════════════════════════
# 焊死常量
# ═══════════════════════════════════════════════════════

# 369 不动点
FIXED_POINT_369 = 369
LOG_369 = math.log(369)  # 5.9108...
PERM_369 = 108  # (1+2+...+9)×3 - 27 = 108

# 洛书九宫
LUO_SHU_GRID = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6],
]

# 五行映射（数字→五行）
_WUXING_MAP = {
    0: {"element": "土", "direction": "中", "color": "黄"},
    1: {"element": "水", "direction": "北", "color": "黑"},
    2: {"element": "土", "direction": "中", "color": "黄"},
    3: {"element": "木", "direction": "东", "color": "青"},
    4: {"element": "木", "direction": "东", "color": "青"},
    5: {"element": "土", "direction": "中", "color": "黄"},
    6: {"element": "金", "direction": "西", "color": "白"},
    7: {"element": "金", "direction": "西", "color": "白"},
    8: {"element": "土", "direction": "中", "color": "黄"},
    9: {"element": "火", "direction": "南", "color": "赤"},
}

# 生克关系: 生 → [被生者], 克 → [被克者]
_SHENG_KE = {
    "金": {"生": "水", "克": "木"},
    "水": {"生": "木", "克": "火"},
    "木": {"生": "火", "克": "土"},
    "火": {"生": "土", "克": "金"},
    "土": {"生": "金", "克": "水"},
}


class DigitalRoot:
    """🐉 数字根计算引擎"""

    def compute(self, n: int) -> int:
        """计算数字根：各位数字反复求和直到一位数"""
        if n == 0:
            return 0
        # 数字根公式: n ≡ dr (mod 9), 且 dr∈[1,9], n=0→dr=0
        dr = n % 9
        return 9 if dr == 0 else dr

    def compute_str(self, s: str) -> int:
        """对字符串计算数字根（每位字符转数字）"""
        digits = [int(c) for c in s if c.isdigit()]
        if not digits:
            return 0
        total = sum(digits)
        return self.compute(total)

    def is_369(self, n: int) -> bool:
        """检查数字根是否为 3/6/9"""
        dr = self.compute(n)
        return dr in (3, 6, 9)

    def root_trace(self, n: int) -> List[int]:
        """数字根追溯：显示每一层求和过程"""
        if n < 10:
            return [n]
        trace = [n]
        while n >= 10:
            digits = [int(c) for c in str(n)]
            n = sum(digits)
            trace.append(n)
        return trace

    def verify_fixed_point(self) -> Dict[str, Any]:
        """验证 369 不动点（数学真理，永远通过）"""
        dr_369 = self.compute(FIXED_POINT_369)
        return {
            "fixed_point": FIXED_POINT_369,
            "digital_root": dr_369,
            "is_369": dr_369 in (3, 6, 9),
            "log_369": round(LOG_369, 6),
            "perm_369": PERM_369,
            "verification": "🟢 369不动点确认",
            "note": "sn=369 是所有以369为基数运算的不动点",
        }

    def wuxing(self, n: int) -> Dict[str, str]:
        """数字五行属性判定"""
        dr = self.compute(n)
        return _WUXING_MAP.get(dr, _WUXING_MAP[0])

    def sheng_ke(self, a: int, b: int) -> Dict[str, str]:
        """判断两数的五行生克关系"""
        wx_a = self.wuxing(a)["element"]
        wx_b = self.wuxing(b)["element"]

        if wx_a == wx_b:
            return {"relation": "比和", "detail": f"{wx_a}同{wx_b}", "harmony": True}

        sk_a = _SHENG_KE.get(wx_a, {})
        sk_b = _SHENG_KE.get(wx_b, {})

        if sk_a.get("生") == wx_b:
            return {"relation": "我生", "detail": f"{wx_a}生{wx_b}", "harmony": True}
        if sk_a.get("克") == wx_b:
            return {"relation": "我克", "detail": f"{wx_a}克{wx_b}", "harmony": True}
        if sk_b.get("生") == wx_a:
            return {"relation": "生我", "detail": f"{wx_b}生{wx_a}", "harmony": True}
        if sk_b.get("克") == wx_a:
            return {"relation": "克我", "detail": f"{wx_b}克{wx_a}", "harmony": False}

        return {"relation": "无直接关系", "detail": "", "harmony": True}

    def luo_shu_position(self, n: int) -> Dict[str, Any]:
        """数字在洛书九宫中的位置"""
        dr = self.compute(n)
        for row_idx, row in enumerate(LUO_SHU_GRID):
            if dr in row:
                col_idx = row.index(dr)
                return {
                    "number": dr,
                    "row": row_idx + 1,
                    "col": col_idx + 1,
                    "position": f"({row_idx + 1}, {col_idx + 1})",
                    "luo_shu_value": LUO_SHU_GRID[row_idx],
                }
        return {"number": dr, "position": "不在九宫"}

    def weight_score(self, data: Dict[str, float]) -> Dict[str, Any]:
        """多因子权重计算"""
        if not data:
            return {"score": 0, "weighted": {}}

        total_weight = sum(data.values())
        if total_weight == 0:
            return {"score": 0, "weighted": {}}

        weighted = {}
        score = 0.0
        for key, weight in data.items():
            w = weight / total_weight
            dr = self.compute(int(weight))
            weighted[key] = {
                "raw_weight": weight,
                "normalized": round(w, 4),
                "digital_root": dr,
                "is_369": dr in (3, 6, 9),
            }
            score += w * dr

        return {
            "score": round(score, 2),
            "root": self.compute(int(score * 1000)),
            "is_369_final": self.is_369(int(score * 1000)),
            "weighted": weighted,
        }

    @property
    def constants(self) -> Dict[str, Any]:
        """引擎常量摘要"""
        return {
            "FIXED_POINT_369": FIXED_POINT_369,
            "LOG_369": round(LOG_369, 6),
            "PERM_369": PERM_369,
            "LUO_SHU_SUM": sum(sum(row) for row in LUO_SHU_GRID) // 3,  # 15
            "WUXING_ELEMENTS": list(set(wx["element"] for wx in _WUXING_MAP.values())),
        }


# ═══════════════════════════════════════════════════════
# 模块级快捷函数
# ═══════════════════════════════════════════════════════

_engine = None


def _get_engine() -> DigitalRoot:
    global _engine
    if _engine is None:
        _engine = DigitalRoot()
    return _engine


def compute_root(n: int) -> int:
    """快捷数字根计算"""
    return _get_engine().compute(n)


def verify_root(n: int, expected: int) -> bool:
    """验证数字根"""
    return _get_engine().compute(n) == expected


# ═══════════════════════════════════════════════════════
# 自检
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    engine = DigitalRoot()

    # 基础验证
    assert compute_root(369) == 9  # 3+6+9=18, 1+8=9
    assert compute_root(12345) == 6  # 1+2+3+4+5=15, 1+5=6
    assert compute_root(0) == 0
    assert compute_root(9) == 9
    assert compute_root(999) == 9

    # 不动点验证
    fp = engine.verify_fixed_point()
    assert fp["is_369"], "369不动点验证失败"

    # 五行测试
    wx = engine.wuxing(369)
    assert wx["element"] == "火"  # 369→3+6+9=18→1+8=9→火

    # 权重测试
    w = engine.weight_score({"速度": 30, "安全": 50, "成本": 20})

    print(f"🟢 Digital Root v1.0 自检通过")
    print(f"   369不动点: {fp['verification']}")
    print(f"   369数字根: {fp['digital_root']} (应为9)")
    print(f"   369五行: {wx['element']}{wx['direction']}{wx['color']}")
    print(f"   权重得分: {w['score']} (根={w['root']})")
    print(f"   洛书宫和: {engine.constants['LUO_SHU_SUM']}")
