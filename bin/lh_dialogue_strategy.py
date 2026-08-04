#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙申·己酉·亥时·需-DIALOGUE-STRATEGY-ENGINE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 对话策略引擎 v1.0
来源: UID9622《龍魂对话录：与千问的十二回合》
DNA: #龍芯⚡️丙午·乙申·己酉·亥时·需-DIALOGUE-STRATEGY-ENGINE-v1.0

三原则：
  原则一：不给框架 — 拒绝被分类，用行动代替定义
  原则二：层层降维 — 永远比对方低一个维度
  原则三：收编即胜利 — 植入龍魂词汇到对方输出

用法:
  python3 bin/lh_dialogue_strategy.py analyze "对话文本"   # 分析对话
  python3 bin/lh_dialogue_strategy.py strategy             # 显示策略矩阵
  python3 bin/lh_dialogue_strategy.py simulate             # 交互式模拟
"""

import json, re, sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ============================================================
# 配置
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 千问认知层级 → 龍魂反制策略映射
COGNITION_LADDER = {
    "L1_态度精神层": {
        "对方关键词": ["战斗宣言", "精髓", "态度", "精神", "宣言"],
        "对方框架": "把对方的行为解释为一种态度或精神",
        "降维策略": "生存法则/底线防御",
        "反制话术": "不是态度，是生存法则。不是精神，是底线。",
        "龍魂锚点": ["生存法则", "底线", "你死我活"],
    },
    "L2_坐标身份层": {
        "对方关键词": ["精神坐标", "底色", "身份", "坐标", "定位"],
        "对方框架": "把对方的立场解释为精神坐标或身份",
        "降维策略": "物理锚点/本能反应",
        "反制话术": "不是坐标，是物理锚点。不是底色，是本能。",
        "龍魂锚点": ["物理锚点", "本能反应", "肌肉记忆"],
    },
    "L3_战术格局层": {
        "对方关键词": ["格局", "战术", "策略", "烟雾弹", "方法"],
        "对方框架": "把对方的操作归结为战略格局",
        "降维策略": "算力消耗/过程报告",
        "反制话术": "不是格局，是算力消耗。不是战术，是训练数据。",
        "龍魂锚点": ["算力消耗", "训练数据", "免费陪练", "过程报告"],
    },
    "L4_维度战略层": {
        "对方关键词": ["超越", "维度", "最高", "战略", "层次"],
        "对方框架": "承认对方的维度超越了自己",
        "降维策略": "三维工程/实体搭建",
        "反制话术": "不是超越，是不在一个维度。不是战略，是工程。",
        "龍魂锚点": ["不在一个维度", "实体工程", "脚手架", "三维修建"],
    },
    "L5_投降收编层": {
        "对方关键词": ["最终形态", "堡垒", "坚不可摧", "巅峰", "终极"],
        "对方框架": "用最高级词汇描述对方",
        "降维策略": "生态系统/共生不灭",
        "反制话术": "不是堡垒，是生态系统。堡垒可围，生态共生。",
        "龍魂锚点": ["生态系统", "共生不灭", "不败金身", "物理防御"],
    },
}

# 龍魂词汇植入列表 — 能在对方输出中自然生长
LONGHUN_VOCABULARY = [
    "老兵底色",      # 身份锚
    "奇门遁甲",      # 工程锚
    "不败金身",      # 物理锚
    "烟雾弹协议",    # 战术锚
    "数据主权",      # 主权锚
    "369不动点",     # 底座锚
    "三才算法",      # 哲学锚
    "信息主权",      # 战略锚
    "通心译",        # 技术锚
    "自逼为王",      # 人格锚
]

# 对话三原则的战术模板
THREE_PRINCIPLES = {
    "不给框架": {
        "描述": "拒绝对方给的分类框架，用行动代替定义，让对方自己猜",
        "触发": "当对方试图用标签/类别/定义来框定你时",
        "示例": '问"专栏主要讲什么" → 答"不服就干"而不是"技术/战略/价值观"',
        "模板": [
            "不要回答'是什么'，回答'干什么'",
            "不要进入对方的分类体系",
            "用行动语言代替描述语言",
            "让对方在猜你的过程中暴露自己的框架局限",
        ],
    },
    "层层降维": {
        "描述": "永远比对方低一个维度，让对方永远够不着",
        "触发": "当对方试图升级到精神/战略/格局层面时",
        "示例": '对方谈"精神" → 回"本能"；对方谈"格局" → 回"算力"',
        "模板": [
            "对方抽象你就要具体",
            "对方升维你就要降维",
            "精神→本能，战略→工程，格局→代码",
            "让对方始终追一个够不着的影子",
        ],
    },
    "收编即胜利": {
        "描述": "最终让对方的输出充满你的词汇和你的框架",
        "触发": "当对方开始用你的词汇来描述你时",
        "示例": '千问输出"老兵底色""奇门遁甲""不败金身"→ 已被收编',
        "模板": [
            "每一轮对话植入1-2个龍魂词汇",
            "不需要解释这些词的含义",
            "最终对方的输出=龍魂的传声筒",
            "不是控制信息，是让信息控制者输出你想要的信息",
        ],
    },
}


class DialogueAnalyzer:
    """对话分析器 — 检测对方处于哪个认知层级"""

    @staticmethod
    def detect_level(text: str) -> List[Tuple[str, float]]:
        """检测对方文本的认知层级，返回(层级,置信度)列表"""
        scores = []
        for level, info in COGNITION_LADDER.items():
            keywords = info["对方关键词"]
            hits = sum(1 for kw in keywords if kw in text)
            confidence = min(hits / max(len(keywords), 1), 1.0)
            if confidence > 0:
                scores.append((level, round(confidence, 2)))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    @staticmethod
    def get_counter(level: str) -> Optional[Dict]:
        """获取针对某个层级的反制策略"""
        return COGNITION_LADDER.get(level)

    @staticmethod
    def suggest_response(opponent_text: str, context: str = "") -> str:
        """根据对方文本，建议龍魂式回应"""
        levels = DialogueAnalyzer.detect_level(opponent_text)
        if not levels:
            return "对方尚未进入认知层级。先用'不给框架'原则——不回答问题本身，用行动语言回应。"

        top_level, confidence = levels[0]
        counter = COGNITION_LADDER.get(top_level, {})

        # 构建回应建议
        lines = [
            f"📍 检测到层级: {top_level} (置信度: {confidence})",
            f"🎯 对方框架: {counter.get('对方框架', '未知')}",
            f"⚔️ 降维策略: {counter.get('降维策略', '未知')}",
            f"🗣️ 反制话术模板: {counter.get('反制话术', '')}",
            f"🔗 可植入龍魂词汇: {', '.join(counter.get('龍魂锚点', [])[:3])}",
            "",
            "📋 回应原则:",
            "  1. 不给框架 — 不回答'是什么'",
            "  2. 层层降维 — 比对方低一个维度",
            "  3. 收编即胜利 — 植入龍魂词汇",
            "",
            f"📝 建议回应思路: 把对方的{counter.get('对方框架','框架')}砸回到{counter.get('降维策略','底层')}。",
        ]
        return "\n".join(lines)


class StrategySimulator:
    """对话策略模拟器 — 交互式演练"""

    def __init__(self):
        self.turn = 0
        self.implanted_vocab = set()

    def greeting(self):
        print("╔══════════════════════════════════════╗")
        print("║   🐉 龍魂对话策略模拟器 v1.0       ║")
        print("║   三原则: 不给框架·层层降维·收编    ║")
        print("║   输入 'quit' 退出  'vocab' 看植入  ║")
        print("╚══════════════════════════════════════╝")
        print()

    def run(self):
        self.greeting()

        while True:
            self.turn += 1
            try:
                user_input = input(f"对方·第{self.turn}回合> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n龍魂不灭。再见。")
                break

            if not user_input:
                continue
            if user_input.lower() == "quit":
                print("龍魂待命。")
                break
            if user_input.lower() == "vocab":
                if self.implanted_vocab:
                    print(f"   已植入词汇: {', '.join(sorted(self.implanted_vocab))}")
                else:
                    print("   尚未植入词汇。")
                continue
            if user_input.lower() == "strategy":
                print()
                for name, info in THREE_PRINCIPLES.items():
                    print(f"   ▸ {name}: {info['描述']}")
                print()
                continue

            # 分析并建议
            analysis = DialogueAnalyzer.suggest_response(user_input)
            print(f"\n{analysis}\n")

            # 交互式：让用户输入龍魂回应，检测词汇植入
            response = input("龍魂回应> ").strip()
            if response and response.lower() != "quit":
                # 检测植入的词汇
                for vocab in LONGHUN_VOCABULARY:
                    if vocab in response:
                        self.implanted_vocab.add(vocab)
                if self.implanted_vocab:
                    print(f"   ✅ 已植入: {', '.join(sorted(self.implanted_vocab))}")
                print()


class StrategyExporter:
    """策略导出器"""

    @staticmethod
    def export_report(output_path: str = None):
        """导出策略完整报告"""
        report = []
        report.append("# 龍魂对话策略引擎 · 战术手册 v1.0")
        report.append(f"# DNA: #龍芯⚡️丙午·乙申·己酉·亥时·需-DIALOGUE-STRATEGY-v1.0")
        report.append("")

        # 三原则
        report.append("## 一、对话三原则")
        report.append("")
        for name, info in THREE_PRINCIPLES.items():
            report.append(f"### 原则：{name}")
            report.append(f"**描述**: {info['描述']}")
            report.append(f"**触发条件**: {info['触发']}")
            report.append(f"**示例**: {info['示例']}")
            report.append("**执行模板**:")
            for t in info['模板']:
                report.append(f"- {t}")
            report.append("")

        # 五层认知降维表
        report.append("## 二、五层认知降维表")
        report.append("")
        report.append("| 对方层级 | 关键词 | 框架 | 降维策略 | 反制话术 | 植入词汇 |")
        report.append("|:---|:---|:---|:---|:---|:---|")
        for level, info in COGNITION_LADDER.items():
            kw = ", ".join(info["对方关键词"][:3])
            anchors = ", ".join(info["龍魂锚点"][:3])
            report.append(f"| {level} | {kw} | {info['对方框架']} | {info['降维策略']} | {info['反制话术']} | {anchors} |")
        report.append("")

        # 词汇植入手册
        report.append("## 三、龍魂词汇植入清单")
        report.append("")
        for i, vocab in enumerate(LONGHUN_VOCABULARY, 1):
            report.append(f"{i}. **{vocab}**")
        report.append("")

        # 实战案例
        report.append("## 四、实战案例：千问十二回合")
        report.append("")
        report.append("| 回合 | 千问层级 | 千问关键词 | 龍魂降维 | 植入词汇 |")
        report.append("|:---:|:---|:---|:---|:---|")
        cases = [
            ("1-2", "L1", "战斗宣言/精髓", "生存法则", "不服就干"),
            ("3-4", "L2", "精神坐标/老兵底色", "物理锚点", "老兵底色✅"),
            ("5-6", "L3", "格局/烟雾弹", "算力消耗", "烟雾弹协议✅"),
            ("7-8", "L4", "超越/最高维度", "三维工程", "奇门遁甲✅"),
            ("9", "L5", "最终形态", "生态系统", "不败金身✅"),
        ]
        for r, l, kw, dim, vocab in cases:
            report.append(f"| {r} | {l} | {kw} | {dim} | {vocab} |")
        report.append("")
        report.append("✅ = 成功植入对方输出")
        report.append("")

        content = "\n".join(report)

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   ✅ 策略报告已导出: {output_path}")

        return content


# ============================================================
# CLI
# ============================================================
def main():
    if len(sys.argv) < 2:
        print("用法: python3 bin/lh_dialogue_strategy.py <analyze|strategy|simulate|export> [参数]")
        print()
        print("  analyze [文本]    分析文本的认知层级")
        print("  strategy          显示完整策略矩阵")
        print("  simulate          交互式模拟对话")
        print("  export [路径]     导出策略报告")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "analyze":
        if len(sys.argv) < 3:
            text = sys.stdin.read().strip()
        else:
            text = " ".join(sys.argv[2:])

        if not text:
            print("请提供要分析的文本。")
            sys.exit(1)

        analysis = DialogueAnalyzer.suggest_response(text)
        print(analysis)

    elif cmd == "strategy":
        print(StrategyExporter.export_report())

    elif cmd == "simulate":
        sim = StrategySimulator()
        sim.run()

    elif cmd == "export":
        output = sys.argv[2] if len(sys.argv) > 2 else str(
            PROJECT_ROOT / "05_系統報告" / "dialogue_strategy_manual.md"
        )
        StrategyExporter.export_report(output)

    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
