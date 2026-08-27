#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 测试运行器 v1.0
DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-CNSH-TEST-RUNNER-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)  ← 工程实现层

功能：
  - 递归扫描 tests/ 下所有 test_*.cnsh / *_test.cnsh 文件
  - 调用 CNSH 编译器编译（真实参数: -o）
  - 执行编译后的 Python 产物
  - 生成三色审计测试报告（🟢≥100% / 🟡≥80% / 🔴<80%）
  - 注册报告哈希到 M73 哈希产权引擎（类库直连，非 HTTP）
  - --watch 模式: 文件变动自动重跑

真实资产对齐（2026-08-25 实测）：
  - 编译器: bin/cnsh_compiler.py（无 --output，用 -o；无 --target，只出 Python）
  - 内置函数: 打印/输入/长度/类型/范围 · 语法: 功能/如果/否则/循环/当/返回
  - M73: render/core/hash_registry.py 的 HashRegistry 类（JSONL 本地存证）
"""

import os
import sys
import subprocess
import json
import hashlib
import time
import argparse
from pathlib import Path
from datetime import datetime

ROOT       = Path(__file__).resolve().parent.parent
TESTS_DIR  = ROOT / "tests"
REPORT_DIR = ROOT / "test_reports"
COMPILER   = ROOT / "bin" / "cnsh_compiler.py"

# ─── 龍魂三色阈值 ───
GREEN_THRESHOLD  = 1.0   # 100% 通过 → 🟢
YELLOW_THRESHOLD = 0.8   # ≥80% 通过  → 🟡（<80% → 🔴）


class CNSHTestRunner:
    """CNSH 测试运行器 · 三色审计 + DNA 追溯 + M73 哈希存证"""

    VERSION = "1.0.0"
    UID     = "UID9622"

    def __init__(self, verbose: bool = False):
        self.results: list = []
        self.passed  = 0
        self.failed  = 0
        self.total   = 0
        self.verbose = verbose
        self._start_time = time.time()

    # ───────── 扫描 ─────────

    def scan_tests(self) -> list:
        """扫描干净测试基线（不扫 tests/ 根目录的历史过时语法文件）

        范围: tests/cnsh_samples + tests/transpile + render/tests
        历史遗留 V21 过时语法文件（tests/*.cnsh 根目录）原样保留、不删除，
        但默认不进基线（避免污染三色判定）。
        """
        roots = [
            TESTS_DIR / "cnsh_samples",
            TESTS_DIR / "transpile",
            ROOT / "render" / "tests",
        ]
        test_files = []
        for root in roots:
            if root.exists():
                test_files.extend(sorted(root.rglob("*.cnsh")))
        return test_files

    # ───────── 单测运行 ─────────

    def run_test(self, test_file: Path) -> dict:
        """编译 + 运行单个测试文件"""
        test_name = test_file.stem
        dna       = self._extract_dna(test_file)
        t0        = time.time()

        tmp_out = ROOT / "_work" / f"cnsh_test_{test_name}.py"
        tmp_out.parent.mkdir(parents=True, exist_ok=True)

        # Step 1: 编译（真实参数 -o）
        compile_cmd = [sys.executable, str(COMPILER),
                       str(test_file), "-o", str(tmp_out)]
        compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)

        if compile_result.returncode != 0:
            return self._build_result(test_name, dna, "red",
                                      error=f"编译失败: {compile_result.stderr[-300:]}",
                                      elapsed=time.time() - t0)

        # Step 2: 执行产物
        try:
            exec_result = subprocess.run(
                [sys.executable, str(tmp_out)],
                capture_output=True, text=True, timeout=30,
            )
            passed = exec_result.returncode == 0
        except subprocess.TimeoutExpired:
            return self._build_result(test_name, dna, "red",
                                      error="运行超时(30s)", elapsed=time.time() - t0)

        return self._build_result(
            test_name, dna,
            "green" if passed else "red",
            output=exec_result.stdout[:2000],
            error=exec_result.stderr[-500:] if not passed else None,
            elapsed=time.time() - t0,
        )

    def _build_result(self, name, dna, color, output=None, error=None, elapsed=0.0) -> dict:
        status = "🟢" if color == "green" else "🔴"
        return {
            "name":      name,
            "dna":       dna,
            "status":    status,
            "tri_color": color,
            "output":    output,
            "error":     error,
            "elapsed":   round(elapsed, 3),
        }

    # ───────── 批量运行 ─────────

    def run_all(self) -> dict:
        test_files = self.scan_tests()
        self.total = len(test_files)

        print(f"\n🐉 CNSH 测试运行器 v{self.VERSION}")
        print(f"DNA: #龍芯⚡️{datetime.now().date()}-TEST-RUN-{self.UID}")
        print(f"发现 {self.total} 个测试文件\n")

        for tf in test_files:
            result = self.run_test(tf)
            self.results.append(result)
            if result["tri_color"] == "green":
                self.passed += 1
            else:
                self.failed += 1
            print(f"  {result['status']} {result['name']}  ({result['elapsed']}s)")
            if self.verbose and result.get("error"):
                print(f"     ↳ {result['error'][:300]}")

        return self._generate_report()

    # ───────── 报告生成 ─────────

    def _generate_report(self) -> dict:
        pass_rate = self.passed / self.total if self.total > 0 else 0
        if pass_rate >= GREEN_THRESHOLD:
            tri_color = "🟢"
        elif pass_rate >= YELLOW_THRESHOLD:
            tri_color = "🟡"
        else:
            tri_color = "🔴"

        dna = f"#龍芯⚡️{datetime.now().date()}-TEST-REPORT-{self.UID}"

        report = {
            "timestamp":  datetime.now().isoformat(),
            "dna":        dna,
            "total":      self.total,
            "passed":     self.passed,
            "failed":     self.failed,
            "pass_rate":  round(pass_rate, 4),
            "elapsed":    round(time.time() - self._start_time, 2),
            "tri_color":  tri_color,
            "results":    self.results,
        }

        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = REPORT_DIR / f"test_report_{ts}.json"
        report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2),
                               encoding="utf-8")
        print(f"\n📄 报告: {report_file}")

        # M73 哈希产权存证（类库直连）
        self._register_hash(report_file)

        return report

    def _register_hash(self, report_file: Path):
        """注册报告哈希到 M73 HashRegistry（本地 JSONL，非 HTTP）"""
        try:
            sys.path.insert(0, str(ROOT))
            from render.core.hash_registry import HashRegistry
            reg = HashRegistry()
            content = report_file.read_bytes()
            sha256 = hashlib.sha256(content).hexdigest()
            reg.register(
                sha256=sha256,
                dna=f"#龍芯⚡️{datetime.now().date()}-TEST-REPORT-{self.UID}",
                url=str(report_file),
                platform="local",
            )
            print(f"  🔐 M73 哈希产权注册成功: {sha256[:16]}...")
        except Exception as e:
            print(f"  ⚠️  M73 未注册（非阻塞）: {str(e)[:80]}")

    def _extract_dna(self, filepath: Path) -> str:
        """提取文件首个 DNA 码（兼容干支式与日期式）"""
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
            for line in content.split("\n"):
                if "#龍芯⚡️" in line:
                    return line.strip().lstrip("#").strip()
        except Exception:
            pass
        return "⚠️ 无DNA — 需补全"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CNSH 测试运行器（三色审计）")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--watch", "-w", action="store_true",
                        help="监听文件变动，自动重跑")
    args = parser.parse_args()

    if args.watch:
        print("👁️  watch 模式：等待 .cnsh 文件变动...")
        last_sig = ""
        while True:
            files = list(TESTS_DIR.rglob("*.cnsh"))
            sig = hashlib.md5(
                b"".join(f.read_bytes() for f in files) if files else b""
            ).hexdigest()
            if sig != last_sig:
                last_sig = sig
                runner = CNSHTestRunner(verbose=args.verbose)
                report = runner.run_all()
                print(f"\n三色: {report['tri_color']} | "
                      f"通过率: {report['pass_rate'] * 100:.1f}%")
            time.sleep(2)
    else:
        runner = CNSHTestRunner(verbose=args.verbose)
        report = runner.run_all()
        print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"总计: {report['total']} | ✅ 通过: {report['passed']} | "
              f"❌ 失败: {report['failed']}")
        print(f"通过率: {report['pass_rate'] * 100:.1f}% | 耗时: {report['elapsed']}s")
        print(f"三色: {report['tri_color']}")
        print(f"DNA:  {report['dna']}")
        sys.exit(1 if report["failed"] > 0 else 0)
