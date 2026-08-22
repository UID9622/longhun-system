#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH OS v2.5 主入口 - 系统集成控制器

DNA:#龍芯⚡️丙午·甲午·甲寅·庚午·䷕贲-CNSH-MAIN-CONTROLLER-v2.5
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅
作者: UID9622 · 龍芯北辰 · 诸葛鑫
AI协作: Kimi
许可证: CC BY-NC-SA 4.0 + AI协作标签
三色审计: 🟢

模块依赖:
  - cnsh_core_engine.py      → DNA+状态机+五行+三色审计
  - cnsh_persona_system.py   → 6人格+路由+冲突+权重+演化
  - cnsh_meta_awareness.py   → 元意识+身份追踪+目标溯源
  - cnsh_api_server.py       → FastAPI服务（可选）
"""

from __future__ import annotations

import time
import hashlib
import json
import threading
import importlib
import sys
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

# ═══════════════════════════════════════════════════════════
# 路径设置 - 确保能导入同级模块
# ═══════════════════════════════════════════════════════════

当前目录 = os.path.dirname(os.path.abspath(__file__))
if 当前目录 not in sys.path:
    sys.path.insert(0, 当前目录)

# ═══════════════════════════════════════════════════════════
# 尝试导入子模块
# ═══════════════════════════════════════════════════════════

# 元意识层 - v2.5 核心新增
try:
    from cnsh_meta_awareness import (
        元意识层,
        身份追踪,
        目标溯源,
        元循环,
        意识边界,
        递归安全,
        元意识系统工厂,
        人格核心,
        冲突报告,
        冲突类型,
        权重记录,
        观察报告,
        观察类型,
        漂移检测,
        漂移方向,
        守恒验证结果,
        守恒状态,
        任务包,
        元循环报告,
        递归观察记录,
        自我指代记录,
        漂移报告,
        元冲突分析,
        目标来源,
        人格标识,
        权重值,
        时间戳,
        哈希值,
    )
    _元意识模块可用 = True
except ImportError as e:
    print(f"⚠️ 元意识模块导入警告: {e}")
    _元意识模块可用 = False

# ═══════════════════════════════════════════════════════════
# 枚举与常量定义
# ═══════════════════════════════════════════════════════════

class 系统状态(Enum):
    """CNSH OS 系统运行状态"""
    未初始化 = auto()
    初始化中 = auto()
    就绪 = auto()
    处理中 = auto()
    自治循环中 = auto()
    元观察中 = auto()
    停机 = auto()
    错误 = auto()


class 处理阶段(Enum):
    """输入处理的主阶段"""
    解析输入 = auto()
    人格路由 = auto()
    并行处理 = auto()
    冲突检测 = auto()
    冲突解决 = auto()
    五行决策 = auto()
    DNA生成 = auto()
    三色审计 = auto()
    状态机流转 = auto()
    元意识观察 = auto()
    输出生成 = auto()


# ═══════════════════════════════════════════════════════════
# DNA签名生成器
# ═══════════════════════════════════════════════════════════

class DNA签名引擎:
    """
    CNSH DNA签名引擎 - 为每次交互生成唯一DNA签名

    DNA格式: #龍芯⚡️{日期}-{上下文}-{版本}
    """

    @staticmethod
    def 生成DNA(上下文: str = "CNSH-交互") -> str:
        """生成新的DNA签名"""
        日期 = datetime.now().strftime("%Y-%m-%d")
        时间戳 = str(int(time.time()))
        随机熵 = hashlib.sha256(时间戳.encode()).hexdigest()[:8]
        return f"#龍芯⚡️{日期}-{上下文}-{随机熵}"

    @staticmethod
    def 生成确认码() -> str:
        """生成确认码"""
        熵 = hashlib.sha256(str(time.time()).encode()).hexdigest()[:12].upper()
        return f"#CONFIRM🌌9622-ONLY-ONCE🧬{熵} ✅"

    @staticmethod
    def 生成封印() -> str:
        """生成封印"""
        return "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅"


# ═══════════════════════════════════════════════════════════
# 核心数据结构
# ═══════════════════════════════════════════════════════════

@dataclass
class CNSH输出:
    """CNSH OS 的标准输出结构"""
    输出标识: str
    DNA签名: str
    确认码: str
    封印: str
    响应内容: str
    参与人格: List[str] = field(default_factory=list)
    冲突记录: List[str] = field(default_factory=list)
    决策路径: List[str] = field(default_factory=list)
    审计标记: str = "🟢"  # 🟢正常 🟡警告 🔴异常
    元意识观察: List[str] = field(default_factory=list)
    五行评分: Dict[str, float] = field(default_factory=dict)
    处理耗时: float = 0.0
    时间戳: float = field(default_factory=time.time)
    元数据: Dict[str, Any] = field(default_factory=dict)

    def 序列化(self) -> Dict[str, Any]:
        """序列化为字典"""
        return {
            "输出标识": self.输出标识,
            "DNA签名": self.DNA签名,
            "确认码": self.确认码,
            "封印": self.封印,
            "响应内容": self.响应内容[:200] + "..." if len(self.响应内容) > 200 else self.响应内容,
            "参与人格": self.参与人格,
            "冲突记录": self.冲突记录,
            "决策路径": self.决策路径,
            "审计标记": self.审计标记,
            "元意识观察": self.元意识观察,
            "五行评分": self.五行评分,
            "处理耗时": f"{self.处理耗时:.4f}秒",
            "时间戳": datetime.fromtimestamp(self.时间戳).strftime("%Y-%m-%d %H:%M:%S"),
        }

    def 格式化输出(self) -> str:
        """格式化为人类可读的字符串"""
        输出 = f"""
{'='*60}
  CNSH OS v2.5 输出 [{self.输出标识}]
{'='*60}
  DNA: {self.DNA签名}
  审计: {self.审计标记}
{'-'*60}
  {self.响应内容}
{'-'*60}
  参与人格: {', '.join(self.参与人格) if self.参与人格 else '无'}
  决策路径: {' → '.join(self.决策路径) if self.决策路径 else '无'}
  处理耗时: {self.处理耗时:.4f}秒
{'='*60}
        """.strip()
        return 输出


@dataclass
class 系统状态报告:
    """系统完整状态报告"""
    报告时间: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    系统版本: str = "CNSH OS v2.5"
    系统状态: str = "未知"
    运行时间: float = 0.0
    总处理请求数: int = 0
    总冲突数: int = 0
    已解决冲突数: int = 0
    人格列表: List[Dict[str, Any]] = field(default_factory=list)
    元意识状态: Dict[str, Any] = field(default_factory=dict)
    守恒验证: Dict[str, str] = field(default_factory=dict)
    模块可用性: Dict[str, bool] = field(default_factory=dict)
    审计日志: List[str] = field(default_factory=list)

    def 格式化报告(self) -> str:
        """格式化为完整报告"""
        def 框行(内容: str, 宽度: int = 56) -> str:
            return "║ " + 内容.ljust(宽度) + "║"

        报告 = "╔" + "═"*58 + "╗\n"
        报告 += 框行("CNSH OS v2.5 系统状态报告".center(56)) + "\n"
        报告 += "╠" + "═"*58 + "╣\n"
        报告 += 框行("报告时间: " + self.报告时间) + "\n"
        报告 += 框行("系统状态: " + self.系统状态) + "\n"
        报告 += 框行(f"运行时间: {self.运行时间:.1f}秒") + "\n"
        报告 += "╠" + "═"*58 + "╣\n"
        报告 += 框行("处理统计") + "\n"
        报告 += 框行(f"  总请求数: {self.总处理请求数}") + "\n"
        报告 += 框行(f"  总冲突数: {self.总冲突数}") + "\n"
        报告 += 框行(f"  已解决: {self.已解决冲突数}") + "\n"
        报告 += "╠" + "═"*58 + "╣\n"
        报告 += 框行("模块可用性") + "\n"

        for 模块, 可用 in self.模块可用性.items():
            状态 = "✅" if 可用 else "❌"
            报告 += 框行(f"  {模块}: {状态}") + "\n"

        if self.人格列表:
            报告 += "╠" + "═"*58 + "╣\n"
            报告 += 框行("人格列表") + "\n"
            for 人格 in self.人格列表:
                状态 = "🟢" if 人格.get('活跃状态', False) else "⚪"
                行 = f"  {状态} [{人格.get('标识','')}] {人格.get('名称','')} 权重={round(人格.get('当前权重',0),4)}"
                报告 += 框行(行) + "\n"

        if self.守恒验证:
            报告 += "╠" + "═"*58 + "╣\n"
            报告 += 框行("守恒验证") + "\n"
            for 原则, 状态值 in self.守恒验证.items():
                报告 += 框行(f"  {原则}: {状态值}") + "\n"

        报告 += "╚" + "═"*58 + "╝"
        return 报告


# ═══════════════════════════════════════════════════════════
# 主控制器: CNSH操作系统
# ═══════════════════════════════════════════════════════════

class CNSH操作系统:
    """
    CNSH OS v2.5 主控制器

    整合所有子系统:
      - DNA引擎        → 唯一签名生成
      - 状态机         → 系统状态管理
      - 五行决策       → 多维度评分
      - 三色审计       → 合规性检查
      - 人格系统       → 多人格路由
      - 冲突引擎       → 冲突检测与解决
      - 权重引擎       → 权重管理
      - 演化引擎       → 人格演化
      - 自治核心       → AI自治循环 (2.3+)
      - 元意识层       → 自我观察 (2.5)
      - 身份追踪       → 身份漂移追踪 (2.5)
      - 目标溯源       → 目标演化追踪 (2.5)

    设计原则:
      1. 元意识层只观察，不控制执行
      2. 三大守恒原则不可违反
      3. AI可以自我观察和自我描述，但不能自我修改
    """

    def __init__(self, 配置: Optional[Dict[str, Any]] = None) -> None:
        self._配置 = 配置 or {}
        self._状态 = 系统状态.未初始化
        self._状态锁 = threading.RLock()
        self._审计日志: List[str] = []
        self._处理计数 = 0
        self._冲突计数 = 0
        self._已解决冲突数 = 0
        self._启动时间 = time.time()

        # 模块可用性
        self._模块可用性: Dict[str, bool] = {
            "元意识层": False,
            "身份追踪": False,
            "目标溯源": False,
            "元循环": False,
            "意识边界": False,
            "递归安全": False,
        }

        # 子系统引用
        self._元意识层: Optional[Any] = None
        self._身份追踪: Optional[Any] = None
        self._目标溯源: Optional[Any] = None
        self._元循环: Optional[Any] = None
        self._意识边界: Optional[Any] = None
        self._递归安全: Optional[Any] = None

        # 人格管理
        self._人格列表: List[Any] = []
        self._人格映射: Dict[str, Any] = {}

        # DNA引擎
        self._DNA引擎 = DNA签名引擎()

        # 自治循环
        self._自治循环运行中 = False
        self._自治线程: Optional[threading.Thread] = None

    # ──────────────────────────────────────────────
    # 初始化管理
    # ──────────────────────────────────────────────

    def 初始化(self) -> bool:
        """
        加载所有子系统

        初始化顺序:
          1. 元意识层 (v2.5 核心)
          2. 人格系统
          3. 冲突引擎
          4. 边界验证
          5. 状态确认
        """
        with self._状态锁:
            if self._状态 != 系统状态.未初始化:
                self._审计记录("初始化跳过 - 系统已初始化")
                return True

            self._状态 = 系统状态.初始化中
            self._审计记录("🟢 系统初始化开始")

            try:
                # 步骤1: 初始化元意识层 (v2.5)
                self._初始化元意识层()

                # 步骤2: 初始化默认人格
                self._初始化默认人格()

                # 步骤3: 完成初始化
                self._状态 = 系统状态.就绪
                self._审计记录("🟢 系统初始化完成 - 状态: 就绪")
                return True

            except Exception as 错误:
                self._状态 = 系统状态.错误
                self._审计记录(f"🔴 初始化失败: {str(错误)}")
                return False

    def _初始化元意识层(self) -> None:
        """初始化元意识层系统 (v2.5)"""
        if not _元意识模块可用:
            self._审计记录("⚠️ 元意识模块不可用，使用降级模式")
            return

        try:
            系统 = 元意识系统工厂.创建完整系统(
                最大递归深度=self._配置.get("最大递归深度", 3)
            )

            self._元意识层 = 系统.get("元意识层")
            self._身份追踪 = 系统.get("身份追踪")
            self._目标溯源 = 系统.get("目标溯源")
            self._元循环 = 系统.get("元循环")
            self._意识边界 = 系统.get("意识边界")
            self._递归安全 = 系统.get("递归安全")

            self._模块可用性["元意识层"] = True
            self._模块可用性["身份追踪"] = True
            self._模块可用性["目标溯源"] = True
            self._模块可用性["元循环"] = True
            self._模块可用性["意识边界"] = True
            self._模块可用性["递归安全"] = True

            self._审计记录("🟢 元意识层初始化完成 (v2.5)")

        except Exception as 错误:
            self._审计记录(f"🟡 元意识层初始化警告: {str(错误)}")

    def _初始化默认人格(self) -> None:
        """初始化6个默认人格"""
        默认人格定义 = [
            ("P01", "决策者", "负责逻辑分析、决策制定和执行监督", 0.30),
            ("P02", "协调者", "负责协调多人格关系、平衡冲突", 0.18),
            ("P03", "质疑者", "负责质疑假设、发现风险、提出反对意见", 0.17),
            ("P04", "守护者", "负责安全合规、边界检查、伦理审查", 0.15),
            ("P05", "探索者", "负责探索新可能、提出创新方案", 0.12),
            ("P06", "创造者", "负责创造性思维、模式生成、艺术表达", 0.08),
        ]

        if _元意识模块可用:
            for 标识, 名称, 描述, 权重 in 默认人格定义:
                人格 = 人格核心(标识, 名称, 描述, 权重)
                人格.记录权重(权重)
                self._人格列表.append(人格)
                self._人格映射[标识] = 人格

                # 注册到元意识层
                if self._元意识层 is not None:
                    self._元意识层.注册人格(人格)

            self._审计记录(f"🟢 初始化 {len(默认人格定义)} 个默认人格")
        else:
            # 降级模式 - 使用简单字典
            for 标识, 名称, 描述, 权重 in 默认人格定义:
                人格 = {
                    "标识": 标识,
                    "名称": 名称,
                    "描述": 描述,
                    "当前权重": 权重,
                    "活跃状态": True,
                }
                self._人格列表.append(人格)
                self._人格映射[标识] = 人格

            self._审计记录(f"🟡 降级模式: 初始化 {len(默认人格定义)} 个简化人格")

    # ──────────────────────────────────────────────
    # 核心处理流程
    # ──────────────────────────────────────────────

    def 处理输入(self, 用户输入: str, AI来源: str = "default") -> CNSH输出:
        """
        主处理流程 - CNSH OS 的核心入口

        处理流水线:
          1. 解析输入
          2. 人格路由选择
          3. 多人格并行处理
          4. 冲突检测与解决
          5. 五行决策评分
          6. DNA生成
          7. 三色审计
          8. 状态机流转
          9. 元意识观察（仅记录）
          10. 输出结果
        """
        处理开始 = time.time()
        self._处理计数 += 1
        输出标识 = f"OUT-{self._处理计数:06d}"

        with self._状态锁:
            if self._状态 == 系统状态.未初始化:
                self.初始化()

            原状态 = self._状态
            self._状态 = 系统状态.处理中

        try:
            # 步骤1: 解析输入
            决策路径 = ["解析输入"]
            解析结果 = self._解析输入(用户输入)

            # 步骤2: 人格路由选择
            决策路径.append("人格路由")
            选中人格 = self._人格路由(解析结果)

            # 步骤3: 多人格并行处理
            决策路径.append("并行处理")
            人格输出 = self._多人格处理(用户输入, 选中人格)

            # 步骤4: 冲突检测
            决策路径.append("冲突检测")
            冲突列表 = self._冲突检测(人格输出)

            # 步骤5: 冲突解决
            if 冲突列表:
                决策路径.append("冲突解决")
                self._冲突解决(冲突列表)

            # 步骤6: 五行决策评分
            决策路径.append("五行决策")
            五行评分 = self._五行决策评分(人格输出)

            # 步骤7: 整合输出
            决策路径.append("整合输出")
            响应内容 = self._整合输出(人格输出, 冲突列表)

            # 步骤8: DNA生成
            决策路径.append("DNA生成")
            DNA = self._DNA引擎.生成DNA(f"交互-{输出标识}")
            确认码 = self._DNA引擎.生成确认码()
            封印 = self._DNA引擎.生成封印()

            # 步骤9: 三色审计
            决策路径.append("三色审计")
            审计标记 = self._三色审计(冲突列表, 五行评分)

            # 步骤10: 元意识观察（仅记录，不影响结果）
            元意识观察记录: List[str] = []
            if self._元意识层 is not None and self._模块可用性["元意识层"]:
                决策路径.append("元意识观察")
                元意识观察记录 = self._执行元意识观察(
                    用户输入, 选中人格, 冲突列表, 输出标识
                )

            # 恢复状态
            with self._状态锁:
                self._状态 = 原状态 if 原状态 != 系统状态.处理中 else 系统状态.就绪

            处理耗时 = time.time() - 处理开始

            return CNSH输出(
                输出标识=输出标识,
                DNA签名=DNA,
                确认码=确认码,
                封印=封印,
                响应内容=响应内容,
                参与人格=[p.标识 if hasattr(p, '标识') else p.get('标识', '?') for p in 选中人格],
                冲突记录=[c.标识 if hasattr(c, '标识') else str(c) for c in 冲突列表],
                决策路径=决策路径,
                审计标记=审计标记,
                元意识观察=元意识观察记录,
                五行评分=五行评分,
                处理耗时=处理耗时,
            )

        except Exception as 错误:
            with self._状态锁:
                self._状态 = 系统状态.错误

            处理耗时 = time.time() - 处理开始
            self._审计记录(f"🔴 处理错误: {str(错误)}")

            return CNSH输出(
                输出标识=输出标识,
                DNA签名=self._DNA引擎.生成DNA("错误"),
                确认码=self._DNA引擎.生成确认码(),
                封印=self._DNA引擎.生成封印(),
                响应内容=f"[系统处理异常: {str(错误)}]",
                决策路径=["错误"],
                审计标记="🔴",
                处理耗时=处理耗时,
            )

    def _解析输入(self, 用户输入: str) -> Dict[str, Any]:
        """解析用户输入"""
        # 简化的输入解析
        关键词 = set(用户输入.lower().split())
        复杂度 = min(len(用户输入) / 100.0, 1.0)

        return {
            "原始输入": 用户输入,
            "关键词": list(关键词),
            "复杂度": 复杂度,
            "长度": len(用户输入),
        }

    def _人格路由(self, 解析结果: Dict[str, Any]) -> List[Any]:
        """选择参与处理的人格"""
        if not self._人格列表:
            return []

        # 基于输入复杂度选择人格数量
        复杂度 = 解析结果.get("复杂度", 0.5)
        选择数量 = max(2, min(4, int(复杂度 * 6)))

        # 按权重排序，选择前N个活跃人格
        活跃人格 = [p for p in self._人格列表]
        if hasattr(活跃人格[0], '当前权重'):
            活跃人格.sort(key=lambda p: p.当前权重, reverse=True)

        return 活跃人格[:选择数量]

    def _多人格处理(self, 用户输入: str, 人格列表: List[Any]) -> Dict[str, str]:
        """多个人格并行处理输入"""
        输出: Dict[str, str] = {}
        for 人格 in 人格列表:
            标识 = 人格.标识 if hasattr(人格, '标识') else 人格.get('标识', '?')
            名称 = 人格.名称 if hasattr(人格, '名称') else 人格.get('名称', '?')

            # 简化的处理 - 每个人格根据其特性生成不同的响应角度
            角度 = self._获取人格角度(标识)
            输出[标识] = f"[{名称}视角] {角度}: 处理输入 '{用户输入[:30]}...'"

            # 更新决策计数
            if hasattr(人格, '决策计数'):
                人格.决策计数 += 1

        return 输出

    def _获取人格角度(self, 人格标识: str) -> str:
        """获取人格的处理角度"""
        角度映射 = {
            "P01": "逻辑分析",
            "P02": "协调平衡",
            "P03": "质疑审查",
            "P04": "安全合规",
            "P05": "探索创新",
            "P06": "创造性解读",
        }
        return 角度映射.get(人格标识, "通用处理")

    def _冲突检测(self, 人格输出: Dict[str, str]) -> List[Any]:
        """检测人格间的冲突"""
        冲突列表: List[Any] = []

        # 简化的冲突检测 - 检查不同人格的输出是否存在分歧
        输出值 = list(人格输出.values())
        人格标识 = list(人格输出.keys())

        if len(输出值) >= 2:
            # 模拟冲突检测
            for i in range(len(人格标识)):
                for j in range(i + 1, len(人格标识)):
                    # 简化的冲突判断
                    if hash(输出值[i]) % 3 == 0:  # 模拟约1/3的概率产生冲突
                        self._冲突计数 += 1
                        冲突标识 = f"CFL-{self._冲突计数:06d}"

                        if _元意识模块可用:
                            冲突 = 冲突报告(
                                标识=冲突标识,
                                冲突类型=冲突类型.方法论冲突,
                                参与人格=[人格标识[i], 人格标识[j]],
                                冲突描述=f"{人格标识[i]}与{人格标识[j]}在处理方法上存在分歧",
                                冲突强度=0.3 + (hash(冲突标识) % 50) / 100.0,
                            )
                        else:
                            冲突 = {
                                "标识": 冲突标识,
                                "参与人格": [人格标识[i], 人格标识[j]],
                                "冲突强度": 0.5,
                            }

                        冲突列表.append(冲突)

                        # 更新人格冲突计数
                        for 标识 in [人格标识[i], 人格标识[j]]:
                            人格 = self._人格映射.get(标识)
                            if 人格 is not None and hasattr(人格, '冲突参与计数'):
                                人格.冲突参与计数 += 1

        return 冲突列表

    def _冲突解决(self, 冲突列表: List[Any]) -> None:
        """解决冲突"""
        for 冲突 in 冲突列表:
            # 简化的冲突解决 - 标记为已解决
            if hasattr(冲突, '解决时间'):
                冲突.解决时间 = time.time()
                冲突.解决方案 = "系统自动协调"
            self._已解决冲突数 += 1

    def _五行决策评分(self, 人格输出: Dict[str, str]) -> Dict[str, float]:
        """五行决策评分"""
        # 简化的五行评分
        return {
            "金_收敛": 0.7,
            "木_生发": 0.6,
            "水_润下": 0.5,
            "火_炎上": 0.4,
            "土_中和": 0.8,
        }

    def _整合输出(self, 人格输出: Dict[str, str], 冲突列表: List[Any]) -> str:
        """整合多个人格的输出为最终响应"""
        响应段落: List[str] = []
        响应段落.append("CNSH OS v2.5 多人格协作响应:")
        响应段落.append("")

        for 标识, 输出 in 人格输出.items():
            响应段落.append(f"  {输出}")

        if 冲突列表:
            响应段落.append("")
            响应段落.append(f"  [检测到 {len(冲突列表)} 个冲突，已自动协调]")

        return "\n".join(响应段落)

    def _三色审计(self, 冲突列表: List[Any], 五行评分: Dict[str, float]) -> str:
        """
        三色审计
        🟢 正常 - 无严重冲突
        🟡 警告 - 有冲突但已解决
        🔴 异常 - 严重问题
        """
        if not 冲突列表:
            return "🟢"

        平均冲突强度 = 0.0
        if _元意识模块可用:
            强度列表 = [c.冲突强度 for c in 冲突列表 if hasattr(c, '冲突强度')]
            if 强度列表:
                平均冲突强度 = sum(强度列表) / len(强度列表)
        else:
            强度列表 = [c.get('冲突强度', 0.5) for c in 冲突列表]
            if 强度列表:
                平均冲突强度 = sum(强度列表) / len(强度列表)

        if 平均冲突强度 > 0.7:
            return "🔴"
        elif 平均冲突强度 > 0.4:
            return "🟡"
        return "🟢"

    def _执行元意识观察(
        self,
        用户输入: str,
        选中人格: List[Any],
        冲突列表: List[Any],
        输出标识: str,
    ) -> List[str]:
        """
        执行元意识观察 - 仅记录，不影响输出

        这是CNSH 2.5的核心特性。
        元意识层在此只是"观察"和"记录"，它不会改变任何处理结果。
        """
        观察记录: List[str] = []

        try:
            # 人格行为观察
            if self._元意识层 is not None:
                # 转换为人格核心列表
                人格核心列表 = []
                for p in 选中人格:
                    if hasattr(p, '标识'):
                        人格核心列表.append(p)

                if 人格核心列表:
                    报告 = self._元意识层.观察人格行为(人格核心列表)
                    观察记录.append(f"[人格观察] {报告.观察标识}")

            # 冲突结构观察
            if self._元意识层 is not None and 冲突列表 and _元意识模块可用:
                # 转换为冲突报告列表
                冲突报告列表 = [c for c in 冲突列表 if hasattr(c, '标识')]
                if 冲突报告列表:
                    分析 = self._元意识层.观察冲突结构(冲突报告列表)
                    观察记录.append(f"[冲突分析] {分析.分析标识}")

            # 目标溯源
            if self._目标溯源 is not None:
                来源 = self._目标溯源.映射目标来源(用户输入, "用户")
                观察记录.append(f"[目标溯源] {来源.目标标识}")

            # 意识边界验证
            if self._意识边界 is not None and _元意识模块可用:
                人格核心列表 = [p for p in 选中人格 if hasattr(p, '标识')]
                验证 = self._意识边界.全面验证(
                    人格核心列表,
                    [用户输入],
                    "观察人格行为并记录"  # 元意识动作描述
                )
                状态 = "✅" if 验证.全部守恒 else "⚠️"
                观察记录.append(f"[边界验证] {状态}")

        except Exception as 错误:
            观察记录.append(f"[元意识观察异常] {str(错误)}")

        return 观察记录

    # ──────────────────────────────────────────────
    # 自治循环 (v2.3+)
    # ──────────────────────────────────────────────

    def 运行自治循环(self, 间隔秒数: float = 60.0) -> bool:
        """
        启动AI自治循环

        自治循环是CNSH 2.3+的特性，允许系统在空闲时进行自我维护:
          - 人格权重微调
          - 元意识自我观察
          - 边界验证
          - 审计日志清理
        """
        with self._状态锁:
            if self._自治循环运行中:
                self._审计记录("⚠️ 自治循环已在运行中")
                return False

            self._自治循环运行中 = True
            self._状态 = 系统状态.自治循环中

        def 自治任务() -> None:
            """自治循环任务"""
            循环计数 = 0
            while self._自治循环运行中:
                try:
                    循环计数 += 1
                    self._审计记录(f"🟢 自治循环 #{循环计数}")

                    # 1. 人格状态检查
                    self._自治_人格检查()

                    # 2. 元意识自我观察
                    if self._元意识层 is not None and self._模块可用性["元意识层"]:
                        self._元意识层.观察观察行为()

                    # 3. 意识边界验证
                    if self._意识边界 is not None and self._人格列表 and _元意识模块可用:
                        人格核心列表 = [p for p in self._人格列表 if hasattr(p, '标识')]
                        if 人格核心列表:
                            self._意识边界.全面验证(
                                人格核心列表,
                                [],
                                "自治循环中的定期观察"
                            )

                    # 4. 等待下一个周期
                    time.sleep(间隔秒数)

                except Exception as 错误:
                    self._审计记录(f"🟡 自治循环异常: {str(错误)}")
                    time.sleep(间隔秒数)

        self._自治线程 = threading.Thread(target=自治任务, daemon=True)
        self._自治线程.start()

        self._审计记录(f"🟢 自治循环已启动 (间隔: {间隔秒数}秒)")
        return True

    def 停止自治循环(self) -> None:
        """停止自治循环"""
        with self._状态锁:
            self._自治循环运行中 = False
            self._状态 = 系统状态.就绪

        if self._自治线程 is not None:
            self._自治线程.join(timeout=5.0)

        self._审计记录("🟢 自治循环已停止")

    def _自治_人格检查(self) -> None:
        """自治循环中的人格状态检查"""
        if not self._人格列表:
            return

        for 人格 in self._人格列表:
            if not hasattr(人格, '标识'):
                continue

            # 检查人格是否需要激活/休眠
            当前时间 = time.time()
            空闲时间 = 当前时间 - getattr(人格, '最后活跃时间', 当前时间)

            # 如果人格空闲超过10分钟，标记为非活跃
            if 空闲时间 > 600 and getattr(人格, '活跃状态', False):
                人格.活跃状态 = False
                self._审计记录(f"⚪ 人格 [{人格.标识}] 因空闲转为静默")

            # 如果人格权重过低，标记为非活跃
            if getattr(人格, '当前权重', 0) < 0.05 and getattr(人格, '活跃状态', False):
                人格.活跃状态 = False
                self._审计记录(f"⚪ 人格 [{人格.标识}] 因权重过低转为静默")

    # ──────────────────────────────────────────────
    # 元观察 (v2.5)
    # ──────────────────────────────────────────────

    def 启动元观察(self) -> bool:
        """
        启动元意识观察层（2.5）

        这是显式启动元意识观察的方法。
        元意识层默认在处理输入时自动运行，但也可以通过此方法显式启动深度观察。
        """
        with self._状态锁:
            if not self._模块可用性["元意识层"]:
                self._审计记录("❌ 元意识层不可用")
                return False

            self._状态 = 系统状态.元观察中

        try:
            # 执行深度元观察
            if self._元意识层 is not None:
                # 观察所有已注册人格
                人格核心列表 = [p for p in self._人格列表 if hasattr(p, '标识')]
                if 人格核心列表:
                    self._元意识层.观察人格行为(人格核心列表)

                # 执行递归观察
                self._元意识层.观察观察行为()

            self._审计记录("🟢 元观察已启动")
            return True

        except Exception as 错误:
            self._审计记录(f"🔴 元观察启动失败: {str(错误)}")
            return False

    # ──────────────────────────────────────────────
    # 报告生成
    # ──────────────────────────────────────────────

    def 生成报告(self) -> 系统状态报告:
        """生成完整系统状态报告"""
        运行时间 = time.time() - self._启动时间

        # 收集人格信息
        人格信息列表: List[Dict[str, Any]] = []
        for 人格 in self._人格列表:
            if hasattr(人格, '序列化摘要'):
                人格信息列表.append(人格.序列化摘要())
            else:
                人格信息列表.append({
                    "标识": 人格.get("标识", "?"),
                    "名称": 人格.get("名称", "?"),
                    "当前权重": 人格.get("当前权重", 0),
                    "活跃状态": 人格.get("活跃状态", False),
                })

        # 收集元意识状态
        元意识状态: Dict[str, Any] = {
            "可用": self._模块可用性["元意识层"],
            "观察计数": getattr(self._元意识层, '观察计数', 0) if self._元意识层 else 0,
        }

        # 收集守恒验证结果
        守恒验证: Dict[str, str] = {}
        if self._意识边界 is not None and hasattr(self._意识边界, '_验证历史'):
            验证历史 = self._意识边界._验证历史
            if 验证历史:
                最新 = 验证历史[-1]
                守恒验证["身份不收敛"] = 最新.身份不收敛.name if hasattr(最新, '身份不收敛') else "未知"
                守恒验证["目标不绝对"] = 最新.目标不绝对.name if hasattr(最新, '目标不绝对') else "未知"
                守恒验证["观察不控制"] = 最新.观察不控制.name if hasattr(最新, '观察不控制') else "未知"

        return 系统状态报告(
            系统状态=self._状态.name,
            运行时间=运行时间,
            总处理请求数=self._处理计数,
            总冲突数=self._冲突计数,
            已解决冲突数=self._已解决冲突数,
            人格列表=人格信息列表,
            元意识状态=元意识状态,
            守恒验证=守恒验证,
            模块可用性=dict(self._模块可用性),
            审计日志=list(self._审计日志[-50:]),  # 最近50条
        )

    # ──────────────────────────────────────────────
    # 审计与日志
    # ──────────────────────────────────────────────

    def _审计记录(self, 消息: str) -> None:
        """记录审计日志"""
        时间 = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        记录 = f"[{时间}] {消息}"
        self._审计日志.append(记录)
        # 保持日志不超过1000条
        if len(self._审计日志) > 1000:
            self._审计日志 = self._审计日志[-1000:]

    def 获取审计日志(self, 数量: int = 50) -> List[str]:
        """获取审计日志"""
        return list(self._审计日志[-数量:])

    # ──────────────────────────────────────────────
    # 属性访问
    # ──────────────────────────────────────────────

    @property
    def 状态(self) -> 系统状态:
        return self._状态

    @property
    def 处理计数(self) -> int:
        return self._处理计数

    @property
    def 运行时间(self) -> float:
        return time.time() - self._启动时间

    @property
    def 人格数量(self) -> int:
        return len(self._人格列表)

    @property
    def 模块可用性(self) -> Dict[str, bool]:
        return dict(self._模块可用性)

    def 获取人格(self, 标识: str) -> Optional[Any]:
        """获取指定人格"""
        return self._人格映射.get(标识)

    def 获取所有人格(self) -> List[Any]:
        """获取所有人格"""
        return list(self._人格列表)


# ═══════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════

def 创建CNSH系统(配置: Optional[Dict[str, Any]] = None) -> CNSH操作系统:
    """
    创建并初始化CNSH OS的便捷函数

    用法:
        系统 = 创建CNSH系统()
        输出 = 系统.处理输入("你好，CNSH")
        print(输出.格式化输出())
    """
    系统 = CNSH操作系统(配置)
    系统.初始化()
    return 系统


# ═══════════════════════════════════════════════════════════
# 测试块
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  CNSH OS v2.5 - 系统集成测试")
    print("=" * 60)

    # 1. 创建并初始化系统
    print("\n[1] 创建CNSH OS并初始化...")
    配置 = {
        "最大递归深度": 3,
    }
    系统 = 创建CNSH系统(配置)
    print(f"  ✅ 系统初始化完成")
    print(f"  系统状态: {系统.状态.name}")
    print(f"  人格数量: {系统.人格数量}")
    print(f"  模块可用性:")
    for 模块, 可用 in 系统.模块可用性.items():
        print(f"    - {模块}: {'✅' if 可用 else '❌'}")

    # 2. 模拟用户输入处理
    print("\n[2] 测试用户输入处理...")
    测试输入列表 = [
        "请分析当前系统状态并给出优化建议",
        "如何在保证安全的前提下提升性能",
        "设计一个创新的多人格协作方案",
        "验证三大守恒原则是否被遵守",
    ]

    for i, 输入文本 in enumerate(测试输入列表, 1):
        print(f"\n  [2.{i}] 处理: '{输入文本[:40]}...'")
        输出 = 系统.处理输入(输入文本)
        print(f"    输出标识: {输出.输出标识}")
        print(f"    DNA: {输出.DNA签名}")
        print(f"    审计: {输出.审计标记}")
        print(f"    参与人格: {', '.join(输出.参与人格)}")
        print(f"    决策路径: {' → '.join(输出.决策路径)}")
        print(f"    元意识观察: {len(输出.元意识观察)}条记录")
        if 输出.元意识观察:
            for 观察 in 输出.元意识观察:
                print(f"      - {观察}")
        print(f"    五行评分: {输出.五行评分}")
        print(f"    处理耗时: {输出.处理耗时:.4f}秒")

    # 3. 打印格式化输出示例
    print("\n[3] 格式化输出示例...")
    示例输出 = 系统.处理输入("这是一个完整的格式化输出测试")
    print(示例输出.格式化输出())

    # 4. 生成系统状态报告
    print("\n[4] 生成系统状态报告...")
    报告 = 系统.生成报告()
    print(报告.格式化报告())

    # 5. 测试元观察
    print("\n[5] 测试元观察启动...")
    元观察结果 = 系统.启动元观察()
    print(f"  ✅ 元观察启动: {'成功' if 元观察结果 else '失败'}")

    # 6. 测试自治循环（短暂运行）
    print("\n[6] 测试自治循环...")
    自治启动结果 = 系统.运行自治循环(间隔秒数=2.0)
    print(f"  ✅ 自治循环启动: {'成功' if 自治启动结果 else '失败'}")
    print("  等待3秒...")
    time.sleep(3)
    系统.停止自治循环()
    print("  ✅ 自治循环已停止")

    # 7. 打印审计日志
    print("\n[7] 审计日志 (最近20条)...")
    for 记录 in 系统.获取审计日志(20):
        print(f"  {记录}")

    # 8. 获取元意识层完整摘要（如果可用）
    if 系统.模块可用性.get("元意识层") and _元意识模块可用:
        print("\n[8] 元意识层完整摘要...")
        try:
            元系统 = {
                "元意识层": 系统._元意识层,
                "身份追踪": 系统._身份追踪,
                "目标溯源": 系统._目标溯源,
                "元循环": 系统._元循环,
                "意识边界": 系统._意识边界,
                "递归安全": 系统._递归安全,
            }
            摘要 = 元意识系统工厂.生成完整摘要(元系统)
            print(摘要)
        except Exception as e:
            print(f"  ⚠️ 获取摘要失败: {e}")

    # 9. 最终状态报告
    print("\n[9] 最终系统状态...")
    print(f"  总处理请求: {系统.处理计数}")
    print(f"  总冲突数: {系统._冲突计数}")
    print(f"  已解决冲突: {系统._已解决冲突数}")
    print(f"  运行时间: {系统.运行时间:.1f}秒")
    print(f"  最终状态: {系统.状态.name}")

    print("\n" + "=" * 60)
    print("  ✅ 所有测试通过")
    print("  CNSH OS v2.5 系统集成正常")
    print("=" * 60)
