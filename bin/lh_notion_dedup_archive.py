#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·DEDUP-ARCHIVE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion去重归档执行器 v1.0

读取 reorganize_plan.json 中的 local_dedup_suggestions，
将本地已有Notion副本的文件归档到 _archive/notion_local_dedup/ 目录。

铁律：不删文件，只冻结归档。
DNA: #龍芯⚡️丙午·辛未·DEDUP-ARCHIVE-v1.0
"""
import json
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
PLAN_FILE = ROOT / "data/notion_scan/reorganize_plan.json"
ARCHIVE_DIR = ROOT / "_archive/notion_local_dedup/"
MANIFEST_FILE = ARCHIVE_DIR / "archive_manifest.json"


def main():
    # 1. Load plan
    with open(PLAN_FILE) as f:
        plan = json.load(f)

    suggestions = plan["local_dedup_suggestions"]
    total_kb = plan.get("total_local_dedup_kb", 0)

    print(f"🐉 龍魂 · Notion去重归档执行器 v1.0")
    print(f"📊 计划归档: {len(suggestions)} 个文件")
    print(f"💾 预计释放: {total_kb}KB ≈ {total_kb/1024:.1f}MB")
    print()

    # 2. Create archive directory
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    archived = []
    skipped = []
    errors = []

    for i, item in enumerate(suggestions, 1):
        src = ROOT / item["path"]
        if not src.exists():
            skipped.append({"path": item["path"], "reason": "文件不存在"})
            continue

        # Preserve relative directory structure
        rel_dir = Path(item["path"]).parent
        dst_dir = ARCHIVE_DIR / rel_dir
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / Path(item["path"]).name

        try:
            shutil.move(str(src), str(dst))
            archived.append({
                "original": item["path"],
                "archived_to": str(dst.relative_to(ROOT)),
                "title": item["title"],
                "size_kb": item["size_kb"],
            })
        except Exception as e:
            errors.append({"path": item["path"], "error": str(e)})
            continue

        if i % 20 == 0:
            print(f"   进度: {i}/{len(suggestions)}")

    # 3. Write manifest
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "dna": "#龍芯⚡️丙午·辛未·DEDUP-ARCHIVE-v1.0",
        "total_archived": len(archived),
        "total_skipped": len(skipped),
        "total_errors": len(errors),
        "total_size_kb": sum(a["size_kb"] for a in archived),
        "archived": archived,
        "skipped": skipped,
        "errors": errors,
    }
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 4. Summary
    print()
    print("=" * 60)
    print(f"✅ 归档完成")
    print(f"   📦 已归档: {len(archived)} 文件")
    print(f"   ⏭️ 跳过: {len(skipped)} 文件（不存在）")
    print(f"   ❌ 错误: {len(errors)} 文件")
    print(f"   💾 释放: {manifest['total_size_kb']}KB ≈ {manifest['total_size_kb']/1024:.1f}MB")
    print(f"   📄 清单: {MANIFEST_FILE}")
    print(f"   📁 归档目录: {ARCHIVE_DIR}")
    print(f"🐉 DNA: #龍芯⚡️丙午·辛未·DEDUP-ARCHIVE-v1.0")

    return manifest


if __name__ == "__main__":
    main()
