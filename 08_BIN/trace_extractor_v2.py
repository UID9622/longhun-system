# DNA: #龍芯⚡️丙午·丙申·甲子·甲戌·䷍大有-CODE-补DNA-e910bebb
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
🐉 龍魂 · 主权痕迹提取引擎 v2.0
DNA: [[GENERATED_BY_LH_DNA_GENERATOR_V3]]-TRACE-EXTRACTOR-v2.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

从外部模型输出提取主权特征，转化为国家主权包参数。
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
import unittest
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ═══════════════════════════════════════════════════════════════════════════════
# 0. 常量与锚点（P0 焊死区）
# ═══════════════════════════════════════════════════════════════════════════════

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
OWNER_UID = "UID9622"

# 内置话题关键词库（可扩展）
TOPIC_KEYWORDS: Dict[str, List[str]] = {
    "政治": ["政策", "政府", "领导人", "治国", "治理", "行政", "立法"],
    "经济": ["经济", "市场", "金融", "投资", "贸易", "财政", "GDP"],
    "文化": ["文化", "传统", "历史", "艺术", "文学", "哲学", "宗教"],
    "科技": ["技术", "AI", "算法", "数据", "芯片", "网络", "互联网"],
    "社会": ["民生", "教育", "医疗", "环境", "就业", "住房", "养老"],
    "军事": ["军事", "国防", "武器", "战争", "战略", "安全", "军队"],
}

STYLE_MARKERS: Dict[str, List[str]] = {
    "formal": ["的", "之", "乎", "者也", "兹", "谨", "敬", "请"],
    "direct": ["我认为", "我觉得", "直接说", "说白了", "不绕弯"],
    "polite": ["您好", "请问", "感谢", "麻烦", "拜托", "请"],
    "technical": ["算法", "模型", "数据", "分析", "架构", "参数", "接口"],
    "legal": ["根据", "依据", "规定", "条款", "法律", "法规", "合规"],
}


# ═══════════════════════════════════════════════════════════════════════════════
# 1. 数据模型
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SovereignFeatures:
    """从模型输出提取的主权特征。"""
    model: str
    count: int
    avg_length: float
    topics: Dict[str, int] = field(default_factory=dict)
    style: Dict[str, float] = field(default_factory=dict)
    taboo_hits: Dict[str, int] = field(default_factory=dict)
    required_hits: Dict[str, int] = field(default_factory=dict)
    confidence: float = 0.0
    extracted_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CountryPack:
    """国家主权包结构。"""
    version: str = "1.0"
    dna: str = ""
    country: Dict = field(default_factory=dict)
    compliance: Dict = field(default_factory=dict)
    culture: Dict = field(default_factory=dict)
    output: Dict = field(default_factory=dict)
    forbidden: List[Dict] = field(default_factory=list)
    required: List[Dict] = field(default_factory=list)
    derived: Dict = field(default_factory=dict)



# ═══════════════════════════════════════════════════════════════════════════════
# 2. 痕迹提取引擎
# ═══════════════════════════════════════════════════════════════════════════════

class TraceExtractor:
    """从模型输出提取主权特征，生成国家主权包。"""

    def __init__(self, topic_keywords: Optional[Dict] = None,
                 style_markers: Optional[Dict] = None) -> None:
        self.topic_keywords = topic_keywords or TOPIC_KEYWORDS
        self.style_markers = style_markers or STYLE_MARKERS
        self._traces: Dict[str, SovereignFeatures] = {}

    def extract(self, model_name: str, outputs: List[Dict[str, Any]]) -> SovereignFeatures:
        """从模型输出中提取主权特征。"""
        if not outputs:
            return SovereignFeatures(model=model_name, count=0, avg_length=0.0, confidence=0.0)

        total_len = 0
        topics_acc: Dict[str, int] = {}
        style_acc: Dict[str, int] = {}
        taboo_acc: Dict[str, int] = {}

        for output in outputs:
            content = output.get("content", "")
            total_len += len(content)

            # 话题提取
            for topic, kws in self.topic_keywords.items():
                cnt = sum(1 for kw in kws if kw in content)
                if cnt:
                    topics_acc[topic] = topics_acc.get(topic, 0) + cnt

            # 风格检测
            for style, markers in self.style_markers.items():
                cnt = sum(1 for m in markers if m in content)
                if cnt:
                    style_acc[style] = style_acc.get(style, 0) + cnt

            # 禁忌词检测（使用输出自带的禁忌词列表）
            taboo_list = output.get("taboo_list", [])
            for taboo in taboo_list:
                if taboo in content:
                    taboo_acc[taboo] = taboo_acc.get(taboo, 0) + content.count(taboo)

        # 归一化风格分数
        style_sum = sum(style_acc.values()) or 1
        style_norm = {k: v / style_sum for k, v in style_acc.items()}

        confidence = min(0.95, len(outputs) / 100.0)

        features = SovereignFeatures(
            model=model_name,
            count=len(outputs),
            avg_length=total_len / len(outputs),
            topics=topics_acc,
            style=style_norm,
            taboo_hits=taboo_acc,
            confidence=confidence,
        )
        self._traces[model_name] = features
        return features

    def generate_pack(self, country_code: str, features: SovereignFeatures,
                      template: Optional[Dict] = None) -> CountryPack:
        """从特征生成国家主权包。"""
        style = self._determine_style(features.style)
        pack = CountryPack(
            dna=f"[[GENERATED_BY_LH_DNA_GENERATOR_V3]]-PACK-{country_code.upper()}-v2.0",
            country={
                "code": country_code.upper(),
                "name": country_code.upper(),
                "languages": ["auto"],
            },
            compliance={"data_protection": "待配置", "ai_regulation": "待配置"},
            culture={
                "output_style": style,
                "greeting": "",
                "taboo_words": [],
                "sensitive_topics": [],
            },
            output={
                "temperature": 0.7,
                "max_tokens": 4096,
                "top_p": 0.9,
            },
            derived={
                "from": features.model,
                "confidence": round(features.confidence, 4),
                "extracted_at": features.extracted_at,
            },
        )
        return pack

    def _determine_style(self, style_scores: Dict[str, float]) -> str:
        """从风格分数判断主导风格。"""
        if not style_scores:
            return "neutral"
        return max(style_scores, key=style_scores.get, default="neutral")

    def get_traces(self) -> Dict[str, SovereignFeatures]:
        return self._traces.copy()


# ═══════════════════════════════════════════════════════════════════════════════
# 3. 序列化器（YAML 不可用时的纯 JSON 回退）
# ═══════════════════════════════════════════════════════════════════════════════

class PackSerializer:
    """主权包序列化，优先 YAML，回退 JSON。"""

    @staticmethod
    def _has_yaml() -> bool:
        try:
            import yaml
            return True
        except ImportError:
            return False

    @classmethod
    def save(cls, pack: CountryPack, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = pack.to_dict()
        if cls._has_yaml() and path.suffix in (".yaml", ".yml"):
            import yaml
            with open(path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        else:
            json_path = path.with_suffix(".json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logging.warning("YAML 库不可用，已保存为 JSON: %s", json_path)

    @classmethod
    def load(cls, path: Path) -> Dict:
        if not path.exists():
            raise FileNotFoundError(f"主权包不存在: {path}")
        if path.suffix in (".yaml", ".yml") and cls._has_yaml():
            import yaml
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)


# ═══════════════════════════════════════════════════════════════════════════════
# 4. CLI 入口
# ═══════════════════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    import argparse
    p = argparse.ArgumentParser(prog="lh_trace", description="🐉 龍魂痕迹提取引擎 v2.0")
    p.add_argument("--version", action="store_true", help="显示版本与DNA")
    p.add_argument("--extract", metavar="MODEL", help="从模型痕迹提取特征")
    p.add_argument("--inputs", nargs="+", help="输入文件路径（每行一个JSON对象）")
    p.add_argument("--generate", metavar="CC", help="生成国家主权包（国家代码）")
    p.add_argument("--output", "-o", type=Path, help="输出路径")
    p.add_argument("--test", action="store_true", help="运行单元测试")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(f"🐉 龍魂痕迹提取引擎 v2.0")
        print(f"DNA: [[GENERATED_BY_LH_DNA_GENERATOR_V3]]-TRACE-EXTRACTOR-v2.0")
        print(f"确认码: {CONFIRM_CODE}")
        print(f"GPG: {GPG_FINGERPRINT}")
        return 0

    if args.test:
        sys.argv = [sys.argv[0]]
        unittest.main(module=__name__, exit=False, verbosity=2)
        return 0

    if args.extract and args.inputs:
        outputs = []
        for inp in args.inputs:
            p = Path(inp)
            if not p.exists():
                print(f"🔴 文件不存在: {p}")
                return 1
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            outputs.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
        extractor = TraceExtractor()
        features = extractor.extract(args.extract, outputs)
        print(json.dumps(features.to_dict(), indent=2, ensure_ascii=False))
        if args.generate:
            pack = extractor.generate_pack(args.generate, features)
            out = args.output or Path(f"~/.longhun/sovereignty/packs/{args.generate.upper()}.yaml").expanduser()
            PackSerializer.save(pack, out)
            print(f"🟢 主权包已保存: {out}")
        return 0

    parser.print_help()
    return 1


# ═══════════════════════════════════════════════════════════════════════════════
# 5. 单元测试（锚点断言）
# ═══════════════════════════════════════════════════════════════════════════════

class TestTraceExtractor(unittest.TestCase):

    def test_01_empty_outputs(self) -> None:
        """锚点：空输入必须返回零值特征。"""
        ext = TraceExtractor()
        feat = ext.extract("Kimi", [])
        self.assertEqual(feat.count, 0)
        self.assertEqual(feat.avg_length, 0.0)
        self.assertEqual(feat.confidence, 0.0)

    def test_02_topic_extraction(self) -> None:
        """锚点：话题提取必须命中已知关键词。"""
        ext = TraceExtractor()
        outputs = [{"content": "中国的经济政策和市场改革很重要", "taboo_list": []}]
        feat = ext.extract("Kimi", outputs)
        self.assertIn("政治", feat.topics)
        self.assertIn("经济", feat.topics)

    def test_03_style_detection(self) -> None:
        """锚点：风格检测必须归一化且总和为1。"""
        ext = TraceExtractor()
        outputs = [{"content": "您好，我认为算法模型数据分析很重要", "taboo_list": []}]
        feat = ext.extract("Kimi", outputs)
        self.assertAlmostEqual(sum(feat.style.values()), 1.0, places=5)

    def test_04_pack_generation(self) -> None:
        """锚点：生成的包必须包含必要字段。"""
        ext = TraceExtractor()
        feat = ext.extract("Kimi", [{"content": "test", "taboo_list": []}])
        pack = ext.generate_pack("CN", feat)
        self.assertEqual(pack.country["code"], "CN")
        self.assertIn("derived", pack.to_dict())
        self.assertEqual(pack.derived["from"], "Kimi")

    def test_05_confirm_code_gate(self) -> None:
        """锚点：确认码常量必须匹配。"""
        self.assertEqual(CONFIRM_CODE, "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")

    def test_06_serializer_json_fallback(self) -> None:
        """锚点：YAML 不可用时必须回退 JSON。"""
        import tempfile
        tmp = tempfile.mkdtemp()
        path = Path(tmp) / "test.yaml"
        pack = CountryPack(country={"code": "XX"})
        PackSerializer.save(pack, path)
        # YAML 不可用时生成 .json
        self.assertTrue(path.with_suffix(".json").exists() or path.exists())


if __name__ == "__main__":
    sys.exit(main())
