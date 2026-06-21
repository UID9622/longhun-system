#!/usr/bin/env python3
"""
根據 docs/private-shared-imports/ 下現有分類目錄，重新生成 README.md。
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
    "ai-behavior": "AI 行為與回覆標準",
    "cnsh-protocols": "CNSH 協議與語言規範",
    "architecture": "系統架構",
    "governance": "治理與憲章",
    "security-audit": "安全與審計",
    "persona-tools": "人格與工具",
    "api-integration": "API 與整合",
    "memory-dna": "記憶與 DNA",
    "documentation": "文檔與說明",
    "decision-records": "決策記錄",
    "developer-tools": "開發者工具",
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
        "# 私人与共享 · Notion 導入文檔總覽",
        "",
        "本目錄收錄從 Notion 工作區 `私人与共享` 篩選後融入主幹的非敏感核心文檔。",
        "",
        f"- **總文件數**：{total}",
        f"- **最後更新**：2026-06-16",
        "",
        "## 分類目錄",
        "",
    ]

    for cat in CATEGORY_ORDER:
        count = stats.get(cat, 0)
        if count == 0:
            continue
        title = CATEGORY_TITLES.get(cat, cat)
        lines.append(f"### {title}（{count} 個文件）— `{cat}/`")
        lines.append("")
        for fn in files_by_cat[cat][:20]:
            lines.append(f"- `{fn}`")
        if count > 20:
            lines.append(f"- ... 與另外 {count - 20} 個文件")
        lines.append("")

    lines.extend([
        "## 掃描與審計記錄",
        "",
        "- `private-shared-scan.json`：頂層掃描元數據",
        "- `private-shared-scan-subfolders.json`：子文件夾掃描元數據",
        "- `private-shared-batch2-scan.json`：第二批自動化補充掃描",
        "",
        "## 敏感內容排除原則",
        "",
        "- 私人對話、情感/家庭內容、加密密鑰、激活碼、DNA 身份檔案、個人主權綁定檔案一律不納入。",
        "- 如文件內出現真實 API Token / 密碼，已替換為佔位符。",
        "",
        "**DNA**:#龍芯⚡️2026-06-16-PRIVATE-SHARED-MASTER-FILE1-v1.2",
    ])

    README.write_text("\n".join(lines), encoding="utf-8")
    print(f"Updated {README} ({total} files)")


if __name__ == "__main__":
    main()
