#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 CNSH 统一语法兼容层
DNA: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-CNSH-UNIFIED-v1.0

把全机龍魂模块里乱七八糟的变量名、函数名、配置键，统一成 CNSH 中文母语命名。
老代码可以逐步迁移，新代码直接从这里 import。
"""
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ============================================================
# 一、路径/目录（统一项目根目录与工作目录概念）
# ============================================================

class 系统路径:
    """统一所有模块的路径变量"""

    @staticmethod
    def 用户主目录() -> Path:
        return Path.home()

    @staticmethod
    def 龍魂系统根目录() -> Path:
        return Path.home() / "longhun-system"

    @staticmethod
    def 龍魂配置目录() -> Path:
        return Path.home() / ".龍魂"

    @staticmethod
    def 龍魂长记忆目录() -> Path:
        return Path.home() / ".longhun"

    @staticmethod
    def 工作数据目录() -> Path:
        return Path.home() / "_work"

    @staticmethod
    def CNSH核心目录() -> Path:
        return 系统路径.龍魂系统根目录() / "cnsh-core"


# 兼容旧变量名（老代码可以直接 import 这些）
PROJECT_ROOT = 系统路径.龍魂系统根目录()
BASE_DIR = 系统路径.龍魂系统根目录()
HOME_DIR = Path.home()
LONGHUN_ROOT = 系统路径.龍魂系统根目录()
WORK_DIR = 系统路径.工作数据目录()


# ============================================================
# 二、DNA 追溯码（统一生成器与格式）
# ============================================================

class DNA工具:
    """
    统一 DNA 生成、校验、解析
    DNA: #龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-CNSH-UNIFIED-繁简归一-v1.1
    🔄 繁简归一更新：简/繁等价接收，自动归一化为标准形式，不熔断
    """

    标准前缀 = "#龍芯⚡️"
    简化字前缀 = "#龍芯⚡️"  # 兼容接收，自动归一
    # 推荐格式同时匹配繁/简，可选哈希后缀
    推荐格式 = re.compile(
        r"^#[龍龍]芯⚡️(?P<日期>\d{4}-\d{2}-\d{2})-(?P<模块>[A-Za-z0-9_\u4e00-\u9fa5]+)-v(?P<版本>\d+\.\d+\.?\d*)(?:-(?P<哈希>[A-Fa-f0-9]{8}))?$"
    )

    @staticmethod
    def 生成(模块名: str, 版本: str = "1.0", 时间: datetime | None = None) -> str:
        时间 = 时间 or datetime.now(timezone.utc)
        日期 = 时间.strftime("%Y-%m-%d")
        时间戳 = 时间.strftime("%Y%m%d%H%M%S")
        哈希 = hashlib.sha256(
            f"{时间戳}-{模块名}-{版本}".encode("utf-8")
        ).hexdigest()[:8].upper()
        return f"{DNA工具.标准前缀}{日期}-{模块名}-v{版本}-{哈希}"

    @staticmethod
    def 校验(dna: str) -> dict[str, Any]:
        if not isinstance(dna, str):
            return {"合法": False, "原因": "DNA 必须是字符串"}
        # 🔄 繁简归一：简体前缀自动归一，视为合法
        _working = dna
        if _working.startswith(DNA工具.简化字前缀):
            _working = DNA工具.规范化(_working)
        if not _working.startswith(DNA工具.标准前缀):
            return {"合法": False, "原因": "缺少标准前缀 #龍芯⚡️（或等价简写 #龍芯⚡️）"}
        m = DNA工具.推荐格式.match(_working) or DNA工具.推荐格式.match(dna)
        if m:
            return {"合法": True, "推荐": True, "解析": m.groupdict(), "已归一": _working if _working != dna else None}
        return {"合法": True, "推荐": False, "原因": "格式不是推荐形式"}

    @staticmethod
    def 规范化(dna: str) -> str:
        """繁简归一：简体前缀统一转为繁体，保持系统内一致性"""
        return dna.replace("#龍芯⚡️", DNA工具.标准前缀).replace("#龍魂", "龍魂").replace("龍魂", "龍魂")


# 兼容旧函数名
def 生成DNA(模块名: str, 版本: str = "1.0") -> str:
    return DNA工具.生成(模块名, 版本)


def DNA校验(dna: str) -> dict[str, Any]:
    return DNA工具.校验(dna)


# ============================================================
# 三、数字根与三色审计（统一函数名）
# ============================================================

class 数学工具:
    @staticmethod
    def 计算数字根(内容: int | str) -> int:
        if isinstance(内容, int):
            n = 内容
        else:
            try:
                n = int(re.sub(r"[^0-9]", "", str(内容)) or "0")
            except Exception:
                n = 0
        if n == 0:
            return 0
        while n >= 10:
            n = sum(int(d) for d in str(n))
        return n

    @staticmethod
    def 文本数字根(文本: str) -> dict[str, Any]:
        数字 = re.sub(r"[^0-9]", "", str(文本))
        if not 数字:
            return {"数字根": 0, "数字序列": "", "原始": 文本}
        return {
            "数字根": 数学工具.计算数字根(int(数字)),
            "数字序列": 数字,
            "原始": 文本,
        }

    @staticmethod
    def 数字根转五行(数字根: int) -> str:
        映射 = {0: "土", 1: "水", 2: "火", 3: "木", 4: "金", 5: "土", 6: "水", 7: "火", 8: "木", 9: "金"}
        return 映射.get(数字根 % 10, "土")

    @staticmethod
    def 数字根闸门(数字根: int) -> str:
        if 数字根 in (3, 6, 9):
            return "🟢"
        elif 数字根 in (1, 2, 4, 5, 7, 8):
            return "🟡"
        return "🔴"


class 审计工具:
    @staticmethod
    def 三色审计(分数: float) -> str:
        if 分数 >= 8.0:
            return "🟢"
        elif 分数 >= 5.0:
            return "🟡"
        return "🔴"

    @staticmethod
    def 三色状态(状态: str) -> str:
        if 状态 in ("pass", "ok", "green", "通过", "正常"):
            return "🟢"
        elif 状态 in ("warn", "warning", "yellow", "警告", "风险"):
            return "🟡"
        return "🔴"


# 兼容旧函数名
def 计算数字根(内容: int | str) -> int:
    return 数学工具.计算数字根(内容)


def 数字根转五行(数字根: int) -> str:
    return 数学工具.数字根转五行(数字根)


def 数字根闸门(数字根: int) -> str:
    return 数学工具.数字根闸门(数字根)


def 三色审计(分数: float) -> str:
    return 审计工具.三色审计(分数)


# ============================================================
# 四、配置键统一（JSON/字典键名映射）
# ============================================================

class 配置键统一:
    """把各种中英文混用的配置键映射到 CNSH 标准键"""

    标准映射 = {
        # DNA
        "DNA": "dna追溯码",
        "dna": "dna追溯码",
        "_dna": "dna追溯码",
        "__dna__": "dna追溯码",
        "dna_code": "dna追溯码",
        # 确认
        "CONFIRM": "确认码",
        "confirm": "确认码",
        "seal": "封印码",
        "SEAL": "封印码",
        # 基础
        "name": "名称",
        "version": "版本",
        "status": "状态",
        "category": "类别",
        "description": "描述",
        # 路径
        "path": "路径",
        "base_dir": "基础目录",
        "project_root": "项目根目录",
        "work_dir": "工作目录",
        "home_dir": "用户主目录",
    }

    @classmethod
    def 标准化字典(cls, 数据: dict[str, Any]) -> dict[str, Any]:
        return {cls.标准映射.get(k, k): v for k, v in 数据.items()}

    @classmethod
    def 还原英文键(cls, 数据: dict[str, Any]) -> dict[str, Any]:
        反向 = {v: k for k, v in cls.标准映射.items()}
        return {反向.get(k, k): v for k, v in 数据.items()}


# ============================================================
# 五、龍/龍规范化 · 繁简归一 v1.1
# 🔄 DNA: #龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-CNSH-UNIFIED-繁简归一-v1.1
# 策略：繁体为规范形式，简体等价接收 · 自动归一 · 不熔断
# ============================================================

class 文字规范:
    @staticmethod
    def 繁体龍(文本: str) -> str:
        """归一化：简体→繁体，保证系统内一致性"""
        return str(文本).replace("龍芯", "龍芯").replace("龍魂", "龍魂")

    @staticmethod
    def 检查简化字(文本: str) -> list[str]:
        """
        🔄 繁简归一更新：简体词不再视为违规。
        此方法仅用于统计/审计记录，不触发熔断或报错。
        返回：检测到的简化词列表（仅供参考）
        """
        命中 = []
        for 词 in ["龍芯", "龍魂"]:
            if 词 in str(文本):
                命中.append(词)
        return 命中

    @staticmethod
    def 繁简等价(文本1: str, 文本2: str) -> bool:
        """判断两个字符串在忽略繁简差异后是否等价"""
        return 文字规范.繁体龍(文本1) == 文字规范.繁体龍(文本2)


# ============================================================
# 六、CNSH 公开内容统一接口
# ============================================================

class 公开内容:
    """扫描并规范化对外公开的内容（DNA、龍字、配置键）· 繁简归一"""

    @staticmethod
    def 扫描文件(路径: Path) -> dict[str, Any]:
        文本 = Path(路径).read_text(encoding="utf-8", errors="ignore")
        return {
            "路径": str(路径),
            "简化字统计": 文字规范.检查简化字(文本),  # 仅统计，不报错
            "dna数量": len(re.findall(r"#[龍龍]芯⚡️[^\s\"'<>]+", 文本)),
            "推荐dna数量": len(DNA工具.推荐格式.findall(文本)),
        }

    @staticmethod
    def 规范化文件(路径: Path, 输出路径: Path | None = None) -> Path:
        原文件 = Path(路径)
        文本 = 原文件.read_text(encoding="utf-8", errors="ignore")
        # 🔄 繁简归一：简化字 → 繁体（保持系统内一致）
        文本 = 文字规范.繁体龍(文本)
        # DNA 前缀规范化
        文本 = DNA工具.规范化(文本)
        目标 = 输出路径 or 原文件
        目标.write_text(文本, encoding="utf-8")
        return 目标


# ============================================================
# 七、统一入口
# ============================================================

if __name__ == "__main__":
    print("龍魂 CNSH 统一语法兼容层")
    print(f"项目根目录: {系统路径.龍魂系统根目录()}")
    print(f"DNA 示例: {DNA工具.生成('测试模块', '1.0')}")
    print(f"数字根(9622): {数学工具.计算数字根('9622')}")
    print(f"三色审计(8.5): {审计工具.三色审计(8.5)}")
