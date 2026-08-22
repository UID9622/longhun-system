#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷓观-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·䷒临-MODULE_INVENTORY-v1.0-984735e1
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂系统 · 功能模块盘点器
扫描主干目录，生成公开透明的模块清单、接口状态与文档覆盖率。
"""
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/zuimeidedeyihan/longhun-system")
OUT_MD = ROOT / "docs" / "MODULE_INVENTORY.md"
OUT_JSON = ROOT / "docs" / "module-inventory.json"

# 忽略目录
IGNORE_DIRS = {
    ".git", "__pycache__", ".pytest_cache", "node_modules", ".venv", "venv",
    ".backups", "logs", "_archive", ".claude", ".obsidian", ".github",
    "cnsh.core.backup", "monitoring.backup", "logging_backup",
}

# 判断是否为活跃模块：包含代码或脚本文件
CODE_EXTS = {".py", ".sh", ".js", ".html", ".command", ".yaml", ".yml", ".json"}


def is_active(module_dir: Path) -> bool:
    if any(p.name in IGNORE_DIRS for p in module_dir.relative_to(ROOT).parents):
        return False
    return any(f.suffix in CODE_EXTS for f in module_dir.rglob("*") if f.is_file())


def inspect(module_dir: Path) -> dict[str, Any]:
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
        "# 龍魂系统 · 功能模块盘点",
        "",
        f"**统计**：共 {len(modules)} 个活跃模块，{complete} 个文档/接口完整，{needs} 个需要补充。",
        "",
        "| 模块路径 | 文件数 | README | 主入口/API | 状态 | 主要入口脚本 |",
        "|----------|--------|--------|-------------|------|--------------|",
    ]
    for m in modules:
        readme = "✅" if m["has_readme"] else "❌"
        entry = "✅" if m["has_main_entry"] or m["has_api"] else "❌"
        status = "🟢 完整" if m["status"] == "complete" else "🟡 需补充"
        scripts = ", ".join(m["entry_scripts"]) or "-"
        lines.append(f"| `{m['path']}` | {m['files']} | {readme} | {entry} | {status} | {scripts} |")

    lines.extend([
        "",
        "## 说明",
        "",
        "- 本清单由 `bin/module_inventory.py` 自动生成。",
        "- `README` 表示该模块是否有说明文件。",
        "- `主入口/API` 表示是否有可调用的入口或接口文件。",
        "- 所有模块必须公开透明，缺失文档的需要补齐。",
        "",
        f"**DNA**:#龍芯⚡️丙午·甲午·壬戌·丙午·䷕贲-MODULE-INVENTORY-FILE1-v1.0",
    ])

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    OUT_JSON.write_text(json.dumps({"modules": modules, "summary": {"total": len(modules), "complete": complete, "needs_doc": needs}}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {OUT_MD} and {OUT_JSON}")


if __name__ == "__main__":
    main()
