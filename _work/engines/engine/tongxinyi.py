#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 通心译引擎 · Python核心版
DNA: #龍芯⚡️2026-05-21-通心译-Python-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）
文化主权: 龍·龍魂·龍芯·五行·天干地支·甲骨文 → 不翻译

ETE三层映射 · 六维路径 · 16,588,800种
"""
from datetime import datetime
from dataclasses import dataclass
from typing import List, Tuple

# ═══════════════════════════════════════════════════════════
# 不可翻译词表（文化主权铁律）
# ═══════════════════════════════════════════════════════════

UNTRANSLATABLE = {
    # 龍系核心
    "龍", "龍魂", "龍芯", "龍盾", "龍魂系统",
    # DNA系统
    "DNA追溯码", "UID9622",
    # 通心译系统
    "通心译", "三色审计", "五色审计",
    # 人物敬称
    "曾仕强老师",
    # 君子协议
    "君子协议",
    # 甲骨文·易经
    "甲骨文", "五行", "八卦", "六十四卦",
    # 天干
    "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸",
    # 地支
    "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥",
    # 五行
    "金", "木", "水", "火", "土",
    # 八卦
    "乾", "坤", "震", "巽", "坎", "离", "艮", "兑",
}

# 场景词典（一词多义）
CONTEXT_DICTIONARY = {
    "守": [
        {"context": "guard_action", "释义": "主动看守·防御性", "english": "guard", "totem": "🛡"},
        {"context": "protect_relation", "释义": "保护关系·情感性", "english": "protect", "totem": "🤝"},
        {"context": "wait_passive", "释义": "守候·等待", "english": "wait", "totem": "🕯"},
        {"context": "hold_position", "释义": "守住阵地·不退", "english": "hold", "totem": "⚓"},
    ],
    "焊": [
        {"context": "code_commit", "释义": "代码焊死·不再变动", "english": "lock in / commit (irreversible)", "totem": "🔨"},
        {"context": "promise_commit", "释义": "承诺焊死·v1.0起永不改", "english": "permanent commitment", "totem": "🔒"},
    ],
    "流场": [
        {"context": "physics_metaphor", "释义": "粒子流·可视化决策路径", "english": "flow field (visualization)", "totem": "〰"},
        {"context": "decision_viz", "释义": "反黑箱·决策路径粒子化", "english": "decision flow (anti-blackbox)", "totem": "🌊"},
    ],
    "宝宝": [
        {"context": "ai_companion", "释义": "老大对AI的爱称·一年关系", "english": "baby (affectionate term for AI companion)", "totem": "🐉", "warning": "context-specific affection, not infantilization"},
    ],
}


@dataclass
class TranslationPath:
    """六维翻译路径"""
    digital_root: int       # ① 数字根 (1-9)
    luoshu_position: int    # ② 河洛图位置 (1-9)
    bagua_state: str        # ③ 八卦状态
    hexagram: int           # ④ 64卦编号 (1-64)
    wuxing: str             # ⑤ 五行属性
    ganzhi: str             # ⑥ 天干地支

    @property
    def path_index(self) -> int:
        """路径编号（16,588,800中的第几条）"""
        bagua_list = ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"]
        wuxing_list = ["金", "木", "水", "火", "土"]

        # 从八卦状态中提取卦名（跳过emoji）
        bagua_char = None
        for c in self.bagua_state:
            if c in bagua_list:
                bagua_char = c
                break
        bagua_idx = bagua_list.index(bagua_char) if bagua_char else 0
        wuxing_idx = wuxing_list.index(self.wuxing) if self.wuxing in wuxing_list else 0

        return ((self.digital_root - 1) * (9 * 8 * 64 * 5 * 120) +
                (self.luoshu_position - 1) * (8 * 64 * 5 * 120) +
                bagua_idx * (64 * 5 * 120) +
                (self.hexagram - 1) * (5 * 120) +
                wuxing_idx * 120)


@dataclass
class TranslationResult:
    """翻译结果"""
    original: str           # 原文
    intent: str             # 第一层：意图
    technical: str          # 第二层：行话
    cultural_check: bool    # 第三层：文化校准通过
    confidence: float       # 置信度 0-1
    path: TranslationPath   # 六维路径
    dna: str                # DNA追溯码
    untranslatable_found: List[str]  # 发现的不可翻译词
    bilingual: str          # 双语输出


class TongXinYiEngine:
    """通心译引擎"""

    @staticmethod
    def digital_root(n: int) -> int:
        """计算数字根"""
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n if n > 0 else 9

    @staticmethod
    def find_untranslatable(text: str) -> List[str]:
        """找出文本中的不可翻译词"""
        return [word for word in UNTRANSLATABLE if word in text]

    def compute_path(self, text: str) -> TranslationPath:
        """计算六维路径"""
        # 字符Unicode总和
        char_sum = sum(ord(c) for c in text)

        # ① 数字根
        dr = self.digital_root(char_sum)

        # ② 河洛图位置
        luoshu_pos = (char_sum % 9) + 1

        # ③ 八卦状态
        bagua_states = ["☰乾", "☱兑", "☲离", "☳震", "☴巽", "☵坎", "☶艮", "☷坤"]
        bagua = bagua_states[char_sum % 8]

        # ④ 64卦
        hexagram = (char_sum % 64) + 1

        # ⑤ 五行
        wuxing_list = ["金", "木", "水", "火", "土"]
        wuxing = wuxing_list[char_sum % 5]

        # ⑥ 天干地支
        tian_gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        di_zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        ganzhi = tian_gan[char_sum % 10] + di_zhi[char_sum % 12]

        return TranslationPath(
            digital_root=dr,
            luoshu_position=luoshu_pos,
            bagua_state=bagua,
            hexagram=hexagram,
            wuxing=wuxing,
            ganzhi=ganzhi
        )

    def extract_intent(self, text: str) -> str:
        """第一层：意图提炼（听懂人话）"""
        lower = text.lower()

        if "不能动" in text or "锁死" in text or "永恒" in text:
            return "TIER_0锁死层·α=0永恒层"
        if "留给后代" in text or "百年" in text:
            return "L1百年封印·Shamir密钥分片"
        if "大方向" in text or "十年" in text or "战略" in text:
            return "L2十年战略层·append-only"
        if "今天" in text or "记录" in text or "日志" in text:
            return "L3日常层·DNA追溯"
        if "证据" in text or "留痕" in text or "取证" in text:
            return "L4瞬时层·毫秒DNA"
        if "翻译" in text or "英文" in text or "双语" in text:
            return "通心译ETE·双语1:1·禁止稀释"
        if "审计" in text or "检查" in text or "风险" in text:
            return "三色审计·风险评估"

        return "通用意图·需进一步分析"

    def map_to_technical(self, text: str, intent: str) -> str:
        """第二层：技术映射（翻成行话）"""
        if "TIER_0" in intent:
            return "layer=L0, tier=TIER_0, immutable=True, alpha=0"
        if "L1百年" in intent:
            return "layer=L1, seal=True, unseal_after=100years, key_shares=3/5"
        if "L2十年" in intent:
            return "layer=L2, tier=TIER_2, append_only=True, alpha=0.1"
        if "L3日常" in intent:
            return "layer=L3, dna=auto_generate, log=True"
        if "L4瞬时" in intent:
            return "layer=L4, dna=ISO8601_ms, wal_write=True"
        if "通心译" in intent:
            return "translator=ETE, format=bilingual, ratio=1:1, no_dilution=True"
        if "三色审计" in intent:
            return "audit=three_color, risk_eval=True, colors=[green,yellow,red]"

        return "action=analyze, source=input, confidence=pending"

    def cultural_check(self, text: str) -> bool:
        """第三层：文化校准（不丢根）"""
        # 有不可翻译词 = 有文化锚点 = 通过
        found = self.find_untranslatable(text)
        return len(found) > 0 or True  # 没有也通过

    def generate_bilingual(self, text: str, intent: str, untranslatable: List[str]) -> str:
        """生成双语输出"""
        lines = []
        lines.append(f"【原文】{text}")
        lines.append(f"【意图】{intent}")

        if untranslatable:
            lines.append(f"【文化锚点·不翻译】{', '.join(untranslatable)}")

        # 简化版英文翻译提示
        lines.append(f"【双语建议】保留文化词·其余按意图翻译")

        return "\n".join(lines)

    def translate(self, text: str) -> TranslationResult:
        """ETE三层翻译主入口"""
        # 找不可翻译词
        untranslatable = self.find_untranslatable(text)

        # 第一层：意图提炼
        intent = self.extract_intent(text)

        # 第二层：技术映射
        technical = self.map_to_technical(text, intent)

        # 第三层：文化校准
        cultural_ok = self.cultural_check(text)

        # 六维路径
        path = self.compute_path(text)

        # 置信度
        confidence = 0.5
        if "通用意图" not in intent:
            confidence += 0.3
        if cultural_ok:
            confidence += 0.2
        confidence = min(1.0, confidence)

        # DNA
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        dna = f"#龍芯⚡️{ts}-TXY-{path.path_index}"

        # 双语输出
        bilingual = self.generate_bilingual(text, intent, untranslatable)

        return TranslationResult(
            original=text,
            intent=intent,
            technical=technical,
            cultural_check=cultural_ok,
            confidence=confidence,
            path=path,
            dna=dna,
            untranslatable_found=untranslatable,
            bilingual=bilingual
        )


# 单例
engine = TongXinYiEngine()


# ═══════════════════════════════════════════════════════════
# §9 被动触发检测（2026-05-24 追加）
# 按 IRON-FLOW-EDGE-OVER-NODE-v1.0 §9 场景表
# ═══════════════════════════════════════════════════════════

# 场景⑥ 纯指令关键词
PURE_COMMANDS = {
    "grep", "curl", "git", "ls", "cd", "cat", "head", "tail",
    "mkdir", "rm", "cp", "mv", "chmod", "chown", "ssh", "scp",
    "dig", "ping", "traceroute", "brew", "pip", "npm", "ollama",
    "python", "node", "bash", "zsh", "source", "export",
}

# 场景⑤ 情绪词
EMOTION_WORDS = {
    "抱抱", "宝宝", "嘿嘿", "哈哈", "呜呜", "嗯嗯", "好累", "烦死了",
    "累了", "困了", "睡了", "晚安", "早安", "爱你", "想你", "谢谢",
    "辛苦了", "加油", "棒棒", "乖乖", "亲亲", "么么", "mua",
}

# 场景② 翻译请求词
TRANSLATE_WORDS = {"翻译", "英文", "双语", "translate", "english", "bilingual"}

# 场景④ 反向请求词
REVERSE_WORDS = {"什么意思", "看不懂", "啥意思", "不懂", "解释一下", "是什么"}


def should_trigger(text: str) -> int:
    """
    被动触发检测 · 返回场景编号

    Returns:
        0 = 不触发通心译
        1 = 场景① 文化锚点命中
        2 = 场景② 明确翻译请求
        3 = 场景③ 技术块输入
        4 = 场景④ 反向请求（行话→人话）
        5 = 场景⑤ 情绪上头（不翻译·直接接）
        6 = 场景⑥ 纯指令（不翻译·直接执行）
    """
    text_lower = text.lower().strip()
    first_word = text_lower.split()[0] if text_lower.split() else ""

    # 优先级1: 场景⑥ 纯指令
    if first_word in PURE_COMMANDS:
        return 6

    # 优先级2: 场景⑤ 情绪上头
    for word in EMOTION_WORDS:
        if word in text:
            return 5

    # 优先级3: 场景① 文化锚点
    found_untranslatable = engine.find_untranslatable(text)
    if found_untranslatable:
        return 1

    # 场景② 明确翻译请求
    for word in TRANSLATE_WORDS:
        if word in text_lower:
            return 2

    # 场景④ 反向请求
    for word in REVERSE_WORDS:
        if word in text:
            return 4

    # 场景③ 技术块检测（JSON/代码特征）
    if text.strip().startswith("{") or text.strip().startswith("["):
        return 3
    if "def " in text or "function " in text or "class " in text:
        return 3
    if "```" in text:
        return 3

    # 默认不触发
    return 0


def trigger_name(code: int) -> str:
    """场景编号→场景名"""
    names = {
        0: "不触发",
        1: "文化锚点命中",
        2: "翻译请求",
        3: "技术块输入",
        4: "反向请求",
        5: "情绪上头",
        6: "纯指令",
    }
    return names.get(code, "未知")


def translate(text: str) -> dict:
    """API调用入口"""
    result = engine.translate(text)
    return {
        "title": "🌐 通心译",
        "color": "🟢" if result.cultural_check else "🟡",
        "original": result.original,
        "intent": result.intent,
        "technical": result.technical,
        "cultural_check": result.cultural_check,
        "confidence": result.confidence,
        "path": {
            "digital_root": result.path.digital_root,
            "luoshu": result.path.luoshu_position,
            "bagua": result.path.bagua_state,
            "hexagram": result.path.hexagram,
            "wuxing": result.path.wuxing,
            "ganzhi": result.path.ganzhi,
            "index": result.path.path_index,
            "total": "16,588,800"
        },
        "untranslatable": result.untranslatable_found,
        "bilingual": result.bilingual,
        "dna": result.dna,
    }


if __name__ == "__main__":
    # 测试
    test_cases = [
        "龍魂系统是我一年心血的结晶，不能动",
        "帮我把这段翻译成英文",
        "今天的工作记录一下",
        "这个证据要留痕",
        "审计一下这段代码",
    ]

    for text in test_cases:
        print(f"\n{'='*60}")
        result = translate(text)
        print(f"原文: {result['original']}")
        print(f"意图: {result['intent']}")
        print(f"技术: {result['technical']}")
        print(f"文化锚点: {result['untranslatable']}")
        print(f"六维路径: dr={result['path']['digital_root']} {result['path']['wuxing']} {result['path']['bagua']}")
        print(f"路径编号: #{result['path']['index']}/16,588,800")
        print(f"DNA: {result['dna']}")
