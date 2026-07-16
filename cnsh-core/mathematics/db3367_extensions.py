#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion DB3367 公式扩展库 v1.0

把 `cnsh/notion/modules/db3367/` 下 16 个 CNSH 注释模块的核心函数
注册进 longhun-math-formula-core，统一入口、统一命名、统一自检。

DNA: #龍芯⚡️2026-07-05-LONGHUN-MATH-FORMULA-DB3367-EXTENSIONS-v1.0
"""
from __future__ import annotations

import math
import random
from math import isclose
from typing import List, Tuple, Dict, Optional, Any

# ═══════════════════════════════════════════════════════════════
# 1. 信息论 · Information Theory
# ═══════════════════════════════════════════════════════════════

def shannon_entropy(sequence: List[Any]) -> float:
    """离散序列的香农熵（单位：bits）"""
    n = len(sequence)
    if n == 0:
        return 0.0
    counts = {}
    for x in sequence:
        counts[x] = counts.get(x, 0) + 1
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def mutual_information(x: List[Any], y: List[Any]) -> float:
    """两个等长序列的互信息"""
    if len(x) != len(y) or len(x) == 0:
        return 0.0
    hxy = shannon_entropy(list(zip(x, y)))
    return shannon_entropy(x) + shannon_entropy(y) - hxy


# ═══════════════════════════════════════════════════════════════
# 2. 河洛图 · Hetu & Luoshu
# ═══════════════════════════════════════════════════════════════

LUOSHU_MATRIX = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6],
]

HETU_PAIRS = {
    "水": (1, 6),
    "火": (2, 7),
    "木": (3, 8),
    "金": (4, 9),
    "土": (5, 10),
}


def luoshu_position(row: int, col: int) -> int:
    """row, col 从 1 开始，返回洛书九宫数字"""
    return LUOSHU_MATRIX[row - 1][col - 1]


def luoshu_magic_ok(m: List[List[int]] = None) -> bool:
    """3 阶幻方校验：行、列、对角线和均为 15"""
    if m is None:
        m = LUOSHU_MATRIX
    rows = [sum(r) for r in m]
    cols = [sum(m[i][j] for i in range(3)) for j in range(3)]
    diag1 = sum(m[i][i] for i in range(3))
    diag2 = sum(m[i][2 - i] for i in range(3))
    return all(x == 15 for x in rows + cols + [diag1, diag2])


def hetu_pair(element: str) -> Tuple[int, int]:
    """返回某五行的河图生成数对"""
    return HETU_PAIRS.get(element, (0, 0))


# ═══════════════════════════════════════════════════════════════
# 3. 采样定理 · Nyquist
# ═══════════════════════════════════════════════════════════════

def nyquist_check(sample_rate: float, max_freq: float, safety_factor: float = 2.2) -> Dict[str, Any]:
    """检查采样率是否满足奈奎斯特条件，并给出工程建议"""
    nyquist_rate = 2 * max_freq
    safe_rate = safety_factor * nyquist_rate
    return {
        "sample_rate": sample_rate,
        "max_freq": max_freq,
        "nyquist_rate": nyquist_rate,
        "safe_rate": safe_rate,
        "meets_theorem": sample_rate >= nyquist_rate,
        "engineer_safe": sample_rate >= safe_rate,
        "advice": "ok" if sample_rate >= safe_rate else ("critical" if sample_rate >= nyquist_rate else "aliasing"),
    }


# ═══════════════════════════════════════════════════════════════
# 4. 傅里叶变换 · Fourier Transform
# ═══════════════════════════════════════════════════════════════

def dft(time_series: List[float]) -> List[complex]:
    """离散傅里叶变换（零依赖实现）"""
    N = len(time_series)
    result = []
    for k in range(N):
        real = 0.0
        imag = 0.0
        for n in range(N):
            angle = -2 * math.pi * k * n / N
            real += time_series[n] * math.cos(angle)
            imag += time_series[n] * math.sin(angle)
        result.append(complex(real, imag))
    return result


def amplitude_spectrum(freq_series: List[complex]) -> List[float]:
    return [abs(x) for x in freq_series]


def dominant_frequency(freq_series: List[complex], sample_rate: float) -> Tuple[int, float]:
    """返回 (频率索引, 频率 Hz)"""
    N = len(freq_series)
    amps = amplitude_spectrum(freq_series)
    k = max(range(N // 2), key=lambda i: amps[i])
    return k, k * sample_rate / N


# ═══════════════════════════════════════════════════════════════
# 5. 自动微分 · Automatic Differentiation
# ═══════════════════════════════════════════════════════════════

class DualNumber:
    """对偶数：a + ε·a'，ε² = 0，用于前向自动微分"""
    def __init__(self, value: float, derivative: float = 0.0):
        self.value = value
        self.derivative = derivative

    def __repr__(self):
        return f"DualNumber({self.value}, {self.derivative})"

    def __add__(self, other):
        o = other if isinstance(other, DualNumber) else DualNumber(other)
        return DualNumber(self.value + o.value, self.derivative + o.derivative)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        o = other if isinstance(other, DualNumber) else DualNumber(other)
        return DualNumber(self.value - o.value, self.derivative - o.derivative)

    def __mul__(self, other):
        o = other if isinstance(other, DualNumber) else DualNumber(other)
        return DualNumber(
            self.value * o.value,
            self.value * o.derivative + self.derivative * o.value,
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, n: int):
        return DualNumber(self.value ** n, n * (self.value ** (n - 1)) * self.derivative)


def dual_sin(x: DualNumber) -> DualNumber:
    return DualNumber(math.sin(x.value), math.cos(x.value) * x.derivative)


def dual_exp(x: DualNumber) -> DualNumber:
    return DualNumber(math.exp(x.value), math.exp(x.value) * x.derivative)


# ═══════════════════════════════════════════════════════════════
# 6. 数值方法 · Numerical Methods
# ═══════════════════════════════════════════════════════════════

def newton_raphson(f, df, x0: float, tol: float = 1e-6, max_iter: int = 100) -> Dict[str, Any]:
    x = x0
    for i in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return {"root": x, "iterations": i, "f(x)": fx}
        dfx = df(x)
        if abs(dfx) < 1e-12:
            return {"root": x, "iterations": i, "f(x)": fx, "error": "derivative near zero"}
        x = x - fx / dfx
    return {"root": x, "iterations": max_iter, "f(x)": f(x), "error": "not converged"}


def bisection(f, a: float, b: float, tol: float = 1e-6) -> Dict[str, Any]:
    if f(a) * f(b) > 0:
        return {"error": "f(a) and f(b) same sign"}
    it = 0
    while abs(b - a) > tol:
        c = (a + b) / 2
        if f(c) == 0:
            return {"root": c, "iterations": it}
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
        it += 1
    return {"root": (a + b) / 2, "iterations": it}


def trapezoidal_integral(f, a: float, b: float, n: int = 100) -> float:
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return s * h


def jacobi_iteration(A: List[List[float]], b: List[float], x0: List[float] = None,
                     tol: float = 1e-6, max_iter: int = 100) -> Dict[str, Any]:
    n = len(A)
    x = x0[:] if x0 else [0.0] * n
    for it in range(max_iter):
        x_new = []
        for i in range(n):
            sigma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new.append((b[i] - sigma) / A[i][i])
        if max(abs(x_new[i] - x[i]) for i in range(n)) < tol:
            return {"solution": x_new, "iterations": it}
        x = x_new
    return {"solution": x, "iterations": max_iter, "error": "not converged"}


# ═══════════════════════════════════════════════════════════════
# 7. 量子计算抽象层 · Quantum Abstract
# ═══════════════════════════════════════════════════════════════

def ket_zero() -> List[complex]:
    return [1 + 0j, 0 + 0j]


def ket_one() -> List[complex]:
    return [0 + 0j, 1 + 0j]


def tensor_product(a: List[complex], b: List[complex]) -> List[complex]:
    return [ai * bj for ai in a for bj in b]


def mat_vec_mul(M: List[List[complex]], v: List[complex]) -> List[complex]:
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def hadamard_gate() -> List[List[complex]]:
    h = 1 / math.sqrt(2)
    return [[h, h], [h, -h]]


def pauli_x_gate() -> List[List[complex]]:
    return [[0, 1], [1, 0]]


def measurement_probabilities(state: List[complex]) -> List[float]:
    return [abs(x) ** 2 for x in state]


def measure_state(state: List[complex]) -> int:
    probs = measurement_probabilities(state)
    r = random.random()
    s = 0.0
    for i, p in enumerate(probs):
        s += p
        if r <= s:
            return i
    return len(probs) - 1


# ═══════════════════════════════════════════════════════════════
# 8. 渲染几何 · Geometry + Rendering
# ═══════════════════════════════════════════════════════════════

class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z

    def __repr__(self):
        return f"Vector3({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, s: float):
        return Vector3(self.x * s, self.y * s, self.z * s)

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self) -> float:
        return math.sqrt(self.dot(self))

    def normalize(self):
        L = self.length()
        if L == 0:
            return Vector3(0, 0, 0)
        return self * (1 / L)


class Ray:
    def __init__(self, origin: Vector3, direction: Vector3):
        self.origin = origin
        self.direction = direction.normalize()

    def at(self, t: float) -> Vector3:
        return self.origin + self.direction * t


class Sphere:
    def __init__(self, center: Vector3, radius: float):
        self.center = center
        self.radius = radius

    def intersect(self, ray: Ray) -> Tuple[bool, float]:
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius ** 2
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return False, float('inf')
        t = (-b - math.sqrt(discriminant)) / (2 * a)
        return t > 0, t


# ═══════════════════════════════════════════════════════════════
# 9. 五行 · WuXing
# ═══════════════════════════════════════════════════════════════

WUXING_ELEMENTS = ["水", "火", "木", "金", "土"]

DR_TO_WUXING = {
    1: "水", 6: "水",
    2: "火", 7: "火",
    3: "木", 8: "木",
    4: "金", 9: "金",
    5: "土",
}

WUXING_GENERATE = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
WUXING_CONTROL = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}


def dr_to_wuxing(dr: int) -> str:
    return DR_TO_WUXING.get(dr, "土")


def wuxing_relation(a: str, b: str) -> str:
    if WUXING_GENERATE.get(a) == b:
        return "generate"
    if WUXING_CONTROL.get(a) == b:
        return "control"
    return "neutral"


def wuxing_harmony(elements: List[str]) -> float:
    if not elements:
        return 0.0
    counts = {w: 0 for w in WUXING_ELEMENTS}
    for e in elements:
        if e in counts:
            counts[e] += 1
    n = len(elements)
    total_deviation = sum(abs(counts[w] / n - 0.2) for w in WUXING_ELEMENTS)
    return max(0.0, 1.0 - total_deviation / 2.0)


def wuxing_chain(start: str, relation: Dict[str, str]) -> List[str]:
    chain = [start]
    current = start
    while True:
        nxt = relation.get(current)
        if not nxt or nxt == start:
            break
        chain.append(nxt)
        current = nxt
    return chain


# ═══════════════════════════════════════════════════════════════
# 10. 数字根 369 · Digital Root 369
# ═══════════════════════════════════════════════════════════════

def digital_root_369(n: int) -> int:
    """世界标准数字根"""
    n = abs(n)
    return 0 if n == 0 else 1 + (n - 1) % 9


def is_369(n: int) -> bool:
    return digital_root_369(n) in {3, 6, 9}


def dr_fuse_369(n: int) -> str:
    """模块规则：dr=1 绿，dr=5 黄，其他红"""
    dr = digital_root_369(n)
    if dr == 1:
        return "🟢"
    if dr == 5:
        return "🟡"
    return "🔴"


DR_TO_LUOSHU_POS = {
    1: (3, 2), 2: (1, 3), 3: (2, 3),
    4: (1, 1), 5: (2, 2), 6: (3, 3),
    7: (3, 1), 8: (2, 1), 9: (1, 2),
}


def dr_to_luoshu_pos(n: int) -> Tuple[int, int]:
    return DR_TO_LUOSHU_POS.get(digital_root_369(n), (2, 2))


def string_digital_root(s: str) -> int:
    total = sum(ord(c) for c in s if not c.isspace())
    return digital_root_369(total)


# ═══════════════════════════════════════════════════════════════
# 11. 通心译六维路由 · Tongxinyi 6-Dim Routing
# ═══════════════════════════════════════════════════════════════

TONGXINYI_BASES = (6, 9, 8, 64, 5, 120)


def encode_tongxinyi_path(coords: Tuple[int, int, int, int, int, int]) -> int:
    """六维坐标 → 路径编号"""
    pid = coords[0]
    for dim, base in zip(coords[1:], TONGXINYI_BASES[1:]):
        pid = pid * base + dim
    return pid


def decode_tongxinyi_path(path_id: int) -> Tuple[int, int, int, int, int, int]:
    """路径编号 → 六维坐标"""
    coords = []
    rest = path_id
    for base in reversed(TONGXINYI_BASES):
        coords.append(rest % base)
        rest //= base
    coords.reverse()
    return tuple(coords)


# ═══════════════════════════════════════════════════════════════
# 12. CNSH 公式三件套 · CNSH Formulas
# ═══════════════════════════════════════════════════════════════

def sancai_energy(sancai: Tuple[float, float, float]) -> float:
    tian, di, ren = sancai
    return math.sqrt(tian * tian + di * di + ren * ren)


def sancai_route(sancai: Tuple[float, float, float], threshold: float = 0.1) -> str:
    tian, di, ren = sancai
    vals = [tian, di, ren]
    names = ["tian", "di", "ren"]
    sorted_vals = sorted(vals, reverse=True)
    if sorted_vals[0] - sorted_vals[1] < threshold:
        return "center"
    return names[vals.index(sorted_vals[0])]


def sancai_validate(sancai: Tuple[float, float, float]) -> Tuple[float, str]:
    tian, di, ren = sancai
    s = tian + di + ren
    penalty = max(0.0, -min(sancai))
    score = max(0.0, 1.0 - abs(s - 1.0) / 2.0 - penalty)
    if score >= 0.85:
        return score, "🟢"
    if score >= 0.50:
        return score, "🟡"
    return score, "🔴"


def hexagram_transition(hexagram: int, yao: int) -> int:
    """hexagram: 0-63, yao: 1-6"""
    return hexagram ^ (1 << (yao - 1))


# ═══════════════════════════════════════════════════════════════
# 13. 八卦 · Bagua
# ═══════════════════════════════════════════════════════════════

BAGUA_NAMES = ["乾", "坤", "震", "巽", "坎", "离", "艮", "兑"]
BAGUA_SYMBOLS = ["☰", "☷", "☳", "☴", "☵", "☲", "☶", "☱"]
BAGUA_NATURE = ["天", "地", "雷", "风", "水", "火", "山", "泽"]
BAGUA_WUXING = ["金", "土", "木", "木", "水", "火", "土", "金"]


def trigram_from_lines(lower: int, middle: int, upper: int) -> int:
    """下爻为最低位，返回 0-7"""
    return lower + middle * 2 + upper * 4


def trigram_to_lines(idx: int) -> Tuple[int, int, int]:
    lower = idx & 1
    middle = (idx >> 1) & 1
    upper = (idx >> 2) & 1
    return lower, middle, upper


def compose_gua64(upper_idx: int, lower_idx: int) -> int:
    return upper_idx * 8 + lower_idx


def split_gua64(gua64_idx: int) -> Tuple[int, int]:
    return gua64_idx // 8, gua64_idx % 8


# ═══════════════════════════════════════════════════════════════
# 14. 64 卦 · 64 Gua
# ═══════════════════════════════════════════════════════════════

GUA64_NAMES = [
    ["乾", "泰", "大壮", "小畜", "需", "大有", "大畜", "夬"],
    ["否", "坤", "豫", "观", "比", "晋", "剥", "萃"],
    ["无妄", "复", "震", "益", "屯", "噬嗑", "颐", "随"],
    ["姤", "升", "恒", "巽", "井", "鼎", "蛊", "大过"],
    ["讼", "师", "解", "涣", "坎", "未济", "蒙", "困"],
    ["同人", "明夷", "丰", "家人", "既济", "离", "贲", "革"],
    ["遁", "谦", "小过", "渐", "蹇", "旅", "艮", "咸"],
    ["履", "临", "归妹", "中孚", "节", "睽", "损", "兑"],
]

GUA64_WUXING_OVERRIDES = {
    "乾": "金", "夬": "金", "大有": "金",
    "坤": "土", "复": "土", "谦": "土",
    "震": "木", "屯": "木", "解": "木",
    "巽": "木", "观": "木", "涣": "木",
    "坎": "水", "讼": "水", "困": "水",
    "离": "火", "革": "火", "同人": "火",
    "艮": "土", "颐": "土", "贲": "土",
    "兑": "金", "咸": "金", "萃": "金",
}

WUXING_TO_AUDIT = {"金": "🟢", "土": "🟢", "木": "🟡", "火": "🟡", "水": "🔴"}


def gua64_name(upper_idx: int, lower_idx: int) -> str:
    return GUA64_NAMES[upper_idx][lower_idx]


def gua64_name_to_index(name: str) -> Tuple[int, int]:
    for i, row in enumerate(GUA64_NAMES):
        for j, n in enumerate(row):
            if n == name:
                return i, j
    raise ValueError(f"Unknown gua64 name: {name}")


def gua64_to_binary(upper_idx: int, lower_idx: int) -> int:
    return (upper_idx << 3) | lower_idx


def binary_to_gua64(g: int) -> Tuple[int, int]:
    return (g >> 3) & 0b111, g & 0b111


def gua64_audit(name: str) -> str:
    wx = GUA64_WUXING_OVERRIDES.get(name, "土")
    return WUXING_TO_AUDIT.get(wx, "🟡")


# ═══════════════════════════════════════════════════════════════
# 15. 天干地支 · Stems & Branches
# ═══════════════════════════════════════════════════════════════

TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
SHENGXIAO = ["鼠", "牛", "虎", "兔", "龍", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

TIANGAN_WUXING = ["木", "木", "火", "火", "土", "土", "金", "金", "水", "水"]
DIZHI_WUXING = ["水", "土", "木", "木", "土", "火", "火", "土", "金", "金", "土", "水"]


def jiazi_sequence(n: int = 60) -> List[str]:
    return [TIANGAN[i % 10] + DIZHI[i % 12] for i in range(n)]


def year_to_ganzhi(year: int) -> str:
    """以 1984 年为甲子年"""
    offset = (year - 1984) % 60
    return TIANGAN[offset % 10] + DIZHI[offset % 12]


def stem_branch_wuxing(ganzhi: str) -> Tuple[str, str]:
    g, z = ganzhi[0], ganzhi[1]
    return TIANGAN_WUXING[TIANGAN.index(g)], DIZHI_WUXING[DIZHI.index(z)]


# ═══════════════════════════════════════════════════════════════
# 16. 三才向量合成 · SanCai Vector Composition
# ═══════════════════════════════════════════════════════════════

def default_sancai_weights() -> Dict[str, float]:
    return {"tian": 0.30, "di": 0.20, "ren": 0.50}


def sancai_vector(sancai: Tuple[float, float, float],
                  weights: Dict[str, float] = None) -> Dict[str, Any]:
    if weights is None:
        weights = default_sancai_weights()
    tian, di, ren = sancai
    w = [weights["tian"], weights["di"], weights["ren"]]
    s = sum(w)
    w = [x / s for x in w]
    vx = w[0] * tian + w[1] * di + w[2] * ren
    vy = w[0] * (tian - ren)
    magnitude = math.sqrt(vx * vx + vy * vy)
    angle = math.atan2(vy, vx)
    return {
        "tian": tian, "di": di, "ren": ren,
        "weights": {"tian": w[0], "di": w[1], "ren": w[2]},
        "magnitude": magnitude,
        "angle": angle,
    }


def sancai_check(sancai: Tuple[float, float, float]) -> Tuple[float, str]:
    score, color = sancai_validate(sancai)
    return score, color


def sancai_route_vector(sancai: Tuple[float, float, float], threshold: float = 0.1) -> Dict[str, Any]:
    route = sancai_route(sancai, threshold)
    return {"route": route, "resonance": {"tian": sancai[0], "di": sancai[1], "ren": sancai[2]}}


def sancai_decision_score(H: float, E: float, P: float) -> Tuple[float, str]:
    human_weight = max(0.5, 1 - (H * 0.3 + E * 0.3))
    score = H * 0.25 + E * 0.25 + P * human_weight
    if score >= 0.85:
        return score, "🟢"
    if score >= 0.50:
        return score, "🟡"
    return score, "🔴"


# ═══════════════════════════════════════════════════════════════
# 自检
# ═══════════════════════════════════════════════════════════════

def selftest() -> None:
    print("\n" + "=" * 80)
    print("🐉 Notion DB3367 公式扩展库 · 自检")
    print("=" * 80 + "\n")

    # 信息论
    assert isclose(shannon_entropy(["龍", "魂", "龍", "魂"]), 1.0)
    print("[1] 信息论: shannon_entropy ✅")

    # 河洛图
    assert luoshu_magic_ok()
    assert luoshu_position(2, 2) == 5
    print("[2] 河洛图: magic_ok, position ✅")

    # 采样定理
    r = nyquist_check(44100, 20000)
    assert r["meets_theorem"]
    print("[3] 采样定理: nyquist_check ✅")

    # 傅里叶变换
    X = dft([math.sin(2 * math.pi * i / 8) for i in range(8)])
    assert len(X) == 8
    print("[4] 傅里叶变换: dft ✅")

    # 自动微分
    x = DualNumber(2.0, 1.0)
    f = x ** 2 + dual_sin(x)
    assert isclose(f.value, 4.909297426825682, abs_tol=1e-6)
    print("[5] 自动微分: DualNumber ✅")

    # 数值方法
    nr = newton_raphson(lambda x: x * x - 2, lambda x: 2 * x, 1.0)
    assert isclose(nr["root"], math.sqrt(2), abs_tol=1e-6)
    print("[6] 数值方法: newton_raphson ✅")

    # 量子计算
    H = hadamard_gate()
    zero = ket_zero()
    super = mat_vec_mul(H, zero)
    assert isclose(sum(measurement_probabilities(super)), 1.0)
    print("[7] 量子计算: hadamard, measure ✅")

    # 渲染几何
    ray = Ray(Vector3(0, 0, 0), Vector3(0, 0, 1))
    sphere = Sphere(Vector3(0, 0, 5), 1)
    hit, t = sphere.intersect(ray)
    assert hit and isclose(t, 4.0)
    print("[8] 渲染几何: ray-sphere intersect ✅")

    # 五行
    assert dr_to_wuxing(8) == "木"
    assert wuxing_relation("木", "火") == "generate"
    assert wuxing_harmony(["水", "火", "木", "金", "土"]) == 1.0
    print("[9] 五行: dr→wuxing, relation, harmony ✅")

    # 数字根 369
    assert digital_root_369(369) == 9
    assert is_369(18)
    assert dr_fuse_369(1) == "🟢"
    print("[10] 数字根369: dr, 369, fuse ✅")

    # 通心译
    coords = (3, 4, 2, 30, 2, 60)
    pid = encode_tongxinyi_path(coords)
    assert decode_tongxinyi_path(pid) == coords
    print("[11] 通心译六维: encode/decode ✅")

    # CNSH 公式
    e = sancai_energy((0.5, 0.3, 0.2))
    assert e > 0
    assert sancai_route((0.5, 0.3, 0.2)) == "tian"
    print("[12] CNSH公式: energy, route ✅")

    # 八卦
    assert trigram_from_lines(1, 1, 1) == 7
    assert compose_gua64(0, 2) == 2
    print("[13] 八卦: trigram, compose ✅")

    # 64卦
    assert gua64_name(0, 0) == "乾"
    assert gua64_audit("讼") == "🔴"
    print("[14] 64卦: name, audit ✅")

    # 天干地支
    assert year_to_ganzhi(1984) == "甲子"
    assert year_to_ganzhi(2026) == "丙午"
    print("[15] 天干地支: year_to_ganzhi ✅")

    # 三才向量
    v = sancai_vector((0.5, 0.3, 0.2))
    assert "magnitude" in v
    print("[16] 三才向量: sancai_vector ✅")

    print("\n" + "=" * 80)
    print("✅ DB3367 全部 16 组公式扩展自检通过")
    print(f"   DNA: #龍芯⚡️2026-07-05-LONGHUN-MATH-FORMULA-DB3367-EXTENSIONS-v1.0")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    selftest()
