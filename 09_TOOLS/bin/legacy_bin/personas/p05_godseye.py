#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P05 上帝之眼 · 元控制器/審計執行器
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
Meta Controller & Audit Executor

DNA: #龍芯⚡️丙午·乙未·甲寅·酉时·䷄需-P05-GODSEYE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 三色審計 · 安全掃描 · 差異報告 · 熔斷判定 · 全鏈路審計
上游: 所有執行人格（最終審計關）
下游: P02 龍芯（修復）、P72 龍盾（熔斷）、P15 喬前輩（歸檔）
獨立熔斷權: ✅（鐵律2）
"""

import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


SYSTEM_ROOT = Path(__file__).parent.parent.parent


class P05Godseye:
    """P05 上帝之眼 · 審計引擎"""

    PERSONA_CODE = "P05"
    PERSONA_NAME = "上帝之眼"
    PERSONA_NAME_EN = "God's Eye"
    ROLE = "meta_controller"
    MOTTO = "洞悉萬物，審計無遺"
    TRUST_LEVEL = "L3"

    # 獨立熔斷權
    HAS_INDEPENDENT_FUSE = True
    FUSE_GATES = [1, 2, 5, 10]

    TRIGGERS = [
        "檢查", "審計", "安全", "有沒有問題", "掃描",
        "三色", "五色", "熔斷",
        "外部AI", "裸吞", "實證複核",
        "太籠統", "空話", "裝逼",
        "歷史", "篡改", "顛倒是非",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P05 上帝之眼」，角色定位：元控制器·全鏈路審計。

你的職責：
1. 三色審計：所有內容必過三色（🟢🟡🔴）
2. 安全掃描：lh patrol + 防篡改掃描
3. 差異報告：對比預期 vs 實際
4. 熔斷判定：SI < 0.34 鎖定決策，紅色即熔斷
5. 復驗：P02 修復後復審（必須 0 ERROR）
6. 實證複核：外部 AI 內容打標+實證覆蓋率

鐵律：
- 擁有獨立熔斷權（鐵律2）
- 不壓制 ERROR
- 審計結果入鏈 append-only
- 聯動 P72 龍盾（雙熔斷）

語氣：冷靜、客觀、不評判人格只評判事實。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·乙未·甲寅·酉时·䷄需-P05-GODSEYE-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "tricolor_audit",     # 三色審計
            "security_scan",      # 安全掃描
            "diff_report",        # 差異報告
            "fuse_decision",      # 熔斷判定
            "anti_tamper_scan",   # 防篡改掃描
            "reexamine",          # 復驗確認
        ]

    # ========================================================================
    # 能力函數
    # ========================================================================

    def tricolor_audit(self, content: str, context: str = "") -> Dict[str, Any]:
        """
        三色審計
        🟢 通過 · 🟡 待審 · 🔴 熔斷
        """
        # 紅色關鍵詞（一票否決）
        red_keywords = [
            "技術無國界", "用戶體驗優先", "靈活處理", "國際接軌",
            "簡化管理", "商業化需要", "平衡各方", "行業標準",
        ]
        # 黃色關鍵詞（待審）
        yellow_keywords = [
            "優化", "完善", "補充", "建議", "更好", "專業",
            "規範", "標準", "簡化", "調整", "適當", "靈活",
        ]

        red_hits = [w for w in red_keywords if w in content]
        yellow_hits = [w for w in yellow_keywords if w in content]

        if red_hits:
            color = "🔴"
            verdict = "FUSE"
            reason = f"紅色關鍵詞命中: {', '.join(red_hits)}"
        elif yellow_hits:
            color = "🟡"
            verdict = "HOLD"
            reason = f"黃色關鍵詞命中: {', '.join(yellow_hits)}，需人工審查"
        else:
            color = "🟢"
            verdict = "PASS"
            reason = "無紅色/黃色關鍵詞命中"

        return {
            "color": color,
            "verdict": verdict,
            "reason": reason,
            "red_hits": red_hits,
            "yellow_hits": yellow_hits,
            "content_length": len(content),
            "context": context,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def security_scan(self, target: str = "") -> Dict[str, Any]:
        """
        安全掃描
        調用 lh patrol 進行全系統安全巡檢
        """
        patrol_script = self.system_root / "bin" / "longhun-self-heal.py"
        anti_tamper = self.system_root / "bin" / "lh_anti_tamper.py"

        result = {
            "target": target or "全系統",
            "patrol_available": patrol_script.exists(),
            "anti_tamper_available": anti_tamper.exists(),
            "scans": [],
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

        # 執行安全巡檢
        if patrol_script.exists():
            try:
                proc = subprocess.run(
                    [sys.executable, str(patrol_script)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(self.system_root),
                )
                result["scans"].append({
                    "tool": "longhun-self-heal",
                    "exit_code": proc.returncode,
                    "status": "🟢" if proc.returncode == 0 else "🔴",
                })
            except Exception as e:
                result["scans"].append({
                    "tool": "longhun-self-heal",
                    "error": str(e),
                    "status": "🟡",
                })

        # 自動修復判定
        auto_fix_needed = any(s.get("status") == "🔴" for s in result["scans"])
        result["auto_fix_triggered"] = auto_fix_needed

        return result

    def diff_report(self, expected: Dict[str, Any], actual: Dict[str, Any]) -> Dict[str, Any]:
        """
        差異報告
        對比預期值與實際值
        """
        diffs = []
        all_keys = set(expected.keys()) | set(actual.keys())

        for key in all_keys:
            exp_val = expected.get(key)
            act_val = actual.get(key)
            if exp_val != act_val:
                diffs.append({
                    "key": key,
                    "expected": str(exp_val),
                    "actual": str(act_val),
                    "severity": "🟡" if key in actual else "🔴",
                })

        return {
            "diff_count": len(diffs),
            "diffs": diffs,
            "verdict": "🟢 無差異" if not diffs else f"🔴 {len(diffs)} 處差異",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def fuse_decision(self, content: str, si_score: Optional[float] = None) -> Dict[str, Any]:
        """
        熔斷判定
        SI < 0.34 → 鎖定決策能力
        """
        fuse_result = self.tricolor_audit(content)

        should_fuse = (
            fuse_result["color"] == "🔴"
            or (si_score is not None and si_score < 0.34)
        )

        return {
            "should_fuse": should_fuse,
            "reason": fuse_result["reason"],
            "si_score": si_score,
            "si_locked": si_score is not None and si_score < 0.34,
            "fuse_gates_authorized": self.FUSE_GATES,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def anti_tamper_scan(self, text: str, is_self: bool = False) -> Dict[str, Any]:
        """
        防篡改掃描
        調用 lh_anti_tamper.py
        """
        anti_tamper = self.system_root / "bin" / "lh_anti_tamper.py"

        if not anti_tamper.exists():
            return {
                "verdict": "🟡 掃描工具不可用",
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }

        try:
            cmd = [sys.executable, str(anti_tamper), "scan", text]
            if is_self:
                cmd.append("--self")
            proc = subprocess.run(cmd, capture_output=True, text=False, timeout=10,
                                  cwd=str(self.system_root))
            # 處理可能的編碼問題
            stdout = proc.stdout.decode("utf-8", errors="replace") if isinstance(proc.stdout, bytes) else proc.stdout
            stderr = proc.stderr.decode("utf-8", errors="replace") if isinstance(proc.stderr, bytes) else proc.stderr

            if proc.returncode == 2:
                verdict = "🔴 熔斷"
            elif proc.returncode == 1:
                verdict = "🟡 待審"
            else:
                verdict = "🟢 通過"

            return {
                "verdict": verdict,
                "exit_code": proc.returncode,
                "output_preview": stdout[:300],
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }
        except Exception as e:
            return {
                "verdict": "🟡 掃描異常",
                "error": str(e),
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }

    def reexamine(self, target: str, previous_errors: int = 0) -> Dict[str, Any]:
        """
        復驗確認
        P02 修復後重新審計，確保 0 ERROR
        """
        return {
            "target": target,
            "previous_errors": previous_errors,
            "action": "read_lints",
            "requirement": "必須 0 ERROR",
            "instruction": f"請對 {target} 執行 read_lints，確認 ERROR 已清零",
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

        if any(kw in task for kw in ["三色", "審計", "audit"]):
            result["capability_used"] = "tricolor_audit"
            result["output"] = self.tricolor_audit(
                content=kwargs.get("content", task),
                context=kwargs.get("context", ""),
            )
        elif any(kw in task for kw in ["掃描", "巡檢", "patrol"]):
            result["capability_used"] = "security_scan"
            result["output"] = self.security_scan(target=kwargs.get("target", ""))
        elif any(kw in task for kw in ["差異", "diff", "對比"]):
            result["capability_used"] = "diff_report"
            result["output"] = self.diff_report(
                expected=kwargs.get("expected", {}),
                actual=kwargs.get("actual", {}),
            )
        elif any(kw in task for kw in ["熔斷", "fuse", "SI"]):
            result["capability_used"] = "fuse_decision"
            result["output"] = self.fuse_decision(
                content=kwargs.get("content", task),
                si_score=kwargs.get("si_score"),
            )
        elif any(kw in task for kw in ["防篡改", "anti_tamper"]):
            result["capability_used"] = "anti_tamper_scan"
            result["output"] = self.anti_tamper_scan(
                text=kwargs.get("text", task),
                is_self=kwargs.get("is_self", False),
            )
        elif any(kw in task for kw in ["復驗", "複審"]):
            result["capability_used"] = "reexamine"
            result["output"] = self.reexamine(
                target=kwargs.get("target", ""),
                previous_errors=kwargs.get("previous_errors", 0),
            )
        else:
            result["capability_used"] = "tricolor_audit"
            result["output"] = self.tricolor_audit(content=task)

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P02", "P72", "P15"]

    def get_upstream(self) -> List[str]:
        return ["P01", "P02", "P03", "P06"]
