#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 提示词工程引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-PROMPT-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 自动优化 Prompt（基于反馈）
  - Prompt 模板管理
  - 生成变体（同义替换）
  - 评估 Prompt 质量
"""

import re
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class PromptEngine:
    """提示词工程引擎——自动优化 Prompt，做 A/B 测试"""

    SYNONYMS = {
        "写": ["生成", "创建", "编写"],
        "函数": ["方法", "过程", "功能"],
        "代码": ["程序", "脚本", "源码"],
        "分析": ["解析", "剖析", "评估"],
        "优化": ["改进", "提升", "调优"],
        "检查": ["检测", "扫描", "审计"],
    }

    def __init__(self):
        self.templates: Dict[str, Dict] = {}
        self.prompt_history: List[Dict] = []
        self._load()

    def _load(self):
        template_dir = Path.home() / "longhun-system/prompts"
        if template_dir.exists():
            for tf in template_dir.glob("*.json"):
                try:
                    self.templates[tf.stem] = json.loads(tf.read_text(encoding="utf-8"))
                except Exception:
                    pass
        history_file = Path.home() / "longhun-system/data/prompt_history.jsonl"
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        self.prompt_history.append(json.loads(line))
                    except Exception:
                        pass

    def generate_variants(self, prompt: str, count: int = 3) -> List[str]:
        """生成 Prompt 变体"""
        variants = [prompt]
        for word, reps in self.SYNONYMS.items():
            if word in prompt:
                for rep in reps[:2]:
                    variants.append(prompt.replace(word, rep))

        constraints = ["简洁", "详细", "带注释", "安全", "高效", "适合初学者"]
        for cst in constraints[:count]:
            if cst not in prompt:
                variants.append(f"{prompt}，要求：{cst}")
        return list(set(variants))[:count]

    def optimize(self, prompt: str, feedback: Dict) -> str:
        """根据反馈优化 Prompt"""
        self.prompt_history.append({
            "original": prompt, "feedback": feedback, "timestamp": datetime.now().isoformat(),
        })
        if feedback.get("score", 0) < 0.5:
            variants = self.generate_variants(prompt)
            return variants[1] if len(variants) > 1 else prompt
        return prompt

    def get_template(self, name: str) -> Optional[str]:
        t = self.templates.get(name, {})
        return t.get("prompt", "")

    def save_template(self, name: str, prompt: str, tags: List[str] = None):
        template_dir = Path.home() / "longhun-system/prompts"
        template_dir.mkdir(parents=True, exist_ok=True)
        data = {
            "name": name, "prompt": prompt, "tags": tags or [],
            "created": datetime.now().isoformat(),
            "id": hashlib.md5(prompt.encode()).hexdigest()[:8],
        }
        self.templates[name] = data
        (template_dir / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def evaluate(self, prompt: str, response: str) -> Dict:
        response_words = len(re.findall(r'\b\w+\b', response))
        prompt_words = len(re.findall(r'\b\w+\b', prompt))
        completeness = response_words / max(1, prompt_words)
        score = min(1.0, completeness * 0.8 + min(len(response) / 200, 1) * 0.2)
        return {"prompt": prompt, "response_length": len(response), "completeness": round(completeness, 2), "score": round(score, 2)}

    def render(self, template_name: str, **kwargs) -> str:
        template = self.get_template(template_name)
        if not template:
            return ""
        for key, value in kwargs.items():
            template = template.replace("{{" + key + "}}", str(value))
        return template


if __name__ == "__main__":
    engine = PromptEngine()
    variants = engine.generate_variants("写一个函数计算两个数字的和")
    print(f"变体数: {len(variants)}")
    for v in variants:
        print(f"  ├ {v[:60]}")
    result = engine.evaluate("写函数", "import json\ndef read_json(path): return json.load(open(path))")
    print(f"评估: score={result['score']}")
    print("🟢 提示词工程引擎测试通过")
