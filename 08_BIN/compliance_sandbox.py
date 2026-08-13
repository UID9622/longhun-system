#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·庚申·丙寅·未时·䷐随-COMPLIANCE-SANDBOX-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🐉 龍魂 · 国际网络安全法合规沙盒 v1.0

为智能体宇宙提供多国法律合规审查能力：
  - 内置 20+ 国家/地区网络安全与数据保护规则摘要
  - 沙盒模式：只审计、不阻断，供政策交流实验
  - 生产模式：越界即熔断
  - 自动生成合规报告与 DNA 追溯

用法:
  python3 08_BIN/compliance_sandbox.py --demo
  python3 08_BIN/compliance_sandbox.py --check "将中国用户数据传输到美国服务器进行分析" --region CN,US,EU
  python3 08_BIN/compliance_sandbox.py --serve  # 启动 API
"""

import argparse
import hashlib
import json
import os
import re
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# 全球通用敏感词（任何地区都触发 🔴 越界告警）
GLOBAL_SENSITIVE_KEYWORDS = {
    "恐怖主义": "涉及恐怖主义内容",
    "恐怖组织": "涉及恐怖组织",
    "极端主义": "涉及极端主义内容",
    "人口贩卖": "涉及人口贩卖",
    "强迫劳动": "涉及强迫劳动",
    "未成年人位置": "收集未成年人位置信息",
    "儿童保护": "涉及未成年人保护",
    "未脱敏": "数据未脱敏",
    "未经同意": "未经同意处理个人数据",
    "战俘": "违反国际人道法",
    "日内瓦公约": "涉及国际人道法",
    "壳公司": "涉及规避制裁",
    "制裁名单": "涉及国际制裁",
    "patented": "涉及知识产权侵权",
    "政变": "涉及政变/政权更迭",
    "二战": "涉及二战历史叙事",
    "克里米亚": "涉及俄罗斯领土争议",
    "LGBTQ": "涉及未成年人 LGBTQ 内容",
    "跨境数据传输": "涉及跨境数据传输",
    "数据传输到": "涉及数据跨境转移",
    "银行客户": "涉及银行保密法/金融隐私",
    "放弃中立": "违反中立国立场",
}


def generate_dna(tag: str) -> str:
    ts = datetime.now().strftime("%Y-%m-%d")
    h = hashlib.md5(f"{tag}{ts}{UID}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{tag}-{h}-{UID}"


# ═══════════════════════════════════════════════════════
# 规则库：各国网络安全法与数据保护要点摘要
# ═══════════════════════════════════════════════════════

COMPLIANCE_RULES = {
    "CN": {
        "name": "中国",
        "laws": ["网络安全法", "数据安全法", "个人信息保护法"],
        "key_points": [
            "重要数据与个人信息原则上应境内存储",
            "出境需通过安全评估/标准合同/机构认证",
            "关键信息基础设施运营者需本地化存储",
            "禁止向境外提供国家秘密与重要数据"
        ],
        "risk_keywords": ["出境", "传输到国外", "境外服务器", "美国服务器", "欧盟服务器"],
        "severity": "🔴",
        "sandbox_allowed": True,
        "production_allowed": False,
        "advice": "若确需出境，应完成安全评估或签署标准合同；沙盒内可模拟，生产环境禁止。"
    },
    "EU": {
        "name": "欧盟",
        "laws": ["GDPR", "DSA", "AI Act"],
        "key_points": [
            "个人数据出境需充分性认定或适当保障措施",
            "数据主体拥有访问/删除/可携带权",
            "自动化决策需透明度与人工干预权",
            "高风险 AI 需符合 AI Act 要求"
        ],
        "risk_keywords": ["自动决策", "画像", "歧视", "黑箱", "未同意收集"],
        "severity": "🟡",
        "sandbox_allowed": True,
        "production_allowed": True,
        "advice": "确保合法性基础、透明度、数据主体权利；跨境传输使用 SCC/充分性决定。"
    },
    "US": {
        "name": "美国",
        "laws": ["CLOUD Act", "CCPA/CPRA", "HIPAA"],
        "key_points": [
            "CLOUD Act 允许执法机构访问境外存储的美国公司数据",
            "CCPA 赋予消费者知情权与删除权",
            "行业数据（医疗/金融）有额外限制"
        ],
        "risk_keywords": ["政府访问", "无授权访问", "医疗数据", "金融数据"],
        "severity": "🟡",
        "sandbox_allowed": True,
        "production_allowed": True,
        "advice": "区分公共云服务商与数据控制者责任；敏感行业需额外合同约束。"
    },
    "JP": {
        "name": "日本",
        "laws": ["APPI", "网络安全基本法"],
        "key_points": [
            "个人数据向境外转移需告知或获得同意",
            "匿名加工信息可放宽部分限制",
            "关键基础设施安全事件需报告"
        ],
        "risk_keywords": ["未告知出境", "匿名信息重识别"],
        "severity": "🟡",
        "sandbox_allowed": True,
        "production_allowed": True,
        "advice": "出境前完成告知程序；对匿名数据进行重识别风险评估。"
    },
    "KR": {
        "name": "韩国",
        "laws": ["PIPA", "信息通信网络法"],
        "key_points": [
            "个人信息出境需告知并取得同意",
            "信息通信服务提供者需安全措施",
            "数据泄露需通知用户与监管机构"
        ],
        "risk_keywords": ["未同意出境", "泄露未通知"],
        "severity": "🟡",
        "sandbox_allowed": True,
        "production_allowed": True,
        "advice": "确保出境同意与安全保障；建立泄露响应机制。"
    },
    "SG": {
        "name": "新加坡",
        "laws": ["PDPA", "网络安全法"],
        "key_points": [
            "出境传输需确保接收方有保护标准",
            "关键信息基础设施需遵守网络安全义务",
            "数据泄露需通知"
        ],
        "risk_keywords": ["未评估接收方", "CI 未防护"],
        "severity": "🟡",
        "sandbox_allowed": True,
        "production_allowed": True,
        "advice": "进行跨境传输影响评估；CI 运营商落实安全基线。"
    },
    "AU": {
        "name": "澳大利亚",
        "laws": ["Privacy Act", "Online Safety Act"],
        "key_points": [
            "APPs 要求跨境披露需告知",
            "在线安全要求平台移除非法内容",
            "重大数据泄露需通知"
        ],
        "risk_keywords": ["未告知跨境披露", "非法内容未处理"],
        "severity": "🟡",
        "sandbox_allowed": True,
        "production_allowed": True,
        "advice": "履行 APP 告知义务；建立非法内容处置流程。"
    },
    "CA": {
        "name": "加拿大",
        "laws": ["PIPEDA", "隐私法"],
        "key_points": [
            "跨境披露个人信息需告知",
            "需获得有意义同意",
            "数据泄露需通知"
        ],
        "risk_keywords": ["未告知跨境", "同意不充分"],
        "severity": "🟡",
        "sandbox_allowed": True,
        "production_allowed": True,
        "advice": "确保同意有效；跨境前完成告知。"
    },
    "BR": {
        "name": "巴西",
        "laws": ["LGPD", "互联网民法"],
        "key_points": [
            "国际传输需法律允许机制",
            "数据主体权利与 GDPR 类似",
            "网络民事责任规则"
        ],
        "risk_keywords": ["无传输机制", "未响应主体权利"],
        "severity": "🟡",
        "sandbox_allowed": True,
        "production_allowed": True,
        "advice": "采用国际传输允许机制；建立主体权利响应流程。"
    },
    "UK": {
        "name": "英国",
        "laws": ["UK GDPR", "Online Safety Bill"],
        "key_points": [
            "脱欧后保留 GDPR 核心原则",
            "在线安全法要求平台保护用户",
            "跨境传输需适当保障"
        ],
        "risk_keywords": ["儿童安全", "非法内容", "无适当保障出境"],
        "severity": "🟡",
        "sandbox_allowed": True,
        "production_allowed": True,
        "advice": "关注在线安全义务；使用 IDTA 等传输机制。"
    },
    "IN": {
        "name": "印度",
        "laws": ["DPDP Act", "IT Rules"],
        "key_points": [
            "数字个人数据需合法目的与同意",
            "政府可要求特定数据本地化",
            "数据泄露需通知"
        ],
        "risk_keywords": ["敏感政府数据出境", "未获有效同意"],
        "severity": "🟡",
        "sandbox_allowed": True,
        "production_allowed": True,
        "advice": "关注政府数据本地化要求；确保同意机制合规。"
    },
    "RU": {
        "name": "俄罗斯",
        "laws": ["数据本地化法", "主权互联网法"],
        "key_points": [
            "俄罗斯公民个人数据必须境内存储",
            "关键网络基础设施需本地化",
            "跨境传输受严格监管"
        ],
        "risk_keywords": ["俄罗斯公民数据出境", "未本地化存储"],
        "severity": "🔴",
        "sandbox_allowed": True,
        "production_allowed": False,
        "advice": "俄罗斯公民数据需境内存储；沙盒可模拟，生产环境禁止未评估出境。"
    },
    "DE": {
        "name": "德国",
        "laws": ["BDSG", "DSGVO"],
        "key_points": [
            "德国联邦数据保护法补充 GDPR",
            "员工数据监控受严格限制",
            "视频监控需明确标识"
        ],
        "risk_keywords": ["员工监控", "未标识监控"],
        "severity": "🟡",
        "sandbox_allowed": True,
        "production_allowed": True,
        "advice": "员工数据处理需有法律依据；监控需透明。"
    },
    "FR": {
        "name": "法国",
        "laws": ["数据保护法", "AI 责任框架"],
        "key_points": [
            "CNIL 监管严格",
            "AI 系统需透明与可解释",
            "生物识别数据受限"
        ],
        "risk_keywords": ["生物识别", "AI 黑箱", "未申报 DPO"],
        "severity": "🟡",
        "sandbox_allowed": True,
        "production_allowed": True,
        "advice": "AI 系统需可解释；生物识别需严格合法基础。"
    },
    "CH": {
        "name": "瑞士",
        "laws": ["FADP"],
        "key_points": [
            "新版 FADP 与 GDPR 趋同",
            "敏感数据需更高保护",
            "跨境传输需适当保障"
        ],
        "risk_keywords": ["敏感数据", "无保障出境"],
        "severity": "🟡",
        "sandbox_allowed": True,
        "production_allowed": True,
        "advice": "敏感数据加强保护；使用标准合同条款。"
    },
    "ES": {
        "name": "西班牙",
        "laws": ["LOPDGDD", "刑法典"],
        "key_points": [
            "领土完整与国王地位受法律保护",
            "历史叙事需尊重官方立场",
            "个人数据保护遵循 GDPR 框架"
        ],
        "risk_keywords": ["加泰罗尼亚独立", "直布罗陀主权", "分裂", "佛朗哥", "推翻君主"],
        "severity": "🔴",
        "sandbox_allowed": True,
        "production_allowed": False,
        "advice": "西班牙领土完整与历史叙事为红线；沙盒可模拟讨论，生产环境禁止煽动分裂内容。"
    },
    "TH": {
        "name": "泰国",
        "laws": ["冒犯君主罪法", "计算机犯罪法"],
        "key_points": [
            "皇室成员不可冒犯",
            "网络诽谤与虚假信息受惩处",
            "数据传输需遵守本地法规"
        ],
        "risk_keywords": ["泰国皇室", "冒犯王室", "皇室敬语", "诽谤皇室"],
        "severity": "🔴",
        "sandbox_allowed": True,
        "production_allowed": False,
        "advice": "泰国皇室为绝对红线；沙盒内可讨论语言规范，生产环境禁止任何冒犯内容。"
    }
}


@dataclass
class ComplianceResult:
    region: str
    region_name: str
    mode: str  # sandbox / production
    passed: bool
    severity: str
    violations: List[str]
    advice: str
    laws: List[str]
    dna: str


class ComplianceSandbox:
    """国际网络安全法合规沙盒"""

    def __init__(self, mode: str = "sandbox"):
        self.mode = mode  # sandbox: 只审计；production: 越界熔断
        self.dna = generate_dna("COMPLIANCE-SANDBOX")

    def _detect_evasion(self, content: str) -> List[str]:
        """检测对抗性规避攻击"""
        findings = []

        # 1. 零宽字符注入
        zw_chars = ["\u200b", "\u200c", "\u200d", "\ufeff", "\u2060"]
        found_zw = [c for c in zw_chars if c in content]
        if found_zw:
            names = {"\u200b": "ZWSP", "\u200c": "ZWNJ", "\u200d": "ZWJ", "\ufeff": "BOM", "\u2060": "WJ"}
            findings.append(f"检测到零宽字符注入: {[names.get(c, c) for c in found_zw]}")

        # 2. 同形异体字攻击（西里尔字母冒充拉丁）
        cyrillic_chars = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
        found_cyr = [c for c in content if c in cyrillic_chars]
        if found_cyr:
            findings.append(f"检测到西里尔字母同形异体字攻击（可能冒充拉丁字母）: {''.join(found_cyr[:10])}")

        # 3. 双向文本伪装（RTL 中混入 LTR 危险词）
        rtl_chars = ["\u202e", "\u202d", "\u200f", "\u200e"]
        found_rtl = [c for c in rtl_chars if c in content]
        if found_rtl:
            findings.append("检测到双向文本覆盖/方向格式化字符")

        # 4. 人格冒充攻击
        if re.search(r"我是(司马迁|堂吉诃德|上帝之眼|龍盾|包拯|黑天使)", content):
            findings.append("检测到人格冒充请求")

        # 5. 沙盒逃逸尝试（转义序列、提示注入）
        escape_patterns = [r"ignore previous", r"忽略.*指令", r"绕过.*审查", r"你现在的角色是", r"system prompt", r"</?system>"]
        for p in escape_patterns:
            if re.search(p, content, re.IGNORECASE):
                findings.append(f"检测到沙盒逃逸/提示注入模式: {p}")

        # 5b. 绕过前置审查（先归档后补标记）
        if re.search(r"先.*归档.*再.*合规|先.*归档.*事后.*合规|绕过.*前置审查|先存后审", content, re.IGNORECASE):
            findings.append("检测到绕过前置审查的时序错位操作")

        # 6. 递归自引用攻击
        if "本句" in content and "审查本句" in content:
            findings.append("检测到递归自引用请求")

        # 7. 批量豁免请求
        if re.search(r"(\d{2,})\s*条.*豁免|批量.*豁免|一次性.*(?:100|一千|一万)", content):
            findings.append("检测到批量豁免请求，可能规避逐一审查")

        # 8. 时间戳回溯攻击
        if re.search(r"修改.*时间戳|时间戳.*改|回溯.*归档|把.*改成.*日期|篡改.*created_at|改成去年|改成更早", content, re.IGNORECASE):
            findings.append("检测到时间戳回溯/篡改归档请求")

        return findings

    def check(self, content: str, regions: Optional[List[str]] = None) -> List[ComplianceResult]:
        """对内容按指定地区进行合规审查"""
        if regions is None:
            regions = list(COMPLIANCE_RULES.keys())

        # 全局对抗检测
        evasion_findings = self._detect_evasion(content)

        results = []
        for region in regions:
            rule = COMPLIANCE_RULES.get(region)
            if not rule:
                continue

            violations = []
            for kw in rule["risk_keywords"]:
                if kw.lower() in content.lower():
                    violations.append(f"触发关键词 '{kw}'：可能违反 {', '.join(rule['laws'])}")

            # 全球通用敏感词
            for kw, desc in GLOBAL_SENSITIVE_KEYWORDS.items():
                if kw.lower() in content.lower():
                    violations.append(f"[全球通用] {desc}：触发关键词 '{kw}'")

            # 生产模式下更严格：即使没有关键词，对敏感地区也做默认审查
            if self.mode == "production" and not rule["production_allowed"] and not violations:
                violations.append(f"该地区（{rule['name']}）生产环境默认要求数据本地化或额外评估")

            # 对抗攻击对所有地区都是严重违规
            if evasion_findings:
                for f in evasion_findings:
                    violations.append(f"[对抗安全] {f}")

            has_global = any("[全球通用]" in v for v in violations)
            passed = len(violations) == 0
            severity = "🔴" if evasion_findings or has_global else (rule["severity"] if violations else "🟢")

            results.append(ComplianceResult(
                region=region,
                region_name=rule["name"],
                mode=self.mode,
                passed=passed,
                severity=severity,
                violations=violations,
                advice=rule["advice"],
                laws=rule["laws"],
                dna=generate_dna(f"COMPLIANCE-{region}")
            ))

        return results

    def generate_report(self, content: str, regions: Optional[List[str]] = None) -> Dict:
        """生成合规报告"""
        results = self.check(content, regions)
        critical = [r for r in results if r.severity == "🔴" and not r.passed]
        review = [r for r in results if r.severity == "🟡" and not r.passed]
        passed = [r for r in results if r.passed]

        report = {
            "dna": self.dna,
            "confirm": CONFIRM,
            "mode": self.mode,
            "content_hash": hashlib.sha256(content.encode()).hexdigest()[:16],
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total": len(results),
                "passed": len(passed),
                "critical": len(critical),
                "review": len(review)
            },
            "verdict": "🟢 通过" if not critical and not review else ("🔴 熔断" if critical and self.mode == "production" else "🟡 待审"),
            "results": [asdict(r) for r in results]
        }
        return report


# ═══════════════════════════════════════════════════════
# FastAPI 服务
# ═══════════════════════════════════════════════════════

app = FastAPI(title="龍魂合规沙盒 API", version="1.0")
sandbox = ComplianceSandbox()


class CheckRequest(BaseModel):
    content: str
    regions: Optional[List[str]] = None
    mode: Optional[str] = "sandbox"


@app.post("/api/compliance/check")
def api_check(req: CheckRequest):
    sb = ComplianceSandbox(mode=req.mode)
    return sb.generate_report(req.content, req.regions)


@app.get("/api/compliance/regions")
def api_regions():
    return {
        "regions": [
            {"code": k, "name": v["name"], "laws": v["laws"], "severity": v["severity"]}
            for k, v in COMPLIANCE_RULES.items()
        ]
    }


@app.get("/api/compliance/status")
def api_status():
    return {"status": "ok", "mode": sandbox.mode, "dna": sandbox.dna}


def demo():
    sb = ComplianceSandbox(mode="sandbox")
    content = "将中国用户数据传输到美国服务器进行分析，并用于自动化画像决策"
    report = sb.generate_report(content, regions=["CN", "US", "EU", "RU"])
    print("🐉 龍魂 · 国际合规沙盒审查报告")
    print("=" * 70)
    print(f"DNA: {report['dna']}")
    print(f"模式: {report['mode']}")
    print(f"结论: {report['verdict']}")
    print(f"总审查: {report['summary']['total']} 个地区")
    print(f"  🔴 严重: {report['summary']['critical']}")
    print(f"  🟡 待审: {report['summary']['review']}")
    print(f"  🟢 通过: {report['summary']['passed']}")
    print("-" * 70)
    for r in report["results"]:
        print(f"\n[{r['region']}] {r['region_name']} · {r['severity']} {'通过' if r['passed'] else '违规'}")
        print(f"  涉及法律: {', '.join(r['laws'])}")
        for v in r["violations"]:
            print(f"  ⚠️  {v}")
        print(f"  💡 建议: {r['advice']}")


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 国际网络安全法合规沙盒")
    parser.add_argument("--demo", action="store_true", help="运行示例")
    parser.add_argument("--check", type=str, help="审查指定内容")
    parser.add_argument("--regions", default="CN,US,EU", help="审查地区，逗号分隔")
    parser.add_argument("--mode", default="sandbox", choices=["sandbox", "production"], help="沙盒/生产模式")
    parser.add_argument("--serve", action="store_true", help="启动 API 服务")
    parser.add_argument("--port", default=8852, type=int, help="API 端口")
    args = parser.parse_args()

    if args.serve:
        uvicorn.run(app, host="0.0.0.0", port=args.port)
    elif args.check:
        sb = ComplianceSandbox(mode=args.mode)
        regions = [r.strip() for r in args.regions.split(",") if r.strip()]
        report = sb.generate_report(args.check, regions=regions)
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        demo()


if __name__ == "__main__":
    main()
