#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷓观-FIX_DNA-v1.0
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·䷒临-LONGHUN_CLICK_AUDITOR-v1.0-12a47a2e
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂系统 · 链接点击审计脚本 v1.0
功能：区分人类点击、AI抓取、异常行为，标记追溯本源
作者：UID9622
协议：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import json
import hashlib
import time
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class ClickType(Enum):
    """点击类型"""
    HUMAN = "human"          # 人类真实点击
    AI_CRAWL = "ai_crawl"    # AI爬虫/抓取
    BOT = "bot"              # 机器人/脚本
    SUSPICIOUS = "suspicious" # 可疑行为
    UNKNOWN = "unknown"      # 未知

class RiskLevel(Enum):
    """风险等级"""
    SAFE = 0       # 安全
    LOW = 1        # 低风险
    MEDIUM = 2     # 中风险
    HIGH = 3       # 高风险
    CRITICAL = 4   # 严重

@dataclass
class ClickEvent:
    """点击事件记录"""
    event_id: str           # 事件唯一ID
    timestamp: float          # 时间戳
    ip: str                 # IP地址
    user_agent: str         # 用户代理
    referer: str            # 来源页面
    target_url: str         # 目标链接
    click_type: str         # 点击类型
    risk_level: int         # 风险等级
    dna: str                # 内容DNA
    fingerprint: str        # 浏览器指纹
    session_id: str         # 会话ID
    click_pattern: Dict     # 点击行为模式
    geo_info: Dict          # 地理位置
    is_verified: bool       # 是否已验证
    trace_chain: List       # 追溯链

class LonghunClickAuditor:
    """
    龍魂链接点击审计器
    区分人类/AI/异常，标记追溯
    """

    # AI爬虫特征库
    AI_CRAWL_PATTERNS = [
        r'(?i)(bot|crawler|spider|scraper)',
        r'(?i)(gpt|claude|gemini|llama|qwen|kimi)',
        r'(?i)(openai|anthropic|googlebot|bingbot)',
        r'(?i)(python-requests|urllib|httpx|aiohttp)',
        r'(?i)(headless|selenium|puppeteer|playwright)',
        r'(?i)(curl|wget|scrapy)',
    ]

    # 异常行为特征
    SUSPICIOUS_PATTERNS = [
        r'(?i)(sql injection|xss|csrf|lfi|rfi)',
        r'(?i)(union select|drop table|delete from)',
        r'(?i)(../../|\\x00|\\xFF)',
        r'(?i)(brute force|dictionary attack)',
    ]

    def __init__(self, uid: str = "UID9622"):
        self.uid = uid
        self.event_registry = {}  # event_id -> ClickEvent
        self.ip_reputation = {}   # ip -> 风险记录
        self.dna_registry = {}    # dna -> 使用记录

    def _generate_event_id(self, ip: str, timestamp: float) -> str:
        """生成事件唯一ID"""
        raw = f"{ip}|{timestamp}|{hashlib.sha256(str(timestamp).encode()).hexdigest()[:8]}"
        return hashlib.sha256(raw.encode()).hexdigest()[:24]

    def _detect_click_type(self, user_agent: str, headers: Dict[str, Any]) -> ClickType:
        """检测点击类型"""
        ua_lower = user_agent.lower()

        # 检查AI爬虫
        for pattern in self.AI_CRAWL_PATTERNS:
            if re.search(pattern, ua_lower):
                return ClickType.AI_CRAWL

        # 检查异常行为
        for pattern in self.SUSPICIOUS_PATTERNS:
            if re.search(pattern, ua_lower):
                return ClickType.SUSPICIOUS

        # 检查是否为机器人
        if 'bot' in ua_lower or 'crawler' in ua_lower:
            return ClickType.BOT

        # 检查人类特征
        if self._has_human_traits(headers):
            return ClickType.HUMAN

        return ClickType.UNKNOWN

    def _has_human_traits(self, headers: Dict[str, Any]) -> bool:
        """判断是否具有人类特征"""
        human_indicators = [
            'accept-language' in headers,  # 人类浏览器会发送语言偏好
            'accept-encoding' in headers,  # 人类浏览器会发送编码偏好
            'cookie' in headers,            # 人类有会话Cookie
            'referer' in headers,           # 人类有来源页面
        ]
        return sum(human_indicators) >= 3

    def _calculate_risk(self, click_type: ClickType, ip: str, 
                        click_pattern: Dict[str, Any]) -> RiskLevel:
        """计算风险等级"""
        risk_score = 0

        # 基础风险
        if click_type == ClickType.AI_CRAWL:
            risk_score += 2
        elif click_type == ClickType.BOT:
            risk_score += 1
        elif click_type == ClickType.SUSPICIOUS:
            risk_score += 4
        elif click_type == ClickType.UNKNOWN:
            risk_score += 1

        # IP信誉
        ip_history = self.ip_reputation.get(ip, {})
        if ip_history.get('suspicious_count', 0) > 5:
            risk_score += 2
        if ip_history.get('ai_crawl_count', 0) > 10:
            risk_score += 1

        # 点击模式异常
        if click_pattern.get('click_speed', 0) < 0.1:  # 点击间隔小于0.1秒
            risk_score += 2
        if click_pattern.get('same_target_clicks', 0) > 5:  # 同一目标多次点击
            risk_score += 1

        # 映射到等级
        if risk_score >= 4:
            return RiskLevel.CRITICAL
        elif risk_score >= 3:
            return RiskLevel.HIGH
        elif risk_score >= 2:
            return RiskLevel.MEDIUM
        elif risk_score >= 1:
            return RiskLevel.LOW
        return RiskLevel.SAFE

    def _generate_fingerprint(self, headers: Dict[str, Any]) -> str:
        """生成浏览器指纹"""
        fingerprint_data = [
            headers.get('user-agent', ''),
            headers.get('accept', ''),
            headers.get('accept-language', ''),
            headers.get('accept-encoding', ''),
            headers.get('dnt', ''),
        ]
        raw = '|'.join(fingerprint_data)
        return hashlib.sha256(raw.encode()).hexdigest()[:32]

    def audit_click(self, ip: str, user_agent: str, target_url: str,
                    referer: str = "", headers: Dict[str, Any] = None,
                    dna: str = "", click_pattern: Dict[str, Any] = None,
                    geo_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        审计点击事件
        返回：审计结果 + 追溯信息
        """
        timestamp = time.time()
        headers = headers or {}
        click_pattern = click_pattern or {}
        geo_info = geo_info or {}

        # 生成事件ID
        event_id = self._generate_event_id(ip, timestamp)

        # 检测点击类型
        click_type = self._detect_click_type(user_agent, headers)

        # 计算风险
        risk_level = self._calculate_risk(click_type, ip, click_pattern)

        # 生成指纹
        fingerprint = self._generate_fingerprint(headers)

        # 生成会话ID
        session_id = hashlib.sha256(f"{ip}|{fingerprint}".encode()).hexdigest()[:16]

        # 构建追溯链
        trace_chain = [
            {"step": 1, "action": "click_detected", "timestamp": timestamp},
            {"step": 2, "action": "type_identified", "value": click_type.value},
            {"step": 3, "action": "risk_assessed", "value": risk_level.name},
            {"step": 4, "action": "fingerprint_generated", "value": fingerprint[:8]},
        ]

        # 创建事件记录
        event = ClickEvent(
            event_id=event_id,
            timestamp=timestamp,
            ip=ip,
            user_agent=user_agent,
            referer=referer,
            target_url=target_url,
            click_type=click_type.value,
            risk_level=risk_level.value,
            dna=dna,
            fingerprint=fingerprint,
            session_id=session_id,
            click_pattern=click_pattern,
            geo_info=geo_info,
            is_verified=(risk_level == RiskLevel.SAFE),
            trace_chain=trace_chain
        )

        # 注册事件
        self.event_registry[event_id] = event

        # 更新IP信誉
        if ip not in self.ip_reputation:
            self.ip_reputation[ip] = {
                'human_count': 0, 'ai_crawl_count': 0,
                'bot_count': 0, 'suspicious_count': 0,
                'unknown_count': 0, 'first_seen': timestamp,
                'last_seen': timestamp
            }

        self.ip_reputation[ip][f'{click_type.value}_count'] += 1
        self.ip_reputation[ip]['last_seen'] = timestamp

        # 更新DNA记录 - 修复：使用正确的字段名
        if dna:
            if dna not in self.dna_registry:
                self.dna_registry[dna] = {
                    'total_clicks': 0, 'human_clicks': 0,
                    'ai_crawl_clicks': 0, 'bot_clicks': 0,
                    'suspicious_clicks': 0, 'unknown_clicks': 0,
                    'unique_ips': set()
                }
            self.dna_registry[dna]['total_clicks'] += 1
            self.dna_registry[dna][f'{click_type.value}_clicks'] += 1
            self.dna_registry[dna]['unique_ips'].add(ip)

        return {
            "event_id": event_id,
            "click_type": click_type.value,
            "risk_level": risk_level.name,
            "is_verified": event.is_verified,
            "session_id": session_id,
            "fingerprint": fingerprint[:16] + "...",
            "trace_chain": trace_chain,
            "timestamp": datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S"),
            "action": "ALLOW" if risk_level.value <= 2 else "BLOCK"
        }

    def trace_event(self, event_id: str) -> Dict[str, Any]:
        """追溯事件本源"""
        event = self.event_registry.get(event_id)
        if not event:
            return {"error": "事件未找到", "event_id": event_id}

        event_dict = asdict(event)
        event_dict['timestamp_readable'] = datetime.fromtimestamp(
            event.timestamp).strftime("%Y-%m-%d %H:%M:%S")

        # 获取IP信誉
        ip_rep = self.ip_reputation.get(event.ip, {})

        # 获取DNA记录
        dna_rec = self.dna_registry.get(event.dna, {}) if event.dna else {}

        return {
            "event": event_dict,
            "ip_reputation": ip_rep,
            "dna_usage": {
                "total_clicks": dna_rec.get('total_clicks', 0),
                "human_clicks": dna_rec.get('human_clicks', 0),
                "ai_clicks": dna_rec.get('ai_crawl_clicks', 0),
                "suspicious_clicks": dna_rec.get('suspicious_clicks', 0),
                "unique_ips": len(dna_rec.get('unique_ips', set()))
            } if dna_rec else None,
            "verdict": "人类点击" if event.click_type == ClickType.HUMAN.value 
                      else "AI抓取" if event.click_type == ClickType.AI_CRAWL.value
                      else "异常行为" if event.click_type == ClickType.SUSPICIOUS.value
                      else "待确认"
        }

    def get_ip_report(self, ip: str) -> Dict[str, Any]:
        """获取IP完整报告"""
        rep = self.ip_reputation.get(ip, {})
        if not rep:
            return {"error": "IP无记录", "ip": ip}

        total = sum([
            rep.get('human_count', 0),
            rep.get('ai_crawl_count', 0),
            rep.get('bot_count', 0),
            rep.get('suspicious_count', 0),
            rep.get('unknown_count', 0)
        ])

        return {
            "ip": ip,
            "total_events": total,
            "human_ratio": rep.get('human_count', 0) / total if total else 0,
            "ai_ratio": rep.get('ai_crawl_count', 0) / total if total else 0,
            "suspicious_ratio": rep.get('suspicious_count', 0) / total if total else 0,
            "first_seen": datetime.fromtimestamp(rep.get('first_seen', 0)).strftime("%Y-%m-%d %H:%M:%S"),
            "last_seen": datetime.fromtimestamp(rep.get('last_seen', 0)).strftime("%Y-%m-%d %H:%M:%S"),
            "risk_assessment": "HIGH" if rep.get('suspicious_count', 0) > 5 else "MEDIUM" if rep.get('ai_crawl_count', 0) > 10 else "LOW"
        }


# ========== 演示 ==========

auditor = LonghunClickAuditor()

print("=" * 60)
print("龍魂系统 · 链接点击审计脚本 v1.0")
print("#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
print("=" * 60)
print()

# 场景1：人类正常点击
print("【场景1】人类正常点击")
result1 = auditor.audit_click(
    ip="192.168.1.100",
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    target_url="https://longhun888.com/article/123",
    referer="https://google.com",
    headers={
        "accept-language": "zh-CN,zh;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "cookie": "session_id=abc123",
        "referer": "https://google.com"
    },
    dna="da146546c027abd9b4353fee362216ea",
    click_pattern={"click_speed": 2.5, "same_target_clicks": 1},
    geo_info={"country": "CN", "city": "Wenzhou"}
)
print(json.dumps(result1, ensure_ascii=False, indent=2))
print()

# 场景2：AI爬虫抓取
print("【场景2】AI爬虫抓取")
result2 = auditor.audit_click(
    ip="10.0.0.50",
    user_agent="Mozilla/5.0 (compatible; GPTBot/1.0; +https://openai.com/gptbot)",
    target_url="https://longhun888.com/article/123",
    headers={"accept": "text/html"},
    dna="da146546c027abd9b4353fee362216ea",
    click_pattern={"click_speed": 0.05, "same_target_clicks": 10}
)
print(json.dumps(result2, ensure_ascii=False, indent=2))
print()

# 场景3：异常行为（SQL注入尝试）
print("【场景3】异常行为（攻击尝试）")
result3 = auditor.audit_click(
    ip="45.23.12.88",
    user_agent="sqlmap/1.7.12#stable",
    target_url="https://longhun888.com/article/123?id=1\' UNION SELECT * FROM users--",
    headers={},
    click_pattern={"click_speed": 0.01, "same_target_clicks": 50}
)
print(json.dumps(result3, ensure_ascii=False, indent=2))
print()

# 场景4：追溯本源
print("【场景4】追溯本源")
trace = auditor.trace_event(result1["event_id"])
print(json.dumps(trace, ensure_ascii=False, indent=2, default=str))
print()

# 场景5：IP报告
print("【场景5】IP信誉报告")
report = auditor.get_ip_report("192.168.1.100")
print(json.dumps(report, ensure_ascii=False, indent=2))
print()

print("=" * 60)
print("审计完成")
print("=" * 60)
