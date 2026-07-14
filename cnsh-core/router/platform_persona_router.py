#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PlatformPersonaRouter·平台人格路由系统

【核心职能】
- 识别用户输入中的平台关键词
- 将平台相关任务路由到对应人格
- 与现有 PersonaRouter 打通，继承 DNA 追溯与三色审计

【龍魂系统坐标】
DNA:#龍芯⚡️2026-06-21-PLATFORM-PERSONA-ROUTER-v1.0
层级: L2·平台路由
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

【责任声明】
UID9622·不免责·永久有效

【平台 → 人格映射】
CSDN      → P16·平台运营官
知乎       → P16·平台运营官 / P08·翻译官（内容发布时）
微信       → P03·雯雯（隐私相关）/ P16·平台运营官（公众号运营）
支付宝     → P72·龍盾（支付安全）
淘宝       → P16·平台运营官（店铺/订单）
博客       → P16·平台运营官 / P15·乔前辈（归档）
"""

import json
import hashlib
import os
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from datetime import datetime


# ═══════════════════════════════════════════════════════════════
# 【平台 → 人格映射】
# ═══════════════════════════════════════════════════════════════

PLATFORM_PERSONA_MAP = {
    "CSDN": {
        "persona": "P16",
        "persona_name": "平台运营官",
        "emoji": "💻",
        "keywords": ["csdn", "CSDN", "博客园", "技术博客", "博文", "点赞", "收藏", "粉丝"],
        "operations": ["浏览消息", "导出消息列表", "登录状态检查", "跳转指定消息页"],
        "logic": "CSDN 账号管理·消息同步·内容导出·创作者保护执行",
    },
    "知乎": {
        "persona": "P16",
        "persona_name": "平台运营官",
        "emoji": "📖",
        "keywords": ["知乎", "zhihu", "回答", "提问", "专栏", "想法"],
        "operations": ["浏览消息", "导出内容", "登录状态检查"],
        "logic": "知乎内容运营·回答整理·专栏归档",
    },
    "微信": {
        "persona": "P03",
        "persona_name": "雯雯",
        "emoji": "💬",
        "keywords": ["微信", "wechat", "公众号", "小程序", "朋友圈"],
        "operations": ["扫码登录", "隐私检查"],
        "logic": "微信隐私优先·最小权限·数据主权保护",
    },
    "支付宝": {
        "persona": "P72",
        "persona_name": "龍盾",
        "emoji": "💰",
        "keywords": ["支付宝", "alipay", "转账", "支付", "花呗", "余额宝"],
        "operations": ["扫码付", "转账", "余额查询"],
        "logic": "支付安全·红色审计·二次确认",
    },
    "淘宝": {
        "persona": "P16",
        "persona_name": "平台运营官",
        "emoji": "🍑",
        "keywords": ["淘宝", "taobao", "订单", "购物车", "商品", "店铺"],
        "operations": ["商品搜索", "订单查询"],
        "logic": "电商平台运营·订单与库存管理",
    },
    "博客": {
        "persona": "P16",
        "persona_name": "平台运营官",
        "emoji": "📝",
        "keywords": ["博客", "blog", "发文章", "发文", "写作", "发布"],
        "operations": ["内容发布", "内容归档", "消息同步"],
        "logic": "博客内容运营·多平台同步·归档管理",
    },
}

DEFAULT_PLATFORM = {
    "persona": "P00",
    "persona_name": "文心",
    "emoji": "🌀",
    "logic": "未识别到明确平台，由文心兜底处理",
}


# ═══════════════════════════════════════════════════════════════
# 【数据模型】
# ═══════════════════════════════════════════════════════════════

@dataclass
class PlatformRoutingDecision:
    """平台人格路由决策记录"""
    routing_id: str
    timestamp: str
    platform: str
    persona: str
    persona_name: str
    emoji: str
    logic: str
    confidence: float
    matched_keywords: List[str]
    text_content: str
    dna: str = ""
    signature: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "routing_id": self.routing_id,
            "timestamp": self.timestamp,
            "platform": self.platform,
            "persona": self.persona,
            "persona_name": self.persona_name,
            "emoji": self.emoji,
            "logic": self.logic,
            "confidence": self.confidence,
            "matched_keywords": self.matched_keywords,
            "text_content": self.text_content[:100] + "..." if len(self.text_content) > 100 else self.text_content,
            "dna": self.dna,
            "signature": self.signature,
            "metadata": self.metadata,
        }


# ═══════════════════════════════════════════════════════════════
# 【PlatformPersonaRouter 主类】
# ═══════════════════════════════════════════════════════════════

class PlatformPersonaRouter:
    """
    平台人格路由系统

    负责:
    1. 从用户输入识别平台关键词
    2. 将任务路由到对应人格
    3. 生成 DNA 追溯与签名
    4. 记录审计日志
    """

    def __init__(self, log_dir: str = None):
        self.log_dir = log_dir or os.path.expanduser("~/longhun-system/logs")
        os.makedirs(self.log_dir, exist_ok=True)
        self.routing_counter = 0

    def route(self, text: str, user_id: str = "UID9622") -> PlatformRoutingDecision:
        """
        执行平台人格路由

        Args:
            text: 用户输入文本
            user_id: 用户标识，默认 UID9622

        Returns:
            PlatformRoutingDecision 对象
        """
        self.routing_counter += 1
        routing_id = f"PLATFORM-ROUTE-{datetime.now().strftime('%Y%m%d')}-{self.routing_counter:03d}"

        # 平台识别
        platform, matched_keywords, confidence = self._detect_platform(text)
        config = PLATFORM_PERSONA_MAP.get(platform, DEFAULT_PLATFORM)

        decision = PlatformRoutingDecision(
            routing_id=routing_id,
            timestamp=datetime.now().isoformat(),
            platform=platform,
            persona=config["persona"],
            persona_name=config["persona_name"],
            emoji=config["emoji"],
            logic=config["logic"],
            confidence=confidence,
            matched_keywords=matched_keywords,
            text_content=text,
            metadata={"user_id": user_id},
        )

        decision.dna = self._generate_dna(decision)
        decision.signature = self._generate_signature(decision)

        self._log_decision(decision)

        return decision

    def _detect_platform(self, text: str) -> tuple[str, List[str], float]:
        """
        检测文本中的平台关键词

        Returns:
            (平台名, 匹配到的关键词列表, 置信度)
        """
        text_lower = text.lower()
        best_platform = "默认"
        best_keywords = []
        best_score = 0.0

        for platform, config in PLATFORM_PERSONA_MAP.items():
            matched = []
            for kw in config["keywords"]:
                if kw.lower() in text_lower:
                    matched.append(kw)

            if matched:
                # 置信度 = 匹配词数 / 总词数，上限 0.95
                score = min(len(matched) / len(config["keywords"]) + 0.1, 0.95)
                if score > best_score:
                    best_score = score
                    best_platform = platform
                    best_keywords = matched

        return best_platform, best_keywords, best_score

    def list_platforms(self) -> Dict[str, Dict]:
        """列出所有支持的平台路由"""
        return PLATFORM_PERSONA_MAP.copy()

    def _generate_dna(self, decision: PlatformRoutingDecision) -> str:
        """生成 DNA 追溯码"""
        data_str = json.dumps({
            "routing_id": decision.routing_id,
            "platform": decision.platform,
            "persona": decision.persona,
            "confidence": decision.confidence,
            "timestamp": decision.timestamp,
        }, sort_keys=True, ensure_ascii=False)

        short_hash = hashlib.sha256(data_str.encode('utf-8')).hexdigest()[:8].upper()
        return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-PLATFORM-ROUTER-{short_hash}"

    def _generate_signature(self, decision: PlatformRoutingDecision) -> str:
        """生成决策签名"""
        data_str = json.dumps({
            "routing_id": decision.routing_id,
            "platform": decision.platform,
            "persona": decision.persona,
            "confidence": decision.confidence,
            "timestamp": decision.timestamp,
            "matched_keywords": decision.matched_keywords,
        }, sort_keys=True, ensure_ascii=False)

        return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

    def _log_decision(self, decision: PlatformRoutingDecision):
        """记录路由决策到 JSONL"""
        log_file = os.path.join(self.log_dir, "platform_persona_router.jsonl")
        entry = {
            "timestamp": datetime.now().isoformat(),
            "routing_id": decision.routing_id,
            "platform": decision.platform,
            "persona": decision.persona,
            "persona_name": decision.persona_name,
            "confidence": decision.confidence,
            "matched_keywords": decision.matched_keywords,
            "dna": decision.dna,
            "signature": decision.signature,
        }

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def print_report(self, decision: PlatformRoutingDecision):
        """打印路由报告"""
        print(f"""
┌─────────────────────────────────────────────────────────┐
│ 龍魂·平台人格路由决策报告                                │
├─────────────────────────────────────────────────────────┤
│ 路由ID: {decision.routing_id}
│ 识别平台: {decision.platform} {decision.emoji}
│ 路由人格: {decision.persona} · {decision.persona_name}
│ 置信度: {decision.confidence:.2%}
│ 匹配关键词: {', '.join(decision.matched_keywords) or '无'}
│ DNA: {decision.dna}
└─────────────────────────────────────────────────────────┘
""")

    def selftest(self) -> tuple[bool, List[str]]:
        """自检"""
        errors = []

        # 测试1: CSDN 路由
        decision = self.route("帮我看看 CSDN 的点赞和收藏")
        if decision.platform != "CSDN" or decision.persona != "P16":
            errors.append("CSDN 路由测试失败")

        # 测试2: 默认路由
        decision = self.route("今天天气怎么样")
        if decision.platform != "默认":
            errors.append("默认路由测试失败")

        # 测试3: DNA 格式
        if not decision.dna.startswith("#龍芯⚡️"):
            errors.append("DNA 格式错误")

        return len(errors) == 0, errors


# ═══════════════════════════════════════════════════════════════
# 【全局单例】
# ═══════════════════════════════════════════════════════════════

_GLOBAL_PLATFORM_ROUTER = None


def get_platform_persona_router(log_dir: str = None) -> PlatformPersonaRouter:
    """获取全局 PlatformPersonaRouter 单例"""
    global _GLOBAL_PLATFORM_ROUTER
    if _GLOBAL_PLATFORM_ROUTER is None:
        _GLOBAL_PLATFORM_ROUTER = PlatformPersonaRouter(log_dir)
    return _GLOBAL_PLATFORM_ROUTER


# ═══════════════════════════════════════════════════════════════
# 【测试代码】
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🔍 PlatformPersonaRouter 自检...\n")

    router = get_platform_persona_router()
    all_pass, errors = router.selftest()

    if all_pass:
        print("✅ 所有自检通过\n")
    else:
        print("❌ 自检失败:")
        for error in errors:
            print(f"  - {error}")
        exit(1)

    # 测试样例
    测试文本 = [
        "CSDN 上有人点赞了我的博文",
        "知乎回答需要整理一下",
        "微信登录状态检查一下",
        "支付宝余额查询",
        "帮我导出博客的周报",
    ]

    for text in 测试文本:
        decision = router.route(text)
        router.print_report(decision)
