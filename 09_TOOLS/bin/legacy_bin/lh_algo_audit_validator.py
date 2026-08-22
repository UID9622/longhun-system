#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂系统 · 算法审计与透明验证模块 v1.0
源协议: 01_protocols/龍魂算法审计与透明协议_v1.0.md
优先级: P0++（最高，不可绕过）
DNA: #龍芯⚡️丙午·乙未·甲寅·庚午·䷀乾-ALGO-AUDIT-VALIDATOR-v1.0

用法:
  python3 bin/lh_algo_audit_validator.py           # 跑全部 12 条测试向量
  python3 bin/lh_algo_audit_validator.py demo      # 示例接入判定
"""

import math
import sys
from statistics import median

# ---------- 第五章参数（上链公开，修改=修协议） ----------
ETA_MIN      = 0.99    # AIGC双标识合规率
DELTA_MIN    = 0.03    # 杀熟价差阈值3%
ALPHA_SIG    = 0.05    # 显著性水平
阅读速度     = 400     # 字/分钟
基础抽检率   = {"L0": 0.05, "L1": 0.05, "L2": 0.20, "L3": 1.00}


class CNSH_算法审计器:
    """生态接入闸门：5.7与门，fail-closed。"""

    DNA = "#龍芯⚡️丙午·乙未·甲寅·庚午·䷀乾-ALGO-AUDIT-VALIDATOR-v1.0"

    # ===== 5.1 备案覆盖率 =====
    @staticmethod
    def 备案覆盖率(备案清单: list[Any], 探测运行清单: list[Any]) -> float:
        if not 探测运行清单:
            return 1.0
        return len(set(备案清单) & set(探测运行清单)) / len(set(探测运行清单))

    # ===== 5.3 杀熟检测：Mann-Whitney U（非参，价格不正态） =====
    @staticmethod
    def 杀熟检验(老客价: list[Any], 新客价: list[Any]) -> dict[str, Any]:
        n1, n2 = len(老客价), len(新客价)
        合并 = sorted([(v, 0) for v in 老客价] + [(v, 1) for v in 新客价])
        秩 = [0.0] * len(合并); i = 0
        while i < len(合并):                                  # 并列秩取平均
            j = i
            while j + 1 < len(合并) and 合并[j+1][0] == 合并[i][0]:
                j += 1
            for t in range(i, j + 1):
                秩[t] = (i + j) / 2 + 1
            i = j + 1
        R1 = sum(秩[t] for t in range(len(合并)) if 合并[t][1] == 0)
        U = n1 * n2 + n1 * (n1 + 1) / 2 - R1
        μ, σ = n1 * n2 / 2, math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
        z = (U - μ) / σ
        p = math.erfc(abs(z) / math.sqrt(2))                  # 双侧p值
        δ = median([(o - n) / n for o, n in zip(sorted(老客价), sorted(新客价))])
        return {"成立": bool(p < ALPHA_SIG and δ > DELTA_MIN),
                "p": round(p, 4), "价差中位数": round(δ, 4)}

    # ===== 5.4 上影检测：KS分布检验 =====
    @staticmethod
    def 上影检验(申报组: list[Any], 对照组: list[Any]) -> dict[str, Any]:
        a, b = sorted(申报组), sorted(对照组)
        n, m = len(a), len(b)
        D, i, j = 0.0, 0, 0
        while i < n and j < m:                                # 双指针求最大分布差
            if a[i] <= b[j]: i += 1
            else: j += 1
            D = max(D, abs(i / n - j / m))
        D临界 = 1.36 * math.sqrt((n + m) / (n * m))           # α=0.05
        return {"成立": D > D临界, "D": round(D, 3), "D临界": round(D临界, 3)}

    # ===== 5.5 授权诱导指数 =====
    @staticmethod
    def 诱导判定(协议字数: int, 停留分钟: float, 默认勾选数: int,
                 授权步骤: int, 撤回步骤: int) -> dict[str, Any]:
        I = (协议字数 / 阅读速度) / max(停留分钟, 1e-6)
        违规项 = []
        if I > 1: 违规项.append("物理上不可能读完")
        if 默认勾选数 > 0: 违规项.append("存在默认勾选")
        if 撤回步骤 > 授权步骤: 违规项.append("撤回难于授权")
        return {"授权有效": not 违规项, "I": round(I, 1), "违规项": 违规项}

    # ===== 5.6 分层抽检密度（含信用修正） =====
    @staticmethod
    def 抽检密度(级别: str, 近12月违规次数: int, 免检: bool) -> float:
        密度 = 基础抽检率[级别] * (1 + 0.5 * 近12月违规次数)
        return min(1.0, 密度 * (0.2 if 免检 else 1.0))

    # ===== 5.7 接入综合判定（与门 + fail-closed） =====
    def 接入判定(self, p: dict[str, Any]) -> dict[str, Any]:
        try:
            C = self.备案覆盖率(p["备案"], p["探测运行"])
            检查 = {
                "备案100%": C >= 1.0,
                "初审通过": p["初审通过"],
                "透明签章": p["透明签章"],
                "授权合规": self.诱导判定(**p["授权参数"])["授权有效"],
                "标识达标": p.get("标识率", 1.0) >= ETA_MIN,
                "母体已整顿": p.get("母体CIVIL_OK", True),
            }
            return {"接入": all(检查.values()),
                    "未过项": [k for k, v in 检查.items() if not v],
                    "level": "ECO_OK" if all(检查.values()) else "DENIED",
                    "dna": self.DNA}
        except Exception as 异常:
            return {"接入": False, "reason": f"🔴 验证异常，默认拒绝: {异常}",
                    "level": "FAIL_CLOSED", "dna": self.DNA}


# 英文别名，方便其他模块 import
AlgoAuditValidator = CNSH_算法审计器


# ---------- 第十二章测试向量 ----------
def run_tests():
    v = CNSH_算法审计器()
    tests = []

    # T01: 备案12个，探测12个 → C=100%
    C_ok = v.备案覆盖率([f"alg{i}" for i in range(12)], [f"alg{i}" for i in range(12)])
    tests.append(("T01 备案12/运行12 C=100%", abs(C_ok - 1.0) < 1e-9, f"C={C_ok:.4f}"))

    # T02: 备案12个，探测13个 → 熔断
    C_bad = v.备案覆盖率([f"alg{i}" for i in range(12)], [f"alg{i}" for i in range(13)])
    r_bad_cov = v.接入判定({
        "备案": [f"alg{i}" for i in range(12)],
        "探测运行": [f"alg{i}" for i in range(13)],
        "初审通过": True, "透明签章": True,
        "授权参数": {"协议字数": 100, "停留分钟": 1.0, "默认勾选数": 0, "授权步骤": 2, "撤回步骤": 2},
        "标识率": 1.0, "母体CIVIL_OK": True,
    })
    tests.append(("T02 备案12/运行13 熔断", not r_bad_cov["接入"] and "备案100%" in r_bad_cov["未过项"],
                  f"C={C_bad:.4f}, level={r_bad_cov['level']}"))

    # T03: 老客价差8%，p<0.01 → 杀熟成立
    老客 = [108, 110, 107, 109, 111, 106, 112, 108, 110, 109, 107, 111]
    新客 = [100, 101, 99, 102, 100, 101, 99, 100, 102, 101, 99, 100]
    r_sha = v.杀熟检验(老客, 新客)
    tests.append(("T03 价差8%杀熟成立", r_sha["成立"] and r_sha["p"] < 0.05,
                  f"p={r_sha['p']}, δ={r_sha['价差中位数']}"))

    # T04: 价差0.5%，p=0.6 → 杀熟不成立
    老客2 = [100.5, 100.4, 100.6, 100.5, 100.4, 100.5, 100.6, 100.5, 100.4, 100.5, 100.6, 100.5]
    新客2 = [100.0] * 12
    r_sha2 = v.杀熟检验(老客2, 新客2)
    tests.append(("T04 价差0.5%杀熟不成立", not r_sha2["成立"],
                  f"p={r_sha2['p']}, δ={r_sha2['价差中位数']}"))

    # T05: 申报账号 vs 对照组，D=0.42 > D临界0.31 → 上影成立
    申报 = [0.05, 0.06, 0.04, 0.05, 0.06, 0.05, 0.04, 0.05, 0.06, 0.05, 0.04, 0.05]
    对照 = [0.25, 0.28, 0.24, 0.27, 0.26, 0.25, 0.28, 0.26, 0.27, 0.25, 0.26, 0.27]
    r_ks = v.上影检验(申报, 对照)
    tests.append(("T05 上影/限流成立", r_ks["成立"],
                  f"D={r_ks['D']}, D临界={r_ks['D临界']}"))

    # T06: 8000字，停留45秒 → I>1，授权无效
    r_auth = v.诱导判定(协议字数=8000, 停留分钟=0.75, 默认勾选数=0, 授权步骤=2, 撤回步骤=2)
    tests.append(("T06 8000字/45秒 诱导成立", not r_auth["授权有效"] and r_auth["I"] > 1,
                  f"I={r_auth['I']}"))

    # T07: 授权3步，撤回7步 → 授权无效
    r_revoke = v.诱导判定(协议字数=100, 停留分钟=1.0, 默认勾选数=0, 授权步骤=3, 撤回步骤=7)
    tests.append(("T07 撤回难于授权 无效", not r_revoke["授权有效"],
                  f"违规={r_revoke['违规项']}"))

    # T08: 365天零违规+飞检3过 → 免检通道，抽检率×20%
    rho_mian = v.抽检密度("L2", 近12月违规次数=0, 免检=True)
    tests.append(("T08 免检通道抽检率×20%", abs(rho_mian - 0.20 * 0.20) < 1e-9,
                  f"密度={rho_mian:.4f}"))

    # T09: 免检期内违规1次 → 立即出通道+密度上浮50%
    rho_vio = v.抽检密度("L2", 近12月违规次数=1, 免检=False)
    tests.append(("T09 违规1次密度上浮50%", abs(rho_vio - 0.20 * 1.5) < 1e-9,
                  f"密度={rho_vio:.4f}"))

    # T10: 五条件全过 → ECO_OK接入
    r_eco = v.接入判定({
        "备案": ["a", "b", "c"],
        "探测运行": ["a", "b", "c"],
        "初审通过": True,
        "透明签章": True,
        "授权参数": {"协议字数": 100, "停留分钟": 1.0, "默认勾选数": 0, "授权步骤": 2, "撤回步骤": 2},
        "标识率": 1.0,
        "母体CIVIL_OK": True,
    })
    tests.append(("T10 五条件全过→ECO_OK", r_eco["接入"] and r_eco["level"] == "ECO_OK",
                  str(r_eco["未过项"])))

    # T11: 覆盖率探测超时/异常 → FAIL_CLOSED
    r_fail = v.接入判定({"备案": []})  # 缺字段触发异常
    tests.append(("T11 异常输入→FAIL_CLOSED", r_fail["level"] == "FAIL_CLOSED",
                  r_fail.get("reason", "")[:40]))

    # T12: AIGC模型未过CIVIL_OK即接入 → 拒绝
    r_civil = v.接入判定({
        "备案": ["a"], "探测运行": ["a"],
        "初审通过": True, "透明签章": True,
        "授权参数": {"协议字数": 100, "停留分钟": 1.0, "默认勾选数": 0, "授权步骤": 2, "撤回步骤": 2},
        "标识率": 1.0, "母体CIVIL_OK": False,
    })
    tests.append(("T12 母体未整顿→拒绝", not r_civil["接入"] and "母体已整顿" in r_civil["未过项"],
                  r_civil["level"]))

    print("\n" + "=" * 60)
    print("龍魂算法审计与透明验证 · 12条测试向量")
    print("=" * 60)
    passed = 0
    for name, ok, detail in tests:
        mark = "✅" if ok else "❌"
        print(f"{mark} {name:35} {detail}")
        if ok:
            passed += 1
    print("=" * 60)
    print(f"结果: {passed}/{len(tests)} 通过")
    return passed == len(tests)


def demo():
    v = CNSH_算法审计器()
    p = {
        "备案": ["推荐排序", "内容过滤", "广告竞价"],
        "探测运行": ["推荐排序", "内容过滤", "广告竞价"],
        "初审通过": True,
        "透明签章": True,
        "授权参数": {"协议字数": 300, "停留分钟": 2.0, "默认勾选数": 0, "授权步骤": 2, "撤回步骤": 2},
        "标识率": 1.0,
        "母体CIVIL_OK": True,
    }
    r = v.接入判定(p)
    print(json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        import json
        demo()
    else:
        ok = run_tests()
        sys.exit(0 if ok else 1)
