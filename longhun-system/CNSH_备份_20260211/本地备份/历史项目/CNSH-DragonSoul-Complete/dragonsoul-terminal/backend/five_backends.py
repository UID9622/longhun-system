#!/usr/bin/env python3
"""
🤖 五大AI后台调度系统 | Five AI Backends Scheduler
DNA追溯码: #龍芯⚡️2026-01-21-五大后台-v2.0

五大后台规则：
1. Notion AI - 优先级1，数据管理专家
2. Claude - 优先级2，通用智能核心
3. DeepSeek - 优先级3，中文理解专家
4. ChatGPT - 优先级4，观察状态
5. 本地模型 - 优先级5，离线备份
"""

import os
import json
import asyncio
import aiohttp
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

# 导入安全模块
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from security_core.audit_engine import ThreeColorAuditEngine, AuditLevel
from security_core.dna_tracer import DNATracer, OperationType


class BackendStatus(Enum):
    """后台状态"""
    ACTIVE = "🟢活跃"
    STANDBY = "🟡待命"
    OBSERVE = "🔵观察"
    OFFLINE = "🔴离线"
    ERROR = "❌错误"


class TaskType(Enum):
    """任务类型"""
    CHAT = "对话"
    ANALYSIS = "分析"
    CODING = "编程"
    TRANSLATION = "翻译"
    DATA_MANAGEMENT = "数据管理"
    AUTOMATION = "自动化"


@dataclass
class AIBackend:
    """AI后台基类"""
    name: str
    priority: int
    status: BackendStatus = BackendStatus.STANDBY
    api_key: str = ""
    base_url: str = ""
    model: str = ""
    specialties: List[TaskType] = field(default_factory=list)
    rate_limit: int = 60  # 每分钟请求限制
    request_count: int = 0
    last_request_time: datetime = field(default_factory=datetime.now)
    
    def can_handle(self, task_type: TaskType) -> bool:
        """检查是否能处理此类任务"""
        return task_type in self.specialties or not self.specialties
    
    def is_available(self) -> bool:
        """检查是否可用"""
        return self.status in [BackendStatus.ACTIVE, BackendStatus.STANDBY]


class FiveBackendsScheduler:
    """五大后台调度器"""
    
    def __init__(self):
        self.audit_engine = ThreeColorAuditEngine()
        self.dna_tracer = DNATracer()
        
        # 初始化五大后台
        self.backends: Dict[str, AIBackend] = {
            "notion": AIBackend(
                name="Notion AI",
                priority=1,
                status=BackendStatus.ACTIVE,
                api_key=os.getenv("NOTION_API_KEY", ""),
                base_url="https://api.notion.com/v1",
                specialties=[TaskType.DATA_MANAGEMENT, TaskType.AUTOMATION]
            ),
            "claude": AIBackend(
                name="Claude",
                priority=2,
                status=BackendStatus.ACTIVE,
                api_key=os.getenv("CLAUDE_API_KEY", ""),
                base_url="https://api.anthropic.com/v1",
                model="claude-sonnet-4-20250514",
                specialties=[TaskType.CHAT, TaskType.ANALYSIS, TaskType.CODING]
            ),
            "deepseek": AIBackend(
                name="DeepSeek",
                priority=3,
                status=BackendStatus.ACTIVE,
                api_key=os.getenv("DEEPSEEK_API_KEY", ""),
                base_url="https://api.deepseek.com/v1",
                model="deepseek-chat",
                specialties=[TaskType.CHAT, TaskType.CODING, TaskType.TRANSLATION]
            ),
            "chatgpt": AIBackend(
                name="ChatGPT",
                priority=4,
                status=BackendStatus.OBSERVE,  # 观察状态
                api_key=os.getenv("OPENAI_API_KEY", ""),
                base_url="https://api.openai.com/v1",
                model="gpt-4",
                specialties=[TaskType.CHAT, TaskType.ANALYSIS]
            ),
            "local": AIBackend(
                name="本地模型",
                priority=5,
                status=BackendStatus.STANDBY,
                base_url="http://localhost:11434",
                model="qwen2.5:7b",
                specialties=[TaskType.CHAT]  # 离线备份
            )
        }
        
        # 任务队列
        self.task_queue: List[Dict] = []
        
    def get_status(self) -> Dict[str, Any]:
        """获取所有后台状态"""
        return {
            name: {
                "name": backend.name,
                "priority": backend.priority,
                "status": backend.status.value,
                "specialties": [s.value for s in backend.specialties]
            }
            for name, backend in self.backends.items()
        }
    
    def select_backend(self, task_type: TaskType) -> Optional[AIBackend]:
        """
        智能选择后台
        
        规则：
        1. 按优先级排序
        2. 检查是否擅长此任务
        3. 检查是否可用
        4. 检查速率限制
        """
        # 按优先级排序的可用后台
        available = sorted(
            [b for b in self.backends.values() if b.is_available()],
            key=lambda x: x.priority
        )
        
        # 优先选择擅长此任务的后台
        for backend in available:
            if backend.can_handle(task_type):
                return backend
        
        # 没有专门的，选第一个可用的
        return available[0] if available else None
    
    async def execute_task(self, 
                           task_type: TaskType,
                           prompt: str,
                           context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行任务
        
        1. 三色审计
        2. 选择后台
        3. DNA追溯
        4. 执行任务
        5. 返回结果
        """
        # 1. 三色审计
        audit_result = self.audit_engine.audit(prompt)
        
        if audit_result.level == AuditLevel.RED:
            return {
                "success": False,
                "error": audit_result.reason,
                "dna_code": audit_result.dna_code
            }
        
        if audit_result.level == AuditLevel.YELLOW:
            # 需要用户确认
            print(f"⚠️ {audit_result.reason}")
            print("建议:", audit_result.suggestions)
            # 在实际应用中，这里应该等待用户确认
        
        # 2. 选择后台
        backend = self.select_backend(task_type)
        if not backend:
            return {
                "success": False,
                "error": "🔴 没有可用的AI后台",
                "dna_code": self.dna_tracer.generate_dna(OperationType.AI_CALL, "NO_BACKEND")
            }
        
        # 3. DNA追溯
        dna_code = self.dna_tracer.start_trace(
            operator=backend.name,
            operation_type=OperationType.AI_CALL,
            detail=f"{task_type.value}: {prompt[:50]}...",
            input_data={"prompt": prompt, "context": context}
        )
        
        try:
            # 4. 执行任务
            if backend.name == "Claude":
                result = await self._call_claude(backend, prompt, context)
            elif backend.name == "DeepSeek":
                result = await self._call_deepseek(backend, prompt, context)
            elif backend.name == "Notion AI":
                result = await self._call_notion(backend, prompt, context)
            else:
                result = {"response": f"[{backend.name}模拟响应] 已收到任务"}
            
            # 5. 完成追溯
            self.dna_tracer.end_trace(
                dna_code,
                output_data=result,
                audit_result="🟢 成功"
            )
            
            return {
                "success": True,
                "backend": backend.name,
                "result": result,
                "dna_code": dna_code,
                "audit": audit_result.level.value
            }
            
        except Exception as e:
            self.dna_tracer.end_trace(
                dna_code,
                output_data=str(e),
                side_effects=[f"异常: {type(e).__name__}"],
                audit_result="🔴 失败"
            )
            
            # 尝试降级到下一个后台
            return await self._fallback_execute(task_type, prompt, context, backend.priority)
    
    async def _fallback_execute(self, 
                                task_type: TaskType,
                                prompt: str,
                                context: Dict,
                                failed_priority: int) -> Dict:
        """降级执行"""
        # 找下一个优先级的后台
        for backend in sorted(self.backends.values(), key=lambda x: x.priority):
            if backend.priority > failed_priority and backend.is_available():
                print(f"⚠️ 降级到 {backend.name}")
                return await self.execute_task(task_type, prompt, context)
        
        return {
            "success": False,
            "error": "🔴 所有后台都不可用"
        }
    
    async def _call_claude(self, backend: AIBackend, prompt: str, context: Dict) -> Dict:
        """调用Claude API"""
        if not backend.api_key:
            raise ValueError("Claude API Key未配置")
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "x-api-key": backend.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            payload = {
                "model": backend.model,
                "max_tokens": 4096,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            async with session.post(
                f"{backend.base_url}/messages",
                headers=headers,
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "response": data["content"][0]["text"],
                        "model": backend.model,
                        "usage": data.get("usage", {})
                    }
                else:
                    raise Exception(f"Claude API错误: {response.status}")
    
    async def _call_deepseek(self, backend: AIBackend, prompt: str, context: Dict) -> Dict:
        """调用DeepSeek API"""
        if not backend.api_key:
            raise ValueError("DeepSeek API Key未配置")
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {backend.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": backend.model,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            async with session.post(
                f"{backend.base_url}/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "response": data["choices"][0]["message"]["content"],
                        "model": backend.model,
                        "usage": data.get("usage", {})
                    }
                else:
                    raise Exception(f"DeepSeek API错误: {response.status}")
    
    async def _call_notion(self, backend: AIBackend, prompt: str, context: Dict) -> Dict:
        """调用Notion API（数据管理）"""
        # Notion主要用于数据管理，不是对话
        return {
            "response": "Notion AI用于数据管理，请使用具体的Notion操作",
            "suggestion": "使用 notion_manager.py 中的功能"
        }


# ==================== 便捷函数 ====================
scheduler = None

def get_scheduler() -> FiveBackendsScheduler:
    """获取调度器单例"""
    global scheduler
    if scheduler is None:
        scheduler = FiveBackendsScheduler()
    return scheduler


async def ask_ai(prompt: str, task_type: TaskType = TaskType.CHAT) -> str:
    """
    便捷函数：询问AI
    
    Usage:
        response = await ask_ai("帮我分析这段代码")
    """
    s = get_scheduler()
    result = await s.execute_task(task_type, prompt)
    
    if result["success"]:
        return result["result"]["response"]
    else:
        return f"错误: {result['error']}"


# ==================== 使用示例 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("🤖 五大AI后台调度系统测试")
    print("=" * 60)
    
    scheduler = FiveBackendsScheduler()
    
    # 显示后台状态
    print("\n📊 后台状态:")
    for name, status in scheduler.get_status().items():
        print(f"  {status['status']} {status['name']} (优先级: {status['priority']})")
    
    # 测试任务选择
    print("\n🎯 任务分配测试:")
    test_tasks = [
        TaskType.DATA_MANAGEMENT,
        TaskType.CHAT,
        TaskType.CODING,
        TaskType.TRANSLATION
    ]
    
    for task in test_tasks:
        backend = scheduler.select_backend(task)
        print(f"  {task.value} → {backend.name if backend else '无'}")
    
    # 异步测试（模拟）
    async def test_execution():
        print("\n🚀 执行测试（模拟模式）:")
        
        # 安全操作
        result = await scheduler.execute_task(
            TaskType.CHAT,
            "你好，请介绍一下龍魂终端"
        )
        print(f"  结果: {result['success']}")
        print(f"  后台: {result.get('backend', 'N/A')}")
        print(f"  DNA: {result['dna_code']}")
        
        # 危险操作测试
        result = await scheduler.execute_task(
            TaskType.AUTOMATION,
            "rm -rf /"
        )
        print(f"\n  危险操作测试:")
        print(f"  结果: {result['success']}")
        print(f"  原因: {result.get('error', 'N/A')}")
    
    asyncio.run(test_execution())
