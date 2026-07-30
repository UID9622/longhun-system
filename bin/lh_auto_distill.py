#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-AUTO-DISTILL-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════
# 龍魂 · 自动蒸馏循环 v1.0
# ═══════════════════════════════════════════
# DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-AUTO-DISTILL-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 三色审计: 🟢 通过
# ═══════════════════════════════════════════
# 生态心脏：修复 → 测试全绿 → 数据更新 → 自动训练 → 合并导出 → 审计 → 产出新模型
#
# 用法:
#   python3 bin/lh_auto_distill.py --dry-run    # 干运行，预览全流程
#   python3 bin/lh_auto_distill.py --smoke      # 冒烟模式（5 iter快速验证）
#   python3 bin/lh_auto_distill.py --live       # 实战：真正跑训练
#   python3 bin/lh_auto_distill.py --base-model qwen2.5:1.5b  # 指定底座
# ═══════════════════════════════════════════
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 核心路径
TESTS_DIR = PROJECT_ROOT / "tests"
REORG_SCRIPT = PROJECT_ROOT / "bin" / "lh_reorganize.py"
TRAINER_V419 = PROJECT_ROOT / "bin" / "lh_lora_trainer_v419.py"
AUDIT_SCRIPT = PROJECT_ROOT / "bin" / "lh_full_system_audit.py"
CNSH_CORPUS_DIR = PROJECT_ROOT / "data" / "reorganize" / "cnsh_corpus"
REPORT_DIR = PROJECT_ROOT / "L7_数据层" / "auto_distill_reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def _run(cmd: List[str], cwd: Path = PROJECT_ROOT, timeout: int = 300) -> Dict[str, Any]:
    """运行命令并返回结构化结果。"""
    start = time.time()
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
        )
        return {
            "status": "🟢" if proc.returncode == 0 else "🔴",
            "returncode": proc.returncode,
            "stdout": proc.stdout[-2000:],
            "stderr": proc.stderr[-1000:],
            "elapsed": round(time.time() - start, 2),
        }
    except subprocess.TimeoutExpired:
        return {"status": "🟡", "error": f"超时（>{timeout}s）", "elapsed": timeout}
    except Exception as e:
        return {"status": "🔴", "error": str(e), "elapsed": round(time.time() - start, 2)}


def step_tests() -> Dict[str, Any]:
    """Step 1: 跑单元测试。"""
    print("\n" + "─" * 50)
    print("🔬 Step 1/6: 单元测试")
    print("─" * 50)

    result = _run(
        [sys.executable, "-m", "pytest", "tests/test_base_reorganizer.py", "-v", "-q"],
        timeout=120,
    )
    passed = result["status"] == "🟢"
    print(f"   状态: {result['status']} | 耗时: {result['elapsed']}s")
    if not passed:
        print(f"   stderr: {result.get('stderr', '')[:300]}")
    return {"name": "单元测试", "passed": passed, **result}


def step_generate_corpus() -> Dict[str, Any]:
    """Step 2: 生成CNSH启蒙语料库。"""
    print("\n" + "─" * 50)
    print("📚 Step 2/6: 生成CNSH启蒙语料库")
    print("─" * 50)

    result = _run(
        [sys.executable, str(REORG_SCRIPT), "cnsh-corpus", "--count", "100"],
        timeout=120,
    )
    passed = result["status"] == "🟢"

    # 统计产出
    corpus_file = sorted(CNSH_CORPUS_DIR.glob("cnsh_training_corpus_*.jsonl"))
    count = 0
    if corpus_file:
        count = sum(1 for _ in open(corpus_file[-1]))
    print(f"   状态: {result['status']} | 语料条数: {count}")
    return {"name": "CNSH语料生成", "passed": passed, "corpus_count": count, **result}


def step_inject_concepts() -> Dict[str, Any]:
    """Step 3: 注入概念关系 + CNSH场景。"""
    print("\n" + "─" * 50)
    print("💉 Step 3/6: 注入概念关系 + CNSH场景")
    print("─" * 50)

    result = _run([sys.executable, str(REORG_SCRIPT), "inject"], timeout=120)
    passed = result["status"] == "🟢"
    print(f"   状态: {result['status']} | 耗时: {result['elapsed']}s")
    return {"name": "概念关系注入", "passed": passed, **result}


def step_train(smoke: bool = False, dry_run: bool = False) -> Dict[str, Any]:
    """Step 4: 自动训练 v4.1.9。"""
    print("\n" + "─" * 50)
    print("⚔️ Step 4/6: 自动训练 → longhun-v4.1.9")
    print("─" * 50)

    if dry_run:
        print("   [干运行] 将执行: python3 bin/lh_lora_trainer_v419.py all")
        return {"name": "自动训练", "passed": True, "dry_run": True}

    action = "test" if smoke else "all"
    timeout = 600 if smoke else 86400  # smoke 10分钟，实战24小时
    result = _run(
        [sys.executable, str(TRAINER_V419), action],
        timeout=timeout,
    )
    passed = result["status"] == "🟢"
    print(f"   状态: {result['status']} | 耗时: {result['elapsed']}s")
    if not passed:
        print(f"   stderr: {result.get('stderr', '')[:500]}")
    return {"name": "自动训练", "passed": passed, "smoke": smoke, **result}


def step_audit(dry_run: bool = False) -> Dict[str, Any]:
    """Step 5: 全系统审计。"""
    print("\n" + "─" * 50)
    print("🔍 Step 5/6: 全系统审计")
    print("─" * 50)

    if dry_run:
        print("   [干运行] 将执行: python3 bin/lh_full_system_audit.py")
        return {"name": "全系统审计", "passed": True, "dry_run": True}

    result = _run([sys.executable, str(AUDIT_SCRIPT)], timeout=600)
    passed = result["status"] == "🟢"
    print(f"   状态: {result['status']} | 耗时: {result['elapsed']}s")
    return {"name": "全系统审计", "passed": passed, **result}


def step_verify_model() -> Dict[str, Any]:
    """Step 6: 验证新模型是否能在Ollama加载。"""
    print("\n" + "─" * 50)
    print("🧪 Step 6/6: 模型可用性验证")
    print("─" * 50)

    result = _run(["ollama", "list"], timeout=30)
    has_v419 = "longhun-v4.1.9" in result.get("stdout", "")
    passed = has_v419
    print(f"   Ollama中 longhun-v4.1.9: {'✅' if has_v419 else '❌'}")
    return {"name": "模型可用性验证", "passed": passed, "has_v419": has_v419, **result}


def generate_report(steps: List[Dict], dry_run: bool, smoke: bool) -> Path:
    """生成蒸馏循环报告。"""
    report_id = f"auto_distill_{_timestamp()}"
    report_path = REPORT_DIR / f"{report_id}.json"

    all_passed = all(s.get("passed", False) for s in steps)

    report = {
        "报告ID": report_id,
        "DNA": f"#龍芯⚡️{_timestamp()[:8]}-AUTO-DISTILL-{hashlib.sha256(report_id.encode()).hexdigest()[:8]}",
        "模式": "干运行" if dry_run else ("冒烟" if smoke else "实战"),
        "时间": datetime.now(timezone.utc).isoformat(),
        "整体状态": "🟢 全部通过" if all_passed else "🔴 存在失败",
        "步骤": steps,
        "产出模型": "longhun-v4.1.9" if (not dry_run and all_passed) else "未产出",
        "确认码": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    }

    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # 同时写一份 Markdown 摘要
    md_path = REPORT_DIR / f"{report_id}.md"
    md_lines = [
        f"# 龍魂自动蒸馏循环报告 · {report_id}",
        "",
        f"**时间**: {report['时间']}",
        f"**模式**: {report['模式']}",
        f"**整体状态**: {report['整体状态']}",
        f"**DNA**: `{report['DNA']}`",
        "",
        "## 步骤明细",
        "",
        "| 步骤 | 状态 | 耗时 | 备注 |",
        "|:---|:---:|:---:|:---|",
    ]
    for s in steps:
        md_lines.append(
            f"| {s['name']} | {s.get('status', s.get('passed', False) and '🟢' or '🔴')} | "
            f"{s.get('elapsed', '-')}s | {s.get('corpus_count', '')} |"
        )
    md_lines.extend(["", f"## 产出", "", f"- 模型: {report['产出模型']}", f"- 报告JSON: {report_path}"])
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    return report_path


def main():
    parser = argparse.ArgumentParser(
        description="龍魂自动蒸馏循环 — 修复→测试→训练→审计→产出v4.1.9"
    )
    parser.add_argument("--dry-run", action="store_true", help="干运行，不真正训练")
    parser.add_argument("--smoke", action="store_true", help="冒烟模式，只跑5 iter训练")
    parser.add_argument("--base-model", default="qwen2.5:1.5b", help="底座模型ID（用于重组管线）")
    parser.add_argument("--skip-train", action="store_true", help="跳过训练步骤")
    parser.add_argument("--skip-audit", action="store_true", help="跳过审计步骤")
    args = parser.parse_args()

    print("=" * 60)
    print("🐉 龍魂自动蒸馏循环 v1.0")
    print("=" * 60)
    print(f"模式: {'干运行' if args.dry_run else ('冒烟' if args.smoke else '实战')}")
    print(f"底座: {args.base_model}")
    print("=" * 60)

    steps = []

    # Step 1: 测试
    steps.append(step_tests())
    if not steps[-1]["passed"]:
        print("\n🔴 测试未通过，停止循环。")
        report_path = generate_report(steps, args.dry_run, args.smoke)
        print(f"\n报告已保存: {report_path}")
        sys.exit(1)

    # Step 2: 生成CNSH语料
    steps.append(step_generate_corpus())

    # Step 3: 注入概念关系
    steps.append(step_inject_concepts())

    # Step 4: 训练
    if args.skip_train:
        steps.append({"name": "自动训练", "passed": True, "skipped": True})
    else:
        steps.append(step_train(smoke=args.smoke, dry_run=args.dry_run))

    # Step 5: 审计
    if args.skip_audit:
        steps.append({"name": "全系统审计", "passed": True, "skipped": True})
    else:
        steps.append(step_audit(dry_run=args.dry_run))

    # Step 6: 模型验证（仅在非干运行且训练未跳过）
    if not args.dry_run and not args.skip_train:
        steps.append(step_verify_model())
    else:
        steps.append({"name": "模型可用性验证", "passed": True, "skipped": True})

    # 生成报告
    report_path = generate_report(steps, args.dry_run, args.smoke)

    # 终报
    all_passed = all(s.get("passed", False) for s in steps)
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 自动蒸馏循环完成")
        print(f"🐉 产出模型: longhun-v4.1.9")
    else:
        print("🔴 自动蒸馏循环存在失败步骤")
    print(f"📊 报告: {report_path}")
    print("=" * 60)

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
