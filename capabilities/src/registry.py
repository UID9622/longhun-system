#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂能力与训练自动迭代系统 · 能力注册表管理
DNA: #龍芯⚡️2026-06-28-LONGHUN-CAPABILITY-REGISTRY-MODULE-v1.0
"""
import json
import subprocess
from pathlib import Path
from datetime import datetime

from config import Config


class CapabilityRegistry:
    """能力注册表管理器。"""

    def __init__(self, path=None):
        self.path = Path(path) if path else Config.registry_path
        self.data = self.load()

    def load(self):
        if not self.path.exists():
            return {"_meta": {}, "categories": {}, "capabilities": {}}
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.data["_meta"]["updated_at"] = datetime.now().isoformat()
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def list_capabilities(self, category=None, status=None):
        caps = self.data.get("capabilities", {})
        result = []
        for name, info in caps.items():
            if category and info.get("category") != category:
                continue
            if status and info.get("status") != status:
                continue
            result.append({"name": name, **info})
        return result

    def get(self, name):
        return self.data.get("capabilities", {}).get(name)

    def set_override(self, name, overridden=True):
        cap = self.get(name)
        if not cap:
            return False
        cap["rules_overridden"] = overridden
        cap["overridden_at"] = datetime.now().isoformat()
        self.save()
        return True

    def scan_ollama(self):
        """扫描 Ollama 本地模型并注册。"""
        try:
            out = subprocess.run(
                ["ollama", "list"],
                capture_output=True, text=True, timeout=30
            )
            lines = out.stdout.strip().splitlines()
            added = []
            for line in lines[1:]:
                parts = line.split()
                if not parts:
                    continue
                model_name = parts[0]
                cap_name = f"ollama-{model_name.replace(':', '-')}"
                if cap_name in self.data["capabilities"]:
                    continue
                self.data["capabilities"][cap_name] = {
                    "name": cap_name,
                    "display_name": f"本地 {model_name}",
                    "category": "local_model",
                    "provider": "ollama",
                    "status": "active",
                    "rules_overridden": False,
                    "input_format": '{"messages": [{"role":"user","content":"..."}]}',
                    "output_format": '{"content":"..."}',
                    "invoke": {
                        "type": "ollama",
                        "model": model_name,
                        "endpoint": "http://localhost:11434/api/chat"
                    },
                    "capacity": ["本地", "私有", "离线"],
                    "dna": f"{Config.dna_prefix}{datetime.now().strftime('%Y%m%d')}-CAP-OLLAMA-{model_name.upper().replace(':','-')}-v1.0"
                }
                added.append(cap_name)
            if added:
                self.save()
            return added
        except Exception as e:
            return [f"error: {e}"]

    def get_stats(self):
        caps = self.data.get("capabilities", {})
        total = len(caps)
        overridden = sum(1 for c in caps.values() if c.get("rules_overridden"))
        by_category = {}
        for c in caps.values():
            cat = c.get("category", "unknown")
            by_category[cat] = by_category.get(cat, 0) + 1
        return {
            "total": total,
            "overridden": overridden,
            "pending_override": total - overridden,
            "by_category": by_category,
        }
