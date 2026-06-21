#!/usr/bin/env python3
"""
為缺失 README.md 的活躍模塊生成透明化說明文件。
"""
import json
from pathlib import Path

ROOT = Path("/Users/zuimeidedeyihan/longhun-system")
INV = json.loads((ROOT / "docs" / "module-inventory.json").read_text(encoding="utf-8"))


def usage_for(script: Path) -> str:
    ext = script.suffix
    if ext == ".py":
        return f"python3 {script.name} --help"
    if ext == ".sh":
        return f"bash {script.name} --help"
    if ext == ".command":
        return f"雙擊 {script.name} 或在終端執行 bash {script.name}"
    return f"# 參見 {script.name}"


def generate(module: dict) -> str:
    path = ROOT / module["path"]
    name = path.name
    entries = module["entry_scripts"]
    lines = [
        f"# {name}",
        "",
        f"**路徑**：`{module['path']}`",
        "",
        "## 狀態",
        "",
        "🟡 本 README 由 `bin/generate_module_readmes.py` 自動生成，用於提高倉庫透明度。",
        "具體用法請結合源碼與實際場景調整。",
        "",
        "## 功能概述",
        "",
        f"該模塊包含 {module['files']} 個文件，主要提供 `{name}` 相關能力。",
        "",
        "## 入口腳本",
        "",
    ]
    if entries:
        for e in entries:
            script_path = path / e
            lines.append(f"- `{e}`")
            lines.append(f"  - 嘗試用法：`{usage_for(script_path)}`")
    else:
        lines.append("- 暫無明確入口腳本，請查看目錄內文件。")

    lines.extend([
        "",
        "## 接口說明",
        "",
        "- 若該模塊提供 API，請在源碼中查找 `api/`、`router/`、`main.py` 等入口。",
        "- 若為腳本工具，可直接調用上述入口腳本。",
        "",
        "## 注意事項",
        "",
        "- 運行前請確認依賴已安裝。",
        "- 建議先閱讀源碼註釋，了解每個腳本的副作用。",
        "",
        f"**DNA**:#龍芯⚡️2026-06-17-NAME_UPPER_REPLACE_-_REPLACE_-README_A171-v1.0",
    ])
    return "\n".join(lines)


def main():
    count = 0
    for m in INV["modules"]:
        if m["status"] == "needs_doc":
            target = ROOT / m["path"] / "README.md"
            if target.exists():
                continue
            target.write_text(generate(m), encoding="utf-8")
            count += 1
            print(f"Generated {target}")
    print(f"Total generated: {count}")


if __name__ == "__main__":
    main()
