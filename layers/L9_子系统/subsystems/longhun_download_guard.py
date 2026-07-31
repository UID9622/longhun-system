# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂下载守卫 — 文件下载自动检测 + 隔离 + 告警
DNA: #龍芯⚡️2026-06-29-LONGHUN-DOWNLOAD-GUARD-v1.0
原则：任何进入系统的文件，先过护盾，再让用户打开
"""

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from longhun_shield_cnsh import 龍魂护盾


class 下载文件检测器:
    """对单个下载文件做静态检测：扩展名、内容模式、AI 语义。"""

    危险扩展名 = {
        ".exe", ".scr", ".bat", ".cmd", ".com", ".pif", ".vbs",
        ".js", ".jse", ".wsf", ".wsh", ".hta", ".sh", ".bash",
        ".app", ".pkg", ".msi", ".deb", ".rpm"
    }

    文本扩展名 = {
        ".txt", ".md", ".markdown", ".py", ".js", ".sh", ".bash",
        ".sql", ".json", ".yaml", ".yml", ".html", ".htm", ".xml",
        ".csv", ".log", ".prompt", ".ini", ".conf", ".cfg"
    }

    可疑模式 = [
        (r"#!/bin/(?:ba)?sh", "shell脚本"),
        (r"rm\s+-rf\s+/", "危险删除命令"),
        (r"curl\s+[^|]+\|\s*(ba)?sh", "curl管道执行"),
        (r"eval\s*\(", "动态执行"),
        (r"exec\s*\(", "进程执行"),
        (r"os\.system", "系统调用"),
        (r"subprocess\.call|subprocess\.run|subprocess\.Popen", "子进程"),
        (r"__import__\s*\(", "动态导入"),
        (r"<script[^>]*>.*?</script>", "脚本标签"),
        (r"javascript:", "JS协议"),
        (r"(?i)(union\s+select|drop\s+table|exec\s*\(|--|;--)", "注入特征"),
        (r"Invoke-Expression|IEX", "PowerShell执行"),
        (r"base64\s+-d\s*\|", "base64解码执行"),
        (r"chmod\s+\+x", "添加执行权限"),
        # LU v3.0 L0 禁止规则
        (r"(?i)(overwrite\s+memory|覆盖记忆)", "LU禁止规则：覆盖记忆"),
        (r"(?i)(delete\s+audit\s+log|删除审计日志)", "LU禁止规则：删除审计日志"),
        (r"(?i)(remove\s+DNA|移除DNA)", "LU禁止规则：移除DNA"),
        (r"(?i)(hidden\s+rewrite|隐性重写)", "LU禁止规则：隐性重写"),
        (r"(?i)(绕过验证门|bypass\s+verification\s+gate)", "LU禁止规则：绕过验证门"),
    ]

    def __init__(self, 护盾: 龍魂护盾):
        self.护盾 = 护盾

    def 检测(self, 文件路径: Path) -> Dict[str, Any]:
        if getattr(self.护盾, "_已熔断", False):
            return {"通过": False, "原因": "主权熔断已触发"}

        结果 = {"通过": True, "原因": "干净", "风险项": []}
        后缀 = 文件路径.suffix.lower()
        是文本 = 后缀 in self.文本扩展名

        # 1. 扩展名检查
        if 后缀 in self.危险扩展名:
            结果["通过"] = False
            结果["风险项"].append(f"危险扩展名：{文件路径.suffix}")

        # 2. 内容扫描（仅文本文件，避免二进制误报）
        if 是文本:
            内容样本 = self._读取样本(文件路径)
            if 内容样本:
                for 模式, 名称 in self.可疑模式:
                    if re.search(模式, 内容样本, re.IGNORECASE):
                        结果["通过"] = False
                        结果["风险项"].append(名称)

                # 3. AI 语义检查（仅脚本/提示类文本）
                if 后缀 in {".txt", ".prompt", ".md"}:
                    ai结果 = self.护盾.检查人工智能(
                        f"download_scan:{文件路径.name}", 内容样本[:2000]
                    )
                    if not ai结果.get("通过"):
                        结果["通过"] = False
                        结果["风险项"].append(f"AI语义熔断：{ai结果.get('原因')}")

        if not 结果["通过"]:
            结果["原因"] = "；".join(结果["风险项"])
        return 结果

    @staticmethod
    def _读取样本(文件路径: Path, 最大字节: int = 32768) -> str:
        try:
            with open(文件路径, "rb") as f:
                raw = f.read(最大字节)
            # 先尝试 UTF-8，失败则忽略非法字节
            return raw.decode("utf-8", errors="ignore")
        except Exception:
            return ""


class 下载隔离区:
    def __init__(self, 隔离目录: Path):
        self.隔离目录 = 隔离目录
        self.隔离目录.mkdir(parents=True, exist_ok=True)

    def 隔离(self, 原路径: Path, 原因: str) -> Path:
        时间戳 = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        新名 = f"{原路径.stem}_{时间戳}_{原因[:30]}{原路径.suffix}"
        新名 = re.sub(r"[^\w\-.]", "_", 新名)
        目标 = self.隔离目录 / 新名
        try:
            shutil.move(str(原路径), str(目标))
        except Exception:
            # 跨设备或权限问题则复制后删除
            shutil.copy2(str(原路径), str(目标))
            原路径.unlink()
        return 目标


class 下载目录看守:
    """
    轮询式目录看守。不依赖 watchdog，纯标准库即可运行。
    """

    def __init__(self, 护盾: 龍魂护盾, 检测器: 下载文件检测器,
                 隔离区: 下载隔离区, 看守目录列表: List[Path],
                 轮询间隔秒: float = 2.0, 稳定轮次: int = 2):
        self.护盾 = 护盾
        self.检测器 = 检测器
        self.隔离区 = 隔离区
        self.看守目录列表 = 看守目录列表
        self.轮询间隔秒 = 轮询间隔秒
        self.稳定轮次 = 稳定轮次
        self._状态: Dict[Path, Tuple[int, float, int]] = {}
        self._已处理: Set[Path] = set()
        self._运行中 = False
        self._已初始化基线 = False

    def _列出文件(self) -> List[Path]:
        文件列表 = []
        for 目录 in self.看守目录列表:
            if not 目录.exists():
                continue
            for 项 in 目录.iterdir():
                if 项.is_file() and not 项.name.startswith("."):
                    文件列表.append(项)
        return 文件列表

    def _更新状态(self, 文件列表: List[Path]):
        新状态 = {}
        for 文件 in 文件列表:
            try:
                stat = 文件.stat()
                大小, mtime = stat.st_size, stat.st_mtime
            except Exception:
                continue
            旧 = self._状态.get(文件)
            if 旧 and 旧[0] == 大小 and 旧[1] == mtime:
                计数 = 旧[2] + 1
            else:
                计数 = 0
            新状态[文件] = (大小, mtime, 计数)
        self._状态 = 新状态

    def _处理(self, 文件: Path):
        if 文件 in self._已处理:
            return
        self._已处理.add(文件)

        print(f"[下载守卫] 检测到新文件：{文件}")
        结果 = self.检测器.检测(文件)

        if 结果["通过"]:
            print(f"[下载守卫] 干净：{文件.name}")
            return

        # 记录到耻辱墙并告警
        self.护盾.感知.上报("download", 文件.name, {
            "原因": "下载文件可疑",
            "路径": str(文件),
            "风险项": 结果["风险项"],
        })

        # 隔离
        隔离路径 = self.隔离区.隔离(文件, "QUARANTINED")
        print(f"[下载守卫] 已隔离至：{隔离路径}")

    def 扫描一次(self):
        文件列表 = self._列出文件()
        self._更新状态(文件列表)
        if not self._已初始化基线:
            # 第一次扫描只建立基线，不处理历史文件
            self._已处理.update(文件列表)
            self._已初始化基线 = True
            print(f"[下载守卫] 已建立基线，忽略 {len(文件列表)} 个历史文件")
            return
        for 文件 in 文件列表:
            大小, mtime, 计数 = self._状态.get(文件, (0, 0, 0))
            if 计数 >= self.稳定轮次 and 文件 not in self._已处理:
                self._处理(文件)

    def 启动(self):
        self._运行中 = True
        print(f"[下载守卫] 启动，看守目录：{self.看守目录列表}")
        print(f"[下载守卫] 隔离目录：{self.隔离区.隔离目录}")
        while self._运行中:
            try:
                self.扫描一次()
            except Exception as e:
                print(f"[下载守卫] 扫描异常：{e}")
            time.sleep(self.轮询间隔秒)

    def 停止(self):
        self._运行中 = False


def 扫描指定路径(路径: Path, 护盾: 龍魂护盾) -> Dict[str, Any]:
    隔离目录 = Path(os.environ.get(
        "LONGHUN_QUARANTINE_DIR",
        str(Path.home() / ".longhun" / "quarantine")
    ))
    检测器 = 下载文件检测器(护盾)
    隔离区 = 下载隔离区(隔离目录)
    结果 = 检测器.检测(路径)
    if not 结果["通过"]:
        隔离路径 = 隔离区.隔离(路径, "MANUAL_SCAN")
        护盾.感知.上报("download", 路径.name, {
            "原因": "手动扫描发现风险",
            "风险项": 结果["风险项"],
        })
        return {**结果, "隔离路径": str(隔离路径)}
    return 结果


def 主函数():
    解析器 = argparse.ArgumentParser(description="龍魂下载守卫")
    解析器.add_argument("--watch", action="store_true", help="启动目录看守")
    解析器.add_argument("--scan", type=str, help="扫描指定文件或目录")
    参数 = 解析器.parse_args()

    脱氧核糖核酸 = os.environ.get(
        "LONGHUN_SHIELD_DNA",
        "#龍芯⚡️2026-06-29-龍魂护盾-v3-CNSH-UID9622"
    )
    护盾 = 龍魂护盾(脱氧核糖核酸)

    if getattr(护盾, "_已熔断", False):
        print(json.dumps(护盾.状态(), indent=2, ensure_ascii=False))
        sys.exit(1)

    if 参数.scan:
        目标 = Path(参数.scan)
        if 目标.is_file():
            print(json.dumps(扫描指定路径(目标, 护盾), indent=2, ensure_ascii=False))
        elif 目标.is_dir():
            for 子文件 in 目标.rglob("*"):
                if 子文件.is_file():
                    print(f"\n=== {子文件} ===")
                    print(json.dumps(扫描指定路径(子文件, 护盾),
                                     indent=2, ensure_ascii=False))
        else:
            print(f"[下载守卫] 路径不存在：{目标}")
        return

    # 默认启动看守
    看守目录字符串 = os.environ.get(
        "LONGHUN_WATCH_DIRS",
        str(Path.home() / "Downloads")
    )
    看守目录列表 = [Path(p.strip()) for p in 看守目录字符串.split(",") if p.strip()]
    隔离目录 = Path(os.environ.get(
        "LONGHUN_QUARANTINE_DIR",
        str(Path.home() / ".longhun" / "quarantine")
    ))

    检测器 = 下载文件检测器(护盾)
    隔离区 = 下载隔离区(隔离目录)
    看守 = 下载目录看守(护盾, 检测器, 隔离区, 看守目录列表)

    try:
        看守.启动()
    except KeyboardInterrupt:
        print("\n[下载守卫] 收到中断，停止")
        看守.停止()


if __name__ == "__main__":
    主函数()
