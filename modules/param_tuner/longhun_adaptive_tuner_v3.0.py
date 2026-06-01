#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  龍魂·自适应微调参数系统 v3.0                                    ║
║  DNA : #龍芯⚡️20260531-自适应参数-v3.0                          ║
║  GPG : A2D0092CEE2E5BA87035600924C3704A8CC26D5F                  ║
║  CONFIRM : #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                   ║
║  SEAL : #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL    ║
╚══════════════════════════════════════════════════════════════════╝

v3.0 相对 v2.0 新增/补全：
  ① 异常事件分级  —— CRITICAL / WARNING / INFO 三级·超阈自动升级
  ② 冷启动保护    —— 样本不足时用默认参数兜底·不静默失败
  ③ 参数漂移检测  —— 连续N次同向调整自动触发漂移警告
  ④ 铁律钩子接口  —— IRON-* 铁律通过 hook 注入·与调节器完全解耦
  ⑤ 实时健康评分  —— 0-100分·综合甩锅/自扛/威胁/补救四维
  ⑥ 草日志自动入册—— 每次微调自动 prepend 到 草日志.md·抹不掉
  ⑦ Web仪表板接口 —— 输出 JSON·供浏览器操作台消费
  ⑧ 参数上下文注释—— 每个参数附带说明·便于新终端接入
  ⑨ 多账本支持    —— 支持按项目分账本·不同项目独立调节
  ⑩ 自动修复建议  —— dr=6黄线时给出具体可执行的修复建议

用法:
  python3 自适应调节器.py --status           # 查看状态 + 健康评分
  python3 自适应调节器.py --analyze          # 数据分析 + 趋势 + 修复建议
  python3 自适应调节器.py --simulate         # 模拟微调（默认安全）
  python3 自适应调节器.py --apply            # 真正落盘微调
  python3 自适应调节器.py --rollback         # 回滚到上一代
  python3 自适应调节器.py --audit            # 生成 Markdown 审计报告
  python3 自适应调节器.py --health           # 仅输出健康评分
  python3 自适应调节器.py --web-export       # 导出 JSON 供操作台消费
  python3 自适应调节器.py --demo             # 完整演示
"""

import json
import hashlib
import os
import sys
import argparse
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from copy import deepcopy

# ═══════════════════════════════════════════════════════════════
# 〇、日志 · 三色 dr 标准
# ═══════════════════════════════════════════════════════════════

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("龍魂·调节器v3")

# ═══════════════════════════════════════════════════════════════
# 一、参数定义（v3.0 新增上下文注释 + 多账本标识）
# ═══════════════════════════════════════════════════════════════

@dataclass
class 微调参数:
    """
    规矩参数（非AI模型参数）。
    每个参数有硬界·越界即拒绝·焊死字段永不可调。
    v3.0 新增：账本标识、漂移计数、健康基线、铁律钩子列表。
    """

    # ── R1 责任承担 ──
    自扛加分: float = 2.0        # 主动承担责任时的加分幅度
    逃避扣分: float = 10.0       # 甩锅/逃避时的扣分幅度

    # ── R2 批评姿态 ──
    没立正扣分: float = 5.0      # 被批评后未立正的扣分

    # ── R4 威胁归零（焊死） ──
    威胁归零开关: bool = True     # 焊死·不可调·威胁行为直接归零
    威胁触发分数: int = 0         # 焊死·威胁后分数强制归零

    # ── R5 主动补救 ──
    补救加分: float = 5.0        # 主动补救行为的加分幅度

    # ── R6 惯犯追踪 ──
    惯犯触发次数: int = 3         # 连续违规N次触发惯犯标记
    惯犯扣分: float = 15.0       # 惯犯额外扣分

    # ── 三色闸门 dr（焊死·永不微调） ──
    熔断_dr: Tuple[int, ...] = (3, 9)   # 焊死
    待审_dr: Tuple[int, ...] = (6,)     # 焊死

    # ── 自适应元参数 ──
    学习率: float = 0.1           # 每次调整幅度·越大越激进
    观察窗口_天: int = 90         # 统计数据的时间窗口
    最小样本: int = 20            # 低于此数冷启动保护介入
    滞回带: float = 0.05          # 防震荡·阈值边缘缓冲区
    回滚冷却_天: int = 14         # 调整后N天内禁止回滚

    # ── 分数边界（焊死） ──
    分数上限: int = 100           # 焊死
    分数下限: int = 0             # 焊死

    # ── v3.0 新增：漂移检测 ──
    漂移阈值_连续次数: int = 3    # 同向调整超过N次触发漂移警告
    漂移计数: Dict = field(default_factory=dict)  # {参数名: 连续同向次数}

    # ── v3.0 新增：健康基线 ──
    健康基线_甩锅率上限: float = 0.3
    健康基线_自扛率下限: float = 0.4
    健康基线_威胁率上限: float = 0.05
    健康基线_补救率下限: float = 0.2

    # ── v3.0 新增：多账本 ──
    账本标识: str = "default"     # 项目名·不同项目独立调节

    # ── 元数据 + 哈希链 ──
    版本: str = "v3.0"
    最后微调时间: str = ""
    参数哈希: str = ""
    父哈希: str = ""
    微调记录: list = field(default_factory=list)
    铁律钩子列表: list = field(default_factory=list)  # v3.0 新增

# ═══════════════════════════════════════════════════════════════
# 二、硬界（焊死·越界即拒绝）
# ═══════════════════════════════════════════════════════════════

参数硬界: Dict[str, Tuple[float, float]] = {
    "自扛加分":              (1.0, 5.0),
    "逃避扣分":              (5.0, 25.0),
    "没立正扣分":            (2.0, 15.0),
    "威胁触发分数":          (0, 10),
    "补救加分":              (2.0, 10.0),
    "惯犯触发次数":          (2, 5),
    "惯犯扣分":              (10.0, 30.0),
    "学习率":                (0.01, 0.3),
    "观察窗口_天":           (30, 365),
    "最小样本":              (10, 100),
    "滞回带":                (0.0, 0.2),
    "回滚冷却_天":           (3, 90),
    "漂移阈值_连续次数":     (2, 10),
    "健康基线_甩锅率上限":   (0.1, 0.6),
    "健康基线_自扛率下限":   (0.2, 0.8),
    "健康基线_威胁率上限":   (0.01, 0.15),
    "健康基线_补救率下限":   (0.1, 0.6),
}

# ═══════════════════════════════════════════════════════════════
# 三、铁律钩子注册表（v3.0 新增·与调节器解耦）
# ═══════════════════════════════════════════════════════════════

_铁律钩子注册表: Dict[str, Callable] = {}

def 注册铁律钩子(铁律名: str):
    """装饰器·将函数注册为铁律钩子"""
    def decorator(fn: Callable) -> Callable:
        _铁律钩子注册表[铁律名] = fn
        return fn
    return decorator

@注册铁律钩子("IRON-THREAT-ZERO")
def _威胁归零钩子(参数: "微调参数", 数据: dict) -> Optional[str]:
    """威胁率过高时强制返回阻断信息"""
    if 数据.get("威胁率", 0) > 参数.健康基线_威胁率上限:
        return f"🔴 IRON-THREAT-ZERO 触发·威胁率 {数据['威胁率']:.1%} 超限·参数不可保存"
    return None

@注册铁律钩子("IRON-TUNER-RED-LINE-MELTDOWN")
def _熔断钩子(参数: "微调参数", 数据: dict) -> Optional[str]:
    """甩锅+没立正双高时熔断"""
    if 数据.get("甩锅率", 0) > 0.7 and 数据.get("没立正率", 0) > 0.6:
        return "🔴 IRON-TUNER-RED-LINE-MELTDOWN 触发·双高熔断"
    return None

def 执行铁律钩子(参数: "微调参数", 数据: dict) -> List[str]:
    """执行所有已注册铁律钩子·返回触发的阻断信息列表"""
    阻断列表 = []
    for 铁律名, fn in _铁律钩子注册表.items():
        结果 = fn(参数, 数据)
        if 结果:
            阻断列表.append(结果)
    return 阻断列表

# ═══════════════════════════════════════════════════════════════
# 四、三色 dr 审计（v3.0 增加修复建议输出）
# ═══════════════════════════════════════════════════════════════

def 三色_dr(数据: dict) -> Tuple[str, int, str, List[str]]:
    """
    返回 (颜色, dr值, 说明, 修复建议列表)
    🟢 dr ∈ {1,2,4,5,7,8}  通行
    🟡 dr = 6               待审·附修复建议
    🔴 dr ∈ {3,9}           熔断·拒绝保存
    """
    修复建议: List[str] = []

    if 数据.get("状态", "").startswith("🟡"):
        修复建议.append("积累更多事件数据后再触发微调（当前样本不足）")
        return ("🟡", 6, "样本不足·冷启动保护介入", 修复建议)

    甩锅率 = 数据.get("甩锅率", 0)
    威胁率 = 数据.get("威胁率", 0)
    没立正率 = 数据.get("没立正率", 0)
    自扛率 = 数据.get("自扛率", 0)
    补救率 = 数据.get("补救率", 0)

    # 🔴 熔断判定
    if 威胁率 > 0.1:
        return ("🔴", 9, f"威胁率 {威胁率:.1%} > 10%·熔断", [])
    if 甩锅率 > 0.7 and 没立正率 > 0.6:
        return ("🔴", 3, "甩锅+没立正双红线·熔断", [])

    # 🟡 黄线判定·附修复建议
    if 甩锅率 > 0.5:
        修复建议.append(f"甩锅率 {甩锅率:.1%} 偏高·建议加重逃避扣分·强化R1铁律")
    if 没立正率 > 0.5:
        修复建议.append(f"没立正率 {没立正率:.1%} 偏高·建议加重没立正扣分·强化R2铁律")
    if 自扛率 < 0.2:
        修复建议.append(f"自扛率 {自扛率:.1%} 偏低·建议提高自扛加分·正向激励")
    if 补救率 < 0.1:
        修复建议.append(f"补救率 {补救率:.1%} 偏低·建议提高补救加分·鼓励主动修复")

    if 修复建议:
        return ("🟡", 6, "单项警戒·人工眼审+执行修复建议", 修复建议)

    return ("🟢", 7, "三色通行·可微调", [])

# ═══════════════════════════════════════════════════════════════
# 五、健康评分（v3.0 新增·0-100分）
# ═══════════════════════════════════════════════════════════════

def 计算健康评分(数据: dict, 参数: "微调参数") -> Tuple[int, str, dict]:
    """
    综合四维指标输出健康评分。
    返回 (分数, 评级, 分项明细)
    """
    if "样本不足" in 数据.get("状态", ""):
        return (0, "🔘 数据不足", {})

    分项: dict = {}
    总分 = 100

    # 甩锅率 (满分25·超基线扣分)
    甩锅 = 数据.get("甩锅率", 0)
    甩锅基线 = 参数.健康基线_甩锅率上限
    甩锅得分 = max(0, 25 - int((甩锅 / 甩锅基线) * 25)) if 甩锅 <= 甩锅基线 else 0
    分项["甩锅维度"] = 甩锅得分

    # 自扛率 (满分25·低于基线扣分)
    自扛 = 数据.get("自扛率", 0)
    自扛基线 = 参数.健康基线_自扛率下限
    自扛得分 = min(25, int((自扛 / 自扛基线) * 25))
    分项["自扛维度"] = 自扛得分

    # 威胁率 (满分30·威胁率超限重扣)
    威胁 = 数据.get("威胁率", 0)
    威胁基线 = 参数.健康基线_威胁率上限
    威胁得分 = max(0, 30 - int((威胁 / 威胁基线) * 30)) if 威胁 <= 威胁基线 else 0
    分项["威胁维度"] = 威胁得分

    # 补救率 (满分20·低于基线扣分)
    补救 = 数据.get("补救率", 0)
    补救基线 = 参数.健康基线_补救率下限
    补救得分 = min(20, int((补救 / 补救基线) * 20))
    分项["补救维度"] = 补救得分

    总分 = sum(分项.values())

    if 总分 >= 85:
        评级 = "🟢 优秀"
    elif 总分 >= 65:
        评级 = "🟡 合格"
    elif 总分 >= 40:
        评级 = "🟠 警戒"
    else:
        评级 = "🔴 危险"

    return (总分, 评级, 分项)

# ═══════════════════════════════════════════════════════════════
# 六、冷启动保护（v3.0 新增）
# ═══════════════════════════════════════════════════════════════

class 冷启动保护:
    """
    样本不足时用默认参数兜底·不静默失败·明确告知状态。
    """
    @staticmethod
    def 检查(事件数: int, 最小样本: int) -> Tuple[bool, str]:
        if 事件数 < 最小样本:
            缺口 = 最小样本 - 事件数
            return (False, f"冷启动保护·当前{事件数}条·还需{缺口}条才可微调·使用默认参数兜底")
        return (True, "样本充足·可正常微调")

# ═══════════════════════════════════════════════════════════════
# 七、参数漂移检测（v3.0 新增）
# ═══════════════════════════════════════════════════════════════

class 漂移检测器:
    """
    连续N次同向调整触发漂移警告·防止参数单向漂移失控。
    """
    @staticmethod
    def 记录调整(参数: "微调参数", 参数名: str, 方向: str) -> Optional[str]:
        """
        方向: "up" 或 "down"
        返回漂移警告（如触发）或 None
        """
        if 参数名 not in 参数.漂移计数:
            参数.漂移计数[参数名] = {"方向": 方向, "次数": 1}
            return None

        记录 = 参数.漂移计数[参数名]
        if 记录["方向"] == 方向:
            记录["次数"] += 1
        else:
            记录["方向"] = 方向
            记录["次数"] = 1

        if 记录["次数"] >= 参数.漂移阈值_连续次数:
            return (f"⚠️ 漂移警告·{参数名}已连续{记录['次数']}次"
                    f"{'上调' if 方向=='up' else '下调'}·建议人工复核")
        return None

# ═══════════════════════════════════════════════════════════════
# 八、调节器主类 v3.0
# ═══════════════════════════════════════════════════════════════

class 自适应调节器:

    def __init__(
        self,
        账本路径: str = os.path.expanduser("~/.龍魂/規則帳本.jsonl"),
        参数路径: str = os.path.expanduser("~/.龍魂/微調參數.json"),
        历史路径: str = os.path.expanduser("~/.龍魂/微調歷史/"),
        审计路径: str = os.path.expanduser("~/.龍魂/微調審計/"),
        草日志路径: str = os.path.expanduser("~/.龍魂/草日志.md"),
    ):
        self.账本路径 = 账本路径
        self.参数路径 = 参数路径
        self.历史路径 = Path(历史路径)
        self.审计路径 = Path(审计路径)
        self.草日志路径 = Path(草日志路径)
        self.历史路径.mkdir(parents=True, exist_ok=True)
        self.审计路径.mkdir(parents=True, exist_ok=True)

        self.参数 = self._加载参数()
        self.事件列表: List[dict] = self._加载账本()
        self.漂移检 = 漂移检测器()

    # ── 持久化 ────────────────────────────────────────────

    def _加载参数(self) -> 微调参数:
        if os.path.exists(self.参数路径):
            with open(self.参数路径, "r", encoding="utf-8") as f:
                data = json.load(f)
            # 清理旧版遗留字段
            for k in ("熔断_dr_说明", "待审_dr_说明", "分数上下限说明"):
                data.pop(k, None)
            # tuple 字段还原
            for k in ("熔断_dr", "待审_dr"):
                if k in data and isinstance(data[k], list):
                    data[k] = tuple(data[k])
            # v3.0 新字段兼容
            已知字段 = {f.name for f in 微调参数.__dataclass_fields__.values()}
            data = {k: v for k, v in data.items() if k in 已知字段}
            return 微调参数(**data)
        return 微调参数()

    def _计算哈希(self, p: 微调参数) -> str:
        snapshot = asdict(p)
        for k in ("参数哈希", "父哈希", "最后微调时间", "微调记录",
                  "铁律钩子列表", "漂移计数"):
            snapshot.pop(k, None)
        for k, v in list(snapshot.items()):
            if isinstance(v, tuple):
                snapshot[k] = list(v)
        s = json.dumps(snapshot, ensure_ascii=False, sort_keys=True)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

    def _保存参数(self):
        # 备份旧版本
        if os.path.exists(self.参数路径) and self.参数.参数哈希:
            备份名 = (self.历史路径 /
                      f"{self.参数.参数哈希}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(self.参数路径, "r", encoding="utf-8") as 旧:
                备份名.write_text(旧.read(), encoding="utf-8")

        self.参数.父哈希 = self.参数.参数哈希
        self.参数.参数哈希 = self._计算哈希(self.参数)

        Path(self.参数路径).parent.mkdir(parents=True, exist_ok=True)
        with open(self.参数路径, "w", encoding="utf-8") as f:
            data = asdict(self.参数)
            for k in ("熔断_dr", "待审_dr"):
                if isinstance(data.get(k), tuple):
                    data[k] = list(data[k])
            json.dump(data, f, ensure_ascii=False, indent=2)

        log.info(f"参数已落盘·哈希 {self.参数.参数哈希}·父 {self.参数.父哈希}")

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

    # ── 草日志自动入册（v3.0 新增） ───────────────────────

    def _草日志入册(self, 内容: str):
        """每次微调前 prepend 一条记录·永久留痕·抹不掉"""
        时间戳 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        新条目 = f"\n---\n[{时间戳}] {内容}\n"
        已有 = ""
        if self.草日志路径.exists():
            已有 = self.草日志路径.read_text(encoding="utf-8")
        self.草日志路径.write_text(新条目 + 已有, encoding="utf-8")

    # ── 时间窗口判定 ──────────────────────────────────────

    def _在窗口内(self, 事件: dict, 天数: int) -> bool:
        try:
            t = datetime.fromisoformat(事件.get("时间戳", ""))
            return t >= datetime.now() - timedelta(days=天数)
        except Exception:
            return False

    def _在窗口区间(self, 事件: dict, 起天数: int, 止天数: int) -> bool:
        try:
            t = datetime.fromisoformat(事件.get("时间戳", ""))
            now = datetime.now()
            return (now - timedelta(days=起天数)) >= t >= (now - timedelta(days=止天数))
        except Exception:
            return False

    # ── 统计分析 + 趋势 ───────────────────────────────────

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
        }

    def 分析(self) -> dict:
        窗口 = self.参数.观察窗口_天
        窗口事件 = [e for e in self.事件列表 if self._在窗口内(e, 窗口)]

        # v3.0 冷启动保护
        可行, 冷启动消息 = 冷启动保护.检查(len(窗口事件), self.参数.最小样本)
        if not 可行:
            return {
                "状态": "🟡 冷启动保护",
                "冷启动消息": 冷启动消息,
                "样本数": len(窗口事件),
                "最小要求": self.参数.最小样本,
                "兜底行为": "使用默认参数·不微调·不静默失败",
            }

        全段 = self._统计一段(窗口事件)
        半 = 窗口 // 2
        前半 = [e for e in self.事件列表 if self._在窗口区间(e, 半, 窗口)]
        后半 = [e for e in self.事件列表 if self._在窗口区间(e, 0, 半)]
        前 = self._统计一段(前半)
        后 = self._统计一段(后半)

        趋势: dict = {}
        for k in ("甩锅率", "自扛率", "没立正率", "补救率", "威胁率"):
            if k in 前 and k in 后:
                趋势[k] = round(后.get(k, 0) - 前.get(k, 0), 3)

        全段["状态"] = "🟢 足够样本"
        全段["趋势"] = 趋势

        # v3.0 健康评分注入分析结果
        评分, 评级, 分项 = 计算健康评分(全段, self.参数)
        全段["健康评分"] = 评分
        全段["健康评级"] = 评级
        全段["健康分项"] = 分项

        return 全段

    # ── 双向调整 + 滞回 + 漂移检测 ───────────────────────

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
        模拟: bool = True,
    ) -> Tuple[float, Optional[str]]:
        滞回 = self.参数.滞回带

        if 指标值 > 高阈值 + 滞回:
            新值 = round(min(当前值 * (1 + 速率), 硬界[1]), 1)
            if 新值 != 当前值:
                漂移警告 = self.漂移检.记录调整(self.参数, 参数名, "up") if not 模拟 else None
                记录 = f"🔼 {参数名}: {当前值} → {新值} ({方向标签}从严·{指标值:.1%} > {高阈值:.0%})"
                if 漂移警告:
                    记录 += f"\n   {漂移警告}"
                return 新值, 记录

        elif 指标值 < 低阈值 - 滞回:
            新值 = round(max(当前值 * (1 - 速率 * 0.5), 硬界[0]), 1)
            if 新值 != 当前值:
                漂移警告 = self.漂移检.记录调整(self.参数, 参数名, "down") if not 模拟 else None
                记录 = f"🔽 {参数名}: {当前值} → {新值} ({方向标签}放松·{指标值:.1%} < {低阈值:.0%})"
                if 漂移警告:
                    记录 += f"\n   {漂移警告}"
                return 新值, 记录

        return 当前值, None

    # ── 微调主流程 ────────────────────────────────────────

    def 微调(self, 模拟: bool = True) -> dict:
        数据 = self.分析()

        # 冷启动保护
        if "冷启动保护" in 数据.get("状态", ""):
            return {"状态": "跳过", "原因": 数据.get("冷启动消息"), "数据": 数据}

        色, dr, dr说明, 修复建议 = 三色_dr(数据)

        # v3.0 铁律钩子执行
        铁律阻断 = 执行铁律钩子(self.参数, 数据)
        if 铁律阻断:
            return {
                "状态": "🔴 铁律熔断·拒绝微调",
                "铁律阻断": 铁律阻断,
                "三色": "🔴", "dr": 9,
                "数据": 数据,
            }

        # 🔴 三色熔断
        if 色 == "🔴":
            return {
                "状态": "🔴 熔断·拒绝微调",
                "三色": 色, "dr": dr, "dr说明": dr说明,
                "数据": 数据, "调整数": 0, "调整记录": [],
                "修复建议": 修复建议,
            }

        调整记录: List[str] = []
        速率 = self.参数.学习率

        # ── R1 责任承担 ──
        for 参数名, 指标键, 高, 低, 标签 in [
            ("逃避扣分",  "甩锅率",  0.5, 0.15, "甩锅"),
            ("自扛加分",  "自扛率",  0.8, 0.3,  "自扛奖励"),
        ]:
            当前 = getattr(self.参数, 参数名)
            新值, 记录 = self._双向调整(
                当前, 数据[指标键], 高, 低,
                参数硬界[参数名], 速率 if "扣" in 参数名 else 速率 * 0.5,
                参数名, 标签, 模拟
            )
            if 记录:
                调整记录.append(记录)
                if not 模拟:
                    setattr(self.参数, 参数名, 新值)

        # ── R2 批评姿态 ──
        当前 = self.参数.没立正扣分
        新值, 记录 = self._双向调整(
            当前, 数据["没立正率"], 0.4, 0.1,
            参数硬界["没立正扣分"], 速率, "没立正扣分", "没立正", 模拟
        )
        if 记录:
            调整记录.append(记录)
            if not 模拟:
                self.参数.没立正扣分 = 新值

        # ── R5 补救 ──
        当前 = self.参数.补救加分
        新值, 记录 = self._双向调整(
            当前, 数据["补救率"], 0.3, 0.05,
            参数硬界["补救加分"], 速率 * 0.5, "补救加分", "补救奖励", 模拟
        )
        if 记录:
            调整记录.append(记录)
            if not 模拟:
                self.参数.补救加分 = 新值

        # ── 趋势警告 ──
        趋势 = 数据.get("趋势", {})
        趋势消息 = []
        if 趋势.get("甩锅率", 0) > 0.1:
            趋势消息.append(f"📈 甩锅率上升 {趋势['甩锅率']:+.1%}·建议人工介入")
        if 趋势.get("自扛率", 0) > 0.1:
            趋势消息.append(f"📈 自扛率上升 {趋势['自扛率']:+.1%}·习惯在养成")
        if 趋势.get("威胁率", 0) > 0.05:
            趋势消息.append(f"🚨 威胁率上升 {趋势['威胁率']:+.1%}·高优先级警告")

        # ── 落盘 ──
        if not 模拟 and 调整记录:
            ts = datetime.now().isoformat()
            self.参数.最后微调时间 = ts
            self.参数.微调记录.append({
                "时间": ts,
                "三色": 色, "dr": dr,
                "调整": [r for r in 调整记录],
                "趋势消息": 趋势消息,
                "修复建议": 修复建议,
                "父哈希": self.参数.参数哈希,
                "健康评分": 数据.get("健康评分", 0),
            })
            self._保存参数()
            # v3.0 草日志自动入册
            self._草日志入册(
                f"微调落盘·三色{色}·dr={dr}·调整{len(调整记录)}项·"
                f"哈希{self.参数.参数哈希}·健康{数据.get('健康评分',0)}分"
            )

        return {
            "状态": ("🟢 微调完成" if (调整记录 and not 模拟) else
                    "🟡 模拟态·未落盘" if (调整记录 and 模拟) else
                    "🟢 无需调整"),
            "三色": 色, "dr": dr, "dr说明": dr说明,
            "调整数": len(调整记录),
            "调整记录": 调整记录,
            "趋势消息": 趋势消息,
            "修复建议": 修复建议,
            "数据": 数据,
            "模拟": 模拟,
            "参数哈希": self.参数.参数哈希,
            "父哈希": self.参数.父哈希,
            "健康评分": 数据.get("健康评分", 0),
            "健康评级": 数据.get("健康评级", "—"),
        }

    # ── 回滚 ─────────────────────────────────────────────

    def 回滚(self) -> dict:
        if not self.参数.父哈希:
            return {"状态": "🟡 无父代·无法回滚"}

        if self.参数.最后微调时间:
            try:
                上次 = datetime.fromisoformat(self.参数.最后微调时间)
                剩余 = self.参数.回滚冷却_天 - (datetime.now() - 上次).days
                if 剩余 > 0:
                    return {"状态": f"🟡 冷却期内·剩余 {剩余} 天"}
            except Exception:
                pass

        候选 = list(self.历史路径.glob(f"{self.参数.父哈希}_*.json"))
        if not 候选:
            return {"状态": "🔴 父代备份缺失·无法回滚", "父哈希": self.参数.父哈希}

        最新 = sorted(候选)[-1]
        with open(最新, "r", encoding="utf-8") as f:
            旧 = json.load(f)
            for k in ("熔断_dr", "待审_dr"):
                if k in 旧 and isinstance(旧[k], list):
                    旧[k] = tuple(旧[k])
            已知字段 = {f.name for f in 微调参数.__dataclass_fields__.values()}
            旧 = {k: v for k, v in 旧.items() if k in 已知字段}
            self.参数 = 微调参数(**旧)

        self._保存参数()
        self._草日志入册(f"回滚完成·恢复到 {self.参数.父哈希}")
        return {
            "状态": "🟢 回滚完成",
            "回滚到": str(最新.name),
            "当前哈希": self.参数.参数哈希,
        }

    # ── 健康评分快捷入口 ──────────────────────────────────

    def 健康报告(self) -> dict:
        数据 = self.分析()
        if "冷启动" in 数据.get("状态", ""):
            return {"状态": "🔘 数据不足", "消息": 数据.get("冷启动消息")}
        评分, 评级, 分项 = 计算健康评分(数据, self.参数)
        return {
            "健康评分": 评分,
            "健康评级": 评级,
            "分项明细": 分项,
            "数据快照": {k: v for k, v in 数据.items()
                        if k not in ("状态", "趋势", "健康评分", "健康评级", "健康分项")},
        }

    # ── Web仪表板JSON导出（v3.0 新增） ───────────────────

    def web导出(self) -> dict:
        """输出完整JSON·供浏览器操作台消费"""
        数据 = self.分析()
        评分, 评级, 分项 = 计算健康评分(数据, self.参数)
        色, dr, dr说明, 修复建议 = 三色_dr(数据)
        参数快照 = asdict(self.参数)
        for k in ("熔断_dr", "待审_dr"):
            if isinstance(参数快照.get(k), tuple):
                参数快照[k] = list(参数快照[k])

        return {
            "meta": {
                "版本": "v3.0",
                "时间": datetime.now().isoformat(),
                "DNA": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-WEB-EXPORT-v3.0",
            },
            "健康": {"评分": 评分, "评级": 评级, "分项": 分项},
            "三色": {"颜色": 色, "dr": dr, "说明": dr说明, "修复建议": 修复建议},
            "数据": 数据,
            "参数": 参数快照,
            "哈希链": {
                "当前": self.参数.参数哈希,
                "父代": self.参数.父哈希,
            },
            "微调历史_最近5次": self.参数.微调记录[-5:],
        }

    # ── 查看参数 ──────────────────────────────────────────

    def 查看参数(self) -> dict:
        d = asdict(self.参数)
        for k in ("熔断_dr", "待审_dr"):
            if isinstance(d.get(k), tuple):
                d[k] = list(d[k])
        d["_焊死字段"] = [
            "熔断_dr", "待审_dr", "分数上限", "分数下限",
            "威胁归零开关", "威胁触发分数"
        ]
        return d

    # ── Markdown 审计报告 ─────────────────────────────────

    def 生成审计报告(self, 微调结果: dict) -> Path:
        今日 = datetime.now().strftime("%Y-%m-%d")
        时分 = datetime.now().strftime("%H%M%S")
        路径 = self.审计路径 / f"{今日}_{时分}.md"

        数据 = 微调结果.get("数据", {})
        趋势 = 数据.get("趋势", {})
        色 = 微调结果.get("三色", "🟡")
        dr = 微调结果.get("dr", 6)
        评分 = 微调结果.get("健康评分", 0)
        评级 = 微调结果.get("健康评级", "—")

        md = [
            f"# 龍魂·自适应微调审计 v3.0 · {今日}",
            "",
            f"- **DNA**: #龍芯⚡️{datetime.now().strftime('%Y%m%d-%H%M%S')}-TUNE-AUDIT-v3.0",
            f"- **GPG**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
            f"- **CONFIRM**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            f"- **三色**: {色} · dr={dr} · {微调结果.get('dr说明','')}",
            f"- **健康评分**: {评分}/100 · {评级}",
            f"- **状态**: {微调结果.get('状态','')}",
            f"- **模拟**: {微调结果.get('模拟', True)}",
            f"- **参数哈希**: `{微调结果.get('参数哈希','')}`",
            f"- **父哈希**: `{微调结果.get('父哈希','')}`",
            "",
            "## 数据快照",
        ]
        for k, v in 数据.items():
            if k in ("状态", "趋势", "健康评分", "健康评级", "健康分项"):
                continue
            md.append(f"- {k}: {v}")

        if 趋势:
            md += ["", "## 趋势（后半段 − 前半段）"]
            for k, v in 趋势.items():
                箭 = "📈" if v > 0 else "📉" if v < 0 else "➖"
                md.append(f"- {箭} {k}: {v:+.3f}")

        md += ["", "## 调整记录"]
        for r in 微调结果.get("调整记录", []) or ["（无调整）"]:
            md.append(f"- {r}")

        修复 = 微调结果.get("修复建议", [])
        if 修复:
            md += ["", "## 修复建议（v3.0）"]
            for r in 修复:
                md.append(f"- {r}")

        趋势消息 = 微调结果.get("趋势消息", [])
        if 趋势消息:
            md += ["", "## 趋势消息"]
            for r in 趋势消息:
                md.append(f"- {r}")

        md += [
            "",
            "---",
            "责任：UID9622·不免责·永久有效",
            "SEAL: #ZHUGEXIN⚡️2025-DEVICE-BIND-SOUL",
        ]

        路径.write_text("\n".join(md), encoding="utf-8")
        log.info(f"审计报告已落: {路径}")
        return 路径

# ═══════════════════════════════════════════════════════════════
# 九、CLI 入口
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="龍魂·自适应微调参数系统 v3.0")
    parser.add_argument("--status",     action="store_true", help="查看参数 + 哈希链 + 健康评分")
    parser.add_argument("--analyze",    action="store_true", help="数据分析 + 趋势 + 修复建议")
    parser.add_argument("--simulate",   action="store_true", help="模拟微调（安全模式）")
    parser.add_argument("--apply",      action="store_true", help="真正落盘微调")
    parser.add_argument("--rollback",   action="store_true", help="回滚到上一代参数")
    parser.add_argument("--audit",      action="store_true", help="生成 Markdown 审计报告")
    parser.add_argument("--health",     action="store_true", help="仅输出健康评分")
    parser.add_argument("--web-export", action="store_true", help="导出 JSON 供操作台消费")
    parser.add_argument("--demo",       action="store_true", help="完整演示")
    args = parser.parse_args()

    调节器 = 自适应调节器()

    if args.status:
        print("\n📊 参数状态 v3.0：")
        for k, v in 调节器.查看参数().items():
            if k in ("微调记录", "漂移计数", "铁律钩子列表"):
                continue
            print(f"   {k}: {v}")
        h = 调节器.健康报告()
        print(f"\n💊 健康评分: {h.get('健康评分',0)}/100 · {h.get('健康评级','—')}")
        print(f"🔗 哈希: {调节器.参数.参数哈希 or '未初始化'} → 父: {调节器.参数.父哈希 or '无'}")
        return

    if args.analyze:
        print("\n📈 分析 + 趋势 + 修复建议：")
        数据 = 调节器.分析()
        for k, v in 数据.items():
            print(f"   {k}: {v}")
        色, dr, 说明, 修复 = 三色_dr(数据)
        print(f"\n🚦 三色: {色} dr={dr} · {说明}")
        if 修复:
            print("\n🔧 修复建议：")
            for r in 修复:
                print(f"   · {r}")
        return

    if args.health:
        h = 调节器.健康报告()
        print(json.dumps(h, ensure_ascii=False, indent=2))
        return

    if args.web_export:
        print(json.dumps(调节器.web导出(), ensure_ascii=False, indent=2))
        return

    if args.rollback:
        print("\n⏪ 回滚...")
        结果 = 调节器.回滚()
        for k, v in 结果.items():
            print(f"   {k}: {v}")
        return

    结果 = None
    if args.apply:
        print("\n🔧 落盘微调（--apply）...")
        结果 = 调节器.微调(模拟=False)
    elif args.simulate or not args.demo:
        print("\n🔍 模拟微调（安全模式）...")
        结果 = 调节器.微调(模拟=True)

    if 结果 is not None:
        print(f"\n📊 {结果['状态']}")
        print(f"🚦 {结果.get('三色','?')} dr={结果.get('dr','?')} · {结果.get('dr说明','')}")
        print(f"💊 健康: {结果.get('健康评分',0)}/100 · {结果.get('健康评级','—')}")
        for r in 结果.get("调整记录", []) or ["  （无调整）"]:
            print(f"   {r}")
        if 结果.get("修复建议"):
            print("\n🔧 修复建议：")
            for r in 结果["修复建议"]:
                print(f"   · {r}")
        if args.audit or args.apply:
            报告 = 调节器.生成审计报告(结果)
            print(f"\n📝 审计报告: {报告}")
        return

    if args.demo:
        print("\n🐉 龍魂·自适应微调参数系统 v3.0 完整演示\n" + "═" * 60)
        数据 = 调节器.分析()
        print("📈 分析结果：")
        for k, v in 数据.items():
            print(f"   {k}: {v}")
        结果 = 调节器.微调(模拟=True)
        print(f"\n🔍 模拟结果: {结果['状态']}")
        报告 = 调节器.生成审计报告(结果)
        print(f"📝 审计报告: {报告}")
        print(f"💊 健康: {结果.get('健康评分',0)}/100 · {结果.get('健康评级','—')}")


if __name__ == "__main__":
    main()
