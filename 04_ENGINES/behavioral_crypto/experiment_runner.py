#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂·行為密碼學實驗運行器 v2.0
DNA: #龍芯⚡️丙午·甲申·丁酉·丙午·䷳艮-EXPERIMENT-RUNNER-V2.0-UID9622
License: MulanPSL v2

五級攻擊模擬 → 七因子保留率測試 → 自動生成實驗報告
攻擊級別：L0(無攻擊) → L1(輕微改寫) → L2(風格模仿) → L3(部分偽造) → L4(完全AI重寫)
"""

import copy
import hashlib
import json
import random
import re
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from .seven_factor_model import (
    SevenFactorEngine,
    BehavioralFingerprint,
    FACTOR_DEFINITIONS,
    SOVEREIGN_ANCHOR,
)


# ============================================================
# 攻擊定義
# ============================================================

ATTACK_LEVELS = {
    "L0": {
        "name": "無攻擊",
        "name_en": "No Attack",
        "description": "原始文本，無任何篡改",
        "expected_retention": 1.0,
        "color": "🟢",
    },
    "L1": {
        "name": "輕微改寫",
        "name_en": "Light Rewrite",
        "description": "替換5%詞彙、調整部分標點",
        "expected_retention": 0.85,
        "color": "🟢",
        "mutation_rate": 0.05,
    },
    "L2": {
        "name": "風格模仿",
        "name_en": "Style Imitation",
        "description": "用AI模仿原文風格重寫，保留關鍵詞但改變句法",
        "expected_retention": 0.65,
        "color": "🟡",
        "mutation_rate": 0.30,
    },
    "L3": {
        "name": "部分偽造",
        "name_en": "Partial Forgery",
        "description": "替換50%內容，插入偽造段落，移除時間戳",
        "expected_retention": 0.38,
        "color": "🟡",
        "mutation_rate": 0.50,
    },
    "L4": {
        "name": "完全AI重寫",
        "name_en": "Full AI Rewrite",
        "description": "用另一個AI模型完全重寫，只保留大致意思",
        "expected_retention": 0.12,
        "color": "🔴",
        "mutation_rate": 0.90,
    },
}


# ============================================================
# 文檔語料庫
# ============================================================

CORPUS_TYPES = {
    "philosophy": {
        "name": "哲學/協議",
        "icon": "📜",
        "templates": [
            "龍魂系統的根本原則是為人民服務。數據主權歸用戶，隱私不可傳，零黑箱運行。每一條輸出必須攜帶可追溯DNA碼，中國法律為唯一準繩。",
            "離火運五條底線：德在技術前、路徑對齊、不讓付出者寒心、信息主權不可讓渡、外化內不化。這不是可選項，這是焊死的天條。",
            "三色審計是龍魂系統的核心治理機制。🟢通過、🟡待核、🔴紅線——每一條代碼、每一篇文檔都必須經過三色標記才能發布。",
        ],
    },
    "engineering": {
        "name": "工程/代碼",
        "icon": "⚙️",
        "templates": [
            "# 龍魂·七因子引擎\nDNA: #龍芯⚡️丙午·甲申·丁酉·丙午·䷳艮\n引擎採用SM3國密哈希進行內容簽名，所有代碼路徑經過P05審計。API接口遵循RESTful規範。",
            "def extract_fingerprint(text: str) -> Dict:\n    \"\"\"提取七因子行為指紋\"\"\"\n    engine = SevenFactorEngine()\n    return engine.extract(text).to_dict()\n\n# 所有輸出必須攜帶DNA追溯碼",
        ],
    },
    "article": {
        "name": "文章/博客",
        "icon": "📝",
        "templates": [
            "今天我們來聊聊AIGC的來源追溯問題。當AI生成的內容滿天飛的時候，我們怎麼知道一段文字到底是人寫的還是機器寫的？龍魂行為密碼學給出了答案。",
            "行為密碼學的核心思想很簡單：每個作者在寫作時都會留下無意識的行為印記。這些印記就像指紋一樣獨一無二，AI無法完美模仿。",
        ],
    },
    "legal": {
        "name": "法律/合規",
        "icon": "⚖️",
        "templates": [
            "根據《中華人民共和國數據安全法》和《個人信息保護法》，所有涉及中國公民數據的處理必須在境內進行，且需要明確的用戶授權。",
            "龍魂系統的所有數據處理流程符合等保2.0三級要求。用戶數據採用SM4國密加密存儲，密鑰採用SM2非對稱加密保護。",
        ],
    },
    "dialogue": {
        "name": "對話/輔導",
        "icon": "💬",
        "templates": [
            "老大，你看這個方案怎麼樣？我們先把七因子引擎跑起來，然後接入API，最後做個好看的控制面板。全程自動化，不需要手動操作。",
            "用戶問：我的數據安全嗎？答：絕對安全。龍魂系統採用端到端國密加密，你的數據只在你的設備上和我們的境內服務器上，永遠不會出境。",
        ],
    },
}


# ============================================================
# 攻擊模擬器
# ============================================================

class AttackSimulator:
    """五級攻擊模擬器"""
    
    def __init__(self, seed: int = 42):
        random.seed(seed)
    
    def apply_attack(self, text: str, level: str) -> Tuple[str, Dict]:
        """
        對文本應用指定級別的攻擊
        
        Returns:
            (attacked_text, attack_metadata)
        """
        config = ATTACK_LEVELS.get(level, ATTACK_LEVELS["L0"])
        
        if level == "L0":
            return text, {"level": "L0", "mutations": 0, "note": "無攻擊"}
        
        mutation_rate = config.get("mutation_rate", 0)
        words = text.split()
        
        if not words:
            return text, {"level": level, "mutations": 0, "note": "空文本"}
        
        attacked = words.copy()
        mutation_count = max(1, int(len(words) * mutation_rate))
        mutation_indices = random.sample(range(len(words)), min(mutation_count, len(words)))
        
        mutation_log = []
        
        for idx in mutation_indices:
            if level == "L1":
                # 輕微替換：改變詞序或同義詞
                if random.random() < 0.5 and idx < len(attacked) - 1:
                    attacked[idx], attacked[idx+1] = attacked[idx+1], attacked[idx]
                    mutation_log.append(f"swap[{idx},{idx+1}]")
                else:
                    attacked[idx] = self._synonym_replace(attacked[idx])
                    mutation_log.append(f"replace[{idx}]")
            
            elif level == "L2":
                # 風格模仿：保留關鍵詞但重組句子
                attacked[idx] = self._style_imitate(attacked[idx])
                mutation_log.append(f"imitate[{idx}]")
            
            elif level == "L3":
                # 部分偽造：刪除時間戳、替換內容
                if "DNA" in attacked[idx] or "#龍芯" in attacked[idx]:
                    attacked[idx] = "[REMOVED]"
                    mutation_log.append(f"strip_dna[{idx}]")
                else:
                    attacked[idx] = self._forge_content(attacked[idx])
                    mutation_log.append(f"forge[{idx}]")
            
            elif level == "L4":
                # 完全AI重寫：大幅改變
                attacked[idx] = self._ai_rewrite(attacked[idx])
                mutation_log.append(f"ai_rewrite[{idx}]")
        
        return " ".join(attacked), {
            "level": level,
            "mutations": len(mutation_indices),
            "mutation_rate": mutation_rate,
            "log": mutation_log[:20],
        }
    
    def _synonym_replace(self, word: str) -> str:
        """同義詞替換"""
        synonyms = {
            "的": "之", "是": "為", "和": "與", "但": "然",
            "数据": "信息", "安全": "防護", "系統": "平台",
            "主權": "控制權", "保護": "守護", "算法": "計算方法",
        }
        return synonyms.get(word, word + "_alt")
    
    def _style_imitate(self, word: str) -> str:
        """AI風格模仿"""
        return f"AI_{word}"
    
    def _forge_content(self, word: str) -> str:
        """偽造內容"""
        fake_words = ["fake_data", "偽造內容", "spoofed", "N/A"]
        return random.choice(fake_words)
    
    def _ai_rewrite(self, word: str) -> str:
        """AI完全重寫"""
        return f"gen_{uuid.uuid4().hex[:4]}"


# ============================================================
# 實驗運行器
# ============================================================

@dataclass
class ExperimentResult:
    """單次實驗結果"""
    document_id: str
    corpus_type: str
    attack_level: str
    original_score: float
    attacked_score: float
    retention: float
    factor_retentions: Dict[str, float]
    fingerprint_dna: str
    timestamp: str


class ExperimentRunner:
    """
    批量實驗運行器
    
    使用:
        runner = ExperimentRunner(num_docs=100, seed=42)
        results = runner.run_full_experiment()
        report = runner.generate_report(results)
    """
    
    def __init__(self, num_docs: int = 100, seed: int = 42):
        self.num_docs = num_docs
        self.seed = seed
        self.engine = SevenFactorEngine()
        self.simulator = AttackSimulator(seed=seed)
        self.results: List[ExperimentResult] = []
    
    def _generate_documents(self) -> List[Dict]:
        """生成測試文檔集"""
        random.seed(self.seed)
        docs = []
        
        for i in range(self.num_docs):
            corp_type = random.choice(list(CORPUS_TYPES.keys()))
            template = random.choice(CORPUS_TYPES[corp_type]["templates"])
            
            # 添加隨機變化使每個文檔獨一無二
            variation = f"\n文檔編號: DOC-{i:04d}\n生成時間: {datetime.now().isoformat()}\n"
            
            docs.append({
                "id": f"DOC-{i:04d}",
                "type": corp_type,
                "text": template + variation,
            })
        
        return docs
    
    def run_full_experiment(self) -> List[Dict]:
        """運行完整五級攻擊實驗"""
        docs = self._generate_documents()
        self.results = []
        
        attack_levels = ["L0", "L1", "L2", "L3", "L4"]
        
        for doc in docs:
            # 更新作者畫像
            self.engine.update_author_profile("UID9622", doc["text"])
            
            # 原始指紋
            original_fp = self.engine.extract(doc["text"])
            
            for level in attack_levels:
                # 攻擊
                attacked_text, attack_meta = self.simulator.apply_attack(doc["text"], level)
                
                # 攻擊後指紋
                attacked_fp = self.engine.extract(attacked_text)
                
                # 計算因子級保留率
                factor_retentions = {}
                for orig_f, att_f in zip(original_fp.factors, attacked_fp.factors):
                    if orig_f.raw_value > 0:
                        retention = att_f.raw_value / orig_f.raw_value
                    else:
                        retention = 1.0 if att_f.raw_value == 0 else 0.0
                    retention = min(1.0, max(0.0, retention))
                    factor_retentions[orig_f.factor_id] = round(retention, 4)
                
                # 綜合保留率
                if original_fp.composite_score > 0:
                    retention = attacked_fp.composite_score / original_fp.composite_score
                else:
                    retention = 1.0
                retention = min(1.0, max(0.0, retention))
                
                result = ExperimentResult(
                    document_id=doc["id"],
                    corpus_type=doc["type"],
                    attack_level=level,
                    original_score=original_fp.composite_score,
                    attacked_score=attacked_fp.composite_score,
                    retention=round(retention, 4),
                    factor_retentions=factor_retentions,
                    fingerprint_dna=original_fp.dna,
                    timestamp=datetime.now().isoformat(),
                )
                self.results.append(result)
        
        return [self._result_to_dict(r) for r in self.results]
    
    def _result_to_dict(self, r: ExperimentResult) -> Dict:
        return {
            "document_id": r.document_id,
            "corpus_type": r.corpus_type,
            "attack_level": r.attack_level,
            "original_score": r.original_score,
            "attacked_score": r.attacked_score,
            "retention": r.retention,
            "factor_retentions": r.factor_retentions,
            "fingerprint_dna": r.fingerprint_dna,
            "timestamp": r.timestamp,
        }
    
    def aggregate_by_level(self) -> Dict[str, Dict]:
        """按攻擊級別聚合結果"""
        aggregated = defaultdict(lambda: {
            "scores": [],
            "factor_retentions": defaultdict(list),
            "count": 0,
            "theoretical": 0,
        })
        
        for r in self.results:
            agg = aggregated[r.attack_level]
            agg["scores"].append(r.retention)
            agg["count"] += 1
            agg["theoretical"] = ATTACK_LEVELS[r.attack_level].get("expected_retention", 0)
            for f_id, retention in r.factor_retentions.items():
                agg["factor_retentions"][f_id].append(retention)
        
        result = {}
        for level, agg in sorted(aggregated.items()):
            scores = agg["scores"]
            factor_avgs = {
                f_id: round(sum(vals) / len(vals), 4)
                for f_id, vals in agg["factor_retentions"].items()
            }
            result[level] = {
                "level": level,
                "name": ATTACK_LEVELS[level]["name"],
                "avg_retention": round(sum(scores) / len(scores), 4) if scores else 0,
                "min_retention": round(min(scores), 4) if scores else 0,
                "max_retention": round(max(scores), 4) if scores else 0,
                "theoretical": agg["theoretical"],
                "sample_count": agg["count"],
                "factor_retentions": factor_avgs,
                "passed": round(sum(scores) / len(scores), 4) >= agg["theoretical"] * 0.7 if scores else False,
            }
        
        return result
    
    def aggregate_by_corpus(self) -> Dict[str, Dict]:
        """按語料類型聚合"""
        aggregated = defaultdict(lambda: {"scores": [], "count": 0})
        
        for r in self.results:
            if r.attack_level != "L0":
                aggregated[r.corpus_type]["scores"].append(r.retention)
                aggregated[r.corpus_type]["count"] += 1
        
        result = {}
        for corp, agg in aggregated.items():
            scores = agg["scores"]
            result[corp] = {
                "type": corp,
                "name": CORPUS_TYPES[corp]["name"],
                "icon": CORPUS_TYPES[corp]["icon"],
                "avg_retention": round(sum(scores) / len(scores), 4) if scores else 0,
                "sample_count": agg["count"],
            }
        
        return result
    
    def generate_summary(self) -> Dict:
        """生成實驗總結"""
        by_level = self.aggregate_by_level()
        by_corpus = self.aggregate_by_corpus()
        
        # 最強/最弱因子
        all_factor_retentions = defaultdict(list)
        for r in self.results:
            if r.attack_level != "L0":
                for f_id, retention in r.factor_retentions.items():
                    all_factor_retentions[f_id].append(retention)
        
        factor_ranking = sorted(
            [
                {
                    "id": f_id,
                    "name": FACTOR_DEFINITIONS[f_id]["name"],
                    "avg_retention": round(sum(vals) / len(vals), 4),
                    "icon": FACTOR_DEFINITIONS[f_id]["icon"],
                    "forge_difficulty": FACTOR_DEFINITIONS[f_id]["forge_difficulty"],
                }
                for f_id, vals in all_factor_retentions.items()
            ],
            key=lambda x: x["avg_retention"],
            reverse=True,
        )
        
        # 總體統計
        all_retentions = [r.retention for r in self.results if r.attack_level != "L0"]
        overall_avg = round(sum(all_retentions) / len(all_retentions), 4) if all_retentions else 0
        
        return {
            "experiment_id": f"BCM-EXP-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "total_documents": self.num_docs,
            "total_results": len(self.results),
            "attack_levels": len(ATTACK_LEVELS),
            "corpus_types": len(CORPUS_TYPES),
            "by_level": by_level,
            "by_corpus": by_corpus,
            "factor_ranking": factor_ranking,
            "overall_avg_retention": overall_avg,
            "sovereignty": SOVEREIGN_ANCHOR,
        }


# ============================================================
# 命令行入口
# ============================================================
if __name__ == "__main__":
    import sys
    import json as json_mod
    
    num_docs = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    
    print(f"🐉 龍魂·行為密碼學實驗 v2.0")
    print(f"📊 運行 {num_docs} 篇文檔 × {len(ATTACK_LEVELS)} 級攻擊 = {num_docs * len(ATTACK_LEVELS)} 次測試...")
    
    runner = ExperimentRunner(num_docs=num_docs, seed=42)
    results = runner.run_full_experiment()
    summary = runner.generate_summary()
    
    print(f"\n📊 實驗結果摘要:")
    print(f"  總體平均保留率: {summary['overall_avg_retention']:.2%}")
    
    for level, data in summary["by_level"].items():
        status = "✅" if data["passed"] else "⚠️"
        print(f"  {ATTACK_LEVELS[level]['color']} {level} {data['name']:10s} | 實測: {data['avg_retention']:.2%} | 理論: {data['theoretical']:.2%} | {status}")
    
    print(f"\n🏆 因子抗攻擊排名:")
    for i, f in enumerate(summary["factor_ranking"]):
        bar = "█" * int(f["avg_retention"] * 20)
        print(f"  {i+1}. {f['icon']} {f['name']:8s} [{bar:20s}] {f['avg_retention']:.2%}")
    
    if "--json" in sys.argv:
        output_path = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv and len(sys.argv) > sys.argv.index("--json") + 1 else None
        if output_path:
            import os
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json_mod.dump(summary, f, ensure_ascii=False, indent=2)
            print(f"\n📄 報告已保存: {output_path}")
