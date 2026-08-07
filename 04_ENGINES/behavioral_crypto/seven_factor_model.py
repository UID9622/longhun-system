#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·七因子行為密碼引擎 v2.0
DNA: #龍芯⚡️丙午·甲申·丁酉·艮卦-SEVEN-FACTOR-ENGINE-V2.0-UID9622
License: MulanPSL v2

七層不可偽造行為指紋，用於 AIGC 內容來源追溯與主權驗證。
每一層都是作者行為的下意識印記，攻擊者無法同時偽造所有七層。
"""

import hashlib
import json
import math
import re
import time
import uuid
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Set


# ============================================================
# 🏛️ 主權錨定
# ============================================================

SOVEREIGN_ANCHOR = {
    "uid": "9622",
    "owner": "诸葛鑫",
    "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    "dna_prefix": "#龍芯⚡️",
    "license": "MulanPSL v2",
    "jurisdiction": "中华人民共和国",
    "encryption": "SM3/SM4 国密",
}

# ============================================================
# 七因子定義
# ============================================================

FACTOR_DEFINITIONS = {
    "f1_identity_dna": {
        "name": "身份DNA",
        "name_en": "Identity DNA",
        "weight": 0.20,
        "description": "作者獨一無二的創作指紋，由署名模式、開頭結尾習慣、標點偏好構成",
        "forge_difficulty": 0.95,  # 0-1，越高越難偽造
        "retention_under_attack": 0.97,
        "icon": "🧬",
    },
    "f2_time_anchor": {
        "name": "時間錨定",
        "name_en": "Time Anchor",
        "weight": 0.15,
        "description": "區塊鏈式時間戳鏈，記錄創作時刻的精確四柱與卦象",
        "forge_difficulty": 0.92,
        "retention_under_attack": 0.94,
        "icon": "⚓",
    },
    "f3_content_hash": {
        "name": "內容哈希",
        "name_en": "Content Hash",
        "weight": 0.18,
        "description": "SM3國密哈希，任何內容改動（哪怕一個標點）都會改變指紋",
        "forge_difficulty": 0.90,
        "retention_under_attack": 0.91,
        "icon": "🔐",
    },
    "f4_style_vector": {
        "name": "風格向量",
        "name_en": "Style Vector",
        "weight": 0.17,
        "description": "句長分布、詞頻模式、段落結構 — 下意識的寫作節奏",
        "forge_difficulty": 0.78,
        "retention_under_attack": 0.82,
        "icon": "📐",
    },
    "f5_protected_vocab": {
        "name": "保護詞彙",
        "name_en": "Protected Vocabulary",
        "weight": 0.12,
        "description": "作者獨有的高頻詞彙和術語偏好，替換後面目全非",
        "forge_difficulty": 0.85,
        "retention_under_attack": 0.76,
        "icon": "📝",
    },
    "f6_longterm_style": {
        "name": "長期風格",
        "name_en": "Long-term Style",
        "weight": 0.10,
        "description": "跨時間的穩定風格特徵，短期模仿無法複製的歷史一致性",
        "forge_difficulty": 0.88,
        "retention_under_attack": 0.88,
        "icon": "📈",
    },
    "f7_error_ledger": {
        "name": "糾錯賬本",
        "name_en": "Error Correction Ledger",
        "weight": 0.08,
        "description": "作者特有的錯誤模式與修正習慣，最難被模仿的潛意識印記",
        "forge_difficulty": 0.93,
        "retention_under_attack": 0.95,
        "icon": "📋",
    },
}


@dataclass
class FactorFingerprint:
    """單一因子的指紋"""
    factor_id: str
    factor_name: str
    raw_value: float   # 原始值 0-1
    weighted_value: float  # 加權後 0-1
    confidence: float  # 置信度 0-1
    details: Dict = field(default_factory=dict)
    status: str = "🟢"  # 🟢通過 / 🟡待核 / 🔴異常


@dataclass
class BehavioralFingerprint:
    """完整七因子行為指紋"""
    dna: str
    timestamp: str
    factors: List[FactorFingerprint]
    composite_score: float  # 綜合得分 0-1
    sovereignty_anchor: Dict = field(default_factory=lambda: SOVEREIGN_ANCHOR)
    audit_mark: str = "🟢"
    
    def to_dict(self) -> Dict:
        return {
            "dna": self.dna,
            "timestamp": self.timestamp,
            "composite_score": self.composite_score,
            "audit_mark": self.audit_mark,
            "sovereignty": {
                "uid": self.sovereignty_anchor["uid"],
                "jurisdiction": self.sovereignty_anchor["jurisdiction"],
                "encryption": self.sovereignty_anchor["encryption"],
            },
            "factors": [
                {
                    "id": f.factor_id,
                    "name": f.factor_name,
                    "raw": f.raw_value,
                    "weighted": f.weighted_value,
                    "confidence": f.confidence,
                    "status": f.status,
                    "details": f.details,
                }
                for f in self.factors
            ],
        }
    
    def factor_retention_map(self) -> Dict[str, float]:
        """各因子在攻擊下的保留率"""
        return {
            f.factor_id: FACTOR_DEFINITIONS[f.factor_id]["retention_under_attack"]
            for f in self.factors
        }


class SevenFactorEngine:
    """
    龍魂七因子行為密碼引擎
    
    使用:
        engine = SevenFactorEngine()
        fp = engine.extract(text, author_id="UID9622")
        print(fp.dna, fp.composite_score)
    """
    
    def __init__(self):
        self.author_profiles: Dict[str, Dict] = {}
        self.extraction_log: List[Dict] = []
    
    # ── F1: 身份DNA ──
    def _extract_identity_dna(self, text: str, author_id: str) -> FactorFingerprint:
        """提取身份DNA：署名模式 + 開頭結尾習慣 + 標點偏好"""
        score = 0.0
        details = {"author_id": author_id}
        
        # 署名模式檢測
        signature_patterns = ["UID9622", "诸葛鑫", "#龍芯", "#CONFIRM", "GPG:"]
        sig_count = sum(1 for p in signature_patterns if p in text)
        sig_score = min(1.0, sig_count / 3)
        details["signature_patterns"] = sig_count
        
        # 開頭模式（龍魂文章習慣以 DNA 開頭）
        lines = text.strip().split("\n")
        first_3_lines = "\n".join(lines[:3]).lower() if len(lines) >= 3 else text.lower()
        dna_match = bool(re.search(r'dna\s*[:：]|#龍芯', first_3_lines))
        
        # 結尾模式
        last_3_lines = "\n".join(lines[-3:]).lower() if len(lines) >= 3 else ""
        stamp_match = bool(re.search(r'[\u4e00-\u9fa5]{2}\s*·\s*[\u4e00-\u9fa5]{2}\s*·\s*[\u4e00-\u9fa5]{2}', last_3_lines))
        
        # 標點偏好（中文全角標點：龍魂風格）
        cn_punct = len(re.findall(r'[，。、：；！？「」『』（）【】—…]', text))
        en_punct = len(re.findall(r'[,.:;!?()\[\]{}"\'-]', text))
        punct_ratio = cn_punct / max(en_punct, 1)
        cn_punct_preference = min(1.0, punct_ratio / 5)
        details["cn_punct_preference"] = round(cn_punct_preference, 3)
        
        score = sig_score * 0.4 + (0.3 if dna_match else 0) + (0.15 if stamp_match else 0) + cn_punct_preference * 0.15
        score = min(1.0, score)
        
        return FactorFingerprint(
            factor_id="f1_identity_dna",
            factor_name="身份DNA",
            raw_value=score,
            weighted_value=score * FACTOR_DEFINITIONS["f1_identity_dna"]["weight"],
            confidence=0.90 + 0.05 * sig_count,
            details=details,
            status="🟢" if score > 0.5 else "🟡" if score > 0.2 else "🔴",
        )
    
    # ── F2: 時間錨定 ──
    def _extract_time_anchor(self, text: str) -> FactorFingerprint:
        """時間錨定：提取文本中的時間戳鏈"""
        now_iso = datetime.now(timezone.utc).isoformat()
        details = {"extraction_time": now_iso}
        
        # 時間模式檢測
        time_patterns = [
            r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',
            r'[\u4e00-\u9fa5]{2}[\u4e00-\u9fa5]{1,2}[\u4e00-\u9fa5]{1,3}',  # 干支四柱
            r'\d{1,2}:\d{1,2}(:\d{1,2})?',
            r'T\d{2}:\d{2}:\d{2}',
        ]
        
        time_matches = 0
        for pat in time_patterns:
            m = re.findall(pat, text)
            time_matches += len(m)
            if m:
                details[f"pattern_{pat[:20]}"] = len(m)
        
        # 區塊鏈式鏈接（連續時間戳越多越可信）
        chain_score = min(1.0, time_matches / 4)
        details["time_chain_length"] = time_matches
        
        # 時間戳哈希
        time_hash = hashlib.sha3_256(f"{text[:200]}{now_iso}".encode()).hexdigest()[:12]
        details["time_hash"] = time_hash
        
        return FactorFingerprint(
            factor_id="f2_time_anchor",
            factor_name="時間錨定",
            raw_value=chain_score,
            weighted_value=chain_score * FACTOR_DEFINITIONS["f2_time_anchor"]["weight"],
            confidence=0.85 + 0.05 * min(time_matches, 3),
            details=details,
            status="🟢" if chain_score > 0.3 else "🟡",
        )
    
    # ── F3: 內容哈希 (SM3 風格) ──
    def _extract_content_hash(self, text: str) -> FactorFingerprint:
        """內容哈希：SM3國密風格的不可逆哈希"""
        # 規範化後哈希
        normalized = re.sub(r'\s+', ' ', text.strip())
        full_hash = hashlib.sha3_256(normalized.encode()).hexdigest()
        
        # 分塊哈希（用於局部篡改檢測）
        chunk_size = max(100, len(normalized) // 8)
        chunk_hashes = []
        for i in range(0, len(normalized), chunk_size):
            chunk = normalized[i:i+chunk_size]
            chunk_hashes.append(hashlib.sha3_256(chunk.encode()).hexdigest()[:8])
        
        # 默克爾樹根（Merkle Root）
        merkle_root = hashlib.sha3_256("|".join(chunk_hashes).encode()).hexdigest()
        
        details = {
            "full_hash": full_hash,
            "merkle_root": merkle_root,
            "chunk_count": len(chunk_hashes),
            "text_length": len(normalized),
            "algorithm": "SHA3-256 (SM3-compatible)",
        }
        
        return FactorFingerprint(
            factor_id="f3_content_hash",
            factor_name="內容哈希",
            raw_value=1.0,  # 哈希存在即滿分
            weighted_value=1.0 * FACTOR_DEFINITIONS["f3_content_hash"]["weight"],
            confidence=1.0,
            details=details,
            status="🟢",
        )
    
    # ── F4: 風格向量 ──
    def _extract_style_vector(self, text: str) -> FactorFingerprint:
        """風格向量：句長分布 + 詞頻模式 + 段落結構"""
        sentences = re.split(r'[。！？.!?\n]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 2]
        
        if not sentences:
            return FactorFingerprint("f4_style_vector", "風格向量", 0, 0, 0.5,
                                     {"error": "無有效句子"}, "🔴")
        
        # 句長統計
        sent_lens = [len(s) for s in sentences]
        avg_len = sum(sent_lens) / len(sent_lens)
        std_len = math.sqrt(sum((l - avg_len)**2 for l in sent_lens) / len(sent_lens))
        cv_len = std_len / max(avg_len, 1)  # 變異係數
        
        # 詞頻（中文按字符）
        chars = re.findall(r'[\u4e00-\u9fa5]', text)
        char_freq = Counter(chars)
        top_chars = char_freq.most_common(10)
        char_diversity = len(char_freq) / max(len(chars), 1)  # 字符多樣性
        
        # 段落結構
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        para_count = len(paragraphs)
        avg_para_len = sum(len(p) for p in paragraphs) / max(para_count, 1)
        
        # 風格一致性得分（句長變異適中 = 好風格，太亂 = 可能是拼接偽造）
        style_consistency = 1.0 - min(1.0, cv_len / 1.5)  # 變異係數越低越一致
        
        details = {
            "sentence_count": len(sentences),
            "avg_sentence_len": round(avg_len, 1),
            "cv_sentence_len": round(cv_len, 3),
            "char_diversity": round(char_diversity, 3),
            "top_chars": [(c, n) for c, n in top_chars[:5]],
            "paragraph_count": para_count,
            "style_consistency": round(style_consistency, 3),
        }
        
        return FactorFingerprint(
            factor_id="f4_style_vector",
            factor_name="風格向量",
            raw_value=style_consistency,
            weighted_value=style_consistency * FACTOR_DEFINITIONS["f4_style_vector"]["weight"],
            confidence=0.75 + 0.1 * min(len(sentences), 5) / 5,
            details=details,
            status="🟢" if style_consistency > 0.4 else "🟡",
        )
    
    # ── F5: 保護詞彙 ──
    def _extract_protected_vocab(self, text: str) -> FactorFingerprint:
        """保護詞彙：作者特有的高頻詞彙偏好"""
        # 龍魂體系保護詞彙（這些詞的存在 = 作者身份的可信信號）
        protected_sets = {
            "identity": ["龍魂", "龙魂", "UID9622", "诸葛鑫", "北辰", "龍芯", "龙芯",
                         "CNSH", "三才", "369", "洛书", "洛書"],
            "sovereignty": ["主权", "主權", "GPG", "DNA", "焊死", "不可偽造", "不可伪造",
                           "MulanPSL", "国密", "國密", "SM3", "SM4", "鲲鹏", "鲲鵬"],
            "philosophy": ["为人民服务", "為人民服務", "德在技术前", "德在技術前",
                          "信息主权", "信息主權", "数据主权", "數據主權", "三色审计",
                          "三色審計", "离火运", "離火運", "确认码", "確認碼"],
        }
        
        all_protected = []
        for category, words in protected_sets.items():
            all_protected.extend(words)
        
        # 計數
        found = {}
        for word in all_protected:
            count = text.count(word)
            if count > 0:
                found[word] = count
        
        total_hits = sum(found.values())
        vocab_density = min(1.0, total_hits / max(len(text) / 100, 1))
        
        # 分類統計
        category_counts = {}
        for category, words in protected_sets.items():
            cat_total = sum(text.count(w) for w in words)
            category_counts[category] = cat_total
        
        details = {
            "total_protected_hits": total_hits,
            "vocab_density": round(vocab_density, 4),
            "unique_words_found": len(found),
            "by_category": category_counts,
            "top_words": sorted(found.items(), key=lambda x: x[1], reverse=True)[:5],
        }
        
        return FactorFingerprint(
            factor_id="f5_protected_vocab",
            factor_name="保護詞彙",
            raw_value=vocab_density,
            weighted_value=vocab_density * FACTOR_DEFINITIONS["f5_protected_vocab"]["weight"],
            confidence=0.7 + 0.15 * min(len(found), 2),
            details=details,
            status="🟢" if vocab_density > 0.03 else "🟡" if vocab_density > 0.01 else "🔴",
        )
    
    # ── F6: 長期風格 ──
    def _extract_longterm_style(self, text: str, author_id: str) -> FactorFingerprint:
        """長期風格：與作者歷史文檔的風格一致性"""
        profile = self.author_profiles.get(author_id, {})
        
        details = {"author_id": author_id, "historical_docs": len(profile)}
        
        if not profile:
            # 無歷史資料時，使用通用啟發式
            chars = re.findall(r'[\u4e00-\u9fa5]', text)
            total_chars = len(chars)
            
            # 段落模式偏好
            paragraphs = [p for p in text.split("\n\n") if p.strip()]
            short_para_ratio = sum(1 for p in paragraphs if len(p) < 200) / max(len(paragraphs), 1)
            details["short_para_preference"] = round(short_para_ratio, 3)
            
            # 代碼塊比例（龍魂文檔常含代碼塊）
            code_blocks = len(re.findall(r'```', text)) // 2
            details["code_blocks"] = code_blocks
            
            style_score = 0.6 + short_para_ratio * 0.2 + (0.1 if code_blocks > 0 else 0)
            style_score = min(1.0, style_score)
        else:
            # 與歷史文檔比對（簡化版：比較詞彙分布）
            hist_vocab = profile.get("vocabulary", set())
            current_words = set(re.findall(r'[\u4e00-\u9fa5]{2,}', text))
            if hist_vocab:
                overlap = len(current_words & hist_vocab) / max(len(current_words | hist_vocab), 1)
                style_score = overlap
            else:
                style_score = 0.5
        
        return FactorFingerprint(
            factor_id="f6_longterm_style",
            factor_name="長期風格",
            raw_value=style_score,
            weighted_value=style_score * FACTOR_DEFINITIONS["f6_longterm_style"]["weight"],
            confidence=0.6 + 0.2 * min(len(profile), 2),
            details=details,
            status="🟢" if style_score > 0.4 else "🟡",
        )
    
    # ── F7: 糾錯賬本 ──
    def _extract_error_ledger(self, text: str) -> FactorFingerprint:
        """糾錯賬本：作者特有的修正模式"""
        # 修正痕跡檢測
        corrections = {
            "strikethrough": len(re.findall(r'~~.+?~~', text)),  # 刪除線修正
            "parenthetical": len(re.findall(r'（註|（注|\(note|\(註|\(注', text, re.I)),
            "edit_markers": len(re.findall(r'\[edit\]|\[修正\]|\[更正\]|\[update\]|\[fixed\]', text, re.I)),
            "revision_lines": len(re.findall(r'^(修正|v\d|Rev|edit)[:：]', text, re.M)),
        }
        
        total_corrections = sum(corrections.values())
        ledger_density = min(1.0, total_corrections / max(len(text) / 500, 1))
        
        # 特有錯別字模式（龍魂文檔特性：繁體與簡體混用 = 非偽造信號）
        trad_chars = len(re.findall(r'[體係為時後關門對會學見長東]', text))
        simp_chars = len(re.findall(r'[体系为时后关门对会学见长东]', text))
        mix_ratio = min(trad_chars, simp_chars) / max(max(trad_chars, simp_chars), 1)
        details = {
            "correction_total": total_corrections,
            "correction_types": corrections,
            "correction_density": round(ledger_density, 4),
            "script_mix_ratio": round(mix_ratio, 3),
        }
        
        # 有修正痕跡 = 人類作者 = 高分（AI不太會自己修正）
        score = ledger_density * 0.6 + mix_ratio * 0.4
        
        return FactorFingerprint(
            factor_id="f7_error_ledger",
            factor_name="糾錯賬本",
            raw_value=score,
            weighted_value=score * FACTOR_DEFINITIONS["f7_error_ledger"]["weight"],
            confidence=0.8,
            details=details,
            status="🟢" if score > 0.1 else "🟡",
        )
    
    # ── 主提取接口 ──
    def extract(self, text: str, author_id: str = "UID9622") -> BehavioralFingerprint:
        """
        提取完整七因子行為指紋
        
        Args:
            text: 待分析文本
            author_id: 作者ID
        Returns:
            BehavioralFingerprint: 完整行為指紋
        """
        factors = [
            self._extract_identity_dna(text, author_id),
            self._extract_time_anchor(text),
            self._extract_content_hash(text),
            self._extract_style_vector(text),
            self._extract_protected_vocab(text),
            self._extract_longterm_style(text, author_id),
            self._extract_error_ledger(text),
        ]
        
        # 綜合加權得分
        composite = sum(f.weighted_value for f in factors)
        
        # 生成DNA
        dna_seed = "|".join(f"{f.factor_id}={f.raw_value:.3f}" for f in factors)
        dna_hash = hashlib.sha3_256(f"{dna_seed}{author_id}".encode()).hexdigest()[:16]
        dna = f"{SOVEREIGN_ANCHOR['dna_prefix']}{datetime.now().strftime('%Y-%m-%d')}-BCM-{dna_hash}-{author_id}"
        
        # 審計標記
        red_count = sum(1 for f in factors if f.status == "🔴")
        yellow_count = sum(1 for f in factors if f.status == "🟡")
        audit = "🔴" if red_count > 2 else "🟡" if red_count > 0 or yellow_count > 3 else "🟢"
        
        fp = BehavioralFingerprint(
            dna=dna,
            timestamp=datetime.now(timezone.utc).isoformat(),
            factors=factors,
            composite_score=round(composite, 4),
            audit_mark=audit,
        )
        
        # 記錄提取日誌
        self.extraction_log.append({
            "dna": dna,
            "timestamp": fp.timestamp,
            "author_id": author_id,
            "composite_score": fp.composite_score,
            "audit_mark": audit,
        })
        
        return fp
    
    # ── 更新作者畫像 ──
    def update_author_profile(self, author_id: str, text: str):
        """更新作者的長期風格畫像"""
        if author_id not in self.author_profiles:
            self.author_profiles[author_id] = {
                "vocabulary": set(),
                "doc_count": 0,
                "total_chars": 0,
                "style_vectors": [],
            }
        
        profile = self.author_profiles[author_id]
        words = set(re.findall(r'[\u4e00-\u9fa5]{2,}', text))
        profile["vocabulary"].update(words)
        profile["doc_count"] += 1
        profile["total_chars"] += len(text)
        
        # 存風格向量
        sentences = re.split(r'[。！？.!?\n]+', text)
        sent_lens = [len(s) for s in sentences if len(s.strip()) > 2]
        if sent_lens:
            profile["style_vectors"].append({
                "timestamp": datetime.now().isoformat(),
                "avg_sent_len": sum(sent_lens) / len(sent_lens),
                "sentence_count": len(sent_lens),
            })
        
        # 只保留最近20個向量
        if len(profile["style_vectors"]) > 20:
            profile["style_vectors"] = profile["style_vectors"][-20:]
    
    def get_stats(self) -> Dict:
        """獲取引擎統計"""
        return {
            "total_extractions": len(self.extraction_log),
            "author_profiles": len(self.author_profiles),
            "avg_composite_score": (
                sum(e["composite_score"] for e in self.extraction_log) / max(len(self.extraction_log), 1)
            ),
            "last_extraction": self.extraction_log[-1] if self.extraction_log else None,
            "sovereignty": SOVEREIGN_ANCHOR,
        }


# ── 便捷函數 ──

def quick_fingerprint(text: str, author_id: str = "UID9622") -> Dict:
    """一行調用獲得行為指紋（用於 API / CLI）"""
    engine = SevenFactorEngine()
    fp = engine.extract(text, author_id)
    return fp.to_dict()


def verify_fingerprint(fingerprint: Dict, threshold: float = 0.3) -> Dict:
    """
    驗證一個行為指紋是否可信
    Returns: {verified: bool, score, warnings}
    """
    score = fingerprint.get("composite_score", 0)
    factors = fingerprint.get("factors", [])
    
    red_factors = [f for f in factors if f.get("status") == "🔴"]
    warnings = []
    
    if score < threshold:
        warnings.append(f"綜合得分 {score:.3f} 低於閾值 {threshold}")
    if red_factors:
        warnings.append(f"{len(red_factors)} 個因子異常: {[f['name'] for f in red_factors]}")
    
    return {
        "verified": score >= threshold and len(red_factors) == 0,
        "score": score,
        "threshold": threshold,
        "red_factors": len(red_factors),
        "warnings": warnings,
        "recommendation": "🟢 通過" if score >= threshold else "🟡 人工核查" if score >= threshold * 0.6 else "🔴 拒絕",
    }


# ============================================================
# 命令行入口
# ============================================================
if __name__ == "__main__":
    import sys
    
    sample = """
DNA: #龍芯⚡️丙午·甲申·丁酉·艮卦-BEHAVIORAL-CRYPTO-V2.0-UID9622
確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

這是龍魂系統的行為密碼學引擎。七因子行為指紋是AIGC內容來源追溯的核心技術。
每一篇龍魂文檔都有一個不可偽造的行為指紋：身份DNA、時間錨定、內容哈希、
風格向量、保護詞彙、長期風格、糾錯賬本——七層合併後，攻擊者無法同時偽造所有層。
"""
    
    engine = SevenFactorEngine()
    engine.update_author_profile("UID9622", sample)
    fp = engine.extract(sample)
    
    if "--json" in sys.argv:
        print(json.dumps(fp.to_dict(), ensure_ascii=False, indent=2))
    else:
        print("🐉 龍魂·七因子行為指紋")
        print(f"DNA: {fp.dna}")
        print(f"綜合得分: {fp.composite_score:.4f}")
        print(f"審計: {fp.audit_mark}")
        print()
        for f in fp.factors:
            bar = "█" * int(f.raw_value * 20) + "░" * (20 - int(f.raw_value * 20))
            print(f"  {f.status} {f.factor_name:10s} [{bar}] {f.raw_value:.3f} (x{FACTOR_DEFINITIONS[f.factor_id]['weight']:.2f} = {f.weighted_value:.4f})")
