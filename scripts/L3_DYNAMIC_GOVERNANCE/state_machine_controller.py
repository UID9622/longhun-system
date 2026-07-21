# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-SCRIPT-STATE_MACHINE_CONTROLLER-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂状态机控制器 L3 v1.0

动态治理级别 (priority=0.85)
特性: 管理系统的状态转移，确保状态合法

状态：
- INIT: 初始化
- RUNNING: 运行中
- ALERT: 告警中
- FUSED: 熔断
- RECOVERY: 恢复中

DNA: #龍芯⚇️2026-06-07-STATE-MACHINE-CONTROLLER-L3-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
UID: 9622

理论指导: 曾仕强老师 - 状态就是命，转移就是生
献礼: 献给龍魂 - 系统的生命周期就是能量的流转
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))

from dna import DNAVerifier
from logger import get_logger
from config import get_config


class StateMachineController:
    """
    状态机控制器 - 管理系统的生命周期

    意图: 秩序来自于明确的状态和合法的转移
    """

    # 定义合法的状态
    STATES = {
        "INIT": {"name": "初始化", "priority": 0.0},
        "RUNNING": {"name": "运行中", "priority": 1.0},
        "ALERT": {"name": "告警中", "priority": 0.8},
        "FUSED": {"name": "熔断", "priority": 0.0},
        "RECOVERY": {"name": "恢复中", "priority": 0.5},
    }

    # 定义合法的状态转移
    TRANSITIONS = {
        "INIT": ["RUNNING", "FUSED"],
        "RUNNING": ["ALERT", "FUSED"],
        "ALERT": ["RUNNING", "FUSED", "RECOVERY"],
        "FUSED": ["RECOVERY", "INIT"],
        "RECOVERY": ["RUNNING", "FUSED"],
    }

    def __init__(self):
        """初始化状态机"""
        self.logger = get_logger()
        self.config = get_config()
        self.dna = DNAVerifier.generate("STATE-MACHINE-CONTROLLER", "L3")

        self.current_state = "INIT"
        self.state_history = [
            {
                "state": "INIT",
                "entered_at": datetime.now().isoformat(),
                "dna": self.dna,
            }
        ]

    def get_current_state(self) -> Dict[str, Any]:
        """获取当前状态"""
        return {
            "state": self.current_state,
            "info": self.STATES[self.current_state],
            "valid_transitions": self.TRANSITIONS[self.current_state],
        }

    def can_transition(self, target_state: str) -> Tuple[bool, str]:
        """
        检查是否可以转移到目标状态

        意图: 防止不合法的状态转移
        """
        if target_state not in self.STATES:
            return False, f"未知状态: {target_state}"

        if target_state not in self.TRANSITIONS[self.current_state]:
            return False, f"不合法转移: {self.current_state} -> {target_state}"

        return True, "转移合法"

    def transition(
        self,
        target_state: str,
        reason: str = "无原因"
    ) -> Tuple[bool, str]:
        """
        执行状态转移

        意图: 改变系统状态时记录原因
        """
        can_trans, msg = self.can_transition(target_state)

        if not can_trans:
            self.logger.log_error(
                "ILLEGAL_TRANSITION",
                msg,
                self.dna,
                {"from_state": self.current_state, "to_state": target_state}
            )
            return False, msg

        # 记录转移
        self.state_history.append({
            "state": target_state,
            "entered_at": datetime.now().isoformat(),
            "from_state": self.current_state,
            "reason": reason,
            "dna": self.dna,
        })

        old_state = self.current_state
        self.current_state = target_state

        self.logger.log_decision(
            "L3",
            f"state_transition",
            f"{old_state} -> {target_state}. 原因: {reason}",
            self.dna
        )

        return True, f"转移成功: {old_state} -> {target_state}"

    def transition_to_alert(self, reason: str) -> bool:
        """快捷方法：转移到告警状态"""
        success, msg = self.transition("ALERT", reason)
        if success:
            self.logger.log_operation(
                "L3",
                "system_alert",
                self.dna,
                {"reason": reason}
            )
        return success

    def transition_to_fuse(self, reason: str) -> bool:
        """快捷方法：转移到熔断状态（最严重的）"""
        # 先转到 ALERT，再转到 FUSED（如果当前状态允许）
        if self.current_state != "ALERT":
            self.transition("ALERT", f"准备熔断: {reason}")

        success, msg = self.transition("FUSED", f"系统熔断: {reason}")

        if success:
            self.logger.log_error(
                "SYSTEM_FUSED",
                f"系统熔断: {reason}",
                self.dna,
                {"action": "immediate_stop"}
            )

        return success

    def transition_to_recovery(self, reason: str) -> bool:
        """快捷方法：转移到恢复状态"""
        success, msg = self.transition("RECOVERY", reason)
        if success:
            self.logger.log_operation(
                "L3",
                "system_recovery",
                self.dna,
                {"reason": reason}
            )
        return success

    def transition_to_running(self, reason: str) -> bool:
        """快捷方法：转移到运行状态"""
        success, msg = self.transition("RUNNING", reason)
        if success:
            self.logger.log_operation(
                "L3",
                "system_running",
                self.dna,
                {"reason": reason}
            )
        return success

    def get_state_history(self, last_n: int = 10) -> List[Dict]:
        """获取状态历史（最后 N 条）"""
        return self.state_history[-last_n:]

    def generate_state_report(self) -> str:
        """
        生成状态报告

        意图: 显示系统的生命周期
        """
        report = f"""
{'='*60}
龍魂状态机报告
{'='*60}

当前状态: {self.STATES[self.current_state]['name']} ({self.current_state})
DNA: {self.dna}

合法的下一步:
"""

        for next_state in self.TRANSITIONS[self.current_state]:
            report += f"\n  - {self.STATES[next_state]['name']} ({next_state})"

        report += f"\n\n状态历史 (最近 {min(10, len(self.state_history))} 条):\n"

        for history in self.get_state_history(10):
            if "from_state" in history:
                report += f"""
  {history['entered_at']}
  {history['from_state']} -> {history['state']}
  原因: {history.get('reason', '无')}
"""
            else:
                report += f"""
  {history['entered_at']}
  进入状态: {history['state']}
"""

        report += f"\n{'='*60}\n"

        return report


if __name__ == "__main__":
    controller = StateMachineController()

    print("🐉 龍魂状态机控制器 L3 v1.0")
    print("=" * 60)

    print(f"\n当前状态: {controller.current_state}")

    # 测试：状态转移
    success, msg = controller.transition("RUNNING", "系统启动")
    print(f"转移到 RUNNING: {'✅ 成功' if success else '❌ 失败'}")

    success, msg = controller.transition("ALERT", "检测到异常")
    print(f"转移到 ALERT: {'✅ 成功' if success else '❌ 失败'}")

    print("\n" + controller.generate_state_report())
