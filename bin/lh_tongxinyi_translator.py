#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·通心译翻译引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-通心译-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

定位：别人翻译语言，我们翻译灵魂。
抄得走代码，抄不走理解人的能力。

功能：
  1. 多后端翻译（本地Ollama / 在线API / 规则引擎）
  2. 文化锚点保护（专有名词不翻译）
  3. DNA追溯 + 三色审计
  4. 批量翻译 + 流式输出
  5. 翻译记忆库（本地SQLite）
"""

import sys
import re
import json
import hashlib
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Generator
from dataclasses import dataclass, field, asdict
import subprocess

# ============================================================
# 一、配置与文化锚点
# ============================================================

# 文化锚点：这些词不翻译，直接保留（文化主权）
CULTURAL_ANCHORS = {
    "龍魂": "Longhun",
    "龙魂": "Longhun",
    "UID9622": "UID9622",
    "诸葛鑫": "Zhuge Xin",
    "龍芯北辰": "Longxin Beichen",
    "曾仕强": "Zeng Shiqiang",
    "鲲鹏": "Kunpeng",
    "昇腾": "Sheng Teng",
    "河图": "Hetu",
    "洛书": "Luoshu",
    "八卦": "Bagua",
    "五行": "Wuxing",
    "天干": "Tiangan",
    "地支": "Dizhi",
    "CNSH": "CNSH",
}

# 翻译方向
LANG_MAP = {
    "zh": "中文",
    "en": "英文",
    "ja": "日文",
    "ko": "韩文",
    "ru": "俄文",
    "fr": "法文",
    "de": "德文",
    "es": "西班牙文",
    "ar": "阿拉伯文",
}

# ============================================================
# 二、数据结构
# ============================================================

@dataclass
class TranslationResult:
    """翻译结果"""
    source_text: str
    target_text: str
    source_lang: str
    target_lang: str
    engine: str
    confidence: float = 0.0
    elapsed_time: float = 0.0
    dna: str = ""
    audit: str = "🟢"
    anchors_preserved: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


# ============================================================
# 三、翻译引擎核心
# ============================================================

class TongxinyiTranslator:
    """
    通心译翻译引擎
    别人翻译语言，我们翻译灵魂。
    """

    def __init__(
        self,
        db_path: Optional[Path] = None,
        cache_enabled: bool = True,
        ollama_model: str = "qwen2.5:1.5b",
        ollama_base_url: str = "http://localhost:11434",
    ):
        self.cache_enabled = cache_enabled
        self.ollama_model = ollama_model
        self.ollama_base_url = ollama_base_url
        self.db_path = db_path or Path.home() / ".longhun/translations.db"
        self._init_db()
        self._translation_count = 0

    def _init_db(self):
        """初始化翻译记忆库"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS translations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_text TEXT,
                target_text TEXT,
                source_lang TEXT,
                target_lang TEXT,
                engine TEXT,
                confidence REAL,
                dna TEXT,
                audit TEXT,
                created_at TEXT,
                UNIQUE(source_text, source_lang, target_lang)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS anchors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_term TEXT UNIQUE,
                target_term TEXT,
                category TEXT,
                created_at TEXT
            )
        """)
        # 预置文化锚点
        for src, tgt in CULTURAL_ANCHORS.items():
            try:
                conn.execute(
                    "INSERT OR IGNORE INTO anchors (source_term, target_term, category, created_at) VALUES (?, ?, ?, ?)",
                    (src, tgt, "culture", datetime.now().isoformat())
                )
            except:
                pass
        conn.commit()
        conn.close()

    def _generate_dna(self, text: str) -> str:
        """生成DNA追溯码"""
        hash_val = hashlib.sha256(text.encode()).hexdigest()[:8]
        today = datetime.now().strftime("%Y%m%d")
        return f"#龍芯⚡️{today}-通心译-{hash_val}"

    def _three_color_audit(self, confidence: float) -> str:
        """三色审计"""
        if confidence >= 0.85:
            return "🟢"
        elif confidence >= 0.60:
            return "🟡"
        else:
            return "🔴"

    def _preserve_anchors(self, text: str, direction: str = "to_target") -> str:
        """
        保护文化锚点
        direction: "to_target" = 中文→外文, "to_source" = 外文→中文
        """
        if direction == "to_target":
            for src, tgt in CULTURAL_ANCHORS.items():
                text = text.replace(src, tgt)
        else:
            for src, tgt in CULTURAL_ANCHORS.items():
                text = text.replace(tgt, src)
        return text

    def _get_from_cache(self, source_text: str, source_lang: str, target_lang: str) -> Optional[str]:
        """从缓存读取翻译"""
        if not self.cache_enabled:
            return None
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute(
            "SELECT target_text FROM translations WHERE source_text = ? AND source_lang = ? AND target_lang = ?",
            (source_text, source_lang, target_lang)
        )
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None

    def _save_to_cache(self, result: TranslationResult):
        """保存翻译到缓存"""
        if not self.cache_enabled:
            return
        conn = sqlite3.connect(str(self.db_path))
        conn.execute(
            """INSERT OR REPLACE INTO translations
               (source_text, target_text, source_lang, target_lang, engine, confidence, dna, audit, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                result.source_text,
                result.target_text,
                result.source_lang,
                result.target_lang,
                result.engine,
                result.confidence,
                result.dna,
                result.audit,
                datetime.now().isoformat()
            )
        )
        conn.commit()
        conn.close()

    # ---------- 翻译后端 ----------

    def _translate_ollama(self, text: str, source_lang: str, target_lang: str) -> Dict:
        """使用本地Ollama翻译"""
        lang_names = LANG_MAP
        system_prompt = f"""你是通心译，龍魂系统的翻译引擎。别人翻译语言，我们翻译灵魂。

将以下{lang_names.get(source_lang, source_lang)}文本翻译成{lang_names.get(target_lang, target_lang)}。

规则：
1. 保护文化锚点：龍魂、UID9622、诸葛鑫、龙芯北辰、鲲鹏、昇腾、河图、洛书、八卦、五行、天干、地支、CNSH 等词不翻译，直接保留
2. 翻译要保留原文的"魂"——不仅是字面意思，更要传递背后的文化和情感
3. 输出只包含翻译结果，不要添加任何解释
4. 保持原文的语气和风格

原文：{text}"""

        try:
            cmd = [
                "ollama", "run", self.ollama_model,
                "--system", system_prompt,
                text
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                translated = result.stdout.strip()
                # 二次保护：确保锚点未被误翻
                translated = self._preserve_anchors(translated, "to_target")
                return {
                    "text": translated,
                    "engine": f"ollama-{self.ollama_model}",
                    "confidence": 0.85
                }
            else:
                return {"text": text, "engine": "ollama-error", "confidence": 0.3}
        except Exception as e:
            return {"text": text, "engine": "ollama-error", "confidence": 0.2, "error": str(e)}

    def _translate_rule_based(self, text: str, source_lang: str, target_lang: str) -> Dict:
        """基于规则的简单翻译（保底方案）"""
        # 简单处理：保护锚点 + 基础替换
        result = self._preserve_anchors(text, "to_target")
        # 非常基础的英文翻译（仅演示，实际使用需扩展）
        if source_lang == "zh" and target_lang == "en":
            replacements = {
                "你好": "Hello",
                "谢谢": "Thank you",
                "再见": "Goodbye",
                "系统": "System",
                "协议": "Protocol",
                "安全": "Security",
                "审计": "Audit",
                "主权": "Sovereignty",
                "数据": "Data",
                "模型": "Model",
            }
            for zh, en in replacements.items():
                result = result.replace(zh, en)
        return {
            "text": result,
            "engine": "rule-based",
            "confidence": 0.50
        }

    # ---------- 主翻译方法 ----------

    def translate(
        self,
        text: str,
        source_lang: str = "auto",
        target_lang: str = "en",
        engine: str = "auto",
        preserve_anchors: bool = True,
    ) -> TranslationResult:
        """
        主翻译入口

        Args:
            text: 待翻译文本
            source_lang: 源语言 (auto/zh/en/ja/ko/ru/fr/de/es/ar)
            target_lang: 目标语言
            engine: 翻译引擎 (auto/ollama/rule)
            preserve_anchors: 是否保护文化锚点
        """
        start_time = datetime.now()

        # 语言检测（简化）
        if source_lang == "auto":
            # 检测中文字符
            if any('\u4e00' <= c <= '\u9fff' for c in text):
                source_lang = "zh"
            else:
                source_lang = "en"

        # 检查缓存
        cached = self._get_from_cache(text, source_lang, target_lang)
        if cached:
            result = TranslationResult(
                source_text=text,
                target_text=cached,
                source_lang=source_lang,
                target_lang=target_lang,
                engine="cache",
                confidence=0.95,
                elapsed_time=0.0,
                dna=self._generate_dna(text + cached),
                audit="🟢"
            )
            return result

        # 选择翻译引擎
        if engine == "auto":
            # 优先使用Ollama，如果不可用则降级到规则引擎
            try:
                subprocess.run(["ollama", "list"], capture_output=True, timeout=5)
                engine = "ollama"
            except:
                engine = "rule"

        # 执行翻译
        if engine == "ollama":
            raw_result = self._translate_ollama(text, source_lang, target_lang)
        else:
            raw_result = self._translate_rule_based(text, source_lang, target_lang)

        # 构建结果
        translated_text = raw_result.get("text", text)
        confidence = raw_result.get("confidence", 0.5)
        engine_name = raw_result.get("engine", engine)

        elapsed = (datetime.now() - start_time).total_seconds()

        # 最终锚点保护
        if preserve_anchors:
            translated_text = self._preserve_anchors(translated_text, "to_target")

        result = TranslationResult(
            source_text=text,
            target_text=translated_text,
            source_lang=source_lang,
            target_lang=target_lang,
            engine=engine_name,
            confidence=confidence,
            elapsed_time=elapsed,
            dna=self._generate_dna(text + translated_text),
            audit=self._three_color_audit(confidence),
            anchors_preserved=list(CULTURAL_ANCHORS.keys())
        )

        # 保存缓存
        self._save_to_cache(result)
        self._translation_count += 1

        return result

    def translate_batch(
        self,
        texts: List[str],
        source_lang: str = "auto",
        target_lang: str = "en",
        engine: str = "auto",
    ) -> List[TranslationResult]:
        """批量翻译"""
        results = []
        for text in texts:
            if text.strip():
                results.append(self.translate(text, source_lang, target_lang, engine))
        return results

    def translate_stream(
        self,
        text: str,
        source_lang: str = "auto",
        target_lang: str = "en",
        engine: str = "auto",
    ) -> Generator[str, None, None]:
        """
        流式翻译（实时输出）
        用于长文本实时翻译场景
        """
        # 先尝试缓存
        cached = self._get_from_cache(text, source_lang, target_lang)
        if cached:
            yield cached
            return

        # 模拟流式输出
        result = self.translate(text, source_lang, target_lang, engine)
        for char in result.target_text:
            yield char

    def get_stats(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("SELECT COUNT(*) FROM translations")
        total = cur.fetchone()[0]
        cur = conn.execute("SELECT COUNT(*) FROM anchors")
        anchors = cur.fetchone()[0]
        conn.close()
        return {
            "total_translations": total,
            "total_anchors": anchors,
            "session_translations": self._translation_count,
            "cache_enabled": self.cache_enabled,
            "ollama_model": self.ollama_model,
        }


# ============================================================
# 四、命令行接口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·通心译翻译引擎 v1.0\n别人翻译语言，我们翻译灵魂。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础翻译（中文→英文）
  python3 lh_tongxinyi_translator.py "龍魂系统是主权AI"

  # 指定源语言和目标语言
  python3 lh_tongxinyi_translator.py "你好世界" -s zh -t en

  # 批量翻译
  python3 lh_tongxinyi_translator.py -b "文本1" "文本2" "文本3"

  # 使用规则引擎（离线模式）
  python3 lh_tongxinyi_translator.py "系统安全" --engine rule

  # 查看统计信息
  python3 lh_tongxinyi_translator.py --stats

  # 查看文化锚点列表
  python3 lh_tongxinyi_translator.py --anchors
        """
    )

    parser.add_argument(
        "text",
        nargs="?",
        help="待翻译文本"
    )
    parser.add_argument(
        "-s", "--source",
        default="auto",
        help="源语言 (auto/zh/en/ja/ko/ru/fr/de/es/ar)"
    )
    parser.add_argument(
        "-t", "--target",
        default="en",
        help="目标语言 (zh/en/ja/ko/ru/fr/de/es/ar)"
    )
    parser.add_argument(
        "-e", "--engine",
        default="auto",
        choices=["auto", "ollama", "rule"],
        help="翻译引擎 (auto/ollama/rule)"
    )
    parser.add_argument(
        "-b", "--batch",
        nargs="+",
        help="批量翻译（多个文本）"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="显示统计信息"
    )
    parser.add_argument(
        "--anchors",
        action="store_true",
        help="显示文化锚点列表"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以JSON格式输出"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细信息"
    )

    args = parser.parse_args()

    translator = TongxinyiTranslator()

    # 显示统计
    if args.stats:
        stats = translator.get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return

    # 显示锚点
    if args.anchors:
        print("\n📜 文化锚点列表（这些词不翻译，直接保留）")
        print("-" * 50)
        for src, tgt in CULTURAL_ANCHORS.items():
            print(f"  {src} → {tgt}")
        return

    # 批量翻译
    if args.batch:
        results = translator.translate_batch(args.batch, args.source, args.target, args.engine)
        if args.json:
            print(json.dumps([r.to_dict() for r in results], ensure_ascii=False, indent=2))
        else:
            for r in results:
                print(f"\n📝 原文: {r.source_text}")
                print(f"🌐 译文: {r.target_text}")
                print(f"🧬 DNA: {r.dna}")
                print(f"🟢 审计: {r.audit}")
        return

    # 单文本翻译
    if not args.text:
        parser.print_help()
        return

    result = translator.translate(args.text, args.source, args.target, args.engine)

    if args.json:
        print(result.to_json())
    else:
        print("\n" + "=" * 60)
        print("🐉 通心译翻译结果")
        print("=" * 60)
        print(f"📝 原文 ({result.source_lang}): {result.source_text}")
        print(f"🌐 译文 ({result.target_lang}): {result.target_text}")
        print(f"⚙️ 引擎: {result.engine}")
        print(f"📊 置信度: {result.confidence:.0%}")
        print(f"🧬 DNA: {result.dna}")
        print(f"🟢 审计: {result.audit}")
        print(f"⏱️ 耗时: {result.elapsed_time:.2f}s")
        if result.anchors_preserved:
            print(f"🔒 保护锚点: {len(result.anchors_preserved)} 个")
        print("=" * 60)


if __name__ == "__main__":
    main()
