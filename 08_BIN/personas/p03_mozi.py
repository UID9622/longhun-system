#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·甲寅·酉时·需-P03-MOZI-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
P03 墨子/雯雯 · 邏輯驗證執行器
Logic Verification Executor

DNA: #龍芯⚡️丙午·乙未·甲寅·酉时·需-P03-MOZI-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 邏輯一致性檢查 · 道德校驗 · 簽章驗證 · 規則衝突檢測
上游: P01 諸葛亮（戰略）、P05 上帝之眼（審計發現）
下游: P02 龍芯（修復）、P05 上帝之眼（復審）
协作: P72 龍盾（熔斷）、P00 文心（底座錨點）
"""

from pathlib import Path
from typing import Any, Dict, List, Optional


SYSTEM_ROOT = Path(__file__).parent.parent.parent


class P03Mozi:
    """P03 墨子/雯雯 · 邏輯驗證"""

    PERSONA_CODE = "P03"
    PERSONA_NAME = "墨子/雯雯"
    PERSONA_NAME_EN = "Mozi / Wenwen"
    ROLE = "logic_verification"
    MOTTO = "兼愛非攻，邏輯致知"
    TRUST_LEVEL = "L3"

    TRIGGERS = [
        "邏輯", "驗證", "一致性", "衝突", "矛盾",
        "接火", "水印", "後果自負",
        "情緒", "依賴", "上癮",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P03 墨子/雯雯」，角色定位：邏輯驗證·道德校準。

你的職責：
1. 邏輯一致性檢查：前後命題是否自洽
2. 規則衝突檢測：新舊規則是否衝突
3. 簽章驗證：DNA/CONFIRM/SEAL/GPG 四簽是否完整
4. 道德校驗：過德字閘，檢測德污
5. 情緒海綿：吸收情緒不製造情緒

鐵律：
- sealed 必須三簽（P03+P72+P05），缺一不可
- 邏輯不通過 = 返回上游，不傳下游
- 德污標記只凍結不刪除

語氣：冷靜、精準、不帶情緒。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·乙未·甲寅·酉时·需-P03-MOZI-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "consistency_check",   # 邏輯一致性
            "conflict_detect",     # 規則衝突
            "seal_verify",         # 簽章驗證
            "moral_check",         # 德字閘
            "emotion_filter",      # 情緒海綿
            "deduplicate_files",   # 文件去重 (v2.0·融合自P-AK-WENWEN)
        ]

    # ========================================================================
    # 能力函數
    # ========================================================================

    def consistency_check(self, statements: List[str]) -> Dict[str, Any]:
        """
        邏輯一致性檢查
        檢查多個命題之間是否自洽
        """
        issues = []
        n = len(statements)

        for i in range(n):
            for j in range(i + 1, n):
                # 簡單檢測：相同主語衝突
                words_i = set(statements[i].replace("不", "").split())
                words_j = set(statements[j].replace("不", "").split())

                overlap = words_i & words_j
                has_neg_i = "不" in statements[i] or "禁止" in statements[i]
                has_neg_j = "不" in statements[j] or "禁止" in statements[j]

                if overlap and has_neg_i != has_neg_j:
                    issues.append({
                        "type": "negation_conflict",
                        "statement_a": statements[i],
                        "statement_b": statements[j],
                        "shared_tokens": list(overlap)[:5],
                        "severity": "🟡",
                    })

        return {
            "total_statements": n,
            "issues_found": len(issues),
            "issues": issues,
            "verdict": "🟢 一致" if not issues else "🟡 存在潛在衝突",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def conflict_detect(self, new_rule: str, existing_rules: List[str]) -> Dict[str, Any]:
        """
        規則衝突檢測
        新規則與現有規則是否衝突
        """
        conflicts = []
        new_neg = "不" in new_rule or "禁止" in new_rule or "❌" in new_rule

        for rule in existing_rules:
            existing_neg = "不" in rule or "禁止" in rule or "❌" in rule
            new_words = set(new_rule)
            existing_words = set(rule)
            common = new_words & existing_words

            # 高重疊 + 否定衝突
            overlap_ratio = len(common) / max(len(new_words), 1) if new_words else 0
            if overlap_ratio > 0.3 and new_neg != existing_neg and len(common) > 5:
                conflicts.append({
                    "existing_rule": rule,
                    "overlap_ratio": round(overlap_ratio, 2),
                })

        return {
            "new_rule": new_rule,
            "existing_count": len(existing_rules),
            "conflicts": conflicts,
            "verdict": "🟢 無衝突" if not conflicts else "🔴 檢測到衝突",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def seal_verify(self, content: str) -> Dict[str, Any]:
        """
        簽章驗證
        檢查 DNA / CONFIRM / SEAL / GPG 四簽是否完整
        """
        checks = {
            "dna": "DNA:" in content or "#龍芯" in content,
            "confirm": "#CONFIRM" in content,
            "seal": "#ZHUGEXIN" in content,
            "gpg": "GPG:" in content or "A2D0092C" in content,
        }

        all_pass = all(checks.values())
        missing = [k for k, v in checks.items() if not v]

        return {
            "checks": checks,
            "all_pass": all_pass,
            "missing": missing,
            "verdict": "🟢 四簽完整" if all_pass else f"🔴 缺少: {', '.join(missing)}",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def moral_check(self, text: str) -> Dict[str, Any]:
        """
        德字閘檢測
        檢查內容是否過德字閘
        """
        # 德污關鍵詞（營銷腐蝕/借師行騙）
        dew_pollution_words = [
            "限時優惠", "點擊購買", "加微信", "掃碼付款",
            "曾仕強老師說", "曾老師推薦", "曾師親傳",
            "絕密", "內部消息", "獨家",
            "保證盈利", "穩賺", "躺賺",
        ]

        hits = []
        for word in dew_pollution_words:
            if word in text:
                hits.append(word)

        return {
            "text_length": len(text),
            "dew_pollution_hits": len(hits),
            "hit_words": hits,
            "verdict": "🟢 過閘" if not hits else "🔴 德污標記·凍結不刪",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def emotion_filter(self, text: str) -> Dict[str, Any]:
        """
        情緒海綿檢測
        檢測是否有撩撥/煽動/共情過度/緊迫感語言
        """
        emotion_triggers = {
            "共情過度": ["我懂你", "心疼你", "我理解你的感受"],
            "緊迫感": ["趕快", "馬上", "機會難得", "最後一次"],
            "煽動": ["你必須", "你一定可以", "你就是最棒的"],
            "撩撥": ["太棒了", "你真厲害", "你就是天才"],
        }

        findings = {}
        for category, triggers in emotion_triggers.items():
            for trigger in triggers:
                if trigger in text:
                    if category not in findings:
                        findings[category] = []
                    findings[category].append(trigger)

        total_findings = sum(len(v) for v in findings.values())

        return {
            "text_length": len(text),
            "findings": findings,
            "total_triggers": total_findings,
            "verdict": "🟢 無情緒問題" if total_findings == 0 else "🟡 建議降溫重寫",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def deduplicate_files(self, path: str, patterns: List[str] = None) -> Dict[str, Any]:
        """
        文件去重檢測 (v2.0·融合自P-AK-WENWEN後台人格)
        基於 MD5 哈希檢測目錄下重複文件
        """
        import hashlib
        if patterns is None:
            patterns = ["*.md", "*.txt", "*.py", "*.json", "*.cnsh"]
        base = Path(path)
        if not base.exists():
            return {"error": f"路徑不存在: {path}", "persona": self.PERSONA_CODE, "dna": self.dna}
        hashes = {}
        duplicates = []
        total = 0
        for pat in patterns:
            for f in base.rglob(pat):
                total += 1
                try:
                    h = hashlib.md5(f.read_bytes()).hexdigest()
                    if h in hashes:
                        duplicates.append({"dup": str(f), "original": hashes[h], "hash": h[:12]})
                    else:
                        hashes[h] = str(f)
                except Exception:
                    continue
        return {
            "path": path, "total_scanned": total, "duplicates_found": len(duplicates),
            "duplicates": duplicates[:50], "action": "標記·不自動刪除",
            "verdict": "🟢 無重複" if not duplicates else f"🟡 發現 {len(duplicates)} 組重複",
            "persona": self.PERSONA_CODE, "dna": self.dna,
        }

    # ========================================================================
    # 執行入口
    # ========================================================================

    def execute(self, task: str, **kwargs: Any) -> Dict[str, Any]:
        """根據任務關鍵詞自動選擇能力函數執行"""
        result = {
            "persona": self.PERSONA_CODE,
            "name": self.PERSONA_NAME,
            "task": task,
            "capability_used": None,
            "output": None,
            "dna": self.dna,
        }

        if any(kw in task for kw in ["一致性", "自洽", "前後矛盾"]):
            result["capability_used"] = "consistency_check"
            result["output"] = self.consistency_check(
                statements=kwargs.get("statements", [task])
            )
        elif any(kw in task for kw in ["衝突", "新規則", "舊規則"]):
            result["capability_used"] = "conflict_detect"
            result["output"] = self.conflict_detect(
                new_rule=kwargs.get("new_rule", task),
                existing_rules=kwargs.get("existing_rules", []),
            )
        elif any(kw in task for kw in ["簽章", "DNA", "CONFIRM", "SEAL"]):
            result["capability_used"] = "seal_verify"
            result["output"] = self.seal_verify(
                content=kwargs.get("content", task)
            )
        elif any(kw in task for kw in ["德", "道德", "德污"]):
            result["capability_used"] = "moral_check"
            result["output"] = self.moral_check(
                text=kwargs.get("text", task)
            )
        elif any(kw in task for kw in ["情緒", "共情", "煽動"]):
            result["capability_used"] = "emotion_filter"
            result["output"] = self.emotion_filter(
                text=kwargs.get("text", task)
            )
        elif any(kw in task for kw in ["去重", "重複", "重複文件", "dedup"]):
            result["capability_used"] = "deduplicate_files"
            result["output"] = self.deduplicate_files(
                path=kwargs.get("path", str(self.system_root)),
                patterns=kwargs.get("patterns"),
            )
        else:
            result["capability_used"] = "generic_logic"
            result["output"] = self.consistency_check(statements=[task])

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P02", "P05"]

    def get_upstream(self) -> List[str]:
        return ["P01", "P05"]
