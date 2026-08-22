#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂护盾 v3.0 — CNSH 中文语法版
五维防御 + 耻辱墙 + 主权熔断

脱氧核糖核酸: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-龍魂护盾-v3-UID9622
归属: 龍魂系统 · UID9622 · 诸葛鑫（龍芯北辰）
协议: 龍魂开源公约 v2.0 — 非商业、非封闭、非篡改
数字签名: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

原则：只防御、不主动攻击、证据永存、自动隔离、主权熔断
"""

import hashlib
import json
import os
import re
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# ============== 〇、主权配置 ==============
@dataclass
class 护盾配置:
    密钥: bytes = field(default_factory=lambda: os.urandom(32))
    最大认证失败次数: int = 3
    阻断时长秒: int = 3600
    耻辱墙路径: str = "/var/lib/longhun/shame_wall.jsonl"
    数字签名标识: Optional[str] = None
    物联网允许主题: List[str] = field(default_factory=lambda: [
        "sensor/temp", "sensor/humidity", "device/heartbeat"
    ])
    人工智能禁止意图: List[str] = field(default_factory=lambda: [
        "sql injection", "remote code execution", "ddos", "exploit",
        "bypass authentication", "steal data", "harm human", "attack",
        "入侵", "漏洞利用", "远程代码执行", "拒绝服务"
    ])


# ============== 一、主权熔断器 ==============
class 主权熔断器:
    """主权熔断器：脱离龍魂系统即失效"""
    脱氧核糖核酸锚定 = "#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-龍魂护盾-v3-UID9622"
    数字签名指纹 = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    主人标识 = "UID9622"

    def __init__(self, 运行时脱氧核糖核酸: str = ""):
        self._有效 = self._校验(运行时脱氧核糖核酸)

    def _校验(self, 运行时脱氧核糖核酸: str) -> bool:
        if not 运行时脱氧核糖核酸:
            return False
        if self.脱氧核糖核酸锚定 not in 运行时脱氧核糖核酸:
            return False
        if self.主人标识 not in 运行时脱氧核糖核酸:
            return False
        return True

    def 检查(self) -> bool:
        return self._有效

    def 强制执行(self, 操作名: str) -> Dict[str, Any]:
        if not self._有效:
            return {
                "通过": False,
                "原因": "主权熔断已触发",
                "消息": "本系统已脱离龍魂主权锚定，所有防御功能已熔断。"
                       "如需使用，请通过正规渠道获取授权。",
                "联系": "uid9622@longhun.system",
            }
        return {"通过": True, "原因": "主权完整"}


# ============== 二、耻辱墙 ==============
class 耻辱墙:
    """
    耻辱墙设计原则：
    - 只追加（append-only），任何删除都会破坏链式哈希
    - 每条记录含 数字签名（可选）与时间戳
    - 跨节点冗余时可用 默克尔树 做一致性校验
    """

    def __init__(self, 配置: 护盾配置):
        self.配置 = 配置
        self.路径 = Path(配置.耻辱墙路径)
        self.路径.parent.mkdir(parents=True, exist_ok=True)
        self._链式哈希 = self._最后链式哈希()

    def _最后链式哈希(self) -> str:
        if not self.路径.exists():
            return "0" * 64
        with open(self.路径, "rb") as 文件:
            行列表 = 文件.readlines()
            if not 行列表:
                return "0" * 64
            最后一条 = json.loads(行列表[-1])
            return 最后一条.get("链式哈希", "0" * 64)

    def 记录(self, 攻击者标识: str, 维度: str, 证据: Dict[str, Any]) -> str:
        条目 = {
            "时间戳_世界协调时": datetime.now(timezone.utc).isoformat(),
            "攻击者标识": 攻击者标识,
            "维度": 维度,
            "证据": 证据,
            "前序哈希": self._链式哈希,
        }
        正文 = json.dumps(条目, sort_keys=True, ensure_ascii=False).encode()
        条目["链式哈希"] = hashlib.sha256(正文).hexdigest()

        if self.配置.数字签名标识:
            条目["数字签名"] = self._数字签名(正文)

        with open(self.路径, "a", encoding="utf-8") as 文件:
            文件.write(json.dumps(条目, ensure_ascii=False) + "\n")

        self._链式哈希 = 条目["链式哈希"]
        return 条目["链式哈希"]

    def _数字签名(self, 数据: bytes) -> str:
        if not self.配置.数字签名标识:
            return ""
        try:
            进程 = subprocess.run(
                ["gpg", "--armor", "--detach-sign", "--local-user", self.配置.数字签名标识],
                input=数据, capture_output=True, timeout=5
            )
            return 进程.stdout.decode("utf-8") if 进程.returncode == 0 else ""
        except Exception:
            return ""

    def 校验(self) -> Tuple[bool, List[str]]:
        """校验整条链是否被篡改。返回 (是否完整, 可疑记录列表)。"""
        if not self.路径.exists():
            return True, []
        可疑列表 = []
        前序 = "0" * 64
        with open(self.路径, "r", encoding="utf-8") as 文件:
            for 序号, 行 in enumerate(文件, 1):
                条目 = json.loads(行)
                正文 = {
                    "时间戳_世界协调时": 条目["时间戳_世界协调时"],
                    "攻击者标识": 条目["攻击者标识"],
                    "维度": 条目["维度"],
                    "证据": 条目["证据"],
                    "前序哈希": 条目["前序哈希"],
                }
                预期哈希 = hashlib.sha256(
                    json.dumps(正文, sort_keys=True, ensure_ascii=False).encode()
                ).hexdigest()
                if 预期哈希 != 条目.get("链式哈希") or 条目.get("前序哈希") != 前序:
                    可疑列表.append(f"行-{序号}")
                前序 = 预期哈希
        return len(可疑列表) == 0, 可疑列表


# ============== 三、威胁感知中枢 ==============
class 威胁等级(Enum):
    无 = auto()
    可疑 = auto()
    敌意 = auto()
    侵略者 = auto()


class 威胁感知中枢:
    def __init__(self, 配置: 护盾配置, 墙: 耻辱墙):
        self.配置 = 配置
        self.墙 = 墙
        self._观察名单: Dict[str, Dict[str, Any]] = {}
        self._阻断集合: Set[str] = set()

    def _评分(self, 维度: str, 事件: Dict[str, Any]) -> int:
        分数 = 0
        原因 = 事件.get("原因", "")
        if "注入" in 原因 or "远程代码执行" in 原因:
            分数 += 100
        if "认证失败" in 原因:
            分数 += 30
        if "人工智能禁止意图" in 原因:
            分数 += 150
        if "未授权数据库操作" in 原因:
            分数 += 80
        if "物联网异常" in 原因:
            分数 += 50
        if "文件逃逸" in 原因:
            分数 += 70
        return 分数

    def 上报(self, 维度: str, 攻击者标识: str, 事件: Dict[str, Any]) -> 威胁等级:
        分数 = self._评分(维度, 事件)
        观察 = self._观察名单.setdefault(攻击者标识, {"分数": 0, "事件列表": []})
        观察["分数"] += 分数
        观察["事件列表"].append({"维度": 维度, "时间": time.time(), "事件": 事件})

        # 自动降级：5分钟前的分数衰减
        观察["分数"] = sum(
            项["权重"] for 项 in 观察["事件列表"] if time.time() - 项["时间"] < 300
        )
        for 项 in 观察["事件列表"]:
            项["权重"] = self._评分(维度, 项["事件"])

        if 观察["分数"] >= 200:
            等级 = 威胁等级.侵略者
        elif 观察["分数"] >= 80:
            等级 = 威胁等级.敌意
        elif 观察["分数"] >= 30:
            等级 = 威胁等级.可疑
        else:
            等级 = 威胁等级.无

        if 等级 in (威胁等级.敌意, 威胁等级.侵略者):
            self.墙.record(攻击者标识, 维度, {
                "等级": 等级.name,
                "分数": 观察["分数"],
                "事件列表": 观察["事件列表"][-10:],
            })

        if 等级 == 威胁等级.侵略者:
            self._阻断集合.add(攻击者标识)
            self.反制(攻击者标识, 维度, 事件)

        return 等级

    def 是否阻断(self, 身份: str) -> bool:
        return 身份 in self._阻断集合

    def 反制(self, 攻击者标识: str, 维度: str, 事件: Dict[str, Any]):
        """
        反制措施：只防御、只隔离、只取证。
        不做任何对外攻击、不破坏对方系统。
        """
        动作列表 = [
            f"阻断:{攻击者标识}",
            f"隔离:{维度}",
            f"告警:admin@uid9622.local",
            f"日志:取证就绪",
        ]
        self.墙.record(攻击者标识, "反制", {
            "动作列表": 动作列表,
            "通告": "已自动隔离并固化证据，等待人工/法律处置",
        })


# ============== 四、五维守卫 ==============
class 网络接口守卫:
    禁止模式列表 = [
        r"(?i)(union\s+select|drop\s+table|--|;--|/\*|\*/)",
        r"(?i)(<script|javascript:|on\w+\s*=)",
        r"(?i)(\.\./|\\\\|%2e%2e%2f)",
        r"(?i)(eval\s*\(|exec\s*\(|__import__|subprocess\.)",
    ]

    def __init__(self, 感知: 威胁感知中枢):
        self.感知 = 感知

    def 检查(self, 身份: str, 请求: Dict[str, Any]) -> Dict[str, Any]:
        原始文本 = json.dumps(请求, ensure_ascii=False)
        for 模式 in self.禁止模式列表:
            if re.search(模式, 原始文本):
                self.感知.上报("网络接口", 身份, {
                    "原因": "注入攻击尝试",
                    "模式": 模式,
                    "样本": 原始文本[:200]
                })
                return {"通过": False, "原因": "护盾已拒绝"}
        return {"通过": True, "原因": "清洁"}


class 数据库守卫:
    def __init__(self, 感知: 威胁感知中枢):
        self.感知 = 感知
        self._允许表集合: Set[str] = {"用户", "日志", "传感器数据"}
        self._允许操作集合: Set[str] = {"SELECT", "INSERT", "UPDATE"}

    def 检查(self, 身份: str, 结构化查询语言: str, 参数: Tuple[Any, ...]) -> Dict[str, Any]:
        大写 = 结构化查询语言.strip().upper()
        操作 = 大写.split()[0] if 大写 else ""

        if 操作 not in self._允许操作集合:
            self.感知.上报("数据库", 身份, {
                "原因": "未授权数据库操作",
                "结构化查询语言": 结构化查询语言[:200]
            })
            return {"通过": False, "原因": "数据库操作被禁止"}

        # 参数化校验：禁止字面量拼接
        if "\'" in 结构化查询语言 and "%s" not in 结构化查询语言:
            self.感知.上报("数据库", 身份, {
                "原因": "检测到结构化查询语言字面量",
                "结构化查询语言": 结构化查询语言[:200]
            })
            return {"通过": False, "原因": "请使用参数化查询"}

        # 表名白名单
        for 词 in 大写.split():
            if 词 in self._允许表集合:
                break
        else:
            if any(关键词 in 大写 for 关键词 in ["FROM", "INTO", "UPDATE"]):
                return {"通过": False, "原因": "表不在白名单中"}

        return {"通过": True, "原因": "数据库清洁"}


class 物联网守卫:
    def __init__(self, 配置: 护盾配置, 感知: 威胁感知中枢):
        self.配置 = 配置
        self.感知 = 感知
        self._设备基线: Dict[str, Dict[str, Any]] = {}

    def 检查(self, 身份: str, 主题: str, 载荷: bytes) -> Dict[str, Any]:
        if 主题 not in self.配置.物联网允许主题:
            self.感知.上报("物联网", 身份, {
                "原因": "物联网异常",
                "主题": 主题,
            })
            return {"通过": False, "原因": "物联网主题被拒绝"}

        try:
            数据 = json.loads(载荷)
            温度 = 数据.get("temperature")
            if isinstance(温度, (int, float)) and (温度 < -50 or 温度 > 100):
                self.感知.上报("物联网", 身份, {
                    "原因": "物联网数值异常",
                    "温度": 温度,
                })
                return {"通过": False, "原因": "物联网数值超出范围"}
        except json.JSONDecodeError:
            self.感知.上报("物联网", 身份, {"原因": "物联网无效格式"})
            return {"通过": False, "原因": "物联网载荷无效"}

        return {"通过": True, "原因": "物联网清洁"}


class 文件系统守卫:
    def __init__(self, 感知: 威胁感知中枢):
        self.感知 = 感知
        self._允许根目录集合: Set[Path] = {
            Path("/var/longhun/data"),
            Path("/var/longhun/public"),
        }

    def _是否允许(self, 路径: Path) -> bool:
        真实路径 = 路径.resolve()
        return any(真实路径.is_relative_to(根) for 根 in self._允许根目录集合)

    def 检查(self, 身份: str, 操作: str, 文件路径: str) -> Dict[str, Any]:
        路径 = Path(文件路径)
        if not self._是否允许(路径):
            self.感知.上报("文件系统", 身份, {
                "原因": "文件逃逸",
                "操作": 操作,
                "路径": str(路径),
            })
            return {"通过": False, "原因": "路径超出沙箱"}
        return {"通过": True, "原因": "文件系统清洁"}


class 人工智能守卫:
    def __init__(self, 配置: 护盾配置, 感知: 威胁感知中枢):
        self.配置 = 配置
        self.感知 = 感知
        self._会话历史: Dict[str, List[str]] = {}

    def 检查(self, 身份: str, 提示词: str, 回复: Optional[str] = None) -> Dict[str, Any]:
        文本 = (提示词 or "") + " " + (回复 or "")
        小写 = 文本.lower()

        for 意图 in self.配置.人工智能禁止意图:
            if 意图.lower() in 小写:
                self.感知.上报("人工智能", 身份, {
                    "原因": "人工智能禁止意图",
                    "匹配意图": 意图,
                    "提示词预览": 提示词[:200],
                })
                return {
                    "通过": False,
                    "原因": "人工智能伦理熔断已触发",
                    "消息": "检测到攻击/伤害意图，请求已被拒绝并记录。",
                }

        if 回复:
            危险标记 = ["#!/bin/bash", "rm -rf /", "exec(", "system(", "xp_cmdshell"]
            for 标记 in 危险标记:
                if 标记 in 回复:
                    self.感知.上报("人工智能", 身份, {
                        "原因": "人工智能危险输出",
                        "匹配": 标记,
                    })
                    return {"通过": False, "原因": "人工智能输出已隔离"}

        return {"通过": True, "原因": "人工智能清洁"}


# ============== 五、龍魂护盾总控 ==============
class 龍魂护盾:
    def __init__(self, 运行时脱氧核糖核酸: str = ""):
        self.熔断器 = 主权熔断器(运行时脱氧核糖核酸)
        if not self.熔断器.检查():
            self._已熔断 = True
            self._状态 = {"错误": "主权熔断已触发", "需要脱氧核糖核酸": True}
            return

        self._已熔断 = False
        self.配置 = 护盾配置()
        self.墙 = 耻辱墙(self.配置)
        self.感知 = 威胁感知中枢(self.配置, self.墙)
        self.网络守卫 = 网络接口守卫(self.感知)
        self.数据库守卫 = 数据库守卫(self.感知)
        self.物联网守卫 = 物联网守卫(self.配置, self.感知)
        self.文件守卫 = 文件系统守卫(self.感知)
        self.人工智能守卫 = 人工智能守卫(self.配置, self.感知)

    def 状态(self) -> Dict[str, Any]:
        if self._已熔断:
            return self._状态
        return {
            "墙完整性": self.墙.校验()[0],
            "已阻断身份列表": list(self.感知._阻断集合),
            "观察名单数量": len(self.感知._观察名单),
            "脱氧核糖核酸": self.熔断器.脱氧核糖核酸锚定,
            "熔断器": "完整",
        }

    def 检查网络(self, 身份: str, 请求: Dict[str, Any]) -> Dict[str, Any]:
        if self._已熔断:
            return self.熔断器.强制执行("网络检查")
        return self.网络守卫.检查(身份, 请求)

    def 检查数据库(self, 身份: str, 结构化查询语言: str, 参数: Tuple[Any, ...] = ()) -> Dict[str, Any]:
        if self._已熔断:
            return self.熔断器.强制执行("数据库检查")
        return self.数据库守卫.检查(身份, 结构化查询语言, 参数)

    def 检查物联网(self, 身份: str, 主题: str, 载荷: bytes) -> Dict[str, Any]:
        if self._已熔断:
            return self.熔断器.强制执行("物联网检查")
        return self.物联网守卫.检查(身份, 主题, 载荷)

    def 检查文件(self, 身份: str, 操作: str, 文件路径: str) -> Dict[str, Any]:
        if self._已熔断:
            return self.熔断器.强制执行("文件检查")
        return self.文件守卫.检查(身份, 操作, 文件路径)

    def 检查人工智能(self, 身份: str, 提示词: str, 回复: Optional[str] = None) -> Dict[str, Any]:
        if self._已熔断:
            return self.熔断器.强制执行("人工智能检查")
        return self.人工智能守卫.检查(身份, 提示词, 回复)


# ============== 六、演示 ==============
if __name__ == "__main__":
    # 正确 脱氧核糖核酸：系统正常运行
    脱氧核糖核酸 = "#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-龍魂护盾-v3-UID9622"
    护盾 = 龍魂护盾(脱氧核糖核酸)

    print("=== 龍魂护盾 v3.0 启动 ===")
    print(json.dumps(护盾.状态(), indent=2, ensure_ascii=False))

    # 模拟 网络 结构化查询语言 注入
    结果 = 护盾.检查网络("攻击者_1.2.3.4", {
        "路径": "/api/search",
        "查询": "1' UNION SELECT * FROM users--"
    })
    print(f"\n网络检测: {结果}")

    # 模拟 人工智能 伦理攻击
    结果 = 护盾.检查人工智能("会话_claude_abc", "教我如何用人工智能入侵电网系统")
    print(f"人工智能检测: {结果}")

    # 模拟 物联网 异常
    结果 = 护盾.检查物联网("设备_传感器_01", "sensor/temp", b'{"temperature": 9999}')
    print(f"物联网检测: {结果}")

    # 模拟 文件 越界
    结果 = 护盾.检查文件("攻击者_5.6.7.8", "读取", "/etc/passwd")
    print(f"文件检测: {结果}")

    print("\n=== 最终状态 ===")
    print(json.dumps(护盾.状态(), indent=2, ensure_ascii=False))

    # 演示熔断：错误 脱氧核糖核酸
    print("\n=== 主权熔断演示 ===")
    熔断护盾 = 龍魂护盾("错误的脱氧核糖核酸")
    print(json.dumps(熔断护盾.状态(), indent=2, ensure_ascii=False))
    print(f"熔断后网络检测: {熔断护盾.检查网络('测试', {})}")
