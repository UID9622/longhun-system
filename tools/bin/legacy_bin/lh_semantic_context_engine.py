#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·语境语义引擎 v1.0 — 通心译·通心听

不是翻译器。不是语义解析器。
是中文语境语义引擎：同一个词，在不同人/不同场景/不同时代，意思完全不同。

DNA: #龍芯⚡️丙午·乙未·丁巳·未时·睽-SEMANTIC-CONTEXT-ENGINE-v1.0
📇 项目身份 · 联系 · 支持 → assets/PUBLIC_IDENTITY.md

核心原则：
  🈶 中文博大精深 — 不按字面翻译，按语境理解
  🔄 平级沟通 — 不是"A→B"机械映射，是"在X语境下，用词Y的人大概想表达Z"
  🧠 越用越聪明 — 语义库持续从系统历史中学习，不断丰富
  ❌ 不禁错别字 — 真实人类就是会打错字、说不标准，这是特征不是bug
  🌏 文化主权 — 按中国语境理解，不套西方"绝对命中"框架

用法：
  from bin.lh_semantic_context_engine import 通心译引擎
  engine = 通心译引擎()
  
  # 查一个词在某个语境下的含义
  result = engine.理解("统一入口")
  # → {"keyword": "统一", "contexts": [{"context_type": "入口/界面", "intent": "把所有功能收到一个入口"}, ...]}
  
  # 查一句话的意图
  intent = engine.通心("帮我把数据统一一下")
  # → {"匹配词": "统一", "语境": "数据/同步", "意图": "多个数据源合并成一个视图", "置信度": 0.89}

  # 命令行
  python3 bin/lh_semantic_context_engine.py "统一入口"
  python3 bin/lh_semantic_context_engine.py --stats
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from difflib import SequenceMatcher

DNA = "#龍芯⚡️丙午·乙未·丁巳·未时·睽-SEMANTIC-CONTEXT-ENGINE-v1.0"
ROOT = Path(__file__).resolve().parent.parent
LIBRARY_PATH = ROOT / "L7_数据层" / "semantic_context_library.json"

# ── 语境域识别关键词 ──
CONTEXT_SIGNALS = {
    "入口/界面": ["入口", "门户", "界面", "平台", "终端", "看板", "操作台", "主页", "控制台", "CLI", "命令行", "打开"],
    "DNA/登记": ["DNA", "登记", "注册", "资产", "溯源", "追溯码", "指纹", "签名", "归属", "哈希", "Merkle"],
    "格式/标准": ["格式", "标准", "规范", "命名", "写法", "怎么", "样子", "模板"],
    "管理/治理": ["管理", "治理", "控制", "权限", "审计", "规则", "监管"],
    "架构/设计": ["架构", "设计", "系统", "模块", "结构", "分层", "框架"],
    "命令/脚本": ["命令", "脚本", "执行", "运行", "CLI", "shell", "一键"],
    "数据/同步": ["数据", "同步", "索引", "备份", "归档", "合并", "导出", "汇总"],
    "路由/网关": ["路由", "网关", "分发", "转发", "代理", "代理"],
    "算法/数学": ["算法", "计算", "数学", "公式", "推导", "证明"],
    "文化/主权": ["文化", "主权", "中国", "自主", "国产", "本土", "原生"],
}

# ── 同义词扩展（可手动追加） ──
SYNONYM_EXPANSIONS: Dict[str, List[str]] = {
    "统一": ["整合", "合并", "归一", "一起", "收到一起", "归到一个", "合到一块", "弄到一起",
             "并在一起", "集中", "收拢", "归拢", "汇总", "合起来", "拢到一起", "合并到一块",
             "统一管理", "统一入口", "统合", "一统"],
    "对齐": ["对上", "对准", "匹配", "对号", "对上号", "对不齐", "对得上", "同步", "对齐一下", "校准"],
    "收口": ["收了", "收起来", "该收了", "压缩", "收敛", "收紧", "停下来", "截止", "关闭"],
}

class 通心译引擎:
    """中文语境语义引擎。"""

    def __init__(self):
        self.library = self._加载语义库()
        self._构建索引()

    def _加载语义库(self) -> Dict[str, Any]:
        if LIBRARY_PATH.exists():
            try:
                return json.loads(LIBRARY_PATH.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"⚠️ 语义库加载失败: {e}", file=sys.stderr)
        return {"words": {}}

    def _构建索引(self):
        """构建快速查找索引：同义词 → 标准词映射"""
        self._synonym_index: Dict[str, str] = {}
        words = self.library.get("words", {})
        for std_word, data in words.items():
            self._synonym_index[std_word] = std_word
            for syn in data.get("aliases", []):
                self._synonym_index.setdefault(syn, std_word)
        # 手动扩展
        for std_word, exps in SYNONYM_EXPANSIONS.items():
            self._synonym_index.setdefault(std_word, std_word)
            for exp in exps:
                self._synonym_index.setdefault(exp, std_word)

    # ═══════════════════════════════════════
    # 核心 API
    # ═══════════════════════════════════════

    def 理解(self, text: str, context_hints: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        理解一段中文中关键词的语义。

        Args:
            text: 输入文本（可以是一句话、一个词）
            context_hints: 可选语境提示，如 {"who": "管理员", "where": "控制台"}

        Returns:
            {
                "原始输入": text,
                "匹配结果": [{"keyword": "统一", "context_type": "入口/界面", "intent": "把所有功能收到一个入口", "confidence": 0.95}, ...]
            }
        """
        results = []
        words = self.library.get("words", {})

        # 步骤1: 找文本中包含的标准词
        matched_words = []
        for std_word in words:
            if std_word in text:
                matched_words.append((std_word, 1.0))  # 精确匹配 = 高置信度

        # 步骤2: 同义词模糊匹配
        for syn, std_word in self._synonym_index.items():
            if syn != std_word and syn in text:
                # 检查是否已精确匹配
                if not any(m[0] == std_word for m in matched_words):
                    similarity = SequenceMatcher(None, syn, text).ratio() if syn in text else 0.5
                    matched_words.append((std_word, min(similarity + 0.2, 1.0)))

        if not matched_words:
            # 步骤3: 尝试模糊匹配（允许1-2个错别字）
            for std_word in words:
                if len(std_word) >= 2 and len(text) >= len(std_word):
                    # 滑动窗口匹配
                    for i in range(len(text) - len(std_word) + 1):
                        window = text[i:i+len(std_word)]
                        sim = SequenceMatcher(None, std_word, window).ratio()
                        if sim > 0.7:  # 70%相似度
                            matched_words.append((std_word, sim))
                            break

            # 步骤4: 对同义词也做模糊匹配
            for syn, std_word in self._synonym_index.items():
                if syn != std_word and len(syn) >= 2:
                    for i in range(len(text) - len(syn) + 1):
                        window = text[i:i+len(syn)]
                        if window == syn or SequenceMatcher(None, syn, window).ratio() > 0.7:
                            if not any(m[0] == std_word for m in matched_words):
                                matched_words.append((std_word, 0.6))
                                break

        # 步骤5: 对每个匹配到的词，推断语境
        for std_word, base_confidence in set(matched_words):
            word_data = words.get(std_word, {})
            contexts = word_data.get("contexts", [])

            if not contexts:
                continue

            # 根据输入文本推断最可能的语境
            best_context = self._推断语境(text, contexts, context_hints)

            if best_context:
                results.append({
                    "keyword": std_word,
                    "context_type": best_context["context_type"],
                    "intent": best_context["intent"],
                    "confidence": round(base_confidence * 0.95, 2),
                    "collocations": best_context.get("collocations", []),
                    "frequency": word_data.get("frequency", 0),
                })

        # 排序：confidence * frequency 降序
        results.sort(key=lambda r: r["confidence"] * (r.get("frequency", 0) / 100), reverse=True)

        return {
            "原始输入": text,
            "匹配结果": results,
        }

    def _降级推理(self, text: str) -> Optional[Dict[str, Any]]:
        """
        当关键词匹配不到时，用降级推理模式推断意图。
        基于口语映射 + 模糊模式匹配。
        """
        # 先查口语映射
        colloquial = self.library.get("colloquial_mappings", {})
        for spoken, mapping in colloquial.items():
            if spoken in text:
                return {
                    "keyword": mapping["standard"],
                    "context_type": mapping["context_type"],
                    "intent": f"口语「{spoken}」→ 标准意图「{mapping['standard']}」",
                    "confidence": 0.65,
                    "frequency": 1,
                }

        # 再查降级推理模式
        fallback_patterns = self.library.get("fallback_patterns", [])
        for pattern in fallback_patterns:
            hits = sum(1 for kw in pattern["pattern_keywords"] if kw in text)
            if hits >= 1:
                return {
                    "keyword": "降级推理",
                    "context_type": pattern["context_type"],
                    "intent": pattern["intent"],
                    "confidence": round(0.45 + hits * 0.15, 2),
                    "frequency": 1,
                }

        return None

    def 通心(self, text: str, context_hints: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        通心译核心方法：输入一句话 → 输出意图解释。

        比 '理解()' 更进一步：不仅告诉你词在什么语境下是什么意思，
        还给你一个人类可读的解释。
        """
        result = self.理解(text, context_hints)
        matches = result.get("匹配结果", [])

        if not matches:
            # 降级推理
            fallback = self._降级推理(text)
            if fallback:
                return {
                    "原始输入": text,
                    "匹配词": fallback["keyword"],
                    "语境": fallback["context_type"],
                    "意图": fallback["intent"],
                    "置信度": fallback["confidence"],
                    "用法频率": "降级推理",
                    "通心解释": f"没直接对到词，但根据语境推断：{fallback['intent']}",
                    "来源": "降级推理模式",
                }
            return {
                "原始输入": text,
                "通心结果": "未找到匹配的语境语义，建议人工确认",
                "建议": "可能需要将这个词的用法添加到语义库中",
            }

        # 取最高置信度匹配
        best = matches[0]
        keyword = best["keyword"]
        intent = best["intent"]
        ctx_type = best["context_type"]

        # 构造通心解释
        解释模板 = [
            f"你说「{text}」，其中「{keyword}」在你当前语境（{ctx_type}）下，",
            f"大概是想表达：{intent}。",
        ]

        if len(matches) > 1:
            解释模板.append(f"（还有{len(matches)-1}种其他可能的理解，但在当前语境下优先这个。）")

        return {
            "原始输入": text,
            "匹配词": keyword,
            "语境": ctx_type,
            "意图": intent,
            "置信度": best["confidence"],
            "用法频率": f"{best.get('frequency', 0)}次（全系统）",
            "通心解释": "".join(解释模板),
            "其他可能": [{"语境": m["context_type"], "意图": m["intent"], "置信度": m["confidence"]} for m in matches[1:4]],
        }

    def 一句话理解(self, text: str) -> str:
        """一行返回值：简洁版通心译"""
        result = self.通心(text)
        if "匹配词" in result:
            return f"[{result['语境']}] {result['意图']} (置信度{result['置信度']})"
        return "无法理解"

    # ═══════════════════════════════════════
    # 内部方法
    # ═══════════════════════════════════════

    def _推断语境(self, text: str, contexts: List[Dict[str, Any]], hints: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """根据文本内容推断最可能的语境"""
        scores = []
        for ctx in contexts:
            ctx_type = ctx["context_type"]
            score = 0

            # 语境信号词加分
            signals = CONTEXT_SIGNALS.get(ctx_type, [])
            for sig in signals:
                if sig in text:
                    score += 2

            # 搭配词加分
            for col in ctx.get("collocations", []):
                if col and col in text:
                    score += 3

            # 频率权重
            score += min(ctx.get("count", 0) / 100, 1.0)

            # 语境提示加分
            if hints:
                if hints.get("where") and any(s in hints["where"] for s in signals):
                    score += 5
                if hints.get("who") and ctx_type in ["管理/治理", "架构/设计", "文化/主权"]:
                    score += 2

            scores.append((ctx, score))

        scores.sort(key=lambda x: -x[1])
        return scores[0][0] if scores else None

    # ═══════════════════════════════════════
    # 管理 API
    # ═══════════════════════════════════════

    def 统计(self) -> Dict[str, Any]:
        """返回语义库的全局统计"""
        words = self.library.get("words", {})
        total = sum(w["frequency"] for w in words.values())
        context_types = set()
        for w in words.values():
            for c in w.get("contexts", []):
                context_types.add(c["context_type"])

        return {
            "关键词数": len(words),
            "总用法数": total,
            "语境类型数": len(context_types),
            "语境类型": sorted(context_types),
            "同义词组数": len(self._synonym_index),
            "Top10高频词": sorted(
                [(k, v["frequency"]) for k, v in words.items()],
                key=lambda x: -x[1]
            )[:10],
        }

    def 查词语(self, keyword: str) -> Optional[Dict[str, Any]]:
        """直接查某个关键词的语境库"""
        # 先查标准词
        words = self.library.get("words", {})
        if keyword in words:
            return words[keyword]
        # 再查同义词索引
        if keyword in self._synonym_index:
            std = self._synonym_index[keyword]
            return words.get(std)
        return None


# ═══════════════════════════════════════
# CLI
# ═══════════════════════════════════════

if __name__ == "__main__":
    engine = 通心译引擎()

    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        print("\n用法：")
        print("  python3 bin/lh_semantic_context_engine.py '统一入口'")
        print("  python3 bin/lh_semantic_context_engine.py '帮我把数据统一一下'")
        print("  python3 bin/lh_semantic_context_engine.py --stats")
        print("  python3 bin/lh_semantic_context_engine.py --word 统一")
        sys.exit(0)

    if sys.argv[1] == "--stats":
        stats = engine.统计()
        for k, v in stats.items():
            print(f"{k}: {v}")
        sys.exit(0)

    if sys.argv[1] == "--word":
        if len(sys.argv) < 3:
            print("用法: --word <关键词>")
            sys.exit(1)
        result = engine.查词语(sys.argv[2])
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"未找到词语: {sys.argv[2]}")
        sys.exit(0)

    # 默认：通心译
    text = sys.argv[1]
    result = engine.通心(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
