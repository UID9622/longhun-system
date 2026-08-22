#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · 语气引擎

让用户/群体自选语气档位：
  - UID9622（默认）：原汁原味的表达
  - 温和：保留事实，降低攻击性，不虚伪
  - 犀利：更直接、更硬
  - 正式：去情绪化，结构化表达

支持按用户画像自动匹配默认档位，强度 0-100 可调。
DNA: #龍芯⚡️丙午·甲午·乙亥·壬午·䷚颐-LONGHUN-TONE-ENGINE-v1.0
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

HOME = Path.home()
CONFIG_DIR = HOME / ".longhun" / "config"
CONFIG_PATH = CONFIG_DIR / "用户语气配置.json"


def _生成DNA(操作: str) -> str:
    日期 = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"#龍芯⚡️{日期}-TONE-{操作.upper()}-UID9622"


class 语气渲染器:
    """把 UID9622 的原话按所选档位重新渲染，保持事实不变，只调语气。"""

    def __init__(self, 配置路径: Path = CONFIG_PATH):
        self.配置路径 = 配置路径
        self.配置 = self._加载配置()

    def _加载配置(self) -> Dict[str, Any]:
        if self.配置路径.exists():
            try:
                return json.loads(self.配置路径.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "_comment": "用户语气配置：按用户ID或群体设置默认模式与强度",
            "默认模式": "UID9622",
            "默认强度": 0,
            "用户映射": {},
            "群体映射": {
                "普通网友": {"模式": "UID9622", "强度": 0},
                "技术人员": {"模式": "正式", "强度": 40},
                "合作方": {"模式": "温和", "强度": 30},
                "恶意攻击者": {"模式": "犀利", "强度": 80},
            },
        }

    def 保存配置(self) -> None:
        self.配置路径.parent.mkdir(parents=True, exist_ok=True)
        self.配置路径.write_text(json.dumps(self.配置, ensure_ascii=False, indent=2), encoding="utf-8")

    def 获取用户模式(self, 用户ID: str, 群体: Optional[str] = None) -> Dict[str, Any]:
        if 用户ID in self.配置.get("用户映射", {}):
            return self.配置["用户映射"][用户ID]
        if 群体 and 群体 in self.配置.get("群体映射", {}):
            return self.配置["群体映射"][群体]
        return {"模式": self.配置.get("默认模式", "UID9622"), "强度": self.配置.get("默认强度", 0)}

    def 设置用户模式(self, 用户ID: str, 模式: str, 强度: int) -> None:
        self.配置.setdefault("用户映射", {})[用户ID] = {"模式": 模式, "强度": 强度}
        self.保存配置()

    def 设置群体模式(self, 群体: str, 模式: str, 强度: int) -> None:
        self.配置.setdefault("群体映射", {})[群体] = {"模式": 模式, "强度": 强度}
        self.保存配置()

    def 渲染(self, 原文: str, 模式: Optional[str] = None, 强度: Optional[int] = None,
             用户ID: Optional[str] = None, 群体: Optional[str] = None) -> Dict[str, Any]:
        if 模式 is None or 强度 is None:
            用户配置 = self.获取用户模式(用户ID or "UID9622", 群体)
            模式 = 模式 or 用户配置["模式"]
            强度 = 强度 if 强度 is not None else 用户配置["强度"]

        强度 = max(0, min(100, 强度))
        渲染后 = 原文

        if 模式 == "UID9622":
            渲染后 = self._渲染UID9622(渲染后, 强度)
        elif 模式 == "温和":
            渲染后 = self._渲染温和(渲染后, 强度)
        elif 模式 == "犀利":
            渲染后 = self._渲染犀利(渲染后, 强度)
        elif 模式 == "正式":
            渲染后 = self._渲染正式(渲染后, 强度)
        else:
            模式 = "UID9622"
            渲染后 = self._渲染UID9622(渲染后, 强度)

        return {
            "原文": 原文,
            "模式": 模式,
            "强度": 强度,
            "渲染后": 渲染后,
            "dna": _生成DNA(模式),
        }

    @staticmethod
    def _插值替换(文本: str, 替换对: Dict[str, str], 强度: int) -> str:
        """按强度百分比决定是否执行替换。强度越高，替换越彻底。"""
        if 强度 <= 0:
            return 文本
        结果 = 文本
        # 先替换长词，避免"他妈的"被拆成"他妈"+"的"
        for 旧, 新 in sorted(替换对.items(), key=lambda x: len(x[0]), reverse=True):
            # 简单线性：强度 100 全部替换，强度 50 替换一半出现次数（向上取整）
            匹配 = list(re.finditer(re.escape(旧), 结果))
            if not 匹配:
                continue
            替换数 = max(1, int(len(匹配) * 强度 / 100))
            计数 = 0
            新结果 = ""
            上次 = 0
            for m in 匹配:
                if 计数 < 替换数:
                    新结果 += 结果[上次:m.start()] + 新
                    计数 += 1
                else:
                    新结果 += 结果[上次:m.end()]
                上次 = m.end()
            新结果 += 结果[上次:]
            结果 = 新结果
        return 结果

    def _渲染UID9622(self, 文本: str, 强度: int) -> str:
        # 默认模式：几乎不动，最多轻微压缩重复语气词
        return 文本

    def _渲染温和(self, 文本: str, 强度: int) -> str:
        # 降低攻击性，但不假、不跪
        替换 = {
            "他妈逼": "真他妈",
            "他妈的": "真的",
            "他妈": "真的",
            "傻逼": "脑子不好",
            "蠢": "不太明白",
            "滚": "请自便",
            "🔴": "⚠️",
        }
        文本 = self._插值替换(文本, 替换, 强度)
        # 在句尾适度加“哈”“吧”，但只在强度高时
        if 强度 >= 50 and not 文本.endswith(("哈", "吧", "。")):
            文本 = 文本.rstrip("，") + "，对吧。"
        return 文本

    def _渲染犀利(self, 文本: str, 强度: int) -> str:
        # 更直接，减少缓冲词
        替换 = {
            "对吧": "",
            "哈": "",
            "可能": "",
            "也许": "",
            "我觉得": "",
        }
        文本 = self._插值替换(文本, 替换, 强度)
        # 高强度时把句号改成感叹号
        if 强度 >= 70:
            文本 = re.sub(r"(?<=[^。！])$", "！", 文本)
        return 文本

    def _渲染正式(self, 文本: str, 强度: int) -> str:
        # 去情绪化、结构化
        替换 = {
            "他妈": "",
            "他妈逼": "",
            "傻逼": "相关人员",
            "🔴": "【需关注】",
            "🟢": "【正常】",
            "🟡": "【提示】",
            "哈": "",
            "对吧": "",
        }
        文本 = self._插值替换(文本, 替换, 强度)
        # 去掉 emoji
        if 强度 >= 50:
            文本 = re.sub(r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+", "", 文本)
        return 文本.strip()


def _cli():
    解析器 = argparse.ArgumentParser(description="龍魂语气引擎")
    子命令 = 解析器.add_subparsers(dest="command", required=True)

    p_render = 子命令.add_parser("渲染", help="渲染一段文本")
    p_render.add_argument("文本", help="要渲染的原文")
    p_render.add_argument("--模式", "-m", choices=["UID9622", "温和", "犀利", "正式"], default=None)
    p_render.add_argument("--强度", "-s", type=int, default=None)
    p_render.add_argument("--用户", "-u", default=None)
    p_render.add_argument("--群体", "-g", default=None)

    p_set = 子命令.add_parser("设置", help="设置用户/群体默认语气")
    p_set.add_argument("对象", help="用户ID 或 群体名")
    p_set.add_argument("模式", choices=["UID9622", "温和", "犀利", "正式"])
    p_set.add_argument("强度", type=int)
    p_set.add_argument("--群体", action="store_true", help="对象按群体处理")

    p_get = 子命令.add_parser("查看", help="查看当前配置")
    p_get.add_argument("--用户", "-u", default=None)
    p_get.add_argument("--群体", "-g", default=None)

    args = 解析器.parse_args()
    引擎 = 语气渲染器()

    if args.command == "渲染":
        结果 = 引擎.渲染(args.文本, 模式=args.模式, 强度=args.强度, 用户ID=args.用户, 群体=args.群体)
        print(json.dumps(结果, ensure_ascii=False, indent=2))

    elif args.command == "设置":
        if args.群体:
            引擎.设置群体模式(args.对象, args.模式, args.强度)
            print(f"🟢 群体 [{args.对象}] 默认语气：{args.模式} / 强度 {args.强度}%")
        else:
            引擎.设置用户模式(args.对象, args.模式, args.强度)
            print(f"🟢 用户 [{args.对象}] 默认语气：{args.模式} / 强度 {args.强度}%")

    elif args.command == "查看":
        配置 = 引擎.获取用户模式(args.用户 or "UID9622", args.群体)
        print(json.dumps(配置, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _cli()
