#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 转译测试 v1.0
DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-CNSH-TRANSPILE-TEST-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)  ← 工程实现层

功能：CNSH → Python 转译回归测试
  1. 对每个 .cnsh 源文件编译
  2. 断言产物包含编译器签名头（由CNSH编译器自动生成）
  3. 运行产物，断言退出码 0
  4. 三色判定汇总

诚实边界（2026-08-25 实测）：
  - 编译器 bin/cnsh_compiler.py 当前只输出 Python（无 --target 参数）
  - C / JS 目标：编译器暂未支持，状态标记 🟡待支持（不假装通过）

Bug B5 已修: 原稿仅有目录结构，本文件为完整实现。
"""

import sys
import subprocess
from pathlib import Path

ROOT        = Path(__file__).resolve().parent.parent.parent
SAMPLE_DIRS = [ROOT / "tests" / "cnsh_samples", ROOT / "tests" / "cnsh-v1.0"]
COMPILER    = ROOT / "bin" / "cnsh_compiler.py"


class TranspileTestRunner:
    """CNSH 转译回归测试运行器"""

    TARGETS = ["python", "c", "js"]  # c/js 待编译器支持

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []

    def scan_cases(self) -> list:
        cases = []
        for d in SAMPLE_DIRS:
            if d.exists():
                cases.extend(sorted(d.rglob("*.cnsh")))
        return sorted(set(cases))

    def run_case(self, cnsh_file: Path) -> dict:
        case_name = cnsh_file.stem
        result = {"name": case_name, "targets": {}}

        tmp_out = ROOT / "_work" / ("transpile_%s.py" % case_name)
        tmp_out.parent.mkdir(parents=True, exist_ok=True)

        proc = subprocess.run(
            [sys.executable, str(COMPILER), str(cnsh_file), "-o", str(tmp_out)],
            capture_output=True, text=True,
        )

        if proc.returncode != 0:
            result["targets"]["python"] = {
                "status": "🔴", "error": proc.stderr[-300:]}
            self.failed += 1
            self.results.append(result)
            return result

        actual = tmp_out.read_text(encoding="utf-8", errors="ignore")
        has_sign = "由CNSH编译器自动生成" in actual

        try:
            run = subprocess.run([sys.executable, str(tmp_out)],
                                 capture_output=True, text=True, timeout=30)
            run_ok = run.returncode == 0
        except subprocess.TimeoutExpired:
            run_ok = False

        if has_sign and run_ok:
            result["targets"]["python"] = {"status": "🟢"}
            self.passed += 1
        else:
            detail = []
            if not has_sign:
                detail.append("产物缺编译器签名头")
            if not run_ok:
                detail.append("产物运行失败")
            result["targets"]["python"] = {
                "status": "🔴", "error": "; ".join(detail)}
            self.failed += 1

        for t in ("c", "js"):
            result["targets"][t] = {"status": "🟡", "note": "编译器暂未支持此目标"}

        self.results.append(result)
        return result

    def run_all(self) -> dict:
        cases = self.scan_cases()
        print("\n🔄 CNSH 转译回归测试 | 发现 %d 个源文件" % len(cases))

        for case in cases:
            r = self.run_case(case)
            parts = " ".join("%s:%s" % (t, v["status"])
                             for t, v in r["targets"].items())
            print("  %s: %s" % (r["name"], parts))

        total = self.passed + self.failed
        tri = "🟢" if self.failed == 0 else (
            "🟡" if self.failed <= max(1, total // 5) else "🔴")
        return {
            "total":     total,
            "passed":    self.passed,
            "failed":    self.failed,
            "tri_color": tri,
            "results":   self.results,
        }


if __name__ == "__main__":
    runner = TranspileTestRunner()
    report = runner.run_all()
    print("\n三色: %s | 通过: %d/%d" % (report["tri_color"],
                                       report["passed"], report["total"]))
    sys.exit(1 if report["failed"] > 0 else 0)
