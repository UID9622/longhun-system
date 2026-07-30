#!/usr/bin/env python3
#龍芯⚡️2026-06-29-CNSH-ECOSUPERVISION-UID9622
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

"""🐉 龍魂引擎：CNSH_生态监管协议
路径：bin/CNSH_生态监管协议.py
TODO：请补充详细功能说明（不少于20字）。"""
import os as _os
import sys as _sys
_module_dir = _os.path.dirname(_os.path.abspath(__file__))
if _module_dir not in _sys.path:
    _sys.path.insert(0, _module_dir)
"""
CNSH 生态监管协议 v1.0
核心原则：
  - 进入龍魂生态的每一个创作/代码，必须有六层来源链 + 人物属性 DNA
  - 抹掉痕迹 → 自动断联 + 发警报
  - 民用创作（图/视频/文章）开放，专业开发（代码/系统/协议）需认证
  - 人人都是开发者，但必须在统一监管框架内
DNA: #龍芯⚡️2026-06-29-CNSH-ECOSUPERVISION-UID9622
"""

import json
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from CNSH_国密工具 import SM3, hmac_sm3, 生成随机密钥


# ============== 创作分级 ==============
class 创作等级:
    L0_游客 = "L0"          # 只能浏览
    L1_民用创作 = "L1"      # 图、视频、音频、文章
    L2_活跃开发者 = "L2"    # 简单代码、脚本、小工具
    L3_认证开发者 = "L3"    # 系统、协议、核心代码，需专业认证


@dataclass
class 人物属性:
    UID: str
    昵称: str
    注册时间: str
    活跃度: int = 0          # 最近30天操作次数
    连续活跃天数: int = 0
    换号次数: int = 0
    专业认证: List[str] = field(default_factory=list)
    信用分: float = 100.0
    等级: str = 创作等级.L0_游客

    def to_dict(self) -> Dict[str, Any]:
        return {
            "UID": self.UID,
            "昵称": self.昵称,
            "注册时间": self.注册时间,
            "活跃度": self.活跃度,
            "连续活跃天数": self.连续活跃天数,
            "换号次数": self.换号次数,
            "专业认证": self.专业认证,
            "信用分": self.信用分,
            "等级": self.等级,
        }


@dataclass
class 创作登记:
    创作ID: str
    创作者UID: str
    内容类型: str
    内容SM3哈希: str
    六层来源链: Dict[str, str]
    人物属性DNA: str
    时间戳: str
    创作等级: str


class CNSH_生态监管协议:
    """
    龍魂生态统一监管入口。
    每个人都是开发者，但每个创作都受监管、可追溯、不可抹痕。
    """

    # 内容类型 → 所需最低创作等级
    分级权限 = {
        "图片": 创作等级.L1_民用创作,
        "视频": 创作等级.L1_民用创作,
        "音频": 创作等级.L1_民用创作,
        "文章": 创作等级.L1_民用创作,
        "脚本": 创作等级.L2_活跃开发者,
        "小工具": 创作等级.L2_活跃开发者,
        "代码": 创作等级.L2_活跃开发者,
        "协议": 创作等级.L3_认证开发者,
        "系统": 创作等级.L3_认证开发者,
        "核心模块": 创作等级.L3_认证开发者,
    }

    # 必须保留的来源链层
    来源链六层 = [
        "道统层",   # 文化根脉/协议来源
        "精神层",   # 创作者理念
        "设备层",   # 生成环境
        "技术层",   # 技术栈
        "系统层",   # 所属系统/模块
        "生命层",   # 真实创作者身份
    ]

    # 不可抹除的标记
    不可抹除标记 = [
        r"#龍芯⚡️",
        r"#CONFIRM",
        r"Author[:=]",
        r"Copyright",
        r"License[:=]",
        r"归属权",
        r"创始人",
        r"创作者",
        r"UID\d+",
    ]

    # 颜色代码 ↔ emoji 映射
    颜色代码表 = {
        "G": "🟢", "Y": "🟡", "R": "🔴", "K": "⚫",
        "P": "🟣", "B": "🔵", "AU": "🟡",
    }

    def __init__(self, 工作目录: str = "./CNSH_监管数据"):
        self.工作目录 = Path(工作目录)
        self.工作目录.mkdir(parents=True, exist_ok=True)
        self.创作者库: Dict[str, 人物属性] = {}
        self.创作登记库: Dict[str, 创作登记] = {}
        self.告警记录: List[Dict[str, Any]] = []
        self.断联列表: List[str] = []
        self.监管密钥 = 生成随机密钥()
        self._加载()

    def _加载(self):
        创作者路径 = self.工作目录 / "创作者库.json"
        创作路径 = self.工作目录 / "创作登记库.json"
        if 创作者路径.exists():
            with open(创作者路径, "r", encoding="utf-8") as f:
                数据 = json.load(f)
                for uid, d in 数据.items():
                    self.创作者库[uid] = 人物属性(**d)
        if 创作路径.exists():
            with open(创作路径, "r", encoding="utf-8") as f:
                数据 = json.load(f)
                for cid, d in 数据.items():
                    self.创作登记库[cid] = 创作登记(**d)

    def _保存(self):
        with open(self.工作目录 / "创作者库.json", "w", encoding="utf-8") as f:
            json.dump({uid: p.to_dict() for uid, p in self.创作者库.items()}, f, ensure_ascii=False, indent=2)
        with open(self.工作目录 / "创作登记库.json", "w", encoding="utf-8") as f:
            json.dump({cid: c.__dict__ for cid, c in self.创作登记库.items()}, f, ensure_ascii=False, indent=2)

    # ============== 1. 人物属性 DNA ==============
    def 注册创作者(self, UID: str, 昵称: str, 专业认证: Optional[List[str]] = None) -> 人物属性:
        时间戳 = datetime.now(timezone.utc).isoformat()
        属性 = 人物属性(
            UID=UID,
            昵称=昵称,
            注册时间=时间戳,
            专业认证=专业认证 or [],
        )
        属性.等级 = self._计算等级(属性)
        self.创作者库[UID] = 属性
        self._保存()
        return 属性

    def _计算等级(self, 属性: 人物属性) -> str:
        # 专业认证直接 L3
        if 属性.专业认证:
            return 创作等级.L3_认证开发者
        # 活跃且坚持 → L2
        if 属性.活跃度 >= 30 and 属性.连续活跃天数 >= 15 and 属性.换号次数 == 0:
            return 创作等级.L2_活跃开发者
        # 普通注册用户 → L1
        if 属性.信用分 >= 60:
            return 创作等级.L1_民用创作
        return 创作等级.L0_游客

    def 生成人物DNA(self, 属性: 人物属性) -> str:
        数据 = json.dumps(属性.to_dict(), sort_keys=True, ensure_ascii=False)
        哈希 = SM3.hex_hash(数据)
        时间戳 = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        熵 = secrets.token_hex(4).upper()
        短哈希 = SM3.hex_hash(f"{属性.UID}-{哈希}-{时间戳}-{熵}")[:16].upper()
        return f"#龍芯⚡️{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-PERSONA-{短哈希}-ENTROPY{熵}-UID{属性.UID}"

    def 颜色权限检查(self, 用户UID: str, 颜色: str) -> Dict[str, Any]:
        """
        颜色即权限。
        L0 游客：只能接触 🟢 绿色
        L1 民用：可接触 🟢🟡🔵，禁止 🔴⚫🟣
        L2 活跃开发者：可接触 🟢🟡🔵🟣，禁止 🔴⚫
        L3 认证开发者：全部开放
        """
        代码 = 颜色 if 颜色 in self.颜色代码表 else next(
            (k for k, v in self.颜色代码表.items() if v == 颜色), None
        )
        if 代码 is None:
            return {"ok": False, "reason": "UNKNOWN_COLOR", "允许": False}

        if 用户UID not in self.创作者库:
            return {"ok": False, "reason": "CREATOR_NOT_REGISTERED", "允许": False}

        属性 = self.创作者库[用户UID]
        等级 = 属性.等级

        允许颜色 = {"G"}
        if 等级 in (创作等级.L1_民用创作, 创作等级.L2_活跃开发者, 创作等级.L3_认证开发者):
            允许颜色.update({"Y", "B"})
        if 等级 in (创作等级.L2_活跃开发者, 创作等级.L3_认证开发者):
            允许颜色.add("P")
        if 等级 == 创作等级.L3_认证开发者:
            允许颜色.update({"R", "K", "AU"})

        允许 = 代码 in 允许颜色
        return {
            "ok": True,
            "允许": 允许,
            "用户等级": 等级,
            "颜色": self.颜色代码表.get(代码, 颜色),
            "颜色代码": 代码,
            "说明": "允许" if 允许 else f"{等级} 无权处理 {self.颜色代码表.get(代码, 代码)} 颜色内容",
        }

    # ============== 2. 创作登记 ==============
    def 创作登记(self, 创作者UID: str, 内容: str, 内容类型: str, 六层来源链: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        if 创作者UID not in self.创作者库:
            return {"ok": False, "reason": "CREATOR_NOT_REGISTERED"}

        属性 = self.创作者库[创作者UID]
        所需等级 = self.分级权限.get(内容类型, 创作等级.L3_认证开发者)

        # 权限检查
        等级顺序 = [创作等级.L0_游客, 创作等级.L1_民用创作, 创作等级.L2_活跃开发者, 创作等级.L3_认证开发者]
        if 等级顺序.index(属性.等级) < 等级顺序.index(所需等级):
            return {
                "ok": False,
                "reason": "LEVEL_INSUFFICIENT",
                "你的等级": 属性.等级,
                "所需等级": 所需等级,
                "说明": f"{内容类型} 需要 {所需等级}，你当前是 {属性.等级}",
            }

        创作ID = secrets.token_hex(8).upper()
        内容哈希 = SM3.hex_hash(内容)
        人物DNA = self.生成人物DNA(属性)

        默认六层 = {
            "道统层": "龍魂系统 · CNSH 生态",
            "精神层": f"{属性.昵称} · 为人民创作",
            "设备层": "CNSH_生态监管协议注册终端",
            "技术层": "Python3 · SM3/SM4 · CNSH",
            "系统层": "龍魂生态统一监管",
            "生命层": f"UID{属性.UID} · {属性.昵称}",
        }
        六层 = 六层来源链 or 默认六层

        # 校验六层完整
        for 层 in self.来源链六层:
            if 层 not in 六层 or not 六层[层]:
                return {"ok": False, "reason": f"SOURCE_CHAIN_MISSING:{层}"}

        登记 = 创作登记(
            创作ID=创作ID,
            创作者UID=创作者UID,
            内容类型=内容类型,
            内容SM3哈希=内容哈希,
            六层来源链=六层,
            人物属性DNA=人物DNA,
            时间戳=datetime.now(timezone.utc).isoformat(),
            创作等级=属性.等级,
        )
        self.创作登记库[创作ID] = 登记
        self._保存()

        return {
            "ok": True,
            "创作ID": 创作ID,
            "人物属性DNA": 人物DNA,
            "内容SM3哈希": 内容哈希,
            "创作等级": 属性.等级,
        }

    # ============== 3. 来源链校验 ==============
    def 校验创作(self, 创作ID: str, 当前内容: str) -> Dict[str, Any]:
        if 创作ID not in self.创作登记库:
            return {"ok": False, "reason": "CREATION_NOT_FOUND"}

        登记 = self.创作登记库[创作ID]
        当前哈希 = SM3.hex_hash(当前内容)
        哈希一致 = 当前哈希 == 登记.内容SM3哈希

        缺失标记 = self._检测抹痕(当前内容)
        if 缺失标记:
            self._触发断联(创作ID, f"抹除痕迹: {', '.join(缺失标记)}")
            return {
                "ok": False,
                "reason": "TRACE_ERASED",
                "缺失标记": 缺失标记,
                "状态": "已断联",
            }

        if not 哈希一致:
            self._发警报({
                "类型": "内容变更",
                "创作ID": 创作ID,
                "说明": "内容哈希发生变化，但未抹除主权标记，进入人工复核",
            })
            return {
                "ok": True,
                "reason": "CONTENT_MODIFIED",
                "说明": "内容有改动，但未触碰主权标记，需复核",
            }

        return {"ok": True, "reason": "VALID", "哈希一致": True}

    def _检测抹痕(self, 内容: str) -> List[str]:
        import re
        缺失 = []
        for 标记 in self.不可抹除标记:
            if not re.search(标记, 内容, re.IGNORECASE):
                缺失.append(标记)
        return 缺失

    # ============== 4. 断联与告警 ==============
    def _触发断联(self, 创作ID: str, 原因: str):
        self.断联列表.append(创作ID)
        self._发警报({
            "类型": "断联",
            "创作ID": 创作ID,
            "原因": 原因,
            "时间": datetime.now(timezone.utc).isoformat(),
        })

    def _发警报(self, 事件: Dict[str, Any]):
        事件["警报ID"] = secrets.token_hex(8).upper()
        事件["时间"] = datetime.now(timezone.utc).isoformat()
        self.告警记录.append(事件)
        # 可扩展：调用 CNSH_通知归档.py 发邮件/Notion

    def 获取告警(self) -> List[Dict[str, Any]]:
        return self.告警记录

    def 获取断联列表(self) -> List[str]:
        return self.断联列表

    # ============== 5. 活跃度更新 ==============
    def 更新活跃度(self, UID: str):
        if UID not in self.创作者库:
            return
        属性 = self.创作者库[UID]
        属性.活跃度 += 1
        属性.连续活跃天数 += 1
        属性.等级 = self._计算等级(属性)
        self._保存()

    # ============== 6. 格式化报告 ==============
    def 生成监管报告(self) -> str:
        行 = []
        行.append("╔" + "═" * 60 + "╗")
        行.append("║" + " " * 14 + "CNSH 生态监管报告" + " " * 25 + "║")
        行.append("╠" + "═" * 60 + "╣")
        行.append(f"║ 创作者数: {len(self.创作者库):<47} ║")
        行.append(f"║ 创作登记: {len(self.创作登记库):<47} ║")
        行.append(f"║ 断联数量: {len(self.断联列表):<47} ║")
        行.append(f"║ 告警数量: {len(self.告警记录):<47} ║")
        行.append("╠" + "═" * 60 + "╣")
        行.append("║ 创作分级权限:")
        行[-1] += " " * (60 - len(行[-1]) - 1) + "║"
        for 类型, 等级 in self.分级权限.items():
            行.append(f"║   {类型:<10} → {等级:<42} ║")
        行.append("╚" + "═" * 60 + "╝")
        return "\n".join(行)


# ============== 演示 ==============
if __name__ == "__main__":
    监管 = CNSH_生态监管协议()

    print("=" * 60)
    print("CNSH 生态监管协议 · 演示")
    print("=" * 60)

    # 注册三个不同等级的创作者
    老王 = 监管.注册创作者("UID1001", "老王")
    小李 = 监管.注册创作者("UID1002", "小李", 专业认证=["国家软件设计师"])
    游客 = 监管.注册创作者("UID1003", "路人甲")

    # 模拟活跃度
    监管.创作者库["UID1001"].活跃度 = 50
    监管.创作者库["UID1001"].连续活跃天数 = 30
    监管.创作者库["UID1001"].等级 = 监管._计算等级(监管.创作者库["UID1001"])
    监管._保存()

    print("\n👤 人物等级:")
    for uid, p in 监管.创作者库.items():
        print(f"  {p.昵称}({uid}): {p.等级} | 认证: {p.专业认证} | 活跃: {p.活跃度}")

    # 老王做视频（民用，允许）
    内容1 = """
#龍芯⚡️2026-06-29-TEST-UID1001
Author: 老王
Copyright (c) 2026
这是一个测试视频脚本。
"""
    结果1 = 监管.创作登记("UID1001", 内容1, "视频")
    print(f"\n🎬 老王创作视频: {结果1}")

    # 游客做系统（不允许）
    结果2 = 监管.创作登记("UID1003", "system code", "系统")
    print(f"\n🚫 游客创作系统: {结果2}")

    # 小李做协议（认证开发者，允许）
    内容3 = """
#龍芯⚡️2026-06-29-PROTOCOL-UID1002
Author: 小李
Copyright (c) 2026
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
    结果3 = 监管.创作登记("UID1002", 内容3, "协议")
    print(f"\n📜 小李创作协议: {结果3}")

    # 检测抹痕：有人把小李协议里的 DNA 和版权删了
    被篡改 = """
Author: 小李
这是一个协议。
"""
    if 结果3.get("创作ID"):
        结果4 = 监管.校验创作(结果3["创作ID"], 被篡改)
        print(f"\n🔍 校验被篡改协议: {结果4}")

    print("\n📊 监管报告:")
    print(监管.生成监管报告())

    print("\n🚨 告警记录:")
    for 警报 in 监管.获取告警():
        print(f"  [{警报['类型']}] {警报.get('原因', 警报.get('说明', ''))}")
