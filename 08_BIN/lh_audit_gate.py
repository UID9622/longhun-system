#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·模块正规审计闸 v1.0（GATE·焊死执行流程）
DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-MODULE-AUDIT-GATE-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)  ← 工程实现层

🔥 铁律: 任何模块产出 / 复盘 / 审计交付，交付前必须跑本闸。
   三色 🟢 才可交付 · 🟡 标记待核（48h 内复查）· 🔴 退回重做。

十步审计链:
  [1] 德本审计五问      （离火运五条底线·自查）
  [2] DNA 完整性校验    （cnsh_dna_check.py）
  [3] 语法纠错引擎      （cnsh_editor.py · 370 条规则冒烟）
  [4] 编译器自测        （全样例编译）
  [5] 单元测试          （cnsh_test_runner.py · 三色）
  [6] 转译回归测试      （run_transpile_tests.py）
  [7] 覆盖率            （cnsh_coverage.py）
  [8] 安全审计          （cnsh_editor.py --security）
  [9] GPG 签名扫描      （lh_gpg_sign.py scan 目标）
  [10] 三色汇总+审计报告 （04_AUDIT/module_audit_*.json）

用法:
  python3 bin/lh_audit_gate.py                 # 全量十步
  python3 bin/lh_audit_gate.py --module <路径> # 指定模块/文件/目录
  python3 bin/lh_audit_gate.py --quick         # 核心三步（DNA+编译+测试）
  python3 bin/lh_audit_gate.py --json          # JSON 输出
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT      = Path(__file__).resolve().parent.parent
BIN       = ROOT / "bin"
AUDIT_DIR = ROOT / "04_AUDIT"


def run_step(cmd: list, timeout: int = 120) -> dict:
    """运行一步审计，捕获返回码与输出"""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {"rc": p.returncode, "out": (p.stdout or "")[-400:],
                "err": (p.stderr or "")[-400:]}
    except subprocess.TimeoutExpired:
        return {"rc": -1, "out": "", "err": "超时(%ds)" % timeout}
    except FileNotFoundError as e:
        return {"rc": -2, "out": "", "err": "工具不存在: %s" % e}


def step(seq: int, name: str, cmd: list, green_rcs=(0,),
         timeout: int = 120) -> dict:
    print("\n[%d/10] %s ..." % (seq, name))
    r = run_step(cmd, timeout)
    ok = r["rc"] in green_rcs
    tri = "🟢" if ok else "🔴"
    print("  %s %s rc=%s" % (tri, name, r["rc"]))
    if r["err"]:
        print("  ↳ %s" % r["err"][-300:])
    return {"step": seq, "name": name, "ok": ok, "rc": r["rc"],
            "out_tail": r["out"][-200:], "err_tail": r["err"][-200:]}


def main():
    ap = argparse.ArgumentParser(description="龍魂·模块正规审计闸（焊死）")
    ap.add_argument("--module", "-m", help="指定审计的模块/文件/目录")
    ap.add_argument("--quick", "-q", action="store_true", help="核心三步快速审计")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    t0 = time.time()
    results = []
    tri_counts = {"🟢": 0, "🔴": 0}

    def do(seq, name, cmd, green_rcs=(0,), timeout=120):
        r = step(seq, name, cmd, green_rcs, timeout)
        results.append(r)
        tri_counts["🟢" if r["ok"] else "🔴"] += 1
        return r

    # ── [1] 德本审计五问（自查清单）──
    print("\n[1/10] 德本审计五问（离火运五条底线）...")
    cinco = [
        "德在技术前: 在帮人还是在收割人？",
        "路径对齐: 文件在正确位置？",
        "不让付出者寒心: 绑死好人=穷了没？",
        "信息主权不可让渡: 数据流向平台了没？",
        "外化内不化: 369 不动点还在吗？",
    ]
    for q in cinco:
        print("  □ %s" % q)
    results.append({"step": 1, "name": "德本审计五问", "ok": True,
                    "rc": 0, "out_tail": "", "err_tail": "自查项: 交付人逐条确认"})
    tri_counts["🟢"] += 1

    # ── [2] DNA 完整性校验 ──
    do(2, "DNA 完整性校验",
       [sys.executable, str(BIN / "cnsh_dna_check.py"), "--loose"])

    # ── [3] 语法纠错引擎（370 条规则）──
    do(3, "语法纠错引擎冒烟",
       [sys.executable, str(BIN / "cnsh_editor.py"), "测试 语法"], green_rcs=(0,))

    # ── [4] 编译器自测（全样例编译）──
    samples = ROOT / "tests" / "cnsh_samples"
    if samples.exists():
        all_ok = True
        print("\n[4/10] 编译器自测（全样例编译）...")
        for f in sorted(samples.glob("*.cnsh")):
            r = run_step([sys.executable, str(BIN / "cnsh_compiler.py"),
                          str(f), "-o", "/tmp/audit_gate_out.py"])
            if r["rc"] != 0:
                all_ok = False
                print("  🔴 编译失败: %s: %s" % (f.name, r["err"][-150:]))
        print("  %s 编译器自测 rc=%s" % ("🟢" if all_ok else "🔴",
                                      0 if all_ok else 1))
        results.append({"step": 4, "name": "编译器自测", "ok": all_ok,
                        "rc": 0 if all_ok else 1, "out_tail": "", "err_tail": ""})
        tri_counts["🟢" if all_ok else "🔴"] += 1

    # ── [5] 单元测试（三色）──
    do(5, "单元测试（三色审计）",
       [sys.executable, str(BIN / "cnsh_test_runner.py")], timeout=180)

    # ── [6] 转译回归测试 ──
    do(6, "转译回归测试",
       [sys.executable, str(ROOT / "tests" / "transpile" / "run_transpile_tests.py")],
       timeout=180)

    # ── [7] 覆盖率 ──
    do(7, "覆盖率报告", [sys.executable, str(BIN / "cnsh_coverage.py")])

    # ── [8] 安全审计 ──
    do(8, "安全审计（XSS/SQL/路径注入扫描）",
       [sys.executable, str(BIN / "cnsh_editor.py"), "--security", "测试"],
       timeout=180)

    # ── [9] GPG 签名扫描 ──
    if args.module:
        target = str(Path(args.module).resolve())
        do(9, "GPG 签名扫描: %s" % target,
           [sys.executable, str(BIN / "lh_gpg_sign.py"), "scan", target], timeout=120)
    else:
        do(9, "GPG 签名扫描（cnsh 工具链）",
           [sys.executable, str(BIN / "lh_gpg_sign.py"), "scan",
            str(BIN / "cnsh_test_runner.py")], timeout=120)

    # ── [10] 三色汇总 + 审计报告 ──
    reds = [r for r in results if not r["ok"]]
    greens = [r for r in results if r["ok"]]
    overall = "🔴" if len(reds) > len(results) // 5 else (
        "🟢" if len(reds) == 0 else "🟡")

    report = {
        "timestamp":  datetime.now().isoformat(),
        "dna":        "#龍芯⚡️%s-AUDIT-GATE-UID9622" % datetime.now().date(),
        "tool":       "lh_audit_gate.py v1.0",
        "module":     args.module or "全量",
        "total_steps": len(results),
        "green":      len(greens),
        "red":        len(reds),
        "overall":    overall,
        "elapsed_s":  round(time.time() - t0, 1),
        "steps":      results,
        "conclusion": {
            "🟢": "放行交付（未跑过的代码不得标🟢已验证）",
            "🟡": "标记待核 + 写明验证路径，48h 内复查",
            "🔴": "退回重做 + DNA 追溯",
        }[overall],
    }

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = AUDIT_DIR / ("module_audit_%s.json" % ts)
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2),
                           encoding="utf-8")

    print("\n" + "━" * 50)
    print("🐉 模块正规审计闸 · 汇总")
    print("模块: %s | 步骤: %d | 🟢 %d | 🔴 %d" % (
        report["module"], report["total_steps"], report["green"], report["red"]))
    print("三色: %s | 耗时: %ss" % (overall, report["elapsed_s"]))
    print("结论: %s" % report["conclusion"])
    print("报告: %s" % report_file)
    print("DNA:  %s" % report["dna"])

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))

    sys.exit(0 if overall != "🔴" else 1)


if __name__ == "__main__":
    main()
