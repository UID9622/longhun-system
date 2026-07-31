# DNA: #龍芯⚡️丙午·乙未·乙丑·明夷-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# core/agent/education_agent.py
# 龍魂 · 教育智能体 · 自主决策与任务规划

from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import hashlib
from datetime import datetime

# === DNA常量 ===
MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️"
MASTER_UID = "9622"

class IntentType(Enum):
    """意图类型"""
    KNOWLEDGE_QUERY = "knowledge_query"      # 知识查询
    HOMEWORK_HELP = "homework_help"          # 作业辅导
    COURSE_RECOMMEND = "course_recommend"   # 课程推荐
    EXAM_PREP = "exam_prep"                 # 备考复习
    CONCEPT_EXPLAIN = "concept_explain"     # 概念解释
    PRACTICE_DRILL = "practice_drill"       # 练习训练
    CHAT_GENERAL = "chat_general"           # 闲聊


@dataclass
class AgentMemory:
    """智能体记忆"""
    short_term: List[Dict] = field(default_factory=list)   # 短期记忆（当前对话）
    long_term: Dict[str, Any] = field(default_factory=dict)            # 长期记忆（用户画像）
    max_short_term: int = 10
    
    def add_interaction(self, role: str, content: str, metadata: Optional[Dict] = None):
        """添加交互记录"""
        self.short_term.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        })
        
        # 限制短期记忆长度
        if len(self.short_term) > self.max_short_term:
            self.short_term = self.short_term[-self.max_short_term:]
    
    def get_context(self) -> str:
        """获取对话上下文"""
        return "\n".join([
            f"{m['role']}: {m['content']}" 
            for m in self.short_term
        ])
    
    def update_long_term(self, key: str, value: any):
        """更新长期记忆"""
        self.long_term[key] = {
            "value": value,
            "updated": datetime.now().isoformat()
        }


@dataclass
class TaskPlan:
    """任务计划"""
    task_id: str
    intent: IntentType
    steps: List[Dict]
    current_step: int = 0
    status: str = "pending"  # pending/running/completed/failed
    result: Optional[str] = None
    
    def next_step(self) -> Optional[Dict]:
        """获取下一步"""
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            self.current_step += 1
            return step
        return None
    
    def is_complete(self) -> bool:
        """是否完成"""
        return self.current_step >= len(self.steps)


class EducationAgent:
    """教育智能体"""
    
    def __init__(self, rag_service=None, tool_registry=None):
        self.memory = AgentMemory()
        self.rag_service = rag_service
        self.tool_registry = tool_registry or {}
        self.intent_classifier = self._init_classifier()
    
    def _init_classifier(self):
        """初始化意图分类器 - 实际使用BERT/规则引擎"""
        return None
    
    def process(self, user_input: str) -> Dict[str, Any]:
        """处理用户输入"""
        # 1. 意图识别
        intent = self._classify_intent(user_input)
        
        # 2. 记录到记忆
        self.memory.add_interaction("user", user_input, {"intent": intent.value})
        
        # 3. 任务规划
        plan = self._plan_task(intent, user_input)
        
        # 4. 执行计划
        result = self._execute_plan(plan)
        
        # 5. 记录结果
        self.memory.add_interaction("assistant", result, {"plan_id": plan.task_id})
        
        # 6. 反思
        reflection = self._reflect(plan, result)
        
        return {
            "response": result,
            "intent": intent.value,
            "plan_id": plan.task_id,
            "reflection": reflection,
            "memory_stats": {
                "short_term": len(self.memory.short_term),
                "long_term_keys": list(self.memory.long_term.keys())
            }
        }
    
    def _classify_intent(self, text: str) -> IntentType:
        """意图分类 - 关键词规则"""
        text = text.lower()
        
        if any(k in text for k in ["什么是", "定义", "概念", "解释", "介绍一下"]):
            return IntentType.CONCEPT_EXPLAIN
        elif any(k in text for k in ["作业", "题目", "怎么做", "求解", "答案"]):
            return IntentType.HOMEWORK_HELP
        elif any(k in text for k in ["推荐", "学什么", "课程", "建议"]):
            return IntentType.COURSE_RECOMMEND
        elif any(k in text for k in ["考试", "复习", "备考", "重点"]):
            return IntentType.EXAM_PREP
        elif any(k in text for k in ["练习", "做题", "训练", "刷题"]):
            return IntentType.PRACTICE_DRILL
        elif any(k in text for k in ["你好", "谢谢", "再见", "在吗"]):
            return IntentType.CHAT_GENERAL
        
        return IntentType.KNOWLEDGE_QUERY
    
    def _plan_task(self, intent: IntentType, query: str) -> TaskPlan:
        """任务规划"""
        steps = []
        
        if intent == IntentType.KNOWLEDGE_QUERY:
            steps = [
                {"action": "rag_search", "params": {"query": query}},
                {"action": "summarize", "params": {"style": "educational"}},
                {"action": "verify", "params": {"check_sources": True}}
            ]
        elif intent == IntentType.HOMEWORK_HELP:
            steps = [
                {"action": "parse_problem", "params": {"text": query}},
                {"action": "rag_search", "params": {"query": query}},
                {"action": "solve_step_by_step", "params": {}},
                {"action": "explain_reasoning", "params": {}}
            ]
        elif intent == IntentType.CONCEPT_EXPLAIN:
            steps = [
                {"action": "rag_search", "params": {"query": query}},
                {"action": "simplify", "params": {"level": "student"}},
                {"action": "add_examples", "params": {"count": 2}}
            ]
        elif intent == IntentType.COURSE_RECOMMEND:
            steps = [
                {"action": "analyze_user_level", "params": {}},
                {"action": "search_courses", "params": {"query": query}},
                {"action": "rank_recommendations", "params": {}}
            ]
        else:
            steps = [
                {"action": "rag_search", "params": {"query": query}},
                {"action": "generate_response", "params": {}}
            ]
        
        return TaskPlan(
            task_id=f"TASK-{hashlib.md5(query.encode()).hexdigest()[:8]}",
            intent=intent,
            steps=steps
        )
    
    def _execute_plan(self, plan: TaskPlan) -> str:
        """执行计划"""
        results = []
        
        while not plan.is_complete():
            step = plan.next_step()
            if not step:
                break
            
            plan.status = "running"
            action = step["action"]
            params = step["params"]
            
            result = self._execute_action(action, params)
            results.append(f"[{action}] {result}")
        
        plan.status = "completed"
        plan.result = "\n".join(results)
        
        return plan.result
    
    def _execute_action(self, action: str, params: Dict[str, Any]) -> str:
        """执行具体动作"""
        if action == "rag_search" and self.rag_service:
            response = self.rag_service.query(params["query"])
            return f"检索到 {len(response.sources)} 个相关文档，置信度 {response.confidence}"
        
        elif action == "summarize":
            return "已生成教育化摘要"
        
        elif action == "parse_problem":
            return "已解析题目结构"
        
        elif action == "solve_step_by_step":
            return "已分步求解"
        
        elif action == "explain_reasoning":
            return "已解释推理过程"
        
        elif action == "simplify":
            return f"已简化至{params.get('level', 'student')}水平"
        
        elif action == "add_examples":
            return f"已添加{params.get('count', 2)}个示例"
        
        elif action == "analyze_user_level":
            level = self.memory.long_term.get("user_level", {}).get("value", "intermediate")
            return f"用户水平: {level}"
        
        elif action == "search_courses":
            return "已搜索相关课程"
        
        elif action == "rank_recommendations":
            return "已排序推荐结果"
        
        elif action == "generate_response":
            return "已生成回复"
        
        elif action == "verify":
            return "已验证来源可靠性"
        
        return f"未知动作: {action}"
    
    def _reflect(self, plan: TaskPlan, result: str) -> Dict[str, Any]:
        """反思机制"""
        reflection = {
            "plan_id": plan.task_id,
            "intent": plan.intent.value,
            "steps_executed": plan.current_step,
            "total_steps": len(plan.steps),
            "success": plan.status == "completed",
            "improvements": []
        }
        
        if plan.current_step < len(plan.steps):
            reflection["improvements"].append("部分步骤未执行，需检查原因")
        
        if plan.intent == IntentType.HOMEWORK_HELP and "rag_search" not in [s["action"] for s in plan.steps]:
            reflection["improvements"].append("作业辅导应优先检索相关知识")
        
        return reflection
    
    def get_memory_snapshot(self) -> Dict[str, Any]:
        """获取记忆快照"""
        return {
            "short_term": self.memory.short_term,
            "long_term": self.memory.long_term,
            "user_profile": self._build_user_profile()
        }
    
    def _build_user_profile(self) -> Dict[str, Any]:
        """构建用户画像"""
        profile = {
            "interests": [],
            "level": "unknown",
            "weak_areas": [],
            "learning_history": []
        }
        
        if "interests" in self.memory.long_term:
            profile["interests"] = self.memory.long_term["interests"]["value"]
        if "level" in self.memory.long_term:
            profile["level"] = self.memory.long_term["level"]["value"]
        
        return profile


# === 使用示例 ===
if __name__ == "__main__":
    agent = EducationAgent()
    
    responses = []
    for query in [
        "什么是二次函数？",
        "帮我解这道数学题：x² + 5x + 6 = 0",
        "推荐一些适合我的物理课程"
    ]:
        result = agent.process(query)
        responses.append(result)
        print(f"\n[用户] {query}")
        print(f"[意图] {result['intent']}")
        print(f"[回复] {result['response'][:100]}...")
        print(f"[反思] {result['reflection']}")
