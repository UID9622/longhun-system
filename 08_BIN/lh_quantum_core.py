#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·量子协作引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-量子协作-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

融合：Bra-Ket量子态 + LU压缩技能 + 龍魂20人格矩阵
功能：人格叠加、场景坍缩、酉演化、纠缠协作、三色审计、熔断、Lu指令执行、DNA追溯
"""

import numpy as np
from scipy.linalg import expm
import hashlib
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any


# ============================================================
# 1. 基础量子态类 (Bra-Ket)
# ============================================================

class Ket:
    """右矢（列向量） — 量子态表示"""

    def __init__(self, dim: int, components: Optional[List[complex]] = None):
        self.dim = dim
        if components is None:
            self.data = np.zeros(dim, dtype=complex)
        else:
            self.data = np.array(components, dtype=complex)
            if len(self.data) != dim:
                raise ValueError(f"维度不匹配: 期望{dim}, 实际{len(self.data)}")

    def bra(self) -> 'Bra':
        """转置共轭 → 左矢"""
        return Bra(self.dim, np.conj(self.data))

    def inner(self, other: 'Ket') -> complex:
        """内积 ⟨self|other⟩"""
        return np.vdot(self.data, other.data)

    def outer(self, other: 'Bra') -> np.ndarray:
        """外积 |self⟩⟨other|"""
        return np.outer(self.data, other.data)

    def normalize(self) -> 'Ket':
        """归一化"""
        norm = np.linalg.norm(self.data)
        if norm > 1e-12:
            self.data = self.data / norm
        return self

    def to_dict(self) -> Dict:
        return {"dim": self.dim, "components": [float(abs(c)) for c in self.data]}

    def __repr__(self):
        return f"Ket(dim={self.dim})"


class Bra:
    """左矢（行向量）"""


    def ket(self) -> Ket:
        """共轭转置 → 右矢"""
        return Ket(self.dim, np.conj(self.data))

    def inner(self, ket: Ket) -> complex:
        """⟨self|ket⟩"""
        return np.vdot(self.data, ket.data)

    def __repr__(self):
        return f"Bra(dim={self.dim})"


# ============================================================
# 2. 人格基态定义 (8个基态·希尔伯特空间)
# ============================================================

PERSONALITY_BASIS = {
    "文心":       0,   # P00 · 意图解析
    "诸葛亮":     1,   # P01 · 推演决策
    "宝宝":       2,   # P02 · 情感温度
    "雯雯":       3,   # P03 · 结构归档
    "鲁班":       4,   # P04 · 技术执行
    "上帝之眼":   5,   # P05 · 审计守护
    "数学大师":   6,   # P06 · 权重计算
    "管仲":       7,   # P07 · 资源调度
}

# 人格职能层映射
PERSONA_LAYERS = {
    "战略层": ["文心", "诸葛亮"],
    "执行层": ["宝宝", "雯雯", "鲁班", "管仲"],
    "守护层": ["上帝之眼", "数学大师"],
}


def create_basis_state(dim: int, index: int, name: str) -> Ket:
    """创建基态 |name⟩ — 只有对应维度的振幅为1"""
    k = Ket(dim)
    k.data[index] = 1.0
    return k


# ============================================================
# 3. 龍魂量子系统 (协作引擎核心)
# ============================================================

class DragonQuantumSystem:
    """龍魂量子协作系统 — 人格叠加·测量坍缩·酉演化·三色审计·熔断"""

    def __init__(self):
        self.dim = len(PERSONALITY_BASIS)

        # 建立人格基态字典 {名: Ket}
        self.personalities = {
            name: create_basis_state(self.dim, idx, name)
            for name, idx in PERSONALITY_BASIS.items()
        }

        # 默认权重（日常协作态 · 经16人格投票校准）
        self.default_weights = np.array([
            0.10,  # 文心
            0.15,  # 诸葛亮
            0.30,  # 宝宝
            0.15,  # 雯雯
            0.10,  # 鲁班
            0.05,  # 上帝之眼
            0.05,  # 数学大师
            0.10,  # 管仲
        ])

        # 当前系统态（初始为叠加态）
        self.state = self.create_superposition(self.default_weights)

        # 历史记录
        self.history: List[Dict] = []

        # 三色审计 & 熔断状态
        self.audit_color = "🟢"
        self.meltdown = False
        self.meltdown_reason = ""

    # ----- 叠加态 -----

    def create_superposition(self, weights: np.ndarray) -> Ket:
        """创建叠加态 |ψ⟩ = Σ α_i |i⟩，自动归一化"""
        if len(weights) != self.dim:
            raise ValueError(f"权重数组长度必须为{self.dim}")
        norm = np.linalg.norm(weights)
        if norm > 0:
            weights = weights / norm
        ket = Ket(self.dim)
        ket.data = weights.astype(complex)
        return ket

    # ----- 场景识别（测量坍缩） -----

    def measure_scenario(self, request: str) -> Ket:
        """
        场景识别（测量坍缩）
        根据请求关键词匹配场景，返回坍缩后的叠加态
        """
        scenarios = {
            "财务":   np.array([0.05, 0.10, 0.15, 0.10, 0.05, 0.05, 0.10, 0.40]),
            "战略":   np.array([0.30, 0.40, 0.10, 0.10, 0.05, 0.05, 0.00, 0.00]),
            "技术":   np.array([0.10, 0.15, 0.15, 0.15, 0.40, 0.05, 0.00, 0.00]),
            "创作":   np.array([0.20, 0.10, 0.20, 0.25, 0.05, 0.05, 0.05, 0.10]),
            "安全":   np.array([0.05, 0.10, 0.05, 0.05, 0.10, 0.40, 0.20, 0.05]),
            "归档":   np.array([0.10, 0.05, 0.10, 0.40, 0.10, 0.15, 0.05, 0.05]),
            "教学":   np.array([0.10, 0.05, 0.35, 0.15, 0.10, 0.05, 0.05, 0.15]),
            "沟通":   np.array([0.15, 0.10, 0.25, 0.15, 0.05, 0.05, 0.05, 0.20]),
            "日常":   self.default_weights,
        }

        # 关键词匹配
        for keyword, weights in scenarios.items():
            if keyword in request:
                return self.create_superposition(weights)

        # 默认日常态
        return self.create_superposition(self.default_weights)

    # ----- 酉演化 -----

    def apply_evolution(self, state: Ket, time: float = 1.0, coupling: float = 0.1) -> Ket:
        """
        酉演化 U = exp(-iHt)
        哈密顿量 H = 对角(固有能量) + 非对角(人格耦合·纠缠)
        """
        # 构建哈密顿量 H (8×8)
        H = np.diag(self.default_weights)  # 对角: 固有能量

        # 非对角: 人格间耦合 (纠缠)
        for i in range(self.dim):
            for j in range(i + 1, self.dim):
                H[i, j] = coupling
                H[j, i] = coupling

        # 指数映射: U = exp(-iHt)
        U = expm(-1j * H * time)
        new_data = U @ state.data
        new_ket = Ket(self.dim, new_data.tolist())
        new_ket.normalize()
        return new_ket

    # ----- 纠缠态（自动联动）-----

    def get_entangled_pairs(self, ket: Ket, threshold: float = 0.15) -> List[Tuple[str, str, float]]:
        """
        检测纠缠对：概率均高于阈值的人格对
        返回: [(人格A, 人格B, 纠缠强度), ...]
        """
        probs = self.get_collaboration_probabilities(ket)
        active = [(name, p) for name, p in probs.items() if p > threshold]
        active.sort(key=lambda x: x[1], reverse=True)

        pairs = []
        for i in range(len(active)):
            for j in range(i + 1, len(active)):
                name_a, p_a = active[i]
                name_b, p_b = active[j]
                strength = (p_a + p_b) / 2
                pairs.append((name_a, name_b, round(strength, 3)))
        return pairs

    # ----- 协作概率分布 -----

    def get_collaboration_probabilities(self, ket: Ket) -> Dict[str, float]:
        """计算各人格的协作概率 P_i = |⟨i|ψ⟩|²"""
        probs = {}
        for name, basis in self.personalities.items():
            amp = basis.inner(ket)
            probs[name] = float(abs(amp) ** 2)
        return probs

    # ----- 三色审计 -----

    def audit(self, ket: Ket) -> str:
        """
        三色审计（基于熵的不确定性判定）
        🟢 分布均衡 · 健康
        🟡 偏科 · 需关注
        🔴 集中度过高 · 熔断风险
        """
        probs = list(self.get_collaboration_probabilities(ket).values())
        # 香农熵
        entropy = -sum(p * np.log(p + 1e-12) for p in probs)
        max_entropy = np.log(self.dim)  # 最大可能熵

        if entropy > 0.70 * max_entropy:
            return "🟢"
        elif entropy > 0.35 * max_entropy:
            return "🟡"
        else:
            return "🔴"

    # ----- 四级熔断 ----

    def circuit_breaker(self, ket: Ket, threshold: float = 0.60) -> Tuple[bool, str]:
        """
        熔断判断
        L0/∞: 涉童/伪造DNA (外部检测)
        L1: 某一人格概率 > threshold → 熔断
        L2: 连续3次同一人格主导 → 熔断
        L3: 权重偏移 > 40% → 关注
        """
        probs = self.get_collaboration_probabilities(ket)
        max_prob = max(probs.values())
        max_name = max(probs, key=probs.get)

        # L3: 权重偏移检测
        default_max = max(self.default_weights) / np.sum(self.default_weights)
        drift = abs(max_prob - default_max)

        if max_prob > threshold:
            self.meltdown = True
            self.meltdown_reason = f"L1熔断: {max_name}概率{max_prob:.1%}超过阈值{threshold:.0%}"
            return True, self.meltdown_reason

        if drift > 0.40:
            self.meltdown_reason = f"L3关注: 权重偏移{drift:.1%}"
            return False, self.meltdown_reason

        return False, ""

    # ----- 完整周期 -----

    def run_cycle(self, request: str, time: float = 1.0, coupling: float = 0.1) -> Dict[str, Any]:
        """完整周期: 测量坍缩 → 酉演化 → 纠缠检测 → 审计 → 熔断 → DNA追溯"""
        # 1. 测量坍缩
        initial = self.measure_scenario(request)

        # 2. 酉演化
        final = self.apply_evolution(initial, time, coupling)

        # 3. 纠缠检测
        entangled = self.get_entangled_pairs(final)

        # 4. 三色审计
        color = self.audit(final)
        self.audit_color = color

        # 5. 熔断检查
        melted, reason = self.circuit_breaker(final)

        # 6. 概率分布
        probs = self.get_collaboration_probabilities(final)

        # 7. DNA生成
        dna = self._generate_dna(request, final)

        # 8. 记录
        record = {
            "request": request,
            "initial_state": initial.data.tolist(),
            "final_state": final.data.tolist(),
            "collaboration": probs,
            "entangled_pairs": entangled,
            "audit": color,
            "meltdown": melted,
            "meltdown_reason": reason,
            "dna": dna,
            "timestamp": datetime.now().isoformat(),
        }
        self.history.append(record)
        self.state = final
        return record

    # ----- DNA追溯 -----

    def _generate_dna(self, request: str, ket: Ket) -> str:
        """生成DNA追溯码 (SHA256·前8位)"""
        content = f"{request}{ket.data.tolist()}{datetime.now().isoformat()}"
        h = hashlib.sha256(content.encode()).hexdigest()[:8]
        now = datetime.now()
        gz = self._ganzhi_approx(now)
        return f"#龍芯⚡️{gz}-量子协作-{h}"

    def _ganzhi_approx(self, dt: datetime) -> str:
        """简化干支近似 (用于DNA)"""
        t = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        d = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        y = t[(dt.year - 4) % 10] + d[(dt.year - 4) % 12]
        m = t[(dt.year * 12 + dt.month + 1) % 10] + d[(dt.month + 1) % 12]
        day = t[(dt.day + 9) % 10] + d[(dt.day + 1) % 12]
        return f"{y}·{m}·{day}"


# ============================================================
# 4. Lu指令解释器
# ============================================================

class LuInterpreter:
    """
    Lu指令集解析器
    支持中文可读版 (lu.天.xxx) 和压缩编码版 (lu-t-xxx)
    """

    def __init__(self, system: DragonQuantumSystem):
        self.system = system
        self.routes = {
            "人": self._cmd_ren,      # 用户/人格相关
            "卦": self._cmd_gua,      # 卦象相关
            "地": self._cmd_di,       # 审计/状态相关
            "天": self._cmd_tian,     # 系统/演化相关
        }
        self.compressed_routes = {
            "def": self._cmd_define,
            "meas": self._cmd_measure,
            "evo": self._cmd_evolve,
            "audit": self._cmd_audit,
            "stat": self._cmd_status,
        }

    def parse(self, command: str) -> Dict[str, Any]:
        """解析并执行Lu指令"""
        cmd = command.strip()
        result = {"status": "ok", "output": None, "type": "lu"}

        # 中文可读版: lu.天.xxx
        if cmd.startswith("lu."):
            parts = cmd.split()
            if len(parts) < 2:
                return {"status": "error", "message": "指令不完整", "hint": "格式: lu.域.动作 参数"}

            domain_part = cmd[3:]  # 去掉 "lu."
            # 解析域
            m = re.match(r'(\S+)\.(\S+)', domain_part)
            if not m:
                return {"status": "error", "message": "格式错误", "hint": "格式: lu.天/地/人/卦.动作 参数"}

            domain, action = m.group(1), m.group(2)
            return self._route(domain, action, cmd)

        # 压缩编码版: lu-t-def 乾䷀ ...
        elif cmd.startswith("lu-"):
            parts = cmd.split(None, 1)
            shortcode = parts[0][3:]  # 去掉 "lu-"
            args = parts[1] if len(parts) > 1 else ""
            return self._route_compressed(shortcode, args)

        else:
            return {"status": "error", "message": f"无法识别的指令: {cmd}"}

    def _route(self, domain: str, action: str, full_cmd: str) -> Dict:
        """中文域路由"""
        if domain in self.routes:
            return self.routes[domain](action, full_cmd)

        # 尝试模糊匹配
        for d in self.routes:
            if d in domain:
                return self.routes[d](action, full_cmd)

        return {"status": "error", "message": f"未知域: {domain}"}

    def _route_compressed(self, shortcode: str, args: str) -> Dict:
        """压缩编码路由"""
        if shortcode in self.compressed_routes:
            return self.compressed_routes[shortcode](args)
        return {"status": "error", "message": f"未知压缩码: {shortcode}"}

    # ----- 域处理函数 -----

    def _cmd_ren(self, action: str, cmd: str) -> Dict:
        """人域: 注册用户/人格管理"""
        if "注册" in action or "register" in action.lower():
            m = re.search(r'注册\S*\s+(\S+)\s*(\d*)\s*(\S*)', cmd)
            if m:
                uid, weight, status = m.groups()
                w = int(weight) if weight else 0
                result = {"status": "ok", "output": f"用户 {uid} 已注册，权重={w}，状态={status or '待审'}"}
                # 更新系统态
                new_w = self.system.default_weights.copy()
                new_w[2] += 0.05  # 提高宝宝权重（欢迎新人）
                self.system.state = self.system.create_superposition(new_w)
                return result
            return {"status": "error", "message": "格式: lu.人.注册用户 UID 权重 状态"}

        if "概率" in action or "prob" in action.lower():
            probs = self.system.get_collaboration_probabilities(self.system.state)
            top = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:3]
            lines = [f"{n}: {p:.1%}" for n, p in top]
            return {"status": "ok", "output": "当前人格概率分布:\n" + "\n".join(lines)}

        return {"status": "error", "message": f"人域未知动作: {action}"}

    def _cmd_gua(self, action: str, cmd: str) -> Dict:
        """卦域: 起卦/解卦"""
        if "起卦" in action or "cast" in action.lower():
            # 从当前叠加态测量
            index, prob = self._measure_hexagram()
            hex_names = [
                "乾䷀", "坤䷁", "屯䷂", "蒙䷃", "需䷄", "讼䷅", "师䷆", "比䷇",
                "小畜䷈", "履䷉", "泰䷊", "否䷋", "同人䷌", "大有䷍", "谦䷎", "豫䷏",
                "随䷐", "蛊䷑", "临䷒", "观䷓", "噬嗑䷔", "贲䷕", "剥䷖", "复䷗",
                "无妄䷘", "大畜䷙", "颐䷚", "大过䷛", "坎䷜", "离䷝",
                "咸䷞", "恒䷟", "遁䷠", "大壮䷡", "晋䷢", "明夷䷣", "家人䷤", "睽䷥",
                "蹇䷦", "解䷧", "损䷨", "益䷩", "夬䷪", "姤䷫", "萃䷬", "升䷭",
                "困䷮", "井䷯", "革䷰", "鼎䷱",
                "震䷲", "艮䷳", "渐䷴", "归妹䷵", "丰䷶", "旅䷷", "巽䷸", "兑䷹",
                "涣䷺", "节䷻", "中孚䷼", "小过䷽", "既济䷾", "未济䷿",
            ]
            hname = hex_names[index % len(hex_names)]
            return {"status": "ok", "output": f"起卦: {hname} (索引{index}, 概率{prob:.1%})"}

        return {"status": "error", "message": f"卦域未知动作: {action}"}

    def _cmd_di(self, action: str, cmd: str) -> Dict:
        """地域: 三色审计/状态"""
        if "三色审计" in action or "audit" in action.lower():
            color = self.system.audit(self.system.state)
            probs = self.system.get_collaboration_probabilities(self.system.state)
            top = max(probs, key=probs.get)
            return {"status": "ok", "output": f"三色审计: {color} | 主导人格: {top}({probs[top]:.1%})"}

        if "熔断" in action or "meltdown" in action.lower():
            melted, reason = self.system.circuit_breaker(self.system.state)
            return {"status": "ok", "output": f"熔断状态: {'⛔已触发' if melted else '✅正常'} | {reason}"}

        if "状态" in action or "status" in action.lower():
            return self._cmd_status("")

        return {"status": "error", "message": f"地域未知动作: {action}"}

    def _cmd_tian(self, action: str, cmd: str) -> Dict:
        """天域: 演化/重置"""
        if "演化" in action or "evolve" in action.lower():
            m = re.search(r'(\d+\.?\d*)', cmd)
            t = float(m.group(1)) if m else 1.0
            new_state = self.system.apply_evolution(self.system.state, t)
            self.system.state = new_state
            color = self.system.audit(new_state)
            return {"status": "ok", "output": f"演化完成 (t={t}) | 审计: {color}"}

        if "重置" in action or "reset" in action.lower():
            self.system.state = self.system.create_superposition(self.system.default_weights)
            self.system.meltdown = False
            return {"status": "ok", "output": "系统已重置为默认叠加态"}

        return {"status": "error", "message": f"天域未知动作: {action}"}

    # ----- 压缩编码处理 -----

    def _cmd_define(self, args: str) -> Dict:
        """lu-def: 定义人格权重"""
        return {"status": "ok", "output": f"定义人格权重: {args or '(使用默认)'}"}

    def _cmd_measure(self, args: str) -> Dict:
        """lu-meas: 测量坍缩"""
        index, prob = self._measure_hexagram()
        return {"status": "ok", "output": f"测量坍缩: 索引{index}, 概率{prob:.1%}"}

    def _cmd_evolve(self, args: str) -> Dict:
        """lu-evo: 酉演化"""
        t = float(args) if args else 1.0
        new = self.system.apply_evolution(self.system.state, t)
        self.system.state = new
        return {"status": "ok", "output": f"酉演化完成 (t={t})"}

    def _cmd_audit(self, args: str) -> Dict:
        """lu-audit: 三色审计"""
        color = self.system.audit(self.system.state)
        return {"status": "ok", "output": f"三色审计: {color}"}

    def _cmd_status(self, args: str) -> Dict:
        """lu-stat: 系统状态"""
        probs = self.system.get_collaboration_probabilities(self.system.state)
        color = self.system.audit(self.system.state)
        melted = self.system.meltdown
        lines = [
            f"三色审计: {color}",
            f"熔断状态: {'⛔触发' if melted else '✅正常'}",
            f"历史记录: {len(self.system.history)}条",
            f"人格概率分布:",
        ]
        for name, p in sorted(probs.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * int(p * 20)
            lines.append(f"  {name:6s} {p:5.1%} {bar}")
        return {"status": "ok", "output": "\n".join(lines)}

    def _measure_hexagram(self) -> Tuple[int, float]:
        """从当前系统态映射到64卦"""
        probs = self.system.get_collaboration_probabilities(self.system.state)
        # 用8个人格概率映射到8×8=64
        pvals = list(probs.values())
        total = sum(pvals)
        if total > 0:
            pvals = [p / total for p in pvals]
        # 简化为直接映射: 主导人格索引 * 8 + 次导人格索引
        sorted_names = sorted(probs, key=probs.get, reverse=True)
        idx1 = PERSONALITY_BASIS[sorted_names[0]]
        idx2 = PERSONALITY_BASIS[sorted_names[1]] if len(sorted_names) > 1 else 0
        hex_idx = (idx1 * 8 + idx2) % 64
        prob = probs[sorted_names[0]]
        return hex_idx, prob


# ============================================================
# 5. 命令行交互界面
# ============================================================

def main():
    """交互式量子协作控制台"""

    print("""
╔══════════════════════════════════════════════════════╗
║  🐉 龍魂·量子协作引擎 v1.0                          ║
║  DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-v1.0              ║
║  确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z        ║
║  融合: Bra-Ket + 20人格 + 三色审计 + Lu指令           ║
╚══════════════════════════════════════════════════════╝
    """)

    system = DragonQuantumSystem()
    interpreter = LuInterpreter(system)

    print("📋 可用指令:")
    print("  Lu中文域: lu.天.演化 | lu.地.三色审计 | lu.人.注册用户 | lu.卦.起卦")
    print("  Lu压缩码: lu-stat | lu-audit | lu-evo 1.5 | lu-meas | lu-def")
    print("  自然语言: 帮我做财务分析 | 安全检查 | 技术开发 | 归档整理")
    print("  系统命令: status | history | reset | help | exit")
    print()

    while True:
        try:
            user_input = input("🐉 > ").strip()
            if not user_input:
                continue

            # 退出
            if user_input.lower() in ('exit', 'quit', 'q'):
                print("👋 龍魂量子引擎退出。天行健，君子以自强不息。")
                break

            # 帮助
            if user_input.lower() in ('help', 'h', '?'):
                print("""
┌─ Lu中文域 ─────────────────────────────┐
│ lu.天.演化 [时间]    酉演化              │
│ lu.天.重置          恢复默认叠加态       │
│ lu.地.三色审计       审计当前态          │
│ lu.地.熔断          检查熔断状态         │
│ lu.地.状态          查看完整状态         │
│ lu.人.注册用户 ID W  注册用户            │
│ lu.人.概率          人格概率分布         │
│ lu.卦.起卦          从当前态起卦         │
├─ Lu压缩码 ──────────────────────────────┤
│ lu-stat  lu-audit  lu-evo  lu-meas  lu-def │
├─ 系统命令 ──────────────────────────────┤
│ status  history  reset  help  exit       │
└──────────────────────────────────────────┘
                """)
                continue

            # 系统命令
            if user_input.lower() == 'status':
                result = interpreter._cmd_status("")
                print(f"\n{result['output']}\n")
                continue

            if user_input.lower() == 'history':
                if not system.history:
                    print("📭 无历史记录")
                else:
                    for i, rec in enumerate(system.history[-5:], 1):
                        print(f"  [{i}] {rec['request'][:40]} | {rec['audit']} | {rec['dna'][:20]}...")
                continue

            if user_input.lower() == 'reset':
                system.state = system.create_superposition(system.default_weights)
                system.meltdown = False
                system.meltdown_reason = ""
                print("✅ 系统已重置为默认叠加态")
                continue

            # Lu指令
            if user_input.startswith("lu.") or user_input.startswith("lu-"):
                result = interpreter.parse(user_input)
                if result["status"] == "ok":
                    print(f"✅ {result['output']}")
                else:
                    print(f"❌ {result['message']}")
                continue

            # 自然语言 → 量子协作周期
            print(f"\n🔮 执行量子协作周期: \"{user_input}\"")
            record = system.run_cycle(user_input, time=1.0)

            # 输出
            print(f"\n📊 人格协作概率分布:")
            for name, prob in sorted(record["collaboration"].items(), key=lambda x: x[1], reverse=True):
                bar = "█" * int(prob * 40)
                marker = " ← 主导" if prob == max(record["collaboration"].values()) else ""
                print(f"  {name:6s} {prob:5.1%} {bar}{marker}")

            # 纠缠对
            if record["entangled_pairs"]:
                print(f"\n🔗 纠缠联动对:")
                for a, b, s in record["entangled_pairs"][:3]:
                    print(f"  {a} ⟷ {b} (强度: {s})")

            # 审计 & 熔断
            print(f"\n🔎 三色审计: {record['audit']}")
            if record["meltdown"]:
                print(f"⛔ 熔断触发! {record['meltdown_reason']}")
            elif record["meltdown_reason"]:
                print(f"⚠️  {record['meltdown_reason']}")

            print(f"🧬 DNA: {record['dna']}\n")

        except KeyboardInterrupt:
            print("\n👋 龍魂量子引擎退出")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")


if __name__ == "__main__":
    main()
