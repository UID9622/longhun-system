#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-ROLLBACK-PIPELINE-UID9622
# 创建者: 诸葛鑫（UID9622）
"""
🐉 龍魂 · 回滚机制 v1.0
功能: 部署失败自动回滚到上一个稳定版本（P0，回滚是发布的一部分）
"""

import json
import shutil
import tarfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from .generate_dna import generate_dna


class RollbackPipeline:
    """回滚流水线"""

    def __init__(self, deploy_dir: Path):
        self.deploy_dir = deploy_dir
        self.rollback_dir = deploy_dir / "rollback_history"
        self.rollback_dir.mkdir(parents=True, exist_ok=True)

    def save_version(self, version: str, source_path: Path) -> Dict:
        """保存版本用于回滚"""
        archive_path = self.rollback_dir / f"{version}_{int(datetime.now().timestamp())}.tar.gz"
        shutil.make_archive(
            str(archive_path).replace('.tar.gz', ''),
            'gztar',
            source_path
        )

        metadata = {
            "version": version,
            "archive": str(archive_path),
            "timestamp": datetime.now().isoformat(),
            "dna": generate_dna("ROLLBACK-SAVE")
        }

        meta_path = self.rollback_dir / f"{version}.meta.json"
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        return metadata

    def rollback(self, target_version: str) -> Dict:
        """回滚到指定版本"""
        meta_path = self.rollback_dir / f"{target_version}.meta.json"
        if not meta_path.exists():
            return {"status": "failed", "error": f"版本 {target_version} 不存在"}

        with open(meta_path, encoding='utf-8') as f:
            metadata = json.load(f)

        archive_path = Path(metadata["archive"])
        if not archive_path.exists():
            return {"status": "failed", "error": f"归档文件不存在: {archive_path}"}

        # 解压回滚
        rollback_target = self.deploy_dir / f"rollback_{target_version}"
        rollback_target.mkdir(exist_ok=True)

        with tarfile.open(archive_path, 'r:gz') as tar:
            tar.extractall(rollback_target)

        # 替换当前部署（旧版本先备份，不删除 —— 不删除只冻结）
        current = self.deploy_dir / "current"
        if current.exists():
            backup = self.deploy_dir / f"current_backup_{int(datetime.now().timestamp())}"
            shutil.move(current, backup)

        shutil.move(rollback_target, current)

        return {
            "status": "success",
            "version": target_version,
            "timestamp": datetime.now().isoformat(),
            "dna": generate_dna("ROLLBACK-EXEC")
        }

    def list_versions(self) -> List[Dict]:
        """列出可回滚的版本"""
        versions = []
        for meta_file in self.rollback_dir.glob("*.meta.json"):
            with open(meta_file, encoding='utf-8') as f:
                data = json.load(f)
            versions.append({
                "version": data["version"],
                "timestamp": data["timestamp"],
                "archive": data["archive"]
            })
        return sorted(versions, key=lambda x: x["timestamp"], reverse=True)
