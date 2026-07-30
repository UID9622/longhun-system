#!/usr/bin/env python3
#龍芯⚡️2026-06-29-CNSH-FLOWFIELD-UID9622
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
CNSH 流场可视化引擎 v1.0
核心理念：粒子 = DNA · 每个决策步骤都是可见粒子
目标：AI 决策全透明、可审计、无黑箱、不失忆
DNA: #龍芯⚡️2026-06-29-CNSH-FLOWFIELD-UID9622
"""

import json
import mimetypes
import re
import secrets
import sys
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set

sys.path.insert(0, str(Path(__file__).parent))
from CNSH_国密工具 import SM3
from CNSH_颜色不动点协议 import CNSH_颜色不动点协议


@dataclass
class 流场粒子:
    粒子ID: str
    名称: str
    类型: str           # file / decision / dna / module / person
    来源路径: str
    DNA: List[str] = field(default_factory=list)
    ParentDNA: List[str] = field(default_factory=list)
    SM3哈希: str = ""
    元数据: Dict[str, Any] = field(default_factory=dict)
    子粒子: List[str] = field(default_factory=list)
    父粒子: List[str] = field(default_factory=list)
    时间戳: str = ""
    透明度评分: float = 1.0  # 1.0 = 全透明，0.0 = 黑箱
    颜色: str = "G"          # 颜色不动点：G/Y/R/K/P/B/AU


class CNSH_流场可视化引擎:
    """
    把龍魂生态中的一切创作、决策、DNA 都变成流场中的粒子。
    每个粒子可追溯、可校验、可点击审计。
    """

    DNA模式 = re.compile(r"#龍芯⚡️[^\s\n]+")
    ParentDNA模式 = re.compile(r"(?:parent_dna|parentDNA|父DNA|上游DNA)[:：]?\s*#龍芯⚡️[^\s\n]+", re.IGNORECASE)

    def __init__(self, 根目录: str = "/Users/zuimeidedeyihan/龍魂待整理/02-流场可视化"):
        self.根目录 = Path(根目录)
        self.粒子库: Dict[str, 流场粒子] = {}
        self.决策粒子库: Dict[str, 流场粒子] = {}
        self.关系网: List[Dict[str, str]] = []
        self.颜色协议 = CNSH_颜色不动点协议()

    # ============== 1. 扫描文件，每个文件 = 一个粒子 = 一个 DNA 载体 ==============
    def 扫描文件粒子(self) -> int:
        """扫描目录下所有文件，每个文件生成一个流场粒子。"""
        if not self.根目录.exists():
            return 0

        计数 = 0
        for 路径 in self.根目录.rglob("*"):
            if 路径.is_file() and 路径.stat().st_size < 5 * 1024 * 1024:  # 跳过超过 5MB
                try:
                    内容 = 路径.read_text(encoding="utf-8", errors="replace")
                except Exception:
                    continue

                DNA列表 = self.DNA模式.findall(内容)
                ParentDNA列表 = []
                for m in self.ParentDNA模式.finditer(内容):
                    ParentDNA列表.extend(self.DNA模式.findall(m.group()))

                相对路径 = str(路径.relative_to(self.根目录))
                内容哈希 = SM3.hex_hash(内容)
                粒子ID = f"FILE-{SM3.hex_hash(相对路径)[:16].upper()}"
                颜色报告 = self.颜色协议.生成报告(内容[:2000])  # 只检测前2000字符，控制性能

                粒子 = 流场粒子(
                    粒子ID=粒子ID,
                    名称=路径.name,
                    类型="file",
                    来源路径=相对路径,
                    DNA=DNA列表,
                    ParentDNA=ParentDNA列表,
                    SM3哈希=内容哈希,
                    元数据={
                        "大小": 路径.stat().st_size,
                        "MIME": mimetypes.guess_type(str(路径))[0] or "unknown",
                        "扩展名": 路径.suffix,
                        "颜色": 颜色报告["主色"],
                        "颜色名": 颜色报告["颜色名"],
                        "颜色含义": 颜色报告["含义"],
                        "颜色原因": 颜色报告["原因"],
                    },
                    时间戳=datetime.fromtimestamp(路径.stat().st_mtime, tz=timezone.utc).isoformat(),
                    透明度评分=1.0 if DNA列表 else 0.5,  # 无 DNA 则半透明
                    颜色=颜色报告["主色"],
                )
                self.粒子库[粒子ID] = 粒子
                计数 += 1

        self._建立文件关系()
        return 计数

    def _建立文件关系(self):
        """根据 ParentDNA 建立父子关系。"""
        # DNA → 粒子ID 映射
        dna_to_particle: Dict[str, List[str]] = {}
        for pid, p in self.粒子库.items():
            for dna in p.DNA:
                dna_to_particle.setdefault(dna, []).append(pid)

        for pid, p in self.粒子库.items():
            for parent_dna in p.ParentDNA:
                for parent_pid in dna_to_particle.get(parent_dna, []):
                    if parent_pid != pid:
                        p.父粒子.append(parent_pid)
                        self.粒子库[parent_pid].子粒子.append(pid)
                        self.关系网.append({
                            "源": parent_pid,
                            "目标": pid,
                            "关系": "parent-of",
                            "DNA": parent_dna,
                        })

    # ============== 2. AI 决策过程透明化：每个决策步骤 = 一个粒子 ==============
    def 添加决策粒子(self, 决策名: str, 步骤列表: List[Dict[str, Any]]) -> str:
        """
        把 AI 决策过程变成一串可见粒子。
        步骤列表: [{"步骤": 1, "动作": "...", "输入": "...", "输出": "..."}, ...]
        """
        决策根ID = f"DECISION-{SM3.hex_hash(决策名 + datetime.now(timezone.utc).isoformat())[:16].upper()}"

        上一个粒子ID = None
        for idx, 步骤 in enumerate(步骤列表, 1):
            步骤名 = 步骤.get("动作", f"步骤{idx}")
            步骤DNA = self._生成决策DNA(决策名, idx, 步骤名)
            粒子ID = f"{决策根ID}-STEP{idx}"
            输入哈希 = SM3.hex_hash(json.dumps(步骤.get("输入", ""), sort_keys=True, ensure_ascii=False))
            输出哈希 = SM3.hex_hash(json.dumps(步骤.get("输出", ""), sort_keys=True, ensure_ascii=False))
            步骤文本 = f"{步骤.get('输入', '')} {步骤.get('输出', '')}"
            颜色报告 = self.颜色协议.生成报告(步骤文本[:1000])

            粒子 = 流场粒子(
                粒子ID=粒子ID,
                名称=f"{决策名} · {步骤名}",
                类型="decision",
                来源路径=f"决策链/{决策名}",
                DNA=[步骤DNA],
                SM3哈希=SM3.hex_hash(f"{输入哈希}-{输出哈希}"),
                元数据={
                    "决策名": 决策名,
                    "步骤号": idx,
                    "动作": 步骤名,
                    "输入SM3": 输入哈希,
                    "输出SM3": 输出哈希,
                    "三色": 步骤.get("三色", "🟢"),
                    "颜色": 颜色报告["主色"],
                    "颜色名": 颜色报告["颜色名"],
                    "颜色含义": 颜色报告["含义"],
                },
                时间戳=datetime.now(timezone.utc).isoformat(),
                透明度评分=1.0,
                颜色=颜色报告["主色"],
            )

            if 上一个粒子ID:
                粒子.父粒子.append(上一个粒子ID)
                self.决策粒子库[上一个粒子ID].子粒子.append(粒子ID)
                self.关系网.append({
                    "源": 上一个粒子ID,
                    "目标": 粒子ID,
                    "关系": "next-step",
                    "DNA": 步骤DNA,
                })

            self.决策粒子库[粒子ID] = 粒子
            上一个粒子ID = 粒子ID

        return 决策根ID

    def _生成决策DNA(self, 决策名: str, 步骤: int, 动作: str) -> str:
        时间戳 = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        熵 = secrets.token_hex(4).upper()
        短哈希 = SM3.hex_hash(f"{决策名}-{步骤}-{动作}-{时间戳}-{熵}")[:16].upper()
        return f"#龍芯⚡️{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-DECISION-{决策名[:10].upper()}-STEP{步骤}-{短哈希}-ENTROPY{熵}-UID9622"

    # ============== 3. 透明审计：点击任一粒子，输出完整来源链 ==============
    def 审计粒子(self, 粒子ID: str) -> Dict[str, Any]:
        粒子 = self.粒子库.get(粒子ID) or self.决策粒子库.get(粒子ID)
        if not 粒子:
            return {"ok": False, "reason": "PARTICLE_NOT_FOUND"}

        def 追溯上游(pid: str, 深度: int = 0) -> List[Dict[str, Any]]:
            if 深度 > 10:
                return [{"粒子ID": pid, "说明": "追溯深度超过10层，停止"}]
            p = self.粒子库.get(pid) or self.决策粒子库.get(pid)
            if not p:
                return []
            链 = [{"粒子ID": pid, "名称": p.名称, "DNA": p.DNA, "SM3": p.SM3哈希}]
            for 父ID in p.父粒子:
                链.extend(追溯上游(父ID, 深度 + 1))
            return 链

        def 追踪下游(pid: str, 深度: int = 0) -> List[Dict[str, Any]]:
            if 深度 > 10:
                return [{"粒子ID": pid, "说明": "追踪深度超过10层，停止"}]
            p = self.粒子库.get(pid) or self.决策粒子库.get(pid)
            if not p:
                return []
            链 = [{"粒子ID": pid, "名称": p.名称, "DNA": p.DNA, "SM3": p.SM3哈希}]
            for 子ID in p.子粒子:
                链.extend(追踪下游(子ID, 深度 + 1))
            return 链

        return {
            "ok": True,
            "粒子": {
                "粒子ID": 粒子.粒子ID,
                "名称": 粒子.名称,
                "类型": 粒子.类型,
                "来源路径": 粒子.来源路径,
                "DNA": 粒子.DNA,
                "ParentDNA": 粒子.ParentDNA,
                "SM3哈希": 粒子.SM3哈希,
                "元数据": 粒子.元数据,
                "透明度评分": 粒子.透明度评分,
            },
            "上游来源链": 追溯上游(粒子ID)[1:],  # 去掉自己
            "下游影响链": 追踪下游(粒子ID)[1:],
            "关系总数": len(粒子.父粒子) + len(粒子.子粒子),
        }

    # ============== 4. 生成流场可视化数据 ==============
    def 生成流场数据(self, 输出路径: str = "./CNSH_流场数据.json") -> Path:
        所有粒子 = {**self.粒子库, **self.决策粒子库}
        数据 = {
            "meta": {
                "生成时间": datetime.now(timezone.utc).isoformat(),
                "粒子总数": len(所有粒子),
                "文件粒子": len(self.粒子库),
                "决策粒子": len(self.决策粒子库),
                "关系总数": len(self.关系网),
                "DNA": "#龍芯⚡️2026-06-29-CNSH-FLOWFIELD-UID9622",
            },
            "nodes": [
                {
                    "id": p.粒子ID,
                    "name": p.名称,
                    "type": p.类型,
                    "path": p.来源路径,
                    "dna": p.DNA,
                    "sm3": p.SM3哈希,
                    "transparency": p.透明度评分,
                    "color": p.颜色,
                    "metadata": p.元数据,
                }
                for p in 所有粒子.values()
            ],
            "links": self.关系网,
        }
        路径 = Path(输出路径)
        with open(路径, "w", encoding="utf-8") as f:
            json.dump(数据, f, ensure_ascii=False, indent=2)
        return 路径

    def 生成透明度报告(self) -> str:
        所有粒子 = {**self.粒子库, **self.决策粒子库}
        不透明 = [p for p in 所有粒子.values() if p.透明度评分 < 1.0]
        黑箱 = [p for p in 所有粒子.values() if p.透明度评分 == 0.0]
        颜色统计 = {}
        for p in 所有粒子.values():
            颜色统计[p.颜色] = 颜色统计.get(p.颜色, 0) + 1

        行 = []
        行.append("╔" + "═" * 58 + "╗")
        行.append("║" + " " * 14 + "CNSH 流场透明度报告" + " " * 23 + "║")
        行.append("╠" + "═" * 58 + "╣")
        行.append(f"║ 总粒子数: {len(所有粒子):<47} ║")
        行.append(f"║ 全透明: {len(所有粒子) - len(不透明):<49} ║")
        行.append(f"║ 半透明/缺DNA: {len(不透明):<43} ║")
        行.append(f"║ 黑箱: {len(黑箱):<50} ║")
        行.append("╠" + "═" * 58 + "╣")
        行.append("║ 颜色分布: " + ", ".join(f"{k}:{v}" for k, v in sorted(颜色统计.items())))
        行[-1] += " " * (58 - len(行[-1]) - 1) + "║"
        if 不透明:
            行.append("╠" + "═" * 58 + "╣")
            行.append("║ 需补 DNA 的粒子:")
            行[-1] += " " * (58 - len(行[-1]) - 1) + "║"
            for p in 不透明[:5]:
                行.append(f"║   · {p.名称[:46]:<46} ║")
        行.append("╚" + "═" * 58 + "╝")
        return "\n".join(行)


# ============== P0: 实时流场监控 ==============
class 流场监控器:
    """后台守护，持续扫描目录，新粒子自动入库。"""

    def __init__(self, 引擎: CNSH_流场可视化引擎, 间隔秒: int = 5, 回调: Optional[Callable] = None):
        self.引擎 = 引擎
        self.间隔 = 间隔秒
        self.回调 = 回调 or (lambda 事件, 数据: None)
        self._运行中 = False
        self._线程: Optional[threading.Thread] = None
        self._已知路径: Set[str] = set()
        self.事件日志: List[Dict[str, Any]] = []

    def 启动(self):
        if self._运行中:
            return
        self._运行中 = True
        self._线程 = threading.Thread(target=self._循环, daemon=True)
        self._线程.start()
        self._记录事件("监控启动", {})

    def 停止(self):
        self._运行中 = False
        if self._线程:
            self._线程.join(timeout=self.间隔 + 1)
        self._记录事件("监控停止", {})

    def _循环(self):
        while self._运行中:
            try:
                self._扫描一次()
            except Exception as e:
                self._记录事件("扫描异常", {"错误": str(e)})
            time.sleep(self.间隔)

    def _扫描一次(self):
        之前数量 = len(self._已知路径)
        self.引擎.扫描文件粒子()
        当前路径 = {p.来源路径 for p in self.引擎.粒子库.values()}
        新增 = 当前路径 - self._已知路径
        删除 = self._已知路径 - 当前路径
        self._已知路径 = 当前路径

        if 新增:
            self._记录事件("新增粒子", {"数量": len(新增), "路径": list(新增)})
            self.回调("新增粒子", list(新增))
        if 删除:
            self._记录事件("粒子消失", {"数量": len(删除), "路径": list(删除)})
            self.回调("粒子消失", list(删除))

    def _记录事件(self, 类型: str, 数据: Dict[str, Any]):
        self.事件日志.append({
            "时间": datetime.now(timezone.utc).isoformat(),
            "类型": 类型,
            "数据": 数据,
        })


# ============== P1: 异常粒子隔离 ==============
class 粒子隔离区:
    """黑箱/半透明粒子先隔离，再审查，不直接删。"""

    def __init__(self, 工作目录: str = "./CNSH_流场隔离区"):
        self.工作目录 = Path(工作目录)
        self.工作目录.mkdir(parents=True, exist_ok=True)
        self.隔离库: Dict[str, Dict[str, Any]] = {}
        self._加载()

    def _加载(self):
        路径 = self.工作目录 / "隔离记录.json"
        if 路径.exists():
            with open(路径, "r", encoding="utf-8") as f:
                self.隔离库 = json.load(f)

    def _保存(self):
        路径 = self.工作目录 / "隔离记录.json"
        with open(路径, "w", encoding="utf-8") as f:
            json.dump(self.隔离库, f, ensure_ascii=False, indent=2)

    def 隔离(self, 粒子: 流场粒子, 原因: str) -> str:
        凭证 = f"QUARANTINE-{secrets.token_hex(8).upper()}"
        self.隔离库[凭证] = {
            "凭证": 凭证,
            "粒子ID": 粒子.粒子ID,
            "名称": 粒子.名称,
            "来源路径": 粒子.来源路径,
            "原因": 原因,
            "透明度评分": 粒子.透明度评分,
            "隔离时间": datetime.now(timezone.utc).isoformat(),
            "状态": "待审查",
        }
        self._保存()
        return 凭证

    def 审查(self, 凭证: str,  verdict: str, 备注: str = "") -> Dict[str, Any]:
        if 凭证 not in self.隔离库:
            return {"ok": False, "reason": "凭证不存在"}
        记录 = self.隔离库[凭证]
        记录["状态"] = verdict
        记录["审查时间"] = datetime.now(timezone.utc).isoformat()
        记录["备注"] = 备注
        self._保存()
        return {"ok": True, "记录": 记录}

    def 列表(self) -> List[Dict[str, Any]]:
        return list(self.隔离库.values())

    def 统计(self) -> Dict[str, int]:
        状态 = {}
        for r in self.隔离库.values():
            状态[r["状态"]] = 状态.get(r["状态"], 0) + 1
        return {"总数": len(self.隔离库), **状态}


# ============== P2: 流场健康度 ==============
class 流场健康度:
    """给整个流场打分，0-100。"""

    def __init__(self, 引擎: CNSH_流场可视化引擎):
        self.引擎 = 引擎

    def 计算(self) -> Dict[str, Any]:
        所有粒子 = {**self.引擎.粒子库, **self.引擎.决策粒子库}
        总数 = len(所有粒子)
        if 总数 == 0:
            return {"总分": 0, "说明": "流场为空"}

        透明数 = sum(1 for p in 所有粒子.values() if p.透明度评分 >= 1.0)
        半透明数 = sum(1 for p in 所有粒子.values() if 0.0 < p.透明度评分 < 1.0)
        黑箱数 = sum(1 for p in 所有粒子.values() if p.透明度评分 <= 0.0)

        透明度 = round(透明数 / 总数 * 100, 2)
        完整性 = round(sum(len(p.DNA) for p in 所有粒子.values()) / max(总数, 1), 2)
        活跃度 = self._计算活跃度()

        # 颜色风险：🔴红线粒子直接拉低健康度
        红线数 = sum(1 for p in 所有粒子.values() if p.颜色 == "R")
        隐私数 = sum(1 for p in 所有粒子.values() if p.颜色 == "K")
        外部数 = sum(1 for p in 所有粒子.values() if p.颜色 == "P")
        颜色风险分 = max(0, 100 - (红线数 * 20 + 隐私数 * 10 + 外部数 * 5))

        # 总分加权：透明度 40% + 完整性 25% + 活跃度 15% + 颜色安全 20%
        总分 = round(
            透明度 * 0.4
            + min(完整性 * 20, 100) * 0.25
            + 活跃度 * 0.15
            + 颜色风险分 * 0.2,
            2,
        )

        风险点 = []
        if 半透明数 > 0:
            风险点.append(f"{半透明数} 个半透明粒子缺 DNA")
        if 黑箱数 > 0:
            风险点.append(f"{黑箱数} 个黑箱粒子")
        if 红线数 > 0:
            风险点.append(f"{红线数} 个 🔴 红线粒子")
        if 隐私数 > 0:
            风险点.append(f"{隐私数} 个 ⚫ 隐私粒子")
        if 外部数 > 0:
            风险点.append(f"{外部数} 个 🟣 外部输入粒子")

        建议 = []
        if 半透明数 > 0:
            建议.append("对半透明粒子补全 DNA 或隔离审查")
        if 黑箱数 > 0:
            建议.append("立即隔离黑箱粒子，查明来源")
        if 红线数 > 0:
            建议.append("立即审查 🔴 红线粒子并触发护盾")
        if 隐私数 > 0:
            建议.append("对 ⚫ 隐私粒子做脱敏处理")
        if 外部数 > 0:
            建议.append("对 🟣 外部输入粒子做隔离验证")

        return {
            "总分": 总分,
            "透明度": 透明度,
            "完整性": round(min(完整性 * 20, 100), 2),
            "活跃度": 活跃度,
            "颜色安全": 颜色风险分,
            "统计": {
                "总数": 总数,
                "透明": 透明数,
                "半透明": 半透明数,
                "黑箱": 黑箱数,
                "🔴红线": 红线数,
                "⚫隐私": 隐私数,
                "🟣外部输入": 外部数,
            },
            "风险点": 风险点,
            "建议": 建议,
        }

    def _计算活跃度(self) -> float:
        所有粒子 = {**self.引擎.粒子库, **self.引擎.决策粒子库}
        if not 所有粒子:
            return 0.0
        现在 = datetime.now(timezone.utc).timestamp()
        近期数 = 0
        for p in 所有粒子.values():
            try:
                t = datetime.fromisoformat(p.时间戳).timestamp()
                if 现在 - t < 7 * 24 * 3600:  # 7 天内
                    近期数 += 1
            except Exception:
                continue
        return round(近期数 / len(所有粒子) * 100, 2)


# ============== P3: 关系图谱 ==============
class 关系图谱:
    """把粒子上下游变成图结构，可查询、可渲染。"""

    def __init__(self, 引擎: CNSH_流场可视化引擎):
        self.引擎 = 引擎

    def 查询影响链(self, 粒子ID: str, 深度: int = 3) -> List[Dict[str, Any]]:
        return self._遍历(粒子ID, "下游", 深度)

    def 查询依赖链(self, 粒子ID: str, 深度: int = 3) -> List[Dict[str, Any]]:
        return self._遍历(粒子ID, "上游", 深度)

    def _遍历(self, 起点ID: str, 方向: str, 最大深度: int) -> List[Dict[str, Any]]:
        结果 = []
        已访问 = {起点ID}
        队列 = [(起点ID, 0)]
        while 队列:
            当前ID, 深度 = 队列.pop(0)
            if 深度 > 最大深度:
                continue
            p = self.引擎.粒子库.get(当前ID) or self.引擎.决策粒子库.get(当前ID)
            if not p:
                continue
            结果.append({"深度": 深度, "粒子ID": 当前ID, "名称": p.名称, "DNA": p.DNA})
            下一层 = p.子粒子 if 方向 == "下游" else p.父粒子
            for 下一ID in 下一层:
                if 下一ID not in 已访问:
                    已访问.add(下一ID)
                    队列.append((下一ID, 深度 + 1))
        return 结果

    def 渲染Mermaid(self, 中心粒子ID: str, 深度: int = 2) -> str:
        依赖 = self.查询依赖链(中心粒子ID, 深度)
        影响 = self.查询影响链(中心粒子ID, 深度)
        所有 = {p["粒子ID"]: p for p in (依赖 + 影响)}
        p0 = self.引擎.粒子库.get(中心粒子ID) or self.引擎.决策粒子库.get(中心粒子ID)
        if p0:
            所有[中心粒子ID] = {"粒子ID": 中心粒子ID, "名称": p0.名称}

        行 = ["graph TD"]
        for pid, info in 所有.items():
            标签 = info["名称"].replace('"', '')
            行.append(f'  {pid}["{标签}"]')

        # 关系边
        for link in self.引擎.关系网:
            if link["源"] in 所有 and link["目标"] in 所有:
                行.append(f'  {link["源"]} -->|{link.get("关系", "")}| {link["目标"]}')

        return "\n".join(行)


# ============== 演示 ==============
if __name__ == "__main__":
    引擎 = CNSH_流场可视化引擎()

    print("=" * 60)
    print("CNSH 流场可视化引擎 v2.0 · 演示")
    print("=" * 60)

    # 1. 扫描文件粒子
    数量 = 引擎.扫描文件粒子()
    print(f"\n📁 扫描到 {数量} 个文件粒子")
    print(引擎.生成透明度报告())

    # 2. P0 实时监控（演示：启动 2 秒后停止）
    监控 = 流场监控器(引擎, 间隔秒=1)
    监控.启动()
    time.sleep(2.1)
    监控.停止()
    print(f"\n📡 监控事件: {len(监控.事件日志)} 条")
    for e in 监控.事件日志:
        print(f"  [{e['时间'][11:19]}] {e['类型']}")

    # 3. P1 异常粒子隔离
    隔离区 = 粒子隔离区()
    不透明粒子 = [p for p in 引擎.粒子库.values() if p.透明度评分 < 1.0]
    for p in 不透明粒子[:2]:
        凭证 = 隔离区.隔离(p, "透明度不足，缺 DNA")
        print(f"\n🔒 隔离粒子: {p.名称} → 凭证 {凭证}")
    print(f"隔离统计: {隔离区.统计()}")

    # 4. P2 健康度
    健康 = 流场健康度(引擎)
    print(f"\n🏥 流场健康度:")
    print(json.dumps(健康.计算(), ensure_ascii=False, indent=2))

    # 5. P3 关系图谱
    图谱 = 关系图谱(引擎)
    if 引擎.粒子库:
        第一个 = next(iter(引擎.粒子库.keys()))
        print(f"\n🕸️ 依赖链深度2: {len(图谱.查询依赖链(第一个, 2))} 个节点")
        print(f"🕸️ 影响链深度2: {len(图谱.查询影响链(第一个, 2))} 个节点")

    # 6. 添加决策链
    决策步骤 = [
        {"动作": "语义翻译", "输入": "宝宝，把协议做成国密 py", "输出": "意图：内容加工+国密+审计", "三色": "🟢"},
        {"动作": "内容加工", "输入": "协议文本", "输出": "CNSH_xxx.py 骨架", "三色": "🟢"},
        {"动作": "国密绑定", "输入": "代码骨架", "输出": "SM3 哈希 + HMAC-SM3", "三色": "🟢"},
        {"动作": "三色审计", "输入": "生成代码", "输出": "🟢 5 🟡 1 🔴 0", "三色": "🟢"},
    ]
    决策ID = 引擎.添加决策粒子("协议转国密Python", 决策步骤)
    print(f"\n🧠 决策链已生成: {决策ID}，共 {len(决策步骤)} 个决策粒子")

    # 7. 生成流场数据
    输出路径 = 引擎.生成流场数据("./CNSH_流场数据.json")
    print(f"\n📊 流场数据已生成: {输出路径}")

    # 8. 审计一个粒子
    if 引擎.粒子库:
        第一个粒子ID = next(iter(引擎.粒子库.keys()))
        审计结果 = 引擎.审计粒子(第一个粒子ID)
        print(f"\n🔍 审计粒子: {第一个粒子ID}")
        print(json.dumps(审计结果, ensure_ascii=False, indent=2)[:600])
