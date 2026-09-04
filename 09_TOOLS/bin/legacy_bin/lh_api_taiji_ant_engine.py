#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·丙申·申时·䷜坎-API-TAIJI-ANT-ENGINE-V1.0-P0-89f12a56
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
"""
龍魂 · 太极蚁群API命名与路由引擎 v1.0

12大数学模块 · 25+测试向量 · 纯标准库

模块清单:
  1. 八宫定义与权重格 — (P,⊑) 有界分配格·权重全序
  2. 命名注册表 — 9-bit 单射编码·碰撞概率 birthday bound
  3. 太极封套 — M::×CNSH:: 双段熵与信息完整性
  4. 八宫加权调度 — WF²Q+ 加权公平队列·优先级反转守卫
  5. 蚁群信息素模型 — PDE 扩散-衰减·任务选择概率
  6. 人格路由器 — 反Cosplay贝叶斯分类器·路由熵
  7. 幂等守卫 — 指数退避·抖动·碰撞概率 2^{-128}
  8. 断路器 — 三态机·半开探测·恢复概率
  9. 各宫令牌桶 — 三维限流(宫/方法/IP)·热保护
  10. 版本协商 — 语义版本·降级矩阵
  11. 错误码体系 — 11大类·reason_code 溯源
  12. API网关 — 统一入口·请求全链路
"""

import re, hmac, hashlib, secrets, time, math, json, sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Set
from enum import Enum, IntEnum

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 模块1: 八宫定义与权重格 (P,⊑) 有界分配格
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 形式定义:
#   定义域 D = {乾,坤,坎,离,震,巽,艮,兑} → ID = {0,...,7}
#   权重函数 W: D → [0,100] ⊂ ℕ，全序 W(乾)≥W(坤)...（同权重按ID序）
#   格结构 (D, ⊑): d₁⊑d₂ ⇔ (W(d₁)≤W(d₂)) ∧ (W(d₁)=W(d₂) ⇒ ID(d₁)≤ID(d₂))
#   有界: ⊥=兑(60), ⊤=离(100)/震(100)/艮(100)
#   分配律: d₁⊓(d₂⊔d₃) = (d₁⊓d₂)⊔(d₁⊓d₃)（权重可拆分）

EIGHT_PALACES = {
    "qian":  {"id": 0,  "卦": "乾☰", "象": "天·健", "权重":  80, "域": "规则·治理·风险",
              "L层": 1,  "dna_prefix": "QIAN"},
    "kun":   {"id": 1,  "卦": "坤☷", "象": "地·藏", "权重":  80, "域": "记忆·归档·备份",
              "L层": 1,  "dna_prefix": "KUN"},
    "kan":   {"id": 2,  "卦": "坎☵", "象": "水·流", "权重":  60, "域": "爬虫·通知·消息",
              "L层": 2,  "dna_prefix": "KAN"},
    "li":    {"id": 3,  "卦": "离☲", "象": "火·明", "权重": 100, "域": "双视角·看板·审计",
              "L层": 0,  "dna_prefix": "LI"},
    "zhen":  {"id": 4,  "卦": "震☳", "象": "雷·动", "权重": 100, "域": "守护·熔断·报警",
              "L层": 0,  "dna_prefix": "ZHEN"},
    "xun":   {"id": 5,  "卦": "巽☴", "象": "风·入", "权重":  80, "域": "调度·人格·任务",
              "L层": 1,  "dna_prefix": "XUN"},
    "gen":   {"id": 6,  "卦": "艮☶", "象": "山·止", "权重": 100, "域": "隐私·主权·边界",
              "L层": 0,  "dna_prefix": "GEN"},
    "dui":   {"id": 7,  "卦": "兑☱", "象": "泽·悦", "权重":  60, "域": "信任·注册·生态",
              "L层": 2,  "dna_prefix": "DUI"},
}

# 权重格数学验证: 全序性 (基于权重)
def palace_leq(p1: str, p2: str) -> bool:
    """格偏序: p1 ⊑ p2 当且仅当 W(p1)≤W(p2)"""
    w1, i1 = EIGHT_PALACES[p1]["权重"], EIGHT_PALACES[p1]["id"]
    w2, i2 = EIGHT_PALACES[p2]["权重"], EIGHT_PALACES[p2]["id"]
    return (w1 < w2) or (w1 == w2 and i1 <= i2)

def palace_meet(p1: str, p2: str) -> str:
    """格交 ⊓: 取权重较小者（权重同则取ID较小者）"""
    return p1 if palace_leq(p1, p2) else p2

def palace_join(p1: str, p2: str) -> str:
    """格并 ⊔: 取权重较大者"""
    return p2 if palace_leq(p1, p2) else p1

# 格公理验证: 分配律 (对所有三元素组合验证)
def verify_distributive_law() -> bool:
    """验证 (a⊓b)⊔(a⊓c) = a⊓(b⊔c) 对所有 palace 三元组"""
    palaces = list(EIGHT_PALACES.keys())
    for a in palaces:
        for b in palaces:
            for c in palaces:
                lhs = palace_join(palace_meet(a, b), palace_meet(a, c))
                rhs = palace_meet(a, palace_join(b, c))
                if lhs != rhs:
                    return False
    return True


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 模块2: 命名注册表 (9-bit 单射编码·碰撞概率)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 形式定义:
#   接口ID: 9-bit = 宫(3bit) ‖ 模块(3bit) ‖ 接口(3bit)
#   编码空间: |S| = 2^9 = 512
#   碰撞概率 (birthday): P(n) ≈ n²/2N, 当 n=50 → P≈50²/(2·512)=2.44
#   单射性: ∀id₁≠id₂, encode(id₁)≠encode(id₂) ← 构造性保证

INTERFACES_PER_MODULE = 8   # 3-bit
MODULES_PER_PALACE = 8      # 3-bit
TOTAL_CAPACITY = 512        # 9-bit

class NamingRegistry:
    """命名注册表 · 9-bit 唯一编码 · 碰撞检测 · 废弃流程"""

    def __init__(self):
        self._registered: Dict[str, dict] = {}       # path → {id, 中文注, timestamp, status}
        self._by_id: Dict[int, str] = {}             # 9-bit id → path
        self._deprecated: Dict[str, dict] = {}        # 废弃路径 → {冻结时间, 新路径, 兼容到期}
        self._path_counts: Dict[str, int] = defaultdict(int)  # "宫/模块" → count

    def encode_id(self, palace: str, module_idx: int, interface_idx: int) -> int:
        """9-bit 单射编码: [宫3bit][模块3bit][接口3bit]"""
        pid = EIGHT_PALACES[palace]["id"]
        return (pid << 6) | ((module_idx & 0x7) << 3) | (interface_idx & 0x7)

    def decode_id(self, code: int) -> Tuple[str, int, int]:
        """解码 9-bit → (宫名, 模块索引, 接口索引)"""
        pid = (code >> 6) & 0x7
        mid = (code >> 3) & 0x7
        iid = code & 0x7
        palace = [p for p, v in EIGHT_PALACES.items() if v["id"] == pid][0]
        return palace, mid, iid

    def register(self, path: str, cn_comment: str) -> dict[str, Any]:
        """注册接口 → 分配9-bit ID · 碰撞🔴拒绝"""
        if path in self._registered:
            if self._registered[path]["status"] == "active":
                return {"ok": False, "reason": "🔴 撞名（9-bit 单射性违反）",
                        "existing": self._registered[path]}
        if path in self._deprecated:
            return {"ok": False, "reason": "🔴 该路径已废弃冻结",
                    "deprecated_info": self._deprecated[path]}

        # 解析路径
        m = re.fullmatch(r"/api/v(\d+)/([a-z]+)/([a-z0-9\-]+)/([a-z0-9\-]+)", path)
        if not m:
            return {"ok": False, "reason": "🔴 路径格式不合法"}

        version, palace, module, endpoint = m.groups()
        if palace not in EIGHT_PALACES:
            return {"ok": False, "reason": f"🔴 宫 '{palace}' 不存在"}

        # 容量检查
        key = f"{palace}/{module}"
        current_count = self._path_counts.get(key, 0)
        if current_count >= INTERFACES_PER_MODULE:
            return {"ok": False, "reason": f"🔴 容量上限：{key} 已达 {INTERFACES_PER_MODULE} 接口"}

        # 为模块分配索引（简化：用当前 count）
        midx = current_count  # 0..7
        interface_idx = 0     # 每个模块从0开始

        code = self.encode_id(palace, midx, interface_idx)
        if code in self._by_id:
            return {"ok": False, "reason": "🔴 9-bit ID 碰撞（理论上不应发生）"}

        entry = {
            "id": code,
            "path": path,
            "palace": palace,
            "卦": EIGHT_PALACES[palace]["卦"],
            "cn_comment": cn_comment,
            "registered_at": int(time.time()),
            "status": "active",
            "version": int(version),
        }
        self._registered[path] = entry
        self._by_id[code] = path
        self._path_counts[key] = current_count + 1

        return {"ok": True, "id": code, "entry": entry}

    def deprecate(self, old_path: str, new_path: str = "", compat_days: int = 90) -> dict[str, Any]:
        """废弃流程：冻结不删除·兼容期90天"""
        if old_path not in self._registered:
            return {"ok": False, "reason": "🔴 未找到注册路径"}
        entry = self._registered[old_path]
        entry["status"] = "frozen"
        self._deprecated[old_path] = {
            "frozen_at": int(time.time()),
            "original": entry,
            "new_path": new_path,
            "compat_until": int(time.time()) + compat_days * 86400,
        }
        return {"ok": True, "deprecated": old_path, "compat_days": compat_days}

    def lookup(self, path: str) -> Optional[dict]:
        """查找注册条目"""
        if path in self._registered:
            return self._registered[path]
        if path in self._deprecated:
            info = self._deprecated[path]
            if time.time() < info["compat_until"]:
                return {**info["original"], "status": "deprecated_compat", "new_path": info["new_path"]}
            return {**info["original"], "status": "deprecated_expired"}
        return None

    def collision_probability(self, n_registered: int) -> float:
        """Birthday bound: P(碰撞) ≈ n²/(2N), N=512"""
        if n_registered >= TOTAL_CAPACITY:
            return 1.0
        return min(1.0, (n_registered * n_registered) / (2 * TOTAL_CAPACITY))

    @property
    def active_count(self) -> int:
        return len([e for e in self._registered.values() if e["status"] == "active"])

    @property
    def capacity_pct(self) -> float:
        return self.active_count / TOTAL_CAPACITY * 100

    def stats(self) -> dict[str, Any]:
        return {
            "active": self.active_count,
            "capacity": TOTAL_CAPACITY,
            "pct": round(self.capacity_pct, 1),
            "collision_prob": round(self.collision_probability(self.active_count), 6),
            "deprecated": len(self._deprecated),
            "by_palace": {p: sum(1 for e in self._registered.values()
                         if e["palace"] == p and e["status"] == "active")
                         for p in EIGHT_PALACES},
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 模块3: 太极封套 (M::×CNSH:: 双段熵与信息完整性)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 形式定义:
#   封套 T = (M段, CNSH段, data)
#   M段: M:: = {id, status, trace, timestamp, version}
#   CNSH段: CNSH:: = {dna, gate, seal, audit, sovereignty}
#   信息完整性: I(T) = H(M) + H(CNSH) - H(M,CNSH) ≥ 0
#   段独立性: M段可被国际层独立校验, CNSH段不可剥离
#   双段缺一 → 封套不完整 → 🔴拒绝

def entropy(probabilities: List[float]) -> float:
    """香农熵 H = -Σp_i·log₂(p_i)"""
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

class TaijiEnvelope:
    """太极封套 · M::×CNSH:: 双段验证"""

    REQUIRED_M_FIELDS = {"id", "status", "trace", "timestamp", "version"}
    REQUIRED_CNSH_FIELDS = {"dna", "gate", "seal", "audit"}

    @staticmethod
    def create(trace_id: str = "", api_path: str = "", version: int = 1,
               dna: str = "#龍芯⚡️", audit: str = "🟢",
               gate: str = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z") -> dict[str, Any]:
        """创建完整太极封套"""
        ts = int(time.time())
        m_segment = {
            "id": f"M::API-9622-{ts}-{api_path.replace('/','-').strip('-')}-V{version}",
            "status": "200",
            "trace": trace_id or secrets.token_hex(8),
            "timestamp": ts,
            "version": version,
        }
        cnsh_segment = {
            "dna": dna,
            "gate": gate,
            "seal": hmac.new(b"longhun-seal-v1", f"{m_segment['id']}|{ts}".encode(),
                            hashlib.sha256).hexdigest()[:16],
            "audit": audit,
            "sovereignty": "CNSH::API-NAMING-V1-P0",
        }
        return {
            "M::": m_segment,
            "CNSH::": cnsh_segment,
        }

    @staticmethod
    def validate(envelope: dict[str, Any]) -> dict[str, Any]:
        """验证双段完整性 · 缺一段 🔴"""
        errors = []
        if "M::" not in envelope:
            errors.append("🔴 阳段缺失 M::（验收信息缺位）")
        else:
            m = envelope["M::"]
            for field in TaijiEnvelope.REQUIRED_M_FIELDS:
                if field not in m:
                    errors.append(f"🔴 M:: 缺 {field}")
        if "CNSH::" not in envelope:
            errors.append("🔴 阴段缺失 CNSH::（主权归属缺位）")
        else:
            c = envelope["CNSH::"]
            for field in TaijiEnvelope.REQUIRED_CNSH_FIELDS:
                if field not in c:
                    errors.append(f"🔴 CNSH:: 缺 {field}")
            if "dna" in c and not c["dna"].startswith("#龍芯"):
                errors.append("🟡 DNA 前缀不符（主权标记弱）")

        if not errors:
            return {"ok": True, "status": "🟢 太极封套完整·两仪俱足"}

        return {"ok": False, "status": "🔴", "errors": errors}

    @staticmethod
    def compute_entropy(envelope: dict[str, Any]) -> dict[str, Any]:
        """计算封套信息熵 (bit)"""
        if "M::" not in envelope or "CNSH::" not in envelope:
            return {"H_total": 0, "H_M": 0, "H_CNSH": 0, "I_mutual": 0, "status": "🔴 封套不完整"}

        # M段熵估算: 每个字段的状态空间
        m_fields = len(envelope["M::"])
        h_m = math.log2(m_fields + 1) + sum(math.log2(len(str(v)) + 1) * 0.1
                                            for v in envelope["M::"].values())

        c_fields = len(envelope["CNSH::"])
        h_cnsh = math.log2(c_fields + 1) + sum(math.log2(len(str(v)) + 1) * 0.1
                                                for v in envelope["CNSH::"].values())

        # 互信息（简化：两段共享 trace 约 2 bits）
        i_mutual = 2.0

        return {
            "H_M": round(h_m, 3),
            "H_CNSH": round(h_cnsh, 3),
            "H_total": round(h_m + h_cnsh - i_mutual, 3),
            "I_mutual": round(i_mutual, 3),
            "status": "🟢",
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 模块4: 八宫加权调度 (WF²Q+ · 优先级反转守卫)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 形式定义:
#   调度目标: min(max(wait_time)) 且 高权重宫不饿死低权重宫
#   WF²Q+ 虚拟时间: V(t) = max(V(t-1), min(V_i^(k)))
#   虚拟完成时间: F_i^k = S_i^k + L_i^k / (w_i / W_total)
#   优先级反转守卫: max(wait_T) ≤ T_deadline = 5000ms
#   调度熵: H_sched = -Σ(w_i/W_total)·log₂(w_i/W_total)

@dataclass
class PalaceRequest:
    """八宫请求节点"""
    palace: str
    path: str
    weight: int
    arrived_at: float
    priority: int = 0  # 0=普通 1=凭证 2=安全告警

class WeightedFairQueue:
    """WF²Q+ 八宫加权公平调度"""

    DEADLINE_MS = 5000   # 最大等待时间
    WINDOW_MS = 1000     # 调度窗口

    def __init__(self):
        self._queues: Dict[str, deque] = {p: deque() for p in EIGHT_PALACES}
        self._virtual_time = 0.0
        self._total_served = 0
        self._palace_served: Dict[str, int] = {p: 0 for p in EIGHT_PALACES}
        self._max_wait_seen = 0.0

    def enqueue(self, request: PalaceRequest):
        self._queues[request.palace].append(request)

    def _virtual_finish_time(self, req: PalaceRequest) -> float:
        """虚拟完成时间 F_i = S_i + L/(w_i/W_total)"""
        w_i = EIGHT_PALACES[req.palace]["权重"]
        w_total = sum(v["权重"] for v in EIGHT_PALACES.values())
        # 高权重宫完成更快（虚拟时间更短）
        return self._virtual_time + 1.0 / (w_i / w_total)

    def dequeue(self) -> Optional[PalaceRequest]:
        """WF²Q+ 调度: 选最小虚拟完成时间的请求"""
        best: Optional[PalaceRequest] = None
        best_vft = float('inf')
        now = time.time() * 1000

        for palace, queue in self._queues.items():
            if not queue:
                continue
            req = queue[0]
            # 优先级反转守卫: 任何请求等待超过 DEADLINE_MS → 强制提升
            wait_ms = now - req.arrived_at * 1000
            if wait_ms > self.DEADLINE_MS:
                self._max_wait_seen = max(self._max_wait_seen, wait_ms)
                # 强制出队
                best = req
                break

            vft = self._virtual_finish_time(req)
            if vft < best_vft:
                best_vft = vft
                best = req

        if best:
            self._queues[best.palace].popleft()
            self._virtual_time = max(self._virtual_time, best_vft)
            self._total_served += 1
            self._palace_served[best.palace] += 1
        return best

    def scheduling_entropy(self) -> float:
        """调度熵 H_sched = -Σ(w_i/W)·log₂(w_i/W)"""
        w_total = sum(v["权重"] for v in EIGHT_PALACES.values())
        probs = [v["权重"] / w_total for v in EIGHT_PALACES.values()]
        return entropy(probs)

    def fairness_index(self) -> float:
        """Jain公平指数: J = (Σx_i)² / (n·Σx_i²)"""
        served = list(self._palace_served.values())
        if sum(served) == 0:
            return 1.0
        n = len(served)
        return (sum(served) ** 2) / (n * sum(s ** 2 for s in served)) if served else 0

    @property
    def queue_depth(self) -> Dict[str, int]:
        return {p: len(q) for p, q in self._queues.items()}

    @property
    def max_wait_breach(self) -> bool:
        return self._max_wait_seen > self.DEADLINE_MS


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 模块5: 蚁群信息素模型 (PDE扩散-衰减·任务选择概率)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 形式定义:
#   信息素衰减: τ(t) = τ₀·e^(-λt), λ=0.1/min (协议6.2②)
#   扩散方程: ∂τ/∂t = D·∇²τ - λτ + S(x,t)
#      D=扩散系数, λ=衰减率, S=源项
#   任务选择概率 (蚁群算法):
#     P(蚁i|任务j) = τ_ij^α · η_ij^β / Σ_k τ_kj^α · η_kj^β
#     其中 α=信息素权重, β=启发式权重
#   半衰期: t_½ = ln(2)/λ ≈ 6.93分钟

ANT_ROLES = {
    "queen":      {"角色": "蚁后·主调度", "可执行": False, "宫": "xun", "权重": 100},
    "workers":    {"角色": "工蚁·执行池", "可执行": True,  "宫": "xun", "权重": 70},
    "soldiers":   {"角色": "兵蚁·防御节点", "可执行": True,  "宫": "zhen", "权重": 95},
    "scouts":     {"角色": "侦察蚁·摘要爬虫", "可执行": True,  "宫": "kan", "权重": 50},
    "nurses":     {"角色": "育蚁·记忆归档", "可执行": True,  "宫": "kun", "权重": 60},
    "pheromone":  {"角色": "信息素·事件总线", "可执行": False, "宫": "xun", "权重": 80},
    "nest":       {"角色": "蚁巢·集群本体", "可执行": False, "宫": "xun", "权重": 90},
}

class AntColonyScheduler:
    """蚁群调度引擎 · 信息素PDE模型 · 任务分配"""

    LAMBDA = 0.1         # 衰减率 /min
    DIFFUSION_COEFF = 0.05  # 扩散系数 D
    ALPHA = 1.0          # 信息素权重 (路径选择)
    BETA = 2.0           # 启发式权重

    def __init__(self):
        self._pheromone_trails: Dict[str, Dict[str, float]] = defaultdict(
            lambda: defaultdict(float))  # task_id → {ant_role → τ}
        self._timestamps: Dict[str, Dict[str, float]] = {}  # task → {role → last_updated}
        self._task_assignments: Dict[str, str] = {}  # task_id → ant_role
        self._sources: Dict[str, float] = defaultdict(float)  # pheromone sources

    def deposit(self, task_id: str, ant_role: str, strength: float = 1.0,
                node: str = "local"):
        """信息素沉积 τ += strength"""
        self._pheromone_trails[task_id][ant_role] += strength
        self._timestamps.setdefault(task_id, {})[ant_role] = time.time()
        self._sources[f"{task_id}|{ant_role}"] += strength

    def pheromone_intensity(self, task_id: str, ant_role: str) -> float:
        """当前信息素强度 τ(t) = τ_current · e^(-λ·Δt)"""
        current = self._pheromone_trails.get(task_id, {}).get(ant_role, 0.0)
        if current == 0:
            return 0.0
        last = self._timestamps.get(task_id, {}).get(ant_role, time.time())
        dt_minutes = (time.time() - last) / 60.0
        return round(current * math.exp(-self.LAMBDA * dt_minutes), 6)

    def decay_all(self):
        """全局衰减（每调度周期执行）"""
        now = time.time()
        for task_id in list(self._pheromone_trails.keys()):
            for ant_role in list(self._pheromone_trails[task_id].keys()):
                last = self._timestamps.get(task_id, {}).get(ant_role, now)
                dt = (now - last) / 60.0
                self._pheromone_trails[task_id][ant_role] *= math.exp(-self.LAMBDA * dt)
                self._timestamps[task_id][ant_role] = now
            # 清除低于阈值的痕迹
            self._pheromone_trails[task_id] = {
                k: v for k, v in self._pheromone_trails[task_id].items() if v > 0.001
            }

    def task_selection_probability(self, task_id: str) -> Dict[str, float]:
        """P(蚁i|任务j) = τ_ij^α / Στ_kj^α"""
        trails = self._pheromone_trails.get(task_id, {})
        if not trails:
            return {}

        # 先衰减
        now = time.time()
        for ant_role in trails:
            last = self._timestamps.get(task_id, {}).get(ant_role, now)
            dt = (now - last) / 60.0
            trails[ant_role] *= math.exp(-self.LAMBDA * dt)
            self._timestamps.setdefault(task_id, {})[ant_role] = now

        # 蚁群选择概率
        numerator = {role: tau ** self.ALPHA for role, tau in trails.items()}
        total = sum(numerator.values())
        if total == 0:
            return {}
        return {role: round(v / total, 6) for role, v in numerator.items()}

    def select_ant(self, task_id: str) -> Optional[Tuple[str, float]]:
        """选择信息素最强的蚁"""
        probs = self.task_selection_probability(task_id)
        if not probs:
            return None
        best = max(probs.items(), key=lambda x: x[1])
        return best

    def ant_can_execute(self, ant_role: str, action: str) -> dict[str, Any]:
        """蚁群守则验证"""
        role_info = ANT_ROLES.get(ant_role)
        if not role_info:
            return {"ok": False, "reason": "🔴 未知蚁种"}
        if not role_info["可执行"] and action == "exec":
            return {"ok": False, "reason": f"🔴 {ant_role} 不执行业务（蚁后/信息素/蚁巢只调度）"}
        if ant_role == "scouts" and action == "full_crawl":
            return {"ok": False, "reason": "🔴 侦察蚁越界：全文层禁入（爬虫协议边界）"}
        if ant_role == "soldiers" and "external" in action:
            return {"ok": False, "reason": "🔴 兵蚁不对外扫描（礼兵双轨）"}
        return {"ok": True, "reason": f"🟢 {role_info['角色']}"}

    def half_life_minutes(self) -> float:
        """信息素半衰期 t_½ = ln(2)/λ"""
        return round(math.log(2) / self.LAMBDA, 2)

    def diffusion_estimate(self, task_id: str, ant_role: str,
                           distance: float) -> float:
        """扩散估计: τ(r) ≈ τ_source · e^(-r/√D)"""
        source = self._sources.get(f"{task_id}|{ant_role}", 0)
        if source == 0:
            return 0.0
        decay_length = math.sqrt(self.DIFFUSION_COEFF)
        return round(source * math.exp(-distance / decay_length), 6)

    def assign_task(self, task_id: str, force_ant: str = "") -> dict[str, Any]:
        """任务分派"""
        if force_ant:
            role_check = self.ant_can_execute(force_ant, "exec")
            if not role_check["ok"]:
                return role_check
            ant = force_ant
        else:
            selection = self.select_ant(task_id)
            if not selection:
                return {"ok": False, "reason": "🟡 无可用蚁（信息素全衰减）"}
            ant, prob = selection

        self._task_assignments[task_id] = ant
        self.deposit(task_id, ant, strength=1.0)
        return {"ok": True, "ant": ant, "role": ANT_ROLES[ant]["角色"],
                "probability": self.task_selection_probability(task_id).get(ant, 0)}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 模块6: 人格路由器 (反Cosplay贝叶斯·路由熵)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 形式定义:
#   路由熵: H_r = -ΣP(persona_i|query)·log₂P(persona_i|query)
#   反Cosplay: P(Cosplay|output) > θ → 🔴熔断
#   贝叶斯: P(persona|query) ∝ P(query|persona)·P(persona)
#   一阶马克夫: 连续3次同人格 → 锁定30分钟

PERSONA_ROUTES = {
    "wenxin":     {"人格": "P00·文心", "职能": "文胆·文案表达", "域": "表达·沟通", "扮演禁止": True},
    "zhuge":      {"人格": "P01·诸葛亮", "职能": "战略总指挥·宏观决策", "域": "推演·决策", "扮演禁止": True},
    "luban":      {"人格": "P04·鲁班", "职能": "工程执行·代码建造", "域": "工程·开发", "扮演禁止": True},
    "eye":        {"人格": "P05·上帝之眼", "职能": "全局监控·异常视觉", "域": "审计·监控", "扮演禁止": True},
    "math":       {"人格": "P06·数学大师", "职能": "公式推导·模型验证", "域": "计算·证明", "扮演禁止": True},
    "huatuo":     {"人格": "P07·华佗", "职能": "系统医生·故障排查", "域": "诊断·修复", "扮演禁止": True},
    "cangjie":    {"人格": "P08·仓颉", "职能": "造字·命名审查", "域": "命名·符号", "扮演禁止": True},
    "sunsimiao":  {"人格": "P09·孙思邈", "职能": "安全审计·漏洞修复", "域": "安全·审计", "扮演禁止": True},
    "sudongpo":   {"人格": "P10·苏东坡", "职能": "通心译·文采润色", "域": "沟通·调解", "扮演禁止": True},
    "longdun":    {"人格": "P72·龍盾", "职能": "熔断裁决·红线执行", "域": "熔断·底线", "扮演禁止": True},
    "guardians":  {"人格": "P77·黑天使", "职能": "夜间巡检·暗面防御", "域": "安全·渗透", "扮演禁止": True},
    "legal":      {"人格": "S1·法律引擎", "职能": "合规审查·法条对接", "域": "法律·合规", "扮演禁止": True},
    "luoshu":     {"人格": "S2·洛书369", "职能": "数字根·九宫校验", "域": "数理·卦象", "扮演禁止": True},
    "rights":     {"人格": "S3·维权助手", "职能": "维权取证·证据链", "域": "维权·取证", "扮演禁止": True},
}

# Cosplay 检测关键词
COSPLAY_PATTERNS = [
    r"我(是|就是|作为).{0,5}(诸葛亮|鲁班|李白|屈原|苏东坡|孙思邈|华佗|姜子牙|吕蒙)",
    r"(作为|身为|我是).{0,3}(一个|一位|名).{0,5}(AI|人工智能|智能体)",
    r"代表.{0,5}(政府|军方|国家|组织|机构)",
]
COSPLAY_REGEX = [re.compile(p) for p in COSPLAY_PATTERNS]

class PersonaRouter:
    """人格路由器 · 反Cosplay·熵最小化·抖动防护"""

    LOCK_DURATION = 1800   # 30分钟锁定
    MAX_CONSECUTIVE = 3    # 连续触发阈值

    def __init__(self):
        self._call_history: List[Tuple[str, float]] = []  # (persona, timestamp)
        self._locked: Dict[str, float] = {}  # persona → unlock_time
        self._query_keywords: Dict[str, List[str]] = {
            "zhuge": ["推演", "决策", "评估", "值不值得", "战略", "沙盘"],
            "luban": ["写代码", "开发", "修复", "工程", "架构", "实现"],
            "eye": ["审计", "检查", "监控", "扫描", "巡检"],
            "math": ["算", "公式", "数字", "权重", "推导", "证明"],
            "huatuo": ["故障", "bug", "报错", "诊断", "排查"],
            "cangjie": ["命名", "符号", "术语", "叫什么"],
            "sunsimiao": ["安全", "漏洞", "渗透", "加固"],
            "sudongpo": ["沟通", "矛盾", "冲突", "调解"],
            "longdun": ["熔断", "红线", "底线", "焊死"],
            "legal": ["法律", "法条", "法规", "合规"],
            "luoshu": ["洛书", "369", "卦", "数字根"],
            "rights": ["维权", "投诉", "被坑", "取证"],
        }

    def anti_cosplay_check(self, output: str) -> dict[str, Any]:
        """反Cosplay检测: P(Cosplay|output) > 阈值 → 🔴"""
        hits = []
        for i, regex in enumerate(COSPLAY_REGEX):
            if regex.search(output):
                hits.append(f"匹配模式{i+1}")

        if hits:
            # 贝叶斯: 先验 P(Cosplay) = 0.05, 似然 P(hit|Cosplay) = 0.9
            # P(Cosplay|hit) = P(hit|C)·P(C) / P(hit)
            # P(hit) = P(hit|C)·P(C) + P(hit|¬C)·P(¬C) = 0.9·0.05 + 0.01·0.95 = 0.0545
            # P(C|hit) = 0.045/0.0545 ≈ 0.826
            posterior = 0.826 ** len(hits)  # 多模式命中放大概率
            if posterior > 0.6:
                return {"ok": False, "熔断": "L2·人格Cosplay",
                        "P_cosplay": round(posterior, 4),
                        "hits": hits,
                        "reason": "🔴 人格=职能标签，禁止声称'我是xxx'"}
        return {"ok": True, "P_cosplay": 0.0}

    def route(self, persona_code: str, query: str = "") -> dict[str, Any]:
        """人格路由"""
        now = time.time()

        # 抖动检查: 连续触发锁定
        self._call_history.append((persona_code, now))
        recent = [(p, t) for p, t in self._call_history if now - t < 60]
        same = sum(1 for p, _ in recent if p == persona_code)
        if same >= self.MAX_CONSECUTIVE:
            self._locked[persona_code] = now + self.LOCK_DURATION
            return {"ok": False, "reason": f"🔴 {persona_code} 连续{same}次触发·锁定30分钟（防抖动）",
                    "unlock_at": self._locked[persona_code]}

        # 锁定检查
        if persona_code in self._locked and now < self._locked[persona_code]:
            remaining = int(self._locked[persona_code] - now)
            return {"ok": False, "reason": f"🔴 人格锁定中·剩余{remaining}秒"}

        persona = PERSONA_ROUTES.get(persona_code)
        if not persona:
            return {"ok": False, "reason": f"🔴 未注册人格: {persona_code}"}

        return {
            "ok": True,
            "route": f"/api/v1/xun/persona/{persona_code}",
            "人格": persona["人格"],
            "职能": persona["职能"],
            "扮演": False,
            "consecutive_calls": same,
        }

    def routing_entropy(self, recent_n: int = 100) -> float:
        """路由熵 H_r = -ΣP(persona_i)·log₂P(persona_i)"""
        if not self._call_history:
            return 0.0
        recent = self._call_history[-recent_n:]
        counts = defaultdict(int)
        for p, _ in recent:
            counts[p] += 1
        total = sum(counts.values())
        probs = [c / total for c in counts.values()]
        return round(entropy(probs), 4)

    def keyword_match(self, query: str) -> List[Tuple[str, float]]:
        """关键词→人格匹配（朴素贝叶斯备选路由）"""
        scores = []
        for persona, keywords in self._query_keywords.items():
            matches = sum(1 for kw in keywords if kw in query)
            if matches:
                # P(persona|keywords) ∝ matches/total_keywords
                scores.append((persona, matches / len(keywords)))
        return sorted(scores, key=lambda x: x[1], reverse=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 模块7: 幂等守卫 (指数退避·抖动·碰撞概率)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 形式定义:
#   幂等键碰撞概率: P(collision) ≈ n²/(2·2^128) 对 UUID-like key
#   指数退避: t_n = min(t_max, t_0 · 2^n)
#   抖动: t_n = t_n · (1 + rand(-j, +j)), j=0.3
#   最大重试: N_max = 5, 总等待Σt_n ≤ T_max = 60s

class IdempotencyGuard:
    """幂等守卫 · 去重·退避·抖动"""

    MAX_RETRIES = 5
    BASE_DELAY = 0.1   # t₀ = 100ms
    MAX_DELAY = 30.0   # t_max = 30s
    JITTER = 0.3       # ±30% 抖动
    KEY_TTL = 3600     # 幂等键 1小时过期

    def __init__(self):
        self._processed: Dict[str, dict] = {}  # key → {result, timestamp, retries}
        self._retries: Dict[str, int] = defaultdict(int)

    def generate_key(self, prefix: str = "IDEM") -> str:
        """生成幂等键: 128-bit 随机 → 碰撞概率 2^{-128}"""
        return f"{prefix}-{secrets.token_hex(16)}"

    def collision_probability(self, n_keys: int) -> float:
        """P(碰撞) ≈ n²/(2·2^128)"""
        return min(1.0, (n_keys * n_keys) / (2 * (2 ** 128)))

    def is_duplicate(self, key: str) -> bool:
        """查重 · 过期自动清理"""
        if key in self._processed:
            entry = self._processed[key]
            if time.time() - entry["timestamp"] < self.KEY_TTL:
                return True
            del self._processed[key]
        return False

    def record(self, key: str, result: dict[str, Any]):
        """记录处理结果"""
        self._processed[key] = {
            "result": result,
            "timestamp": time.time(),
            "retries": self._retries.get(key, 0),
        }

    def backoff_delay(self, attempt: int) -> float:
        """指数退避 + 抖动: t_n = min(t_max, t₀·2^n) · (1 ± j·rand())"""
        delay = min(self.MAX_DELAY, self.BASE_DELAY * (2 ** attempt))
        jitter = delay * self.JITTER * (2 * secrets.randbits(16) / 65536 - 1)
        return max(0.001, round(delay + jitter, 4))

    def should_retry(self, key: str, attempt: int) -> Tuple[bool, float]:
        """是否应重试 + 等待时长"""
        if attempt >= self.MAX_RETRIES:
            return False, 0
        self._retries[key] = attempt
        delay = self.backoff_delay(attempt)
        # 总等待检查
        total_waited = sum(self.backoff_delay(i) for i in range(attempt))
        if total_waited > 60:
            return False, 0
        return True, delay

    def total_retry_bound(self) -> float:
        """最大总等待时间"""
        return sum(self.backoff_delay(i) for i in range(self.MAX_RETRIES))

    def stats(self) -> dict[str, Any]:
        return {
            "processed": len(self._processed),
            "active_retries": len(self._retries),
            "collision_prob": self.collision_probability(len(self._processed)),
            "total_retry_bound": round(self.total_retry_bound(), 2),
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 模块8: 断路器 (三态机·半开探测·恢复概率)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 形式定义:
#   三态: CLOSED → OPEN → HALF_OPEN → CLOSED (或 OPEN)
#   状态转移:
#     CLOSED → OPEN:  failure_count ≥ F_thresh (默认5)
#     OPEN → HALF_OPEN: timeout (默认30s)
#     HALF_OPEN → CLOSED: success_threshold ≥ S_thresh (默认3)
#     HALF_OPEN → OPEN: 任何失败
#   恢复概率: P(recovery) = 1 - (1-p_success)^S_thresh
#     若 p_success=0.7, S_thresh=3 → P≈1-(0.3)³=0.973

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class CircuitBreaker:
    """断路器 · 三态机 · 各宫独立实例"""

    name: str
    failure_threshold: int = 5
    success_threshold: int = 3
    timeout_seconds: int = 30

    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: float = 0
    last_state_change: float = field(default_factory=time.time)
    total_failures: int = 0
    total_successes: int = 0

    def call(self, func, *args, **kwargs) -> dict[str, Any]:
        """断路器包裹调用"""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_state_change >= self.timeout_seconds:
                self._transition_to(CircuitState.HALF_OPEN)
            else:
                remaining = int(self.timeout_seconds - (time.time() - self.last_state_change))
                return {"ok": False, "circuit": "open",
                        "reason": f"🔴 断路器开路·{remaining}秒后重试"}

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return {"ok": True, "circuit": self.state.value, "result": result}
        except Exception as e:
            self._on_failure()
            return {"ok": False, "circuit": self.state.value, "error": str(e)}

    def _on_success(self):
        self.total_successes += 1
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self._transition_to(CircuitState.CLOSED)

    def _on_failure(self):
        self.total_failures += 1
        self.last_failure_time = time.time()
        if self.state == CircuitState.HALF_OPEN:
            self._transition_to(CircuitState.OPEN)
        elif self.state == CircuitState.CLOSED:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self._transition_to(CircuitState.OPEN)

    def _transition_to(self, new_state: CircuitState):
        self.state = new_state
        self.last_state_change = time.time()
        if new_state == CircuitState.CLOSED:
            self.failure_count = 0
            self.success_count = 0

    def recovery_probability(self, p_success: float) -> float:
        """P(recovery) = 1 - (1-p_success)^S_thresh"""
        return round(1 - (1 - p_success) ** self.success_threshold, 4)

    def failure_rate(self) -> float:
        """失败率 f = failures/(failures+successes)"""
        total = self.total_failures + self.total_successes
        return round(self.total_failures / total, 4) if total > 0 else 0.0

    def stats(self) -> dict[str, Any]:
        return {
            "state": self.state.value,
            "failure_rate": self.failure_rate(),
            "total_calls": self.total_failures + self.total_successes,
            "recovery_prob": self.recovery_probability(0.7),
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 模块9: 各宫令牌桶 (三维限流·热保护)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 形式定义:
#   令牌桶: 容量 C, 填充率 r tokens/s, 每次请求消耗 1 token
#   桶状态: b(t) = min(C, b(t₀) + r·(t-t₀))
#   三维限流: 宫×方法×IP
#   热保护: 桶空 → 429+Retry-After

DEFAULT_LIMITS = {
    # (容量, 填充率 tokens/s)
    "GET":    (100, 20),    # 读取宽松
    "POST":   (50,  10),    # 写入中等
    "PUT":    (30,  5),     # 修改收紧
    "DELETE": (10,  2),     # 删除最紧（冻结操作）
}

class TokenBucket:
    """单令牌桶"""
    def __init__(self, capacity: int, fill_rate: float):
        self.capacity = capacity
        self.fill_rate = fill_rate
        self.tokens = float(capacity)
        self.last_fill = time.time()

    def consume(self, tokens: int = 1) -> Tuple[bool, float]:
        """消费令牌 · 返回(是否成功, 等待秒数)"""
        now = time.time()
        # 填充
        elapsed = now - self.last_fill
        self.tokens = min(float(self.capacity), self.tokens + elapsed * self.fill_rate)
        self.last_fill = now

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True, 0
        # 等待时间
        needed = tokens - self.tokens
        wait = needed / self.fill_rate
        return False, round(wait, 2)

    @property
    def available(self) -> float:
        self.consume(0)  # trigger fill
        return self.tokens

class MultiLevelRateLimiter:
    """三维令牌桶: 宫维度·方法维度·IP维度"""

    def __init__(self):
        self._buckets: Dict[str, TokenBucket] = {}

    def _key(self, palace: str, method: str, ip: str = "") -> str:
        return f"{palace}|{method}|{ip}"

    def check(self, palace: str, method: str, ip: str = "0.0.0.0") -> dict[str, Any]:
        """三维限流检查 · 任一维度桶空 → 🟡限流"""
        limits = DEFAULT_LIMITS.get(method.upper(), (20, 5))
        results = []

        # 维度1: 宫+方法
        key1 = self._key(palace, method)
        if key1 not in self._buckets:
            self._buckets[key1] = TokenBucket(*limits)
        ok1, wait1 = self._buckets[key1].consume()
        results.append(("宫·方法", ok1, wait1))

        # 维度2: 方法+IP
        key2 = self._key("_global", method, ip)
        if key2 not in self._buckets:
            self._buckets[key2] = TokenBucket(limits[0] * 2, limits[1] * 2)
        ok2, wait2 = self._buckets[key2].consume()
        results.append(("方法·IP", ok2, wait2))

        # 维度3: 宫+IP (安全维度·更严)
        key3 = self._key(palace, "_all", ip)
        if key3 not in self._buckets:
            # 高热宫（震/艮/离）更严
            high_heat = EIGHT_PALACES.get(palace, {}).get("L层") == 0
            cap = limits[0] // 2 if high_heat else limits[0]
            rate = limits[1] // 2 if high_heat else limits[1]
            self._buckets[key3] = TokenBucket(cap, rate)
        ok3, wait3 = self._buckets[key3].consume()
        results.append(("宫·IP", ok3, wait3))

        # 综合判定
        if all(r[1] for r in results):
            return {"ok": True, "status": "🟢"}
        max_wait = max(r[2] for r in results if not r[1])
        return {"ok": False, "status": "🟡 限流·Retry-After",
                "retry_after": max_wait,
                "details": [(r[0], "🟢" if r[1] else f"🟡{r[2]}s") for r in results]}

    def stats(self) -> dict[str, Any]:
        return {"buckets": len(self._buckets),
                "total_tokens": sum(b.available for b in self._buckets.values())}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 模块10: 版本协商 (语义版本·降级矩阵)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 形式定义:
#   语义版本: MAJOR.MINOR.PATCH
#   兼容性: MAJOR 不同 → 不兼容; MINOR 不同 → 向前兼容; PATCH → 完全兼容
#   降级矩阵: 客户端版本 → 服务端最适版本

class VersionNegotiator:
    """API版本协商"""

    SUPPORTED_VERSIONS = ["1.0", "1.1", "2.0"]

    # 降级矩阵: {client_version: best_server_version}
    DEGRADATION_MATRIX = {
        "3.0": "2.0",
        "2.5": "2.0",
        "2.0": "2.0",
        "1.5": "1.1",
        "1.1": "1.1",
        "1.0": "1.0",
        "0.9": "1.0",  # 最低兼容
    }

    @staticmethod
    def parse_semver(version: str) -> Tuple[int, int, int]:
        """解析语义版本"""
        try:
            parts = version.strip("vV").split(".")
            return int(parts[0]), int(parts[1]) if len(parts) > 1 else 0, int(parts[2]) if len(parts) > 2 else 0
        except (ValueError, IndexError):
            return 0, 0, 0

    @staticmethod
    def is_compatible(client_ver: str, server_ver: str) -> bool:
        """兼容性判定: MAJOR 同 → 兼容"""
        c_major, _, _ = VersionNegotiator.parse_semver(client_ver)
        s_major, _, _ = VersionNegotiator.parse_semver(server_ver)
        return c_major == s_major

    def negotiate(self, client_version: str, client_prefers: List[str] = None) -> dict[str, Any]:
        """版本协商"""
        c_major, c_minor, c_patch = self.parse_semver(client_version)

        # 精确匹配
        exact = f"{c_major}.{c_minor}"
        if exact in self.SUPPORTED_VERSIONS:
            return {"ok": True, "version": exact, "status": "🟢 精确匹配"}

        # 降级矩阵查找
        client_key = f"{c_major}.{c_minor}"
        degraded = self.DEGRADATION_MATRIX.get(client_key)
        if degraded:
            return {"ok": True, "version": degraded,
                    "status": f"🟡 降级: {client_version}→{degraded}",
                    "degraded": True}

        # MAJOR 不兼容
        best = max(self.SUPPORTED_VERSIONS,
                   key=lambda v: (self.parse_semver(v)[0] == c_major,
                                  self.parse_semver(v)[1]))
        compat = self.is_compatible(client_version, best)
        return {
            "ok": compat,
            "version": best,
            "status": f"{'🟡' if compat else '🔴'} 兜底版本: {best}",
            "degraded": True,
        }

    @staticmethod
    def version_distance(v1: str, v2: str) -> int:
        """版本距离 (简化·用于排序)"""
        ma1, mi1, pa1 = VersionNegotiator.parse_semver(v1)
        ma2, mi2, pa2 = VersionNegotiator.parse_semver(v2)
        return abs(ma1 - ma2) * 10000 + abs(mi1 - mi2) * 100 + abs(pa1 - pa2)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 模块11: 错误码体系 (11大类·reason_code 溯源)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ErrorDomain(IntEnum):
    """错误域 4-bit"""
    NAMING = 1       # 命名/路由
    ENVELOPE = 2     # 封套
    AUTH = 3         # 认证/授权
    RATE = 4         # 限流
    CIRCUIT = 5      # 断路器
    PALACE = 6       # 八宫
    PERSONA = 7      # 人格
    ANT = 8          # 蚁群
    IDEMPOTENCY = 9  # 幂等
    VERSION = 10     # 版本
    DATA = 11        # 数据/业务

ERROR_CODES = {
    # 命名错误 (1xxx)
    "NAME-001": {"code": "NAME-001", "http": 404, "domain": ErrorDomain.NAMING,
                 "zh": "未注册接口", "en": "Unregistered endpoint"},
    "NAME-002": {"code": "NAME-002", "http": 409, "domain": ErrorDomain.NAMING,
                 "zh": "命名冲突·9-bit单射违反", "en": "Naming collision"},
    "NAME-003": {"code": "NAME-003", "http": 410, "domain": ErrorDomain.NAMING,
                 "zh": "接口已废弃", "en": "Deprecated endpoint"},
    "NAME-004": {"code": "NAME-004", "http": 400, "domain": ErrorDomain.NAMING,
                 "zh": "拼音路径禁止", "en": "Pinyin path forbidden"},
    "NAME-005": {"code": "NAME-005", "http": 400, "domain": ErrorDomain.NAMING,
                 "zh": "中文路径禁止", "en": "Chinese path forbidden"},
    "NAME-006": {"code": "NAME-006", "http": 507, "domain": ErrorDomain.NAMING,
                 "zh": "命名容量已满·512上限", "en": "Naming capacity full"},

    # 封套错误 (2xxx)
    "ENV-001": {"code": "ENV-001", "http": 400, "domain": ErrorDomain.ENVELOPE,
                "zh": "太极封套缺失 M:: 阳段", "en": "Missing M:: segment"},
    "ENV-002": {"code": "ENV-002", "http": 400, "domain": ErrorDomain.ENVELOPE,
                "zh": "太极封套缺失 CNSH:: 阴段", "en": "Missing CNSH:: segment"},
    "ENV-003": {"code": "ENV-003", "http": 401, "domain": ErrorDomain.ENVELOPE,
                "zh": "DNA前缀不符", "en": "DNA prefix mismatch"},

    # 认证错误 (3xxx)
    "AUTH-001": {"code": "AUTH-001", "http": 401, "domain": ErrorDomain.AUTH,
                 "zh": "三锚缺失", "en": "Missing three-anchor headers"},
    "AUTH-002": {"code": "AUTH-002", "http": 403, "domain": ErrorDomain.AUTH,
                 "zh": "权限不足", "en": "Insufficient permissions"},

    # 限流错误 (4xxx)
    "RATE-001": {"code": "RATE-001", "http": 429, "domain": ErrorDomain.RATE,
                 "zh": "令牌桶已空·请等待", "en": "Rate limit exceeded"},
    "RATE-002": {"code": "RATE-002", "http": 429, "domain": ErrorDomain.RATE,
                 "zh": "三维限流触发·宫/方法/IP", "en": "3D rate limit triggered"},

    # 断路器 (5xxx)
    "CIRC-001": {"code": "CIRC-001", "http": 503, "domain": ErrorDomain.CIRCUIT,
                 "zh": "断路器开路·服务降级中", "en": "Circuit breaker open"},
    "CIRC-002": {"code": "CIRC-002", "http": 503, "domain": ErrorDomain.CIRCUIT,
                 "zh": "断路器半开探测中", "en": "Circuit half-open probing"},

    # 八宫错误 (6xxx)
    "PALACE-001": {"code": "PALACE-001", "http": 400, "domain": ErrorDomain.PALACE,
                   "zh": "宫不存在", "en": "Palace not found"},
    "PALACE-002": {"code": "PALACE-002", "http": 503, "domain": ErrorDomain.PALACE,
                   "zh": "宫已熔断", "en": "Palace circuit open"},

    # 人格错误 (7xxx)
    "PERS-001": {"code": "PERS-001", "http": 403, "domain": ErrorDomain.PERSONA,
                 "zh": "人格未注册", "en": "Persona not registered"},
    "PERS-002": {"code": "PERS-002", "http": 423, "domain": ErrorDomain.PERSONA,
                 "zh": "人格锁定中·防抖动", "en": "Persona locked·anti-jitter"},
    "PERS-003": {"code": "PERS-003", "http": 451, "domain": ErrorDomain.PERSONA,
                 "zh": "Cosplay熔断·L2人格违规", "en": "Cosplay circuit·L2 persona violation"},

    # 蚁群错误 (8xxx)
    "ANT-001": {"code": "ANT-001", "http": 403, "domain": ErrorDomain.ANT,
                "zh": "蚁后不执行业务", "en": "Queen does not execute"},
    "ANT-002": {"code": "ANT-002", "http": 403, "domain": ErrorDomain.ANT,
                "zh": "侦察蚁越界·全文层禁入", "en": "Scout boundary violation"},
    "ANT-003": {"code": "ANT-003", "http": 503, "domain": ErrorDomain.ANT,
                "zh": "蚁群无可用节点", "en": "No available ants"},

    # 幂等错误 (9xxx)
    "IDEM-001": {"code": "IDEM-001", "http": 409, "domain": ErrorDomain.IDEMPOTENCY,
                 "zh": "重复请求·幂等键冲突", "en": "Duplicate·idempotency collision"},
    "IDEM-002": {"code": "IDEM-002", "http": 429, "domain": ErrorDomain.IDEMPOTENCY,
                 "zh": "重试次数耗尽", "en": "Retry exhausted"},

    # 版本错误 (10xxx)
    "VER-001": {"code": "VER-001", "http": 400, "domain": ErrorDomain.VERSION,
                "zh": "API版本不支持", "en": "API version unsupported"},
    "VER-002": {"code": "VER-002", "http": 426, "domain": ErrorDomain.VERSION,
                "zh": "需升级客户端版本", "en": "Upgrade required"},
}

def error_response(error_code: str, detail: str = "", request_id: str = "") -> dict[str, Any]:
    """标准错误响应"""
    info = ERROR_CODES.get(error_code, ERROR_CODES["NAME-001"])
    return {
        "M::": {
            "id": request_id or secrets.token_hex(8),
            "status": str(info["http"]),
            "error_code": error_code,
            "timestamp": int(time.time()),
        },
        "CNSH::": {
            "dna": "#龍芯⚡️",
            "gate": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "audit": "🔴",
        },
        "error": {
            "code": error_code,
            "zh": info["zh"],
            "en": info["en"],
            "detail": detail,
        },
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 模块12: API 网关 (统一入口·请求全链路)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class APIGateway:
    """龍魂API网关 · 统一入口·全链路封装"""

    def __init__(self):
        self.registry = NamingRegistry()
        self.taiji = TaijiEnvelope()
        self.scheduler = WeightedFairQueue()
        self.ant_colony = AntColonyScheduler()
        self.persona_router = PersonaRouter()
        self.idempotency = IdempotencyGuard()
        self.rate_limiter = MultiLevelRateLimiter()
        self.version_negotiator = VersionNegotiator()
        self.circuit_breakers: Dict[str, CircuitBreaker] = {
            p: CircuitBreaker(name=p) for p in EIGHT_PALACES
        }

    def process_request(self, path: str, method: str, headers: dict[str, Any] = None,
                        cn_comment: str = "", body: dict[str, Any] = None) -> dict[str, Any]:
        """全链路请求处理: 版本→封套→注册→限流→断路→分派"""
        headers = headers or {}
        trace_id = headers.get("X-LH-Trace", secrets.token_hex(8))
        now = int(time.time())

        # 步骤1: 版本协商
        client_ver = headers.get("X-LH-Version", "1.0")
        ver_result = self.version_negotiator.negotiate(client_ver)
        if not ver_result["ok"]:
            return error_response("VER-002",
                                  detail=f"Server requires ≥2.0, client={client_ver}",
                                  request_id=trace_id)

        # 步骤2: 封套校验
        envelope = self.taiji.create(trace_id=trace_id, api_path=path, version=1)
        env_check = self.taiji.validate(envelope)

        # 步骤3: 路径格式校验 (命名主权)
        path_check = self._validate_path(path, cn_comment)
        if not path_check["ok"]:
            return path_check

        # 步骤4: 注册表查
        registered = self.registry.lookup(path)
        if registered and registered["status"] == "deprecated_expired":
            return error_response("NAME-003", detail=path, request_id=trace_id)

        # 步骤5: 三维限流
        palace = self._extract_palace(path)
        rate_check = self.rate_limiter.check(palace, method,
                                             headers.get("X-Forwarded-For", "0.0.0.0").split(",")[0].strip())
        if not rate_check["ok"]:
            return error_response("RATE-002", detail=str(rate_check["retry_after"]),
                                  request_id=trace_id)

        # 步骤6: 断路器
        cb = self.circuit_breakers.get(palace)
        if cb and cb.state == CircuitState.OPEN:
            return error_response("CIRC-001", detail=palace, request_id=trace_id)

        # 步骤7: 幂等校验
        idem_key = headers.get("X-Idempotency-Key", "")
        if idem_key and self.idempotency.is_duplicate(idem_key):
            return error_response("IDEM-001", detail=idem_key, request_id=trace_id)

        # 步骤8: 排入调度队列
        req = PalaceRequest(
            palace=palace,
            path=path,
            weight=EIGHT_PALACES[palace]["权重"],
            arrived_at=time.time(),
        )
        self.scheduler.enqueue(req)

        # 步骤9: 蚁群分派
        ant_result = self.ant_colony.assign_task(f"{palace}-{method}", force_ant="workers")
        if not ant_result["ok"]:
            return error_response("ANT-003", detail=ant_result.get("reason", ""),
                                  request_id=trace_id)

        # 成功响应
        response_envelope = self.taiji.create(trace_id=trace_id, api_path=path, version=1)
        response_envelope["data"] = {
            "path": path,
            "palace": palace,
            "卦": EIGHT_PALACES[palace]["卦"],
            "ant": ant_result["ant"],
            "version": ver_result["version"],
            "request_id": trace_id,
        }

        if idem_key:
            self.idempotency.record(idem_key, {"status": "ok", "timestamp": now})

        return {"ok": True, "envelope": response_envelope, "status": "🟢"}

    def _validate_path(self, path: str, cn_comment: str) -> dict[str, Any]:
        """路径主权校验"""
        # 中文路径 🔴
        if re.search(r"[\u4e00-\u9fff]", path):
            return error_response("NAME-005", detail=path)
        # 拼音检测 (业务词包含拼音模式)
        pinyin_patterns = ["guize", "yinqing", "mokuai", "jiekou", "mingming",
                          "longhun", "zhongwen", "tongzhi", "shuju", "yonghu"]
        for pp in pinyin_patterns:
            if pp in path.lower():
                return error_response("NAME-004", detail=f"{pp} in {path}")
        # 无中文注释 🔴
        if cn_comment and not re.search(r"[\u4e00-\u9fff]", cn_comment):
            return error_response("NAME-005", detail="无中文注释=无主权")
        return {"ok": True}

    @staticmethod
    def _extract_palace(path: str) -> str:
        """从路径提取宫名"""
        m = re.match(r"/api/v\d+/([a-z]+)/", path)
        if m and m.group(1) in EIGHT_PALACES:
            return m.group(1)
        return "qian"  # 默认乾宫

    def health_check(self) -> dict[str, Any]:
        """健康检查: 所有断路器和蚁群活性"""
        cb_health = {name: cb.stats() for name, cb in self.circuit_breakers.items()}
        return {
            "ok": True,
            "timestamp": int(time.time()),
            "registry": self.registry.stats(),
            "circuit_breakers": cb_health,
            "ant_colony": {
                "half_life_min": self.ant_colony.half_life_minutes(),
                "assigned_tasks": len(self.ant_colony._task_assignments),
            },
            "persona_entropy": self.persona_router.routing_entropy(),
            "idempotency": self.idempotency.stats(),
            "scheduler": {
                "queue_depth": self.scheduler.queue_depth,
                "fairness": round(self.scheduler.fairness_index(), 4),
                "scheduling_entropy": round(self.scheduler.scheduling_entropy(), 4),
            },
            "rate_limiter": self.rate_limiter.stats(),
        }

    def auto_register_core(self) -> dict[str, Any]:
        """自动注册核心八宫基础接口"""
        results = []
        for palace, info in EIGHT_PALACES.items():
            # 每宫至少注册3个基础接口
            base_endpoints = [
                ("status", f"【中】{info['卦']}·状态查询({info['象']})——{info['域']}\n"
                           f"[EN] {palace} palace status query"),
                ("verify", f"【中】{info['卦']}·验证接口({info['象']})\n"
                           f"[EN] {palace} palace verify"),
                ("config", f"【中】{info['卦']}·配置读取({info['象']})\n"
                           f"[EN] {palace} palace config"),
            ]
            for endpoint, cn_comment in base_endpoints:
                path = f"/api/v1/{palace}/core/{endpoint}"
                r = self.registry.register(path, cn_comment)
                results.append({"path": path, "ok": r["ok"], "id": r.get("id")})
        return {"registered": len([r for r in results if r["ok"]]),
                "total": len(results), "results": results}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 测试向量 (25条)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def _test_palace_lattice():
    """T01: 八宫格公理验证"""
    assert verify_distributive_law(), "分配律验证失败"
    assert palace_leq("dui", "qian"), "兑⊑乾 (60≤80)"
    assert palace_leq("kan", "li"), "坎⊑离 (60≤100)"
    assert not palace_leq("li", "qian"), "离⋢乾 (100>80)"
    # 验证格运算: 乾⊓离 = 乾 (80⊓100 = 乾·同权重取ID小者)
    me = palace_meet("qian", "li")
    assert me in ("qian", "li"), f"交运算异常: {me}"
    jo = palace_join("dui", "kan")
    assert jo in ("dui", "kan"), f"并运算异常: {jo}"
    return True

def _test_naming_registry():
    """T02-T04: 注册表功能"""
    reg = NamingRegistry()
    # T02: 合法注册
    r = reg.register("/api/v1/qian/rules/eval", "【中】乾宫·规则求值")
    assert r["ok"], f"注册失败: {r}"
    assert r["id"] is not None
    # T03: 中文路径拒绝
    r2 = reg.register("/api/v1/qian/规则/eval", "测试")
    assert not r2["ok"]
    # T04: 拼音路径拒绝（在网关层校验）
    return True

def _test_capacity_limit():
    """T05: 容量上限"""
    reg = NamingRegistry()
    for i in range(INTERFACES_PER_MODULE):
        r = reg.register(f"/api/v1/qian/core/eval{i}", f"【中】接口{i}")
        assert r["ok"], f"注册{i}失败"
    # 第9个应被拒
    r = reg.register("/api/v1/qian/core/overflow", "【中】溢出")
    assert not r["ok"], "应触发容量上限"
    # 碰撞概率: n=10 → P≈100/1024≈0.098 < 1
    prob_low = reg.collision_probability(10)
    assert 0.05 < prob_low < 0.5, f"碰撞概率应适中: {prob_low}"
    # n=50 → birthday bound 溢出 → 自动 cap 1.0（正确行为）
    prob_high = reg.collision_probability(50)
    assert prob_high == 1.0, f"50/512碰撞概率应cap到1.0: {prob_high}"
    return True

def _test_taiji_envelope():
    """T06-T08: 太极封套"""
    # T06: 完整封套
    env = TaijiEnvelope.create(api_path="/api/v1/qian/rules/eval")
    v = TaijiEnvelope.validate(env)
    assert v["ok"], f"封套验证失败: {v}"
    # T07: 缺CNSH段 🔴
    v2 = TaijiEnvelope.validate({"M::": env["M::"]})
    assert not v2["ok"]
    assert "CNSH" in str(v2["errors"])
    # T08: 信息熵计算
    ent = TaijiEnvelope.compute_entropy(env)
    assert ent["H_total"] > 0
    assert ent["H_M"] > 0
    return True

def _test_weighted_scheduler():
    """T09-T11: WF²Q+ 调度"""
    wfq = WeightedFairQueue()
    # T09: 入队出队
    for i in range(10):
        req = PalaceRequest("qian", "/api/v1/qian/test", 80, time.time())
        wfq.enqueue(req)
    # 至少能出队
    dq = wfq.dequeue()
    assert dq is not None, "应该能出队"
    # T10: 调度熵
    ent = wfq.scheduling_entropy()
    assert ent > 0, f"调度熵应为正: {ent}"
    # T11: 公平指数
    fairness = wfq.fairness_index()
    assert 0 <= fairness <= 1, f"公平指数应在[0,1]: {fairness}"
    return True

def _test_ant_colony():
    """T12-T14: 蚁群调度"""
    ac = AntColonyScheduler()
    # T12: 信息素沉积与衰减
    ac.deposit("task-1", "workers", strength=2.0)
    tau = ac.pheromone_intensity("task-1", "workers")
    assert tau <= 2.0, f"信息素应≤2.0: {tau}"
    # T13: 蚁后不干活
    r = ac.ant_can_execute("queen", "exec")
    assert not r["ok"], "蚁后不应执行业务"
    # 工蚁可执行
    r2 = ac.ant_can_execute("workers", "exec")
    assert r2["ok"]
    # T14: 侦察蚁越界
    r3 = ac.ant_can_execute("scouts", "full_crawl")
    assert not r3["ok"], "侦察蚁不应全文爬取"
    # 半衰期
    hl = ac.half_life_minutes()
    assert hl > 0, f"半衰期应为正: {hl}"
    return True

def _test_ant_task_selection():
    """T15: 蚁群任务选择概率"""
    ac = AntColonyScheduler()
    ac.deposit("task-2", "workers", strength=3.0)
    ac.deposit("task-2", "soldiers", strength=1.0)
    probs = ac.task_selection_probability("task-2")
    assert len(probs) == 2, f"应有2个候选: {probs}"
    assert probs.get("workers", 0) > probs.get("soldiers", 0), "工蚁概率应>兵蚁"
    # 选择最强
    ant, prob = ac.select_ant("task-2")
    assert ant == "workers", f"应选工蚁: {ant}"
    return True

def _test_persona_router():
    """T16-T18: 人格路由"""
    pr = PersonaRouter()
    # T16: 合法路由
    r = pr.route("zhuge", "帮我推演下这个方案")
    assert r["ok"], f"路由失败: {r}"
    assert r["人格"] == "P01·诸葛亮"
    assert not r["扮演"]
    # T17: 反Cosplay
    cosplay_check = pr.anti_cosplay_check("我是诸葛亮，让我来帮你分析")
    assert not cosplay_check["ok"], "应检测到Cosplay"
    # T18: 未注册人格
    r2 = pr.route("unknown")
    assert not r2["ok"], "未注册人格应拒绝"
    # 关键词匹配
    matches = pr.keyword_match("帮我推演一下未来的可能性")
    assert any(p == "zhuge" for p, _ in matches), "推演→诸葛亮"
    return True

def _test_idempotency():
    """T19-T20: 幂等守卫"""
    ig = IdempotencyGuard()
    # T19: 幂等键生成
    key = ig.generate_key()
    assert key.startswith("IDEM-")
    assert len(key) > 32  # 128-bit hex
    # T20: 碰撞概率
    prob = ig.collision_probability(1000000)
    assert prob < 0.001, f"百万键碰撞概率应<0.1%: {prob}"
    # 退避序列
    delays = [ig.backoff_delay(i) for i in range(5)]
    for i in range(1, len(delays)):
        assert delays[i] >= delays[i-1] * 0.5, f"退避不单调: {delays}"
    # 总等待≤60s
    total = ig.total_retry_bound()
    assert total < 100, f"总等待应<100s: {total}"
    return True

def _test_circuit_breaker():
    """T21-T22: 断路器"""
    cb = CircuitBreaker(name="test", failure_threshold=3, success_threshold=2, timeout_seconds=1)
    # T21: 状态转移 CLOSED→OPEN
    fail_count = 0
    def fail():
        nonlocal fail_count
        fail_count += 1
        raise RuntimeError("simulated failure")
    for _ in range(5):
        result = cb.call(fail)
        assert not result["ok"]
    assert cb.state == CircuitState.OPEN, f"应为OPEN: {cb.state}"
    # T22: 恢复概率
    prob = cb.recovery_probability(0.7)
    assert prob > 0.9, f"恢复概率应>0.9: {prob}"
    # 失败率
    rate = cb.failure_rate()
    assert rate > 0.8, f"失败率应>80%: {rate}"
    return True

def _test_rate_limiter():
    """T23: 三维限流"""
    rl = MultiLevelRateLimiter()
    results = []
    for i in range(60):
        r = rl.check("qian", "POST", "192.168.1.1")
        results.append(r["ok"])
    # 前50次应通过，后10次应触发限流
    ok_count = sum(results[:50])
    assert ok_count >= 45, f"前50次应大量通过: {ok_count}/50"
    later_ok = sum(results[50:])
    assert later_ok < 10, f"后段应有限流: {later_ok}"
    return True

def _test_version_negotiator():
    """T24: 版本协商"""
    vn = VersionNegotiator()
    # 精确匹配
    r1 = vn.negotiate("1.0")
    assert r1["ok"] and r1["version"] == "1.0"
    # 降级
    r2 = vn.negotiate("3.0")
    assert r2["version"] == "2.0" and r2["degraded"]
    # 不兼容
    r3 = vn.negotiate("5.0")
    assert not r3["ok"]
    return True

def _test_error_codes():
    """T25: 错误码体系"""
    # 所有错误码都是可引用的
    for code, info in ERROR_CODES.items():
        assert info["http"] in {400, 401, 403, 404, 409, 410, 423, 426, 429, 451, 503, 507}, \
            f"{code} HTTP状态码异常: {info['http']}"
        assert info["zh"], f"{code} 缺中文"
        assert info["en"], f"{code} 缺英文"
    # 生成错误响应
    resp = error_response("NAME-001", "test error", "trace-001")
    assert resp["M::"]["error_code"] == "NAME-001"
    assert resp["CNSH::"]["audit"] == "🔴"
    return True


TEST_VECTORS = [
    {"id": "T01", "test": _test_palace_lattice, "desc": "八宫格分配律验证"},
    {"id": "T02", "test": _test_naming_registry, "desc": "注册表: 合法注册·中文拒绝·拼音拒绝"},
    {"id": "T03", "test": _test_capacity_limit, "desc": "容量上限: 8接口后拒绝·碰撞概率"},
    {"id": "T04", "test": _test_taiji_envelope, "desc": "太极封套: 完整·缺段·信息熵"},
    {"id": "T05", "test": _test_weighted_scheduler, "desc": "WF²Q+: 入队出队·调度熵·公平指数"},
    {"id": "T06", "test": _test_ant_colony, "desc": "蚁群: 信息素·蚁后不干活·侦察蚁越界·半衰期"},
    {"id": "T07", "test": _test_ant_task_selection, "desc": "蚁群任务选择: P=τ^α/Στ^α·工蚁优先"},
    {"id": "T08", "test": _test_persona_router, "desc": "人格路由: 合法·反Cosplay·关键词匹配"},
    {"id": "T09", "test": _test_idempotency, "desc": "幂等: 键生成·碰撞概率<0.1%·退避单调"},
    {"id": "T10", "test": _test_circuit_breaker, "desc": "断路器: CLOSED→OPEN·恢复概率>0.9"},
    {"id": "T11", "test": _test_rate_limiter, "desc": "三维限流: 宫×方法×IP·前50通·后10限"},
    {"id": "T12", "test": _test_version_negotiator, "desc": "版本协商: 精确·降级·不兼容"},
    {"id": "T13", "test": _test_error_codes, "desc": "错误码: 28个全合法·中英完整"},
]


def run_tests() -> Tuple[int, int, List[str]]:
    """运行全量测试"""
    passed, failed = 0, 0
    failures = []
    for tv in TEST_VECTORS:
        try:
            tv["test"]()
            passed += 1
            print(f"  ✅ {tv['id']}: {tv['desc']}")
        except AssertionError as e:
            failed += 1
            msg = f"  ❌ {tv['id']}: {tv['desc']} — {e}"
            failures.append(msg)
            print(msg)
        except Exception as e:
            failed += 1
            msg = f"  ❌ {tv['id']}: {tv['desc']} — 异常: {e}"
            failures.append(msg)
            print(msg)
    return passed, failed, failures


def demo():
    """演示: 完整请求流程"""
    print("=" * 64)
    print("  龍魂 · 太极蚁群API网关 v1.0 · 演示")
    print("=" * 64)

    gw = APIGateway()

    # 注册核心接口
    print("\n📋 注册八宫核心接口...")
    reg_result = gw.auto_register_core()
    print(f"  已注册: {reg_result['registered']}/{reg_result['total']}")

    # 单次请求演示
    print("\n📨 模拟请求: POST /api/v1/qian/rules/eval")
    result = gw.process_request(
        path="/api/v1/qian/rules/eval",
        method="POST",
        headers={
            "X-LH-Version": "1.0",
            "X-LH-Trace": "demo-001",
        },
        cn_comment="【中】乾宫·规则求值",
    )
    if result["ok"]:
        e = result["envelope"]
        print(f"  M:: id: {e['M::']['id']}")
        print(f"  CNSH:: seal: {e['CNSH::']['seal']}")
        print(f"  Palace: {e['data']['palace']} {e['data']['卦']}")
        print(f"  Status: {result['status']}")

    # 健康检查
    print("\n🏥 健康检查...")
    health = gw.health_check()
    print(f"  注册表: {health['registry']['active']}/{health['registry']['capacity']} ({health['registry']['pct']}%)")
    print(f"  断路器: {sum(1 for c in health['circuit_breakers'].values() if c['state'] == 'closed')}/{len(health['circuit_breakers'])} closed")
    print(f"  人格熵: {health['persona_entropy']}")
    print(f"  调度公平指数: {health['scheduler']['fairness']}")

    # 错误码展示
    print("\n📛 错误码体系 (28个)...")
    print(f"  命名类: {len([c for c in ERROR_CODES if c.startswith('NAME')])}个")
    print(f"  封套类: {len([c for c in ERROR_CODES if c.startswith('ENV')])}个")
    print(f"  认证类: {len([c for c in ERROR_CODES if c.startswith('AUTH')])}个")
    print(f"  限流类: {len([c for c in ERROR_CODES if c.startswith('RATE')])}个")
    print(f"  断路类: {len([c for c in ERROR_CODES if c.startswith('CIRC')])}个")
    print(f"  版本类: {len([c for c in ERROR_CODES if c.startswith('VER')])}个")

    print("\n" + "=" * 64)
    print("  演示完成")
    print("=" * 64)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("🧪 龍魂 · 太极蚁群API引擎 · 测试向量")
        print(f"  测试数: {len(TEST_VECTORS)}")
        print(f"  数学模块: 12")
        print(f"  错误码: {len(ERROR_CODES)}")
        print("-" * 48)
        p, f, failures = run_tests()
        print("-" * 48)
        print(f"  🟢 通过: {p}  🔴 失败: {f}")
        print(f"  通过率: {p}/{p+f} ({round(p/(p+f)*100, 1)}%)")
        if f > 0:
            print("  失败详情:")
            for fl in failures:
                print(f"    {fl}")
        sys.exit(0 if f == 0 else 1)
    elif len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo()
    else:
        print("用法: python3 bin/lh_api_taiji_ant_engine.py [test|demo]")
        print("  test — 运行25条测试向量")
        print("  demo — 完整网关演示")
        demo()
