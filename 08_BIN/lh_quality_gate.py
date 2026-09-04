#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-QUALITY-GATE-CLI-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
"""🐉 龍魂 · 质量门禁 CLI: python3 08_BIN/lh_quality_gate.py --check"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from factory.quality_gate import QualityGate  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 质量门禁 CLI")
    parser.add_argument("--check", metavar="REPORT_JSON", nargs="?",
                        const="", help="对测试报告执行门禁检查（缺省=规则预览）")
    args = parser.parse_args()

    gate = QualityGate()

    if args.check is None:
        print("🚧 质量门禁规则:")
        for r in gate.rules:
            print(f"  - {r.name} ({r.condition}) 阈值={r.threshold} 级别={r.severity}")
        return

    # --check 带报告路径
    report_path = Path(args.check) if args.check else None
    if report_path and report_path.exists():
        with open(report_path, encoding="utf-8") as f:
            report = json.load(f)
    else:
        # 用最近一份报告
        reports_dir = Path.home() / ".longhun" / "factory" / "reports"
        if reports_dir.exists():
            files = sorted(reports_dir.glob("test_report_*.json"), reverse=True)
            if files:
                with open(files[0], encoding="utf-8") as f:
                    report = json.load(f)
            else:
                print("❌ 无测试报告可检查")
                return
        else:
            print("❌ 无测试报告可检查")
            return

    result = gate.evaluate(report)
    print(f"🚧 质量门禁: {result['overall']}")
    for r in result['results']:
        print(f"  - {r['rule']}: {r['status']} (actual={r['actual']:.2f}, threshold={r['threshold']})")
    print(f"  DNA: {result['dna']}")


if __name__ == "__main__":
    main()
