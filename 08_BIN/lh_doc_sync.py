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

# ── 对外文档版本联动 v5.2.0（2026-09-05 任务C焊入 · 与系统主干版本联动）
# 系统版本口径: 主干 v5.2.0（2026-09-04 PR#98 · rust 主干）· 控制台 lh v1.3
DOCS_VERSION = "v5.2.0"

DELIVERY_DOCS = [
    "12_DOCS/DEPENDENCIES.md", "12_DOCS/INSTALL.md", "12_DOCS/QUICKSTART.md",
    "12_DOCS/USAGE.md", "12_DOCS/API_REFERENCE.md", "12_DOCS/JSONRPC.md",
    "12_DOCS/MCP_GUIDE.md", "12_DOCS/NOTION_MCP_GUIDE.md", "12_DOCS/TROUBLESHOOTING.md",
    "12_DOCS/30分钟接入龙魂系统.md", "12_DOCS/龍魂对外交付文档体系-v1.0.md",
]


def bump_delivery_versions(version=DOCS_VERSION, dry=False) -> list:
    """同步 12_DOCS 交付文档头部版本行：
    无 `> 文档版本:` → 在 `> 协议:` 行后插入；有 → 替换为最新版本。
    返回已变更(或需变更 dry)的文件相对路径列表。"""
    import re as _re
    pat = _re.compile(r"^> 文档版本:.*$")
    changed = []
    for rel in DELIVERY_DOCS:
        p = ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        lines = text.split("\n")
        head = lines[:10]
        idx = next((i for i, l in enumerate(head) if pat.match(l)), None)
        if idx is not None:
            if head[idx] == f"> 文档版本: {version}":
                continue
            lines[idx] = f"> 文档版本: {version}"
        else:
            pi = next((i for i, l in enumerate(head) if l.startswith("> 协议:")), None)
            if pi is None:
                continue
            lines.insert(pi + 1, f"> 文档版本: {version}")
        if dry:
            changed.append(rel)
            continue
        p.write_text("\n".join(lines), encoding="utf-8")
        changed.append(rel)
    return changed

HEADER = """# 🐉 龍魂命令总表 · 自动生成（DO NOT EDIT）

> 由 `lh doc-sync` 从 `08_BIN/lh.py` SUB_DISPATCH 自动提取。
> 手工改动会被下次同步覆盖。真源: `08_BIN/lh.py`。
> 生成时间: {ts}
> 文档版本: {docs_version}
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


def run_topo_docs_auto_sync() -> list:
    """lh doc-sync 后自动拓扑同步钩子 v1.7（2026-09-05 焊入）：
    扫 docs/topology/*_legion_topo.json 中 auto_docs_sync=true 的图谱
    → subprocess lh_topo.py sync <图谱名>（12_DOCS 文档差异扫描+自动补全节点+verify）
    → 结果并入 JSON 输出；同步引擎自写 ~/.longhun/topo_auto_sync.log"""
    import subprocess as _sp
    results = []
    topo_dir = ROOT / "docs" / "topology"
    if not topo_dir.is_dir():
        return results
    for f in sorted(topo_dir.glob("*_legion_topo.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not d.get("auto_docs_sync"):
            continue
        r = _sp.run([sys.executable, str(ROOT / "08_BIN" / "lh_topo.py"),
                     "sync", str(d.get("topo_name", ""))],
                    capture_output=True, text=True, timeout=180)
        tail = (r.stdout or "").strip().splitlines()
        results.append({
            "topo": d.get("topo_name"),
            "rc": r.returncode,
            "tail": tail[-2:] if tail else [],
        })
    return results


def render(items) -> str:
    lines = [HEADER.format(
        ts=__import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"),
        docs_version=DOCS_VERSION)]
    for key, script, emoji, desc in items:
        lines.append(f"| `lh {key}` | {emoji} | {desc} |")
    lines.append(f"\n共 {len(items)} 条子命令。")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="文档自动同步 v1.0 (lh doc-sync)")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--diff", action="store_true", help="只报告差异，不写文件")
    ap.add_argument("--no-bump", action="store_true", help="跳过 12_DOCS 交付文档版本行更新")
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

    bumped = []
    if not args.no_bump:
        bumped = bump_delivery_versions()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(new_text, encoding="utf-8")
    topo_auto = run_topo_docs_auto_sync()   # v1.7 钩子: 自动拓扑同步（12_DOCS ↔ 对外交付图谱）
    print(json.dumps({
        "tool": "lh-doc-sync", "ok": True, "mode": "write",
        "commands": len(items), "docs_version": DOCS_VERSION,
        "bumped": bumped, "output": str(OUT),
        "topo_auto": topo_auto,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
