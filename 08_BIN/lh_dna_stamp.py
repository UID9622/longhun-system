#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-04-RECAP-DNA-STAMP-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""龍魂·DNA 时间戳生成器 v1.0（复盘系统锚定件）

为每次执行/每份复盘生成唯一追溯对:
  - DNA:    #龍芯⚡️<干支四柱>·<卦>-<模块>-<动作>-<HASH8>   （v∞ 标准）
  - STAMP:  干支四柱 + 卦象 + 三色相位（lh_time_engine 权威）
用途: 复盘文档头 · 执行注册 · 决策节点盖戳 · 任何需要"可追溯"的文件。

用法:
  python3 08_BIN/lh_dna_stamp.py --module recap --action generate          # 打印一行 DNA
  python3 08_BIN/lh_dna_stamp.py --module recap --action generate --json    # JSON 双输出(DNA+STAMP)
  python3 08_BIN/lh_dna_stamp.py --check "#龍芯⚡️…"                          # 校验 DNA 格式
零三方 · 降级链: lh_dna_vinf → 简化本地方案（永不崩）。
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

_BIN = Path(__file__).resolve().parent
_ROOT = _BIN.parent
_GANZHI_HOUR = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]


def _clean_dna(dna: str) -> str:
    """清洗: 掐掉卦后混入的三色相位修饰（·🟢/·🟡/·🔴）→ 规范 v∞ 格式。
    例: #龍芯⚡️…·䷛大过·🟢-MOD-ACT-H8 → #龍芯⚡️…·䷛大过-MOD-ACT-H8"""
    head, sep, tail = dna.rpartition("-")
    if not sep:
        return dna
    for mark in ("·🟢", "·🟡", "·🔴"):
        head = head.replace(mark, "")
    return head + "-" + tail


def _sanitize(s: str) -> str:
    return re.sub(r"[^0-9A-Za-z\u4e00-\u9fff\u9f8f]", "_", str(s)) or "x"


def _get_dna(module: str, action: str) -> str:
    """主通道: lh_dna_vinf.generate（v∞ 干支四柱+卦+hash8）。失败→降级。"""
    module, action = _sanitize(module), _sanitize(action)
    try:
        sys.path.insert(0, str(_BIN))
        import lh_dna_vinf
        dna = lh_dna_vinf.generate(module, action)
        if dna.startswith("#龍芯⚡"):
            return _clean_dna(dna)
    except Exception:
        pass
    # 降级: 干支四柱取时间引擎 → 无则纯哈希 DNA（格式仍合规·hash 可核）
    try:
        sys.path.insert(0, str(_BIN))
        import lh_time_engine as _te
        stamp = _te.get_output_stamp(format_type="full")   # [丙午·甲申·…·巳时·䷋否·🟢] ISO
        import re
        m = re.search(r"\[([^\]]+)\]", stamp)
        gz_gua = m.group(1).replace("·", "·") if m else ""
    except Exception:
        gz_gua = ""
    ts = int(datetime.now().timestamp())
    h = hashlib.sha256(f"{module}-{action}-UID9622-{ts}".encode("utf-8")).hexdigest()[:8].upper()
    if gz_gua:
        return _clean_dna(f"#龍芯⚡️{gz_gua}-{module}-{action}-{h}")
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{module}-{action}-{h}"


def get_stamp() -> str:
    """干支四柱+卦象+三色（simple）。失败降级: 本地干支时辰近似。"""
    try:
        sys.path.insert(0, str(_BIN))
        import lh_time_engine as _te
        return _te.get_output_stamp(format_type="simple")
    except Exception:
        pass
    h = _GANZHI_HOUR[(datetime.now().hour + 1) // 2 % 12]
    return f"🐉{datetime.now().strftime('%Y')}·{h}时·䷀乾·🟢"


def _check(dna: str) -> tuple[bool, str]:
    if not dna.startswith("#龍芯⚡"):
        return False, "缺失 #龍芯⚡ 前缀"
    if "-" not in dna:
        return False, "无模块-动作段"
    return True, "ok"


def main() -> int:
    argv = sys.argv[1:]
    if argv and argv[0] in ("--check", "-c") and len(argv) > 1:
        ok, why = _check(argv[1])
        print(f"{'🟢' if ok else '🔴'} {argv[1]} · {why}")
        return 0 if ok else 1
    module = action = ""
    js = False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--module", "-m") and i + 1 < len(argv):
            module, i = argv[i + 1], i + 1
        elif a in ("--action", "-a") and i + 1 < len(argv):
            action, i = argv[i + 1], i + 1
        elif a == "--json":
            js = True
        i += 1
    module = module or "recap"
    action = action or "stamp"
    dna = _get_dna(module, action)
    stamp = get_stamp()
    if js:
        print(json.dumps({"dna": dna, "stamp": stamp, "module": module,
                          "action": action, "iso": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")},
                         ensure_ascii=False))
    else:
        print(dna)
        print(stamp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
