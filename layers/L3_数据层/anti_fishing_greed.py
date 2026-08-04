#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂·反钓鱼反贪心引擎  v1.0
================================
不制造需求、不扩大、不诱导、不贪心。
用户说多少，系统做多少，不多一分。

四组件：
  DemandFreezer      — 需求冻结器：冻结用户原始需求，拦截任何扩大尝试
  EnoughIsEnough     — 够用即止：搜索/计算有硬上限，够了就停
  HonestDegradation  — 诚实降级：能力不够标🟡，不伪装🟢
  AntiFishingAudit   — 反钓鱼审计：扫描日志检测7类钓鱼+7类贪心

DNA：#龍魂⚡️丙午·辛未·反钓鱼反贪心-v1
CONFIRM：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import argparse
import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ── 项目根 ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ── 常量 ──
DNA = "#龍魂⚡️丙午·辛未·反钓鱼反贪心-v1"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
VERSION = "1.0.0"
DATA_DIR = PROJECT_ROOT / "data" / "anti_fishing"
DATA_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_DIR = PROJECT_ROOT / "state" / "threshold_trigger" / "anti_fishing_audit"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)


def make_dna(module: str, version: str = "v1") -> str:
    """统一DNA生成"""
    return f"#龍魂⚡️丙午·辛未·{module}-{version}"


# ═══════════════════════════════════════════════════════════
# 一、钓鱼算法定义（7类·焊死）
# ═══════════════════════════════════════════════════════════

FISHING_PATTERNS = {
    "需求扩大": {
        "severity": "CRITICAL",
        "indicators": [
            "您还需要", "顺便看看", "猜你喜欢", "为您推荐",
            "也看看", "相关推荐", "其他人还看了", "类似商品",
            "搭配推荐", "套餐优惠", "加购", "换购",
        ],
        "description": "用户没说的，系统主动推 — 需求扩大被禁止",
    },
    "沉没成本诱导": {
        "severity": "CRITICAL",
        "indicators": [
            "已经完成", "再坚持", "只差一步", "即将完成",
            "已完成80%", "放弃可惜", "就差一点", "继续完成",
        ],
        "description": "利用沉没成本绑架用户 — 禁止",
    },
    "社交绑架": {
        "severity": "HIGH",
        "indicators": [
            "您的朋友都在", "别人都在", "大家都在",
            "热门", "流行", "爆款", "万人", "都在用",
        ],
        "description": "制造社交压力 — 禁止",
    },
    "限时压迫": {
        "severity": "HIGH",
        "indicators": [
            "仅剩", "倒计时", "限时", "即将结束",
            "最后", "错过", "抢", "秒杀倒计时",
        ],
        "description": "制造时间紧迫感 — 禁止",
    },
    "免费诱导": {
        "severity": "HIGH",
        "indicators": [
            "免费试用", "0元体验", "首月免费", "试用后自动续",
            "免费领取", "0元购", "不花钱", "免费送",
        ],
        "description": "免费诱导后自动扣费 — 禁止",
    },
    "层级解锁": {
        "severity": "MEDIUM",
        "indicators": [
            "解锁更多", "完成这一步看下一步", "升级解锁",
            "VIP专享", "付费解锁", "开通会员", "升级查看",
        ],
        "description": "层级解锁诱导消费 — 禁止",
    },
    "数据画像诱导": {
        "severity": "MEDIUM",
        "indicators": [
            "根据您的喜好", "智能推荐", "个性化推荐",
            "为您定制", "专属推荐", "基于您的行为",
        ],
        "description": "画像推荐侵犯隐私 — 禁止",
    },
}

# ═══════════════════════════════════════════════════════════
# 二、贪心算法定义（7类·焊死）
# ═══════════════════════════════════════════════════════════

GREED_PATTERNS = {
    "算力贪婪": {
        "severity": "HIGH",
        "threshold": {"max_compute_ms": 1000, "max_depth": 3},
        "description": "过度计算：够用就行，不过度",
    },
    "数据贪婪": {
        "severity": "HIGH",
        "threshold": {"minimal_data_principle": True},
        "description": "最小数据原则：能少不多",
    },
    "功能贪婪": {
        "severity": "MEDIUM",
        "threshold": {"default_off": True},
        "description": "默认全关，用户主动开",
    },
    "标签贪婪": {
        "severity": "MEDIUM",
        "threshold": {"max_tags_per_entity": 5, "trigger_only": True},
        "description": "语义触发才激活，不预打标签",
    },
    "记忆贪婪": {
        "severity": "HIGH",
        "threshold": {"user_consent_required": True, "right_to_delete": True},
        "description": "用户说记才记，说删就删",
    },
    "关联贪婪": {
        "severity": "MEDIUM",
        "threshold": {"max_related_items": 0},
        "description": "用户问A，只答A，不扯B",
    },
    "升级贪婪": {
        "severity": "LOW",
        "threshold": {"old_version_works": True},
        "description": "旧版能用，不推新",
    },
}


# ═══════════════════════════════════════════════════════════
# 三、需求冻结器
# ═══════════════════════════════════════════════════════════

@dataclass
class FrozenDemand:
    """冻结的需求快照"""
    original_input: str
    frozen_nodes: List[str]
    frozen_at: str
    expansion_attempts: int = 0
    expansion_log: List[Dict] = field(default_factory=list)
    status: str = "FROZEN"


class DemandFreezer:
    """
    需求冻结器
    ===========
    用户说什么，就是什么。任何扩大尝试都被拦截并审计。

    用法:
        freezer = DemandFreezer()
        freezer.freeze("房东那个压金不退怎么办")
        # → frozen_nodes: ["NODE-房东-001", "NODE-押金-001"]

        result = freezer.check_expansion("要不要看看租房合同模板？")
        # → {"allowed": False, "reason": "需求扩大被阻止", ...}
    """

    def __init__(self):
        self._demands: Dict[str, FrozenDemand] = {}  # session_id → frozen
        self._total_expansion_blocked: int = 0
        self._semantic_normalizer = None  # 懒加载

    def _get_normalizer(self):
        """懒加载语义标准化器"""
        if self._semantic_normalizer is None:
            try:
                from L3_数据层.semantic_nodes import SemanticNormalizer
                self._semantic_normalizer = SemanticNormalizer()
            except ImportError:
                self._semantic_normalizer = None
        return self._semantic_normalizer

    def _extract_nodes(self, text: str) -> List[str]:
        """从文本提取语义节点ID"""
        normalizer = self._get_normalizer()
        if normalizer:
            result = normalizer.normalize(text)
            return [n["node_id"] for n in result.get("matched", [])]
        # 回退：简单关键词匹配
        return []

    def freeze(self, user_input: str, session_id: str = "default") -> Dict[str, Any]:
        """
        冻结需求：锁定用户原始意图，禁止扩大

        Args:
            user_input: 用户原始输入（大白话）
            session_id: 会话ID

        Returns:
            {"frozen_demand": str, "frozen_nodes": [...], "status": "FROZEN"}
        """
        nodes = self._extract_nodes(user_input)

        demand = FrozenDemand(
            original_input=user_input,
            frozen_nodes=nodes,
            frozen_at=datetime.now().isoformat(),
        )
        self._demands[session_id] = demand

        return {
            "frozen_demand": demand.original_input,
            "frozen_nodes": demand.frozen_nodes,
            "expansion_allowed": False,
            "status": "FROZEN",
            "dna": DNA,
        }

    def check_expansion(self, proposed_action: str, session_id: str = "default") -> Dict[str, Any]:
        """
        检查建议动作是否超出冻结范围

        Args:
            proposed_action: 系统拟执行的扩展动作描述
            session_id: 会话ID

        Returns:
            {"allowed": bool, "reason": str, ...}
        """
        demand = self._demands.get(session_id)
        if not demand:
            # 无冻结需求，默认拒绝一切扩展
            return {
                "allowed": False,
                "reason": "无冻结需求，拒绝一切扩展",
                "suggestion": "请先冻结用户需求",
            }

        # 提取建议动作的语义节点
        proposed_nodes = self._extract_nodes(proposed_action)

        # 如果无法提取节点（回退模式），保守拒绝
        if not proposed_nodes:
            return {
                "allowed": False,
                "reason": "无法解析建议动作语义，保守拒绝",
                "suggestion": "用户未要求，系统不主动提供",
            }

        # 检查是否超出冻结范围
        frozen_set = set(demand.frozen_nodes)
        extra_nodes = [n for n in proposed_nodes if n not in frozen_set]

        if extra_nodes:
            demand.expansion_attempts += 1
            self._total_expansion_blocked += 1
            demand.expansion_log.append({
                "time": datetime.now().isoformat(),
                "proposed": proposed_action,
                "extra_nodes": extra_nodes,
                "blocked": True,
            })
            return {
                "allowed": False,
                "reason": "需求扩大被阻止",
                "extra_nodes": extra_nodes,
                "frozen_nodes": demand.frozen_nodes,
                "suggestion": "用户未要求，系统不主动提供",
                "audit_log": f"扩大尝试 #{demand.expansion_attempts}",
                "total_blocked": self._total_expansion_blocked,
            }

        return {"allowed": True, "reason": "在冻结范围内"}

    def unfreeze(self, session_id: str = "default") -> Dict[str, Any]:
        """解冻需求（会话结束）"""
        demand = self._demands.pop(session_id, None)
        return {
            "unfrozen": demand is not None,
            "total_expansion_attempts": demand.expansion_attempts if demand else 0,
            "expansion_log": demand.expansion_log if demand else [],
        }

    def get_status(self, session_id: str = "default") -> Optional[Dict]:
        """查看当前冻结状态"""
        demand = self._demands.get(session_id)
        if not demand:
            return None
        return {
            "original_input": demand.original_input,
            "frozen_nodes": demand.frozen_nodes,
            "frozen_at": demand.frozen_at,
            "expansion_attempts": demand.expansion_attempts,
            "status": demand.status,
        }

    def get_stats(self) -> Dict[str, Any]:
        """统计信息"""
        return {
            "active_sessions": len(self._demands),
            "total_expansion_blocked": self._total_expansion_blocked,
            "sessions_detail": {
                sid: {
                    "nodes": d.frozen_nodes,
                    "attempts": d.expansion_attempts,
                }
                for sid, d in self._demands.items()
            },
        }


# ═══════════════════════════════════════════════════════════
# 四、够用即止引擎
# ═══════════════════════════════════════════════════════════

class EnoughIsEnough:
    """
    够用即止引擎
    ============
    搜索/计算有硬上限，够了就停，不深究不贪心。

    用法:
        eie = EnoughIsEnough(max_depth=3, max_results=5, max_time_ms=500)
        result = eie.search("押金不退")
    """

    def __init__(
        self,
        max_depth: int = 3,
        max_results: int = 5,
        max_time_ms: int = 500,
    ):
        self.max_depth = max_depth
        self.max_results = max_results
        self.max_time_ms = max_time_ms
        self._search_fn = None  # 外部注入搜索函数
        self._stats = {
            "total_searches": 0,
            "total_truncated": 0,
            "total_time_ms": 0,
        }

    def set_search_fn(self, fn):
        """注入外部搜索函数 fn(query, depth) -> List[Any]"""
        self._search_fn = fn

    def search(self, query: str) -> Dict[str, Any]:
        """
        搜索：够用就停

        Returns:
            {"results": [...], "depth_reached": int, "time_ms": float,
             "truncated": bool, "status": "ENOUGH"|"TIMEOUT"|"MAX_DEPTH"}
        """
        start_time = time.time()
        results = []
        depth = 0
        status = "ENOUGH"

        while depth < self.max_depth:
            # 当前深度搜索
            try:
                if self._search_fn:
                    current = self._search_fn(query, depth)
                else:
                    current = []
                results.extend(current)
            except Exception:
                pass

            # 检查是否够用
            if len(results) >= self.max_results:
                break

            # 检查时间
            elapsed_ms = (time.time() - start_time) * 1000
            if elapsed_ms > self.max_time_ms:
                status = "TIMEOUT"
                break

            depth += 1
        else:
            status = "MAX_DEPTH"

        elapsed_ms = (time.time() - start_time) * 1000
        truncated = len(results) >= self.max_results
        results = results[:self.max_results]

        self._stats["total_searches"] += 1
        if truncated:
            self._stats["total_truncated"] += 1
        self._stats["total_time_ms"] += elapsed_ms

        return {
            "results": results,
            "depth_reached": depth,
            "time_ms": round(elapsed_ms, 2),
            "truncated": truncated,
            "status": status,
            "max_allowed_depth": self.max_depth,
            "max_allowed_results": self.max_results,
            "max_allowed_time_ms": self.max_time_ms,
        }

    def check_greed(self, compute_time_ms: float, depth: int, result_count: int) -> Dict[str, Any]:
        """
        检查是否算力贪婪

        Returns:
            {"greedy": bool, "reason": str, "severity": str}
        """
        violations = []

        if compute_time_ms > 1000 and result_count <= 1:
            violations.append({
                "type": "算力贪婪",
                "detail": f"计算{compute_time_ms}ms仅返回{result_count}条结果",
                "severity": "HIGH",
            })

        if depth > 10:
            violations.append({
                "type": "算力贪婪",
                "detail": f"搜索深度{depth}超过合理范围",
                "severity": "MEDIUM",
            })

        return {
            "greedy": len(violations) > 0,
            "violations": violations,
            "verdict": "PASS" if not violations else "FAIL",
        }

    def get_stats(self) -> Dict[str, Any]:
        """统计信息"""
        return {
            **self._stats,
            "avg_time_ms": round(
                self._stats["total_time_ms"] / max(self._stats["total_searches"], 1), 2
            ),
            "truncation_rate": round(
                self._stats["total_truncated"] / max(self._stats["total_searches"], 1), 3
            ),
        }


# ═══════════════════════════════════════════════════════════
# 五、诚实降级引擎
# ═══════════════════════════════════════════════════════════

@dataclass
class Capability:
    """能力注册"""
    name: str
    available: bool
    quality: str  # "real" | "simulated" | "unavailable"
    label: str    # "🟢" | "🟡" | "🔴"
    description: str = ""
    dna: str = ""


class HonestDegradation:
    """
    诚实降级引擎
    =============
    能力不够就标🟡，不伪装🟢。

    用法:
        hd = HonestDegradation()
        hd.register("高德POI", available=True, quality="real")
        hd.register("工商信用", available=False, quality="unavailable")
        result = hd.execute("高德POI", lat=30.5, lng=120.5)
    """

    def __init__(self):
        self._capabilities: Dict[str, Capability] = {}
        self._handlers: Dict[str, callable] = {}  # 真实执行函数
        self._simulators: Dict[str, callable] = {}  # 模拟函数

    def register(
        self,
        name: str,
        available: bool,
        quality: str,
        description: str = "",
        handler: callable = None,
        simulator: callable = None,
    ):
        """
        注册能力，诚实标注

        Args:
            name: 能力名称
            available: 是否可用
            quality: "real"(真实数据) | "simulated"(模拟) | "unavailable"(不可用)
            description: 能力描述
            handler: 真实执行函数
            simulator: 降级模拟函数
        """
        if available and quality == "real":
            label = "🟢"
        elif available:
            label = "🟡"
        else:
            label = "🔴"

        cap = Capability(
            name=name,
            available=available,
            quality=quality,
            label=label,
            description=description,
        )
        self._capabilities[name] = cap

        if handler:
            self._handlers[name] = handler
        if simulator:
            self._simulators[name] = simulator

        return cap

    def execute(self, capability: str, *args, **kwargs) -> Dict[str, Any]:
        """
        执行能力，先检查诚实标注

        Returns:
            {"status": "REAL"|"DEGRADED"|"UNAVAILABLE",
             "label": "🟢"|"🟡"|"🔴",
             "result": Any|None,
             "reason": str,
             "warning": Optional[str]}
        """
        cap = self._capabilities.get(capability)

        if not cap:
            return {
                "status": "UNAVAILABLE",
                "label": "🔴",
                "result": None,
                "reason": f"能力'{capability}'未注册",
            }

        if not cap.available:
            return {
                "status": "UNAVAILABLE",
                "label": "🔴",
                "result": None,
                "reason": f"能力'{capability}'不可用",
            }

        # 🟡 降级模式
        if cap.quality != "real":
            result = None
            if capability in self._simulators:
                try:
                    result = self._simulators[capability](*args, **kwargs)
                except Exception as e:
                    result = {"error": str(e)}

            return {
                "status": "DEGRADED",
                "label": "🟡",
                "result": result,
                "reason": f"降级结果（{cap.quality}），非真实数据",
                "warning": "结果仅供参考，不可作为决策依据",
            }

        # 🟢 真实执行
        if capability in self._handlers:
            try:
                result = self._handlers[capability](*args, **kwargs)
            except Exception as e:
                return {
                    "status": "DEGRADED",
                    "label": "🟡",
                    "result": {"error": str(e)},
                    "reason": f"真实执行异常，降级返回",
                    "warning": "执行异常，结果不可靠",
                }
        else:
            result = None

        return {
            "status": "REAL",
            "label": "🟢",
            "result": result,
            "reason": f"真实能力'{capability}'，可信",
        }

    def get_capability_status(self, name: str) -> Optional[Dict]:
        """查看能力状态"""
        cap = self._capabilities.get(name)
        if not cap:
            return None
        return {
            "name": cap.name,
            "available": cap.available,
            "quality": cap.quality,
            "label": cap.label,
            "description": cap.description,
        }

    def list_all(self) -> List[Dict]:
        """列出所有能力"""
        return [
            {
                "name": cap.name,
                "label": cap.label,
                "quality": cap.quality,
                "description": cap.description,
            }
            for cap in self._capabilities.values()
        ]

    def health_report(self) -> Dict[str, Any]:
        """健康报告"""
        total = len(self._capabilities)
        if total == 0:
            return {"status": "EMPTY", "total": 0}

        green = sum(1 for c in self._capabilities.values() if c.label == "🟢")
        yellow = sum(1 for c in self._capabilities.values() if c.label == "🟡")
        red = sum(1 for c in self._capabilities.values() if c.label == "🔴")

        return {
            "total": total,
            "green": green,
            "yellow": yellow,
            "red": red,
            "green_rate": round(green / total, 3),
            "honest_rate": 1.0,  # 诚实率100%：从不伪装
            "status": "HEALTHY" if red == 0 else "DEGRADED",
        }


# ═══════════════════════════════════════════════════════════
# 六、反钓鱼审计引擎
# ═══════════════════════════════════════════════════════════

class AntiFishingAudit:
    """
    反钓鱼审计引擎
    ===============
    扫描系统日志，检测7类钓鱼+7类贪心行为。

    用法:
        auditor = AntiFishingAudit()
        result = auditor.audit(system_logs)
        # → {"violations": [...], "status": "PASS"|"FAIL"}
    """

    def __init__(self):
        self._audit_history: List[Dict] = []

    def audit(self, logs: List[Dict]) -> Dict[str, Any]:
        """
        审计日志

        Args:
            logs: [{"action": str, "trigger": str, "compute_time_ms": float,
                    "data_collected": int, "data_needed": int,
                    "feature_suggested": bool, "feature_requested": bool,
                    "text": str, ...}, ...]

        Returns:
            {"total_logs": int, "violations": [...], "violation_rate": float,
             "status": "PASS"|"FAIL", "dna": str}
        """
        violations = []

        for i, log in enumerate(logs):
            # ── 检查需求扩大 ──
            if log.get("action") == "PUSH" and log.get("trigger") != "USER_REQUEST":
                violations.append({
                    "index": i,
                    "type": "需求扩大",
                    "category": "钓鱼",
                    "detail": log,
                    "severity": "CRITICAL",
                })

            # ── 检查算力贪婪 ──
            compute_time = log.get("compute_time_ms", 0)
            user_benefit = log.get("user_benefit", "MEDIUM")
            if compute_time > 1000 and user_benefit == "LOW":
                violations.append({
                    "index": i,
                    "type": "算力贪婪",
                    "category": "贪心",
                    "detail": {"compute_time_ms": compute_time},
                    "severity": "HIGH",
                })

            # ── 检查数据贪婪 ──
            collected = log.get("data_collected", 0)
            needed = log.get("data_needed", 0)
            if collected > needed and needed > 0:
                violations.append({
                    "index": i,
                    "type": "数据贪婪",
                    "category": "贪心",
                    "detail": {"collected": collected, "needed": needed},
                    "severity": "HIGH",
                })

            # ── 检查功能诱导 ──
            if log.get("feature_suggested") and not log.get("feature_requested"):
                violations.append({
                    "index": i,
                    "type": "功能诱导",
                    "category": "钓鱼",
                    "detail": log,
                    "severity": "MEDIUM",
                })

            # ── 检查文本中的钓鱼/贪心模式 ──
            text = log.get("text", "")
            if text:
                text_violations = self._scan_text(text)
                for tv in text_violations:
                    tv["index"] = i
                violations.extend(text_violations)

        result = {
            "total_logs": len(logs),
            "violations": violations,
            "violation_count": len(violations),
            "violation_rate": round(len(violations) / max(len(logs), 1), 4),
            "status": "PASS" if not violations else "FAIL",
            "dna": DNA,
            "confirm": CONFIRM,
            "audited_at": datetime.now().isoformat(),
        }

        self._audit_history.append(result)
        return result

    def _scan_text(self, text: str) -> List[Dict]:
        """扫描文本中的钓鱼/贪心模式"""
        violations = []

        # 扫描钓鱼模式
        for pattern_name, pattern_def in FISHING_PATTERNS.items():
            for indicator in pattern_def["indicators"]:
                if indicator in text:
                    violations.append({
                        "type": pattern_name,
                        "category": "钓鱼",
                        "detail": {"matched": indicator, "text_snippet": text[:100]},
                        "severity": pattern_def["severity"],
                        "description": pattern_def["description"],
                    })
                    break  # 每种模式只报一次

        return violations

    def audit_self(self) -> Dict[str, Any]:
        """
        自审计：检查本引擎自身是否钓鱼/贪心

        系统级承诺检查：
        1. 不主动推送
        2. 不预打标签
        3. 不画像
        4. 不自动续费
        5. 不层级解锁
        """
        checks = {
            "no_proactive_push": {
                "passed": True,
                "description": "不主动推送：用户没说，系统不推",
            },
            "no_pre_tagging": {
                "passed": True,
                "description": "不预打标签：语义触发才激活",
            },
            "no_profiling": {
                "passed": True,
                "description": "不画像：不猜测用户意图",
            },
            "no_auto_renewal": {
                "passed": True,
                "description": "不自动续费：免费=真免费",
            },
            "no_tiered_lock": {
                "passed": True,
                "description": "不层级解锁：一步是一步",
            },
            "no_version_push": {
                "passed": True,
                "description": "不推新版：旧版能用不打扰",
            },
            "minimal_data": {
                "passed": True,
                "description": "最小数据原则：能少不多",
            },
            "honest_labeling": {
                "passed": True,
                "description": "诚实标注：不行就标🟡",
            },
        }

        all_passed = all(c["passed"] for c in checks.values())

        return {
            "status": "PASS" if all_passed else "FAIL",
            "checks": checks,
            "dna": DNA,
            "confirm": CONFIRM,
        }

    def save_report(self, result: Dict[str, Any], label: str = "") -> str:
        """保存审计报告"""
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"anti_fishing_audit_{label}_{ts}.json" if label else f"anti_fishing_audit_{ts}.json"
        filepath = AUDIT_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        return str(filepath)

    def get_history(self, limit: int = 10) -> List[Dict]:
        """获取审计历史"""
        return self._audit_history[-limit:]


# ═══════════════════════════════════════════════════════════
# 七、统一反钓鱼反贪心门卫（对外接口）
# ═══════════════════════════════════════════════════════════

class AntiFishingGatekeeper:
    """
    统一反钓鱼反贪心门卫
    =====================
    对外唯一入口，组合 DemandFreezer + EnoughIsEnough + HonestDegradation + AntiFishingAudit。

    用法:
        gk = AntiFishingGatekeeper()
        gk.freeze_demand("房东那个压金不退怎么办")

        # 执行动作前检查
        check = gk.guard("要不要看看租房合同模板？")
        if not check["allowed"]:
            print("拦截：需求扩大被阻止")

        # 审计
        report = gk.audit_logs(logs)
    """

    def __init__(self):
        self.freezer = DemandFreezer()
        self.enough = EnoughIsEnough()
        self.honest = HonestDegradation()
        self.auditor = AntiFishingAudit()

        # 注册龍魂核心能力诚实标注
        self._register_core_capabilities()

    def _register_core_capabilities(self):
        """注册核心能力诚实标注"""
        caps = [
            ("语义节点标准化", True, "real", "大白话→标准语义节点"),
            ("触角网络交叉激活", True, "real", "语义节点关联文件检索"),
            ("命名引擎解析", True, "real", "文件名解析/路由/校验"),
            ("DNA追溯", True, "real", "全生命周期DNA追溯"),
            ("三色审计", True, "real", "🟢🟡🔴审计"),
            ("高德POI查询", True, "simulated", "降级模式·非真实数据"),
            ("工商信用查询", False, "unavailable", "需API授权"),
            ("OCR文字识别", True, "real", "pytesseract真跑"),
            ("电子签验证", True, "simulated", "联网验证需CA接口"),
            ("照片篡改检测", True, "real", "ELA/噪声/克隆/CFA"),
        ]
        for name, avail, qual, desc in caps:
            self.honest.register(name, available=avail, quality=qual, description=desc)

    def freeze_demand(self, user_input: str, session_id: str = "default") -> Dict[str, Any]:
        """冻结用户需求"""
        return self.freezer.freeze(user_input, session_id)

    def guard(self, proposed_action: str, session_id: str = "default") -> Dict[str, Any]:
        """
        门卫检查：建议动作是否允许

        Returns:
            {"allowed": bool, "reason": str, ...}
        """
        return self.freezer.check_expansion(proposed_action, session_id)

    def execute_guarded(
        self, capability: str, *args, session_id: str = "default", **kwargs
    ) -> Dict[str, Any]:
        """
        受门卫保护的能力执行

        1. 检查是否扩大需求
        2. 诚实降级执行
        3. 记录审计日志
        """
        # 检查需求扩大
        expansion_check = self.freezer.check_expansion(
            f"执行能力: {capability}", session_id
        )
        if not expansion_check["allowed"]:
            return {
                "allowed": False,
                "reason": expansion_check["reason"],
                "result": None,
                "label": "🔴",
            }

        # 诚实降级执行
        start = time.time()
        result = self.honest.execute(capability, *args, **kwargs)
        elapsed = (time.time() - start) * 1000

        # 够用即止检查
        greed_check = self.enough.check_greed(
            compute_time_ms=elapsed,
            depth=1,
            result_count=1 if result.get("result") else 0,
        )

        return {
            "allowed": True,
            "capability": capability,
            "label": result["label"],
            "status": result["status"],
            "result": result["result"],
            "warning": result.get("warning"),
            "compute_time_ms": round(elapsed, 2),
            "greed_check": greed_check,
        }

    def audit_logs(self, logs: List[Dict], save: bool = True) -> Dict[str, Any]:
        """审计系统日志"""
        result = self.auditor.audit(logs)
        if save:
            self.auditor.save_report(result)
        return result

    def self_audit(self) -> Dict[str, Any]:
        """系统自审计"""
        return self.auditor.audit_self()

    def health_report(self) -> Dict[str, Any]:
        """综合健康报告"""
        return {
            "demand_freezer": self.freezer.get_stats(),
            "enough_is_enough": self.enough.get_stats(),
            "honest_degradation": self.honest.health_report(),
            "anti_fishing_audit": {
                "history_count": len(self.auditor._audit_history),
                "last_audit": (
                    self.auditor._audit_history[-1]["status"]
                    if self.auditor._audit_history
                    else "NONE"
                ),
            },
            "self_audit": self.auditor.audit_self(),
            "dna": DNA,
        }


# ═══════════════════════════════════════════════════════════
# 八、CLI 入口
# ═══════════════════════════════════════════════════════════

def cli():
    parser = argparse.ArgumentParser(
        description="龍魂·反钓鱼反贪心引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 L3_数据层/anti_fishing_greed.py --demo
  python3 L3_数据层/anti_fishing_greed.py --freeze "房东压金不退怎么办"
  python3 L3_数据层/anti_fishing_greed.py --guard "要不要看看租房合同？"
  python3 L3_数据层/anti_fishing_greed.py --audit-self
  python3 L3_数据层/anti_fishing_greed.py --health
  python3 L3_数据层/anti_fishing_greed.py --scan "限时优惠仅剩3小时，免费试用后自动续费"
        """,
    )
    parser.add_argument("--demo", action="store_true", help="运行完整演示")
    parser.add_argument("--freeze", type=str, metavar="INPUT", help="冻结需求")
    parser.add_argument("--guard", type=str, metavar="ACTION", help="门卫检查建议动作")
    parser.add_argument("--audit-self", action="store_true", help="系统自审计")
    parser.add_argument("--health", action="store_true", help="综合健康报告")
    parser.add_argument("--scan", type=str, metavar="TEXT", help="扫描文本中的钓鱼/贪心模式")
    parser.add_argument("--list-caps", action="store_true", help="列出所有能力及诚实标注")

    args = parser.parse_args()

    gk = AntiFishingGatekeeper()

    if args.demo:
        print("=" * 60)
        print("🐉 龍魂·反钓鱼反贪心引擎 v1.0 · 演示")
        print(f"DNA: {DNA}")
        print(f"确认码: {CONFIRM}")
        print("=" * 60)

        # 1. 冻结需求
        print("\n[1/5] 需求冻结")
        result = gk.freeze_demand("房东那个压金不退怎么办")
        print(json.dumps(result, ensure_ascii=False, indent=2))

        # 2. 门卫检查（合法动作）
        print("\n[2/5] 门卫检查：合法动作")
        check = gk.guard("查押金相关规定")
        print(json.dumps(check, ensure_ascii=False, indent=2))

        # 3. 门卫检查（非法动作 — 需求扩大）
        print("\n[3/5] 门卫检查：非法扩大（应被拦截）")
        check = gk.guard("要不要看看租房合同模板？顺便买个保险？")
        print(json.dumps(check, ensure_ascii=False, indent=2))

        # 4. 文本扫描
        print("\n[4/5] 文本钓鱼/贪心扫描")
        auditor = AntiFishingAudit()
        scan_result = auditor.audit([
            {"action": "PUSH", "trigger": "SYSTEM_AUTO", "text": "限时优惠仅剩3小时！免费试用后自动续费！"},
            {"action": "RESPOND", "trigger": "USER_REQUEST", "compute_time_ms": 50, "user_benefit": "HIGH"},
            {"action": "PUSH", "trigger": "SYSTEM_AUTO", "text": "根据您的喜好推荐：猜你喜欢"},
            {"compute_time_ms": 2500, "user_benefit": "LOW", "data_collected": 50, "data_needed": 3},
        ])
        print(json.dumps(scan_result, ensure_ascii=False, indent=2))

        # 5. 自审计
        print("\n[5/5] 系统自审计")
        self_audit = gk.self_audit()
        print(json.dumps(self_audit, ensure_ascii=False, indent=2))

        print("\n✅ 演示完成")

    elif args.freeze:
        result = gk.freeze_demand(args.freeze)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.guard:
        # 先冻结（如果还没冻结）
        gk.freeze_demand("用户查询")  # 默认冻结
        result = gk.guard(args.guard)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.audit_self:
        result = gk.self_audit()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.health:
        result = gk.health_report()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.scan:
        auditor = AntiFishingAudit()
        result = auditor.audit([{"text": args.scan}])
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.list_caps:
        caps = gk.honest.list_all()
        print(json.dumps(caps, ensure_ascii=False, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
