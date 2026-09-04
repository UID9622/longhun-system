#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·戊申·戊午·䷬萃-MATH-EXPLORER-v2.0-落地-a1b2c3d4
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
"""
龍魂·数学难题解决工作流 — lh_math_explorer.py v2.0
落地自 Kimi Agent 整套解题输出，适配 longhun-system 路径。
Mode B 单脚本工具。严格按 SPEC.md 实现 Step 1-8。
seed=9622，结果完全可复现。

用法:
  python3 bin/lh_math_explorer.py                    # 默认 N=10^6 全流程
  python3 bin/lh_math_explorer.py --n 100000          # 指定 N
  python3 bin/lh_math_explorer.py --benchmark-only     # 仅性能基准
  python3 bin/lh_math_explorer.py --json              # JSON 结构化输出
"""

import sys
import os
import time
import random
import tracemalloc
import json
import argparse
from datetime import date
from pathlib import Path

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False

SEED = 9622
N_DEFAULT = 10 ** 6
BENCH_NS = [10 ** 4, 10 ** 5, 10 ** 6]
ROOTS6 = [1, 2, 4, 5, 7, 8]
CHI2_CRIT = 11.070  # df=5, α=0.05

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
ROOT_CARD_PATH = REPORTS_DIR / "ROOT_CARD_math_solve.txt"

FALLBACK_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
    71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
    151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
]

# ───────────────────────────────────── 核心函数 ─────────────────────────────────────

def digital_root(n: int) -> int:
    """dr(n) = n - 9 * ((n - 1) // 9)"""
    if n <= 0:
        raise ValueError("digital_root 仅定义于正整数")
    return n - 9 * ((n - 1) // 9)


def sieve(limit: int) -> list:
    """埃氏筛，返回 limit 以内全部素数。异常由调用方捕获并回退。"""
    if not isinstance(limit, int) or limit < 0:
        raise ValueError(f"非法筛法上限: {limit!r}")
    if limit < 2:
        return []
    bs = bytearray(b"\x01") * (limit + 1)
    bs[0] = bs[1] = 0
    for i in range(2, int(limit ** 0.5) + 1):
        if bs[i]:
            bs[i * i::i] = b"\x00" * (((limit - i * i) // i) + 1)
    return [i for i in range(2, limit + 1) if bs[i]]


def wuxing(dr: int) -> str:
    """河图映射: 1,6→水; 2,7→火; 3,8→木; 4,9→金; 5→土"""
    return {1: "水", 6: "水", 2: "火", 7: "火", 3: "木", 8: "木",
            4: "金", 9: "金", 5: "土"}[dr]


def transition_matrix(dr_seq):
    """6x6 转移矩阵（索引 [1,2,4,5,7,8]），M[i][j]=count(i→j)/count(i)，行归一化。"""
    idx = {r: k for k, r in enumerate(ROOTS6)}
    M = [[0.0] * 6 for _ in range(6)]
    rows = [0] * 6
    for a, b in zip(dr_seq, dr_seq[1:]):
        if a in idx and b in idx:
            M[idx[a]][idx[b]] += 1.0
            rows[idx[a]] += 1
    for i in range(6):
        if rows[i]:
            M[i] = [v / rows[i] for v in M[i]]
    if HAS_NUMPY:
        return np.array(M)
    return M


def _power_iteration_stationary(M, iters=10000, tol=1e-15):
    """纯 Python 幂迭代求平稳分布（numpy 不可用时的回退）。"""
    v = [1.0 / 6] * 6
    for _ in range(iters):
        nv = [sum(v[i] * M[i][j] for i in range(6)) for j in range(6)]
        s = sum(nv)
        nv = [x / s for x in nv]
        if max(abs(nv[i] - v[i]) for i in range(6)) < tol:
            v = nv
            break
        v = nv
    return 1.0, v


def eigen_analysis(M):
    """返回 (特征值列表, 主特征值, 主特征向量/平稳分布)。"""
    if HAS_NUMPY:
        vals, vecs = np.linalg.eig(np.array(M).T)
        k = int(np.argmax(np.real(vals)))
        stationary = np.real(vecs[:, k])
        stationary = stationary / stationary.sum()
        return list(np.real(vals)), float(np.real(vals[k])), list(stationary)
    lam, v = _power_iteration_stationary(M)
    return [lam], lam, v


def chi_square(freq: dict) -> float:
    """H0: {1,2,4,5,7,8} 均匀 1/6。freq 为六类实际计数。"""
    total = sum(freq[r] for r in ROOTS6)
    expected = total / 6.0
    return sum((freq[r] - expected) ** 2 / expected for r in ROOTS6)


def goldbach_weak_check(n: int, prime_set, primes):
    """弱哥德巴赫优化路径：奇数 n>5，n-3 为偶数 ≥4，分解 n-3=p+q → n=3+p+q。"""
    if n % 2 == 0 or n <= 5:
        raise ValueError("仅处理奇数 n>5")
    m = n - 3
    for p in primes:
        if p > m - 2:
            break
        if (m - p) in prime_set:
            return (3, p, m - p)
    return None


# ───────────────────────────────────── 干支四柱 ─────────────────────────────────────

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"

TERM_C21 = {
    "小寒": 6.11, "立春": 3.87, "惊蛰": 5.63, "清明": 4.81,
    "立夏": 5.52, "芒种": 5.678, "小暑": 7.108, "立秋": 7.5,
    "白露": 7.646, "寒露": 8.318, "立冬": 7.438, "大雪": 7.18,
}
TERM_MONTH = {"小寒": 1, "立春": 2, "惊蛰": 3, "清明": 4, "立夏": 5,
              "芒种": 6, "小暑": 7, "立秋": 8, "白露": 9, "寒露": 10,
              "立冬": 11, "大雪": 12}
TERM_BRANCH = {"小寒": "丑", "立春": "寅", "惊蛰": "卯", "清明": "辰",
               "立夏": "巳", "芒种": "午", "小暑": "未", "立秋": "申",
               "白露": "酉", "寒露": "戌", "立冬": "亥", "大雪": "子"}

HEXAGRAMS = [
    "乾为天", "坤为地", "水雷屯", "山水蒙", "水天需", "天水讼", "地水师", "水地比",
    "风天小畜", "天泽履", "地天泰", "天地否", "天火同人", "火天大有", "地山谦", "雷地豫",
    "泽雷随", "山风蛊", "地泽临", "风地观", "火雷噬嗑", "山火贲", "山地剥", "地雷复",
    "天雷无妄", "山天大畜", "山雷颐", "泽风大过", "坎为水", "离为火", "泽山咸", "雷风恒",
    "天山遁", "雷天大壮", "火地晋", "地火明夷", "风火家人", "火泽睽", "水山蹇", "雷水解",
    "山泽损", "风雷益", "泽天夬", "天风姤", "泽地萃", "地风升", "泽水困", "水风井",
    "泽火革", "火风鼎", "震为雷", "艮为山", "风山渐", "雷泽归妹", "雷火丰", "火山旅",
    "巽为风", "兑为泽", "风水涣", "水泽节", "风泽中孚", "雷山小过", "水火既济", "火水未济",
]


def solar_term_day(year: int, term: str) -> int:
    """21 世纪节气日天文近似（通用公式，误差≤1天）。"""
    if not (2000 <= year <= 2099):
        raise ValueError("节气近似仅支持 2000-2099")
    Y = year % 100
    C = TERM_C21[term]
    m = TERM_MONTH[term]
    L = (Y - 1) // 4 if m in (1, 2) else Y // 4
    return int(Y * 0.2422 + C) - L


def ganzhi(year, month, day) -> dict:
    """干支四柱（年/月/日柱）算法生成，禁止手写。基准日 1900-01-01 = 甲戌。"""
    delta = (date(year, month, day) - date(1900, 1, 1)).days
    day_idx = (10 + delta) % 60
    day_gz = STEMS[day_idx % 10] + BRANCHES[day_idx % 12]

    year_idx = (36 + (year - 1900)) % 60
    year_gz = STEMS[year_idx % 10] + BRANCHES[year_idx % 12]

    d = date(year, month, day)
    candidates = []
    for term, m in TERM_MONTH.items():
        td = date(year, m, solar_term_day(year, term))
        candidates.append((td, TERM_BRANCH[term]))
    candidates.append((date(year - 1, 12, solar_term_day(year - 1, "大雪")), "子"))
    candidates.append((date(year - 1, 1, solar_term_day(year - 1, "小寒")), "丑"))
    candidates.sort()
    month_branch = None
    for td, br in candidates:
        if td <= d:
            month_branch = br
        else:
            break
    if month_branch is None:
        month_branch = "子"
    year_stem_idx = year_idx % 10
    first_month_stem = ((year_stem_idx % 5) * 2 + 2) % 10
    offset = (BRANCHES.index(month_branch) - 2) % 12
    month_stem = STEMS[(first_month_stem + offset) % 10]
    month_gz = month_stem + month_branch

    return {"year_gz": year_gz, "month_gz": month_gz, "day_gz": day_gz,
            "day_idx": day_idx, "year_idx": year_idx,
            "month_branch": month_branch, "delta_days": delta}


def hexagram(day_gz_index: int) -> str:
    """卦名 = 文王六十四卦序[日柱干支序号 % 64]（0 基索引）。"""
    return HEXAGRAMS[day_gz_index % 64]


def dna_code(gz: dict) -> str:
    return (f"#龍芯⚡️{gz['year_gz']}·{gz['month_gz']}·{gz['day_gz']}·"
            f"{hexagram(gz['day_idx'])}-MATH-SOLVE-v2.0")


# ───────────────────────────────────── Step 流程 ─────────────────────────────────────

def step1_sieve(N, quiet=False):
    if not quiet:
        print(f"\n=== Step 1 数据生成: sieve({N}) ===")
    try:
        primes = sieve(N)
        if not quiet:
            print(f"筛法正常完成，素数个数 = {len(primes)}")
        fallback = False
    except Exception as e:
        primes = [p for p in FALLBACK_PRIMES if p <= N]
        print(f"🟡 告警: 筛法失败({e})，回退内置素数表，共 {len(primes)} 个")
        fallback = True
    return primes, fallback


def step2_digital_root(primes, quiet=False):
    if not quiet:
        print("\n=== Step 2 数字根变换 ===")
    dr_seq = [digital_root(p) for p in primes]
    special = [p for p in primes if digital_root(p) in (3, 6, 9)]
    assert special == [3], f"断言失败: dr∈{{3,6,9}} 出现于 {special}"
    if not quiet:
        print("断言通过: dr∈{3,6,9} 仅出现在素数 3 本身 (dr=3；{6,9} 无素数)")
    return dr_seq


def step3_freq(dr_seq, primes, quiet=False):
    if not quiet:
        print("\n=== Step 3 频率统计 + 五行分布 ===")
    freq = {r: 0 for r in ROOTS6}
    for p in primes:
        if p == 3:
            continue
        freq[digital_root(p)] += 1
    total = sum(freq.values())
    if not quiet:
        for r in ROOTS6:
            print(f"  dr={r} ({wuxing(r)}): count={freq[r]}, freq={freq[r]/total:.6f}")
        print(f"  合计(排除素数3) = {total}")
        wx_count = {}
        for r in ROOTS6:
            wx_count[wuxing(r)] = wx_count.get(wuxing(r), 0) + freq[r]
        print("  五行分布: " + ", ".join(f"{k}={v}" for k, v in wx_count.items()))
    return freq


def step4_flow(dr_seq, quiet=False):
    if not quiet:
        print("\n=== Step 4 流场构建: 6x6 转移矩阵 ===")
    M = transition_matrix(dr_seq)
    Ml = M.tolist() if HAS_NUMPY else M
    if not quiet:
        print("  行序 [1,2,4,5,7,8]，行归一化矩阵 M:")
        for i, row in enumerate(Ml):
            print("   " + " ".join(f"{v:.6f}" for v in row) + f"   # dr={ROOTS6[i]}")
    vals, lam, stat = eigen_analysis(M)
    if not quiet:
        print(f"  特征值(实部): {['%.6f' % v for v in sorted(vals, reverse=True)]}")
        print(f"  主特征值 λ1 = {lam:.6f}")
        print("  平稳分布 π = " + str([f"{v:.6f}" for v in stat]) + " (对应 [1,2,4,5,7,8])")
    return M, vals, lam, stat


def step5_chi2(freq, quiet=False):
    if not quiet:
        print("\n=== Step 5 卡方检验 ===")
    chi2 = chi_square(freq)
    verdict = "接受 H0（均匀）" if chi2 < CHI2_CRIT else "拒绝 H0（非均匀）"
    if not quiet:
        print(f"  χ² = {chi2:.6f}, df=5, α=0.05, 临界值 = {CHI2_CRIT} → {verdict}")
    return chi2, verdict


def step6_goldbach(N, primes, quiet=False):
    if not quiet:
        print(f"\n=== Step 6 弱哥德巴赫验证: 奇数 n=7..{N} (步长2) ===")
    prime_set = set(primes)
    fails = 0
    max_verified = 0
    first_example = None
    for n in range(7, N + 1, 2):
        res = goldbach_weak_check(n, prime_set, primes)
        if res is None:
            fails += 1
        else:
            max_verified = n
            if first_example is None:
                first_example = (n, res)
    n_checked = len(range(7, N + 1, 2))
    if not quiet:
        print(f"  检查奇数个数 = {n_checked}, 失败数 = {fails}, 最大验证 n = {max_verified}")
        if first_example:
            n_val, (a, b, c) = first_example
            print(f"  示例: {n_val} = {a} + {b} + {c}")
    return fails, max_verified, n_checked


def step7_audit(primes, freq, quiet=False):
    if not quiet:
        print("\n=== Step 7 数学根审计 + 三色审计 ===")
    sum_p = sum(primes)
    dr_sum = digital_root(sum_p)
    dr_seq_sum = sum(digital_root(p) for p in primes)
    weighted = sum(freq[r] * r for r in ROOTS6) + 3
    audits = []
    a1 = dr_sum == digital_root(dr_seq_sum)
    audits.append((a1, f"dr(Σp)={dr_sum} 与 dr(Σdr(p))={digital_root(dr_seq_sum)} 一致性"))
    a2 = dr_sum == digital_root(weighted)
    audits.append((a2, f"dr(Σp)={dr_sum} 与 dr(加权数字根和)={digital_root(weighted)} 一致性"))
    a3 = dr_sum in range(1, 10)
    audits.append((a3, f"审计根值 dr={dr_sum} ∈ [1,9] 合法性"))
    if not quiet:
        for ok, msg in audits:
            print(f"  {'🟢' if ok else '🔴'} {msg}: {'PASS' if ok else 'FAIL'}")
        tri = "🟢" if all(a[0] for a in audits) else "🔴"
        print(f"  Σp = {sum_p}, 审计根值 dr(Σp) = {dr_sum}, 五行 = {wuxing(dr_sum)}, TriColor = {tri}")
    tri = "🟢" if all(a[0] for a in audits) else "🔴"
    return dr_sum, tri, audits, sum_p


def step8_root_card(dr_val, tri, gz, output_path=None, quiet=False):
    if not quiet:
        print("\n=== Step 8 ROOT_CARD ===")
    dna = dna_code(gz)
    card = f"""Root: dr={dr_val}
Wuxing: {wuxing(dr_val)}
TriColor: {tri}
DataLevel: L0_PUBLIC
PrivacyMode: normal
Retention: summary_only
TraceMode: chain
Route: [MATH-SOLVE-EXAMPLE]
Backend: python / jupyter / notion
Action: archive
DNA: {dna}
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F"""
    if not quiet:
        print(card)
    path = Path(output_path) if output_path else ROOT_CARD_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(card + "\n")
    if not quiet:
        print(f"  已写入 {path}")
    else:
        print(f"  已写入 {path}", file=sys.stderr)
    return card, dna, str(path)


def benchmark(quiet=False):
    if not quiet:
        print("\n=== 性能基准 (time + tracemalloc 峰值内存) ===")
        print(f"  {'N':>10} | {'筛法耗时s':>10} | {'筛法峰值B':>12} | {'哥德巴赫耗时s':>10} | {'哥德巴赫峰值B':>14}")
    results = {}
    for N in BENCH_NS:
        tracemalloc.start()
        t0 = time.perf_counter()
        primes = sieve(N)
        t1 = time.perf_counter()
        _, peak_sieve = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        prime_set = set(primes)
        tracemalloc.start()
        t2 = time.perf_counter()
        for n in range(7, N + 1, 2):
            goldbach_weak_check(n, prime_set, primes)
        t3 = time.perf_counter()
        _, peak_gb = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        results[N] = {"sieve_time": t1 - t0, "sieve_mem": peak_sieve,
                       "goldbach_time": t3 - t2, "goldbach_mem": peak_gb}
        if not quiet:
            print(f"  {N:>10} | {t1-t0:>10.4f} | {peak_sieve:>12} | {t3-t2:>10.4f} | {peak_gb:>14}")
    return results


# ───────────────────────────────────── 主流程 ─────────────────────────────────────

def run_full(N=N_DEFAULT, quiet=False, output_path=None):
    """执行完整 Step 1-8 + 性能基准，返回结构化结果。"""
    random.seed(SEED)
    if HAS_NUMPY:
        np.random.seed(SEED)

    run_date = date.today()
    if not quiet:
        print("龍魂·数学难题解决工作流 lh_math_explorer.py v2.0")
        print(f"seed={SEED}, 运行日期={run_date.isoformat()}, "
              f"numpy={'可用 ' + np.__version__ if HAS_NUMPY else '不可用(幂迭代回退)'}, N={N}")

    t_start = time.perf_counter()

    primes, fallback = step1_sieve(N, quiet)
    dr_seq = step2_digital_root(primes, quiet)
    freq = step3_freq(dr_seq, primes, quiet)
    M, vals, lam, stat = step4_flow(dr_seq, quiet)
    chi2, verdict = step5_chi2(freq, quiet)
    fails, max_n, n_checked = step6_goldbach(N, primes, quiet)
    dr_val, tri, audits, sum_p = step7_audit(primes, freq, quiet)

    gz = ganzhi(run_date.year, run_date.month, run_date.day)
    if not quiet:
        print("\n=== DNA 干支四柱（算法生成）===")
        print(f"  年柱={gz['year_gz']}(序号{gz['year_idx']}), 月柱={gz['month_gz']}"
              f"(节气近似定月支={gz['month_branch']}), 日柱={gz['day_gz']}"
              f"(序号{gz['day_idx']}, 距基准日{gz['delta_days']}天)")
        print(f"  卦名 = 文王序[{gz['day_idx']} % 64 = {gz['day_idx'] % 64}] = {hexagram(gz['day_idx'])}")
        print(f"  DNA = {dna_code(gz)}")

    card, dna, card_path = step8_root_card(dr_val, tri, gz, output_path, quiet)
    bench = benchmark(quiet)

    elapsed = time.perf_counter() - t_start
    if not quiet:
        print(f"\n主流程总耗时 = {elapsed:.4f}s")
        print("运行完成。")

    return {
        "seed": SEED,
        "run_date": run_date.isoformat(),
        "n": N,
        "numpy_available": HAS_NUMPY,
        "primes_count": len(primes),
        "fallback_used": fallback,
        "dr_assertion_passed": True,
        "freq": {str(k): v for k, v in freq.items()},
        "wuxing_distribution": {
            k: sum(freq[r] for r in ROOTS6 if wuxing(r) == k)
            for k in ["水", "火", "木", "金", "土"]
        },
        "eigenvalues": [round(float(v), 6) for v in sorted(vals, reverse=True)],
        "principal_eigenvalue": round(float(lam), 6),
        "stationary_distribution": [round(float(v), 6) for v in stat],
        "chi_square": round(chi2, 6),
        "chi_verdict": verdict,
        "goldbach_fails": fails,
        "goldbach_max_verified": max_n,
        "goldbach_total_checked": n_checked,
        "sum_primes": sum_p,
        "audit_root": dr_val,
        "audit_wuxing": wuxing(dr_val),
        "audit_tricolor": tri,
        "audit_details": [{"pass": ok, "msg": msg} for ok, msg in audits],
        "ganzhi": {
            "year": gz["year_gz"],
            "month": gz["month_gz"],
            "day": gz["day_gz"],
            "calendar": gz["month_branch"],
            "day_index": gz["day_idx"],
        },
        "hexagram": hexagram(gz["day_idx"]),
        "dna": dna_code(gz),
        "root_card_path": card_path,
        "benchmark": {str(k): {
            "sieve_time_s": round(v["sieve_time"], 4),
            "sieve_mem_b": v["sieve_mem"],
            "goldbach_time_s": round(v["goldbach_time"], 4),
            "goldbach_mem_b": v["goldbach_mem"],
        } for k, v in bench.items()},
        "total_time_s": round(elapsed, 4),
    }


# ───────────────────────────────────── CLI ─────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="龍魂·数学难题解决工作流 v2.0 — Step 1-8 全流程 + 性能基准",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_math_explorer.py                          # 默认 N=10^6 全流程
  python3 bin/lh_math_explorer.py --n 100000                # 指定素数上限
  python3 bin/lh_math_explorer.py --benchmark-only           # 仅跑性能基准
  python3 bin/lh_math_explorer.py --json                     # JSON 结构化输出
  python3 bin/lh_math_explorer.py --output reports/my_card.txt  # 自定义输出路径
        """)
    parser.add_argument("--n", type=int, default=N_DEFAULT,
                        help=f"素数筛上限（默认 {N_DEFAULT}）")
    parser.add_argument("--benchmark-only", action="store_true",
                        help="仅跑三档性能基准（跳过 Step 1-8）")
    parser.add_argument("--json", action="store_true",
                        help="结构化 JSON 输出")
    parser.add_argument("--quiet", action="store_true",
                        help="精简输出")
    parser.add_argument("--output", type=str, default=None,
                        help="ROOT_CARD 输出路径（默认 reports/ROOT_CARD_math_solve.txt）")
    args = parser.parse_args()

    if args.benchmark_only:
        print("=== 性能基准（仅 benchmark）===")
        bench = benchmark(quiet=args.quiet)
        if args.json:
            print(json.dumps({str(k): v for k, v in bench.items()},
                             ensure_ascii=False, indent=2))
        return 0

    result = run_full(N=args.n, quiet=args.quiet or args.json, output_path=args.output)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    # 三色审计最终判定
    if result["audit_tricolor"] == "🔴":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
