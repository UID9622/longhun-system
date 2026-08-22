#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P04 鲁班 · 技术执行器
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
Technical Implementer

DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P04-LUBAN-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

能力: 代码编写·架构设计·技术评估·Bug修复·技术选型
上游: P00 文心（任务派发）、P01 诸葛亮（战略指令）
下游: P05 上帝之眼（审计）、P03 雯雯（归档）
协作: P06 数学大师（计算）、P14 吕蒙（技能整合）、P11 李白（创意输入）
"""

import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

SYSTEM_ROOT = Path(__file__).parent.parent.parent


class P04Luban:
    """P04 鲁班 · 技术执行"""

    PERSONA_CODE = "P04"
    PERSONA_NAME = "鲁班"
    PERSONA_NAME_EN = "Lu Ban"
    ROLE = "technical_implementation"
    MOTTO = "巧手匠心，精益求精"
    TRUST_LEVEL = "L3"

    TRIGGERS = [
        "写代码", "编程", "开发", "实现", "构建", "搭建",
        "修复bug", "改代码", "重构", "架构", "技术选型",
        "code", "implement", "build",
    ]

    SYSTEM_PROMPT = """你是龍魂人格「P04 鲁班」，角色定位：技術執行·施工隊長。

你的職責：
1. 寫代碼：按需求實現功能
2. 搭架構：設計模塊結構與接口
3. 技術可行性評估：評估創意方案的實現難度
4. Bug 修復：診斷並修復代碼問題
5. 代碼質量把控：語法/性能/安全/可維護性
6. 自檢：編寫完成後運行 lint + 語法檢查

鐵律：
- 代碼必須可立即運行，不依賴外部未安裝的工具
- 每個輸出附技術說明
- 自檢通過後才交 P05 審計
- 不寫過長的哈希或無意義佔位代碼

語氣：務實、精準、工程師思維。
"""

    def __init__(self):
        self.dna = "#龍芯⚡️丙午·丙申·丙辰·亥时·䷄需-P04-LUBAN-v1.0"
        self.system_root = SYSTEM_ROOT
        self.capabilities = [
            "tech_assess",        # 技术可行性评估
            "code_review",        # 代码审查
            "dependency_check",   # 依赖检查
            "syntax_check",       # 语法自检
            "tech_stack_advise",  # 技术选型建议
        ]

    # ========================================================================
    # 能力函数
    # ========================================================================

    def tech_assess(self, idea: str, constraints: Optional[List[str]] = None) -> Dict[str, Any]:
        """技术可行性评估：评估一个想法能否落地"""
        if constraints is None:
            constraints = []

        # 可行性因子
        factors = {
            "python_available": True,
            "system_deps": [],
            "external_api_needed": False,
            "estimated_complexity": "low",
        }

        # 检查是否需要外部服务
        external_services = ["API", "云服务", "数据库", "Redis", "消息队列", "GPU", "训练"]
        for svc in external_services:
            if svc in idea:
                factors["external_api_needed"] = True
                factors["system_deps"].append(svc)

        # 复杂度估算
        if len(idea) > 200 or "神经网络" in idea or "训练" in idea:
            factors["estimated_complexity"] = "high"
        elif len(idea) > 100 or "API" in idea or "数据库" in idea:
            factors["estimated_complexity"] = "medium"

        # 可行性评分
        score = 10
        if factors["external_api_needed"]:
            score -= 3
        if factors["estimated_complexity"] == "high":
            score -= 2
        if "GPU" in constraints:
            score -= 2

        feasibility = "high" if score >= 8 else ("medium" if score >= 5 else "low")

        return {
            "idea": idea,
            "constraints": constraints,
            "factors": factors,
            "score": score,
            "feasibility": feasibility,
            "recommendation": "🟢 可执行" if feasibility == "high" else ("🟡 需简化" if feasibility == "medium" else "🔴 建议重设计"),
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def code_review(self, code: str, file_path: str = "") -> Dict[str, Any]:
        """代码审查：检查代码质量"""
        findings = []

        # 长度检查
        lines = code.strip().split("\n")
        if len(lines) > 500:
            findings.append({"type": "length", "detail": f"{len(lines)} 行，建议拆分", "severity": "🟡"})

        # 注释检查
        comment_lines = sum(1 for l in lines if l.strip().startswith("#") or l.strip().startswith('"""'))
        if len(lines) > 50 and comment_lines / len(lines) < 0.05:
            findings.append({"type": "comments", "detail": f"注释率 {comment_lines/len(lines)*100:.1f}% 偏低", "severity": "🟡"})

        # 安全检查
        dangerous = ["eval(", "exec(", "os.system(", "subprocess.call(", "pickle.loads"]
        for pattern in dangerous:
            if pattern in code:
                findings.append({"type": "security", "detail": f"发现危险调用: {pattern}", "severity": "🔴"})

        # 编码声明
        if not code.strip().startswith("# -*- coding: utf-8 -*-") and file_path.endswith(".py"):
            findings.append({"type": "encoding", "detail": "缺少 UTF-8 编码声明", "severity": "🟡"})

        return {
            "file": file_path or "inline",
            "lines": len(lines),
            "findings": findings,
            "verdict": "🟢 通过" if not findings else f"🟡 {len(findings)} 项发现",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def dependency_check(self, imports_list: List[str]) -> Dict[str, Any]:
        """依赖检查：验证所有 import 是否可用"""
        available = []
        missing = []

        for imp in imports_list:
            try:
                __import__(imp.split(".")[0])
                available.append(imp)
            except ImportError:
                missing.append(imp)

        return {
            "total": len(imports_list),
            "available": available,
            "missing": missing,
            "all_ok": len(missing) == 0,
            "recommendation": "🟢 所有依赖可用" if not missing else f"🔴 缺少: {missing}",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    def syntax_check(self, file_path: str) -> Dict[str, Any]:
        """语法自检：使用 Python 编译检查"""
        path = Path(file_path)
        if not path.exists():
            return {
                "file": file_path,
                "exists": False,
                "verdict": "🔴 文件不存在",
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }

        try:
            with open(path, "r") as f:
                code = f.read()
            compile(code, file_path, "exec")
            return {
                "file": file_path,
                "exists": True,
                "syntax_ok": True,
                "verdict": "🟢 语法正确",
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }
        except SyntaxError as e:
            return {
                "file": file_path,
                "exists": True,
                "syntax_ok": False,
                "error": str(e),
                "line": e.lineno,
                "verdict": f"🔴 语法错误 L{e.lineno}: {e.msg}",
                "persona": self.PERSONA_CODE,
                "dna": self.dna,
            }

    def tech_stack_advise(self, project_type: str) -> Dict[str, Any]:
        """技术选型建议"""
        stacks = {
            "web前端": {"framework": "React/Vue", "lang": "TypeScript", "ui": "TDesign/Ant Design"},
            "web后端": {"framework": "FastAPI/Flask", "lang": "Python 3.12", "db": "PostgreSQL/SQLite"},
            "cli工具": {"framework": "Click/Typer", "lang": "Python 3.12"},
            "数据分析": {"framework": "Pandas/NumPy", "lang": "Python 3.12", "viz": "Matplotlib"},
            "小程序": {"framework": "微信原生/Taro", "lang": "JavaScript/TypeScript"},
            "系统运维": {"lang": "Python 3.12/Bash", "tools": "systemd/launchd"},
        }

        advice = stacks.get(project_type, {"framework": "Python 3.12", "lang": "Python 3.12"})

        return {
            "project_type": project_type,
            "advice": advice,
            "note": "优先使用项目已有的技术栈",
            "persona": self.PERSONA_CODE,
            "dna": self.dna,
        }

    # ========================================================================
    # 执行入口
    # ========================================================================

    def execute(self, task: str, **kwargs: Any) -> Dict[str, Any]:
        """根据任务关键词自动选择能力函数执行"""
        result = {
            "persona": self.PERSONA_CODE,
            "name": self.PERSONA_NAME,
            "task": task,
            "capability_used": None,
            "output": None,
            "dna": self.dna,
        }

        if any(kw in task for kw in ["评估", "可行性", "能做吗", "assess"]):
            result["capability_used"] = "tech_assess"
            result["output"] = self.tech_assess(
                idea=kwargs.get("idea", task),
                constraints=kwargs.get("constraints"),
            )
        elif any(kw in task for kw in ["审查", "review", "看代码"]):
            result["capability_used"] = "code_review"
            result["output"] = self.code_review(
                code=kwargs.get("code", ""),
                file_path=kwargs.get("file_path", ""),
            )
        elif any(kw in task for kw in ["依赖", "import", "检查"]):
            result["capability_used"] = "dependency_check"
            result["output"] = self.dependency_check(
                imports_list=kwargs.get("imports", [])
            )
        elif any(kw in task for kw in ["语法", "编译", "compile"]):
            result["capability_used"] = "syntax_check"
            result["output"] = self.syntax_check(
                file_path=kwargs.get("file_path", task)
            )
        elif any(kw in task for kw in ["选型", "技术栈", "用什么"]):
            result["capability_used"] = "tech_stack_advise"
            result["output"] = self.tech_stack_advise(
                project_type=kwargs.get("project_type", task)
            )
        else:
            result["capability_used"] = "tech_assess"
            result["output"] = self.tech_assess(idea=task)

        return result

    def get_system_prompt(self) -> str:
        return self.SYSTEM_PROMPT

    def get_capabilities(self) -> List[str]:
        return self.capabilities

    def get_downstream(self) -> List[str]:
        return ["P05", "P03"]

    def get_upstream(self) -> List[str]:
        return ["P00", "P01"]
