#!/usr/bin/env python3
"""
龍魂双盾引擎 · Shield Engine v1.0
===================================
UID9622 原创 · 入口盾 + 出口盾 + 数字根熔断 + 三色审计

盾的位置设计思路：
  入口盾（Inbox Gate）= 在 Learning Inbox 投喂口做第一道拦截
    → 内容进来时：分类贴标签、数字根检测、污染过滤、敏感信息拦截
    → 决定：放行 / 待审 / 熔断拒绝

  出口盾（Output Gate）= 在知识输出/分享时做最后一道审查
    → 内容出去时：检查是否含隐私数据、是否符合三色审计、DNA追溯码是否完整
    → 决定：放行 / 脱敏后放行 / 阻止输出

  数字根熔断（Digital Root Fuse）= 嵌入双盾的第一道闸门
    → dr(n) = 1 + ((n-1) mod 9)
    → {1,2,4,5,7,8} 🟢通行 | {6} 🟡待审 | {3,9} 🔴熔断

用法：
  # 入口检测
  python shield_engine.py gate-in --text "要投喂的内容" --url "https://..."

  # 出口检测
  python shield_engine.py gate-out --text "要输出的内容"

  # 单独测试数字根
  python shield_engine.py dr --text "测试123456"

  # 完整管道：入口检测 → 分类 → 卦象 → 骨检索 一条龙
  python shield_engine.py pipeline --text "内容" --url "https://..."
"""

import re
import json
import hashlib
import argparse
import os
import sys
from datetime import datetime
from collections import Counter


# ============================================================
# 一、数字根熔断器（洛书369 · 第一道闸门）
# ============================================================

class DigitalRootFuse:
    """
    数字根熔断闸门
    数学来源：洛书369 · dr(n)不动点定理
    公式：dr(n) = 1 + ((n-1) mod 9)，任意正整数压缩到1-9
    """

    # 三色分区
    GREEN = {1, 2, 4, 5, 7, 8}   # 🟢 通行
    YELLOW = {6}                    # 🟡 待审
    RED = {3, 9}                    # 🔴 熔断

    @staticmethod
    def extract_numbers(text):
        """从文本中提取所有数字"""
        digits = re.findall(r'\d', text)
        return digits

    @staticmethod
    def digital_root(n):
        """计算数字根 dr(n) = 1 + ((n-1) mod 9)"""
        if n == 0:
            return 0
        return 1 + ((n - 1) % 9)

    def check(self, text):
        """
        对文本执行数字根熔断检测
        返回: {"dr": int, "color": str, "action": str, "detail": str}
        """
        digits = self.extract_numbers(text)

        if not digits:
            return {
                "dr": 0,
                "color": "⬜ 无数字",
                "action": "pass",
                "detail": "无数字内容，跳过熔断，走正常流程"
            }

        # 所有数字求和
        digit_sum = sum(int(d) for d in digits)
        dr = self.digital_root(digit_sum)

        if dr in self.GREEN:
            return {
                "dr": dr,
                "color": "🟢 绿色通行",
                "action": "pass",
                "detail": f"dr={dr}，属于绿色区间{{1,2,4,5,7,8}}，正常通行"
            }
        elif dr in self.YELLOW:
            return {
                "dr": dr,
                "color": "🟡 黄色待审",
                "action": "review",
                "detail": f"dr={dr}，属于黄色区间{{6}}，需人工审核补充数据/来源/边界"
            }
        elif dr in self.RED:
            # 生成证据链哈希
            evidence_hash = hashlib.sha256(
                f"{text}|{datetime.now().isoformat()}|dr={dr}".encode()
            ).hexdigest()[:16].upper()
            return {
                "dr": dr,
                "color": "🔴 红色熔断",
                "action": "fuse",
                "detail": f"【熔断】dr={dr}，拒绝处理。证据链哈希: {evidence_hash}",
                "evidence_hash": evidence_hash
            }

        # 不应到达这里
        return {"dr": dr, "color": "未知", "action": "pass", "detail": ""}


# ============================================================
# 二、入口盾（Inbox Gate · 投喂口拦截）
# ============================================================

class InboxGate:
    """
    入口盾：Learning Inbox 的第一道防线

    检测项：
    1. 数字根熔断（第一道闸门，优先级最高）
    2. 内容分类贴标签
    3. 污染检测（营销/水文/空洞结论）
    4. 敏感信息检测（密码/密钥/个人隐私）
    5. 来源可信度评估
    """

    def __init__(self):
        self.dr_fuse = DigitalRootFuse()

        # 污染关键词（营销/水文标记）
        self.pollution_markers = {
            "high": [  # 高污染
                "震惊", "必看", "99%的人不知道", "年入百万", "躺赚",
                "一夜暴富", "月薪过万", "绝密", "限时免费", "点击领取",
                "手把手教你", "保姆级", "一文读懂", "干货满满",
                "建议收藏", "赶紧转发", "不看后悔", "独家揭秘",
            ],
            "medium": [  # 中污染
                "深度好文", "强烈推荐", "吐血整理", "万字长文",
                "终极指南", "从入门到精通", "一篇就够",
            ]
        }

        # 敏感信息模式
        self.sensitive_patterns = [
            (r'(?:password|密码|pwd)\s*[:=：]\s*\S+', "密码泄露"),
            (r'(?:sk-|sk_)[a-zA-Z0-9]{20,}', "API密钥"),
            (r'(?:AKIA|ASIA)[A-Z0-9]{16}', "AWS密钥"),
            (r'ghp_[a-zA-Z0-9]{36}', "GitHub Token"),
            (r'\b\d{17}[\dXx]\b', "身份证号"),
            (r'\b1[3-9]\d{9}\b', "手机号"),
            (r'(?:private[_ ]?key|私钥)\s*[:=：]', "私钥泄露"),
        ]

        # 内容类型关键词
        self.type_keywords = {
            "Website": ["http", "https", "www", ".com", ".io", ".org", "网站", "官网"],
            "Paper": ["论文", "paper", "arxiv", "研究", "实验", "结论", "摘要", "abstract"],
            "Video": ["视频", "video", "youtube", "bilibili", "b站", "看了", "讲了"],
            "Code": ["代码", "code", "github", "仓库", "repo", "函数", "class", "def ", "import"],
            "Idea": ["想法", "灵感", "突然想到", "如果", "能不能", "我觉得", "试试"],
            "Trend": ["趋势", "未来", "风口", "赛道", "方向", "发展", "行业"],
        }

    def scan(self, text, url=None):
        """
        完整入口扫描
        返回: {
            "allowed": bool,
            "dr_result": dict,
            "content_type": str,
            "pollution_level": str,
            "sensitive_alerts": list,
            "tags": list,
            "recommendation": str
        }
        """
        result = {
            "timestamp": datetime.now().isoformat(),
            "input_length": len(text),
            "url": url,
            "tags": [],
        }

        # === 第一关：数字根熔断（最高优先级）===
        dr_result = self.dr_fuse.check(text)
        result["dr_result"] = dr_result

        if dr_result["action"] == "fuse":
            result["allowed"] = False
            result["recommendation"] = f"🔴 熔断拒绝 · {dr_result['detail']}"
            result["tags"].append("🔴熔断")
            return result

        if dr_result["action"] == "review":
            result["tags"].append("🟡待审")

        # === 第二关：敏感信息检测 ===
        sensitive_alerts = []
        for pattern, alert_type in self.sensitive_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                sensitive_alerts.append(alert_type)
        result["sensitive_alerts"] = sensitive_alerts

        if sensitive_alerts:
            result["tags"].append("⚠️敏感")
            # 敏感信息不直接熔断，但标记为高优先审核
            result["recommendation"] = f"⚠️ 检测到敏感信息: {', '.join(sensitive_alerts)}。建议脱敏后再入库。"
            result["allowed"] = dr_result["action"] != "review"  # 如果同时黄色待审+敏感，则不放行
            if not result["allowed"]:
                result["tags"].append("🔒需脱敏")
                return result

        # === 第三关：内容分类 ===
        content_type = self._classify_type(text, url)
        result["content_type"] = content_type
        result["tags"].append(f"📂{content_type}")

        # === 第四关：污染检测 ===
        pollution = self._check_pollution(text)
        result["pollution_level"] = pollution["level"]
        result["pollution_markers_found"] = pollution["markers"]

        if pollution["level"] == "high":
            result["tags"].append("🗑️高污染")
        elif pollution["level"] == "medium":
            result["tags"].append("⚡中污染")
        else:
            result["tags"].append("✨纯净")

        # === 第五关：来源可信度 ===
        if url:
            trust = self._check_source_trust(url)
            result["source_trust"] = trust["level"]
            result["tags"].append(f"🔗{trust['level']}")

        # === 综合判断 ===
        if dr_result["action"] == "review":
            result["allowed"] = False
            result["recommendation"] = f"🟡 黄色待审 · dr={dr_result['dr']}，请补充数据/来源/边界后重新提交"
        elif pollution["level"] == "high" and not sensitive_alerts:
            result["allowed"] = True  # 高污染可以进，但标记明显
            result["recommendation"] = "⚡ 内容可入库但污染指数高，净化时需大量过滤"
        else:
            result["allowed"] = True
            result["recommendation"] = "🟢 通行 · 内容可安全入库"

        # 生成入口DNA
        content_hash = hashlib.sha256(text.encode()).hexdigest()[:8].upper()
        result["gate_dna"] = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-GATE-IN-{content_hash}"
        result["tags_summary"] = " | ".join(result["tags"])

        return result

    def _classify_type(self, text, url=None):
        """自动分类内容类型"""
        scores = {}
        combined = text + (f" {url}" if url else "")
        for type_name, keywords in self.type_keywords.items():
            score = sum(1 for kw in keywords if kw.lower() in combined.lower())
            scores[type_name] = score

        if not any(scores.values()):
            return "Idea"  # 默认归类为想法

        return max(scores, key=scores.get)

    def _check_pollution(self, text):
        """检测内容污染程度"""
        high_found = [m for m in self.pollution_markers["high"] if m in text]
        med_found = [m for m in self.pollution_markers["medium"] if m in text]

        if len(high_found) >= 2:
            return {"level": "high", "markers": high_found}
        elif high_found or len(med_found) >= 2:
            return {"level": "medium", "markers": high_found + med_found}
        else:
            return {"level": "low", "markers": med_found}

    def _check_source_trust(self, url):
        """评估来源可信度"""
        trusted_domains = [
            "arxiv.org", "github.com", "developer.apple.com", "notion.so",
            "pytorch.org", "tensorflow.org", "huggingface.co",
            "docs.python.org", "developer.mozilla.org", "w3.org",
            "3blue1brown.com", "khanacademy.org", "mit.edu",
            "anthropic.com", "openai.com", "modelcontextprotocol.io",
            "bilibili.com",  # B站有曾老师内容
        ]
        suspicious_domains = [
            "bit.ly", "tinyurl", "t.co",  # 短链接
        ]

        url_lower = url.lower()
        if any(d in url_lower for d in trusted_domains):
            return {"level": "可信", "reason": "知名可信来源"}
        elif any(d in url_lower for d in suspicious_domains):
            return {"level": "可疑", "reason": "短链接/可疑来源"}
        else:
            return {"level": "未知", "reason": "来源待验证"}


# ============================================================
# 三、出口盾（Output Gate · 输出审查）
# ============================================================

class OutputGate:
    """
    出口盾：知识/内容输出前的最后防线

    检测项：
    1. 数字根熔断（出口同样执行）
    2. 隐私数据泄露检测
    3. DNA追溯码完整性
    4. 三色审计合规性
    5. 内容脱敏处理
    """

    def __init__(self):
        self.dr_fuse = DigitalRootFuse()

        # 必须脱敏的模式
        self.pii_patterns = [
            (r'\b\d{17}[\dXx]\b', "身份证号", self._mask_id),
            (r'\b1[3-9]\d{9}\b', "手机号", self._mask_phone),
            (r'[\w.-]+@[\w.-]+\.\w+', "邮箱", self._mask_email),
            (r'(?:password|密码|pwd)\s*[:=：]\s*\S+', "密码", self._mask_password),
            (r'(?:sk-|sk_)[a-zA-Z0-9]{20,}', "API密钥", self._mask_key),
            (r'ghp_[a-zA-Z0-9]{36}', "GitHub Token", self._mask_key),
            (r'(?:AKIA|ASIA)[A-Z0-9]{16}', "AWS密钥", self._mask_key),
        ]

    def scan(self, text, require_dna=True):
        """
        完整出口扫描
        返回: {
            "allowed": bool,
            "dr_result": dict,
            "pii_found": list,
            "sanitized_text": str,
            "dna_check": dict,
            "recommendation": str
        }
        """
        result = {
            "timestamp": datetime.now().isoformat(),
            "output_length": len(text),
        }

        # === 第一关：数字根熔断 ===
        dr_result = self.dr_fuse.check(text)
        result["dr_result"] = dr_result

        if dr_result["action"] == "fuse":
            result["allowed"] = False
            result["sanitized_text"] = ""
            result["recommendation"] = f"🔴 出口熔断 · {dr_result['detail']}"
            return result

        # === 第二关：PII 检测与脱敏 ===
        pii_found = []
        sanitized = text
        for pattern, pii_type, mask_func in self.pii_patterns:
            matches = re.finditer(pattern, sanitized, re.IGNORECASE)
            for match in matches:
                pii_found.append({
                    "type": pii_type,
                    "position": match.span(),
                    "preview": match.group()[:4] + "***"
                })
            sanitized = re.sub(pattern, lambda m: mask_func(m.group()), sanitized, flags=re.IGNORECASE)

        result["pii_found"] = pii_found
        result["sanitized_text"] = sanitized

        # === 第三关：DNA 追溯码检查 ===
        dna_check = self._check_dna(text)
        result["dna_check"] = dna_check

        if require_dna and not dna_check["has_dna"]:
            result["recommendation"] = "⚠️ 输出内容缺少DNA追溯码，建议补充后再发布"
            # 不阻止，但提醒

        # === 第四关：三色审计标记检查 ===
        audit_check = self._check_audit_tags(text)
        result["audit_check"] = audit_check

        # === 综合判断 ===
        if dr_result["action"] == "review":
            result["allowed"] = False
            result["recommendation"] = f"🟡 出口待审 · dr={dr_result['dr']}"
        elif pii_found:
            result["allowed"] = True  # 允许输出，但用脱敏版
            result["recommendation"] = f"⚠️ 检测到 {len(pii_found)} 处隐私数据，已自动脱敏。使用 sanitized_text 输出。"
        else:
            result["allowed"] = True
            result["recommendation"] = "🟢 出口通行 · 内容安全可输出"

        # 出口DNA
        content_hash = hashlib.sha256(text.encode()).hexdigest()[:8].upper()
        result["gate_dna"] = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-GATE-OUT-{content_hash}"

        return result

    def _check_dna(self, text):
        """检查文本中是否包含有效的DNA追溯码"""
        dna_pattern = r'#龍芯⚡️\d{8}-[A-Z]+-[A-F0-9]{8}'
        matches = re.findall(dna_pattern, text)
        return {
            "has_dna": len(matches) > 0,
            "dna_codes": matches,
            "count": len(matches)
        }

    def _check_audit_tags(self, text):
        """检查三色审计标记"""
        green = len(re.findall(r'🟢', text))
        yellow = len(re.findall(r'🟡', text))
        red = len(re.findall(r'🔴', text))
        return {
            "green": green,
            "yellow": yellow,
            "red": red,
            "has_audit": (green + yellow + red) > 0
        }

    # === 脱敏函数 ===
    @staticmethod
    def _mask_id(text):
        return text[:6] + "********" + text[-4:]

    @staticmethod
    def _mask_phone(text):
        return text[:3] + "****" + text[-4:]

    @staticmethod
    def _mask_email(text):
        parts = text.split("@")
        return parts[0][:2] + "***@" + parts[1]

    @staticmethod
    def _mask_password(text):
        return re.sub(r'([:=：]\s*)\S+', r'\1********', text)

    @staticmethod
    def _mask_key(text):
        return text[:6] + "****" + text[-4:]


# ============================================================
# 四、CLI 入口
# ============================================================

def format_gate_result(result, gate_type="入口"):
    """格式化盾检测结果"""
    lines = []
    lines.append(f"\n🛡️ 龍魂{gate_type}盾 · 检测报告")
    lines.append("─" * 55)

    # 数字根
    dr = result.get("dr_result", {})
    lines.append(f"  数字根闸门: {dr.get('color', '未知')} [dr={dr.get('dr', '?')} | {dr.get('action', '?')}]")

    if gate_type == "入口":
        # 内容类型
        if "content_type" in result:
            lines.append(f"  内容分类: 📂 {result['content_type']}")
        # 污染
        if "pollution_level" in result:
            level_emoji = {"high": "🗑️", "medium": "⚡", "low": "✨"}.get(result["pollution_level"], "❓")
            lines.append(f"  污染指数: {level_emoji} {result['pollution_level']}")
            if result.get("pollution_markers_found"):
                lines.append(f"  污染标记: {', '.join(result['pollution_markers_found'][:5])}")
        # 来源
        if "source_trust" in result:
            lines.append(f"  来源可信度: 🔗 {result['source_trust']}")
        # 敏感
        if result.get("sensitive_alerts"):
            lines.append(f"  ⚠️ 敏感信息: {', '.join(result['sensitive_alerts'])}")
    else:
        # PII
        if result.get("pii_found"):
            lines.append(f"  ⚠️ 隐私数据: {len(result['pii_found'])} 处已脱敏")
            for pii in result["pii_found"]:
                lines.append(f"     - {pii['type']}: {pii['preview']}")
        # DNA
        dna = result.get("dna_check", {})
        lines.append(f"  DNA追溯: {'✅ 有' if dna.get('has_dna') else '❌ 缺失'} ({dna.get('count', 0)} 个)")

    # 标签
    if "tags_summary" in result:
        lines.append(f"  标签: {result['tags_summary']}")

    lines.append("─" * 55)
    # 结论
    allowed = result.get("allowed", False)
    lines.append(f"  结论: {'✅ 放行' if allowed else '🚫 拦截'}")
    lines.append(f"  建议: {result.get('recommendation', '无')}")

    if "gate_dna" in result:
        lines.append(f"  盾DNA: {result['gate_dna']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="龍魂双盾引擎 · Inbox Gate + Output Gate + Digital Root Fuse",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 入口检测
  python shield_engine.py gate-in --text "一篇关于Transformer的论文" --url "https://arxiv.org/abs/1706.03762"

  # 出口检测
  python shield_engine.py gate-out --text "我的密码是abc123，手机号13812345678"

  # 数字根检测
  python shield_engine.py dr --text "订单号123456"

  # 完整管道
  python shield_engine.py pipeline --text "震惊！99%的人不知道的AI秘密！" --url "https://bit.ly/xxx"
        """
    )
    sub = parser.add_subparsers(dest="command")

    # gate-in
    p_in = sub.add_parser("gate-in", help="入口盾检测")
    p_in.add_argument("--text", required=True, help="要检测的内容")
    p_in.add_argument("--url", help="来源URL")

    # gate-out
    p_out = sub.add_parser("gate-out", help="出口盾检测")
    p_out.add_argument("--text", required=True, help="要检测的输出内容")
    p_out.add_argument("--no-dna-check", action="store_true", help="不检查DNA追溯码")

    # dr
    p_dr = sub.add_parser("dr", help="单独数字根检测")
    p_dr.add_argument("--text", required=True, help="要检测的文本")

    # pipeline
    p_pipe = sub.add_parser("pipeline", help="完整双盾管道")
    p_pipe.add_argument("--text", required=True, help="内容")
    p_pipe.add_argument("--url", help="来源URL")

    args = parser.parse_args()

    if args.command == "gate-in":
        gate = InboxGate()
        result = gate.scan(args.text, url=args.url)
        print(format_gate_result(result, "入口"))

    elif args.command == "gate-out":
        gate = OutputGate()
        result = gate.scan(args.text, require_dna=not args.no_dna_check)
        print(format_gate_result(result, "出口"))
        if result.get("pii_found"):
            print(f"\n📝 脱敏后内容:\n{result['sanitized_text']}")

    elif args.command == "dr":
        fuse = DigitalRootFuse()
        result = fuse.check(args.text)
        print(f"\n🔢 数字根检测")
        print(f"  输入: \"{args.text}\"")
        print(f"  结果: {result['color']} [dr={result['dr']} | {result['detail']}]")

    elif args.command == "pipeline":
        print("🛡️🛡️ 龍魂双盾管道 · 全流程检测")
        print("=" * 55)

        # 入口盾
        in_gate = InboxGate()
        in_result = in_gate.scan(args.text, url=args.url)
        print(format_gate_result(in_result, "入口"))

        if not in_result["allowed"]:
            print("\n🚫 入口盾拦截，内容不进入管道。")
            return

        print("\n  ↓ 入口通过，模拟净化后检测出口 ↓\n")

        # 出口盾
        out_gate = OutputGate()
        out_result = out_gate.scan(args.text, require_dna=False)
        print(format_gate_result(out_result, "出口"))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
