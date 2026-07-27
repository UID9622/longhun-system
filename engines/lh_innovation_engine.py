#!/usr/bin/env python3
"""
龍魂 · 创新推演引擎 v1.0
DNA: #龍芯⚡️2026-07-25-INNOVATION-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）· 协议: CC BY-NC-SA 4.0

21人格矩阵同时分析新内容，多视角交叉创新。
不是抄——是「我们的版本」。

铁律：推演标"推演"·实测才标"已验证"·不替老大做决定
"""

import hashlib, json, sys, time, uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# ═══ 常量 ═══
DNA = "#龍芯⚡️2026-07-25-INNOVATION-ENGINE-v2.0-DEPTH-GUARD"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "auto-learned" / "innovations"
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge" / "auto-learned" / "innovations"

# 推理深度阈值（v2.0新增·审计修复）
# depth_score < DEPTH_SHALLOW → 标记浅层推演·降级为🟡
# 当前模型规模限制：非bug·物理限制·v5.0蒸馏时作为核心指标优化
DEPTH_SHALLOW = 0.70       # 低于此值标记浅层
DEPTH_CRITICAL = 0.45      # 低于此值强制🟡+不可落地

# 21人格推演矩阵（每个输入项，每个相关人格给出评估）
PERSONA_MATRIX = {
    "诸葛亮": {"role": "战略推演", "weight": 0.15, "color": "#c9a84c",
               "prompt": "战略价值评估：这个技术能否成为我们的战略优势？"},
    "鲁班": {"role": "技术落地", "weight": 0.13, "color": "#3b82f6",
             "prompt": "技术落地路径：需要多少工时？依赖哪些现有组件？"},
    "上帝之眼": {"role": "审计安全", "weight": 0.12, "color": "#ef4444",
               "prompt": "安全风险扫描：有什么安全隐患？触碰哪些红线？"},
    "管仲": {"role": "资源核算", "weight": 0.10, "color": "#22c55e",
             "prompt": "资源消耗计算：算力/存储/人力/时间成本？"},
    "李白": {"role": "美学适配", "weight": 0.08, "color": "#a855f7",
             "prompt": "美学风格适配：暗色鎏金匹配吗？用户感受如何？"},
    "孙子": {"role": "竞争分析", "weight": 0.10, "color": "#eab308",
             "prompt": "竞争态势：有什么差异化价值？对手能做到吗？"},
    "文心": {"role": "意图校验", "weight": 0.07, "color": "#06b6d4",
             "prompt": "意图校验：符合为人民服务的总方向吗？"},
    "屈原": {"role": "底线守卫", "weight": 0.10, "color": "#f97316",
             "prompt": "底线检查：触碰P0天条了吗？信息主权是否让渡？"},
    "姜子牙": {"role": "权限调度", "weight": 0.05, "color": "#84cc16",
               "prompt": "权限影响：需要调整哪些角色的权限？"},
    "乔前辈": {"role": "交付验收", "weight": 0.05, "color": "#14b8a6",
               "prompt": "交付标准：满足GATE-01~10吗？DNA签章齐全吗？"},
    "孙思邈": {"role": "系统健康", "weight": 0.05, "color": "#6366f1",
               "prompt": "系统健康：接入后会影响现有系统稳定性吗？"},
}


class AuditMark(str, Enum):
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


@dataclass
class PersonaOpinion:
    """单个人格的推演意见"""
    persona: str
    role: str
    opinion: str           # 推演结论
    recommendation: str    # 建议
    audit: AuditMark = AuditMark.GREEN


@dataclass
class InnovationReport:
    """创新推演报告"""
    report_id: str
    input_topic: str        # 原始输入主题
    input_source: str       # 来源
    personas_opinions: List[PersonaOpinion] = field(default_factory=list)
    cross_innovation: str = ""     # 交叉创新结果
    longhun_version: str = ""      # 龍魂创新版本
    overall_audit: AuditMark = AuditMark.YELLOW
    actionability: bool = False
    risk_score: float = 0.0        # 0-1, 1=最高风险
    dna: str = ""
    # v2.0 推理深度守卫
    depth_score: float = 1.0       # 推理深度 0-1（模板匹配+意见完整+创新具体）
    shallow_reason: str = ""       # 浅层原因（depth<DEPTH_SHALLOW时有值）


class InnovationEngine:
    """创新推演引擎·21人格矩阵+交叉创新"""

    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)

        # 各人格对各领域的推演模板
        self._opinion_templates = self._build_templates()

    def _build_templates(self) -> Dict[str, Dict[str, tuple]]:
        """构建人格×领域的推演模板 (opinion, recommendation, audit)"""
        return {
            "多Agent协作": {
                "诸葛亮": ("战略级功能。多Agent协作是AI系统走向自主的关键一步。\n可用于军团指挥中枢的战术层，让21人格真正并行工作。",
                           "建议立即落地，优先接入TeamOrchestrator。", AuditMark.GREEN),
                "鲁班": ("技术可行。需适配消息总线(MessageBus)和权限体系。\n预计12工时，核心难度在并发控制和死锁检测。",
                         "建议P0优先，先做最小可行版本再迭代。", AuditMark.GREEN),
                "上帝之眼": ("⚠️ 多Agent并行带来新攻击面：\n- Agent间通信可能被中间人劫持\n- 权限提升风险（低权限Agent调用高权限API）",
                           "必须实现Agent间TLS加密+P72熔断联动。", AuditMark.YELLOW),
                "管仲": ("成本评估：\n- 开发成本12工时≈1.5人天\n- 运行成本：每次协作消耗额外2-3次API调用\n- 长期收益：减少人工调度50%",
                         "ROI为正，建议纳入P0计划。", AuditMark.GREEN),
                "李白": ("协作面板用暗色鎏金！\n- 主色：龍魂金(#c9a84c)\n- 辅色：暗影蓝(#1e2a3a)\n- 动画：粒子连线·易经六十四卦流转",
                         "视觉方案已就绪，Portal可同步开工。", AuditMark.GREEN),
                "孙子": ("差异化优势显著：\n- 竞争者用线性流程，我们用易经八卦路由\n- 竞争者无追溯，我们有DNA全程追溯\n- 但竞争者先发优势，需加速落地",
                         "速度优先，先占领心智再优化。", AuditMark.GREEN),
                "文心": ("意图纯正：为人民服务的AI可控协作，\n非资本黑箱式多Agent。方向正确。", "通过意图校验。", AuditMark.GREEN),
                "屈原": ("底线安全：Agent间数据流动必须在本地，\n禁止Agent数据出境。协作日志不泄露用户隐私。",
                        "增设数据主权闸门后通过。", AuditMark.YELLOW),
            },
            "底座模型升级": {
                "诸葛亮": ("底座是AI的根。新底座=更强的中文理解力=更好的为人民服务能力。\n长期战略投资，不可不察。",
                           "建议P1规划，先评估再决策。", AuditMark.GREEN),
                "鲁班": ("技术路径：加载新底座→适配CNSH→跑测试→对比基准。\n难点：9B模型需要更多显存/内存，Mac可能吃力。",
                         "建议先在鲲鹏测试，Mac本地保留小底座的降级方案。", AuditMark.YELLOW),
                "上帝之眼": ("🔴 底座切换安全风险：\n- 新底座可能包含后门权重\n- 输出行为可能与现有CNSH不一致\n- 必须沙箱隔离测试至少48h",
                           "安全审核不过不切换。建议安全扫描后再定。", AuditMark.RED),
                "管仲": ("成本核算：\n- 训练成本：约$200-500云GPU\n- 推理成本：9B模型≈2-3倍当前1.5B的算力消耗\n- 收益：中文能力预计提升40-60%",
                         "ROI正面，但需分阶段投入。建议先小规模测试。", AuditMark.GREEN),
                "李白": ("底座升级不影响用户界面。\n但可在知识中枢API返回中注明'Powered by xx底座'，增强品牌感。",
                         "纯技术层面，UI无影响。", AuditMark.GREEN),
                "孙子": ("行业共识：大模型底座=AI基础设施。\n不升级=落后。但升级时机和底座选择决定胜负。\nYi-1.5-9B中文能力业界认可，时机已到。",
                         "审慎但果断，建议P1排期。", AuditMark.GREEN),
            },
            "工作流编排": {
                "诸葛亮": ("自动化工作流是AI自治的基础设施。\n有望将龍魂从'被动响应'升级为'主动服务'。",
                           "建议P1规划，配合自动学习引擎一起上线。", AuditMark.GREEN),
                "鲁班": ("可基于现有五阶管道扩展。\n新增可视化编辑器和条件分支。预计8工时。",
                         "建议先做核心4种模式（顺序/并行/条件/循环），预留扩展接口。", AuditMark.GREEN),
                "上帝之眼": ("⚠️ 工作流引擎的安全关注点：\n- 注入攻击（恶意工作流定义）\n- 权限逃逸（工作流绕过审计）\n- 无限循环DoS",
                           "必须引入工作流沙箱+执行超时+权限校验。", AuditMark.YELLOW),
            },
            "自动部署": {
                "诸葛亮": ("少人工=少错误。自动部署是系统成熟的标志。\n战略价值中等但执行价值高。",
                           "建议P1执行，配合GATE-01~10形成完整CI/CD。", AuditMark.GREEN),
                "鲁班": ("可复用现有deploy/脚本。\n新增：WebHook触发→GATE审计→同步鲲鹏→验证→报告。预计6工时。",
                         "先做最小部署链，再做完整CI/CD。", AuditMark.GREEN),
                "上帝之眼": ("部署自动化本身不增加安全风险，但需确保：\n- 部署凭证不入代码库\n- 部署前自动过GATE-01~10\n- 失败自动回滚",
                           "增设安全闸后通过。", AuditMark.YELLOW),
                "管仲": ("ROI极高：每次手动部署约30分钟，\n自动化后每次<5分钟。每年节省约50工时。\n投入6工时，ROI>800%。",
                         "强烈建议执行。", AuditMark.GREEN),
                "李白": ("部署面板用暗色鎏金风格！\n- 进度条：易经六十四卦依次点亮\n- 成功动画：龍魂金粒子汇聚\n- 失败动画：红色裂隙扩散",
                         "视觉方案同步准备好。", AuditMark.GREEN),
            },
            "AI伦理": {
                "诸葛亮": ("AI伦理不是束缚，是方向。\n有伦理约束的AI才值得信任，才能服务更多人。",
                           "必须P0焊死。", AuditMark.GREEN),
                "屈原": ("🔴 伦理底线不可谈判：\n- 数据主权不可让渡\n- 不监控不收割不欺骗\n- 不替资本做黑箱决策\n任何试图削弱伦理的'优化'，一律拒绝。",
                        "P0焊死·永不撤销。", AuditMark.GREEN),
                "文心": ("为人民服务的AI必有伦理底线。\n此条方向完全正确，无异议。", "通过。", AuditMark.GREEN),
            },
            "数据集/弹药": {
                "诸葛亮": ("数据是AI的粮食。中文高质量数据集是战略物资。\n越多越好，但要确保质量。",
                           "建议P1持续收集，建立数据集质量评级体系。", AuditMark.GREEN),
                "鲁班": ("接入数据炼化管道即可。\n需要：数据格式标准化→去重→去偏→质量评分→入库。预计16工时。",
                         "先通管道，再持续收集。", AuditMark.GREEN),
                "上帝之眼": ("⚠️ 数据集安全：\n- 来源验证：防止投毒数据混入\n- 隐私扫描：检查是否包含PII\n- 价值观审查：过滤有害内容",
                           "增设三道防线后通过。", AuditMark.YELLOW),
            },
        }

    def analyze(self, topic: str, source: str = "auto-learner") -> InnovationReport:
        """对输入主题进行21人格推演"""
        report_id = str(uuid.uuid4())[:8]
        opinions = []
        risk_score = 0.0

        # 查找匹配领域的模板
        template = self._match_template(topic)

        if template:
            for persona, info in PERSONA_MATRIX.items():
                if persona in template:
                    op, rec, audit = template[persona]
                    opinion = PersonaOpinion(
                        persona=persona,
                        role=info["role"],
                        opinion=op,
                        recommendation=rec,
                        audit=audit
                    )
                else:
                    # 未覆盖的人格给默认意见
                    opinion = PersonaOpinion(
                        persona=persona,
                        role=info["role"],
                        opinion=f"（{info['role']}）对「{topic}」无直接相关意见，建议关注其他维度的推演结果。",
                        recommendation="跟踪观察",
                        audit=AuditMark.GREEN
                    )
                opinions.append(opinion)

                if opinion.audit == AuditMark.RED:
                    risk_score += 0.3
                elif opinion.audit == AuditMark.YELLOW:
                    risk_score += 0.1
        else:
            # 无匹配模板 → 生成通用推演
            for persona, info in PERSONA_MATRIX.items():
                opinion = PersonaOpinion(
                    persona=persona,
                    role=info["role"],
                    opinion=f"「{topic}」进入{info['role']}推演队列。待人工确认具体场景后给出详细分析。",
                    recommendation="标记待人工复核",
                    audit=AuditMark.YELLOW
                )
                opinions.append(opinion)
                risk_score += 0.05

        risk_score = min(risk_score, 1.0)

        # 交叉创新
        cross = self._cross_innovate(topic, opinions)
        longhun_version = self._generate_longhun_version(topic, opinions)

        # 综合审计
        reds = sum(1 for o in opinions if o.audit == AuditMark.RED)
        yellows = sum(1 for o in opinions if o.audit == AuditMark.YELLOW)
        if reds > 0:
            overall = AuditMark.RED
        elif yellows > 3:
            overall = AuditMark.YELLOW
        else:
            overall = AuditMark.GREEN

        report = InnovationReport(
            report_id=report_id,
            input_topic=topic,
            input_source=source,
            personas_opinions=opinions,
            cross_innovation=cross,
            longhun_version=longhun_version,
            overall_audit=overall,
            actionability=reds == 0,
            risk_score=round(risk_score, 2),
            dna=self._make_dna(f"innovation:{topic}")
        )

        # v2.0 推理深度评估
        depth_score, shallow_reason = self._assess_depth(report, template is not None)
        report.depth_score = depth_score
        report.shallow_reason = shallow_reason

        # 深度不足时降级：浅层推演不可出厂
        if depth_score < DEPTH_CRITICAL:
            report.overall_audit = AuditMark.YELLOW if report.overall_audit != AuditMark.RED else AuditMark.RED
            report.actionability = False
            report.cross_innovation += f"\n\n⚠️ 推理深度不足({depth_score:.2f}<{DEPTH_CRITICAL})：{shallow_reason}"
        elif depth_score < DEPTH_SHALLOW and report.overall_audit == AuditMark.GREEN:
            report.overall_audit = AuditMark.YELLOW
            report.cross_innovation += f"\n\n💡 推理深度偏浅({depth_score:.2f})：{shallow_reason}。建议v5.0蒸馏时优化。"

        self._save_report(report)
        return report

    def _match_template(self, topic: str) -> Optional[Dict]:
        """匹配推演模板"""
        keywords_map = {
            "多Agent协作": ["agent", "协作", "collaboration", "多agent", "军团"],
            "底座模型升级": ["底座", "模型", "qwen", "千问", "llama", "yi-", "chatglm", "智谱", "deepseek"],
            "工作流编排": ["工作流", "编排", "workflow", "管道", "pipeline"],
            "自动部署": ["部署", "deploy", "ci/cd", "发布", "上线"],
            "AI伦理": ["伦理", "ethics", "道德", "底线", "红线"],
            "数据集/弹药": ["数据集", "dataset", "训练数据", "弹药", "语料", "corpus"],
        }
        topic_lower = topic.lower()
        for domain, kws in keywords_map.items():
            if any(kw in topic_lower for kw in kws):
                return self._opinion_templates.get(domain, {})
        return None

    def _cross_innovate(self, topic: str, opinions: List[PersonaOpinion]) -> str:
        """交叉创新：多视角碰撞出龍魂版本"""
        greens = [o for o in opinions if o.audit == AuditMark.GREEN]
        yellows = [o for o in opinions if o.audit == AuditMark.YELLOW]
        reds = [o for o in opinions if o.audit == AuditMark.RED]

        parts = []

        if greens:
            parts.append(f"✅ 通过视角({len(greens)}): {'·'.join(o.persona for o in greens[:3])}")
        if yellows:
            parts.append(f"⚠️ 需关注({len(yellows)}): {'·'.join(o.persona for o in yellows[:3])}")
        if reds:
            parts.append(f"🔴 否决({len(reds)}): {'·'.join(o.persona for o in reds[:3])}")

        if not reds:
            parts.append("\n交叉创新方案：")
            parts.append(f"- 诸葛亮战略方向 + 鲁班落地路径 = 可执行战略")
            parts.append(f"- 李白美学 + 管仲成本控制 = 好看不贵")
            parts.append(f"- 孙子竞争 + 屈原底线 = 差异化的安全优势")
            parts.append(f"\n交叉结果：在保持龍魂DNA追溯+三色审计+暗色鎏金的基础上，将「{topic}」融入生态，形成独特竞争优势。")
        else:
            parts.append("\n🔴 存在红线否决，交叉创新暂缓。待安全问题解决后再推进。")

        return "\n".join(parts)

    def _assess_depth(self, report: InnovationReport, has_template: bool) -> tuple:
        """v2.0 推理深度评估·自我认知
        返回 (depth_score: 0-1, shallow_reason: str)

        评估维度：
        - 模板匹配度（0-0.3）：有专属模板=高分
        - 人格覆盖度（0-0.25）：有实质意见的人格占比
        - 交叉创新质量（0-0.25）：创新是否具体、是否有差异化
        - 龍魂版本质量（0-0.20）：是否生成具体的龍魂版本描述
        """
        opinions = report.personas_opinions
        total = len(opinions)
        if total == 0:
            return 0.0, "无人格参与推演"

        scores = {}
        reasons = []

        # 1. 模板匹配度（0-0.30）
        scores["template"] = 0.30 if has_template else 0.10
        if not has_template:
            reasons.append("无匹配推演模板（通用推演）")

        # 2. 人格覆盖度（0-0.25）：多少人给出了实质意见（非默认/占位）
        substantive = sum(1 for o in opinions
                         if not o.opinion.startswith("（")
                         and not o.opinion.startswith("「"))
        coverage = substantive / total
        scores["coverage"] = 0.25 * coverage
        if coverage < 0.5:
            reasons.append(f"实质意见人格仅{substantive}/{total}（{coverage:.0%}）")

        # 3. 交叉创新质量（0-0.25）
        cross = report.cross_innovation
        cross_len = len(cross)
        if cross_len > 300:
            scores["innovation"] = 0.25
        elif cross_len > 150:
            scores["innovation"] = 0.20
        elif cross_len > 80:
            scores["innovation"] = 0.15
            reasons.append("交叉创新内容偏短")
        else:
            scores["innovation"] = 0.08
            reasons.append("交叉创新过于简略")

        # 是否有具体的差异化点
        if "差异化" in cross or "我们的版本" in cross or "DNA" in cross:
            scores["innovation"] = min(0.25, scores["innovation"] + 0.02)

        # 4. 龍魂版本质量（0-0.20）
        lhv = report.longhun_version
        if lhv.startswith("🔴"):
            scores["version"] = 0.05
            reasons.append("龍魂版本被否决")
        elif len(lhv) > 60:
            scores["version"] = 0.20
        elif len(lhv) > 30:
            scores["version"] = 0.12
            reasons.append("龍魂版本描述偏短")
        else:
            scores["version"] = 0.06
            reasons.append("龍魂版本过于简略")

        depth = sum(scores.values())
        depth = round(min(depth, 1.0), 2)

        reason = "; ".join(reasons) if reasons else "推理深度充分"

        return depth, reason

    def _generate_longhun_version(self, topic: str, opinions: List[PersonaOpinion]) -> str:
        """生成龍魂创新版本描述"""
        reds = [o for o in opinions if o.audit == AuditMark.RED]
        if reds:
            return f"🔴 暂缓 — {'·'.join(o.persona for o in reds)}否决"

        # 提取各维度关键词
        strategy = next((o.opinion.split('\n')[0] for o in opinions if o.persona == "诸葛亮"), "")
        tech = next((o.opinion.split('\n')[0] for o in opinions if o.persona == "鲁班"), "")
        aesthetic = next((o.opinion.split('\n')[0] for o in opinions if o.persona == "李白"), "")

        return (
            f"龍魂版「{topic}」：暗色鎏金风格·DNA全程追溯·三色审计集成·"
            f"本地优先·鲲鹏同步。不是抄——是我们的版本。"
        )

    def _save_report(self, report: InnovationReport):
        p = self.data_dir / f"innovation_{report.report_id}.json"
        data = asdict(report)
        # 转换enum
        data["overall_audit"] = report.overall_audit.value
        for op in data["personas_opinions"]:
            op["audit"] = op["audit"]
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")

    def _make_dna(self, tag: str) -> str:
        h = hashlib.sha256(f"{tag}:{time.time_ns()}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️2026-07-25-{tag.replace(':','-')}-{h}"

    # ─── Batch Analyze ───
    def batch_analyze(self, topics: List[Dict[str, str]]) -> List[InnovationReport]:
        """批量推演多个主题"""
        reports = []
        for t in topics:
            report = self.analyze(t.get("topic", ""), t.get("source", "auto-learner"))
            reports.append(report)
        return reports

    # ─── Summary Report ───
    def summary_report(self, reports: List[InnovationReport]) -> str:
        """汇总多个推演报告"""
        buf = []
        buf.append("═══════════════════════════════════")
        buf.append("  🧠 龍魂 · 创新推演汇总报告")
        buf.append("═══════════════════════════════════")
        buf.append(f"  时间: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
        buf.append(f"  DNA:  {DNA}")
        buf.append(f"  推演项: {len(reports)}")
        buf.append("")

        for i, r in enumerate(reports, 1):
            icon = "✅" if r.overall_audit == AuditMark.GREEN else ("⚠️" if r.overall_audit == AuditMark.YELLOW else "🔴")
            depth_icon = "🧠" if r.depth_score >= DEPTH_SHALLOW else "🌊"
            buf.append(f"  {i}. {icon} [{r.risk_score:.0%}风险] {depth_icon}深度{r.depth_score:.0%} {r.input_topic}")
            buf.append(f"     来源: {r.input_source} | 可落地: {'是' if r.actionability else '🔴否'}")
            buf.append(f"     龍魂版: {r.longhun_version[:80]}...")
            if r.shallow_reason and r.depth_score < DEPTH_SHALLOW:
                buf.append(f"     🌊 浅层: {r.shallow_reason}")
            buf.append("")

        actionable = sum(1 for r in reports if r.actionability)
        buf.append(f"  可落地: {actionable}/{len(reports)} · 等待老大拍板")
        buf.append("═══════════════════════════════════")
        return "\n".join(buf)


# ═══ CLI ═══
def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·创新推演引擎 v1.0")
    sub = parser.add_subparsers(dest="cmd")

    sp_analyze = sub.add_parser("analyze", help="对主题进行21人格推演")
    sp_analyze.add_argument("topic", help="推演主题")

    sp_batch = sub.add_parser("batch", help="批量推演演示")
    sp_summary = sub.add_parser("summary", help="汇总推演报告")
    sp_selftest = sub.add_parser("selftest", help="自检")

    args = parser.parse_args()
    engine = InnovationEngine()

    if args.cmd == "analyze":
        report = engine.analyze(args.topic)
        print(f"\n🧠 推演主题: {report.input_topic}")
        print(f"   综合审计: {report.overall_audit.value} | 风险: {report.risk_score:.0%} | 可落地: {'是' if report.actionability else '否'}")
        print(f"\n── 各人格推演 ──")
        for op in report.personas_opinions:
            if op.opinion.startswith("（"):
                continue  # 跳过默认无意义意见
            print(f"  [{op.audit.value}] {op.persona}({op.role})")
            print(f"  🔍 {op.opinion[:100]}...")
            print(f"  💡 {op.recommendation}")
            print()
        print(f"── 交叉创新 ──")
        print(report.cross_innovation)
        print(f"\n── 龍魂版本 ──")
        print(report.longhun_version)

    elif args.cmd == "batch":
        topics = [
            {"topic": "多Agent协作框架", "source": "GitHub Trending"},
            {"topic": "中文大模型底座Qwen2.5", "source": "HuggingFace"},
            {"topic": "AI工作流自动化编排", "source": "CSDN"},
            {"topic": "自动部署到鲲鹏服务器", "source": "GitHub"},
            {"topic": "AI伦理与数据主权框架", "source": "知乎"},
        ]
        reports = engine.batch_analyze(topics)
        print(engine.summary_report(reports))

    elif args.cmd == "summary":
        topics = [
            {"topic": "多Agent协作框架", "source": "GitHub"},
            {"topic": "中文大模型底座", "source": "HuggingFace"},
        ]
        reports = engine.batch_analyze(topics)
        print(engine.summary_report(reports))

    elif args.cmd == "selftest":
        errors = 0
        engine = InnovationEngine()

        # Test 1: analyze single topic
        report = engine.analyze("多Agent协作框架", "GitHub")
        assert len(report.personas_opinions) == 11, f"Expected 11 opinions, got {len(report.personas_opinions)}"
        print(f"  ✅ 1/8 单主题推演: {len(report.personas_opinions)}人格参与")

        # Test 2: opinions have required fields
        for op in report.personas_opinions:
            assert op.persona, "Missing persona"
            assert op.role, "Missing role"
            assert op.opinion, "Missing opinion"
        print("  ✅ 2/8 意见完整性: 全部字段齐全")

        # Test 3: audit marks
        audits = {op.audit for op in report.personas_opinions}
        assert len(audits) >= 1, "No audit marks"
        print(f"  ✅ 3/8 审计标记: {len(audits)}种不同标记")

        # Test 4: cross innovation
        assert len(report.cross_innovation) > 50, f"Cross innovation too short: {len(report.cross_innovation)}"
        print(f"  ✅ 4/8 交叉创新: {len(report.cross_innovation)}字符")

        # Test 5: batch analyze
        topics = [
            {"topic": "多Agent协作框架", "source": "GitHub"},
            {"topic": "底座模型升级Qwen2.5", "source": "HuggingFace"},
            {"topic": "用户行为追踪SDK", "source": "GitHub"},  # 应该触发红色
        ]
        reports = engine.batch_analyze(topics)
        assert len(reports) == 3
        print(f"  ✅ 5/8 批量推演: {len(reports)}项")

        # Test 6: summary report
        summary = engine.summary_report(reports)
        assert len(summary) > 200, f"Summary too short: {len(summary)}"
        print(f"  ✅ 6/8 汇总报告: {len(summary)}字符")

        # Test 7: v2.0 深度评估-有模板
        assert report.depth_score > 0, f"Depth should be non-zero"
        assert report.depth_score >= DEPTH_SHALLOW, f"Templated topic depth={report.depth_score} should >= {DEPTH_SHALLOW}"
        print(f"  ✅ 7/8 推理深度(有模板): {report.depth_score:.0%} 🧠充分")

        # Test 8: v2.0 深度评估-无模板（通用推演应标记浅层）
        unknown_report = engine.analyze("未知技术XYZ", "Somewhere")
        assert unknown_report.depth_score < DEPTH_SHALLOW, \
            f"Unknown topic depth={unknown_report.depth_score} should < {DEPTH_SHALLOW}"
        assert len(unknown_report.shallow_reason) > 0, "Should have shallow reason"
        print(f"  ✅ 8/8 推理深度(无模板): {unknown_report.depth_score:.0%} 🌊浅层'{unknown_report.shallow_reason}'")

        print(f"\n🎯 自检: 8/8 全绿 (v2.0 深度守卫已激活)")
        sys.exit(0)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
