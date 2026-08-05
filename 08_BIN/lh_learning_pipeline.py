#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·丙申·丙辰·己丑时·蒙-LEARNING-PIPELINE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂学习管道 v1.0 · 六库自动化学习系统
Inbox → DNA拆解 → 任务派生 → 趋势绑定 → 项目实战 → 数字大军

DNA: #龍芯⚡️丙午·丙申·丙辰·己丑时·蒙-LEARNING-PIPELINE-v1.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import sys
import json
import hashlib
import time
import uuid
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
from datetime import datetime

# ═══════════════════════════════════════════════════════════
# 存储路径
# ═══════════════════════════════════════════════════════════

PIPELINE_DIR = Path.home() / ".longhun" / "learning_pipeline"
PIPELINE_DIR.mkdir(parents=True, exist_ok=True)


def _jsonl_path(db_name: str) -> Path:
    return PIPELINE_DIR / f"{db_name}.jsonl"


def _append_jsonl(path: Path, record: Dict[str, Any]):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')


def _read_jsonl(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    records = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return records


def _gen_id(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4().hex[:12]}"


# ═══════════════════════════════════════════════════════════
# 一、Learning Inbox · 学习入口池
# ═══════════════════════════════════════════════════════════

class ResourceType(Enum):
    WEBSITE = "Website"
    PAPER = "Paper"
    VIDEO = "Video"
    IDEA = "Idea"
    CODE = "Code"
    TREND = "Trend"


class InboxStatus(Enum):
    PURIFYING = "待净化"
    PURIFIED = "已净化"
    IMPORTED = "已入库"


@dataclass
class InboxItem:
    """入口池条目"""
    item_id: str
    title: str
    resource_type: ResourceType
    url: str = ""
    raw_content: str = ""
    status: InboxStatus = InboxStatus.PURIFYING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    purified_at: Optional[str] = None
    imported_at: Optional[str] = None
    purity_score: float = 100.0       # 净化分数
    noise_flags: List[str] = field(default_factory=list)  # 噪音标记
    dna_list: List[str] = field(default_factory=list)     # 拆解后的DNA列表

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['resource_type'] = self.resource_type.value
        d['status'] = self.status.value
        return d


class LearningInbox:
    """学习入口池 · 一切内容丢这里"""

    def __init__(self):
        self.path = _jsonl_path("inbox")
        self.items: Dict[str, InboxItem] = {}
        self._load()

    def _load(self):
        for record in _read_jsonl(self.path):
            item = InboxItem(
                item_id=record['item_id'],
                title=record['title'],
                resource_type=ResourceType(record['resource_type']),
                url=record.get('url', ''),
                raw_content=record.get('raw_content', ''),
                status=InboxStatus(record.get('status', '待净化')),
                created_at=record.get('created_at', ''),
                purified_at=record.get('purified_at'),
                imported_at=record.get('imported_at'),
                purity_score=record.get('purity_score', 100.0),
                noise_flags=record.get('noise_flags', []),
                dna_list=record.get('dna_list', []),
            )
            self.items[item.item_id] = item

    def add(self, title: str, resource_type: ResourceType,
            url: str = "", raw_content: str = "") -> InboxItem:
        """投喂新内容 → 自动进入待净化"""
        item = InboxItem(
            item_id=_gen_id("INBOX-"),
            title=title,
            resource_type=resource_type,
            url=url,
            raw_content=raw_content,
            status=InboxStatus.PURIFYING,
        )
        self.items[item.item_id] = item
        _append_jsonl(self.path, item.to_dict())
        return item

    def purify(self, item_id: str) -> Tuple[bool, InboxItem]:
        """净化 → 过滤营销语言/空洞结论/噪音"""
        if item_id not in self.items:
            return (False, None)

        item = self.items[item_id]
        content = item.raw_content

        # 净化检测
        noise_patterns = {
            '营销话术': ['限时优惠','立即购买','点击链接','加微信','扫码','免费领取','名额有限'],
            '空洞结论': ['众所周知','毫无疑问','显而易见','必须','一定','绝对'],
            '引流话术': ['关注我','点赞收藏','转发分享','评论区见','si我'],
            '过度承诺': ['保证','100%','肯定','一定成功','稳赚'],
            '情绪操控': ['错过后悔','最后机会','再不行动','马上涨价'],
        }

        noise_flags = []
        for category, patterns in noise_patterns.items():
            for p in patterns:
                if p in content:
                    noise_flags.append(f"{category}:{p}")

        # 计算纯度分数
        if noise_flags:
            item.purity_score = max(0, 100 - len(noise_flags) * 8)
        else:
            item.purity_score = 100.0

        item.noise_flags = noise_flags
        item.status = InboxStatus.PURIFIED
        item.purified_at = datetime.now().isoformat()

        _append_jsonl(self.path, item.to_dict())
        return (True, item)

    def list_by_status(self, status: InboxStatus) -> List[InboxItem]:
        return [item for item in self.items.values() if item.status == status]

    def stats(self) -> Dict[str, Any]:
        items = list(self.items.values())
        return {
            "total": len(items),
            "purifying": sum(1 for i in items if i.status == InboxStatus.PURIFYING),
            "purified": sum(1 for i in items if i.status == InboxStatus.PURIFIED),
            "imported": sum(1 for i in items if i.status == InboxStatus.IMPORTED),
            "avg_purity": sum(i.purity_score for i in items) / max(1, len(items)),
        }


# ═══════════════════════════════════════════════════════════
# 二、Knowledge DNA · 知识基因库
# ═══════════════════════════════════════════════════════════

class DNADirection(Enum):
    AI = "AI"
    WEB = "Web"
    METAVERSE = "元宇宙"
    SYSTEM = "系统"
    PHILOSOPHY = "哲学"
    UNKNOWN = "未知"


class DNADifficulty(Enum):
    BASIC = "基础"
    INTERMEDIATE = "中级"
    ADVANCED = "高级"
    EXPERT = "专家"


@dataclass
class KnowledgeDNA:
    """知识基因 · 可复用的知识原子"""
    dna_id: str
    direction: DNADirection
    core_concept: str          # 核心概念
    technical_points: List[str] = field(default_factory=list)  # 技术点
    examples: List[str] = field(default_factory=list)          # 示例/伪代码
    replicable: bool = True    # 是否可复用
    difficulty: DNADifficulty = DNADifficulty.INTERMEDIATE
    purity: str = "高"         # 纯度 高/中/低
    source_inbox_id: str = ""  # 来源Inbox条目
    source_url: str = ""       # 原始来源链接
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: List[str] = field(default_factory=list)
    related_dna: List[str] = field(default_factory=list)  # 关联DNA
    derived_tasks: List[str] = field(default_factory=list)  # 派生的学习任务

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['direction'] = self.direction.value
        d['difficulty'] = self.difficulty.value
        return d


class KnowledgeDNABase:
    """知识基因库 · 核心中的核心"""

    def __init__(self):
        self.path = _jsonl_path("knowledge_dna")
        self.dnas: Dict[str, KnowledgeDNA] = {}
        self._load()

    def _load(self):
        for record in _read_jsonl(self.path):
            dna = KnowledgeDNA(
                dna_id=record['dna_id'],
                direction=DNADirection(record['direction']),
                core_concept=record['core_concept'],
                technical_points=record.get('technical_points', []),
                examples=record.get('examples', []),
                replicable=record.get('replicable', True),
                difficulty=DNADifficulty(record.get('difficulty', '中级')),
                purity=record.get('purity', '高'),
                source_inbox_id=record.get('source_inbox_id', ''),
                source_url=record.get('source_url', ''),
                created_at=record.get('created_at', ''),
                tags=record.get('tags', []),
                related_dna=record.get('related_dna', []),
                derived_tasks=record.get('derived_tasks', []),
            )
            self.dnas[dna.dna_id] = dna

    def decompose(self, inbox_item: InboxItem) -> List[KnowledgeDNA]:
        """从一个Inbox条目拆解为多条DNA · 自动拆解"""
        content = inbox_item.raw_content[:2000]  # 取前2000字符
        results = []

        # 基于内容主题拆解
        directions_map = {
            'AI': ['AI','人工智能','机器学习','深度学习','LLM','GPT','transformer','neural','模型','训练'],
            'Web': ['前端','后端','React','Vue','Node','API','HTTP','REST','数据库','SQL'],
            '元宇宙': ['元宇宙','虚拟','AR','VR','3D','数字人','spatial','avatar'],
            '系统': ['系统','架构','分布式','微服务','docker','k8s','linux','运维'],
            '哲学': ['哲学','伦理','易经','道德经','文化','价值观','意义'],
        }

        detected_directions = []
        for direction, keywords in directions_map.items():
            if any(kw.lower() in content.lower() for kw in keywords):
                detected_directions.append(DNADirection(direction))

        if not detected_directions:
            detected_directions = [DNADirection.UNKNOWN]

        # 拆解：提取核心概念
        sentences = [s.strip() for s in content.replace('\n', '。').split('。') if len(s.strip()) > 10]

        for i, direction in enumerate(detected_directions[:3]):
            concept = sentences[i] if i < len(sentences) else f"{inbox_item.title} - {direction.value}方向"

            # 提取技术点
            tech_points = []
            for s in sentences:
                # 检测技术相关关键词
                tech_kw = ['算法','函数','API','架构','模式','协议','数据','计算','引擎']
                if any(kw in s for kw in tech_kw):
                    tech_points.append(s[:100])

            dna = KnowledgeDNA(
                dna_id=_gen_id(f"DNA-{direction.value[:2]}-"),
                direction=direction,
                core_concept=concept[:100],
                technical_points=tech_points[:5],
                examples=[s[:100] for s in sentences[1:4]],
                purity="高" if inbox_item.purity_score > 70 else ("中" if inbox_item.purity_score > 40 else "低"),
                source_inbox_id=inbox_item.item_id,
                source_url=inbox_item.url,
                tags=inbox_item.noise_flags[:3],
            )
            results.append(dna)
            self.dnas[dna.dna_id] = dna
            _append_jsonl(self.path, dna.to_dict())

        # 更新 Inbox 的 dna_list
        inbox_item.dna_list = [d.dna_id for d in results]
        inbox_item.status = InboxStatus.IMPORTED
        inbox_item.imported_at = datetime.now().isoformat()

        return results

    def stats(self) -> Dict[str, Any]:
        dnas = list(self.dnas.values())
        dir_counts = {}
        for d in dnas:
            dir_name = d.direction.value
            dir_counts[dir_name] = dir_counts.get(dir_name, 0) + 1
        return {
            "total": len(dnas),
            "by_direction": dir_counts,
            "replicable": sum(1 for d in dnas if d.replicable),
            "high_purity": sum(1 for d in dnas if d.purity == "高"),
        }


# ═══════════════════════════════════════════════════════════
# 三、Learning Tasks · 学习小卡片
# ═══════════════════════════════════════════════════════════

class LearnMode(Enum):
    SCAN = "扫盲"
    DEEP = "深入"
    PRACTICE = "实战"


class TaskStatus(Enum):
    TODO = "Todo"
    DOING = "Doing"
    DONE = "Done"


class EnergyCost(Enum):
    LOW = "低"
    MEDIUM = "中"
    HIGH = "高"


@dataclass
class LearningTask:
    """学习任务卡片 · 每日玩的地方"""
    task_id: str
    name: str
    related_dna_id: str
    learn_mode: LearnMode = LearnMode.SCAN
    status: TaskStatus = TaskStatus.TODO
    energy: EnergyCost = EnergyCost.MEDIUM
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    review_url: str = ""
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['learn_mode'] = self.learn_mode.value
        d['status'] = self.status.value
        d['energy'] = self.energy.value
        return d


class LearningTaskBoard:
    """学习任务看板"""

    def __init__(self):
        self.path = _jsonl_path("learning_tasks")
        self.tasks: Dict[str, LearningTask] = {}
        self._load()

    def _load(self):
        for record in _read_jsonl(self.path):
            task = LearningTask(
                task_id=record['task_id'],
                name=record['name'],
                related_dna_id=record.get('related_dna_id', ''),
                learn_mode=LearnMode(record.get('learn_mode', '扫盲')),
                status=TaskStatus(record.get('status', 'Todo')),
                energy=EnergyCost(record.get('energy', '中')),
                created_at=record.get('created_at', ''),
                completed_at=record.get('completed_at'),
                review_url=record.get('review_url', ''),
                notes=record.get('notes', ''),
            )
            self.tasks[task.task_id] = task

    def derive_from_dna(self, dna: KnowledgeDNA) -> LearningTask:
        """从DNA自动派生学习任务"""
        task = LearningTask(
            task_id=_gen_id(f"TASK-{dna.direction.value[:2]}-"),
            name=f"学习{dna.direction.value}：{dna.core_concept[:30]}",
            related_dna_id=dna.dna_id,
            learn_mode=LearnMode.SCAN,
            status=TaskStatus.TODO,
            energy=EnergyCost.MEDIUM if dna.difficulty.value == "中级" else (
                EnergyCost.HIGH if dna.difficulty.value in ("高级","专家") else EnergyCost.LOW
            ),
        )
        self.tasks[task.task_id] = task
        _append_jsonl(self.path, task.to_dict())

        # 回写到 DNA
        dna.derived_tasks.append(task.task_id)
        return task

    def mark_done(self, task_id: str):
        if task_id in self.tasks:
            self.tasks[task_id].status = TaskStatus.DONE
            self.tasks[task_id].completed_at = datetime.now().isoformat()
            _append_jsonl(self.path, self.tasks[task_id].to_dict())

    def stats(self) -> Dict[str, Any]:
        tasks = list(self.tasks.values())
        return {
            "total": len(tasks),
            "todo": sum(1 for t in tasks if t.status == TaskStatus.TODO),
            "doing": sum(1 for t in tasks if t.status == TaskStatus.DOING),
            "done": sum(1 for t in tasks if t.status == TaskStatus.DONE),
        }


# ═══════════════════════════════════════════════════════════
# 四、Future Signals · 世界趋势库
# ═══════════════════════════════════════════════════════════

class TimeScale(Enum):
    SHORT = "3年"
    MEDIUM = "5年"
    LONG = "10年"


@dataclass
class FutureSignal:
    """世界趋势信号"""
    signal_id: str
    name: str
    direction: str  # AGI/对齐/Agent/数字人/3DWeb/算力/人机/去中心化/生产关系
    strength: float = 0.5     # 信号强度 0-1
    uncertainty: float = 0.5  # 不确定性 0-1
    time_scale: TimeScale = TimeScale.MEDIUM
    related_dna: List[str] = field(default_factory=list)
    related_projects: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['time_scale'] = self.time_scale.value
        return d


class FutureSignalBase:
    """世界趋势库"""

    BUILTIN_DIRECTIONS = [
        "AGI/大模型瓶颈", "AI对齐&安全", "Agent社会",
        "数字人/虚拟文明", "3D Web/空间计算", "算力/能源极限",
        "人机融合", "去中心化vs平台化", "新生产关系"
    ]

    def __init__(self):
        self.path = _jsonl_path("future_signals")
        self.signals: Dict[str, FutureSignal] = {}
        self._load()
        self._ensure_builtin()

    def _load(self):
        for record in _read_jsonl(self.path):
            sig = FutureSignal(
                signal_id=record['signal_id'],
                name=record['name'],
                direction=record['direction'],
                strength=record.get('strength', 0.5),
                uncertainty=record.get('uncertainty', 0.5),
                time_scale=TimeScale(record.get('time_scale', '5年')),
                related_dna=record.get('related_dna', []),
                related_projects=record.get('related_projects', []),
                created_at=record.get('created_at', ''),
            )
            self.signals[sig.signal_id] = sig

    def _ensure_builtin(self):
        for direction in self.BUILTIN_DIRECTIONS:
            if not any(s.direction == direction for s in self.signals.values()):
                sig = FutureSignal(
                    signal_id=_gen_id("SIG-"),
                    name=direction,
                    direction=direction,
                    strength=0.5,
                    uncertainty=0.6,
                )
                self.signals[sig.signal_id] = sig
                _append_jsonl(self.path, sig.to_dict())

    def link_dna(self, signal_id: str, dna_id: str):
        if signal_id in self.signals and dna_id not in self.signals[signal_id].related_dna:
            self.signals[signal_id].related_dna.append(dna_id)
            _append_jsonl(self.path, self.signals[signal_id].to_dict())

    def stats(self) -> Dict[str, Any]:
        signals = list(self.signals.values())
        return {
            "total": len(signals),
            "avg_strength": sum(s.strength for s in signals) / max(1, len(signals)),
            "high_uncertainty": sum(1 for s in signals if s.uncertainty > 0.7),
        }


# ═══════════════════════════════════════════════════════════
# 五、Projects · 实验与战场
# ═══════════════════════════════════════════════════════════

class ProjectMaturity(Enum):
    IDEA = "想法"
    VALIDATION = "验证"
    PROTOTYPE = "原型"
    TOOL = "工具"
    SYSTEM = "系统实验"


@dataclass
class Project:
    """实验项目"""
    project_id: str
    name: str
    goal: str
    project_type: str  # 技术验证/原型/世界模型/工具/系统实验
    used_dna: List[str] = field(default_factory=list)
    maturity: ProjectMaturity = ProjectMaturity.IDEA
    scalable_to_system: bool = False
    status: str = "规划中"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['maturity'] = self.maturity.value
        return d


class ProjectBase:
    """项目库"""

    def __init__(self):
        self.path = _jsonl_path("projects")
        self.projects: Dict[str, Project] = {}
        self._load()

    def _load(self):
        for record in _read_jsonl(self.path):
            proj = Project(
                project_id=record['project_id'],
                name=record['name'],
                goal=record['goal'],
                project_type=record.get('project_type', '原型'),
                used_dna=record.get('used_dna', []),
                maturity=ProjectMaturity(record.get('maturity', '想法')),
                scalable_to_system=record.get('scalable_to_system', False),
                status=record.get('status', '规划中'),
                created_at=record.get('created_at', ''),
            )
            self.projects[proj.project_id] = proj

    def stats(self) -> Dict[str, Any]:
        projects = list(self.projects.values())
        return {
            "total": len(projects),
            "by_maturity": {m.value: sum(1 for p in projects if p.maturity == m)
                           for m in ProjectMaturity},
        }


# ═══════════════════════════════════════════════════════════
# 六、Digital Army · 数字大军编制表
# ═══════════════════════════════════════════════════════════

@dataclass
class Soldier:
    """数字兵种"""
    soldier_id: str
    name: str
    role: str  # 分析/构建/判断/清洗
    ability_source: List[str] = field(default_factory=list)  # DNA集合
    specialties: List[str] = field(default_factory=list)     # 擅长领域
    problem_types: List[str] = field(default_factory=list)   # 可解决问题
    combat_power: float = 1.0   # 战力值
    level: int = 1
    status: str = "待训练"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DigitalArmy:
    """数字大军编制"""

    ROLES = ["分析", "构建", "判断", "清洗"]
    ROLE_KEYWORDS = {
        "分析": ["分析","评估","对比","review","analysis"],
        "构建": ["构建","创建","开发","build","create","develop"],
        "判断": ["判断","决策","判定","judge","decide"],
        "清洗": ["净化","过滤","清洗","purify","filter","clean"],
    }

    def __init__(self):
        self.path = _jsonl_path("digital_army")
        self.soldiers: Dict[str, Soldier] = {}
        self._load()

    def _load(self):
        for record in _read_jsonl(self.path):
            sol = Soldier(
                soldier_id=record['soldier_id'],
                name=record['name'],
                role=record['role'],
                ability_source=record.get('ability_source', []),
                specialties=record.get('specialties', []),
                problem_types=record.get('problem_types', []),
                combat_power=record.get('combat_power', 1.0),
                level=record.get('level', 1),
                status=record.get('status', '待训练'),
            )
            self.soldiers[sol.soldier_id] = sol

    def recruit_from_dna(self, dna: KnowledgeDNA) -> Soldier:
        """从DNA招募新兵种"""
        # 根据DNA方向匹配角色
        role_map = {
            DNADirection.AI: ["分析", "构建"],
            DNADirection.WEB: ["构建"],
            DNADirection.SYSTEM: ["构建", "判断"],
            DNADirection.PHILOSOPHY: ["分析", "判断"],
            DNADirection.METAVERSE: ["构建"],
            DNADirection.UNKNOWN: ["分析"],
        }
        roles = role_map.get(dna.direction, ["分析"])
        role = roles[0]

        soldier = Soldier(
            soldier_id=_gen_id("SOLDIER-"),
            name=f"{dna.direction.value}{role}兵·{dna.core_concept[:10]}",
            role=role,
            ability_source=[dna.dna_id],
            specialties=dna.technical_points[:3],
            problem_types=[dna.core_concept],
            combat_power=1.0 + (len(dna.technical_points) * 0.1),
            status="新兵入伍",
        )
        self.soldiers[soldier.soldier_id] = soldier
        _append_jsonl(self.path, soldier.to_dict())

        dna.tags.append(f"ARMY:{soldier.soldier_id}")
        return soldier

    def stats(self) -> Dict[str, Any]:
        soldiers = list(self.soldiers.values())
        role_counts = {}
        for s in soldiers:
            role_counts[s.role] = role_counts.get(s.role, 0) + 1
        return {
            "total": len(soldiers),
            "by_role": role_counts,
            "avg_power": sum(s.combat_power for s in soldiers) / max(1, len(soldiers)),
            "trained": sum(1 for s in soldiers if s.status == "已训练"),
        }


# ═══════════════════════════════════════════════════════════
# 七、自动化管道引擎
# ═══════════════════════════════════════════════════════════

class LearningPipelineEngine:
    """学习管道主引擎 · 六库联动自动化"""

    def __init__(self):
        self.inbox = LearningInbox()
        self.dna_base = KnowledgeDNABase()
        self.tasks = LearningTaskBoard()
        self.signals = FutureSignalBase()
        self.projects = ProjectBase()
        self.army = DigitalArmy()

    def feed(self, title: str, resource_type: str, url: str = "", content: str = "") -> InboxItem:
        """投喂内容 → 自动进入待净化"""
        rt = ResourceType(resource_type) if resource_type in [e.value for e in ResourceType] else ResourceType.IDEA
        return self.inbox.add(title, rt, url, content)

    def process_inbox_item(self, item_id: str) -> Dict[str, Any]:
        """处理单个Inbox条目：净化→拆DNA→派任务→趋势绑定"""
        result = {"inbox_id": item_id, "steps": []}

        # 步骤1：净化
        ok, item = self.inbox.purify(item_id)
        if not ok:
            result["steps"].append({"step": "purify", "status": "❌ 未找到"})
            return result
        result["steps"].append({
            "step": "purify",
            "status": "✅",
            "purity": item.purity_score,
            "noise": item.noise_flags,
        })

        # 步骤2：DNA拆解
        dnas = self.dna_base.decompose(item)
        result["steps"].append({
            "step": "decompose",
            "status": "✅",
            "dna_count": len(dnas),
            "dna_ids": [d.dna_id for d in dnas],
        })

        # 步骤3：派生学习任务
        tasks_created = []
        for dna in dnas:
            task = self.tasks.derive_from_dna(dna)
            tasks_created.append(task.task_id)
        result["steps"].append({
            "step": "derive_tasks",
            "status": "✅",
            "task_count": len(tasks_created),
            "task_ids": tasks_created,
        })

        # 步骤4：趋势绑定
        for dna in dnas:
            for sig_id in self.signals.signals:
                sig = self.signals.signals[sig_id]
                if dna.direction.value in sig.direction or sig.direction.split('/')[0] in dna.direction.value:
                    self.signals.link_dna(sig_id, dna.dna_id)
        result["steps"].append({
            "step": "signal_binding",
            "status": "✅",
        })

        # 步骤5：数字大军招募
        for dna in dnas[:2]:
            soldier = self.army.recruit_from_dna(dna)
            result["steps"].append({
                "step": "army_recruit",
                "status": "✅",
                "soldier": soldier.soldier_id,
                "role": soldier.role,
            })

        return result

    def pipeline_status(self) -> Dict[str, Any]:
        """管道全貌"""
        return {
            "inbox": self.inbox.stats(),
            "dna": self.dna_base.stats(),
            "tasks": self.tasks.stats(),
            "signals": self.signals.stats(),
            "projects": self.projects.stats(),
            "army": self.army.stats(),
        }

    def auto_process_all(self) -> List[Dict]:
        """自动处理所有待净化条目"""
        results = []
        for item in self.inbox.list_by_status(InboxStatus.PURIFYING):
            results.append(self.process_inbox_item(item.item_id))
        return results


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main():
    engine = LearningPipelineEngine()

    if len(sys.argv) < 2:
        print("╔══════════════════════════════════════╗")
        print("║  龍魂学习管道 v1.0                    ║")
        print("╠══════════════════════════════════════╣")
        print("║  python3 bin/lh_learning_pipeline.py feed <标题> <类型> [URL] [内容]")
        print("║    投喂新内容 → 自动进入待净化")
        print("║    feed 示例 网页 https://example.com '这是一个测试内容'")
        print("║")
        print("║  python3 bin/lh_learning_pipeline.py process <item_id>")
        print("║    处理单条：净化→拆DNA→派任务→绑定趋势→招募兵种")
        print("║")
        print("║  python3 bin/lh_learning_pipeline.py process-all")
        print("║    自动处理所有待净化条目")
        print("║")
        print("║  python3 bin/lh_learning_pipeline.py status")
        print("║    查看管道全貌")
        print("║")
        print("║  python3 bin/lh_learning_pipeline.py inbox")
        print("║    查看入口池")
        print("║")
        print("║  python3 bin/lh_learning_pipeline.py dna")
        print("║    查看知识基因库")
        print("║")
        print("║  python3 bin/lh_learning_pipeline.py tasks")
        print("║    查看学习任务")
        print("║")
        print("║  python3 bin/lh_learning_pipeline.py army")
        print("║    查看数字大军")
        print("╚══════════════════════════════════════╝")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "feed":
        if len(sys.argv) < 4:
            print("❌ 用法: feed <标题> <类型> [URL] [内容]")
            print("   类型: Website/Paper/Video/Idea/Code/Trend")
            sys.exit(1)
        title = sys.argv[2]
        rtype = sys.argv[3]
        url = sys.argv[4] if len(sys.argv) > 4 else ""
        content = sys.argv[5] if len(sys.argv) > 5 else ""
        item = engine.feed(title, rtype, url, content)
        print(f"✅ 已投喂: {item.item_id}")
        print(f"   标题: {title}")
        print(f"   类型: {rtype}")
        print(f"   状态: {item.status.value}")
        print(f"   → 运行 'process {item.item_id}' 开始自动化管道")

    elif cmd == "process":
        if len(sys.argv) < 3:
            print("❌ 用法: process <item_id>")
            sys.exit(1)
        item_id = sys.argv[2]
        result = engine.process_inbox_item(item_id)
        print(f"\n📦 处理结果: {item_id}")
        for step in result['steps']:
            icon = step['status']
            name = step['step']
            print(f"  {icon} {name}", end="")
            if 'purity' in step:
                print(f" (纯度:{step['purity']})", end="")
            if 'dna_count' in step:
                print(f" (拆解{step['dna_count']}条DNA)", end="")
            if 'task_count' in step:
                print(f" (派生{step['task_count']}个任务)", end="")
            if 'soldier' in step:
                print(f" (新兵:{step['role']})", end="")
            print()

    elif cmd == "process-all":
        results = engine.auto_process_all()
        print(f"✅ 自动处理完成: {len(results)} 条")

    elif cmd == "status":
        status = engine.pipeline_status()
        print("╔══════════════════════════════════════╗")
        print("║  学习管道全貌                        ║")
        print("╠══════════════════════════════════════╣")
        for db_name, stats in status.items():
            print(f"║  📦 {db_name}: {stats.get('total', 0)} 条                ║")
        print("╚══════════════════════════════════════╝")

    elif cmd == "inbox":
        print("📥 入口池:")
        for item in engine.inbox.items.values():
            print(f"  [{item.status.value}] {item.title[:40]} (纯度:{item.purity_score})")

    elif cmd == "dna":
        print("🧬 知识基因库:")
        for dna in engine.dna_base.dnas.values():
            print(f"  [{dna.direction.value}] {dna.core_concept[:50]} (纯度:{dna.purity})")

    elif cmd == "tasks":
        print("📋 学习任务:")
        for task in engine.tasks.tasks.values():
            print(f"  [{task.status.value}] {task.name[:40]} ({task.learn_mode.value}|{task.energy.value})")

    elif cmd == "army":
        print("🤖 数字大军:")
        for sol in engine.army.soldiers.values():
            print(f"  [{sol.role}] {sol.name[:30]} (战力:{sol.combat_power:.1f}|{sol.status})")

    else:
        print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()
