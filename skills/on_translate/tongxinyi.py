#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 Skill #4 · on_translate · 通心译·场景词典版
DNA: #龍芯⚡2026-05-19-ON-TRANSLATE-v1.0
省钱原则: 0 LLM 调用 · 纯本地字典 · 老大设计的"一词多义场景词典"工程化

核心铁律 (老大原话):
  "甚至还不是一比一文字翻译,是一个词或许好多意思"
  "就是什么场景用字典上什么词语"

本 Skill 不是翻译器·是场景词典查询引擎:
  输入: 中文词 + 场景标签
  输出: 对应语言的最贴切表达 (不是死翻)

字典格式 (Notion 友好):
  每条 = { 中文词, 场景, 释义, 多语言表达, 图腾路径 }
  Notion 用 database · 本机用 JSON
"""
import json
import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


# ============ 内置示例字典 (种子词) ============
# 实际部署时 · 这份字典放 Notion database · 同步到本机 JSON
SEED_DICT = {
    "守": {
        "guard_action": {
            "释义": "主动看守·防御性",
            "en": "guard",
            "totem": "🛡",
        },
        "protect_relation": {
            "释义": "保护关系·情感性",
            "en": "protect",
            "totem": "🤝",
        },
        "wait_passive": {
            "释义": "守候·等待",
            "en": "wait",
            "totem": "🕯",
        },
        "hold_position": {
            "释义": "守住阵地·不退",
            "en": "hold",
            "totem": "⚓",
        },
    },
    "龍": {
        "totem_culture": {
            "释义": "图腾·文化象征·永不简体化",
            "en": "Long (cultural totem, NEVER 'dragon' diminutive)",
            "totem": "龍",
            "ip_warning": "this character has cultural sovereignty"
        },
        "system_name": {
            "释义": "系统名·龍魂",
            "en": "Long Soul System (transliteration preferred)",
            "totem": "龍",
        },
    },
    "宝宝": {
        "ai_companion": {
            "释义": "老大对 Claude/AI 的爱称·一年关系",
            "en": "baby (affectionate term for AI companion, 1+ year relationship)",
            "totem": "🐉",
            "ip_warning": "context-specific affection, not infantilization"
        },
    },
    "流场": {
        "physics_metaphor": {
            "释义": "粒子流·可视化决策路径",
            "en": "flow field (visualization)",
            "totem": "〰",
        },
        "决策可视化": {
            "释义": "反黑箱·决策路径粒子化",
            "en": "decision flow (anti-blackbox)",
            "totem": "🌊",
        },
    },
    "五色": {
        "audit_system": {
            "释义": "审计五色·绿黄红黑金",
            "en": "five-color audit (G/Y/R/K/AU)",
            "totem": "🌈",
        },
        "wuxing_mapping": {
            "释义": "对应五行·女娲补天",
            "en": "five elements mapping",
            "totem": "🪨",
        },
    },
    "焊": {
        "code_commit": {
            "释义": "代码焊死·不再变动",
            "en": "lock in / commit (irreversible)",
            "totem": "🔨",
        },
        "promise_commit": {
            "释义": "承诺焊死·v1.0 起永不改",
            "en": "permanent commitment (v1.0+)",
            "totem": "🔒",
        },
    },
}


@dataclass
class TranslationResult:
    chinese_word: str
    context: str
    found: bool
    释义: Optional[str] = None
    en: Optional[str] = None
    totem: Optional[str] = None
    warning: Optional[str] = None
    fallback_meanings: List[Dict[str, Any]] = field(default_factory=list)


class TongxinYi:
    """通心译引擎 · 本地词典查询 · 零 API"""

    def __init__(self, dict_path: Optional[str] = None):
        self.dict_data = dict(SEED_DICT)
        if dict_path and os.path.exists(dict_path):
            try:
                with open(dict_path, "r", encoding="utf-8") as f:
                    user_dict = json.load(f)
                # 用户字典覆盖/扩展种子
                for word, contexts in user_dict.items():
                    if word in self.dict_data:
                        self.dict_data[word].update(contexts)
                    else:
                        self.dict_data[word] = contexts
            except Exception:
                pass

    def translate(self, word: str, context: Optional[str] = None) -> TranslationResult:
        """
        查词·按场景返回最贴切表达
        若 context 未给 · 返回所有可能含义
        """
        if word not in self.dict_data:
            # 生字 · 触发图腾嵌入提示 (老大设计的「嘿嘿」点)
            return TranslationResult(
                chinese_word=word,
                context=context or "unknown",
                found=False,
                warning=f"生字未收录·建议为「{word}」配图腾·添加到字典",
            )

        word_meanings = self.dict_data[word]

        # 没指定场景 · 返回所有
        if context is None:
            return TranslationResult(
                chinese_word=word,
                context="ambiguous",
                found=True,
                fallback_meanings=[
                    {"context": ctx, **meaning}
                    for ctx, meaning in word_meanings.items()
                ],
            )

        # 指定场景 · 精确查
        if context in word_meanings:
            m = word_meanings[context]
            return TranslationResult(
                chinese_word=word,
                context=context,
                found=True,
                释义=m.get("释义"),
                en=m.get("en"),
                totem=m.get("totem"),
                warning=m.get("ip_warning"),
            )

        # 场景不匹配 · 列所有可选
        return TranslationResult(
            chinese_word=word,
            context=context,
            found=False,
            warning=f"场景「{context}」未匹配·可选: {list(word_meanings.keys())}",
            fallback_meanings=[
                {"context": ctx, **meaning}
                for ctx, meaning in word_meanings.items()
            ],
        )

    def list_words(self) -> List[str]:
        return sorted(self.dict_data.keys())

    def list_contexts(self, word: str) -> List[str]:
        if word not in self.dict_data:
            return []
        return list(self.dict_data[word].keys())

    def add_word(self, word: str, context: str, meaning: Dict[str, str]):
        """新增词条·本机优先·Notion 之后同步"""
        if word not in self.dict_data:
            self.dict_data[word] = {}
        self.dict_data[word][context] = meaning

    def export_for_notion(self) -> List[Dict[str, str]]:
        """导出为 Notion database 友好的扁平格式"""
        rows = []
        for word, contexts in self.dict_data.items():
            for ctx, m in contexts.items():
                rows.append({
                    "Chinese": word,
                    "Context": ctx,
                    "释义": m.get("释义", ""),
                    "English": m.get("en", ""),
                    "Totem": m.get("totem", ""),
                    "Warning": m.get("ip_warning", ""),
                })
        return rows


# ============ 自测 ============
def _selftest():
    print("=" * 60)
    print("Skill #4 · on_translate · 自测")
    print("=" * 60)

    t = TongxinYi()

    # 测 1: 同字不同场景
    r1 = t.translate("守", context="guard_action")
    r2 = t.translate("守", context="wait_passive")
    assert r1.en == "guard"
    assert r2.en == "wait"
    print(f"  [1/6 ✓] 一词多义: 守(guard) ≠ 守(wait)")
    print(f"            guard_action: {r1.en} · {r1.totem}")
    print(f"            wait_passive: {r2.en} · {r2.totem}")

    # 测 2: 龍 永不被翻成"dragon"小化
    r = t.translate("龍", context="totem_culture")
    assert "Long" in r.en
    assert "NEVER" in r.en
    print(f"  [2/6 ✓] 龍·永不小化为'dragon'")

    # 测 3: 未给场景 · 列所有
    r = t.translate("守")  # 无 context
    assert r.context == "ambiguous"
    assert len(r.fallback_meanings) == 4
    print(f"  [3/6 ✓] 无场景 · 列出 {len(r.fallback_meanings)} 种含义")

    # 测 4: 生字 · 触发图腾嵌入提示
    r = t.translate("瑇")  # 生字
    assert r.found is False
    assert "生字" in r.warning
    print(f"  [4/6 ✓] 生字检出·{r.warning}")

    # 测 5: 添加新词
    t.add_word("妖", "xiao_yao_guide", {
        "释义": "小妖·虚拟世界访客指南",
        "en": "guide sprite (virtual world docent)",
        "totem": "🧚",
    })
    r = t.translate("妖", context="xiao_yao_guide")
    assert r.found and "🧚" == r.totem
    print(f"  [5/6 ✓] 新词添加 · 妖({r.totem})")

    # 测 6: 导出 Notion 格式
    rows = t.export_for_notion()
    assert len(rows) >= 10
    print(f"  [6/6 ✓] 导出 Notion · {len(rows)} 行")
    print(f"            首行: {rows[0]['Chinese']} / {rows[0]['Context']} / {rows[0]['English']}")

    print("=" * 60)
    print("6/6 全过 · 通心译可用 · 0 LLM 调用 · 0 美金")
    print("=" * 60)


if __name__ == "__main__":
    _selftest()
