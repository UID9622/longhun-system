#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 Notion 配置管理系统 v1.0

DNA: #龍芯⚇️2026-06-01-NOTION-CONFIG-v1.0
UID: 9622
Purpose: 加载、验证和管理 Notion API 配置

Features:
  - 从环境变量加载配置
  - 从 ~/.龍魂_config/ 读取配置文件
  - 验证 API token 和数据库 ID
  - 提供配置验证和初始化
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class NotionConfig:
    """Notion 配置数据类"""
    api_token: str
    api_version: str = "2022-06-28"
    base_url: str = "https://api.notion.com/v1"

    # 三个工作区的数据库 ID
    workspace_1_id: Optional[str] = None  # CNSH 基准测试工作区
    workspace_2_id: Optional[str] = None  # 龍魂知识图谱工作区
    workspace_3_id: Optional[str] = None  # 系统监控工作区

    # CNSH 数据库 ID（工作区 1）
    cnsh_model_db: Optional[str] = None      # 模型认证记录
    cnsh_dimension_db: Optional[str] = None  # 维度测试结果
    cnsh_metric_db: Optional[str] = None     # 性能指标
    cnsh_cert_db: Optional[str] = None       # 认证证书

    # 知识图谱数据库 ID（工作区 2）
    rules_db: Optional[str] = None           # CNSH 规则库
    nodes_db: Optional[str] = None           # IPA 节点注册表
    decision_db: Optional[str] = None        # 系统决策树
    relation_db: Optional[str] = None        # 组件关系图

    # 监控数据库 ID（工作区 3）
    health_db: Optional[str] = None          # 健康检查日志
    baseline_db: Optional[str] = None        # 性能基线
    alert_db: Optional[str] = None           # 警告事件
    audit_db: Optional[str] = None           # 审计日志

    # 运行时配置
    rate_limit: int = 3                      # 每秒请求数
    retry_count: int = 3                     # 重试次数
    timeout: int = 30                        # 超时秒数
    batch_size: int = 100                    # 批量操作大小

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)

    def is_valid(self) -> bool:
        """检查配置是否有效"""
        return bool(self.api_token and len(self.api_token) > 20)


class NotionConfigManager:
    """Notion 配置管理器"""

    def __init__(self):
        self.config_dir = Path.home() / ".龍魂_config"
        self.config_file = self.config_dir / "notion_config.json"
        self.config: Optional[NotionConfig] = None

    def load_from_env(self) -> NotionConfig:
        """从环境变量加载配置"""
        token = os.getenv("NOTION_TOKEN")

        if not token:
            raise ValueError(
                "❌ NOTION_TOKEN 未设置\n"
                "请运行: export NOTION_TOKEN='your-token-here'\n"
                "Token 获取方式: https://www.notion.so/my-integrations"
            )

        config = NotionConfig(
            api_token=token,
            workspace_1_id=os.getenv("NOTION_WORKSPACE_1"),
            workspace_2_id=os.getenv("NOTION_WORKSPACE_2"),
            workspace_3_id=os.getenv("NOTION_WORKSPACE_3"),
            cnsh_model_db=os.getenv("NOTION_CNSH_MODEL_DB"),
            cnsh_dimension_db=os.getenv("NOTION_CNSH_DIMENSION_DB"),
            cnsh_metric_db=os.getenv("NOTION_CNSH_METRIC_DB"),
            cnsh_cert_db=os.getenv("NOTION_CNSH_CERT_DB"),
            rules_db=os.getenv("NOTION_RULES_DB"),
            nodes_db=os.getenv("NOTION_NODES_DB"),
            decision_db=os.getenv("NOTION_DECISION_DB"),
            relation_db=os.getenv("NOTION_RELATION_DB"),
            health_db=os.getenv("NOTION_HEALTH_DB"),
            baseline_db=os.getenv("NOTION_BASELINE_DB"),
            alert_db=os.getenv("NOTION_ALERT_DB"),
            audit_db=os.getenv("NOTION_AUDIT_DB"),
        )

        self.config = config
        return config

    def load_from_file(self) -> Optional[NotionConfig]:
        """从配置文件加载"""
        if not self.config_file.exists():
            return None

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            config = NotionConfig(**data)
            self.config = config
            return config
        except Exception as e:
            print(f"⚠️  加载配置文件失败: {e}")
            return None

    def load(self) -> NotionConfig:
        """加载配置（优先环境变量，然后文件）"""
        try:
            return self.load_from_env()
        except ValueError:
            config = self.load_from_file()
            if config:
                return config
            raise ValueError(
                "❌ 无法加载 Notion 配置\n"
                "请设置 NOTION_TOKEN 环境变量"
            )

    def save(self, config: NotionConfig) -> Path:
        """保存配置到文件"""
        self.config_dir.mkdir(parents=True, exist_ok=True)

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config.to_dict(), f, ensure_ascii=False, indent=2)

        print(f"✅ 配置已保存: {self.config_file}")
        return self.config_file

    def update_database_ids(
        self,
        workspace_id: int,
        **db_ids
    ) -> NotionConfig:
        """更新特定工作区的数据库 ID"""
        if not self.config:
            raise ValueError("请先加载配置")

        # 根据工作区编号更新相应数据库 ID
        if workspace_id == 1:
            self.config.cnsh_model_db = db_ids.get('model_db')
            self.config.cnsh_dimension_db = db_ids.get('dimension_db')
            self.config.cnsh_metric_db = db_ids.get('metric_db')
            self.config.cnsh_cert_db = db_ids.get('cert_db')
        elif workspace_id == 2:
            self.config.rules_db = db_ids.get('rules_db')
            self.config.nodes_db = db_ids.get('nodes_db')
            self.config.decision_db = db_ids.get('decision_db')
            self.config.relation_db = db_ids.get('relation_db')
        elif workspace_id == 3:
            self.config.health_db = db_ids.get('health_db')
            self.config.baseline_db = db_ids.get('baseline_db')
            self.config.alert_db = db_ids.get('alert_db')
            self.config.audit_db = db_ids.get('audit_db')

        return self.config

    def print_status(self):
        """打印配置状态"""
        if not self.config:
            print("❌ 未加载配置")
            return

        print("\n📋 Notion 配置状态")
        print("=" * 60)
        print(f"API Token: {'✅ 已设置' if self.config.api_token else '❌ 未设置'}")
        print(f"API 版本: {self.config.api_version}")

        print("\n工作区和数据库:")
        print(f"  工作区 1 (CNSH 基准): {'✅' if self.config.workspace_1_id else '⏳'}")
        print(f"    - 模型数据库: {'✅' if self.config.cnsh_model_db else '⏳'}")
        print(f"    - 维度数据库: {'✅' if self.config.cnsh_dimension_db else '⏳'}")
        print(f"    - 性能数据库: {'✅' if self.config.cnsh_metric_db else '⏳'}")
        print(f"    - 证书数据库: {'✅' if self.config.cnsh_cert_db else '⏳'}")

        print(f"\n  工作区 2 (知识图谱): {'✅' if self.config.workspace_2_id else '⏳'}")
        print(f"    - 规则库: {'✅' if self.config.rules_db else '⏳'}")
        print(f"    - 节点库: {'✅' if self.config.nodes_db else '⏳'}")
        print(f"    - 决策树: {'✅' if self.config.decision_db else '⏳'}")
        print(f"    - 关系图: {'✅' if self.config.relation_db else '⏳'}")

        print(f"\n  工作区 3 (系统监控): {'✅' if self.config.workspace_3_id else '⏳'}")
        print(f"    - 健康日志: {'✅' if self.config.health_db else '⏳'}")
        print(f"    - 性能基线: {'✅' if self.config.baseline_db else '⏳'}")
        print(f"    - 警告事件: {'✅' if self.config.alert_db else '⏳'}")
        print(f"    - 审计日志: {'✅' if self.config.audit_db else '⏳'}")

        print("\n运行时配置:")
        print(f"  速率限制: {self.config.rate_limit} 请求/秒")
        print(f"  重试次数: {self.config.retry_count}")
        print(f"  超时: {self.config.timeout} 秒")
        print(f"  批量大小: {self.config.batch_size}")
        print("=" * 60)


if __name__ == "__main__":
    # 测试配置管理
    manager = NotionConfigManager()
    try:
        config = manager.load()
        manager.print_status()
    except ValueError as e:
        print(f"❌ {e}")
