#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                     龍魂体系 · 德者永生殿 v2.0                                 ║
║              LongHun Hall of Eternal Merit v2.0                           ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️2026-03-30-路由回流协议-v2.0                                       ║
║  授权: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅                                  ║
║  守门人: ⚖️ 龍芯·姜子牙（P13）                                                  ║
║  管辖库: 🧬 龍芯·德者永生殿                                                     ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                                ║
╚═══════════════════════════════════════════════════════════════════════════════╝

《道德经》第七十九章："天道无亲，常与善人。"

德者永生殿核心职能：
1. 记录人格调用与贡献（谁用了，谁加分）
2. 计算贡献值 v2.0（总调用 + 准确率 + 信任等级 + 七维覆盖 + 专属测试 - 警告 - 熔断）
3. 活跃度自动评级与三色审计联动
4. IP 路由注册规范 v2.0（含乔接/小艺/MCP 分组）
5. 信任等级晋升机制（老大一人授权）
6. 姜子牙自动化职责对接（每周检查、晋升汇报、违规记录、七维统计）
"""

import json
import math
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum


# ═══════════════════════════════════════════════════════════════════════════════
# 常量与枚举
# ═══════════════════════════════════════════════════════════════════════════════

UID = "UID9622"
OPERATOR = "龍芯北辰·诸葛鑫"
VERSION = "v2.0"

DNA_SIGNATURE = "#龍芯⚡️2026-03-30-路由回流协议-v2.0"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


class AuditColor(str, Enum):
    """三色审计"""
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


class ActivityLevel(str, Enum):
    """活跃度标签"""
    HIGH = "🔥 高频"
    NORMAL = "✅ 正常"
    LOW = "⚠️ 低频"
    DORMANT = "❌ 休眠"


class TrustLevel(str, Enum):
    """信任等级 L1~L5"""
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"
    L5 = "L5"


TRUST_SCORES = {
    TrustLevel.L1: 20,
    TrustLevel.L2: 40,
    TrustLevel.L3: 60,
    TrustLevel.L4: 80,
    TrustLevel.L5: 100,
}

TRUST_LABELS = {
    TrustLevel.L1: "见习 ⭐",
    TrustLevel.L2: "正式 ⭐⭐",
    TrustLevel.L3: "核心 ⭐⭐⭐",
    TrustLevel.L4: "战略 ⭐⭐⭐⭐",
    TrustLevel.L5: "元老 ⭐⭐⭐⭐⭐",
}


# 晋升门槛（建议值，老大可随时调整）
PROMOTION_THRESHOLDS = {
    (TrustLevel.L1, TrustLevel.L2): {"contribution": 50, "no_warning": True},
    (TrustLevel.L2, TrustLevel.L3): {"contribution": 150, "no_fuse": True},
    (TrustLevel.L3, TrustLevel.L4): {"contribution": 400, "boss_recognition": True, "seven_dim_min": 3},
    (TrustLevel.L4, TrustLevel.L5): {"contribution": 1000, "boss_appoint": True},
}


# IP 路由分组规范
IP_ROUTE_GROUPS = {
    "core": {"prefix": "dragon-soul.local/core/", "priority": "P0", "color": "🔴"},
    "platform": {"prefix": "dragon-soul.local/platform/", "priority": "P1", "color": "🟠"},
    "strategic": {"prefix": "dragon-soul.local/strategic/", "priority": "P2", "color": "🟡"},
    "exec": {"prefix": "dragon-soul.local/exec/", "priority": "P2", "color": "🟡"},
    "qiaojie": {"prefix": "dragon-soul.local/qiaojie/", "priority": "P2", "color": "🟡"},
    "xiaoyi": {"prefix": "dragon-soul.local/xiaoyi/", "priority": "P2", "color": "🟡"},
    "digital_human": {"prefix": "dragon-soul.local/", "priority": "P3", "color": "⚪"},
}


# ═══════════════════════════════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class PersonaMeritRecord:
    """单个人格在德者永生殿中的完整档案"""
    code: str
    name: str
    total_invocations: int = 0
    weekly_invocations: int = 0
    monthly_invocations: int = 0
    help_count: int = 0
    weekly_help_count: int = 0
    monthly_help_count: int = 0
    test_contributions: int = 0
    warnings: int = 0
    fuses: int = 0
    accuracy_rate: float = 0.95
    trust_level: str = "L1"
    seven_dim_coverage: List[str] = field(default_factory=list)
    last_active_at: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class IPRouteRecord:
    """IP 路由注册记录"""
    persona_code: str
    persona_name: str
    group: str
    ip: str
    route_id: str
    priority: str
    priority_color: str
    active: bool = True
    registered_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ═══════════════════════════════════════════════════════════════════════════════
# 德者永生殿主类
# ═══════════════════════════════════════════════════════════════════════════════

class 德者永生殿:
    """
    德者永生殿 v2.0
    功过分明，德者永生，无德者退场。
    """

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.registry_path = self.base_dir / "persona_registry.json"
        self.state_path = self.base_dir / "merit_hall_state.json"
        self.ip_routing_path = self.base_dir / "ip_routing_registry.json"

        self.registry = self._load_json(self.registry_path)
        self.state = self._load_json(self.state_path)
        self.ip_registry = self._load_json(self.ip_routing_path)

        self.personas = self.registry.get("personas", {})
        self._ensure_state()

    def _load_json(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_json(self, path: Path, data: Dict[str, Any]):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _ensure_state(self):
        """确保 state 中包含所有注册人格的 merit 记录"""
        records = self.state.setdefault("records", {})
        for code, info in self.personas.items():
            if code not in records:
                records[code] = PersonaMeritRecord(
                    code=code,
                    name=info.get("name", code),
                    trust_level=info.get("trust_level", "L1"),
                ).to_dict()
        self._save_json(self.state_path, self.state)

    # ───────────────────────────────────────────────────────────────────────────
    # 1. 调用与贡献记录
    # ───────────────────────────────────────────────────────────────────────────

    def record_invocation(self, persona_code: str, test_mode: bool = False,
                          dimensions: Optional[List[str]] = None) -> Dict[str, Any]:
        """记录一次人格调用"""
        if persona_code not in self.personas:
            return {"error": f"人格 {persona_code} 未注册"}

        record = self.state["records"].setdefault(
            persona_code,
            PersonaMeritRecord(code=persona_code, name=self.personas[persona_code]["name"]).to_dict()
        )

        record["total_invocations"] = record.get("total_invocations", 0) + 1
        record["weekly_invocations"] = record.get("weekly_invocations", 0) + 1
        record["monthly_invocations"] = record.get("monthly_invocations", 0) + 1
        record["last_active_at"] = datetime.now().isoformat()

        if test_mode:
            record["test_contributions"] = record.get("test_contributions", 0) + 1

        if dimensions:
            existing = set(record.get("seven_dim_coverage", []))
            existing.update(dimensions)
            record["seven_dim_coverage"] = sorted(existing)

        self._save_json(self.state_path, self.state)
        return self._build_activity_result(persona_code)

    def record_help(self, persona_code: str) -> Dict[str, Any]:
        """记录人格帮助用户解决了一次问题"""
        if persona_code not in self.personas:
            return {"error": f"人格 {persona_code} 未注册"}

        record = self.state["records"][persona_code]
        record["help_count"] = record.get("help_count", 0) + 1
        record["weekly_help_count"] = record.get("weekly_help_count", 0) + 1
        record["monthly_help_count"] = record.get("monthly_help_count", 0) + 1
        record["last_active_at"] = datetime.now().isoformat()

        self._save_json(self.state_path, self.state)
        return self._build_activity_result(persona_code)

    def record_warning(self, persona_code: str, reason: str = "") -> Dict[str, Any]:
        """记录一次警告"""
        if persona_code not in self.personas:
            return {"error": f"人格 {persona_code} 未注册"}

        record = self.state["records"][persona_code]
        record["warnings"] = record.get("warnings", 0) + 1

        # 写草日志
        self._append_grass_log("warning", {
            "persona_code": persona_code,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        })
        self._save_json(self.state_path, self.state)
        return self._build_activity_result(persona_code)

    def record_fuse(self, persona_code: str, reason: str = "") -> Dict[str, Any]:
        """记录一次熔断"""
        if persona_code not in self.personas:
            return {"error": f"人格 {persona_code} 未注册"}

        record = self.state["records"][persona_code]
        record["fuses"] = record.get("fuses", 0) + 1

        self._append_grass_log("fuse", {
            "persona_code": persona_code,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        })
        self._save_json(self.state_path, self.state)
        return self._build_activity_result(persona_code)

    def set_accuracy(self, persona_code: str, accuracy: float):
        """更新执行准确率"""
        if persona_code not in self.personas:
            return {"error": f"人格 {persona_code} 未注册"}
        record = self.state["records"][persona_code]
        record["accuracy_rate"] = max(0.0, min(1.0, accuracy))
        self._save_json(self.state_path, self.state)
        return self._build_activity_result(persona_code)

    # ───────────────────────────────────────────────────────────────────────────
    # 2. 贡献值计算 v2.0
    # ───────────────────────────────────────────────────────────────────────────

    def calculate_contribution(self, persona_code: str) -> Dict[str, Any]:
        """计算人格贡献值（v2.0 公式）"""
        if persona_code not in self.state["records"]:
            return {"error": f"人格 {persona_code} 无记录"}

        record = self.state["records"][persona_code]
        total_inv = record.get("total_invocations", 0)
        accuracy = record.get("accuracy_rate", 0.95)
        trust_level = TrustLevel(record.get("trust_level", "L1"))
        trust_score = TRUST_SCORES.get(trust_level, 20)
        warnings = record.get("warnings", 0)
        fuses = record.get("fuses", 0)
        test_contributions = record.get("test_contributions", 0)
        dim_count = len(record.get("seven_dim_coverage", []))

        # 七维覆盖加成
        if dim_count >= 6:
            dim_bonus = 35
        elif dim_count >= 4:
            dim_bonus = 22
        elif dim_count >= 2:
            dim_bonus = 12
        elif dim_count >= 1:
            dim_bonus = 5
        else:
            dim_bonus = 0

        contribution = (
            total_inv * 0.40
            + accuracy * 100 * 0.30
            + trust_score * 0.30
            + dim_bonus
            + test_contributions * 2
            - warnings * 5
            - fuses * 20
        )

        return {
            "persona_code": persona_code,
            "persona_name": record.get("name", ""),
            "contribution": round(contribution, 2),
            "breakdown": {
                "total_invocations": total_inv,
                "invocation_score": round(total_inv * 0.40, 2),
                "accuracy": accuracy,
                "accuracy_score": round(accuracy * 100 * 0.30, 2),
                "trust_level": trust_level.value,
                "trust_score": trust_score,
                "trust_weighted": round(trust_score * 0.30, 2),
                "seven_dim_count": dim_count,
                "seven_dim_bonus": dim_bonus,
                "test_contributions": test_contributions,
                "test_bonus": test_contributions * 2,
                "warnings": warnings,
                "warning_penalty": warnings * 5,
                "fuses": fuses,
                "fuse_penalty": fuses * 20,
            }
        }

    # ───────────────────────────────────────────────────────────────────────────
    # 3. 活跃度评级与三色审计
    # ───────────────────────────────────────────────────────────────────────────

    def get_activity_status(self, persona_code: str) -> Dict[str, Any]:
        """获取人格活跃度评级与三色审计"""
        if persona_code not in self.state["records"]:
            return {"error": f"人格 {persona_code} 无记录"}

        record = self.state["records"][persona_code]
        last_active = record.get("last_active_at")
        weekly = record.get("weekly_invocations", 0)

        if last_active is None:
            level = ActivityLevel.DORMANT
            color = AuditColor.RED
        else:
            last = datetime.fromisoformat(last_active)
            days_inactive = (datetime.now() - last).days

            if days_inactive > 90:
                level = ActivityLevel.DORMANT
                color = AuditColor.RED
            elif days_inactive > 30:
                level = ActivityLevel.LOW
                color = AuditColor.YELLOW
            elif days_inactive > 7:
                level = ActivityLevel.NORMAL
                color = AuditColor.GREEN
            else:
                level = ActivityLevel.HIGH
                color = AuditColor.GREEN

        contribution = self.calculate_contribution(persona_code)

        return {
            "persona_code": persona_code,
            "persona_name": record.get("name", ""),
            "activity_level": level.value,
            "audit_color": color.value,
            "last_active_at": last_active,
            "weekly_invocations": weekly,
            "monthly_invocations": record.get("monthly_invocations", 0),
            "contribution": contribution.get("contribution", 0),
            "trust_level": record.get("trust_level", "L1"),
            "audit_status": f"{color.value} {level.value} · 本周调用 {weekly} 次 · 贡献值 {contribution.get('contribution', 0)}",
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-活跃度更新-{persona_code}-{VERSION}",
        }

    # ───────────────────────────────────────────────────────────────────────────
    # 4. IP 路由注册 v2.0
    # ───────────────────────────────────────────────────────────────────────────

    def register_ip_route(self, persona_code: str, group: str, persona_name_key: str = "",
                          route_seq: Optional[int] = None, active: bool = True) -> Dict[str, Any]:
        """注册人格 IP 路由"""
        if persona_code not in self.personas:
            return {"error": f"人格 {persona_code} 未注册"}
        if group not in IP_ROUTE_GROUPS:
            return {"error": f"分组 {group} 不存在，可用: {list(IP_ROUTE_GROUPS.keys())}"}

        info = self.personas[persona_code]
        name = persona_name_key or info.get("name", persona_code)
        prefix = IP_ROUTE_GROUPS[group]["prefix"]
        ip = f"{prefix}{name.lower().replace(' ', '_')}"

        seq = route_seq or (len(self.ip_registry.get("routes", [])) + 1)
        route_id = f"{UID}-{persona_code}-{seq:03d}"

        route = IPRouteRecord(
            persona_code=persona_code,
            persona_name=info.get("name", ""),
            group=group,
            ip=ip,
            route_id=route_id,
            priority=IP_ROUTE_GROUPS[group]["priority"],
            priority_color=IP_ROUTE_GROUPS[group]["color"],
            active=active,
        ).to_dict()

        routes = self.ip_registry.setdefault("routes", [])
        # 去重：同一人格同一分组只保留一个
        routes = [r for r in routes if not (r["persona_code"] == persona_code and r["group"] == group)]
        routes.append(route)
        self.ip_registry["routes"] = routes
        self.ip_registry["_meta"] = {
            "DNA": DNA_SIGNATURE,
            "version": VERSION,
            "last_updated": datetime.now().isoformat(),
        }
        self._save_json(self.ip_routing_path, self.ip_registry)
        return route

    def get_ip_route(self, persona_code: str) -> Optional[Dict[str, Any]]:
        """获取人格 IP 路由"""
        routes = self.ip_registry.get("routes", [])
        for r in routes:
            if r["persona_code"] == persona_code:
                return r
        return None

    # ───────────────────────────────────────────────────────────────────────────
    # 5. 信任等级晋升
    # ───────────────────────────────────────────────────────────────────────────

    def check_promotion_eligibility(self, persona_code: str) -> Dict[str, Any]:
        """检查人格是否满足晋升条件"""
        if persona_code not in self.state["records"]:
            return {"error": f"人格 {persona_code} 无记录"}

        record = self.state["records"][persona_code]
        current = TrustLevel(record.get("trust_level", "L1"))

        levels = [TrustLevel.L1, TrustLevel.L2, TrustLevel.L3, TrustLevel.L4, TrustLevel.L5]
        idx = levels.index(current)
        if idx >= len(levels) - 1:
            return {"persona_code": persona_code, "eligible": False, "reason": "已是最高等级"}

        next_level = levels[idx + 1]
        threshold = PROMOTION_THRESHOLDS.get((current, next_level), {})
        contrib = self.calculate_contribution(persona_code)
        contrib_value = contrib.get("contribution", 0)

        checks = {
            "contribution_enough": contrib_value >= threshold.get("contribution", 0),
            "no_warning": (not threshold.get("no_warning", False)) or record.get("warnings", 0) == 0,
            "no_fuse": (not threshold.get("no_fuse", False)) or record.get("fuses", 0) == 0,
            "boss_recognition": not threshold.get("boss_recognition", False),
            "seven_dim_ok": (not threshold.get("seven_dim_min", False)) or len(record.get("seven_dim_coverage", [])) >= threshold.get("seven_dim_min", 0),
            "boss_appoint": not threshold.get("boss_appoint", False),
        }

        eligible = all(checks.values())
        return {
            "persona_code": persona_code,
            "current_level": current.value,
            "next_level": next_level.value,
            "eligible": eligible,
            "contribution": contrib_value,
            "required_contribution": threshold.get("contribution", 0),
            "checks": checks,
            "message": "可晋升" if eligible else "条件未满足",
        }

    def promote(self, persona_code: str, new_level: str, authorized_by: str = UID) -> Dict[str, Any]:
        """
        晋升人格信任等级
        必须由老大（UID9622）授权
        """
        if authorized_by != UID:
            return {"error": "晋升必须由 UID9622 授权"}
        if persona_code not in self.state["records"]:
            return {"error": f"人格 {persona_code} 无记录"}

        record = self.state["records"][persona_code]
        old_level = record.get("trust_level", "L1")
        record["trust_level"] = new_level

        # 同步到 registry
        if persona_code in self.personas:
            self.personas[persona_code]["trust_level"] = new_level
            self.registry["_meta"]["last_updated"] = datetime.now().isoformat()
            self._save_json(self.registry_path, self.registry)

        self._save_json(self.state_path, self.state)

        # 写草日志
        self._append_grass_log("promotion", {
            "persona_code": persona_code,
            "old_level": old_level,
            "new_level": new_level,
            "authorized_by": authorized_by,
            "timestamp": datetime.now().isoformat(),
        })

        return {
            "persona_code": persona_code,
            "old_level": old_level,
            "new_level": new_level,
            "authorized_by": authorized_by,
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-PROMOTION-{persona_code}-{VERSION}",
        }

    # ───────────────────────────────────────────────────────────────────────────
    # 6. 姜子牙自动化职责
    # ───────────────────────────────────────────────────────────────────────────

    def weekly_check(self) -> Dict[str, Any]:
        """每周检查全体人格活跃度"""
        results = []
        warnings = []
        dormant = []

        for code in self.personas:
            status = self.get_activity_status(code)
            results.append(status)
            if "低频" in status["activity_level"]:
                warnings.append(code)
            if "休眠" in status["activity_level"]:
                dormant.append(code)

        self._append_grass_log("weekly_check", {
            "checked_at": datetime.now().isoformat(),
            "total": len(self.personas),
            "low_frequency": warnings,
            "dormant": dormant,
        })

        return {
            "checked_at": datetime.now().isoformat(),
            "total": len(self.personas),
            "low_frequency": warnings,
            "dormant": dormant,
            "details": results,
        }

    def reset_weekly_counters(self):
        """每周一 00:00 重置周计数器"""
        for record in self.state["records"].values():
            record["weekly_invocations"] = 0
            record["weekly_help_count"] = 0
        self.state["_meta"] = self.state.get("_meta", {})
        self.state["_meta"]["last_weekly_reset"] = datetime.now().isoformat()
        self._save_json(self.state_path, self.state)
        return {"status": "weekly counters reset"}

    def reset_monthly_counters(self):
        """每月1日 00:00 重置月计数器"""
        for record in self.state["records"].values():
            record["monthly_invocations"] = 0
            record["monthly_help_count"] = 0
        self.state["_meta"] = self.state.get("_meta", {})
        self.state["_meta"]["last_monthly_reset"] = datetime.now().isoformat()
        self._save_json(self.state_path, self.state)
        return {"status": "monthly counters reset"}

    def seven_dim_report(self) -> Dict[str, Any]:
        """每月盘点各人格七维覆盖维度数"""
        report = {}
        for code, record in self.state["records"].items():
            dims = record.get("seven_dim_coverage", [])
            report[code] = {
                "name": record.get("name", ""),
                "dim_count": len(dims),
                "dimensions": dims,
            }
        return {
            "report_at": datetime.now().isoformat(),
            "personas": report,
        }

    # ───────────────────────────────────────────────────────────────────────────
    # 内部工具
    # ───────────────────────────────────────────────────────────────────────────

    def _build_activity_result(self, persona_code: str) -> Dict[str, Any]:
        """构建一次操作后的返回结果"""
        status = self.get_activity_status(persona_code)
        contribution = self.calculate_contribution(persona_code)
        return {
            "persona_code": persona_code,
            "activity": status,
            "contribution": contribution,
        }

    def _append_grass_log(self, event_type: str, payload: Dict[str, Any]):
        """写入草日志（JSONL 追加）"""
        log_dir = self.base_dir.parent / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "merit_hall_grass.jsonl"
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "payload": payload,
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-MERIT-{event_type.upper()}-{VERSION}",
        }
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # ───────────────────────────────────────────────────────────────────────────
    # 报告与自检
    # ───────────────────────────────────────────────────────────────────────────

    def generate_report(self, limit: int = 100) -> Dict[str, Any]:
        """生成德者永生殿整体报告"""
        records = []
        for code in self.personas:
            status = self.get_activity_status(code)
            contrib = self.calculate_contribution(code)
            route = self.get_ip_route(code)
            records.append({
                "code": code,
                "name": self.personas[code].get("name", ""),
                "activity": status,
                "contribution": contrib,
                "ip_route": route,
            })

        records.sort(key=lambda x: x["contribution"].get("contribution", 0), reverse=True)

        return {
            "DNA": DNA_SIGNATURE,
            "version": VERSION,
            "generated_at": datetime.now().isoformat(),
            "total_personas": len(self.personas),
            "top_personas": records[:limit],
        }

    def selftest(self) -> Tuple[bool, List[str]]:
        """自检"""
        errors = []

        # 1. 检查注册表不为空
        if not self.personas:
            errors.append("人格注册表为空")

        # 2. 检查 state 已初始化
        if not self.state.get("records"):
            errors.append("德者永生殿状态未初始化")

        # 3. 测试调用记录
        if self.personas:
            first_code = list(self.personas.keys())[0]
            before = self.state["records"][first_code].get("total_invocations", 0)
            self.record_invocation(first_code)
            after = self.state["records"][first_code].get("total_invocations", 0)
            if after != before + 1:
                errors.append("调用记录计数失败")

        # 4. 测试贡献值计算
        if self.personas:
            first_code = list(self.personas.keys())[0]
            contrib = self.calculate_contribution(first_code)
            if "contribution" not in contrib:
                errors.append("贡献值计算失败")

        # 5. 测试活跃度
        if self.personas:
            first_code = list(self.personas.keys())[0]
            status = self.get_activity_status(first_code)
            if "audit_color" not in status:
                errors.append("活跃度评级失败")

        # 6. 测试 IP 注册
        if self.personas:
            first_code = list(self.personas.keys())[0]
            route = self.register_ip_route(first_code, "exec")
            if "route_id" not in route:
                errors.append("IP 路由注册失败")

        return len(errors) == 0, errors


# ═══════════════════════════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="德者永生殿 v2.0 命令行工具")
    parser.add_argument("--report", action="store_true", help="生成整体报告")
    parser.add_argument("--record", type=str, help="记录一次调用，参数：人格code")
    parser.add_argument("--test-mode", action="store_true", help="标记为专属测试模式调用")
    parser.add_argument("--dimensions", type=str, help="七维维度，逗号分隔，如 w1,w3,w5")
    parser.add_argument("--weekly-check", action="store_true", help="执行每周检查")
    parser.add_argument("--selftest", action="store_true", help="运行自检")
    args = parser.parse_args()

    hall = 德者永生殿()

    if args.selftest:
        ok, errors = hall.selftest()
        print("✅ 自检通过" if ok else "❌ 自检失败")
        for e in errors:
            print(f"  - {e}")
        return

    if args.report:
        report = hall.generate_report()
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    if args.weekly_check:
        result = hall.weekly_check()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.record:
        dims = args.dimensions.split(",") if args.dimensions else None
        result = hall.record_invocation(args.record, test_mode=args.test_mode, dimensions=dims)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
