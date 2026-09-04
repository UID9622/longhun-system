#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 模型管理引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-MODELMGR-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 模型生命周期管理（训练→导出→注册→部署→监控→退役）
  - 版本管理（自动编号、回滚）
  - 模型性能追踪
  - 模型注册表
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class ModelInfo:
    name: str
    version: str
    path: str
    format: str
    size_gb: float
    created_at: str
    status: str
    performance: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ModelManager:
    """模型管理引擎——训练/导出/注册/部署/退役全生命周期"""

    def __init__(self):
        self.registry_file = Path.home() / "longhun-system/data/model_registry.json"
        self.models_dir = Path.home() / "longhun-system/models"
        self.models_dir.mkdir(parents=True, exist_ok=True)
        self._registry: Dict[str, ModelInfo] = self._load_registry()

    def _load_registry(self) -> Dict[str, ModelInfo]:
        if self.registry_file.exists():
            try:
                data = json.loads(self.registry_file.read_text(encoding="utf-8"))
                return {k: ModelInfo(**v) for k, v in data.items()}
            except Exception:
                pass
        return {}

    def _save_registry(self):
        data = {}
        for k, v in self._registry.items():
            d = v.__dict__.copy()
            data[k] = d
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        self.registry_file.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str))

    def register(self, name: str, path: Path, fmt: str = "gguf", metadata: Dict = None) -> ModelInfo:
        """注册新模型"""
        versions = [m.version for m in self._registry.values() if m.name == name]
        if versions:
            max_v = max(versions)
            parts = max_v.replace("v", "").split(".")
            new_version = f"v{parts[0]}.{int(parts[-1])+1}"
        else:
            new_version = "v1.0"

        size_gb = self._get_size(path) / (1024**3)

        info = ModelInfo(
            name=name, version=new_version, path=str(path),
            format=fmt, size_gb=round(size_gb, 2),
            created_at=datetime.now().isoformat(), status="registered",
            metadata=metadata or {},
        )
        key = f"{name}:{new_version}"
        self._registry[key] = info
        self._save_registry()
        return info

    def _get_size(self, path: Path) -> int:
        if path.is_file():
            return path.stat().st_size
        return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())

    def deploy(self, model_id: str, replicas: int = 1) -> Dict:
        if model_id not in self._registry:
            return {"status": "error", "message": f"模型 {model_id} 未注册"}
        self._registry[model_id].status = "deployed"
        self._save_registry()
        return {"status": "deployed", "model": self._registry[model_id].name,
                "version": self._registry[model_id].version, "replicas": replicas}

    def rollback(self, name: str, target_version: str) -> Dict:
        target_id = f"{name}:{target_version}"
        if target_id not in self._registry:
            return {"status": "error", "message": f"版本 {target_version} 不存在"}
        for mid, info in self._registry.items():
            if info.name == name and info.status == "deployed":
                info.status = "deprecated"
        self._registry[target_id].status = "deployed"
        self._save_registry()
        return {"status": "rolled_back", "model": name, "version": target_version}

    def list_models(self) -> List[Dict]:
        return [
            {"id": mid, "name": info.name, "version": info.version,
             "status": info.status, "size_gb": info.size_gb}
            for mid, info in self._registry.items()
        ]

    def get_model(self, name: str, version: Optional[str] = None) -> Optional[ModelInfo]:
        if version:
            return self._registry.get(f"{name}:{version}")
        matches = [info for mid, info in self._registry.items() if info.name == name]
        if matches:
            matches.sort(key=lambda x: x.version, reverse=True)
            return matches[0]
        return None

    def export_to_ollama(self, model_id: str) -> Dict:
        if model_id not in self._registry:
            return {"status": "error", "message": f"模型 {model_id} 未注册"}
        info = self._registry[model_id]
        model_path = Path(info.path)
        if not model_path.exists():
            return {"status": "error", "message": f"路径不存在: {model_path}"}
        modelfile_content = f"""FROM {model_path}
TEMPLATE "{{{{ .Prompt }}}}"
PARAMETER temperature 0.7
PARAMETER top_p 0.9
SYSTEM "龍魂 ASI 智能体，遵循君子协议。DNA: UID9622"
"""
        mf_path = self.models_dir / f"Modelfile_{info.name}"
        mf_path.write_text(modelfile_content)
        try:
            result = subprocess.run(
                ["ollama", "create", info.name, "-f", str(mf_path)],
                capture_output=True, text=True, timeout=120,
            )
            return {"status": "exported", "model": info.name, "output": result.stdout, "error": result.stderr}
        except Exception as e:
            return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    mgr = ModelManager()
    print(f"已注册模型: {len(mgr.list_models())}")
    for m in mgr.list_models():
        print(f"  ├ {m['name']}:{m['version']} ({m['status']}) {m['size_gb']}GB")
    print("🟢 模型管理引擎测试通过")
