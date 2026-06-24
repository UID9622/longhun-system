#!/usr/bin/env python3
"""
根据 docs/private-shared-imports/ 下现有分类目录，重新生成 README.md。
"""
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/zuimeidedeyihan/longhun-system/docs/private-shared-imports")
README = ROOT / "README.md"

CATEGORY_ORDER = [
    "ai-behavior",
    "cnsh-protocols",
    "architecture",
    "governance",
    "security-audit",
    "persona-tools",
    "api-integration",
    "memory-dna",
    "documentation",
    "decision-records",
    "developer-tools",
]

CATEGORY_TITLES = {
    "ai-behavior": "AI 行为与回复标准",
    "cnsh-protocols": "CNSH 协议与语言规范",
    "architecture": "系统架构",
    "governance": "治理与宪章",
    "security-audit": "安全与审计",
    "persona-tools": "人格与工具",
    "api-integration": "API 与整合",
    "memory-dna": "记忆与 DNA",
    "documentation": "文档与说明",
    "decision-records": "决策记录",
    "developer-tools": "开发者工具",
}


def main():
    stats = {}
    files_by_cat = defaultdict(list)
    for d in sorted(ROOT.iterdir()):
        if d.is_dir():
            files = sorted([f for f in d.iterdir() if f.is_file() and f.name not in ("README.md", f"{d.name}-scan.json")])
            stats[d.name] = len(files)
            for f in files:
                files_by_cat[d.name].append(f.name)

    total = sum(stats.values())

    lines = [
        "# 私人与共享 · Notion 导入文档总览",
        "",
        "本目录收录从 Notion 工作区 `私人与共享` 筛选后融入主干的非敏感核心文档。",
        "",
        f"- **总文件数**：{total}",
        f"- **最后更新**：2026-06-16",
        "",
        "## 分类目录",
        "",
    ]

    for cat in CATEGORY_ORDER:
        count = stats.get(cat, 0)
        if count == 0:
            continue
        title = CATEGORY_TITLES.get(cat, cat)
        lines.append(f"### {title}（{count} 个文件）— `{cat}/`")
        lines.append("")
        for fn in files_by_cat[cat][:20]:
            lines.append(f"- `{fn}`")
        if count > 20:
            lines.append(f"- ... 与另外 {count - 20} 个文件")
        lines.append("")

    lines.extend([
        "## 扫描与审计记录",
        "",
        "- `private-shared-scan.json`：顶层扫描元数据",
        "- `private-shared-scan-subfolders.json`：子文件夹扫描元数据",
        "- `private-shared-batch2-scan.json`：第二批自动化补充扫描",
        "",
        "## 敏感内容排除原则",
        "",
        "- 私人对话、情感/家庭内容、加密密钥、激活码、DNA 身份档案、个人主权绑定档案一律不纳入。",
        "- 如文件内出现真实 API Token / 密码，已替换为占位符。",
        "",
        "**DNA**:#龍芯⚡️2026-06-16-PRIVATE-SHARED-MASTER-FILE1-v1.2",
    ])

    README.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {README} ({total} files)")


if __name__ == "__main__":
    main()
