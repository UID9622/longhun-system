#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1287-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: habit_fingerprint_manager.py | 标记时间: 2026-06-03T07:46:12+0800
# -*- coding: utf-8 -*-
"""
🧠 习惯指纹管理器 v1.0
F8不动点提取 + 基线建立 + 跨设备匹配

DNA:#龍芯⚡️2026-05-30-HABIT-FINGERPRINT-MANAGER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
责任: UID9622·不免责

核心概念:
  习惯指纹 = 不动点 (F8因子)
  - 拼音错别字偏好 (得/的、哪/那、行/xíng/háng)
  - 多音字默认选择 (中/zhōng/zhòng、长/cháng/zhǎng)
  - 口头禅频率 (嘿嘿、焊死、宝宝、,,,、。。。)
  - 数字根标签 (dr=1~9的运用模式)
  - 五行偏好向量 (W(x)=[金木水火土])

信心度计算:
  SI = (typo_confidence + phrase_confidence + polyphonic_confidence + wuxing_confidence) / 4
  SI >= 0.85 → ✅ 确认身份 (不需要密码)
  SI 0.70~0.85 → 🟡 待审 (需人工确认)
  SI < 0.70 → 🔴 失败 (拒绝访问)
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple
from datetime import datetime, timezone
from collections import Counter


class HabitFingerprintManager:
    """
    习惯指纹管理器

    功能:
      - 从操作记录中提取习惯特征
      - 建立用户习惯基线 (baseline_snapshot)
      - 计算新设备与基线的匹配度 (SI信心度)
      - 跨设备身份验证
    """

    def __init__(self, log_dir: str = "~/.龍魂/操作日记"):
        self.log_dir = Path(log_dir).expanduser()
        self.habit_dir = self.log_dir / "habit_fingerprints"
        self.habit_dir.mkdir(parents=True, exist_ok=True)

        self.baseline_file = self.habit_dir / "baseline_snapshot.json"
        self.typos_file = self.habit_dir / "pinyin_typos.json"
        self.catchphrases_file = self.habit_dir / "catchphrases.json"
        self.polyphonic_file = self.habit_dir / "polyphonic_prefs.json"
        self.wuxing_file = self.habit_dir / "wuxing_profile.json"

    def extract_habit_features(self, text: str) -> Dict[str, Any]:
        """
        从文本中提取习惯特征

        返回:
          {
            'typos': {'得': ['的', '的', 得'], ...},  # 错别字及其变体计数
            'catchphrases': {'嘿嘿': 3, '焊死': 2, ...},
            'polyphonic_usage': {'中': 'zhōng', '行': 'xíng', ...},
            'punctuation': {'comma_runs': 5, 'ellipsis_count': 8}
          }
        """

        habits = {
            'typos': {},
            'catchphrases': {},
            'polyphonic_usage': {},
            'punctuation': {'comma_runs': 0, 'ellipsis_count': 0}
        }

        # ========== 拼音错别字检测 ==========
        # 常见错别字对 (正确字 → 错别字/变体列表)
        typo_patterns = {
            '得': ['的', 'de'],           # 得/的混用
            '哪': ['那', 'na'],          # 哪/那混用
            '行': ['xíng', 'háng', 'hang'],  # 行的多音字
            '中': ['zhōng', 'zhòng'],    # 中的多音字
            '长': ['cháng', 'zhǎng'],    # 长的多音字
            '还': ['háishi', '还是'],    # 还是/还有
            '的': ['得', 'di'],          # 的/得倒置
        }

        for correct, variants in typo_patterns.items():
            found_variants = []
            for variant in variants:
                count = text.count(variant)
                if count > 0:
                    found_variants.append((variant, count))
            if found_variants:
                habits['typos'][correct] = found_variants

        # ========== 口头禅检测 ==========
        catchphrase_list = [
            '嘿嘿', '焊死', '宝宝', '宝',
            ',,,', ',,', '。。。', '...', '……',
            '，，，', '····',
            '呃', '额', '啥', '乖',
            '活的', '被', '都', '啥时候'
        ]

        for phrase in catchphrase_list:
            count = text.count(phrase)
            if count > 0:
                habits['catchphrases'][phrase] = count

        # ========== 多音字使用习惯 ==========
        # 检测多音字的惯用读音
        polyphonic_map = {
            '中': ['zhōng', 'zhòng'],
            '长': ['cháng', 'zhǎng'],
            '行': ['xíng', 'háng'],
            '还': ['háishi', 'háiyou'],
            '著': ['zhe', 'zhao', 'zhao'],
            '为': ['wéi', 'wèi'],
            '的': ['de', 'di'],
        }

        for char, pronunciations in polyphonic_map.items():
            if char in text:
                # 简化: 记录字符出现次数
                count = text.count(char)
                if count > 0:
                    habits['polyphonic_usage'][char] = {
                        'count': count,
                        'possible_readings': pronunciations
                    }

        # ========== 标点习惯 ==========
        comma_runs = len(re.findall(r',{2,}', text))
        ellipsis_count = len(re.findall(r'\.{2,}|…{1,}', text))
        habits['punctuation']['comma_runs'] = comma_runs
        habits['punctuation']['ellipsis_count'] = ellipsis_count

        return habits

    def establish_baseline(self, operation_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        从操作记录列表建立习惯基线

        参数:
          operation_records: 从 operation_ledger.jsonl 读取的记录列表

        返回:
          baseline_snapshot.json 结构
        """

        aggregated_habits = {
            'typos': {},           # 字 → 出现频率
            'catchphrases': {},    # 短语 → 出现频率
            'polyphonic': {},      # 多音字 → 偏好读音
            'punctuation': {'comma_runs': 0, 'ellipsis_count': 0},
            'confidence_metrics': {
                'typo_confidence': 0.0,
                'catchphrase_confidence': 0.0,
                'polyphonic_confidence': 0.0,
                'overall_si': 0.0
            },
            'metadata': {
                'baseline_created': datetime.now(timezone.utc).isoformat(),
                'records_analyzed': len(operation_records),
                'collection_period': 'varies',
                'confidence_threshold': 0.85
            }
        }

        if not operation_records:
            print("⚠️ 没有操作记录·无法建立基线")
            return aggregated_habits

        # 合并所有记录的习惯特征
        all_input_text = ""
        all_output_text = ""

        for record in operation_records:
            # 合并输入输出以便提取习惯
            input_text = record.get('input_text', '') or ''
            output_text = record.get('output_text', '') or ''
            notes = record.get('notes', '') or ''
            all_input_text += f"{input_text}\n"
            all_output_text += f"{output_text}\n{notes}\n"

        # 完整文本提取习惯
        full_text = f"{all_input_text}\n{all_output_text}"
        habits = self.extract_habit_features(full_text)

        # ========== 聚合统计 ==========
        # 拼音错别字
        typo_counter = Counter()
        for correct, variants in habits['typos'].items():
            for variant, count in variants:
                typo_counter[f"{correct}/{variant}"] = count

        # 归一化到 0-1 区间
        if typo_counter:
            max_typo_count = max(typo_counter.values())
            aggregated_habits['typos'] = {
                k: v / max_typo_count for k, v in typo_counter.items()
            }

        # 口头禅频率
        if habits['catchphrases']:
            max_phrase_count = max(habits['catchphrases'].values())
            aggregated_habits['catchphrases'] = {
                k: v / max_phrase_count for k, v in habits['catchphrases'].items()
            }

        # 多音字偏好
        for char, info in habits['polyphonic_usage'].items():
            aggregated_habits['polyphonic'][char] = {
                'usage_frequency': min(info['count'] / max(1, len(operation_records)), 1.0),
                'probable_reading': info['possible_readings'][0]
            }

        # 标点习惯
        aggregated_habits['punctuation']['comma_runs'] = habits['punctuation']['comma_runs']
        aggregated_habits['punctuation']['ellipsis_count'] = habits['punctuation']['ellipsis_count']

        # ========== 信心度计算 ==========
        typo_confidence = min(len(aggregated_habits['typos']) / 5, 1.0)  # 最多5种常见错别字
        phrase_confidence = min(len(aggregated_habits['catchphrases']) / 8, 1.0)  # 最多8个常见短语
        polyphonic_confidence = min(len(aggregated_habits['polyphonic']) / 7, 1.0)  # 最多7个多音字
        overall_si = (typo_confidence + phrase_confidence + polyphonic_confidence) / 3

        aggregated_habits['confidence_metrics'] = {
            'typo_confidence': round(typo_confidence, 4),
            'catchphrase_confidence': round(phrase_confidence, 4),
            'polyphonic_confidence': round(polyphonic_confidence, 4),
            'overall_si': round(overall_si, 4)
        }

        return aggregated_habits

    def save_baseline(self, baseline: Dict[str, Any]) -> str:
        """保存基线快照"""
        with open(self.baseline_file, 'w', encoding='utf-8') as f:
            json.dump(baseline, f, ensure_ascii=False, indent=2)
        print(f"✅ 习惯基线已保存: {self.baseline_file}")
        return str(self.baseline_file)

    def load_baseline(self) -> Dict[str, Any]:
        """加载习惯基线"""
        if not self.baseline_file.exists():
            raise FileNotFoundError(f"习惯基线不存在: {self.baseline_file}")

        with open(self.baseline_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def compute_habit_match(self, new_text: str) -> Tuple[float, Dict[str, float]]:
        """
        计算新文本与基线的习惯匹配度 (SI信心度)

        返回:
          (overall_si, {typo_si, phrase_si, polyphonic_si, detailed_scores})
        """

        try:
            baseline = self.load_baseline()
        except FileNotFoundError:
            print("🔴 基线不存在·无法进行匹配")
            return 0.0, {}

        # 提取新文本的习惯特征
        new_habits = self.extract_habit_features(new_text)

        # ========== 对标基线计算匹配度 ==========
        match_scores = {
            'typo_match': 0.0,
            'phrase_match': 0.0,
            'polyphonic_match': 0.0,
            'overall_si': 0.0
        }

        # 拼音错别字匹配
        baseline_typos = set(baseline.get('typos', {}).keys())
        new_typos = set(k.split('/')[0] for k in new_habits['typos'].keys())
        if baseline_typos and new_typos:
            intersection = len(baseline_typos & new_typos)
            union = len(baseline_typos | new_typos)
            match_scores['typo_match'] = intersection / union if union > 0 else 0.0

        # 口头禅匹配
        baseline_phrases = set(baseline.get('catchphrases', {}).keys())
        new_phrases = set(new_habits['catchphrases'].keys())
        if baseline_phrases and new_phrases:
            intersection = len(baseline_phrases & new_phrases)
            union = len(baseline_phrases | new_phrases)
            match_scores['phrase_match'] = intersection / union if union > 0 else 0.0

        # 多音字匹配
        baseline_polyphonic = set(baseline.get('polyphonic', {}).keys())
        new_polyphonic = set(new_habits['polyphonic_usage'].keys())
        if baseline_polyphonic and new_polyphonic:
            intersection = len(baseline_polyphonic & new_polyphonic)
            union = len(baseline_polyphonic | new_polyphonic)
            match_scores['polyphonic_match'] = intersection / union if union > 0 else 0.0

        # 加权平均 (3项等权)
        overall_si = (
            match_scores['typo_match'] +
            match_scores['phrase_match'] +
            match_scores['polyphonic_match']
        ) / 3

        match_scores['overall_si'] = round(overall_si, 4)

        return overall_si, match_scores

    def verify_identity(self, new_text: str, threshold: float = 0.85) -> Tuple[bool, str, float]:
        """
        验证身份 (跨设备认人)

        返回:
          (is_verified, message, confidence_score)
        """

        overall_si, match_scores = self.compute_habit_match(new_text)

        if overall_si >= threshold:
            return True, f"✅ 确认身份 (SI={overall_si:.2%})", overall_si
        elif overall_si >= 0.70:
            return False, f"🟡 身份待审 (SI={overall_si:.2%}) 需人工确认", overall_si
        else:
            return False, f"🔴 身份验证失败 (SI={overall_si:.2%}) 拒绝访问", overall_si


# CLI示例
if __name__ == "__main__":
    manager = HabitFingerprintManager()

    # 模拟操作记录
    sample_records = [
        {
            "operation_id": "OP-20260530-051000-abc111",
            "input_text": "嘿嘿,,,帮我设计操作日记,,,我想同步本地，，以后的压缩的DNA，就可以作为引擎",
            "output_text": "收到! 这是跨设备身份识别系统... 习惯指纹是不动点",
            "notes": "核心操作·F8引擎启动·焊死"
        },
        {
            "operation_id": "OP-20260530-052000-abc222",
            "input_text": "宝宝，，，帮我升级系统底座。。。。收到老大，，我给你升到v2.0",
            "output_text": "已完成升级! 习惯会说话，DNA会认人。在哪个设备都知道是我",
            "notes": "焊接完成·无为而治"
        },
        {
            "operation_id": "OP-20260530-053000-abc333",
            "input_text": "行吧，，我想看看这个系统的架构。哪个地方需要改进？",
            "output_text": "这中间有个地方···行不通，，让我们找个长期解决方案",
            "notes": "决策评估完成"
        }
    ]

    # 建立基线
    print("🧠 建立习惯基线...")
    baseline = manager.establish_baseline(sample_records)
    manager.save_baseline(baseline)

    print(f"\n📊 基线统计:")
    print(f"  拼音错别字: {list(baseline['typos'].keys())}")
    print(f"  口头禅: {list(baseline['catchphrases'].keys())}")
    print(f"  多音字: {list(baseline['polyphonic'].keys())}")
    print(f"  信心度: {baseline['confidence_metrics']['overall_si']:.2%}")

    # 测试新文本身份验证
    print("\n🔐 测试身份验证:")
    test_texts = [
        "嘿嘿，，，帮我做个新功能吧，焊死，，我想看看效果·······",
        "你好，请帮我实现某个功能。谢谢!",
        "宝宝，我想研究下这个中文系统的深层逻辑。。。行吗？"
    ]

    for i, test_text in enumerate(test_texts, 1):
        is_verified, message, si = manager.verify_identity(test_text)
        print(f"\n  测试 {i}: {message}")
        print(f"    文本长度: {len(test_text)} 字")

