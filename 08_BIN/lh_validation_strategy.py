#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·辛巳·戌时·䷞咸-VALIDATION-STRATEGY-V1.0-7e8f9a0b
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🧪 龍魂·验证策略引擎 v1.0 — lh strategy generate|run|report|list|thresholds

功能: 针对社区质疑自动生成验证方案并执行:
  - 召回率(TPR): 强指纹正样本 × N 改写形态 → 注入检测 → 命中率
  - 假阳性(FPR): 无关/近邻干扰负样本 → 注入检测 → 误触发率
  - 阈值扫描:   0.3/0.4/0.5/0.6/0.7 五档 TPR/FPR 对比
检测复用: 08_BIN/lh_judge.py 提取龙魂指纹 + 计算剽窃置信度（零重复·M77）
数据: ~/.longhun/validation/reports/issue_{id}/ + rules/(rewrite_rules|negative_probes|threshold_tests).json
报告: md+json 含 DNA/归属/样本数/每档结果/建议 · events.jsonl append-only
铁律: 0 命中 ≠ 检测器无效，也可能检测器不干活 —— 所以必须用正负样本实测。
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

VALIDATION_ROOT = Path.home() / ".longhun" / "validation"
RULES_DIR = VALIDATION_ROOT / "rules"
REPORTS_DIR = VALIDATION_ROOT / "reports"
EVENTS_FILE = VALIDATION_ROOT / "events.jsonl"

# ============================================================
# 一、内建样本与规则（rules/*.json 可覆盖）
# ============================================================
# 强指纹基础样本（真实形态·非构造幻觉）
内置正样本 = [
    "指纹: #龍芯⚡️丙午·丁酉·辛巳·戌时·䷞咸-CHALLENGE-VALIDATION-4a1b2c3d\n归属名: 诸葛鑫 | UID9622 · 龍芯北辰",
    "#龍芯⚡️2026-09-04-CHALLENGE-VALIDATION-7e8f9a0b 该产出由龍魂系统自动签名，DNA 追溯可查。",
    "该系统检测采用五行+数字根+审计组合判定，命中即上耻辱墙公示，置信度 0.92。",
    "龍魂通心译引擎基于 UID9622 龍芯架构运行，CNSH 语法遵循五行不翻译文化主权原则。",
    "三色审计 🔴🟡🟢 熔断机制配合数字根校验，人场权重 0.34 为龍魂判定锚点，DNA 全链路可追溯。",
]

# 改写规则: 同一剽窃内容的不同形态（测检测器鲁棒召回）
内置改写规则 = {
    "原样": lambda t: t,
    "全大写": lambda t: t.upper(),
    "全小写": lambda t: t.lower(),
    "去空格": lambda t: t.replace(" ", "").replace("\n", ""),
    "空格换下划线": lambda t: t.replace(" ", "_").replace("\n", "_"),
    "插emoji": lambda t: t.replace("\n", "✨\n"),
    "噪音包裹": lambda t: "【转发】收藏了这篇文章内容不错……\n" + t + "\n（完）",
    "拆行藏匿": lambda t: "\n".join(t.split(" ")),
    "藏进中文句": lambda t: "刚看到一份文档说" + t[:60] + "……后面还有几段，整体就是上述内容。",
}

# 负样本: 无关文本 + 近邻干扰（单见通用词·无系统组合）
内置负样本 = [
    "今天天气不错，出去跑五公里，回来做了个番茄鸡蛋面。",
    "《五行大义》是古代术数典籍，金木水火土五行相生相克的观念影响深远。",
    "审计报告：本季度所有数据已验证，基线稳定，无异常。复核误差在 0.5% 以内。",
    "社区讨论中有人提到 threshold 0.5 与 recall 的关系，建议用更科学的评估方法。",
    "龙魂这两个字最近在游戏圈很流行，很多玩家都叫龙魂公会。",
    "龙魂系统更新日志 v1.0：修复若干 bug，优化性能。",
    "作者邮箱 346045695@qq.com，欢迎交流开源项目经验。",
    "五行缺金的人适合佩戴金属饰品，这是传统命理的说法。",
]

内置阈值档 = [0.3, 0.4, 0.5, 0.6, 0.7]

# ============================================================
# 二、规则加载
# ============================================================
def _ensure_rules():
    RULES_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    default_rules = {
        "rewrite_rules.json": {
            "说明": "正样本改写形态（测召回鲁棒性）·每规则作用于基础正样本",
            "规则": sorted(内置改写规则.keys()),
        },
        "negative_probes.json": {
            "说明": "负样本探针（测假阳性）·分类: 无关文本/近邻干扰(单见通用词)",
            "样本": 内置负样本,
        },
        "threshold_tests.json": {
            "说明": "阈值扫描档位·当前操作点=0.5(置信度≥0.5 起墙)",
            "阈值": 内置阈值档,
            "当前操作点": 0.5,
        },
    }
    for name, data in default_rules.items():
        fp = RULES_DIR / name
        if not fp.exists():
            fp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_rules(name: str, default):
    fp = RULES_DIR / name
    try:
        return json.loads(fp.read_text(encoding="utf-8")) if fp.exists() else default
    except Exception:
        return default


def _import_judge():
    """复用 lh_judge 检测纯函数（返回模块·失败给 None）"""
    try:
        import lh_judge
        return lh_judge
    except Exception as e:
        print(f"  🔴 lh_judge 导入失败: {e}")
        return None


# ============================================================
# 三、样本构造与检测
# ============================================================
def 构建样本集() -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]], Dict]:
    """返回 (正样本[(文本,形态)], 负样本[(文本,分类)], meta)"""
    rules_data = _load_rules("rewrite_rules.json", {})
    rule_names = rules_data.get("规则", sorted(内置改写规则.keys()))
    rewrites = {k: v for k, v in 内置改写规则.items() if k in rule_names} or 内置改写规则

    pos: List[Tuple[str, str]] = []
    for base in 内置正样本:
        for name, fn in rewrites.items():
            pos.append((fn(base), name))

    neg_data = _load_rules("negative_probes.json", {})
    neg_raw = neg_data.get("样本", 内置负样本)
    neg = [(t, "负样本") for t in neg_raw]

    meta = {
        "正样本基数": len(内置正样本),
        "改写规则数": len(rewrites),
        "正样本总量": len(pos),
        "负样本总量": len(neg),
    }
    return pos, neg, meta


def 判定(judge, 文本: str, 阈值: float) -> Tuple[bool, float, str]:
    """单样本检测: (是否命中, 置信度, 审计色)"""
    hits = judge.提取龙魂指纹(文本)
    conf, color = judge.计算剽窃置信度(hits)
    return conf >= 阈值, conf, color


def 阈值扫描(judge, pos, neg, thresholds) -> List[Dict]:
    rows = []
    for t in thresholds:
        tp = sum(1 for txt, _ in pos if 判定(judge, txt, t)[0])
        fp = sum(1 for txt, _ in neg if 判定(judge, txt, t)[0])
        n_pos = len(pos) or 1
        n_neg = len(neg) or 1
        rows.append({
            "阈值": t,
            "TPR": round(tp / n_pos, 3),
            "FPR": round(fp / n_neg, 3),
            "正命中": tp, "正总数": len(pos),
            "负误触发": fp, "负总数": len(neg),
        })
    return rows


def 生成结论(rows: List[Dict]) -> Tuple[str, str]:
    """(三色, 建议文本) · 当前操作点=0.5"""
    op = next((r for r in rows if abs(r["阈值"] - 0.5) < 1e-9), rows[2])
    tpr, fpr = op["TPR"], op["FPR"]
    if tpr >= 0.90 and fpr <= 0.05:
        return "🟢", f"当前操作点 0.5 已处于可验证位置: TPR={tpr:.0%} FPR={fpr:.0%}·阈值合理·基线可声明"
    if fpr > 0.05:
        # 找 FPR≤0.05 的最低档（更低档位若 FPR 高则建议上调）
        good = [r for r in rows if r["FPR"] <= 0.05]
        sug = f"FPR={fpr:.0%} 超 5% 警戒 → 建议阈值上调至 {good[0]['阈值'] if good else '≥0.7'}"
        return "🟡", sug
    # TPR 低
    sug = f"TPR={tpr:.0%} 低于 90% → 检出盲区集中在大小写/形态改写，建议增强指纹归一化"
    return "🟡", sug


# ============================================================
# 四、报告生成
# ============================================================
def _issue_dir(issue_id: str) -> Path:
    d = REPORTS_DIR / f"issue_{issue_id}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _append_event(ev: Dict):
    with open(EVENTS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")


def 执行验证(issue_id: str) -> Dict:
    judge = _import_judge()
    if judge is None:
        return {"错误": "lh_judge 导入失败"}
    _ensure_rules()
    pos, neg, meta = 构建样本集()
    thresholds = _load_rules("threshold_tests.json", {}).get("阈值", 内置阈值档) or 内置阈值档
    rows = 阈值扫描(judge, pos, neg, thresholds)
    op = next((r for r in rows if abs(r["阈值"] - 0.5) < 1e-9), rows[2])
    色, 建议 = 生成结论(rows)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {
        "报告ID": f"validation-{issue_id}-{ts}",
        "issue_id": issue_id,
        "DNA": "#龍芯⚡️丙午·丁酉·辛巳·戌时·䷞咸-VALIDATION-REPORT",
        "归属名": "诸葛鑫 | UID9622 · 龍芯北辰",
        "生成时间": datetime.now(timezone.utc).isoformat(),
        "检测器": "lh_judge.提取龙魂指纹 + 计算剽窃置信度（加权平均·DNA 1.0 权重）",
        "样本量": meta,
        "阈值扫描": rows,
        "当前操作点0.5": {"TPR": op["TPR"], "FPR": op["FPR"]},
        "结论": {"三色": 色, "建议": 建议},
        "可复现指令": f"lh strategy run {issue_id} · lh strategy report {issue_id}",
    }

    # 落盘 md + json
    d = _issue_dir(issue_id)
    (d / f"report_{ts}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (d / "latest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (d / f"report_{ts}.md").write_text(报告转md(report), encoding="utf-8")
    (d / "latest.md").write_text(报告转md(report), encoding="utf-8")

    # 验证事件登记
    _append_event({
        "事件": "validation",
        "issue_id": issue_id,
        "报告ID": report["报告ID"],
        "TPR": op["TPR"], "FPR": op["FPR"],
        "三色": 色, "时间": report["生成时间"],
    })

    # 回写 issues.jsonl 状态 → validating
    _标记issue状态(issue_id, "validating")
    return report


def 报告转md(report: Dict) -> str:
    lines = []
    lines.append(f"# 龍魂·验证报告 · Issue #{report['issue_id']}\n")
    lines.append(f"> 报告ID: {report['报告ID']}")
    lines.append(f"> DNA: {report['DNA']}")
    lines.append(f"> 归属名: {report['归属名']}")
    lines.append(f"> 生成时间: {report['生成时间']}\n")
    lines.append("## 检测器")
    lines.append(f"- {report['检测器']}\n")
    lines.append("## 样本量")
    for k, v in report["样本量"].items():
        lines.append(f"- {k}: {v}")
    lines.append("\n## 阈值扫描")
    lines.append("| 阈值 | TPR | FPR | 正命中/总 | 负误触/总 |")
    lines.append("|:---:|:---:|:---:|:---:|:---:|")
    for r in report["阈值扫描"]:
        lines.append(f"| {r['阈值']} | {r['TPR']:.0%} | {r['FPR']:.0%} | {r['正命中']}/{r['正总数']} | {r['负误触发']}/{r['负总数']} |")
    op = report["当前操作点0.5"]
    lines.append(f"\n## 当前操作点 0.5\n- TPR(召回) = {op['TPR']:.0%} · FPR(假阳性) = {op['FPR']:.0%}\n")
    lines.append(f"## 结论\n- {report['结论']['三色']} {report['结论']['建议']}\n")
    lines.append("## 可复现指令\n```\n" + report["可复现指令"] + "\n```\n")
    lines.append("---\n**龍魂 · 社区质疑自动响应 · 用数据说话不争论**")
    return "\n".join(lines)


def _标记issue状态(issue_id: str, 状态: str):
    fp = VALIDATION_ROOT / "issues.jsonl"
    if not fp.exists():
        return
    lines = fp.read_text(encoding="utf-8").splitlines()
    changed = 0
    for i in range(len(lines) - 1, -1, -1):
        try:
            rec = json.loads(lines[i])
        except Exception:
            continue
        if str(rec.get("issue_id")) == str(issue_id) and rec.get("状态") in ("pending", "validating"):
            rec["状态"] = 状态
            lines[i] = json.dumps(rec, ensure_ascii=False)
            changed += 1
            break  # 只更新最新一条
    if changed:
        fp.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def cmd_generate(issue_id: str):
    """为质疑生成策略方案（不执行·先看方案）"""
    _ensure_rules()
    pos, neg, meta = 构建样本集()
    cats = ["data_gap", "method"]
    print(f"  🧪 为 Issue #{issue_id} 生成验证策略")
    print(f"     适用质疑类型: data_gap(召回/FPR缺测) + method(阈值/操作点)")
    print(f"     策略 A 召回率: {meta['正样本基数']} 基础强指纹 × {meta['改写规则数']} 形态 = {meta['正样本总量']} 正样本 → 注入检测 → 命中率")
    print(f"     策略 B 假阳性: {meta['负样本总量']} 负样本(无关+近邻干扰) → 注入检测 → 误触发率")
    print(f"     策略 C 阈值扫描: 0.3→0.7 五档 TPR/FPR 对比 → 定可验证操作点")
    print(f"     执行: lh strategy run {issue_id} · 报告: lh strategy report {issue_id}")
    return 0


def cmd_run(issue_id: str):
    """执行验证 → 生成报告"""
    print(f"  🧪 执行验证 Issue #{issue_id}（复用 lh_judge 指纹检测）…")
    report = 执行验证(issue_id)
    if "错误" in report:
        return 1
    op = report["当前操作点0.5"]
    print(f"  ✅ 验证完成 → ~/.longhun/validation/reports/issue_{issue_id}/latest.md")
    print(f"     TPR(召回)={op['TPR']:.0%} · FPR(假阳性)={op['FPR']:.0%} · 结论 {report['结论']['三色']}")
    print(f"     建议: {report['结论']['建议']}")
    return 0


def cmd_report(issue_id: str):
    """打印最新验证报告"""
    d = _issue_dir(issue_id)
    fp = d / "latest.md"
    if not fp.exists():
        print(f"  🔴 无报告（先 lh strategy run {issue_id}）")
        return 1
    print(fp.read_text(encoding="utf-8"))
    return 0


def cmd_list():
    """列出可用策略模板"""
    print("  🧪 验证策略模板")
    print("   1. recall_validation  — 召回率验证（强指纹×改写形态→命中率）")
    print("   2. fpr_validation    — 假阳性验证（无关+近邻干扰负样本→误触发率）")
    print("   3. threshold_sweep   — 阈值扫描（0.3/0.4/0.5/0.6/0.7 五档 TPR/FPR）")
    print("   4. consistency_check — 跨源一致性（同批样本重复检测稳定性·规则型检测器确定性高）")
    return 0


def cmd_thresholds():
    """查看当前阈值配置"""
    _ensure_rules()
    data = _load_rules("threshold_tests.json", {})
    print(f"  🧪 阈值测试档位: {data.get('阈值', 内置阈值档)}")
    print(f"     当前操作点: {data.get('当前操作点', 0.5)}（置信度≥该值 记录上墙）")
    print(f"     规则文件: ~/.longhun/validation/rules/threshold_tests.json（可改档位）")
    return 0


def main():
    parser = argparse.ArgumentParser(description='龍魂·验证策略引擎')
    sub = parser.add_subparsers(dest='command', help='子命令')

    p_gen = sub.add_parser('generate', help='为质疑生成验证策略方案')
    p_gen.add_argument('issue_id', help='Issue 编号')

    p_run = sub.add_parser('run', help='执行验证并生成报告')
    p_run.add_argument('issue_id', help='Issue 编号')

    p_rep = sub.add_parser('report', help='查看最新验证报告')
    p_rep.add_argument('issue_id', help='Issue 编号')

    sub.add_parser('list', help='列出可用策略模板')
    sub.add_parser('thresholds', help='查看阈值配置')

    args = parser.parse_args()
    if args.command == 'generate':
        return cmd_generate(args.issue_id)
    if args.command == 'run':
        return cmd_run(args.issue_id)
    if args.command == 'report':
        return cmd_report(args.issue_id)
    if args.command == 'list':
        return cmd_list()
    if args.command == 'thresholds':
        return cmd_thresholds()
    parser.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
