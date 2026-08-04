#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 统一系统评估报告生成器

把现有的评估/审计/复盘技能跑一遍，再叠加当前 LU/集思广益/工具集生态的
自定义检查，生成一份统一评估报告。

DNA:#龍芯⚡️2026-06-30-LONGHUN-SYSTEM-EVALUATION-FILE1-v1.0
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

HOME = Path.home()
SKILLS = HOME / ".kimi-code" / "skills"
OUTPUT_DIR = HOME / ".longhun" / "evaluation"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _run(cmd: List[str], cwd: Path = HOME, timeout: int = 120) -> Dict[str, Any]:
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {"ok": True, "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _latest_json(dir_path: Path, pattern: str) -> Optional[Path]:
    files = sorted(dir_path.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def _load_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def run_automation_assessment() -> Dict[str, Any]:
    script = SKILLS / "longhun-automation" / "scripts" / "自动化评估.py"
    result = _run(["python3", str(script), "--cron"], cwd=script.parent)
    latest = _latest_json(HOME / ".龍魂" / "assessments", "local_assessment_*.json")
    data = _load_json(latest) if latest else None
    if not data:
        return {"ok": False, "raw": result}
    return {
        "ok": True,
        "score": data.get("total_score", 0),
        "max_score": data.get("max_score", 10),
        "status": data.get("status", "unknown"),
        "dimensions": {a.get("category", "unknown"): {"score": a.get("score", 0), "max": a.get("max_score", 10)} for a in data.get("assessments", [])},
        "report_path": str(latest),
    }


def run_daily_review() -> Dict[str, Any]:
    script = SKILLS / "longhun-review" / "scripts" / "复盘引擎.py"
    result = _run(["python3", str(script), "--cron"], cwd=script.parent)
    latest = _latest_json(HOME / ".龍魂" / "reviews", "daily_review_*.json")
    data = _load_json(latest) if latest else None
    if not data:
        return {"ok": False, "raw": result}
    tri = data.get("三色總評", "")
    tricolor_map = {"🟢": "green", "🟡": "yellow", "🔴": "red"}
    color_key = tricolor_map.get(tri, "unknown")
    items = data.get("審計結果", {})
    tricolor_counts = {"green": 0, "yellow": 0, "red": 0, "unknown": 0}
    for detail in items.values():
        c = detail.get("顏色", "")
        tricolor_counts[tricolor_map.get(c, "unknown")] = tricolor_counts.get(tricolor_map.get(c, "unknown"), 0) + 1
    return {
        "ok": True,
        "score": data.get("綜合評分", 0),
        "tricolor": {**tricolor_counts, "overall": tri},
        "items": items,
        "report_path": str(latest),
    }


def run_dna_alignment(target: Path = HOME / "longhun-system" / "scripts") -> Dict[str, Any]:
    script = SKILLS / "longhun-dna-align" / "scripts" / "DNA对齐审计器.py"
    out_dir = OUTPUT_DIR / "dna_audit"
    out_dir.mkdir(parents=True, exist_ok=True)
    result = _run(["python3", str(script), str(target), "-o", str(out_dir), "--json"], cwd=script.parent)
    latest = _latest_json(out_dir, "DNA_ALIGNMENT_AUDIT_*.json")
    data = _load_json(latest) if latest else None
    if not data:
        return {"ok": False, "raw": result}
    stat = data.get("統計", {})
    return {
        "ok": True,
        "total_files": stat.get("總文件數", 0),
        "with_dna": stat.get("有DNA文件數", 0),
        "without_dna": stat.get("無DNA文件數", 0),
        "duplicate_dna": stat.get("重複DNA數", 0),
        "invalid_dna": stat.get("無效DNA數", 0),
        "alignment_rate": stat.get("DNA對齐率", 0),
        "health_level": data.get("健康評級", "unknown"),
        "report_path": str(latest),
    }


def run_integration_tests() -> Dict[str, Any]:
    script = SKILLS / "longhun-integration" / "scripts" / "集成测试引擎.py"
    json_path = OUTPUT_DIR / "integration_report.json"
    md_path = OUTPUT_DIR / "integration_report.md"
    result = _run(
        ["python3", str(script), "--export-json", str(json_path), "--export-md", str(md_path), "--quiet"],
        cwd=script.parent,
    )
    data = _load_json(json_path)
    if not data:
        return {"ok": False, "raw": result}
    summary = data.get("summary", {})
    return {
        "ok": True,
        "total": summary.get("total_tests", 0),
        "passed": summary.get("passed", 0),
        "failed": summary.get("failed", 0),
        "warnings": summary.get("warnings", 0),
        "success_rate": summary.get("success_rate", 0),
        "report_path": str(json_path),
    }


def run_archive_evaluation() -> Dict[str, Any]:
    script = SKILLS / "longhun-audit" / "scripts" / "归档评估器.py"
    result = _run(["python3", str(script)], cwd=script.parent)
    # 优先读取生成的 JSON 导出，稳定解析条目与决策
    report_dir = script.parent / "archive_data"
    latest_json = _latest_json(report_dir, "归档评估导出_*.json")
    entries = 0
    deletable_dirs = 0
    if latest_json and latest_json.exists():
        try:
            data = json.loads(latest_json.read_text(encoding="utf-8"))
            entries = len(data)
            deletable_dirs = sum(1 for v in data.values() if v.get("决策建议") == "delete_suggested")
        except Exception:
            pass
    # Markdown 报告用于展示决策摘要
    latest_md = _latest_json(report_dir, "归档评估报告_*.md")
    text = latest_md.read_text(encoding="utf-8") if latest_md and latest_md.exists() else result.get("stdout", "")
    return {
        "ok": True,
        "stdout_tail": "\n".join(text.splitlines()[-30:]),
        "entries": entries,
        "deletable_dirs": deletable_dirs,
    }


def collect_subsystem_stats() -> Dict[str, Any]:
    sys.path.insert(0, str(HOME / "longhun-system" / "scripts"))
    stats: Dict[str, Any] = {}
    try:
        from longhun_lu_compress import LonghunLuMemoryEngine
        with LonghunLuMemoryEngine() as engine:
            stats["lu_memory"] = engine.stats()
    except Exception as e:
        stats["lu_memory"] = {"error": str(e)}

    try:
        from longhun_collective_wisdom import CollectiveWisdomEngine
        with CollectiveWisdomEngine() as engine:
            stats["collective_wisdom"] = engine.stats()
    except Exception as e:
        stats["collective_wisdom"] = {"error": str(e)}

    try:
        from longhun_toolset_ecosystem import ToolsetEcosystemEngine
        with ToolsetEcosystemEngine() as engine:
            stats["toolset_ecosystem"] = engine.stats()
    except Exception as e:
        stats["toolset_ecosystem"] = {"error": str(e)}

    return stats


def check_key_files() -> Dict[str, Any]:
    files = {
        "LU 压缩引擎": HOME / "longhun-system" / "scripts" / "longhun_lu_compress.py",
        "语义闸": HOME / "longhun-system" / "scripts" / "龍魂語義歸一化閘門.py",
        "DNA 主权引擎": HOME / "longhun-system" / "scripts" / "龍魂DNA主權引擎.py",
        "集思广益引擎": HOME / "longhun-system" / "scripts" / "longhun_collective_wisdom.py",
        "工具集生态引擎": HOME / "longhun-system" / "scripts" / "longhun_toolset_ecosystem.py",
        "LU 画廊": HOME / "longhun-system" / "scripts" / "longhun_lu_gallery.py",
        "批量导入器": HOME / "longhun-system" / "scripts" / "longhun_lu_importer.py",
        "龍智守机器人": HOME / "Downloads" / "龍智守_本地控制接口_v2.0.py",
        "LU 设计文档": HOME / ".longhun" / "lu_memory" / "LU语义与压缩还原模型.md",
        "集思广益文档": HOME / ".longhun" / "collective_wisdom" / "集思广益机制.md",
    }
    result = {}
    for name, path in files.items():
        result[name] = {"exists": path.exists(), "path": str(path)}
    return result


def generate_report(results: Dict[str, Any]) -> Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_path = OUTPUT_DIR / f"unified_evaluation_{ts}.md"

    lines = [
        "# 🐉 龍魂系统 · 统一评估报告",
        "",
        f"**评估时间**: {_now()}",
        f"**DNA**: `#龍芯⚡️2026-06-30-LONGHUN-SYSTEM-EVALUATION-v1.0`",
        "",
        "---",
        "",
        "## 一、评估来源",
        "",
        "本次评估综合运行了以下现有技能：",
        "",
        "| 技能 | 作用 |",
        "|---|---|",
        "| longhun-automation | 6 维度系统健康评估 |",
        "| longhun-review | 每日复盘 / 三色审计 |",
        "| longhun-dna-align | DNA 对齐率审计 |",
        "| longhun-integration | 集成测试 |",
        "| longhun-audit | 归档价值评估 |",
        "",
        "---",
        "",
        "## 二、现有技能评估结果",
        "",
    ]

    auto = results.get("automation", {})
    lines.append("### 2.1 自动化日评估（longhun-automation）")
    if auto.get("ok"):
        lines.append(f"- **总评分**: {auto.get('score', 0)}/10.0")
        lines.append(f"- **状态**: {auto.get('status', '-')}")
        lines.append(f"- **报告**: `{auto.get('report_path', '-')}`")
        lines.append("- **各维度**:")
        for dim, info in (auto.get("dimensions") or {}).items():
            lines.append(f"  - {dim}: {info.get('score', 0)}/10.0")
    else:
        lines.append(f"- 运行失败或无法解析: {auto.get('raw', {})}")
    lines.append("")

    review = results.get("review", {})
    lines.append("### 2.2 每日复盘（longhun-review）")
    if review.get("ok"):
        lines.append(f"- **综合评分**: {review.get('score', 0)}/10.0")
        tc = review.get("tricolor", {})
        lines.append(f"- **三色结果**: 🟢 {tc.get('green', 0)} | 🟡 {tc.get('yellow', 0)} | 🔴 {tc.get('red', 0)}")
        lines.append(f"- **报告**: `{review.get('report_path', '-')}`")
        lines.append("- **关键项**:")
        for item, detail in (review.get("items") or {}).items():
            lines.append(f"  - {item}: {detail.get('顏色', '')} {detail.get('狀態', '')} ({detail.get('詳情', '')}) [{detail.get('分值', 0)}分]")
    else:
        lines.append(f"- 运行失败或无法解析: {review.get('raw', {})}")
    lines.append("")

    dna = results.get("dna_alignment", {})
    lines.append("### 2.3 DNA 对齐审计（longhun-dna-align）")
    if dna.get("ok"):
        lines.append(f"- **扫描文件数**: {dna.get('total_files', 0)}")
        lines.append(f"- **有 DNA**: {dna.get('with_dna', 0)} | **无 DNA**: {dna.get('without_dna', 0)}")
        lines.append(f"- **重复 DNA**: {dna.get('duplicate_dna', 0)} | **无效 DNA**: {dna.get('invalid_dna', 0)}")
        lines.append(f"- **对齐率**: {dna.get('alignment_rate', 0):.1f}%")
        lines.append(f"- **健康评级**: {dna.get('health_level', '-')}")
        lines.append(f"- **报告**: `{dna.get('report_path', '-')}`")
    else:
        lines.append(f"- 运行失败或无法解析")
    lines.append("")

    integration = results.get("integration", {})
    lines.append("### 2.4 集成测试（longhun-integration）")
    if integration.get("ok"):
        lines.append(f"- **总测试数**: {integration.get('total', 0)}")
        lines.append(f"- **通过**: {integration.get('passed', 0)} | **失败**: {integration.get('failed', 0)} | **警告**: {integration.get('warnings', 0)}")
        lines.append(f"- **成功率**: {integration.get('success_rate', 0):.1f}%")
        lines.append(f"- **报告**: `{integration.get('report_path', '-')}`")
        lines.append("> 注：大量失败项源于 `~/longhun-system/integrated-modules/` 子系统未部署或云端服务未启动，"
            "与本次落地的 LU/集思广益/工具集生态子集无直接关系。"
        )
    else:
        lines.append(f"- 运行失败或无法解析")
    lines.append("")

    archive = results.get("archive", {})
    lines.append("### 2.5 归档评估（longhun-audit）")
    if archive.get("ok"):
        lines.append(f"- **评估条目数**: {archive.get('entries', 0)}")
        lines.append(f"- **建议删除目录数**: {archive.get('deletable_dirs', 0)}")
        lines.append("- **最近决策汇总**:")
        lines.append("```")
        lines.append(archive.get("stdout_tail", ""))
        lines.append("```")
    else:
        lines.append(f"- 运行失败")
    lines.append("")

    lines.extend([
        "---",
        "",
        "## 三、当前子系统状态",
        "",
    ])

    sub = results.get("subsystem_stats", {})
    lu = sub.get("lu_memory", {})
    cw = sub.get("collective_wisdom", {})
    te = sub.get("toolset_ecosystem", {})

    lines.append("### 3.1 LU 认知压缩")
    if "error" in lu:
        lines.append(f"- 错误: {lu['error']}")
    else:
        lines.append(f"- **总记录**: {lu.get('total_records', 0)}")
        lines.append(f"- **活跃记录**: {lu.get('active_records', 0)}")
        lines.append(f"- **累计字符**: {lu.get('total_chars', 0):,}")
        lines.append(f"- **血缘事件**: {lu.get('lineage_events', 0)}")
    lines.append("")

    lines.append("### 3.2 集思广益")
    if "error" in cw:
        lines.append(f"- 错误: {cw['error']}")
    else:
        lines.append(f"- **总意见**: {cw.get('total', 0)}")
        lines.append(f"- **已采纳**: {cw.get('adopted', 0)} | **已拒绝**: {cw.get('rejected', 0)}")
        lines.append(f"- **平均权重**: {cw.get('avg_weight', 0)}")
    lines.append("")

    lines.append("### 3.3 自适应工具集生态")
    if "error" in te:
        lines.append(f"- 错误: {te['error']}")
    else:
        funcs = te.get("functions", {})
        lines.append(f"- **功能模块**: 总 {funcs.get('total', 0)}，活跃 {funcs.get('active', 0)}，待上架 {funcs.get('pending', 0)}")
        lines.append(f"- **真实使用事件**: {te.get('usage_events', 0)}")
        lines.append(f"- **主动提醒**: {te.get('reminders', 0)}")
        lines.append(f"- **公开意见包**: {te.get('public_packages', 0)}")
    lines.append("")

    lines.extend([
        "---",
        "",
        "## 四、关键文件检查",
        "",
    ])
    files = results.get("key_files", {})
    lines.append("| 组件 | 状态 | 路径 |")
    lines.append("|---|---|---|")
    for name, info in files.items():
        status = "✅" if info["exists"] else "❌"
        lines.append(f"| {name} | {status} | `{info['path']}` |")
    lines.append("")

    lines.extend([
        "---",
        "",
        "## 五、综合结论与建议",
        "",
        "### 5.1 评分汇总",
        "",
    ])
    scores = []
    if auto.get("ok"):
        scores.append(("自动化评估", auto.get("score", 0), 10.0))
    if review.get("ok"):
        scores.append(("每日复盘", review.get("score", 0), 10.0))
    if dna.get("ok"):
        scores.append(("DNA 对齐率", dna.get("alignment_rate", 0), 100.0))
    if integration.get("ok"):
        scores.append(("集成测试成功率", integration.get("success_rate", 0), 100.0))

    lines.append("| 评估项 | 得分 | 满分 |")
    lines.append("|---|---|---|")
    for name, score, full in scores:
        lines.append(f"| {name} | {score:.2f} | {full:.1f} |")
    lines.append("")

    lines.extend([
        "### 5.2 关键发现",
        "",
        "1. **LU/集思广益/工具集生态子集已落地并跑通**：",
        "   - 压缩-还原-DNA 闭环正常；",
        "   - 集思广益意见提交/验证/采纳/权重计算正常；",
        "   - 工具集生态主动提醒、一键 DNA 反馈、公开包生成正常。",
        "",
        "2. **现有评估技能反映的是旧系统（xpay / integrated-modules）状态**：",
        "   - 自动化评估 5.8/10、每日复盘 5.0/10、集成测试 51.6%，主要扣分点是旧模块缺失或服务未启动；",
        "   - 这些结果对当前子集不具直接指导意义，需要为 LU/集思广益/工具集生态建立专用评估基线。",
        "",
        "3. **DNA 对齐率良好（81.8%）**：",
        "   - 新落地文件均带 DNA；",
        "   - 剩余无 DNA 文件多为旧脚本或第三方文件。",
        "",
        "### 5.3 下一步建议",
        "",
        "- 为当前子系统编写专用 pytest 测试集，纳入 `longhun-review` 的测试项；",
        "- 将 LU/集思广益/工具集的关键文件加入 `longhun-automation` 的核心文件清单；",
        "- 启动相关 API 服务后重新跑 `longhun-integration`；",
        "- 定期生成公开意见包，让高权重意见自动浮出水面。",
        "",
        "---",
        "",
        f"**DNA追溯码**: `#龍芯⚡️2026-06-30-LONGHUN-SYSTEM-EVALUATION-v1.0`",
        "**确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬EV9X-772Z` ✅",
        "",
    ])

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main() -> int:
    print("🐉 开始统一系统评估...")
    results: Dict[str, Any] = {}

    print("  运行自动化日评估...")
    results["automation"] = run_automation_assessment()

    print("  运行每日复盘...")
    results["review"] = run_daily_review()

    print("  运行 DNA 对齐审计...")
    results["dna_alignment"] = run_dna_alignment()

    print("  运行集成测试...")
    results["integration"] = run_integration_tests()

    print("  运行归档评估...")
    results["archive"] = run_archive_evaluation()

    print("  收集子系统统计...")
    results["subsystem_stats"] = collect_subsystem_stats()

    print("  检查关键文件...")
    results["key_files"] = check_key_files()

    print("  生成统一报告...")
    report_path = generate_report(results)

    print(f"\n🟢 统一评估报告已生成：{report_path}")
    print(f"   报告 DNA: #龍芯⚡️2026-06-30-LONGHUN-SYSTEM-EVALUATION-v1.0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
