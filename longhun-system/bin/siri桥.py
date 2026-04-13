#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·Siri桥 — 一句话调本地模型
DNA: #龍芯⚡️2026-04-13-SIRI-BRIDGE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创始人: UID9622 · 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）
创作地: 中华人民共和国
献礼: 新中国成立77周年（1949-2026）· 丙午马年
协议: Apache License 2.0
"""

import sys
import requests

问题 = " ".join(sys.argv[1:])

响应 = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5",
        "prompt": 问题,
        "stream": False
    }
)

回答 = 响应.json().get("response", "没有回应")
print(回答)
