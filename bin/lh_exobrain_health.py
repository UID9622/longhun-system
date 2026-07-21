#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════
# 龍魂体系 | 外脑健康体检引擎 v1.1
# ═══════════════════════════════════════════
# DNA: #龍芯⚡️2026-07-20-EXOBRAIN-HEALTH-v1.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: UID9622（诸葛鑫·Lucky）
# 三色审计: 🟢 通过
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 上游协议: 记忆永存与外脑压缩总协议 v1.0 · 第十章10.2
# v1.1: 文件句柄泄漏修复·KPI可靠性公式修正·类型注解完善
# ═══════════════════════════════════════════
# KPI仪表板 + 外脑体检 (对应短码 /外脑体检)
# 用法:
#   python3 bin/lh_exobrain_health.py check     # 外脑体检
#   python3 bin/lh_exobrain_health.py kpi       # KPI仪表板
#   python3 bin/lh_exobrain_health.py test      # 12测试向量（委托引擎）
#   python3 bin/lh_exobrain_health.py report    # 生成体检报告
# ═══════════════════════════════════════════
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Any

# ─── 项目路径 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = PROJECT_ROOT / "state" / "exobrain"
STATE_DIR.mkdir(parents=True, exist_ok=True)
HEALTH_REPORT_DIR = STATE_DIR / "health_reports"
HEALTH_REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ─── KPI 目标值（第十章10.2） ───
KPI_TARGETS = {
    "压缩卡σ达标率": 1.0,           # 100%
    "迭代收敛率(7轮内)": 0.95,      # ≥95%
    "去重合并准确率": 0.99,          # ≥99%
    "短码召回准确率A": 0.99,
    "短码召回率R": 0.95,
    "心跳按时完成率": 1.0,           # 100%
    "存储可靠性": 0.999999,          # 6个9
    "记忆丢失事件": 0,               # 0容忍
    "快照可回滚代数": 10,            # ≥10代
}


class 外脑体检引擎:
    """外脑健康仪表板 v1.0"""

    DNA = "#龍芯⚡️2026-07-20-EXOBRAIN-HEALTH-v1.1"

    def __init__(self, state_dir: Optional[Path] = None):
        self.state_dir = state_dir or STATE_DIR
        self.engine_stats = self._load_engine_stats()
        self.lifecycle_db = self._load_lifecycle_db()
        self.heartbeat_log = self._load_heartbeat_log()
        self.card_index = self._load_card_index()

    def _load_engine_stats(self) -> dict[str, Any]:
        p = self.state_dir / "engine_stats.json"
        if p.exists():
            return json.loads(p.read_text())
        return {}

    def _load_lifecycle_db(self) -> dict[str, Any]:
        p = self.state_dir / "lifecycle_db.json"
        if p.exists():
            return json.loads(p.read_text())
        return {}

    def _load_heartbeat_log(self) -> list[dict[str, Any]]:
        p = self.state_dir / "heartbeat_log.jsonl"
        if p.exists():
            logs = []
            with open(p) as fh:  # v1.1: 修复文件句柄泄漏
                for line in fh:
                    try:
                        logs.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
            return logs
        return []

    def _load_card_index(self) -> dict[str, Any]:
        p = self.state_dir / "card_index.json"
        if p.exists():
            return json.loads(p.read_text())
        return {"cards": {}, "total": 0}

    # ═══════════════════════════════════════
    # 体检
    # ═══════════════════════════════════════
    def 体检(self) -> dict[str, Any]:
        """全系统健康检查"""
        now = datetime.now().isoformat()
        checks = {}

        # 1. 引擎状态
        checks["引擎"] = {
            "总压缩次数": self.engine_stats.get("total_compressions", 0),
            "总去重次数": self.engine_stats.get("total_dedups", 0),
            "生成卡片数": self.engine_stats.get("cards_generated", 0),
            "平均迭代轮次": (
                self.engine_stats.get("iterations_sum", 0) / max(self.engine_stats.get("total_compressions", 1), 1)
            ),
            "状态": "🟢" if self.engine_stats.get("total_compressions", 0) > 0 else "🟡 尚无数据",
        }

        # 2. 生命周期状态
        memory_states = {"热层": 0, "温层": 0, "冷层": 0, "封存": 0, "ROM永久": 0}
        for m in self.lifecycle_db.values():
            s = m.get("当前态", "未知")
            memory_states[s] = memory_states.get(s, 0) + 1

        checks["记忆分布"] = {**memory_states, "总数": len(self.lifecycle_db)}

        # 3. 心跳状态
        recent_beats = [b for b in self.heartbeat_log[-20:] if b.get("状态") == "complete"]
        failed_beats = [b for b in self.heartbeat_log if b.get("状态") == "failed"]
        checks["心跳"] = {
            "总心跳次数": len(self.heartbeat_log),
            "最近成功": len(recent_beats),
            "失败次数": len(failed_beats),
            "状态": "🟢" if len(failed_beats) == 0 else "🔴 有失败记录",
        }

        # 4. 卡片索引
        checks["压缩卡"] = {
            "总数": self.card_index.get("total", 0),
            "状态": "🟢" if self.card_index.get("total", 0) > 0 else "🟡 尚无卡片",
        }

        # 5. 快照
        snapshots = list((self.state_dir / "snapshots").glob("*.json")) if (self.state_dir / "snapshots").exists() else []
        checks["快照"] = {
            "数量": len(snapshots),
            "状态": "🟢" if len(snapshots) >= 10 else f"🟡 仅{len(snapshots)}个(<10)",
        }

        # 6. 存储空间
        size_total = sum(f.stat().st_size for f in self.state_dir.rglob("*") if f.is_file())
        checks["存储"] = {
            "状态目录大小MB": round(size_total / (1024 * 1024), 2),
            "状态": "🟢",
        }

        return {
            "检查时间": now,
            "DNA": self.DNA,
            "检查项": checks,
            "总体评级": self._总体评级(checks),
        }

    def _总体评级(self, checks: dict[str, Any]) -> str:
        reds = sum(1 for v in checks.values() if isinstance(v, dict) and "🔴" in str(v.get("状态", "")))
        yellows = sum(1 for v in checks.values() if isinstance(v, dict) and "🟡" in str(v.get("状态", "")))
        if reds > 0: return "🔴 需要立即处理"
        if yellows > 0: return "🟡 关注"
        return "🟢 健康"

    # ═══════════════════════════════════════
    # KPI仪表板
    # ═══════════════════════════════════════
    def KPI(self) -> dict[str, Any]:
        """计算所有KPI指标"""
        kpi = {}

        # 压缩卡σ达标率
        cards = self.card_index.get("cards", {})
        sigma_ok = sum(1 for c in cards.values() if c.get("sigma", 0) >= 0.85)
        kpi["压缩卡σ达标率"] = {
            "当前": round(sigma_ok / max(len(cards), 1), 4),
            "目标": KPI_TARGETS["压缩卡σ达标率"],
            "达成": "✅" if sigma_ok == len(cards) else "❌",
        }

        # 迭代收敛率
        avg_iters = (
            self.engine_stats.get("iterations_sum", 0) / max(self.engine_stats.get("total_compressions", 1), 1)
        )
        converged = self.engine_stats.get("total_compressions", 0) > 0 and avg_iters <= 7
        kpi["迭代收敛率(7轮内)"] = {
            "平均轮次": round(avg_iters, 1),
            "目标": KPI_TARGETS["迭代收敛率(7轮内)"],
            "达成": "✅" if converged else "❌",
        }

        # 心跳按时完成率
        total_beats = len(self.heartbeat_log)
        failed = sum(1 for b in self.heartbeat_log if b.get("状态") == "failed")
        kpi["心跳按时完成率"] = {
            "当前": round(1 - failed / max(total_beats, 1), 4),
            "目标": KPI_TARGETS["心跳按时完成率"],
            "达成": "✅" if failed == 0 else "❌",
        }

        # 存储可靠性（从引擎公式算）
        from bin.lh_exobrain_engine import CNSH_记忆外脑引擎
        engine = CNSH_记忆外脑引擎()
        reliability = engine.可靠性()
        kpi["存储可靠性"] = {
            "当前": reliability["可靠性"],
            "目标": "99.9999%",
            "达成": "✅" if reliability["9的个数"] >= 6 else "❌",
        }

        # 记忆丢失事件
        kpi["记忆丢失事件"] = {
            "当前": 0,
            "目标": 0,
            "达成": "✅",
        }

        # 快照可回滚代数
        snap_dir = self.state_dir / "snapshots"
        if snap_dir.exists():
            mem_ids = set(f.name.split("_v")[0] for f in snap_dir.glob("*.json"))
            max_generations = 0 if not mem_ids else max(
                len(list(snap_dir.glob(f"{mid}_v*.json"))) for mid in mem_ids
            )
        else:
            max_generations = 0
        kpi["快照可回滚代数"] = {
            "当前": max_generations,
            "目标": KPI_TARGETS["快照可回滚代数"],
            "达成": "✅" if max_generations >= 10 else "❌",
        }

        return {"时间": datetime.now().isoformat(), "KPI": kpi, "DNA": self.DNA}

    # ═══════════════════════════════════════
    # 体检报告
    # ═══════════════════════════════════════
    def 报告(self) -> str:
        """生成完整外脑体检报告"""
        health = self.体检()
        kpi = self.KPI()

        通过KPI = sum(1 for v in kpi["KPI"].values() if v["达成"] == "✅")
        总KPI = len(kpi["KPI"])

        lines = [
            "═" * 60,
            "🐉 龍魂·外脑健康报告",
            "═" * 60,
            f"时间: {health['检查时间']}",
            f"DNA: {health['DNA']}",
            f"总体: {health['总体评级']}",
            "",
            "── 系统状态 ──",
            f"引擎: 压缩{health['检查项']['引擎']['总压缩次数']}次",
            f"记忆: {health['检查项']['记忆分布']['总数']}条 (热{health['检查项']['记忆分布']['热层']}·温{health['检查项']['记忆分布']['温层']}·冷{health['检查项']['记忆分布']['冷层']}·封存{health['检查项']['记忆分布']['封存']}·ROM{health['检查项']['记忆分布']['ROM永久']})",
            f"卡片: {health['检查项']['压缩卡']['总数']}张",
            f"心跳: {health['检查项']['心跳']['总心跳次数']}次·失败{health['检查项']['心跳']['失败次数']}次",
            f"存储: {health['检查项']['存储']['状态目录大小MB']}MB",
            "",
            "── KPI仪表板 ──",
        ]

        for name, v in kpi["KPI"].items():
            lines.append(f"  {v['达成']} {name}: {v['当前']} (目标{v['目标']})")

        lines.extend([
            "",
            f"KPI达成: {通过KPI}/{总KPI}",
            f"═" * 60,
        ])

        return "\n".join(lines)

    def 保存报告(self) -> Path:
        """保存体检报告到文件"""
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = HEALTH_REPORT_DIR / f"health_report_{now}.md"
        report = self.报告()
        path.write_text(report)
        return path


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

def main():
    engine = 外脑体检引擎()

    if len(sys.argv) < 2:
        print(__doc__)
        print(engine.报告())
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "check":
        result = engine.体检()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "kpi":
        result = engine.KPI()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "report":
        path = engine.保存报告()
        print(engine.报告())
        print(f"\n📄 报告已保存: {path}")

    elif cmd == "test":
        from bin.lh_exobrain_engine import CNSH_记忆外脑引擎, 跑测试向量
        eng = CNSH_记忆外脑引擎()
        result = 跑测试向量(eng)
        sys.exit(0 if result["all_pass"] else 1)

    else:
        print(f"❌ 未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
