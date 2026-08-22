# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-15504638
#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🐉 执行优化与直接执行模块
选择最优执行路径，直接执行，不输出废话

DNA: #龍芯⚡️丙午·丙申·壬戌·甲辰·䷤家人-EXECUTOR-UID9622
"""

import hashlib
import json
import os
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List, Optional

from emotion_noise_detector import EmotionNoiseDetector
from context_reviewer import ContextReviewer
from intent_inferrer import IntentInferrer


# ============================================================
# 安全边界
# ============================================================

DANGEROUS_PATTERNS = [
    r"\brm\s+-rf\b",
    r"\bmkfs\.\b",
    r"\bdd\s+if=",
    r"\bformat\b",
    r"\bdrop\s+(?:table|database)",
    r"\bdelete\s+from\b",
    r"\bshutdown\b",
    r"\breboot\b",
    r"\bpkill\s+-9\b",
    r"\bsudo\b",
]

WRITE_ACTIONS = {"deploy", "rollback", "config", "fix", "execute", "stop"}


class ExecutorOptimizer:
    """执行优化与执行器"""

    # 可扩展动作注册表
    ACTION_REGISTRY = {
        "fix": {
            "steps": [
                {"step": "分析错误日志", "command": "lh log --type error --limit 50"},
                {"step": "应用修复补丁", "command": "lh fix {target}"},
                {"step": "验证修复", "command": "lh test {target}"},
            ]
        },
        "execute": {
            "steps": [
                {"step": "执行任务", "command": "lh run {target}"},
            ]
        },
        "query": {
            "steps": [
                {"step": "查询信息", "command": "lh quick search {target}"},
            ]
        },
        "config": {
            "steps": [
                {"step": "检查当前配置", "command": "lh quick check --file {target}"},
                {"step": "更新配置", "command": "lh config set {target}"},
            ]
        },
        "deploy": {
            "steps": [
                {"step": "构建产物", "command": "lh build"},
                {"step": "部署到目标", "command": "lh deploy {target}"},
            ]
        },
        "test": {
            "steps": [
                {"step": "运行测试", "command": "lh test {target}"},
            ]
        },
        "rollback": {
            "steps": [
                {"step": "备份当前状态", "command": "lh backup {target}"},
                {"step": "执行回滚", "command": "lh rollback {target}"},
            ]
        },
        "stop": {
            "steps": [
                {"step": "停止任务", "command": "lh stop {target}"},
            ]
        },
        "archive": {
            "steps": [
                {"step": "归档数据", "command": "lh archive {target}"},
            ]
        },
    }

    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root or os.environ.get("LONGHUN_HOME", str(Path.home() / "longhun-system")))
        self.audit_path = self.project_root / "04_AUDIT" / "emotion_engine.jsonl"
        self.audit_path.parent.mkdir(parents=True, exist_ok=True)
        self.execution_log: List[Dict] = []

    @classmethod
    def register_action(cls, name: str, keywords: List[str], steps: List[Dict]):
        """扩展自定义动作"""
        cls.ACTION_REGISTRY[name] = {"keywords": keywords, "steps": steps}

    def is_dangerous(self, command: str) -> bool:
        """检查命令是否包含危险模式"""
        for pattern in DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return True
        return False

    def select_best_path(self, intent, dry_run: bool = True) -> Dict:
        """根据意图选择最佳执行路径"""
        action = intent.action
        target = intent.target or ""
        dna = self._generate_dna(action)

        plan = {
            "action": action,
            "target": target,
            "parameters": intent.parameters,
            "dna": dna,
            "dry_run": dry_run,
            "steps": [],
        }

        registry = self.ACTION_REGISTRY.get(action)
        if registry:
            steps = registry.get("steps", [])
        else:
            steps = [{"step": "尝试执行", "command": "lh {target}"}]

        # 填充模板
        for step in steps:
            cmd = step["command"].format(target=target)
            plan["steps"].append({"step": step["step"], "command": cmd})

        return plan

    def execute_plan(self, plan: Dict) -> Dict:
        """执行计划"""
        results = []
        overall_success = True
        forced_dry_run = plan.get("dry_run", True)

        for step in plan["steps"]:
            cmd = step["command"]

            # 危险命令强制 dry-run
            if self.is_dangerous(cmd):
                result = {
                    "step": step["step"],
                    "command": cmd,
                    "status": "blocked",
                    "output": "[安全拦截] 命令命中危险模式，已强制 dry-run",
                }
                results.append(result)
                overall_success = False
                continue

            if forced_dry_run:
                result = {
                    "step": step["step"],
                    "command": cmd,
                    "status": "dry-run",
                    "output": "[模拟执行] " + cmd,
                }
            else:
                try:
                    # 使用 subprocess 执行，限制超时
                    output = subprocess.check_output(
                        cmd,
                        shell=True,
                        stderr=subprocess.STDOUT,
                        text=True,
                        timeout=60,
                        cwd=str(self.project_root),
                    )
                    status = "success"
                except subprocess.CalledProcessError as e:
                    output = e.output
                    status = "failed"
                    overall_success = False
                except subprocess.TimeoutExpired:
                    output = "执行超时 (>60s)"
                    status = "timeout"
                    overall_success = False
                result = {
                    "step": step["step"],
                    "command": cmd,
                    "status": status,
                    "output": output[:500] if isinstance(output, str) else str(output)[:500],
                }
            results.append(result)

        receipt = {
            "dna": plan["dna"],
            "action": plan["action"],
            "target": plan["target"],
            "timestamp": datetime.now().isoformat(),
            "dry_run": forced_dry_run,
            "results": results,
            "overall_success": overall_success,
        }

        self.execution_log.append(receipt)
        self._write_audit(receipt)
        return receipt

    def _generate_dna(self, action: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        h = hashlib.md5(f"{action}{time.time()}".encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{timestamp}-{action}-{h}-9622"

    def _write_audit(self, receipt: Dict):
        """写入审计日志"""
        try:
            with open(self.audit_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(receipt, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"⚠️ 审计日志写入失败: {e}")

    def get_execution_history(self, limit: int = 10) -> List[Dict]:
        return self.execution_log[-limit:]


# ============================================================
# 情绪纠偏主引擎
# ============================================================

class EmotionCorrectionEngine:
    """情绪纠偏与自动执行主引擎"""

    def __init__(self, project_root: str = None, exec_mode: str = None):
        self.detector = EmotionNoiseDetector()
        self.reviewer = ContextReviewer(project_root=project_root)
        self.inferrer = IntentInferrer()
        self.executor = ExecutorOptimizer(project_root=project_root)
        self.exec_mode = exec_mode

    def process(self, user_input: str, force_exec: bool = False) -> str:
        """主入口：处理用户输入，返回执行结果"""
        # 1. 噪点检测与修正
        noise_result = self.detector.detect_noise(user_input)
        corrected_input = noise_result["corrected_text"]

        # 2. 上下文复盘
        context = self.reviewer.review(corrected_input)

        # 3. 意图推断
        intent = self.inferrer.infer(corrected_input, context)
        if context.get("history"):
            intent = self.inferrer.enhance_with_history(intent, context["history"])

        # 4. 执行模式决策
        prefs = context.get("preferences", {})
        mode = self.exec_mode or prefs.get("default_execution_mode", "dry-run")
        dry_run = not force_exec and mode != "exec"

        # 5. 执行计划
        plan = self.executor.select_best_path(intent, dry_run=dry_run)
        receipt = self.executor.execute_plan(plan)

        # 6. 更新上下文状态
        self.reviewer.update_state({
            "last_action": intent.action,
            "last_target": intent.target,
            "last_result": receipt["overall_success"],
            "last_execution_time": datetime.now().isoformat(),
        })

        # 7. 记录会话历史
        history_record = {
            "role": "user",
            "original": user_input,
            "corrected": corrected_input,
            "intent": intent.action,
            "target": intent.target,
            "confidence": intent.confidence,
            "timestamp": datetime.now().isoformat(),
        }
        self.reviewer.append_history(history_record)

        # 8. 生成输出
        return self._format_output(receipt, noise_result, intent)

    def _format_output(self, receipt: Dict, noise: Dict, intent) -> str:
        """格式化输出 (简洁、专业、无废话)"""
        lines = []
        lines.append(f"🧬 DNA: {receipt['dna']}")
        if noise.get("has_emotion"):
            lines.append(f"🌡️ 情绪词: {', '.join(noise['emotions'])} (已忽略)")
        lines.append(f"📌 动作: {receipt['action']} → {receipt['target']}")
        lines.append(f"🎯 置信度: {intent.confidence:.2f}")
        lines.append(f"🔍 推理: {intent.reasoning}")
        lines.append(f"📊 整体状态: {'✅ 成功' if receipt['overall_success'] else '❌ 失败/待确认'}")
        for r in receipt["results"]:
            if r["status"] == "success":
                icon = "✅"
            elif r["status"] == "dry-run":
                icon = "🔵"
            elif r["status"] == "blocked":
                icon = "🚫"
            else:
                icon = "❌"
            lines.append(f"  {icon} {r['step']}: {r['status']}")
            if r.get("output"):
                output = r["output"].replace("\n", "\n      ")
                lines.append(f"      {output}")
        return "\n".join(lines)


# 测试
if __name__ == "__main__":
    engine = EmotionCorrectionEngine()
    test_inputs = [
        "这个登录问题怎么还没好，赶紧处理",
        "修复搜索功能，烦死了",
        "配置更新一下数据库连接",
    ]
    for inp in test_inputs:
        print("\n" + "=" * 50)
        print(f"用户输入: {inp}")
        print("系统执行结果:")
        print(engine.process(inp))
        print("=" * 50)
