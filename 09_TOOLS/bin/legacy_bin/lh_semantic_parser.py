#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
🐉 龍魂·语义解析引擎 v1.0 — 文本/OCR/语音转录 → 结构化语义
DNA: #龍芯⚡️丙午·辛未·SEMANTIC-PARSER-v1.0-INTENT2ACTION

三步处理管线:
  ① 意图识别: 判断用户想要什么/在问什么/在抱怨什么
  ② 情感分析: 正面/负面/中性 + 强度评分
  ③ 实体提取: 人名/地名/组织/时间/金额/技术术语

三模块联动:
  视觉提取文字 → 送给语义 → 结构化意图
  音频转录文字 → 送给语义 → 情感+实体
  语义统一处理 → 结构化结果 → 送审计层记录 → 送响应层生成回复

统一接口: parse(input_data: str|dict) → SemanticOutput

用法:
  from bin.lh_semantic_parser import SemanticParser
  parser = SemanticParser()
  result = parser.parse("这个订单能不能退款？")
  print(result.intent.label, result.sentiment.polarity)

部署: Mac M4 Max / 华为鲲鹏均可，离线可用
"""

import json
import os
import sys
import hashlib
import time
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, Union, Dict, Any, List, Tuple
from datetime import datetime, timezone, timedelta

# ── 审计层导入 ──
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
try:
    from tools.logging.action_logger import ActionLogger, log_operation
except ImportError:
    ActionLogger = None
    def log_operation(*args, **kwargs):
        from contextlib import nullcontext
        return nullcontext()

DNA = "#龍芯⚡️丙午·辛未·SEMANTIC-PARSER-v1.0-INTENT2ACTION"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬SEMP-E3F4"

# ═══════════════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════════════

@dataclass
class IntentResult:
    """意图识别结果"""
    label: str = "unknown"                    # complaint/inquiry/request/command/greeting/feedback
    sub_intent: str = ""                      # 子意图
    confidence: float = 0.0
    action_suggestion: str = ""               # 建议动作
    route_to: str = ""                        # 路由到的人格/模块

@dataclass
class SentimentResult:
    """情感分析结果"""
    polarity: str = "neutral"                 # positive/negative/neutral
    intensity: float = 0.0                    # 0-1
    keywords: List[str] = field(default_factory=list)  # 情感关键词
    confidence: float = 0.0

@dataclass
class KeyEntity:
    """命名实体"""
    entity_type: str = ""                     # person/location/organization/time/amount/tech_term
    value: str = ""
    normalized: str = ""                      # 归一化值 (如金额→数字)
    confidence: float = 0.8

@dataclass
class Relation:
    """实体关系"""
    subject: str = ""
    predicate: str = ""                       # 投诉/购买/询问/要求
    obj: str = ""
    confidence: float = 0.0

@dataclass
class SemanticOutput:
    """语义解析统一输出"""
    input_hash: str = ""
    raw_text: str = ""
    intent: IntentResult = field(default_factory=IntentResult)
    sentiment: SentimentResult = field(default_factory=SentimentResult)
    entities: List[KeyEntity] = field(default_factory=list)
    relations: List[Relation] = field(default_factory=list)
    summary: str = ""
    risk_level: str = "low"                   # low/medium/high/critical
    action_suggestion: str = ""
    processing_time_ms: float = 0.0
    model_version: str = "v1.0-local"
    dna: str = DNA
    parsed_at: str = ""

    def to_json(self, indent: int = 2) -> str:
        d = asdict(self)
        d["intent"] = asdict(self.intent)
        d["sentiment"] = asdict(self.sentiment)
        d["entities"] = [asdict(e) for e in self.entities]
        d["relations"] = [asdict(r) for r in self.relations]
        return json.dumps(d, ensure_ascii=False, indent=indent)

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.to_json())

    def to_audit_record(self) -> dict[str, Any]:
        """导出审计摘要 (不含原始内容，只含哈希+摘要)"""
        return {
            "input_hash": self.input_hash,
            "intent": self.intent.label,
            "sentiment": self.sentiment.polarity,
            "entity_count": len(self.entities),
            "risk_level": self.risk_level,
            "processing_time_ms": self.processing_time_ms,
            "model_version": self.model_version,
            "dna": self.dna,
            "parsed_at": self.parsed_at,
        }


# ═══════════════════════════════════════════════════════════════
# 意图识别引擎
# ═══════════════════════════════════════════════════════════════

class IntentRecognizer:
    """意图识别: 判断用户想要什么/在问什么/在抱怨什么"""

    INTENT_PATTERNS = [
        {
            "label": "complaint",
            "patterns": [
                r'(投诉|举报|曝光|维权|退钱|退款|赔偿|差评|坑|骗|烂|垃圾|受不了)',
                r'(我要|帮我).*?(投诉|举报|维权|退款)',
                r'(不.?满意|太.?差|真.?烂|什么.?垃圾)',
            ],
            "action": "转投诉处理/维权引擎",
            "route": "P03雯雯·维权",
        },
        {
            "label": "inquiry",
            "patterns": [
                r'(怎么|如何|什么|为什么|哪里|什么时候|能不能|可以.?吗)',
                r'(帮我|我想).*?(查|看|了解|知道|确认)',
                r'(是.?什么|有.?没有|会不会|可.?不可.?以)',
                r'\?|？',
            ],
            "action": "查询信息/检索知识库",
            "route": "P00文心·意图理解",
        },
        {
            "label": "request",
            "patterns": [
                r'(帮我|帮个忙|麻烦|请|求|我需要|我想)',
                r'(做|写|画|生成|计算|翻译|整理|总结|分析)',
                r'(帮我|我想).*?(一个|一下)',
            ],
            "action": "执行任务/调度人格",
            "route": "P02龍芯·命令执行",
        },
        {
            "label": "command",
            "patterns": [
                r'^(检查|审计|修复|部署|同步|推送|启动|停止|重启|扫描)',
                r'^(lh|lh6|系统|共)\w*',
                r'检查一下|看一下|扫一下',
            ],
            "action": "系统命令执行",
            "route": "P13姜子牙·路由分发",
        },
        {
            "label": "greeting",
            "patterns": [
                r'^(你好|嗨|哈喽|早上好|晚上好|晚安|拜拜|再见)',
            ],
            "action": "友好回应",
            "route": "P00文心·社交",
        },
        {
            "label": "feedback",
            "patterns": [
                r'(不错|很好|太棒了|谢谢|感谢|学到了|有用|帮大忙)',
                r'(不行|不对|错了|不对不对|不是这样)',
            ],
            "action": "收集反馈/校准",
            "route": "P01诸葛亮·战略校准",
        },
    ]

    @classmethod
    def recognize(cls, text: str) -> IntentResult:
        scores = {}
        for intent in cls.INTENT_PATTERNS:
            score = 0
            for pattern in intent["patterns"]:
                if re.search(pattern, text):
                    score += 1
            if score > 0:
                scores[intent["label"]] = {
                    "score": score,
                    "action": intent["action"],
                    "route": intent["route"],
                }

        if not scores:
            return IntentResult(
                label="inquiry",
                sub_intent="general_question",
                confidence=0.3,
                action_suggestion="查询知识库",
                route_to="P00文心·意图理解",
            )

        dominant = max(scores, key=lambda k: scores[k]["score"])
        total_score = sum(s["score"] for s in scores.values())
        conf = min(0.95, scores[dominant]["score"] / max(total_score + 1, 1) + 0.3)

        sub = ""
        second_best = sorted(
            [(k, v["score"]) for k, v in scores.items() if k != dominant],
            key=lambda x: x[1], reverse=True
        )
        if second_best:
            sub = second_best[0][0]

        return IntentResult(
            label=dominant,
            sub_intent=sub,
            confidence=round(conf, 3),
            action_suggestion=scores[dominant]["action"],
            route_to=scores[dominant]["route"],
        )


# ═══════════════════════════════════════════════════════════════
# 情感分析引擎
# ═══════════════════════════════════════════════════════════════

class SentimentAnalyzer:
    """情感分析: 正面/负面/中性 + 强度评分"""

    POSITIVE = [
        "好", "棒", "赞", "感谢", "开心", "满意", "推荐",
        "给力", "良心", "靠谱", "专业", "高效", "完美", "优秀",
        "哈哈哈", "太好了", "很不错", "非常好", "真不错", "学到了",
        "哈哈", "谢谢", "感恩",
    ]
    NEGATIVE = [
        "差", "烂", "坑", "骗", "垃圾", "恶心", "投诉", "举报",
        "退款", "赔", "失望", "无语", "坑爹",
        "太差了", "太烂了", "太恶心了", "受不了",
        "辣鸡", "cao", "tmd",
    ]
    INTENSIFIERS = [
        (r'非常', 0.3), (r'特别', 0.3), (r'极其', 0.4), (r'太', 0.25),
        (r'真', 0.2), (r'超级', 0.35), (r'极', 0.4),
        (r'死了', 0.3), (r'疯了', 0.35),
    ]
    NEGATORS = [r'不', r'没', r'未', r'无']

    @classmethod
    def analyze(cls, text: str) -> SentimentResult:
        pos_score = 0
        neg_score = 0
        keywords: List[str] = []

        for word in cls.POSITIVE:
            if re.search(word, text):
                pos_score += 1
                keywords.append(word)

        for word in cls.NEGATIVE:
            if re.search(word, text):
                neg_score += 1
                keywords.append(word)

        intensity = 0.5
        for pattern, boost in cls.INTENSIFIERS:
            if re.search(pattern, text):
                intensity += boost

        has_negator = any(re.search(neg, text[:20]) for neg in cls.NEGATORS)
        if has_negator and pos_score > neg_score:
            pos_score, neg_score = neg_score, pos_score

        if pos_score > neg_score + 1:
            polarity = "positive"
            intensity = min(1.0, intensity + 0.1)
        elif neg_score > pos_score + 1:
            polarity = "negative"
            intensity = min(1.0, intensity + 0.15)
        else:
            polarity = "neutral"
            intensity = 0.3 if pos_score == neg_score == 0 else 0.5

        confidence = min(0.9, (abs(pos_score - neg_score) / max(pos_score + neg_score + 1, 1)) + 0.3)

        return SentimentResult(
            polarity=polarity,
            intensity=round(intensity, 2),
            keywords=keywords[:10],
            confidence=round(confidence, 3),
        )


# ═══════════════════════════════════════════════════════════════
# 实体提取引擎
# ═══════════════════════════════════════════════════════════════

class EntityExtractor:
    """实体提取: 人名/地名/组织/时间/金额/技术术语"""

    PATTERNS = [
        (r'(?:人民币|¥|￥|CNY|USD|\$)\s*[\d,]+\.?\d*\s*(?:元|块|万|亿|k|w|W)?', 'amount'),
        (r'[\d,]+\.?\d*\s*(?:元|块)\s*(?:钱)?', 'amount'),
        (r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日号]?', 'time'),
        (r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}', 'time'),
        (r'(?:今天|明天|昨天|上周|下周|本月|下月|今年|明年)', 'time'),
        (r'\d{1,2}月\d{1,2}[日号]', 'time'),
        (r'\d{1,2}:\d{2}(?::\d{2})?', 'time'),
        (r'(?:北京|上海|广州|深圳|杭州|成都|武汉|南京|西安|重庆|长沙|郑州|天津|苏州|东莞|厦门|青岛|大连|济南|哈尔滨|沈阳|长春|合肥|南昌|福州|南宁|昆明|贵阳|兰州|银川|西宁|拉萨|乌鲁木齐|呼和浩特|海口|三亚|香港|澳门|台北)[市省区]?', 'location'),
        (r'(?:腾讯|阿里|百度|华为|字节|京东|美团|小米|网易|拼多多|比亚迪|蔚来|理想|小鹏|OPPO|vivo|中兴|海康|大疆|科大讯飞|商汤|旷视)', 'organization'),
        (r'(?:公安局|法院|检察院|工商局|税务局|教育局|卫健委|人社局|住建局|交通局|环保局)', 'organization'),
        (r'(?:Python|Java|JavaScript|TypeScript|C\+\+|Go|Rust|Swift|Kotlin|PHP|Ruby|Scala|SQL|NoSQL|Redis|MySQL|PostgreSQL|MongoDB|Docker|K8s|Kubernetes|AWS|GCP|Azure|API|REST|GraphQL|HTTP|HTTPS|TCP|SSL|TLS|JWT|Git|Jenkins|Terraform|Nginx|Linux)', 'tech_term'),
        (r'(?:React|Vue|Angular|Next\.js|Nuxt\.js|Flutter|React Native|Electron|Spring|Django|Flask|FastAPI|Express|Koa|Nest\.js)', 'tech_term'),
        (r'1[3-9]\d{9}', 'phone'),
        (r'\d{17}[\dXx]', 'id_card'),
        (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', 'email'),
        (r'https?://[^\s,，。！？]+', 'url'),
    ]

    @classmethod
    def extract(cls, text: str) -> List[KeyEntity]:
        entities = []
        seen_values = set()

        for pattern, etype in cls.PATTERNS:
            for m in re.finditer(pattern, text):
                value = m.group()
                if value in seen_values:
                    continue
                seen_values.add(value)
                normalized = cls._normalize(value, etype)
                entities.append(KeyEntity(
                    entity_type=etype,
                    value=value,
                    normalized=normalized,
                    confidence=0.8 if len(value) > 3 else 0.65,
                ))

        # 人名: 常见姓氏 + 1-2字
        surname = r'[王李张刘陈杨黄赵周吴徐孙马胡朱郭何罗高林郑梁谢唐许冯宋韩董袁邓曹彭苏蒋蔡贾丁魏薛叶阎余潘杜戴夏钟汪田任姜范方石姚谭廖邹熊金陆郝孔白崔康毛邱秦江史顾侯邵孟龙万段雷钱汤尹黎易常武乔贺赖龚文]'
        name_pattern = rf'{surname}[一-龥]{{1,2}}(?![A-Za-z0-9])'
        for m in re.finditer(name_pattern, text[:len(text)//2]):
            value = m.group()
            if value in seen_values or len(value) < 2:
                continue
            if any(kw in value for kw in ['垃圾', '投诉', '维权', '退款']):
                continue
            seen_values.add(value)
            entities.append(KeyEntity(
                entity_type="person",
                value=value,
                normalized=value,
                confidence=0.5,
            ))

        return entities

    @staticmethod
    def _normalize(value: str, etype: str) -> str:
        if etype == "amount":
            cleaned = re.sub(r'[¥￥$,元块万]', '', value)
            cleaned = re.sub(r'[a-zA-Z]', '', cleaned)
            return cleaned.strip() or value
        if etype == "phone":
            return value[:3] + "****" + value[-4:]
        return value


# ═══════════════════════════════════════════════════════════════
# 解析引擎
# ═══════════════════════════════════════════════════════════════

class SemanticParser:
    """语义解析器 · 统一接口 parse(input_data) → SemanticOutput"""

    def __init__(self):
        self.intent_recognizer = IntentRecognizer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.entity_extractor = EntityExtractor()

    def parse(self, input_data: Union[str, dict[str, Any]]) -> SemanticOutput:
        """
        统一解析接口。支持:
        - str: 纯文本
        - dict: {"text": "...", "source": "vision"|"audio"|"direct", ...}
        """
        t_start = time.time()

        if isinstance(input_data, dict):
            text = input_data.get("text", "")
            source = input_data.get("source", "direct")
        elif isinstance(input_data, str):
            text = input_data
            source = "direct"
        else:
            raise TypeError(f"输入类型不支持: {type(input_data)}")

        text = text.strip()
        if not text:
            return SemanticOutput(
                input_hash="",
                raw_text="",
                intent=IntentResult(label="empty", confidence=0),
                sentiment=SentimentResult(polarity="neutral"),
                model_version="v1.0-local",
                dna=DNA,
                parsed_at=datetime.now(timezone(timedelta(hours=8))).isoformat(),
            )

        with log_operation("语义解析", "semantic_parser", persona="P00文心"):
            input_hash = hashlib.sha256(text.encode()).hexdigest()[:16]

            # ── 步骤①: 意图识别 ──
            intent = self.intent_recognizer.recognize(text)

            # ── 步骤②: 情感分析 ──
            sentiment = self.sentiment_analyzer.analyze(text)

            # ── 步骤③: 实体提取 ──
            entities = self.entity_extractor.extract(text)

            # 风险评估
            risk_level = self._assess_risk(intent, sentiment, entities)

            # 行动建议
            action_suggestion = intent.action_suggestion
            if sentiment.polarity == "negative" and sentiment.intensity > 0.7:
                action_suggestion += " | 情绪强烈，建议人工介入"
            if risk_level in ("high", "critical"):
                action_suggestion += " | 🚨 高风险，触发三色审计"

            # 摘要
            intent_cn = {
                "complaint": "投诉/不满", "inquiry": "询问/查询",
                "request": "请求/需求", "command": "系统命令",
                "greeting": "问候/社交", "feedback": "反馈/评价",
            }
            summary = f"[{intent_cn.get(intent.label, intent.label)}] 情感:{sentiment.polarity}({sentiment.intensity:.1f}) 实体:{len(entities)}个 | {text[:100]}"

            output = SemanticOutput(
                input_hash=input_hash,
                raw_text=text[:500],
                intent=intent,
                sentiment=sentiment,
                entities=entities,
                relations=[],
                summary=summary,
                risk_level=risk_level,
                action_suggestion=action_suggestion,
                processing_time_ms=round((time.time() - t_start) * 1000, 1),
                model_version="v1.0-local",
                dna=DNA,
                parsed_at=datetime.now(timezone(timedelta(hours=8))).isoformat(),
            )

            return output

    def _assess_risk(self, intent: IntentResult, sentiment: SentimentResult, entities: List[KeyEntity]) -> str:
        risk_score = 0
        if intent.label == "complaint":
            risk_score += 2
        if sentiment.polarity == "negative" and sentiment.intensity > 0.6:
            risk_score += 2
        elif sentiment.polarity == "negative":
            risk_score += 1
        sensitive_types = {"amount", "id_card", "phone"}
        for e in entities:
            if e.entity_type in sensitive_types:
                risk_score += 1
        if risk_score >= 4:
            return "critical"
        elif risk_score >= 3:
            return "high"
        elif risk_score >= 2:
            return "medium"
        return "low"


# ═══════════════════════════════════════════════════════════════
# 三模块联动桥接
# ═══════════════════════════════════════════════════════════════

def bridge_vision_to_semantic(vision_output) -> SemanticOutput:
    """视觉→语义: OCR文字送入语义解析"""
    parser = SemanticParser()
    ocr_text = " ".join(o.text for o in vision_output.ocr_texts)
    if not ocr_text:
        ocr_text = vision_output.raw_description
    return parser.parse({"text": ocr_text, "source": "vision", "vision_hash": vision_output.input_hash})


def bridge_audio_to_semantic(audio_output) -> SemanticOutput:
    """音频→语义: 转录文字送入语义解析"""
    parser = SemanticParser()
    text = audio_output.cleaned_transcript or audio_output.full_transcript
    return parser.parse({
        "text": text, "source": "audio",
        "audio_hash": audio_output.input_hash,
        "speaker_count": len(audio_output.speakers),
    })


# ═══════════════════════════════════════════════════════════════
# 快速入口
# ═══════════════════════════════════════════════════════════════

_default_parser: Optional[SemanticParser] = None

def parse(input_data: Union[str, dict[str, Any]]) -> SemanticOutput:
    global _default_parser
    if _default_parser is None:
        _default_parser = SemanticParser()
    return _default_parser.parse(input_data)


# ═══════════════════════════════════════════════════════════════
# 命令行
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="🐉 龍魂语义解析器")
    ap.add_argument("text", help="待解析文本")
    ap.add_argument("--json", action="store_true", help="JSON输出")
    args = ap.parse_args()

    parser = SemanticParser()
    result = parser.parse(args.text)

    if args.json:
        print(result.to_json())
    else:
        print(f"🐉 龍魂语义解析 · {result.input_hash}")
        print(f"   意图: {result.intent.label} ({result.intent.confidence:.2f})")
        print(f"   路由: {result.intent.route_to}")
        print(f"   情感: {result.sentiment.polarity} (强度{result.sentiment.intensity:.1f})")
        print(f"   实体: {len(result.entities)}个")
        for e in result.entities:
            print(f"     [{e.entity_type}] {e.value}")
        print(f"   风险: {result.risk_level}")
        print(f"   建议: {result.action_suggestion}")
        print(f"   耗时: {result.processing_time_ms}ms")
        print(f"   DNA: {DNA}")
