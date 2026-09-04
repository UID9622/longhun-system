# P0焊死: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
# License: CC BY-NC-SA 4.0（核心思想层·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# #龍芯⚡️丙午·甲午·己卯·庚午·䷚颐-SANCAI-PROTOCOL-GUARD-v1.0
# -*- coding: utf-8 -*-
"""
三才算法协议守护脚本

用法:
    python3 scripts/L2_WELDED_PROTOCOLS/sancai_protocol_guard.py

行为:
    1. 导入 cnsh-core.constitution.sancai_protocol，触发完整性校验。
    2. 强制将协议文件、校验文件、模块文件设为只读。
    3. 输出三色状态：🟢 通过 / 🔴 熔断。

任何篡改协议文件的行为都会在本脚本运行时触发 SancaiProtocolTamperedError，
并返回非零退出码，可被龍魂审计系统捕获。
"""

import importlib
import os
import stat
import sys
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

# 抑制 cnsh-core 顶层可能产生的降级警告，只关注协议本身
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    sancai_mod = importlib.import_module("cnsh-core.constitution.sancai_protocol")

PROTOCOL_FILE = sancai_mod.PROTOCOL_FILE
CHECKSUM_FILE = sancai_mod.CHECKSUM_FILE
SANCAI = sancai_mod.SANCAI
SancaiProtocolTamperedError = sancai_mod.SancaiProtocolTamperedError
verify_protocol_integrity = sancai_mod.verify_protocol_integrity
_set_readonly = sancai_mod._set_readonly

MODULE_FILE = Path(__file__).resolve().parents[2] / "cnsh-core" / "constitution" / "sancai_protocol.py"


def main() -> int:
    try:
        # 重新执行校验（模块导入时已经执行一次，这里显式再锁一次）
        file_hash = verify_protocol_integrity()

        # 强制只读（即使外部误改权限也能恢复）
        _set_readonly(PROTOCOL_FILE)
        _set_readonly(CHECKSUM_FILE)
        _set_readonly(MODULE_FILE)

        print("🟢 三才算法协议校验通过")
        print(f"   DNA: {SANCAI.dna}")
        print(f"   文件: {PROTOCOL_FILE}")
        print(f"   SHA256: {file_hash}")
        print(f"   天:{SANCAI.tian} 地:{SANCAI.di} 人:{SANCAI.ren} 中宫:{SANCAI.zhonggong} 369:{SANCAI.san}-{SANCAI.liu}-{SANCAI.jiu}")
        return 0
    except SancaiProtocolTamperedError as e:
        print(f"🔴 三才算法协议熔断: {e}")
        return 77
    except Exception as e:
        print(f"🔴 三才算法协议守护异常: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
