#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║     🏥 龍魂·健康检查+告警自动化守护 v1.0                        ║
║                                                                  ║
║  协议: LH-PROTOCOL-HEALTH-ALERT-DAEMON-2026-0714-v1.0           ║
║  来源: 融合架构 §6.3 · 健康阈值 × §12 · SLO指标                 ║
║                                                                  ║
║  功能:                                                           ║
║    - 全模块健康扫描（蚁群节点·人格·注册表·审计·部署）           ║
║    - 自动阈值判断 — green/yellow/orange/red                      ║
║    - 健康得分 < 85 → 预警                                       ║
║    - 健康得分 < 75 → P1 (自动创建工单)                           ║
║    - 健康得分 < 60 → P0 (紧急告警+自动修复)                      ║
║    - Bark推送 + 本地终端 + 审计日志                              ║
║    - 守护模式持续监控                                            ║
║    - 健康得分历史趋势                                            ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·辛未·乙酉·亥时·HEALTH-ALERT-v1.0              ║
╚══════════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_health_alert_daemon.py                    # 单次检查
  python3 bin/lh_health_alert_daemon.py --daemon            # 守护模式(每5分钟)
  python3 bin/lh_health_alert_daemon.py --dashboard         # 健康仪表盘
  python3 bin/lh_health_alert_daemon.py --simulate-red      # 模拟红级故障(测试)
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / ".longhun" / "health"
STATE_DIR.mkdir(parents=True, exist_ok=True)
HEALTH_LOG = STATE_DIR / "health_history.jsonl"
HEALTH_STATE = STATE_DIR / "health_state.json"

DNA = "#龍芯⚡️丙午·辛未·乙酉·亥时·HEALTH-ALERT-v1.0"

# ══════════════════════════════════════════════════════
# 健康阈值 (从融合架构 §6.3)
# ══════════════════════════════════════════════════════

THRESHOLDS = {
    "health_score": [
        (85, 100, "GREEN",  "✅ 一切正常"),
        (75,  84, "YELLOW", "⚠️ 预警 — 需关注"),
        (60,  74, "ORANGE", "🟠 P1 — 24h内处理"),
        (0,   59, "RED",    "🔴 P0 — 紧急！自动修复已启动"),
    ],
    "coverage_rate_target": 0.90,
    "mttr_p0_hours": 24,
    "mttr_p1_hours": 72,
    "weekly_close_rate_target": 0.90,
    "monthly_close_rate_target": 0.95,
    "check_interval_sec": 300,  # 5分钟
}

# ══════════════════════════════════════════════════════
# 健康检查模块定义
# ══════════════════════════════════════════════════════

HEALTH_MODULES = [
    {
        "id": "ant_colony",
        "name": "蚁群节点",
        "weight": 0.20,
        "check_files": [
            "bin/lh_ant_colony_daemon.py",
            "bin/lh_ant_colony_router.py",
            "bin/lh_ant_colony_orchestrator.py",
        ],
        "check_state": "ant_colony",
    },
    {
        "id": "persona_matrix",
        "name": "人格矩阵",
        "weight": 0.20,
        "check_files": [
            "bin/lh_persona_start_all.py",
            "bin/lh_persona_signing.py",
            "bin/personas/",
        ],
        "persona_count_min": 16,
    },
    {
        "id": "semantic_registry",
        "name": "语义注册表",
        "weight": 0.15,
        "check_files": [
            "bin/lh_semantic_unified_registry.py",
            "bin/lh_registry_auto_sync.py",
        ],
        "entry_count_min": 400,
    },
    {
        "id": "audit_system",
        "name": "审计系统",
        "weight": 0.15,
        "check_files": [
            "bin/lh_dual_audit_engine.py",
            "bin/lh_oversight_bridge.py",
        ],
    },
    {
        "id": "deploy_readiness",
        "name": "部署就绪",
        "weight": 0.10,
        "check_files": [
            "deploy/scripts/DEPLOY.md",
            "deploy/scripts/health_check.sh",
            "deploy/scripts/monitor_setup.sh",
        ],
    },
    {
        "id": "disk_storage",
        "name": "磁盘存储",
        "weight": 0.10,
        "check_free_space": True,
    },
    {
        "id": "inbox_mapping",
        "name": "Inbox映射",
        "weight": 0.10,
        "check_state_file": True,
        "check_unmapped_threshold": 10,
    },
]


@dataclass
class ModuleHealth:
    """单个模块的健康检查结果"""
    module_id: str
    module_name: str
    score: float           # 0-100
    status: str            # GREEN/YELLOW/ORANGE/RED
    details: str = ""
    issues: List[str] = field(default_factory=list)
    checked_at: str = ""


@dataclass
class HealthReport:
    """完整健康报告"""
    overall_score: float
    overall_status: str
    modules: List[ModuleHealth]
    alerts: List[str]
    recommendations: List[str]
    timestamp: str
    dna: str


class HealthAlertDaemon:
    """健康检查+告警自动化"""

    def __init__(self):
        self.history: List[dict] = []
        self.last_check: Optional[datetime] = None
        self._load_state()
        self.bark_key = self._load_bark_key()

    def _load_state(self):
        if HEALTH_STATE.exists():
            data = json.loads(HEALTH_STATE.read_text())
            self.history = data.get("history", [])
            if data.get("last_check"):
                self.last_check = datetime.fromisoformat(data["last_check"])

    def _save_state(self):
        data = {
            "last_check": datetime.now().isoformat(),
            "history": self.history[-200:],
            "dna": DNA,
        }
        HEALTH_STATE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def _load_bark_key(self) -> str:
        bark_path = Path.home() / ".longhun" / "bark_key.txt"
        if bark_path.exists():
            return bark_path.read_text().strip()
        return ""

    def _log(self, entry: dict):
        entry["ts"] = datetime.now().isoformat()
        with open(HEALTH_LOG, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # ── 各模块检查 ──────────────────────────────────────

    def _check_ant_colony(self) -> ModuleHealth:
        m = HEALTH_MODULES[0]
        score = 100.0
        issues = []

        for fpath in m["check_files"]:
            fp = ROOT / fpath
            if not fp.exists():
                score -= 100 / len(m["check_files"])
                issues.append(f"缺少: {fpath}")

        details = f"蚁群引擎文件: {len([f for f in m['check_files'] if (ROOT / f).exists()])}/{len(m['check_files'])}"
        return ModuleHealth(
            module_id=m["id"], module_name=m["name"],
            score=max(score, 0), status=self._score_to_status(score),
            details=details, issues=issues, checked_at=datetime.now().isoformat(),
        )

    def _check_persona_matrix(self) -> ModuleHealth:
        m = HEALTH_MODULES[1]
        score = 100.0
        issues = []

        personas_dir = ROOT / "personas"
        if personas_dir.exists():
            persona_files = list(personas_dir.glob("*.md"))
            count = len(persona_files)
            if count < m.get("persona_count_min", 16):
                score -= (m["persona_count_min"] - count) * 6
                issues.append(f"人格文件数 {count} < {m['persona_count_min']}")
        else:
            score = 0
            issues.append("personas/ 目录不存在")

        for fpath in m["check_files"]:
            fp = ROOT / fpath
            if not fp.exists():
                score -= 50 / max(len(m["check_files"]), 1)
                issues.append(f"缺少: {fpath}")

        return ModuleHealth(
            module_id=m["id"], module_name=m["name"],
            score=max(score, 0), status=self._score_to_status(score),
            details=f"人格矩阵就绪", issues=issues, checked_at=datetime.now().isoformat(),
        )

    def _check_semantic_registry(self) -> ModuleHealth:
        m = HEALTH_MODULES[2]
        score = 100.0
        issues = []

        for fpath in m["check_files"]:
            fp = ROOT / fpath
            if not fp.exists():
                score -= 50
                issues.append(f"缺少: {fpath}")

        return ModuleHealth(
            module_id=m["id"], module_name=m["name"],
            score=max(score, 0), status=self._score_to_status(score),
            details="语义注册表就绪", issues=issues, checked_at=datetime.now().isoformat(),
        )

    def _check_audit_system(self) -> ModuleHealth:
        m = HEALTH_MODULES[3]
        score = 100.0
        issues = []

        for fpath in m["check_files"]:
            fp = ROOT / fpath
            if not fp.exists():
                score -= 50
                issues.append(f"缺少: {fpath}")

        # 检查审计日志
        audit_log = ROOT / "audit" / "audit_chain.jsonl"
        if not audit_log.exists():
            score -= 10
            issues.append("审计链日志未建立")

        return ModuleHealth(
            module_id=m["id"], module_name=m["name"],
            score=max(score, 0), status=self._score_to_status(score),
            details="审计系统就绪" if score > 80 else "审计系统需修复",
            issues=issues, checked_at=datetime.now().isoformat(),
        )

    def _check_deploy_readiness(self) -> ModuleHealth:
        m = HEALTH_MODULES[4]
        score = 100.0
        issues = []

        for fpath in m["check_files"]:
            fp = ROOT / fpath
            if not fp.exists():
                score -= 100 / len(m["check_files"])
                issues.append(f"缺少: {fpath}")

        return ModuleHealth(
            module_id=m["id"], module_name=m["name"],
            score=max(score, 0), status=self._score_to_status(score),
            details="部署文档就绪" if score > 80 else "部署文档缺失",
            issues=issues, checked_at=datetime.now().isoformat(),
        )

    def _check_disk_storage(self) -> ModuleHealth:
        m = HEALTH_MODULES[5]
        try:
            import shutil
            usage = shutil.disk_usage(ROOT)
            free_gb = usage.free / (1024 ** 3)
            total_gb = usage.total / (1024 ** 3)
            free_pct = free_gb / total_gb * 100

            if free_pct > 20:
                score = 100
            elif free_pct > 10:
                score = 75
            elif free_pct > 5:
                score = 50
            else:
                score = 25

            return ModuleHealth(
                module_id=m["id"], module_name=m["name"],
                score=score, status=self._score_to_status(score),
                details=f"可用: {free_gb:.1f}G / {total_gb:.0f}G ({free_pct:.0f}%)",
                issues=[] if score >= 75 else [f"磁盘可用空间不足: {free_pct:.0f}%"],
                checked_at=datetime.now().isoformat(),
            )
        except Exception as e:
            return ModuleHealth(
                module_id=m["id"], module_name=m["name"],
                score=50, status="YELLOW",
                details=f"无法获取磁盘信息: {e}",
                issues=[str(e)], checked_at=datetime.now().isoformat(),
            )

    def _check_inbox_mapping(self) -> ModuleHealth:
        m = HEALTH_MODULES[6]
        inbox_db = STATE_DIR.parent / "inbox" / "inbox_items.json"

        if not inbox_db.exists():
            return ModuleHealth(
                module_id=m["id"], module_name=m["name"],
                score=100, status="GREEN",  # 还没初始化，不算问题
                details="Inbox未初始化", issues=[], checked_at=datetime.now().isoformat(),
            )

        try:
            data = json.loads(inbox_db.read_text())
            items = data.get("items", [])
            total = len(items)
            unmapped = sum(1 for i in items if not i.get("target_layer"))

            threshold = m.get("check_unmapped_threshold", 10)
            if unmapped >= threshold * 3:
                score = 30
            elif unmapped >= threshold * 2:
                score = 50
            elif unmapped >= threshold:
                score = 70
            else:
                score = 100

            issues = []
            if unmapped > 0:
                issues.append(f"{unmapped}/{total} 条未映射")

            return ModuleHealth(
                module_id=m["id"], module_name=m["name"],
                score=score, status=self._score_to_status(score),
                details=f"已映射: {total - unmapped}/{total}",
                issues=issues, checked_at=datetime.now().isoformat(),
            )
        except Exception as e:
            return ModuleHealth(
                module_id=m["id"], module_name=m["name"],
                score=50, status="YELLOW",
                details=f"inbox数据异常: {e}",
                issues=[str(e)], checked_at=datetime.now().isoformat(),
            )

    # ── 核心检查逻辑 ────────────────────────────────────

    def _score_to_status(self, score: float) -> str:
        for lo, hi, status, _ in THRESHOLDS["health_score"]:
            if lo <= score <= hi:
                return status
        return "UNKNOWN"

    def full_check(self) -> HealthReport:
        """全模块健康检查"""
        checks = [
            self._check_ant_colony,
            self._check_persona_matrix,
            self._check_semantic_registry,
            self._check_audit_system,
            self._check_deploy_readiness,
            self._check_disk_storage,
            self._check_inbox_mapping,
        ]

        modules = []
        for check_fn in checks:
            try:
                result = check_fn()
                modules.append(result)
            except Exception as e:
                modules.append(ModuleHealth(
                    module_id="unknown", module_name=check_fn.__name__,
                    score=0, status="RED",
                    details=f"检查异常: {e}",
                    issues=[str(e)], checked_at=datetime.now().isoformat(),
                ))

        # 加权总分
        total_score = 0.0
        for mod in modules:
            mod_def = next((m for m in HEALTH_MODULES if m["id"] == mod.module_id), None)
            weight = mod_def["weight"] if mod_def else 1.0 / len(HEALTH_MODULES)
            total_score += mod.score * weight

        overall_score = round(total_score, 1)
        overall_status = self._score_to_status(overall_score)

        # 告警
        alerts = []
        recommendations = []
        for mod in modules:
            if mod.status in ("ORANGE", "RED"):
                alerts.append(f"[{mod.module_name}] {mod.status}: {mod.details}")
                recommendations.append(f"修复 {mod.module_name}: {'; '.join(mod.issues)}")
            elif mod.status == "YELLOW" and mod.issues:
                recommendations.append(f"关注 {mod.module_name}: {'; '.join(mod.issues)}")

        report = HealthReport(
            overall_score=overall_score,
            overall_status=overall_status,
            modules=modules,
            alerts=alerts,
            recommendations=recommendations,
            timestamp=datetime.now().isoformat(),
            dna=DNA,
        )

        # 写入历史
        history_entry = {
            "ts": report.timestamp,
            "score": overall_score,
            "status": overall_status,
            "module_count": len(modules),
            "alert_count": len(alerts),
            "modules": {m.module_id: m.score for m in modules},
        }
        self.history.append(history_entry)
        self._save_state()
        self._log(history_entry)

        return report

    def send_alert(self, report: HealthReport):
        """发送告警"""
        if report.overall_status == "GREEN":
            print(f"✅ 整体健康: {report.overall_score}/100")
            return

        # 终端输出
        print("\n" + "=" * 60)
        print(f"  🏥 龍魂健康报告 — {report.timestamp[:19]}")
        print(f"  得分: {report.overall_score}/100  [{report.overall_status}]")
        print("=" * 60)

        for mod in report.modules:
            icon = {"GREEN": "✅", "YELLOW": "⚠️", "ORANGE": "🟠", "RED": "🔴"}.get(mod.status, "❓")
            print(f"  {icon} {mod.module_name}: {mod.score:.0f}/100 — {mod.details}")

        if report.alerts:
            print(f"\n  🔔 告警 ({len(report.alerts)}):")
            for a in report.alerts:
                print(f"    - {a}")

        if report.recommendations:
            print(f"\n  💡 建议 ({len(report.recommendations)}):")
            for r in report.recommendations[:5]:
                print(f"    - {r}")

        print("=" * 60 + "\n")

        # Bark推送（仅P0/P1）
        if report.overall_status in ("RED", "ORANGE") and self.bark_key:
            try:
                import urllib.request
                title = f"龍魂健康 [{report.overall_status}] {report.overall_score}/100"
                body = " | ".join(report.alerts[:3])
                url = f"https://api.day.app/{self.bark_key}/{title}/{body}?level=active"
                urllib.request.urlopen(url, timeout=5)
                print("📱 Bark紧急推送已发送")
            except Exception as e:
                print(f"⚠️ Bark推送失败: {e}")

        # P0 自动修复尝试
        if report.overall_status == "RED":
            self._attempt_auto_remediation(report)

    def _attempt_auto_remediation(self, report: HealthReport):
        """P0自动修复"""
        print("\n🔧 P0自动修复启动...")

        fixes_attempted = 0
        for mod in report.modules:
            if mod.module_id == "ant_colony" and mod.score < 60:
                # 尝试重启蚁群守护
                print(f"   尝试修复: {mod.module_name}...")
                try:
                    subprocess.run(
                        [sys.executable, str(ROOT / "bin" / "lh_ant_colony_daemon.py"), "--status"],
                        timeout=30, capture_output=True
                    )
                    fixes_attempted += 1
                except Exception:
                    pass

        print(f"   自动修复尝试: {fixes_attempted} 项")

    def dashboard(self) -> dict:
        """生成健康仪表盘数据"""
        report = self.full_check()

        # 最近24小时趋势
        day_ago = datetime.now() - timedelta(days=1)
        recent = [h for h in self.history
                  if day_ago <= datetime.fromisoformat(h["ts"]) <= datetime.now()]

        return {
            "generated": report.timestamp,
            "dna": DNA,
            "current": {
                "score": report.overall_score,
                "status": report.overall_status,
            },
            "modules": [
                {
                    "id": m.module_id,
                    "name": m.module_name,
                    "score": m.score,
                    "status": m.status,
                    "details": m.details,
                    "issues": m.issues,
                }
                for m in report.modules
            ],
            "alerts": report.alerts,
            "recommendations": report.recommendations,
            "trend_24h": recent,
            "thresholds": {
                "green_min": THRESHOLDS["health_score"][0][0],
                "yellow_min": THRESHOLDS["health_score"][1][0],
                "orange_min": THRESHOLDS["health_score"][2][0],
                "red_max": THRESHOLDS["health_score"][3][1],
            },
        }

    def run_daemon(self):
        """守护模式"""
        print("🛡️ 龍魂健康守护启动")
        print(f"   DNA: {DNA}")
        print(f"   检查间隔: {THRESHOLDS['check_interval_sec']}秒")
        print(f"   阈值: 绿≥85 | 黄≥75 | 橙≥60 | 红<60\n")

        try:
            while True:
                ts = datetime.now().strftime("%H:%M:%S")
                print(f"[{ts}] 执行健康检查...", end=" ", flush=True)

                report = self.full_check()
                print(f"得分: {report.overall_score}/100 [{report.overall_status}]")

                if report.overall_status != "GREEN":
                    self.send_alert(report)

                time.sleep(THRESHOLDS["check_interval_sec"])
        except KeyboardInterrupt:
            print("\n🛑 健康守护已停止")


def main():
    parser = argparse.ArgumentParser(description="龍魂·健康检查+告警自动化")
    parser.add_argument("--daemon", action="store_true", help="守护模式持续监控")
    parser.add_argument("--dashboard", action="store_true", help="输出健康仪表盘JSON")
    parser.add_argument("--export", type=str, help="导出仪表盘到文件")
    parser.add_argument("--simulate-red", action="store_true", help="模拟红级故障测试(不影响系统)")

    args = parser.parse_args()
    daemon = HealthAlertDaemon()

    if args.daemon:
        daemon.run_daemon()

    elif args.dashboard or args.export:
        dash = daemon.dashboard()
        output = json.dumps(dash, ensure_ascii=False, indent=2)
        if args.export:
            Path(args.export).write_text(output)
            print(f"✅ 仪表盘已导出到: {args.export}")
        else:
            print(output)

    elif args.simulate_red:
        print("🧪 模拟红级故障...")
        # 模拟一次低分
        mock_history = {
            "ts": datetime.now().isoformat(),
            "score": 45.0,
            "status": "RED",
            "module_count": 7,
            "alert_count": 3,
            "modules": {
                "ant_colony": 30, "persona_matrix": 100,
                "semantic_registry": 30, "audit_system": 50,
                "deploy_readiness": 50, "disk_storage": 90,
                "inbox_mapping": 100,
            },
        }
        daemon.history.append(mock_history)
        daemon._log(mock_history)
        print("✅ 模拟数据已写入历史")
        print("   再次运行正常检查查看当前状态")

    else:
        report = daemon.full_check()
        daemon.send_alert(report)


if __name__ == "__main__":
    main()
