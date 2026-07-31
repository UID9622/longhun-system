#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂引擎主控 · 统一配置管理
DNA: #龍芯⚡️丙午·丙申·癸酉·庚申·临-LH-CTL-CONFIG-v1.0-A1B2C3D4
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore


DEFAULT_CONFIG = """# 龍魂引擎主控 · 统一配置
# DNA: #龍芯⚡️丙午·丙申·癸酉·庚申·临-LH-CTL-CONFIG-v1.0

longhun:
  root: ~/longhun-system
  logs_dir: ~/.longhun/logs/lh_ctl
  state_dir: ~/.longhun/state

notion:
  integration_token: ""          # 优先读取环境变量 NOTION_INTEGRATION_TOKEN
  engine_registry_db_id: ""      # 龍魂引擎注册表 v2 的 database_id

engines:
  search:
    script: bin/lh_search_engine.py
    description: 龍魂搜索引擎
    output_dir: data/search_results
    default_args:
      query: ""
  video:
    script: bin/lh_video_studio.py
    description: 龍魂视频工坊
    output_dir: videos
    default_args:
      script: ""
      style: 龍魂
      name: output
  distill:
    script: bin/lh_k3_distill_v39.py
    description: K3 教师模型蒸馏
    output_dir: models/longhun-v1.0/lora_output/k3_distill_v39
    default_args:
      mock: false
      local: false
  audit:
    script: bin/lh_sg_auditor.py
    description: 语义安全闸审计
    output_dir: data/audit
    default_args:
      target: ""
  3d:
    script: bin/lh_3d_pipeline.py
    description: 龍魂图生三维引擎
    output_dir: data/3d_forge
    default_args:
      input: ""
      category: object
      style: realistic

web:
  host: 127.0.0.1
  port: 9630
  dashboard_html: portal/dashboard/index.html

schedule:
  db_path: ~/.longhun/state/scheduler.sqlite
"""


def _expand(path_str: str) -> Path:
    return Path(path_str).expanduser().resolve()


def config_path() -> Path:
    return Path.home() / ".longhun" / "config.yaml"


def ensure_config() -> Path:
    """如果配置文件不存在，则创建默认配置。"""
    p = config_path()
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(DEFAULT_CONFIG, encoding="utf-8")
    return p


def load_config() -> Dict[str, Any]:
    """加载配置；若 YAML 未安装则返回最小默认配置。"""
    ensure_config()
    p = config_path()
    if yaml is None:
        return _minimal_config()
    with open(p, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    # 环境变量覆盖 token
    token = os.environ.get("NOTION_INTEGRATION_TOKEN") or os.environ.get("NOTION_TOKEN")
    if token:
        cfg.setdefault("notion", {})
        cfg["notion"]["integration_token"] = token

    db_id = os.environ.get("NOTION_DATABASE_ID")
    if db_id:
        cfg.setdefault("notion", {})
        cfg["notion"]["engine_registry_db_id"] = db_id

    return cfg


def _minimal_config() -> Dict[str, Any]:
    return {
        "longhun": {
            "root": str(Path.home() / "longhun-system"),
            "logs_dir": str(Path.home() / ".longhun" / "logs" / "lh_ctl"),
            "state_dir": str(Path.home() / ".longhun" / "state"),
        },
        "notion": {
            "integration_token": os.environ.get("NOTION_INTEGRATION_TOKEN", ""),
            "engine_registry_db_id": os.environ.get("NOTION_DATABASE_ID", ""),
        },
        "engines": {
            "search": {"script": "bin/lh_search_engine.py", "description": "龍魂搜索引擎", "output_dir": "data/search_results"},
            "video": {"script": "bin/lh_video_studio.py", "description": "龍魂视频工坊", "output_dir": "videos"},
            "distill": {"script": "bin/lh_k3_distill_v39.py", "description": "K3 蒸馏", "output_dir": "models/longhun-v1.0/lora_output/k3_distill_v39"},
            "audit": {"script": "bin/lh_sg_auditor.py", "description": "语义审计", "output_dir": "data/audit"},
        },
        "web": {"host": "127.0.0.1", "port": 9630, "dashboard_html": "portal/dashboard/index.html"},
        "schedule": {"db_path": str(Path.home() / ".longhun" / "state" / "scheduler.sqlite")},
    }


def project_root(cfg: Dict[str, Any]) -> Path:
    return _expand(cfg.get("longhun", {}).get("root", "~/longhun-system"))


def logs_dir(cfg: Dict[str, Any]) -> Path:
    d = _expand(cfg.get("longhun", {}).get("logs_dir", "~/.longhun/logs/lh_ctl"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def state_dir(cfg: Dict[str, Any]) -> Path:
    d = _expand(cfg.get("longhun", {}).get("state_dir", "~/.longhun/state"))
    d.mkdir(parents=True, exist_ok=True)
    return d
