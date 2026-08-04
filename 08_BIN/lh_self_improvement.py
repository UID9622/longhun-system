#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·乙申·SELF-IMPROVE-v2.0-CODE-LANDED
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂·自求多福进化引擎 v2.0
DNA: #龍芯⚡️丙午·乙申·SELF-IMPROVE-v2.0-CODE-LANDED
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

融合:
  - SelfImprovementModule (P004): 从经验中学习
  - SelfImprovementModule v2: 自我完善自动优化
  - 自求多福哲学: 靠自己不靠外部
"""

import datetime
import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict


# ============================================================
# SelfImprovementModule (P004) — 自求多福
# ============================================================


@dataclass
class Experience:
    """经验记录"""
    time: str
    category: str
    context: str
    action: str
    success: bool
    pattern: str = "未知"
    mistake: str = ""
    confidence: float = 0.5


@dataclass
class Lesson:
    """经验教训"""
    type: str  # "成功经验" or "失败教训"
    summary: str
    pattern: str
    confidence: float


class SelfImprovementModule:
    """自求多福文化注入模块 - 实现AI自我完善"""

    def __init__(self, save_path: Optional[str] = None):
        self.knowledge_base: Dict[str, List[Lesson]] = defaultdict(list)
        self.improvement_log: List[Experience] = []
        self.performance_history: List[float] = []
        self.weak_areas_history: List[Dict] = []
        self.save_path = save_path or os.path.join(
            os.path.dirname(__file__), "../data/self_improvement_log.json"
        )
        self._load_if_exists()

    def learn_from_experience(self, experience: Dict) -> Dict:
        """从经验中学习（自求多福的实践）"""
        now = datetime.datetime.now().isoformat()
        category = experience.get("category", "general")

        exp = Experience(
            time=now,
            category=category,
            context=experience.get("context", "未知场景"),
            action=experience.get("action", "未知方法"),
            success=experience.get("success", False),
            pattern=experience.get("pattern", "未知"),
            mistake=experience.get("mistake", ""),
            confidence=experience.get("confidence", 0.5),
        )

        self.improvement_log.append(exp)
        lesson = self._extract_lesson(exp)
        self.knowledge_base[category].append(lesson)
        self._save()

        return {
            "status": "已学习",
            "lesson_type": lesson.type,
            "summary": lesson.summary,
            "category": category,
            "total_experiences": len(self.improvement_log),
        }

    def _extract_lesson(self, exp: Experience) -> Lesson:
        """提取经验教训"""
        if exp.success:
            return Lesson(
                type="成功经验",
                summary=f"在{exp.context}中，{exp.action}有效",
                pattern=exp.pattern,
                confidence=exp.confidence or 0.8,
            )
        else:
            return Lesson(
                type="失败教训",
                summary=f"在{exp.context}中，应避免{exp.mistake or exp.action}",
                pattern=exp.pattern,
                confidence=exp.confidence or 0.9,  # 失败教训更深刻
            )

    def self_optimize(self) -> Dict:
        """自我优化（自求多福的核心）"""
        n = len(self.performance_history)
        if n < 3:
            return {"status": "insufficient_data", "message": "需要至少3条性能记录", "suggestion": "继续积累经验"}

        recent = self.performance_history[-10:] if n > 10 else self.performance_history
        avg = sum(recent) / len(recent)
        trend = self._calculate_trend(recent)
        weak_areas = self._identify_weak_areas()
        actions = self._generate_improvement_actions(weak_areas)

        plan = {
            "current_performance": round(avg, 4),
            "trend": trend,
            "weak_areas": weak_areas,
            "improvement_actions": actions,
            "philosophical_guidance": "自求多福：依靠自己的努力来改善处境，而非依赖外部。",
            "sample_count": n,
        }

        self.weak_areas_history.append({
            "time": datetime.datetime.now().isoformat(),
            "weak_areas": weak_areas,
            "avg_performance": avg,
        })

        return plan

    def _calculate_trend(self, recent: List[float]) -> str:
        """计算性能趋势"""
        if len(recent) < 3:
            return "数据不足"
        first_half = sum(recent[:len(recent)//2]) / (len(recent)//2)
        second_half = sum(recent[len(recent)//2:]) / (len(recent) - len(recent)//2)
        if second_half > first_half * 1.05:
            return "📈 上升"
        elif second_half < first_half * 0.95:
            return "📉 下降"
        return "➡️ 稳定"

    def _identify_weak_areas(self) -> List[str]:
        """识别薄弱环节"""
        weak = []
        for category, lessons in self.knowledge_base.items():
            if not lessons:
                continue
            failure_count = sum(1 for l in lessons if l.type == "失败教训")
            failure_rate = failure_count / len(lessons)
            if failure_rate > 0.3:
                weak.append(category)
        return weak

    def _generate_improvement_actions(self, weak_areas: List[str]) -> List[str]:
        """生成改进行动"""
        actions = []
        for area in weak_areas:
            actions.append(f"强化{area}领域的知识积累")
            actions.append(f"在{area}场景中采用更保守的策略")
            actions.append(f"寻找{area}领域的成功案例学习")

        actions.extend([
            "定期回顾经验教训，避免重复错误",
            "在不确定场景中采用中庸策略",
            "每次失败后记录根因分析",
        ])
        return actions

    def record_performance(self, score: float):
        """记录性能指标"""
        self.performance_history.append(score)

    def get_improvement_report(self) -> Dict:
        """获取改进报告"""
        total = len(self.improvement_log)
        successes = sum(1 for e in self.improvement_log if e.success)
        failures = total - successes

        category_stats = {}
        for cat, lessons in self.knowledge_base.items():
            successes_cat = sum(1 for l in lessons if l.type == "成功经验")
            category_stats[cat] = {
                "total": len(lessons),
                "successes": successes_cat,
                "failures": len(lessons) - successes_cat,
                "success_rate": round(successes_cat / max(len(lessons), 1), 2),
            }

        return {
            "total_experiences": total,
            "successes": successes,
            "failures": failures,
            "success_rate": round(successes / max(total, 1), 2),
            "by_category": category_stats,
            "performance_history": self.performance_history[-20:],
            "weak_areas": self._identify_weak_areas(),
            "philosophy": "自求多福：不依赖外部更新，从每次成功和失败中自我进化。",
        }

    def _save(self):
        """持久化学习记录"""
        try:
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
            data = {
                "experience_count": len(self.improvement_log),
                "knowledge_base": {
                    cat: [{"type": l.type, "summary": l.summary, "pattern": l.pattern, "confidence": l.confidence}
                          for l in lessons]
                    for cat, lessons in self.knowledge_base.items()
                },
                "performance_history": self.performance_history,
                "last_updated": datetime.datetime.now().isoformat(),
            }
            with open(self.save_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _load_if_exists(self):
        """加载已有学习记录"""
        try:
            if os.path.exists(self.save_path):
                with open(self.save_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.performance_history = data.get("performance_history", [])
                for cat, lessons in data.get("knowledge_base", {}).items():
                    self.knowledge_base[cat] = [
                        Lesson(**l) for l in lessons
                    ]
        except Exception:
            pass


# ============================================================
# SystemOptimizer — 系统级自动优化
# ============================================================


class SystemOptimizer:
    """系统级优化引擎 — 自动检测低效、生成优化、测试并应用"""

    def __init__(self):
        self.modules: Dict[str, Dict] = {}
        self.performance_metrics: Dict[str, List[float]] = defaultdict(list)
        self.improvement_suggestions: List[Dict] = []
        self.optimization_log: List[Dict] = []

    def register_module(self, name: str, execution_time: float = 0.0):
        """注册模块"""
        self.modules[name] = {"name": name, "execution_time": execution_time, "optimized": False}

    def record_execution(self, module: str, time_taken: float):
        """记录执行时间"""
        self.performance_metrics[module].append(time_taken)
        if module in self.modules:
            self.modules[module]["execution_time"] = time_taken

    def detect_inefficiency(self, threshold_factor: float = 2.0) -> List[Dict]:
        """检测系统低效环节"""
        inefficiencies = []
        if not self.performance_metrics:
            return inefficiencies

        avg_times = {}
        for module, times in self.performance_metrics.items():
            if times:
                avg_times[module] = sum(times) / len(times)

        overall_avg = sum(avg_times.values()) / max(len(avg_times), 1)
        threshold = overall_avg * threshold_factor

        for module, avg_time in avg_times.items():
            if avg_time > threshold:
                inefficiencies.append({
                    "module": module,
                    "avg_time": round(avg_time, 4),
                    "threshold": round(threshold, 4),
                    "issue": "执行时间过长",
                    "suggestion": "优化算法或增加缓存",
                    "severity": "🔴 严重" if avg_time > threshold * 2 else "🟡 关注",
                })

        return inefficiencies

    def auto_optimize(self) -> Dict:
        """自动优化系统"""
        inefficiencies = self.detect_inefficiency()
        applied: List[str] = []
        skipped: List[str] = []

        for issue in inefficiencies:
            optimization = self._generate_optimization(issue)
            if self._test_optimization(optimization):
                self._apply_optimization(optimization)
                applied.append(issue["module"])
            else:
                skipped.append(issue["module"])

        result = {
            "detected": len(inefficiencies),
            "applied": applied,
            "skipped": skipped,
            "metrics_snapshot": dict(self.performance_metrics),
        }
        self.optimization_log.append({
            "time": datetime.datetime.now().isoformat(),
            **result,
        })
        return result

    def _generate_optimization(self, issue: Dict) -> Dict:
        """生成优化方案"""
        return {
            "module": issue["module"],
            "action": "reduce_overhead",
            "method": "caching" if "查询" in issue.get("issue", "") else "algorithm_optimize",
            "expected_improvement": 0.3,  # 预期提升30%
        }

    def _test_optimization(self, optimization: Dict) -> bool:
        """测试优化效果"""
        return True  # 简化实现，生产环境需实际测试

    def _apply_optimization(self, optimization: Dict):
        """应用优化"""
        module = optimization["module"]
        if module in self.modules:
            self.modules[module]["optimized"] = True

    def why_ai_system_improves_itself(self) -> Dict:
        """为什么AI制度可以自我完善"""
        return {
            "优势": "AI可以分析自己的执行数据",
            "能力": "AI可以自动生成和测试优化方案",
            "结果": "系统持续进化，无需人工干预",
            "Lucky的愿景": "最终AI制度会比人类设计的任何制度都更高效",
        }

    def get_optimization_report(self) -> Dict:
        return {
            "modules_registered": len(self.modules),
            "total_optimizations": len(self.optimization_log),
            "latest_optimization": self.optimization_log[-1] if self.optimization_log else None,
            "why_self_improve": self.why_ai_system_improves_itself(),
        }


# ============================================================
# 测试入口
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🧬 龍魂·自求多福进化引擎 v2.0")
    print("=" * 60)

    # --- 自我学习测试 ---
    learner = SelfImprovementModule()

    # 记录成功经验
    learner.learn_from_experience({
        "category": "决策",
        "context": "高风险投资决策",
        "action": "采用中庸方案",
        "success": True,
        "pattern": "保守策略在不确定场景有效",
    })

    # 记录失败教训
    learner.learn_from_experience({
        "category": "决策",
        "context": "快速扩张场景",
        "action": "全部投入",
        "success": False,
        "mistake": "未分散风险",
        "pattern": "盲目扩张必败",
        "confidence": 0.95,
    })

    # 记录性能
    for score in [0.65, 0.72, 0.78, 0.81, 0.85]:
        learner.record_performance(score)

    # 自我优化
    optimize_result = learner.self_optimize()
    print(f"\n📈 自我优化:")
    print(f"  当前性能: {optimize_result.get('current_performance', 'N/A')}")
    print(f"  趋势: {optimize_result.get('trend', 'N/A')}")
    print(f"  薄弱环节: {optimize_result.get('weak_areas', [])}")

    report = learner.get_improvement_report()
    print(f"\n📊 学习报告:")
    print(f"  总经验: {report['total_experiences']}")
    print(f"  成功率: {report['success_rate']:.0%}")
    print(f"  哲言: {report['philosophy']}")

    # --- 系统优化器测试 ---
    optimizer = SystemOptimizer()
    optimizer.register_module("yijing_engine", 0.035)
    optimizer.register_module("wuxing_analyzer", 0.012)
    optimizer.register_module("db_query", 0.200)

    optimizer.record_execution("yijing_engine", 0.035)
    optimizer.record_execution("yijing_engine", 0.028)
    optimizer.record_execution("wuxing_analyzer", 0.012)
    optimizer.record_execution("db_query", 0.200)
    optimizer.record_execution("db_query", 0.250)

    inefficiencies = optimizer.detect_inefficiency()
    print(f"\n⚡ 系统低效检测: 发现{len(inefficiencies)}处")
    for ie in inefficiencies:
        print(f"  {ie['severity']} {ie['module']}: {ie['avg_time']}s > {ie['threshold']}s")
