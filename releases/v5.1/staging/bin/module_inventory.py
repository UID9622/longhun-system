#!/usr/bin/env python3
"""
龍魂系統 · 功能模塊盤點器
掃描主幹目錄，生成公開透明的模塊清單、接口狀態與文檔覆蓋率。
"""
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/zuimeidedeyihan/longhun-system")
OUT_MD = ROOT / "docs" / "MODULE_INVENTORY.md"
OUT_JSON = ROOT / "docs" / "module-inventory.json"

# 忽略目錄
IGNORE_DIRS = {
    ".git", "__pycache__", ".pytest_cache", "node_modules", ".venv", "venv",
    ".backups", "logs", "_archive", ".claude", ".obsidian", ".github",
    "cnsh-core.backup", "monitoring.backup", "logging_backup",
}

# 判斷是否為活躍模塊：包含代碼或腳本文件
CODE_EXTS = {".py", ".sh", ".js", ".html", ".command", ".yaml", ".yml", ".json"}


def is_active(module_dir: Path) -> bool:
    if any(p.name in IGNORE_DIRS for p in module_dir.relative_to(ROOT).parents):
        return False
    return any(f.suffix in CODE_EXTS for f in module_dir.rglob("*") if f.is_file())


def inspect(module_dir: Path) -> dict:
    rel = module_dir.relative_to(ROOT)
    files = [f for f in module_dir.rglob("*") if f.is_file()]
    has_readme = any(f.name.lower() == "readme.md" for f in files)
    has_main_entry = any(f.name in ("main.py", "main.js", "main.sh", "launch.sh", "__main__.py") for f in files)
    has_api = any("api" in f.name.lower() or "router" in f.name.lower() for f in files)
    entry_scripts = [f.name for f in files if f.suffix in (".py", ".sh") and not f.name.startswith("_")][:5]
    return {
        "path": str(rel),
        "files": len(files),
        "has_readme": has_readme,
        "has_main_entry": has_main_entry,
        "has_api": has_api,
        "entry_scripts": entry_scripts,
        "status": "complete" if has_readme and (has_main_entry or has_api) else "needs_doc",
    }


def main():
    modules = []
    for d in sorted(ROOT.iterdir()):
        if d.is_dir() and d.name not in IGNORE_DIRS:
            if is_active(d):
                modules.append(inspect(d))

    complete = sum(1 for m in modules if m["status"] == "complete")
    needs = len(modules) - complete

    lines = [
        "# 龍魂系統 · 功能模塊盤點",
        "",
        f"**統計**：共 {len(modules)} 個活躍模塊，{complete} 個文檔/接口完整，{needs} 個需要補充。",
        "",
        "| 模塊路徑 | 文件數 | README | 主入口/API | 狀態 | 主要入口腳本 |",
        "|----------|--------|--------|-------------|------|--------------|",
    ]
    for m in modules:
        readme = "✅" if m["has_readme"] else "❌"
        entry = "✅" if m["has_main_entry"] or m["has_api"] else "❌"
        status = "🟢 完整" if m["status"] == "complete" else "🟡 需補充"
        scripts = ", ".join(m["entry_scripts"]) or "-"
        lines.append(f"| `{m['path']}` | {m['files']} | {readme} | {entry} | {status} | {scripts} |")

    lines.extend([
        "",
        "## 說明",
        "",
        "- 本清單由 `bin/module_inventory.py` 自動生成。",
        "- `README` 表示該模塊是否有說明文件。",
        "- `主入口/API` 表示是否有可調用的入口或接口文件。",
        "- 所有模塊必須公開透明，缺失文檔的需要補齊。",
        "",
        f"**DNA**: #龍芯⚡️2026-06-17-MODULE-INVENTORY-v1.0",
    ])

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    OUT_JSON.write_text(json.dumps({"modules": modules, "summary": {"total": len(modules), "complete": complete, "needs_doc": needs}}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {OUT_MD} and {OUT_JSON}")


if __name__ == "__main__":
    main()
