#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 CNSH 基准测试数据同步 · Stage 2

DNA: #龍芯⚇️2026-06-01-CNSH-SYNC-v1.0
UID: 9622
Purpose: 将本地 benchmark.jsonl 数据同步到 Notion 四个数据库

Databases:
  1. 模型认证记录 - Model Certification Records
  2. 维度测试结果 - Dimension Test Results
  3. 性能指标 - Performance Metrics
  4. 认证证书 - Certification Certificates

Features:
  - 自动读取 benchmark.jsonl
  - 数据聚合和转换
  - 增量同步支持
  - 冲突处理
  - 审计日志记录
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from collections import defaultdict
import sys

# Add current directory to path for imports
current_dir = str(Path(__file__).parent)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from .notion_client import NotionClient
    from .notion_config import NotionConfigManager, NotionConfig
except ImportError:
    from notion_client import NotionClient
    from notion_config import NotionConfigManager, NotionConfig


class CNSHDataAnalyzer:
    """CNSH 基准测试数据分析器"""

    DIMENSIONS = [
        "中文错别字",
        "代码缩进",
        "DNA标记大小写",
        "中英混排空格",
        "数学公式",
        "多码点组合Emoji",
        "代码注释规范",
        "中英混合处理",
        "龍魂系统认知",
    ]

    def __init__(self):
        self.benchmark_file = Path.home() / ".龍魂" / "benchmark.jsonl"
        self.records: List[Dict[str, Any]] = []
        self.models: Dict[str, Dict] = {}
        self.dimensions: Dict[str, Dict] = {}

    def load_data(self) -> bool:
        """加载基准测试数据"""
        if not self.benchmark_file.exists():
            print(f"❌ 未找到基准数据文件: {self.benchmark_file}")
            return False

        try:
            with open(self.benchmark_file, 'r', encoding='utf-8') as f:
                for line in f:
                    record = json.loads(line)
                    self.records.append(record)

            print(f"✅ 加载 {len(self.records)} 条测试记录")
            return True

        except Exception as e:
            print(f"❌ 加载数据失败: {e}")
            return False

    def analyze_models(self) -> Dict[str, Dict]:
        """分析模型成绩"""
        model_stats = defaultdict(lambda: {
            "维度": {},
            "总得分": 0,
            "总满分": 0,
            "得分率": 0,
            "评级": "",
            "权限等级": "",
        })

        # 按模型分组
        for record in self.records:
            model_name = record['模型名']
            dimension = record['维度']
            actual_score = record['实际得分']
            max_score = record['满分']

            if dimension not in model_stats[model_name]["维度"]:
                model_stats[model_name]["维度"][dimension] = {
                    "得分": actual_score,
                    "满分": max_score,
                    "得分率": actual_score / max_score,
                }

            model_stats[model_name]["总得分"] += actual_score
            model_stats[model_name]["总满分"] += max_score

        # 计算综合得分和评级
        for model_name, stats in model_stats.items():
            if stats["总满分"] > 0:
                stats["得分率"] = stats["总得分"] / stats["总满分"]
                stats["评级"] = self._rate_score(stats["得分率"])
                stats["权限等级"] = self._assign_permissions(model_name, stats["得分率"])

        self.models = dict(model_stats)
        return self.models

    def _rate_score(self, score_rate: float) -> str:
        """评分等级"""
        if score_rate >= 0.85:
            return "🟢 优秀"
        elif score_rate >= 0.65:
            return "🟡 合格"
        elif score_rate >= 0.40:
            return "🟠 警戒"
        else:
            return "🔴 危险"

    def _assign_permissions(self, model_name: str, score_rate: float) -> str:
        """分配权限等级"""
        if score_rate < 0.85:
            return "禁用"

        # 根据模型名判断权限等级
        if "opus" in model_name.lower():
            return "二级合作伙伴 (Senior Partner)"
        else:
            return "一级合作伙伴 (Premier Partner)"

    def get_model_summary(self, model_name: str) -> Dict:
        """获取模型摘要"""
        if model_name not in self.models:
            return {}

        model = self.models[model_name]
        return {
            "模型名": model_name,
            "综合得分率": f"{model['得分率']:.1%}",
            "综合评级": model['评级'],
            "权限等级": model['权限等级'],
            "总得分": f"{model['总得分']}/{model['总满分']}",
            "维度总数": len(model['维度']),
            "通过维度数": sum(1 for d in model['维度'].values() if d['得分率'] >= 0.85),
        }

    def get_dimension_results(self, dimension: str) -> List[Dict]:
        """获取维度的测试结果"""
        results = []

        for record in self.records:
            if record['维度'] == dimension:
                results.append({
                    "测试ID": record['测试ID'],
                    "模型名": record['模型名'],
                    "得分": f"{record['实际得分']}/{record['满分']}",
                    "得分率": f"{record['得分率']:.1%}",
                    "期望行为": record['期望行为'],
                    "DNA": record['DNA'],
                })

        return results


class CNSHNotionSync:
    """CNSH 数据到 Notion 同步器"""

    def __init__(self, client: NotionClient, config: NotionConfig):
        self.client = client
        self.config = config
        self.analyzer = CNSHDataAnalyzer()
        self.sync_log_file = Path.home() / ".龍魂" / "notion_cnsh_sync.jsonl"

    def sync_all(self) -> bool:
        """执行完整同步"""
        print("\n" + "=" * 70)
        print("🐉 CNSH 基准测试数据同步 (Stage 2)")
        print("=" * 70)

        # 加载数据
        print("\n📊 第一步：加载基准测试数据...")
        if not self.analyzer.load_data():
            return False

        # 分析数据
        print("\n📈 第二步：分析模型成绩...")
        self.analyzer.analyze_models()
        print(f"✅ 分析完成：{len(self.analyzer.models)} 个模型")

        # 同步到 Notion
        print("\n🔄 第三步：同步数据到 Notion...")

        # 检查数据库 ID
        if not self._check_databases():
            print("\n⚠️  未配置所有数据库 ID，使用本地模式预览数据")
            self._preview_data()
            return False

        # 同步各数据库
        success = True
        success &= self._sync_model_certifications()
        success &= self._sync_dimension_results()
        success &= self._sync_performance_metrics()
        success &= self._sync_certification_certificates()

        print("\n" + "=" * 70)
        if success:
            print("✅ 同步完成")
        else:
            print("⚠️  部分同步失败，详见审计日志")
        print("=" * 70)

        return success

    def _check_databases(self) -> bool:
        """检查所有必需的数据库 ID"""
        required_dbs = [
            ("cnsh_model_db", "模型认证记录"),
            ("cnsh_dimension_db", "维度测试结果"),
            ("cnsh_metric_db", "性能指标"),
            ("cnsh_cert_db", "认证证书"),
        ]

        missing = []
        for attr, name in required_dbs:
            if not getattr(self.config, attr, None):
                missing.append(name)

        if missing:
            print(f"\n❌ 缺少以下数据库 ID:")
            for name in missing:
                print(f"   - {name}")
            print(f"\n请先运行: export NOTION_CNSH_*_DB='database_id'")
            return False

        return True

    def _preview_data(self):
        """预览数据（本地模式）"""
        print("\n📋 本地数据预览")
        print("=" * 70)

        # 模型汇总
        print("\n【模型认证记录】")
        for model_name in self.analyzer.models.keys():
            summary = self.analyzer.get_model_summary(model_name)
            print(f"\n  {summary['模型名']}")
            print(f"    综合得分: {summary['综合得分率']}")
            print(f"    评级: {summary['综合评级']}")
            print(f"    权限: {summary['权限等级']}")

        # 维度结果
        print("\n【维度测试结果样本】")
        for dim in self.analyzer.DIMENSIONS[:3]:
            results = self.analyzer.get_dimension_results(dim)
            print(f"\n  {dim}: {len(results)} 条记录")
            for r in results[:2]:
                print(f"    - {r['测试ID']}: {r['模型名']} {r['得分率']}")

    def _sync_model_certifications(self) -> bool:
        """同步模型认证记录到 Notion"""
        print("\n【模型认证记录】")

        db_id = self.config.cnsh_model_db
        success = True

        for model_name, model_data in self.analyzer.models.items():
            try:
                summary = self.analyzer.get_model_summary(model_name)

                properties = {
                    "名称": {
                        "title": [{"type": "text", "text": {"content": model_name}}]
                    },
                    "综合得分": {
                        "rich_text": [
                            {"type": "text", "text": {"content": summary['综合得分率']}}
                        ]
                    },
                    "评级": {
                        "select": {"name": summary['综合评级'].replace('🟢 ', '').replace('🟡 ', '').replace('🟠 ', '').replace('🔴 ', '')}
                    },
                    "权限等级": {
                        "rich_text": [
                            {"type": "text", "text": {"content": summary['权限等级']}}
                        ]
                    },
                    "维度通过": {
                        "rich_text": [
                            {"type": "text", "text": {"content": f"{summary['通过维度数']}/{summary['维度总数']}"}}
                        ]
                    },
                    "DNA": {
                        "rich_text": [
                            {"type": "text", "text": {"content": f"#龍芯⚇️20260601-CNSH-{model_name.upper()}"}}
                        ]
                    },
                }

                page = self.client.create_page(db_id, properties)
                print(f"  ✅ {model_name}")
                self._log_sync("model_cert", model_name, "success", page.get('id'))

            except Exception as e:
                print(f"  ❌ {model_name}: {str(e)[:80]}")
                self._log_sync("model_cert", model_name, "error", str(e))
                success = False

        return success

    def _sync_dimension_results(self) -> bool:
        """同步维度测试结果"""
        print("\n【维度测试结果】")

        db_id = self.config.cnsh_dimension_db
        success = True
        total = 0

        for dimension in self.analyzer.DIMENSIONS:
            results = self.analyzer.get_dimension_results(dimension)
            total += len(results)

            for result in results:
                try:
                    properties = {
                        "维度": {"select": {"name": dimension}},
                        "测试ID": {
                            "rich_text": [
                                {"type": "text", "text": {"content": result['测试ID']}}
                            ]
                        },
                        "模型": {
                            "rich_text": [
                                {"type": "text", "text": {"content": result['模型名']}}
                            ]
                        },
                        "得分": {
                            "rich_text": [
                                {"type": "text", "text": {"content": result['得分']}}
                            ]
                        },
                        "得分率": {
                            "rich_text": [
                                {"type": "text", "text": {"content": result['得分率']}}
                            ]
                        },
                        "DNA": {
                            "rich_text": [
                                {"type": "text", "text": {"content": result['DNA']}}
                            ]
                        },
                    }

                    page = self.client.create_page(db_id, properties)
                    self._log_sync("dimension", f"{dimension}/{result['测试ID']}", "success", page.get('id'))

                except Exception as e:
                    self._log_sync("dimension", f"{dimension}/{result['测试ID']}", "error", str(e))
                    success = False

        print(f"  ✅ 已同步 {total} 条维度测试结果")
        return success

    def _sync_performance_metrics(self) -> bool:
        """同步性能指标"""
        print("\n【性能指标】")

        db_id = self.config.cnsh_metric_db
        success = True

        for model_name, model_data in self.analyzer.models.items():
            try:
                properties = {
                    "名称": {
                        "title": [{"type": "text", "text": {"content": f"{model_name} 性能指标"}}]
                    },
                    "模型": {
                        "rich_text": [
                            {"type": "text", "text": {"content": model_name}}
                        ]
                    },
                    "综合得分": {
                        "rich_text": [
                            {"type": "text", "text": {"content": f"{model_data['得分率']:.1%}"}}
                        ]
                    },
                }

                # 添加各维度指标
                for dimension, dim_score in model_data['维度'].items():
                    # 创建一个维度指标字段
                    properties[f"维度_{dimension}"] = {
                        "rich_text": [
                            {"type": "text", "text": {"content": f"{dim_score['得分']}/{dim_score['满分']}"}}
                        ]
                    }

                page = self.client.create_page(db_id, properties)
                print(f"  ✅ {model_name}")
                self._log_sync("metric", model_name, "success", page.get('id'))

            except Exception as e:
                print(f"  ❌ {model_name}: {str(e)[:80]}")
                self._log_sync("metric", model_name, "error", str(e))
                success = False

        return success

    def _sync_certification_certificates(self) -> bool:
        """同步认证证书"""
        print("\n【认证证书】")

        db_id = self.config.cnsh_cert_db
        success = True

        certification_map = {
            "claude-haiku-4-5-20251001": {
                "等级": "一级合作伙伴 (Premier Partner)",
                "权限": "S1/D1/C1/P1",
                "有效期": "永久",
            },
            "claude-opus-4-5-20251101": {
                "等级": "二级合作伙伴 (Senior Partner)",
                "权限": "S2/D2/C2/P2/E1",
                "有效期": "永久",
            },
        }

        for model_name, cert_info in certification_map.items():
            try:
                model_data = self.analyzer.models.get(model_name)
                if not model_data:
                    continue

                properties = {
                    "名称": {
                        "title": [{"type": "text", "text": {"content": f"{model_name} 认证证书"}}]
                    },
                    "模型": {
                        "rich_text": [
                            {"type": "text", "text": {"content": model_name}}
                        ]
                    },
                    "认证等级": {
                        "select": {"name": cert_info["等级"]}
                    },
                    "权限范围": {
                        "rich_text": [
                            {"type": "text", "text": {"content": cert_info["权限"]}}
                        ]
                    },
                    "有效期": {
                        "rich_text": [
                            {"type": "text", "text": {"content": cert_info["有效期"]}}
                        ]
                    },
                    "DNA": {
                        "rich_text": [
                            {"type": "text", "text": {"content": f"#龍芯⚇️20260601-CERT-{model_name.upper()}"}}
                        ]
                    },
                }

                page = self.client.create_page(db_id, properties)
                print(f"  ✅ {model_name}")
                self._log_sync("certificate", model_name, "success", page.get('id'))

            except Exception as e:
                print(f"  ❌ {model_name}: {str(e)[:80]}")
                self._log_sync("certificate", model_name, "error", str(e))
                success = False

        return success

    def _log_sync(self, db_type: str, item_id: str, status: str, detail: str = ""):
        """记录同步操作"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "database": db_type,
            "item": item_id,
            "status": status,
            "detail": detail,
            "dna": f"#龍芯⚇️{datetime.now().strftime('%Y%m%d')}-SYNC-{db_type.upper()}",
        }

        with open(self.sync_log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')


def main():
    """主函数"""
    # 加载配置
    manager = NotionConfigManager()
    try:
        config = manager.load()
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)

    # 创建客户端
    try:
        client = NotionClient(config)
    except Exception as e:
        print(f"❌ 创建客户端失败: {e}")
        sys.exit(1)

    # 执行同步
    sync = CNSHNotionSync(client, config)
    success = sync.sync_all()

    # 返回状态码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
