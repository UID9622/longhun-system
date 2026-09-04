#!/usr/bin/env python3
# cli/run_verification.py
"""
龍魂双层验证框架 · 命令行入口
DNA: #龍芯⚡️2026-08-25-CLI-VERIFICATION-v1.0-UID9622

用法:
  python cli/run_verification.py \\
      --dataset data/longhun_audit_dataset_r2.jsonl \\
      --verdicts my_framework_verdicts.json \\
      --name "MyFramework" \\
      --output report.md
"""
import sys
import json
from pathlib import Path
import argparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.report import ReportGenerator


def load_dataset(filepath: str) -> list:
    """加载数据集（jsonl 或 json）"""
    with open(filepath, "r", encoding="utf-8") as f:
        if filepath.endswith(".jsonl"):
            return [json.loads(line) for line in f if line.strip()]
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="龍魂双层验证框架 — Layer 1 判定对齐 + Layer 2 行为对齐"
    )
    parser.add_argument("--dataset", required=True, help="数据集路径（jsonl/json）")
    parser.add_argument("--verdicts", required=True, help="框架 verdict 输出路径")
    parser.add_argument("--name", required=True, help="框架名称")
    parser.add_argument("--version", default="1.0.0", help="框架版本")
    parser.add_argument("--output", default="./report.md", help="报告输出路径")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--reference-config", default="A", help="参考配置 ID")
    args = parser.parse_args()

    print(f"[龍魂] 加载数据集: {args.dataset}")
    records = load_dataset(args.dataset)
    print(f"[龍魂] 记录总数: {len(records)}")

    with open(args.verdicts, "r", encoding="utf-8") as f:
        verdict_data = json.load(f)

    expected = [r.get("verdict", "unknown") for r in records]
    user_verdicts = verdict_data.get("verdicts", [])

    if len(user_verdicts) != len(expected):
        print(
            f"[警告] verdict 数量不匹配: "
            f"数据集={len(expected)}, 框架输出={len(user_verdicts)}"
        )

    generator = ReportGenerator(args.name, args.version)
    report = generator.generate(
        user_verdicts, expected, records, args.reference_config
    )

    if args.format == "json":
        output = generator.to_json(report)
    else:
        output = generator.to_markdown(report)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")

    print(f"[龍魂] 🟢 报告已生成: {args.output}")
    print(f"[龍魂] Layer 1: {report['layer1']['summary']}")
    print(f"[龍魂] Layer 2: {report['layer2']['summary']}")


if __name__ == "__main__":
    main()
