#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# ============================================================
# DNA: #龍芯⚡️丙午·乙未·丁酉·子时·䷀乾-GUANLAN-PRIVACY-SCANNER-v1.0-ps8e4f2a
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫 (UID9622)
# 协议: CC BY-NC-SA 4.0
# ============================================================
"""
龍魂 · 观澜 — 隐私扫描器 v1.0
检测：第三方Cookie | Canvas指纹 | WebRTC泄露 | 浏览器指纹 | 追踪脚本
输出：0-100 隐私风险评分，红色≥70立刻告警
"""
import hashlib
import json
import re
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from urllib.parse import urlparse


class RiskLevel(Enum):
    LOW = "low"       # 0-39
    MEDIUM = "medium" # 40-69
    HIGH = "high"     # 70-100


@dataclass
class ScanFinding:
    """单项检测发现"""
    category: str          # 分类: tracking / fingerprint / cookie / webrtc / ai_script
    sub_type: str          # 子类型
    source: str            # 来源URL或域名
    severity: int          # 严重程度 1-10
    detail: str = ""       # 详情
    evidence: str = ""     # 证据
    timestamp: float = field(default_factory=time.time)


@dataclass
class ScanResult:
    """扫描结果"""
    url: str
    domain: str
    score: int = 0
    risk_level: RiskLevel = RiskLevel.LOW
    findings: list[ScanFinding] = field(default_factory=list)
    threat_summary: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    scan_time: float = field(default_factory=time.time)
    dna: str = ""


class PrivacyScanner:
    """觀澜隐私扫描器 — 主权防线第二道"""

    # 已知追踪域名
    TRACKING_DOMAINS: set[str] = {
        "doubleclick.net", "google-analytics.com", "googletagmanager.com",
        "facebook.net", "fbcdn.net", "hotjar.com", "clarity.ms",
        "amplitude.com", "mixpanel.com", "segment.io", "fullstory.com",
        "mouseflow.com", "crazyegg.com", "optimizely.com", "vwo.com",
        "adnxs.com", "rubiconproject.com", "pubmatic.com", "openx.net",
        "criteo.com", "casalemedia.com", "adsrvr.org", "moatads.com",
        "scorecardresearch.com", "bluekai.com", "exelator.com",
        "nexac.com", "rlcdn.com", "tidaltv.com", "turn.com",
        "yieldmo.com", "zemanta.com", "3lift.com", "agkn.com",
        "bidswitch.net", "contextweb.com", "krxd.net",
        "mathtag.com", "outbrain.com", "taboola.com", "yahoo.com/tag",
        "baidu.com/hm.js", "cnzz.com", "51.la", "tongji.baidu.com",
    }

    # 已知AI域名
    AI_DOMAINS: set[str] = {
        "api.openai.com", "api.anthropic.com", "api.deepseek.com",
        "api.moonshot.cn", "api.baichuan-ai.com", "api.zhipuai.cn",
        "api.minimax.chat", "api.stepfun.com", "dashscope.aliyuncs.com",
        "hunyuan.tencentcloudapi.com", "generativelanguage.googleapis.com",
        "api.coze.cn", "api.coze.com", "api.302.ai",
        "api.siliconflow.cn", "api.groq.com", "api.mistral.ai",
        "api.together.xyz", "api.perplexity.ai",
    }

    # Canvas指纹检测模式
    CANVAS_FINGERPRINT_PATTERNS: list[re.Pattern] = [
        re.compile(r"canvas\.toDataURL\s*\(", re.IGNORECASE),
        re.compile(r"canvas\.toBlob\s*\(", re.IGNORECASE),
        re.compile(r"getImageData\s*\(", re.IGNORECASE),
        re.compile(r"HTMLCanvasElement\.prototype", re.IGNORECASE),
    ]

    # WebRTC泄露检测模式
    WEBRTC_PATTERNS: list[re.Pattern] = [
        re.compile(r"RTCPeerConnection", re.IGNORECASE),
        re.compile(r"webkitRTCPeerConnection", re.IGNORECASE),
        re.compile(r"RTCIceCandidate", re.IGNORECASE),
        re.compile(r"createDataChannel", re.IGNORECASE),
    ]

    def __init__(self, alert_threshold: int = 70):
        self.alert_threshold = alert_threshold

    def scan_page(self, url: str, scripts: list[str], cookies: list[str],
                  inline_scripts: list[str] | None = None,
                  request_urls: list[str] | None = None) -> ScanResult:
        """扫描单个页面"""
        domain = urlparse(url).netloc
        result = ScanResult(url=url, domain=domain)

        # 1. 检测第三方追踪脚本
        self._scan_tracking_scripts(scripts, request_urls or [], domain, result)

        # 2. 检测Canvas指纹
        self._scan_canvas_fingerprint(inline_scripts or [], scripts, result)

        # 3. 检测WebRTC泄露
        self._scan_webrtc(inline_scripts or [], scripts, result)

        # 4. 检测第三方Cookie
        self._scan_cookies(cookies, domain, result)

        # 5. 检测AI脚本
        self._scan_ai_scripts(scripts, request_urls or [], result)

        # 6. 检测浏览器指纹
        self._scan_browser_fingerprint(inline_scripts or [], scripts, result)

        # 汇总评分
        result.score = self._calculate_score(result)
        result.risk_level = self._assess_risk(result.score)
        result.dna = self._generate_dna()

        return result

    def _scan_tracking_scripts(self, scripts: list[str], request_urls: list[str],
                                domain: str, result: ScanResult):
        """检测第三方追踪脚本"""
        seen = set()
        for script_url in scripts + request_urls:
            if script_url in seen:
                continue
            seen.add(script_url)

            try:
                script_domain = urlparse(script_url).netloc
            except Exception:
                continue

            if script_domain == domain or not script_domain:
                continue

            for tracker in self.TRACKING_DOMAINS:
                if tracker in script_domain:
                    result.findings.append(ScanFinding(
                        category="tracking",
                        sub_type="third_party_tracker",
                        source=script_url,
                        severity=7,
                        detail=f"检测到第三方追踪: {tracker}",
                        evidence=script_url
                    ))
                    break

    def _scan_canvas_fingerprint(self, inline_scripts: list[str],
                                  scripts: list[str], result: ScanResult):
        """检测Canvas指纹"""
        all_scripts = inline_scripts + scripts
        for script in all_scripts:
            for pattern in self.CANVAS_FINGERPRINT_PATTERNS:
                if pattern.search(script):
                    result.findings.append(ScanFinding(
                        category="fingerprint",
                        sub_type="canvas_fingerprint",
                        source="inline_script" if script in inline_scripts else script,
                        severity=8,
                        detail="检测到Canvas指纹采集代码",
                        evidence=pattern.pattern
                    ))
                    return  # 找到一个就够了

    def _scan_webrtc(self, inline_scripts: list[str],
                      scripts: list[str], result: ScanResult):
        """检测WebRTC泄露"""
        all_scripts = inline_scripts + scripts
        for script in all_scripts:
            for pattern in self.WEBRTC_PATTERNS:
                if pattern.search(script):
                    result.findings.append(ScanFinding(
                        category="webrtc",
                        sub_type="webrtc_leak",
                        source="inline_script" if script in inline_scripts else script,
                        severity=6,
                        detail="检测到WebRTC相关代码，可能存在IP泄露风险",
                        evidence=pattern.pattern
                    ))
                    return

    def _scan_cookies(self, cookies: list[str], domain: str,
                       result: ScanResult):
        """检测第三方Cookie"""
        # 第三方Cookie的特征名
        THIRD_PARTY_COOKIE_NAMES = {
            "__utma", "__utmb", "__utmc", "__utmz", "__utmv",
            "_ga", "_gid", "_gat", "_gcl_au", "_fbp", "_fbc",
            "_hj", "_mkto", "optimizely", "mp_", "intercom-",
            "hubspotutk", "_uet", "_scid", "_uetmsclkid",
            "Hm_lvt", "Hm_lpvt", "CNZZDATA",
        }

        for cookie in cookies:
            name = cookie.split("=")[0].strip() if "=" in cookie else cookie.strip()
            for tpc_name in THIRD_PARTY_COOKIE_NAMES:
                if name.startswith(tpc_name) or name == tpc_name:
                    result.findings.append(ScanFinding(
                        category="cookie",
                        sub_type="third_party_cookie",
                        source=domain,
                        severity=4,
                        detail=f"检测到第三方/追踪Cookie: {name}",
                        evidence=cookie[:100]
                    ))
                    break

    def _scan_ai_scripts(self, scripts: list[str], request_urls: list[str],
                           result: ScanResult):
        """检测AI相关脚本"""
        for url in scripts + request_urls:
            try:
                url_domain = urlparse(url).netloc
            except Exception:
                continue

            for ai_domain in self.AI_DOMAINS:
                if ai_domain in url_domain:
                    result.findings.append(ScanFinding(
                        category="ai_script",
                        sub_type="ai_api_call",
                        source=url,
                        severity=5,
                        detail=f"检测到AI服务调用: {ai_domain}",
                        evidence=url
                    ))
                    break

    def _scan_browser_fingerprint(self, inline_scripts: list[str],
                                   scripts: list[str], result: ScanResult):
        """检测浏览器指纹"""
        FP_PATTERNS: list[re.Pattern] = [
            re.compile(r"navigator\.(userAgent|platform|language|plugins|"
                       r"hardwareConcurrency|deviceMemory|languages|"
                       r"maxTouchPoints|vendor|webdriver)", re.IGNORECASE),
            re.compile(r"screen\.(width|height|colorDepth|pixelDepth|availWidth|availHeight)", re.IGNORECASE),
            re.compile(r"new AudioContext", re.IGNORECASE),
            re.compile(r"window\.devicePixelRatio", re.IGNORECASE),
            re.compile(r"Intl\.DateTimeFormat\(\).resolvedOptions", re.IGNORECASE),
            re.compile(r"navigator\.getBattery", re.IGNORECASE),
        ]

        all_scripts = inline_scripts + scripts
        detected = set()
        for script in all_scripts:
            for pattern in FP_PATTERNS:
                if pattern.search(script):
                    detected.add(pattern.pattern)

        if len(detected) >= 3:
            result.findings.append(ScanFinding(
                category="fingerprint",
                sub_type="browser_fingerprint",
                source="inline_scripts",
                severity=7,
                detail=f"检测到浏览器指纹采集（{len(detected)}项特征）",
                evidence=", ".join(list(detected)[:3])
            ))

    def _calculate_score(self, result: ScanResult) -> int:
        """计算隐私风险评分 0-100"""
        score = 0
        category_counts: dict[str, int] = {}

        for finding in result.findings:
            cat = finding.category
            category_counts[cat] = category_counts.get(cat, 0) + 1
            score += finding.severity

            # 构造告警摘要
            if cat == "tracking":
                result.threat_summary.append(f"追踪器: {finding.source[:60]}")
            elif cat == "fingerprint":
                result.threat_summary.append(f"指纹采集: {finding.sub_type}")
            elif cat == "webrtc":
                result.threat_summary.append("WebRTC泄露风险")
            elif cat == "cookie":
                result.threat_summary.append(f"追踪Cookie: {finding.evidence[:30]}")
            elif cat == "ai_script":
                result.threat_summary.append(f"AI调用: {finding.source[:60]}")

        # 生成建议
        if category_counts.get("tracking", 0) > 0:
            result.recommendations.append("建议启用第三方追踪拦截")
        if category_counts.get("fingerprint", 0) > 0:
            result.recommendations.append("建议启用反指纹保护")
        if category_counts.get("webrtc", 0) > 0:
            result.recommendations.append("建议禁用WebRTC或使用VPN")
        if category_counts.get("cookie", 0) > 0:
            result.recommendations.append("建议清除第三方Cookie")
        if category_counts.get("ai_script", 0) > 0:
            result.recommendations.append("AI请求将通过观澜网关授权管控")

        return min(score, 100)

    def _assess_risk(self, score: int) -> RiskLevel:
        if score >= 70:
            return RiskLevel.HIGH
        elif score >= 40:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def _generate_dna(self) -> str:
        seed = f"{time.time()}-privacy-scan"
        h = hashlib.sha256(seed.encode()).hexdigest()[:8]
        return f"#龍芯⚡️GUANLAN-PRIVACY-SCAN-v1.0-{h}"

    def to_dict(self, result: ScanResult) -> dict[str, object]:
        return {
            "url": result.url,
            "domain": result.domain,
            "score": result.score,
            "risk_level": result.risk_level.value,
            "findings": [
                {
                    "category": f.category,
                    "sub_type": f.sub_type,
                    "source": f.source,
                    "severity": f.severity,
                    "detail": f.detail,
                }
                for f in result.findings
            ],
            "threat_summary": result.threat_summary,
            "recommendations": result.recommendations,
            "scan_time": result.scan_time,
            "dna": result.dna,
        }


# ============================================================
# 自检
# ============================================================
if __name__ == "__main__":
    scanner = PrivacyScanner(alert_threshold=70)

    # 模拟扫描
    result = scanner.scan_page(
        url="https://example-shop.com/product/123",
        scripts=[
            "https://example-shop.com/js/app.js",
            "https://www.googletagmanager.com/gtag/js?id=UA-XXX",
            "https://connect.facebook.net/en_US/fbevents.js",
            "https://api.openai.com/v1/chat/completions",
        ],
        cookies=[
            "session=abc123",
            "_ga=GA1.2.123456789.1234567890",
            "_gid=GA1.2.987654321.1234567890",
            "_fbp=fb.1.1234567890.123456789",
        ],
        inline_scripts=[
            "navigator.userAgent + screen.width + screen.height",
            "canvas.toDataURL('image/png')",
            "new RTCPeerConnection(config)",
            "navigator.plugins; navigator.hardwareConcurrency; navigator.deviceMemory",
        ],
        request_urls=[
            "https://www.google-analytics.com/collect",
            "https://bat.bing.com/action/0",
        ],
    )

    print(json.dumps(scanner.to_dict(result), ensure_ascii=False, indent=2))
    print(f"\n风险评分: {result.score}/100 | 等级: {result.risk_level.value}")
    print(f"威胁: {len(result.threat_summary)}项 | 建议: {len(result.recommendations)}项")
    print(f"DNA: {result.dna}")
