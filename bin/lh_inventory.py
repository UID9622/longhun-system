#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·戊寅·午时·大有-INVENTORY-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂 · 功能盘点器
扫描全系统脚本/引擎/触发词，生成 JSON + Markdown 功能清单

用法:
    python3 bin/lh_inventory.py              # 生成 JSON + Markdown
    python3 bin/lh_inventory.py --json-only  # 只输出 JSON
    python3 bin/lh_inventory.py --md-only    # 只输出 Markdown
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
BIN_DIR = ROOT / "bin"
ENGINES_DIR = ROOT / "engines"
OUTPUT_JSON = ROOT / ".inventory.json"
OUTPUT_MD = ROOT / "功能清单.md"
LH_RUN = BIN_DIR / "lh_run.py"


def extract_triggers_from_lh_run() -> dict:
    """从 lh_run.py 动态提取触发词映射"""
    result = {}
    if not LH_RUN.exists():
        return result
    try:
        content = LH_RUN.read_text(encoding="utf-8")
        # 匹配 dict 中的触发词映射
        for m in re.finditer(r'"([^"]+)"\s*:\s*"([^"]+)"', content):
            trigger = m.group(1)
            script = m.group(2)
            if trigger and script:
                result[trigger] = script
    except Exception:
        pass
    return result


def scan_scripts() -> list:
    """扫描 bin/ 下所有 Python 脚本，获取描述"""
    scripts = []
    for f in sorted(BIN_DIR.glob("*.py")):
        if not f.is_file():
            continue
        # 跳过自引用
        if f.name == "lh_inventory.py":
            continue
        help_text = ""
        try:
            result = subprocess.run(
                [sys.executable, str(f), "--help"],
                capture_output=True, text=True, timeout=2,
            )
            help_text = (result.stdout or result.stderr).strip()
        except Exception:
            pass

        # 提取 docstring 第一行作为描述
        desc = ""
        try:
            first_line = f.read_text(encoding="utf-8").split('\n')
            in_doc = False
            for line in first_line:
                stripped = line.strip()
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    if in_doc:
                        break
                    in_doc = True
                    # 可能同一行结束
                    if len(stripped) > 3 and stripped.rstrip('"\'').strip():
                        desc = stripped.strip('"\'').strip()
                        break
                    continue
                if in_doc and stripped and not stripped.startswith('#') and not stripped.startswith('DNA:'):
                    desc = stripped
                    break
        except Exception:
            pass

        scripts.append({
            "name": f.name,
            "path": str(f),
            "description": desc if desc else (help_text[:120] if help_text else ""),
            "help": help_text[:300],
            "executable": os.access(f, os.X_OK),
        })
    return scripts


def scan_engines() -> list:
    """扫描 engines/ 目录"""
    engines = []
    if ENGINES_DIR.exists():
        for f in sorted(ENGINES_DIR.glob("*.py")):
            engines.append({"name": f.name, "path": str(f)})
    return engines


def scan_cnsh_modules() -> list:
    """扫描 CNSH 模块"""
    modules = []
    cnsh_dir = ROOT / "cnsh" / "core"
    if cnsh_dir.exists():
        for f in cnsh_dir.glob("*.cnsh"):
            modules.append({"name": f.name, "path": str(f)})
    # 也扫描 bin/ 下的 .cnsh
    for f in BIN_DIR.glob("*.cnsh"):
        modules.append({"name": f.name, "path": str(f)})
    return modules


def scan_protocols() -> list:
    """扫描协议文件"""
    protocols = []
    proto_dir = ROOT / "01_protocols"
    if proto_dir.exists():
        for f in sorted(proto_dir.rglob("*.md")):
            protocols.append({"name": f.name, "path": str(f.relative_to(ROOT))})
    return protocols


def count_personas() -> dict:
    """统计人格"""
    personas_dir = ROOT / "personas"
    count = 0
    if personas_dir.exists():
        count = len(list(personas_dir.glob("*.md")))
    exec_dir = ROOT / "bin" / "personas"
    exec_count = 0
    if exec_dir.exists():
        exec_count = len(list(exec_dir.glob("*.py")))
    return {"definitions": count, "executors": exec_count}


def generate_inventory() -> dict:
    """生成完整功能清单"""
    triggers = extract_triggers_from_lh_run()
    scripts = scan_scripts()
    engines = scan_engines()
    cnsh = scan_cnsh_modules()
    protocols = scan_protocols()
    personas = count_personas()

    inventory = {
        "generated_at": datetime.now().isoformat(),
        "generated_by": "lh_inventory.py v1.0",
        "dna": "#龍芯⚡️丙午·乙未·戊寅·午时·大有-INVENTORY-v1.0",
        "summary": {
            "total_scripts": len(scripts),
            "total_executable": sum(1 for s in scripts if s.get("executable")),
            "total_triggers": len(triggers),
            "total_engines": len(engines),
            "total_cnsh_modules": len(cnsh),
            "total_protocols": len(protocols),
            "personas": personas,
        },
        "triggers": triggers,
        "scripts": scripts,
        "engines": engines,
        "cnsh_modules": cnsh,
        "protocols": protocols,
    }
    return inventory


def write_markdown(inv: dict) -> str:
    """生成 Markdown 清单"""
    s = inv["summary"]
    lines = [
        "# 🐉 龙魂系统功能清单",
        "",
        f"> 生成时间: {inv['generated_at']}",
        f"> DNA: {inv['dna']}",
        "",
        "---",
        "",
        "## 概览",
        "",
        f"| 类别 | 数量 |",
        f"|:---|---:|",
        f"| 可执行脚本 (bin/) | {s['total_scripts']} |",
        f"| 其中可执行 | {s['total_executable']} |",
        f"| 触发词 (说人话) | {s['total_triggers']} |",
        f"| 引擎模块 (engines/) | {s['total_engines']} |",
        f"| CNSH 模块 | {s['total_cnsh_modules']} |",
        f"| 协议文档 | {s['total_protocols']} |",
        f"| 人格定义 | {s['personas']['definitions']} |",
        f"| 人格执行器 | {s['personas']['executors']} |",
        "",
        "---",
        "",
        "## 触发词列表 (说人话就能用)",
        "",
    ]

    if inv.get("triggers"):
        for trigger, script in sorted(inv["triggers"].items()):
            lines.append(f"- **{trigger}** → `{script}`")
    else:
        lines.append("*(从 lh_run.py 动态提取)*")

    lines.extend([
        "",
        "---",
        "",
        "## 可执行脚本 (bin/)",
        "",
    ])
    for s_item in inv["scripts"]:
        lines.append(f"### `{s_item['name']}`")
        if s_item.get("description"):
            lines.append(f">{s_item['description']}")
        if s_item.get("executable"):
            lines.append("✅ 可执行")
        else:
            lines.append("⚠️ 无执行权限")
        if s_item.get("help"):
            help_preview = s_item["help"][:200].replace("\n", " ")
            lines.append(f"```\n{help_preview}\n```")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## 引擎模块 (engines/)",
        "",
    ])
    for e in inv["engines"]:
        lines.append(f"- `{e['name']}`")

    lines.extend([
        "",
        "---",
        "",
        "## CNSH 核心模块",
        "",
    ])
    for c in inv["cnsh_modules"]:
        lines.append(f"- `{c['name']}`")

    lines.extend([
        "",
        "---",
        "",
        "## 协议文档 (01_protocols/)",
        "",
    ])
    for p in inv["protocols"]:
        lines.append(f"- [{p['name']}]({p['path']})")

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂功能盘点器")
    parser.add_argument("--json-only", action="store_true", help="只输出 JSON")
    parser.add_argument("--md-only", action="store_true", help="只输出 Markdown")
    args = parser.parse_args()

    inv = generate_inventory()

    if not args.md_only:
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(inv, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON: {OUTPUT_JSON}")

    if not args.json_only:
        md = write_markdown(inv)
        with open(OUTPUT_MD, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"✅ Markdown: {OUTPUT_MD}")

    s = inv["summary"]
    print(f"\n📊 盘点完成:")
    print(f"   脚本: {s['total_scripts']} | 引擎: {s['total_engines']} | 触发词: {s['total_triggers']}")
    print(f"   CNSH: {s['total_cnsh_modules']} | 协议: {s['total_protocols']} | 人格: {s['personas']['definitions']}+{s['personas']['executors']}")


if __name__ == "__main__":
    main()
