#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
构建统一的 cnsh-editor 模块
将分散在项目各处的编辑器相关文件（引擎、UI、关键字登记册、平台编辑器、文档）
整合到 cnsh-editor/，并清理 downloads-imports 中的冗余副本。

执行：
  cd /Users/zuimeidedeyihan/longhun-system/03_知識圖譜
  python3 build_cnsh_editor_module.py
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path("/Users/zuimeidedeyihan/longhun-system")
EDITOR_ROOT = PROJECT_ROOT / "cnsh-editor"
REPORT = PROJECT_ROOT / "03_知識圖譜" / "cnsh_editor_build_report.md"

# 来源 -> 目标（相对 cnsh-editor/）
# 复制项目级核心文件
COPY_FILES = [
    ("cnsh-terminal/engines/cnsh_editor_engine_v2.0.py", "core/cnsh_editor_engine_v2.0.py"),
    ("cnsh-terminal/modules/editor_ui.py", "ui/editor_ui.py"),
    ("CNSH_中文编辑关键字登记册.md", "docs/CNSH_中文编辑关键字登记册.md"),
    ("cnsh-core/language/CNSH编辑器-使用指南.md", "docs/CNSH编辑器-使用指南.md"),
    ("cnsh-core/language/CNSH编辑器-完成报告.md", "docs/CNSH编辑器-完成报告.md"),
    ("cnsh-core/language/CNSH编辑器.html", "web/CNSH编辑器.html"),
    ("bin/build-chinese-editor.sh", "scripts/build-chinese-editor.sh"),
    ("docs/manuals/cnsh-editor-mapper-v1.pdf", "docs/cnsh-editor-mapper-v1.pdf"),
    ("web/p0-controls/memory-editor.html", "web/memory-editor.html"),
    ("cnsh_terminal_v5.0/modules/editor_ui.py", "legacy/cnsh_terminal_v5_editor_ui.py"),
]


def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def copy_src(src_rel: str, dst_rel: str, report_lines):
    src = PROJECT_ROOT / src_rel
    dst = EDITOR_ROOT / dst_rel
    if not src.exists():
        report_lines.append(f"- ⚠️ 源文件不存在，跳过：`{src_rel}`")
        return
    ensure_dir(dst.parent)
    shutil.copy2(src, dst)
    report_lines.append(f"- ✅ 复制 `{src_rel}` -> `{dst_rel}`")


def move_one_and_delete_others(pattern: str, dst_rel: str, report_lines):
    """从 downloads-imports 中找一个文件移动到模块目标，并删除其余重复副本。"""
    sources = sorted(PROJECT_ROOT.rglob(pattern))
    # 只处理 downloads-imports 内的副本
    targets = [p for p in sources if "downloads-imports" in p.parts]
    if not targets:
        report_lines.append(f"- ⚠️ 未找到 `{pattern}`，跳过")
        return
    dst = EDITOR_ROOT / dst_rel
    ensure_dir(dst.parent)
    # 移动第一个到模块
    shutil.move(str(targets[0]), str(dst))
    report_lines.append(f"- ✅ 迁移 `{targets[0].relative_to(PROJECT_ROOT)}` -> `{dst_rel}`")
    # 删除其余
    for p in targets[1:]:
        try:
            p.unlink()
            report_lines.append(f"- 🗑️ 删除重复副本：`{p.relative_to(PROJECT_ROOT)}`")
        except Exception as e:
            report_lines.append(f"- ❌ 删除失败 `{p.relative_to(PROJECT_ROOT)}`: {e}")


def delete_redundant(pattern: str, report_lines):
    """删除 downloads-imports 中已无需保留的副本（项目已有核心版本）。"""
    targets = [p for p in PROJECT_ROOT.rglob(pattern) if "downloads-imports" in p.parts]
    for p in targets:
        try:
            p.unlink()
            report_lines.append(f"- 🗑️ 删除冗余副本：`{p.relative_to(PROJECT_ROOT)}`")
        except Exception as e:
            report_lines.append(f"- ❌ 删除失败 `{p.relative_to(PROJECT_ROOT)}`: {e}")


def write_readme():
    readme = EDITOR_ROOT / "README.md"
    content = f"""# CNSH Editor · 龍魂中文编辑器统一模块

**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**DNA**:`#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-CNSH-EDITOR-v1.0`

## 模块定位

`cnsh-editor` 是龍魂体系中所有编辑器能力的统一入口，把原先分散在 `cnsh-terminal`、`cnsh-core`、`web`、`docs`、`Downloads` 导入区的编辑器相关文件整合为一处，减少重复、便于维护。

## 目录结构

| 目录 | 内容 |
|---|---|
| `core/` | 编辑器引擎 (`cnsh_editor_engine_v2.0.py`) |
| `ui/` | 终端 UI (`editor_ui.py`) |
| `docs/` | 中文编辑关键字登记册、使用指南、完成报告、PDF 手册 |
| `web/` | Web 端编辑器页面 (`CNSH编辑器.html`, `memory-editor.html`) |
| `scripts/` | 构建脚本 (`build-chinese-editor.sh`) |
| `platforms/harmonyos/` | 鸿蒙 ArkTS 编辑器页面 (`CNSHEditor.ets`) |
| `platforms/ios/` | iOS 日记本编辑器 (`DiaryEditor.swift`, `ContentView.swift`) |
| `legacy/` | 历史版本/替代实现 (`cnsh_terminal_v5_editor_ui.py`) |

## 使用方式

- Python 引擎：`from cnsh_editor.core.cnsh_editor_engine_v2_0 import ...`
- 终端 UI：直接运行或 import `cnsh_editor/ui/editor_ui.py`
- 鸿蒙：将 `platforms/harmonyos/CNSHEditor.ets` 复制到 ArkTS 项目 pages 目录
- iOS：将 `platforms/ios/*.swift` 加入 Xcode 项目

## 来源与压缩

本模块通过 `build_cnsh_editor_module.py` 自动构建：
- 项目核心文件复制到本模块
- `cnsh-terminal/downloads-imports/` 中大量重复的 `CNSHEditor.ets`、`cnsh_editor_engine_v2.0.py`、`editor_ui.py` 等副本被迁移或删除
- 详细清单见 `03_知識圖譜/cnsh_editor_build_report.md`

---

**自动生成于**: {datetime.now().isoformat()}
"""
    readme.write_text(content, encoding="utf-8")


def write_manifest(report_lines):
    manifest = EDITOR_ROOT / "MANIFEST.md"
    lines = [
        "# cnsh-editor 来源清单",
        "",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 操作记录",
        "",
    ] + report_lines + [
        "",
        "---",
        "",
        f"**自动生成于**: {datetime.now().isoformat()}",
    ]
    manifest.write_text("\n".join(lines), encoding="utf-8")


def update_graph():
    import generate_downloads_inbox as gdi
    data = gdi.load_graph_data()
    now = datetime.now().strftime("%Y-%m-%d")
    node_id = "cnsh-editor"
    data["nodes"][node_id] = {
        "node_id": node_id,
        "label": "CNSH Editor 统一编辑器模块",
        "type": "component",
        "dna": f"#龍芯⚡️{now}-CNSH-EDITOR-v1.0",
        "description": "龍魂中文编辑器统一模块，整合引擎/UI/关键字/平台编辑器/文档",
        "related_nodes": ["l0-core", "/kimi-webbridge", "downloads/inbox"],
    }
    # 避免重复边
    existing = {(e["source"], e["target"]) for e in data["edges"]}
    for rel, strength in [("l0-core", 0.9), ("/kimi-webbridge", 0.7), ("downloads/inbox", 0.6)]:
        if (node_id, rel) not in existing and (rel, node_id) not in existing:
            data["edges"].append({"source": node_id, "target": rel, "relationship": "relates_to", "strength": strength})
    gdi.GRAPH_DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    gdi.GRAPH_INDEX.write_text(gdi.regenerate_graph_index(data), encoding="utf-8")


def main():
    report_lines = []
    ensure_dir(EDITOR_ROOT)

    for src_rel, dst_rel in COPY_FILES:
        copy_src(src_rel, dst_rel, report_lines)

    # 迁移鸿蒙编辑器页面：移动一个，删除其余重复
    move_one_and_delete_others("CNSHEditor.ets", "platforms/harmonyos/CNSHEditor.ets", report_lines)

    # 迁移 iOS 日记本编辑器
    move_one_and_delete_others("日记编辑器.swift", "platforms/ios/DiaryEditor.swift", report_lines)
    move_one_and_delete_others("ContentView.swift", "platforms/ios/ContentView.swift", report_lines)

    # 删除 downloads-imports 中已冗余的 engine/ui 副本（项目核心版本已复制到模块）
    delete_redundant("cnsh_editor_engine_v2.0.py", report_lines)
    delete_redundant("editor_ui.py", report_lines)

    write_readme()
    write_manifest(report_lines)
    update_graph()

    REPORT.write_text("\n".join([
        "# cnsh-editor 构建报告",
        "",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 操作记录",
        "",
    ] + report_lines + [
        "",
        "---",
        "",
        f"**自动生成于**: {datetime.now().isoformat()}",
    ]), encoding="utf-8")

    print("cnsh-editor 模块构建完成")
    print(f"模块路径：{EDITOR_ROOT}")
    print(f"报告：{REPORT}")


if __name__ == "__main__":
    main()

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·申时·小畜-CONFIRM-SEAL-build_cnsh_editor_mo-53C4543C
