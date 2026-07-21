#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂系统·模块 F：自动化补益建议 v1.0
===============================================

功能：
  自动分析五行失衡 → 生成补益方案（颜色·方位·数字·行动）

补益策略：
  1. 缺失五行 → 紫急补（🔴 级别）
  2. 最弱五行 → 建议补（🟡 级别）
  3. 最强五行 → 疏导（🟢 级别）
  4. 相克过强 → 制约方案

签署：
  DNA: #龍芯⚡️2026-06-08-模块F-自动化补益建议-v1.0
  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ✅
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum
import hashlib


# ============ 补益方案常量 ============

class WuXingSupply(Enum):
    """五行补益方案"""
    JIN = {
        "名称": "金",
        "颜色": ["白", "金", "银"],
        "方位": ["西", "西北", "西南"],
        "数字": [4, 6, 7, 9],
        "时间": ["秋季", "酉时", "申时"],
        "食物": ["鸡蛋", "牛奶", "豆制品", "白色食物"],
        "行动": ["整理·规划", "边界设定", "规则制订", "决策执行"],
        "习惯": ["准时守约", "说到做到", "清洁整齐", "言行一致"],
    }
    
    MU = {
        "名称": "木",
        "颜色": ["绿", "青", "蓝绿"],
        "方位": ["东", "东北", "东南"],
        "数字": [1, 2, 3, 8],
        "时间": ["春季", "卯时", "寅时"],
        "食物": ["青菜", "水果", "豆芽", "绿色食物"],
        "行动": ["学习·进修", "计划制订", "新项目启动", "人际连接"],
        "习惯": ["坚持练习", "定期阅读", "建立目标", "积极行动"],
    }
    
    SHUI = {
        "名称": "水",
        "颜色": ["黑", "深蓝", "深灰"],
        "方位": ["北", "西北", "北东"],
        "数字": [6, 8, 9, 1],
        "时间": ["冬季", "亥时", "子时"],
        "食物": ["黑色食物", "海产", "坚果", "蜂蜜"],
        "行动": ["记录整理", "知识积累", "反思总结", "保存资料"],
        "习惯": ["写日记", "保存档案", "静坐冥想", "深度思考"],
    }
    
    HUO = {
        "名称": "火",
        "颜色": ["红", "橙", "紫"],
        "方位": ["南", "东南", "西南"],
        "数字": [2, 3, 7, 9],
        "时间": ["夏季", "午时", "巳时"],
        "食物": ["红色食物", "温热食物", "辛辣食物"],
        "行动": ["表达分享", "创意发挥", "公开发言", "内容创作"],
        "习惯": ["定期分享", "社交互动", "创意练习", "文化活动"],
    }
    
    TU = {
        "名称": "土",
        "颜色": ["黄", "棕", "米色"],
        "方位": ["中宫", "中心", "转轴"],
        "数字": [5, 10, 15, 20],
        "时间": ["季节交替时", "午后", "黄昏"],
        "食物": ["黄色食物", "根茎类", "谷物", "蜂蜜"],
        "行动": ["承载责任", "收纳整理", "社区服务", "身心调理"],
        "习惯": ["定期打扫", "照顾他人", "瑜伽冥想", "接地练习"],
    }


# ============ 补益方案数据结构 ============

@dataclass
class SupplyPlan:
    """单个补益方案"""
    wuxing: str              # 五行
    level: str               # 级别（🔴紫急补·🟡建议补·🟢疏导）
    reason: str              # 原因说明
    
    # 补益方案
    colors: List[str]        # 推荐颜色
    directions: List[str]    # 推荐方位
    numbers: List[int]       # 推荐数字
    times: List[str]         # 推荐时间
    foods: List[str]         # 推荐食物
    actions: List[str]       # 推荐行动
    habits: List[str]        # 推荐习惯
    
    # 评估
    urgency: int             # 紧急程度 (1-10)
    effectiveness: float     # 预期效果 (0-1)
    timeline: str            # 补益时间表


@dataclass
class ComprehensiveSupply:
    """综合补益方案"""
    primary_plan: SupplyPlan       # 主要补益方案
    secondary_plans: List[SupplyPlan]  # 次要补益方案
    
    # 整体评估
    total_urgency: int             # 总体紧急程度
    estimated_recovery_time: str   # 预期恢复时间
    success_rate: float            # 预期成功率
    
    # 执行计划
    weekly_plan: Dict[str, List[str]]   # 周计划
    monthly_focus: str                   # 月度重点
    
    # 监控指标
    monitoring_metrics: List[str]   # 监控指标
    checkpoint_schedule: List[str]   # 检查点


# ============ 自动化补益引擎 ============

class AutoSupplyEngine:
    """自动化补益建议引擎"""
    
    def __init__(self):
        """初始化"""
        self.wuxing_supply = {
            "金": WuXingSupply.JIN.value,
            "木": WuXingSupply.MU.value,
            "水": WuXingSupply.SHUI.value,
            "火": WuXingSupply.HUO.value,
            "土": WuXingSupply.TU.value,
        }
        
        # 补益优先级：缺失 > 最弱 > 最强 > 相克
        self.supply_priority = ["缺失", "最弱", "最强", "相克"]
    
    # ========== 诊断五行状态 ==========
    
    def diagnose_wuxing(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """
        诊断五行状态：
        1. 找出缺失的五行（得分 < 10）
        2. 找出最弱的五行（得分最低但不缺失）
        3. 找出最强的五行（得分最高）
        4. 分析相克关系
        """
        diagnosis = {
            "缺失": [],
            "最弱": None,
            "最强": None,
            "相克": [],
            "详细分析": "",
        }
        
        # 找缺失
        for wuxing, score in scores.items():
            if score < 10:
                diagnosis["缺失"].append(wuxing)
        
        # 找最弱和最强
        if scores:
            valid_scores = {k: v for k, v in scores.items() if v >= 10}
            if valid_scores:
                diagnosis["最弱"] = min(valid_scores, key=valid_scores.get)
                diagnosis["最强"] = max(valid_scores, key=valid_scores.get)
        
        # 分析相克（简化版）
        # 金克木·木克土·土克水·水克火·火克金
        克制关系 = {
            "金": "木", "木": "土", "土": "水", "水": "火", "火": "金"
        }
        
        for wuxing, target in 克制关系.items():
            if scores.get(wuxing, 0) > 50 and scores.get(target, 0) < 30:
                diagnosis["相克"].append(f"{wuxing}克制{target}·需防范")
        
        # 详细分析
        analysis_parts = []
        
        if diagnosis["缺失"]:
            analysis_parts.append(f"🔴 缺失五行：{','.join(diagnosis['缺失'])}·需紫急补益")
        
        if diagnosis["最弱"]:
            weakest_score = scores.get(diagnosis["最弱"], 0)
            analysis_parts.append(f"🟡 最弱五行：{diagnosis['最弱']}（{weakest_score:.0f}分）·需加强")
        
        if diagnosis["最强"]:
            strongest_score = scores.get(diagnosis["最强"], 0)
            analysis_parts.append(f"🟢 最强五行：{diagnosis['最强']}（{strongest_score:.0f}分）·可疏导")
        
        diagnosis["详细分析"] = "\n".join(analysis_parts)
        
        return diagnosis
    
    # ========== 生成补益方案 ==========
    
    def generate_supply_plan(self, wuxing: str, level: str, 
                             scores: Dict[str, float]) -> SupplyPlan:
        """
        为某个五行生成补益方案
        """
        supply_data = self.wuxing_supply.get(wuxing, {})
        
        # 确定原因
        score = scores.get(wuxing, 0)
        if score < 10:
            reason = f"{wuxing}缺失（得分 {score:.0f}）·需要紫急补益"
            urgency = 10
        elif level == "🟡 最弱":
            reason = f"{wuxing}是最弱五行·需要加强"
            urgency = 7
        else:
            reason = f"{wuxing}过强·需要适当疏导"
            urgency = 5
        
        # 预期效果
        if urgency == 10:
            effectiveness = 0.9  # 高
        elif urgency == 7:
            effectiveness = 0.7  # 中
        else:
            effectiveness = 0.5  # 低
        
        # 时间表
        if urgency == 10:
            timeline = "立即开始·每日执行·7-14 天见效"
        elif urgency == 7:
            timeline = "本周开始·每周加强·21 天见效"
        else:
            timeline = "本月开始·每月调整·30-60 天见效"
        
        return SupplyPlan(
            wuxing=wuxing,
            level=level,
            reason=reason,
            colors=supply_data.get("颜色", []),
            directions=supply_data.get("方位", []),
            numbers=supply_data.get("数字", []),
            times=supply_data.get("时间", []),
            foods=supply_data.get("食物", []),
            actions=supply_data.get("行动", []),
            habits=supply_data.get("习惯", []),
            urgency=urgency,
            effectiveness=effectiveness,
            timeline=timeline,
        )
    
    # ========== 综合补益方案 ==========
    
    def generate_comprehensive_plan(self, scores: Dict[str, float]) -> ComprehensiveSupply:
        """
        根据诊断结果生成综合补益方案
        """
        # Step 1：诊断
        diagnosis = self.diagnose_wuxing(scores)
        
        # Step 2：优先排序
        # 缺失 > 最弱 > 最强 > 相克
        
        plans = []
        
        # 缺失五行：最高优先级
        for wuxing in diagnosis["缺失"]:
            plan = self.generate_supply_plan(wuxing, "🔴 紫急补", scores)
            plans.append(plan)
        
        # 最弱五行：第二优先级
        if diagnosis["最弱"]:
            plan = self.generate_supply_plan(diagnosis["最弱"], "🟡 最弱", scores)
            plans.append(plan)
        
        # 最强五行：第三优先级（疏导）
        if diagnosis["最强"]:
            plan = self.generate_supply_plan(diagnosis["最强"], "🟢 疏导", scores)
            plans.append(plan)
        
        # 相克关系：第四优先级
        for relationship in diagnosis["相克"]:
            # 简化：对相克的被克制者补益
            pass
        
        # Step 3：确定主要和次要方案
        primary_plan = plans[0] if plans else self.generate_supply_plan("土", "🟢 疏导", scores)
        secondary_plans = plans[1:] if len(plans) > 1 else []
        
        # Step 4：计算总体紧急程度和恢复时间
        total_urgency = sum(p.urgency for p in plans) // len(plans) if plans else 5
        
        if total_urgency >= 9:
            recovery_time = "1-2 周"
        elif total_urgency >= 7:
            recovery_time = "2-4 周"
        else:
            recovery_time = "4-8 周"
        
        # 预期成功率
        success_rate = sum(p.effectiveness for p in plans) / len(plans) if plans else 0.5
        
        # Step 5：生成周计划
        weekly_plan = self._generate_weekly_plan(primary_plan)
        
        # Step 6：月度重点
        monthly_focus = self._generate_monthly_focus(plans)
        
        # Step 7：监控指标
        monitoring_metrics = [
            "每日五行评分",
            "平衡指数变化",
            "相克强度变化",
            "身心状态反馈",
        ]
        
        checkpoint_schedule = [
            "第 3 天：初期反应检查",
            "第 7 天：周期检查·调整方案",
            "第 14 天：中期效果评估",
            "第 30 天：月度总结·长期计划",
        ]
        
        return ComprehensiveSupply(
            primary_plan=primary_plan,
            secondary_plans=secondary_plans,
            total_urgency=total_urgency,
            estimated_recovery_time=recovery_time,
            success_rate=round(success_rate, 3),
            weekly_plan=weekly_plan,
            monthly_focus=monthly_focus,
            monitoring_metrics=monitoring_metrics,
            checkpoint_schedule=checkpoint_schedule,
        )
    
    def _generate_weekly_plan(self, plan: SupplyPlan) -> Dict[str, List[str]]:
        """生成周计划"""
        return {
            "周一": [f"【{plan.wuxing}】开始补益", f"颜色提示：{plan.colors[0]}", f"食物补充：{plan.foods[0]}"],
            "周二": [f"【{plan.wuxing}】强化习惯", f"行动练习：{plan.actions[0]}", "记录反应"],
            "周三": [f"【{plan.wuxing}】维持节奏", f"时间调整：{plan.times[0]}", "检查进度"],
            "周四": [f"【{plan.wuxing}】深化体验", f"方位能量：{plan.directions[0]}", "调整计划"],
            "周五": [f"【{plan.wuxing}】复习巩固", f"习惯强化：{plan.habits[0]}", "准备周末"],
            "周六": [f"【{plan.wuxing}】社交分享", f"与人交流", "获取反馈"],
            "周日": ["周末反思", "总结成果", "计划下周"],
        }
    
    def _generate_monthly_focus(self, plans: List[SupplyPlan]) -> str:
        """生成月度重点"""
        if plans:
            primary = plans[0]
            return f"本月重点：加强【{primary.wuxing}】五行·{primary.reason}·预期 {primary.timeline}"
        return "保持平衡·稳步推进"
    
    # ========== 输出报告 ==========
    
    def generate_report(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """生成完整补益报告"""
        
        # 执行诊断和生成方案
        diagnosis = self.diagnose_wuxing(scores)
        comprehensive = self.generate_comprehensive_plan(scores)
        
        return {
            "诊断结果": diagnosis,
            "主要补益方案": {
                "五行": comprehensive.primary_plan.wuxing,
                "级别": comprehensive.primary_plan.level,
                "原因": comprehensive.primary_plan.reason,
                "推荐颜色": comprehensive.primary_plan.colors,
                "推荐方位": comprehensive.primary_plan.directions,
                "推荐数字": comprehensive.primary_plan.numbers,
                "推荐行动": comprehensive.primary_plan.actions,
                "推荐习惯": comprehensive.primary_plan.habits,
                "紧急程度": f"{comprehensive.primary_plan.urgency}/10",
                "预期效果": f"{comprehensive.primary_plan.effectiveness*100:.0f}%",
                "时间表": comprehensive.primary_plan.timeline,
            },
            "次要补益方案": [
                {
                    "五行": p.wuxing,
                    "级别": p.level,
                    "推荐行动": p.actions,
                } for p in comprehensive.secondary_plans
            ],
            "整体评估": {
                "总体紧急程度": f"{comprehensive.total_urgency}/10",
                "预期恢复时间": comprehensive.estimated_recovery_time,
                "预期成功率": f"{comprehensive.success_rate*100:.1f}%",
            },
            "执行计划": {
                "周计划": comprehensive.weekly_plan,
                "月度重点": comprehensive.monthly_focus,
            },
            "监控": {
                "监控指标": comprehensive.monitoring_metrics,
                "检查点": comprehensive.checkpoint_schedule,
            },
            "DNA签署": f"#龍芯⚡️{hashlib.sha256(str(scores).encode()).hexdigest()[:16].upper()}",
        }


# ============ 测试 ============

if __name__ == "__main__":
    
    print("=" * 80)
    print("龍魂系统·模块 F：自动化补益建议 v1.0")
    print("=" * 80)
    
    engine = AutoSupplyEngine()
    
    # 测试数据（不平衡的五行）
    scores = {
        "金": 45,
        "木": 35,
        "水": 55,
        "火": 40,
        "土": 50,
    }
    
    # 生成报告
    report = engine.generate_report(scores)
    
    print("\n【诊断结果】")
    print(f"  {report['诊断结果']['详细分析']}")
    
    print("\n【主要补益方案】")
    for key, value in report["主要补益方案"].items():
        if isinstance(value, list):
            print(f"  {key}：{', '.join(str(v) for v in value)}")
        else:
            print(f"  {key}：{value}")
    
    print("\n【次要补益方案】")
    for plan in report["次要补益方案"]:
        print(f"  - 【{plan['五行']}】{plan['级别']}")
        print(f"    推荐行动：{', '.join(plan['推荐行动'])}")
    
    print("\n【整体评估】")
    for key, value in report["整体评估"].items():
        print(f"  {key}：{value}")
    
    print("\n【周计划】")
    for day, actions in report["执行计划"]["周计划"].items():
        print(f"  {day}：{' → '.join(actions)}")
    
    print("\n【监控】")
    print(f"  监控指标：{', '.join(report['监控']['监控指标'])}")
    print(f"  检查点：")
    for checkpoint in report["监控"]["检查点"]:
        print(f"    - {checkpoint}")
    
    print("\n" + "=" * 80)
    print(f"DNA 追溯码：#龍芯⚡️2026-06-08-模块F-自动化补益建议-v1.0")
    print("=" * 80)
