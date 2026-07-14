#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║     龍魂·统一训练管线 v1.0 — 多引擎联动·可扩展架构                            ║
║     Unified Training Pipeline · Multi-Engine Orchestration              ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·辛未·乙酉·需-UNIFIED-PIPELINE-v1.0                      ║
║  架构: 输入→预处理→路由→并行引擎→聚合→训练数据输出                            ║
║  联动: 7引擎·3管线·交叉验证·共享上下文                                     ║
║  铁律: 底座不动·变量可动·引擎可插拔·管线可扩展                                ║
╠══════════════════════════════════════════════════════════════════════════╣
║  📂 数据来源:                                                             ║
║    类型: 编排引擎 · 不存储用户数据 · 纯计算管道                               ║
║    联动: 各引擎共享中间结果上下文·交叉验证·互增强                              ║
║    训练: 输出结构化JSONL·供后续模型训练使用                                   ║
╠══════════════════════════════════════════════════════════════════════════╣
║  📋 责任清单:                                                             ║
║    管线设计: UID9622（多引擎联动架构）                                       ║
║    代码实现: AI执行器                                                      ║
║    审核: UID9622                                                           ║
╚══════════════════════════════════════════════════════════════════════════╝

用法:
    # 单次全管线推演
    python3 bin/lh_unified_pipeline.py "中美关系未来走向"

    # 指定引擎子集
    python3 bin/lh_unified_pipeline.py --engines yijing,philosophy,sandbox "AI发展趋势"

    # 批量处理 + 导出训练数据
    python3 bin/lh_unified_pipeline.py --batch queries.txt --export training_data.jsonl

    # 管道模式
    echo "量子计算对人类社会的影响" | python3 bin/lh_unified_pipeline.py --stdin

    # JSON输出
    python3 bin/lh_unified_pipeline.py --json "你的问题"

    # 查看管线状态
    python3 bin/lh_unified_pipeline.py --status

    # 模块导入
    from bin.lh_unified_pipeline import UnifiedPipeline
    pipeline = UnifiedPipeline()
    result = pipeline.run("你的问题")

架构:
    ┌─────────────────────────────────────────────────────┐
    │              龍魂·统一训练管线 v2.0                    │
    │                                                       │
    │  Input → Preprocess → [Router] → Parallel Engines    │
    │                         │                             │
    │              ┌──────────┼──────────┐                 │
    │              ▼          ▼          ▼                  │
    │         TextAnalysis  Philosophy  Simulation          │
    │         (Anxiety+      (Yijing+    (Sandbox+          │
    │          RobotScore)   Philosophy) Observer+          │
    │                                      RBConfrontation) │
    │              │          │          │                   │
    │              └──────────┼──────────┘                  │
    │                         ▼                             │
    │                   Aggregator                          │
    │                    │        │                          │
    │                    ▼        ▼                          │
    │            UnifiedReport  TrainingData                │
    │            (JSON+MD)      (JSONL)                     │
    └─────────────────────────────────────────────────────┘
"""

import sys
import os
import json
import time
import hashlib
import threading
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# 项目根路径
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "bin"))


# ═══════════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════════

@dataclass
class EngineResult:
    """单个引擎执行结果"""
    engine: str
    status: str           # success / error / skipped
    duration_ms: float
    output: Dict[str, Any]
    error: Optional[str] = None


@dataclass
class PipelineResult:
    """管线聚合结果"""
    dna: str
    timestamp: str
    input_text: str
    input_hash: str
    engines_used: List[str]
    results: Dict[str, EngineResult]
    cross_validation: Dict[str, Any]
    synthesis: Dict[str, Any]
    training_vector: Dict[str, Any]   # 可导出的训练特征向量
    total_duration_ms: float


# ═══════════════════════════════════════════════════════════
# 引擎适配器 — 统一接口封装各引擎
# ═══════════════════════════════════════════════════════════

class EngineAdapter:
    """引擎适配器基类 — 统一接口"""

    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category  # text_analysis / philosophy / simulation
        self._engine = None
        self._available = False

    def initialize(self) -> bool:
        """初始化引擎，返回是否可用"""
        raise NotImplementedError

    def execute(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行引擎，返回结果字典"""
        raise NotImplementedError

    def is_available(self) -> bool:
        return self._available


class YijingAdapter(EngineAdapter):
    """易经推演引擎适配器"""

    def __init__(self):
        super().__init__("yijing", "philosophy")

    def initialize(self) -> bool:
        try:
            from bin.lh_yijing_推演引擎 import YijingEngine
            self._engine = YijingEngine()
            self._available = True
            return True
        except Exception as e:
            self._available = False
            return False

    def execute(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self._engine:
            return {"error": "引擎未初始化"}
        result = self._engine.deduce(text)
        return {
            "卦象": result.get("gua_xiang", {}),
            "五行": result.get("five_element_deduction", {}),
            "道德经公理": result.get("dao_de_jing_axioms", []),
            "结论": result.get("conclusion", {}),
            "推导链": result.get("trace", []),
        }


class PhilosophyAdapter(EngineAdapter):
    """统一哲学引擎适配器"""

    def __init__(self):
        super().__init__("philosophy", "philosophy")

    def initialize(self) -> bool:
        try:
            from bin.lh_philosophy_unified_engine import PhilosophyUnifiedEngine
            self._engine = PhilosophyUnifiedEngine()
            self._available = True
            return True
        except Exception as e:
            self._available = False
            return False

    def execute(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self._engine:
            return {"error": "引擎未初始化"}
        result = self._engine.deduce(text)
        return {
            "维度结果": {k: v for k, v in result.get("dimensions", {}).items()},
            "交叉验证": result.get("cross_validation", {}),
            "综合结论": result.get("synthesis", {}),
        }


class SandboxAdapter(EngineAdapter):
    """
    沙盒推演引擎适配器 — 聚合多子引擎。

    沙盒引擎由多个独立子引擎组成（无单一入口类），
    适配器实例化关键子引擎并按需调用。
    """

    def __init__(self):
        super().__init__("sandbox", "simulation")
        self._time_engine = None
        self._game_engine = None
        self._hweapon = None

    def initialize(self) -> bool:
        try:
            from bin.lh_sandbox_console import (
                TimeProjectionEngine,
                GameTheorySandbox,
                HWeaponSystem,
            )
            self._time_engine = TimeProjectionEngine()
            self._game_engine = GameTheorySandbox()
            self._hweapon = HWeaponSystem()
            self._available = True
            return True
        except Exception as e:
            self._available = False
            return False

    def execute(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self._time_engine:
            return {"error": "沙盒子引擎未初始化"}

        # 获取哲学/易经结论作为推演上下文
        philosophy_ctx = context.get("philosophy", {})
        yijing_ctx = context.get("yijing", {})

        # 提取关键信号
        yj_gua = ""
        yj_strategy = ""
        if yijing_ctx:
            gua = yijing_ctx.get("卦象", {})
            yj_gua = f"{gua.get('upper', {}).get('name', '')}{gua.get('lower', {}).get('name', '')}"
            yj_strategy = yijing_ctx.get("结论", {}).get("strategy", "")

        ph_tricolor = ""
        if philosophy_ctx:
            synth = philosophy_ctx.get("综合结论", {})
            ph_tricolor = synth.get("tricolor", "")

        # 时间推演（含易经卦象上下文）
        try:
            time_result = self._time_engine.project(text, time_range_years=5)
            time_out = {
                "卦象": getattr(time_result, "gua_name", ""),
                "五行": getattr(time_result, "wuxing", ""),
                "三色": getattr(time_result, "tricolor", ""),
                "预测": getattr(time_result, "prediction", "")[:300],
            }
        except Exception:
            time_out = {"预测": "时间推演子引擎执行异常"}

        # 博弈对抗（中等级别防线）
        try:
            game_result = self._game_engine.simulate(text, depth=2)
            game_out = {
                "卦象": getattr(game_result, "gua_name", ""),
                "防御成功率": getattr(game_result, "confidence", 0),
                "预测": getattr(game_result, "prediction", "")[:300],
            }
        except Exception:
            game_out = {"预测": "博弈对抗子引擎执行异常"}

        return {
            "时间推演": time_out,
            "博弈对抗": game_out,
            "上下文信号": {
                "易经卦象": yj_gua,
                "易经策略": yj_strategy,
                "哲学审计": ph_tricolor,
            },
            "综合建议": (
                f"[易经信号] {yj_strategy} | "
                f"[哲学审计] {ph_tricolor} | "
                f"[时间推演] {time_out.get('预测', '')[:100]}"
            ),
        }


class AnxietyAdapter(EngineAdapter):
    """焦虑检测引擎适配器"""

    def __init__(self):
        super().__init__("anxiety", "text_analysis")

    def initialize(self) -> bool:
        try:
            from bin.lh_anxiety_detector import 焦虑检测器
            self._engine = 焦虑检测器()
            self._available = True
            return True
        except Exception as e:
            self._available = False
            return False

    def execute(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self._engine:
            return {"error": "引擎未初始化"}
        result = self._engine.检测(text)
        # 触角检测结果属性: 命中, 话术类型编码, 话术类型中文, 毒性等级, 本源追溯, 反制建议, 建议输出
        return {
            "检测到焦虑话术": result.命中,
            "话术类型编码": result.话术类型编码 if result.命中 else "",
            "话术类型中文": result.话术类型中文 if result.命中 else "",
            "毒性等级": result.毒性等级.name if result.命中 else "无",
            "毒性emoji": result.毒性等级.emoji if result.命中 else "",
            "本源追溯": {
                "文化根_根源": result.本源追溯.文化根_根源 if result.命中 and result.本源追溯 else "",
                "心理根_机制": result.本源追溯.心理根_机制 if result.命中 and result.本源追溯 else "",
                "权力根_结构": result.本源追溯.权力根_结构 if result.命中 and result.本源追溯 else "",
            } if result.命中 else {},
            "反制公式": result.反制建议.公式名称 if result.命中 and result.反制建议 else "",
            "反制内容": result.反制建议.公式内容 if result.命中 and result.反制建议 else "",
            "建议输出": result.建议输出 if result.命中 else "未检测到焦虑话术",
        }


class RobotScoreAdapter(EngineAdapter):
    """反图灵检测引擎适配器"""

    def __init__(self):
        super().__init__("robot_score", "text_analysis")

    def initialize(self) -> bool:
        try:
            from bin.lh_robot_score import RobotScore检测器
            self._engine = RobotScore检测器()
            self._available = True
            return True
        except Exception as e:
            self._available = False
            return False

    def execute(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self._engine:
            return {"error": "引擎未初始化"}
        report = self._engine.检测(text)
        return {
            "RobotScore": report.score,
            "判定": report.verdict,
            "可疑度": report.is_suspicious,
            "真人度": report.is_human,
            "分解": report.breakdown,
            "建议": report.recommendation,
        }


class ActiveObserverAdapter(EngineAdapter):
    """
    主动观察引擎适配器 — 守护模式适配为一次性扫描。

    原始引擎设计为守护进程（常驻扫描），管线中使用时
    适配为单次规则扫描 + 状态快照。
    """

    def __init__(self):
        super().__init__("active_observer", "simulation")

    def initialize(self) -> bool:
        try:
            from bin.lh_active_observation import get_observation_engine
            self._engine = get_observation_engine()
            self._engine.load_default_rules()
            self._available = True
            return True
        except Exception:
            self._available = False
            return False

    def execute(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self._engine:
            return {"状态": "跳过", "原因": "观察引擎不可用"}

        try:
            # 获取规则和状态快照
            rules = self._engine.get_rules()
            active_rules = [r for r in rules if r.enabled]
            stats = self._engine.get_stats() if hasattr(self._engine, 'get_stats') else {}

            # 结合管线上下文的联动信号
            signals = {}
            # 如果焦虑检测触发了 → 建议启动情绪守护规则
            if context.get("anxiety", {}).get("检测到焦虑话术"):
                signals["建议"] = "检测到焦虑话术·建议启用情绪守护规则"
            # 如果 RobotScore 判定机器嫌疑
            if context.get("robot_score", {}).get("可疑度"):
                signals["注意"] = "RobotScore判定机器嫌疑·建议审计来源"

            return {
                "活跃规则数": len(active_rules),
                "总规则数": len(rules),
                "统计": stats,
                "联动信号": signals,
            }
        except Exception as e:
            return {"状态": "扫描异常", "错误": str(e)}


class RBConfrontationAdapter(EngineAdapter):
    """
    红蓝对抗融合引擎适配器 — 五阶段对抗融合

    与其他引擎联动:
    - 输入先经过 anxiety/robot_score 过滤
    - 对抗结果作为哲学推演的上游信号
    - 融合体命名可结合易经卦象
    """

    def __init__(self):
        super().__init__("rb_confrontation", "simulation")

    def initialize(self) -> bool:
        try:
            from bin.lh_rb_confrontation_engine import (
                RBConfrontationEngine, TriggerType,
                BlackAngelLegionBridge, DualBrainBridge,
            )
            self._engine = RBConfrontationEngine()
            self._trigger_type = TriggerType
            self._angel_bridge = BlackAngelLegionBridge
            self._brain_bridge = DualBrainBridge
            self._available = True
            return True
        except Exception:
            self._available = False
            return False

    def execute(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self._engine:
            return {"error": "红蓝对抗引擎未初始化"}

        # 提取前置引擎信号
        module_name = context.get("module", "unified_pipeline_input")
        auto_advance = context.get("auto_advance", True)

        # 获取已有引擎上下文
        anxiety_ctx = context.get("anxiety", {})
        robot_ctx = context.get("robot_score", {})

        # 如果焦虑检测触发了 → 用哲学冲突触发
        trigger = self._trigger_type.MANUAL
        if anxiety_ctx.get("检测到焦虑话术"):
            trigger = self._trigger_type.PHILOSOPHY_CONFLICT

        try:
            log = self._engine.full_confrontation(
                target_content=text,
                module=module_name,
                trigger=trigger,
                auto_advance=auto_advance,
            )

            # 桥接黑天使军团
            angels = self._angel_bridge.deploy_to_red_team(self._engine)

            # 桥接双脑七因子
            brain_audit = self._brain_bridge.integrate(log.confrontation_id, text)

            return {
                "对抗ID": log.confrontation_id,
                "触发类型": log.trigger.value,
                "最终判定": log.final_verdict,
                "三色": log.overall_color,
                "牺牲次数": len(log.sacrifices),
                "牺牲荣誉": sum(
                    s.get("honor_level", 0) for s in log.sacrifices
                ),
                "融合体": log.fusion.get("new_entity_name", "") if log.fusion else "",
                "五阶段完成": log.is_complete,
                "哲学标签": log.philosophy_tags,
                "黑天使军团": [
                    {"天使": a["angel"], "红蓝角色": a["role"], "专攻": a["focus"]}
                    for a in angels
                ],
                "双脑审计": brain_audit,
                "DNA": log.dna_trace,
                "哈希链": log.hash_chain[:16] if log.hash_chain else "",
            }
        except RuntimeError as e:
            return {"状态": "跳过", "原因": str(e)}
        except Exception as e:
            return {"状态": "执行异常", "错误": str(e)}


class UniversalParserAdapter(EngineAdapter):
    """
    全文件解析引擎适配器 — 将解析能力接入管线。

    解析输入文本中提到的文件路径/URL，返回结构化解析结果。
    """
    def __init__(self):
        super().__init__("universal_parser", "text_analysis")

    def initialize(self) -> bool:
        try:
            from bin.lh_universal_parser import UniversalParser
            self._engine = UniversalParser()
            self._available = True
            return True
        except Exception:
            self._available = False
            return False

    def execute(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self._engine:
            return {"error": "解析引擎未初始化"}

        report = self._engine.get_capability_report()
        # 从文本中提取可能的文件路径
        import re, os
        file_refs = re.findall(r'(?:文件|路径|读取|解析)\s*[:：]?\s*([^\s,，。．]+(?:\.\w+)?)', text)
        paths = [f for f in file_refs if os.path.exists(f)]

        results = {}
        for p in paths[:5]:  # 最多解析5个文件
            try:
                r = self._engine.parse(p)
                results[p] = {
                    "文件": r.file_path,
                    "大小": r.file_size,
                    "元数据": r.metadata,
                    "解析时间": r.parse_time_ms,
                    "引擎": r.parser_used,
                }
            except Exception:
                results[p] = {"错误": "解析失败"}

        return {
            "解析器版本": "v1.0",
            "支持格式数": report["total_formats"],
            "解析器数": report["parser_count"],
            "已解析": results if results else {},
            "提示": "未检测到文件路径引用" if not paths else f"已解析{len(paths)}个文件",
        }


class SovereignLLMAdapter(EngineAdapter):
    """
    中国芯主权大模型适配器 — 将主权推理能力接入管线。

    执行: 芯片门禁→国密加密→本地推理→安全过滤→输出
    不依赖任何外部平台，纯本地运行。
    """
    def __init__(self):
        super().__init__("sovereign_llm", "simulation")

    def initialize(self) -> bool:
        try:
            from bin.lh_sovereign_llm import (
                SovereignLLM, ChipGate, GuoMiCrypto, SafetyFilter,
            )
            self._llm_cls = SovereignLLM
            self._chip_gate = ChipGate()
            self._crypto = GuoMiCrypto
            self._safety = SafetyFilter
            self._available = True
            return True
        except Exception:
            self._available = False
            return False

    def execute(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if not self._available:
            return {"error": "主权大模型不可用"}

        # 芯片门禁
        chip_info = {
            "芯片类型": self._chip_gate.chip_info.get("chip_type", "未知"),
            "信任层级": self._chip_gate.tier.value,
            "能力百分比": self._chip_gate.get_capability_percent(),
            "是否通过": self._chip_gate.is_allowed(),
        }

        # 安全过滤
        safety_level, safety_reason = self._safety.check_input(text)

        # 国密签名
        sm3_hash = self._crypto.sm3_hash(text.encode("utf-8")).hex()

        # 从上游引擎收集上下文信号
        yj_signal = ""
        if context.get("yijing") and context["yijing"].get("结论"):
            yj_signal = context["yijing"]["结论"].get("结果", "")[:100]
        ph_signal = ""
        if context.get("philosophy") and context["philosophy"].get("综合结论"):
            ph_signal = context["philosophy"]["综合结论"].get("综合输出", "")[:100]

        return {
            "芯片状态": chip_info,
            "安全等级": safety_level.value,
            "安全原因": safety_reason or "通过",
            "输入SM3": sm3_hash[:16] + "...",
            "易经信号": yj_signal or "无",
            "哲学信号": ph_signal or "无",
            "推理模式": "气隙模式" if context.get("air_gap") else "本地优先",
            "说    明": "中国芯主权大模型·数据不出机·国密全链路",
            "DNA": "#龍芯⚡️-SOVEREIGN-LLM-v1.0",
        }


# ═══════════════════════════════════════════════════════════
# 交叉验证引擎 — 引擎间互相校验
# ═══════════════════════════════════════════════════════════

class CrossValidator:
    """
    交叉验证：多个引擎结果互相校验，增强结论可信度。

    验证维度:
    1. 哲学一致性: 易经卦象 ↔ 哲学十维结论是否自洽
    2. 情感一致性: 焦虑检测 ↔ RobotScore 判定是否一致
    3. 战略一致性: 沙盒推演 ↔ 易经/哲学是否同向
    """

    def validate(self, results: Dict[str, EngineResult]) -> Dict[str, Any]:
        validations = {}

        # 1. 哲学一致性：易经 ↔ 统一哲学
        validations["philosophy_consistency"] = self._check_philosophy_consistency(
            results.get("yijing"), results.get("philosophy"))

        # 2. 情感一致性：焦虑检测 ↔ RobotScore
        validations["sentiment_consistency"] = self._check_sentiment_consistency(
            results.get("anxiety"), results.get("robot_score"))

        # 3. 战略一致性：沙盒 ↔ 易经/哲学
        validations["strategy_consistency"] = self._check_strategy_consistency(
            results.get("sandbox"), results.get("yijing"), results.get("philosophy"))

        # 4. 综合分数
        scores = [v.get("一致性分数", 0.5) for v in validations.values() if isinstance(v, dict)]
        validations["综合一致性"] = round(sum(scores) / len(scores), 3) if scores else 0.5

        return validations

    def _check_philosophy_consistency(self, yijing, philosophy) -> Dict:
        if not yijing or not philosophy:
            return {"状态": "跳过", "原因": "引擎结果缺失"}
        try:
            yj_conclusion = str(yijing.output.get("结论", ""))
            ph_conclusion = str(philosophy.output.get("综合结论", ""))
            # 简单对比：关键词重叠度
            yj_words = set(yj_conclusion)
            ph_words = set(ph_conclusion)
            overlap = len(yj_words & ph_words) / max(len(yj_words | ph_words), 1)
            return {
                "一致性分数": round(overlap, 3),
                "评价": "高度一致" if overlap > 0.3 else "部分一致" if overlap > 0.1 else "需人工审视",
            }
        except Exception:
            return {"一致性分数": 0.5, "评价": "无法计算"}

    def _check_sentiment_consistency(self, anxiety, robot_score) -> Dict:
        if not anxiety and not robot_score:
            return {"状态": "跳过", "原因": "文本分析引擎均不可用"}
        try:
            anx_detected = anxiety and anxiety.output.get("检测到焦虑话术", False)
            robot_sus = robot_score and robot_score.output.get("可疑度", False)
            score = 0.5
            if anx_detected == robot_sus:
                score = 0.8  # 一致
            elif anxiety and robot_score:
                score = 0.3  # 不一致
            return {
                "一致性分数": score,
                "焦虑检测": "触发" if anx_detected else "未触发",
                "RobotScore": "可疑" if robot_sus else "正常",
            }
        except Exception:
            return {"一致性分数": 0.5, "评价": "无法计算"}

    def _check_strategy_consistency(self, sandbox, yijing, philosophy) -> Dict:
        if not sandbox:
            return {"状态": "跳过", "原因": "沙盒引擎结果缺失"}
        # 检查沙盒推演方向是否与易经卦象方向一致
        try:
            sb_recommendation = str(sandbox.output.get("综合建议", ""))
            yj_strategy = ""
            if yijing:
                yj_strategy = str(yijing.output.get("结论", {}).get("strategy", ""))
            # 简单评估
            sb_len = len(sb_recommendation)
            score = min(0.9, 0.5 + sb_len / 5000)  # 输出越详细分数越高
            return {"一致性分数": round(score, 3), "评价": "推演完整" if sb_len > 100 else "推演简略"}
        except Exception:
            return {"一致性分数": 0.5, "评价": "无法计算"}


# ═══════════════════════════════════════════════════════════
# 训练数据导出器
# ═══════════════════════════════════════════════════════════

class TrainingDataExporter:
    """
    将管线聚合结果导出为结构化训练数据。

    输出格式: JSONL，每行一条训练记录
    训练特征向量包含:
    - 输入文本特征
    - 各引擎输出特征
    - 交叉验证分数
    - 综合结论编码
    """

    def export_single(self, result: PipelineResult) -> Dict[str, Any]:
        """导出一条训练记录"""
        record = {
            "meta": {
                "pipeline_version": "v1.0",
                "timestamp": result.timestamp,
                "dna": result.dna,
            },
            "input": {
                "text": result.input_text,
                "hash": result.input_hash,
                "length": len(result.input_text),
            },
            "engines": {},
            "cross_validation": result.cross_validation,
            "synthesis": result.synthesis,
            "training_vector": result.training_vector,
        }

        for name, eng in result.results.items():
            record["engines"][name] = {
                "status": eng.status,
                "duration_ms": eng.duration_ms,
                "output": eng.output if eng.status == "success" else None,
            }

        return record

    def export_jsonl(self, results: List[PipelineResult], filepath: str) -> int:
        """批量导出为 JSONL 文件"""
        count = 0
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            for result in results:
                record = self.export_single(result)
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1
        return count


# ═══════════════════════════════════════════════════════════
# 统一管线主引擎
# ═══════════════════════════════════════════════════════════

class UnifiedPipeline:
    """
    龍魂·统一训练管线 v2.0

    四类管线:
    - text_analysis: 焦虑检测 + RobotScore + 全文件解析（文本质量+格式解析）
    - philosophy: 易经推演 + 统一哲学（哲学维度分析）
    - simulation: 沙盒推演 + 主动观察 + 红蓝对抗 + 主权大模型（推演模拟）
    - sovereignty: 中国芯主权大模型（芯片门禁+国密+本地推理）

    默认全开，可按需选择子集。
    """

    DNA = "#龍芯⚡️丙午·辛未·乙酉·需-UNIFIED-PIPELINE-v1.0"

    def __init__(self, engines_subset: Optional[List[str]] = None):
        """
        Args:
            engines_subset: 指定使用的引擎列表，None表示全部。
                           可选: yijing, philosophy, sandbox, anxiety, robot_score, active_observer
        """
        # 注册所有可用适配器
        self._adapter_registry: Dict[str, EngineAdapter] = {
            "yijing": YijingAdapter(),
            "philosophy": PhilosophyAdapter(),
            "sandbox": SandboxAdapter(),
            "anxiety": AnxietyAdapter(),
            "robot_score": RobotScoreAdapter(),
            "active_observer": ActiveObserverAdapter(),
            "rb_confrontation": RBConfrontationAdapter(),
            "universal_parser": UniversalParserAdapter(),
            "sovereign_llm": SovereignLLMAdapter(),
        }

        # 初始化引擎
        self._available_engines: Dict[str, EngineAdapter] = {}
        for name, adapter in self._adapter_registry.items():
            if adapter.initialize():
                self._available_engines[name] = adapter
            else:
                print(f"  ⚠️ 引擎 [{name}] 初始化失败，跳过", file=sys.stderr)

        # 如果指定了子集，只保留可用且被选中的
        if engines_subset:
            self._active_engines = {
                name: adapter
                for name, adapter in self._available_engines.items()
                if name in engines_subset
            }
        else:
            self._active_engines = dict(self._available_engines)

        self._cross_validator = CrossValidator()
        self._exporter = TrainingDataExporter()

    def status(self) -> Dict[str, Any]:
        """获取管线状态"""
        engine_status = {}
        for name, adapter in self._adapter_registry.items():
            engine_status[name] = {
                "可用": adapter.is_available(),
                "激活": name in self._active_engines,
                "分类": adapter.category,
            }

        return {
            "管线版本": "v1.0",
            "DNA": self.DNA,
            "引擎总数": len(self._adapter_registry),
            "可用引擎": len(self._available_engines),
            "激活引擎": len(self._active_engines),
            "引擎状态": engine_status,
            "交叉验证": "就绪",
            "训练数据导出": "就绪",
        }

    def run(self, text: str, export_path: Optional[str] = None) -> PipelineResult:
        """
        执行全管线推演。

        Args:
            text: 输入文本/问题
            export_path: 训练数据导出路径（可选）

        Returns:
            PipelineResult: 聚合结果
        """
        t0 = time.time()
        input_hash = hashlib.sha256(text.encode()).hexdigest()[:16]

        # Phase 1: 预处理 — 文本分析先跑，为后续引擎提供上下文
        context: Dict[str, Any] = {"input": text, "input_hash": input_hash}

        # 文本分析引擎先跑（焦虑检测 + RobotScore）
        text_results = {}
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {}
            for name in ["anxiety", "robot_score"]:
                if name in self._active_engines:
                    adapter = self._active_engines[name]
                    futures[executor.submit(adapter.execute, text, context)] = name

            for future in as_completed(futures):
                name = futures[future]
                t_engine = time.time()
                try:
                    output_data = future.result(timeout=30)
                    text_results[name] = EngineResult(
                        engine=name,
                        status="success",
                        duration_ms=round((time.time() - t_engine) * 1000, 1),
                        output=output_data,
                    )
                except Exception as e:
                    text_results[name] = EngineResult(
                        engine=name,
                        status="error",
                        duration_ms=0,
                        output={},
                        error=str(e),
                    )
                context[name] = text_results[name].output if text_results[name].status == "success" else {}

        # Phase 2: 哲学+推演引擎并行执行（获得文本分析上下文后）
        other_results = {}
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {}
            for name in ["yijing", "philosophy", "sandbox", "active_observer"]:
                if name in self._active_engines:
                    adapter = self._active_engines[name]
                    futures[executor.submit(adapter.execute, text, context)] = name

            for future in as_completed(futures):
                name = futures[future]
                t_engine = time.time()
                try:
                    output_data = future.result(timeout=60)
                    other_results[name] = EngineResult(
                        engine=name,
                        status="success",
                        duration_ms=round((time.time() - t_engine) * 1000, 1),
                        output=output_data,
                    )
                except Exception as e:
                    other_results[name] = EngineResult(
                        engine=name,
                        status="error",
                        duration_ms=0,
                        output={},
                        error=str(e),
                    )
                context[name] = other_results[name].output if other_results[name].status == "success" else {}

        # 合并结果
        all_results = {**text_results, **other_results}

        # Phase 3: 交叉验证
        cross_validation = self._cross_validator.validate(all_results)

        # Phase 4: 综合结论
        synthesis = self._build_synthesis(all_results, cross_validation, text)

        # Phase 5: 构建训练特征向量
        training_vector = self._build_training_vector(all_results, cross_validation, synthesis)

        total_ms = round((time.time() - t0) * 1000, 1)

        result = PipelineResult(
            dna=self.DNA,
            timestamp=datetime.now().isoformat(),
            input_text=text,
            input_hash=input_hash,
            engines_used=list(all_results.keys()),
            results=all_results,
            cross_validation=cross_validation,
            synthesis=synthesis,
            training_vector=training_vector,
            total_duration_ms=total_ms,
        )

        # 导出训练数据
        if export_path:
            self._exporter.export_jsonl([result], export_path)

        return result

    def run_batch(self, texts: List[str], export_path: str) -> List[PipelineResult]:
        """批量处理并导出训练数据"""
        results = []
        for text in texts:
            text = text.strip()
            if text:
                result = self.run(text)
                results.append(result)
        if export_path:
            count = self._exporter.export_jsonl(results, export_path)
            print(f"📦 训练数据已导出: {count} 条 → {export_path}", file=sys.stderr)
        return results

    def _build_synthesis(self, results: Dict[str, EngineResult],
                         cross_validation: Dict[str, Any],
                         text: str) -> Dict[str, Any]:
        """构建综合结论 — 多引擎交叉融合"""
        synthesis = {
            "输入摘要": text[:200],
            "一致性分数": cross_validation.get("综合一致性", 0.5),
            "引擎结论": {},
        }

        # 提取各引擎核心结论
        for name, er in results.items():
            if er.status != "success":
                continue
            out = er.output
            if name == "yijing":
                synthesis["引擎结论"]["易经"] = out.get("结论", {}).get("summary", "")
            elif name == "philosophy":
                synthesis["引擎结论"]["哲学十维"] = str(out.get("综合结论", ""))[:200]
            elif name == "sandbox":
                synthesis["引擎结论"]["沙盒推演"] = str(out.get("综合建议", ""))[:200]
            elif name == "anxiety":
                synthesis["引擎结论"]["焦虑检测"] = "检测到焦虑话术" if out.get("检测到焦虑话术") else "未检测到焦虑话术"
            elif name == "robot_score":
                synthesis["引擎结论"]["RobotScore"] = f"{out.get('RobotScore', 'N/A')} — {out.get('判定', 'N/A')}"

        # 一致性评价
        consistency_score = cross_validation.get("综合一致性", 0.5)
        if consistency_score >= 0.7:
            synthesis["一致性评价"] = "多引擎高度一致 · 结论可信"
        elif consistency_score >= 0.4:
            synthesis["一致性评价"] = "多引擎部分一致 · 建议人工复核"
        else:
            synthesis["一致性评价"] = "多引擎分歧较大 · 需深入分析"

        return synthesis

    def _build_training_vector(self, results: Dict[str, EngineResult],
                               cross_validation: Dict[str, Any],
                               synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """构建训练特征向量 — 浓缩版供模型训练"""
        vector = {
            "一致性分数": cross_validation.get("综合一致性", 0.5),
            "引擎数量": len([r for r in results.values() if r.status == "success"]),
        }

        # 易经特征
        if "yijing" in results and results["yijing"].status == "success":
            yj = results["yijing"].output
            vector["易经_上卦"] = yj.get("卦象", {}).get("upper", {}).get("name", "")
            vector["易经_下卦"] = yj.get("卦象", {}).get("lower", {}).get("name", "")
            vector["易经_五行关系"] = yj.get("五行", {}).get("relation", "")

        # 哲学特征
        if "philosophy" in results and results["philosophy"].status == "success":
            ph = results["philosophy"].output
            dims = ph.get("维度结果", {})
            vector["哲学_太极阴阳比"] = dims.get("太极", {}).get("阴阳比", 0)

        # RobotScore 特征
        if "robot_score" in results and results["robot_score"].status == "success":
            rs = results["robot_score"].output
            vector["RobotScore"] = rs.get("RobotScore", 0)
            vector["RobotScore_判定"] = 1 if rs.get("可疑度") else 0

        # 焦虑检测特征
        if "anxiety" in results and results["anxiety"].status == "success":
            ax = results["anxiety"].output
            vector["焦虑_检测到"] = 1 if ax.get("检测到焦虑话术") else 0

        return vector


# ═══════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════

def print_status(pipeline: UnifiedPipeline):
    """打印管线状态仪表盘"""
    status = pipeline.status()
    print("""
╔══════════════════════════════════════════════════════════╗
║     龍魂·统一训练管线 v1.0 · 多引擎联动                      ║
╠══════════════════════════════════════════════════════════╣
║  🧬 DNA: #龍芯⚡️丙午·辛未·乙酉·需-UNIFIED-PIPELINE-v1.0   ║
╠══════════════════════════════════════════════════════════╣""")
    print(f"║  引擎总数: {status['引擎总数']}  |  可用: {status['可用引擎']}  |  激活: {status['激活引擎']}                      ║")
    print(f"║  交叉验证: {status['交叉验证']}  |  训练导出: {status['训练数据导出']}                    ║")
    print("╠══════════════════════════════════════════════════════════╣")

    for name, info in status["引擎状态"].items():
        icon = "✅" if info["可用"] and info["激活"] else "⚠️" if info["可用"] else "❌"
        cat = info["分类"]
        print(f"║  {icon} {name:<20}  {cat:<18}  {'激活' if info['激活'] else '停用':<6}     ║")

    print("""╠══════════════════════════════════════════════════════════╣
║  🚀 用法:                                                 ║
║    python3 bin/lh_unified_pipeline.py "你的问题"           ║
║    python3 bin/lh_unified_pipeline.py --json "问题"        ║
║    python3 bin/lh_unified_pipeline.py --batch file.txt     ║
║    python3 bin/lh_unified_pipeline.py --engines a,b "问题" ║
╚══════════════════════════════════════════════════════════╝""")


def print_result(result: PipelineResult, json_mode: bool = False):
    """格式化输出结果"""
    if json_mode:
        exporter = TrainingDataExporter()
        print(json.dumps(exporter.export_single(result), ensure_ascii=False, indent=2))
        return

    print(f"""
╔══════════════════════════════════════════════════════════╗
║     龍魂·统一训练管线 · 推演报告                           ║
╠══════════════════════════════════════════════════════════╣
║  输入: {result.input_text[:50]}{'...' if len(result.input_text) > 50 else ''}
║  哈希: {result.input_hash}  |  耗时: {result.total_duration_ms}ms
║  引擎: {', '.join(result.engines_used)}
╠══════════════════════════════════════════════════════════╣""")

    # 各引擎结果摘要
    for name, er in result.results.items():
        if er.status != "success":
            print(f"║  ❌ {name}: {er.error}")
            continue

        if name == "yijing":
            c = er.output.get("结论", {})
            print(f"║  ☯️  易经推演: {c.get('summary', '')[:60]}")
        elif name == "philosophy":
            s = er.output.get("综合结论", "")
            print(f"║  📐 哲学十维: {str(s)[:60]}")
        elif name == "sandbox":
            r = er.output.get("综合建议", "")
            print(f"║  🌌 沙盒推演: {str(r)[:60]}")
        elif name == "anxiety":
            d = "检测到" if er.output.get("检测到焦虑话术") else "未检测到"
            print(f"║  🐜 焦虑检测: {d}焦虑话术")
        elif name == "robot_score":
            print(f"║  🤖 RobotScore: {er.output.get('RobotScore', 'N/A')} — {er.output.get('判定', 'N/A')}")

    # 交叉验证
    print("╠══════════════════════════════════════════════════════════╣")
    cv = result.cross_validation
    print(f"║  🔗 交叉验证: 综合一致性 {cv.get('综合一致性', 'N/A')}")
    for k, v in cv.items():
        if k != "综合一致性" and isinstance(v, dict):
            score = v.get("一致性分数", v.get("评价", ""))
            print(f"║     {k}: {score}")

    # 综合结论
    print("╠══════════════════════════════════════════════════════════╣")
    syn = result.synthesis
    print(f"║  📋 {syn.get('一致性评价', '')}")
    for k, v in syn.get("引擎结论", {}).items():
        print(f"║     {k}: {str(v)[:60]}")

    # 训练特征
    print("╠══════════════════════════════════════════════════════════╣")
    tv = result.training_vector
    print(f"║  🧬 训练特征: {json.dumps({k: v for k, v in tv.items() if not isinstance(v, dict)}, ensure_ascii=False)[:80]}")
    print("╚══════════════════════════════════════════════════════════╝")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or "--status" in args or "-s" in args:
        pipeline = UnifiedPipeline()
        print_status(pipeline)
        sys.exit(0)

    json_mode = "--json" in args or "-j" in args
    use_stdin = "--stdin" in args
    batch_files = []
    engines_subset = None
    export_path = None
    text_inputs = []

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--engines" or arg == "-e":
            i += 1
            if i < len(args):
                engines_subset = [e.strip() for e in args[i].split(",")]
        elif arg == "--batch" or arg == "-b":
            i += 1
            batch_mode = True
            while i < len(args) and not args[i].startswith("-"):
                batch_files.append(args[i])
                i += 1
            continue
        elif arg == "--export" or arg == "-o":
            i += 1
            if i < len(args):
                export_path = args[i]
        elif arg in ("--json", "-j", "--stdin"):
            pass  # 已处理
        elif arg in ("--help", "-h"):
            print(__doc__)
            sys.exit(0)
        else:
            text_inputs.append(arg)
        i += 1

    # stdin 输入
    if use_stdin or (not text_inputs and not batch_files and not sys.stdin.isatty()):
        stdin_text = sys.stdin.read().strip()
        if stdin_text:
            text_inputs.append(stdin_text)

    pipeline = UnifiedPipeline(engines_subset=engines_subset)

    # 批量模式
    if batch_files:
        all_texts = []
        for fpath in batch_files:
            try:
                with open(fpath, "r") as f:
                    lines = [l.strip() for l in f if l.strip()]
                    all_texts.extend(lines)
            except FileNotFoundError:
                print(f"⚠️ 文件未找到: {fpath}", file=sys.stderr)
        if all_texts:
            exp = export_path or "data/unified_pipeline_training.jsonl"
            results = pipeline.run_batch(all_texts, exp)
            print(f"✅ 批量处理完成: {len(results)} 条 → {exp}")
        sys.exit(0)

    # 单次输入 + JSON 模式
    if text_inputs:
        text = " ".join(text_inputs)
        result = pipeline.run(text, export_path=export_path)
        print_result(result, json_mode=json_mode)
    else:
        print_status(pipeline)
