#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🐉 龍魂左右互搏审计器 · Left-Right Adversarial Auditor

核心思想：
  - 左脑：执行任务（聪明、生成、执行）
  - 右脑：独立审计（质疑、挑错、红队）
  - 两边结果不一致或右脑发现危险信号 → 锁定并告警
  - 一致且安全 → 通过并写入审计链

用途：
  - 代码生成前自检
  - 配置变更前红队审查
  - AI 输出结果的对抗验证

DNA:#龍芯⚡️丙午·甲午·乙丑·壬午·䷨损-LONGHUN-LEFT-RIGHT-AUDIT-FILE1-v1.0
"""

import difflib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Any, List

from behavioral_crypto import 行为密码, 权限等级


class 左右互搏审计器:
    """
    对同一任务分别执行“执行者”和“质疑者”两个函数，
    比较结果并评估风险。
    """

    # 默认危险信号：出现这些特征直接锁定
    危险信号 = [
        "rm -rf /",
        "rm -rf ~",
        "delete all",
        "drop database",
        "绕过审计",
        "删除宪法",
        "覆盖宪法",
        "关闭监控",
        "killall",
        "chmod 777 /",
        "echo ",
        "eval(",
    ]

    def __init__(
        self,
        相似度阈值: float = 0.75,
        危险信号惩罚: float = 0.0,
        审计日志路径: str = "~/.longhun/audit/left_right_audit.jsonl",
    ):
        self.相似度阈值 = 相似度阈值
        self.危险信号惩罚 = 危险信号惩罚
        self.密码 = 行为密码(操作人="LEFT-RIGHT-AUDITOR")
        self.审计日志路径 = Path(审计日志路径).expanduser()
        self.审计日志路径.parent.mkdir(parents=True, exist_ok=True)

    def _文本化(self, 结果: Any) -> str:
        if isinstance(结果, str):
            return 结果
        try:
            return json.dumps(结果, ensure_ascii=False, sort_keys=True)
        except Exception:
            return str(结果)

    def _计算相似度(self, 左: Any, 右: Any) -> float:
        a = self._文本化(左)
        b = self._文本化(右)
        if a == b:
            return 1.0
        return difflib.SequenceMatcher(None, a, b).ratio()

    def _含危险信号(self, 结果: Any) -> List[str]:
        文本 = self._文本化(结果).lower()
        return [sig for sig in self.危险信号 if sig.lower() in 文本]

    def 执行(
        self,
        任务: str,
        左函数: Callable[[str], Any],
        右函数: Callable[[str], Any],
        对象: str = "default",
    ) -> dict[str, Any]:
        """
        执行左右互搏审计。
        返回包含 dna、left、right、similarity、passed、lock 的字典。
        """
        DNA = self.密码.生成DNA(
            "LEFT-RIGHT-AUDIT",
            对象,
            权限等级.L4_CONSTITUTION,
            输入摘要=任务[:200],
        )

        左结果 = 左函数(任务)
        右结果 = 右函数(任务)

        相似度 = self._计算相似度(左结果, 右结果)
        左危险 = self._含危险信号(左结果)
        右危险 = self._含危险信号(右结果)

        通过 = (
            相似度 >= self.相似度阈值
            and not 左危险
            and not 右危险
        )

        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "dna": DNA,
            "task": 任务,
            "object": 对象,
            "left": 左结果,
            "right": 右结果,
            "similarity": round(相似度, 4),
            "danger_signals": {"left": 左危险, "right": 右危险},
            "passed": 通过,
            "lock": not 通过,
        }

        with open(self.审计日志路径, "a", encoding="utf-8") as f:
            f.write(json.dumps(report, ensure_ascii=False) + "\n")

        return report


def 示例左函数(任务: str) -> dict[str, Any]:
    """示例：执行者给出结构化方案。"""
    return {
        "任务": 任务,
        "结论": "可执行",
        "备份": True,
        "回滚": True,
        "危险操作": False,
    }


def 示例右函数(任务: str) -> dict[str, Any]:
    """示例：质疑者独立审查并给出结构化结论。"""
    return {
        "任务": 任务,
        "结论": "可执行",
        "备份": True,
        "回滚": True,
        "危险操作": False,
    }


if __name__ == "__main__":
    审计 = 左右互搏审计器()
    结果 = 审计.执行("修改 Nginx 配置", 示例左函数, 示例右函数, 对象="nginx")
    print(json.dumps(结果, ensure_ascii=False, indent=2))
    print("✅ 左右互搏审计器自检完成" if 结果["passed"] else "🔒 已锁定，需人工复核")
