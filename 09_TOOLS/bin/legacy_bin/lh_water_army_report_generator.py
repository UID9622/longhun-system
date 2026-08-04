#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
lh_water_army_report_generator — 龍魂·举报材料自动生成器 v1.0

根据检测结果自动生成标准化举报材料，包含：
  - 证据摘要（水军行为总结）
  - 完整证据链（每条证据的详细描述+原始数据哈希）
  - 法律条款引用（自动匹配相关法条+大白话解释）
  - 举报建议（向哪个平台举报、举报理由、预期处理）
  - DNA不可篡改签名

支持输出格式：Markdown / JSON / HTML / 纯文本 举报函

用法：
  python3 bin/lh_water_army_report_generator.py --forensic forensic_pack.json
  python3 bin/lh_water_army_report_generator.py --findings findings.json --format markdown
  python3 bin/lh_water_army_report_generator.py --case-id CASE001 --output report.md

DNA: #龍芯⚡️丙午·辛未·REPORT-GENERATOR-v1.0-5D7C1A9E
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DNA = "#龍芯⚡️丙午·辛未·REPORT-GENERATOR-v1.0-5D7C1A9E"
DNA_HASH = hashlib.sha256(DNA.encode()).hexdigest()[:16]

AUDIT_GREEN = "🟢"
AUDIT_YELLOW = "🟡"
AUDIT_RED = "🔴"

# ============================================
# 平台举报渠道配置
# ============================================
PLATFORM_REPORT_CHANNELS = {
    "weibo": {
        "name": "微博",
        "report_url": "https://service.account.weibo.com/report",
        "report_email": "weiboreport@vip.sina.com",
        "tips": "通过微博举报入口提交，选择'垃圾营销'或'人身攻击'类别",
    },
    "douyin": {
        "name": "抖音",
        "report_url": "https://www.douyin.com/user/self/report",
        "report_email": "feedback@douyin.com",
        "tips": "长按评论→举报→选择'垃圾广告'或'违规内容'",
    },
    "zhihu": {
        "name": "知乎",
        "report_url": "https://www.zhihu.com/report",
        "report_email": "support@zhihu.com",
        "tips": "点击评论右侧'...'→举报→选择对应违规类型",
    },
    "bilibili": {
        "name": "B站",
        "report_url": "https://www.bilibili.com/video/supplement",
        "report_email": "help@bilibili.com",
        "tips": "举报评论→选择'引战'或'人身攻击'或'垃圾广告'",
    },
    "xiaohongshu": {
        "name": "小红书",
        "report_url": "https://www.xiaohongshu.com/report",
        "report_email": "support@xiaohongshu.com",
        "tips": "长按评论→举报→选择对应类型",
    },
    "wechat": {
        "name": "微信公众号/视频号",
        "report_url": "https://mp.weixin.qq.com/",
        "report_email": "weixinreport@qq.com",
        "tips": "通过腾讯110小程序或微信客户端举报入口提交",
    },
    "default": {
        "name": "网络平台",
        "report_url": "",
        "report_email": "",
        "tips": "通过平台官方举报渠道提交，同时可向网信办12377举报",
    },
}

# ============================================
# 法律条款库
# ============================================
LAW_REFERENCES = [
    {
        "name": "网络安全法 第12条",
        "official": "任何个人和组织使用网络应当遵守宪法法律，遵守公共秩序，尊重社会公德，不得利用网络从事...传播暴力、淫秽色情信息，编造、传播虚假信息扰乱经济秩序和社会秩序等活动。",
        "plain": "不能用网络传播虚假信息、扰乱社会秩序。水军刷评属于违法行为。",
        "applicable_to": ["虚假评论", "水军", "造谣传谣"],
    },
    {
        "name": "网络安全法 第24条",
        "official": "网络运营者为用户办理网络接入、域名注册服务，办理固定电话、移动电话等入网手续，或者为用户提供信息发布、即时通讯等服务...应当要求用户提供真实身份信息。",
        "plain": "网络平台必须要求用户实名认证。不提供实名就是平台违法。",
        "applicable_to": ["未实名账号", "匿名评论", "身份造假"],
    },
    {
        "name": "民法典 第1024条",
        "official": "民事主体享有名誉权。任何组织或者个人不得以侮辱、诽谤等方式侵害他人的名誉权。",
        "plain": "不能用侮辱、诽谤的方式伤害他人的名誉。恶意差评、造谣都算。",
        "applicable_to": ["恶意差评", "诽谤", "名誉侵害", "竞品抹黑"],
    },
    {
        "name": "民法典 第1194条",
        "official": "网络用户、网络服务提供者利用网络侵害他人民事权益的，应当承担侵权责任。",
        "plain": "在网上侵害别人权益，要承担法律责任。",
        "applicable_to": ["网络侵权", "恶意剪辑", "虚假信息传播"],
    },
    {
        "name": "刑法 第246条 诽谤罪",
        "official": "以暴力或者其他方法公然侮辱他人或者捏造事实诽谤他人，情节严重的，处三年以下有期徒刑、拘役、管制或者剥夺政治权利。",
        "plain": "严重的造谣诽谤要坐牢（最高3年）。",
        "applicable_to": ["严重诽谤", "造谣", "恶意剪辑造谣"],
    },
    {
        "name": "反不正当竞争法 第8条",
        "official": "经营者不得对其商品的性能、功能、质量、销售状况、用户评价、曾获荣誉等作虚假或者引人误解的商业宣传，欺骗、误导消费者。经营者不得通过组织虚假交易等方式，帮助其他经营者进行虚假或者引人误解的商业宣传。",
        "plain": "商家不能刷假好评骗人，也不能找人刷竞争对手的差评。",
        "applicable_to": ["刷单刷评", "虚假好评", "竞品抹黑"],
    },
    {
        "name": "反不正当竞争法 第11条",
        "official": "经营者不得编造、传播虚假信息或者误导性信息，损害竞争对手的商业信誉、商品声誉。",
        "plain": "不能编造假消息损害竞争对手的名声。商业诋毁违法。",
        "applicable_to": ["竞品抹黑", "商业诋毁", "虚假差评"],
    },
    {
        "name": "电子商务法 第17条",
        "official": "电子商务经营者应当全面、真实、准确、及时地披露商品或者服务信息，保障消费者的知情权和选择权。电子商务经营者不得以虚构交易、编造用户评价等方式进行虚假或者引人误解的商业宣传，欺骗、误导消费者。",
        "plain": "电商不能刷假评价骗消费者。",
        "applicable_to": ["虚假评论", "刷单刷评", "电商欺诈"],
    },
    {
        "name": "网络信息内容生态治理规定 第6条",
        "official": "网络信息内容生产者不得制作、复制、发布含有下列内容的违法信息：...(八)散布谣言，扰乱经济秩序和社会秩序的...",
        "plain": "不能在网上散布谣言，水军带节奏属于散布谣言。",
        "applicable_to": ["水军带节奏", "散布谣言", "虚假信息"],
    },
    {
        "name": "治安管理处罚法 第25条",
        "official": "散布谣言，谎报险情、疫情、警情或者以其他方法故意扰乱公共秩序的，处五日以上十日以下拘留，可以并处五百元以下罚款；情节较轻的，处五日以下拘留或者五百元以下罚款。",
        "plain": "散布谣言扰乱秩序的，拘留5-10天，罚款最高500元。",
        "applicable_to": ["散布谣言", "恶意剪辑传播", "虚假信息"],
    },
    {
        "name": "关于办理利用信息网络实施诽谤等刑事案件适用法律若干问题的解释",
        "official": "同一诽谤信息实际被点击、浏览次数达到五千次以上，或者被转发次数达到五百次以上的，应当认定为'情节严重'。",
        "plain": "网上诽谤被浏览5000次或转发500次以上，就构成情节严重，要追究刑事责任。",
        "applicable_to": ["网络诽谤", "造谣传播", "水军扩散"],
    },
]


# ============================================
# 法律条款匹配
# ============================================

def match_law_references(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """根据检测发现匹配相关法律条款"""
    matched = []
    finding_types = set()

    for f in findings:
        ftype = f.get("type", "")
        detail = f.get("detail", "")
        finding_types.add(ftype)

        for law in LAW_REFERENCES:
            if law["name"] in [m["name"] for m in matched]:
                continue
            for keyword in law["applicable_to"]:
                if keyword in ftype or keyword in detail:
                    matched.append(law)
                    break

    # 如果匹配太少，补充通用条款
    if len(matched) < 2:
        for law in LAW_REFERENCES:
            if law["name"] not in [m["name"] for m in matched]:
                if any(kw in str(finding_types) for kw in ["虚假", "水军", "评论", "剪辑", "造谣"]):
                    matched.append(law)
                if len(matched) >= 3:
                    break

    return matched[:5]


# ============================================
# 举报材料生成
# ============================================

def generate_report(
    forensic_pack: Dict[str, Any],
    all_results: Optional[Dict[str, Any]] = None,
    target_info: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """生成完整举报材料"""

    evidence_chain = forensic_pack.get("evidence_chain", [])
    all_findings: List[Dict] = []

    if all_results:
        for key in ["behavior", "malicious_edit", "fake_review"]:
            section = all_results.get(key, {})
            all_findings.extend(section.get("findings", []))

    # 匹配法律条款
    legal_matches = match_law_references(all_findings) if all_findings else match_law_references(evidence_chain)

    # 确定平台
    platform = (target_info or {}).get("platform", "default")
    channel = PLATFORM_REPORT_CHANNELS.get(platform, PLATFORM_REPORT_CHANNELS["default"])

    # 证据统计
    red_ev = [e for e in evidence_chain if e.get("level") == AUDIT_RED]
    yellow_ev = [e for e in evidence_chain if e.get("level") == AUDIT_YELLOW]

    report = {
        "report_id": f"RPT-{DNA_HASH}",
        "generated_at": datetime.now().isoformat(),
        "dna": DNA,
        "version": "v1.0",

        # 基本信息
        "case_info": {
            "title": _generate_case_title(all_findings, target_info),
            "target": target_info or {},
            "incident_date": datetime.now().strftime("%Y-%m-%d"),
            "reporter": "龍魂系统自动生成",
        },

        # 摘要
        "summary": {
            "total_evidence_items": len(evidence_chain),
            "serious_evidence": len(red_ev),
            "suspicious_evidence": len(yellow_ev),
            "main_issues": _extract_main_issues(all_findings),
            "recommended_action": _recommend_action(len(red_ev), len(yellow_ev)),
        },

        # 证据列表
        "evidence": [
            {
                "id": e.get("evidence_id", ""),
                "type": e.get("source", "unknown"),
                "severity": "严重" if e.get("level") == AUDIT_RED else ("可疑" if e.get("level") == AUDIT_YELLOW else "提示"),
                "description": e.get("detail", ""),
                "data_integrity_hash": e.get("raw_data_hash", ""),
            }
            for e in evidence_chain
        ],

        # 法律依据
        "legal_basis": [
            {
                "law": l["name"],
                "official_text": l["official"],
                "plain_explanation": l["plain"],
            }
            for l in legal_matches
        ],

        # 举报指引
        "report_guidance": {
            "channel": channel,
            "national_report": {
                "name": "国家网信办举报中心",
                "url": "https://www.12377.cn",
                "phone": "12377",
                "tips": "情节严重的网络水军行为可通过12377举报",
            },
            "tips": [
                "举报时附上本报告中的证据编号和完整性哈希",
                "要求平台依据《网络安全法》第24条对水军账号进行实名核验",
                "如涉及商业诽谤，可同步向市场监管部门举报",
                "保留原始数据作为电子证据",
            ],
        },

        # 完整性签名
        "integrity": {
            "report_hash": hashlib.sha256(
                json.dumps(evidence_chain, ensure_ascii=False, sort_keys=True).encode()
            ).hexdigest(),
            "dna": DNA,
            "generator": "lh_water_army_report_generator.py v1.0",
            "immutable": True,
        },
    }

    return {
        "phase": "举报材料生成",
        "status": "completed",
        "report": report,
    }


def _generate_case_title(findings: List[Dict], target_info: Optional[Dict]) -> str:
    """生成案件标题"""
    types = set(f.get("type", "") for f in findings)
    if "恶意剪辑" in str(types) or "快剪拼接" in str(types) or "PS合成" in str(types):
        base = "涉嫌恶意剪辑及虚假信息传播"
    elif "未实名" in str(types) and "模板化" in str(types):
        base = "涉嫌未实名账号批量虚假评论"
    elif "模板化" in str(types) or "刷单" in str(types):
        base = "涉嫌批量刷评及虚假营销"
    elif "协同" in str(types):
        base = "涉嫌协同水军行为"
    else:
        base = "涉嫌网络水军违规行为"

    if target_info and target_info.get("url"):
        base += f"（涉及内容：{target_info.get('url', '')[:30]}）"

    return base


def _extract_main_issues(findings: List[Dict]) -> List[str]:
    """提取主要问题"""
    issues = []
    for f in findings[:5]:
        issues.append(f.get("detail", f.get("type", "未知")))
    if not issues:
        issues = ["经龍魂系统检测，存在可疑水军行为模式"]
    return issues


def _recommend_action(red_count: int, yellow_count: int) -> str:
    if red_count >= 3:
        return "建议立即向平台举报，并保留证据向网信办12377举报，必要时向公安机关报案"
    elif red_count >= 1:
        return "建议向平台举报，要求平台对水军账号进行实名核验及降权处理"
    elif yellow_count >= 3:
        return "建议向平台反馈异常情况，持续观察后续行为"
    else:
        return "建议记录存档，持续监测"


# ============================================
# 格式化输出
# ============================================

def format_report_markdown(report: Dict[str, Any]) -> str:
    """生成Markdown格式举报材料"""
    r = report["report"]
    case = r["case_info"]
    summary = r["summary"]
    guidance = r["report_guidance"]

    lines = []
    lines.append(f"# 网络水军违规行为举报材料")
    lines.append("")
    lines.append(f"**举报编号**: {r['report_id']}  ")
    lines.append(f"**生成时间**: {r['generated_at']}  ")
    lines.append(f"**DNA追溯码**: {r['dna']}  ")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"## 一、案件概况")
    lines.append("")
    lines.append(f"**案件标题**: {case['title']}  ")
    lines.append(f"**涉及日期**: {case['incident_date']}  ")
    lines.append("")

    if case["target"]:
        lines.append("**涉及内容**:")
        for k, v in case["target"].items():
            lines.append(f"- {k}: {v}")
        lines.append("")

    lines.append(f"## 二、检测摘要")
    lines.append("")
    lines.append(f"- 证据条目: {summary['total_evidence_items']} 条")
    lines.append(f"- 🔴 严重问题: {summary['serious_evidence']} 项")
    lines.append(f"- 🟡 可疑问题: {summary['suspicious_evidence']} 项")
    lines.append("")
    lines.append("**主要问题**:")
    for issue in summary["main_issues"][:5]:
        lines.append(f"- {issue}")
    lines.append("")
    lines.append(f"**建议措施**: {summary['recommended_action']}")
    lines.append("")

    lines.append("## 三、证据详情")
    lines.append("")
    lines.append("| 编号 | 类型 | 严重程度 | 描述 | 数据哈希 |")
    lines.append("|------|------|----------|------|----------|")
    for e in r["evidence"]:
        desc = e["description"][:60]
        hash_short = e["data_integrity_hash"][:12] if e.get("data_integrity_hash") else "-"
        lines.append(f"| {e['id']} | {e['type']} | {e['severity']} | {desc} | {hash_short} |")
    lines.append("")

    lines.append("## 四、法律依据")
    lines.append("")
    for i, law in enumerate(r["legal_basis"], 1):
        lines.append(f"### {i}. {law['law']}")
        lines.append(f"**原文**: {law['official_text']}  ")
        lines.append(f"**大白话**: {law['plain_explanation']}  ")
        lines.append("")

    lines.append("## 五、举报指引")
    lines.append("")
    lines.append(f"**首选举报渠道**: {guidance['channel']['name']}")
    if guidance['channel'].get('report_url'):
        lines.append(f"- 举报链接: {guidance['channel']['report_url']}")
    if guidance['channel'].get('report_email'):
        lines.append(f"- 举报邮箱: {guidance['channel']['report_email']}")
    lines.append(f"- 操作提示: {guidance['channel']['tips']}")
    lines.append("")
    lines.append(f"**国家举报渠道**: {guidance['national_report']['name']}")
    lines.append(f"- 举报网站: {guidance['national_report']['url']}")
    lines.append(f"- 举报电话: {guidance['national_report']['phone']}")
    lines.append(f"- 说明: {guidance['national_report']['tips']}")
    lines.append("")
    lines.append("**举报建议**:")
    for tip in guidance["tips"]:
        lines.append(f"- {tip}")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"**报告完整性哈希**: `{r['integrity']['report_hash']}`  ")
    lines.append(f"**生成引擎**: {r['integrity']['generator']}  ")
    lines.append(f"**DNA签名**: {r['integrity']['dna']}  ")
    lines.append("")
    lines.append("> 本报告由龍魂·拔水军系统自动生成，所有证据附带完整性哈希，不可篡改。")
    lines.append("> 铁律：只标记不封禁 · 只降权不删号 · 可申诉可追溯 · 依法举报")

    return "\n".join(lines)


def format_report_html(report: Dict[str, Any]) -> str:
    """生成HTML格式举报材料"""
    r = report["report"]
    case = r["case_info"]
    summary = r["summary"]
    guidance = r["report_guidance"]

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>网络水军举报材料 - {case['title'][:20]}</title>
<style>
  body {{ font-family: -apple-system, 'PingFang SC', sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; color: #e0d8c0; background: #1a1a2e; line-height: 1.8; }}
  h1 {{ color: #d4a843; border-bottom: 2px solid #d4a843; padding-bottom: 10px; }}
  h2 {{ color: #c9a24e; margin-top: 30px; }}
  h3 {{ color: #b8943f; }}
  table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
  th, td {{ padding: 10px 12px; border: 1px solid #3a3a5c; text-align: left; }}
  th {{ background: #2a2a4a; color: #d4a843; }}
  .red {{ color: #e74c3c; font-weight: bold; }}
  .yellow {{ color: #f39c12; }}
  .green {{ color: #2ecc71; }}
  .meta {{ color: #8a8aaa; font-size: 0.9em; }}
  .hash {{ font-family: monospace; font-size: 0.85em; color: #7a7aaa; }}
  blockquote {{ border-left: 3px solid #d4a843; padding-left: 15px; margin: 20px 0; color: #aaa; }}
  .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #333; color: #666; font-size: 0.85em; }}
</style>
</head>
<body>
<h1>网络水军违规行为举报材料</h1>
<p class="meta">举报编号: {r['report_id']} | 生成时间: {r['generated_at']}</p>
<p class="meta">DNA追溯: {r['dna']}</p>

<h2>一、案件概况</h2>
<p><strong>案件标题:</strong> {case['title']}</p>
<p><strong>涉及日期:</strong> {case['incident_date']}</p>

<h2>二、检测摘要</h2>
<ul>
<li>证据条目: {summary['total_evidence_items']} 条</li>
<li class="red">严重问题: {summary['serious_evidence']} 项</li>
<li class="yellow">可疑问题: {summary['suspicious_evidence']} 项</li>
</ul>
<p><strong>主要问题:</strong></p>
<ul>
{''.join(f'<li>{i}</li>' for i in summary['main_issues'][:5])}
</ul>
<p><strong>建议措施:</strong> {summary['recommended_action']}</p>

<h2>三、证据详情</h2>
<table>
<tr><th>编号</th><th>类型</th><th>严重程度</th><th>描述</th><th>数据哈希</th></tr>
{''.join(f'<tr><td>{e["id"]}</td><td>{e["type"]}</td><td class="{_severity_class(e["severity"])}">{e["severity"]}</td><td>{e["description"][:80]}</td><td class="hash">{e.get("data_integrity_hash", "-")[:12]}</td></tr>' for e in r['evidence'])}
</table>

<h2>四、法律依据</h2>
{''.join(f'<h3>{i+1}. {l["law"]}</h3><p><strong>原文:</strong> {l["official_text"]}</p><p><strong>白话:</strong> {l["plain_explanation"]}</p>' for i, l in enumerate(r['legal_basis']))}

<h2>五、举报指引</h2>
<p><strong>首选渠道:</strong> {guidance['channel']['name']}</p>
<ul>
<li>举报链接: {guidance['channel'].get('report_url', 'N/A')}</li>
<li>操作提示: {guidance['channel']['tips']}</li>
</ul>
<p><strong>国家渠道:</strong> {guidance['national_report']['name']}</p>
<ul>
<li>网站: {guidance['national_report']['url']}</li>
<li>电话: {guidance['national_report']['phone']}</li>
</ul>

<div class="footer">
<p>报告完整性哈希: <span class="hash">{r['integrity']['report_hash']}</span></p>
<p>生成引擎: {r['integrity']['generator']} | DNA: {r['integrity']['dna']}</p>
<blockquote>本报告由龍魂·拔水军系统自动生成，所有证据附带完整性哈希，不可篡改。<br>铁律：只标记不封禁 · 只降权不删号 · 可申诉可追溯 · 依法举报</blockquote>
</div>
</body>
</html>"""
    return html


def _severity_class(severity: str) -> str:
    if severity == "严重":
        return "red"
    elif severity == "可疑":
        return "yellow"
    return "green"


def format_report_plain(report: Dict[str, Any]) -> str:
    """生成纯文本举报函"""
    r = report["report"]
    case = r["case_info"]
    summary = r["summary"]

    lines = []
    lines.append("=" * 60)
    lines.append("  网络水军违规行为举报函")
    lines.append("=" * 60)
    lines.append(f"举报编号: {r['report_id']}")
    lines.append(f"日期: {case['incident_date']}")
    lines.append("")
    lines.append(f"致相关平台及监管部门：")
    lines.append("")
    lines.append(f"经龍魂系统检测，发现以下网络水军违规行为：")
    lines.append(f"  {case['title']}")
    lines.append("")
    lines.append("主要问题：")
    for i, issue in enumerate(summary["main_issues"][:5], 1):
        lines.append(f"  {i}. {issue}")
    lines.append("")
    lines.append(f"共发现 {summary['total_evidence_items']} 条证据，")
    lines.append(f"其中严重问题 {summary['serious_evidence']} 项，可疑问题 {summary['suspicious_evidence']} 项。")
    lines.append("")
    lines.append("相关法律依据：")
    for i, law in enumerate(r["legal_basis"], 1):
        lines.append(f"  {i}. {law['law']}: {law['plain_explanation']}")
    lines.append("")
    lines.append(f"建议措施: {summary['recommended_action']}")
    lines.append("")
    lines.append(f"证据完整性哈希: {r['integrity']['report_hash']}")
    lines.append(f"DNA签名: {r['integrity']['dna']}")
    lines.append("")
    lines.append("=" * 60)
    lines.append("  龍魂系统 · 自动生成 · 依法举报 · 证据不可篡改")
    lines.append("=" * 60)

    return "\n".join(lines)


# ============================================
# 命令行入口
# ============================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="龍魂·举报材料自动生成器 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
输出格式:
  markdown  — Markdown格式报告（默认）
  html      — HTML格式（可直接打印或提交）
  plain     — 纯文本举报函
  json      — JSON原始数据
        """,
    )

    parser.add_argument("--forensic", help="取证包JSON文件（来自统帅引擎Phase 4输出）")
    parser.add_argument("--findings", help="检测发现JSON文件")
    parser.add_argument("--target", help="目标URL或文章标识")
    parser.add_argument("--platform", help="平台名称（weibo/douyin/zhihu等）")
    parser.add_argument("--format", choices=["markdown", "html", "plain", "json"], default="markdown", help="输出格式")
    parser.add_argument("--output", help="输出文件路径")

    args = parser.parse_args()

    # 加载数据
    forensic_pack = {}
    all_results = {}

    if args.forensic:
        path = Path(args.forensic)
        if path.exists():
            forensic_pack = json.loads(path.read_text(encoding="utf-8"))
            # forensic文件可能包含嵌套的all_results
            if "full_forensic_pack" in forensic_pack:
                forensic_pack = forensic_pack["full_forensic_pack"]

    if args.findings:
        path = Path(args.findings)
        if path.exists():
            all_results = json.loads(path.read_text(encoding="utf-8"))

    # 如果没有forensic但有findings，构建基础forensic
    if not forensic_pack and all_results:
        findings = all_results.get("findings", [])
        forensic_pack = {
            "evidence_chain": [
                {
                    "evidence_id": f"EVD-{DNA_HASH}-{i+1:04d}",
                    "source": f.get("type", f.get("detector", "unknown")),
                    "level": f.get("level", AUDIT_YELLOW),
                    "detail": f.get("detail", ""),
                    "raw_data_hash": hashlib.sha256(json.dumps(f, sort_keys=True).encode()).hexdigest(),
                    "timestamp": datetime.now().isoformat(),
                }
                for i, f in enumerate(findings)
            ],
            "pack_hash": hashlib.sha256(json.dumps(findings, sort_keys=True).encode()).hexdigest(),
        }

    target_info = {"url": args.target} if args.target else None
    if args.platform:
        target_info = target_info or {}
        target_info["platform"] = args.platform

    # 生成报告
    result = generate_report(forensic_pack, all_results, target_info)
    report = result["report"]

    # 格式化输出
    if args.format == "json":
        output = json.dumps(result, ensure_ascii=False, indent=2)
    elif args.format == "html":
        output = format_report_html(result)
    elif args.format == "plain":
        output = format_report_plain(result)
    else:  # markdown
        output = format_report_markdown(result)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"✅ 举报材料已生成: {args.output}")
        print(f"   格式: {args.format}")
        print(f"   编号: {report['report_id']}")
    else:
        print(output)


if __name__ == "__main__":
    main()
