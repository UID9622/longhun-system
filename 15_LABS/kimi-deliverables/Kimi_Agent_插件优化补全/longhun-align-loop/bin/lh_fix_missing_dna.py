#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·自动补DNA签章 v2.0
DNA: 由 bin/lh_dna_generator.py 生成
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

v2.0 修复清单：
  1. 【致命BUG修复】v1.0 用了 datetime 但没 import，一跑就崩
  2. 【合规】DNA 一律调用 bin/lh_dna_generator.py 生成（干支四柱+卦名），
     禁止手写时间戳格式；生成器不可用时跳过该文件并告警，绝不写违规DNA
  3. 【P0：不删除只冻结】写入前先把原文件备份到 archive/frozen/，再改
  4. 幂等：已有DNA的文件直接跳过
  5. 支持三种输入：命令行参数 / stdin 列表 / --from-report <对齐报告json>

用法：
  python3 bin/lh_fix_missing_dna.py file1.py file2.py
  python3 bin/lh_fix_missing_dna.py --from-report reports/align_xxx.json
  cat filelist.txt | python3 bin/lh_fix_missing_dna.py
"""

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

BASE_DIR = Path.home() / "longhun-system"
FROZEN_DIR = BASE_DIR / "archive" / "frozen"   # P0：不删除只冻结
DNA_GENERATOR = BASE_DIR / "bin" / "lh_dna_generator.py"
CONFIRM_LINE = "# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def generate_dna(action_tag: str = "补DNA", version: str = "v1.0") -> Optional[str]:
    """调用本地DNA生成器，返回形如 '# DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-补DNA-v1.0' 的行。
    生成器不可用或输出异常时返回 None（绝不手写DNA）。"""
    if not DNA_GENERATOR.exists():
        print(f"⚠️ DNA生成器不存在: {DNA_GENERATOR}")
        return None
    try:
        result = subprocess.run(
            [sys.executable, str(DNA_GENERATOR),
             "--tag", action_tag, "--version", version],
            capture_output=True, text=True, timeout=30,
        )
    except subprocess.TimeoutExpired:
        print("⚠️ DNA生成器超时")
        return None
    if result.returncode != 0:
        print(f"⚠️ DNA生成器执行失败: {result.stderr[:200]}")
        return None
    # 从输出中提取以 #龍芯 开头的DNA串
    for line in result.stdout.splitlines():
        line = line.strip()
        if "#龍芯" in line:
            return f"# DNA: {line}" if not line.startswith("# DNA:") else line
    print(f"⚠️ DNA生成器输出无法识别: {result.stdout[:200]}")
    return None


def freeze_original(p: Path) -> Path:
    """写入前冻结原文件（P0：不删除只冻结）"""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    rel = p.name
    frozen_path = FROZEN_DIR / f"{rel}.{ts}.frozen"
    FROZEN_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, frozen_path)
    return frozen_path


def fix_dna(filepath: str) -> str:
    p = Path(filepath)
    if not p.exists():
        return f"❌ 文件不存在: {filepath}"
    if p.suffix not in (".py", ".sh", ".md", ".js", ".ts"):
        return f"⏭️ 跳过非文本代码文件: {filepath}"

    content = p.read_text(encoding="utf-8", errors="replace")
    if "# DNA:" in content and "#龍芯" in content:
        return f"⏭️ 已存在DNA: {filepath}"

    dna_line = generate_dna()
    if dna_line is None:
        return f"🟡 DNA生成器不可用，跳过（需人工处理）: {filepath}"

    header_lines = [dna_line]
    if "#CONFIRM🌌9622" not in content:
        header_lines.append(CONFIRM_LINE)
    new_content = "\n".join(header_lines) + "\n" + content

    frozen = freeze_original(p)   # 先冻结，再写入
    p.write_text(new_content, encoding="utf-8")
    return f"✅ 已补DNA: {filepath}（原版已冻结: {frozen.name}）"


def files_from_report(report_path: str) -> List[str]:
    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)
    missing = report.get("missing_dna") or []
    if isinstance(missing, dict):
        out: List[str] = []
        for v in missing.values():
            out.extend(v if isinstance(v, list) else [v])
        return [x for x in out if isinstance(x, str)]
    return [x for x in missing if isinstance(x, str)]


def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂·自动补DNA签章 v2.0")
    parser.add_argument("files", nargs="*", help="待补DNA的文件")
    parser.add_argument("--from-report", help="从对齐报告JSON读取 missing_dna 列表")
    args = parser.parse_args()

    files: List[str] = list(args.files)
    if args.from_report:
        files.extend(files_from_report(args.from_report))
    if not files and not sys.stdin.isatty():
        files.extend(line.strip() for line in sys.stdin if line.strip())

    if not files:
        print("没有待处理文件。")
        return 0

    ok = skipped = failed = 0
    for f in files:
        msg = fix_dna(f)
        print(msg)
        if msg.startswith("✅"):
            ok += 1
        elif msg.startswith(("⏭️", "🟡")):
            skipped += 1
        else:
            failed += 1

    print(f"\n📊 补DNA总结: 成功 {ok} | 跳过 {skipped} | 失败 {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
