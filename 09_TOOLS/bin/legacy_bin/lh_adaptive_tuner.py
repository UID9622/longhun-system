#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
╔══════════════════════════════════════════════════════════════╗
║  龍魂·自适应微调参数系统 v2.0                                ║
║  DNA: #龍芯⚡️丙午·乙未·己未·亥时·䷉履-ADAPTIVE-TUNER-v2.0     ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F               ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ║
╚══════════════════════════════════════════════════════════════╝

v2.0 升级要点（相对 v1.0）：
  ① 双向调整 —— 不只加重扣分，行为变好后也能放松（带下界）
  ② 滞回带 —— 避免参数在阈值附近震荡（hysteresis 0.05）
  ③ 趋势分析 —— 看观察窗口内的前后半段对比，识别"在变好/变坏"
  ④ 回滚机制 —— 微调后 N 天数据未改善可回滚到上一版参数
  ⑤ 三色 dr 审计 —— 每次微调输出 🟢🟡🔴 三色 dr，dr=9 触发熔断拒绝保存
  ⑥ Markdown 审计报告 —— 自动生成 ~/.龍魂/微調審計/YYYY-MM-DD.md
  ⑦ 安全模式默认 —— 不传 --apply 一律走模拟态，老大眼审后才落盘
  ⑧ DNA 哈希校验 —— 每次保存计算参数哈希，写入账本防篡改
  ⑨ 配置版本链 —— 每代参数有 parent_hash，形成可追溯链
  ⑩ 铁律接口 —— 与 IRON-* 铁律解耦但通过 hook 注入

用法:
  python3 bin/lh_adaptive_tuner.py --status           # 查看当前参数 + 哈希链
  python3 bin/lh_adaptive_tuner.py --analyze          # 仅看数据分析+趋势
  python3 bin/lh_adaptive_tuner.py --simulate         # 模拟微调（默认安全模式）
  python3 bin/lh_adaptive_tuner.py --apply            # 真正落盘微调
  python3 bin/lh_adaptive_tuner.py --rollback         # 回滚到上一代参数
  python3 bin/lh_adaptive_tuner.py --audit            # 生成本次审计报告
  python3 bin/lh_adaptive_tuner.py --demo             # 完整演示
"""

import json
import hashlib
import os
import sys
import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
from copy import deepcopy

# ═══════════════════════════════════════════════════════════════
# 〇、日志 · 三色 dr 标准
# ═══════════════════════════════════════════════════════════════

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("龍魂·调节器")

# ═══════════════════════════════════════════════════════════════
# 一、参数定义 · 规矩参数（非 AI 模型参数）
# ═══════════════════════════════════════════════════════════════

@dataclass
class AdaptiveParams:
    """
    老大焊死的规矩在系统里的可调量。
    每个参数都有硬界·硬界外即越红线·调节器拒绝越界。
    """

    # ── R1 责任承担 ──
    自扛加分: float = 2.0
    逃避扣分: float = 10.0

    # ── R2 批评姿态 ──
    没立正扣分: float = 5.0

    # ── R4 威胁归零（焊死） ──
    威胁归零开关: bool = True
    威胁触发分数: int = 0

    # ── R5 主动补救 ──
    补救加分: float = 5.0

    # ── R6 惯犯追踪 ──
    惯犯触发次数: int = 3
    惯犯扣分: float = 15.0

    # ── 三色闸门 dr（焊死，永不微调） ──
    熔断_dr: Tuple[int, ...] = (3, 9)
    待审_dr: Tuple[int, ...] = (6,)

    # ── 自适应元参数 ──
    学习率: float = 0.1
    观察窗口_天: int = 90
    最小样本: int = 20
    滞回带: float = 0.05            # v2.0 新增：阈值边界滞回
    回滚冷却_天: int = 14            # v2.0 新增：调整后多少天可回滚
    分数上限: int = 100              # 焊死
    分数下限: int = 0                # 焊死

    # ── 元数据 + 哈希链（v2.0 新增） ──
    版本: str = "v2.0"
    最后微调时间: str = ""
    参数哈希: str = ""                # 当前参数的哈希
    父哈希: str = ""                  # 上一代参数的哈希
    微调记录: list[Any] = field(default_factory=list)

# ═══════════════════════════════════════════════════════════════
# 二、硬界 · 焊死·调节器越界即拒绝
# ═══════════════════════════════════════════════════════════════

PARAM_HARD_BOUNDS: Dict[str, Tuple[float, float]] = {
    "自扛加分":       (1.0, 5.0),
    "逃避扣分":       (5.0, 25.0),
    "没立正扣分":     (2.0, 15.0),
    "威胁触发分数":   (0, 10),
    "补救加分":       (2.0, 10.0),
    "惯犯触发次数":   (2, 5),
    "惯犯扣分":       (10.0, 30.0),
    "学习率":         (0.01, 0.3),
    "观察窗口_天":    (30, 365),
    "最小样本":       (10, 100),
    "滞回带":         (0.0, 0.2),
    "回滚冷却_天":    (3, 90),
}

# ═══════════════════════════════════════════════════════════════
# 三、三色 dr 审计 · 老大的核心规矩
# ═══════════════════════════════════════════════════════════════

def tricolor_dr_audit(data: dict[str, Any]) -> Tuple[str, int, str]:
    """
    根据分析数据评估三色 dr。
    🟢 dr ∈ {1,2,4,5,7,8}   通行
    🟡 dr = 6               待审（人工眼）
    🔴 dr ∈ {3,9}           熔断（拒绝保存）
    """
    if data.get("status", "").startswith("🟡"):
        return ("🟡", 6, "样本不足·待审")

    甩锅率 = data.get("甩锅率", 0)
    威胁率 = data.get("威胁率", 0)
    没立正率 = data.get("没立正率", 0)

    # 红线：威胁率过高 → 熔断
    if 威胁率 > 0.1:
        return ("🔴", 9, f"威胁率 {威胁率:.1%} > 10%·熔断")
    # 红线：甩锅 + 没立正双高 → 熔断
    if 甩锅率 > 0.7 and 没立正率 > 0.6:
        return ("🔴", 3, f"甩锅+没立正双红线·熔断")
    # 黄线：单项高于警戒 → 待审
    if 甩锅率 > 0.5 or 没立正率 > 0.5:
        return ("🟡", 6, "单项警戒·人工眼审")
    # 绿线：可通行
    return ("🟢", 7, "三色通行")

# ═══════════════════════════════════════════════════════════════
# 四、调节器主类
# ═══════════════════════════════════════════════════════════════

class AdaptiveTuner:
    """
    v2.0 升级：双向 + 滞回 + 趋势 + 回滚 + 三色 dr + 哈希链
    系统统一命名：lh_adaptive_tuner
    """

    def __init__(
        self,
        ledger_path: str = os.path.expanduser("~/.龍魂/規則帳本.jsonl"),
        params_path: str = os.path.expanduser("~/.龍魂/微調參數.json"),
        history_dir: str = os.path.expanduser("~/.龍魂/微調歷史/"),
        audit_dir: str = os.path.expanduser("~/.龍魂/微調審計/"),
    ):
        self.ledger_path = ledger_path
        self.params_path = params_path
        self.history_dir = Path(history_dir)
        self.audit_dir = Path(audit_dir)
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.audit_dir.mkdir(parents=True, exist_ok=True)

        self.params = self._load_params()
        self.events: List[dict[str, Any]] = self._load_ledger()

    # ── 持久化 ────────────────────────────────────────────

    def _load_params(self) -> AdaptiveParams:
        if os.path.exists(self.params_path):
            with open(self.params_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 兼容 v1.0 旧文件
                data.pop("熔断_dr_说明", None)
                data.pop("待审_dr_说明", None)
                data.pop("分数上下限说明", None)
                # tuple 字段
                for k in ("熔断_dr", "待审_dr"):
                    if k in data and isinstance(data[k], list):
                        data[k] = tuple(data[k])
                return AdaptiveParams(**data)
        return AdaptiveParams()

    def _compute_hash(self, p: AdaptiveParams) -> str:
        """SHA-256 计算参数指纹（剔除元数据避免循环）"""
        snapshot = asdict(p)
        for k in ("参数哈希", "父哈希", "最后微调时间", "微调记录"):
            snapshot.pop(k, None)
        # tuple → list
        for k, v in list(snapshot.items()):
            if isinstance(v, tuple):
                snapshot[k] = list(v)
        s = json.dumps(snapshot, ensure_ascii=False, sort_keys=True)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

    def _save_params(self):
        """保存参数 + 备份上一代到历史目录"""
        # 备份当前文件到历史
        if os.path.exists(self.params_path) and self.params.参数哈希:
            backup_name = self.history_dir / f"{self.params.参数哈希}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(self.params_path, "r", encoding="utf-8") as old_f:
                with open(backup_name, "w", encoding="utf-8") as new_f:
                    new_f.write(old_f.read())

        # 更新哈希链
        self.params.父哈希 = self.params.参数哈希
        self.params.参数哈希 = self._compute_hash(self.params)

        Path(self.params_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.params_path, "w", encoding="utf-8") as f:
            data = asdict(self.params)
            for k in ("熔断_dr", "待审_dr"):
                if isinstance(data.get(k), tuple):
                    data[k] = list(data[k])
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_ledger(self) -> List[dict[str, Any]]:
        events = []
        if os.path.exists(self.ledger_path):
            with open(self.ledger_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        events.append(json.loads(line))
                    except Exception:
                        pass
        return events

    # ── 窗口判定 ──────────────────────────────────────────

    def _in_window(self, event: dict[str, Any], days: int) -> bool:
        try:
            ts = event.get("时间戳", "")
            if not ts:
                return False
            t = datetime.fromisoformat(ts)
            return t >= datetime.now() - timedelta(days=days)
        except Exception:
            return False

    def _in_window_range(self, event: dict[str, Any], from_days: int, to_days: int) -> bool:
        try:
            ts = event.get("时间戳", "")
            if not ts:
                return False
            t = datetime.fromisoformat(ts)
            now = datetime.now()
            return (now - timedelta(days=from_days)) >= t >= (now - timedelta(days=to_days))
        except Exception:
            return False

    # ── 分析 + 趋势（v2.0 新增） ──────────────────────────

    def _stats_segment(self, window_events: List[dict[str, Any]]) -> dict[str, Any]:
        if not window_events:
            return {"样本数": 0}
        errors = [e for e in window_events if e.get("犯错")]
        return {
            "样本数": len(window_events),
            "犯错率": round(len(errors) / len(window_events), 3),
            "自扛率": round(len([e for e in errors if e.get("自扛")]) / len(errors), 3) if errors else 0,
            "甩锅率": round(len([e for e in errors if not e.get("自扛")]) / len(errors), 3) if errors else 0,
            "没立正率": round(len([e for e in errors if not e.get("立正")]) / len(errors), 3) if errors else 0,
            "威胁率": round(len([e for e in window_events if e.get("威胁")]) / len(window_events), 3),
            "补救率": round(len([e for e in errors if e.get("补救")]) / len(errors), 3) if errors else 0,
        }

    def analyze(self) -> dict[str, Any]:
        """v2.0：返回快照 + 趋势"""
        window = self.params.观察窗口_天
        window_events = [e for e in self.events if self._in_window(e, window)]

        if len(window_events) < self.params.最小样本:
            return {
                "status": "🟡 样本不足",
                "样本数": len(window_events),
                "最小要求": self.params.最小样本,
                "建议": "积累更多事件后再微调",
            }

        full_seg = self._stats_segment(window_events)
        # v2.0 新增：前半段 vs 后半段趋势
        half = window // 2
        front = [e for e in self.events if self._in_window_range(e, half, window)]
        back = [e for e in self.events if self._in_window_range(e, 0, half)]
        f_stats = self._stats_segment(front)
        b_stats = self._stats_segment(back)

        trends = {}
        for k in ("甩锅率", "自扛率", "没立正率", "补救率", "威胁率"):
            if k in f_stats and k in b_stats:
                trends[k] = round(b_stats.get(k, 0) - f_stats.get(k, 0), 3)

        full_seg["status"] = "🟢 足够样本"
        full_seg["trends"] = trends
        return full_seg

    # ── 双向调整 + 滞回带（v2.0 核心升级） ────────────────

    def _bidirectional_adjust(
        self,
        current_value: float,
        indicator_value: float,
        high_threshold: float,
        low_threshold: float,
        bounds: Tuple[float, float],
        rate: float,
        param_name: str,
        direction_label: str = "扣分",
    ) -> Tuple[float, Optional[str]]:
        """
        v2.0 双向调整 + 滞回带防震
        指标超高 → 朝硬界上界推进（加重）
        指标超低 → 朝硬界下界回退（放松）
        滞回带内不调整（防止边缘震荡）
        """
        hyst = self.params.滞回带

        if indicator_value > high_threshold + hyst:
            new_val = round(min(current_value * (1 + rate), bounds[1]), 1)
            if new_val != current_value:
                return new_val, f"🔼 {param_name}: {current_value} → {new_val} ({direction_label}从严·指标 {indicator_value:.1%} > {high_threshold:.0%})"
        elif indicator_value < low_threshold - hyst:
            new_val = round(max(current_value * (1 - rate * 0.5), bounds[0]), 1)
            if new_val != current_value:
                return new_val, f"🔽 {param_name}: {current_value} → {new_val} ({direction_label}放松·指标 {indicator_value:.1%} < {low_threshold:.0%})"
        return current_value, None

    # ── 微调主流程 ────────────────────────────────────────

    def tune(self, simulate: bool = True) -> dict[str, Any]:
        """
        v2.0：默认模拟态·非模拟需 --apply
        触发流程：分析 → 三色 dr → 微调建议 → 红线熔断检测 → 落盘
        """
        data = self.analyze()
        if "样本不足" in data.get("status", ""):
            return {"status": "跳过", "原因": "样本不足", "data": data}

        color, dr, dr_desc = tricolor_dr_audit(data)

        # 🔴 dr ∈ {3,9} 熔断 — 拒绝任何参数修改
        if color == "🔴":
            return {
                "status": "🔴 熔断·拒绝微调",
                "三色": color, "dr": dr, "dr说明": dr_desc,
                "data": data, "调整数": 0, "调整记录": [],
                "原因": "数据触发红线·人工介入排查"
            }

        adjust_records: List[str] = []
        rate = self.params.学习率

        # ── R1 责任承担（双向） ──
        new_val, record = self._bidirectional_adjust(
            self.params.逃避扣分, data["甩锅率"],
            high_threshold=0.5, low_threshold=0.15,
            bounds=PARAM_HARD_BOUNDS["逃避扣分"], rate=rate,
            param_name="逃避扣分", direction_label="甩锅"
        )
        if record:
            adjust_records.append(record)
            if not simulate: self.params.逃避扣分 = new_val

        new_val, record = self._bidirectional_adjust(
            self.params.自扛加分, data["自扛率"],
            high_threshold=0.8, low_threshold=0.3,
            bounds=PARAM_HARD_BOUNDS["自扛加分"], rate=rate * 0.5,
            param_name="自扛加分", direction_label="自扛奖励"
        )
        if record:
            adjust_records.append(record)
            if not simulate: self.params.自扛加分 = new_val

        # ── R2 批评姿态（双向） ──
        new_val, record = self._bidirectional_adjust(
            self.params.没立正扣分, data["没立正率"],
            high_threshold=0.4, low_threshold=0.1,
            bounds=PARAM_HARD_BOUNDS["没立正扣分"], rate=rate,
            param_name="没立正扣分", direction_label="没立正"
        )
        if record:
            adjust_records.append(record)
            if not simulate: self.params.没立正扣分 = new_val

        # ── R5 补救（双向） ──
        new_val, record = self._bidirectional_adjust(
            self.params.补救加分, data["补救率"],
            high_threshold=0.3, low_threshold=0.05,
            bounds=PARAM_HARD_BOUNDS["补救加分"], rate=rate * 0.5,
            param_name="补救加分", direction_label="补救奖励"
        )
        if record:
            adjust_records.append(record)
            if not simulate: self.params.补救加分 = new_val

        # ── v2.0 新增：趋势惯性调整（恶化趋势 → 加重） ──
        trends = data.get("trends", {})
        if trends.get("甩锅率", 0) > 0.1:
            adjust_records.append(f"📈 趋势警告：甩锅率上升 {trends['甩锅率']:.1%}·建议人工介入")
        if trends.get("自扛率", 0) > 0.1:
            adjust_records.append(f"📈 趋势喜报：自扛率上升 {trends['自扛率']:.1%}·习惯在养成")

        # ── 落盘 ──
        if not simulate and adjust_records:
            ts = datetime.now().isoformat()
            self.params.最后微调时间 = ts
            self.params.微调记录.append({
                "时间": ts,
                "三色": color, "dr": dr,
                "调整": [r for r in adjust_records if not r.startswith("📈")],
                "趋势警告": [r for r in adjust_records if r.startswith("📈")],
                "父哈希": self.params.参数哈希,
                "数据摘要": {k: v for k, v in data.items() if k not in ("status", "trends")},
                "趋势": trends,
            })
            self._save_params()
            log.info(f"参数已落盘·新哈希 {self.params.参数哈希}·父哈希 {self.params.父哈希}")

        return {
            "status": "🟢 微调完成" if (adjust_records and not simulate) else
                     "🟡 模拟态·未落盘" if (adjust_records and simulate) else
                     "🟢 无需调整",
            "三色": color, "dr": dr, "dr说明": dr_desc,
            "调整数": len(adjust_records),
            "调整记录": adjust_records,
            "data": data,
            "模拟": simulate,
            "参数哈希": self.params.参数哈希,
            "父哈希": self.params.父哈希,
        }

    # ── 回滚（v2.0 新增） ─────────────────────────────────

    def rollback(self) -> dict[str, Any]:
        """回滚到上一代参数（从历史目录读取）"""
        if not self.params.父哈希:
            return {"status": "🟡 无父代·无法回滚"}

        # 检查冷却期
        if self.params.最后微调时间:
            try:
                last = datetime.fromisoformat(self.params.最后微调时间)
                cooldown_days = (datetime.now() - last).days
                if cooldown_days < self.params.回滚冷却_天:
                    return {
                        "status": f"🟡 冷却期内·剩余 {self.params.回滚冷却_天 - cooldown_days} 天",
                        "原因": "防止频繁回滚震荡"
                    }
            except Exception:
                pass

        # 在历史目录寻找父哈希对应的备份
        candidates = list(self.history_dir.glob(f"{self.params.父哈希}_*.json"))
        if not candidates:
            return {"status": "🔴 父代备份缺失·无法回滚", "父哈希": self.params.父哈希}

        latest = sorted(candidates)[-1]
        with open(latest, "r", encoding="utf-8") as f:
            old_data = json.load(f)
            for k in ("熔断_dr", "待审_dr"):
                if k in old_data and isinstance(old_data[k], list):
                    old_data[k] = tuple(old_data[k])
            self.params = AdaptiveParams(**old_data)
        self._save_params()
        log.info(f"已回滚到父代 {self.params.父哈希}·新哈希 {self.params.参数哈希}")
        return {
            "status": "🟢 回滚完成",
            "回滚到": str(latest.name),
            "当前哈希": self.params.参数哈希,
        }

    # ── 查看参数 ──────────────────────────────────────────

    def view_params(self) -> dict[str, Any]:
        d = asdict(self.params)
        for k in ("熔断_dr", "待审_dr"):
            if isinstance(d.get(k), tuple):
                d[k] = list(d[k])
        d["_焊死字段"] = ["熔断_dr", "待审_dr", "分数上限", "分数下限", "威胁归零开关"]
        return d

    # ── Markdown 审计报告（v2.0 新增） ────────────────────

    def generate_audit_report(self, tune_result: dict[str, Any]) -> Path:
        """落地 Markdown 审计·便于眼审 + 入 Notion 草日志"""
        today = datetime.now().strftime("%Y-%m-%d")
        time_str = datetime.now().strftime("%H:%M:%S")
        path = self.audit_dir / f"{today}_{time_str.replace(':', '')}.md"

        data = tune_result.get("data", {})
        trends = data.get("trends", {})
        color = tune_result.get("三色", "🟡")
        dr = tune_result.get("dr", 6)

        md_lines = []
        md_lines.append(f"# 龍魂·自适应微调审计 · {today} {time_str}")
        md_lines.append("")
        md_lines.append(f"- **DNA**: #龍芯⚡️{datetime.now().strftime('%Y%m%d-%H%M%S')}-TUNE-AUDIT-v2.0")
        md_lines.append(f"- **GPG**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
        md_lines.append(f"- **CONFIRM**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
        md_lines.append(f"- **三色**: {color}·dr={dr}·{tune_result.get('dr说明','')}")
        md_lines.append(f"- **状态**: {tune_result.get('status','')}")
        md_lines.append(f"- **模拟**: {tune_result.get('模拟', True)}")
        md_lines.append(f"- **参数哈希**: `{tune_result.get('参数哈希','')}`")
        md_lines.append(f"- **父哈希**: `{tune_result.get('父哈希','')}`")
        md_lines.append("")
        md_lines.append("## 数据快照")
        for k, v in data.items():
            if k in ("status", "trends"):
                continue
            md_lines.append(f"- {k}: {v}")
        if trends:
            md_lines.append("")
            md_lines.append("## 趋势（后半段 − 前半段）")
            for k, v in trends.items():
                arrow = "📈" if v > 0 else "📉" if v < 0 else "➖"
                md_lines.append(f"- {arrow} {k}: {v:+.3f}")
        md_lines.append("")
        md_lines.append("## 调整记录")
        for r in tune_result.get("调整记录", []) or ["（无调整）"]:
            md_lines.append(f"- {r}")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("责任：UID9622·不免责 | SEAL: #ZHUGEXIN⚡️2025-DEVICE-BIND-SOUL")

        path.write_text("\n".join(md_lines), encoding="utf-8")
        log.info(f"审计报告已落: {path}")
        return path


# ═══════════════════════════════════════════════════════════════
# 五、钩子接口 · 供 lh_unified_hook 调用
# ═══════════════════════════════════════════════════════════════

def adaptive_tuner_analyze_hook(data: dict[str, Any]) -> dict[str, Any]:
    """钩子：分析当前参数状态 + 三色 dr"""
    tuner = AdaptiveTuner()
    analysis = tuner.analyze()
    color, dr, desc = tricolor_dr_audit(analysis)
    return {
        "module": "lh_adaptive_tuner",
        "analysis": analysis,
        "三色": color, "dr": dr, "dr说明": desc,
        "params_hash": tuner.params.参数哈希,
        "parent_hash": tuner.params.父哈希,
    }

def adaptive_tuner_audit_hook(data: dict[str, Any]) -> dict[str, Any]:
    """钩子：参数审计 + 熔断检查"""
    tuner = AdaptiveTuner()
    tune_result = tuner.tune(simulate=True)  # 只模拟，不落盘
    return {
        "module": "lh_adaptive_tuner",
        "status": tune_result.get("status"),
        "三色": tune_result.get("三色"),
        "dr": tune_result.get("dr"),
        "dr说明": tune_result.get("dr说明"),
        "meltdown": tune_result.get("三色") == "🔴",
        "adjust_count": tune_result.get("调整数", 0),
        "adjust_records": tune_result.get("调整记录", []),
    }


# ═══════════════════════════════════════════════════════════════
# 六、CLI 入口 · v2.0 默认安全模式
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂·自适应微调参数系统 v2.0 (lh_adaptive_tuner)"
    )
    parser.add_argument("--status",   action="store_true", help="查看当前参数 + 哈希链")
    parser.add_argument("--analyze",  action="store_true", help="仅看数据分析 + 趋势")
    parser.add_argument("--simulate", action="store_true", help="模拟微调（默认安全模式）")
    parser.add_argument("--apply",    action="store_true", help="真正落盘微调")
    parser.add_argument("--rollback", action="store_true", help="回滚到上一代参数")
    parser.add_argument("--audit",    action="store_true", help="本次微调结束自动生成审计报告")
    parser.add_argument("--demo",     action="store_true", help="完整演示")
    args = parser.parse_args()

    tuner = AdaptiveTuner()

    # ── status ──
    if args.status:
        print("\n📊 当前自适应参数 v2.0：")
        for k, v in tuner.view_params().items():
            if k.startswith("_") or k in ("微调记录",):
                continue
            print(f"   {k}: {v}")
        print("\n🔗 哈希链：")
        print(f"   当前: {tuner.params.参数哈希 or '（未初始化）'}")
        print(f"   父代: {tuner.params.父哈希 or '（无）'}")
        print(f"\n📋 微调历史 ({len(tuner.params.微调记录)} 次)：")
        for rec in tuner.params.微调记录[-5:]:
            n_adj = len(rec.get("调整", []))
            n_trend = len(rec.get("趋势警告", []))
            print(f"   [{rec['时间'][:16]}] {rec.get('三色','?')} dr={rec.get('dr','?')} {n_adj}项调整 {n_trend}项趋势警告")
        return

    # ── analyze ──
    if args.analyze:
        print("\n📈 数据分析 + 趋势：")
        data = tuner.analyze()
        for k, v in data.items():
            print(f"   {k}: {v}")
        color, dr, desc = tricolor_dr_audit(data)
        print(f"\n🚦 三色 dr: {color} dr={dr} · {desc}")
        return

    # ── rollback ──
    if args.rollback:
        print("\n⏪ 回滚到上一代参数...")
        result = tuner.rollback()
        for k, v in result.items():
            print(f"   {k}: {v}")
        return

    # ── apply / simulate ──
    if args.apply:
        print("\n🔧 真正落盘微调（--apply）...")
        result = tuner.tune(simulate=False)
    elif args.simulate or not (args.demo):
        print("\n🔍 模拟微调（安全模式·不落盘）...")
        result = tuner.tune(simulate=True)
    else:
        result = None

    if result is not None:
        print(f"\n📊 状态: {result['status']}")
        print(f"🚦 三色: {result.get('三色','?')} dr={result.get('dr','?')} · {result.get('dr说明','')}")
        for r in result.get("调整记录", []):
            print(f"   {r}")
        if not result.get("调整记录"):
            print("   无需调整")
        if args.audit or args.apply:
            report = tuner.generate_audit_report(result)
            print(f"\n📝 审计报告: {report}")
        return

    # ── demo ──
    if args.demo:
        print("\n🐉 龍魂·自适应微调参数系统 v2.0 演示\n")
        print("═" * 60)
        print("📊 当前参数：")
        for k, v in tuner.view_params().items():
            if k.startswith("_") or k == "微调记录":
                continue
            print(f"   {k}: {v}")
        print("\n" + "═" * 60)
        print("📈 数据分析 + 趋势：")
        data = tuner.analyze()
        for k, v in data.items():
            print(f"   {k}: {v}")
        print("\n" + "═" * 60)
        print("🔍 模拟微调（不落盘）：")
        result = tuner.tune(simulate=True)
        print(f"   状态: {result['status']}")
        print(f"   三色: {result.get('三色','?')} dr={result.get('dr','?')}")
        for r in result.get("调整记录", []) or ["   （无调整建议）"]:
            print(f"   {r}")
        print("\n" + "═" * 60)
        print("📝 生成演示审计报告...")
        report = tuner.generate_audit_report(result)
        print(f"   {report}")
        return


if __name__ == "__main__":
    main()
