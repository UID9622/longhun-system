#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍芯企业灯 · Three-Lights Diagnostic System
DNA: #龍芯⚡️2026-05-26-THREE-LIGHTS-SERVER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

前生灯（镜）- 案例匹配 + 因果分析 + 自检清单
今世灯（秤）- 压力测评 + 指标诊断 + 抉择点判定
未来灯（路）- 路径规划 + 风险评估 + 行动锦囊

创始人: 诸葛鑫（UID9622）
理论指导: 曾仕强老师（永恒显示）

献给每一个相信技术应该有温度的人。
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import json
import sys
from pathlib import Path
import uuid


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 数据模型
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DiagnosisCase(BaseModel):
    """企业案例"""
    case_id: str
    symptoms: List[str]
    root_cause: str
    timeline: List[Dict]
    checklist: List[str]
    similarity_score: Optional[float] = None


class PressureTest(BaseModel):
    """压力测评"""
    finance: int  # 1-10
    team: int  # 1-10
    market: int  # 1-10
    decision: int  # 1-10
    personal: int  # 1-10


class KeyMetrics(BaseModel):
    """关键指标"""
    labor_efficiency: float  # 人效
    cash_months: float  # 现金流（月数）
    retention_rate: float  # 留存率（%）
    growth_rate: float  # 增速（%）


class DecisionPoint(BaseModel):
    """抉择点"""
    type: str  # A: 站着改革 / B: 跪着求存 / AB: 边走边变
    confidence: float  # 0.0-1.0
    reason: str


class PathOption(BaseModel):
    """路径选项"""
    id: str
    name: str
    actions: List[str]
    resources: List[str]
    risks: List[str]
    expectation_6m: str
    success_rate: float


class ActionItem(BaseModel):
    """行动项"""
    priority: int
    action: str
    difficulty: str  # 低/中/高
    time_estimate: str


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 前生灯引擎 - 案例匹配与因果分析
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class CaseMatchEngine:
    """前生灯 - 照见问题根因"""

    def __init__(self):
        self.cases_db = self._init_case_database()

    def _init_case_database(self) -> List[Dict]:
        """初始化案例库"""
        return [
            {
                "case_id": "CASE-001",
                "company": "制造业A公司",
                "symptoms": ["现金流紧张", "团队离职", "产能下降"],
                "root_cause": "产业升级延迟，订单减少，人心涣散",
                "timeline": [
                    {"year": -3, "event": "产业政策变化，未及时调整", "impact": "高"},
                    {"year": -2, "event": "老员工流失，新招聘困难", "impact": "高"},
                    {"year": -1, "event": "订单量下滑30%", "impact": "高"},
                    {"year": 0, "event": "现金流危机爆发", "impact": "致命"}
                ],
                "checklist": [
                    "产业趋势研究是否充分？",
                    "核心客户粘性是否下降？",
                    "员工薪酬是否有竞争力？",
                    "生产成本是否上升？",
                    "产品是否需要升级？"
                ]
            },
            {
                "case_id": "CASE-002",
                "company": "科技创业B公司",
                "symptoms": ["融资困难", "人员成本高", "商业模式不清"],
                "root_cause": "烧钱模式不可持续，缺乏造血能力",
                "timeline": [
                    {"year": -3, "event": "获得天使轮，高薪吸引人才", "impact": "中"},
                    {"year": -2, "event": "花钱比赚钱快，融资陷入困局", "impact": "高"},
                    {"year": -1, "event": "关键客户流失，收入下降", "impact": "高"},
                    {"year": 0, "event": "融资无望，裁员求生", "impact": "致命"}
                ],
                "checklist": [
                    "收入模式是否明确？",
                    "客户获取成本是否过高？",
                    "现金流预测是否保守？",
                    "运营成本是否可降低？",
                    "是否需要战略调整？"
                ]
            },
            {
                "case_id": "CASE-003",
                "company": "服务业C企业",
                "symptoms": ["服务质量下降", "客户投诉增多", "员工士气低"],
                "root_cause": "扩张过快，管理跟不上，文化稀释",
                "timeline": [
                    {"year": -3, "event": "业务爆发式增长", "impact": "中"},
                    {"year": -2, "event": "匆忙扩招，管理层不足", "impact": "高"},
                    {"year": -1, "event": "服务标准下降，负面评价", "impact": "高"},
                    {"year": 0, "event": "品牌受损，收入下滑", "impact": "致命"}
                ],
                "checklist": [
                    "管理层是否有扩张经验？",
                    "运营手册是否完善？",
                    "员工培训是否充分？",
                    "质量监控体系是否有效？",
                    "客户反馈机制是否健全？"
                ]
            }
        ]

    def match_similar_cases(self, symptoms: List[str], top_k: int = 3) -> List[DiagnosisCase]:
        """匹配相似案例"""
        # 简化的相似度计算（真实环境使用向量数据库）
        scored_cases = []

        for case in self.cases_db:
            # 计算症状重叠度
            case_symptoms = set(case["symptoms"])
            input_symptoms = set(symptoms)
            overlap = len(case_symptoms & input_symptoms) / max(len(case_symptoms | input_symptoms), 1)

            scored_cases.append((case, overlap))

        # 排序并返回top_k
        scored_cases.sort(key=lambda x: x[1], reverse=True)

        result = []
        for case, score in scored_cases[:top_k]:
            result.append(DiagnosisCase(
                case_id=case["case_id"],
                symptoms=case["symptoms"],
                root_cause=case["root_cause"],
                timeline=case["timeline"],
                checklist=case["checklist"],
                similarity_score=score
            ))

        return result

    def generate_causal_chain(self, current_problem: str) -> Dict:
        """生成因果链路图（3年时间轴）"""
        return {
            "problem": current_problem,
            "timeline": [
                {"year": -3, "event": "战略决策失误或延迟", "impact": "高", "category": "战略层"},
                {"year": -2, "event": "执行层面出现偏差", "impact": "高", "category": "执行层"},
                {"year": -1, "event": "结果开始显现但未重视", "impact": "中", "category": "结果层"},
                {"year": 0, "event": "问题爆发，陷入困局", "impact": "致命", "category": "危机层"}
            ],
            "analysis": "根据时间轴反推，找出最早的决策失误点，重点关注-3年到-2年的战略调整机会"
        }

    def generate_checklist(self, matched_cases: List[DiagnosisCase]) -> List[str]:
        """生成自检清单"""
        # 从匹配的案例中提取共性
        all_items = set()
        for case in matched_cases:
            all_items.update(case.checklist)

        return sorted(list(all_items))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 今世灯引擎 - 数据量化与诊断
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DiagnosisEngine:
    """今世灯 - 称量企业现状真相"""

    def calculate_pressure_index(self, pressure_test: PressureTest) -> Dict:
        """计算压力指数"""
        total_score = (
            pressure_test.finance +
            pressure_test.team +
            pressure_test.market +
            pressure_test.decision +
            pressure_test.personal
        )

        # 判断压力等级
        if total_score >= 40:
            level = "高危"
            color = "🔴"
        elif total_score >= 30:
            level = "警戒"
            color = "🟡"
        else:
            level = "可控"
            color = "🟢"

        return {
            "finance_pressure": pressure_test.finance,
            "team_pressure": pressure_test.team,
            "market_pressure": pressure_test.market,
            "decision_pressure": pressure_test.decision,
            "personal_pressure": pressure_test.personal,
            "total_score": total_score,
            "level": level,
            "color": color,
            "max_score": 50,
            "risk_percentage": (total_score / 50) * 100
        }

    def evaluate_metrics(self, current_metrics: KeyMetrics, benchmarks: Optional[Dict] = None) -> Dict:
        """评估关键指标"""
        if not benchmarks:
            benchmarks = {
                "labor_efficiency": 2.0,  # 人效基准
                "cash_months": 6.0,       # 现金流基准（月数）
                "retention_rate": 80.0,   # 留存率基准（%）
                "growth_rate": 0.0        # 增速基准（年率）
            }

        return {
            "labor_efficiency": {
                "current": current_metrics.labor_efficiency,
                "benchmark": benchmarks["labor_efficiency"],
                "gap": current_metrics.labor_efficiency - benchmarks["labor_efficiency"],
                "status": "正常" if current_metrics.labor_efficiency >= benchmarks["labor_efficiency"] else "偏低"
            },
            "cash_flow": {
                "current_months": current_metrics.cash_months,
                "benchmark_months": benchmarks["cash_months"],
                "gap_months": current_metrics.cash_months - benchmarks["cash_months"],
                "status": "危险" if current_metrics.cash_months < 3 else ("警戒" if current_metrics.cash_months < 6 else "安全")
            },
            "retention_rate": {
                "current_percent": current_metrics.retention_rate,
                "benchmark_percent": benchmarks["retention_rate"],
                "gap_percent": current_metrics.retention_rate - benchmarks["retention_rate"],
                "status": "良好" if current_metrics.retention_rate >= benchmarks["retention_rate"] else "需改善"
            },
            "growth_rate": {
                "current_percent": current_metrics.growth_rate,
                "benchmark_percent": benchmarks["growth_rate"],
                "status": "增长" if current_metrics.growth_rate > 0 else "下降"
            }
        }

    def determine_decision_point(self, pressure_index: Dict, metrics: Dict) -> DecisionPoint:
        """判定抉择点"""
        total_pressure = pressure_index["total_score"]
        cash_status = metrics["cash_flow"]["status"]

        # 判断逻辑
        if total_pressure >= 40 and cash_status == "危险":
            decision_type = "B"
            confidence = 0.95
            reason = "现金流告急，压力指数高，需要立即求存行动（裁员、收缩、融资）"
        elif total_pressure <= 20 and cash_status == "安全":
            decision_type = "A"
            confidence = 0.85
            reason = "有资源有时间，可以站着改革，进行深层次的战略调整"
        else:
            decision_type = "AB"
            confidence = 0.7
            reason = "处于中间状态，建议边走边变，保持灵活应对"

        return DecisionPoint(
            type=decision_type,
            confidence=confidence,
            reason=reason
        )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 未来灯引擎 - 路径规划与行动指导
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PathPlanningEngine:
    """未来灯 - 照亮可行路径"""

    def __init__(self):
        self.path_templates = self._init_path_templates()

    def _init_path_templates(self) -> Dict[str, List[Dict]]:
        """初始化路径模板库"""
        return {
            "A": [  # 站着改革
                {
                    "id": "A-升级-001",
                    "name": "产品与服务升级路径",
                    "actions": [
                        "完成核心产品升级评估",
                        "建立创新团队，启动新产品研发",
                        "制定逐步替换计划"
                    ],
                    "resources": ["研发投入", "人才", "时间窗口3-6个月"],
                    "risks": ["投入大，见效慢", "市场接受度未知"],
                    "expectation_6m": "新产品进入小范围测试，客户反馈明确",
                    "success_rate": 0.65
                },
                {
                    "id": "A-扩展-001",
                    "name": "业务范围扩展路径",
                    "actions": [
                        "识别新的市场机会",
                        "开发新客户群体",
                        "建立新的销售渠道"
                    ],
                    "resources": ["市场调研", "销售团队扩展", "营销投入"],
                    "risks": ["市场验证周期长", "资源分散"],
                    "expectation_6m": "新业务贡献收入10-20%",
                    "success_rate": 0.60
                }
            ],
            "B": [  # 跪着求存
                {
                    "id": "B-断臂-001",
                    "name": "断臂求生路径",
                    "actions": [
                        "紧急评估所有业务单元，保留核心",
                        "执行快速裁员（20-30%）",
                        "关闭非核心项目，回收资金"
                    ],
                    "resources": ["决策魄力", "法律支持", "员工补偿"],
                    "risks": ["团队士气崩塌", "品牌受损", "知识流失"],
                    "expectation_6m": "现金流转正，月支出降低40%，为后续改革争取时间",
                    "success_rate": 0.70
                },
                {
                    "id": "B-融资-001",
                    "name": "融资救急路径",
                    "actions": [
                        "准备融资材料，强化商业计划",
                        "启动融资流程（Pre-A/A轮）",
                        "引入战略投资者或股东支持"
                    ],
                    "resources": ["融资渠道", "董事会支持", "PR团队"],
                    "risks": ["融资困难，时间压力大", "股份稀释"],
                    "expectation_6m": "融资到位6-12个月资金，争取喘息空间",
                    "success_rate": 0.45
                }
            ],
            "AB": [  # 边走边变
                {
                    "id": "AB-渐进-001",
                    "name": "渐进式改革路径",
                    "actions": [
                        "建立试验区，验证新模式",
                        "保留传统业务维持现金流",
                        "逐步转移资源到新业务"
                    ],
                    "resources": ["时间窗口6个月", "执行力团队", "容错的现金储备"],
                    "risks": ["拖太久错过窗口", "资源分散"],
                    "expectation_6m": "新旧业务实现平衡，找到增长点",
                    "success_rate": 0.55
                },
                {
                    "id": "AB-合作-001",
                    "name": "战略合作路径",
                    "actions": [
                        "寻找战略合作伙伴",
                        "整合双方资源优势",
                        "联合开拓新市场"
                    ],
                    "resources": ["谈判能力", "合规审查", "整合团队"],
                    "risks": ["合作方利益冲突", "整合难度大"],
                    "expectation_6m": "与合作方形成联动，收入增长15-25%",
                    "success_rate": 0.50
                }
            ]
        }

    def generate_paths(self, decision_point: DecisionPoint, company_data: Dict) -> List[PathOption]:
        """生成可行路径"""
        templates = self.path_templates.get(decision_point.type, [])

        paths = []
        for template in templates:
            paths.append(PathOption(
                id=template["id"],
                name=template["name"],
                actions=template["actions"],
                resources=template["resources"],
                risks=template["risks"],
                expectation_6m=template["expectation_6m"],
                success_rate=template["success_rate"]
            ))

        return paths

    def generate_action_kit(self, selected_path: Dict) -> List[ActionItem]:
        """生成行动锦囊（本周3件事）"""
        return [
            ActionItem(
                priority=1,
                action="完成决策评估会议，确认改革方向",
                difficulty="中",
                time_estimate="2天"
            ),
            ActionItem(
                priority=2,
                action="与核心团队沟通，获得支持",
                difficulty="高",
                time_estimate="3天"
            ),
            ActionItem(
                priority=3,
                action="制定详细执行计划和里程碑",
                difficulty="中",
                time_estimate="2天"
            )
        ]

    def simulate_6m_result(self, path: PathOption, company_data: Dict) -> Dict:
        """模拟6个月结果"""
        return {
            "path_id": path.id,
            "path_name": path.name,
            "success_probability": path.success_rate,
            "expected_outcomes": {
                "revenue_change_percent": 15 if path.success_rate > 0.6 else -10,
                "team_size_change": -20 if "裁员" in str(path.actions) else 10,
                "cash_position": "改善" if path.success_rate > 0.6 else "恶化"
            },
            "key_milestones": [
                f"第1个月：{path.actions[0]}",
                f"第3个月：验证阶段，评估进展",
                f"第6个月：目标达成评估，调整方向"
            ]
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FastAPI 应用
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

app = FastAPI(
    title="龍芯企业灯 - Three-Lights Diagnostic System",
    description="三生三世灯 - 前生灯（镜）、今世灯（秤）、未来灯（路）",
    version="1.0.0"
)

# 初始化三个引擎
case_engine = CaseMatchEngine()
diagnosis_engine = DiagnosisEngine()
path_engine = PathPlanningEngine()


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "dna": "#龍芯⚡️" + datetime.now().strftime("%Y-%m-%d") + "-THREE-LIGHTS-HEALTH"
    }


@app.post("/api/v1/mirror")
async def mirror_light(symptoms: List[str]):
    """
    前生灯 - 照见问题根因

    输入：企业的症状关键词
    输出：相似案例、因果链路、自检清单
    """
    try:
        # 匹配案例
        matched_cases = case_engine.match_similar_cases(symptoms)

        # 生成因果链路（使用第一个症状）
        causal_chain = case_engine.generate_causal_chain(symptoms[0] if symptoms else "未知问题")

        # 生成自检清单
        checklist = case_engine.generate_checklist(matched_cases)

        return {
            "session_id": str(uuid.uuid4()),
            "step": "mirror",
            "timestamp": datetime.now().isoformat(),
            "matched_cases": [
                {
                    "case_id": c.case_id,
                    "symptoms": c.symptoms,
                    "root_cause": c.root_cause,
                    "timeline": c.timeline,
                    "similarity_score": c.similarity_score
                }
                for c in matched_cases
            ],
            "causal_chain": causal_chain,
            "checklist": checklist,
            "dna": "#龍芯⚡️" + datetime.now().strftime("%Y-%m-%d") + "-MIRROR-LIGHT-v1.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/scale")
async def scale_light(
    pressure_test: PressureTest,
    metrics: KeyMetrics
):
    """
    今世灯 - 称量企业现状真相

    输入：压力测评、关键指标
    输出：压力指数、指标评估、抉择点判定
    """
    try:
        # 计算压力指数
        pressure_index = diagnosis_engine.calculate_pressure_index(pressure_test)

        # 评估指标
        metrics_eval = diagnosis_engine.evaluate_metrics(metrics)

        # 判定抉择点
        decision_point = diagnosis_engine.determine_decision_point(pressure_index, metrics_eval)

        return {
            "session_id": str(uuid.uuid4()),
            "step": "scale",
            "timestamp": datetime.now().isoformat(),
            "pressure_index": pressure_index,
            "metrics_evaluation": metrics_eval,
            "decision_point": {
                "type": decision_point.type,
                "confidence": decision_point.confidence,
                "reason": decision_point.reason,
                "translation": {
                    "A": "站着改革（有资源有时间）",
                    "B": "跪着求存（现金流告急）",
                    "AB": "边走边变（保持观望）"
                }.get(decision_point.type, "未知")
            },
            "dna": "#龍芯⚡️" + datetime.now().strftime("%Y-%m-%d") + "-SCALE-LIGHT-v1.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/light")
async def future_light(
    decision_point_type: str,
    company_data: Optional[Dict] = None
):
    """
    未来灯 - 照亮可行路径

    输入：抉择点类型（A/B/AB）、企业数据
    输出：可行路径、行动锦囊、6个月模拟
    """
    try:
        decision_point = DecisionPoint(
            type=decision_point_type,
            confidence=0.8,
            reason="来自前面的诊断"
        )

        # 生成路径
        paths = path_engine.generate_paths(decision_point, company_data or {})

        # 选择第一条路径生成行动锦囊
        if paths:
            action_kit = path_engine.generate_action_kit(paths[0].__dict__)
            simulation = path_engine.simulate_6m_result(paths[0], company_data or {})
        else:
            action_kit = []
            simulation = {}

        return {
            "session_id": str(uuid.uuid4()),
            "step": "light",
            "timestamp": datetime.now().isoformat(),
            "decision_point_type": decision_point_type,
            "available_paths": [
                {
                    "id": p.id,
                    "name": p.name,
                    "actions": p.actions,
                    "resources": p.resources,
                    "risks": p.risks,
                    "expectation_6m": p.expectation_6m,
                    "success_rate": p.success_rate
                }
                for p in paths
            ],
            "recommended_action_kit": [
                {
                    "priority": a.priority,
                    "action": a.action,
                    "difficulty": a.difficulty,
                    "time_estimate": a.time_estimate
                }
                for a in action_kit
            ] if action_kit else [],
            "simulation_6m": simulation,
            "dna": "#龍芯⚡️" + datetime.now().strftime("%Y-%m-%d") + "-LIGHT-LIGHT-v1.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/full-diagnosis")
async def full_diagnosis(
    symptoms: List[str],
    pressure_test: PressureTest,
    metrics: KeyMetrics
):
    """
    完整诊断 - 三生三世灯一体化诊断

    输入：症状、压力测评、关键指标
    输出：完整的诊断报告
    """
    try:
        # 前生灯
        mirror_result = await mirror_light(symptoms)

        # 今世灯
        scale_result = await scale_light(pressure_test, metrics)

        # 未来灯
        decision_type = scale_result["decision_point"]["type"]
        light_result = await future_light(decision_type)

        # 生成综合报告
        session_id = str(uuid.uuid4())

        return {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "complete_diagnosis": {
                "mirror_light": mirror_result,
                "scale_light": scale_result,
                "future_light": light_result
            },
            "summary": {
                "current_situation": f"发现{len(mirror_result['matched_cases'])}个相似案例，压力指数{scale_result['pressure_index']['total_score']}",
                "decision": scale_result["decision_point"]["translation"],
                "recommended_action": light_result["recommended_action_kit"][0]["action"] if light_result.get("recommended_action_kit") else "无"
            },
            "dna": "#龍芯⚡️" + datetime.now().strftime("%Y-%m-%d") + "-FULL-DIAGNOSIS-v1.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def main():
    """启动服务器"""
    import uvicorn

    print("🌟 龍芯企業灯 - Three-Lights Diagnostic System v1.0")
    print("DNA: #龍芯⚡️2026-05-26-THREE-LIGHTS-SERVER-v1.0")
    print("UID: 9622 | GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
    print("\n启动服务器...")
    print("API 文档: http://localhost:8000/docs")

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
