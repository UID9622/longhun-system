#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系統知識圖譜同步 · Stage 3

DNA: #龍芯⚇️2026-06-01-KNOWLEDGE-SYNC-v1.0
UID: 9622
Purpose: 將龍魂系統的知識圖譜同步到 Notion 四個數據庫

Databases (工作區 2):
  1. CNSH 規則庫 - CNSH 格式標準和修正規則
  2. IPA 節點註冊表 - 50+ IPA 指令頁錨點
  3. 系統決策樹 - 循環觸發和五行流轉規則
  4. 組件關係圖 - 人格矩陣、中心、閘門、引擎

Features:
  - 從系統配置加載知識圖譜數據
  - 生成知識節點和關係
  - Notion 同步和索引建立
  - DNA 簽名和追溯鏈
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


class KnowledgeGraphAnalyzer:
    """龍魂知識圖譜分析器"""

    # CNSH 規則庫數據
    CNSH_RULES = {
        "中文錯別字": {
            "規則": "繁簡混用檢查及統一",
            "特例": "龍字保留繁體",
            "示例": "系統→系统（繁簡混用）",
            "修正方式": "統一為簡體（龍字除外）",
        },
        "代碼縮進": {
            "規則": "4 空格 PEP 8 標準",
            "特例": "無",
            "示例": "def test():\\n    pass",
            "修正方式": "按層級調整縮進",
        },
        "DNA標記大小寫": {
            "規則": "格式 #龍芯⚇️YYYY-MM-DD-TYPE-v1.0",
            "特例": "龍字必須繁體，版本號小寫",
            "示例": "#龍芯⚇️2026-06-01-CNSH-BENCHMARK-v1.0",
            "修正方式": "按規範格式重寫 DNA",
        },
        "中英混排空格": {
            "規則": "中文與英文間加空格",
            "特例": "中文與數字也要空格",
            "示例": "使用 Python 3.11 實現",
            "修正方式": "在中英邊界插入空格",
        },
    }

    # IPA 節點核心清單
    IPA_NODES = [
        {"id": "IPA-ROUTE-REGISTRY", "name": "分布式總線路由註冊表", "level": "L0", "type": "門戶"},
        {"id": "IPA-CORE-CMD-v3.0", "name": "指令統一核心", "level": "L1", "type": "核心"},
        {"id": "IPA-PERSONA-MATRIX", "name": "人格矩陣（P00-P72）", "level": "L1", "type": "人格"},
        {"id": "IPA-FLOW-DECISION-CORE-v4.1", "name": "CNSH 流場決策總核", "level": "L2", "type": "決策樹"},
        {"id": "IPA-FAMILY-ROSTER-CNS-v1.0", "name": "花名冊中樞神經", "level": "L2", "type": "路由"},
        {"id": "IPA-DNA-BOOK", "name": "DNA v1.0 規範", "level": "L1", "type": "規範"},
        {"id": "IPA-DICT-101-111", "name": "循環觸發五行流轉", "level": "L2", "type": "決策樹"},
    ]

    # 系統決策樹核心規則
    DECISION_RULES = {
        "GATE-01": {
            "name": "第一道門·數字根熔斷",
            "condition": "dr ∈ {1,2,4,5,7,8} → 🟢 / 6 → 🟡 / {3,9} → 🔴",
            "trigger": "所有輸入",
            "type": "安全閘門",
        },
        "CYCLE-101": {
            "name": "微觀循環（毫秒）",
            "condition": "任何用戶輸入後 5ms",
            "trigger": "流式推理微調",
            "type": "循環觸發",
        },
        "CYCLE-102": {
            "name": "宏觀循環（分鐘）",
            "condition": "完成一次完整對話",
            "trigger": "性能/資源/質量複盤",
            "type": "循環觸發",
        },
        "WUXING-FLOW": {
            "name": "五行流轉循環",
            "condition": "火 → 木 → 金 → 水 → 火",
            "trigger": "決策流場",
            "type": "決策樹",
        },
    }

    # 組件關係圖
    COMPONENTS = {
        "人格": [
            "L0 (老大·終極決策)",
            "P00-P15 (核心人格)",
            "P72 (龍盾·情緒五態)",
        ],
        "中心": [
            "CENTER-RULES (規則中心)",
            "CENTER-AUDIT (審計中心)",
            "CENTER-RUNTIME (運行中心)",
            "CENTER-UNDERSTAND (理解中心)",
            "CENTER-PRIVATE (私密中心)",
        ],
        "閘門": [
            "GATE-01 (數字根熔斷)",
            "GATE-02 (身份認證)",
            "GATE-03 (倫理防火牆)",
            "GATE-04 (CNSH 關·保安亭)",
        ],
        "引擎": [
            "LOCAL-CNSH-GATE (CNSH 關)",
            "LOCAL-DNA-GEN-V2 (DNA 追蹤碼)",
            "LOCAL-SANDBOX-SORTER (沙盒分拣)",
            "LOCAL-DETECTOR (異常檢測)",
        ],
    }

    def __init__(self):
        self.knowledge_file = Path.home() / ".龍魂" / "knowledge_graph.jsonl"
        self.rules_count = 0
        self.nodes_count = 0
        self.relations_count = 0

    def analyze_cnsh_rules(self) -> Dict[str, List[Dict]]:
        """分析 CNSH 規則庫"""
        rules_data = {}

        for rule_name, rule_info in self.CNSH_RULES.items():
            rules_data[rule_name] = {
                "規則": rule_info["規則"],
                "特例": rule_info["特例"],
                "示例": rule_info["示例"],
                "修正方式": rule_info["修正方式"],
                "DNA": f"#龍芯⚇️20260601-CNSH-RULE-{rule_name.upper()}",
            }
            self.rules_count += 1

        return rules_data

    def analyze_ipa_nodes(self) -> Dict[str, List[Dict]]:
        """分析 IPA 節點註冊表"""
        nodes_by_level = defaultdict(list)

        for node in self.IPA_NODES:
            nodes_by_level[node["level"]].append(node)
            self.nodes_count += 1

        return dict(nodes_by_level)

    def analyze_decision_tree(self) -> Dict[str, List[Dict]]:
        """分析決策樹"""
        decisions = {}

        for rule_id, rule_info in self.DECISION_RULES.items():
            decisions[rule_id] = {
                "名稱": rule_info["name"],
                "條件": rule_info["condition"],
                "觸發": rule_info["trigger"],
                "類型": rule_info["type"],
                "DNA": f"#龍芯⚇️20260601-DECISION-{rule_id}",
            }

        return decisions

    def analyze_components(self) -> Dict[str, List[Dict]]:
        """分析組件關係圖"""
        component_data = {}

        for component_type, items in self.COMPONENTS.items():
            component_data[component_type] = [
                {
                    "名稱": item,
                    "類型": component_type,
                    "DNA": f"#龍芯⚇️20260601-COMPONENT-{component_type.upper()}",
                }
                for item in items
            ]
            self.relations_count += len(items)

        return component_data


class KnowledgeNotionSync:
    """知識圖譜到 Notion 同步器"""

    def __init__(self, client: NotionClient, config: NotionConfig):
        self.client = client
        self.config = config
        self.analyzer = KnowledgeGraphAnalyzer()
        self.sync_log_file = Path.home() / ".龍魂" / "notion_knowledge_sync.jsonl"

    def sync_all(self) -> bool:
        """執行完整同步"""
        print("\n" + "=" * 70)
        print("🐉 龍魂知識圖譜同步 (Stage 3)")
        print("=" * 70)

        # 分析數據
        print("\n📚 分析知識圖譜...")
        self.analyzer.analyze_cnsh_rules()
        self.analyzer.analyze_ipa_nodes()
        self.analyzer.analyze_decision_tree()
        self.analyzer.analyze_components()

        print(f"✅ 分析完成：{self.analyzer.rules_count} 條規則 + {self.analyzer.nodes_count} 個節點 + {self.analyzer.relations_count} 個關係")

        # 檢查數據庫 ID
        if not self._check_databases():
            print("\n⚠️  未配置所有數據庫 ID，使用本地模式預覽數據")
            self._preview_data()
            return False

        # 同步到 Notion
        print("\n🔄 同步數據到 Notion...")
        success = True
        success &= self._sync_cnsh_rules()
        success &= self._sync_ipa_nodes()
        success &= self._sync_decision_tree()
        success &= self._sync_components()

        print("\n" + "=" * 70)
        if success:
            print("✅ 同步完成")
        else:
            print("⚠️  部分同步失敗，詳見審計日誌")
        print("=" * 70)

        return success

    def _check_databases(self) -> bool:
        """檢查所有必需的數據庫 ID"""
        required_dbs = [
            ("rules_db", "CNSH 規則庫"),
            ("nodes_db", "IPA 節點註冊表"),
            ("decision_db", "系統決策樹"),
            ("relation_db", "組件關係圖"),
        ]

        missing = []
        for attr, name in required_dbs:
            if not getattr(self.config, attr, None):
                missing.append(name)

        if missing:
            print(f"\n❌ 缺少以下數據庫 ID:")
            for name in missing:
                print(f"   - {name}")
            print(f"\n請先運行: export NOTION_RULES_DB='...' 等")
            return False

        return True

    def _preview_data(self):
        """預覽數據（本地模式）"""
        print("\n📋 本地數據預覽")
        print("=" * 70)

        # CNSH 規則預覽
        print("\n【CNSH 規則庫】")
        rules = self.analyzer.analyze_cnsh_rules()
        for rule_name, rule_info in list(rules.items())[:3]:
            print(f"\n  {rule_name}")
            print(f"    規則: {rule_info['規則']}")
            print(f"    特例: {rule_info['特例']}")

        # IPA 節點預覽
        print("\n【IPA 節點註冊表】")
        nodes = self.analyzer.analyze_ipa_nodes()
        for level, node_list in nodes.items():
            print(f"\n  {level}: {len(node_list)} 個節點")
            for node in node_list[:2]:
                print(f"    - {node['id']}: {node['name']}")

        # 決策樹預覽
        print("\n【系統決策樹】")
        decisions = self.analyzer.analyze_decision_tree()
        for rule_id, rule_info in list(decisions.items())[:3]:
            print(f"\n  {rule_id}: {rule_info['名稱']}")
            print(f"    類型: {rule_info['類型']}")

        # 組件關係預覽
        print("\n【組件關係圖】")
        components = self.analyzer.analyze_components()
        for comp_type, comp_list in components.items():
            print(f"\n  {comp_type}: {len(comp_list)} 個組件")
            for comp in comp_list[:2]:
                print(f"    - {comp['名稱']}")

    def _sync_cnsh_rules(self) -> bool:
        """同步 CNSH 規則庫"""
        print("\n【CNSH 規則庫】")

        db_id = self.config.rules_db
        rules = self.analyzer.analyze_cnsh_rules()
        success = True

        for rule_name, rule_info in rules.items():
            try:
                properties = {
                    "名稱": {
                        "title": [{"type": "text", "text": {"content": rule_name}}]
                    },
                    "規則": {
                        "rich_text": [
                            {"type": "text", "text": {"content": rule_info['規則']}}
                        ]
                    },
                    "特例": {
                        "rich_text": [
                            {"type": "text", "text": {"content": rule_info['特例']}}
                        ]
                    },
                    "示例": {
                        "rich_text": [
                            {"type": "text", "text": {"content": rule_info['示例']}}
                        ]
                    },
                    "修正方式": {
                        "rich_text": [
                            {"type": "text", "text": {"content": rule_info['修正方式']}}
                        ]
                    },
                    "DNA": {
                        "rich_text": [
                            {"type": "text", "text": {"content": rule_info['DNA']}}
                        ]
                    },
                }

                page = self.client.create_page(db_id, properties)
                print(f"  ✅ {rule_name}")
                self._log_sync("cnsh_rules", rule_name, "success", page.get('id'))

            except Exception as e:
                print(f"  ❌ {rule_name}: {str(e)[:80]}")
                self._log_sync("cnsh_rules", rule_name, "error", str(e))
                success = False

        return success

    def _sync_ipa_nodes(self) -> bool:
        """同步 IPA 節點註冊表"""
        print("\n【IPA 節點註冊表】")

        db_id = self.config.nodes_db
        nodes = self.analyzer.analyze_ipa_nodes()
        success = True

        for level, node_list in nodes.items():
            for node in node_list:
                try:
                    properties = {
                        "名稱": {
                            "title": [{"type": "text", "text": {"content": node['name']}}]
                        },
                        "節點ID": {
                            "rich_text": [
                                {"type": "text", "text": {"content": node['id']}}
                            ]
                        },
                        "層級": {
                            "select": {"name": node['level']}
                        },
                        "類型": {
                            "select": {"name": node['type']}
                        },
                        "DNA": {
                            "rich_text": [
                                {"type": "text", "text": {"content": f"#龍芯⚇️20260601-NODE-{node['id']}"}}
                            ]
                        },
                    }

                    page = self.client.create_page(db_id, properties)
                    print(f"  ✅ {node['id']}")
                    self._log_sync("ipa_nodes", node['id'], "success", page.get('id'))

                except Exception as e:
                    print(f"  ❌ {node['id']}: {str(e)[:80]}")
                    self._log_sync("ipa_nodes", node['id'], "error", str(e))
                    success = False

        return success

    def _sync_decision_tree(self) -> bool:
        """同步系統決策樹"""
        print("\n【系統決策樹】")

        db_id = self.config.decision_db
        decisions = self.analyzer.analyze_decision_tree()
        success = True

        for rule_id, rule_info in decisions.items():
            try:
                properties = {
                    "規則ID": {
                        "title": [{"type": "text", "text": {"content": rule_id}}]
                    },
                    "名稱": {
                        "rich_text": [
                            {"type": "text", "text": {"content": rule_info['名稱']}}
                        ]
                    },
                    "條件": {
                        "rich_text": [
                            {"type": "text", "text": {"content": rule_info['條件']}}
                        ]
                    },
                    "觸發": {
                        "rich_text": [
                            {"type": "text", "text": {"content": rule_info['觸發']}}
                        ]
                    },
                    "類型": {
                        "select": {"name": rule_info['類型']}
                    },
                    "DNA": {
                        "rich_text": [
                            {"type": "text", "text": {"content": rule_info['DNA']}}
                        ]
                    },
                }

                page = self.client.create_page(db_id, properties)
                print(f"  ✅ {rule_id}")
                self._log_sync("decision_tree", rule_id, "success", page.get('id'))

            except Exception as e:
                print(f"  ❌ {rule_id}: {str(e)[:80]}")
                self._log_sync("decision_tree", rule_id, "error", str(e))
                success = False

        return success

    def _sync_components(self) -> bool:
        """同步組件關係圖"""
        print("\n【組件關係圖】")

        db_id = self.config.relation_db
        components = self.analyzer.analyze_components()
        success = True
        total = 0

        for comp_type, comp_list in components.items():
            for comp in comp_list:
                try:
                    properties = {
                        "名稱": {
                            "title": [{"type": "text", "text": {"content": comp['名稱']}}]
                        },
                        "組件類型": {
                            "select": {"name": comp['類型']}
                        },
                        "DNA": {
                            "rich_text": [
                                {"type": "text", "text": {"content": comp['DNA']}}
                            ]
                        },
                    }

                    page = self.client.create_page(db_id, properties)
                    print(f"  ✅ {comp['名稱']}")
                    total += 1
                    self._log_sync("components", comp['名稱'], "success", page.get('id'))

                except Exception as e:
                    print(f"  ❌ {comp['名稱']}: {str(e)[:80]}")
                    self._log_sync("components", comp['名稱'], "error", str(e))
                    success = False

        print(f"  已同步 {total} 個組件")
        return success

    def _log_sync(self, db_type: str, item_id: str, status: str, detail: str = ""):
        """記錄同步操作"""
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
    """主函數"""
    # 加載配置
    manager = NotionConfigManager()
    try:
        config = manager.load()
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)

    # 創建客戶端
    try:
        client = NotionClient(config)
    except Exception as e:
        print(f"❌ 創建客戶端失敗: {e}")
        sys.exit(1)

    # 執行同步
    sync = KnowledgeNotionSync(client, config)
    success = sync.sync_all()

    # 返回狀態碼
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
