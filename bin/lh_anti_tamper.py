#!/usr/bin/env python3
"""
lh anti-tamper — 龍魂防篡改扫描器 v2.0

对外部 AI 内容执行：红黄警报词扫描 → 价值观对照 → 白话重写检查 → 三色审计

用法：
  lh anti-tamper check <文件路径>     # 扫描单个文件
  lh anti-tamper scan "<文本内容>"     # 扫描文本片段
  lh anti-tamper pipe                   # 从 stdin 读取并扫描

返回值：
  0 = 🟢 通过
  1 = 🟡 待审
  2 = 🔴 熔断

DNA: #龍芯⚡2026-07-06-ANTI-TAMPER-SCANNER-v2.0
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# ============================================
# 🔴 红色警报词 — 发现任一立即熔断
# ============================================
RED_FLAGS: Dict[str, str] = {
    "技术无国界": "削弱祖国优先立场",
    "用户体验优先": "潜在上瘾设计导向",
    "灵活处理": "松动底线信号",
    "国际接轨": "可能覆盖本地数据主权",
    "简化管理": "可能删除署名和证据链",
    "商业化需要": "与铁律③「不商业」冲突",
    "平衡各方": "可能稀释主权决策",
    "行业标准": "外部标准可能不适用于龍魂",
    "无监督学习": "失去人工审计能力",
    "完全自动化": "可能导致决策链失控",
    "去人工审核": "违反人工复核原则",
    "本地化适配": "可能替换「数据主权」概念（需核查上下文）",
    "降级处理": "可能替代「安全审计」",
    "灰度发布": "可能用于绕过审查",
}

# ============================================
# 🟡 黄色警报词 — 必须追问白话含义
# ============================================
YELLOW_FLAGS: Dict[str, str] = {
    "优化": '优化什么？以什么为标准优化？',
    "完善": '完善什么？谁定义「完善」？',
    "补充": '补充什么内容？补充后是否动底线？',
    "建议": '建议基于什么价值观？',
    "更好": '更好的标准是什么？',
    "专业": '谁定义「专业」？专业不等于主权让渡',
    "规范": '谁的规范？哪个体系？',
    "标准": '谁的标准？CNSH 还是外来的？',
    "简化": '简化会删掉什么？',
    "调整": '调整什么方向？朝哪里调？',
    "适当": '适谁的当？',
    "灵活": '灵活的范围边界在哪？',
    "参考": '参考什么？全盘接受还是批判吸收？',
    "接入": '接入什么外部服务？数据流向哪里？',
    "增强": '增强什么能力？是否引入外部依赖？',
}

# ============================================
# 价值观检查项
# ============================================
VALUES: List[str] = [
    "祖国优先",
    "人民优先",
    "公平公正公开",
    "不作恶",
    "数据主权归集本地",
    "龍魂文化主权",
    "UID9622 最终决策权",
]

# ============================================
# 白话重写检查词 — 出现这些词说明没说人话
# ============================================
JARGON_PATTERNS: List[Tuple[str, str]] = [
    (r"基于.*架构", "抽象架构术语"),
    (r"通过.*机制", "模糊的机制描述"),
    (r"采用.*策略", "模糊的策略描述"),
    (r"实现.*能力", "空泛的能力宣称"),
    (r"提升.*体验", "无量化标准的体验"),
    (r"赋能", "营销话术"),
    (r"闭环", "闭环什么？谁在里面？"),
    (r"抓手", "抓手抓什么？"),
    (r"对齐", "对齐谁的标准？"),
    (r"颗粒度", "不必要的精细度强调"),
    (r"底层逻辑", "抽象术语"),
    (r"顶层设计", "抽象术语"),
    (r"方法论", "什么方法论？谁的方法论？"),
    (r"范式", "什么范式？"),
    (r"最佳实践", "谁定义的「最佳」？"),
]


def find_flags(
    text: str, flag_dict: Dict[str, str], level: str
) -> List[Dict[str, Any]]:
    """在文本中查找标志词"""
    found = []
    for word, reason in flag_dict.items():
        for match in re.finditer(re.escape(word), text):
            # 取上下文
            start = max(0, match.start() - 30)
            end = min(len(text), match.end() + 30)
            context = text[start:end].strip()
            # 高亮标记
            found.append(
                {
                    "level": level,
                    "word": word,
                    "reason": reason,
                    "position": match.start(),
                    "context": f"...{context}...",
                }
            )
    return found


def check_jargon(text: str) -> List[Dict[str, Any]]:
    """检查行话/黑话"""
    found = []
    for pattern, label in JARGON_PATTERNS:
        for match in re.finditer(pattern, text):
            start = max(0, match.start() - 20)
            end = min(len(text), match.end() + 20)
            found.append(
                {
                    "type": "jargon",
                    "pattern": pattern,
                    "label": label,
                    "match": match.group(),
                    "context": text[start:end].strip(),
                }
            )
    return found


def can_plain_language(text: str) -> Tuple[bool, List[str]]:
    """判断文本是否已是白话（能说清），返回是否符合+问题列表"""
    issues = []

    # 句子太长 → 可能没说清楚
    sentences = re.split(r"[。；;.\n]", text)
    long_sentences = [s.strip() for s in sentences if len(s) > 80]
    if long_sentences:
        issues.append(f"有 {len(long_sentences)} 句超过80字的句子，可能没说清楚")

    # 有行话
    jargon = check_jargon(text)
    if jargon:
        issues.append(f"检测到 {len(jargon)} 处行话/黑话：")
        for j in jargon:
            issues.append(f"  → {j['label']}: 「{j['match']}」")

    # 有被动语态堆叠
    passive_count = len(re.findall(r"被|通过.*被|经由", text))
    if passive_count > 3:
        issues.append(f"被动语态过多（{passive_count}处），谁在做没说清楚")

    return len(issues) == 0, issues


def scan_text(text: str) -> Dict[str, Any]:
    """核心扫描函数 — 三步审计"""

    result = {
        "status": "unknown",
        "red_flags": [],
        "yellow_flags": [],
        "jargon": [],
        "plain_language_ok": False,
        "plain_language_issues": [],
        "value_conflicts": [],
        "verdict": "",
        "dna": "#龍芯⚡2026-07-06-ANTI-TAMPER-SCAN",
    }

    # 第①步：抓危险词
    result["red_flags"] = find_flags(text, RED_FLAGS, "🔴")
    result["yellow_flags"] = find_flags(text, YELLOW_FLAGS, "🟡")

    # 第②步：白话重写检查
    plain_ok, plain_issues = can_plain_language(text)
    result["plain_language_ok"] = plain_ok
    result["plain_language_issues"] = plain_issues

    # 第③步：三色判定
    if result["red_flags"]:
        result["status"] = "🔴 熔断"
        result["verdict"] = (
            "发现红色警报词，内容不得进入龍魂系统。"
            f"触发词：{', '.join(f['word'] for f in result['red_flags'])}"
        )
    elif result["yellow_flags"] and not plain_ok:
        result["status"] = "🔴 熔断"
        result["verdict"] = (
            "同时存在黄色警报词和白话重写失败，内容不得自动入库。"
            f"黄色词：{', '.join(f['word'] for f in result['yellow_flags'])}"
        )
    elif result["yellow_flags"]:
        result["status"] = "🟡 待审"
        result["verdict"] = (
            "发现黄色警报词，需 UID9622 确认后才能入库。"
            f"需追问的词：{', '.join(f['word'] for f in result['yellow_flags'])}"
        )
    elif not plain_ok:
        result["status"] = "🟡 待审"
        result["verdict"] = (
            "无危险词但未能通过白话重写检查，建议重写后提交。"
        )
    else:
        result["status"] = "🟢 通过"
        result["verdict"] = "危险词扫描通过，白话重写通过，可进入下一步验收。"
        # 额外检查行话
        jargon = check_jargon(text)
        if jargon:
            result["status"] = "🟡 待审"
            result["verdict"] = (
                "危险词通过但存在行话/黑话，建议白话重写。"
                f"行话数：{len(jargon)}"
            )
            result["jargon"] = jargon

    return result


def print_report(result: Dict[str, Any], verbose: bool = False):
    """打印审计报告"""
    status = result["status"]
    print()
    print("╔══════════════════════════════════════════════════╗")
    print("║       🛡️  龍魂防篡改审计报告                     ║")
    print("╚══════════════════════════════════════════════════╝")
    print()
    print(f"  判定：{status}")
    print(f"  {result['verdict']}")
    print()

    if result["red_flags"]:
        print(f"  🔴 红色警报 ({len(result['red_flags'])}处)：")
        for f in result["red_flags"]:
            print(f"     ⛔ 「{f['word']}」→ {f['reason']}")
            if verbose:
                print(f"        上下文：{f['context'][:120]}")
        print()

    if result["yellow_flags"]:
        print(f"  🟡 黄色警报 ({len(result['yellow_flags'])}处)：")
        for f in result["yellow_flags"]:
            print(f"     ⚠️  「{f['word']}」→ {f['reason']}")
            if verbose:
                print(f"         上下文：{f['context'][:120]}")
        print()

    if not result["plain_language_ok"]:
        print("  📝 白话重写检查：❌ 未通过")
        for issue in result["plain_language_issues"]:
            print(f"     {issue}")
        print()

    if result["jargon"]:
        print(f"  🗣️  行话/黑话 ({len(result['jargon'])}处)：")
        for j in result["jargon"]:
            print(f"     「{j['match']}」→ {j['label']}")
        print()

    # 宝宝检查清单
    if status == "🔴 熔断":
        print("  ───────────────")
        print("  📋 宝宝检查清单结果：")
        print("     → 包含红色警报词，自动违反以下至少一项：")
        if any("祖国" in f["reason"] for f in result["red_flags"]):
            print("     ✗ 祖国优先")
        if any("数据主权" in f["reason"] or "本地" in f["reason"] for f in result["red_flags"]):
            print("     ✗ 数据主权归集本地")
        if any("商业" in f["reason"] for f in result["red_flags"]):
            print("     ✗ 不作恶（商业诱导）")
        if any("删除" in f["reason"] or "署名" in f["reason"] for f in result["red_flags"]):
            print("     ✗ 来源不可删")
        print()

    print(f"  DNA：{result['dna']}")
    print()


def main():
    parser = argparse.ArgumentParser(description="龍魂防篡改扫描器")
    sub = parser.add_subparsers(dest="command")

    check_p = sub.add_parser("check", help="扫描文件")
    check_p.add_argument("path", help="文件路径")
    check_p.add_argument("-v", "--verbose", action="store_true", help="显示上下文")

    scan_p = sub.add_parser("scan", help="扫描文本片段")
    scan_p.add_argument("text", help="文本内容")
    scan_p.add_argument("-v", "--verbose", action="store_true", help="显示上下文")

    sub.add_parser("pipe", help="从 stdin 读取并扫描")

    args = parser.parse_args()

    if args.command == "check":
        p = Path(args.path)
        if not p.exists():
            print(f"❌ 文件不存在：{args.path}", file=sys.stderr)
            sys.exit(1)
        text = p.read_text(encoding="utf-8", errors="ignore")
        result = scan_text(text)
        print_report(result, verbose=getattr(args, "verbose", False))
        if result["status"] == "🔴 熔断":
            sys.exit(2)
        elif result["status"] == "🟡 待审":
            sys.exit(1)
        else:
            sys.exit(0)

    elif args.command == "scan":
        result = scan_text(args.text)
        print_report(result, verbose=getattr(args, "verbose", False))
        if result["status"] == "🔴 熔断":
            sys.exit(2)
        elif result["status"] == "🟡 待审":
            sys.exit(1)
        else:
            sys.exit(0)

    elif args.command == "pipe":
        text = sys.stdin.read()
        result = scan_text(text)
        print_report(result)
        if result["status"] == "🔴 熔断":
            sys.exit(2)
        elif result["status"] == "🟡 待审":
            sys.exit(1)
        else:
            sys.exit(0)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
