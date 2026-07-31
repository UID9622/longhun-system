# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 训练数据报告生成器
把 JSON 质量报告转成 Markdown 可读报告，便于飞书推送或人工审阅。
DNA: #龍芯⚡️2026-06-30-LONGHUN-TRAINING-REPORT-v1.0
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
REPORT_DIR = HOME / "longhun-system" / "data" / "training" / "reports"


def main():
    日期 = datetime.now(timezone.utc).strftime("%Y%m%d")
    json路径 = REPORT_DIR / f"quality_report_{日期}.json"
    if not json路径.exists():
        print(f"🟡 今日无质量报告: {json路径}")
        sys.exit(0)

    报告 = json.loads(json路径.read_text(encoding="utf-8"))
    md路径 = REPORT_DIR / f"training_report_{日期}.md"

    md = f"""# 🐉 龍魂训练数据日报 · {报告['日期']}

**DNA**: `{报告['dna']}`
**生成时间**: {datetime.now(timezone.utc).isoformat()}

## 一、总体指标

| 指标 | 数值 |
|------|------|
| 总样本数 | {报告['总数']} |
| 平均得分 | {报告['平均得分']} |
| 最高分 | {报告['最高分']} |
| 最低分 | {报告['最低分']} |
| 错误率 | {报告['错误率']} |

## 二、等级分布

| 等级 | 数量 |
|------|------|
| 🟢 优质 | {报告['等级分布'].get('🟢', 0)} |
| 🟡 待优化 | {报告['等级分布'].get('🟡', 0)} |
| 🔴 不合格 | {报告['等级分布'].get('🔴', 0)} |

## 三、低质量样本 TOP

"""
    for item in 报告.get("低质量样本", []):
        md += f"- `{item['data_id']}` ({item['source']}) 得分 {item['score']}：{item['raw_preview']}...\n"

    md += f"""
## 四、下一步行动

- 错误率目标 < 0.1%，当前 {报告['错误率']}：{"✅ 达标" if 报告['错误率'] < 0.001 else "⚠️ 需优化"}
- 对 🔴 样本进行人工复核或删除
- 对 🟡 样本补充上下文或重新标注

---
*本报告由 龍魂训练数据流水线自动生成*
"""

    md路径.write_text(md, encoding="utf-8")
    print(f"🟢 Markdown 报告已生成: {md路径}")
    print(f"   DNA: {报告['dna']}")


if __name__ == "__main__":
    main()
