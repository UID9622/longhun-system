#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·辛巳·戌时·䷞咸-REVIEW-ENGINE-V1.0-8e5f6a7b
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🧑⚖️ 龍魂·数字人协同审核引擎 v1.0 — lh review evaluate|status|summary|dashboard

设计: 社区质疑自动审核回复系统 v1.0（老大 2026-09-04 方案稿）。
核心理念: 社区有人质疑 → 5 数字人并行审核 → 最优解方案 → 三色门控
          🟢 全过 → 自动回复 | 🟡 1-2 不过 → 待人工复核 | 🔴 ≥3 不过 → 记录耻辱墙等待人工。

5 数字人（digital_humans/registry.json 已注册·映射真实 IPA）:
  ASI-005 包青天·铁面审计师 — 质疑证据链是否被完整回应（TPR/FPR/样本量裁决）
  DH-012 明鉴·审计验收官   — 代码/报告合规（可复现指令·append-only 证据链·报告完整性）
  DH-011 匠心·代码工匠官   — 修复方案设计（阈值操作点可用性·修复建议）
  DH-013 诗仙·灵感创意官   — 回复草案与文档（草稿可用性·回复要点）
  DH-016 知行·部署上线官   — 性能与可维护性（验证运行成本·数据规模）

诚实声明: 本引擎为规则化启发式审核（纯本地·零三方·零网络·基于验证硬数据），
         非 LLM 语义理解。判定可复现、可复核。不伪装智能——每项判定都有数据依据。

数据: ~/.longhun/review/reviews/{issue_id}.json（append 历史版本）· dashboard.md
联动: 输入=~/.longhun/validation/reports/issue_{id}/latest.json + issues.jsonl 质疑记录
      respond 门控: lh challenge respond → 自动过本引擎 🟢 才发布（任务2/3/4）
      🔴 事件落 validation/events.jsonl（append-only·耻辱墙联动记录）
"""

import os
import sys
import json
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

VALIDATION_ROOT = Path.home() / ".longhun" / "validation"
REPORTS_DIR = VALIDATION_ROOT / "reports"
ISSUES_FILE = VALIDATION_ROOT / "issues.jsonl"
EVENTS_FILE = VALIDATION_ROOT / "events.jsonl"
REVIEW_ROOT = Path.home() / ".longhun" / "review"
REVIEWS_DIR = REVIEW_ROOT / "reviews"

# 5 数字人注册映射（digital_humans/registry.json 实测 IPA）
DIGITAL_REVIEWERS = [
    {"ipa": "ASI-005", "数字人": "包青天·铁面审计师", "职责": "审计与裁决·证据链"},
    {"ipa": "DH-012", "数字人": "明鉴·审计验收官",   "职责": "代码审核·合规证据"},
    {"ipa": "DH-011", "数字人": "匠心·代码工匠官",   "职责": "修复方案设计"},
    {"ipa": "DH-013", "数字人": "诗仙·灵感创意官",   "职责": "回复草案与文档"},
    {"ipa": "DH-016", "数字人": "知行·部署上线官",   "职责": "性能与可维护性"},
]
# 置信度权重（合计1.0·审计裁决最高）
WEIGHTS = {"ASI-005": 0.30, "DH-012": 0.20, "DH-011": 0.20, "DH-013": 0.15, "DH-016": 0.15}

# 通过门槛（写死·出处=设计稿 v1.0 三色触发条件 + 工程经验值）
TPR_OK, FPR_OK, MIN_SAMPLES = 0.80, 0.20, 40      # 包青天证据门槛
MIN_SCAN_BANDS = 3                                  # 匠心: 阈值扫描≥3档才有操作点可选


def _ensure_dirs():
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 一、数据源
# ============================================================
def _load_report(issue_id: str) -> Optional[Dict]:
    fp = REPORTS_DIR / f"issue_{issue_id}" / "latest.json"
    if not fp.exists():
        return None
    try:
        return json.loads(fp.read_text(encoding="utf-8"))
    except Exception:
        return None


def _load_rec(issue_id: str) -> Optional[Dict]:
    if not ISSUES_FILE.exists():
        return None
    for line in reversed(ISSUES_FILE.read_text(encoding="utf-8").splitlines()):
        try:
            rec = json.loads(line)
        except Exception:
            continue
        if str(rec.get("issue_id")) == str(issue_id):
            return rec
    return None


def _issue_events(issue_id: str) -> List[Dict]:
    if not EVENTS_FILE.exists():
        return []
    evs = []
    for line in EVENTS_FILE.read_text(encoding="utf-8").splitlines():
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if str(ev.get("issue_id")) == str(issue_id):
            evs.append(ev)
    return evs


def _fmt(v) -> str:
    return f"{v:.0%}" if isinstance(v, (int, float)) else str(v)


# ============================================================
# 二、5 数字人审核函数（规则化·每项判定带数据依据）
# ============================================================
def _审_包青天(report: Dict, rec: Optional[Dict]) -> Dict:
    """审计与裁决: 质疑是否成立、证据链是否完整。依据 = TPR/FPR/样本量。"""
    op = report.get("当前操作点0.5", {})
    tpr, fpr = op.get("TPR", 0), op.get("FPR", 1)
    ss = report.get("样本量", {})
    n_pos, n_neg = ss.get("正样本总量", 0), ss.get("负样本总量", 0)
    n_total = n_pos + n_neg
    problems = []
    if tpr < TPR_OK:
        problems.append(f"TPR={_fmt(tpr)} 低于召回门槛 {_fmt(TPR_OK)}")
    if fpr > FPR_OK:
        problems.append(f"FPR={_fmt(fpr)} 高于假阳性门槛 {_fmt(FPR_OK)}")
    if n_total < MIN_SAMPLES:
        problems.append(f"样本总量 {n_total} 不足门槛 {MIN_SAMPLES}")
    passed = not problems
    分 = round(((tpr + (1 - fpr)) / 2) * 100)
    意见 = ("证据链完整: 召回与误报双维实测均达标。" if passed
            else "证据链不足: " + "；".join(problems) + "。")
    return {"数字人": "包青天·铁面审计师", "ipa": "ASI-005", "判定": "通过" if passed else "不通过",
            "分数": 分, "意见": 意见, "建议": ("继续自动回复" if passed else "补足正负样本后重新验证")}


def _审_明鉴(report: Dict, rec: Optional[Dict]) -> Dict:
    """代码审核: 可复现性 + append-only 证据链 + 报告完整性。依据 = 文件与事件存在性。"""
    issue_id = str(report.get("issue_id", ""))
    md_fp = REPORTS_DIR / f"issue_{issue_id}" / "latest.md"
    md_ok = md_fp.exists() and md_fp.read_text(encoding="utf-8", errors="ignore").count("lh strategy run") > 0
    ev_ok = len(_issue_events(issue_id)) >= 1
    结论 = report.get("结论", {})
    concl_ok = bool(结论.get("建议")) and 结论.get("三色") in ("🟢", "🟡", "🔴")
    checks = [("可复现指令", md_ok), ("验证事件证据链(append-only)", ev_ok), ("结论完整性", concl_ok)]
    failed = [name for name, ok in checks if not ok]
    passed = not failed
    return {"数字人": "明鉴·审计验收官", "ipa": "DH-012", "判定": "通过" if passed else "不通过",
            "分数": round(sum(1 for _, ok in checks if ok) / len(checks) * 100),
            "意见": ("工程合规: " + "、".join(n for n, _ in checks) + " 全部就绪。" if passed
                     else "合规缺口: " + "、".join(failed) + " 缺失。"),
            "建议": ("无代码变更·合规放行" if passed else "补齐缺失项后重跑 lh strategy run")}


def _审_匠心(report: Dict, rec: Optional[Dict]) -> Dict:
    """修复方案设计: 结论非🟢时需有可切换的操作点（阈值扫描）。依据 = 扫描档数。"""
    结论 = report.get("结论", {})
    色 = 结论.get("三色", "🟡")
    bands = report.get("阈值扫描", [])
    if 色 == "🟢":
        passed = True
        意见 = "结论绿: 无需修复·当前操作点 0.5 即最优解。"
        建议 = "保持现状·不引入多余改动（最小变更原则）。"
    elif len(bands) >= MIN_SCAN_BANDS:
        passed = True
        best = max(bands, key=lambda b: (b.get("TPR", 0), -b.get("FPR", 1)))
        意见 = f"提供修复操作点: 阈值扫描 {len(bands)} 档可切换·推荐档位 {best.get('阈值')}。"
        建议 = f"修复方案=按阈值 {best.get('阈值')} 调整操作点后重新验证。"
    else:
        passed = False
        意见 = f"结论 {色} 但阈值扫描不足 {MIN_SCAN_BANDS} 档·无可验证的修复操作点。"
        建议 = "补充阈值扫描（至少 3 档）以定位可切换操作点。"
    return {"数字人": "匠心·代码工匠官", "ipa": "DH-011", "判定": "通过" if passed else "不通过",
            "分数": 100 if 色 == "🟢" else (85 if passed else 40), "意见": 意见, "建议": 建议}


def _审_诗仙(report: Dict, rec: Optional[Dict]) -> Dict:
    """回复草案: 数据字段齐备可生成回复 + 草稿落盘可用。依据 = 报告字段完整性。"""
    issue_id = str(report.get("issue_id", ""))
    op = report.get("当前操作点0.5", {})
    need = all(k in op for k in ("TPR", "FPR")) and bool(report.get("结论", {}).get("建议"))
    drafts = list((REPORTS_DIR / f"issue_{issue_id}").glob("response_*.md"))
    passed = need
    意见 = (f"回复材料齐备（TPR={_fmt(op.get('TPR'))} FPR={_fmt(op.get('FPR'))}）·"
            f"草稿缓存 {len(drafts)} 份。" if passed else "回复字段缺失·无法生成完整回复。")
    return {"数字人": "诗仙·灵感创意官", "ipa": "DH-013", "判定": "通过" if passed else "不通过",
            "分数": 100 if passed else 35, "意见": 意见,
            "建议": "回复要点=致谢质疑→验证摘要表→结论→可复现指令（lh response build 出稿）"}


def _审_知行(report: Dict, rec: Optional[Dict]) -> Dict:
    """性能与可维护性: 验证运行成本可控、数据规模合理。依据 = 验证事件数与样本规模。"""
    issue_id = str(report.get("issue_id", ""))
    n_ev = len(_issue_events(issue_id))
    ss = report.get("样本量", {})
    n_total = ss.get("正样本总量", 0) + ss.get("负样本总量", 0)
    # 每次验证落 1 条事件（append-only 成本低）；>8 次重跑提示维护负担
    run_cost_ok = n_ev <= 8
    意见 = f"运行成本: 验证事件 {n_ev} 条（{'正常' if run_cost_ok else '偏多·建议合并重跑'}）· 样本规模 {n_total} 条。"
    return {"数字人": "知行·部署上线官", "ipa": "DH-016", "判定": "通过" if run_cost_ok else "不通过",
            "分数": 100 if run_cost_ok else 60, "意见": 意见,
            "建议": "当前无可维护性风险" if run_cost_ok else "重跑前先复核样本是否增量更新（避免重复全量）"}


def _reviewers():
    return {
        "ASI-005": _审_包青天, "DH-012": _审_明鉴, "DH-011": _审_匠心,
        "DH-013": _审_诗仙, "DH-016": _审_知行,
    }


def _run_parallel(report: Dict, rec: Optional[Dict]) -> List[Dict]:
    """并行触发 5 数字人审核（设计稿 v1.0: 并行触发→汇总）"""
    funcs = _reviewers()
    with ThreadPoolExecutor(max_workers=len(funcs)) as ex:
        futs = {ex.submit(fn, report, rec): fn for fn in funcs.values()}
        results = [f.result() for f in futs]
    return results


# ============================================================
# 三、汇总 + 三色门控 + 最优解方案
# ============================================================
def _aggregate(results: List[Dict]) -> Dict:
    n_fail = sum(1 for r in results if r["判定"] != "通过")
    if n_fail >= 3:
        色 = "🔴"
    elif n_fail >= 1:
        色 = "🟡"
    else:
        色 = "🟢"
    置信度 = round(sum(r["分数"] * WEIGHTS[r["ipa"]] for r in results), 1)
    return {"n_fail": n_fail, "n_total": len(results), "三色": 色, "置信度": 置信度}


def _best_solution(issue_id: str, results: List[Dict], agg: Dict) -> Dict:
    """最优解方案 = 审计结论 + 修复补丁建议 + 回复草案 + 性能 + 安全 + 置信度"""
    by_ipa = {r["ipa"]: r for r in results}
    gate = {"🟢": "自动回复（respond 门控放行）",
            "🟡": "待人工复核（不自动发布·标记 needs_human + 通知）",
            "🔴": "记录耻辱墙事件（append-only）·等待人工介入"}[agg["三色"]]
    return {
        "报告ID": issue_id,
        "三色": agg["三色"],
        "置信度": agg["置信度"],
        "门控动作": gate,
        "审计结论(包青天)": by_ipa["ASI-005"]["意见"] + " " + by_ipa["ASI-005"]["建议"],
        "修复方案(匠心)": by_ipa["DH-011"]["意见"] + " " + by_ipa["DH-011"]["建议"],
        "回复草案(诗仙)": by_ipa["DH-013"]["意见"] + " " + by_ipa["DH-013"]["建议"],
        "性能评估(知行)": by_ipa["DH-016"]["意见"],
        "合规审核(明鉴)": by_ipa["DH-012"]["意见"],
    }


def _save_review(issue_id: str, results: List[Dict], agg: Dict, solution: Dict) -> Path:
    _ensure_dirs()
    fp = REVIEWS_DIR / f"{issue_id}.json"
    hist = []
    if fp.exists():
        try:
            hist = json.loads(fp.read_text(encoding="utf-8"))
        except Exception:
            hist = []
    hist.append({
        "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "三色": agg["三色"],
        "置信度": agg["置信度"],
        "数字人结果": results,
        "最优解方案": solution,
    })
    fp.write_text(json.dumps(hist, ensure_ascii=False, indent=1), encoding="utf-8")
    return fp


# ============================================================
# 四、子命令
# ============================================================
def cmd_evaluate(issue_id: str) -> int:
    """触发 5 数字人并行审核（任务1 调度器核心）"""
    report = _load_report(issue_id)
    if not report:
        print(f"  🔴 无验证报告（先 lh strategy run {issue_id} 或 lh challenge respond {issue_id}）")
        return 1
    rec = _load_rec(issue_id)
    print(f"  🧑⚖️ 触发 5 数字人并行审核 Issue #{issue_id}…")
    results = _run_parallel(report, rec)
    for r in results:
        mark = {"通过": "✅", "不通过": "❌"}.get(r["判定"], "⏭️")
        print(f"    {mark} {r['数字人']} ({r['ipa']}) · {r['分数']}分 · {r['意见'][:60]}")
    agg = _aggregate(results)
    print(f"\n  📊 汇总: 通过 {agg['n_total'] - agg['n_fail']}/{agg['n_total']} · "
          f"三色 {agg['三色']} · 置信度 {agg['置信度']}")
    solution = _best_solution(issue_id, results, agg)
    fp = _save_review(issue_id, results, agg, solution)
    print(f"  最优解方案门控: {solution['门控动作']}")
    print(f"  已存档: {fp}")
    # 🔴 落耻辱墙联动事件（append-only·不删除只冻结）
    if agg["三色"] == "🔴":
        with open(EVENTS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps({"事件": "review_red", "issue_id": issue_id, "三色": "🔴",
                                "置信度": agg["置信度"], "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                               ensure_ascii=False) + "\n")
        print(f"  🔴 已记录耻辱墙联动事件（{EVENTS_FILE}）· 等待人工介入")
    return 0


def cmd_status(issue_id: str) -> int:
    """查看审核进度（各数字人状态）"""
    fp = REVIEWS_DIR / f"{issue_id}.json"
    if not fp.exists():
        print(f"  🔴 该 issue 尚无数字人审核记录（先 lh review evaluate {issue_id}）")
        return 1
    hist = json.loads(fp.read_text(encoding="utf-8"))
    latest = hist[-1]
    print(f"  🧑⚖️ Issue {issue_id} · 数字人审核 v{len(hist)} · {latest['时间']} · {latest['三色']} 置信度 {latest['置信度']}")
    for r in latest["数字人结果"]:
        mark = {"通过": "✅", "不通过": "❌"}.get(r["判定"], "⏭️")
        print(f"    {mark} {r['数字人']} ({r['ipa']}) · 判定: {r['判定']} · 分数 {r['分数']}")
    return 0


def cmd_summary(issue_id: str) -> int:
    """查看审核结果汇总（最优解方案）"""
    fp = REVIEWS_DIR / f"{issue_id}.json"
    if not fp.exists():
        print(f"  🔴 无审核记录（先 lh review evaluate {issue_id}）")
        return 1
    hist = json.loads(fp.read_text(encoding="utf-8"))
    sol = hist[-1]["最优解方案"]
    print(f"  📋 Issue #{sol['报告ID']} 最优解方案 · {sol['三色']} 置信度 {sol['置信度']}")
    for k, v in sol.items():
        if k in ("报告ID", "三色", "置信度", "门控动作"):
            continue
        print(f"    · {k}: {v}")
    print(f"    门控: {sol['门控动作']}")
    return 0


def cmd_dashboard() -> int:
    """审核状态总览 → dashboard.md（任务5）"""
    _ensure_dirs()
    issues = []
    if ISSUES_FILE.exists():
        seen = set()
        for line in ISSUES_FILE.read_text(encoding="utf-8").splitlines():
            try:
                rec = json.loads(line)
            except Exception:
                continue
            iid = str(rec.get("issue_id"))
            if iid and iid not in seen:
                seen.add(iid)
                issues.append(rec)
    lines = [f"# 🧑⚖️ 龍魂·社区质疑审核看板 · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
             "", "| Issue | 质疑者 | 分类 | 状态 | 审核三色 | 置信度 |", "|:---|:---|:---|:---|:---|:---:|"]
    n_reviewed = n_auto = n_wait = 0
    for rec in issues:
        iid = str(rec.get("issue_id"))
        fp = REVIEWS_DIR / f"{iid}.json"
        mark = "—"
        conf = "—"
        if fp.exists():
            hist = json.loads(fp.read_text(encoding="utf-8"))
            last = hist[-1]
            mark = last["三色"]
            conf = last["置信度"]
            n_reviewed += 1
            if last["三色"] == "🟢":
                n_auto += 1
            else:
                n_wait += 1
        st = {"pending": "⏳待验证", "validating": "🧪验证中", "responded": "✅已回复",
              "needs_human": "📋待人工复核"}.get(rec.get("状态"), str(rec.get("状态", "?")))
        lines.append(f"| #{iid} | {rec.get('质疑者', '-')} | {'/'.join(rec.get('分类', []))} | {st} | {mark} | {conf} |")
    lines += ["", f"汇总: {len(issues)} 质疑 · {n_reviewed} 已审 · 🟢自动 {n_auto} · 🟡/🔴待人工 {n_wait}",
              "", "> 数据: ~/.longhun/review/reviews/ · 输入: ~/.longhun/validation/（append-only）"]
    fp = REVIEW_ROOT / "dashboard.md"
    fp.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    print(f"\n  📊 看板已存: {fp}")
    return 0


def main():
    parser = argparse.ArgumentParser(description='🧑⚖️ 龍魂·数字人协同审核引擎')
    sub = parser.add_subparsers(dest='command', help='子命令')
    pe = sub.add_parser('evaluate', help='触发 5 数字人并行审核同一质疑')
    pe.add_argument('issue_id', help='Issue 编号')
    ps = sub.add_parser('status', help='查看审核进度（各数字人状态）')
    ps.add_argument('issue_id', help='Issue 编号')
    pm = sub.add_parser('summary', help='查看审核结果汇总（最优解方案）')
    pm.add_argument('issue_id', help='Issue 编号')
    sub.add_parser('dashboard', help='审核状态总览 → ~/.longhun/review/dashboard.md')
    args = parser.parse_args()
    if args.command == 'evaluate':
        return cmd_evaluate(args.issue_id)
    if args.command == 'status':
        return cmd_status(args.issue_id)
    if args.command == 'summary':
        return cmd_summary(args.issue_id)
    if args.command == 'dashboard':
        return cmd_dashboard()
    parser.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
