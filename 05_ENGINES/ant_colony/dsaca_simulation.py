# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · DSACA 蚁群架构仿真实验 v1.1
DNA: #龍芯⚡️丙午·丙申·庚申·辛巳·䷡大壮-DSACA-SIM-v1.1-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）· 工程层 MulanPSL v2
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

按论文《龍魂分布式认知架构 v1.1》§9 代码原样实现 + §10 三组仿真实验：
  - 实验1: 定理5 鲁棒性验证（蒙特卡洛故障注入）
  - 实验2: 涌现质量动态演化（冷启动→稳态→压力→恢复）
  - 实验3: 信息素安全机制（伪造/重放/篡改/TTL）
零外部依赖，纯 Python 标准库。用法:
  python3 dsaca_simulation.py [--rounds 10000] [--modules 103]
"""
import json
import hashlib
import hmac
import time
import uuid
import math
import random
import argparse
from dataclasses import dataclass, field
from typing import Dict, Optional, List, Tuple
from enum import Enum


class PheromoneType(Enum):
    RECRUIT = "recruit"   # 招募素
    ALERT = "alert"       # 警戒素
    TRAIL = "trail"       # 足迹素
    GATHER = "gather"     # 聚集素
    META = "meta"         # 元信息素


LAMBDA = {
    PheromoneType.RECRUIT: 0.10,
    PheromoneType.ALERT: 0.05,
    PheromoneType.TRAIL: 0.01,
    PheromoneType.GATHER: 0.02,
    PheromoneType.META: 0.005,
}

PRIORITY = {
    PheromoneType.ALERT: 100,
    PheromoneType.GATHER: 80,
    PheromoneType.RECRUIT: 60,
    PheromoneType.TRAIL: 40,
    PheromoneType.META: 90,
}


@dataclass
class Pheromone:
    ptype: PheromoneType
    source: str
    target: str
    priority: int
    payload: Dict
    timestamp: float
    dna: str
    ttl: int
    nonce: str
    hmac: str = ""

    def to_dict(self) -> Dict:
        return {
            "type": self.ptype.value, "source": self.source, "target": self.target,
            "priority": self.priority, "payload": self.payload,
            "timestamp": self.timestamp, "dna": self.dna, "ttl": self.ttl,
            "nonce": self.nonce, "hmac": self.hmac,
        }

    @classmethod
    def create(cls, ptype, source, target, payload, dna, secret_key, ttl=300):
        nonce = str(uuid.uuid4())
        ts = time.time()
        p = cls(ptype, source, target, PRIORITY[ptype], payload, ts, dna, ttl, nonce)
        p.hmac = p._sign(secret_key)
        return p

    def _sign(self, key: bytes) -> str:
        msg = f"{self.ptype.value}|{self.source}|{self.timestamp}|{self.nonce}|{json.dumps(self.payload, sort_keys=True)}"
        try:
            # 标准 HMAC-SM3 构造（带密钥）: SM3(opad||SM3(ipad||msg))
            from gmssl import sm3 as _sm3mod
            block = 64
            k = key if len(key) <= block else _sm3mod.sm3_hash(bytearray(key))
            k = bytes(k) + b"\x00" * (block - len(k))
            ipad = bytes(b ^ 0x36 for b in k)
            opad = bytes(b ^ 0x5C for b in k)
            inner = _sm3mod.sm3_hash(bytearray(ipad + msg.encode()))
            outer = _sm3mod.sm3_hash(bytearray(opad + inner.encode()))
            return outer[:32]
        except (ImportError, TypeError, AttributeError):
            # fallback: 标准 HMAC-SHA256（密钥参与）
            return hmac.new(key, msg.encode(), hashlib.sha256).hexdigest()[:32]

    def verify(self, key: bytes) -> bool:
        if time.time() - self.timestamp > self.ttl:
            return False
        expected = self._sign(key)
        if not hmac.compare_digest(self.hmac, expected):
            return False
        return True

    def concentration(self, now: Optional[float] = None) -> float:
        t = now or time.time()
        elapsed = max(t - self.timestamp, 0.0)
        return self.priority * (2.718 ** (-LAMBDA[self.ptype] * elapsed))


class PheromoneField:
    def __init__(self, secret_key: bytes):
        self.signals: Dict[str, Pheromone] = {}
        self.seen_nonces: set = set()
        self.key = secret_key

    def emit(self, p: Pheromone) -> bool:
        if p.nonce in self.seen_nonces:
            return False
        if not p.verify(self.key):
            return False
        self.signals[p.nonce] = p
        self.seen_nonces.add(p.nonce)
        return True

    def sense(self, module_id: str, ptype=None, threshold: float = 1.0) -> list:
        now = time.time()
        results = []
        for nonce, p in list(self.signals.items()):
            if now - p.timestamp > p.ttl:
                del self.signals[nonce]
                continue
            if p.target not in (module_id, "broadcast", p.ptype.value + "_group"):
                continue
            if ptype and p.ptype != ptype:
                continue
            conc = p.concentration(now)
            if conc > threshold:
                results.append((conc, p))
        results.sort(key=lambda x: -x[0])
        return results

    def evaporate(self):
        now = time.time()
        expired = [n for n, p in self.signals.items() if now - p.timestamp > p.ttl]
        for n in expired:
            del self.signals[n]


def compute_emergence(modules: list, signals: list, audit_scores: list) -> dict:
    """论文 §9.2 涌现质量计算，原样实现"""
    n = len(modules)
    if n == 0:
        return {"E": 0.0, "D": 0.0, "I": 0.0, "C": 0.0, "V": 0.0}

    counts = [0] * 8
    for m in modules:
        counts[m.get("func_dim", 0)] += 1
    entropy = -sum((c / n) * math.log2(c / n) for c in counts if c > 0)
    D = entropy / math.log2(8)

    I = min(len(signals) / (n * 10), 1.0)

    if signals:
        avg_conc = sum(s.concentration() for s in signals) / len(signals)
        C = min(avg_conc / 50.0, 1.0)
    else:
        C = 0.0

    V = sum(audit_scores) / len(audit_scores) / 100.0 if audit_scores else 1.0

    alpha = beta = gamma = delta = 0.25
    E = alpha * D + beta * I + gamma * C + delta * V

    return {"E": round(E, 4), "D": round(D, 4), "I": round(I, 4),
            "C": round(C, 4), "V": round(V, 4),
            "status": "🟢" if E >= 0.85 else "🟡" if E >= 0.60 else "🔴"}


# ============ 仿真环境 ============

# 附录A映射: 八维功能空间分布（数据采集/计算处理/存储管理/输出渲染/
#            防护审计/感知预警/知识沉淀/成长迭代）
FUNC_DIMS = [25, 20, 10, 7, 10, 7, 12, 11]  # 合计102，+1元知=103

# 种群划分: {种群: (func_dim 列表)}
POPULATION_DIMS = {
    "工蚁群":   [0, 1, 2, 3],   # 采集/计算/存储/渲染
    "兵蚁群":   [4],            # 防护审计
    "侦察蚁群": [5],            # 感知预警
    "储蜜蚁群": [6],            # 知识沉淀
    "育幼蚁群": [7],            # 成长迭代
}


def build_modules(n: int = 103) -> List[Dict]:
    """按附录A构建模块（func_dim 0-7，含种群归属）"""
    modules = []
    dims = FUNC_DIMS[:]
    # 补足到 n（多余全塞给 func_dim 0）
    while sum(dims) < n:
        dims[0] += 1
    for dim, cnt in enumerate(dims):
        for _ in range(cnt):
            modules.append({
                "id": f"m{len(modules)}",
                "func_dim": dim,
                "population": next(p for p, ds in POPULATION_DIMS.items() if dim in ds),
            })
    return modules[:n]


def build_signals(modules: List[Dict], n_signals: Optional[int] = None,
                  key: bytes = b"sim-secret", dna: str = "DNA-SIM",
                  signed: bool = False) -> List[Pheromone]:
    """生成一批信息素（按模块数比例，目标匹配 broadcast）
    signed=True 时走 HMAC 签名（安全测试用）；仿真默认免签提升速度"""
    n = n_signals if n_signals is not None else len(modules) * 8
    signals = []
    ptypes = [PheromoneType.RECRUIT, PheromoneType.ALERT,
              PheromoneType.TRAIL, PheromoneType.GATHER, PheromoneType.META]
    for i in range(n):
        src = random.choice(modules)
        pt = random.choice(ptypes)
        if signed:
            p = Pheromone.create(pt, src["id"], "broadcast",
                                 {"task": f"t{i}"}, dna, key, ttl=300)
            # 仿真：人为控制时间戳在0~30秒前（模拟新鲜信号），保证浓度有意义
            p.timestamp = time.time() - random.uniform(0, 30)
            p.hmac = p._sign(key)  # 重新签名（时间戳变了）
        else:
            # 快速路径：免签名的轻量信号（仅仿真指标计算用）
            p = Pheromone(pt, src["id"], "broadcast", PRIORITY[pt],
                          {"task": f"t{i}"},
                          time.time() - random.uniform(0, 30), dna, 300,
                          str(uuid.uuid4()))
        signals.append(p)
    return signals


def run_fault_simulation(rounds: int = 10000, modules_n: int = 103) -> dict:
    """实验1: 定理5 鲁棒性验证（蒙特卡洛故障注入）

    负载模型（按论文附录C定理5证明口径）:
      - C_total = 全系统容量（模块数）; L_total = 0.8·C_total（额定负载）
      - 失效后 C_remain = 存活模块数; 负载率 ρ = L_total / C_remain
      - 吞吐 = min(1, 1/ρ): ρ>1 时任务排队/降级，信号产出同步衰减
      - 失效模块的信号随之消失（孤儿信号），平均信号龄随负载上升
    两种注入口径:
      - per_pop（论文字面）: 随机选一个种群，失效该种群 p% 模块
      - global（附录C证明口径）: 全系统随机失效 p% 模块（更严苛）
    """
    random.seed(42)
    key = b"sim-secret"
    dna = "#龍芯⚡️SIM"
    rates = list(range(0, 75, 5))  # 0,5,...,70
    per_rate = max(rounds // len(rates) // 2, 100)

    results = {"per_pop": {}, "global": {}}
    total_loops = len(rates) * per_rate
    loop_idx = 0
    for mode in ("per_pop", "global"):
        for rate in rates:
            es = []
            for _ in range(per_rate):
                loop_idx += 1
                if loop_idx % 200 == 0:
                    print(f"  …进度 {mode} {loop_idx}/{total_loops} 轮", flush=True)
                original = build_modules(modules_n)
                C_total = float(len(original))
                L_total = 0.8 * C_total

                if mode == "per_pop":
                    pop = random.choice(list(POPULATION_DIMS.keys()))
                    pop_mods = [m for m in original if m["population"] == pop]
                    n_fail = int(len(pop_mods) * rate / 100.0)
                    failed = set(random.sample([m["id"] for m in pop_mods], n_fail))
                else:
                    n_fail = int(len(original) * rate / 100.0)
                    failed = set(random.sample([m["id"] for m in original], n_fail))

                all_modules = [m for m in original if m["id"] not in failed]
                C_remain = float(len(all_modules))
                rho = L_total / C_remain if C_remain > 0 else float("inf")
                throughput = min(1.0, 1.0 / rho) if rho > 0 else 0.0

                # 信号: 存活模块按吞吐产出（失效模块的信号已消失）
                n_sig = int(8 * len(all_modules) * throughput)
                signals = build_signals(all_modules, n_signals=n_sig, key=key, dna=dna)
                audit = [random.uniform(88, 99) for _ in all_modules]
                r = compute_emergence(all_modules, signals, audit)
                es.append(r["E"])
            avg = sum(es) / len(es)
            std = math.sqrt(sum((e - avg) ** 2 for e in es) / len(es))
            mn = min(es)
            results[mode][rate] = {"avg": round(avg, 4), "std": round(std, 4),
                                   "min": round(mn, 4),
                                   "status": "🟢" if avg >= 0.85 else "🟡" if avg >= 0.60 else "🔴"}
    return results


def run_dynamic_evolution(modules_n: int = 103) -> dict:
    """实验2: 涌现质量动态演化（冷启动→稳态→压力→恢复）"""
    random.seed(7)
    key = b"sim-secret"
    dna = "#龍芯⚡️SIM"
    phases = [
        ("0-30s 冷启动",  30, 1.0, 0.35),   # 任务量系数, 起始E
        ("30-60s 稳态",   30, 1.0, None),
        ("60-90s 压力",   30, 2.0, None),
        ("90-120s 恢复",  30, 1.0, None),
    ]
    report = []
    modules = build_modules(modules_n)
    field = PheromoneField(key)
    emitted = 0
    e_prev = 0.35

    for name, dur, load_factor, start_e in phases:
        e_samples = []
        for _ in range(dur):
            # 任务流: 每次时间步产生 load_factor * 20 条招募素
            for _ in range(int(load_factor * 20)):
                src = random.choice(modules)
                p = Pheromone.create(PheromoneType.RECRUIT, src["id"], "broadcast",
                                     {"task": f"t{emitted}"}, dna, key)
                p.timestamp = time.time() - random.uniform(0, 5)
                p.hmac = p._sign(key)
                field.emit(p)
                emitted += 1
            field.evaporate()
            sigs = list(field.signals.values())
            audit = [random.uniform(88, 99) for _ in modules]
            r = compute_emergence(modules, sigs, audit)
            e_samples.append(r["E"])
        avg = sum(e_samples) / len(e_samples)
        e_prev = avg
        report.append({"phase": name, "E": round(avg, 4),
                       "signals": len(field.signals)})
    return report


def _legacy_unkeyed_sm3(p: Pheromone) -> str:
    """论文v1.1原版 _sign 的 SM3 路径（gmssl可用时）——无密钥，实测可被伪造穿透"""
    from gmssl import sm3
    msg = f"{p.ptype.value}|{p.source}|{p.timestamp}|{p.nonce}|{json.dumps(p.payload, sort_keys=True)}"
    return sm3.sm3_hash(bytearray(msg.encode()))[:32]


class LegacyField:
    """论文v1.1原版信息素场：签名+验证均用无密钥SM3（还原原始漏洞场景）"""

    def __init__(self):
        self.signals: Dict[str, Pheromone] = {}
        self.seen_nonces: set = set()

    def emit(self, p: Pheromone) -> bool:
        if p.nonce in self.seen_nonces:
            return False
        if time.time() - p.timestamp > p.ttl:
            return False
        # 原版验证: 无密钥SM3重算对比（密钥形同虚设）
        if not hmac.compare_digest(p.hmac, _legacy_unkeyed_sm3(p)):
            return False
        self.signals[p.nonce] = p
        self.seen_nonces.add(p.nonce)
        return True


def run_security_tests() -> dict:
    """实验3: 信息素安全机制（伪造/重放/篡改/TTL）
    对照两组签名实现:
      A. 论文v1.1原版代码（SM3路径无密钥）→ 预期暴露伪造漏洞
      B. 修复版（标准HMAC-SM3带密钥）→ 预期全部拦截
    """
    key = b"device-fingerprint-derived-key"
    dna = "#龍芯⚡️SECURITY-TEST"
    r = {}

    for impl_name, legacy in (("原版代码(无密钥SM3)", True),
                              ("修复版(带密钥HMAC-SM3)", False)):
        r[impl_name] = {}
        field = LegacyField() if legacy else PheromoneField(key)
        # ① 正常释放
        p1 = Pheromone.create(PheromoneType.ALERT, "guard01", "broadcast",
                              {"sev": "high"}, dna, key)
        if legacy:
            p1.hmac = _legacy_unkeyed_sm3(p1)
        r[impl_name]["合法释放"] = field.emit(p1)
        # ② 伪造（攻击者用自己钥匙；原版无密钥路径 key 形同虚设 → 穿透）
        forged = Pheromone.create(PheromoneType.ALERT, "guard01", "broadcast",
                                  {"sev": "high"}, dna, b"attacker-key")
        if legacy:
            forged.hmac = _legacy_unkeyed_sm3(forged)
        r[impl_name]["伪造签名拦截"] = not field.emit(forged)
        # ③ 重放
        p1_copy = Pheromone(p1.ptype, p1.source, p1.target, p1.priority,
                            p1.payload, p1.timestamp, p1.dna, p1.ttl, p1.nonce, p1.hmac)
        r[impl_name]["重放拦截"] = not field.emit(p1_copy)
        # ④ 篡改（payload改后不重签）
        tampered = Pheromone(p1.ptype, p1.source, p1.target, p1.priority,
                             {"sev": "LOW"}, p1.timestamp, p1.dna, p1.ttl, p1.nonce, p1.hmac)
        r[impl_name]["篡改拦截"] = not field.emit(tampered)
        # ⑤ TTL过期
        old = Pheromone.create(PheromoneType.TRAIL, "collect01", "broadcast",
                               {"path": "ok"}, dna, key, ttl=5)
        old.timestamp = time.time() - 10
        old.hmac = old._sign(key)
        r[impl_name]["TTL过期拦截"] = not field.emit(old)

    # ⑥ 元信息素衰减对比（定理1: λ_meta=0.005 衰减最慢）
    now = time.time()
    p_meta = Pheromone.create(PheromoneType.META, "queen", "broadcast", {}, dna, key)
    p_meta.timestamp = now - 60
    p_rec = Pheromone.create(PheromoneType.RECRUIT, "worker01", "broadcast", {}, dna, key)
    p_rec.timestamp = now - 60
    r["60秒后元信息素浓度(meta)"] = round(p_meta.concentration(now), 2)
    r["60秒后招募素浓度(recruit)"] = round(p_rec.concentration(now), 2)
    r["定理1成立(元>普通)"] = p_meta.concentration(now) > p_rec.concentration(now)

    return r


def main():
    ap = argparse.ArgumentParser(description="DSACA 蚁群架构仿真实验 v1.1")
    ap.add_argument("--rounds", type=int, default=10000, help="蒙特卡洛总轮次")
    ap.add_argument("--modules", type=int, default=103, help="模块数")
    ap.add_argument("--exp", default="all", help="all|exp1|exp2|exp3")
    args = ap.parse_args()

    print("=" * 68)
    print(" 🐉 DSACA 蚁群架构仿真实验 v1.1")
    print(f" DNA: #龍芯⚡️丙午·丙申·庚申·辛巳·䷡大壮-DSACA-SIM-v1.1-UID9622")
    print(" 复现论文: 《龍魂分布式认知架构 v1.1》§9/§10")
    print(f" 模块数={args.modules} · 蒙特卡洛轮次={args.rounds} · 种子固定")
    print("=" * 68)

    if args.exp in ("all", "exp1"):
        print("\n[实验1] 定理5 鲁棒性验证（蒙特卡洛故障注入）")
        t0 = time.time()
        res = run_fault_simulation(args.rounds, args.modules)
        dt = time.time() - t0
        print(f" 完成 {args.rounds} 轮，耗时 {dt:.1f}s")
        for mode, label in (("per_pop", "口径A: 单种群失效（论文字面）"),
                            ("global", "口径B: 全系统失效（附录C证明口径·更严苛）")):
            print(f"\n {label}")
            print(f" {'失效比例':<8} {'平均E':<8} {'标准差':<8} {'最小E':<8} 状态")
            print("-" * 46)
            for rate, r in res[mode].items():
                print(f" {rate}%     {r['avg']:<8} {r['std']:<8} {r['min']:<8} {r['status']}")

    if args.exp in ("all", "exp2"):
        print("\n[实验2] 涌现质量动态演化（冷启动→稳态→压力→恢复）")
        rep = run_dynamic_evolution(args.modules)
        for ph in rep:
            print(f" {ph['phase']:<16} E={ph['E']}  (信号数 {ph['signals']})")

    if args.exp in ("all", "exp3"):
        print("\n[实验3] 信息素安全机制验证（对照原版 vs 修复版）")
        sec = run_security_tests()
        for impl, checks in sec.items():
            if impl == "定理1成立(元>普通)":
                continue
            if isinstance(checks, dict):
                print(f"\n {impl}:")
                for k, v in checks.items():
                    mark = "✅" if v is True else "❌" if v is False else "·"
                    print(f"   {mark} {k}: {v}")
            else:
                print(f" {impl}: {checks}")
        if sec.get("定理1成立(元>普通)"):
            print(f" ✅ 定理1成立(元>普通): 60s后 meta={sec.get('60秒后元信息素浓度(meta)')} vs recruit={sec.get('60秒后招募素浓度(recruit)')}")

    print("\n" + "=" * 68)
    print(" 三色: 🟡 仿真结果 = 设计预期验证，非真实系统实测")
    print(" 诚实边界: 仿真模型存在同构假设/零网络延迟/无真实负载模型")
    print("=" * 68)
    print("🐉丙午·丙申·庚申·辛巳·大壮·🟡")


if __name__ == "__main__":
    main()
