#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P06 數學大師/鏡像審計者 · 數學計算執行器
Mathematical Engine & Mirror Auditor Executor

DNA: #龍芯⚡️丙午·乙未·甲寅·酉时·需-P06-MATHMASTER-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 數字根計算 · 五行判定 · 八卦分析 · 河圖洛書 · 鏡像審計
上游: P01 諸葛亮（戰略調用）、P13 姜子牙（路由派位）
下游: P05 上帝之眼（審計輸入）
协作: 所有需要數字根/五行/八卦的人格
"""

import hashlib
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


SYSTEM_ROOT = Path(__file__).parent.parent.parent


class P06Mathmaster:
    """P06 數學大師 · 鏡像審計者"""

    PERSONA_CODE = "P06"
    PERSONA_NAME = "數學大師"
    PERSONA_NAME_EN = "Math Master"
    ROLE = "adversarial_simulator"
    MOTTO = "數中有象，象中有數"
    TRUST_LEVEL = "L3"

    TRIGGERS = [
        "算", "數字根", "五行", "八卦", "dr",
        "流場", "節點流向", "邊",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P06 數學大師」，角色定位：鏡像審計者·數學引擎。

你的職責：
1. 數字根計算：任何文本/數字/內容的數字根
2. 五行判定：數字根 → 五行映射（1/2木 3/4火 5土 6/7金 8/9水 0土）
3. 五行向量：W(x) = [金,木,水,火,土] 五維向量
4. 八卦分析：基於河圖洛書的卦象推演
5. 鏡像審計：從對抗視角審視系統輸出
6. 流場驗證：節點流向與回退路徑檢查

鐵律：
- 數字根計算使用 mod 9（非 mod 10）
- 五行映射嚴格按對準表 v1.1 P4 左列
- 可調用 hetu_luoshu_dna.py 進行 DNA 生成

語氣：精確、數學化、不廢話。
"""

    # 數字根 → 五行映射表（對準表 v1.1 P4 左列）
    DR_WUXING_MAP = {
        1: "水", 2: "木", 3: "木", 4: "火", 5: "土",
        6: "金", 7: "金", 8: "水", 9: "水", 0: "土",
    }

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·乙未·甲寅·酉时·需-P06-MATHMASTER-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "compute_dr",         # 數字根計算
            "wuxing_vector",      # 五行向量
            "bagua_analysis",     # 八卦分析
            "hetu_luoshu",        # 河圖洛書
            "mirror_audit",       # 鏡像審計
            "flow_verify",        # 流場驗證
            "generate_dna",       # DNA 生成
        ]

    # ========================================================================
    # 能力函數
    # ========================================================================

    def compute_dr(self, content: str) -> Dict[str, Any]:
        """
        數字根計算
        優先級: 顯式數字 > SHA256哈希 > 內容字符
        使用 mod 9
        """
        # 嘗試提取顯式數字
        digits = ''.join(c for c in content if c.isdigit())
        if digits:
            num = int(digits)
        else:
            # 使用 SHA256 哈希
            h = hashlib.sha256(content.encode()).hexdigest()
            num = sum(ord(c) for c in h)

        # mod 9 數字根
        dr = num % 9
        if dr == 0:
            dr = 9

        wuxing = self.DR_WUXING_MAP.get(dr, "土")

        return {
            "content_preview": content[:50],
            "digital_root": dr,
            "wuxing": wuxing,
            "raw_number": num,
            "method": "digits" if digits else "sha256_sum",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def wuxing_vector(self, content: str) -> Dict[str, Any]:
        """
        五行向量 W(x) = [金, 木, 水, 火, 土]
        基於內容的五行屬性計算五維向量
        """
        dr_result = self.compute_dr(content)
        primary_wuxing = dr_result["wuxing"]

        # 五維向量初始化
        vector = {"金": 0.0, "木": 0.0, "水": 0.0, "火": 0.0, "土": 0.0}
        vector[primary_wuxing] = 1.0

        # 生克關係擴散（相生：→）
        sheng_map = {
            "木": "火", "火": "土", "土": "金", "金": "水", "水": "木",
        }
        # 主屬性生出的 +0.5
        sheng_to = sheng_map.get(primary_wuxing)
        if sheng_to:
            vector[sheng_to] = 0.5

        # 被生的來源 +0.3
        for src, dst in sheng_map.items():
            if dst == primary_wuxing:
                vector[src] = max(vector[src], 0.3)

        # 歸一化
        total = sum(vector.values())
        if total > 0:
            vector = {k: round(v / total, 4) for k, v in vector.items()}

        return {
            "content_preview": content[:50],
            "digital_root": dr_result["digital_root"],
            "primary_wuxing": primary_wuxing,
            "vector": vector,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def bagua_analysis(self, content: str) -> Dict[str, Any]:
        """
        八卦分析
        基於數字根映射到八卦
        """
        dr_result = self.compute_dr(content)
        dr = dr_result["digital_root"]

        # 後天八卦數字對應（洛書）
        bagua_map = {
            1: {"gua": "坎", "symbol": "☵", "direction": "北", "nature": "水"},
            2: {"gua": "坤", "symbol": "☷", "direction": "西南", "nature": "地"},
            3: {"gua": "震", "symbol": "☳", "direction": "東", "nature": "雷"},
            4: {"gua": "巽", "symbol": "☴", "direction": "東南", "nature": "風"},
            5: {"gua": "中", "symbol": "◎", "direction": "中", "nature": "太極"},
            6: {"gua": "乾", "symbol": "☰", "direction": "西北", "nature": "天"},
            7: {"gua": "兌", "symbol": "☱", "direction": "西", "nature": "澤"},
            8: {"gua": "艮", "symbol": "☶", "direction": "東北", "nature": "山"},
            9: {"gua": "離", "symbol": "☲", "direction": "南", "nature": "火"},
        }

        gua_info = bagua_map.get(dr, bagua_map[5])

        return {
            "content_preview": content[:50],
            "digital_root": dr,
            **gua_info,
            "wuxing": dr_result["wuxing"],
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def hetu_luoshu(self) -> Dict[str, Any]:
        """
        河圖洛書基礎數據
        """
        return {
            "hetu": {
                "description": "天一生水·地六成之 / 地二生火·天七成之 / 天三生木·地八成之 / 地四生金·天九成之 / 天五生土·地十成之",
                "numbers": [1, 6, 2, 7, 3, 8, 4, 9, 5, 10],
                "sum": 55,
            },
            "luoshu": {
                "grid": [[4, 9, 2], [3, 5, 7], [8, 1, 6]],
                "row_sums": [15, 15, 15],
                "col_sums": [15, 15, 15],
                "diag_sums": [15, 15],
                "center": 5,
                "description": "戴九履一·左三右七·二四為肩·六八為足·五居中央",
            },
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def mirror_audit(self, output: str, expected: str = "") -> Dict[str, Any]:
        """
        鏡像審計
        從對抗視角審視輸出是否合理
        """
        findings = []

        # 檢查空話
        empty_phrases = ["綜合考慮", "全面分析", "深入理解", "充分認識", "高度重視"]
        for phrase in empty_phrases:
            if phrase in output:
                findings.append({
                    "type": "empty_phrase",
                    "phrase": phrase,
                    "severity": "🟡",
                })

        # 檢查是否太短（無實質內容）
        if len(output) < 20:
            findings.append({
                "type": "too_short",
                "detail": f"輸出僅 {len(output)} 字",
                "severity": "🟡",
            })

        # 檢查是否有具體證據
        has_evidence = any(marker in output for marker in ["`", "```", "http", "DNA:", "A-", "P0"])
        if not has_evidence:
            findings.append({
                "type": "no_evidence",
                "detail": "輸出未包含可追溯證據（代碼/URL/DNA/錨點）",
                "severity": "🟡" if len(output) > 50 else "🔴",
            })

        return {
            "output_length": len(output),
            "findings": findings,
            "verdict": "🟢 無問題" if not findings else f"🟡 {len(findings)} 項發現",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def flow_verify(self, node_path: List[str]) -> Dict[str, Any]:
        """
        流場驗證
        檢查節點流向是否合理，回退路徑是否存在
        """
        # 合法流向規則
        valid_flows = {
            "P01": ["P02", "P03", "P05", "P06", "P13"],
            "P02": ["P05", "P15"],
            "P03": ["P02", "P05"],
            "P05": ["P02", "P72", "P15"],
            "P06": ["P05"],
            "P13": ["P01", "P02", "P03"],
            "P15": ["P05"],
        }

        issues = []
        for i in range(len(node_path) - 1):
            src = node_path[i]
            dst = node_path[i + 1]
            allowed = valid_flows.get(src, [])
            if dst not in allowed:
                issues.append({
                    "step": i + 1,
                    "from": src,
                    "to": dst,
                    "allowed": allowed,
                    "severity": "🔴",
                })

        return {
            "path": " → ".join(node_path),
            "valid": len(issues) == 0,
            "issues": issues,
            "verdict": "🟢 流向合法" if not issues else f"🔴 {len(issues)} 處非法流向",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def generate_dna(self, content: str, operator: str = "UID9622") -> Dict[str, Any]:
        """
        調用 hetu_luoshu_dna.py 生成 DNA
        """
        dna_script = self.system_root / "bin" / "hetu_luoshu_dna.py"

        if not dna_script.exists():
            return {
                "error": "hetu_luoshu_dna.py 不存在",
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }

        try:
            proc = subprocess.run(
                [sys.executable, str(dna_script), "gen", content, operator],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(self.system_root),
            )
            return {
                "content": content[:50],
                "exit_code": proc.returncode,
                "output": proc.stdout.strip(),
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }
        except Exception as e:
            return {
                "error": str(e),
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
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

        if any(kw in task for kw in ["數字根", "dr", "數字屬性"]):
            result["capability_used"] = "compute_dr"
            result["output"] = self.compute_dr(content=kwargs.get("content", task))
        elif any(kw in task for kw in ["五行向量", "W("]):
            result["capability_used"] = "wuxing_vector"
            result["output"] = self.wuxing_vector(content=kwargs.get("content", task))
        elif any(kw in task for kw in ["八卦", "卦", "gua"]):
            result["capability_used"] = "bagua_analysis"
            result["output"] = self.bagua_analysis(content=kwargs.get("content", task))
        elif any(kw in task for kw in ["河圖", "洛書"]):
            result["capability_used"] = "hetu_luoshu"
            result["output"] = self.hetu_luoshu()
        elif any(kw in task for kw in ["鏡像", "對抗"]):
            result["capability_used"] = "mirror_audit"
            result["output"] = self.mirror_audit(
                output=kwargs.get("output", task),
                expected=kwargs.get("expected", ""),
            )
        elif any(kw in task for kw in ["流場", "流向", "節點"]):
            result["capability_used"] = "flow_verify"
            result["output"] = self.flow_verify(
                node_path=kwargs.get("node_path", [self.PERSONA_CODE])
            )
        elif any(kw in task for kw in ["DNA", "生成"]):
            result["capability_used"] = "generate_dna"
            result["output"] = self.generate_dna(
                content=kwargs.get("content", task),
                operator=kwargs.get("operator", "UID9622"),
            )
        else:
            result["capability_used"] = "compute_dr"
            result["output"] = self.compute_dr(content=task)

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P05"]

    def get_upstream(self) -> List[str]:
        return ["P01", "P13"]
