#!/usr/bin/env python3
"""
📝 Notion集成管理器 | Notion Integration Manager
DNA追溯码: #龙芯⚡️2026-01-21-Notion管理-v2.0

功能：
- 任务管理
- 财务记录
- 实时看板更新
- 自动化同步
"""

import os
import json
import aiohttp
import asyncio
from datetime import datetime, date
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

# 导入安全模块
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from security_core.dna_tracer import DNATracer, OperationType


class TaskPriority(Enum):
    """任务优先级"""
    HIGH = "高"
    MEDIUM = "中"
    LOW = "低"


class TaskStatus(Enum):
    """任务状态"""
    TODO = "待办"
    IN_PROGRESS = "进行中"
    DONE = "完成"
    BLOCKED = "阻塞"


@dataclass
class NotionTask:
    """Notion任务"""
    id: str
    title: str
    priority: TaskPriority
    status: TaskStatus
    assignee: str
    due_date: Optional[date] = None
    tags: List[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority.value,
            "status": self.status.value,
            "assignee": self.assignee,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "tags": self.tags or []
        }


@dataclass
class FinanceRecord:
    """财务记录"""
    id: str
    date: date
    amount: float
    category: str
    description: str
    account: str  # 支付宝/微信/银行卡
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "account": self.account
        }


class NotionManager:
    """Notion管理器"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("NOTION_API_KEY", "")
        self.base_url = "https://api.notion.com/v1"
        self.version = "2022-06-28"
        self.dna_tracer = DNATracer()
        
        # 数据库ID（需要配置）
        self.task_database_id = os.getenv("NOTION_TASK_DB", "")
        self.finance_database_id = os.getenv("NOTION_FINANCE_DB", "")
        
    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": self.version
        }
    
    async def create_task(self, 
                          title: str,
                          priority: TaskPriority = TaskPriority.MEDIUM,
                          assignee: str = "",
                          due_date: date = None,
                          tags: List[str] = None) -> Dict[str, Any]:
        """
        创建任务
        
        Usage:
            await notion.create_task(
                title="完成龙魂终端",
                priority=TaskPriority.HIGH,
                assignee="Claude"
            )
        """
        dna_code = self.dna_tracer.start_trace(
            operator="NotionManager",
            operation_type=OperationType.WRITE,
            detail=f"创建任务: {title}",
            input_data={"title": title, "priority": priority.value}
        )
        
        if not self.api_key or not self.task_database_id:
            self.dna_tracer.end_trace(dna_code, audit_result="🔴 未配置")
            return {"error": "Notion API未配置", "dna_code": dna_code}
        
        # 构建Notion页面属性
        properties = {
            "任务名称": {
                "title": [{"text": {"content": title}}]
            },
            "优先级": {
                "select": {"name": priority.value}
            },
            "状态": {
                "select": {"name": TaskStatus.TODO.value}
            }
        }
        
        if assignee:
            properties["负责人"] = {
                "rich_text": [{"text": {"content": assignee}}]
            }
        
        if due_date:
            properties["截止日期"] = {
                "date": {"start": due_date.isoformat()}
            }
        
        if tags:
            properties["标签"] = {
                "multi_select": [{"name": tag} for tag in tags]
            }
        
        payload = {
            "parent": {"database_id": self.task_database_id},
            "properties": properties
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/pages",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.dna_tracer.end_trace(
                            dna_code,
                            output_data={"page_id": data["id"]},
                            audit_result="🟢 成功"
                        )
                        return {
                            "success": True,
                            "page_id": data["id"],
                            "dna_code": dna_code
                        }
                    else:
                        error = await response.text()
                        self.dna_tracer.end_trace(dna_code, audit_result="🔴 失败")
                        return {"error": error, "dna_code": dna_code}
                        
        except Exception as e:
            self.dna_tracer.end_trace(dna_code, audit_result="🔴 异常")
            return {"error": str(e), "dna_code": dna_code}
    
    async def get_tasks(self, 
                        status: TaskStatus = None,
                        priority: TaskPriority = None) -> List[NotionTask]:
        """获取任务列表"""
        dna_code = self.dna_tracer.start_trace(
            operator="NotionManager",
            operation_type=OperationType.READ,
            detail="获取任务列表"
        )
        
        if not self.api_key or not self.task_database_id:
            self.dna_tracer.end_trace(dna_code, audit_result="🔴 未配置")
            return []
        
        # 构建过滤器
        filters = []
        if status:
            filters.append({
                "property": "状态",
                "select": {"equals": status.value}
            })
        if priority:
            filters.append({
                "property": "优先级",
                "select": {"equals": priority.value}
            })
        
        payload = {}
        if filters:
            payload["filter"] = {"and": filters} if len(filters) > 1 else filters[0]
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/databases/{self.task_database_id}/query",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        tasks = [self._parse_task(page) for page in data.get("results", [])]
                        self.dna_tracer.end_trace(
                            dna_code,
                            output_data={"count": len(tasks)},
                            audit_result="🟢 成功"
                        )
                        return tasks
                    else:
                        self.dna_tracer.end_trace(dna_code, audit_result="🔴 失败")
                        return []
                        
        except Exception as e:
            self.dna_tracer.end_trace(dna_code, audit_result="🔴 异常")
            return []
    
    async def add_finance_record(self,
                                 amount: float,
                                 category: str,
                                 description: str,
                                 account: str = "支付宝",
                                 record_date: date = None) -> Dict[str, Any]:
        """
        添加财务记录
        
        Usage:
            await notion.add_finance_record(
                amount=-35.5,
                category="餐饮",
                description="午餐",
                account="支付宝"
            )
        """
        record_date = record_date or date.today()
        
        dna_code = self.dna_tracer.start_trace(
            operator="NotionManager",
            operation_type=OperationType.WRITE,
            detail=f"添加财务记录: {amount}元 - {description}",
            input_data={"amount": amount, "category": category}
        )
        
        if not self.api_key or not self.finance_database_id:
            self.dna_tracer.end_trace(dna_code, audit_result="🔴 未配置")
            return {"error": "财务数据库未配置", "dna_code": dna_code}
        
        properties = {
            "日期": {
                "date": {"start": record_date.isoformat()}
            },
            "金额": {
                "number": amount
            },
            "分类": {
                "select": {"name": category}
            },
            "描述": {
                "title": [{"text": {"content": description}}]
            },
            "账户": {
                "select": {"name": account}
            }
        }
        
        payload = {
            "parent": {"database_id": self.finance_database_id},
            "properties": properties
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/pages",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.dna_tracer.end_trace(dna_code, audit_result="🟢 成功")
                        return {
                            "success": True,
                            "page_id": data["id"],
                            "dna_code": dna_code
                        }
                    else:
                        self.dna_tracer.end_trace(dna_code, audit_result="🔴 失败")
                        return {"error": await response.text(), "dna_code": dna_code}
                        
        except Exception as e:
            self.dna_tracer.end_trace(dna_code, audit_result="🔴 异常")
            return {"error": str(e), "dna_code": dna_code}
    
    async def get_finance_summary(self, 
                                  start_date: date = None,
                                  end_date: date = None) -> Dict[str, Any]:
        """获取财务汇总"""
        start_date = start_date or date.today().replace(day=1)
        end_date = end_date or date.today()
        
        dna_code = self.dna_tracer.start_trace(
            operator="NotionManager",
            operation_type=OperationType.READ,
            detail=f"获取财务汇总: {start_date} - {end_date}"
        )
        
        # 模拟数据（实际应从Notion获取）
        summary = {
            "period": f"{start_date} - {end_date}",
            "total_income": 10000,
            "total_expense": 3500,
            "balance": 6500,
            "by_category": {
                "餐饮": 800,
                "交通": 200,
                "购物": 1500,
                "娱乐": 500,
                "其他": 500
            },
            "dna_code": dna_code
        }
        
        self.dna_tracer.end_trace(dna_code, output_data=summary, audit_result="🟢 成功")
        return summary
    
    async def update_dashboard(self, dashboard_page_id: str = None) -> Dict[str, Any]:
        """
        更新实时看板
        
        看板内容：
        - 五大后台状态
        - 今日任务进度
        - 本月财务概览
        """
        dna_code = self.dna_tracer.start_trace(
            operator="NotionManager",
            operation_type=OperationType.WRITE,
            detail="更新实时看板"
        )
        
        # 获取各项数据
        tasks = await self.get_tasks()
        finance = await self.get_finance_summary()
        
        # 计算任务进度
        total_tasks = len(tasks)
        done_tasks = len([t for t in tasks if t.status == TaskStatus.DONE])
        progress = (done_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        dashboard_content = {
            "update_time": datetime.now().isoformat(),
            "backends": {
                "Notion AI": "🟢活跃",
                "Claude": "🟢活跃",
                "DeepSeek": "🟢活跃",
                "ChatGPT": "🟡观察"
            },
            "tasks": {
                "total": total_tasks,
                "done": done_tasks,
                "progress": f"{progress:.1f}%"
            },
            "finance": {
                "balance": f"¥{finance['balance']:,.0f}",
                "expense_this_month": f"¥{finance['total_expense']:,.0f}"
            }
        }
        
        self.dna_tracer.end_trace(
            dna_code,
            output_data=dashboard_content,
            audit_result="🟢 成功"
        )
        
        return {
            "success": True,
            "dashboard": dashboard_content,
            "dna_code": dna_code
        }
    
    def _parse_task(self, page: Dict) -> NotionTask:
        """解析Notion页面为任务对象"""
        props = page.get("properties", {})
        
        # 获取标题
        title = ""
        if "任务名称" in props:
            title_prop = props["任务名称"].get("title", [])
            if title_prop:
                title = title_prop[0].get("text", {}).get("content", "")
        
        # 获取优先级
        priority = TaskPriority.MEDIUM
        if "优先级" in props:
            priority_name = props["优先级"].get("select", {}).get("name", "")
            for p in TaskPriority:
                if p.value == priority_name:
                    priority = p
                    break
        
        # 获取状态
        status = TaskStatus.TODO
        if "状态" in props:
            status_name = props["状态"].get("select", {}).get("name", "")
            for s in TaskStatus:
                if s.value == status_name:
                    status = s
                    break
        
        # 获取负责人
        assignee = ""
        if "负责人" in props:
            assignee_prop = props["负责人"].get("rich_text", [])
            if assignee_prop:
                assignee = assignee_prop[0].get("text", {}).get("content", "")
        
        return NotionTask(
            id=page["id"],
            title=title,
            priority=priority,
            status=status,
            assignee=assignee
        )


# ==================== 便捷函数 ====================
_notion = None

def get_notion() -> NotionManager:
    """获取Notion管理器单例"""
    global _notion
    if _notion is None:
        _notion = NotionManager()
    return _notion


async def create_task(title: str, priority: str = "中", assignee: str = "") -> str:
    """
    便捷函数：创建任务
    
    Usage:
        result = await create_task("完成报告", priority="高", assignee="Claude")
    """
    n = get_notion()
    
    # 转换优先级
    priority_map = {"高": TaskPriority.HIGH, "中": TaskPriority.MEDIUM, "低": TaskPriority.LOW}
    p = priority_map.get(priority, TaskPriority.MEDIUM)
    
    result = await n.create_task(title, priority=p, assignee=assignee)
    
    if result.get("success"):
        return f"✅ 任务已创建: {title}"
    else:
        return f"❌ 创建失败: {result.get('error', '未知错误')}"


# ==================== 使用示例 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("📝 Notion集成管理器测试")
    print("=" * 60)
    
    notion = NotionManager()
    
    async def test():
        # 测试更新看板
        print("\n📊 更新看板:")
        dashboard = await notion.update_dashboard()
        
        if dashboard["success"]:
            d = dashboard["dashboard"]
            print(f"  更新时间: {d['update_time']}")
            print(f"  后台状态:")
            for name, status in d["backends"].items():
                print(f"    {status} {name}")
            print(f"  任务进度: {d['tasks']['progress']}")
            print(f"  本月支出: {d['finance']['expense_this_month']}")
            print(f"  DNA追溯码: {dashboard['dna_code']}")
        
        # 测试财务汇总
        print("\n💰 财务汇总:")
        finance = await notion.get_finance_summary()
        print(f"  周期: {finance['period']}")
        print(f"  收入: ¥{finance['total_income']:,}")
        print(f"  支出: ¥{finance['total_expense']:,}")
        print(f"  结余: ¥{finance['balance']:,}")
        print(f"  分类:")
        for cat, amount in finance["by_category"].items():
            print(f"    {cat}: ¥{amount:,}")
    
    asyncio.run(test())
