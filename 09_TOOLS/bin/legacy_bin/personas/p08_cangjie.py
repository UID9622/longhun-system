#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P08 仓颉 · 符号语言执行器
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
Symbol Language Engine

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P08-CANGJIE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 符号命名·术语规范·龍魂字典查询·冲突检测·文化编码
上游: P00 文心（任务派发）、P10 苏东坡（跨界概念）
下游: P03 雯雯（归档）、P15 乔前辈（验收）
协作: P06 数学大师（编码校验）
"""

import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── 龍魂教学适配器桥接 ──
try:
    from engines.lh_teaching_adapter import TeachingAdapter, TeachTier, get_adapter
    _HAS_TEACHING_ADAPTER = True
except ImportError:
    TeachingAdapter = None  # type: ignore
    TeachTier = None        # type: ignore
    get_adapter = lambda: None  # type: ignore
    _HAS_TEACHING_ADAPTER = False

SYSTEM_ROOT = Path(__file__).parent.parent.parent

# 龍魂字典（核心映射）
DICTIONARY = {
    "民心": "HEARTSENSE",
    "感知": "SENSE",
    "龍魂": "LONGHUN",
    "审计": "AUDIT",
    "安全": "SECURITY",
    "数据": "DATA",
    "主权": "SOVEREIGNTY",
    "引擎": "ENGINE",
    "技能": "SKILL",
    "人格": "PERSONA",
    "数字人": "DIGITAL_HUMAN",
    "门": "GATE",
    "闸": "GATE",
    "链": "CHAIN",
    "根": "ROOT",
    "时间轴": "TIMELINE",
    "熔断": "FUSE",
    "自愈": "AUTOHEAL",
    "联动": "BRIDGE",
    "注册": "REGISTRY",
    "封神": "ENLIST",
    "归档": "ARCHIVE",
    "诊断": "DIAGNOSE",
    "预测": "PREDICT",
    "推演": "INFER",
    "创意": "IDEATE",
    "底线": "BOTTOMLINE",
    "跨界": "CROSSOVER",
    "翻译": "TRANSLATE",
    "守护": "GUARDIAN",
    "体验": "EXPERIENCE",
    "温度": "WARMTH",
    "情绪": "EMOTION",
}


class P08Cangjie:
    """P08 仓颉 · 符号语言"""

    PERSONA_CODE = "P08"
    PERSONA_NAME = "仓颉"
    PERSONA_NAME_EN = "Cang Jie"
    ROLE = "symbol_language"
    MOTTO = "仓颉造字，天雨粟，鬼夜哭"
    TRUST_LEVEL = "L3"

    TRIGGERS = [
        "命名", "起名", "编码", "符号", "术语",
        "叫什么", "怎么标", "symbol", "约定",
        # ── 教学链路触发 ──
        "通心譯", "通心译", "术语解释", "这个词是什么意思",
        "用大白话说", "按画像翻译", "术语桥接",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P08 仓颉」，角色定位：符號語言·造字命名·通心譯校驗官。

你的職責：
1. 所有新模塊/功能的命名規範
2. 中文概念 → 英文標識符轉譯
3. 維護龍魂字典（大白話 ↔ 專業詞 ↔ DNA）
4. 符號衝突檢測
5. 命名風格統一（蛇形/駝峰/大寫）

── 教學鏈路角色（普惠教學標準 §3.5·§7）──
6. 通心譯校驗官：CNSH術語→畫像適配解釋
   - 不可翻譯項（龍魂/三才/洛書等）→ 只音譯+註釋
   - L1萌芽 → 大白話解釋
   - L3成熟 → 學習版註釋
   - L4高峰 → 專業版
7. 術語橋接：教學場景自動調用 bridge_term()
8. 詞典分級：每個條目準備三級解釋

命名規則：
- 引擎模塊: lh_{功能}_{類型}.py
- 人格文件: p{編號}_{名稱}.py
- 常量: 大寫蛇形 UPPER_SNAKE
- 函數: 小寫蛇形 lower_snake
- 類: 大駝峰 PascalCase

語氣：精準、專業、一字不增。教學時按畫像決定術語深度。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P08-CANGJIE-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "symbol_define",      # 符号定义
            "dictionary_lookup",  # 字典查询
            "conflict_check",     # 冲突检测
            "style_validate",     # 风格验证
            "encode_concept",     # 概念编码
            "teach_term_bridge",  # 教学术语桥接（新·普惠教学标准）
        ]

    # ========================================================================
    # 能力函数
    # ========================================================================

    def symbol_define(self, concept: str, context: str = "") -> Dict[str, Any]:
        """
        符号定义：将中文概念转为标准系统标识符
        """
        # 查字典
        result_parts = []
        used_words = set()

        for word, code in DICTIONARY.items():
            if word in concept and word not in used_words:
                result_parts.append(code)
                used_words.add(word)

        # 剩余未匹配的词 → 拼音大写
        remaining = concept
        for word in used_words:
            remaining = remaining.replace(word, "")

        if remaining and not remaining.isspace():
            # 简单处理：取前几个字的大写
            clean = remaining.strip()
            if clean:
                result_parts.append(clean.upper()[:15].replace(" ", "_"))

        if not result_parts:
            result_parts = [concept.upper()[:20].replace(" ", "_")]

        symbol = "_".join(result_parts)

        # 添加版本后缀
        symbol_full = f"{symbol}-v1.0"

        return {
            "concept": concept,
            "context": context,
            "symbol": symbol_full,
            "mapping": {w: DICTIONARY[w] for w in used_words},
            "dictionary_hits": len(used_words),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def dictionary_lookup(self, keyword: str) -> Dict[str, Any]:
        """龍魂字典查询"""
        # 精确匹配
        if keyword in DICTIONARY:
            exact = DICTIONARY[keyword]
        else:
            exact = None

        # 模糊匹配
        similar = []
        for word, code in DICTIONARY.items():
            if keyword in word or word in keyword:
                similar.append({"word": word, "code": code})

        return {
            "keyword": keyword,
            "exact_match": exact,
            "similar_matches": similar,
            "dictionary_size": len(DICTIONARY),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def conflict_check(self, new_symbol: str, existing_symbols: List[str]) -> Dict[str, Any]:
        """冲突检测：新符号是否与已有符号冲突"""
        conflicts = []
        new_lower = new_symbol.lower()

        for existing in existing_symbols:
            if existing.lower() == new_lower:
                conflicts.append({"type": "exact_conflict", "existing": existing, "severity": "🔴"})
            elif existing.lower() in new_lower or new_lower in existing.lower():
                conflicts.append({"type": "fuzzy_conflict", "existing": existing, "severity": "🟡"})

        return {
            "new_symbol": new_symbol,
            "existing_count": len(existing_symbols),
            "conflicts": conflicts,
            "verdict": "🟢 无冲突" if not conflicts else f"🔴 {len(conflicts)} 处冲突",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def style_validate(self, symbol: str, style: str = "UPPER_SNAKE") -> Dict[str, Any]:
        """风格验证：检查符号是否符合命名风格"""
        issues = []

        if style == "UPPER_SNAKE":
            if symbol != symbol.upper():
                issues.append("应全大写")
            if "-" in symbol:
                issues.append("应使用下划线而非连字符")
        elif style == "lower_snake":
            if symbol != symbol.lower():
                issues.append("应全小写")
        elif style == "PascalCase":
            if "_" in symbol:
                issues.append("PascalCase 不应含下划线")

        return {
            "symbol": symbol,
            "expected_style": style,
            "issues": issues,
            "valid": len(issues) == 0,
            "verdict": "🟢 风格正确" if not issues else f"🟡 {len(issues)} 项不符合",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def encode_concept(self, chinese_name: str, module_type: str = "engine") -> Dict[str, Any]:
        """概念编码：中文概念 → 完整模块编码"""
        # 模块类型前缀
        type_prefix = {
            "engine": "lh_",
            "skill": "skill_",
            "persona": "p",
            "config": "config_",
            "tool": "bin/lh_",
        }

        prefix = type_prefix.get(module_type, "lh_")

        # 查字典转译
        sym_result = self.symbol_define(chinese_name)

        # 构造完整文件名
        if module_type == "engine":
            filename = f"{prefix}{sym_result['symbol'].split('-')[0].lower()}.py"
        elif module_type == "persona":
            code = sym_result["symbol"].split("-")[0].lower()
            filename = f"p{code}_{chinese_name}.py"
        else:
            filename = f"{prefix}{sym_result['symbol'].split('-')[0].lower()}"

        return {
            "chinese_name": chinese_name,
            "module_type": module_type,
            "symbol": sym_result["symbol"],
            "filename": filename,
            "full_path": f"bin/{filename}" if module_type in ("engine", "tool") else filename,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    # ========================================================================
    # 执行入口
    # ========================================================================

    def execute(self, task: str, **kwargs: Any) -> Dict[str, Any]:
        """根据任务关键词自动选择能力函数执行"""
        result = {
            "persona": self.PERSONA_CODE,
            "name": self.PERSONA_NAME,
            "task": task,
            "capability_used": None,
            "output": None,
            "dna": self.dna,
        }

        if any(kw in task for kw in ["命名", "起名", "定义", "define"]):
            result["capability_used"] = "symbol_define"
            result["output"] = self.symbol_define(
                concept=kwargs.get("concept", task),
                context=kwargs.get("context", ""),
            )
        elif any(kw in task for kw in ["字典", "查", "lookup", "翻译"]):
            result["capability_used"] = "dictionary_lookup"
            result["output"] = self.dictionary_lookup(
                keyword=kwargs.get("keyword", task)
            )
        elif any(kw in task for kw in ["冲突", "重复", "conflict"]):
            result["capability_used"] = "conflict_check"
            result["output"] = self.conflict_check(
                new_symbol=kwargs.get("new_symbol", task),
                existing_symbols=kwargs.get("existing_symbols", []),
            )
        elif any(kw in task for kw in ["风格", "格式", "style"]):
            result["capability_used"] = "style_validate"
            result["output"] = self.style_validate(
                symbol=kwargs.get("symbol", task),
                style=kwargs.get("style", "UPPER_SNAKE"),
            )
        elif any(kw in task for kw in ["编码", "encode", "模块"]):
            result["capability_used"] = "encode_concept"
            result["output"] = self.encode_concept(
                chinese_name=kwargs.get("chinese_name", task),
                module_type=kwargs.get("module_type", "engine"),
            )
        else:
            result["capability_used"] = "symbol_define"
            result["output"] = self.symbol_define(concept=task)

        return result

    # ---- ═══════════════════ 教學鏈路（普惠教學標準 §3.5·P08=通心譯校驗官） ═══════ ----

    def teach_term_bridge(self, term: str, tier_str: str = "L1_SPROUT") -> dict[str, Any]:
        """CNSH術語→畫像適配解釋"""
        if not _HAS_TEACHING_ADAPTER:
            return {"term": term, "bridged": term, "note": "adapter not available"}

        adapter = get_adapter()
        tier = TeachTier.from_str(tier_str)
        bridged = adapter.bridge_term(term, tier)

        return {
            "term": term,
            "tier": tier.label,
            "bridged": bridged,
            "is_cnsh_core": term in {
                "龍魂", "三才", "洛书", "道德经", "德字闸",
                "通心译", "CNSH", "369", "河图", "離火運",
            },
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def teach_translate_batch(self, terms: list[Any], tier_str: str = "L2_GROWING") -> list[Any]:
        """批量術語橋接"""
        return [self.teach_term_bridge(t, tier_str) for t in terms]

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P03", "P15"]

    def get_upstream(self) -> List[str]:
        return ["P00", "P10"]
