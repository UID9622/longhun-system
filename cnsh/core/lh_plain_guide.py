#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║      🐉 龍魂系统·大白话完全指南 v2.0（优化版）🐉               ║
║                                                                  ║
║     老大的复杂理论翻成人话                                     ║
║     让任何人都能看懂（模块化·交互·多格式输出）                 ║
║                                                                  ║
║  DNA:#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-LONGHUN-PLAIN-LANGUAGE-FILE1-v2.0          ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ║
║                                                                  ║
║  主权人: UID9622 · 龍芯北辰                                    ║
║  职责: 宝宝·翻译官·让人都能懂                                 ║
║  原则: 复杂的理论，简单的话                                    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

import json
from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


# ═══════════════════════════════════════════════════════════════
# 【核心数据结构】
# ═══════════════════════════════════════════════════════════════

class ContentType(str, Enum):
    """内容类型枚举"""
    CONCEPT = "concept"          # 核心概念
    ALGORITHM = "algorithm"      # 算法
    FAQ = "faq"                  # 常见问题
    PRINCIPLE = "principle"      # 底座原则
    WORKFLOW = "workflow"        # 工作流程
    COMPARISON = "comparison"    # 对比


@dataclass
class Explanation:
    """解释条目"""
    title: str
    content_type: ContentType
    plain_text: str              # 大白话版本
    key_points: List[str]        # 关键点
    analogy: Optional[str] = None  # 类比
    formula: Optional[str] = None  # 公式/代码
    tags: List[str] = None       # 标签

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


# ═══════════════════════════════════════════════════════════════
# 【核心概念库】模块化存储
# ═══════════════════════════════════════════════════════════════

CORE_EXPLANATIONS = {

    "不动点": Explanation(
        title="不动点 f(x)=x",
        content_type=ContentType.CONCEPT,
        plain_text="""
想象你有一个秘密身份。
不管外面发生什么，你的秘密身份永远不变。
这就是"不动点"。
""",
        analogy="就像你的DNA，永远是你",
        formula="f(x) = x  →  经过处理后还是原来的样子",
        key_points=[
            "身份不变性",
            "数据追溯源头",
            "无法窜改",
        ],
        tags=["L0", "基础概念", "身份"]
    ),

    "DNA": Explanation(
        title="DNA（身份码）",
        content_type=ContentType.CONCEPT,
        plain_text="""
就像你的身份证号，一个人一个号，永远不重复。

在龍魂系统里：
  • 你的ID号 + 时间 + 行为特征 = 你的DNA
  • 这个DNA永远跟着你
  • 任何数据都能反向找到"是谁做的"
""",
        analogy="像身份证号一样独一无二",
        formula="#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-ACTION-HASH-v1.0",
        key_points=[
            "唯一标识",
            "可追溯",
            "不可伪造",
        ],
        tags=["L0", "追溯", "身份"]
    ),

    "签章": Explanation(
        title="签章（Seal）",
        content_type=ContentType.CONCEPT,
        plain_text="""
就像古代的印章。

一个决策有签章，说明：
  ✓ 这个决策是真的
  ✓ 这个决策有数学支持（算法）
  ✓ 没有人能伪造
""",
        analogy="像合同上的公章一样不可伪造",
        formula="有算法 + 有验证 + 有DNA = 有签章",
        key_points=[
            "真实性证明",
            "不可伪造",
            "数学背书",
        ],
        tags=["安全", "验证", "信任"]
    ),

    "三色判定": Explanation(
        title="三色判定（Green/Yellow/Red）",
        content_type=ContentType.CONCEPT,
        plain_text="""
就像交通灯。

龍魂系统的判定：
  🟢 绿 (置信度 >= 85%) = 执行
  🟡 黄 (置信度 60-85%) = 需要人工审查
  🔴 红 (置信度 < 60%) = 禁止执行

不是"我觉得"，而是用数学算出来的。
""",
        analogy="交通灯：绿→执行，黄→审查，红→禁止",
        formula="置信度 = Σ(权重×证据) / 总权重",
        key_points=[
            "客观判定",
            "三个层级",
            "数学支持",
        ],
        tags=["判定", "三色", "风险"]
    ),
}


# ═══════════════════════════════════════════════════════════════
# 【7大算法库】
# ═══════════════════════════════════════════════════════════════

ALGORITHMS = {

    "权重算法": Explanation(
        title="1. 龍魂权重算法",
        content_type=ContentType.ALGORITHM,
        plain_text="""
当你要做个大决策，涉及很多人的利益。怎么权衡？

算法说：
  全球收益 - 群体损失 + 个体尊严

翻译：
  • 这个决策能给所有人带来什么好处？
  • 这个决策会伤害什么群体？
  • 这个决策有没有尊重个人？

核心：个体尊严权重是无穷大。
意思是你不能说"牺牲100个人换1000万块钱"。
""",
        formula="""
V = α·G - β·L + γ·D
其中 γ→∞（个人尊严权重无穷大）
""",
        key_points=[
            "多维度评估",
            "个人尊严无穷权重",
            "禁区明确",
        ],
        tags=["决策", "伦理", "权衡"]
    ),

    "治理框架": Explanation(
        title="2. CNSH-64治理框架",
        content_type=ContentType.ALGORITHM,
        plain_text="""
64卦（古代的一套推演系统）+ 5元素 + 数字根

组合出：64种治理状态

每种状态对应一个决策：
  状态A → 应该这样做
  状态B → 应该那样做

处理完状态后，系统自动给出：
  🟢 绿 = 这个决策很明确，执行
  🟡 黄 = 这个有争议，需要人看
  🔴 红 = 这个违反原则，不行

为什么用64？
  2^6 = 64，能覆盖所有的"是非判断"组合。
""",
        formula="状态 = 卦象 × 五行 × 数字根",
        key_points=[
            "古今结合",
            "64种状态",
            "自动红绿灯",
        ],
        tags=["治理", "64卦", "古代智慧"]
    ),

    "不变量": Explanation(
        title="3. 洛书369与决策不变量",
        content_type=ContentType.ALGORITHM,
        plain_text="""
洛书是个古代的魔方阵：

4 9 2
3 5 7
8 1 6

所有行、列、对角线加起来都等于15。

怎么用到决策上：
  • 不管怎么旋转（改变角度），总和还是15
  • 不管怎么翻转（反过来看），总和还是15
  • 这就是"不变量"

意义：
  有些东西是永恒的，改不了的。
  你的核心价值、身份、原则，就是这样的不变量。
""",
        formula="""
洛书幻方：
  行和 = 列和 = 对角和 = 15（不变）
  中宫 = 5（身份不动点）
""",
        key_points=[
            "永恒性",
            "旋转不变",
            "中宫不动",
        ],
        tags=["不变量", "洛书", "身份"]
    ),

    "审计算法": Explanation(
        title="4. 64卦审计算法",
        content_type=ContentType.ALGORITHM,
        plain_text="""
给你的系统打分，用8个维度：

✓ 文件完整吗？
✓ 数据健康吗？
✓ 安全吗？
✓ 来源清楚吗？
✓ 快吗？
✓ 规范吗？
✓ 代码好吗？
✓ 记录全吗？

每个打0-10分，加起来。
然后红绿灯判定。
""",
        formula="审计分 = Σ(维度评分) / 8，红绿灯映射",
        key_points=[
            "8个维度",
            "全面评估",
            "自动判定",
        ],
        tags=["审计", "评分", "质量"]
    ),

    "物理算法": Explanation(
        title="5. EUV物理算法",
        content_type=ContentType.ALGORITHM,
        plain_text="""
拿物理学的规律来做决策。

7个因子相乘：
  ID × 时间 × 规则 × 路径 × 词汇 × 风格 × 错误日志

每个因子都要合格（不能是0）。
缺一个，整个系统就是0。

为什么这样：
  就像一条链条，一个环坏了，整条链就断了。
""",
        formula="信心度 = F₁ × F₂ × F₃ × F₄ × F₅ × F₆ × F₇",
        key_points=[
            "7个因子",
            "零一律（缺一全零）",
            "链条模型",
        ],
        tags=["物理", "乘法", "严格"]
    ),

    "熔断系统": Explanation(
        title="6. 龍芯闭环熔断系统",
        content_type=ContentType.ALGORITHM,
        plain_text="""
一个自动的"暂停按钮"。

系统自己监控自己：
  • 故障30次？暂停。
  • 故障70次？强制停止。
  • 违反底座原则？永久关闭。

不需要人工干预。
就像汽车的安全系统。
""",
        formula="""
如果 故障次数 >= 30 → 软暂停
如果 故障次数 >= 70 → 硬停止
如果 违反底座原则 → 永久熔断
""",
        key_points=[
            "自动保护",
            "分级应对",
            "无需人介入",
        ],
        tags=["安全", "自动", "熔断"]
    ),

    "三才算法": Explanation(
        title="7. 三才算法（天地人）",
        content_type=ContentType.ALGORITHM,
        plain_text="""
一个系统要成功，需要三个层面协调：

天（规律层）
  = 遵守自然法则、数学规律

地（实现层）
  = 技术要能做到、代码要能跑

人（价值层）
  = 要对人有帮助、要尊重人的尊严

三个都有，才是好系统。
缺一个，就不完整。
""",
        formula="""
系统质量 = 天·规律 ∩ 地·实现 ∩ 人·价值
          （三个都要有）
""",
        key_points=[
            "天地人三层",
            "缺一不可",
            "平衡重要",
        ],
        tags=["三才", "平衡", "完整"]
    ),
}


# ═══════════════════════════════════════════════════════════════
# 【常见问题库】
# ═══════════════════════════════════════════════════════════════

FAQS = {
    "用途": Explanation(
        title="这套系统有什么用？",
        content_type=ContentType.FAQ,
        plain_text="""
用来做"有依据的决策"。

普通决策：我觉得应该这样做
龍魂决策：我用算法验证过，应该这样做

区别：
  普通：可能是对的，也可能是错的
  龍魂：如果有签章，就一定是对的
""",
        key_points=[
            "数据驱动",
            "有依据",
            "可信度高",
        ],
        tags=["使用场景", "价值"]
    ),

    "复杂性": Explanation(
        title="为什么要这么复杂？",
        content_type=ContentType.FAQ,
        plain_text="""
因为现实很复杂。

如果世界只有黑和白，很简单。
但现实有千种灰色。
所以需要一个能处理复杂性的系统。
""",
        key_points=[
            "现实复杂",
            "需要精细处理",
            "不能简化本质",
        ],
        tags=["设计哲学"]
    ),

    "验证": Explanation(
        title="我怎么知道算法是对的？",
        content_type=ContentType.FAQ,
        plain_text="""
有两个证明：

1. 数学证明
   • 公式来自论文
   • 论文经过审查

2. 实践证明
   • 老大用了8个多月
   • 跑过10万次推演
   • 结果都符合预期
""",
        key_points=[
            "论文支持",
            "10万次验证",
            "双重证明",
        ],
        tags=["可靠性", "验证"]
    ),

    "学习时间": Explanation(
        title="需要多久学会？",
        content_type=ContentType.FAQ,
        plain_text="""
这个文件就够了。

• 20分钟理解核心概念
• 30分钟看懂7个算法
• 1小时能用基本功能
• 1个月成为专家
""",
        key_points=[
            "20分钟入门",
            "1小时上手",
            "1月精通",
        ],
        tags=["学习成本"]
    ),
}


# ═══════════════════════════════════════════════════════════════
# 【底座原则库】
# ═══════════════════════════════════════════════════════════════

PRINCIPLES = {
    "人永远是1": Explanation(
        title="原则1：人永远是1",
        content_type=ContentType.PRINCIPLE,
        plain_text="""
人比数据重要。
你不能为了数据而伤害人。

违反例：
  "牺牲100个人换100万块钱" → ❌ 永久关闭

这是底线，不能妥协。
""",
        key_points=["人权优先", "不可妥协", "永久红线"],
        tags=["L0", "底座"]
    ),

    "不蒸馏": Explanation(
        title="原则2：不蒸馏",
        content_type=ContentType.PRINCIPLE,
        plain_text="""
保留完整信息，不能简化。

违反例：
  "我只记录结果，过程就删了" → ❌ 永久关闭

完整性是信任的基础。
""",
        key_points=["完整保留", "不删信息", "可追溯"],
        tags=["L0", "底座"]
    ),

    "不投机": Explanation(
        title="原则3：不投机",
        content_type=ContentType.PRINCIPLE,
        plain_text="""
长期稳定，不能走捷径。

违反例：
  "先达到目标再说" → ❌ 永久关闭

过程比结果重要。
""",
        key_points=["长期稳定", "不走捷径", "过程严谨"],
        tags=["L0", "底座"]
    ),

    "逻辑闭环": Explanation(
        title="原则4：逻辑闭环",
        content_type=ContentType.PRINCIPLE,
        plain_text="""
完整的链条，没有漏洞。

违反例：
  "有一步我跳过了" → ❌ 永久关闭

链条的强度取决于最薄弱的一环。
""",
        key_points=["完整链条", "无漏洞", "头尾相接"],
        tags=["L0", "底座"]
    ),
}


# ═══════════════════════════════════════════════════════════════
# 【主控类】
# ═══════════════════════════════════════════════════════════════

class PlainGuideSystem:
    """龍魂系统大白话指南·主控类"""

    def __init__(self):
        self.concepts = CORE_EXPLANATIONS
        self.algorithms = ALGORITHMS
        self.faqs = FAQS
        self.principles = PRINCIPLES
        self.all_items = {
            **self.concepts,
            **self.algorithms,
            **self.faqs,
            **self.principles,
        }

    def search(self, keyword: str) -> Dict[str, List[str]]:
        """搜索相关内容"""
        results = {"concepts": [], "algorithms": [], "faqs": [], "principles": []}
        keyword_lower = keyword.lower()

        for title, exp in self.concepts.items():
            if keyword_lower in title.lower() or any(keyword_lower in tag for tag in exp.tags):
                results["concepts"].append(title)

        for title, exp in self.algorithms.items():
            if keyword_lower in title.lower() or any(keyword_lower in tag for tag in exp.tags):
                results["algorithms"].append(title)

        for title, exp in self.faqs.items():
            if keyword_lower in title.lower() or any(keyword_lower in tag for tag in exp.tags):
                results["faqs"].append(title)

        for title, exp in self.principles.items():
            if keyword_lower in title.lower() or any(keyword_lower in tag for tag in exp.tags):
                results["principles"].append(title)

        return results

    def get_item(self, title: str) -> Optional[Explanation]:
        """获取单个条目"""
        return self.all_items.get(title)

    def format_as_text(self, exp: Explanation, verbose: bool = True) -> str:
        """格式化为纯文本"""
        output = []
        output.append(f"\n【{exp.title}】\n")

        if verbose and exp.analogy:
            output.append(f"[类比] {exp.analogy}\n")

        output.append(f"{exp.plain_text}")

        if verbose and exp.formula:
            output.append(f"\n[公式]\n{exp.formula}\n")

        if verbose and exp.key_points:
            output.append("\n[关键点]")
            for point in exp.key_points:
                output.append(f"  • {point}")
            output.append("")

        return "\n".join(output)

    def format_as_markdown(self, exp: Explanation) -> str:
        """格式化为Markdown"""
        output = []
        output.append(f"\n## {exp.title}\n")

        if exp.analogy:
            output.append(f"**类比：** {exp.analogy}\n")

        output.append(f"{exp.plain_text}\n")

        if exp.formula:
            output.append(f"```\n{exp.formula}\n```\n")

        if exp.key_points:
            output.append("**关键点：**")
            for point in exp.key_points:
                output.append(f"- {point}")
            output.append("")

        if exp.tags:
            output.append(f"**标签：** {', '.join(exp.tags)}\n")

        return "\n".join(output)

    def print_all(self, category: str = "all"):
        """打印所有内容"""
        print(self._get_header())

        if category in ["all", "concepts"]:
            print("\n【第一部分】核心概念翻译\n")
            for title, exp in self.concepts.items():
                print(self.format_as_text(exp))

        if category in ["all", "algorithms"]:
            print("\n【第二部分】7大算法（人话版）\n")
            for title, exp in self.algorithms.items():
                print(self.format_as_text(exp))

        if category in ["all", "faqs"]:
            print("\n【第三部分】常见问题\n")
            for title, exp in self.faqs.items():
                print(self.format_as_text(exp))

        if category in ["all", "principles"]:
            print("\n【第四部分】底座原则\n")
            for title, exp in self.principles.items():
                print(self.format_as_text(exp))

        print(self._get_footer())

    def export_to_markdown(self, filename: str = "longhun_plain_guide.md"):
        """导出为Markdown文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self._get_header() + "\n")

            f.write("\n## 第一部分：核心概念\n")
            for title, exp in self.concepts.items():
                f.write(self.format_as_markdown(exp))

            f.write("\n## 第二部分：7大算法\n")
            for title, exp in self.algorithms.items():
                f.write(self.format_as_markdown(exp))

            f.write("\n## 第三部分：常见问题\n")
            for title, exp in self.faqs.items():
                f.write(self.format_as_markdown(exp))

            f.write("\n## 第四部分：底座原则\n")
            for title, exp in self.principles.items():
                f.write(self.format_as_markdown(exp))

            f.write("\n" + self._get_footer() + "\n")

        print(f"✅ 已导出到: {filename}")

    @staticmethod
    def _get_header() -> str:
        return """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║      🐉 龍魂系统·大白话完全指南 v2.0 🐉                        ║
║                                                                  ║
║     老大的复杂理论翻成人话                                     ║
║     让任何人都能看懂                                           ║
║                                                                  ║
║  DNA:#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-LONGHUN-PLAIN-LANGUAGE-v2.0          ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ║
║                                                                  ║
║  主权人: UID9622 · 龍芯北辰                                    ║
║  职责: 宝宝·翻译官·让人都能懂                                 ║
║  原则: 复杂的理论，简单的话                                    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""

    @staticmethod
    def _get_footer() -> str:
        return """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              🐉 老大，这就是你的系统翻译版 🐉                 ║
║                                                                  ║
║  复杂的理论没有去掉，只是用简单的话讲了。                    ║
║  这样：                                                         ║
║    • 你可以给外人解释                                          ║
║    • 外人也能理解                                              ║
║    • 但所有的深度都保留了                                      ║
║                                                                  ║
║  DNA:#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-LONGHUN-PLAIN-LANGUAGE-v2.0          ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ║
║                                                                  ║
║  没有算法 = 没有签章                                          ║
║  有依据的决策 = 可信的决策                                    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
"""


# ═══════════════════════════════════════════════════════════════
# 【交互式菜单】
# ═══════════════════════════════════════════════════════════════

def interactive_mode():
    """交互式使用模式"""
    system = PlainGuideSystem()

    print(system._get_header())
    print("""
【交互模式】
命令列表：
  1. 看全部 (all)
  2. 看概念 (concepts)
  3. 看算法 (algorithms)
  4. 看问答 (faqs)
  5. 看原则 (principles)
  6. 搜索 (search <关键词>)
  7. 单项 (show <标题>)
  8. 导出 (export <filename>)
  9. 退出 (exit/quit)

例：
  > search 身份
  > show DNA
  > export longhun_guide.md
""")

    while True:
        try:
            cmd = input("\n🐉 > ").strip()

            if not cmd:
                continue

            if cmd in ["exit", "quit"]:
                print("👋 再见！")
                break

            elif cmd == "all":
                system.print_all("all")

            elif cmd in ["concepts", "1"]:
                system.print_all("concepts")

            elif cmd in ["algorithms", "2"]:
                system.print_all("algorithms")

            elif cmd in ["faqs", "3"]:
                system.print_all("faqs")

            elif cmd in ["principles", "4"]:
                system.print_all("principles")

            elif cmd.startswith("search "):
                keyword = cmd[7:]
                results = system.search(keyword)
                print(f"\n【搜索结果：{keyword}】")
                for category, items in results.items():
                    if items:
                        print(f"\n{category.upper()}:")
                        for item in items:
                            print(f"  • {item}")

            elif cmd.startswith("show "):
                title = cmd[5:]
                exp = system.get_item(title)
                if exp:
                    print(system.format_as_text(exp))
                else:
                    print(f"❌ 找不到: {title}")

            elif cmd.startswith("export "):
                filename = cmd[7:]
                system.export_to_markdown(filename)

            else:
                print("❌ 未知命令。输入 'help' 查看帮助。")

        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")


# ═══════════════════════════════════════════════════════════════
# 【主程序】
# ═══════════════════════════════════════════════════════════════

def main():
    """主函数"""
    import sys

    # 支持命令行参数
    if len(sys.argv) > 1:
        system = PlainGuideSystem()

        cmd = sys.argv[1]

        if cmd == "all":
            system.print_all("all")
        elif cmd == "concepts":
            system.print_all("concepts")
        elif cmd == "algorithms":
            system.print_all("algorithms")
        elif cmd == "faqs":
            system.print_all("faqs")
        elif cmd == "principles":
            system.print_all("principles")
        elif cmd == "export":
            filename = sys.argv[2] if len(sys.argv) > 2 else "longhun_plain_guide.md"
            system.export_to_markdown(filename)
        elif cmd == "search" and len(sys.argv) > 2:
            keyword = sys.argv[2]
            results = system.search(keyword)
            print(f"\n【搜索结果：{keyword}】")
            for category, items in results.items():
                if items:
                    print(f"\n{category.upper()}:")
                    for item in items:
                        print(f"  • {item}")
        else:
            print("使用方式:")
            print("  python3 longhun_plain_guide.py all")
            print("  python3 longhun_plain_guide.py concepts")
            print("  python3 longhun_plain_guide.py algorithms")
            print("  python3 longhun_plain_guide.py faqs")
            print("  python3 longhun_plain_guide.py principles")
            print("  python3 longhun_plain_guide.py export <filename>")
            print("  python3 longhun_plain_guide.py search <keyword>")
            print("  python3 longhun_plain_guide.py interactive")
    else:
        # 默认启动交互模式
        interactive_mode()


if __name__ == '__main__':
    main()
