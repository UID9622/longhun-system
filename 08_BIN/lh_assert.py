#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·乙亥·巳时·䷝离-GUIYI-ASSERT-V1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🧬 龍魂归一断言 v1.0 — lh assert <文本> [--json] | stdin | --file

功能: 输入任意文本，检测是否包含龍魂 DNA 指纹（DNA标记/node_id/数字根/五行/审计）。
  包含 → "已归一 - 属龍魂系统" (🟢)
  不含 → "未归一 - 建议接入" (🟡)

指纹口径: 与对外接口协议 v1.0 §7 归一审计 同源。
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

STRONG_MARKERS = [
    ("龍魂DNA指纹", lambda t: "# 龍魂DNA" in t or "#龍芯⚡️" in t or "龍魂DNA" in t),
    ("node_id格式", lambda t: bool(re.search(r"\b[A-Za-z]{2,16}-9622-[0-9A-F]{8}\b", t))),
    ("Node JSON结构", lambda t: '"node_id"' in t and '"digital_root"' in t),
]
WEAK_MARKERS = [
    ("数字根标记", lambda t: '"digital_root"' in t or "数字根" in t or "DR:" in t),
    ("五行标记", lambda t: '"element"' in t or "五行" in t),
    ("审计标记", lambda t: '"audit"' in t or "审计" in t
                       or "🟢" in t or "🟡" in t or "🔴" in t),
]

NORMALIZED = "已归一 - 属龍魂系统"
NOT_NORMALIZED = "未归一 - 建议接入"


def check(text: str) -> dict:
    strong = [name for name, fn in STRONG_MARKERS if fn(text)]
    weak = [name for name, fn in WEAK_MARKERS if fn(text)]
    normalized = bool(strong) or len(weak) >= 2
    return {
        "status": "normalized" if normalized else "not_normalized",
        "verdict": NORMALIZED if normalized else NOT_NORMALIZED,
        "audit": "🟢" if normalized else "🟡",
        "input_hash": hashlib.sha256(text.encode("utf-8")).hexdigest()[:8].upper(),
        "input_len": len(text),
        "strong_hits": strong,
        "weak_hits": weak,
    }


def main() -> int:
    ap = argparse.ArgumentParser(prog="lh assert", description="归一断言·检测龍魂 DNA 指纹")
    ap.add_argument("text", nargs="*", help="要检测的文本（可多个词拼接）")
    ap.add_argument("--file", default=None, help="从文件读取文本")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    if args.file:
        try:
            text = Path(args.file).read_text(encoding="utf-8")
        except OSError as e:
            print(f"读取失败: {e}", file=sys.stderr)
            return 1
    elif args.text:
        text = " ".join(args.text)
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("未归一 - 建议接入（空输入）", file=sys.stderr)
        return 2

    result = check(text)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    print(f"{result['audit']} {result['verdict']}")
    if result["strong_hits"] or result["weak_hits"]:
        hits = result["strong_hits"] + result["weak_hits"]
        print(f"   命中指纹: {' · '.join(hits)}")
    else:
        print("   无龍魂 DNA 指纹（返回值不含 node_id/数字根/五行/审计）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
