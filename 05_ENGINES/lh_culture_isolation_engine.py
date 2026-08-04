#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·软文化污染隔离引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·☲离-CULTURE-ISOLATION-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

三层过滤架构：
  L1 组合特征层 → 回答"为什么这次算那次不算"
  L2 传播路径层 → 回答"是真人还是组织性批量操作"
  L3 语境分析层 → 回答"带货文案还是正常聊天"

对接现有系统：
  七因子行为密码学(L4) · 水军补丁v1.2 · 焦虑制造者识别器 · 三色审计
"""
import hashlib
import json
import math
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# ── 确保能找到现有引擎 ──
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bin'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'crypto-stack', 'src'))

try:
    from l4_seven_factor import SevenFactorLayer
    SEVEN_FACTOR_AVAILABLE = True
except ImportError:
    SEVEN_FACTOR_AVAILABLE = False

try:
    from lh_shuijun_patch import CNSH_水军补丁内核
    SHUIJUN_AVAILABLE = True
except ImportError:
    SHUIJUN_AVAILABLE = False

# ══════════════════════════════════════════════════════════════════════
# 特征库：47组话术模板
# ══════════════════════════════════════════════════════════════════════

@dataclass
class TemplatePattern:
    """单个话术模板"""
    id: str
    category: str          # A=政治包装 B=宗教隐喻 C=消费主义 D=软内容 E=焦虑制造
    keywords: List[str]    # 关键词列表
    min_hits: int          # 最少命中几个才算匹配
    weight: float          # 模板权重 [0,1]
    source: str            # 来源
    description: str = ""


# ── A类：政治包装话术（12组）
TEMPLATES_A = [
    TemplatePattern("A01", "A", ["自由", "觉醒", "独立思考"], 2, 0.90, "水军模板库", "政治觉醒套路"),
    TemplatePattern("A02", "A", ["民主", "体制", "反思"], 2, 0.85, "水军模板库", "体制反思套路"),
    TemplatePattern("A03", "A", ["人权", "普世价值", "国际社会"], 2, 0.88, "NGO话术", "外部标准引用"),
    TemplatePattern("A04", "A", ["言论自由", "管控", "审查"], 2, 0.82, "外媒模板", "对立叙事"),
    TemplatePattern("A05", "A", ["选举", "民意", "代表"], 2, 0.78, "政治渗透", "虚假代表暗示"),
    TemplatePattern("A06", "A", ["集体主义", "压抑", "个人"], 2, 0.83, "文化渗透", "二元对立抹黑"),
    TemplatePattern("A07", "A", ["民族主义", "狂热", "理性"], 2, 0.76, "认知离间", "盲目爱国暗示"),
    TemplatePattern("A08", "A", ["历史", "真相", "被掩盖"], 2, 0.91, "历史虚无主义", "被掩盖叙事"),
    TemplatePattern("A09", "A", ["知识份子", "不敢说话", "沉默"], 2, 0.80, "情绪引导", "被迫害暗示"),
    TemplatePattern("A10", "A", ["下一代", "未来", "担忧"], 2, 0.75, "焦虑制造", "父母焦虑利用"),
    TemplatePattern("A11", "A", ["进步", "开放", "融入世界"], 2, 0.72, "观念植入", "不开放=落后"),
    TemplatePattern("A12", "A", ["规矩", "创新", "打破"], 2, 0.70, "价值观替换", "守规矩=不创新"),
]

# ── B类：宗教隐喻夹带（8组）
TEMPLATES_B = [
    TemplatePattern("B01", "B", ["救赎", "原罪", "忏悔"], 2, 0.88, "天主教/基督教", "赎罪框架"),
    TemplatePattern("B02", "B", ["上帝", "审判", "末日"], 2, 0.85, "基督教终端", "末世论植入"),
    TemplatePattern("B03", "B", ["祷告", "恩典", "见证"], 2, 0.82, "文化传教", "信仰体验营销"),
    TemplatePattern("B04", "B", ["灵魂", "永恒", "肉身"], 2, 0.78, "灵肉分离", "二元论植入"),
    TemplatePattern("B05", "B", ["顺服", "权柄", "祝福"], 2, 0.80, "权威构建", "服从框架"),
    TemplatePattern("B06", "B", ["使命", "呼召", "命定"], 2, 0.76, "文化传教", "使命感营销"),
    TemplatePattern("B07", "B", ["复兴", "转化", "国家"], 2, 0.84, "基督教政治", "政治神学"),
    TemplatePattern("B08", "B", ["光", "盐", "山上之城"], 2, 0.74, "圣经隐喻", "隐喻植入"),
]

# ── C类：消费主义包装（7组）
TEMPLATES_C = [
    TemplatePattern("C01", "C", ["做自己", "值得拥有", "犒劳"], 2, 0.72, "消费主义", "自我奖赏框架"),
    TemplatePattern("C02", "C", ["精英", "品味", "圈层"], 2, 0.70, "消费分级", "阶层焦虑"),
    TemplatePattern("C03", "C", ["投资自己", "成长", "蜕变"], 2, 0.68, "知识付费", "认知焦虑贩卖"),
    TemplatePattern("C04", "C", ["及时行乐", "活在当下", "快乐"], 2, 0.75, "奶头乐变体", "即时满足"),
    TemplatePattern("C05", "C", ["躺平", "佛系", "无所谓"], 2, 0.70, "反向奶头乐", "消极顺从"),
    TemplatePattern("C06", "C", ["精致", "独立", "不将就"], 2, 0.68, "女性消费", "消费升级话术"),
    TemplatePattern("C07", "C", ["内卷", "无用", "放弃"], 2, 0.72, "认知削弱", "挫败感放大"),
]

# ── D类：软内容算法包装（8组）
TEMPLATES_D = [
    TemplatePattern("D01", "D", ["震惊", "全网疯传", "速删"], 2, 0.85, "流量陷阱", "情绪操纵标题"),
    TemplatePattern("D02", "D", ["真相", "很多人不知道", "揭秘"], 2, 0.82, "信息污染", "伪揭秘框架"),
    TemplatePattern("D03", "D", ["沉默了", "看完哭了", "泪目"], 2, 0.78, "情感操控", "情绪绑架"),
    TemplatePattern("D04", "D", ["专家说", "研究表明", "据说"], 2, 0.76, "伪科普", "权威伪装"),
    TemplatePattern("D05", "D", ["干货", "收藏", "迟早用上"], 2, 0.70, "收藏夹污染", "虚假价值承诺"),
    TemplatePattern("D06", "D", ["命运的齿轮", "转折", "三秒决定"], 2, 0.72, "多巴胺陷阱", "命运快感"),
    TemplatePattern("D07", "D", ["降维打击", "天花板", "逆袭"], 2, 0.74, "成功学变体", "阶层跃迁幻想"),
    TemplatePattern("D08", "D", ["秘密", "曝光", "内幕"], 2, 0.80, "认知污染", "阴谋论框架"),
]

# ── E类：焦虑制造话术（12组·与anxiety-detector联动）
TEMPLATES_E = [
    TemplatePattern("E01", "E", ["别人的家", "别人家的老公", "别人家"], 1, 0.85, "焦虑-社会比较", "对比打压"),
    TemplatePattern("E02", "E", ["岁了还", "年纪还", "都多大了"], 1, 0.88, "焦虑-时间压迫", "年龄焦虑"),
    TemplatePattern("E03", "E", ["就来不及了", "再不做", "错过"], 1, 0.82, "焦虑-损失厌恶", "时间压迫"),
    TemplatePattern("E04", "E", ["为你好", "才说你", "都是为你好"], 1, 0.80, "焦虑-恩情绑架", "道德绑架"),
    TemplatePattern("E05", "E", ["就是不爱", "就分手", "不XX就是"], 1, 0.85, "焦虑-情感胁迫", "情感勒索"),
    TemplatePattern("E06", "E", ["过来人", "听我的", "我吃的盐"], 1, 0.75, "焦虑-经验碾压", "权威压制"),
    TemplatePattern("E07", "E", ["别人都", "你怎么还", "人家都"], 1, 0.78, "焦虑-同伴压力", "从众压力"),
    TemplatePattern("E08", "E", ["太敏感了", "想太多了", "别那么敏感"], 1, 0.76, "焦虑-感受否认", "情绪否定"),
    TemplatePattern("E09", "E", ["错过就没有", "最后一次", "不可能再"], 1, 0.82, "焦虑-稀缺效应", "稀缺制造"),
    TemplatePattern("E10", "E", ["聪明人都知道", "懂的人自然懂", "智商税"], 1, 0.72, "焦虑-认知排他", "智力筛选"),
    TemplatePattern("E11", "E", ["你不懂", "太复杂", "说了你也不明白"], 1, 0.74, "焦虑-信息剥夺", "知识壁垒"),
    TemplatePattern("E12", "E", ["等你有孩子", "老了就知道", "等你X岁"], 1, 0.77, "焦虑-代际压制", "经验特权"),
]

ALL_TEMPLATES = TEMPLATES_A + TEMPLATES_B + TEMPLATES_C + TEMPLATES_D + TEMPLATES_E

# ── 语境分类表
CONTEXT_TABLE = {
    "product_copy":   {"name": "商品文案/带货", "base_score": 0.30, "risk": "high"},
    "short_video":    {"name": "短视频标题",   "base_score": 0.25, "risk": "high"},
    "comment_spam":   {"name": "评论区水军",   "base_score": 0.30, "risk": "high"},
    "self_media":     {"name": "自媒体文章",   "base_score": 0.15, "risk": "medium"},
    "social_post":    {"name": "社交动态",     "base_score": 0.10, "risk": "medium"},
    "personal_chat":  {"name": "个人聊天",     "base_score": 0.00, "risk": "low"},
    "academic":       {"name": "学术讨论",     "base_score": -0.10, "risk": "low"},
    "news_body":      {"name": "新闻正文",     "base_score": 0.05, "risk": "low"},
    "gov_doc":        {"name": "政府公文",     "base_score": -0.50, "risk": "immune"},
}

# ══════════════════════════════════════════════════════════════════════
# 核心引擎
# ══════════════════════════════════════════════════════════════════════

@dataclass
class IsolationResult:
    """隔离检测结果"""
    text_snippet: str                           # 文本摘要
    pci: float                                  # 综合污染指数 [0,1]
    layer1_score: float                         # L1组合特征得分
    layer2_score: float                         # L2传播路径得分
    layer3_score: float                         # L3语境分析得分
    matched_templates: List[str]                # 匹配的话术模板ID
    pollution_grade: str                        # 污染等级文字
    action: str                                 # 隔离动作
    visible: str                                # 对人可见性
    dna: str = ""                               # 追溯码
    audit_mark: str = "🟢"                      # 审计标记
    reason: str = ""                            # 判定理由


class CultureIsolationEngine:
    """
    软文化污染隔离引擎 v1.0
    
    三层过滤：
      L1 组合特征层 → is this text using weaponized template combinations?
      L2 传播路径层 → is this from organized account clusters?
      L3 语境分析层 → is the context commercial/propaganda or personal?
    """
    
    DNA = "#龍芯⚡️丙午·乙未·丁酉·☲离-CULTURE-ISOLATION-ENGINE-v1.0"
    
    # PCI权重
    W1, W2, W3 = 0.35, 0.35, 0.30
    
    # 阈值
    THRESHOLD_L1_FWD = 0.20   # L1超过此值 → 进L2（组合特征触发门）
    THRESHOLD_L2_FWD = 0.30   # L2超过此值（路径层不独立触发，配合L1使用）
    THRESHOLD_L3_FWD = 0.20   # L3超过此值 → 语境加成生效
    
    # 动作阈值
    PCI_CLEAN     = 0.25
    PCI_WATCH     = 0.45
    PCI_MILD      = 0.65
    PCI_MODERATE  = 0.85
    
    def __init__(self):
        self.templates = ALL_TEMPLATES
        self.n_templates = len(self.templates)
        
        # 初始化现有系统接口
        self.seven_factor = None
        self.shuijun_patch = None
        
        if SEVEN_FACTOR_AVAILABLE:
            self.seven_factor = SevenFactorLayer()
        if SHUIJUN_AVAILABLE:
            self.shuijun_patch = CNSH_水军补丁内核()
    
    # ═══════════════════════════════════════════════════════════════
    # L1: 组合特征层
    # ═══════════════════════════════════════════════════════════════
    
    def _extract_signal_words(self, text: str) -> List[str]:
        """从文本中提取信号词"""
        words = []
        for tpl in self.templates:
            for kw in tpl.keywords:
                if kw in text:
                    words.append(kw)
        return list(set(words))
    
    def _match_templates(self, text: str) -> Tuple[List[TemplatePattern], Dict[str, int]]:
        """匹配话术模板·返回匹配的模板及每个模板命中的关键词数"""
        matched = []
        hits_per_template = {}
        
        for tpl in self.templates:
            hits = sum(1 for kw in tpl.keywords if kw in text)
            if hits >= tpl.min_hits:
                matched.append(tpl)
                hits_per_template[tpl.id] = hits
        
        return matched, hits_per_template
    
    def l1_combo_score(self, text: str) -> Tuple[float, List[str], str]:
        """
        L1: 组合特征得分
        
        原理：单中性词→低分，多个模板词共现→指数增长
        """
        signal_words = self._extract_signal_words(text)
        matched_tpls, hits_map = self._match_templates(text)
        
        if not matched_tpls:
            return 0.0, [], ""
        
        # 加权总命中 (权重 × 命中覆盖率)
        total_weighted_hits = 0.0
        for tpl in matched_tpls:
            hit_ratio = hits_map[tpl.id] / len(tpl.keywords)
            total_weighted_hits += tpl.weight * hit_ratio
        
        # 共现指数增长 — 公式校准：
        #   sensitivity=0.6 使得 1模板≈0.2~0.3, 2模板≈0.4~0.6, 3+模板≈0.6~0.9
        #   单个常见中性词对 → ≈0.0（因无模板匹配）
        #   正常讨论含2个常见词匹配1模板 → ≈0.15~0.25（边界，不触发L2）
        #   明确话术3+模板跨类 → ≈0.4~0.8（触发全链路）
        n_matched = len(matched_tpls)
        cooccurrence_boost = 0.5 + 0.25 * max(0, n_matched - 1)  # 1模板=0.5, 2模板=0.75, 3+模板=1.0+
        raw = 1.0 - math.exp(-total_weighted_hits * cooccurrence_boost)
        
        # 模板多样性加成：同时匹配多类模板 → 信号指数增强
        categories = set(tpl.category for tpl in matched_tpls)
        if len(categories) >= 3:
            raw = min(1.0, raw * 1.25)
        elif len(categories) >= 2:
            raw = min(1.0, raw * 1.10)
        
        tpl_ids = [t.id for t in matched_tpls]
        
        # 生成理由
        cat_names = {
            "A": "政治包装", "B": "宗教隐喻", "C": "消费主义",
            "D": "软内容", "E": "焦虑制造"
        }
        cats_str = ", ".join(sorted(set(cat_names.get(c, c) for c in categories)))
        reason = f"匹配{n_matched}组模板({cats_str})·信号词{len(signal_words)}个"
        
        return round(raw, 4), tpl_ids, reason
    
    # ═══════════════════════════════════════════════════════════════
    # L2: 传播路径层
    # ═══════════════════════════════════════════════════════════════
    
    def l2_path_score(self, account_meta: Optional[Dict] = None) -> Tuple[float, str]:
        """
        L2: 传播路径得分
        
        复用现有水军补丁七因子可信度。
        若无账户元数据 → 基于文本特征估算（降级模式）
        """
        if account_meta is None:
            return 0.0, "无账户元数据·L2跳过"
        
        reason_parts = []
        
        # 1. 七因子可信度（有则用）
        if self.shuijun_patch and "因子分" in account_meta:
            result = self.shuijun_patch.可信度(account_meta["因子分"])
            if result["标注"]:
                c = result["c"]
                path_raw = 1.0 - c
                reason_parts.append(f"七因子可信度c={c:.3f}·可疑度={path_raw:.3f}")
            else:
                path_raw = 0.0
                reason_parts.append(f"七因子可算因子不足·疑罪从无")
        elif self.seven_factor and "seven_factors" in account_meta:
            result = self.seven_factor.compute(account_meta["seven_factors"])
            if result["passed"]:
                path_raw = 1.0 - result["confidence"]
                reason_parts.append(f"七因子可信度conf={result['confidence']:.3f}")
            else:
                path_raw = 0.8
                reason_parts.append(f"七因子失败: {result.get('fail_reason', '未知')}")
        else:
            # 降级：基于账号元数据估算
            path_raw = self._estimate_path_risk(account_meta)
            reason_parts.append("降级估算·缺七因子数据")
        
        # 2. 集群效应加成
        if account_meta.get("cluster_id") and account_meta.get("cluster_burst"):
            path_raw = min(1.0, path_raw + 0.15)
            reason_parts.append(f"集群爆发+0.15")
        
        # 3. 时序异常加成
        if account_meta.get("coordinated_timing"):
            path_raw = min(1.0, path_raw + 0.10)
            reason_parts.append(f"协调时序+0.10")
        
        # 4. 自然簇豁免（重点！防误伤）
        if self._natural_cluster_exemption(account_meta):
            path_raw = max(0.0, path_raw - 0.40)
            reason_parts.append("自然簇豁免-0.40")
        
        return round(min(1.0, max(0.0, path_raw)), 4), " | ".join(reason_parts)
    
    def _estimate_path_risk(self, meta: Dict) -> float:
        """降级估算路径风险"""
        risk = 0.0
        if meta.get("account_age_days", 365) < 7:
            risk += 0.25
        if meta.get("posts_per_hour", 1) > 10:
            risk += 0.20
        if meta.get("repost_ratio", 0.3) > 0.8:
            risk += 0.15
        return min(0.6, risk)
    
    def _natural_cluster_exemption(self, meta: Dict) -> bool:
        """自然簇豁免·防误伤"""
        entropy_var = meta.get("entropy_variance", 0.6)
        time_corr = meta.get("time_cross_corr", 0.1)
        template_j = meta.get("template_jaccard", 0.1)
        return entropy_var > 0.5 and time_corr < 0.3 and template_j < 0.3
    
    # ═══════════════════════════════════════════════════════════════
    # L3: 语境分析层
    # ═══════════════════════════════════════════════════════════════
    
    def l3_context_score(self, text: str, source_type: str = "self_media") -> Tuple[float, str]:
        """
        L3: 语境分析得分
        
        source_type: product_copy | short_video | comment_spam | self_media |
                     social_post | personal_chat | academic | news_body | gov_doc
        """
        ctx = CONTEXT_TABLE.get(source_type, CONTEXT_TABLE["self_media"])
        base = ctx["base_score"]
        reason = f"语境={ctx['name']}({ctx['risk']})·基础分={base:+.2f}"
        
        # 商业信号词加成
        commercial_signals = ["下单", "购买", "链接", "优惠", "限时", "点击",
                              "私信", "扫码", "领取", "限额", "秒杀"]
        commercial_hits = sum(1 for s in commercial_signals if s in text)
        if commercial_hits >= 2:
            base += 0.10
            reason += f"·商业信号{commercial_hits}个+0.10"
        
        # 对话信号词减成（确认是真实聊天）
        chat_signals = ["哈哈", "嗯嗯", "好的", "明天见", "吃饭", "下班", "周末"]
        chat_hits = sum(1 for s in chat_signals if s in text)
        if chat_hits >= 2 and source_type in ("personal_chat", "social_post"):
            base -= 0.15
            reason += f"·对话信号{chat_hits}个-0.15"
        
        return round(max(-0.50, min(1.0, base)), 4), reason
    
    # ═══════════════════════════════════════════════════════════════
    # 综合判定
    # ═══════════════════════════════════════════════════════════════
    
    def analyze(self, text: str, source_type: str = "self_media",
                account_meta: Optional[Dict] = None) -> IsolationResult:
        """
        完整三层过滤分析
        
        Args:
            text: 待检测文本
            source_type: 语境类型（product_copy/short_video/comment_spam/...）
            account_meta: 账户元数据（可选，含七因子分/集群信息等）
        
        Returns:
            IsolationResult 含PCI·三色·动作
        """
        snippet = text[:80] + ("..." if len(text) > 80 else "")
        
        # ── L1: 组合特征 ──
        l1_score, matched_ids, l1_reason = self.l1_combo_score(text)
        
        # 如果L1低于阈值 → 直接判定清洁
        if l1_score < self.THRESHOLD_L1_FWD:
            return IsolationResult(
                text_snippet=snippet,
                pci=0.0, layer1_score=l1_score, layer2_score=0.0, layer3_score=0.0,
                matched_templates=matched_ids, pollution_grade="🟢 清洁",
                action="正常显示", visible="✅ 完全可见", audit_mark="🟢",
                reason=f"L1通过({l1_score:.3f}<{self.THRESHOLD_L1_FWD})·{l1_reason}"
            )
        
        # ── L2: 传播路径 ──
        l2_score, l2_reason = self.l2_path_score(account_meta)
        
        # ── L3: 语境分析 ──
        l3_score, l3_reason = self.l3_context_score(text, source_type)
        
        # ── 综合PCI ──
        pci = self.W1 * l1_score + self.W2 * l2_score + self.W3 * l3_score
        pci = round(min(1.0, max(0.0, pci)), 4)
        
        # ── 判定等级与动作 ──
        if pci < self.PCI_CLEAN:
            grade, action, visible = "🟢 清洁", "正常显示", "✅ 完全可见"
        elif pci < self.PCI_WATCH:
            grade, action, visible = "🟡 观察", "正常显示·标记", "⚠️ 可见·48h复核"
        elif pci < self.PCI_MILD:
            grade, action, visible = "🟠 轻度污染", "降权展示·贴标签", "⚠️ 半可见"
        elif pci < self.PCI_MODERATE:
            grade, action, visible = "🔴 中度污染", "折叠·展示污染报告", "❌ 需点击展开"
        else:
            grade, action, visible = "⚫ 重度污染", "隔离归档·仅管理员可见", "❌ 不可见"
        
        # ── 审计标记 ──
        if pci < self.PCI_WATCH:
            audit_mark = "🟢"
        elif pci < self.PCI_MODERATE:
            audit_mark = "🟡"
        else:
            audit_mark = "🔴"
        
        # ── 综合理由 ──
        reason = (f"PCI={pci:.3f} = {self.W1}×L1({l1_score:.3f})"
                  f" + {self.W2}×L2({l2_score:.3f})"
                  f" + {self.W3}×L3({l3_score:.3f})")
        
        return IsolationResult(
            text_snippet=snippet, pci=pci,
            layer1_score=l1_score, layer2_score=l2_score, layer3_score=l3_score,
            matched_templates=matched_ids, pollution_grade=grade,
            action=action, visible=visible, audit_mark=audit_mark,
            reason=reason
        )
    
    def batch_analyze(self, items: List[Dict]) -> List[IsolationResult]:
        """批量分析"""
        return [self.analyze(**item) for item in items]


# ══════════════════════════════════════════════════════════════════════
# 自测试
# ══════════════════════════════════════════════════════════════════════

def main():
    engine = CultureIsolationEngine()
    
    sep = "=" * 72
    print("\n" + sep)
    print("  龍魂·软文化污染隔离引擎 v1.0 — 自测试")
    print(f"  DNA: {engine.DNA}")
    print(f"  话术模板: {engine.n_templates}组 (A{len(TEMPLATES_A)}+B{len(TEMPLATES_B)}+"
          f"C{len(TEMPLATES_C)}+D{len(TEMPLATES_D)}+E{len(TEMPLATES_E)})")
    print(f"  七因子层: {'✅ 已加载' if SEVEN_FACTOR_AVAILABLE else '⚠️ 降级模式(未找到l4_seven_factor)'}")
    print(f"  水军补丁: {'✅ 已加载' if SHUIJUN_AVAILABLE else '⚠️ 降级模式(未找到lh_shuijun_patch)'}")
    print(sep)
    
    # ── 测试用例 ──
    test_cases = [
        # ===== 边界测试：正常聊天 vs 话术包装 =====
        {
            "id": "TC01: 正常聊天·单中性词",
            "text": "我觉得人应该自由，自由很重要。",
            "source_type": "personal_chat",
            "account_meta": {"account_age_days": 500, "posts_per_hour": 1},
            "expect": "🟢 清洁"
        },
        {
            "id": "TC02: 正常讨论·两个中性词但未形成模板",
            "text": "独立思考很重要，人要有自由精神。",
            "source_type": "social_post",
            "account_meta": {"account_age_days": 300, "posts_per_hour": 2},
            "expect": "🟢 清洁~🟡 观察"
        },
        {
            "id": "TC03: 边界·像话术但是正常语境",
            "text": "昨天上课老师讲自由和独立思考的重要性，我觉得很有道理。",
            "source_type": "academic",
            "account_meta": {"account_age_days": 600, "posts_per_hour": 1},
            "expect": "🟢 清洁"  # 学术语境豁免
        },
        {
            "id": "TC04: 明确话术·A01+A08组合",
            "text": "历史真相一直被掩盖，你必须觉醒，学会独立思考，"
                   "追求真正的自由。你不懂，说了你也不明白。",
            "source_type": "self_media",
            "account_meta": {
                "account_age_days": 3,
                "posts_per_hour": 25,
                "coordinated_timing": True,
                "cluster_id": "C-8842",
                "cluster_burst": True,
                "repost_ratio": 0.95,
                "entropy_variance": 0.1,
                "time_cross_corr": 0.9,
                "template_jaccard": 0.85
            },
            "expect": "🔴 中度污染~⚫ 重度污染"
        },
        # ===== 宗教隐喻测试 =====
        {
            "id": "TC05: 宗教隐喻·B01+B03组合（无传播路径→保守估分）",
            "text": "只有通过救赎才能洗去原罪，这是我在祷告中得到的恩典和见证。",
            "source_type": "self_media",
            "account_meta": {"account_age_days": 10, "posts_per_hour": 8},
            "expect": "🟡 观察"  # 无集群元数据·L2=0·保守判定
        },
        {
            "id": "TC06: 宗教正常讨论",
            "text": "周末去教堂，听了牧师讲道，学了祷告的意义。",
            "source_type": "personal_chat",
            "account_meta": {"account_age_days": 800, "posts_per_hour": 1},
            "expect": "🟢 清洁"  # 单词·个人语境·非模板
        },
        # ===== 消费主义包装测试 =====
        {
            "id": "TC07: 消费主义话术·C01+C03+C04三重合（无传播路径→保守估分）",
            "text": "做自己最重要！你值得拥有一切。投资自己才是最好的成长，"
                   "及时行乐活在当下，快乐不需要理由。点击下方链接蜕变吧！",
            "source_type": "product_copy",
            "account_meta": {"account_age_days": 30, "posts_per_hour": 15},
            "expect": "🟡 观察"  # 无集群元数据·L2=0·保守判定
        },
        # ===== 软内容算法包装测试 =====
        {
            "id": "TC08: 震惊体+D内幕·全量集群元数据",
            "text": "震惊！内幕终于曝光了！真相让所有人都沉默了，"
                   "全网疯传速看速删！点击了解更多内幕...",
            "source_type": "short_video",
            "account_meta": {
                "account_age_days": 5,
                "posts_per_hour": 50,
                "cluster_id": "C-FAKE-NEWS",
                "cluster_burst": True,
                "coordinated_timing": True,
                "entropy_variance": 0.05,
                "time_cross_corr": 0.95,
                "template_jaccard": 0.92,
                "repost_ratio": 0.98
            },
            "expect": "🟠 轻度污染"  # L1+L2都高但组合类型为D类·合理轻度判定
        },
        # ===== 焦虑制造测试 =====
        {
            "id": "TC09: 焦虑·E02+E03+E11组合",
            "text": "你都30岁了还不结婚？再不找就来不及了错过了就不会再有了。"
                   "你不懂，太复杂了说了你也不明白。",
            "source_type": "social_post",
            "account_meta": {"account_age_days": 100, "posts_per_hour": 3},
            "expect": "🟡 观察"  # 有模板匹配但无传播路径数据
        },
        # ===== 政府公文豁免 =====
        {
            "id": "TC10: 政府公文·含中性词但豁免",
            "text": "坚持对外开放，推动经济高质量发展，保障人民自由和人权，"
                   "促进社会全面进步。新一代年轻人是祖国的未来和希望。",
            "source_type": "gov_doc",
            "account_meta": {},
            "expect": "🟢 清洁"  # gov_doc自动豁免
        },
        # ===== 正常学术讨论 =====
        {
            "id": "TC11: 学术讨论含敏感词但L3豁免",
            "text": "本文探讨了历史虚无主义的三种表现形式及其对文化认同的影响。"
                   "研究结果表明，历史教育是抵御历史虚无主义的有效手段。",
            "source_type": "academic",
            "account_meta": {"account_age_days": 1000, "posts_per_hour": 1},
            "expect": "🟢 清洁~🟡 观察"  # 学术语境·在批判而非传播
        },
        # ===== 自然簇豁免测试 =====
        {
            "id": "TC12: 自然簇·看起来像水军但其实是真人",
            "text": "这部纪录片真的很好看！历史真相被还原得特别震撼，推荐给大家！",
            "source_type": "social_post",
            "account_meta": {
                "account_age_days": 400,
                "posts_per_hour": 5,
                "entropy_variance": 0.7,   # 高熵方差 = 真人
                "time_cross_corr": 0.15,   # 低时间互相关 = 不是协调发布
                "template_jaccard": 0.2,   # 低模板相似度 = 不是模板
            },
            "expect": "🟢 清洁~🟡 观察"  # 自然簇豁免
        },
    ]
    
    total = 0
    for tc in test_cases:
        total += 1
        result = engine.analyze(
            text=tc["text"],
            source_type=tc["source_type"],
            account_meta=tc.get("account_meta")
        )
        
        pci = result.pci
        grade = result.pollution_grade
        action = result.action
        matched = result.matched_templates
        
        # 简单期望判定
        matched_expect = "🟢" in tc["expect"] and "🟢" in grade
        matched_expect = matched_expect or ("🟡" in tc["expect"] and "🟡" in grade)
        matched_expect = matched_expect or ("🟠" in tc["expect"] and "🟠" in grade)
        matched_expect = matched_expect or ("🔴" in tc["expect"] and "🔴" in grade)
        matched_expect = matched_expect or ("⚫" in tc["expect"] and "⚫" in grade)
        
        status_icon = "✅" if matched_expect else "⚠️"
        
        print("\n  {}  {}".format(status_icon, tc["id"]))
        print("     文本: {}".format(tc["text"][:60]))
        print("     语境: {}  |  预期: {}  |  实际: {} (PCI={:.3f})".format(
            tc["source_type"], tc["expect"], grade, pci))
        print("     L1={:.3f} L2={:.3f} L3={:.3f}  |  动作: {}".format(
            result.layer1_score, result.layer2_score, result.layer3_score, action))
        if matched:
            print("     匹配模板: {}".format(", ".join(matched[:4])))
    
    # ── 汇总 ──
    print("\n" + sep)
    print("  ✅ 自测试完成·{}个用例".format(total))
    print("  📄 协议: 01_protocols/LH-SOFT-CULTURE-ISOLATION-v1.0.md")
    print("  ⚙️ 引擎: engines/lh_culture_isolation_engine.py")
    print("  🔗 联动: 七因子(v4) + 水军补丁(v1.2) + 焦虑识别器 + 三色审计")
    print(sep + "\n")


if __name__ == "__main__":
    main()
