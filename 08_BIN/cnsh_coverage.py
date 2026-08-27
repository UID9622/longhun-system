#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 代码覆盖率 v1.1
DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-CNSH-COVERAGE-v1.1-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)  ← 工程实现层

功能（静态基线·诚实可算·不编造）：
  - 可编译率: 通过编译器的样例文件 / 总样例文件（语法覆盖）
  - DNA 覆盖率: 文件头含 DNA（#龍芯⚡️）的文件 / 总文件
  - 综合评分 = 可编译率×0.7 + DNA覆盖×0.3 → 三色判定
  - 行级运行时覆盖（trace 采集）为扩展接口，默认不假装有数据
  - 生成 JSON 报告 + HTML 报告
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

ROOT      = Path(__file__).resolve().parent.parent
COMPILER  = ROOT / "bin" / "cnsh_compiler.py"
SAMPLE_DIRS = [ROOT / "tests" / "cnsh_samples", ROOT / "tests" / "cnsh-v1.0"]


class CNSHCoverage:
    """CNSH 覆盖率 · 可编译率 + DNA 覆盖 + 三色判定"""

    GREEN_THRESHOLD  = 0.80
    YELLOW_THRESHOLD = 0.50

    def __init__(self):
        self.total_files = 0
        self.compile_ok  = 0
        self.dna_ok      = 0
        self.total_lines = 0
        self._file_stats = {}

    def check_file(self, filepath: Path):
        """静态检查单文件: 可编译性 + 文件头 DNA"""
        fn = str(filepath.relative_to(ROOT))
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return

        lines = content.split("\n")
        executable = sum(1 for ln in lines
                         if ln.strip() and not ln.strip().startswith("#"))
        header = "\n".join(lines[:5])
        has_dna = "#龍芯⚡️" in header

        # 编译检测
        tmp = ROOT / "_work" / ("cov_check_%s.py" % filepath.stem)
        tmp.parent.mkdir(parents=True, exist_ok=True)
        p = subprocess.run([sys.executable, str(COMPILER), str(filepath),
                            "-o", str(tmp)], capture_output=True, text=True)
        compiles = p.returncode == 0

        self.total_files += 1
        if compiles:
            self.compile_ok += 1
        if has_dna:
            self.dna_ok += 1
        self.total_lines += executable
        self._file_stats[fn] = {
            "executable": executable, "dna": has_dna, "compiles": compiles}

    def compile_coverage(self) -> float:
        return (self.compile_ok / self.total_files if self.total_files > 0 else 0)

    def dna_coverage(self) -> float:
        return (self.dna_ok / self.total_files if self.total_files > 0 else 0)

    def report(self) -> dict:
        cc = self.compile_coverage()
        dc = self.dna_coverage()
        overall = cc * 0.7 + dc * 0.3
        tri = ("🟢" if overall >= self.GREEN_THRESHOLD else
               "🟡" if overall >= self.YELLOW_THRESHOLD else "🔴")
        return {
            "timestamp":        datetime.now().isoformat(),
            "dna":              "#龍芯⚡️%s-COVERAGE-UID9622" % datetime.now().date(),
            "total_files":      self.total_files,
            "compile_ok":       self.compile_ok,
            "dna_ok":           self.dna_ok,
            "compile_coverage": round(cc, 4),
            "dna_coverage":     round(dc, 4),
            "overall":          round(overall, 4),
            "tri_color":        tri,
            "file_stats":       self._file_stats,
        }

    def generate_html(self, output_path: Path = None) -> Path:
        r = self.report()
        if output_path is None:
            output_path = ROOT / "test_reports" / "coverage.html"
        rows = "".join(
            "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                k, v["executable"], "✅" if v["compiles"] else "❌",
                "✅" if v["dna"] else "❌")
            for k, v in r["file_stats"].items())
        html = """<!DOCTYPE html>
<html lang='zh'><head><meta charset='UTF-8'>
<title>CNSH 覆盖率报告</title>
<style>body{font-family:monospace;max-width:900px;margin:auto;padding:20px}
.green{color:#22c55e}.yellow{color:#f59e0b}.red{color:#ef4444}
table{border-collapse:collapse;width:100%%}
td,th{border:1px solid #ccc;padding:6px 12px}
</style></head><body>
<h1>🐉 CNSH 覆盖率报告</h1>
<p>DNA: %s</p>
<p>生成时间: %s</p>
<h2>总览</h2>
<table><tr><th>维度</th><th>覆盖率</th><th>三色</th></tr>
<tr><td>可编译率(语法覆盖)</td><td>%.1f%%</td><td>%s</td></tr>
<tr><td>DNA覆盖率</td><td>%.1f%%</td><td>-</td></tr>
<tr><td>综合评分</td><td>%.1f%%</td><td>%s</td></tr>
</table>
<h2>文件明细</h2>
<table><tr><th>文件</th><th>可执行行</th><th>可编译</th><th>含DNA</th></tr>
%s
</table>
</body></html>""" % (r["dna"], r["timestamp"],
                      r["compile_coverage"] * 100, r["tri_color"],
                      r["dna_coverage"] * 100,
                      r["overall"] * 100, r["tri_color"], rows)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
        return output_path


def main():
    cov = CNSHCoverage()
    for t in SAMPLE_DIRS:
        if t.exists():
            for f in sorted(t.rglob("*.cnsh")):
                cov.check_file(f)
    r = cov.report()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    html_path = cov.generate_html()
    print("📊 HTML 报告: %s" % html_path)
    print("\n三色: %s | 可编译率: %.1f%% | DNA覆盖: %.1f%% | 综合: %.1f%%" % (
        r["tri_color"], r["compile_coverage"] * 100,
        r["dna_coverage"] * 100, r["overall"] * 100))
    sys.exit(0 if r["tri_color"] == "🟢" else 1)


if __name__ == "__main__":
    main()
