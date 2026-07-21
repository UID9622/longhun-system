# -*- coding: utf-8 -*-
"""
CNSH v2.1 项目配置管理
DNA: #龍芯⚡️2026-06-29-CNSH-PROJECT-v2.1
"""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_CONFIG = {
    "name": "my-cnsh-project",
    "version": "0.1.0",
    "entry": "main.cnsh",
    "targets": ["python"],
    "deps": [],
    "description": "",
}


class CNSHProject:
    """解析和管理 cnsh.json 项目配置"""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.config = self._load()

    def _load(self) -> Dict[str, Any]:
        config_file = self.root / "cnsh.json"
        if config_file.exists():
            try:
                data = json.loads(config_file.read_text(encoding="utf-8"))
                merged = DEFAULT_CONFIG.copy()
                merged.update(data)
                return merged
            except json.JSONDecodeError as exc:
                raise CNSHProjectError(f"cnsh.json 解析失败: {exc}") from exc
        return DEFAULT_CONFIG.copy()

    @property
    def name(self) -> str:
        return self.config.get("name", DEFAULT_CONFIG["name"])

    @property
    def version(self) -> str:
        return self.config.get("version", DEFAULT_CONFIG["version"])

    @property
    def entry(self) -> Path:
        return self.root / self.config.get("entry", DEFAULT_CONFIG["entry"])

    @property
    def targets(self) -> List[str]:
        return self.config.get("targets", DEFAULT_CONFIG["targets"])

    @property
    def deps(self) -> List[str]:
        return self.config.get("deps", DEFAULT_CONFIG["deps"])

    def save(self):
        config_file = self.root / "cnsh.json"
        config_file.write_text(
            json.dumps(self.config, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


class CNSHProjectError(Exception):
    pass
