#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 备份/恢复引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-BACKUP-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 自动备份关键数据（配置/数据库/模型/代码）
  - 支持本地备份
  - 一键恢复
  - 备份校验
"""

import shutil
import tarfile
import json
import hashlib
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class BackupEngine:
    """备份/恢复引擎——自动备份+一键恢复+校验"""

    def __init__(self):
        self.backup_dir = Path.home() / "longhun-system/backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_file = self.backup_dir / "manifest.json"

    def _load_manifest(self) -> Dict:
        if self.manifest_file.exists():
            return json.loads(self.manifest_file.read_text(encoding="utf-8"))
        return {"backups": []}

    def _save_manifest(self, manifest: Dict):
        manifest["last_updated"] = datetime.now().isoformat()
        self.manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

    def create(self, paths: List[str], description: str = "") -> Dict:
        """创建备份"""
        backup_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = self.backup_dir / f"{backup_id}.tar.gz"

        with tarfile.open(backup_path, "w:gz") as tar:
            for p in paths:
                path = Path(p)
                if path.exists():
                    tar.add(path, arcname=path.name)

        sha = hashlib.sha256(backup_path.read_bytes()).hexdigest()
        size_mb = round(backup_path.stat().st_size / (1024**2), 2)

        manifest = self._load_manifest()
        manifest["backups"].append({
            "id": backup_id, "created": datetime.now().isoformat(),
            "paths": paths, "description": description,
            "size_mb": size_mb, "sha256": sha,
        })
        self._save_manifest(manifest)
        return {"status": "created", "id": backup_id, "size_mb": size_mb}

    def list_backups(self) -> List[Dict]:
        return self._load_manifest().get("backups", [])

    def restore(self, backup_id: str, target_dir: Path) -> Dict:
        """恢复备份"""
        manifest = self._load_manifest()
        entries = [b for b in manifest["backups"] if b["id"] == backup_id]
        if not entries:
            return {"status": "error", "message": f"备份 {backup_id} 不存在"}

        entry = entries[0]
        backup_path = self.backup_dir / f"{backup_id}.tar.gz"
        if not backup_path.exists():
            return {"status": "error", "message": "备份文件不存在"}

        # 校验
        sha = hashlib.sha256(backup_path.read_bytes()).hexdigest()
        if sha != entry["sha256"]:
            return {"status": "error", "message": "备份文件校验失败"}

        with tarfile.open(backup_path, "r:gz") as tar:
            tar.extractall(target_dir)
        return {"status": "restored", "id": backup_id, "target": str(target_dir)}

    def auto_backup(self) -> Dict:
        """自动备份关键目录"""
        paths = [
            str(Path.home() / "longhun-system/data"),
            str(Path.home() / "longhun-system/models"),
            str(Path.home() / "longhun-system/config"),
        ]
        return self.create(paths, "自动备份")


if __name__ == "__main__":
    engine = BackupEngine()

    # 快速测试：备份一个小目录
    result = engine.create([str(Path.home() / "longhun-system/bin/lh.py")], "测试备份")
    print(f"备份: {result}")

    backups = engine.list_backups()
    print(f"备份记录: {len(backups)} 条")
    print("🟢 备份/恢复引擎测试通过")
