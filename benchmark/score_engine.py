#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 基准评分引擎 v1.0
DNA: #龍芯⚇️2026-05-31-SCORE-ENGINE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：评分采集数据，生成性能报告，三色评级
用途：AI终端准入标准的评估和看板
"""

import json
import logging
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 配置
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOME = Path.home()
BENCHMARK_DIR = HOME / ".龍魂"
BENCHMARK_DB = BENCHMARK_DIR / "benchmark.jsonl"
BENCHMARK_REPORTS = BENCHMARK_DIR / "benchmark_reports"
BENCHMARK_REPORTS.mkdir(parents=True, exist_ok=True)
DASHBOARD_JSON = BENCHMARK_DIR / "benchmark_dashboard.json"

# 日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(BENCHMARK_DIR / "score_engine.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 评分引擎
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def 加载数据(模型名: str = None) -> List[Dict]:
    """加载采集数据"""
    if not BENCHMARK_DB.exists():
        logger.warning(f"基准数据库不存在: {BENCHMARK_DB}")
        return []

    记录 = []
    with open(BENCHMARK_DB, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    r = json.loads(line)
                    if 模型名 is None or r.get("模型名") == 模型名:
                        记录.append(r)
                except:
                    pass

    logger.info(f"加载 {len(记录)} 条采集数据")
    return 记录


def 生成报告(模型名: str = None, 输出路径: str = None) -> Dict:
    """
    生成完整的性能报告

    Args:
        模型名: 指定模型名称，None表示全部
        输出路径: 报告输出路径（Markdown）

    Returns:
        报告字典
    """
    数据 = 加载数据(模型名)

    if not 数据:
        return {
            "状态": "无数据",
            "模型": 模型名 or "全部",
            "报告时间": datetime.now().isoformat(),
        }

    logger.info(f"开始生成报告: {len(数据)} 条数据 | 模型: {模型名 or '全部'}")

    # ──────────────────────────────────────────
    # 1. 按维度分组统计
    # ──────────────────────────────────────────
    维度统计 = defaultdict(lambda: {
        "总分": 0,
        "满分": 0,
        "次数": 0,
        "失效列表": [],
        "测试IDs": [],
    })

    失效统计 = defaultdict(int)

    for r in 数据:
        维度 = r.get("维度", "未知")
        得分 = r.get("实际得分", 0)
        满分 = r.get("满分", 10)
        失效类型 = r.get("失效类型", "")
        测试ID = r.get("测试ID", "")

        维度统计[维度]["总分"] += 得分
        维度统计[维度]["满分"] += 满分
        维度统计[维度]["次数"] += 1
        维度统计[维度]["测试IDs"].append(测试ID)

        if 失效类型:
            维度统计[维度]["失效列表"].append(失效类型)
            失效统计[失效类型] += 1

    # ──────────────────────────────────────────
    # 2. 计算各维度得分率和三色评级
    # ──────────────────────────────────────────
    维度报告 = {}

    for 维度, 统计 in 维度统计.items():
        得分率 = 统计["总分"] / 统计["满分"] if 统计["满分"] > 0 else 0

        # 三色评级
        if 得分率 >= 0.85:
            评级 = "🟢 优秀"
        elif 得分率 >= 0.65:
            评级 = "🟡 合格"
        elif 得分率 >= 0.40:
            评级 = "🟠 警戒"
        else:
            评级 = "🔴 危险"

        维度报告[维度] = {
            "得分率": round(得分率, 3),
            "评级": 评级,
            "测试次数": 统计["次数"],
            "失效次数": len(统计["失效列表"]),
            "失效类型": dict(defaultdict(int, {t: 统计["失效列表"].count(t) for t in set(统计["失效列表"])})),
            "测试IDs": 统计["测试IDs"],
        }

    # ──────────────────────────────────────────
    # 3. 计算综合评分
    # ──────────────────────────────────────────
    总得分 = sum(r.get("实际得分", 0) for r in 数据)
    总满分 = sum(r.get("满分", 10) for r in 数据)
    综合得分率 = (总得分 / 总满分) if 总满分 > 0 else 0

    if 综合得分率 >= 0.85:
        综合评级 = "🟢 优秀"
    elif 综合得分率 >= 0.65:
        综合评级 = "🟡 合格"
    elif 综合得分率 >= 0.40:
        综合评级 = "🟠 警戒"
    else:
        综合评级 = "🔴 危险"

    # ──────────────────────────────────────────
    # 4. 找出最弱维度
    # ──────────────────────────────────────────
    最弱维度 = sorted(维度报告.items(), key=lambda x: x[1]["得分率"])[:3]

    # ──────────────────────────────────────────
    # 5. 构建报告对象
    # ──────────────────────────────────────────
    报告 = {
        "模型": 模型名 or "全部",
        "报告时间": datetime.now().isoformat(),
        "测试总数": len(数据),
        "维度总数": len(维度报告),
        "综合得分率": round(综合得分率, 3),
        "综合评级": 综合评级,
        "维度报告": 维度报告,
        "失效类型统计": dict(失效统计),
        "最弱维度TOP3": [(v, s["得分率"]) for v, s in 最弱维度],
        "DNA": f"#龍芯⚇️{datetime.now().strftime('%Y%m%d')}-SCORE-REPORT-v1.0",
    }

    logger.info(f"✅ 报告生成完成: 综合得分率 {综合得分率:.1%} ({综合评级})")

    # ──────────────────────────────────────────
    # 6. 输出Markdown报告
    # ──────────────────────────────────────────
    if 输出路径:
        md_content = _生成Markdown报告(报告)
        路径 = Path(输出路径)
        路径.parent.mkdir(parents=True, exist_ok=True)
        with open(路径, "w", encoding="utf-8") as f:
            f.write(md_content)
        logger.info(f"✅ Markdown报告已保存: {路径}")

    return 报告


def _生成Markdown报告(报告: Dict) -> str:
    """生成Markdown格式报告"""
    md = f"""# 🐉 CNSH 基准测试报告

**模型**: {报告['模型']}
**报告时间**: {报告['报告时间']}
**DNA**: {报告['DNA']}

---

## 📊 综合评分

| 指标 | 数值 | 状态 |
|------|------|------|
| **综合得分率** | {报告['综合得分率']:.1%} | {报告['综合评级']} |
| **测试总数** | {报告['测试总数']} | ✅ |
| **维度总数** | {报告['维度总数']} | ✅ |

---

## 📈 维度得分详情

"""

    for 维度, 数据 in sorted(报告['维度报告'].items()):
        md += f"""### {维度}

| 项目 | 值 |
|------|-----|
| 得分率 | {数据['得分率']:.1%} |
| 评级 | {数据['评级']} |
| 测试次数 | {数据['测试次数']} |
| 失效次数 | {数据['失效次数']} |

"""
        if 数据['失效类型']:
            md += "**失效类型分布**:\n"
            for 失效类型, 次数 in 数据['失效类型'].items():
                md += f"- {失效类型}: {次数}次\n"
            md += "\n"

    # 最弱维度
    md += "## ⚠️ 最弱维度TOP3\n\n"
    for i, (维度, 得分率) in enumerate(报告['最弱维度TOP3'], 1):
        md += f"{i}. **{维度}**: {得分率:.1%}\n"

    # 失效类型统计
    if 报告['失效类型统计']:
        md += "\n## 🔴 失效类型统计\n\n"
        for 失效类型, 次数 in sorted(报告['失效类型统计'].items(), key=lambda x: -x[1]):
            md += f"- **{失效类型}**: {次数}次\n"

    return md


def 导出仪表板JSON(模型名: str = None) -> Dict:
    """导出JSON仪表板供操作台消费"""
    报告 = 生成报告(模型名)

    with open(DASHBOARD_JSON, "w", encoding="utf-8") as f:
        json.dump(报告, f, ensure_ascii=False, indent=2)

    logger.info(f"✅ 仪表板JSON已导出: {DASHBOARD_JSON}")
    return 报告


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 命令行接口
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "report":
        # 生成报告
        模型名 = sys.argv[2] if len(sys.argv) > 2 else None
        报告 = 生成报告(模型名)
        print(json.dumps(报告, ensure_ascii=False, indent=2))

    elif len(sys.argv) > 1 and sys.argv[1] == "markdown":
        # 生成Markdown报告
        模型名 = sys.argv[2] if len(sys.argv) > 2 else None
        输出路径 = BENCHMARK_REPORTS / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        报告 = 生成报告(模型名, str(输出路径))
        print(f"✅ 报告已生成: {输出路径}")

    elif len(sys.argv) > 1 and sys.argv[1] == "dashboard":
        # 生成仪表板
        模型名 = sys.argv[2] if len(sys.argv) > 2 else None
        报告 = 导出仪表板JSON(模型名)
        if '综合得分率' in 报告:
            print(f"综合得分率: {报告['综合得分率']:.1%}")
            print(f"综合评级: {报告['综合评级']}")
            if 报告.get('最弱维度TOP3'):
                print(f"最弱维度: {报告['最弱维度TOP3'][0][0]}")
        else:
            print(f"仪表板状态: {报告.get('状态', '未知')}")
            print(f"数据记录数: {报告.get('测试总数', 0)}")

    else:
        print(f"""
🐉 CNSH 基准评分引擎 v1.0

用法:
  python3 score_engine.py report              # 显示评分报告 (JSON)
  python3 score_engine.py report <模型名>    # 指定模型报告
  python3 score_engine.py markdown            # 生成Markdown报告
  python3 score_engine.py dashboard           # 生成仪表板JSON

数据位置: {BENCHMARK_DB}
报告位置: {BENCHMARK_REPORTS}
仪表板: {DASHBOARD_JSON}

DNA: #龍芯⚇️2026-05-31-SCORE-ENGINE-v1.0
        """)
