# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂技能去重整理工具
DNA: #龍芯⚡️2026-06-29-LONGHUN-SKILL-DEDUP-v1.0

把重复的技能备份到统一目录，只保留主副本，并生成注册表。
"""
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

INVENTORY = Path("/Users/zuimeidedeyihan/_work/inventory_skills.json")
BACKUP_ROOT = Path.home() / ".龍魂" / "backups" / "skills-dedup" / datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
REGISTRY_PATH = Path.home() / ".龍魂" / "longhun_skill_registry.json"


def 提取主路径(notes: str) -> str:
    if "duplicate of" in notes:
        return notes.split("duplicate of")[-1].strip()
    return ""


def 技能目录(skill_md_path: Path) -> Path:
    """返回 SKILL.md 所在的技能目录（通常是父目录）"""
    p = skill_md_path
    # 如果路径在 .backup.*/xxx/SKILL.md，则向上两级拿到 .backup.* 目录
    if ".backup." in str(p):
        parts = p.parts
        for i, part in enumerate(parts):
            if ".backup." in part:
                return Path(*parts[: i + 1])
    return p.parent


def 主函数(dry_run: bool = False):
    if not INVENTORY.exists():
        print(f"❌ 找不到盘点文件: {INVENTORY}")
        return

    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    skills = data.get("skills", [])

    重复项 = [s for s in skills if "duplicate" in s.get("notes", "")]
    注册表 = {}

    # 先建立主副本映射
    for s in skills:
        name = s["name"]
        if "duplicate" not in s.get("notes", ""):
            注册表[name] = {
                "primary_path": str(Path(s["absolute_path"]).parent),
                "scope": s.get("scope"),
                "dna": s.get("dna"),
                "duplicates": [],
            }

    成功 = 0
    跳过 = 0
    失败 = 0

    if not dry_run:
        BACKUP_ROOT.mkdir(parents=True, exist_ok=True)

    print(f"\n🐉 龍魂技能去重整理")
    print(f"发现重复项: {len(重复项)}")
    print(f"备份根目录: {BACKUP_ROOT}\n")

    for s in 重复项:
        src_md = Path(s["absolute_path"])
        src_dir = 技能目录(src_md)
        主相对 = 提取主路径(s.get("notes", ""))
        主名 = s["name"]

        if not src_dir.exists():
            print(f"⚪ 跳过（已不存在）: {src_dir}")
            跳过 += 1
            continue

        if 主名 in 注册表:
            注册表[主名]["duplicates"].append(str(src_dir))

        # 构造备份目标路径，保留原相对结构
        try:
            rel = src_dir.relative_to(Path.home())
        except ValueError:
            rel = src_dir.relative_to(Path("/"))
        dest = BACKUP_ROOT / rel

        if dest.exists():
            print(f"⚪ 跳过（目标已存在）: {dest}")
            跳过 += 1
            continue

        if dry_run:
            print(f"[预览] 移动: {src_dir} -> {dest}")
            成功 += 1
            continue

        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_dir), str(dest))
            print(f"✅ 已备份: {src_dir} -> {dest}")
            成功 += 1
        except Exception as e:
            print(f"❌ 失败: {src_dir} -> {e}")
            失败 += 1

    if not dry_run:
        REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        registry_data = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "backup_root": str(BACKUP_ROOT),
            "total_skills": len(skills),
            "duplicates_backed_up": 成功,
            "skills": 注册表,
        }
        REGISTRY_PATH.write_text(json.dumps(registry_data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n📝 注册表已保存: {REGISTRY_PATH}")

    print(f"\n结果: 成功 {成功}，跳过 {跳过}，失败 {失败}")


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    主函数(dry_run=dry)
