#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·戊寅·辰时·䷝离-LH-DOC-SYNC-v1.0-AUTOGEN
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# 文档自动同步 v1.0 — `lh doc-sync`
# 从 08_BIN/lh.py 的 SUB_DISPATCH 提取命令表 → 生成 docs/LH-COMMANDS-AUTOGEN.md
# 只更新 autogen 清单文件，绝不改动 README/其他文档正文（不误伤他人心血）。

import argparse
import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LH_PY = ROOT / "08_BIN" / "lh.py"
OUT = ROOT / "docs" / "LH-COMMANDS-AUTOGEN.md"

HEADER = """# 🐉 龍魂命令总表 · 自动生成（DO NOT EDIT）

> 由 `lh doc-sync` 从 `08_BIN/lh.py` SUB_DISPATCH 自动提取。
> 手工改动会被下次同步覆盖。真源: `08_BIN/lh.py`。
> 生成时间: {ts}
> DNA: #龍芯⚡️丙午·丁酉·戊寅·辰时·䷝离-LH-DOC-SYNC-v1.0-AUTOGEN
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰

## 子命令清单

| 命令 | 图标 | 说明 |
|:---|:---|:---|
"""


def extract_dispatch() -> list:
    """ast 解析 lh.py，提取 SUB_DISPATCH 的 (key, script, emoji, desc)"""
    tree = ast.parse(LH_PY.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "SUB_DISPATCH":
                    items = []
                    pairs = []
                    if isinstance(node.value, ast.Dict):      # {'a': (...), 'b': (...)}
                        pairs = zip(node.value.keys, node.value.values)
                    elif isinstance(node.value, ast.List):    # [('a', (...)), ...]
                        pairs = [(kv.elts[0], kv.elts[1]) for kv in node.value.elts
                                 if isinstance(kv, ast.Tuple)]
                    for key_el, val_el in pairs:
                        key = ast.literal_eval(key_el)
                        if not isinstance(val_el, ast.Tuple) or len(val_el.elts) < 3:
                            continue
                        try:
                            script = ast.literal_eval(val_el.elts[0])
                            emoji = ast.literal_eval(val_el.elts[1])
                            desc = ast.literal_eval(val_el.elts[2])
                        except Exception:
                            continue
                        items.append((key, script, emoji, desc))
                    return sorted(items, key=lambda x: x[0])
    return []


def render(items) -> str:
    lines = [HEADER.format(ts=__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"))]
    for key, script, emoji, desc in items:
        lines.append(f"| `lh {key}` | {emoji} | {desc} |")
    lines.append(f"\n共 {len(items)} 条子命令。")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="文档自动同步 v1.0 (lh doc-sync)")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--diff", action="store_true", help="只报告差异，不写文件")
    args = ap.parse_args()

    if not LH_PY.exists():
        print(json.dumps({"tool": "lh-doc-sync", "ok": False, "error": "lh.py 不存在"}))
        sys.exit(1)

    items = extract_dispatch()
    new_text = render(items)

    if args.diff:
        old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        added = [k for k, _, _, _ in items if f"`lh {k}`" not in old]
        print(json.dumps({
            "tool": "lh-doc-sync", "ok": True, "mode": "diff",
            "commands": len(items), "new": added,
        }, ensure_ascii=False, indent=2))
        return

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(new_text, encoding="utf-8")
    print(json.dumps({
        "tool": "lh-doc-sync", "ok": True, "mode": "write",
        "commands": len(items), "output": str(OUT),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
