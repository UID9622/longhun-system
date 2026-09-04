#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷯井-FIX_DNA-v1.0
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

"""
🧮 龍魂数学公式套件统一运行器
═══════════════════════════════════════════════════════════════════════════

把核心算法层的脚本串成一键自检：
  1. formula_core_v2.py      —— F01-F25 全公式代码实现自检
  2. formula_chain_v2.py     —— 根治理决策链 + CNSH 双视角封装自检
  3. formula_catalog_v2.py   —— F01-F25 母册完整性自检
  4. formula_core_cnsh.py    —— 单公式 + 易经 CNSH 双视角封装自检
  5. yijing_engine.py        —— 易经 64 卦推演引擎自检
  6. yijing_decision_bridge.py —— 易经 → 决策链联动桥接自检
  7. terminology_bank.py     —— 中央藏经阁术语导入/查询抽检

输出：聚合报告 + CNSH 双视角封装（M:: + CNSH::）。

DNA：    #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-SUITE-RUNNER-v2.3-ALL-ROUTES-DONE
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL:    #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
三色审计：🟢 通过
═══════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations
import os
import sys
import io
import hashlib
import json
import time
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, List, Any

# ============ 路径注入 ============
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORMULA_DIR = os.path.join(ROOT, "cnsh-core", "downloads-imports", "formula", "计算公式")
YIJING_DIR = os.path.join(ROOT, "scripts", "yijing_algorithm")
TERMINOLOGY_DIR = os.path.join(ROOT, "cnsh-terminal", "modules")
SCRIPTS_DIR = os.path.join(ROOT, "scripts")

for p in (FORMULA_DIR, YIJING_DIR, TERMINOLOGY_DIR, SCRIPTS_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)


# ============ 运行辅助 ============

def run_selftest(module_name: str, func_name: str = "selftest") -> Dict[str, Any]:
    """运行某模块的自检函数，捕获输出与异常"""
    result = {"name": module_name, "ok": False, "error": None, "output": ""}
    try:
        module = __import__(module_name)
        test_func = getattr(module, func_name, None)
        if test_func is None:
            result["error"] = f"模块没有 {func_name}()"
            return result

        buf = io.StringIO()
        with redirect_stdout(buf), redirect_stderr(buf):
            test_func()
        result["ok"] = True
        result["output"] = buf.getvalue()
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"
        # 仍尝试保留已输出内容
        result["output"] = getattr(e, "__traceback__", "")
    return result



def run_terminology_check() -> Dict[str, Any]:
    """术语库抽检：导入数学公式术语 + 查询 digital_root"""
    result = {"name": "terminology_bank", "ok": False, "error": None, "output": ""}
    try:
        import terminology_bank as tb
        buf = io.StringIO()
        with redirect_stdout(buf), redirect_stderr(buf):
            藏经阁 = tb.中央藏经阁()
            imported = tb.导入数学公式术语(藏经阁)
            hits = 藏经阁.查询术语("digital_root", 数量=3)
            stats = 藏经阁.获取统计()
            assert any(h["英文"] == "digital_root" for h in hits), "未命中 digital_root"
            assert stats["术语总数"] >= 19, f"术语总数不足：{stats['术语总数']}"
            chroma_enabled = (藏经阁.chroma集合 is not None) and (藏经阁.嵌入模型 is not None)
            print(f"[1] 数学公式术语导入：{sum(imported.values())}/{len(imported)} 条成功")
            print(f"[2] 查询 digital_root 命中：{len(hits)} 条")
            print(f"[3] 术语库统计：总数={stats['术语总数']} 分类={len(stats.get('分类统计', {}))}")
            print(f"[4] Chroma 向量检索：{'已启用 ✅' if chroma_enabled else '未启用（SQLite 回退）⚠️'}")
        result["ok"] = True
        result["output"] = buf.getvalue()
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"
    return result


# ============ 主控 ============

def run_all() -> Dict[str, Any]:
    """运行全部套件"""
    start = time.time()
    results: List[Dict] = []

    results.append(run_selftest("formula_core_v2"))
    results.append(run_selftest("formula_chain_v2"))
    results.append(run_selftest("formula_catalog_v2"))
    results.append(run_selftest("formula_core_cnsh"))
    results.append(run_selftest("yijing_engine"))
    results.append(run_selftest("yijing_decision_bridge"))
    results.append(run_terminology_check())

    elapsed = round((time.time() - start) * 1000, 3)
    passed = sum(1 for r in results if r["ok"])
    failed = len(results) - passed
    all_ok = failed == 0

    # 聚合报告文本
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("🧮 龍魂数学公式套件统一运行器 v2.3")
    report_lines.append("=" * 80)
    report_lines.append(f"总耗时：{elapsed} ms")
    report_lines.append(f"通过：{passed}/{len(results)} · 失败：{failed}/{len(results)}")
    report_lines.append("")

    for r in results:
        icon = "🟢" if r["ok"] else "🔴"
        report_lines.append(f"{icon} {r['name']}")
        if r["error"]:
            report_lines.append(f"   错误：{r['error']}")
        # 只打印自检输出的首行摘要，避免刷屏
        out_summary = r["output"].strip().splitlines()[0] if r["output"].strip() else "(无输出)"
        report_lines.append(f"   摘要：{out_summary}")
        report_lines.append("")

    report_lines.append("=" * 80)
    if all_ok:
        report_lines.append("🟢 全部套件自检通过")
    else:
        report_lines.append("🔴 存在失败套件，需修复")
    report_lines.append("=" * 80)
    report_text = "\n".join(report_lines)

    # CNSH 双视角封装
    payload = {
        "suite": "math_formula_v2.3",
        "passed": passed,
        "total": len(results),
        "elapsed_ms": elapsed,
        "details": {r["name"]: r["ok"] for r in results}
    }
    payload_json = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    trace_hash = hashlib.sha256(payload_json.encode()).hexdigest()[:16]

    cnsh = {
        "M::": {
            "type": "math_suite_aggregate",
            "status": "pass" if all_ok else "reject",
            "payload": payload
        },
        "CNSH::": {
            "dna": "#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-MATH-SUITE-RUNNER-v2.3-ALL-ROUTES-DONE",
            "gate": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
            "audit": "🟢" if all_ok else "🔴",
            "policy": "pass" if all_ok else "reject",
            "trace_hash": trace_hash,
        }
    }

    return {"report": report_text, "cnsh": cnsh, "all_ok": all_ok, "results": results}


if __name__ == "__main__":
    outcome = run_all()
    print(outcome["report"])
    print("\n【CNSH 双视角封装】")
    print(json.dumps(outcome["cnsh"], ensure_ascii=False, indent=2))
    sys.exit(0 if outcome["all_ok"] else 1)
