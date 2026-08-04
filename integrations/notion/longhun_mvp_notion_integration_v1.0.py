#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 Notion集成引擎 v1.0
LongHun Notion Integration Engine

DNA:#龍芯⚡️2026-06-04-NOTION-INTEGRATION-v1.0

功能：
- Notion数据库同步（4个核心表）
- 人格权重自适应学习
- DNA链生成与记录
- 三色审计日志写回
"""

import json
import hashlib
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class NotionAuth:
    """Notion API认证与连接"""

    def __init__(self, notion_token: str, database_ids: Dict[str, str]):
        self.token = notion_token
        self.headers = {
            "Authorization": f"Bearer {notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.database_ids = database_ids
        self.base_url = "https://api.notion.com/v1"

    def query_database(self, db_key: str, filters: Dict[str, Any] = None) -> List[Dict]:
        """查询Notion数据库"""
        url = f"{self.base_url}/databases/{self.database_ids[db_key]}/query"
        payload = {"filter": filters} if filters else {}

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            if response.status_code == 200:
                return response.json()["results"]
            else:
                print(f"❌ Notion查询失败: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ API错误: {e}")
            return []

    def create_page(self, db_key: str, data: Dict[str, Any]) -> Optional[Dict]:
        """创建Notion页面"""
        url = f"{self.base_url}/pages"
        payload = {
            "parent": {"database_id": self.database_ids[db_key]},
            "properties": data
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ 页面创建失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ API错误: {e}")
            return None

    def update_page(self, page_id: str, data: Dict[str, Any]) -> bool:
        """更新Notion页面"""
        url = f"{self.base_url}/pages/{page_id}"
        payload = {"properties": data}

        try:
            response = requests.patch(url, headers=self.headers, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ 更新失败: {e}")
            return False


class PersonaWeightManager:
    """人格权重自适应学习"""

    WEIGHT_RULES = {
        "SUCCESS": 0.02,
        "PARTIAL": 0.01,
        "FAILED": -0.01,
        "KEY_FINDING": 0.05,
        "CONFLICT_RESOLUTION": 0.03
    }

    @staticmethod
    def calculate_new_weight(current_weight: float, result: str, factors: Dict[str, Any] = None) -> float:
        """计算新权重"""
        delta = PersonaWeightManager.WEIGHT_RULES.get(result, 0)

        if factors:
            if factors.get("confidence", 0) > 0.95:
                delta += 0.02
            if factors.get("novelty", False):
                delta += 0.05

        new_weight = max(0.0, min(1.0, current_weight + delta))
        return round(new_weight, 3)


class NotionSyncEngine:
    """Notion同步引擎"""

    def __init__(self, notion_auth: NotionAuth):
        self.notion = notion_auth
        self.personas_cache = {}
        self.rules_cache = {}
        self._load_caches()

    def _load_caches(self):
        """加载Notion缓存到内存"""
        # 加载人格花名册
        personas = self.notion.query_database("personas")
        for persona in personas:
            props = persona["properties"]
            code = props.get("人格代码", {}).get("rich_text", [{}])[0].get("text", {}).get("content", "")
            self.personas_cache[code] = {
                "page_id": persona["id"],
                "name": props.get("人格名称", {}).get("title", [{}])[0].get("text", {}).get("content", ""),
                "weight": props.get("当前权重", {}).get("number", 0.5),
                "success_rate": props.get("成功率", {}).get("number", 0),
                "execution_count": props.get("执行次数", {}).get("number", 0)
            }

        print(f"✅ 加载了 {len(self.personas_cache)} 个人格到缓存")

    def sync_execution_result(self, exec_data: Dict[str, Any]) -> bool:
        """同步执行结果到Notion"""
        # 提取数据
        exec_id = exec_data.get("exec_id")
        task_input = exec_data.get("task_input")
        personas_involved = exec_data.get("personas", [])
        result_status = exec_data.get("result_status", "UNKNOWN")
        audit_color = exec_data.get("audit_color", "🟡")
        dna_code = exec_data.get("dna_code")

        # 构建Notion页面数据
        notion_data = {
            "执行ID": {"title": [{"text": {"content": exec_id}}]},
            "输入任务": {"rich_text": [{"text": {"content": task_input[:500]}}]},
            "成功状态": {"select": {"name": result_status}},
            "审计等级": {"select": {"name": audit_color}},
            "DNA追溯码": {"rich_text": [{"text": {"content": dna_code}}]},
            "执行耗时": {"number": exec_data.get("duration_ms", 0)},
            "执行时间": {"date": {"start": datetime.now().isoformat()}}
        }

        # 创建日志记录
        result = self.notion.create_page("execution_logs", notion_data)

        if result:
            print(f"✅ 执行记录 {exec_id} 已写入Notion")

            # 更新人格权重
            for persona_code in personas_involved:
                if persona_code in self.personas_cache:
                    old_weight = self.personas_cache[persona_code]["weight"]
                    new_weight = PersonaWeightManager.calculate_new_weight(
                        old_weight,
                        result_status,
                        {"confidence": exec_data.get("confidence", 0.8)}
                    )

                    # 更新Notion中的权重
                    update_data = {
                        "当前权重": {"number": new_weight}
                    }
                    page_id = self.personas_cache[persona_code]["page_id"]
                    self.notion.update_page(page_id, update_data)

                    # 更新本地缓存
                    self.personas_cache[persona_code]["weight"] = new_weight

                    print(f"📊 {persona_code} 权重: {old_weight} → {new_weight}")

            return True

        return False

    def get_routing_rules(self, task_type: str) -> Dict[str, Any]:
        """从Notion获取路由规则"""
        rules = self.notion.query_database("routing_rules")

        for rule in rules:
            props = rule["properties"]
            rule_type = props.get("任务类型", {}).get("select", {}).get("name", "")

            if rule_type == task_type:
                return {
                    "rule_id": props.get("规则ID", {}).get("rich_text", [{}])[0].get("text", {}).get("content", ""),
                    "primary_persona": props.get("主人格", {}).get("relation", [{}])[0].get("id", ""),
                    "execution_mode": props.get("执行模式", {}).get("select", {}).get("name", "sequential")
                }

        return {}

    def generate_execution_dna(self, exec_id: str, task_name: str) -> str:
        """生成执行DNA"""
        dna_input = f"{exec_id}-{task_name}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        hash_code = hashlib.sha256(dna_input.encode()).hexdigest()[:8]
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-{exec_id}-{hash_code}"
        return dna


class NotionMVPBridge:
    """Notion-MVP双向桥接"""

    def __init__(self, executor, notion_auth: NotionAuth):
        self.executor = executor
        self.sync_engine = NotionSyncEngine(notion_auth)

    def sync_tasks_from_notion(self) -> List[Dict]:
        """从Notion加载任务"""
        rules = self.sync_engine.notion.query_database("routing_rules")
        tasks = []

        for rule in rules:
            props = rule["properties"]
            tasks.append({
                "rule_id": props.get("规则ID", {}).get("rich_text", [{}])[0].get("text", {}).get("content", ""),
                "name": props.get("规则名称", {}).get("rich_text", [{}])[0].get("text", {}).get("content", ""),
                "task_type": props.get("任务类型", {}).get("select", {}).get("name", "")
            })

        print(f"✅ 从Notion加载了 {len(tasks)} 条任务规则")
        return tasks

    def sync_execution(self, exec_id: str, exec_result: Dict[str, Any]) -> bool:
        """同步执行结果"""
        exec_data = {
            "exec_id": exec_id,
            "task_input": exec_result.get("task_name", ""),
            "personas": exec_result.get("assigned_personas", []),
            "result_status": "SUCCESS" if exec_result.get("success") else "FAILED",
            "audit_color": exec_result.get("audit_color", "🟡"),
            "dna_code": self.sync_engine.generate_execution_dna(exec_id, exec_result.get("task_name", "")),
            "duration_ms": exec_result.get("duration_ms", 0),
            "confidence": exec_result.get("confidence", 0.8)
        }

        return self.sync_engine.sync_execution_result(exec_data)

    def generate_notion_report(self) -> Dict[str, Any]:
        """生成Notion统计报告"""
        personas = self.sync_engine.personas_cache

        report = {
            "timestamp": datetime.now().isoformat(),
            "total_personas": len(personas),
            "personas_stats": [],
            "average_weight": 0,
            "highest_performer": None,
            "lowest_performer": None
        }

        weights = []
        for code, data in personas.items():
            weight = data.get("weight", 0)
            weights.append(weight)

            report["personas_stats"].append({
                "code": code,
                "name": data.get("name", ""),
                "weight": weight,
                "success_rate": data.get("success_rate", 0),
                "execution_count": data.get("execution_count", 0)
            })

        if weights:
            report["average_weight"] = round(sum(weights) / len(weights), 3)
            report["highest_performer"] = max(report["personas_stats"], key=lambda x: x["weight"])
            report["lowest_performer"] = min(report["personas_stats"], key=lambda x: x["weight"])

        return report


if __name__ == '__main__':
    print("🔗 龍魂Notion集成引擎 v1.0")
    print("=" * 60)

    # 示例：Notion认证配置
    # NOTION_TOKEN = "your_notion_token"
    # DATABASE_IDS = {
    #     "personas": "xxx",
    #     "routing_rules": "xxx",
    #     "conflict_arbiter": "xxx",
    #     "execution_logs": "xxx"
    # }

    print("\n💡 使用方式:")
    print("1. 设置NOTION_TOKEN和DATABASE_IDS")
    print("2. notion = NotionAuth(NOTION_TOKEN, DATABASE_IDS)")
    print("3. bridge = NotionMVPBridge(executor, notion)")
    print("4. bridge.sync_execution(exec_id, exec_result)")
