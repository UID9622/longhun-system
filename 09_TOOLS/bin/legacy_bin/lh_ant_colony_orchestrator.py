#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║     🐜 龍魂 · 蚁群联动编排引擎 v1.0                              ║
║                                                                  ║
║  蚁后不动点 → 信息素网络 → 工蚁自主协作 → 闭环自治               ║
║                                                                  ║
║  协议编号：LH-PROTOCOL-ANT-COLONY-2026-0714-v1.0                 ║
║  哲学底座：蚁群算法 · 信息素轨迹 · 忠于蚁后不动点                ║
║  主权人格：UID9622 | 龍芯北辰                                     ║
║  生成时间：2026-07-14 亥时                                        ║
║                                                                  ║
║  关联协议：                                                       ║
║  - LH-PROTOCOL-RB-2026-0714-v1.0（红蓝对抗）                     ║
║  - LH-PROTOCOL-IPA-RB-2026-0714-v1.0（IPA联动触发）              ║
║  - LH-ARCH-CLOSED-LOOP-2026-0714-v1.0（闭环架构）                ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·辛未·ANT-COLONY-ORCHESTRATOR-v1.0             ║
╚══════════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_ant_colony_orchestrator.py --run          # 运行一次完整闭环
  python3 bin/lh_ant_colony_orchestrator.py --discover     # 仅脚本发现
  python3 bin/lh_ant_colony_orchestrator.py --evaluate     # 全量阈值评估
  python3 bin/lh_ant_colony_orchestrator.py --dashboard    # 蚁群仪表盘
  python3 bin/lh_ant_colony_orchestrator.py --trail <id>   # 追踪指定脚本的信息素轨迹
  python3 bin/lh_ant_colony_orchestrator.py --audit-hook   # 生成审计钩子代码
  python3 bin/lh_ant_colony_orchestrator.py --daemon       # 守护模式（持续监控）
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / ".longhun" / "ant_colony"
STATE_DIR.mkdir(parents=True, exist_ok=True)

DNA = "#龍芯⚡️丙午·辛未·ANT-COLONY-ORCHESTRATOR-v1.0"
UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 蚁后不动点（不可变精神锚点）
QUEEN_FIXED_POINTS = {
    "fp_001": {"name": "中国法律唯一准绳", "domain": "legal", "priority": "∞", "immutable": True},
    "fp_002": {"name": "技术为人民服务", "domain": "ethics", "priority": "∞", "immutable": True},
    "fp_003": {"name": "底座不动·变量可动", "domain": "architecture", "priority": "∞", "immutable": True},
    "fp_004": {"name": "人民数据主权", "domain": "sovereignty", "priority": "∞", "immutable": True},
    "fp_005": {"name": "不删除只冻结", "domain": "operations", "priority": "∞", "immutable": True},
    "fp_006": {"name": "谁签名谁负责", "domain": "governance", "priority": "∞", "immutable": True},
    "fp_007": {"name": "369不动点·河图洛书焊死", "domain": "philosophy", "priority": "∞", "immutable": True},
    "fp_008": {"name": "女儿永不抵押", "domain": "family", "priority": "∞", "immutable": True},
    "fp_009": {"name": "三色审计·一票否决", "domain": "audit", "priority": "∞", "immutable": True},
}

# 信息素类型
class PheromoneType(Enum):
    EVENT = "event"           # 事件信息素：发生了什么
    TRAIL = "trail"           # 轨迹信息素：谁做了什么
    ALARM = "alarm"           # 告警信息素：异常信号
    STATE = "state"           # 状态信息素：当前状态
    LINKAGE = "linkage"       # 关联信息素：依赖关系

# 工蚁角色
class WorkerRole(Enum):
    DISCOVERER = "discoverer"     # 发现蚁：扫描脚本
    REGISTRAR = "registrar"       # 注册蚁：归档注册
    SENTINEL = "sentinel"         # 哨兵蚁：阈值监测
    RB_RED = "rb_red"             # 红方蚁：质疑攻击
    RB_BLUE = "rb_blue"           # 蓝方蚁：防守验证
    AUDITOR = "auditor"           # 审计蚁：全程记录
    OVERSEER = "overseer"         # 监管天蚁：全局熔断
    HEALER = "healer"             # 自愈蚁：自动修复

# ═══════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════

@dataclass
class Pheromone:
    """信息素 — 蚁群间传递的信息单位"""
    id: str
    type: PheromoneType
    source: str          # 发出者（工蚁/事件）
    target: str          # 目标（工蚁/固定点）
    intensity: float     # 0.0~1.0 强度（随时间衰减）
    content: Dict[str, Any]
    timestamp: str
    ttl_seconds: int = 3600  # 存活时间
    decay_rate: float = 0.01  # 每秒衰减率

    def is_valid(self) -> bool:
        ts = datetime.fromisoformat(self.timestamp)
        elapsed = (datetime.now() - ts).total_seconds()
        self.intensity = max(0, self.intensity - elapsed * self.decay_rate)
        return self.intensity > 0.01 and elapsed < self.ttl_seconds

@dataclass
class ScriptFingerprint:
    """脚本指纹 — 每个脚本的身份信息"""
    script_id: str
    path: str
    name: str
    ext: str
    size_bytes: int
    lines: int
    hash: str
    dna_markers: List[str] = field(default_factory=list)
    fixed_point: str = "通用工具"
    upstream: List[str] = field(default_factory=list)
    downstream: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)
    has_chinese: bool = False
    registered_at: str = ""
    last_executed: str = ""
    execution_count: int = 0
    audit_history: List[Dict] = field(default_factory=list)
    optimization_history: List[Dict] = field(default_factory=list)
    status: str = "active"
    pheromone_trail: List[Dict] = field(default_factory=list)  # 信息素轨迹

@dataclass
class ThresholdAlert:
    """阈值告警"""
    alert_id: str
    script_id: str
    alert_type: str       # code_quality / freshness / execution / linkage / anomaly
    metric: str
    value: float
    threshold: float
    action: str
    priority: str         # P0/P1/P2/P3
    triggered_at: str
    handled: bool = False

@dataclass
class ColonyState:
    """蚁群全局状态"""
    total_scripts: int = 0
    registered_scripts: int = 0
    orphan_scripts: int = 0
    active_pheromones: int = 0
    alerts_firing: int = 0
    persona_activations: Dict[str, int] = field(default_factory=dict)
    rb_confrontations_today: int = 0
    last_discovery: str = ""
    last_evaluation: str = ""
    last_closed_loop: str = ""
    colony_health: float = 1.0

# ═══════════════════════════════════════════════
# 工蚁1：发现蚁 — Script Discovery
# ═══════════════════════════════════════════════

class DiscovererAnt:
    """发现蚁：扫描所有路径，发现脚本并生成指纹"""

    DISCOVERY_PATHS = [
        "~/longhun-system/bin/",
        "~/longhun-system/engine/",
        "~/longhun-system/engines/",
        "~/longhun-system/scripts/",
        "~/longhun-system/skills/",
        "~/.longhun/",
        "~/.龍魂/",
    ]

    SCRIPT_EXTENSIONS = [".py", ".sh", ".zsh", ".js", ".ts"]

    def discover(self) -> Dict[str, List[ScriptFingerprint]]:
        """扫描所有路径，返回分类脚本清单"""
        discovered: List[ScriptFingerprint] = []
        seen_hashes = set()

        EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv",
                       "site-packages", "dist", "build", ".egg", ".eggs",
                       ".codebuddy", "backups", "archive", "_archive",
                       ".DS_Store", "Library", ".Trash"}

        for raw_path in self.DISCOVERY_PATHS:
            expanded = Path(raw_path).expanduser()
            if not expanded.exists():
                continue
            for ext in self.SCRIPT_EXTENSIONS:
                for file_path in expanded.rglob(f"*{ext}"):
                    # 排除目录 + 符号链接
                    if file_path.is_symlink():
                        continue
                    parts = set(file_path.parts)
                    if parts & EXCLUDE_DIRS:
                        continue
                    try:
                        fp = self._analyze(file_path)
                        if fp.hash not in seen_hashes:
                            seen_hashes.add(fp.hash)
                            discovered.append(fp)
                    except Exception:
                        continue

        return self._categorize(discovered)

    def _analyze(self, file_path: Path) -> ScriptFingerprint:
        """分析单个脚本"""
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        lines = content.split("\n")
        stat = file_path.stat()

        script_id = hashlib.sha256(str(file_path).encode()).hexdigest()[:12]

        return ScriptFingerprint(
            script_id=script_id,
            path=str(file_path),
            name=file_path.name,
            ext=file_path.suffix,
            size_bytes=stat.st_size,
            lines=len(lines),
            hash=hashlib.sha256(content.encode()).hexdigest()[:16],
            dna_markers=self._extract_dna(content),
            fixed_point=self._determine_fixed_point(file_path.name, content),
            imports=self._extract_imports(content),
            functions=self._extract_functions(content),
            has_chinese=self._detect_chinese(content),
        )

    def _extract_dna(self, content: str) -> List[str]:
        markers = []
        triggers = {"UID9622": "UID9622", "龍魂": "龍魂", "龍芯": "龍芯",
                    "#CONFIRM": "CONFIRM", "GPG": "GPG", "丙午": "干支历"}
        for keyword, label in triggers.items():
            if keyword in content:
                markers.append(label)
        return markers

    def _determine_fixed_point(self, name: str, content: str) -> str:
        name_lower = name.lower()
        content_sample = content[:500]

        mapping = [
            (["signing", "sign", "签章", "signature"], "签章链"),
            (["rb_", "confrontation", "对抗", "红蓝"], "红蓝对抗"),
            (["threshold", "trigger", "阈值", "触发"], "阈值决策"),
            (["audit", "regulatory", "审计"], "审计管道"),
            (["persona", "人格"], "人格矩阵"),
            (["oversight", "监督", "监管天"], "监管天"),
            (["discovery", "registry", "发现", "注册"], "脚本注册"),
            (["ant_colony", "蚁群", "orchestrat"], "蚁群编排"),
            (["pipeline", "管线"], "统一管线"),
            (["health", "health_check", "健康"], "健康检查"),
            (["deploy", "部署"], "部署"),
            (["backup", "备份"], "备份"),
        ]

        for keywords, point in mapping:
            for kw in keywords:
                if kw in name_lower or kw in content_sample:
                    return point
        return "通用工具"

    def _extract_imports(self, content: str) -> List[str]:
        imports = []
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                imports.append(stripped[:80])
        return imports[:20]

    def _extract_functions(self, content: str) -> List[str]:
        funcs = []
        for line in content.split("\n"):
            stripped = line.strip()
            if stripped.startswith("def ") or stripped.startswith("class "):
                funcs.append(stripped.split("(")[0].replace("def ", "").replace("class ", ""))
        return funcs[:30]

    def _detect_chinese(self, content: str) -> bool:
        for ch in content[:1000]:
            if "\u4e00" <= ch <= "\u9fff":
                return True
        return False

    def _categorize(self, discovered: List[ScriptFingerprint]) -> Dict[str, List[ScriptFingerprint]]:
        cats = {
            "core_engine": [], "persona": [], "rb_confrontation": [],
            "audit": [], "signing": [], "threshold": [],
            "orchestrator": [], "utility": [], "orphan": [],
        }

        for s in discovered:
            n = s.name.lower()
            fp = s.fixed_point
            if fp == "红蓝对抗" or "rb_" in n:
                cats["rb_confrontation"].append(s)
            elif fp == "审计管道" or "audit" in n:
                cats["audit"].append(s)
            elif fp == "签章链" or "sign" in n:
                cats["signing"].append(s)
            elif fp == "阈值决策" or "threshold" in n:
                cats["threshold"].append(s)
            elif fp == "人格矩阵" or "persona" in n:
                cats["persona"].append(s)
            elif fp in ("蚁群编排", "统一管线", "脚本注册"):
                cats["orchestrator"].append(s)
            elif s.name.startswith("lh_"):
                cats["core_engine"].append(s)
            elif not s.dna_markers:
                cats["orphan"].append(s)
            else:
                cats["utility"].append(s)

        return cats


# ═══════════════════════════════════════════════
# 工蚁2：注册蚁 — Script Registry
# ═══════════════════════════════════════════════

class RegistrarAnt:
    """注册蚁：归档脚本指纹，建立关联网络"""

    REGISTRY_FILE = STATE_DIR / "script_registry.json"

    def __init__(self):
        self.registry = self._load()

    def _load(self) -> Dict[str, Dict]:
        if self.REGISTRY_FILE.exists():
            return json.loads(self.REGISTRY_FILE.read_text())
        return {}

    def _save(self):
        self.REGISTRY_FILE.write_text(json.dumps(self.registry, ensure_ascii=False, indent=2))

    def register(self, fp: ScriptFingerprint) -> Dict[str, Any]:
        """注册或更新脚本"""
        sid = fp.script_id
        now = datetime.now().isoformat()

        if sid in self.registry:
            existing = self.registry[sid]
            existing["path"] = fp.path
            existing["lines"] = fp.lines
            existing["hash"] = fp.hash
            existing["functions"] = fp.functions
            existing["last_checked"] = now
            self._save()
            return {"status": "updated", "script_id": sid}

        entry = {
            "script_id": sid,
            "path": fp.path,
            "name": fp.name,
            "ext": fp.ext,
            "lines": fp.lines,
            "hash": fp.hash,
            "fixed_point": fp.fixed_point,
            "dna_markers": fp.dna_markers,
            "upstream": self._find_upstream(fp),
            "downstream": [],
            "imports": fp.imports,
            "functions": fp.functions,
            "registered_at": now,
            "last_executed": "",
            "execution_count": 0,
            "audit_history": [],
            "optimization_history": [],
            "pheromone_trail": [],
            "status": "active",
        }

        self.registry[sid] = entry
        self._update_downstream_links(sid, entry["upstream"])
        self._save()

        return {"status": "registered", "script_id": sid, "fixed_point": fp.fixed_point}

    def _find_upstream(self, fp: ScriptFingerprint) -> List[str]:
        """从import语句找上游依赖"""
        upstream = set()
        local_prefixes = ["lh_", "longhun", "cnsh", "bin.", "engine."]

        for imp in fp.imports:
            for prefix in local_prefixes:
                if prefix in imp.lower():
                    mod = imp.replace("import ", "").replace("from ", "").strip().split()[0].split(".")[0]
                    if mod and mod != fp.name.replace(".py", ""):
                        upstream.add(mod)
                    break
        return list(upstream)[:10]

    def _update_downstream_links(self, new_sid: str, upstream_mods: List[str]):
        """反向填充下游依赖"""
        for sid, data in self.registry.items():
            if sid == new_sid:
                continue
            data_name = data["name"].replace(".py", "")
            for um in upstream_mods:
                if um in data_name or um in " ".join(data.get("functions", [])):
                    if new_sid not in data.get("downstream", []):
                        data.setdefault("downstream", []).append(new_sid)

    def get_all(self) -> Dict[str, Dict]:
        return self.registry

    def get_orphans(self) -> List[str]:
        orphans = []
        for sid, data in self.registry.items():
            up = len(data.get("upstream", []))
            down = len(data.get("downstream", []))
            if up + down < 1:
                orphans.append(sid)
        return orphans

    def get_stale_scripts(self, days: int = 30) -> List[str]:
        stale = []
        for sid, data in self.registry.items():
            last = data.get("last_checked", data.get("registered_at", ""))
            if last:
                days_since = (datetime.now() - datetime.fromisoformat(last)).days
                if days_since > days:
                    stale.append(sid)
        return stale


# ═══════════════════════════════════════════════
# 工蚁3：哨兵蚁 — Threshold Sentinel
# ═══════════════════════════════════════════════

class SentinelAnt:
    """哨兵蚁：持续监测阈值，自动发出告警信息素"""

    THRESHOLD_RULES = {
        "code_quality": {
            "line_count": {"warning": 300, "critical": 500, "action": "trigger_optimization"},
            "orphan": {"critical": 0, "action": "trigger_linkage_review"},  # 无关联即为孤儿
        },
        "freshness": {
            "stale_days": {"warning": 30, "critical": 90, "action": "trigger_freshness_audit"},
        },
        "execution_frequency": {
            "weekly_min": {"warning": 0, "action": "trigger_dormancy_alert"},  # 一周未激活告警
        },
    }

    def evaluate(self, registry: Dict[str, Dict]) -> List[ThresholdAlert]:
        """全量阈值评估"""
        alerts = []
        now = datetime.now().isoformat()

        for sid, data in registry.items():
            # 1. 代码质量检查
            lines = data.get("lines", 0)
            if lines > self.THRESHOLD_RULES["code_quality"]["line_count"]["critical"]:
                alerts.append(ThresholdAlert(
                    alert_id=f"ALT-{hashlib.sha256(f'{sid}-linecount'.encode()).hexdigest()[:10]}",
                    script_id=sid,
                    alert_type="code_quality",
                    metric="line_count",
                    value=lines,
                    threshold=500,
                    action="trigger_optimization",
                    priority="P1",
                    triggered_at=now,
                ))

            # 2. 关联性检查
            linkage = len(data.get("upstream", [])) + len(data.get("downstream", []))
            if linkage == 0 and data.get("fixed_point") != "通用工具":
                alerts.append(ThresholdAlert(
                    alert_id=f"ALT-{hashlib.sha256(f'{sid}-orphan'.encode()).hexdigest()[:10]}",
                    script_id=sid,
                    alert_type="linkage",
                    metric="linkage_count",
                    value=0,
                    threshold=1,
                    action="trigger_linkage_review",
                    priority="P2",
                    triggered_at=now,
                ))

            # 3. 时效性检查
            last = data.get("last_checked", data.get("registered_at", ""))
            if last:
                days_since = (datetime.now() - datetime.fromisoformat(last)).days
                if days_since > self.THRESHOLD_RULES["freshness"]["stale_days"]["critical"]:
                    alerts.append(ThresholdAlert(
                        alert_id=f"ALT-{hashlib.sha256(f'{sid}-stale'.encode()).hexdigest()[:10]}",
                        script_id=sid,
                        alert_type="freshness",
                        metric="days_stale",
                        value=days_since,
                        threshold=90,
                        action="trigger_freshness_audit",
                        priority="P2",
                        triggered_at=now,
                    ))
                elif days_since > self.THRESHOLD_RULES["freshness"]["stale_days"]["warning"]:
                    alerts.append(ThresholdAlert(
                        alert_id=f"ALT-{hashlib.sha256(f'{sid}-stalewarn'.encode()).hexdigest()[:10]}",
                        script_id=sid,
                        alert_type="freshness",
                        metric="days_stale",
                        value=days_since,
                        threshold=30,
                        action="trigger_freshness_warning",
                        priority="P3",
                        triggered_at=now,
                    ))

        return sorted(alerts, key=lambda a: int(a.priority[1]))


# ═══════════════════════════════════════════════
# 工蚁4：执行蚁 — RB/Audit/Oversee 联动
# ═══════════════════════════════════════════════

class ExecutionAnt:
    """执行蚁：实际调用红蓝对抗、审计、签章"""

    def __init__(self):
        self.rb_engine = str(ROOT / "bin" / "lh_rb_confrontation_engine.py")
        self.signing_engine = str(ROOT / "bin" / "lh_persona_signing.py")
        self.oversight_engine = str(ROOT / "bin" / "lh_oversight_bridge.py")

    def trigger_rb(self, target: str, reason: str = "") -> Dict[str, Any]:
        """触发红蓝对抗"""
        try:
            result = subprocess.run(
                ["python3", self.rb_engine, "--auto", "--trigger", "threshold", "--target", target],
                capture_output=True, text=True, timeout=120,
                cwd=str(ROOT),
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout[:500] if result.stdout else "",
                "exit_code": result.returncode,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def trigger_signing(self, persona: str, action: str, target: str) -> Dict[str, Any]:
        """触发签章"""
        try:
            result = subprocess.run(
                ["python3", self.signing_engine, "--sign", persona, "--action", action,
                 "--target", target, "--no-oversight", "--json"],
                capture_output=True, text=True, timeout=60,
                cwd=str(ROOT),
            )
            if result.stdout.strip():
                return json.loads(result.stdout)
            return {"success": result.returncode == 0}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def trigger_oversight(self, target: str, content: str = "", audit_color: str = "🟢", audit_score: float = 85.0) -> Dict[str, Any]:
        """触发监管天联动"""
        try:
            result = subprocess.run(
                ["python3", self.oversight_engine, "--trigger-audit", target,
                 "--audit-color", audit_color, "--audit-score", str(audit_score),
                 "--content", content, "--json"],
                capture_output=True, text=True, timeout=60,
                cwd=str(ROOT),
            )
            if result.stdout.strip():
                return json.loads(result.stdout)
            return {"success": result.returncode == 0}
        except Exception as e:
            return {"success": False, "error": str(e)}


# ═══════════════════════════════════════════════
# 蚁后：精神不动点守护
# ═══════════════════════════════════════════════

class QueenGuardian:
    """蚁后守护者：确保所有操作不违背不动点"""

    def validate(self, action: Dict[str, Any]) -> Tuple[bool, str]:
        """
        验证操作是否忠于蚁后不动点
        返回：(is_valid, reason)
        """
        action_type = action.get("action", "")
        target = action.get("target", "")

        # 1. 防删除检查
        delete_keywords = ["rm ", "delete", "remove", "删除", "清除"]
        for kw in delete_keywords:
            if kw in action_type.lower() or kw in str(target).lower():
                # 允许冻结但不允许真删除
                if "freeze" not in action_type.lower() and "冻结" not in action_type.lower():
                    return False, f"违反不动点fp_005（不删除只冻结）：操作含删除语义"

        # 2. 防修改核心底座
        protected_files = [
            "lh_memory_load.py", "longhun_neural_net.json",
            "BEICHEN-MOTHER-PROTOCOL", "GPG_SIGNING_REGISTRY",
        ]
        for pf in protected_files:
            if pf in str(target):
                return False, f"违反不动点fp_003（底座不动）：目标为核心底座文件"

        # 3. 签章检查（签章相关的操作必须有sign action）
        if any(kw in action_type for kw in ["执行", "新增", "变更", "修改"]):
            if "sign" not in action.get("signature_id", "").lower():
                return False, "违反不动点fp_006（谁签名谁负责）：缺少签章"

        return True, "✅ 忠于蚁后不动点"


# ═══════════════════════════════════════════════
# 信息素网络：蚁群间的信息传递总线
# ═══════════════════════════════════════════════

class PheromoneNetwork:
    """信息素网络 — 蚁群内所有信息传递的中枢"""

    PHEROMONE_FILE = STATE_DIR / "pheromone_network.jsonl"

    def __init__(self):
        self.active_pheromones: List[Pheromone] = []

    def emit(self, ptype: PheromoneType, source: str, target: str,
             intensity: float, content: Dict[str, Any], ttl: int = 3600) -> Pheromone:
        """发射信息素到网络中"""
        p = Pheromone(
            id=hashlib.sha256(f"{source}-{target}-{time.time()}".encode()).hexdigest()[:12],
            type=ptype,
            source=source,
            target=target,
            intensity=min(intensity, 1.0),
            content=content,
            timestamp=datetime.now().isoformat(),
            ttl_seconds=ttl,
        )
        self.active_pheromones.append(p)
        self._persist(p)
        return p

    def sense(self, ptype: Optional[PheromoneType] = None, source: Optional[str] = None,
              min_intensity: float = 0.1) -> List[Pheromone]:
        """感知信息素（读取网络中的信息）"""
        results = []
        for p in self.active_pheromones[:]:
            if not p.is_valid():
                self.active_pheromones.remove(p)
                continue
            if ptype and p.type != ptype:
                continue
            if source and p.source != source:
                continue
            if p.intensity < min_intensity:
                continue
            results.append(p)
        return results

    def _persist(self, p: Pheromone):
        with open(self.PHEROMONE_FILE, "a") as f:
            f.write(json.dumps({
                "id": p.id, "type": p.type.value,
                "source": p.source, "target": p.target,
                "intensity": p.intensity, "content": p.content,
                "timestamp": p.timestamp, "ttl": p.ttl_seconds,
            }, ensure_ascii=False) + "\n")

    def get_network_stats(self) -> Dict[str, Any]:
        active = sum(1 for p in self.active_pheromones if p.is_valid())
        types = {}
        for p in self.active_pheromones:
            if p.is_valid():
                types[p.type.value] = types.get(p.type.value, 0) + 1
        return {"active_pheromones": active, "by_type": types}


# ═══════════════════════════════════════════════
# 审计钩子生成器
# ═══════════════════════════════════════════════

AUDIT_HOOK_TEMPLATE = '''# 审计钩子装饰器 — 自动生成 · 不可删除
from functools import wraps
import hashlib, json, time, traceback
from pathlib import Path
from datetime import datetime

_STATE_DIR = Path.home() / ".longhun" / "ant_colony"
_STATE_DIR.mkdir(parents=True, exist_ok=True)
_AUDIT_LOG = _STATE_DIR / "audit_hook_log.jsonl"

def audit_hook(action_type: str = "执行", fixed_point: str = "通用工具"):
    """
    审计钩子装饰器
    每个函数执行自动留痕，异常自动触发红蓝对抗
    不要删除此装饰器 — 它是审计闭环的神经末梢
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sign_id = hashlib.sha256(f"{func.__name__}-{time.time()}".encode()).hexdigest()[:12]
            start = time.time()

            # 执行前信息素：即将执行
            _emit_pheromone("pre_exec", func.__name__, sign_id, action_type, fixed_point)

            try:
                result = func(*args, **kwargs)
                status = "success"
                error = None
            except Exception as e:
                result = None
                status = "error"
                error = f"{type(e).__name__}: {str(e)}"
                # 自动告警信息素
                _emit_pheromone("alarm", func.__name__, sign_id, "execution_error", fixed_point,
                               {"error": error, "traceback": traceback.format_exc()[-500:]})

            duration = time.time() - start

            # 记录审计日志
            _log(sign_id, func.__name__, action_type, fixed_point, status, duration, error)

            # 执行后信息素：已完成
            _emit_pheromone("post_exec", func.__name__, sign_id, status, fixed_point,
                           {"duration": duration})

            return result
        return wrapper
    return decorator


def _emit_pheromone(event: str, func_name: str, sign_id: str,
                    status: str, fixed_point: str, extra: dict[str, Any] = None):
    """向信息素网络发射信号"""
    record = {
        "event": event, "function": func_name, "sign_id": sign_id,
        "status": status, "fixed_point": fixed_point,
        "timestamp": datetime.now().isoformat(),
        "extra": extra or {},
    }
    with open(_AUDIT_LOG, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\\n")


def _log(sign_id, func_name, action_type, fixed_point, status, duration, error):
    with open(_AUDIT_LOG, "a") as f:
        f.write(json.dumps({
            "sign_id": sign_id, "function": func_name,
            "action_type": action_type, "fixed_point": fixed_point,
            "status": status, "duration": round(duration, 4),
            "error": error, "timestamp": datetime.now().isoformat(),
        }, ensure_ascii=False) + "\\n")
'''


# ═══════════════════════════════════════════════
# 主编排器：蚁群女王的总指挥
# ═══════════════════════════════════════════════

class AntColonyOrchestrator:
    """蚁群联动编排总引擎"""

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.discoverer = DiscovererAnt()
        self.registrar = RegistrarAnt()
        self.sentinel = SentinelAnt()
        self.executor = ExecutionAnt()
        self.guardian = QueenGuardian()
        self.pheromones = PheromoneNetwork()
        self.state_file = STATE_DIR / "colony_state.json"

    def _log(self, msg: str):
        if self.verbose:
            print(f"  🐜 {msg}")

    def _emit_state_pheromone(self, stage: str, data: Dict[str, Any]):
        """发射状态信息素"""
        self.pheromones.emit(
            ptype=PheromoneType.STATE,
            source="蚁群编排器",
            target="全蚁群",
            intensity=0.9,
            content={"stage": stage, **data},
        )

    def run_closed_loop(self) -> Dict[str, Any]:
        """
        执行一次完整闭环：发现→注册→评估→对抗→审计→签章→反馈
        这是蚁群的日常心跳
        """
        print(f"\n{'═'*60}")
        print(f"  🐜 龍魂蚁群联动 · 闭环心跳 · {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'═'*60}")
        results = {"stages": {}, "alerts": [], "actions_taken": []}

        # ── 阶段1：发现（发现蚁出动）──
        print(f"\n[1/7] 🔍 发现蚁 — 扫描脚本...")
        self._emit_state_pheromone("discovery", {"status": "scanning"})
        discovered = self.discoverer.discover()
        total = sum(len(v) for v in discovered.values())
        orphans = len(discovered.get("orphan", []))
        self._log(f"扫描完成：{total}个脚本，{orphans}个孤儿脚本")
        results["stages"]["discovery"] = {"total": total, "orphans": orphans}

        # ── 阶段2：注册（注册蚁归档案）──
        print(f"\n[2/7] 📋 注册蚁 — 归档注册...")
        self._emit_state_pheromone("registration", {"status": "registering"})
        new_count = 0
        for cat, scripts in discovered.items():
            for s in scripts:
                reg = self.registrar.register(s)
                if reg["status"] == "registered":
                    new_count += 1
                    # 发射关联信息素
                    self.pheromones.emit(
                        PheromoneType.LINKAGE, s.name, s.fixed_point,
                        0.7, {"script_id": s.script_id, "path": s.path},
                    )
        self._log(f"注册完成：新增{new_count}个，总计{len(self.registrar.registry)}个")
        results["stages"]["registration"] = {"new": new_count, "total": len(self.registrar.registry)}

        # ── 阶段3：评估（哨兵蚁检测）──
        print(f"\n[3/7] ⚡ 哨兵蚁 — 阈值评估...")
        self._emit_state_pheromone("evaluation", {"status": "evaluating"})
        alerts = self.sentinel.evaluate(self.registrar.registry)
        results["alerts"] = [
            {"id": a.alert_id, "type": a.alert_type, "script": a.script_id,
             "priority": a.priority, "action": a.action}
            for a in alerts
        ]

        stale_ids = self.registrar.get_stale_scripts(90)
        orphan_ids = self.registrar.get_orphans()

        p0_alerts = [a for a in alerts if a.priority == "P0"]
        p1_alerts = [a for a in alerts if a.priority == "P1"]
        self._log(f"阈值评估：P0={len(p0_alerts)} P1={len(p1_alerts)} "
                  f"陈旧={len(stale_ids)} 孤儿={len(orphan_ids)}")

        # 发射告警信息素
        for a in alerts:
            self.pheromones.emit(
                PheromoneType.ALARM, "哨兵蚁", a.script_id,
                intensity=0.8 if a.priority == "P0" else 0.5,
                content={"alert_id": a.alert_id, "type": a.alert_type,
                        "priority": a.priority, "metric": a.metric},
            )

        # ── 阶段4：对抗（红蓝执行蚁）──
        print(f"\n[4/7] ⚔️ 红蓝执行蚁 — 处理告警...")
        self._emit_state_pheromone("confrontation", {"status": "confronting"})
        rb_count = 0
        for alert in alerts[:5]:  # 每次最多处理5条
            script_data = self.registrar.registry.get(alert.script_id, {})
            script_name = script_data.get("name", alert.script_id)

            # 蚁后不动点验证
            valid, reason = self.guardian.validate({
                "action": alert.action,
                "target": script_name,
            })
            if not valid:
                self._log(f"⚠️ 阻断：{script_name} — {reason}")
                continue

            # P0/P1 告警自动触发红蓝对抗
            if alert.priority in ("P0", "P1"):
                self._log(f"触发红蓝对抗：{script_name}（{alert.action}）")
                rb_result = self.executor.trigger_rb(script_name, alert.action)
                results["actions_taken"].append({
                    "action": "rb_confrontation",
                    "script": script_name,
                    "result": rb_result.get("success", False),
                })
                rb_count += 1

        # ── 阶段5：审计（审计蚁记录）──
        print(f"\n[5/7] 📝 审计蚁 — 审计归档...")
        self._emit_state_pheromone("audit", {"status": "auditing"})
        audit_count = 0
        for alert in alerts[:3]:
            script_data = self.registrar.registry.get(alert.script_id, {})
            script_name = script_data.get("name", alert.script_id)
            self._log(f"审计记录：{script_name}")

            # 更新审计历史
            if alert.script_id in self.registrar.registry:
                self.registrar.registry[alert.script_id].setdefault("audit_history", []).append({
                    "date": datetime.now().isoformat(),
                    "alert_type": alert.alert_type,
                    "action": alert.action,
                    "result": "🔍 已审",
                })
            audit_count += 1
        self.registrar._save()

        # ── 阶段6：签章（人格签章）──
        print(f"\n[6/7] 🖊️ 签章蚁 — 人格签章...")
        self._emit_state_pheromone("signing", {"status": "signing"})
        if rb_count > 0:
            # 有红蓝对抗就触发签章
            sign_result = self.executor.trigger_signing("P05", "审计触发", "蚁群联动")
            results["actions_taken"].append({
                "action": "signing",
                "persona": "P05",
                "result": sign_result.get("success", False),
            })
            self._log("P05上帝之眼已签章")
        else:
            self._log("无对抗事件，跳过签章")

        # ── 阶段7：反馈（信息素回灌）──
        print(f"\n[7/7] 🔄 反馈蚁 — 信息素回灌...")
        self._emit_state_pheromone("feedback", {"status": "closing"})

        # 保存蚁群状态
        state = {
            "last_closed_loop": datetime.now().isoformat(),
            "total_scripts": total,
            "registered_scripts": len(self.registrar.registry),
            "orphan_scripts": orphans,
            "alerts_firing": len(alerts),
            "rb_confrontations_today": rb_count,
            "active_pheromones": self.pheromones.get_network_stats()["active_pheromones"],
            "colony_health": self._calculate_health(total, orphans, len(alerts)),
        }
        self.state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2))

        # 发射闭环完成信息素
        self.pheromones.emit(
            PheromoneType.EVENT, "蚁群编排器", "全蚁群",
            intensity=0.95,
            content={"event": "closed_loop_completed", "summary": {
                "scripts": total, "alerts": len(alerts), "rb_triggered": rb_count,
                "health": state["colony_health"],
            }},
            ttl=86400,
        )

        print(f"\n{'═'*60}")
        print(f"  ✅ 闭环完成")
        print(f"  脚本: {total} | 告警: {len(alerts)} | 对抗: {rb_count} | 签章: {rb_count > 0}")
        print(f"  信息素: {state['active_pheromones']}活跃 | 健康度: {state['colony_health']:.1%}")
        print(f"{'═'*60}\n")

        results["health"] = state["colony_health"]
        return results

    def _calculate_health(self, total: int, orphans: int, alerts: int) -> float:
        """
        计算蚁群健康度 v2.0 — 注入五行公式
        
        公式引用：
          H = 五行均衡 × 0.25 + 链路健康 × 0.20 + 对冲指数H × 0.30
            + 生物完备度 × 0.15 + 孤儿惩罚 × 0.10
        
        退路：如果生物度量不可用，回退到旧公式
        """
        try:
            from lh_biometric_health import (
                计算五行强度, 完整链路分析, 计算五行对冲指数, 计算生物完备度
            )
            classified = {}
            for sid, data in self.registrar.registry.items():
                name = data.get("name", "")
                path = data.get("path", "")
                content = " ".join(data.get("functions", []) + data.get("imports", []))
                # 内联五行分类
                wuxing = "土"
                for element, rules in [
                    ("金", ["audit", "sign", "secur", "rule", "threshold", "govern", "regul"]),
                    ("水", ["memory", "data", "stor", "backup", "sync", "dna", "knowledge", "search"]),
                    ("木", ["innov", "grow", "deploy", "build", "optimize", "evolve"]),
                    ("火", ["exec", "confront", "rb_", "persona", "dual", "alert", "culture"]),
                    ("土", ["health", "monitor", "daemon", "system", "config", "util", "bridge", "base"]),
                ]:
                    for kw in rules:
                        if kw in name.lower() or kw in content[:500].lower():
                            wuxing = element
                            break
                    if wuxing != "土":
                        break
                classified[sid] = {**data, "wuxing": wuxing}

            wuxing_intensity = 计算五行强度(classified)
            link_analysis = 完整链路分析(wuxing_intensity["五行得分"])
            hedging = 计算五行对冲指数(wuxing_intensity, link_analysis)
            bio = 计算生物完备度(classified)

            orphan_ratio = orphans / max(total, 1)

            H = round(
                wuxing_intensity["均衡指数"] * 0.25
                + min(link_analysis["链路健康度"] / 100, 1.0) * 0.20
                + hedging["对冲指数H"] * 0.30
                + bio["总完备度"] * 0.15
                + max(0, 1.0 - orphan_ratio) * 0.10,
                4
            )
            return max(0.0, H)
        except Exception:
            # 退路：旧公式
            if total == 0:
                return 1.0
            orphan_penalty = orphans / total * 0.3
            alert_penalty = alerts / max(total, 1) * 0.2
            return max(0.0, 1.0 - orphan_penalty - alert_penalty)

    def print_dashboard(self):
        """打印蚁群仪表盘"""
        registry = self.registrar.registry
        state = {}
        if self.state_file.exists():
            state = json.loads(self.state_file.read_text())
        stats = self.pheromones.get_network_stats()

        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🐜 龍魂 · 蚁群联动仪表盘                                   ║
║   {DNA}                         ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  👑 蚁后不动点                                                ║
║  ────────────────────────────────────────────────            ║
║  {len(QUEEN_FIXED_POINTS)}个不可变精神锚点 · 全部正常守护                          ║
║""")

        # 显示前5个不动点
        for i, (fpid, fp) in enumerate(list(QUEEN_FIXED_POINTS.items())[:5]):
            print(f"║  [{fpid}] {fp['name']:<24s} {'∞ 不可变':>10s}                       ║")

        print(f"""║                                                              ║
║  🐜 蚁群状态                                                  ║
║  ────────────────────────────────────────────────            ║
║  注册脚本: {len(registry):>4}                                ║
║  活跃信息素: {stats['active_pheromones']:>2}                                  ║
║  健康度: {state.get('colony_health', 1.0)*100:>4.0f}%                                        ║
║  上次闭环: {state.get('last_closed_loop', '未运行')[:19]}            ║
║                                                              ║
║  📊 脚本分布                                                  ║""")

        # 按不动点统计
        fp_count: Dict[str, int] = {}
        for sid, data in registry.items():
            fp = data.get("fixed_point", "未知")
            fp_count[fp] = fp_count.get(fp, 0) + 1

        for fp, count in sorted(fp_count.items(), key=lambda x: -x[1])[:8]:
            bar = "█" * min(count, 20)
            print(f"║  {fp:<16s} {bar:<20s} {count:>3}                          ║")

        print(f"""║                                                              ║
║  🔗 关联网络                                                  ║""")

        # 找关联最多的脚本
        top_linked = sorted(registry.items(),
                           key=lambda x: len(x[1].get("upstream", [])) + len(x[1].get("downstream", [])),
                           reverse=True)[:5]
        for sid, data in top_linked:
            name = data.get("name", sid[:12])
            links = len(data.get("upstream", [])) + len(data.get("downstream", []))
            up = len(data.get("upstream", []))
            down = len(data.get("downstream", []))
            print(f"║  {name:<24s} 关联:{links:>3} (↑{up} ↓{down})                      ║")

        print(f"""║                                                              ║
║  ⚠️ 告警                                                      ║""")
        alerts = self.sentinel.evaluate(registry)
        if alerts:
            for a in alerts[:5]:
                script_name = registry.get(a.script_id, {}).get("name", a.script_id[:12])
                print(f"║  [{a.priority}] {script_name:<20s} {a.metric}={a.value:.0f}                        ║")
        else:
            print(f"║  ✅ 无告警·蚁群健康                                          ║")

        print(f"""║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)

    def print_trail(self, script_id: str):
        """追踪指定脚本的信息素轨迹"""
        registry = self.registrar.registry
        if script_id not in registry:
            # 尝试模糊匹配
            for sid, data in registry.items():
                if script_id in data.get("name", ""):
                    script_id = sid
                    break
            else:
                print(f"未找到脚本: {script_id}")
                return

        data = registry[script_id]
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🐜 信息素轨迹追踪                                           ║
║  脚本: {data.get('name', script_id[:12]):<45s} ║
╠══════════════════════════════════════════════════════════════╣
║  不动点: {data.get('fixed_point', '?'):<48s} ║
║  行数: {data.get('lines', 0):>6} | 上游: {len(data.get('upstream', [])):>2} | 下游: {len(data.get('downstream', [])):>2}      ║
╠══════════════════════════════════════════════════════════════╣
""")
        print("║  上游依赖:")
        for dep in data.get("upstream", [])[:10]:
            print(f"║    ↑ {dep}")
        print("║")
        print("║  下游影响:")
        for dep in data.get("downstream", [])[:10]:
            dep_data = registry.get(dep, {})
            print(f"║    ↓ {dep_data.get('name', dep[:12])}")
        print("║")
        print("║  审计历史:")
        for audit in data.get("audit_history", [])[-5:]:
            print(f"║    {audit.get('date', '?')[:10]} → {audit.get('result', '?')}")

        # 追踪信息素
        trail = self.pheromones.sense(source=data.get("name", ""))
        if trail:
            print("║")
            print("║  信息素痕迹:")
            for p in trail[:5]:
                print(f"║    [{p.type.value}] → {p.target} (强度:{p.intensity:.2f})")
        print("╚══════════════════════════════════════════════════════════════╝")


# ═══════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂·蚁群联动编排引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_ant_colony_orchestrator.py --run         # 执行一次完整闭环
  python3 bin/lh_ant_colony_orchestrator.py --discover    # 仅脚本发现
  python3 bin/lh_ant_colony_orchestrator.py --evaluate    # 全量阈值评估
  python3 bin/lh_ant_colony_orchestrator.py --dashboard   # 蚁群仪表盘
  python3 bin/lh_ant_colony_orchestrator.py --trail lh_persona_signing.py  # 追踪轨迹
  python3 bin/lh_ant_colony_orchestrator.py --audit-hook  # 生成审计钩子
        """
    )

    parser.add_argument("--run", action="store_true", help="执行一次完整闭环")
    parser.add_argument("--discover", action="store_true", help="仅执行脚本发现")
    parser.add_argument("--evaluate", action="store_true", help="全量阈值评估")
    parser.add_argument("--dashboard", "-d", action="store_true", help="显示蚁群仪表盘")
    parser.add_argument("--trail", metavar="SCRIPT_ID", help="追踪指定脚本的信息素轨迹")
    parser.add_argument("--audit-hook", action="store_true", help="生成审计钩子代码")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--quiet", "-q", action="store_true", help="安静模式")

    args = parser.parse_args()

    orchestrator = AntColonyOrchestrator(verbose=not args.quiet)

    if args.audit_hook:
        print(AUDIT_HOOK_TEMPLATE)
        return 0

    if args.trail:
        orchestrator.print_trail(args.trail)
        return 0

    if args.dashboard:
        orchestrator.discoverer.discover()  # 先刷新
        orchestrator.print_dashboard()
        return 0

    if args.discover:
        discovered = orchestrator.discoverer.discover()
        if args.json:
            result = {}
            for cat, scripts in discovered.items():
                result[cat] = [{"name": s.name, "path": s.path, "fixed_point": s.fixed_point,
                               "lines": s.lines, "dna": s.dna_markers} for s in scripts]
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for cat, scripts in discovered.items():
                print(f"\n=== {cat} ({len(scripts)}) ===")
                for s in scripts[:5]:
                    print(f"  {s.name:<40s} {s.fixed_point:<12s} {s.lines:>5}行")
                if len(scripts) > 5:
                    print(f"  ... 还有 {len(scripts)-5} 个")
        return 0

    if args.evaluate:
        orchestrator.discoverer.discover()
        # 注册所有
        discovered = orchestrator.discoverer.discover()
        for cat, scripts in discovered.items():
            for s in scripts:
                orchestrator.registrar.register(s)
        alerts = orchestrator.sentinel.evaluate(orchestrator.registrar.registry)
        if args.json:
            print(json.dumps([
                {"id": a.alert_id, "script": a.script_id, "type": a.alert_type,
                 "metric": a.metric, "value": a.value, "threshold": a.threshold,
                 "priority": a.priority, "action": a.action}
                for a in alerts
            ], ensure_ascii=False, indent=2))
        else:
            print(f"\n阈值评估结果：{len(alerts)}条告警")
            for a in alerts:
                script_name = orchestrator.registrar.registry.get(a.script_id, {}).get("name", a.script_id[:12])
                print(f"  [{a.priority}] {script_name:<30s} {a.metric}={a.value:.0f} → {a.action}")
        return 0

    if args.run:
        result = orchestrator.run_closed_loop()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    # 默认：仪表盘
    orchestrator.discoverer.discover()
    orchestrator.print_dashboard()
    return 0


if __name__ == "__main__":
    sys.exit(main())
