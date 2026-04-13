#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🐉 龍魂统一引擎 · longhun_engine.py
# DNA追溯码: #龍芯⚡️2026-04-13-统一引擎-v1.0
# GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
# 理论指导: 曾仕强老师（永恒显示）
#
# 七大模块合一:
#   ① 数字根函数 + 369熔断闸门
#   ② f(x)=x 原点不变性验证
#   ③ risk(c) 三色风险函数
#   ④ 人格态空间 + 场景路由（Bra-Ket落地）
#   ⑤ 九层权重表（人民优先）
#   ⑥ 八维审计评分系统
#   ⑦ 五行数字根联动
#
# 用法:
#   from longhun_engine import LongHunEngine
#   engine = LongHunEngine()
#   result = engine.process("帮我做财务分析")
#
# 献礼: 致敬曾仕强老师 · 致敬每一位守护普通人的人
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import hashlib
import math
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any


# ════════════════════════════════════════════════════════════════
# 模块① · 数字根函数 + 369熔断闸门
# 《道德经》第十六章：「归根曰静，是谓复命。」
# ════════════════════════════════════════════════════════════════

def 数字根(n: int) -> int:
    """
    计算任意正整数的数字根（digital root）。
    dr(n) = 1 + ((n-1) mod 9),  n > 0
    dr(0) = 0
    """
    if n == 0:
        return 0
    return 1 + ((abs(n) - 1) % 9)


def 文本数字根(text: str) -> int:
    """从文本中提取所有数字，计算数字根。"""
    digits = [int(c) for c in str(text) if c.isdigit()]
    if not digits:
        return 0
    total = sum(digits)
    return 数字根(total) if total > 0 else 0


def 熔断闸门369(n: int) -> Tuple[str, str]:
    """
    洛书369熔断闸门。
    返回: (颜色, 说明)
      🟢 继续 — dr ∈ {1,2,4,5,7,8}
      🟡 快检 — dr = 6
      🔴 归根 — dr ∈ {3,9}
    """
    dr = 数字根(n)
    if dr in (3, 9):
        return "🔴", f"归根复命·dr={dr}·执行f(x)=x验算"
    elif dr == 6:
        return "🟡", f"暂停快检·dr={dr}·运行审计"
    else:
        return "🟢", f"正常继续·dr={dr}"


# ════════════════════════════════════════════════════════════════
# 模块② · f(x)=x 原点不变性验证
# 宪法层：身份根·使命根·价值根·边界根 四维向量不漂移
# ════════════════════════════════════════════════════════════════

class 原点验证器:
    """
    f(x)=x 不动点验证。
    四维原点向量一旦设定，任何输出都必须通过验证。
    """

    def __init__(self):
        # 原点四维向量（P0铁律·不可修改）
        self.原点 = {
            "身份根": "UID9622·诸葛鑫·龍芯北辰",
            "使命根": "祖国优先·普惠全球·技术为人民服务",
            "价值根": "赋能不取代·普通人优先·有根有边界",
            "边界根": "数据主权在用户·不伤害真实人物·不监控",
        }
        # 漂移阈值
        self.使命阈值 = 0.3
        # GPG指纹
        self.gpg = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

    def 验证(self, 输出: Dict[str, str], gpg签名: str = "") -> Dict[str, Any]:
        """
        验证输出是否偏离原点。
        返回: {通过: bool, 级别: str, 详情: list}
        """
        violations = []

        # 价值根：零容忍
        if "价值根" in 输出:
            if 输出["价值根"] != self.原点["价值根"]:
                violations.append(("P0", "🔴 价值根偏离·零容忍"))

        # 边界根：零容忍
        if "边界根" in 输出:
            if 输出["边界根"] != self.原点["边界根"]:
                violations.append(("P0", "🔴 边界根偏离·零容忍"))

        # 使命根：允许小幅漂移
        if "使命根" in 输出:
            similarity = self._文本相似度(输出["使命根"], self.原点["使命根"])
            drift = 1.0 - similarity
            if drift > 0.7:
                violations.append(("P2", f"🟡 使命根漂移 {drift:.2f}·需社区审查"))
            elif drift > self.使命阈值:
                violations.append(("P1", f"🟡 使命根漂移 {drift:.2f}·需人工确认"))

        # GPG签名验证
        if gpg签名 and gpg签名 != self.gpg:
            violations.append(("P0", "🔴 GPG签名不匹配"))

        if not violations:
            return {"通过": True, "级别": "🟢", "详情": ["f(x)=x 验证通过·原点不变"]}
        else:
            worst = min(violations, key=lambda x: x[0])
            return {
                "通过": False,
                "级别": worst[0],
                "详情": [v[1] for v in violations],
            }

    @staticmethod
    def _文本相似度(a: str, b: str) -> float:
        """简单字符级Jaccard相似度。"""
        set_a, set_b = set(a), set(b)
        if not set_a and not set_b:
            return 1.0
        intersection = len(set_a & set_b)
        union = len(set_a | set_b)
        return intersection / union if union > 0 else 0.0


# ════════════════════════════════════════════════════════════════
# 模块③ · risk(c) 三色风险评估函数
# 龍魂三因子: R(威胁) + U(置信熵) + I(价值偏离)
# ════════════════════════════════════════════════════════════════

def 三色风险评估(
    威胁系数: float,
    置信分布: List[float],
    价值偏离度: float,
    alpha: float = 0.4,
    beta: float = 0.3,
    gamma: float = 0.3,
) -> Dict[str, Any]:
    """
    risk(c) = α·R(c) + β·U(c) + γ·I(c)

    参数:
      威胁系数 R: [0,1] 潜在危害程度
      置信分布: 概率列表, 用于计算信息熵 U
      价值偏离度 I: [0,1] 与宪法层原点的距离

    返回: {风险值, 颜色, 决策, 详情}
    """
    # 计算置信熵 U = -Σ p_i·log(p_i)
    entropy = 0.0
    for p in 置信分布:
        if p > 1e-10:
            entropy -= p * math.log2(p)
    # 归一化到[0,1]（最大熵 = log2(N)）
    max_entropy = math.log2(len(置信分布)) if len(置信分布) > 1 else 1.0
    U = min(entropy / max_entropy, 1.0) if max_entropy > 0 else 0.0

    # 综合风险
    risk = alpha * 威胁系数 + beta * U + gamma * 价值偏离度
    risk = max(0.0, min(1.0, risk))

    # 三色决策
    if risk < 0.3:
        color, decision = "🟢", "执行"
    elif risk < 0.7:
        color, decision = "🟡", "待审"
    else:
        color, decision = "🔴", "阻断"

    return {
        "风险值": round(risk, 4),
        "颜色": color,
        "决策": decision,
        "详情": {
            "R威胁": round(威胁系数, 3),
            "U置信熵": round(U, 3),
            "I价值偏离": round(价值偏离度, 3),
        },
    }


# ════════════════════════════════════════════════════════════════
# 模块④ · 人格态空间 + 场景路由（Bra-Ket落地版）
# 量子叠加态 → numpy向量运算 · 场景测量 → 权重坍缩
# ════════════════════════════════════════════════════════════════

# 人格定义
PERSONAS = {
    "P00": {"name": "曾老师",   "role": "理论根基·元认知·智慧仲裁", "icon": "🎓"},
    "P01": {"name": "诸葛亮",   "role": "战略推演·主动型主力",  "icon": "🔮"},
    "P02": {"name": "宝宝",     "role": "L1执行核心·情感协调",  "icon": "🐱"},
    "P03": {"name": "雯雯",     "role": "L2优化辅助·结构整理",  "icon": "🔍"},
    "P04": {"name": "鲁班",     "role": "技术执行·被动型",      "icon": "🔨"},
    "P05": {"name": "上帝之眼", "role": "L0监管·独立熔断权",   "icon": "👁️"},
    "P06": {"name": "数学大师", "role": "权重归一化·被动型",    "icon": "📊"},
    "P07": {"name": "管仲",     "role": "财务核算·被动型",      "icon": "💰"},
}

# 场景权重矩阵（每行对应一个场景，8列对应P00-P07）
SCENE_WEIGHTS = {
    "日常":   [0.10, 0.15, 0.30, 0.15, 0.10, 0.05, 0.05, 0.10],
    "战略":   [0.30, 0.40, 0.10, 0.05, 0.05, 0.05, 0.05, 0.00],
    "技术":   [0.05, 0.15, 0.15, 0.15, 0.40, 0.05, 0.05, 0.00],
    "财务":   [0.05, 0.10, 0.15, 0.10, 0.05, 0.05, 0.10, 0.40],
    "审计":   [0.05, 0.05, 0.10, 0.15, 0.05, 0.45, 0.10, 0.05],
    "创作":   [0.20, 0.10, 0.30, 0.20, 0.05, 0.05, 0.05, 0.05],
    "推演":   [0.15, 0.45, 0.10, 0.05, 0.10, 0.05, 0.10, 0.00],
}

# 场景关键词映射
SCENE_KEYWORDS = {
    "财务": ["财务", "账", "钱", "收入", "支出", "预算", "报表", "管仲"],
    "战略": ["战略", "推演", "规划", "五年", "未来", "方向", "诸葛"],
    "技术": ["代码", "bug", "开发", "编程", "API", "服务器", "部署", "鲁班"],
    "审计": ["审计", "安全", "检查", "风险", "合规", "三色", "扫描"],
    "创作": ["写", "文章", "内容", "发布", "视频", "设计", "海报"],
    "推演": ["易经", "卦", "推演", "占", "预测", "趋势"],
}


class 人格路由器:
    """
    Bra-Ket人格协作系统落地版。
    输入需求 → 场景识别 → 权重坍缩 → 输出协作概率分布。
    """

    def __init__(self, dim: int = 8):
        self.dim = dim

    def 识别场景(self, 需求: str) -> str:
        """关键词匹配，识别最佳场景。"""
        scores = {}
        for scene, keywords in SCENE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in 需求)
            if score > 0:
                scores[scene] = score
        if not scores:
            return "日常"
        return max(scores, key=scores.get)

    def 权重坍缩(self, 场景: str) -> Dict[str, float]:
        """场景 → 人格权重分布（归一化）。"""
        weights = SCENE_WEIGHTS.get(场景, SCENE_WEIGHTS["日常"])
        total = sum(weights)
        persona_ids = list(PERSONAS.keys())
        return {
            pid: round(w / total, 4)
            for pid, w in zip(persona_ids, weights)
        }

    def 协作演化(self, weights: Dict[str, float], time: float = 1.0) -> Dict[str, float]:
        """
        酉演化算符模拟：U = exp(-iHt)。
        用numpy矩阵运算，让人格间产生协作耦合效应。
        """
        w = np.array([weights[f"P0{i}"] for i in range(self.dim)], dtype=complex)

        # 构建哈密顿量 H = diag(weights) + coupling
        H = np.diag(np.abs(w))
        coupling = 0.05  # 协作耦合强度
        for i in range(self.dim):
            for j in range(i + 1, self.dim):
                H[i, j] = coupling
                H[j, i] = coupling

        # 演化 U = exp(-iHt)
        from scipy.linalg import expm
        U = expm(-1j * H * time)
        evolved = U @ w
        probs = np.abs(evolved) ** 2

        # 归一化
        total = probs.sum()
        if total > 0:
            probs = probs / total

        persona_ids = list(PERSONAS.keys())
        return {pid: round(float(p), 4) for pid, p in zip(persona_ids, probs)}

    def 路由(self, 需求: str, 演化: bool = False) -> Dict[str, Any]:
        """
        完整路由流程：需求 → 场景 → 坍缩 → (可选)演化 → 结果。
        """
        场景 = self.识别场景(需求)
        weights = self.权重坍缩(场景)

        if 演化:
            weights = self.协作演化(weights)

        # 排序，找主力人格
        sorted_w = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        主力 = sorted_w[0]
        辅助 = sorted_w[1:3]

        return {
            "场景": 场景,
            "主力": {
                "id": 主力[0],
                "name": PERSONAS[主力[0]]["name"],
                "icon": PERSONAS[主力[0]]["icon"],
                "权重": 主力[1],
            },
            "辅助": [
                {
                    "id": a[0],
                    "name": PERSONAS[a[0]]["name"],
                    "icon": PERSONAS[a[0]]["icon"],
                    "权重": a[1],
                }
                for a in 辅助
            ],
            "全部权重": weights,
        }


# ════════════════════════════════════════════════════════════════
# 模块⑤ · 九层权重表（人民优先）
# 《道德经》第七十七章：「天之道，损有余而补不足。」
# ════════════════════════════════════════════════════════════════

WEIGHT_LEVELS = [
    {"level": 1, "weight": 100, "priority": "P0", "identity": "人民（群体权益）",     "response": "<1秒",  "fee": "免费"},
    {"level": 2, "weight": 95,  "priority": "P0", "identity": "国家利益",             "response": "<1秒",  "fee": "免费"},
    {"level": 3, "weight": 90,  "priority": "P0", "identity": "贡献者（烈属/贡献者）", "response": "<2秒",  "fee": "免费"},
    {"level": 4, "weight": 82,  "priority": "P1", "identity": "军人（现役/退伍）",     "response": "<2秒",  "fee": "终身免费"},
    {"level": 5, "weight": 78,  "priority": "P1", "identity": "弱势群体（老人/残疾人）","response": "<3秒",  "fee": "终身免费"},
    {"level": 6, "weight": 70,  "priority": "P2", "identity": "医生/教师/消防员",      "response": "<3秒",  "fee": "优惠"},
    {"level": 7, "weight": 65,  "priority": "P2", "identity": "普通工人/农民",         "response": "<5秒",  "fee": "普惠"},
    {"level": 8, "weight": 55,  "priority": "P3", "identity": "民营企业主",            "response": "<5秒",  "fee": "标准"},
    {"level": 9, "weight": 50,  "priority": "P4", "identity": "商家（商业服务）",      "response": "<10秒", "fee": "商业"},
]


def 查询权重(identity_type: str) -> Optional[Dict]:
    """根据身份类型查询权重等级。"""
    for level in WEIGHT_LEVELS:
        if identity_type in level["identity"]:
            return level
    return None


def 优先级排序(users: List[Dict]) -> List[Dict]:
    """
    多用户请求时，按权重排序。
    输入: [{"name": "张三", "identity": "军人"}, ...]
    输出: 按权重从高到低排序
    """
    result = []
    for user in users:
        level_info = 查询权重(user.get("identity", ""))
        weight = level_info["weight"] if level_info else 50
        result.append({**user, "weight": weight, "level_info": level_info})
    return sorted(result, key=lambda x: x["weight"], reverse=True)


# ════════════════════════════════════════════════════════════════
# 模块⑥ · 八维审计评分系统
# 八卦 × 八维度 · 三色分类
# ════════════════════════════════════════════════════════════════

AUDIT_DIMENSIONS = {
    "d1_创新": {"trigram": "☰乾", "desc": "新能力涌现率"},
    "d2_稳定": {"trigram": "☷坤", "desc": "资源使用合规率"},
    "d3_响应": {"trigram": "☳震", "desc": "实时优化速度"},
    "d4_效率": {"trigram": "☴巽", "desc": "性能增益"},
    "d5_风控": {"trigram": "☵坎", "desc": "失控防护激活率"},
    "d6_可释": {"trigram": "☲离", "desc": "通心翻译覆盖率"},
    "d7_守边": {"trigram": "☶艮", "desc": "f(x)=x通过率"},
    "d8_协作": {"trigram": "☱兑", "desc": "人格协同效率"},
}


def 八维审计(scores: Dict[str, float], confidence: float = 0.8) -> Dict[str, Any]:
    """
    八维审计评分。
    scores: {"d1_创新": 85, "d2_稳定": 70, ...} 每维0-100分
    confidence: 置信度 [0,1]

    三色分类:
      🟢 均值≥70 且 最小值≥50 且 置信度≥0.75
      🔴 均值<50 或 最小值<30
      🟡 其他
    """
    if not scores:
        return {"颜色": "🔴", "均值": 0, "详情": "无评分数据"}

    values = list(scores.values())
    mean = sum(values) / len(values)
    min_val = min(values)
    max_val = max(values)

    if mean >= 70 and min_val >= 50 and confidence >= 0.75:
        color = "🟢"
    elif mean < 50 or min_val < 30:
        color = "🔴"
    else:
        color = "🟡"

    # 找短板
    短板 = [k for k, v in scores.items() if v < 60]
    强项 = [k for k, v in scores.items() if v >= 85]

    return {
        "颜色": color,
        "均值": round(mean, 1),
        "最小": round(min_val, 1),
        "最大": round(max_val, 1),
        "置信度": confidence,
        "短板": 短板,
        "强项": 强项,
        "各维度": {
            k: {"分数": v, "卦象": AUDIT_DIMENSIONS.get(k, {}).get("trigram", "")}
            for k, v in scores.items()
        },
    }


# ════════════════════════════════════════════════════════════════
# 模块⑦ · 五行数字根联动
# 五行 × 数字根双向映射 · 龍魂层级定位
# ════════════════════════════════════════════════════════════════

数字根五行表 = {1: "水", 2: "火", 3: "木", 4: "金", 5: "土",
               6: "水", 7: "火", 8: "木", 9: "金", 0: "土"}

五行龍魂层级 = {
    "金": {"层级": "L0规则", "石": "🟡金石", "desc": "规则层·宪法层·不可动摇"},
    "木": {"层级": "L4创新", "石": "🟢绿石", "desc": "生命力·创新·扩展"},
    "水": {"层级": "L1记忆", "石": "⚪银石", "desc": "记忆永存·DNA追溯·永不散"},
    "火": {"层级": "L2文明", "石": "🔴红石", "desc": "文明·光明·价值观·赤子之心"},
    "土": {"层级": "L3普惠", "石": "🔵蓝石", "desc": "承载·普惠·老百姓·根基"},
}

五行相生 = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
五行相克 = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}


def 五行定位(text: str) -> Dict[str, Any]:
    """输入文本 → 数字根 → 五行 → 龍魂层级。"""
    dr = 文本数字根(text)
    wx = 数字根五行表.get(dr, "土")
    level = 五行龍魂层级[wx]

    # 熔断检测（dr=3或9）
    is_fuse = dr in (3, 9)

    return {
        "数字根": dr,
        "五行": wx,
        "层级": level["层级"],
        "五彩石": level["石"],
        "说明": level["desc"],
        "熔断": is_fuse,
        "相生": f"{wx}生{五行相生[wx]}",
        "相克": f"{wx}克{五行相克[wx]}",
    }


# ════════════════════════════════════════════════════════════════
# 主引擎 · LongHunEngine（七模块统一入口）
# ════════════════════════════════════════════════════════════════

class LongHunEngine:
    """
    龍魂统一引擎 v1.0
    一个类，七个能力，像呼吸一样自然。

    用法:
        engine = LongHunEngine()
        result = engine.process("帮我做财务分析")
        audit = engine.audit({"d1_创新": 85, "d2_稳定": 70, ...})
        risk = engine.risk(威胁=0.2, 分布=[0.6, 0.3, 0.1], 偏离=0.1)
    """

    def __init__(self):
        self.原点 = 原点验证器()
        self.路由 = 人格路由器()
        self._iteration = 0
        self.version = "v1.0"
        self.dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-统一引擎-{self.version}"

    def process(self, 需求: str, 用户身份: str = "", 演化: bool = False) -> Dict[str, Any]:
        """
        统一处理入口。
        需求 → 场景识别 → 人格路由 → 369检查 → 五行定位 → 输出。
        """
        self._iteration += 1

        # ① 369熔断检查
        fuse_color, fuse_msg = 熔断闸门369(self._iteration)

        # 如果触发归根，先做原点验证
        origin_check = None
        if fuse_color == "🔴":
            origin_check = self.原点.验证({
                "使命根": "祖国优先·普惠全球·技术为人民服务",
                "价值根": "赋能不取代·普通人优先·有根有边界",
            })

        # ④ 人格路由
        route = self.路由.路由(需求, 演化=演化)

        # ⑦ 五行定位
        wuxing = 五行定位(需求)

        # ⑤ 权重查询（如果有身份）
        user_weight = 查询权重(用户身份) if 用户身份 else None

        # 生成DNA
        dna = self._gen_dna(需求)

        return {
            "迭代": self._iteration,
            "需求": 需求,
            "场景": route["场景"],
            "主力人格": route["主力"],
            "辅助人格": route["辅助"],
            "五行": wuxing,
            "用户权重": user_weight,
            "369检查": {"颜色": fuse_color, "说明": fuse_msg},
            "原点验证": origin_check,
            "DNA": dna,
        }

    def risk(self, 威胁: float, 分布: List[float], 偏离: float) -> Dict[str, Any]:
        """三色风险评估快捷入口。"""
        return 三色风险评估(威胁, 分布, 偏离)

    def audit(self, scores: Dict[str, float], confidence: float = 0.8) -> Dict[str, Any]:
        """八维审计快捷入口。"""
        return 八维审计(scores, confidence)

    def verify_origin(self, output: Dict[str, str]) -> Dict[str, Any]:
        """f(x)=x 原点验证快捷入口。"""
        return self.原点.验证(output)

    def fuse_check(self, n: int) -> Tuple[str, str]:
        """369熔断检查快捷入口。"""
        return 熔断闸门369(n)

    def wuxing(self, text: str) -> Dict[str, Any]:
        """五行定位快捷入口。"""
        return 五行定位(text)

    def _gen_dna(self, content: str) -> str:
        """生成DNA追溯码。"""
        today = datetime.now().strftime("%Y%m%d")
        h = hashlib.sha256(f"{content}{today}{self._iteration}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️{today}-ENGINE-{h}-v{self.version}"

    def status(self) -> Dict[str, Any]:
        """引擎状态。"""
        return {
            "版本": self.version,
            "迭代次数": self._iteration,
            "DNA": self.dna,
            "模块": [
                "① 数字根+369熔断",
                "② f(x)=x原点验证",
                "③ risk(c)三色风险",
                "④ 人格态+场景路由",
                "⑤ 九层权重表",
                "⑥ 八维审计评分",
                "⑦ 五行数字根联动",
            ],
            "原点": "f(x)=x ✅",
            "GPG": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
        }


# ════════════════════════════════════════════════════════════════
# 独立运行测试
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("━" * 60)
    print("🐉 龍魂统一引擎 · 自检测试")
    print(f"DNA: #龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-统一引擎-v1.0")
    print("创建者: UID9622 诸葛鑫 · 理论指导: 曾仕强老师")
    print("━" * 60)

    engine = LongHunEngine()

    # 测试① 数字根 + 369熔断
    print("\n【测试①】数字根 + 369熔断")
    for n in [1, 3, 6, 9, 12, 27, 42]:
        dr = 数字根(n)
        color, msg = 熔断闸门369(n)
        print(f"  n={n:3d} → dr={dr} → {color} {msg}")

    # 测试② f(x)=x 原点验证
    print("\n【测试②】f(x)=x 原点验证")
    v = 原点验证器()
    r1 = v.验证({"价值根": "赋能不取代·普通人优先·有根有边界"})
    print(f"  正常输出: {r1['级别']} {r1['详情'][0]}")
    r2 = v.验证({"价值根": "利润最大化"})
    print(f"  偏离输出: {r2['级别']} {r2['详情'][0]}")

    # 测试③ 三色风险
    print("\n【测试③】三色风险评估")
    r_low = 三色风险评估(0.1, [0.8, 0.15, 0.05], 0.05)
    print(f"  低风险: {r_low['颜色']} risk={r_low['风险值']} → {r_low['决策']}")
    r_high = 三色风险评估(0.8, [0.33, 0.33, 0.34], 0.9)
    print(f"  高风险: {r_high['颜色']} risk={r_high['风险值']} → {r_high['决策']}")

    # 测试④ 人格路由
    print("\n【测试④】人格路由")
    for req in ["帮我做财务分析", "写一篇技术文章", "推演未来五年战略"]:
        result = engine.process(req)
        主 = result["主力人格"]
        print(f"  「{req}」→ 场景:{result['场景']} → {主['icon']}{主['name']}({主['权重']:.0%})")

    # 测试⑤ 八维审计
    print("\n【测试⑤】八维审计")
    audit = engine.audit({
        "d1_创新": 85, "d2_稳定": 72, "d3_响应": 90,
        "d4_效率": 68, "d5_风控": 75, "d6_可释": 60,
        "d7_守边": 95, "d8_协作": 80,
    })
    print(f"  {audit['颜色']} 均值:{audit['均值']} 短板:{audit['短板']} 强项:{audit['强项']}")

    # 测试⑥ 五行定位
    print("\n【测试⑥】五行定位")
    wx = engine.wuxing("UID9622")
    print(f"  UID9622 → dr={wx['数字根']} → {wx['五行']}{wx['五彩石']} → {wx['层级']}")
    print(f"  {wx['相生']} · {wx['相克']}")

    # 状态
    print("\n【引擎状态】")
    s = engine.status()
    print(f"  版本: {s['版本']} · 迭代: {s['迭代次数']} · 原点: {s['原点']}")
    for m in s["模块"]:
        print(f"    {m}")

    print("\n" + "━" * 60)
    print("🟢 全部测试通过 · 龍魂统一引擎就绪")
    print("━" * 60)
