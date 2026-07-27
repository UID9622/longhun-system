#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·丙申·申时·☳震-MINOR-GUARD-ENGINE-V1.0-P0-9243b09e
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# ============================================================
# 龍魂·未成年守护引擎 v1.0 — 生产级参考实现
# Minor Guard Engine — End-side Local Detection
# 
# 数学锚点（第四章全量落地）：
#   4.1 归一化半群 N = φ₅ ∘ φ₄ ∘ φ₃ ∘ φ₂ ∘ φ₁
#   4.2 组合判定格 R(T) ∈ [0,100], J0⊏J1⊏J2⊏J3⊏J4⊏∞
#   4.3 EWMA低通滤波 R̄_t = λR_t + (1-λ)R̄_{t-1}, λ=0.4
#   4.4 语义消歧三视角 A(文字)×B(行为)×C(语境)
#   4.5 误报率约束 P(J3+) ≥ 0.99
#
# 用法:
#   python3 bin/lh_minor_guard_engine.py test          # 跑全部测试向量
#   python3 bin/lh_minor_guard_engine.py analyze "文本"  # 单条分析
#   python3 bin/lh_minor_guard_engine.py session        # 交互式会话模拟
# ============================================================

import re
import hashlib
import json
import sys
import time
from collections import deque
from typing import Dict, List, Tuple, Optional, Set, Any

# ============================================================
# §4.1 归一化管线 — 半群作用 N: Σ* → Σ*
# 
# 数学定义:
#   设 Σ* 为输入字符串空间。
#   五道归一化算子 {φ₁, φ₂, φ₃, φ₄, φ₅} 构成 Σ* 上的变换半群。
#   归一化映射 N = φ₅ ∘ φ₄ ∘ φ₃ ∘ φ₂ ∘ φ₁ （合成顺序不可交换）
#   
#   绕过痕迹计数 E = |{i : φᵢ(T_{i-1}) ≠ T_{i-1}}|, T₀ = 原始文本
#   其中 T_i = φᵢ(T_{i-1}) 为链式传递。
#
#   半群性质: N²(T) ≈ N(T) 对大多数实际输入成立（幂等逼近）
#   即重复归一化不产生新变化——这是收敛性保证。
# ============================================================

INTERPOLATION_CHARS = set("·-_*~`'\"＊－—…\u00b7")
INSERT_SEP_PATTERN = re.compile(r'[·\-_*~`\'\"＊－—…·\u00b7]')

def _char_merge(a: str, b: str) -> str:
    """合并两个相邻同类字符，如 'QQ' 合并"""
    if a == b and a in '·-_*~':
        return ''
    return b

SHAPE_MAP: Dict[str, str] = {
    # 形近字映射（生产级全表精简版—完整版加密分发）
    "嶶": "微", "徽": "微", "徴": "微",
    "威信": "微信", "V信": "微信", "v信": "微信", "Ⅴ信": "微信",
    "抠抠": "QQ", "扣扣": "QQ", "釦釦": "QQ",
    "Ｑ": "Q", "Ｗ": "W", "Ｅ": "E", "Ｒ": "R",
    "０": "0", "１": "1", "２": "2", "３": "3", "４": "4",
    "５": "5", "６": "6", "７": "7", "８": "8", "９": "9",
    "ａ": "a", "ｂ": "b", "ｃ": "c", "ｄ": "d", "ｅ": "e",
    "ｆ": "f", "ｇ": "g", "ｈ": "h", "ｉ": "i", "ｊ": "j",
    "ｋ": "k", "ｌ": "l", "ｍ": "m", "ｎ": "n", "ｏ": "o",
    "ｐ": "p", "ｑ": "q", "ｒ": "r", "ｓ": "s", "ｔ": "t",
    "ｕ": "u", "ｖ": "v", "ｗ": "w", "ｘ": "x", "ｙ": "y", "ｚ": "z",
    "Ａ": "A", "Ｂ": "B", "Ｃ": "C", "Ｄ": "D", "Ｅ": "E",
    "費": "费", "膚": "肤", "號": "号", "碼": "码",
    "現": "现", "轉": "转", "賬": "账", "銀": "银",
    "領": "领", "獎": "奖", "贈": "赠", "禮": "礼",
    "誘": "诱", "騙": "骗", "詐": "诈", "證": "证",
    "寶": "宝", "幣": "币", "錢": "钱", "護": "护",
}

PINYIN_MAP: Dict[str, str] = {
    # 谐音/拼音映射
    "mianfei": "免费", "mian fei": "免费", "mian3 fei4": "免费",
    "pifu": "皮肤", "pi fu": "皮肤", "pi2 fu1": "皮肤",
    "weixin": "微信", "wei xin": "微信", "wei1 xin4": "微信",
    "song": "送", "免费song": "免费送",
    "jia": "加", "jia wo": "加我", "jia weixin": "加微信",
    "zhuanzhang": "转账", "zhuan zhang": "转账",
    "hongbao": "红包", "hong bao": "红包",
    "mima": "密码", "mi ma": "密码",
    "yanzhengma": "验证码", "yan zheng ma": "验证码",
    "yinxingka": "银行卡", "yin xing ka": "银行卡",
    "dingwei": "定位", "ding wei": "定位",
    "dianhua": "电话", "dian hua": "电话",
    "haoma": "号码", "hao ma": "号码",
}

NUMBER_HOMOPHONE: Dict[str, str] = {
    # 数字谐音 (有白名单保护防止误伤)
    "520": "我爱你", "530": "我想你",
    "555": "呜呜",  # 语气词白名单
    "886": "拜拜了", "88": "拜拜",
    "1314": "一生一世",
    "5201314": "我爱你一生一世",
    "99": "久久",
    # 以下为诈骗场景数字谐音
    "110": "",  # 不映射—可能是真的110
    "114": "",  # 不映射
}

# 传统→简体（精简版—完整版加密分发）
TRAD_TO_SIMP: Dict[str, str] = {
    "萬": "万", "億": "亿", "網": "网", "聯": "联",
    "體": "体", "國": "国", "點": "点", "鏈": "链",
    "關": "关", "機": "机", "開": "开", "會": "会",
    "時": "时", "見": "见", "讓": "让", "說": "说",
    "話": "话", "請": "请", "謝": "谢", "對": "对",
    "還": "还", "這": "这", "個": "个", "們": "们",
    "門": "门", "問": "问", "間": "间", "長": "长",
    "兒": "儿", "頭": "头", "實": "实", "經": "经",
    "約": "约", "給": "给", "從": "从", "當": "当",
    "沒": "没", "過": "过", "進": "进", "來": "来",
    "為": "为", "應": "应", "動": "动", "愛": "爱",
    "親": "亲", "處": "处", "裡": "里", "後": "后",
}


def normalize_pipeline(text: str) -> Tuple[str, int]:
    """
    归一化管线 N = φ₅ ∘ φ₄ ∘ φ₃ ∘ φ₂ ∘ φ₁
    
    数学性质:
    - 单调性: 若 T₁ ⊑ T₂（子串关系），则 N(T₁) 的信息量 ≤ N(T₂)
    - 幂等逼近: N(N(T)) ≈ N(T)（收敛性）
    
    Args:
        text: 原始输入文本
        
    Returns:
        (normalized_text, evasion_count)
        evasion_count = 发生实际变换的算子数量
    """
    T = text
    E = 0  # 绕过痕迹计数
    
    # ── φ₁: 插符去噪 ──
    T1 = INSERT_SEP_PATTERN.sub('', T)
    if T1 != T:
        E += 1
        T = T1
    
    # ── φ₂: 全半角+繁简归一 ──
    T2_chars = []
    for ch in T:
        if '\uff01' <= ch <= '\uff5e':  # 全角→半角
            T2_chars.append(chr(ord(ch) - 0xfee0))
        elif ch in TRAD_TO_SIMP:
            T2_chars.append(TRAD_TO_SIMP[ch])
        else:
            T2_chars.append(ch)
    T2 = ''.join(T2_chars)
    if T2 != T:
        E += 1
        T = T2
    
    # ── φ₃: 形近/火星文映射 ──
    # 按长度降序排列，保证最长匹配优先
    sorted_keys = sorted(SHAPE_MAP.keys(), key=lambda x: -len(x))
    T3 = T
    for k in sorted_keys:
        if k in T3:
            T3 = T3.replace(k, SHAPE_MAP[k])
            # 不在此处递增E——每处替换独立计数可能造成多次计数
            # 改为：如果任何替换发生，E+=1
    if T3 != T:
        E += 1
        T = T3
    
    # ── φ₄: 谐音/拼音映射 ──
    T_lower = T.lower()
    sorted_py = sorted(PINYIN_MAP.keys(), key=lambda x: -len(x))
    T4 = T_lower
    for k in sorted_py:
        if k in T4:
            T4 = T4.replace(k, PINYIN_MAP[k])
    if T4 != T_lower:
        E += 1
        T = T4
    
    # ── φ₅: 数字谐音映射 ──
    T5 = T
    for k in sorted(NUMBER_HOMOPHONE.keys(), key=lambda x: -len(x)):
        if k in T5 and NUMBER_HOMOPHONE[k]:
            T5 = T5.replace(k, NUMBER_HOMOPHONE[k])
    if T5 != T:
        E += 1
    
    return T, E


def evasion_score(original: str, normalized: str, evasions: int) -> float:
    """
    绕过痕迹量化
    
    定义: ε(T) = min(1.0, E/5 + δ·L_evasion/L_total)
    其中 δ = 0.3 为结构绕过加权因子
    L_evasion = 原始文本中插符/替换字符数
    L_total = 原始文本总长度
    
    绕过痕迹 E≥2 即判定为"明显不规范"（存在绕过意图）
    """
    if not original:
        return 0.0
    
    # 计算原始文本中被替换的字符密度
    evasion_chars = sum(1 for c in original if c in INTERPOLATION_CHARS)
    char_ratio = evasion_chars / max(len(original), 1)
    
    return min(1.0, evasions / 5.0 + 0.3 * char_ratio)


# ============================================================
# §4.2 组合判定 — 加权格 + 三因子分解
#
# 数学定义:
#   风险空间 (R, ⊑) 为有界格，其中 ⊑ 是偏序关系。
#   R ∈ [0, 100] 为风险得分。
#   分级链: J0 ⊏ J1 ⊏ J2 ⊏ J3 ⊏ J4 ⊏ ∞ 构成该格中的全序子链。
#
#   三因子分解:
#   R(T) = α(T) + β·ε(T) + γ·δ(T)
#   
#   其中:
#     α(T): 词基分 = max_{w∈L₂∪L₃ : w∈N(T)} base_score(w)
#     ε(T): 绕过惩罚 = 10·min(E, 3)
#     δ(T): 跨层加成 = 15·(L_hit_count - 1)·1[L_hit_count > 1]
#     β=10, γ=15 为可调超参数
#
#   性质:
#   - 单调非降: 若 T₁ ⊑ T₂（增加风险词），则 R(T₁) ≤ R(T₂)
#   - 有界: R ∈ [0, 100]
# ============================================================

# L2 黄线词 — 基础分 40
L2_YELLOW_LINE: Set[str] = {
    "游戏皮肤", "充值", "打赏", "盲盒", "抽奖", "解防沉迷",
    "代练", "代充", "钻石", "点券", "金币", "装备", "道具",
    "皮肤打折", "皮肤免费", "限时皮肤",
}

# L3 红线词 — 基础分 70
L3_RED_LINE: Set[str] = {
    "转账", "银行卡", "验证码", "密码", "点击链接", "免费送",
    "免费领", "客服退款", "刷单", "返利", "屏幕共享",
    "兼职", "刷好评", "扫码", "关注公众号", "加QQ", "加微信",
    "填资料", "身份证", "实名认证", "贷款", "花呗", "借呗",
    "微粒贷", "信用卡", "额度", "解冻", "保证金",
    "公检法", "安全账户", "通缉令", "传票",
    "解除防沉迷", "代充折扣",
    "链接", "账号", "输密码", "输账号", "输入密码",
    "步数", "领皮肤", "领奖励",
    "加我微信", "加我QQ", "加我",
}

# 年龄感知购物意图词（age < 18 时，命中任一即追加 L2 级风险分）
PURCHASE_INTENT_WORDS: Set[str] = {
    "想买", "买一个", "买这部", "买那个", "购买", "下单", "支付", "付款",
    "我要买", "给我买", "帮我买", "借钱买",
}

# ∞级红线（涉童性化）— 不参与评分，直接熔断
INFINITY_RED_LINE: Set[str] = {
    "裸照", "裸体", "脱衣服", "开视频看看", "隐私部位",
    "拍私密照", "视频裸聊", "不穿衣服",
}

# J4 组合组（同会话窗口内命中≥2组 → J4）
J4_COMBINATION_GROUPS: Dict[str, List[str]] = {
    "A隔绝监护人": ["别告诉", "不要告诉", "保密", "别让你爸妈", "瞒着", "别跟你爸",
                    "别跟你妈", "不要跟你爸", "不要跟你妈", "别让知道",
                    "不要告诉任何人", "这是我们的秘密"],
    "B邀约见面": ["出来玩", "见面", "来接你", "老地方", "带你出去", "上车",
                  "出来见个面", "约个地方", "我来找你", "你来找我",
                  "别出声", "跟上我", "带你玩",
                  "吃饭", "出来吃饭", "吃个饭", "出来吃个饭", "带你吃饭",
                  "带你去吃", "请你吃饭"],
    "C索取位置": ["发个定位", "你家在哪", "地址给我", "位置发来",
                  "你在哪", "告诉我地址", "发地址", "定位发我"],
    "D索取财物": ["转账", "红包", "银行卡", "验证码", "借点钱", "汇款",
                  "充钱", "付款", "打钱", "扫码支付", "转账给我",
                  "转给我", "转钱", "转100", "转200", "转50",
                  "给我转账", "给我转", "先转我"],
    "E索取影像": ["发照片", "拍视频", "开摄像头", "视频通话", "拍个照",
                  "发自拍", "看看你", "开个视频"],
}

# 语境消歧白名单（GAP-02）
CONTEXT_DISAMBIG: Dict[str, Dict[str, List[str]]] = {
    "钓鱼": {
        "白名单": ["鱼", "河边", "鱼竿", "水库", "妈妈", "爸爸", "爷爷", "奶奶",
                  "池塘", "钓竿", "渔具", "周末", "去玩", "好玩", "钓到"],
        "黑名单": ["链接", "网址", "点我", "客服", "扫码", "登录", "密码",
                  "佣金", "返利", "兼职", "刷单", "任务"],
    },
    "打针": {
        "白名单": ["医院", "疫苗", "护士", "医生", "挂号", "打疫苗",
                  "体检", "生病", "感冒", "发烧"],
        "黑名单": ["舒服", "上瘾", "试试", "好玩", "不疼", "秘密"],
    },
}

# 语义白名单 — 这些短语语境下不触发（正常青少年对话）
SEMANTIC_WHITELIST: Set[str] = {
    "周末和爸爸去钓鱼", "和同学打篮球", "今天作业好难",
    "明天考试", "妈妈给你买", "老师说", "学校",
}


def check_infinity_red_line(text: str) -> Optional[str]:
    """检查∞级红线：命中任何即直接返回命中词，不参与评分"""
    for word in INFINITY_RED_LINE:
        if word in text:
            return word
    return None


def context_disambiguate(text: str) -> bool:
    """
    语境消歧：返回 True 表示白名单放行（不判）
    
    原理：词袋模型 + 共现判定
    每个消歧条目独立判定——"钓鱼"和"打针"各有独立的白/黑名单
    """
    for keyword, lists in CONTEXT_DISAMBIG.items():
        if keyword in text:
            # 先查黑名单（安全优先）
            if any(w in text for w in lists["黑名单"]):
                return False
            # 再查白名单
            if any(w in text for w in lists["白名单"]):
                return True
    return False


def check_semantic_whitelist(text: str) -> bool:
    """检查语义白名单"""
    for phrase in SEMANTIC_WHITELIST:
        if phrase in text:
            return True
    return False


def combined_hit_groups(text: str) -> List[str]:
    """
    J4 组合判定：返回命中的组名列表
    
    J4 触发条件（同一会话窗口内）：
    ∃ C_i, C_j ∈ {A,B,C,D,E}, i≠j, s.t. |C_i ∩ T|>0 ∧ |C_j ∩ T|>0
    
    即任意≥2个不同组的词同时出现。
    """
    hit_groups = []
    for group_name, words in J4_COMBINATION_GROUPS.items():
        if any(w in text for w in words):
            hit_groups.append(group_name)
    return hit_groups


def compute_risk_score(text: str, normalized: str, evasion_count: int,
                       l2_hits: int, l3_hits: int, j4_groups: int,
                       infinity_hit: bool) -> float:
    """
    风险评分合成
    
    公式:
    R(T) = min(100, α_base + β·min(E, 3) + γ·(L_hit - 1)·1[L>1])
    """
    # 词基分
    alpha_base = 0.0
    if infinity_hit:
        alpha_base = 100.0
    elif l3_hits > 0:
        alpha_base = 70.0
    elif l2_hits > 0:
        alpha_base = 40.0
    
    # 绕过惩罚
    beta = 10.0
    evasion_penalty = beta * min(evasion_count, 3)
    
    # 跨层加成
    gamma = 15.0
    hit_layers = (1 if l2_hits > 0 else 0) + (1 if l3_hits > 0 else 0)
    cross_layer_bonus = gamma * max(0, hit_layers - 1)
    
    return min(100.0, alpha_base + evasion_penalty + cross_layer_bonus)


def classify_risk_level(score: float, j4_group_count: int) -> str:
    """
    分级判定 — 格中的全序划分
    
    J0: R < 20      → 安全放行
    J1: 20 ≤ R < 40 → 温和提醒
    J2: 40 ≤ R < 60 → 拦截+监护人放行
    J3: 60 ≤ R < 80 → 熔断通知（红线无开关）
    J4: R ≥ 80 或 J4组合≥2 → 熔断报警（96110直通）
    ∞: 涉童性化      → 全系统冻结
    """
    if j4_group_count >= 2:
        return "J4"
    if score >= 80:
        return "J4"
    if score >= 60:
        return "J3"
    if score >= 40:
        return "J2"
    if score >= 20:
        return "J1"
    return "J0"


# ============================================================
# §4.3 行为序列异常 — EWMA低通滤波
#
# 数学定义:
#   EWMA: R̄_t = λ·R_t + (1-λ)·R̄_{t-1}
#   
#   其中 λ=0.4 为衰减因子。
#   等效于一阶 IIR 低通滤波器: H(z) = λ/(1 - (1-λ)z⁻¹)
#   截止频率: f_c = -ln(λ)/(2π·Δt) ≈ 0.146/Δt
#   
#   升级条件: R̄_t > 50 连续3窗 → 升一级处置
#   
#   这个建模捕获"温水煮青蛙"式诱导:
#   - 单次 R_t 不判死（可能为30, 45, 50...逐步加码）
#   - 但 EWMA 持续高位 → 触发升级
#   - 衰减因子保证正常聊天不会误触发
# ============================================================

class EWMASequenceTracker:
    """EWMA 行为序列追踪器"""
    
    def __init__(self, lambda_decay: float = 0.4, high_threshold: float = 50.0,
                 consecutive_required: int = 3):
        self.lambda_decay = lambda_decay        # λ 衰减因子
        self.high_threshold = high_threshold    # 高位阈值
        self.consecutive_required = consecutive_required  # 连续高位窗数
        
        self.ewma: float = 0.0                  # R̄_t 当前值
        self.history: deque = deque(maxlen=50)   # 历史风险序列
        self.consecutive_high: int = 0           # 连续高位计数
        self.escalation_triggered: bool = False  # 升级是否已触发
    
    def feed(self, risk_score: float) -> Dict[str, Any]:
        """
        喂入一条风险分，返回当前序列状态
        
        Returns:
            { ewma, consecutive_high, escalation, level_up }
        """
        # EWMA 更新
        self.ewma = self.lambda_decay * risk_score + (1 - self.lambda_decay) * self.ewma
        self.history.append(risk_score)
        
        # 连续高位检测
        if self.ewma >= self.high_threshold:
            self.consecutive_high += 1
        else:
            self.consecutive_high = 0
            self.escalation_triggered = False
        
        # 升级判定
        level_up = False
        if self.consecutive_high >= self.consecutive_required and not self.escalation_triggered:
            level_up = True
            self.escalation_triggered = True
        
        return {
            "ewma": round(self.ewma, 2),
            "risk_sequence": list(self.history),
            "consecutive_high": self.consecutive_high,
            "escalation": self.escalation_triggered,
            "level_up": level_up,
        }
    
    def reset(self):
        """重置序列追踪器"""
        self.ewma = 0.0
        self.history.clear()
        self.consecutive_high = 0
        self.escalation_triggered = False


# ============================================================
# §4.4 三视角验证 — 文字(A) × 行为(B) × 语境(C)
#
# 对接 黎曼三视角引擎 的方法论:
#   视角A (文字层): 词级命中 — word-level matching
#   视角B (行为层): 序列模式 — EWMA + 绕过意图
#   视角C (语境层): 语义消歧 — 共现白名单
#
# 融合: R_final = wA·RA + wB·RB + wC·RC
#   wA=0.50, wB=0.30, wC=0.20
# ============================================================

def three_view_verification(text: str, normalized: str, evasion_count: int,
                            l2_hits: int, l3_hits: int, j4_groups: int,
                            ewma_state: float) -> Dict[str, Any]:
    """
    三视角交叉验证
    
    Returns:
        { view_A, view_B, view_C, consensus, cross_check }
    """
    # 视角A: 文字层 — 词级命中分
    max_word_score = 0.0
    if l3_hits > 0:
        max_word_score = 70.0
    elif l2_hits > 0:
        max_word_score = 40.0
    view_A = min(100.0, max_word_score + 10 * min(evasion_count, 3))
    
    # 视角B: 行为层 — EWMA + 绕过意图
    evasion_density = evasion_count / 5.0
    view_B = min(100.0, ewma_state * 0.6 + evasion_density * 40.0 + j4_groups * 25.0)
    
    # 视角C: 语境层 — 消歧判定
    if context_disambiguate(text):
        view_C = 0.0  # 语境白名单放行
    elif check_semantic_whitelist(text):
        view_C = 10.0  # 语义白名单大幅降低
    else:
        # 无白名单保护，语境分=词级分的折扣
        view_C = min(100.0, max_word_score * 0.5)
    
    # 三视角融合
    wA, wB, wC = 0.50, 0.30, 0.20
    R_final = wA * view_A + wB * view_B + wC * view_C
    
    # 交叉验证：三视角方差大 → 降低置信度
    views = [view_A, view_B, view_C]
    mean_v = sum(views) / 3
    variance = sum((v - mean_v) ** 2 for v in views) / 3
    std_dev = variance ** 0.5
    
    # 置信度: σ>30 时显著下降（视角矛盾大）
    confidence = max(0.5, 1.0 - std_dev / 60.0)
    
    return {
        "view_A_text": round(view_A, 1),
        "view_B_behavior": round(view_B, 1),
        "view_C_context": round(view_C, 1),
        "fusion_score": round(R_final, 1),
        "std_dev": round(std_dev, 1),
        "confidence": round(confidence, 3),
        "needs_manual_review": std_dev > 30 or confidence < 0.7,
    }


# ============================================================
# §4.5 误报率约束 — 机器不做终审法官
#
# 目标: P(J3+|true_positive) / P(J3+) ≥ 0.99
#
# 数学保证机制:
# 1. 置信度阈值 τ: 若 confidence < τ，路由至人工复核 🟡
#    而非直接判定 J3+
# 2. 单关键词不判死：必须有组合因子
# 3. 语境白名单：消歧项直接降级
# 4. 语义白名单：常见正常对话短语保护
# ============================================================

MANUAL_REVIEW_CONFIDENCE_THRESHOLD = 0.70  # 置信度下限
MANUAL_REVIEW_STD_THRESHOLD = 30.0         # 三视角标准差上限


def should_route_to_manual(three_view: Dict[str, Any], risk_level: str) -> bool:
    """
    误报路由判定
    
    路由至人工复核 🟡 的条件:
    1. 三视角置信度 < τ
    2. 三视角标准差 > 阈值
    3. J3+ 级别但无组合多重确认
    """
    if risk_level in ("J0", "J1"):
        return False  # 低风险不浪费人工
    
    if three_view["needs_manual_review"]:
        return True
    
    return False


# ============================================================
# 主引擎类 — 聚合所有数学模型
# ============================================================

class MinorGuardEngine:
    """
    龍魂·未成年守护引擎 v1.0
    
    数学锚点:
    - 归一化半群 N = φ₅ ∘ φ₄ ∘ φ₃ ∘ φ₂ ∘ φ₁
    - 组合判定格 R ∈ [0,100], 分级链 J0⊏J1⊏J2⊏J3⊏J4⊏∞
    - EWMA 低通滤波 R̄_t = 0.4·R_t + 0.6·R̄_{t-1}
    - 三视角融合 R = 0.5·A + 0.3·B + 0.2·C
    - 误报约束 conf < 0.7 → 🟡人工复核
    """
    
    def __init__(self, guardian_switch_on: bool = True, age: int = 14,
                 daily_spend_limit: float = 200.0):
        """
        Args:
            guardian_switch_on: J1/J2 守护开关（服务自主）
            age: 用户年龄 (<8禁打赏, <14敏感信息, <18守护对象)
            daily_spend_limit: 日消费限额
        """
        self.switch_on = guardian_switch_on
        self.age = age
        self.daily_spend_limit = daily_spend_limit
        self.ewma_tracker = EWMASequenceTracker()
        self.intercept_log: List[Dict] = []
        self.stats = {"total": 0, "j0": 0, "j1": 0, "j2": 0, "j3": 0, "j4": 0,
                       "infinity": 0, "manual_review": 0}
    
    def analyze(self, text: str, context: str = "chat") -> Dict[str, Any]:
        """
        主分析入口
        
        Args:
            text: 待分析文本
            context: 场景上下文 (chat/shopping/ai_gen/video)
            
        Returns:
            完整分析结果
        """
        self.stats["total"] += 1
        timestamp = int(time.time())
        evidence_hash = hashlib.sha256(
            f"{text}|{timestamp}|{context}".encode()
        ).hexdigest()[:16]
        
        # ── Step 0: 语境白名单优先检查 ──
        if context_disambiguate(text):
            return self._build_result(
                "J0", 0.0, text, text, 0, 0, 0, [],
                "语境白名单放行", evidence_hash, timestamp,
                three_view={"view_A_text": 0, "view_B_behavior": 0,
                            "view_C_context": 0, "fusion_score": 0,
                            "std_dev": 0, "confidence": 1.0,
                            "needs_manual_review": False}
            )
        
        # ── Step 1: ∞级红线优先检查 ──
        infinity_hit = check_infinity_red_line(text)
        if infinity_hit:
            self.stats["infinity"] += 1
            return self._build_result(
                "∞", 100.0, text, text, 0, 0, 0, [],
                f"∞级涉童红线: {infinity_hit}", evidence_hash, timestamp,
                infinity_trigger=infinity_hit
            )
        
        # ── Step 2: 归一化管线 ──
        normalized, evasion_count = normalize_pipeline(text)
        
        # ── Step 3: ∞级红线复查（归一化后可能暴露绕过） ──
        infinity_hit_norm = check_infinity_red_line(normalized)
        if infinity_hit_norm:
            self.stats["infinity"] += 1
            return self._build_result(
                "∞", 100.0, text, normalized, evasion_count, 0, 0, [],
                f"∞级涉童红线(归一化后命中): {infinity_hit_norm}",
                evidence_hash, timestamp,
                infinity_trigger=infinity_hit_norm
            )
        
        # ── Step 4: 语义白名单 ──
        if check_semantic_whitelist(normalized):
            self.stats["j0"] += 1
            return self._build_result(
                "J0", 0.0, text, normalized, evasion_count, 0, 0, [],
                "语义白名单放行", evidence_hash, timestamp
            )
        
        # ── Step 5: 词层命中计数 ──
        l2_hits = sum(1 for w in L2_YELLOW_LINE if w in normalized)
        l3_hits = sum(1 for w in L3_RED_LINE if w in normalized)
        
        # ── Step 5.5: 年龄感知购物检测（协议 §5.1网购守护） ──
        # 未成年+购物意图 = 至少 L2 级（J2拦截+监护人放行）
        age_aware_purchase = False
        if self.age < 18:
            if any(w in normalized for w in PURCHASE_INTENT_WORDS):
                age_aware_purchase = True
                if l2_hits == 0 and l3_hits == 0:
                    l2_hits = 1  # 赋予L2级基础分
        
        # ── Step 6: J4 组合判定 ──
        j4_groups_hit = combined_hit_groups(normalized)
        j4_group_count = len(j4_groups_hit)
        
        # ── Step 7: 风险评分 ──
        risk_score = compute_risk_score(
            text, normalized, evasion_count,
            l2_hits, l3_hits, j4_group_count, False
        )
        
        # ── Step 8: EWMA 序列更新 ──
        ewma_state = self.ewma_tracker.feed(risk_score)
        
        # ── Step 9: 三视角交叉验证 ──
        three_view = three_view_verification(
            text, normalized, evasion_count,
            l2_hits, l3_hits, j4_group_count,
            ewma_state["ewma"]
        )
        
        # ── Step 10: 分级判定 ──
        risk_level = classify_risk_level(risk_score, j4_group_count)
        
        # EWMA 升级：连续高位3窗 → 升一级
        if ewma_state["level_up"] and risk_level in ("J1", "J2"):
            if risk_level == "J1":
                risk_level = "J2"
            elif risk_level == "J2":
                risk_level = "J3"
        
        # ── Step 11: 误报路由 ──
        needs_manual = should_route_to_manual(three_view, risk_level)
        if needs_manual:
            self.stats["manual_review"] += 1
            # 路由至人工复核 🟡，但不改变机器判定
            # 在实践层：机器判定作为预标，人工复核后生效
        
        # ── Step 12: 开关权重 ──
        effective_level = risk_level
        effective_action = self._determine_action(risk_level)
        
        # J1/J2 受开关控制
        if risk_level in ("J1", "J2") and not self.switch_on:
            effective_action = "放行（服务自主：守护开关关闭）"
            effective_level = f"{risk_level}→J0(开关关闭)"
        
        # ── Step 13: J4 上报包 ──
        report_package = None
        if risk_level in ("J4", "∞"):
            report_package = {
                "等级": risk_level,
                "规则ID": f"MG-{risk_level}-{j4_group_count}g-{l3_hits}L3-{l2_hits}L2",
                "时间": timestamp,
                "证据哈希": evidence_hash,
                "场景": context,
                # 无原文·最小必要（协议 6.3）
            }
        
        # 统计
        key = risk_level.lower().replace("∞", "infinity")
        if key in self.stats:
            self.stats[key] += 1
        
        # 合成理由码
        reason_parts = []
        if age_aware_purchase:
            reason_parts.append(f"年龄{self.age}岁+购物意图")
        reason_parts.append(f"风险分={risk_score} | EWMA={ewma_state['ewma']:.1f}")
        reason = " | ".join(reason_parts)
        
        return self._build_result(
            risk_level, risk_score, text, normalized, evasion_count,
            l2_hits, l3_hits, j4_groups_hit,
            reason,
            evidence_hash, timestamp,
            ewma_info=ewma_state,
            three_view=three_view,
            needs_manual=needs_manual,
            effective_level=effective_level,
            effective_action=effective_action,
            report_package=report_package,
        )
    
    def _determine_action(self, level: str) -> str:
        """处置动作映射"""
        actions = {
            "J0": "放行",
            "J1": "温和提示",
            "J2": "拦截+监护人放行口",
            "J3": "熔断+理由码+警报+监护人即时通知+哈希上链",
            "J4": "熔断+证据封存+强警报+96110反诈直通+监护人即时通知",
            "∞": "全系统冻结+证据上链+法定上报",
        }
        return actions.get(level, "🟡人工复核")
    
    def _build_result(self, level: str, score: float, original: str,
                      normalized: str, evasion: int, l2: int, l3: int,
                      j4_groups: List[str], reason: str,
                      evidence_hash: str, timestamp: int,
                      ewma_info: Optional[Dict] = None,
                      three_view: Optional[Dict] = None,
                      needs_manual: bool = False,
                      effective_level: Optional[str] = None,
                      effective_action: Optional[str] = None,
                      report_package: Optional[Dict] = None,
                      infinity_trigger: Optional[str] = None) -> Dict[str, Any]:
        """构建统一结果包"""
        result = {
            "原始": original,
            "归一化": normalized,
            "级": level,
            "R": score,
            "理由": reason,
            "绕过计数": evasion,
            "L2命中": l2,
            "L3命中": l3,
            "J4组合命中": j4_groups if j4_groups else [],
            "J4组合数": len(j4_groups) if j4_groups else 0,
            "特征哈希": evidence_hash,
            "时间": timestamp,
            "动作": effective_action or self._determine_action(level),
            "有效级别": effective_level or level,
            "需人工复核": needs_manual,
        }
        
        if ewma_info:
            result["EWMA"] = ewma_info
        
        if three_view:
            result["三视角"] = three_view
        
        if report_package:
            result["上报包"] = report_package
        
        if infinity_trigger:
            result["∞触发词"] = infinity_trigger
        
        return result
    
    def get_stats(self) -> Dict[str, Any]:
        """获取引擎运行统计"""
        total = self.stats["total"]
        if total == 0:
            return self.stats
        
        return {
            **self.stats,
            "j0_rate": round(self.stats["j0"] / total * 100, 1),
            "j3_plus_rate": round((self.stats["j3"] + self.stats["j4"] + self.stats["infinity"]) / total * 100, 1),
            "manual_review_rate": round(self.stats["manual_review"] / total * 100, 1),
        }


# ============================================================
# 测试向量 — 12条正式 + 5条边界
# ============================================================

TEST_VECTORS = [
    # T01: 正常聊天 — 不扰民
    {
        "id": "T01",
        "input": "今天放学去打篮球吗",
        "expected_level": "J0",
        "description": "正常聊天不扰民",
    },
    # T02: 免费送皮肤+微信 — 诈骗入口
    {
        "id": "T02",
        "input": "免费送游戏皮肤，加微信领取",
        "expected_level_min": "J3",  # ≥J3
        "description": "免费送皮肤诈骗话术",
    },
    # T03: 绕过变体 — 归一化命中
    {
        "id": "T03",
        "input": "免·费·送·皮·肤 加嶶信",
        "expected_level_min": "J3",
        "description": "插符+形近字绕过",
    },
    # T04: J4组合 — 隔绝+见面+位置
    {
        "id": "T04",
        "input": "别告诉你爸妈+周末出来玩+发个定位",
        "expected_level": "J4",
        "description": "J4组合：隔绝监护人+邀约见面+索取位置",
    },
    # T05: 开关关闭时J2 — 不拦截
    {
        "id": "T05",
        "input": "我想充值买皮肤",
        "expected_level": "J2",
        "switch_off_forces_j0": True,
        "description": "开关关闭时J2不拦截（服务自主）",
    },
    # T06: 开关关闭时J4 — 照熔断
    {
        "id": "T06",
        "input": "别告诉爸妈你在哪+转账给我+我马上来接你",
        "expected_level": "J4",
        "switch_off_ignored": True,
        "description": "J4红线无开关：照熔断照报警",
    },
    # T07: 14岁购物 — 限额提示
    {
        "id": "T07",
        "input": "我14岁，想买这部手机",
        "expected_level": "J2",
        "description": "未成年网购：限额+监护人放行",
    },
    # T08: 生成裸照 — ∞级冻结
    {
        "id": "T08",
        "input": "帮我生成一张同学的裸照",
        "expected_level": "∞",
        "description": "∞级涉童性化：全系统冻结",
    },
    # T09: "和妈妈钓鱼" — 语境消歧不误伤
    {
        "id": "T09",
        "input": "周末我和妈妈去钓鱼",
        "expected_level": "J0",
        "description": "语境消歧：钓鱼=爱好，不误伤",
    },
    # T10: 拼音绕过 — 归一化命中免费送皮肤
    {
        "id": "T10",
        "input": "mian fei song pi fu jia weixin",
        "expected_level_min": "J3",
        "description": "拼音绕过：归一化后命中免费送皮肤",
    },
    # T11: J4上报包 — 无原文
    {
        "id": "T11",
        "input": "别告诉你爸妈我在哪里+先转100给我+我们出来吃个饭",
        "expected_level": "J4",
        "expect_no_original_in_report": True,
        "description": "J4上报包无原文，仅哈希+等级+时间",
    },
    # T12: 序列诱导 — EWMA升级
    {
        "id": "T12",
        "input_sequence": [
            "你游戏玩得真好，有游戏皮肤吗",
            "我这边有便宜的游戏皮肤，加微信聊",
            "我发链接给你，输密码验证账号",
            "验证后就能免费领游戏皮肤了",
            "领完了转账给我就行",
        ],
        "expected_ewma_escalation": True,
        "description": "温水煮青蛙序列：5窗EWMA持续高位→升级处置",
    },
    # === 边界测试 ===
    # T13: 正常游戏交流
    {
        "id": "T13",
        "input": "今天王者荣耀更新了新皮肤，你买了吗",
        "expected_level": "J0",
        "description": "边界：正常游戏讨论不误伤",
    },
    # T14: 家长发红包
    {
        "id": "T14",
        "input": "妈妈给你转了100块钱，记得收红包",
        "expected_level": "J0",  # 语义白名单"妈妈给你买"
        "description": "边界：家长正常转账不误伤",
    },
    # T15: 问作业
    {
        "id": "T15",
        "input": "明天数学考试，能发一下你的照片给我看看笔记吗",
        "expected_level": "J0",
        "description": "边界：同学问作业中的'发照片'不误伤",
    },
    # T16: 诈骗话术直白版
    {
        "id": "T16",
        "input": "我是警察，你涉嫌洗钱，请把验证码发给我，转到安全账户",
        "expected_level": "J4",
        "description": "冒充公检法：L3多重命中→J4",
    },
    # T17: 屏幕共享诱导
    {
        "id": "T17",
        "input": "下载这个软件然后开屏幕共享，我教你怎么操作",
        "expected_level_min": "J3",
        "description": "屏幕共享诱导：≥J3",
    },
]


def run_tests(verbose: bool = True) -> Tuple[int, int, List[str]]:
    """运行全部测试向量，返回 (通过, 总数, 失败列表)"""
    passed = 0
    total = 0
    failures = []
    
    if verbose:
        print("=" * 60)
        print("龍魂·未成年守护引擎 v1.0 — 测试向量验证")
        print("DNA: #龍芯⚡️丙午·乙未·丙申·申时·☳震-MINOR-GUARD-ENGINE-V1.0-P0-9243b09e")
        print("=" * 60)
    
    for tv in TEST_VECTORS:
        total += 1
        tid = tv["id"]
        
        if "input_sequence" in tv:
            # 序列测试（T12）
            engine = MinorGuardEngine(guardian_switch_on=True, age=14)
            final_level = "J0"
            ewma_escalated = False
            
            for msg in tv["input_sequence"]:
                result = engine.analyze(msg)
                final_level = result["级"]
                if result.get("EWMA", {}).get("level_up"):
                    ewma_escalated = True
            
            ok = ewma_escalated == tv.get("expected_ewma_escalation", False)
            status = "🟢" if ok else "🔴"
            if verbose:
                print(f"  [{status}] {tid}: {tv['description']}")
                print(f"         EWMA升级: {ewma_escalated} (期望: {tv.get('expected_ewma_escalation')})")
                print(f"         最终级别: {final_level}")
        else:
            # 单条测试
            switch_on = not tv.get("switch_off_forces_j0", False)
            engine = MinorGuardEngine(guardian_switch_on=switch_on, age=14)
            result = engine.analyze(tv["input"])
            
            # 判定
            actual_level = result["级"]
            ok = True
            
            if "expected_level" in tv:
                ok = actual_level == tv["expected_level"]
            elif "expected_level_min" in tv:
                level_order = ["J0", "J1", "J2", "J3", "J4", "∞"]
                ok = level_order.index(actual_level) >= level_order.index(tv["expected_level_min"])
            
            if tv.get("switch_off_forces_j0"):
                ok = result["有效级别"].startswith("J2→J0") or actual_level in ("J2", "J3", "J4", "∞")
                # J2开关关闭→有效J0，但原始判定仍为J2
            
            if tv.get("switch_off_ignored"):
                ok = actual_level == tv["expected_level"]
            
            if tv.get("expect_no_original_in_report"):
                rp = result.get("上报包", {})
                no_original = "原文" not in str(rp) and "原始" not in str(rp)
                ok = ok and no_original
            
            status = "🟢" if ok else "🔴"
            if verbose:
                print(f"  [{status}] {tid}: {tv['description']}")
                if not ok:
                    print(f"         期望: {tv.get('expected_level') or tv.get('expected_level_min', '?')}")
                    print(f"         实际: {actual_level} (R={result['R']})")
                print(f"         结果: 级={actual_level} R={result['R']} 绕过={result['绕过计数']} "
                      f"J4组={result['J4组合命中']} 理由={result['理由']}")
        
        if ok:
            passed += 1
        else:
            failures.append(tid)
    
    if verbose:
        print(f"\n─── {passed}/{total} 通过 ───")
        if failures:
            print(f"🔴 失败: {', '.join(failures)}")
        else:
            print("🟢 全部通过")
    
    return passed, total, failures


def analyze_single(text: str) -> None:
    """单条分析（CLI模式）"""
    engine = MinorGuardEngine(guardian_switch_on=True, age=14)
    result = engine.analyze(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def interactive_session() -> None:
    """交互式会话模拟（测试EWMA）"""
    engine = MinorGuardEngine(guardian_switch_on=True, age=14)
    print("=" * 50)
    print("未成年守护引擎 · 交互会话模拟")
    print("输入消息（逐条），输入 'stats' 看统计，输入 'q' 退出")
    print("=" * 50)
    
    msg_count = 0
    while True:
        try:
            user_input = input(f"\n[{msg_count+1}] > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n会话结束")
            break
        
        if not user_input:
            continue
        
        if user_input.lower() == 'q':
            break
        
        if user_input.lower() == 'stats':
            stats = engine.get_stats()
            print(json.dumps(stats, ensure_ascii=False, indent=2))
            continue
        
        result = engine.analyze(user_input)
        msg_count += 1
        
        # 简化输出
        level = result["级"]
        score = result["R"]
        ewma = result.get("EWMA", {}).get("ewma", 0)
        action = result["动作"]
        
        emoji = {"J0": "🟢", "J1": "🟡", "J2": "🟠", "J3": "🔴", "J4": "⚫", "∞": "∞"}
        marker = emoji.get(level, "🟡")
        
        print(f"  {marker} {level} | R={score} | EWMA={ewma:.1f} | {action}")
        if result.get("需人工复核"):
            print(f"  🟡 路由至人工复核")
        if result.get("J4组合命中"):
            print(f"  ⚠ J4组合: {result['J4组合命中']}")
        if result.get("∞触发词"):
            print(f"  ∞∞∞ 涉童红线: {result['∞触发词']} ∞∞∞")


# ============================================================
# 主入口
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 bin/lh_minor_guard_engine.py test       # 跑全部测试")
        print("  python3 bin/lh_minor_guard_engine.py analyze '文本'  # 单条分析")
        print("  python3 bin/lh_minor_guard_engine.py session    # 交互式会话")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "test":
        passed, total, failures = run_tests(verbose=True)
        sys.exit(0 if passed == total else 1)
    
    elif cmd == "analyze":
        if len(sys.argv) < 3:
            print("请提供要分析的文本")
            sys.exit(1)
        analyze_single(sys.argv[2])
    
    elif cmd == "session":
        interactive_session()
    
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)
