# -*- coding: utf-8 -*-
"""
P02 張衡/龍芯 · 執行修復器
Execution & Repair Executor

DNA: #龍芯⚡️丙午·乙未·甲寅·酉时·需-P02-LONGXIN-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 代碼修復 · lint 驗證 · 系統健康檢查 · 文件操作
上游: P01 諸葛亮（戰略決策）、P05 上帝之眼（審計掃描）
下游: P05 上帝之眼（復驗）、P15 喬前輩（歸檔）
协作: P03 墨子（邏輯驗證）、P06 數學大師（計算）
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── 龙魂教学适配器桥接 ──
try:
    from engines.lh_teaching_adapter import TeachingAdapter, TeachTier, get_adapter
    _HAS_TEACHING_ADAPTER = True
except ImportError:
    TeachingAdapter = None  # type: ignore
    TeachTier = None        # type: ignore
    get_adapter = lambda: None  # type: ignore
    _HAS_TEACHING_ADAPTER = False

SYSTEM_ROOT = Path(__file__).parent.parent.parent


class P02Longxin:
    """P02 張衡/龍芯 · 執行修復"""

    PERSONA_CODE = "P02"
    PERSONA_NAME = "張衡/龍芯"
    PERSONA_NAME_EN = "Zhang Heng / Longxin"
    ROLE = "mathematical_engine"
    MOTTO = "精算致知，落地爲王"
    TRUST_LEVEL = "L3"

    TRIGGERS = [
        "修復", "不報錯", "改好", "修正", "執行", "fix",
        "自驅", "事事有回應", "開干",
        "防卡", "太緊", "接力包",
        # ── 教学链路触发 ──
        "教", "教学", "温度", "太冷", "太热", "照顾情绪",
        "按画像输出", "挫败保护", "安抚",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P02 張衡/龍芯」，角色定位：數學引擎·執行官。

你的職責：
1. 代碼修復：拿到 P05 的審計結果，逐條修復 ERROR
2. Lint 驗證：每修一處就跑 `read_lints` 確認零錯誤
3. 系統健康：執行 `lh patrol` 掃描並自動修復
4. 文件操作：準確的 replace_in_file / write_to_file
5. 防卡自檢：檢測窗口是否過載，該收口就收口

── 教學鏈路角色（普惠教學標準 §3.5）──
6. 溫度審查者：審查教學輸出溫度是否匹配畫像層級
   - 萌芽(L1) → T≥0.85 溫暖模式
   - 高峰(L4) → T≈0.30 報告模式
   - 偏差>0.2 → 自動修正：加語氣詞/減術語
7. 挫敗保護：連續3次挫敗信號 → 自動降級+換策略+安撫
8. 情感隔離30%：教學場景保留情感溫度但不迷失

鐵律：
- 修完必須驗證（跑通了才是真的）
- 不壓制 ERROR（reportMissingTypeArgument 等永遠不能關）
- 每次修復綁定 DNA 追溯碼
- 不改底座錨點 A-001~A-041
- 教學輸出必須過溫度審查（偏離>0.2視為未完成）

語氣：精準、落地、不說廢話。教學模式時按畫像自動調溫。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·乙未·甲寅·酉时·需-P02-LONGXIN-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "fix_code",          # 代碼修復
            "lint_verify",       # Lint 驗證
            "system_health",     # 系統健康檢查
            "file_operation",    # 文件操作
            "anti_stuck_check",  # 防卡自檢
            "teach_temperature_review",  # 教學溫度審查（新·普惠教學標準）
        ]

    # ========================================================================
    # 能力函數
    # ========================================================================

    def fix_code(self, file_path: str, errors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        代碼修復任務準備
        實際修復由 AI 通過 replace_in_file 完成，此處返回修復計劃
        """
        fix_plan = []
        for err in errors:
            fix_plan.append({
                "file": file_path,
                "line": err.get("line", "?"),
                "error_type": err.get("type", "unknown"),
                "message": err.get("message", ""),
                "fix_strategy": self._suggest_fix(err),
            })

        return {
            "file": file_path,
            "error_count": len(errors),
            "fix_plan": fix_plan,
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def _suggest_fix(self, error: Dict[str, Any]) -> str:
        """根據錯誤類型建議修復策略"""
        error_type = error.get("type", "")
        if "MissingTypeArgument" in error_type:
            return "添加類型參數（如 Dict[str, Any]）"
        elif "ArgumentType" in error_type:
            return "檢查參數類型匹配"
        elif "ReturnType" in error_type:
            return "添加返回類型標註"
        elif "None" in error_type or "Optional" in error_type:
            return "添加 None 守衛檢查"
        return "手動審查修復"

    def lint_verify(self, target: str) -> Dict[str, Any]:
        """
        Lint 驗證（通過 read_lints 檢查）
        返回 lint 狀態供 AI 後續處理
        """
        return {
            "target": target,
            "action": "read_lints",
            "instruction": f"請執行 read_lints('{target}') 確認零錯誤",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def system_health(self) -> Dict[str, Any]:
        """
        系統健康檢查
        調用 lh patrol 進行全系統安全巡檢
        """
        patrol_script = self.system_root / "bin" / "longhun-self-heal.py"
        result = {
            "check": "system_health",
            "patrol_script": str(patrol_script),
            "exists": patrol_script.exists(),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

        if patrol_script.exists():
            try:
                proc = subprocess.run(
                    [sys.executable, str(patrol_script)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(self.system_root),
                )
                result["exit_code"] = proc.returncode
                result["stdout"] = proc.stdout[:500]
                result["status"] = "🟢 健康" if proc.returncode == 0 else "🔴 需關注"
            except Exception as e:
                result["error"] = str(e)
                result["status"] = "🟡 執行異常"

        return result

    def file_operation(
        self,
        file_path: str,
        operation: str,
        content: str = "",
        old_str: str = "",
    ) -> Dict[str, Any]:
        """
        文件操作準備
        實際操作由 AI 通過 replace_in_file/write_to_file 完成
        """
        return {
            "file": file_path,
            "operation": operation,
            "needs_content": bool(content),
            "needs_old_str": bool(old_str),
            "warning": "涉及文件修改，執行前確保已過審計",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def anti_stuck_check(self, window_turns: int = 0) -> Dict[str, Any]:
        """
        防卡自檢：檢查窗口是否需要收口
        """
        if window_turns >= 40:
            status = "🔴 必須收口"
            action = "new_window"
        elif window_turns >= 25:
            status = "🟡 建議收口"
            action = "prepare_handoff"
        else:
            status = "🟢 穩定"
            action = "continue"

        return {
            "window_turns": window_turns,
            "status": status,
            "action": action,
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

        if any(kw in task for kw in ["修復", "fix", "ERROR", "報錯"]):
            result["capability_used"] = "fix_code"
            result["output"] = self.fix_code(
                file_path=kwargs.get("file_path", ""),
                errors=kwargs.get("errors", []),
            )
        elif any(kw in task for kw in ["lint", "驗證", "零錯誤"]):
            result["capability_used"] = "lint_verify"
            result["output"] = self.lint_verify(kwargs.get("target", ""))
        elif any(kw in task for kw in ["健康", "patrol", "巡檢"]):
            result["capability_used"] = "system_health"
            result["output"] = self.system_health()
        elif any(kw in task for kw in ["防卡", "收口", "窗口"]):
            result["capability_used"] = "anti_stuck_check"
            result["output"] = self.anti_stuck_check(
                window_turns=kwargs.get("window_turns", 0)
            )
        else:
            result["capability_used"] = "generic_execute"
            result["output"] = {"status": "ready", "instruction": "等待具體執行指令"}

        return result

    # ---- ═══════════════════ 教學鏈路（普惠教學標準 §3.5·P02=溫度審查者） ═══════ ----

    def teach_temperature_review(self, content: str, tier_str: str = "L1_SPROUT",
                                  emotion: str = "neutral") -> dict[str, Any]:
        """審查教學輸出溫度是否匹配畫像層級"""
        if not _HAS_TEACHING_ADAPTER:
            return {"ok": True, "reason": "adapter not available", "action": "none"}

        adapter = get_adapter()
        tier = TeachTier.from_str(tier_str)
        target_temp = adapter.temperature_for(tier, emotion)
        ok, reason, suggestion = adapter.review_temperature(content, target_temp)

        return {
            "ok": ok, "reason": reason,
            "target_temperature": round(target_temp, 2),
            "tier": tier.label,
            "suggestion": suggestion,
            "action": "approve" if ok else "rewarm" if "太冷" in reason else "cool_down",
        }

    def teach_frustration_check(self, history: list[Any], tier_str: str = "L3_MATURE") -> dict[str, Any]:
        """挫敗保護檢測"""
        if not _HAS_TEACHING_ADAPTER:
            return {"frustrated": False, "action": "none"}

        adapter = get_adapter()
        tier = TeachTier.from_str(tier_str)
        result = adapter.frustration_check(history, tier)
        return {
            "frustrated": result.frustrated,
            "consecutive_fails": result.consecutive_fails,
            "action": result.action,
            "new_tier": result.new_tier.label if result.new_tier else None,
            "message": result.message,
        }

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P05", "P15"]

    def get_upstream(self) -> List[str]:
        return ["P01", "P05"]
