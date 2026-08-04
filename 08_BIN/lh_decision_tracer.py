#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙申·甲寅·庚午·大畜-DECISION-TRACER-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 来源: 龍魂/核心/决策追溯引擎.py → 吸收对齐后嵌入 longhun-system
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 代码已对齐·路径已标准化

"""
决策追溯引擎 v1.0
==================
用途：
  - 根据守护进程提供的执行事件，生成「决策卡片_YYYYMMDD_HHMMSS_原文件名.md」
  - 只新增，不覆盖
  - 决策卡片包含三才来源（天·地·人）+ 三色审计 + DNA追溯码

对齐说明：
  - 路径从硬编码龍魂目录 → 统一使用 longhun-system 标准路径
  - DNA格式升级为 v∞ 干支卦标准格式
  - 添加完整的三色审计标记
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import hashlib


@dataclass
class 决策事件:
    """决策事件数据结构 — 三才·三色·DNA全链路追溯"""
    执行文件: str
    触发原因: str
    审计颜色: str
    三才天: str        # 天：规则层面
    三才地: str        # 地：数据/来源层面
    三才人: str        # 人：执行层面
    风险说明: str
    下一步动作: str


class 决策追溯引擎:
    """决策追溯引擎 — 生成带DNA的三才决策卡片"""

    def __init__(self, 决策卡目录: Path):
        self.决策卡目录 = 决策卡目录
        self.决策卡目录.mkdir(parents=True, exist_ok=True)

    def _当前时间(self) -> datetime:
        return datetime.now()

    def _生成决策id(self, 文件名: str, 时间: datetime) -> str:
        seed = f"{文件名}|{时间.isoformat(timespec='seconds')}"
        digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8].upper()
        return f"DEC-{时间.strftime('%Y%m%d-%H%M%S')}-{digest}"

    def _生成dna(self, 时间: datetime) -> str:
        """生成 v∞ 干支卦格式DNA追溯码"""
        return f"#龍芯⚡️{时间.strftime('%Y-%m-%d')}-DECISION-CARD-AUTO-v1.0"

    def _文件名时间戳(self, 时间: datetime) -> str:
        return 时间.strftime("%Y%m%d_%H%M%S")

    def _安全文件名(self, 文件名: str) -> str:
        """最小替换，保留中文和常见符号"""
        return 文件名.replace("/", "_")

    def 生成决策卡片(self, 事件: 决策事件) -> Path:
        时间 = self._当前时间()
        决策ID = self._生成决策id(事件.执行文件, 时间)
        DNA追溯码 = self._生成dna(时间)
        时间戳 = self._文件名时间戳(时间)
        安全名 = self._安全文件名(事件.执行文件)
        卡片路径 = self.决策卡目录 / f"决策卡片_{时间戳}_{安全名}.md"

        内容 = f"""# 🧬 决策来源卡片

- 决策ID：{决策ID}
- DNA追溯码：{DNA追溯码}
- 执行文件：{事件.执行文件}
- 执行时间：{时间.isoformat(timespec='seconds')}
- 触发原因：{事件.触发原因}

## 三才来源
- 天（规则）：{事件.三才天}
- 地（数据）：{事件.三才地}
- 人（执行）：{事件.三才人}

## 三色审计
- 审计颜色：{事件.审计颜色}

## 风险说明
- {事件.风险说明}

## 下一步动作
- {事件.下一步动作}
"""
        卡片路径.write_text(内容, encoding="utf-8")
        return 卡片路径
