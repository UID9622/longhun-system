#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
Downloads 主干迁移脚本
读取 downloads_inbox_manifest.json，将非图片、非安装包的交付物
按类别复制到龍魂主干对应目录，并更新清单、图谱与索引页。

执行：
  cd /Users/zuimeidedeyihan/longhun-system/03_知識圖譜
  python3 migrate_downloads_inbox.py
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path("/Users/zuimeidedeyihan/longhun-system")
MANIFEST = PROJECT_ROOT / "03_知識圖譜" / "downloads_inbox_manifest.json"
INDEX_MD = PROJECT_ROOT / "03_知識圖譜" / "downloads_inbox_index.md"

SKIP_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic", ".bmp", ".tiff"}
SKIP_NAMES = {".DS_Store", "Thumbs.db", "__pycache__", "logs", "audit_logs", "checkpoints"}

# 类别 -> 主干归宿（均在项目根目录下）
DEST_MAP = {
    "skill": "01_技能库/downloads-imports",
    "cnsh": "cnsh-core/downloads-imports",
    "protocol": "01_protocols/downloads-imports",
    "semantic": "cnsh-core/downloads-imports/semantic",
    "audit": "audit/downloads-imports",
    "monitoring": "baobao-guardian/downloads-imports",
    "terminal": "cnsh-terminal/downloads-imports",
    "gateway": "agents/downloads-imports",
    "launcher": "agents/downloads-imports",
    "formula": "cnsh-core/downloads-imports/formula",
    "paper": "_archive/papers",
    "evidence": "_archive/evidence",
    "notion_export": "_archive/notion-exports",
    "media": "_archive/media",
    "agent_session": "_archive/agent-sessions",
    "inbox": "_archive/downloads-inbox/misc",
}


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)
    return p


def unique_dest(parent: Path, name: str) -> Path:
    dest = parent / name
    if not dest.exists():
        return dest
    stem = Path(name).stem
    suffix = Path(name).suffix
    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        dest = parent / new_name
        if not dest.exists():
            return dest
        counter += 1


def should_skip_path(p: Path) -> bool:
    return p.name in SKIP_NAMES or p.suffix.lower() in {".dmg"} or p.name.startswith(".")


SKIP_FILE_EXTS = SKIP_IMAGE_EXTS | {".dmg"}


def copy_item_filtered(source: Path, dest: Path):
    """安全复制文件或目录；自动跳过图片/DMG/隐藏文件，目标已存在则重命名。"""
    dest = unique_dest(dest.parent, dest.name)
    copied_files = 0
    if source.is_dir():
        dest.mkdir(parents=True, exist_ok=False)
        for root, dirs, files in os.walk(source):
            rel = Path(root).relative_to(source)
            cur_dest = dest / rel
            # 过滤掉隐藏/噪声目录
            dirs[:] = [d for d in dirs if d not in SKIP_NAMES and not d.startswith(".")]
            for d in dirs:
                (cur_dest / d).mkdir(parents=True, exist_ok=True)
            for f in files:
                if f in SKIP_NAMES or f.startswith("."):
                    continue
                src_file = Path(root) / f
                if src_file.suffix.lower() in SKIP_FILE_EXTS:
                    continue
                dst_file = unique_dest(cur_dest, f)
                shutil.copy2(src_file, dst_file)
                copied_files += 1
    else:
        if source.suffix.lower() in SKIP_FILE_EXTS:
            return dest, 0
        shutil.copy2(source, dest)
        copied_files = 1
    return dest, copied_files


def migrate():
    manifest_data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    items = manifest_data["items"]
    stats = {"migrated": 0, "skipped": 0, "errors": 0}
    log_lines = []

    for item in items:
        name = item["label"]
        category = item["category"]
        paths = item.get("paths", [])

        # 跳过图片与安装包（保留在 Downloads，截图后续再处理）
        all_exts = {Path(p["path"]).suffix.lower() for p in paths}
        if all_exts.issubset(SKIP_IMAGE_EXTS | {".dmg"}):
            item["status"] = "已跳过（图片/DMG，暂不处理）"
            item["migrated_to"] = None
            stats["skipped"] += 1
            log_lines.append(f"[SKIP] {name}")
            continue

        rel_dest = DEST_MAP.get(category, DEST_MAP["inbox"])
        dest_root = ensure_dir(PROJECT_ROOT / rel_dest)

        migrated_parts = []
        total_copied = 0
        try:
            for p in paths:
                src = Path(p["path"])
                if not src.exists() or should_skip_path(src):
                    continue
                copied, cnt = copy_item_filtered(src, dest_root / src.name)
                if cnt > 0:
                    migrated_parts.append(str(copied.relative_to(PROJECT_ROOT)))
                    total_copied += cnt
            if migrated_parts:
                item["status"] = "已迁移至主干"
                item["migrated_to"] = migrated_parts
                item["files_copied"] = total_copied
                stats["migrated"] += 1
                log_lines.append(f"[MIGRATE] {name} -> {rel_dest} ({total_copied} files)")
            else:
                item["status"] = "已跳过（图片/DMG/无有效文件）"
                item["migrated_to"] = None
                stats["skipped"] += 1
                log_lines.append(f"[SKIP] {name}")
        except Exception as e:
            item["status"] = f"迁移失败: {e}"
            item["migrated_to"] = None
            stats["errors"] += 1
            log_lines.append(f"[ERROR] {name}: {e}")

    # 更新清单与索引
    manifest_data["stats"]["migrated"] = stats["migrated"]
    manifest_data["stats"]["skipped"] = stats["skipped"]
    manifest_data["stats"]["errors"] = stats["errors"]
    manifest_data["stats"]["migrated_at"] = datetime.now().isoformat()
    MANIFEST.write_text(json.dumps(manifest_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # 重新生成索引页与图谱
    import generate_downloads_inbox as gdi
    data = gdi.update_graph_data(items)
    gdi.GRAPH_DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    gdi.GRAPH_INDEX.write_text(gdi.regenerate_graph_index(data), encoding="utf-8")
    INDEX_MD.write_text(gdi.generate_markdown(items, manifest_data["stats"]), encoding="utf-8")

    # 写迁移日志
    log_path = PROJECT_ROOT / "03_知識圖譜" / "downloads_migration.log"
    log_path.write_text("\n".join(log_lines) + "\n", encoding="utf-8")

    print(f"迁移完成：{stats['migrated']} 个，跳过 {stats['skipped']} 个，失败 {stats['errors']} 个")
    print(f"日志：{log_path}")


if __name__ == "__main__":
    migrate()

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·申时·观-CONFIRM-SEAL-migrate_downloads_in-3678FD44
