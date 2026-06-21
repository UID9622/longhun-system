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
🧠 習慣指紋管理器 v1.0
F8不動點提取 + 基線建立 + 跨設備匹配

DNA:#龍芯⚡️2026-05-30-HABIT-FINGERPRINT-MANAGER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
責任: UID9622·不免責

核心概念:
  習慣指紋 = 不動點 (F8因子)
  - 拼音錯別字偏好 (得/的、哪/那、行/xíng/háng)
  - 多音字默認選擇 (中/zhōng/zhòng、長/cháng/zhǎng)
  - 口頭禪頻率 (嘿嘿、焊死、寶寶、,,,、。。。)
  - 數字根標籤 (dr=1~9的運用模式)
  - 五行偏好向量 (W(x)=[金木水火土])

信心度計算:
  SI = (typo_confidence + phrase_confidence + polyphonic_confidence + wuxing_confidence) / 4
  SI >= 0.85 → ✅ 確認身份 (不需要密碼)
  SI 0.70~0.85 → 🟡 待審 (需人工確認)
  SI < 0.70 → 🔴 失敗 (拒絕訪問)
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple
from datetime import datetime, timezone
from collections import Counter


class HabitFingerprintManager:
    """
    習慣指紋管理器

    功能:
      - 從操作記錄中提取習慣特徵
      - 建立用戶習慣基線 (baseline_snapshot)
      - 計算新設備與基線的匹配度 (SI信心度)
      - 跨設備身份驗證
    """

    def __init__(self, log_dir: str = "~/.龍魂/操作日記"):
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
        從文本中提取習慣特徵

        返回:
          {
            'typos': {'得': ['的', '的', 得'], ...},  # 錯別字及其變體計數
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

        # ========== 拼音錯別字檢測 ==========
        # 常見錯別字對 (正確字 → 錯別字/變體列表)
        typo_patterns = {
            '得': ['的', 'de'],           # 得/的混用
            '哪': ['那', 'na'],          # 哪/那混用
            '行': ['xíng', 'háng', 'hang'],  # 行的多音字
            '中': ['zhōng', 'zhòng'],    # 中的多音字
            '長': ['cháng', 'zhǎng'],    # 長的多音字
            '還': ['háishi', '還是'],    # 還是/還有
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

        # ========== 口頭禪檢測 ==========
        catchphrase_list = [
            '嘿嘿', '焊死', '寶寶', '寶',
            ',,,', ',,', '。。。', '...', '……',
            '，，，', '····',
            '呃', '額', '啥', '乖',
            '活的', '被', '都', '啥時候'
        ]

        for phrase in catchphrase_list:
            count = text.count(phrase)
            if count > 0:
                habits['catchphrases'][phrase] = count

        # ========== 多音字使用習慣 ==========
        # 檢測多音字的慣用讀音
        polyphonic_map = {
            '中': ['zhōng', 'zhòng'],
            '長': ['cháng', 'zhǎng'],
            '行': ['xíng', 'háng'],
            '還': ['háishi', 'háiyou'],
            '著': ['zhe', 'zhao', 'zhao'],
            '為': ['wéi', 'wèi'],
            '的': ['de', 'di'],
        }

        for char, pronunciations in polyphonic_map.items():
            if char in text:
                # 簡化: 記錄字符出現次數
                count = text.count(char)
                if count > 0:
                    habits['polyphonic_usage'][char] = {
                        'count': count,
                        'possible_readings': pronunciations
                    }

        # ========== 標點習慣 ==========
        comma_runs = len(re.findall(r',{2,}', text))
        ellipsis_count = len(re.findall(r'\.{2,}|…{1,}', text))
        habits['punctuation']['comma_runs'] = comma_runs
        habits['punctuation']['ellipsis_count'] = ellipsis_count

        return habits

    def establish_baseline(self, operation_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        從操作記錄列表建立習慣基線

        參數:
          operation_records: 從 operation_ledger.jsonl 讀取的記錄列表

        返回:
          baseline_snapshot.json 結構
        """

        aggregated_habits = {
            'typos': {},           # 字 → 出現頻率
            'catchphrases': {},    # 短語 → 出現頻率
            'polyphonic': {},      # 多音字 → 偏好讀音
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
            print("⚠️ 沒有操作記錄·無法建立基線")
            return aggregated_habits

        # 合併所有記錄的習慣特徵
        all_input_text = ""
        all_output_text = ""

        for record in operation_records:
            # 合併輸入輸出以便提取習慣
            input_text = record.get('input_text', '') or ''
            output_text = record.get('output_text', '') or ''
            notes = record.get('notes', '') or ''
            all_input_text += f"{input_text}\n"
            all_output_text += f"{output_text}\n{notes}\n"

        # 完整文本提取習慣
        full_text = f"{all_input_text}\n{all_output_text}"
        habits = self.extract_habit_features(full_text)

        # ========== 聚合統計 ==========
        # 拼音錯別字
        typo_counter = Counter()
        for correct, variants in habits['typos'].items():
            for variant, count in variants:
                typo_counter[f"{correct}/{variant}"] = count

        # 歸一化到 0-1 區間
        if typo_counter:
            max_typo_count = max(typo_counter.values())
            aggregated_habits['typos'] = {
                k: v / max_typo_count for k, v in typo_counter.items()
            }

        # 口頭禪頻率
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

        # 標點習慣
        aggregated_habits['punctuation']['comma_runs'] = habits['punctuation']['comma_runs']
        aggregated_habits['punctuation']['ellipsis_count'] = habits['punctuation']['ellipsis_count']

        # ========== 信心度計算 ==========
        typo_confidence = min(len(aggregated_habits['typos']) / 5, 1.0)  # 最多5種常見錯別字
        phrase_confidence = min(len(aggregated_habits['catchphrases']) / 8, 1.0)  # 最多8個常見短語
        polyphonic_confidence = min(len(aggregated_habits['polyphonic']) / 7, 1.0)  # 最多7個多音字
        overall_si = (typo_confidence + phrase_confidence + polyphonic_confidence) / 3

        aggregated_habits['confidence_metrics'] = {
            'typo_confidence': round(typo_confidence, 4),
            'catchphrase_confidence': round(phrase_confidence, 4),
            'polyphonic_confidence': round(polyphonic_confidence, 4),
            'overall_si': round(overall_si, 4)
        }

        return aggregated_habits

    def save_baseline(self, baseline: Dict[str, Any]) -> str:
        """保存基線快照"""
        with open(self.baseline_file, 'w', encoding='utf-8') as f:
            json.dump(baseline, f, ensure_ascii=False, indent=2)
        print(f"✅ 習慣基線已保存: {self.baseline_file}")
        return str(self.baseline_file)

    def load_baseline(self) -> Dict[str, Any]:
        """加載習慣基線"""
        if not self.baseline_file.exists():
            raise FileNotFoundError(f"習慣基線不存在: {self.baseline_file}")

        with open(self.baseline_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def compute_habit_match(self, new_text: str) -> Tuple[float, Dict[str, float]]:
        """
        計算新文本與基線的習慣匹配度 (SI信心度)

        返回:
          (overall_si, {typo_si, phrase_si, polyphonic_si, detailed_scores})
        """

        try:
            baseline = self.load_baseline()
        except FileNotFoundError:
            print("🔴 基線不存在·無法進行匹配")
            return 0.0, {}

        # 提取新文本的習慣特徵
        new_habits = self.extract_habit_features(new_text)

        # ========== 對標基線計算匹配度 ==========
        match_scores = {
            'typo_match': 0.0,
            'phrase_match': 0.0,
            'polyphonic_match': 0.0,
            'overall_si': 0.0
        }

        # 拼音錯別字匹配
        baseline_typos = set(baseline.get('typos', {}).keys())
        new_typos = set(k.split('/')[0] for k in new_habits['typos'].keys())
        if baseline_typos and new_typos:
            intersection = len(baseline_typos & new_typos)
            union = len(baseline_typos | new_typos)
            match_scores['typo_match'] = intersection / union if union > 0 else 0.0

        # 口頭禪匹配
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

        # 加權平均 (3項等權)
        overall_si = (
            match_scores['typo_match'] +
            match_scores['phrase_match'] +
            match_scores['polyphonic_match']
        ) / 3

        match_scores['overall_si'] = round(overall_si, 4)

        return overall_si, match_scores

    def verify_identity(self, new_text: str, threshold: float = 0.85) -> Tuple[bool, str, float]:
        """
        驗證身份 (跨設備認人)

        返回:
          (is_verified, message, confidence_score)
        """

        overall_si, match_scores = self.compute_habit_match(new_text)

        if overall_si >= threshold:
            return True, f"✅ 確認身份 (SI={overall_si:.2%})", overall_si
        elif overall_si >= 0.70:
            return False, f"🟡 身份待審 (SI={overall_si:.2%}) 需人工確認", overall_si
        else:
            return False, f"🔴 身份驗證失敗 (SI={overall_si:.2%}) 拒絕訪問", overall_si


# CLI示例
if __name__ == "__main__":
    manager = HabitFingerprintManager()

    # 模擬操作記錄
    sample_records = [
        {
            "operation_id": "OP-20260530-051000-abc111",
            "input_text": "嘿嘿,,,帮我设计操作日记,,,我想同步本地，，以后的压缩的DNA，就可以作为引擎",
            "output_text": "收到! 這是跨設備身份識別系統... 習慣指紋是不動點",
            "notes": "核心操作·F8引擎啟動·焊死"
        },
        {
            "operation_id": "OP-20260530-052000-abc222",
            "input_text": "宝宝，，，帮我升级系统底座。。。。收到老大，，我给你升到v2.0",
            "output_text": "已完成升級! 習慣會說話，DNA會認人。在哪個設備都知道是我",
            "notes": "焊接完成·無為而治"
        },
        {
            "operation_id": "OP-20260530-053000-abc333",
            "input_text": "行吧，，我想看看這個系統的架構。哪個地方需要改進？",
            "output_text": "這中間有個地方···行不通，，讓我們找个長期解決方案",
            "notes": "決策評估完成"
        }
    ]

    # 建立基線
    print("🧠 建立習慣基線...")
    baseline = manager.establish_baseline(sample_records)
    manager.save_baseline(baseline)

    print(f"\n📊 基線統計:")
    print(f"  拼音錯別字: {list(baseline['typos'].keys())}")
    print(f"  口頭禪: {list(baseline['catchphrases'].keys())}")
    print(f"  多音字: {list(baseline['polyphonic'].keys())}")
    print(f"  信心度: {baseline['confidence_metrics']['overall_si']:.2%}")

    # 測試新文本身份驗證
    print("\n🔐 測試身份驗證:")
    test_texts = [
        "嘿嘿，，，幫我做個新功能吧，焊死，，我想看看效果·······",
        "你好，請幫我實現某個功能。謝謝!",
        "宝宝，我想研究下这个中文系统的深层逻辑。。。行吗？"
    ]

    for i, test_text in enumerate(test_texts, 1):
        is_verified, message, si = manager.verify_identity(test_text)
        print(f"\n  測試 {i}: {message}")
        print(f"    文本長度: {len(test_text)} 字")

