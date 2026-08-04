#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#龍芯⚡️2026-06-21-ENGINE-GENERATE_WORKSPACE_METADATA-FILE1-FILE1-v1.0-2
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-ENGINE-GENERATE_WORKSPACE_METADATA-FILE1-FILE1-v1.0-2
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
"""
为已复制到 docs/<workspace>/ 的 Notion 导出文件生成 README.md 与 scan.json。
"""
import json
import sys
from pathlib import Path
from collections import Counter


def main(target_dir: Path, source_workspace: str, description: str):
    if not target_dir.exists():
        print(f"Target dir not found: {target_dir}")
        sys.exit(1)

    files = sorted([p for p in target_dir.rglob("*") if p.is_file() and p.name not in ("README.md", f"{target_dir.name}-scan.json")])
    category_counter = Counter()
    file_list = []
    for f in files:
        rel = f.relative_to(target_dir)
        category = rel.parts[0] if len(rel.parts) > 1 else "root"
        category_counter[category] += 1
        file_list.append({"path": str(rel), "category": category, "size": f.stat().st_size})

    # README
    lines = [
        f"# {source_workspace}",
        "",
        description,
        "",
        f"- 本目录文件数：{len(files)}",
        "",
        "## 分类目录",
        "",
    ]
    for cat in sorted(category_counter.keys()):
        lines.append(f"### {cat}/（{category_counter[cat]} 个文件）")
        lines.append("")
        for item in file_list:
            if item["category"] == cat:
                lines.append(f"- `{item['path']}`")
        lines.append("")

    readme_path = target_dir / "README.md"
    readme_path.write_text("\n".join(lines), encoding="utf-8")

    # Scan JSON
    scan = {
        "source_workspace": source_workspace,
        "destination_path": str(target_dir),
        "file_count": len(files),
        "category_stats": dict(sorted(category_counter.items())),
        "files": file_list,
    }
    scan_path = target_dir / f"{target_dir.name}-scan.json"
    scan_path.write_text(json.dumps(scan, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Generated {readme_path} and {scan_path} ({len(files)} files)")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python generate_workspace_metadata.py <target_dir> <source_workspace_name> '<description>'")
        sys.exit(1)
    main(Path(sys.argv[1]), sys.argv[2], sys.argv[3])
