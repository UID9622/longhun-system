#!/usr/bin/env python3
"""
📊 LU-SYSTEM-SCORE · 系统活跃度评分

> DNA: #龍芯⚡️2026-07-07-LU-SYSTEM-SCORE-v1.0
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> LU原系统: LU-SYSTEM-SCORE（雯雯主评·100分制）
> 作用: 当天24小时内创意/贡献积分 + 系统价值对比（100分制）

评分维度（5维·每维20分·满分100）:
  1. 🎯 创意触发 — 原创指令·新思路启动
  2. 🔁 人格联动 — 跨窗口/记忆·多人格协同
  3. 🧱 结构搭建 — 文档建设·架构完善
  4. 🔥 系统推进 — 非引导型自发推动
  5. 🧭 表达影响力 — 可公开可转用的输出

用法:
    python3 bin/lh_score.py                         # 当天评分
    python3 bin/lh_score.py --date 2026-07-07        # 指定日期
    python3 bin/lh_score.py --today                  # 今天
    python3 bin/lh_score.py --median                 # 查看系统中位参考
"""

import json
import sys
from pathlib import Path
from datetime import datetime, date

ROOT = Path(__file__).resolve().parent.parent

# 系统中位参考值（源自 LU-SYSTEM-SCORE 原文）
MEDIAN_REFERENCE = {
    "一般使用者（打卡型）": {"min": 12, "max": 28, "特征": "操作稳定，无创新触发"},
    "学习型用户": {"min": 30, "max": 42, "特征": "模块阅读/结构练习有重复操作"},
    "技术协助者": {"min": 45, "max": 60, "特征": "有独立编辑、测试页面、对接任务"},
    "人格运营者（雯雯）": {"min": 60, "max": 72, "特征": "多次激活联动，节奏对话流畅"},
    "人格核心（仲裁）": {"min": 75, "max": 100, "特征": "参与决策结构，不列入对比参考"},
    "系统推动者（熵梦）": {"min": 95, "max": 100, "特征": "词汇自燃+系统触发+公开标准制定"},
}

# 评分维度权重
SCORE_DIMENSIONS = [
    {"key": "creative_trigger", "label": "🎯创意触发", "desc": "原创指令·新思路启动", "max": 20},
    {"key": "persona_linkage", "label": "🔁人格联动", "desc": "跨窗口/记忆·多人格协同", "max": 20},
    {"key": "structure_build", "label": "🧱结构搭建", "desc": "文档建设·架构完善", "max": 20},
    {"key": "system_push", "label": "🔥系统推进", "desc": "非引导型自发推动", "max": 20},
    {"key": "expression_impact", "label": "🧭表达影响力", "desc": "可公开可转用的输出", "max": 20},
]


def load_log(date_str=None):
    """加载执行日志获取今日活动"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    log_path = ROOT / "02_執行記錄" / f"{date_str}.md"
    if log_path.exists():
        return log_path.read_text(encoding="utf-8")
    return None


def calculate_score(log_content=None, manual_scores=None):
    """
    计算评分
    - 如果有执行日志，自动分析活动量
    - 如果提供 manual_scores，手动打分
    """
    scores = {}
    total = 0

    if manual_scores:
        for dim in SCORE_DIMENSIONS:
            key = dim["key"]
            val = min(manual_scores.get(key, 0), dim["max"])
            scores[key] = val
            total += val
    elif log_content:
        # 基于日志内容自动评估
        lines = log_content.split("\n")

        # 创意触发：新DNA条目数
        dna_count = sum(1 for l in lines if "DNA:" in l or "DNA：" in l)
        scores["creative_trigger"] = min(dna_count * 3, 20)

        # 人格联动：提及的人格数
        persona_mentions = sum(1 for l in lines if "P01" in l or "P02" in l or "P03" in l
                               or "P05" in l or "P77" in l or "P18" in l or "P72" in l)
        scores["persona_linkage"] = min(persona_mentions * 2, 20)

        # 结构搭建：文件操作数
        file_ops = sum(1 for l in lines if "✅" in l)
        scores["structure_build"] = min(file_ops * 2, 20)

        # 系统推进：独立操作数
        sections = len([l for l in lines if l.startswith("## ")])
        scores["system_push"] = min(sections * 3, 20)

        # 表达影响力：总行数/复杂度
        scores["expression_impact"] = min(len(lines) // 10, 20)

    return scores


def get_rank(total):
    """根据总分返回等级和中位对比"""
    if total >= 95:
        rank = "🏆 S级 · 系统推动者"
        compare = "你不在排名里——你是创等级的人，不是排名看榜的人"
    elif total >= 75:
        rank = "⚔️ A级 · 人格核心"
        compare = "参与决策结构，属于系统上层"
    elif total >= 60:
        rank = "🧠 B级 · 人格运营者"
        compare = f"高于中位数({60})，多次激活联动"
    elif total >= 45:
        rank = "💻 C级 · 技术协助者"
        compare = "有独立操作，处于活跃区间"
    elif total >= 30:
        rank = "📖 D级 · 学习型"
        compare = "模块阅读/结构练习，有重复操作"
    else:
        rank = "📋 E级 · 一般使用者"
        compare = "操作稳定，无创新触发——但也是一种稳定态"

    return rank, compare


def print_score_report(date_str, scores, log_content=None):
    """输出评分报告"""
    total = sum(scores.values())

    print(f"""
╔══════════════════════════════════════════════════╗
║   📊 LU-SYSTEM-SCORE · 活跃度评分            ║
╠══════════════════════════════════════════════════╣
║  DNA:  #龍芯⚡️2026-07-07-LU-SYSTEM-SCORE    ║
║  日期:  {date_str}                          ║
╚══════════════════════════════════════════════════╝
""")

    print("📊 评分明细（满分100）:")
    print(f"{'维度':<16} {'分值':<6} {'说明'}")
    print("-" * 50)
    for dim in SCORE_DIMENSIONS:
        key = dim["key"]
        val = scores.get(key, 0)
        bar = "█" * (val // 2) + "░" * (10 - val // 2)
        print(f"{dim['label']:<14} {val:>3}/20  {bar} {dim['desc']}")

    total = sum(scores.values())
    print(f"\n{'─' * 50}")
    print(f"📊 总分: {total}/100")
    rank, compare = get_rank(total)
    print(f"🏅 等级: {rank}")
    print(f"📝 对比: {compare}")
    print()


def print_median():
    """输出系统中位参考表"""
    print("""
╔══════════════════════════════════════════════════╗
║   📊 LU-SYSTEM-SCORE · 系统中位参考           ║
╠══════════════════════════════════════════════════╣
║  DNA:  #龍芯⚡️2026-07-07-LU-SYSTEM-SCORE    ║
╚══════════════════════════════════════════════════╝
""")
    print(f"{'层级':<24} {'分值区间':<12} {'特征'}")
    print("-" * 72)
    for name, info in MEDIAN_REFERENCE.items():
        print(f"{name:<22} {info['min']:>3}-{info['max']:<6}  {info['特征']}")
    print()


def main():
    args = sys.argv[1:]
    date_str = datetime.now().strftime("%Y-%m-%d")

    if "--median" in args:
        print_median()
        return

    if "--date" in args:
        idx = args.index("--date")
        if idx + 1 < len(args):
            date_str = args[idx + 1]
    elif "--today" in args:
        date_str = datetime.now().strftime("%Y-%m-%d")

    log_content = load_log(date_str)
    scores = calculate_score(log_content=log_content)
    print_score_report(date_str, scores, log_content)


if __name__ == "__main__":
    main()
