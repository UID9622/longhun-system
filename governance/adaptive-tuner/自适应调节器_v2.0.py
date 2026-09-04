#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  龍魂·自适应微调参数系统 v2.0                                ║
║  DNA: #龍芯⚡️20260529-自适应参数-v2.0                       ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F               ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ║
║  RBT-SEAL: #龍芯⚡️20260423-ROOT-SEAL-01F32FFD                ║
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

联动（2026-07-27 接入·bridge/）：
  微调/熔断/回滚/审计四处发射事件 → 联动桥分发四引擎适配器
  （规则引擎快照+熔断LOCK / 三色审计交叉验证 / 草日志入册 / DNA§14登记）
  --link-status 查看注册表 + 四适配器自检表

用法:
  python3 自适应调节器.py --status           # 查看当前参数 + 哈希链
  python3 自适应调节器.py --analyze          # 仅看数据分析+趋势
  python3 自适应调节器.py --simulate         # 模拟微调（默认安全模式）
  python3 自适应调节器.py --apply            # 真正落盘微调
  python3 自适应调节器.py --rollback         # 回滚到上一代参数
  python3 自适应调节器.py --audit            # 生成本次审计报告（可单独使用·走模拟+出报告）
  python3 自适应调节器.py --verify           # 哈希链完整性校验（任一失败退出码非零）
  python3 自适应调节器.py --demo-data [N]    # 生成 N 个合成事件写入账本（默认 60·追加不覆盖）
  python3 自适应调节器.py --seed 9622        # 配合 --demo-data 复现随机序列
  python3 自适应调节器.py --demo             # 完整演示
  python3 自适应调节器.py --link-status      # 联动注册表 + 四适配器自检
  python3 自适应调节器.py                    # 无参数 → 默认模拟（安全模式）
"""

import json
import hashlib
import os
import sys
import argparse
import logging
import random
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict, fields
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
class 微调参数:
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
    微调记录: list = field(default_factory=list)

# ═══════════════════════════════════════════════════════════════
# 二、硬界 · 焊死·调节器越界即拒绝
# ═══════════════════════════════════════════════════════════════

参数硬界: Dict[str, Tuple[float, float]] = {
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

def 三色_dr(数据: dict) -> Tuple[str, int, str]:
    """
    根据分析数据评估三色 dr。
    🟢 dr ∈ {1,2,4,5,7,8}   通行
    🟡 dr = 6               待审（人工眼）
    🔴 dr ∈ {3,9}           熔断（拒绝保存）
    """
    if 数据.get("状态", "").startswith("🟡"):
        return ("🟡", 6, "样本不足·待审")

    甩锅率 = 数据.get("甩锅率", 0)
    威胁率 = 数据.get("威胁率", 0)
    没立正率 = 数据.get("没立正率", 0)

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
# 三点五、DNA 生成器钩子 · 前向兼容工具（v2.0 加固）
# ═══════════════════════════════════════════════════════════════

def 生成DNA(动作标签: str, 版本: str = "2.0") -> str:
    """
    新格式 DNA 一律以本地生成器为准·禁止手写伪造。
    依次在 脚本所在目录/bin/ 与 ~/.龍魂/bin/ 查找 lh_dna_generator.py，
    生成器 CLI 首行为 DNA 本体（其后为干支/卦名详情·只取首行），
    任何失败（不存在/超时/非零退出/空输出/首行非DNA）→ 返回待校正占位 DNA。
    注意：生成器内部自拼 "-v{版本}"·本钩子版本号不带 v 前缀。
    """
    候选路径 = [
        Path(__file__).resolve().parent / "bin" / "lh_dna_generator.py",
        Path(os.path.expanduser("~/.龍魂/bin/lh_dna_generator.py")),
    ]
    for 路径 in 候选路径:
        if not 路径.is_file():
            continue
        try:
            结果 = subprocess.run(
                [sys.executable, str(路径), 动作标签, 版本],
                capture_output=True, text=True, timeout=5,
            )
            if 结果.returncode == 0 and 结果.stdout.strip():
                首行 = 结果.stdout.strip().splitlines()[0].strip()
                if 首行.startswith("#龍芯⚡️"):
                    return 首行
        except Exception:
            # ── 超时/执行异常 → 尝试下一个候选 ──
            continue
    return f"#龍芯⚡️待生成器校正-{动作标签}-{版本}"

def _过滤已知字段(data: dict) -> dict:
    """
    前向兼容加载：剔除 dataclass 未知键，
    防止旧/新 JSON 多字段导致 微调参数(**data) TypeError。
    """
    已知键 = {f.name for f in fields(微调参数)}
    return {k: v for k, v in data.items() if k in 已知键}

# ═══════════════════════════════════════════════════════════════
# 三点六、联动桥钩子（v2.0 追加·SPEC §六·fail-isolated 零影响主流程）
# ═══════════════════════════════════════════════════════════════

def _发射联动(事件类型: str, 载荷: dict):
    """可选联动·桥缺席或异常零影响"""
    try:
        from pathlib import Path as _P
        import importlib.util as _iu
        桥文件 = _P(__file__).resolve().parent / "bridge" / "lh_tuner_bridge.py"
        if not 桥文件.is_file():
            return
        spec = _iu.spec_from_file_location("lh_tuner_bridge", 桥文件)
        mod = _iu.module_from_spec(spec); spec.loader.exec_module(mod)
        mod.取桥().emit(事件类型, 载荷)
    except Exception:
        pass

def _联动数据摘要(数据: dict) -> dict:
    """从分析数据取六率组装载荷数据摘要（缺失键补默认 0.0）"""
    return {k: 数据.get(k, 0.0) for k in
            ("甩锅率", "自扛率", "没立正率", "威胁率", "补救率", "惯犯率")}

# ═══════════════════════════════════════════════════════════════
# 四、调节器主类
# ═══════════════════════════════════════════════════════════════

class 自适应调节器:
    """
    v2.0 升级：双向 + 滞回 + 趋势 + 回滚 + 三色 dr + 哈希链
    """

    def __init__(
        self,
        账本路径: str = os.path.expanduser("~/.龍魂/規則帳本.jsonl"),
        参数路径: str = os.path.expanduser("~/.龍魂/微調參數.json"),
        历史路径: str = os.path.expanduser("~/.龍魂/微調歷史/"),
        审计路径: str = os.path.expanduser("~/.龍魂/微調審計/"),
    ):
        self.账本路径 = 账本路径
        self.参数路径 = 参数路径
        self.历史路径 = Path(历史路径)
        self.审计路径 = Path(审计路径)
        self.历史路径.mkdir(parents=True, exist_ok=True)
        self.审计路径.mkdir(parents=True, exist_ok=True)

        self.参数 = self._加载参数()
        self.事件列表: List[dict] = self._加载账本()

    # ── 持久化 ────────────────────────────────────────────

    def _加载参数(self) -> 微调参数:
        if os.path.exists(self.参数路径):
            with open(self.参数路径, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 兼容 v1.0 旧文件
                data.pop("熔断_dr_说明", None)
                data.pop("待审_dr_说明", None)
                data.pop("分数上下限说明", None)
                # tuple 字段
                for k in ("熔断_dr", "待审_dr"):
                    if k in data and isinstance(data[k], list):
                        data[k] = tuple(data[k])
                # 加固①：前向兼容·过滤未知键防 TypeError
                return 微调参数(**_过滤已知字段(data))
        return 微调参数()

    def _计算哈希(self, p: 微调参数) -> str:
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

    def _保存参数(self):
        """保存参数 + 备份上一代到历史目录"""
        # 备份当前文件到历史
        if os.path.exists(self.参数路径) and self.参数.参数哈希:
            备份名 = self.历史路径 / f"{self.参数.参数哈希}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(self.参数路径, "r", encoding="utf-8") as 旧:
                with open(备份名, "w", encoding="utf-8") as 新:
                    新.write(旧.read())

        # 更新哈希链
        self.参数.父哈希 = self.参数.参数哈希
        self.参数.参数哈希 = self._计算哈希(self.参数)

        Path(self.参数路径).parent.mkdir(parents=True, exist_ok=True)
        with open(self.参数路径, "w", encoding="utf-8") as f:
            data = asdict(self.参数)
            # tuple 转 list 写入
            for k in ("熔断_dr", "待审_dr"):
                if isinstance(data.get(k), tuple):
                    data[k] = list(data[k])
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _加载账本(self) -> List[dict]:
        events = []
        if os.path.exists(self.账本路径):
            with open(self.账本路径, "r", encoding="utf-8") as f:
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

    def _在窗口内(self, 事件: dict, 天数: int) -> bool:
        try:
            ts = 事件.get("时间戳", "")
            if not ts:
                return False
            t = datetime.fromisoformat(ts)
            return t >= datetime.now() - timedelta(days=天数)
        except Exception:
            return False

    def _在窗口区间(self, 事件: dict, 起天数: int, 止天数: int) -> bool:
        try:
            ts = 事件.get("时间戳", "")
            if not ts:
                return False
            t = datetime.fromisoformat(ts)
            now = datetime.now()
            return (now - timedelta(days=起天数)) >= t >= (now - timedelta(days=止天数))
        except Exception:
            return False

    # ── 分析 + 趋势（v2.0 新增） ──────────────────────────

    def _统计一段(self, 窗口事件: List[dict]) -> dict:
        if not 窗口事件:
            return {"样本数": 0}
        犯错 = [e for e in 窗口事件 if e.get("犯错")]
        return {
            "样本数": len(窗口事件),
            "犯错率": round(len(犯错) / len(窗口事件), 3),
            "自扛率": round(len([e for e in 犯错 if e.get("自扛")]) / len(犯错), 3) if 犯错 else 0,
            "甩锅率": round(len([e for e in 犯错 if not e.get("自扛")]) / len(犯错), 3) if 犯错 else 0,
            "没立正率": round(len([e for e in 犯错 if not e.get("立正")]) / len(犯错), 3) if 犯错 else 0,
            "威胁率": round(len([e for e in 窗口事件 if e.get("威胁")]) / len(窗口事件), 3),
            "补救率": round(len([e for e in 犯错 if e.get("补救")]) / len(犯错), 3) if 犯错 else 0,
            # 加固③：R6 惯犯追踪接入微调（犯错事件中惯犯占比）
            "惯犯率": round(len([e for e in 犯错 if e.get("惯犯")]) / len(犯错), 3) if 犯错 else 0,
        }

    def 分析(self) -> dict:
        """v2.0：返回快照 + 趋势"""
        窗口 = self.参数.观察窗口_天
        窗口事件 = [e for e in self.事件列表 if self._在窗口内(e, 窗口)]

        if len(窗口事件) < self.参数.最小样本:
            return {
                "状态": "🟡 样本不足",
                "样本数": len(窗口事件),
                "最小要求": self.参数.最小样本,
                "建议": "积累更多事件后再微调",
            }

        全段 = self._统计一段(窗口事件)
        # v2.0 新增：前半段 vs 后半段趋势
        半 = 窗口 // 2
        前半 = [e for e in self.事件列表 if self._在窗口区间(e, 半, 窗口)]
        后半 = [e for e in self.事件列表 if self._在窗口区间(e, 0, 半)]
        前 = self._统计一段(前半)
        后 = self._统计一段(后半)

        趋势 = {}
        for k in ("甩锅率", "自扛率", "没立正率", "补救率", "威胁率"):
            if k in 前 and k in 后:
                趋势[k] = round(后.get(k, 0) - 前.get(k, 0), 3)

        全段["状态"] = "🟢 足够样本"
        全段["趋势"] = 趋势
        return 全段

    # ── 双向调整 + 滞回带（v2.0 核心升级） ────────────────

    def _双向调整(
        self,
        当前值: float,
        指标值: float,
        高阈值: float,
        低阈值: float,
        硬界: Tuple[float, float],
        速率: float,
        参数名: str,
        方向标签: str = "扣分",
        取整: bool = False,
    ) -> Tuple[float, Optional[str]]:
        """
        v2.0 双向调整 + 滞回带防震
        指标超高 → 朝硬界上界推进（加重）
        指标超低 → 朝硬界下界回退（放松）
        滞回带内不调整（防止边缘震荡）
        加固②：取整=True 时新值 round 为 int（为整数参数铺路）
        """
        滞回 = self.参数.滞回带

        if 指标值 > 高阈值 + 滞回:
            新值 = round(min(当前值 * (1 + 速率), 硬界[1]), 1)
            if 取整:
                新值 = int(round(新值))
            if 新值 != 当前值:
                return 新值, f"🔼 {参数名}: {当前值} → {新值} ({方向标签}从严·指标 {指标值:.1%} > {高阈值:.0%})"
        elif 指标值 < 低阈值 - 滞回:
            新值 = round(max(当前值 * (1 - 速率 * 0.5), 硬界[0]), 1)
            if 取整:
                新值 = int(round(新值))
            if 新值 != 当前值:
                return 新值, f"🔽 {参数名}: {当前值} → {新值} ({方向标签}放松·指标 {指标值:.1%} < {低阈值:.0%})"
        return 当前值, None

    # ── 微调主流程 ────────────────────────────────────────

    def 微调(self, 模拟: bool = True) -> dict:
        """
        v2.0：默认模拟态·非模拟需 --apply
        触发流程：分析 → 三色 dr → 微调建议 → 红线熔断检测 → 落盘
        """
        数据 = self.分析()
        if "样本不足" in 数据.get("状态", ""):
            return {"状态": "跳过", "原因": "样本不足", "数据": 数据}

        色, dr, dr说明 = 三色_dr(数据)

        # 🔴 dr ∈ {3,9} 熔断 — 拒绝任何参数修改
        if 色 == "🔴":
            # ── 联动桥发射点①：TUNE_MELTDOWN（追加·fail-isolated） ──
            _发射联动("TUNE_MELTDOWN", {
                "状态": "🔴 熔断·拒绝微调",
                "三色": 色, "dr": dr,
                "参数哈希": self.参数.参数哈希,
                "父哈希": self.参数.父哈希,
                "调整数": 0, "调整记录": [],
                "数据摘要": _联动数据摘要(数据),
                "趋势": 数据.get("趋势", {}),
                "原因": "数据触发红线·人工介入排查",
            })
            return {
                "状态": f"🔴 熔断·拒绝微调",
                "三色": 色, "dr": dr, "dr说明": dr说明,
                "数据": 数据, "调整数": 0, "调整记录": [],
                "模拟": 模拟,
                "参数哈希": self.参数.参数哈希,
                "父哈希": self.参数.父哈希,
                "原因": "数据触发红线·人工介入排查"
            }

        调整记录: List[str] = []
        原参数 = deepcopy(self.参数)
        速率 = self.参数.学习率

        # ── R1 责任承担（双向） ──
        新值, 记录 = self._双向调整(
            self.参数.逃避扣分, 数据["甩锅率"],
            高阈值=0.5, 低阈值=0.15,
            硬界=参数硬界["逃避扣分"], 速率=速率,
            参数名="逃避扣分", 方向标签="甩锅"
        )
        if 记录:
            调整记录.append(记录)
            if not 模拟: self.参数.逃避扣分 = 新值

        新值, 记录 = self._双向调整(
            self.参数.自扛加分, 数据["自扛率"],
            高阈值=0.8, 低阈值=0.3,
            硬界=参数硬界["自扛加分"], 速率=速率 * 0.5,
            参数名="自扛加分", 方向标签="自扛奖励"
        )
        if 记录:
            调整记录.append(记录)
            if not 模拟: self.参数.自扛加分 = 新值

        # ── R2 批评姿态（双向） ──
        新值, 记录 = self._双向调整(
            self.参数.没立正扣分, 数据["没立正率"],
            高阈值=0.4, 低阈值=0.1,
            硬界=参数硬界["没立正扣分"], 速率=速率,
            参数名="没立正扣分", 方向标签="没立正"
        )
        if 记录:
            调整记录.append(记录)
            if not 模拟: self.参数.没立正扣分 = 新值

        # ── R5 补救（双向） ──
        新值, 记录 = self._双向调整(
            self.参数.补救加分, 数据["补救率"],
            高阈值=0.3, 低阈值=0.05,
            硬界=参数硬界["补救加分"], 速率=速率 * 0.5,
            参数名="补救加分", 方向标签="补救奖励"
        )
        if 记录:
            调整记录.append(记录)
            if not 模拟: self.参数.补救加分 = 新值

        # ── R6 惯犯追踪（双向·加固③接入微调） ──
        # 惯犯扣分随惯犯率双向调整；惯犯触发次数保持静态不动（避免反向逻辑）
        新值, 记录 = self._双向调整(
            self.参数.惯犯扣分, 数据["惯犯率"],
            高阈值=0.2, 低阈值=0.05,
            硬界=参数硬界["惯犯扣分"], 速率=速率,
            参数名="惯犯扣分", 方向标签="惯犯"
        )
        if 记录:
            调整记录.append(记录)
            if not 模拟: self.参数.惯犯扣分 = 新值

        # ── v2.0 新增：趋势惯性调整（恶化趋势 → 加重） ──
        趋势 = 数据.get("趋势", {})
        if 趋势.get("甩锅率", 0) > 0.1:
            调整记录.append(f"📈 趋势警告：甩锅率上升 {趋势['甩锅率']:.1%}·建议人工介入")
        if 趋势.get("自扛率", 0) > 0.1:
            调整记录.append(f"📈 趋势喜报：自扛率上升 {趋势['自扛率']:.1%}·习惯在养成")

        # ── 落盘 ──
        # 有调整则落盘；首次 --apply（哈希链未初始化）也落盘一次，建立版本链起点
        if not 模拟 and (调整记录 or not self.参数.参数哈希):
            ts = datetime.now().isoformat()
            self.参数.最后微调时间 = ts
            self.参数.微调记录.append({
                "时间": ts,
                "三色": 色, "dr": dr,
                "调整": [r for r in 调整记录 if not r.startswith("📈")],
                "趋势警告": [r for r in 调整记录 if r.startswith("📈")],
                "父哈希": self.参数.参数哈希,
                "数据摘要": {k: v for k, v in 数据.items() if k not in ("状态", "趋势")},
                "趋势": 趋势,
            })
            self._保存参数()
            log.info(f"参数已落盘·新哈希 {self.参数.参数哈希}·父哈希 {self.参数.父哈希}")

        # ── 联动桥发射点②：TUNE_APPLIED（非模拟且有落盘）/ TUNE_SIMULATED（模拟） ──
        # 落盘判定复刻上方落盘条件（追加计算·不改旧逻辑）
        _已落盘 = (not 模拟) and (bool(调整记录) or not 原参数.参数哈希)
        if _已落盘:
            _事件类型 = "TUNE_APPLIED"
        elif 模拟:
            _事件类型 = "TUNE_SIMULATED"
        else:
            _事件类型 = ""   # 落盘态但无需调整且无状态变化·不发射
        if _事件类型:
            _发射联动(_事件类型, {
                "状态": "🟢 微调完成" if _已落盘 else "🟡 模拟态·未落盘",
                "三色": 色, "dr": dr,
                "参数哈希": self.参数.参数哈希,
                "父哈希": self.参数.父哈希,
                "调整数": len(调整记录),
                "调整记录": list(调整记录),
                "数据摘要": _联动数据摘要(数据),
                "趋势": 数据.get("趋势", {}),
            })

        return {
            "状态": "🟢 微调完成" if (调整记录 and not 模拟) else
                   "🟡 模拟态·未落盘" if (调整记录 and 模拟) else
                   "🟢 无需调整",
            "三色": 色, "dr": dr, "dr说明": dr说明,
            "调整数": len(调整记录),
            "调整记录": 调整记录,
            "数据": 数据,
            "模拟": 模拟,
            "参数哈希": self.参数.参数哈希,
            "父哈希": self.参数.父哈希,
        }

    # ── 回滚（v2.0 新增） ─────────────────────────────────

    def 回滚(self) -> dict:
        """回滚到上一代参数（从历史目录读取）"""
        if not self.参数.父哈希:
            return {"状态": "🟡 无父代·无法回滚"}

        # 检查冷却期
        if self.参数.最后微调时间:
            try:
                上次 = datetime.fromisoformat(self.参数.最后微调时间)
                冷却天数 = (datetime.now() - 上次).days
                if 冷却天数 < self.参数.回滚冷却_天:
                    return {
                        "状态": f"🟡 冷却期内·剩余 {self.参数.回滚冷却_天 - 冷却天数} 天",
                        "原因": "防止频繁回滚震荡"
                    }
            except Exception:
                pass

        # 在历史目录寻找父哈希对应的备份
        候选 = list(self.历史路径.glob(f"{self.参数.父哈希}_*.json"))
        if not 候选:
            return {"状态": "🔴 父代备份缺失·无法回滚", "父哈希": self.参数.父哈希}

        最新 = sorted(候选)[-1]
        with open(最新, "r", encoding="utf-8") as f:
            旧 = json.load(f)
            for k in ("熔断_dr", "待审_dr"):
                if k in 旧 and isinstance(旧[k], list):
                    旧[k] = tuple(旧[k])
            # 加固①：前向兼容·过滤未知键防 TypeError
            self.参数 = 微调参数(**_过滤已知字段(旧))
        self._保存参数()
        log.info(f"已回滚到父代 {self.参数.父哈希}·新哈希 {self.参数.参数哈希}")
        # ── 联动桥发射点③：TUNE_ROLLBACK（追加·fail-isolated） ──
        _发射联动("TUNE_ROLLBACK", {
            "状态": "🟢 回滚完成",
            "三色": "🟢", "dr": 7,
            "参数哈希": self.参数.参数哈希,
            "父哈希": self.参数.父哈希,
            "调整数": 0, "调整记录": [],
            "原因": "回滚完成·解除从严模式",
        })
        return {
            "状态": "🟢 回滚完成",
            "回滚到": str(最新.name),
            "当前哈希": self.参数.参数哈希,
        }

    # ── 查看参数 ──────────────────────────────────────────

    def 查看参数(self) -> dict:
        d = asdict(self.参数)
        for k in ("熔断_dr", "待审_dr"):
            if isinstance(d.get(k), tuple):
                d[k] = list(d[k])
        d["_焊死字段"] = ["熔断_dr", "待审_dr", "分数上限", "分数下限", "威胁归零开关"]
        return d

    # ── 哈希链完整性校验（加固④·--verify） ────────────────

    def 校验哈希链(self) -> Tuple[bool, List[Tuple[str, bool, str]]]:
        """
        哈希链完整性校验：
          ① 重算当前参数哈希 ↔ 存储值比对
          ② 父哈希须在历史目录有对应备份文件
        返回 (总判定, [(检查项, 通过, 说明), ...])
        """
        检查: List[Tuple[str, bool, str]] = []

        # ── ① 当前参数哈希一致性 ──
        重算 = self._计算哈希(self.参数)
        存储 = self.参数.参数哈希
        if not 存储:
            检查.append(("当前参数哈希", False, f"存储值为空（从未落盘）·重算 {重算}"))
        else:
            通过 = (重算 == 存储)
            检查.append(("当前参数哈希", 通过, f"重算 {重算} ↔ 存储 {存储}"))

        # ── ② 父哈希历史备份存在性 ──
        if not self.参数.父哈希:
            检查.append(("父哈希历史备份", True, "无父代（首代参数）·无需备份"))
        else:
            候选 = list(self.历史路径.glob(f"{self.参数.父哈希}_*.json"))
            通过 = bool(候选)
            说明 = f"找到 {len(候选)} 份备份" if 通过 else f"缺失 {self.参数.父哈希}_*.json"
            检查.append(("父哈希历史备份", 通过, 说明))

        总判定 = all(通过 for _, 通过, _ in 检查)
        return 总判定, 检查

    # ── 合成演示数据（加固⑦·--demo-data） ─────────────────

    def 生成演示数据(self, 数量: int = 60, 种子: Optional[int] = None) -> int:
        """
        生成 N 个合成事件追加写入账本（不覆盖已有内容）。
        时间戳随机分布在过去 观察窗口_天 内（锚定当日 23:59:59·同种子同日可复现）；
        bool 字段概率：自扛 0.6 / 立正 0.7 / 威胁 0.02 / 补救 0.3 / 惯犯 0.1。
        """
        rng = random.Random(种子)
        窗口 = self.参数.观察窗口_天
        now = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
        事件列 = []
        for _ in range(数量):
            # 随机分布在窗口内（按秒偏移）
            偏移秒 = rng.randint(0, 窗口 * 86400)
            ts = (now - timedelta(seconds=偏移秒)).isoformat()
            犯错 = rng.random() < 0.75
            事件列.append({
                "时间戳": ts,
                "犯错": 犯错,
                # 以下字段仅对犯错事件有意义·非犯错一律 False
                "自扛": 犯错 and rng.random() < 0.6,
                "立正": 犯错 and rng.random() < 0.7,
                "威胁": rng.random() < 0.02,
                "补救": 犯错 and rng.random() < 0.3,
                "惯犯": 犯错 and rng.random() < 0.1,
            })
        # 按时间排序后追加·保持账本时序整洁
        事件列.sort(key=lambda e: e["时间戳"])
        Path(self.账本路径).parent.mkdir(parents=True, exist_ok=True)
        with open(self.账本路径, "a", encoding="utf-8") as f:
            for e in 事件列:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
        return len(事件列)

    # ── Markdown 审计报告（v2.0 新增） ────────────────────

    def 生成审计报告(self, 微调结果: dict) -> Path:
        """落地 Markdown 审计·便于眼审 + 入 Notion 草日志"""
        今日 = datetime.now().strftime("%Y-%m-%d")
        时分 = datetime.now().strftime("%H:%M:%S")
        路径 = self.审计路径 / f"{今日}_{时分.replace(':','')}.md"

        数据 = 微调结果.get("数据", {})
        趋势 = 数据.get("趋势", {})
        色 = 微调结果.get("三色", "🟡")
        dr = 微调结果.get("dr", 6)

        md = []
        md.append(f"# 龍魂·自适应微调审计 · {今日} {时分}")
        md.append("")
        # 加固⑥：新格式 DNA 走本地生成器钩子·禁止手写伪造
        md.append(f"- **DNA**: {生成DNA('TUNE-AUDIT')}")
        md.append(f"- **GPG**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
        md.append(f"- **CONFIRM**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
        md.append(f"- **三色**: {色}·dr={dr}·{微调结果.get('dr说明','')}")
        md.append(f"- **状态**: {微调结果.get('状态','')}")
        md.append(f"- **模拟**: {微调结果.get('模拟', True)}")
        md.append(f"- **参数哈希**: `{微调结果.get('参数哈希','')}`")
        md.append(f"- **父哈希**: `{微调结果.get('父哈希','')}`")
        md.append("")
        md.append("## 数据快照")
        for k, v in 数据.items():
            if k in ("状态", "趋势"):
                continue
            md.append(f"- {k}: {v}")
        if 趋势:
            md.append("")
            md.append("## 趋势（后半段 − 前半段）")
            for k, v in 趋势.items():
                箭头 = "📈" if v > 0 else "📉" if v < 0 else "➖"
                md.append(f"- {箭头} {k}: {v:+.3f}")
        md.append("")
        md.append("## 调整记录")
        for r in 微调结果.get("调整记录", []) or ["（无调整）"]:
            md.append(f"- {r}")
        md.append("")
        md.append("---")
        md.append("责任：UID9622·不免责 | SEAL: #ZHUGEXIN⚡️2025-DEVICE-BIND-SOUL")

        路径.write_text("\n".join(md), encoding="utf-8")
        log.info(f"审计报告已落: {路径}")
        # ── 联动桥发射点④：TUNE_AUDIT（追加·fail-isolated·调整记录可传空list） ──
        _发射联动("TUNE_AUDIT", {
            "状态": 微调结果.get("状态", ""),
            "三色": 色, "dr": dr,
            "参数哈希": 微调结果.get("参数哈希", ""),
            "父哈希": 微调结果.get("父哈希", ""),
            "调整数": 微调结果.get("调整数", 0),
            "调整记录": [],
            "数据摘要": _联动数据摘要(数据),
            "趋势": 趋势,
        })
        return 路径

# ═══════════════════════════════════════════════════════════════
# 五、CLI 入口 · v2.0 默认安全模式
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂·自适应微调参数系统 v2.0"
    )
    parser.add_argument("--status",   action="store_true", help="查看当前参数 + 哈希链")
    parser.add_argument("--analyze",  action="store_true", help="仅看数据分析 + 趋势")
    parser.add_argument("--simulate", action="store_true", help="模拟微调（默认安全模式）")
    parser.add_argument("--apply",    action="store_true", help="真正落盘微调")
    parser.add_argument("--rollback", action="store_true", help="回滚到上一代参数")
    parser.add_argument("--audit",    action="store_true", help="本次微调结束自动生成审计报告（可单独使用·走模拟+出报告）")
    parser.add_argument("--verify",   action="store_true", help="哈希链完整性校验（任一失败退出码非零）")
    parser.add_argument("--demo-data", nargs="?", const=60, type=int, default=None, metavar="N",
                        help="生成 N 个合成事件写入账本（默认 60·追加不覆盖）")
    parser.add_argument("--seed",     type=int, default=None, help="配合 --demo-data 复现随机序列")
    parser.add_argument("--demo",     action="store_true", help="完整演示")
    parser.add_argument("--link-status", action="store_true", help="打印联动注册表 + 四适配器自检结果表")
    args = parser.parse_args()

    调节器 = 自适应调节器()

    # ── link-status（联动桥自检·追加分支·不改旧分支） ──
    if args.link_status:
        try:
            from pathlib import Path as _P
            import importlib.util as _iu
            桥文件 = _P(__file__).resolve().parent / "bridge" / "lh_tuner_bridge.py"
            if not 桥文件.is_file():
                print("\n🟡 联动桥未安装：未找到 bridge/lh_tuner_bridge.py"
                      "·调节器独立运行不受影响")
                return
            spec = _iu.spec_from_file_location("lh_tuner_bridge", 桥文件)
            mod = _iu.module_from_spec(spec); spec.loader.exec_module(mod)
            桥 = mod.取桥()
            print(f"\n🔗 联动注册表: {桥.注册表路径}")
            print(json.dumps(桥.注册表, ensure_ascii=False, indent=2))
            print("\n🧪 四适配器自检（TUNE_AUDIT 测试事件）:")
            for r in 桥.自检():
                print(f"   {r['状态']} {r['适配器']}: {r['说明']}")
        except Exception as e:
            print(f"\n🟡 联动桥自检失败（不影响调节器本体）: {e}")
        return

    # ── demo-data（加固⑦） ──
    if args.demo_data is not None:
        if os.path.exists(调节器.账本路径):
            print(f"⚠️ 账本已存在：{调节器.账本路径}·本次为追加写入·不覆盖")
        n = 调节器.生成演示数据(数量=args.demo_data, 种子=args.seed)
        print(f"\n🧪 已生成 {n} 个合成事件 → {调节器.账本路径}")
        return

    # ── verify（加固④） ──
    if args.verify:
        print("\n🔗 哈希链完整性校验：")
        总判定, 检查 = 调节器.校验哈希链()
        for 名称, 通过, 说明 in 检查:
            图标 = "🟢" if 通过 else "🔴"
            print(f"   {图标} {名称}: {说明}")
        if 总判定:
            print("\n🟢 总判定：通过·哈希链完整")
            sys.exit(0)
        else:
            print("\n🔴 总判定：失败·哈希链受损")
            sys.exit(1)

    # ── status ──
    if args.status:
        print("\n📊 当前自适应参数 v2.0：")
        for k, v in 调节器.查看参数().items():
            if k.startswith("_") or k in ("微调记录",):
                continue
            print(f"   {k}: {v}")
        print(f"\n🔗 哈希链：")
        print(f"   当前: {调节器.参数.参数哈希 or '（未初始化）'}")
        print(f"   父代: {调节器.参数.父哈希 or '（无）'}")
        print(f"\n📋 微调历史 ({len(调节器.参数.微调记录)} 次)：")
        for rec in 调节器.参数.微调记录[-5:]:
            n调整 = len(rec.get("调整", []))
            n趋势 = len(rec.get("趋势警告", []))
            print(f"   [{rec['时间'][:16]}] {rec.get('三色','?')} dr={rec.get('dr','?')} {n调整}项调整 {n趋势}项趋势警告")
        return

    # ── analyze ──
    if args.analyze:
        print("\n📈 数据分析 + 趋势：")
        数据 = 调节器.分析()
        for k, v in 数据.items():
            print(f"   {k}: {v}")
        色, dr, 说明 = 三色_dr(数据)
        print(f"\n🚦 三色 dr: {色} dr={dr} · {说明}")
        return

    # ── rollback ──
    if args.rollback:
        print("\n⏪ 回滚到上一代参数...")
        结果 = 调节器.回滚()
        for k, v in 结果.items():
            print(f"   {k}: {v}")
        return

    # ── apply / simulate ──
    if args.apply:
        print("\n🔧 真正落盘微调（--apply）...")
        结果 = 调节器.微调(模拟=False)
    elif args.simulate or not (args.demo):
        print("\n🔍 模拟微调（安全模式·不落盘）...")
        结果 = 调节器.微调(模拟=True)
    else:
        结果 = None

    if 结果 is not None:
        print(f"\n📊 状态: {结果['状态']}")
        print(f"🚦 三色: {结果.get('三色','?')} dr={结果.get('dr','?')} · {结果.get('dr说明','')}")
        for r in 结果.get("调整记录", []):
            print(f"   {r}")
        if not 结果.get("调整记录"):
            print("   无需调整")
        if args.audit or args.apply:
            报告 = 调节器.生成审计报告(结果)
            print(f"\n📝 审计报告: {报告}")
        return

    # ── demo ──
    if args.demo:
        print("\n🐉 龍魂·自适应微调参数系统 v2.0 演示\n")
        print("═" * 60)
        print("📊 当前参数：")
        for k, v in 调节器.查看参数().items():
            if k.startswith("_") or k == "微调记录":
                continue
            print(f"   {k}: {v}")
        print("\n" + "═" * 60)
        print("📈 数据分析 + 趋势：")
        数据 = 调节器.分析()
        for k, v in 数据.items():
            print(f"   {k}: {v}")
        print("\n" + "═" * 60)
        print("🔍 模拟微调（不落盘）：")
        结果 = 调节器.微调(模拟=True)
        print(f"   状态: {结果['状态']}")
        print(f"   三色: {结果.get('三色','?')} dr={结果.get('dr','?')}")
        for r in 结果.get("调整记录", []) or ["   （无调整建议）"]:
            print(f"   {r}")
        print("\n" + "═" * 60)
        print("📝 生成演示审计报告...")
        报告 = 调节器.生成审计报告(结果)
        print(f"   {报告}")
        return

if __name__ == "__main__":
    main()
