# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂能力与训练自动迭代系统 · 配置中心
DNA: #龍芯⚡️2026-06-28-LONGHUN-CAPABILITY-CONFIG-v1.0
"""
from pathlib import Path


class Config:
    """系统配置。"""

    # DNA 前缀
    dna_prefix = "#龍芯⚡️"

    # 路径
    project_root = Path(__file__).resolve().parent.parent
    registry_path = project_root / "capability_registry.json"
    log_dir = project_root / "logs"
    model_dir = project_root / "models"
    audit_log = log_dir / "capability_audit.jsonl"
    train_log = log_dir / "train_pipeline.jsonl"
    train_state = project_root / "train_state.json"

    # 训练相关
    train_raw_dir = Path.home() / "longhun-system" / "train" / "data" / "raw"
    train_script = Path.home() / "longhun-system" / "train" / "scripts" / "train.sh"
    train_output_dir = Path.home() / "longhun-system" / "train" / "output"
    train_model_dir = train_output_dir / "models"
    train_report_path = train_output_dir / "龍魂-0.1B_train_report.json"

    # 模型版本管理
    active_model_marker = model_dir / "active_model.json"
    model_backup_dir = model_dir / "backups"
    max_model_backups = 5

    # 守护进程
    daemon_interval_seconds = 30
    daemon_pid = project_root / "daemon.pid"

    # 评估阈值：新模型 loss 降低比例超过该值才上线
    deploy_improvement_threshold = 0.05

    # 能力展示页面
    web_page = project_root / "web" / "index.html"

    log_dir.mkdir(parents=True, exist_ok=True)
    model_dir.mkdir(parents=True, exist_ok=True)
    model_backup_dir.mkdir(parents=True, exist_ok=True)
