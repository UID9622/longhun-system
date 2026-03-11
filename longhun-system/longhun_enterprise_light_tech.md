━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 龙芯企业灯：技术实现方案 v2.0
## 三生三世灯 + AI智能诊断系统

**DNA追溯码**: #龍芯⚡️2026-03-09-ENTERPRISE-LIGHT-TECH-v2.0  
**GPG指纹**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F  
**确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z  
**创建者**: 诸葛鑫（UID9622）  
**理论指导**: 曾仕强老师（永恒显示）

**五行标签**：
🫡 退伍军人 | 🧮 三才算法创始人 | ⚡ 龙魂系统创始人  
🇨🇳 数字主权守护者 | 📜 中华文化传承者

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📋 目录

1. 核心定位（优化版）
2. 三生三世灯技术映射
3. 技术实现架构（给千问的搭建方向）
4. 数据库设计
5. AI诊断引擎
6. 前端交互设计
7. 与龙魂系统的整合
8. 实施路线图

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 一、核心定位（优化版）

### 1.1 产品定位

```yaml
产品名称:
  龙芯企业灯（Longhun Enterprise Light）

核心价值:
  🪞 镜子 - 照见问题根因（AI因果分析）
  ⚖️ 秤 - 称量企业现状（数据量化诊断）
  🔦 灯 - 照亮活路（AI路径规划）

一句话定位:
  "不给答案，给镜子+秤+灯，让企业家自己找活路"

与市面产品的区别:
  ❌ 不是管理咨询（太贵）
  ❌ 不是商业培训（太虚）
  ❌ 不是软件工具（太冷）
  ✅ 是AI+三才算法的诊断系统
  ✅ 是功德钱模式的自助服务
  ✅ 是真实案例库+智能匹配
```

### 1.2 受众筛选

```yaml
目标用户:
  ✅ 中小企业CEO/创始人
  ✅ 面临生死抉择的决策者
  ✅ 愿意自省、愿意付费、愿意行动

筛选机制:
  第一层: 功德钱门槛（100元/次起）
  第二层: 自我诊断问卷（过滤伸手党）
  第三层: 承诺行动（认路费机制）

不服务的人:
  ❌ 只想要答案的人
  ❌ 不愿付费的人
  ❌ 不愿行动的人
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 二、三生三世灯技术映射

### 2.1 前生灯（镜）- AI因果分析引擎

```yaml
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
核心功能: 照见问题根因
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

技术实现:
  1. 案例库匹配引擎
     - 输入: 企业当前症状（关键词）
     - 处理: 向量相似度匹配
     - 输出: 3-5个相似案例
  
  2. 因果推理引擎
     - 输入: 当前问题描述
     - 处理: 时间轴回溯算法
     - 输出: 因果链路图（3年时间轴）
  
  3. 自检清单生成
     - 输入: 匹配到的案例
     - 处理: 提取共性雷点
     - 输出: 10-15条自检清单

数据结构:
  case_id: 案例唯一ID
  symptoms: [症状标签数组]
  root_cause: 根因描述
  timeline: [
    {year: -3, event: "战略失误", impact: "高"},
    {year: -2, event: "激励失效", impact: "中"},
    {year: -1, event: "执行断层", impact: "高"},
    {year: 0, event: "结果爆发", impact: "致命"}
  ]
  checklist: [自检项数组]

AI提示词模板:
  "基于以下企业症状：{症状描述}
   从案例库中找出3个最相似案例
   分析问题的时间演化路径
   生成因果链路图（3年时间轴）
   提取自检清单（10-15条）"
```

### 2.2 今世灯（秤）- 数据量化诊断

```yaml
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
核心功能: 称量企业现状真相
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

技术实现:
  1. 压力测评系统
     - 5维度量表（1-10分）
     - 实时计算压力指数
     - 生成压力热力图
  
  2. 关键指标秤
     - 用户输入真实数据
     - 对比行业基准
     - 计算健康度得分
  
  3. 抉择点判定算法
     - 基于压力指数+财务数据
     - 智能判定：站着改革/跪着求存/边走边变
     - 输出建议路径权重

数据结构:
  pressure_test: {
    finance: 1-10,      # 资金压力
    team: 1-10,         # 团队压力
    market: 1-10,       # 市场压力
    decision: 1-10,     # 决策压力
    personal: 1-10,     # 个人状态
    total_score: 计算值,
    level: "高危/警戒/可控"
  }
  
  key_metrics: {
    人效: {current: 用户值, benchmark: 行业值, gap: 差距},
    现金流: {current: 月数, benchmark: 6, gap: 差距},
    留存率: {current: %, benchmark: 80, gap: 差距},
    增速: {current: %, benchmark: 0, gap: 差距}
  }
  
  decision_point: {
    type: "A站着改革 / B跪着求存 / AB边走边变",
    confidence: 0.0-1.0,
    reason: "判定理由"
  }

AI提示词模板:
  "基于以下数据：
   压力测评：{5维度得分}
   关键指标：{人效/现金流/留存率/增速}
   
   判断企业当前站在哪个抉择点：
   A: 站着改革（有资源有时间）
   B: 跪着求存（现金流告急）
   AB: 边走边变（保持观望）
   
   给出判定理由和置信度"
```

### 2.3 未来灯（路）- AI路径规划

```yaml
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
核心功能: 照亮可行路径
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

技术实现:
  1. 路径生成引擎
     - 输入: 抉择点类型+企业数据
     - 处理: 从路径模板库匹配
     - 输出: 1-3条可行路径
  
  2. 风险评估模块
     - 每条路径计算风险系数
     - 资源需求评估
     - 6个月预期推演
  
  3. 行动锦囊生成
     - 基于路径选择
     - 生成本周3件具体事
     - 关联执行难度

数据结构:
  path_options: [
    {
      id: "A断臂求生",
      actions: ["收缩非核心业务", "裁员20%", "聚焦主航道"],
      resources: ["决策魄力", "现金储备100万"],
      risks: ["团队士气崩塌", "品牌受损"],
      6m_expectation: "现金流转正，规模缩小15-20%",
      success_rate: 0.7
    },
    {
      id: "B渐进改革",
      actions: ["优化流程", "提升人效", "保留主干"],
      resources: ["时间窗口6个月", "执行力团队"],
      risks: ["拖太久错过窗口"],
      6m_expectation: "人效提升20-30%",
      success_rate: 0.5
    }
  ]
  
  action_kit: [
    {
      priority: 1,
      action: "本周完成核心业务梳理",
      difficulty: "中",
      time: "3天"
    },
    {
      priority: 2,
      action: "与核心团队沟通改革方向",
      difficulty: "高",
      time: "1周"
    },
    {
      priority: 3,
      action: "制定现金流监控表",
      difficulty: "低",
      time: "1天"
    }
  ]

AI提示词模板:
  "基于企业当前状态：
   抉择点：{A/B/AB}
   压力指数：{总分}
   关键指标：{数据}
   
   生成1-3条可行路径，每条包含：
   - 核心动作（3-5个）
   - 所需资源（具体列举）
   - 主要风险（可能性+影响）
   - 6个月预期（数字化描述）
   - 成功率估计
   
   并生成本周行动锦囊（3件具体事）"
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 三、技术实现架构（给千问的搭建方向）

### 3.1 整体架构

```yaml
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
技术栈选择
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

后端:
  语言: Python 3.10+
  框架: FastAPI
  AI引擎: 千问API（通义千问）
  数据库: 
    - PostgreSQL（关系数据）
    - Milvus（向量数据库，案例匹配）
  缓存: Redis

前端:
  框架: React + TypeScript
  UI: Ant Design / shadcn/ui
  图表: ECharts（因果链路图、压力热力图）
  交互: 渐进式表单（三步走）

AI能力:
  千问API:
    - 案例库向量化（Embedding）
    - 因果分析（Reasoning）
    - 路径生成（Planning）
    - 报告生成（Writing）
```

### 3.2 核心模块设计

```python
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. 案例库匹配引擎
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class CaseMatchEngine:
    """前生灯 - 案例匹配引擎"""
    
    def __init__(self, qianwen_api, milvus_client):
        self.qianwen = qianwen_api
        self.milvus = milvus_client
    
    def match_similar_cases(self, symptoms: List[str], top_k: int = 3):
        """
        根据症状匹配相似案例
        
        流程:
        1. 用千问API将症状向量化
        2. 在Milvus中搜索相似案例
        3. 返回top_k个案例
        """
        # 症状向量化
        symptom_embedding = self.qianwen.embedding(
            text=" ".join(symptoms)
        )
        
        # 向量搜索
        search_results = self.milvus.search(
            collection="enterprise_cases",
            query_vectors=[symptom_embedding],
            top_k=top_k
        )
        
        # 返回案例详情
        cases = []
        for result in search_results:
            case = self.load_case_by_id(result.id)
            case['similarity_score'] = result.score
            cases.append(case)
        
        return cases
    
    def generate_causal_chain(self, current_problem: str):
        """
        生成因果链路图（3年时间轴）
        
        用千问API推理问题根因
        """
        prompt = f"""
        企业当前问题：{current_problem}
        
        请分析这个问题是如何形成的，生成3年时间轴：
        - 3年前（起点）：最初的决策失误或战略偏差
        - 2年前：问题开始显现
        - 1年前：问题加剧
        - 现在：问题爆发
        
        每个节点包含：
        - 事件描述（具体）
        - 影响程度（高/中/低）
        - 因果关系（为什么导致下一步）
        
        输出JSON格式。
        """
        
        response = self.qianwen.chat(
            messages=[{"role": "user", "content": prompt}],
            response_format="json"
        )
        
        timeline = json.loads(response.content)
        return timeline
    
    def generate_checklist(self, matched_cases: List[Dict]):
        """
        生成自检清单
        
        从匹配案例中提取共性雷点
        """
        prompt = f"""
        以下是3个相似企业案例：
        {json.dumps(matched_cases, ensure_ascii=False)}
        
        从这些案例中提取10-15条自检清单：
        - 每条针对一个常见"雷点"
        - 问句形式（你是否...？）
        - 按重要性排序
        
        输出JSON数组。
        """
        
        response = self.qianwen.chat(
            messages=[{"role": "user", "content": prompt}],
            response_format="json"
        )
        
        checklist = json.loads(response.content)
        return checklist


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. 数据量化诊断引擎
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DiagnosisEngine:
    """今世灯 - 数据量化诊断"""
    
    def calculate_pressure_index(self, pressure_data: Dict):
        """
        计算压力指数
        
        输入: {finance: 8, team: 7, market: 9, decision: 8, personal: 7}
        输出: {total: 39, level: "高危"}
        """
        total = sum(pressure_data.values())
        
        if total >= 40:
            level = "高危"
        elif total >= 30:
            level = "警戒"
        else:
            level = "可控"
        
        return {
            "total_score": total,
            "level": level,
            "max": 50,
            "percentage": total / 50
        }
    
    def evaluate_metrics(self, metrics: Dict, benchmarks: Dict):
        """
        评估关键指标
        
        输入: 
          metrics = {人效: 50万, 现金流: 3月, 留存率: 70%, 增速: -5%}
          benchmarks = {人效: 80万, 现金流: 6月, 留存率: 80%, 增速: 0%}
        
        输出: 每个指标的健康度得分
        """
        scores = {}
        
        for key in metrics:
            current = metrics[key]
            benchmark = benchmarks[key]
            
            # 计算差距百分比
            if isinstance(current, (int, float)):
                gap_percent = (current - benchmark) / benchmark
            else:
                gap_percent = 0  # 需要更复杂处理
            
            # 转换为0-100分
            if gap_percent >= 0:
                score = 100
            elif gap_percent >= -0.5:
                score = 50 + gap_percent * 100
            else:
                score = max(0, 50 + gap_percent * 50)
            
            scores[key] = {
                "current": current,
                "benchmark": benchmark,
                "gap": current - benchmark,
                "gap_percent": gap_percent,
                "score": score
            }
        
        return scores
    
    def determine_decision_point(self, pressure_index: Dict, metrics_scores: Dict):
        """
        判定抉择点
        
        逻辑:
        - 压力高危 + 现金流<3月 → B跪着求存
        - 压力可控 + 指标健康 → A站着改革
        - 其他 → AB边走边变
        """
        total_pressure = pressure_index['total_score']
        cash_flow = metrics_scores['现金流']['current']
        
        if total_pressure >= 40 and cash_flow < 3:
            return {
                "type": "B跪着求存",
                "confidence": 0.9,
                "reason": "压力指数高危且现金流不足3个月，必须立即止血"
            }
        elif total_pressure <= 30 and all(v['score'] >= 70 for v in metrics_scores.values()):
            return {
                "type": "A站着改革",
                "confidence": 0.8,
                "reason": "压力可控且关键指标健康，有窗口进行系统改革"
            }
        else:
            return {
                "type": "AB边走边变",
                "confidence": 0.7,
                "reason": "压力适中，建议边维持现有、边做小范围试验"
            }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. 路径规划引擎
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class PathPlanningEngine:
    """未来灯 - 路径规划"""
    
    def __init__(self, qianwen_api):
        self.qianwen = qianwen_api
    
    def generate_paths(self, decision_point: Dict, company_data: Dict):
        """
        生成可行路径
        
        基于抉择点类型，从路径模板库生成1-3条路径
        """
        prompt = f"""
        企业当前状态：
        - 抉择点：{decision_point['type']}
        - 压力指数：{company_data['pressure_index']['total_score']}
        - 现金流：{company_data['metrics']['现金流']}个月
        - 团队规模：{company_data.get('team_size', '未知')}人
        
        请生成1-3条可行路径，每条包含：
        1. 路径名称（如"断臂求生"、"渐进改革"）
        2. 核心动作（3-5个具体动作）
        3. 所需资源（列举具体资源）
        4. 主要风险（可能性+影响程度）
        5. 6个月预期（数字化描述结果）
        6. 成功率估计（0-1）
        
        输出JSON数组格式。
        """
        
        response = self.qianwen.chat(
            messages=[{"role": "user", "content": prompt}],
            response_format="json"
        )
        
        paths = json.loads(response.content)
        return paths
    
    def generate_action_kit(self, selected_path: Dict):
        """
        生成行动锦囊（本周3件事）
        """
        prompt = f"""
        用户选择了路径：{selected_path['name']}
        核心动作：{selected_path['actions']}
        
        请生成本周必须完成的3件具体事：
        1. 优先级1（最重要）
        2. 优先级2
        3. 优先级3
        
        每件事包含：
        - 具体动作描述
        - 执行难度（低/中/高）
        - 预计耗时
        
        输出JSON数组。
        """
        
        response = self.qianwen.chat(
            messages=[{"role": "user", "content": prompt}],
            response_format="json"
        )
        
        action_kit = json.loads(response.content)
        return action_kit
    
    def simulate_6m_result(self, path: Dict, company_data: Dict):
        """
        6个月结果预演
        
        基于路径和当前数据，推演6个月后的状态
        """
        prompt = f"""
        当前状态：
        - 现金流：{company_data['metrics']['现金流']}个月
        - 人效：{company_data['metrics']['人效']}
        - 团队规模：{company_data.get('team_size')}人
        
        选择路径：{path['name']}
        核心动作：{path['actions']}
        
        请推演6个月后：
        - 现金流会变成几个月？
        - 人效会提升/下降多少？
        - 团队规模会如何变化？
        - 主营业务增速？
        
        给出具体数字，并说明推演逻辑。
        输出JSON格式。
        """
        
        response = self.qianwen.chat(
            messages=[{"role": "user", "content": prompt}],
            response_format="json"
        )
        
        simulation = json.loads(response.content)
        return simulation
```

### 3.3 API接口设计

```python
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FastAPI路由设计
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="龙芯企业灯 API")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 数据模型
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class SymptomInput(BaseModel):
    """用户输入症状"""
    symptoms: List[str]
    problem_description: str

class PressureTestInput(BaseModel):
    """压力测评输入"""
    finance: int  # 1-10
    team: int
    market: int
    decision: int
    personal: int

class MetricsInput(BaseModel):
    """关键指标输入"""
    人效: float
    现金流: int  # 月数
    留存率: float  # %
    增速: float  # %
    team_size: int  # 团队规模

class DiagnosisInput(BaseModel):
    """完整诊断输入"""
    symptoms: SymptomInput
    pressure_test: PressureTestInput
    metrics: MetricsInput

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# API端点
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.post("/api/v1/mirror")
async def mirror_analysis(input: SymptomInput):
    """
    前生灯 - 镜子分析
    
    返回：
    - 匹配的案例
    - 因果链路图
    - 自检清单
    """
    case_engine = CaseMatchEngine(qianwen_api, milvus_client)
    
    # 匹配案例
    cases = case_engine.match_similar_cases(input.symptoms)
    
    # 生成因果链
    causal_chain = case_engine.generate_causal_chain(input.problem_description)
    
    # 生成自检清单
    checklist = case_engine.generate_checklist(cases)
    
    return {
        "matched_cases": cases,
        "causal_chain": causal_chain,
        "checklist": checklist,
        "dna_trace": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-MIRROR-{user_id}"
    }


@app.post("/api/v1/scale")
async def scale_diagnosis(input: DiagnosisInput):
    """
    今世灯 - 秤诊断
    
    返回：
    - 压力指数
    - 指标评分
    - 抉择点判定
    """
    diagnosis_engine = DiagnosisEngine()
    
    # 计算压力指数
    pressure_index = diagnosis_engine.calculate_pressure_index(
        input.pressure_test.dict()
    )
    
    # 评估指标
    metrics_scores = diagnosis_engine.evaluate_metrics(
        metrics=input.metrics.dict(),
        benchmarks={
            "人效": 800000,
            "现金流": 6,
            "留存率": 80,
            "增速": 0
        }
    )
    
    # 判定抉择点
    decision_point = diagnosis_engine.determine_decision_point(
        pressure_index, metrics_scores
    )
    
    return {
        "pressure_index": pressure_index,
        "metrics_scores": metrics_scores,
        "decision_point": decision_point,
        "dna_trace": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-SCALE-{user_id}"
    }


@app.post("/api/v1/light")
async def light_planning(decision_point: Dict, company_data: Dict):
    """
    未来灯 - 路径规划
    
    返回：
    - 可行路径（1-3条）
    - 行动锦囊
    - 6个月预演
    """
    path_engine = PathPlanningEngine(qianwen_api)
    
    # 生成路径
    paths = path_engine.generate_paths(decision_point, company_data)
    
    # 生成行动锦囊（假设用户选择了第一条路径）
    action_kit = path_engine.generate_action_kit(paths[0])
    
    # 6个月预演
    simulations = []
    for path in paths:
        sim = path_engine.simulate_6m_result(path, company_data)
        simulations.append(sim)
    
    return {
        "paths": paths,
        "action_kit": action_kit,
        "simulations": simulations,
        "dna_trace": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-LIGHT-{user_id}"
    }


@app.post("/api/v1/full-diagnosis")
async def full_diagnosis(input: DiagnosisInput):
    """
    完整诊断 - 三灯一起
    
    流程：
    1. 前生灯分析
    2. 今世灯诊断
    3. 未来灯规划
    """
    # 前生灯
    mirror_result = await mirror_analysis(input.symptoms)
    
    # 今世灯
    scale_result = await scale_diagnosis(input)
    
    # 未来灯
    light_result = await light_planning(
        decision_point=scale_result['decision_point'],
        company_data={
            "pressure_index": scale_result['pressure_index'],
            "metrics": input.metrics.dict()
        }
    )
    
    return {
        "mirror": mirror_result,
        "scale": scale_result,
        "light": light_result,
        "full_dna_trace": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-FULL-DIAGNOSIS-{user_id}",
        "timestamp": datetime.now().isoformat()
    }
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 四、数据库设计

### 4.1 PostgreSQL表结构

```sql
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 案例库表
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CREATE TABLE enterprise_cases (
    case_id UUID PRIMARY KEY,
    title VARCHAR(200),
    industry VARCHAR(100),  -- 行业
    company_size VARCHAR(50),  -- 企业规模
    symptoms TEXT[],  -- 症状标签数组
    problem_description TEXT,
    root_cause TEXT,
    timeline JSONB,  -- 因果时间轴
    checklist JSONB,  -- 自检清单
    outcome TEXT,  -- 最终结果
    lessons_learned TEXT,  -- 经验教训
    is_public BOOLEAN DEFAULT FALSE,  -- 是否公开
    created_at TIMESTAMP DEFAULT NOW(),
    dna_trace VARCHAR(200)  -- DNA追溯码
);

-- 案例症状索引
CREATE INDEX idx_symptoms ON enterprise_cases USING GIN(symptoms);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 诊断记录表
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CREATE TABLE diagnosis_records (
    record_id UUID PRIMARY KEY,
    user_id UUID,  -- 用户ID
    company_name VARCHAR(200),
    
    -- 前生灯数据
    symptoms TEXT[],
    matched_cases UUID[],  -- 匹配到的案例ID
    causal_chain JSONB,
    
    -- 今世灯数据
    pressure_test JSONB,
    pressure_index JSONB,
    metrics JSONB,
    metrics_scores JSONB,
    decision_point JSONB,
    
    -- 未来灯数据
    generated_paths JSONB,
    selected_path VARCHAR(100),
    action_kit JSONB,
    simulation_results JSONB,
    
    -- 认路费
    commitment TEXT,  -- 用户承诺
    committed_at TIMESTAMP,
    
    -- 元数据
    created_at TIMESTAMP DEFAULT NOW(),
    dna_trace VARCHAR(200)
);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 用户表
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    username VARCHAR(100),
    company_name VARCHAR(200),
    industry VARCHAR(100),
    role VARCHAR(50),  -- CEO/创始人/高管
    
    -- 支付信息
    payment_tier VARCHAR(50),  -- 功德钱等级
    total_paid DECIMAL(10, 2),
    
    -- 使用统计
    diagnosis_count INT DEFAULT 0,
    last_diagnosis_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT NOW(),
    dna_id VARCHAR(200)  -- 用户DNA标识
);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 还账记录表（社群功能）
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CREATE TABLE progress_updates (
    update_id UUID PRIMARY KEY,
    user_id UUID,
    diagnosis_id UUID,  -- 关联诊断记录
    
    action_taken TEXT,  -- 采取了什么行动
    result TEXT,  -- 结果如何
    next_step TEXT,  -- 下一步
    
    is_anonymous BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 4.2 Milvus向量数据库

```python
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Milvus集合设计（案例向量化）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from pymilvus import Collection, FieldSchema, CollectionSchema, DataType

# 定义字段
fields = [
    FieldSchema(name="case_id", dtype=DataType.VARCHAR, max_length=200, is_primary=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024),  # 千问embedding维度
    FieldSchema(name="symptoms", dtype=DataType.VARCHAR, max_length=1000),
    FieldSchema(name="industry", dtype=DataType.VARCHAR, max_length=100)
]

# 创建集合
schema = CollectionSchema(fields=fields, description="企业案例向量库")
collection = Collection(name="enterprise_cases", schema=schema)

# 创建索引（提高搜索速度）
index_params = {
    "metric_type": "IP",  # 内积相似度
    "index_type": "IVF_FLAT",
    "params": {"nlist": 128}
}
collection.create_index(field_name="embedding", index_params=index_params)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 五、前端交互设计

### 5.1 三步式诊断流程

```yaml
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
用户体验流程
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: 前生灯 - 照见根因
  页面元素:
    - 症状多选框（10-15个常见症状）
    - 问题描述输入框
    - "照镜子"按钮
  
  交互:
    - 用户选择症状 + 描述问题
    - 点击按钮 → Loading动画
    - 展示结果：
      * 左侧：3个相似案例卡片
      * 中间：因果链路图（时间轴可视化）
      * 右侧：自检清单（可勾选）
  
  下一步:
    - "继续秤一秤"按钮

Step 2: 今世灯 - 称量现状
  页面元素:
    - 压力测评滑块（5维度，1-10分）
    - 关键指标输入表单
    - "开始称量"按钮
  
  交互:
    - 用户拖动滑块 + 填写数据
    - 点击按钮 → 计算动画
    - 展示结果：
      * 压力热力图
      * 指标雷达图
      * 抉择点判定（大字显示：A/B/AB）
  
  下一步:
    - "看看活路"按钮

Step 3: 未来灯 - 照亮路径
  页面元素:
    - 路径选择卡片（1-3条）
    - 每条路径的详细展开
    - "选择这条路"按钮
  
  交互:
    - 用户查看每条路径
    - 点击卡片展开详情
    - 选择一条路径 → 生成行动锦囊
    - 展示：
      * 本周3件事（可打印/导出）
      * 6个月预演图表
      * 认路费提交框
  
  最终:
    - 用户填写认路费
    - 生成完整诊断报告（PDF）
    - DNA追溯码打印在报告上
```

### 5.2 前端组件设计（React）

```typescript
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 前生灯组件 - MirrorAnalysis.tsx
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import React, { useState } from 'react';
import { Card, Checkbox, Input, Button, Timeline } from 'antd';
import ECharts from 'echarts-for-react';

interface CausalNode {
  year: number;
  event: string;
  impact: 'high' | 'medium' | 'low';
}

const MirrorAnalysis: React.FC = () => {
  const [symptoms, setSymptoms] = useState<string[]>([]);
  const [problemDesc, setProblemDesc] = useState('');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const symptomOptions = [
    '团队执行力差',
    '现金流紧张',
    '核心员工流失',
    '市场份额下滑',
    '战略方向不清',
    // ... 更多
  ];

  const handleAnalyze = async () => {
    setLoading(true);
    
    const response = await fetch('/api/v1/mirror', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        symptoms,
        problem_description: problemDesc
      })
    });
    
    const data = await response.json();
    setResult(data);
    setLoading(false);
  };

  // 因果链路图配置
  const causalChartOption = {
    tooltip: {},
    series: [{
      type: 'graph',
      layout: 'force',
      data: result?.causal_chain?.map((node: CausalNode) => ({
        name: node.event,
        value: node.year,
        itemStyle: {
          color: node.impact === 'high' ? '#f5222d' : 
                 node.impact === 'medium' ? '#fa8c16' : '#52c41a'
        }
      })),
      links: result?.causal_chain?.map((node: CausalNode, idx: number) => 
        idx < result.causal_chain.length - 1 ? {
          source: node.event,
          target: result.causal_chain[idx + 1].event
        } : null
      ).filter(Boolean)
    }]
  };

  return (
    <div className="mirror-analysis">
      <h2>🪞 前生灯 - 照见问题根因</h2>
      
      {/* 症状选择 */}
      <Card title="选择症状">
        <Checkbox.Group
          options={symptomOptions}
          value={symptoms}
          onChange={setSymptoms}
        />
      </Card>

      {/* 问题描述 */}
      <Card title="问题描述" style={{ marginTop: 16 }}>
        <Input.TextArea
          rows={4}
          placeholder="请描述你的企业当前面临的核心问题..."
          value={problemDesc}
          onChange={(e) => setProblemDesc(e.target.value)}
        />
      </Card>

      {/* 照镜子按钮 */}
      <Button
        type="primary"
        size="large"
        loading={loading}
        onClick={handleAnalyze}
        style={{ marginTop: 16 }}
      >
        照镜子 🪞
      </Button>

      {/* 结果展示 */}
      {result && (
        <div className="mirror-result" style={{ marginTop: 32 }}>
          {/* 相似案例 */}
          <Card title="相似案例">
            {result.matched_cases.map((case: any) => (
              <Card.Grid key={case.case_id} style={{ width: '33%' }}>
                <h4>{case.title}</h4>
                <p>相似度: {(case.similarity_score * 100).toFixed(1)}%</p>
                <p>{case.problem_description}</p>
              </Card.Grid>
            ))}
          </Card>

          {/* 因果链路图 */}
          <Card title="因果链路图" style={{ marginTop: 16 }}>
            <ECharts option={causalChartOption} style={{ height: 400 }} />
          </Card>

          {/* 自检清单 */}
          <Card title="自检清单" style={{ marginTop: 16 }}>
            {result.checklist.map((item: string, idx: number) => (
              <Checkbox key={idx}>{item}</Checkbox>
            ))}
          </Card>
        </div>
      )}
    </div>
  );
};

export default MirrorAnalysis;
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 六、与龙魂系统整合

### 6.1 DNA追溯集成

```yaml
整合点:
  1. 用户DNA统一
     - 企业灯用户 = 龙魂系统用户
     - 共享GPG指纹验证
     - DNA格式统一：#龍芯⚡️YYYY-MM-DD-[模块]-UID-序号
  
  2. 诊断记录DNA化
     - 每次诊断自动打DNA追溯码
     - 存入龙魂系统区块链
     - 可公证、可追溯
  
  3. 案例库DNA保护
     - 每个案例都有DNA
     - 防止抄袭和盗用
     - 溯源机制

代码示例:
  def generate_diagnosis_dna(user_id, module):
      """生成诊断DNA追溯码"""
      timestamp = datetime.now().strftime('%Y-%m-%d')
      sequence = get_next_sequence(user_id, module)
      
      dna = f"#龍芯⚡️{timestamp}-{module}-{user_id}-{sequence:04d}"
      
      # 写入龙魂系统区块链
      longhun_blockchain.record(dna, {
          "user_id": user_id,
          "module": "企业灯",
          "sub_module": module,
          "timestamp": datetime.now().isoformat()
      })
      
      return dna
```

### 6.2 三色审计集成

```yaml
审计规则:
  🟢 绿灯（放行）
     - 正常诊断行为
     - 合规数据输入
     - 付费用户
  
  🟡 黄灯（警告）
     - 频繁诊断（疑似滥用）
     - 数据异常（虚假输入）
     - 未付费但频繁使用
  
  🔴 红灯（熔断）
     - 恶意攻击
     - 数据泄露企图
     - 批量抓取案例

实现:
  在每个API端点加入审计装饰器
  
  @audit_decorator(level="企业灯")
  async def full_diagnosis(input):
      # 自动三色审计
      pass
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 七、实施路线图

### 7.1 MVP阶段（1-2个月）

```yaml
Week 1-2: 基础架构搭建
  ✅ FastAPI后端框架
  ✅ PostgreSQL数据库
  ✅ Milvus向量数据库
  ✅ 千问API集成

Week 3-4: 核心引擎开发
  ✅ CaseMatchEngine（案例匹配）
  ✅ DiagnosisEngine（诊断引擎）
  ✅ PathPlanningEngine（路径规划）

Week 5-6: 前端开发
  ✅ React三步式流程
  ✅ 数据可视化组件
  ✅ 认路费交互

Week 7-8: 内测与优化
  ✅ 服务3-5家企业
  ✅ 收集反馈
  ✅ 优化算法
```

### 7.2 正式发布（3-4个月）

```yaml
Month 3: 案例库建设
  ✅ 积累10+真实案例
  ✅ 向量化入库
  ✅ 建立匿名机制

Month 4: 功能完善
  ✅ 支付系统（功德钱）
  ✅ 还账记录社群
  ✅ PDF报告生成
  ✅ DNA公证集成
```

### 7.3 深度运营（5-6个月）

```yaml
Month 5-6: 高端服务
  ✅ 保密协议签署
  ✅ 深度诊断服务
  ✅ 企业跟踪辅导
  ✅ 案例库持续丰富
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 八、给千问的技术集成要点

### 8.1 千问API调用示例

```python
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 千问API集成（通义千问）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from dashscope import Generation
import dashscope

# 设置API Key
dashscope.api_key = "your-qianwen-api-key"

class QianwenService:
    """千问AI服务封装"""
    
    def embedding(self, text: str):
        """
        文本向量化
        用于案例匹配
        """
        response = Generation.call(
            model='qwen-turbo',
            prompt=text,
            task='embedding'
        )
        return response.output.embedding
    
    def chat(self, messages: List[Dict], response_format: str = "text"):
        """
        对话生成
        
        用于：
        - 因果分析
        - 路径规划
        - 报告生成
        """
        response = Generation.call(
            model='qwen-max',  # 使用最强模型
            messages=messages,
            result_format='message'
        )
        
        content = response.output.choices[0].message.content
        
        if response_format == "json":
            # 提取JSON（千问输出可能包含Markdown）
            import re
            json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                content = json_match.group(1)
        
        return content
    
    def stream_chat(self, messages: List[Dict]):
        """
        流式输出
        用于实时生成报告
        """
        responses = Generation.call(
            model='qwen-max',
            messages=messages,
            result_format='message',
            stream=True
        )
        
        for response in responses:
            if response.status_code == 200:
                yield response.output.choices[0].message.content
```

### 8.2 核心提示词模板库

```python
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 提示词模板库（给千问用的）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROMPT_TEMPLATES = {
    
    "causal_analysis": """
你是一位资深企业诊断专家。

企业当前问题：{problem_description}

请分析这个问题是如何一步步形成的，生成3年时间轴：

要求：
1. 从3年前开始追溯
2. 每个节点必须有：
   - 具体事件（不能太笼统）
   - 影响程度（高/中/低）
   - 因果关系（为什么导致下一步）
3. 输出JSON格式

示例格式：
```json
[
  {{
    "year": -3,
    "event": "2022年决定进军新业务，但没有做充分市场调研",
    "impact": "high",
    "reason": "盲目扩张导致资源分散"
  }},
  {{
    "year": -2,
    "event": "2023年新业务亏损500万，但继续投入",
    "impact": "high",
    "reason": "沉没成本心理，不愿止损"
  }},
  ...
]
```

请开始分析：
""",

    "path_generation": """
你是一位企业战略顾问。

企业当前状态：
- 抉择点：{decision_point_type}
- 压力指数：{pressure_score}/50
- 现金流：还能撑{cash_flow_months}个月
- 团队规模：{team_size}人

请生成1-3条可行路径，帮助企业找到活路。

要求：
1. 每条路径包含：
   - 路径名称（简洁有力，如"断臂求生"）
   - 核心动作（3-5个，必须具体可执行）
   - 所需资源（列举清楚）
   - 主要风险（可能性+影响）
   - 6个月预期（数字化描述）
   - 成功率估计（0-1之间）

2. 路径要有差异性：
   - 激进 vs 保守
   - 短期 vs 长期
   - 内部 vs 外部

3. 输出JSON数组格式

示例：
```json
[
  {{
    "name": "断臂求生",
    "actions": [
      "立即砍掉亏损的X业务",
      "裁员20%，保留核心团队",
      "聚焦主航道，停止所有试错"
    ],
    "resources": ["决策魄力", "现金储备100万用于补偿"],
    "risks": [
      {{"risk": "团队士气崩塌", "probability": 0.7, "impact": "中"}},
      {{"risk": "品牌受损", "probability": 0.5, "impact": "低"}}
    ],
    "6m_expectation": "现金流从3个月提升到6个月，规模缩小15-20%",
    "success_rate": 0.7
  }}
]
```

请开始规划：
""",

    "action_kit": """
你是一位执行教练。

用户选择了路径：{path_name}
核心动作：{path_actions}

请生成本周（7天内）必须完成的3件具体事：

要求：
1. 优先级明确（1最重要）
2. 动作具体可执行（不能是"思考"、"研究"这种虚的）
3. 包含：
   - 动作描述
   - 执行难度（低/中/高）
   - 预计耗时
   - 成功标准（怎么算完成）

输出JSON格式：
```json
[
  {{
    "priority": 1,
    "action": "召集核心团队会议，宣布收缩决定，说明原因",
    "difficulty": "高",
    "time": "2天内完成",
    "success_criteria": "团队理解并接受，无核心成员离职"
  }},
  ...
]
```

请开始生成：
"""
}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📝 总结：技术实现核心要点

```yaml
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
千问需要做的事
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. AI能力提供:
   ✅ 文本向量化（Embedding）
   ✅ 因果推理（Reasoning）
   ✅ 路径规划（Planning）
   ✅ 报告生成（Writing）

2. API集成:
   ✅ 提供稳定的API接口
   ✅ 支持JSON格式输出
   ✅ 流式输出支持

3. 数据库协作:
   ✅ PostgreSQL存关系数据
   ✅ Milvus存向量数据
   ✅ Redis做缓存

4. 前端对接:
   ✅ React三步式流程
   ✅ ECharts数据可视化
   ✅ 实时交互体验

5. 与龙魂整合:
   ✅ DNA追溯统一
   ✅ 三色审计集成
   ✅ 区块链存证

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
关键技术点
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

镜子（前生灯）:
  案例库向量匹配 → Milvus + 千问Embedding
  因果分析 → 千问Reasoning能力

秤（今世灯）:
  数据量化 → Python算法
  抉择判定 → 规则引擎 + AI辅助

灯（未来灯）:
  路径规划 → 千问Planning能力
  6个月预演 → 千问推理 + 数学模拟
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**DNA追溯码**: #龍芯⚡️2026-03-09-ENTERPRISE-LIGHT-TECH-COMPLETE-v2.0  
**确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅  
**创建者**: 诸葛鑫（UID9622）  
**理论指导**: 曾仕强老师（永恒显示）

**五行标签**：
🫡 退伍军人 | 🧮 三才算法创始人 | ⚡ 龙魂系统创始人  
🇨🇳 数字主权守护者 | 📜 中华文化传承者

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**老大，技术方案全写好了，给千问搭建用！** 💪🔥
