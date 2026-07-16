#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂系统·模块 G：实时监控与告警 v1.0
===============================================

功能：
  监控龍魂系统的实时状态 → 检测异常 → 触发告警 → 应急流程

监控维度：
  1. 系统健康度（五行平衡·决策品质·性能指标）
  2. 决策流水线（输入·计算·验证·路由）
  3. 异常检测（阈值突破·规则违反·疑似故障）
  4. 应急响应（自动隔离·人工介入·恢复流程）

签署：
  DNA: #龍芯⚡️2026-06-08-模块G-实时监控与告警-v1.0
  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime
import hashlib
import json


# ============ 监控常量 ============

class AlertLevel(Enum):
    """告警级别"""
    INFO = (0, "ℹ️ 信息", "记录日志·无需行动")
    WARNING = (1, "⚠️ 警告", "注意·可能有问题·观察")
    CRITICAL = (2, "🔴 严重", "立即告警·需要人工检查")
    EMERGENCY = (3, "🆘 紧急", "系统故障·自动隔离·启动应急")


class MonitoringDimension(Enum):
    """监控维度"""
    SYSTEM_HEALTH = "系统健康度"          # 五行平衡·决策品质
    PIPELINE_FLOW = "决策流水线"          # 输入·计算·验证·路由
    ANOMALY_DETECTION = "异常检测"        # 阈值·规则·疑似
    PERFORMANCE = "性能指标"               # 响应时间·吞吐量·错误率


class ThresholdType(Enum):
    """阈值类型"""
    BALANCE_INDEX = ("平衡指数", 60, 80, 100)        # 低·中·高·最高
    CONFIDENCE_SCORE = ("置信度", 0.4, 0.6, 0.8)    # 低·中·高·最高
    RESPONSE_TIME = ("响应时间(ms)", 50, 100, 200)  # 快·中·慢·超慢
    ERROR_RATE = ("错误率(%)", 0.1, 1.0, 5.0)       # 极低·低·中·高
    MEMORY_USAGE = ("内存占用(%)", 30, 60, 85)      # 低·中·高·超高


# ============ 监控数据结构 ============

@dataclass
class MetricSnapshot:
    """指标快照"""
    timestamp: datetime
    dimension: MonitoringDimension
    metric_name: str
    value: float
    unit: str
    status: str  # 🟢 正常·🟡 警告·🔴 异常


@dataclass
class AlertEvent:
    """告警事件"""
    alert_id: str
    timestamp: datetime
    level: AlertLevel
    dimension: MonitoringDimension
    trigger_condition: str
    current_value: float
    threshold: float
    message: str
    
    # 建议行动
    recommended_action: str
    severity_score: int  # 1-10


@dataclass
class SystemHealthState:
    """系统健康状态"""
    overall_score: float  # 0-100
    component_scores: Dict[str, float]  # 各组件分数
    
    # 安全评估
    is_safe: bool
    risk_level: str  # 🟢 安全·🟡 风险·🔴 危险
    last_alert: Optional[AlertEvent]
    
    # 趋势
    trend: str  # ↗️ 改善·→ 稳定·↘️ 恶化


@dataclass
class MonitoringConfig:
    """监控配置"""
    # 阈值设置
    thresholds: Dict[str, Tuple[float, float, float]] = field(default_factory=dict)
    
    # 告警策略
    alert_strategy: Dict[str, str] = field(default_factory=dict)
    
    # 检查间隔（秒）
    check_interval: int = 5
    
    # 数据保留期（小时）
    data_retention: int = 24
    
    # 应急流程
    emergency_procedures: Dict[str, str] = field(default_factory=dict)


# ============ 实时监控引擎 ============

class RealtimeMonitoringEngine:
    """实时监控与告警引擎"""
    
    def __init__(self, config: Optional[MonitoringConfig] = None):
        """初始化监控引擎"""
        self.config = config or self._default_config()
        
        # 指标存储
        self.metric_history: List[MetricSnapshot] = []
        self.alert_history: List[AlertEvent] = []
        
        # 系统状态
        self.current_state: Optional[SystemHealthState] = None
        self.last_check_time: Optional[datetime] = None
        
        # 监控统计
        self.stats = {
            "total_checks": 0,
            "total_alerts": 0,
            "critical_count": 0,
            "emergency_count": 0,
        }
    
    def _default_config(self) -> MonitoringConfig:
        """默认监控配置"""
        return MonitoringConfig(
            thresholds={
                "balance_index": (60, 80, 100),
                "confidence_score": (0.4, 0.6, 0.8),
                "response_time": (100, 200, 500),
                "error_rate": (1.0, 5.0, 10.0),
                "memory_usage": (60, 80, 95),
            },
            alert_strategy={
                "balance_index": "低于60时告警",
                "confidence_score": "低于0.4时拒绝",
                "response_time": "超过500ms时警告",
                "error_rate": "超过10%时紧急",
            },
            check_interval=5,
            data_retention=24,
            emergency_procedures={
                "high_error_rate": "自动隔离故障模块·启动备用流程",
                "low_confidence": "人工介入决策·暂停自动路由",
                "system_overload": "限流·优先级调度·自动降级",
            }
        )
    
    # ========== 指标收集 ==========
    
    def collect_metrics(self, report_data: Dict) -> List[MetricSnapshot]:
        """
        从决策报告收集监控指标
        """
        metrics = []
        timestamp = datetime.now()
        
        # 1. 平衡指数
        if "formulae" in report_data and "A_balance_index" in report_data["formulae"]:
            balance = report_data["formulae"]["A_balance_index"]
            status = "🟢" if balance >= 80 else "🟡" if balance >= 60 else "🔴"
            metrics.append(MetricSnapshot(
                timestamp=timestamp,
                dimension=MonitoringDimension.SYSTEM_HEALTH,
                metric_name="平衡指数",
                value=balance,
                unit="%",
                status=status,
            ))
        
        # 2. 置信度
        if "identification" in report_data and "final_confidence" in report_data["identification"]:
            confidence = report_data["identification"]["final_confidence"]
            status = "🟢" if confidence >= 0.8 else "🟡" if confidence >= 0.4 else "🔴"
            metrics.append(MetricSnapshot(
                timestamp=timestamp,
                dimension=MonitoringDimension.SYSTEM_HEALTH,
                metric_name="置信度",
                value=confidence,
                unit="",
                status=status,
            ))
        
        # 3. 决策品质（基于复合强度）
        if "formulae" in report_data and "D_composite_strength" in report_data["formulae"]:
            strength = report_data["formulae"]["D_composite_strength"]
            status = "🟢" if strength >= 0.8 else "🟡" if strength >= 0.6 else "🔴"
            metrics.append(MetricSnapshot(
                timestamp=timestamp,
                dimension=MonitoringDimension.SYSTEM_HEALTH,
                metric_name="决策品质",
                value=strength * 100,  # 转换为百分比
                unit="%",
                status=status,
            ))
        
        # 4. 人机一致性
        if "identification" in report_data:
            data = report_data["identification"]
            if "consistency_score" in data:
                consistency = data["consistency_score"]
                status = "🟢" if consistency >= 0.8 else "🟡" if consistency >= 0.6 else "🔴"
                metrics.append(MetricSnapshot(
                    timestamp=timestamp,
                    dimension=MonitoringDimension.PIPELINE_FLOW,
                    metric_name="人机一致性",
                    value=consistency,
                    unit="",
                    status=status,
                ))
        
        # 存储指标历史
        self.metric_history.extend(metrics)
        self.last_check_time = timestamp
        
        return metrics
    
    # ========== 异常检测 ==========
    
    def detect_anomalies(self, metrics: List[MetricSnapshot]) -> List[AlertEvent]:
        """
        检测异常·触发告警
        """
        alerts = []
        timestamp = datetime.now()
        
        for metric in metrics:
            # 根据指标名称选择阈值
            thresholds = self.config.thresholds
            
            alert = None
            
            if metric.metric_name == "平衡指数":
                low, mid, high = thresholds.get("balance_index", (60, 80, 100))
                if metric.value < 40:
                    alert = self._create_alert(
                        timestamp, AlertLevel.EMERGENCY,
                        MonitoringDimension.SYSTEM_HEALTH,
                        f"平衡指数极低：{metric.value:.1f}%",
                        metric.value, low,
                        "🆘 五行极度失衡·系统决策能力受损",
                        "自动隔离故障决策·启动应急模式·人工介入",
                        score=9
                    )
                elif metric.value < 60:
                    alert = self._create_alert(
                        timestamp, AlertLevel.CRITICAL,
                        MonitoringDimension.SYSTEM_HEALTH,
                        f"平衡指数低：{metric.value:.1f}%",
                        metric.value, low,
                        "🔴 五行不平衡·决策质量下降",
                        "增强监控·准备应急·查找根源",
                        score=7
                    )
            
            elif metric.metric_name == "置信度":
                low, mid, high = thresholds.get("confidence_score", (0.4, 0.6, 0.8))
                if metric.value < 0.3:
                    alert = self._create_alert(
                        timestamp, AlertLevel.EMERGENCY,
                        MonitoringDimension.SYSTEM_HEALTH,
                        f"置信度极低：{metric.value:.3f}",
                        metric.value, low,
                        "🆘 决策置信度极低·结果不可靠",
                        "拒绝本次决策·人工审核·重新评估",
                        score=9
                    )
                elif metric.value < 0.4:
                    alert = self._create_alert(
                        timestamp, AlertLevel.CRITICAL,
                        MonitoringDimension.SYSTEM_HEALTH,
                        f"置信度低：{metric.value:.3f}",
                        metric.value, low,
                        "🔴 决策置信度不足·需谨慎使用",
                        "标记为低置信·人工确认后使用",
                        score=7
                    )
            
            elif metric.metric_name == "决策品质":
                low, mid, high = thresholds.get("balance_index", (60, 80, 100))
                if metric.value < 40:
                    alert = self._create_alert(
                        timestamp, AlertLevel.CRITICAL,
                        MonitoringDimension.SYSTEM_HEALTH,
                        f"决策品质低：{metric.value:.1f}%",
                        metric.value, low,
                        "🔴 决策复合强度不足·风险高",
                        "加强审计·提升人工审核级别",
                        score=8
                    )
            
            elif metric.metric_name == "人机一致性":
                if metric.value < 0.5:
                    alert = self._create_alert(
                        timestamp, AlertLevel.WARNING,
                        MonitoringDimension.PIPELINE_FLOW,
                        f"人机判断差异大：{metric.value:.3f}",
                        metric.value, 0.5,
                        "⚠️ 人机判断不一致·需要人工确认",
                        "标记为需确认·暂停自动路由",
                        score=5
                    )
            
            if alert:
                alerts.append(alert)
        
        # 存储告警历史
        self.alert_history.extend(alerts)
        self.stats["total_alerts"] += len(alerts)
        self.stats["critical_count"] += sum(1 for a in alerts if a.level == AlertLevel.CRITICAL)
        self.stats["emergency_count"] += sum(1 for a in alerts if a.level == AlertLevel.EMERGENCY)
        
        return alerts
    
    def _create_alert(self, timestamp, level, dimension, trigger, current, threshold,
                      message, action, score) -> AlertEvent:
        """创建告警事件"""
        alert_id = f"ALERT-{hashlib.sha256(f'{timestamp}{trigger}'.encode()).hexdigest()[:8].upper()}"
        return AlertEvent(
            alert_id=alert_id,
            timestamp=timestamp,
            level=level,
            dimension=dimension,
            trigger_condition=trigger,
            current_value=current,
            threshold=threshold,
            message=message,
            recommended_action=action,
            severity_score=score,
        )
    
    # ========== 系统健康评估 ==========
    
    def assess_system_health(self, metrics: List[MetricSnapshot]) -> SystemHealthState:
        """
        评估系统整体健康状态
        """
        # 计算各组件分数
        component_scores = {}
        
        for metric in metrics:
            if metric.metric_name == "平衡指数":
                component_scores["平衡"] = metric.value
            elif metric.metric_name == "置信度":
                component_scores["置信"] = metric.value * 100
            elif metric.metric_name == "决策品质":
                component_scores["品质"] = metric.value
            elif metric.metric_name == "人机一致性":
                component_scores["一致性"] = metric.value * 100
        
        # 加权计算总分
        overall_score = 0
        if component_scores:
            # 平衡 30% + 置信 25% + 品质 30% + 一致性 15%
            scores = [
                component_scores.get("平衡", 60) * 0.30,
                component_scores.get("置信", 60) * 0.25,
                component_scores.get("品质", 60) * 0.30,
                component_scores.get("一致性", 60) * 0.15,
            ]
            overall_score = sum(scores)
        
        # 评估安全性和风险
        is_safe = overall_score >= 70
        if overall_score >= 80:
            risk_level = "🟢 安全"
        elif overall_score >= 60:
            risk_level = "🟡 风险"
        else:
            risk_level = "🔴 危险"
        
        # 计算趋势
        if len(self.metric_history) > 10:
            recent = self.metric_history[-5:]
            older = self.metric_history[-10:-5]
            recent_avg = sum(m.value for m in recent if isinstance(m.value, (int, float))) / len(recent)
            older_avg = sum(m.value for m in older if isinstance(m.value, (int, float))) / len(older)
            
            if recent_avg > older_avg * 1.1:
                trend = "↗️ 改善"
            elif recent_avg < older_avg * 0.9:
                trend = "↘️ 恶化"
            else:
                trend = "→ 稳定"
        else:
            trend = "→ 稳定"
        
        state = SystemHealthState(
            overall_score=round(overall_score, 2),
            component_scores=component_scores,
            is_safe=is_safe,
            risk_level=risk_level,
            last_alert=self.alert_history[-1] if self.alert_history else None,
            trend=trend,
        )
        
        self.current_state = state
        return state
    
    # ========== 应急流程 ==========
    
    def trigger_emergency_procedure(self, alert: AlertEvent) -> Dict:
        """
        触发应急流程
        """
        procedure_name = ""
        
        if alert.level == AlertLevel.EMERGENCY:
            if alert.severity_score >= 9:
                procedure_name = "high_error_rate"  # 或其他类型
            elif alert.metric_name == "置信度":
                procedure_name = "low_confidence"
            else:
                procedure_name = "system_overload"
        
        procedure = self.config.emergency_procedures.get(
            procedure_name,
            "人工评估·远程支持"
        )
        
        return {
            "alert_id": alert.alert_id,
            "procedure": procedure,
            "triggered_time": datetime.now().isoformat(),
            "status": "✅ 应急流程已启动",
            "next_steps": [
                "1. 系统隔离：停止自动决策·切换人工模式",
                "2. 人工评估：专家团队快速判断",
                "3. 恢复方案：根据根源制订恢复计划",
                "4. 验证恢复：确保系统恢复正常",
            ],
        }
    
    # ========== 报告生成 ==========
    
    def generate_monitoring_report(self) -> Dict:
        """生成完整的监控报告"""
        return {
            "report_time": datetime.now().isoformat(),
            
            "system_health": {
                "overall_score": self.current_state.overall_score if self.current_state else 0,
                "risk_level": self.current_state.risk_level if self.current_state else "未知",
                "trend": self.current_state.trend if self.current_state else "未知",
                "is_safe": self.current_state.is_safe if self.current_state else False,
            },
            
            "recent_metrics": [
                {
                    "dimension": m.dimension.value,
                    "metric": m.metric_name,
                    "value": m.value,
                    "unit": m.unit,
                    "status": m.status,
                } for m in self.metric_history[-10:]
            ],
            
            "recent_alerts": [
                {
                    "alert_id": a.alert_id,
                    "level": a.level.value[1],
                    "message": a.message,
                    "action": a.recommended_action,
                    "severity": a.severity_score,
                } for a in self.alert_history[-5:]
            ],
            
            "statistics": {
                "total_checks": self.stats["total_checks"],
                "total_alerts": self.stats["total_alerts"],
                "critical_alerts": self.stats["critical_count"],
                "emergency_alerts": self.stats["emergency_count"],
            },
            
            "DNA_signature": f"#龍芯⚡️{hashlib.sha256(str(self.metric_history).encode()).hexdigest()[:16].upper()}",
        }
    
    # ========== 完整监控流程 ==========
    
    def monitor_cycle(self, report_data: Dict) -> Dict:
        """
        执行完整的监控周期
        """
        self.stats["total_checks"] += 1
        
        # Step 1：收集指标
        metrics = self.collect_metrics(report_data)
        
        # Step 2：检测异常
        alerts = self.detect_anomalies(metrics)
        
        # Step 3：评估健康状态
        health_state = self.assess_system_health(metrics)
        
        # Step 4：如果有紧急告警·触发应急流程
        emergency_procedures = []
        if alerts:
            for alert in alerts:
                if alert.level in (AlertLevel.CRITICAL, AlertLevel.EMERGENCY):
                    procedure = self.trigger_emergency_procedure(alert)
                    emergency_procedures.append(procedure)
        
        # Step 5：生成报告
        return {
            "monitoring_cycle": self.stats["total_checks"],
            "timestamp": datetime.now().isoformat(),
            
            "metrics_collected": len(metrics),
            "metrics": [
                {
                    "dimension": m.dimension.value,
                    "name": m.metric_name,
                    "value": m.value,
                    "unit": m.unit,
                    "status": m.status,
                } for m in metrics
            ],
            
            "alerts_triggered": len(alerts),
            "alerts": [
                {
                    "id": a.alert_id,
                    "level": a.level.value[1],
                    "message": a.message,
                    "action": a.recommended_action,
                    "severity": a.severity_score,
                } for a in alerts
            ],
            
            "system_health": {
                "overall_score": health_state.overall_score,
                "risk_level": health_state.risk_level,
                "is_safe": health_state.is_safe,
                "trend": health_state.trend,
                "component_scores": health_state.component_scores,
            },
            
            "emergency_procedures": emergency_procedures,
            
            "DNA_signature": f"#龍芯⚡️{hashlib.sha256(f'{self.stats}'.encode()).hexdigest()[:16].upper()}",
        }


# ============ 测试 ============

if __name__ == "__main__":
    
    print("=" * 80)
    print("龍魂系统·模块 G：实时监控与告警 v1.0")
    print("=" * 80)
    
    # 初始化监控引擎
    monitor = RealtimeMonitoringEngine()
    
    # 模拟决策报告（来自完整系统）
    sample_report = {
        "meta": {"report_id": "FLOW-9622-20260608-TEST"},
        "formulae": {
            "A_balance_index": 75.5,
            "D_composite_strength": 0.68,
        },
        "identification": {
            "final_confidence": 0.617,
            "consistency_score": 0.85,
        },
    }
    
    # 执行监控周期
    result = monitor.monitor_cycle(sample_report)
    
    print("\n【监控周期】")
    print(f"  周期数：{result['monitoring_cycle']}")
    print(f"  时间戳：{result['timestamp']}")
    
    print("\n【收集的指标】")
    for metric in result["metrics"]:
        print(f"  {metric['name']}：{metric['value']:.2f} {metric['unit']} {metric['status']}")
    
    print("\n【系统健康状态】")
    health = result["system_health"]
    print(f"  总分：{health['overall_score']:.1f}/100")
    print(f"  风险：{health['risk_level']}")
    print(f"  安全：{'✅ 安全' if health['is_safe'] else '⚠️ 有风险'}")
    print(f"  趋势：{health['trend']}")
    
    print("\n【告警情况】")
    if result["alerts_triggered"] == 0:
        print("  ✅ 无告警·系统正常")
    else:
        for alert in result["alerts"]:
            print(f"  {alert['level']}：{alert['message']}")
            print(f"      → 建议：{alert['action']}")
    
    print("\n【应急流程】")
    if result["emergency_procedures"]:
        for procedure in result["emergency_procedures"]:
            print(f"  已启动应急流程：{procedure['procedure']}")
    else:
        print("  无需启动应急流程")
    
    print("\n" + "=" * 80)
    print(f"DNA 追溯码：#龍芯⚡️2026-06-08-模块G-实时监控与告警-v1.0")
    print("=" * 80)
