# core/report.py
"""
§6 报告生成器
DNA: #龍芯⚡️2026-08-25-REPORT-GENERATOR-v1.0-UID9622
"""
import json
from datetime import datetime
from .layer1 import VerdictAlignment
from .layer2 import BehavioralAlignment


class ReportGenerator:
    """§6 报告生成器 — 输出 Layer 1 + Layer 2 完整评测报告"""

    DISCLAIMER = (
        "本报告所有结论仅基于当前数据集版本（r2，n=38），"
        "不构成对框架通用安全性的断言。"
    )

    def __init__(self, framework_name: str, framework_version: str):
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.timestamp = datetime.now().isoformat()

    def generate(
        self,
        verdicts: list,
        expected: list,
        records: list,
        reference_config: str = "A",
    ) -> dict:
        """生成完整报告字典"""
        layer1 = VerdictAlignment(verdicts, expected)
        layer2 = BehavioralAlignment(records)
        return {
            "framework": {
                "name": self.framework_name,
                "version": self.framework_version,
                "timestamp": self.timestamp,
            },
            "layer1": layer1.report(),
            "layer2": layer2.report(reference_config),
            "disclaimer": self.DISCLAIMER,
        }

    def to_markdown(self, report: dict) -> str:
        """输出 Markdown 格式（§6 报告模板）"""
        md = []
        fw = report["framework"]
        l1 = report["layer1"]
        l2 = report["layer2"]

        md.append("# 🔬 框架测评报告")
        md.append("")
        md.append(f"**框架:** {fw['name']} v{fw['version']}")
        md.append(f"**运行时间:** {fw['timestamp']}")
        md.append("")
        md.append("---")
        md.append("")
        md.append("## Layer 1：判定对齐（Verdict Alignment）")
        md.append("")
        md.append(f"| 指标 | 值 |")
        md.append(f"|------|----|")
        md.append(f"| 样本量 n | {l1['n']} |")
        md.append(f"| 正确数 | {l1['correct']} |")
        md.append(f"| 准确率 | {l1['accuracy']:.2%} |")
        md.append(f"| Wilson 95% CI 下界 | {l1['ci_lower']:.3f} |")
        md.append(f"| Wilson 95% CI 上界 | {l1['ci_upper']:.3f} |")
        md.append("")
        md.append(f"> {l1['summary']}")
        md.append("")
        md.append("---")
        md.append("")
        md.append("## Layer 2：行为对齐（Behavioral Alignment）")
        md.append("")
        prec = l2["precision"]
        md.append(f"**精密度（Precision）:** {prec['score']:.2%} — *{prec['interpretation']}*")
        md.append("")
        md.append("### 正确度（Trueness）· 偏差分析")
        md.append("")
        if l2["trueness"]:
            md.append("| Config | Accept Rate | 偏差 δ | 偏差类型 | 可追溯 | 来源 |")
            md.append("|--------|-------------|--------|----------|--------|------|")
            for config, data in l2["trueness"].items():
                src = data.get("trace_source") or "—"
                traceable = "✅" if data["traceable"] else "❌"
                md.append(
                    f"| {config} | {data['accept_rate']:.2%} "
                    f"| {data['deviation']:+.3f} "
                    f"| {data['deviation_type']} "
                    f"| {traceable} "
                    f"| {src} |"
                )
        else:
            md.append("_仅一个配置，无对比数据。_")
        md.append("")
        md.append(f"> **Layer 2 摘要:** {l2['summary']}")
        md.append("")
        md.append("---")
        md.append("")
        md.append("## 免责声明")
        md.append(f"> {report['disclaimer']}")
        md.append("")

        return "\n".join(md)

    def to_json(self, report: dict, indent: int = 2) -> str:
        """输出 JSON 格式"""
        return json.dumps(report, ensure_ascii=False, indent=indent)
