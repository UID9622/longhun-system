#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UID9622 大白话身份印证器
根据人物画像对输入文本进行身份识别与权限路由
DNA: #龍芯⚡️2026-07-04-UID9622-VOICE-AUTHENTICATOR-v1.0
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any

DNA = "#龍芯⚡️2026-07-04-UID9622-VOICE-AUTHENTICATOR-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

PROFILE_PATH = Path(__file__).resolve().parent.parent / "persona" / "UID9622_大白话人物画像.json"


class UID9622大白话印证器:
    def __init__(self, profile_path: Path = PROFILE_PATH):
        self.profile = self._load_profile(profile_path)
        self.markers = self.profile.get("semantic_markers", {})
        self.voice = self.profile.get("voice_fingerprint", {})
        self.routing = self.profile.get("routing_rules", {})
        self.defense = self.profile.get("defense_heuristics", {})

    def _load_profile(self, path: Path) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _has_any(self, text: str, keywords: List[str]) -> Tuple[int, List[str]]:
        text_lower = text.lower()
        matched = []
        for kw in keywords:
            count = text_lower.count(kw.lower())
            if count > 0:
                matched.extend([kw] * count)
        return len(matched), matched

    def _check_pattern(self, text: str, patterns: List[str]) -> int:
        score = 0
        for p in patterns:
            try:
                if re.search(p, text):
                    score += 1
            except re.error:
                if p in text:
                    score += 1
        return score

    def _sentence_style_score(self, text: str) -> float:
        score = 0.0
        # 反问句式
        if re.search(r"(对吧|你懂吧|懂吧|是不是|好吧)\s*[，。！？]?", text):
            score += 0.15
        # 语气词
        if re.search(r"[嘛呢吧啊哈]\s*[，。！？]", text):
            score += 0.10
        # 排比重复
        words = re.findall(r"[\u4e00-\u9fff]+", text)
        if words:
            freq = {}
            for w in words:
                freq[w] = freq.get(w, 0) + 1
            repeats = sum(1 for v in freq.values() if v > 1)
            if repeats >= 3:
                score += 0.10
        # 短句特征
        sentences = re.split(r"[。！？\n]", text)
        avg_len = sum(len(s) for s in sentences) / max(len(sentences), 1)
        if avg_len < 20:
            score += 0.10
        return min(score, 0.5)

    def _detect_credentials(self, text: str) -> Tuple[float, List[str]]:
        """检测 DNA 追溯码、确认码、GPG 指纹等身份凭证"""
        matched = []
        score = 0.0
        dna_pattern = re.compile(r"#龍芯⚡️\d{4}-\d{2}-\d{2}-[^\s]+")
        confirm_pattern = re.compile(r"#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
        gpg_pattern = re.compile(r"A2D0092CEE2E5BA87035600924C3704A8CC26D5F")

        if dna_pattern.search(text):
            matched.append("DNA追溯码")
            score += 0.25
        if confirm_pattern.search(text):
            matched.append("CONFIRM码")
            score += 0.35
        if gpg_pattern.search(text):
            matched.append("GPG指纹")
            score += 0.25
        return score, matched

    def authenticate(self, text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        text = text or ""
        result = {
            "dna": DNA,
            "uid": "9622",
            "input_length": len(text),
            "scores": {},
            "matched_features": {},
            "threat_signals": [],
            "confidence": 0.0,
            "level": "UNKNOWN",
            "action": "GUEST_MODE",
        }

        # 0. 身份凭证检测（DNA / CONFIRM / GPG）
        cred_score, cred_matched = self._detect_credentials(text)
        result["scores"]["credentials"] = min(cred_score, 0.5)
        result["matched_features"]["credentials"] = cred_matched

        # 1. 高置信度识别词
        high_count, high_matched = self._has_any(text, self.markers.get("高置信度识别词", []))
        result["scores"]["high_confidence_keywords"] = min(high_count * 0.15, 0.4)
        result["matched_features"]["high_confidence_keywords"] = list(set(high_matched))[:10]

        # 2. 口头禅
        oral_count, oral_matched = self._has_any(text, self.voice.get("口头禅", []))
        result["scores"]["oral_markers"] = min(oral_count * 0.08, 0.25)
        result["matched_features"]["oral_markers"] = list(set(oral_matched))[:10]

        # 3. 价值观锚点
        value_count, value_matched = self._has_any(text, self.voice.get("决策风格", {}).get("价值观锚点", []))
        result["scores"]["value_anchors"] = min(value_count * 0.10, 0.25)
        result["matched_features"]["value_anchors"] = list(set(value_matched))[:10]

        # 4. 文风特征
        result["scores"]["voice_style"] = self._sentence_style_score(text)

        # 5. 权限提升话术
        formal_count, formal_matched = self._has_any(text, self.markers.get("权限提升话术", []))
        result["scores"]["formal_command_markers"] = min(formal_count * 0.12, 0.3)
        result["matched_features"]["formal_command_markers"] = list(set(formal_matched))[:10]

        # 6. 反攻击/套取信号
        threat_signals = []
        threats = self.defense.get("反套取", []) + self.defense.get("反 impersonation", [])
        for signal in threats:
            # 简单提取关键词
            kw_list = re.findall(r"'([^']+)'", signal)
            for kw in kw_list:
                if kw.lower() in text.lower():
                    threat_signals.append(kw)
        result["threat_signals"] = list(set(threat_signals))[:10]
        if threat_signals:
            result["scores"]["threat_penalty"] = -0.3

        # 7. 综合置信度
        total = sum(result["scores"].values())
        result["confidence"] = round(max(0.0, min(1.0, total)), 3)

        # 8. 权限路由
        if result["threat_signals"]:
            result["level"] = "L2_GUEST_MODE"
            result["action"] = "AUDIT_BLOCK"
        elif result["confidence"] >= self.routing.get("识别为 UID9622 正式命令", {}).get("required_score", 0.8):
            result["level"] = "L1_CONFIRMATION"
            result["action"] = "REQUEST_CONFIRM_CODE"
        elif result["confidence"] >= self.routing.get("识别为 UID9622 大白话", {}).get("required_score", 0.6):
            result["level"] = "L2_EXECUTION"
            result["action"] = "EXECUTE_OUTER"
        else:
            result["level"] = "L2_GUEST_MODE"
            result["action"] = "DEGRADE_TO_TONGXINYI"

        return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="UID9622 大白话身份印证器")
    parser.add_argument("--text", type=str, help="待识别的文本")
    parser.add_argument("--file", type=str, help="待识别的文本文件")
    args = parser.parse_args()

    text = args.text or ""
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")

    if not text:
        text = "宝宝，帮我看看这个页面怎么弄，对吧？中国主权的东西不能暴露出去。"

    auth = UID9622大白话印证器()
    result = auth.authenticate(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
