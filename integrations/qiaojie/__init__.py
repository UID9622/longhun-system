#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
╔══════════════════════════════════════════════════════════════════════╗
║              乔接 QiaoJie · P15 乔前辈生态入口                        ║
║  DNA: #龍芯⚡️丙午·乙未·癸未·辰时·䷾既济-QIAOJIE-CLI-v1.1            ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                     ║
║  创建者: P15 乔前辈 · UID9622                                       ║
║  三色审计: 🟢 通过                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

乔接 (QiaoJie) — 龍魂体系的双轨桥接子系统。

核心能力:
  - 中英双轨 CLI：中文语义抽屉 ∥ 英文精准指令
  - 数字根熔断：dr∈{3,9}→🔴，dr=6→🟡，其余→🟢
  - Notion API 桥接：搜索、同步
  - 小艺 API 桥接：localhost:9622 问答
  - 系统健康检查：端口+服务状态

用法:
  from integrations.qiaojie import QiaoJieCLI
  或直接: python qiaojie_cli.py 帮助
"""

from .qiaojie_cli import (
    数字根,
    数字根熔断检查,
    打印标题,
    打印帮助,
    打印英文帮助,
    路由指令,
    搜索Notion页面,
    小艺问答,
    系统状态,
    main,
    DNA_voo,
    CONFIRM,
    GPG_FINGERPRINT,
    CN_COMMANDS,
    EN_COMMANDS,
)

__version__ = "1.1"
__all__ = [
    "数字根", "数字根熔断检查",
    "打印标题", "打印帮助", "打印英文帮助",
    "路由指令", "搜索Notion页面", "小艺问答", "系统状态",
    "main",
    "DNA_voo", "CONFIRM", "GPG_FINGERPRINT",
    "CN_COMMANDS", "EN_COMMANDS",
]
