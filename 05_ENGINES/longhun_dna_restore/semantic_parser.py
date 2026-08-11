#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 语义摘要解析器 v1.1
DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-SEMANTIC-PARSER-V1.1-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

语义摘要→结构化变更指令。支持AI解析（OpenAI/Anthropic/本地模型）
和基于规则的回退解析。
"""

import re
import json
from typing import Dict, List, Optional


class SemanticParser:
    """
    语义摘要解析器

    将自然语言变更描述（"为什么改"）转换为结构化变更指令。
    三层策略:
    1. 有structured_diff → 优先使用（置信度最高）
    2. 有AI provider → 调用AI解析（置信度高）
    3. 无AI → 规则匹配回退（置信度中）
    """

    # 变更类型关键词映射
    TYPE_KEYWORDS = {
        "feat": ["新增", "添加", "创建", "实现", "加入", "引入"],
        "fix": ["修复", "修正", "解决", "修补", "bug"],
        "refactor": ["重构", "重写", "优化结构", "拆分", "合并"],
        "perf": ["优化", "提速", "加速", "性能", "加快", "降低", "减少"],
        "style": ["格式化", "排版", "缩进", "命名"],
        "docs": ["文档", "注释", "说明", "readme"],
        "test": ["测试", "单元测试", "集成测试"],
    }

    def __init__(self, ai_provider: Optional[str] = None, model: Optional[str] = None):
        """
        Args:
            ai_provider: AI提供者 ("openai" / "anthropic" / "local")
            model: 模型名称 (如 "gpt-4" / "claude-3")
        """
        self.ai_provider = ai_provider
        self.model = model or "gpt-4"
        self._ai_client = None

    def parse(
        self, semantic_diff: str, structured_diff: Optional[Dict] = None
    ) -> Dict:
        """
        解析语义摘要 → 生成可执行的变更指令

        Args:
            semantic_diff: 自然语言变更描述
            structured_diff: 预先提供的结构化描述（如有）

        Returns:
            {"type": "...", "files": [...], "operations": [...], "confidence": float, ...}
        """
        # 策略1: 结构化数据优先
        if structured_diff and structured_diff.get("type"):
            return self._parse_structured(structured_diff)

        # 策略2: AI解析
        if self._ai_client or self.ai_provider:
            try:
                ai_result = self._call_ai_parse(semantic_diff)
                if ai_result:
                    return ai_result
            except Exception:
                pass  # fallthrough to rule-based

        # 策略3: 规则匹配回退
        return self._rule_based_parse(semantic_diff)

    def _parse_structured(self, structured: Dict) -> Dict:
        """解析结构化变更描述（置信度最高）"""
        return {
            "type": structured.get("type", "unknown"),
            "files": structured.get("files", []),
            "functions": structured.get("functions",
                structured.get("function", "").split(",") if structured.get("function") else []),
            "description": structured.get("change", structured.get("description", "")),
            "modules": structured.get("modules", []),
            "complexity": structured.get("complexity", "中"),
            "confidence": 0.95,
            "source": "structured",
        }

    def _rule_based_parse(self, text: str) -> Dict:
        """
        基于规则的简易解析（AI不可用时的fallback）

        通过关键词匹配推断变更类型和影响范围。
        """
        result = {
            "type": "unknown",
            "files": [],
            "description": text[:100],
            "confidence": 0.5,
            "source": "rule_based",
        }

        # 1. 提取文件名
        file_pattern = r'[a-zA-Z0-9_/\\-]+\.(?:py|js|ts|html|css|md|yaml|json|ets)'
        files = re.findall(file_pattern, text)
        result["files"] = files[:5] if files else ["unknown"]

        # 2. 推断变更类型
        scores = {}
        for ctype, keywords in self.TYPE_KEYWORDS.items():
            scores[ctype] = sum(1 for kw in keywords if kw in text)

        if scores:
            best_type = max(scores, key=scores.get)
            if scores[best_type] > 0:
                result["type"] = best_type
                result["confidence"] = min(0.65, 0.4 + scores[best_type] * 0.1)

        # 3. 尝试提取函数名
        func_pattern = r'(?:函数|方法|def\s+)([a-zA-Z_][a-zA-Z0-9_]*)'
        funcs = re.findall(func_pattern, text)
        result["functions"] = funcs[:3] if funcs else []

        return result

    def _call_ai_parse(self, text: str) -> Optional[Dict]:
        """
        调用AI API解析语义摘要

        当前为接口占位，实际集成时替换为:
        - OpenAI: openai.ChatCompletion.create()
        - Anthropic: anthropic.messages.create()
        - Ollama: ollama.chat()
        """
        # 接口占位 —— 实际集成时替换
        # if self.ai_provider == "openai":
        #     import openai
        #     response = openai.ChatCompletion.create(
        #         model=self.model,
        #         messages=[{
        #             "role": "system",
        #             "content": "你是一个代码变更解析器。将语义描述转为结构化JSON: "
        #                        '{"type":"feat/fix/refactor/perf","files":[],"description":"..."}'
        #         }, {"role": "user", "content": text}]
        #     )
        #     return json.loads(response.choices[0].message.content)
        return None

    def batch_parse(self, diffs: List[str]) -> List[Dict]:
        """批量解析语义摘要"""
        return [self.parse(d) for d in diffs]
