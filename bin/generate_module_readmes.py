#!/usr/bin/env python3
"""
为缺失 README.md 的活跃模块生成透明化说明文件。
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
        return f"双击 {script.name} 或在终端执行 bash {script.name}"
    return f"# 参见 {script.name}"


def generate(module: dict) -> str:
    path = ROOT / module["path"]
    name = path.name
    entries = module["entry_scripts"]
    lines = [
        f"# {name}",
        "",
        f"**路径**：`{module['path']}`",
        "",
        "## 状态",
        "",
        "🟡 本 README 由 `bin/generate_module_readmes.py` 自动生成，用于提高仓库透明度。",
        "具体用法请结合源码与实际场景调整。",
        "",
        "## 功能概述",
        "",
        f"该模块包含 {module['files']} 个文件，主要提供 `{name}` 相关能力。",
        "",
        "## 入口脚本",
        "",
    ]
    if entries:
        for e in entries:
            script_path = path / e
            lines.append(f"- `{e}`")
            lines.append(f"  - 尝试用法：`{usage_for(script_path)}`")
    else:
        lines.append("- 暂无明确入口脚本，请查看目录内文件。")

    lines.extend([
        "",
        "## 接口说明",
        "",
        "- 若该模块提供 API，请在源码中查找 `api/`、`router/`、`main.py` 等入口。",
        "- 若为脚本工具，可直接调用上述入口脚本。",
        "",
        "## 注意事项",
        "",
        "- 运行前请确认依赖已安装。",
        "- 建议先阅读源码注释，了解每个脚本的副作用。",
        "",
        f"**DNA**:#龍芯⚡️2026-06-17-NAME_UPPER_REPLACE_-_REPLACE_-README-FILE1_B626-v1.0",
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
