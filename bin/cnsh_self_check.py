#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os as _os
import sys as _sys
_module_dir = _os.path.dirname(_os.path.abspath(__file__))
if _module_dir not in _sys.path:
    _sys.path.insert(0, _module_dir)
"""
CNSH 系统自检脚本 v1.0
定期检查所有 CNSH 模块健康状态、知识库完整性、DNA 一致性。
原则：自动化、无感、只追加报告、不删不改。
#龍芯⚡️丙午·乙未·乙卯·戌时·䷰革-cnsh_self_check-INTEGRATION-SYSTEM
"""

import importlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from CNSH_国密工具 import SM3


class CNSH_系统自检:
    def __init__(self, 工作目录: str = _os.path.dirname(_os.path.abspath(__file__))):
        self.工作目录 = Path(工作目录)
        self.报告: Dict[str, Any] = {
            "时间": datetime.now(timezone.utc).isoformat(),
            "DNA": "#龍芯⚡️丙午·乙未·乙卯·戌时·䷰革-cnsh_self_check-INTEGRATION-SYSTEM",
            "总体状态": "🟢",
            "检查项": [],
        }

    def _记录(self, 名称: str, 状态: str, 详情: str):
        self.报告["检查项"].append({
            "名称": 名称,
            "状态": 状态,
            "详情": 详情,
        })
        if 状态 == "🔴" and self.报告["总体状态"] != "🔴":
            self.报告["总体状态"] = "🔴"
        elif 状态 == "🟡" and self.报告["总体状态"] == "🟢":
            self.报告["总体状态"] = "🟡"

    def 检查模块存在(self):
        必要模块 = [
            "CNSH_基础类型",
            "CNSH_国密工具",
            "CNSH_规则库",
            "CNSH_代码审计引擎",
            "CNSH_目录审计",
            "CNSH_通知归档",
            "CNSH_排序不动点协议",
            "CNSH_内容加工管道",
            "CNSH_收口摘要生成器",
            "CNSH_知识库",
            "CNSH_宝宝指令路由器",
            "CNSH_龍魂宝宝指令中枢",
            "CNSH_生态监管协议",
            "CNSH_流场可视化引擎",
        ]
        缺失 = []
        for m in 必要模块:
            路径 = self.工作目录 / f"{m}.py"
            if not 路径.exists():
                缺失.append(m)
        if 缺失:
            self._记录("模块完整性", "🔴", f"缺失: {', '.join(缺失)}")
        else:
            self._记录("模块完整性", "🟢", f"共 {len(必要模块)} 个核心模块齐全")

    def 检查国密工具(self):
        try:
            from CNSH_国密工具 import SM3, SM4, 生成随机密钥
            sm3_ok = SM3.hex_hash("abc") == "66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0"
            key = 生成随机密钥()
            pt = b"CNSH_HEALTH_CHECK_"
            ct = SM4.encrypt_ecb(pt, key)
            dt = SM4.decrypt_ecb(ct, key)
            sm4_ok = dt == pt
            if sm3_ok and sm4_ok:
                self._记录("国密工具", "🟢", "SM3/SM4 自测通过")
            else:
                self._记录("国密工具", "🔴", f"SM3={sm3_ok}, SM4={sm4_ok}")
        except Exception as e:
            self._记录("国密工具", "🔴", str(e))

    def 检查规则库(self):
        try:
            from CNSH_规则库 import 获取规则库
            规则 = 获取规则库()
            if len(规则) >= 100:
                self._记录("规则库", "🟢", f"共 {len(规则)} 条规则")
            else:
                self._记录("规则库", "🟡", f"仅 {len(规则)} 条规则，建议扩展")
        except Exception as e:
            self._记录("规则库", "🔴", str(e))

    def 检查知识库(self):
        路径 = self.工作目录 / "CNSH_知识库.json"
        if not 路径.exists():
            self._记录("知识库", "🟡", "知识库尚未创建")
            return
        try:
            with open(路径, "r", encoding="utf-8") as f:
                数据 = json.load(f)
            条目数 = len(数据.get("条目", []))
            self._记录("知识库", "🟢", f"知识库正常，共 {条目数} 条记录")
        except Exception as e:
            self._记录("知识库", "🔴", f"JSON 损坏: {e}")

    def 检查DNA标记(self):
        路径列表 = list(self.工作目录.glob("CNSH_*.py"))
        无DNA = []
        for 路径 in 路径列表:
            try:
                内容 = 路径.read_text(encoding="utf-8")
                if "#龍芯⚡️" not in 内容:
                    无DNA.append(路径.name)
            except Exception:
                pass
        if 无DNA:
            self._记录("DNA 标记", "🟡", f"以下文件无 DNA: {', '.join(无DNA)}")
        else:
            self._记录("DNA 标记", "🟢", f"所有 {len(路径列表)} 个 CNSH 模块均含 DNA")

    def 检查配置模板(self):
        路径 = self.工作目录 / "CNSH_通知配置.json"
        if 路径.exists():
            self._记录("通知配置", "🟢", "已配置 SMTP/Notion")
        else:
            self._记录("通知配置", "🟡", "未配置，通知功能处于跳过状态")

    def 检查生态监管(self):
        try:
            from CNSH_生态监管协议 import CNSH_生态监管协议
            监管 = CNSH_生态监管协议()
            监管.生成监管报告()
            self._记录("生态监管", "🟢", "监管模块可正常加载")
        except Exception as e:
            self._记录("生态监管", "🔴", str(e))

    def 检查流场引擎(self):
        try:
            from CNSH_流场可视化引擎 import CNSH_流场可视化引擎
            引擎 = CNSH_流场可视化引擎()
            数量 = 引擎.扫描文件粒子()
            self._记录("流场可视化", "🟢", f"扫描到 {数量} 个文件粒子")
        except Exception as e:
            self._记录("流场可视化", "🔴", str(e))

    def 运行全部检查(self) -> Dict[str, Any]:
        self.检查模块存在()
        self.检查国密工具()
        self.检查规则库()
        self.检查知识库()
        self.检查DNA标记()
        self.检查配置模板()
        self.检查生态监管()
        self.检查流场引擎()
        self.报告["报告SM3哈希"] = SM3.hex_hash(json.dumps(self.报告, sort_keys=True, ensure_ascii=False))
        return self.报告

    def 保存报告(self) -> Path:
        路径 = self.工作目录 / f"CNSH_系统自检报告.{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        with open(路径, "w", encoding="utf-8") as f:
            json.dump(self.报告, f, ensure_ascii=False, indent=2)
        return 路径

    def 格式化(self) -> str:
        行 = []
        行.append("╔" + "═" * 58 + "╗")
        行.append("║" + " " * 18 + "CNSH 系统自检报告" + " " * 23 + "║")
        行.append("╠" + "═" * 58 + "╣")
        行.append(f"║ 时间: {self.报告['时间'][:48]:<48} ║")
        行.append(f"║ 总体: {self.报告['总体状态']:<49} ║")
        行.append("╠" + "═" * 58 + "╣")
        for 项 in self.报告["检查项"]:
            行.append(f"║ {项['状态']} {项['名称']:<10} {项['详情']:<36} ║")
        行.append("╚" + "═" * 58 + "╝")
        return "\n".join(行)


if __name__ == "__main__":
    目录 = sys.argv[1] if len(sys.argv) > 1 else _os.path.dirname(_os.path.abspath(__file__))
    自检 = CNSH_系统自检(目录)
    自检.运行全部检查()
    路径 = 自检.保存报告()
    print(自检.格式化())
    print(f"\n报告已保存: {路径}")
