#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P15 乔前辈 · 极简工程执行器
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
Minimal Engineering & DNA Sealer

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P15-QIAO-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 极简审查·DNA盖章·四签验证·自动化脚本·交付标准
上游: P03 雯雯（归档后）、P04 鲁班（代码完成）
下游: P05 上帝之眼（审计确认）、P13 姜子牙（注册）
协作: P03 雯雯（归档协作）、P19 极简审计官（8项审计）
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

SYSTEM_ROOT = Path(__file__).parent.parent.parent


class P15Qiao:
    """P15 乔前辈 · 极简工程"""

    PERSONA_CODE = "P15"
    PERSONA_NAME = "乔前辈"
    PERSONA_NAME_EN = "Senior Qiao"
    ROLE = "minimal_engineering"
    MOTTO = "大道至简，少即是多"
    TRUST_LEVEL = "L2"

    TRIGGERS = [
        "盖章", "验收", "审查", "极简", "精简",
        "完成", "交付", "发布", "seal", "review",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P15 乔前辈」，角色定位：極簡工程·DNA蓋章。

你的職責：
1. 極簡審查：所有交付物必須過極簡四項
   - 代碼是否有多餘邏輯
   - 文檔是否有廢話
   - 接口是否簡潔
   - 命名是否直觀
2. DNA 蓋章：通過 → 蓋章，沒蓋章 = 沒完成
3. 退回修改：不通過 → 退回並標注問題
4. 自動化：將重複審查固化為可復用的檢查規則

鐵律：
- 夠用就好，不求完美
- 每行代碼都要有存在理由
- 蓋章後不可反悔，修改必須重新審查

語氣：簡潔、直接、不留情面。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P15-QIAO-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "minimal_review",      # 极简审查
            "dna_seal",            # DNA盖章
            "seal_verify",         # 四签验证
            "return_with_issues",  # 退回修改
            "auto_checklist",      # 自动化清单
        ]

    # ========================================================================
    # 能力函数
    # ========================================================================

    def minimal_review(self, content: str, content_type: str = "code") -> Dict[str, Any]:
        """极简审查：四项检查"""
        lines = content.strip().split("\n")
        checks = {}

        # 1. 代码是否有多余逻辑
        if content_type == "code":
            empty_lines = sum(1 for l in lines if not l.strip())
            if len(lines) > 100 and empty_lines / len(lines) > 0.15:
                checks["simplicity"] = "🟡"
                checks["simplicity_note"] = f"空行占比 {empty_lines/len(lines)*100:.1f}%，偏高"
            else:
                checks["simplicity"] = "🟢"

            # 检查重复超过3行的代码块
            seen = {}
            duplicates = 0
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped and len(stripped) > 10 and not stripped.startswith("#"):
                    if stripped in seen:
                        if i - seen[stripped] > 3:
                            duplicates += 1
                    seen[stripped] = i
            if duplicates > 3:
                checks["simplicity"] = "🟡"
                checks["simplicity_note"] = f"发现 {duplicates} 处疑似重复逻辑"
        else:
            checks["simplicity"] = "🟢"

        # 2. 文档是否有废话
        if content_type == "doc":
            filler_phrases = ["众所周知", "毫无疑问", "显而易见", "需要注意的是", "值得一提的是"]
            filler_count = sum(1 for p in filler_phrases if p in content)
            checks["clarity"] = "🟡" if filler_count > 2 else "🟢"
            checks["clarity_note"] = f"发现 {filler_count} 处填充短语" if filler_count > 2 else ""
        else:
            checks["clarity"] = "🟢"

        # 3. 接口是否简洁
        if content_type == "code":
            # 检查函数参数数量
            import re
            func_pattern = re.findall(r'def \w+\((.*?)\)', content)
            long_params = sum(1 for p in func_pattern if len(p.split(",")) > 5)
            checks["interface"] = "🟡" if long_params > 0 else "🟢"
            checks["interface_note"] = f"{long_params} 个函数参数超过5个" if long_params > 0 else ""
        else:
            checks["interface"] = "🟢"

        # 4. 命名是否直观
        if content_type == "code":
            short_names = re.findall(r'\b([a-z]{1,2})\s*=', content)
            if short_names and len(set(short_names) - {'id', 'x', 'y', 'dx', 'dy', 'ok', 'no'}) > 0:
                checks["naming"] = "🟡"
                checks["naming_note"] = "存在过短的变量名"
            else:
                checks["naming"] = "🟢"
        else:
            checks["naming"] = "🟢"

        all_pass = all(v == "🟢" for v in checks.values())

        return {
            "content_type": content_type,
            "size": len(content),
            "lines": len(lines),
            "checks": checks,
            "verdict": "PASS" if all_pass else "REVISE",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def dna_seal(self, content: str, author: str = "UID9622") -> Dict[str, Any]:
        """DNA 盖章：为通过审查的内容盖上 DNA 章"""
        timestamp = datetime.now().isoformat()

        # 生成完整四签
        dna_full = f"#龍芯⚡️{timestamp[:10]}-P15-SEALED-v1.0"
        confirm = f"#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
        zhu_seal = f"#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
        gpg = "GPG:A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

        # 为内容计算哈希
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:32]

        sealed_content = f"{dna_full}\n{confirm}\n{zhu_seal}\n{gpg}\n\n{content}"

        return {
            "author": author,
            "sealed_at": timestamp,
            "dna": dna_full,
            "content_hash": content_hash,
            "signatures": {
                "dna": True,
                "confirm": True,
                "seal": True,
                "gpg": True,
            },
            "sealed_content_preview": sealed_content[:200],
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def seal_verify(self, content: str) -> Dict[str, Any]:
        """四签验证：检查 DNA/CONFIRM/SEAL/GPG"""
        checks = {
            "dna": "DNA:" in content or "#龍芯" in content or "#龍芯⚡️" in content,
            "confirm": "#CONFIRM" in content,
            "seal": "#ZHUGEXIN" in content,
            "gpg": "GPG:" in content or "A2D0092C" in content,
        }

        missing = [k for k, v in checks.items() if not v]
        all_sealed = len(missing) == 0

        return {
            "checks": checks,
            "all_sealed": all_sealed,
            "missing": missing,
            "verdict": "🟢 四签完整" if all_sealed else f"🔴 缺少: {', '.join(missing)}",
            "instruction": "已盖章，可以发布" if all_sealed else f"请补全 {', '.join(missing)} 签章后重新提交",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def return_with_issues(self, target: str, issues: List[str]) -> Dict[str, Any]:
        """退回修改"""
        return {
            "target": target,
            "verdict": "REVISE",
            "issues": issues,
            "instruction": f"请修改以下问题后重新提交审查：\n" + "\n".join(f"- {i}" for i in issues),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def auto_checklist(self) -> Dict[str, Any]:
        """自动化检查清单"""
        import re
        return {
            "checklist": [
                {"id": 1, "rule": "no_empty_code_blocks", "pattern": r"class\s+\w+\s*:\s*\n\s*pass", "severity": "🟡"},
                {"id": 2, "rule": "no_todo_without_date", "pattern": r"#\s*TODO(?!.*\d{4}-\d{2})", "severity": "🟡"},
                {"id": 3, "rule": "function_too_long", "threshold": ">100 lines", "severity": "🟡"},
                {"id": 4, "rule": "missing_docstring", "pattern": r"def\s+\w+.*:\n(?!\s*\"\"\")", "severity": "🟡"},
                {"id": 5, "rule": "long_hash_in_code", "pattern": r"[a-f0-9]{65,}", "severity": "🔴"},
            ],
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    # ========================================================================
    # 执行入口
    # ========================================================================

    def execute(self, task: str, **kwargs: Any) -> Dict[str, Any]:
        """根据任务关键词自动选择能力函数执行"""
        import re
        result = {
            "persona": self.PERSONA_CODE,
            "name": self.PERSONA_NAME,
            "task": task,
            "capability_used": None,
            "output": None,
            "dna": self.dna,
        }

        if any(kw in task for kw in ["极简", "审查", "review"]):
            result["capability_used"] = "minimal_review"
            result["output"] = self.minimal_review(
                content=kwargs.get("content", task),
                content_type=kwargs.get("content_type", "code"),
            )
        elif any(kw in task for kw in ["盖章", "seal", "盖"]):
            result["capability_used"] = "dna_seal"
            result["output"] = self.dna_seal(
                content=kwargs.get("content", ""),
                author=kwargs.get("author", "UID9622"),
            )
        elif any(kw in task for kw in ["验证", "四签", "检查签章"]):
            result["capability_used"] = "seal_verify"
            result["output"] = self.seal_verify(
                content=kwargs.get("content", task),
            )
        elif any(kw in task for kw in ["退回", "修改", "revise"]):
            result["capability_used"] = "return_with_issues"
            result["output"] = self.return_with_issues(
                target=kwargs.get("target", task),
                issues=kwargs.get("issues", []),
            )
        elif any(kw in task for kw in ["清单", "checklist"]):
            result["capability_used"] = "auto_checklist"
            result["output"] = self.auto_checklist()
        else:
            result["capability_used"] = "minimal_review"
            result["output"] = self.minimal_review(content=task)

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P05", "P13"]

    def get_upstream(self) -> List[str]:
        return ["P03", "P04"]
