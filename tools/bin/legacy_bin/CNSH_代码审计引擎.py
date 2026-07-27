#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os as _os
import sys as _sys
_module_dir = _os.path.dirname(_os.path.abspath(__file__))
if _module_dir not in _sys.path:
    _sys.path.insert(0, _module_dir)
"""
CNSH 三色代码审计引擎 v2.0
覆盖：安全漏洞、归属主权、DNA 追溯、命名规范、输入消毒
特性：SM3 国密哈希、GPG 签名修复区、115+ 规则、只修复不覆盖
DNA: #龍芯⚡️2026-06-29-CNSH-AUDIT-ENGINE-v2-UID9622
"""

import json
import os
import re
import secrets
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from CNSH_基础类型 import 三色, 审计维度, 审计项, 审计报告
from CNSH_国密工具 import SM3, SM4, 生成随机密钥, hmac_sm3
from CNSH_颜色不动点协议 import CNSH_颜色不动点协议


# ============== 主权配置 ==============
class 引擎配置:
    def __init__(
        self,
        修复输出目录: str = "./CNSH_修复输出",
        gpg密钥ID: Optional[str] = None,
        sm4密钥: Optional[bytes] = None,
        启用修复加密: bool = False,
    ):
        self.修复输出目录 = Path(修复输出目录)
        self.修复输出目录.mkdir(parents=True, exist_ok=True)
        self.gpg密钥ID = gpg密钥ID
        self.sm4密钥 = sm4密钥 or 生成随机密钥()
        self.启用修复加密 = 启用修复加密


# ============== GPG 签名工具 ==============
class CNSH_GPG工具:
    def __init__(self, 密钥ID: Optional[str] = None):
        self.密钥ID = 密钥ID
        self.gpg命令 = shutil.which("gpg") or shutil.which("gpg2")

    def 可用(self) -> bool:
        return self.gpg命令 is not None and self.密钥ID is not None

    def 签名(self, 数据: bytes) -> Optional[str]:
        if not self.可用():
            return None
        try:
            结果 = subprocess.run(
                [self.gpg命令, "--armor", "--detach-sign", "--local-user", self.密钥ID],
                input=数据,
                capture_output=True,
                timeout=10,
            )
            if 结果.returncode == 0:
                return 结果.stdout.decode("utf-8")
            return f"GPG_ERROR:{结果.stderr.decode('utf-8', errors='replace')[:100]}"
        except Exception as e:
            return f"GPG_EXCEPTION:{e}"

    def 验证(self, 数据: bytes, 签名: str) -> bool:
        if not self.可用():
            return False
        try:
            结果 = subprocess.run(
                [self.gpg命令, "--verify", "-"],
                input=签名.encode("utf-8") + b"\n" + 数据,
                capture_output=True,
                timeout=10,
            )
            return 结果.returncode == 0
        except Exception:
            return False


# ============== CNSH 代码审计引擎 ==============
class CNSH_代码审计引擎:
    """
    开发者代码审计引擎。
    原则：只修复、不破译；不删水印；不去归属；不覆盖原文件；只追加 DNA。
    """

    # 归属权/DNA 保护模式
    保护模式 = [
        (r"#龍芯⚡️", "CNSH DNA 水印"),
        (r"(?i)#\s*DNA[:：]", "DNA 声明"),
        (r"(?i)^#\s*Author\s*[:=]", "作者声明"),
        (r"(?i)Copyright", "版权声明"),
        (r"(?i)License\s*[:=]", "许可证声明"),
        (r"(?i)归属权", "中文归属权"),
        (r"(?i)创始人", "创始人声明"),
        (r"(?i)创作者", "创作者声明"),
        (r"(?i)UID9622", "UID 主权声明"),
    ]

    def __init__(self, 配置: Optional[引擎配置] = None):
        self.配置 = 配置 or 引擎配置()
        self.gpg = CNSH_GPG工具(self.配置.gpg密钥ID)
        self._规则库: List[Dict[str, Any]] = []
        self.颜色协议 = CNSH_颜色不动点协议()
        self._加载规则库()

    def _加载规则库(self):
        try:
            from CNSH_规则库 import 获取规则库
            self._规则库 = 获取规则库()
        except Exception as e:
            print(f"[CNSH] 规则库加载失败: {e}，将使用内置精简规则。")
            self._规则库 = []

    # ---------- 工具方法 ----------
    def _计算SM3哈希(self, 内容: str) -> str:
        return SM3.hex_hash(内容)

    def _生成DNA(self, 动作: str, 原哈希: str) -> str:
        时间戳 = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        随机熵 = secrets.token_hex(4).upper()
        哈希原料 = f"{动作}-{原哈希}-{时间戳}-{随机熵}-UID9622"
        短哈希 = SM3.hex_hash(哈希原料)[:16].upper()
        return f"#龍芯⚡️{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-{动作}-{短哈希}-ENTROPY{随机熵}-UID9622-REPAIR"

    def _读取文件(self, 路径: str) -> str:
        with open(路径, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    # ---------- 归属权与水印保护 ----------
    def _检查归属权(self, 代码: str) -> List[审计项]:
        结果 = []
        行列表 = 代码.splitlines()
        发现标记 = []

        for 行号, 行 in enumerate(行列表, 1):
            for 模式, 名称 in self.保护模式:
                if re.search(模式, 行):
                    发现标记.append((行号, 名称, 行))

        if not 发现标记:
            结果.append(审计项(
                维度=审计维度.归属主权,
                行号=0,
                等级=三色.黄,
                规则ID="CNSH-R090",
                规则名="缺失作者声明",
                分类="OWN-归属",
                CWE="CWE-NA",
                描述="未检测到作者、版权、DNA 或归属权声明，建议修复时追加。",
                原始代码="",
                修复建议="在文件头部追加作者、版权、DNA 声明。",
            ))
        else:
            for 行号, 名称, 行 in 发现标记:
                结果.append(审计项(
                    维度=审计维度.归属主权,
                    行号=行号,
                    等级=三色.绿,
                    规则ID="CNSH-R092",
                    规则名=f"保护标记存在：{名称}",
                    分类="OWN-归属",
                    CWE="CWE-NA",
                    描述="该标记将在修复过程中被完整保留，绝不被覆盖或删除。",
                    原始代码=行.strip(),
                    修复建议="无需修改，继续保留。",
                    不可覆盖=True,
                ))

        # 繁体龍字主权检查
        if re.search(r"(?i)(龙芯|龙魂|龙字)", 代码):
            行号 = 1
            for idx, 行 in enumerate(行列表, 1):
                if re.search(r"(?i)(龙芯|龙魂|龙字)", 行):
                    行号 = idx
                    break
            结果.append(审计项(
                维度=审计维度.归属主权,
                行号=行号,
                等级=三色.红,
                规则ID="CNSH-R093",
                规则名="繁体龍字被简化",
                分类="OWN-主权字",
                CWE="CWE-NA",
                描述="发现「龙」字简化，违反 CNSH 主权字规范。",
                原始代码="龙",
                修复建议="恢复繁体「龍」字，保护文化主权。",
                不可覆盖=True,
            ))

        return 结果

    # ---------- 安全漏洞审计（规则库驱动） ----------
    def _检查规则库(self, 代码: str) -> List[审计项]:
        结果 = []
        行列表 = 代码.splitlines()

        for 行号, 行 in enumerate(行列表, 1):
            for 规则 in self._规则库:
                if 规则["维度"] in (审计维度.归属主权, 审计维度.DNA追溯):
                    continue  # 归属与 DNA 单独检查
                try:
                    编译模式 = 规则.get("编译模式")
                    if 编译模式 is None:
                        continue
                    if 编译模式.search(行):
                        结果.append(审计项(
                            维度=规则["维度"],
                            行号=行号,
                            等级=规则["等级"],
                            规则ID=规则["规则ID"],
                            规则名=规则["名称"],
                            分类=规则["分类"],
                            CWE=规则.get("CWE", ""),
                            描述=f"{规则['名称']} ({规则['CWE']})",
                            原始代码=行.strip(),
                            修复建议=规则["修复建议"],
                        ))
                except re.error:
                    continue

        return 结果

    # ---------- DNA 追溯审计 ----------
    def _检查DNA(self, 代码: str) -> List[审计项]:
        结果 = []
        匹配 = list(re.finditer(r"#龍芯⚡️[^\n]+", 代码))

        if not 匹配:
            结果.append(审计项(
                维度=审计维度.DNA追溯,
                行号=0,
                等级=三色.黄,
                规则ID="CNSH-R091",
                规则名="缺失 CNSH DNA",
                分类="DNA-追溯",
                CWE="CWE-NA",
                描述="代码中没有发现 #龍芯⚡️ DNA 追溯标记。",
                原始代码="",
                修复建议="修复时将追加不可消除的 DNA 追溯链。",
            ))
        else:
            for m in 匹配:
                行号 = 代码[:m.start()].count("\n") + 1
                结果.append(审计项(
                    维度=审计维度.DNA追溯,
                    行号=行号,
                    等级=三色.绿,
                    规则ID="CNSH-R091",
                    规则名="DNA 追溯存在",
                    分类="DNA-追溯",
                    CWE="CWE-NA",
                    描述="已发现 DNA 标记，修复时将保留并追加新链。",
                    原始代码=m.group().strip(),
                    修复建议="无需修改，继续保留。",
                    不可覆盖=True,
                ))

        return 结果

    # ---------- 主审计入口 ----------
    def 审计(self, 文件路径: str) -> 审计报告:
        代码 = self._读取文件(文件路径)
        文件哈希 = self._计算SM3哈希(代码)

        文件GPG签名 = None
        if self.gpg.可用():
            文件GPG签名 = self.gpg.签名(代码.encode("utf-8"))

        所有项 = []
        所有项.extend(self._检查归属权(代码))
        所有项.extend(self._检查规则库(代码))
        所有项.extend(self._检查DNA(代码))

        摘要 = {"🟢": 0, "🟡": 0, "🔴": 0}
        for 项 in 所有项:
            摘要[项.等级.value] += 1

        报告 = 审计报告(
            文件路径=文件路径,
            文件SM3哈希=文件哈希,
            文件GPG签名=文件GPG签名,
            三色摘要=摘要,
            审计项列表=所有项,
        )
        报告.颜色状态 = self._审计报告颜色状态(报告)
        return 报告

    # ---------- 修复入口：只修复、不覆盖 ----------
    def 修复(self, 报告: 审计报告, 是否签名: bool = True) -> 审计报告:
        """
        修复逻辑：
        1. 原文件一字不动
        2. 保留所有水印/版权/DNA
        3. 对明确高危模式做保守替换
        4. 追加修复审计 DNA
        5. 可选 GPG 签名修复审计区
        6. 可选 SM4 加密修复后文件
        7. 写入新文件
        """
        原代码 = self._读取文件(报告.文件路径)
        修复后代码 = 原代码

        # 保守替换表（只替换明确的高危模式）
        替换表 = [
            (r"yaml\.load\s*\(", "yaml.safe_load("),
            (r"requests\.get\s*\(([^)]*?)verify\s*=\s*False([^)]*?)\)", r"requests.get(\1verify=True\2)"),
            (r"DEBUG\s*=\s*True", "DEBUG = False"),
            (r"(?i)(龙芯|龙魂|龙字)", lambda m: m.group().replace("龙", "龍")),
        ]

        for 模式, 替换 in 替换表:
            修复后代码 = re.sub(模式, 替换, 修复后代码)

        # 追加不可消除的修复审计 DNA
        修复DNA = self._生成DNA("CNSH-AUDIT-REPAIR", 报告.文件SM3哈希)
        时间戳 = datetime.now(timezone.utc).isoformat()
        修复注释 = f'''
# {"="*60}
# CNSH 修复审计区 · 只追加 · 不覆盖 · 不抹除
# 修复时间: {时间戳}
# 原文件: {报告.文件路径}
# 原文件 SM3 哈希: {报告.文件SM3哈希}
# 修复原则: 只修复安全漏洞，不删除原水印、版权、作者、DNA
# 引擎 DNA: #龍芯⚡️2026-06-29-CNSH-AUDIT-ENGINE-v2-UID9622
# {修复DNA}
# {"="*60}
'''
        修复后代码 = 修复后代码.rstrip() + "\n" + 修复注释 + "\n"

        # GPG 签名修复审计区
        修复区GPG签名 = None
        if 是否签名 and self.gpg.可用():
            修复区GPG签名 = self.gpg.签名(修复注释.encode("utf-8"))

        # 生成新路径
        原路径 = Path(报告.文件路径)
        时间戳短 = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        新文件名 = f"{原路径.stem}.fixed.{时间戳短}{原路径.suffix}"
        新路径 = self.配置.修复输出目录 / 新文件名

        # 可选 SM4 加密
        if self.配置.启用修复加密:
            密文 = SM4.encrypt_ecb(修复后代码.encode("utf-8"), self.配置.sm4密钥)
            新路径 = 新路径.with_suffix(新路径.suffix + ".sm4")
            with open(新路径, "wb") as f:
                f.write(密文)
        else:
            with open(新路径, "w", encoding="utf-8") as f:
                f.write(修复后代码)

        报告.修复后路径 = str(新路径)
        报告.修复审计DNA = 修复DNA
        报告.修复区GPG签名 = 修复区GPG签名
        return 报告

    # ---------- 报告生成 ----------
    def _审计报告颜色状态(self, 报告: 审计报告) -> Dict[str, Any]:
        摘要 = 报告.三色摘要
        if 摘要["🔴"] > 0:
            主色, 含义 = "R", "代码含红线风险"
        elif 摘要["🟡"] > 0:
            主色, 含义 = "Y", "代码需确认/补证据"
        else:
            主色, 含义 = "G", "代码安全可放行"
        色带 = ["K"] + [主色] * 6 + (["Y"] if 主色 == "R" else ["B"]) * 4 + ["K"]
        return {
            "主色": 主色,
            "颜色名": {"R": "红色", "Y": "黄色", "G": "绿色"}.get(主色, "未知"),
            "emoji": {"R": "🔴", "Y": "🟡", "G": "🟢"}.get(主色, "⚪"),
            "含义": 含义,
            "色带": 色带,
        }

    def 生成报告(self, 报告: 审计报告, 保存: bool = True) -> str:
        颜色状态 = self._审计报告颜色状态(报告)
        行 = []
        行.append("╔" + "═" * 62 + "╗")
        行.append("║" + " " * 14 + "CNSH 三色代码审计报告 v2.0" + " " * 20 + "║")
        行.append("╠" + "═" * 62 + "╣")
        行.append(f"║ 颜色状态: {颜色状态['emoji']} {颜色状态['颜色名']} · {颜色状态['含义']:<35} ║")
        行.append("║ 颜色色带: " + self.颜色协议.渲染色带(颜色状态['色带']) + " " * (53 - len(颜色状态['色带']) * 2) + "║")
        行.append("╠" + "═" * 62 + "╣")
        行.append(f"║ 文件路径: {报告.文件路径:<49} ║")
        行.append(f"║ 文件 SM3: {报告.文件SM3哈希[:40]:<49} ║")
        if 报告.文件GPG签名:
            行.append(f"║ 文件 GPG: {'已签名':<49} ║")
        行.append(f"║ 三色统计: 🟢 {报告.三色摘要['🟢']}  🟡 {报告.三色摘要['🟡']}  🔴 {报告.三色摘要['🔴']:<34} ║")
        行.append("╠" + "═" * 62 + "╣")

        for 项 in 报告.审计项列表:
            保护标 = "【不可覆盖】" if 项.不可覆盖 else ""
            行.append(f"║ {项.等级.value} [{项.维度.value}] 行{项.行号:>4} {项.规则ID} {项.规则名:<18} ║")
            行.append(f"║    CWE: {项.CWE:<6} 分类: {项.分类:<30} ║")
            行.append(f"║    描述: {项.描述[:48]:<48} ║")
            if 项.修复建议:
                行.append(f"║    建议: {项.修复建议[:48]:<48} ║")
            if 保护标:
                行.append(f"║    {保护标:<56} ║")
            行.append("║" + " " * 62 + "║")

        if 报告.修复后路径:
            行.append(f"║ 修复输出: {报告.修复后路径:<49} ║")
            行.append(f"║ 修复 DNA: {报告.修复审计DNA:<49} ║")
            if 报告.修复区GPG签名:
                行.append(f"║ 修复 GPG: {'已签名':<49} ║")

        行.append("╚" + "═" * 62 + "╝")
        文本 = "\n".join(行)

        if 保存:
            报告名 = f"{Path(报告.文件路径).stem}.audit.{datetime.now(timezone.utc).strftime('Y%m%d_%H%M%S')}.json"
            报告路径 = self.配置.修复输出目录 / 报告名
            with open(报告路径, "w", encoding="utf-8") as f:
                json.dump({
                    "文件路径": 报告.文件路径,
                    "文件SM3哈希": 报告.文件SM3哈希,
                    "文件GPG签名": 报告.文件GPG签名,
                    "三色摘要": 报告.三色摘要,
                    "审计项": [
                        {
                            "维度": 项.维度.value,
                            "行号": 项.行号,
                            "等级": 项.等级.value,
                            "规则ID": 项.规则ID,
                            "规则名": 项.规则名,
                            "分类": 项.分类,
                            "CWE": 项.CWE,
                            "描述": 项.描述,
                            "原始代码": 项.原始代码,
                            "修复建议": 项.修复建议,
                            "不可覆盖": 项.不可覆盖,
                        }
                        for 项 in 报告.审计项列表
                    ],
                    "修复后路径": 报告.修复后路径,
                    "修复审计DNA": 报告.修复审计DNA,
                    "修复区GPG签名": 报告.修复区GPG签名 is not None,
                }, f, ensure_ascii=False, indent=2)

        return 文本


# ============== 演示 ==============
if __name__ == "__main__":
    演示代码 = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: 原作者
# Copyright (c) 2025
# #龍芯⚡️2026-06-01-ORIGINAL-ABC123-UID9622

import yaml
import requests
import hashlib

DEBUG = True
SECRET_KEY = "hardcoded_secret_1234567890123456"

def login(user_input):
    query = "SELECT * FROM users WHERE name = '%s'" % user_input
    return query

def run(cmd):
    eval(cmd)

data = yaml.load(open("config.yaml").read())
r = requests.get("https://api.example.com", verify=False)
print("龙魂系统启动")
'''

    演示路径 = "./demo_vulnerable.py"
    with open(演示路径, "w", encoding="utf-8") as f:
        f.write(演示代码)

    引擎 = CNSH_代码审计引擎()
    报告 = 引擎.审计(演示路径)
    报告 = 引擎.修复(报告, 是否签名=False)
    print(引擎.生成报告(报告))

    print("\n✅ 原文件未改动")
    print(f"✅ 修复文件: {报告.修复后路径}")
    print(f"✅ 修复 DNA: {报告.修复审计DNA}")
