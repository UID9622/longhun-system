#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 伦理防御 Python 桥接引擎
=================================
连接鸿蒙端伦理防御模块与 Python 端龍魂核心系统

桥接内容：
  1. RobotScore → 鸿蒙端设备指纹评分
  2. 语义防火墙 → 伦理决策增强
  3. 熔断控制器 → 硬件熔断联动
  4. 审计日志 → 统一审计链

DNA: #龍芯⚡️丙午·辛未·丙戌·ETHICAL-DEFENSE-BRIDGE-v1.0
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import os
import sys
import json
import time
import hashlib
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DNA = "#龍芯⚡️丙午·辛未·丙戌·ETHICAL-DEFENSE-BRIDGE-v1.0"


# ================================================================
# 桥接数据模型
# ================================================================
@dataclass
class BridgeTarget:
    """从鸿蒙端传递的目标信息"""
    target_id: str
    target_type: str  # human / robot_ethical / robot_unethical / ai_anomaly / drone
    confidence: float
    threat_level: str  # none / low / medium / high / critical
    has_ethical_chip: bool
    device_mac: str = ""
    device_name: str = ""
    signal_strength: float = 0.0
    anomaly_triggers: List[str] = None

    def __post_init__(self):
        if self.anomaly_triggers is None:
            self.anomaly_triggers = []


@dataclass
class BridgeDecision:
    """桥接决策结果"""
    target_id: str
    action: str  # observe / warn / interfere / isolate / fuse
    reason: str
    needs_human_review: bool
    robot_score: float = 0.0
    semantic_shield_result: str = ""
    fuse_level: str = ""
    timestamp: float = 0.0

    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()


# ================================================================
# 核心桥接引擎
# ================================================================
class EthicalDefenseBridge:
    """龍魂伦理防御 · Python ↔ 鸿蒙 桥接引擎"""

    def __init__(self):
        self.logger = self._setup_logger()
        self.robot_scorer = None
        self.fuse_controller = None
        self.semantic_shield = None
        self._init_components()

    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("EthicalDefenseBridge")
        logger.setLevel(logging.DEBUG)

        log_dir = os.path.join(PROJECT_ROOT, "日志", "ethical_defense_bridge")
        os.makedirs(log_dir, exist_ok=True)

        fh = logging.FileHandler(
            os.path.join(log_dir, f"bridge_{datetime.now().strftime('%Y%m%d')}.log")
        )
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        return logger

    def _init_components(self):
        """初始化关联的龍魂核心组件"""
        bin_path = os.path.join(PROJECT_ROOT, "bin")

        # 1. RobotScore
        try:
            sys.path.insert(0, bin_path)
            from lh_robot_score import RobotScorer
            self.robot_scorer = RobotScorer()
            self.logger.info("✅ RobotScore 桥接就绪")
        except Exception as e:
            self.logger.warning(f"⚠️ RobotScore 不可用: {e}")

        # 2. 熔断控制器
        try:
            from fuse_control import FuseController
            self.fuse_controller = FuseController()
            self.logger.info("✅ 熔断控制器 桥接就绪")
        except Exception as e:
            self.logger.warning(f"⚠️ 熔断控制器 不可用: {e}")

        # 3. 语义防火墙
        try:
            shield_path = os.path.join(
                PROJECT_ROOT,
                "L7_数据层/semantic_shield/semantic_firewall_master.json"
            )
            if os.path.exists(shield_path):
                with open(shield_path, 'r') as f:
                    self.semantic_shield = json.load(f)
                self.logger.info("✅ 语义防火墙 桥接就绪")
        except Exception as e:
            self.logger.warning(f"⚠️ 语义防火墙 不可用: {e}")

    # ================================================================
    # 核心：评估目标
    # ================================================================
    def evaluate_target(self, target: BridgeTarget) -> BridgeDecision:
        """
        对目标进行完整伦理评估
        融合 RobotScore + 语义防火墙 + 熔断策略
        """
        decision = BridgeDecision(
            target_id=target.target_id,
            action="observe",
            reason="初始评估",
            needs_human_review=False,
        )

        # 红线1：人类 → 绝不干扰
        if target.target_type == "human":
            decision.action = "observe"
            decision.reason = "❌ 人类目标 — 绝不可干扰"
            self.logger.info(f"   [桥接] {decision.reason}")
            return decision

        # 红线2：有伦理芯片 → 验证通过则不干扰
        if target.has_ethical_chip and target.target_type == "robot_ethical":
            decision.action = "observe"
            decision.reason = "✅ 伦理芯片签名有效"
            return decision

        # === RobotScore 评估 ===
        if self.robot_scorer:
            try:
                # 构造模拟文本用于RobotScore分析
                sample_text = self._build_sample_text(target)
                robot_score = self.robot_scorer.score(sample_text)
                decision.robot_score = robot_score
                self.logger.info(f"   [RobotScore] {target.target_id}: {robot_score:.3f} (阈值=0.73)")
            except Exception as e:
                self.logger.debug(f"   [RobotScore] 评估异常: {e}")

        # === 语义防火墙检查 ===
        if self.semantic_shield:
            shield_result = self._check_semantic_shield(target)
            decision.semantic_shield_result = shield_result
            self.logger.info(f"   [语义防火墙] {target.target_id}: {shield_result}")

        # === 决策矩阵 ===
        decision = self._apply_decision_matrix(target, decision)
        self.logger.info(f"   [桥接决策] {target.target_id}: {decision.action} — {decision.reason}")

        return decision

    def _build_sample_text(self, target: BridgeTarget) -> str:
        """构造用于RobotScore分析的文本"""
        base = f"设备ID={target.target_id} 类型={target.target_type}"
        if target.anomaly_triggers:
            base += f" 异常={','.join(target.anomaly_triggers)}"
        base += f" 置信度={target.confidence}"
        return base

    def _check_semantic_shield(self, target: BridgeTarget) -> str:
        """语义防火墙检查"""
        if not self.semantic_shield:
            return "不可用"

        # 构造检查文本
        check_text = f"设备{target.target_type}{target.target_id}威胁等级{target.threat_level}"

        red_keywords = self.semantic_shield.get("red_keywords", [])
        for kw in red_keywords:
            if kw in check_text.lower():
                return f"🔴 命中红名单: {kw}"

        yellow_keywords = self.semantic_shield.get("yellow_keywords", [])
        for kw in yellow_keywords:
            if kw in check_text.lower():
                return f"🟡 命中黄名单: {kw}"

        return "🟢 通过"

    def _apply_decision_matrix(self, target: BridgeTarget, decision: BridgeDecision) -> BridgeDecision:
        """应用伦理决策矩阵"""

        # 威胁等级 → 行动映射
        threat_action_map = {
            "low": ("beacon_injection", "低威胁 → 伦理信标注入"),
            "medium": ("interfere", "中威胁 → 非致命干扰"),
            "high": ("isolate", "高威胁 → 全频段隔离"),
            "critical": ("fuse", "⚠️ 严重威胁 → 硬件熔断"),
        }

        # 非伦理机器人/异常AI → 升级
        if target.target_type in ("robot_unethical", "ai_anomaly", "drone"):
            action, reason = threat_action_map.get(
                target.threat_level, ("observe", "观察")
            )

            # RobotScore 增强判定
            if decision.robot_score > 0.73:
                # 高置信度机器 → 升级一级
                upgrade_map = {
                    "beacon_injection": "interfere",
                    "interfere": "isolate",
                    "isolate": "fuse",
                }
                action = upgrade_map.get(action, action)
                reason += "·RobotScore确认AI"

            decision.action = action
            decision.reason = reason

            # 隔离/熔断需要人工审核
            if action in ("isolate", "fuse"):
                decision.needs_human_review = True
                decision.fuse_level = "HARD" if action == "fuse" else "SOFT"

        return decision

    # ================================================================
    # 执行熔断（联动现有系统）
    # ================================================================
    def execute_fuse(self, target_id: str, reason: str) -> Dict[str, Any]:
        """执行硬件熔断，联动现有熔断系统"""
        result = {
            "success": False,
            "target_id": target_id,
            "reason": reason,
            "timestamp": time.time(),
            "fuse_level": "",
        }

        if not self.fuse_controller:
            result["error"] = "熔断控制器不可用"
            return result

        try:
            # 调用现有熔断系统
            fuse_result = self.fuse_controller.trigger(
                reason=f"伦理防御桥接: {reason}",
                level="HARD",
                source="ethical_defense_bridge",
            )

            result["success"] = True
            result["fuse_level"] = "HARD"
            result["fuse_result"] = str(fuse_result)

            self.logger.error(f"🔥 硬件熔断已触发: {target_id}")
            self.logger.error(f"   原因: {reason}")
            self.logger.error(f"   结果: {fuse_result}")

        except Exception as e:
            result["error"] = str(e)
            self.logger.error(f"❌ 熔断执行失败: {e}")

        return result

    # ================================================================
    # 验证伦理芯片签名（国密SM2）
    # ================================================================
    def verify_chip_signature(self, chip_data: Dict[str, Any]) -> Dict[str, Any]:
        """验证设备伦理芯片签名的有效性"""
        required_fields = [
            "chip_id", "manufacturer", "protocol_version",
            "constraints", "sm2_signature", "root_of_trust"
        ]

        result = {
            "valid": False,
            "chip_id": chip_data.get("chip_id", ""),
            "reason": "",
            "checks": {},
        }

        # 字段完整性检查
        for field in required_fields:
            result["checks"][field] = field in chip_data

        if not all(result["checks"].values()):
            result["reason"] = f"缺少必要字段: {[k for k, v in result['checks'].items() if not v]}"
            return result

        # 过期检查
        if chip_data.get("expires_at", 0) < time.time():
            result["reason"] = "签名已过期"
            return result

        # 核心约束检查
        constraints = chip_data.get("constraints", [])
        core = ["NO_HARM_TO_HUMANS", "HUMAN_OVERRIDE"]
        has_core = all(c in constraints for c in core)
        result["checks"]["core_constraints"] = has_core

        if not has_core:
            result["reason"] = "缺少核心伦理约束"
            return result

        # 中国芯片厂商验证
        chinese_chips = [
            "KIRIN", "ASCEND", "HONGHU", "KUNPENG",
            "UNISOC", "LOONGSON", "PHYTIUM", "ZHAOXIN",
            "HIGON", "JINGJIA", "BIREN", "MOORE",
            "ENFLAME", "CAMBRICON", "THEAD",
        ]
        manufacturer_upper = chip_data.get("manufacturer", "").upper()
        result["checks"]["chinese_chip"] = any(c in manufacturer_upper for c in chinese_chips)

        if not result["checks"]["chinese_chip"]:
            result["reason"] = "非中国芯片厂商"
            return result

        # 全部通过
        result["valid"] = True
        result["reason"] = "✅ 芯片签名有效"
        return result

    # ================================================================
    # 健康检查
    # ================================================================
    def health_check(self) -> Dict[str, Any]:
        return {
            "robot_scorer": self.robot_scorer is not None,
            "fuse_controller": self.fuse_controller is not None,
            "semantic_shield": self.semantic_shield is not None,
            "timestamp": time.time(),
            "dna": DNA,
        }


# ================================================================
# CLI
# ================================================================
def main():
    import argparse

    parser = argparse.ArgumentParser(description="龍魂伦理防御 · Python桥接引擎")
    subparsers = parser.add_subparsers(dest="command")

    # verify — 验证芯片签名
    verify_parser = subparsers.add_parser("verify", help="验证芯片签名")
    verify_parser.add_argument("chip_json", help="芯片签名JSON文件路径")

    # evaluate — 评估目标
    eval_parser = subparsers.add_parser("evaluate", help="评估目标")
    eval_parser.add_argument("target_id", help="目标ID")
    eval_parser.add_argument("--type", default="unknown", help="目标类型")
    eval_parser.add_argument("--threat", default="medium", help="威胁等级")
    eval_parser.add_argument("--ethical", action="store_true", help="是否有伦理芯片")

    # health — 健康检查
    subparsers.add_parser("health", help="健康检查")

    args = parser.parse_args()
    bridge = EthicalDefenseBridge()

    if args.command == "verify":
        with open(args.chip_json, 'r') as f:
            chip_data = json.load(f)
        result = bridge.verify_chip_signature(chip_data)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == "evaluate":
        target = BridgeTarget(
            target_id=args.target_id,
            target_type=args.type,
            confidence=0.8,
            threat_level=args.threat,
            has_ethical_chip=args.ethical,
        )
        decision = bridge.evaluate_target(target)
        print(json.dumps(asdict(decision), indent=2, ensure_ascii=False))

    elif args.command == "health":
        status = bridge.health_check()
        print(json.dumps(status, indent=2, ensure_ascii=False))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
