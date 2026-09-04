#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂全球开发者平台 · 统一 DNA 工具层
DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-GLOBAL-DEV-PLATFORM-DNA-LAYER-v1.0
创建者: 诸葛鑫（UID9622）
协议: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

设计原则:
  所有 DNA 一律走系统干支卦引擎（bin/ganzhi_dna_engine.py · v∞ 格式），
  不在平台内部自造 MD5 简化版。每个 DNA 携带干支四柱+卦象+哈希8，可占可验。
"""

import os
import sys
import hashlib
from datetime import datetime
from typing import Optional

# 对接系统干支卦 DNA 引擎
_BIN_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bin"))
if _BIN_DIR not in sys.path:
    sys.path.insert(0, _BIN_DIR)

try:
    from ganzhi_dna_engine import DNA生成  # noqa: F401
    ENGINE_OK = True
except Exception:
    ENGINE_OK = False

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
AUTHOR = "UID9622"


def lh_dna(module: str, action: str = "RUN", version: str = "v1.0",
           level: str = "", anchor: str = "", ts: Optional[datetime] = None) -> str:
    """
    统一 DNA 生成入口。
    - 优先系统干支卦引擎（v∞ 格式: #龍芯⚡️干支·干支·干支·时辰·卦-模块-动作-版本-哈希8）
    - 引擎不可用时降级 SHA256 前8位（绝不使用 MD5）
    """
    if ENGINE_OK:
        try:
            return DNA生成(模块=module, 动作=action, 版本=version,
                          级别=level, timestamp=ts, 内容锚点=anchor)
        except Exception:
            pass
    # 降级路径：SHA256（与系统引擎哈希规则一致，仅缺少卦象）
    stamp = ts or datetime.now()
    body = f"{stamp.isoformat()}-{module}-{action}-{version}-{level}-{anchor}"
    h8 = hashlib.sha256(body.encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{stamp.strftime('%Y%m%d')}-{module}-{action}-{version}-{h8}"


if __name__ == "__main__":
    print("龍魂全球开发者平台 · 统一 DNA 层")
    print(f"  干支卦引擎: {'✅ 已对接 bin/ganzhi_dna_engine.py' if ENGINE_OK else '❌ 不可用(降级 SHA256)'}")
    print(f"  测试 DNA:   {lh_dna('GLOBAL-DEV-PLATFORM', 'TEST', 'v1.0')}")
