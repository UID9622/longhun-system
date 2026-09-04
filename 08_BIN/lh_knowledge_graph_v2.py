#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂 · CNSH知识图谱引擎 v2.0（完整可运行版）
DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-KNOWLEDGE-GRAPH-V2-UID9622
创建者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

核心思想：知识不是堆在仓库里，知识是长在结构里的。
用三才算法（天·地·人）做分类骨架，用CNSH语法做索引语言，
让每个概念都有坐标、有溯源、可被AI修复和重新组织。
Kimi和CodeBuddy不是"查"知识，是"修复"知识图——因为知识是活的。

功能:
  1. 三才知识分类（天/地/人）— 60领域全量预置，可无限扩展
  2. 知识节点CRUD — 节点ID  K-日期-哈希8
  3. 知识关系管理 — 包含/依赖/引用/冲突
  4. 知识图修复 — AI可调用（Kimi/CodeBuddy）
  5. 知识检索与索引 — 三才坐标+关键词+全文
  6. 知识导出 — CNSH格式 / JSON / Markdown
  7. 知识图可视化 — Mermaid树形图
  8. 与记忆引擎集成 — 知识变更自动写记忆摘要
  9. 剪贴板导出 — 知识节点一键导出为剪贴板格式
  10. API服务 — FastAPI(可选) 端口8767

用法:
  python3 08_BIN/lh_knowledge_graph_v2.py --init           # 初始化图谱(60领域·幂等)
  python3 08_BIN/lh_knowledge_graph_v2.py --status          # 系统状态
  python3 08_BIN/lh_knowledge_graph_v2.py --list            # 列出所有节点
  python3 08_BIN/lh_knowledge_graph_v2.py --list-tiancai 天 # 按三才列出
  python3 08_BIN/lh_knowledge_graph_v2.py --search "博弈论" # 搜索(名称/ID均可)
  python3 08_BIN/lh_knowledge_graph_v2.py --tree 天·元知识层 # 知识树(名称/ID)
  python3 08_BIN/lh_knowledge_graph_v2.py --path 博弈论      # 根路径追溯
  python3 08_BIN/lh_knowledge_graph_v2.py --mermaid 天·元知识层 # Mermaid可视化
  python3 08_BIN/lh_knowledge_graph_v2.py --clipboard 博弈论  # 剪贴板导出
  python3 08_BIN/lh_knowledge_graph_v2.py --repair          # 修复建议
  python3 08_BIN/lh_knowledge_graph_v2.py --export          # 导出CNSH
  python3 08_BIN/lh_knowledge_graph_v2.py --server 8767     # 启动API服务
"""

import os
import sys
import json
import hashlib
import time
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import argparse

# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# 数据目录：默认 ~/.longhun/knowledge_graph（跨应用共享知识·只新建子目录不触碰既有数据）
# 可用环境变量 LONGHUN_HOME 重定向 · 项目归档镜像见 ARCHIVE_DIR
LONGHUN_HOME = Path(os.environ.get("LONGHUN_HOME", Path.home() / ".longhun"))
KNOWLEDGE_DIR = LONGHUN_HOME / "knowledge_graph"
NODES_DIR = KNOWLEDGE_DIR / "nodes"
RELATIONS_DIR = KNOWLEDGE_DIR / "relations"
MEMORY_DIR = LONGHUN_HOME / "memory"
INDEX_FILE = KNOWLEDGE_DIR / "knowledge_index.json"
CNSH_OUTPUT = KNOWLEDGE_DIR / "cnsh_knowledge.cnsh"
CLIPBOARD_OUTPUT = KNOWLEDGE_DIR / "clipboard_export.md"
# 项目内归档镜像（路径铁律：产出可追溯）
ARCHIVE_DIR = Path.home() / "longhun-system/11_DATA/knowledge_graph"

for d in [KNOWLEDGE_DIR, NODES_DIR, RELATIONS_DIR, MEMORY_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# 三才分类映射（文档 §1.3 全量领域名单）
TIANCAI_MAP = {
    "天": {
        "T-001": ("认识论", ["知识", "真理", "信念", "证成", "怀疑论"]),
        "T-002": ("本体论", ["存在", "实体", "属性", "关系", "范畴"]),
        "T-003": ("逻辑学", ["演绎", "归纳", "谬误", "谓词逻辑", "模态逻辑"]),
        "T-004": ("伦理学", ["功利主义", "义务论", "德性伦理", "AI伦理"]),
        "T-005": ("美学", ["感知", "艺术", "设计美学", "数字美学"]),
        "T-006": ("现象学", ["意向性", "生活世界", "具身认知"]),
        "T-007": ("系统论", ["整体论", "涌现", "反馈", "自组织"]),
        "T-008": ("信息论", ["熵", "信息量", "信道容量", "编码"]),
        "T-009": ("博弈论", ["纳什均衡", "演化博弈", "机制设计"]),
        "T-010": ("控制论", ["反馈", "稳态", "自适应", "第二序控制论"]),
        "T-011": ("复杂性理论", ["混沌", "分形", "自组织临界性"]),
        "T-012": ("认知科学", ["认知", "心智", "意识", "具身认知"]),
        "T-013": ("语言哲学", ["指称", "意义", "语用学", "言语行为"]),
        "T-014": ("科学哲学", ["证伪主义", "范式转换", "研究纲领"]),
        "T-015": ("技术哲学", ["技术本质", "工具理性", "技术批判"]),
        "T-016": ("数学哲学", ["柏拉图主义", "直觉主义", "形式主义"]),
        "T-017": ("易经哲学", ["阴阳", "五行", "八卦", "变易"]),
        "T-018": ("道家哲学", ["道", "无为", "自然", "相对主义"]),
        "T-019": ("儒家哲学", ["仁", "礼", "中庸", "修身"]),
        "T-020": ("法家哲学", ["法", "术", "势", "变"]),
    },
    "地": {
        "D-001": ("编程语言理论", ["类型系统", "语义", "编译器", "解释器"]),
        "D-002": ("算法与数据结构", ["排序", "搜索", "图论", "动态规划"]),
        "D-003": ("操作系统", ["进程", "内存", "文件系统", "调度"]),
        "D-004": ("计算机网络", ["TCP/IP", "路由", "协议", "安全"]),
        "D-005": ("数据库系统", ["ACID", "索引", "事务", "分布式DB"]),
        "D-006": ("软件架构", ["微服务", "事件驱动", "DDD"]),
        "D-007": ("设计模式", ["创建型", "结构型", "行为型"]),
        "D-008": ("AI/ML基础", ["神经网络", "深度学习", "强化学习"]),
        "D-009": ("NLP", ["分词", "语义", "情感", "生成"]),
        "D-010": ("计算机视觉", ["卷积", "检测", "分割", "生成"]),
        "D-011": ("分布式系统", ["一致性", "CAP", "Paxos/Raft"]),
        "D-012": ("安全与加密", ["加密", "身份验证", "零信任"]),
        "D-013": ("图形学", ["渲染", "光追", "可视化"]),
        "D-014": ("编译器技术", ["词法分析", "语法分析", "优化"]),
        "D-015": ("运行时系统", ["JVM", "V8", "GC", "JIT"]),
        "D-016": ("CNSH语言", ["中文语法", "转译", "AST", "编译器"]),
        "D-017": ("龍魂系统架构", ["四层命名", "DNA链", "三色审计"]),
        "D-018": ("Web技术", ["HTML/CSS/JS", "WebAssembly"]),
        "D-019": ("云计算", ["IaaS", "PaaS", "SaaS", "容器"]),
        "D-020": ("DevOps", ["CI/CD", "监控", "日志", "可观测性"]),
    },
    "人": {
        "R-001": ("AI治理", ["对齐", "透明度", "责任", "监管"]),
        "R-002": ("数字主权", ["数据主权", "技术主权", "身份主权"]),
        "R-003": ("人机交互", ["UX", "可用性", "交互设计"]),
        "R-004": ("社会计算", ["众包", "社交网络", "社区治理"]),
        "R-005": ("创新理论", ["颠覆性创新", "S曲线", "技术采纳"]),
        "R-006": ("教育科技", ["个性化学习", "自适应教育"]),
        "R-007": ("知识管理", ["隐性知识", "显性知识", "SECI模型"]),
        "R-008": ("传播学", ["媒体理论", "信息传播", "网络效应"]),
        "R-009": ("语言学", ["语法", "语义", "语用", "中文特性"]),
        "R-010": ("心理学", ["认知", "行为", "动机", "决策"]),
        "R-011": ("社会学", ["结构", "权力", "网络", "群体行为"]),
        "R-012": ("经济学", ["网络效应", "平台经济", "token经济"]),
        "R-013": ("法学", ["知识产权", "隐私法", "平台责任"]),
        "R-014": ("政策研究", ["数字政策", "监管框架", "标准"]),
        "R-015": ("未来学", ["预测", "情景规划", "弱信号"]),
        "R-016": ("文化研究", ["数字文化", "亚文化", "全球化"]),
        "R-017": ("用户研究", ["人种志", "访谈", "可用性测试"]),
        "R-018": ("数据叙事", ["数据可视化", "叙事结构"]),
        "R-019": ("社区建设", ["参与", "治理", "激励机制"]),
        "R-020": ("龍魂知识体系", ["CNSH", "三才", "DNA", "三色审计"]),
    },
}
TIANCAI_DESC = {
    "天": "元知识·哲学·理论",
    "地": "技术·工程·实现",
    "人": "应用·社会·交互",
}
# 领域描述（简要·供节点 description 使用）
DOMAIN_DESC = {
    "天": {
        "T-001": "知识的本质、来源与验证",
        "T-002": "存在的本质与范畴",
        "T-003": "推理与论证的规则",
        "T-004": "道德与价值的判断",
        "T-005": "感知与艺术审美",
        "T-006": "意识与生活世界的直观研究",
        "T-007": "整体与部分的动态关系",
        "T-008": "信息量化与传输",
        "T-009": "多主体决策互动",
        "T-010": "系统调节与自适应",
        "T-011": "混沌与自组织",
        "T-012": "心智与认知机制",
        "T-013": "语言与意义的关系",
        "T-014": "科学知识的结构与演进",
        "T-015": "技术对人类社会的塑造",
        "T-016": "数学基础与本质",
        "T-017": "阴阳变化与系统",
        "T-018": "道与无为的哲学",
        "T-019": "仁礼中庸的哲学",
        "T-020": "法术势的治理哲学",
    },
    "地": {
        "D-001": "编程语言的语义与类型",
        "D-002": "计算与数据组织",
        "D-003": "计算机系统管理",
        "D-004": "信息网络通信",
        "D-005": "数据存储与管理",
        "D-006": "系统结构设计与组织",
        "D-007": "可复用解决方案",
        "D-008": "人工智能与机器学习",
        "D-009": "自然语言处理技术",
        "D-010": "视觉信息处理技术",
        "D-011": "跨节点协调与一致性",
        "D-012": "信息安全与保护",
        "D-013": "视觉计算与渲染",
        "D-014": "语言翻译与代码生成",
        "D-015": "程序执行环境",
        "D-016": "中文原生编程语言",
        "D-017": "龍魂系统自身架构",
        "D-018": "网页与前端技术",
        "D-019": "弹性计算与资源服务",
        "D-020": "开发运维一体化",
    },
    "人": {
        "R-001": "AI的对齐与监管",
        "R-002": "数据与技术主权",
        "R-003": "人与系统的交互",
        "R-004": "社交与群体计算",
        "R-005": "技术演进与创新",
        "R-006": "技术与教育融合",
        "R-007": "知识的创造与传播",
        "R-008": "信息传播与媒体",
        "R-009": "人类语言系统",
        "R-010": "心智与行为规律",
        "R-011": "社会结构与群体",
        "R-012": "资源配置与决策",
        "R-013": "法律规范与权利",
        "R-014": "公共政策与治理",
        "R-015": "未来情景推演",
        "R-016": "文化符号与认同",
        "R-017": "理解真实用户需求",
        "R-018": "数据驱动的叙事表达",
        "R-019": "社群激活与运营",
        "R-020": "龍魂系统自身知识体系",
    },
}


def _sha256_short(text: str, length: int = 8) -> str:
    """SHA-256 截断（规则禁 MD5/SHA-1·统一 SHA-256）"""
    return hashlib.sha256(text.encode()).hexdigest()[:length].upper()


def generate_dna(module: str = "KNOWLEDGE") -> str:
    h = _sha256_short(f"{module}{time.time_ns()}")
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{module}-{h}-{UID}"


def now_iso() -> str:
    return datetime.now().isoformat()


# ============================================================
# 三才分类定义
# ============================================================

class TianCai(Enum):
    TIAN = "天"
    DI = "地"
    REN = "人"


TIAN_KEYWORDS = ["哲学", "理论", "范式", "认识论", "本体论", "逻辑", "系统论", "信息论", "博弈论", "控制论", "认知", "美学", "现象学"]
DI_KEYWORDS = ["技术", "工程", "实现", "编程", "算法", "架构", "数据库", "网络", "安全", "系统", "语言", "编译", "分布式", "云计算"]
REN_KEYWORDS = ["应用", "社会", "交互", "伦理", "治理", "用户", "教育", "传播", "文化", "政策", "经济", "心理", "法律"]


def classify_tiancai(name: str, description: str = "") -> str:
    """根据名称和描述进行三才分类（新增未知节点时的自动分类）"""
    text = name + description
    tian_score = sum(1 for kw in TIAN_KEYWORDS if kw in text)
    di_score = sum(1 for kw in DI_KEYWORDS if kw in text)
    ren_score = sum(1 for kw in REN_KEYWORDS if kw in text)
    if tian_score >= di_score and tian_score >= ren_score:
        return "天"
    elif di_score >= ren_score:
        return "地"
    return "人"


# ============================================================
# 知识节点
# ============================================================

@dataclass
class KnowledgeNode:
    """知识节点"""
    id: str
    name: str
    tiancai: str          # 天/地/人
    domain_id: str = ""   # 领域编号 T-001 / D-001 / R-001
    parent_id: Optional[str] = None
    description: str = ""
    keywords: List[str] = field(default_factory=list)
    relations: List[Dict] = field(default_factory=list)  # [{type,target,weight}]
    cnsh_file: Optional[str] = None
    source: str = ""
    contributor: str = UID
    status: str = "活跃"  # 活跃/待完善/已归档
    dna: str = field(default_factory=lambda: generate_dna("NODE"))
    created_at: str = field(default_factory=now_iso)
    updated_at: str = field(default_factory=now_iso)

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'KnowledgeNode':
        return cls(**data)


# ============================================================
# 知识图谱引擎
# ============================================================

class KnowledgeGraphEngine:
    """知识图谱引擎"""

    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.index: Dict = {}
        self._load_index()
        self._load_nodes()

    # ---------- 持久化 ----------
    def _load_index(self):
        if INDEX_FILE.exists():
            try:
                with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                    self.index = json.load(f)
            except Exception:
                self.index = {}
        else:
            self.index = {}
        if not isinstance(self.index, dict) or "version" not in self.index:
            self.index = {
                "version": "2.0",
                "total_nodes": 0,
                "by_tiancai": {"天": 0, "地": 0, "人": 0},
                "by_keyword": {},
                "last_update": None,
            }

    def _save_index(self):
        self.index["total_nodes"] = len(self.nodes)
        self.index["by_tiancai"] = {"天": 0, "地": 0, "人": 0}
        by_kw: Dict[str, List[str]] = {}
        for node in self.nodes.values():
            self.index["by_tiancai"][node.tiancai] = self.index["by_tiancai"].get(node.tiancai, 0) + 1
            for kw in node.keywords:
                by_kw.setdefault(kw, [])
                if node.name not in by_kw[kw]:
                    by_kw[kw].append(node.name)
        self.index["by_keyword"] = by_kw
        self.index["last_update"] = datetime.now().isoformat()
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)

    def _load_nodes(self):
        for file in NODES_DIR.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    node = KnowledgeNode.from_dict(data)
                    self.nodes[node.id] = node
            except Exception as e:
                print(f"⚠️ 加载节点失败 {file}: {e}")

    def _save_node(self, node: KnowledgeNode):
        filepath = NODES_DIR / f"{node.id}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(node.to_dict(), f, indent=2, ensure_ascii=False)
        self._save_index()

    # ---------- 节点CRUD ----------
    def create_node(self, name: str, description: str = "",
                    parent_id: str = None, keywords: List[str] = None,
                    tiancai: str = None, domain_id: str = "") -> KnowledgeNode:
        """创建知识节点（同名存在则直接复用·幂等）"""
        existing = self.find_by_name(name)
        if existing:
            return existing
        if tiancai is None:
            tiancai = classify_tiancai(name, description)
        node_id = f"K-{datetime.now().strftime('%Y%m%d')}-{_sha256_short(name)}"
        node = KnowledgeNode(
            id=node_id,
            name=name,
            tiancai=tiancai,
            domain_id=domain_id,
            parent_id=parent_id,
            description=description,
            keywords=keywords or [],
        )
        self.nodes[node_id] = node
        self._save_node(node)
        self._update_memory(node)
        return node

    def update_node(self, node_id: str, **fields) -> Optional[KnowledgeNode]:
        """更新节点字段"""
        node = self.get_node(node_id)
        if not node:
            return None
        for k, v in fields.items():
            if hasattr(node, k) and k not in ("id", "dna", "created_at"):
                setattr(node, k, v)
        node.updated_at = now_iso()
        self._save_node(node)
        self._update_memory(node)
        return node

    def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        return self.nodes.get(node_id)

    def resolve(self, key: str) -> Optional[KnowledgeNode]:
        """解析节点：优先ID，其次精确名称，再退模糊名称"""
        node = self.get_node(key)
        if node:
            return node
        for n in self.nodes.values():
            if n.name == key:
                return n
        for n in self.nodes.values():
            if key in n.name:
                return n
        return None

    def find_by_name(self, name: str) -> Optional[KnowledgeNode]:
        for n in self.nodes.values():
            if n.name == name:
                return n
        return None

    def get_by_tiancai(self, tiancai: str) -> List[KnowledgeNode]:
        return [n for n in self.nodes.values() if n.tiancai == tiancai]

    def get_by_keyword(self, keyword: str) -> List[KnowledgeNode]:
        results = []
        for node in self.nodes.values():
            if keyword in node.name or keyword in node.description:
                results.append(node)
                continue
            for kw in node.keywords:
                if keyword == kw:
                    results.append(node)
                    break
        return results

    def search(self, query: str) -> List[KnowledgeNode]:
        """搜索知识节点（名称/描述/关键词）"""
        q = query.lower()
        results = []
        for node in self.nodes.values():
            if (q in node.name.lower() or q in node.description.lower() or
                    any(q in kw.lower() for kw in node.keywords) or
                    q in node.domain_id.lower()):
                results.append(node)
        return results

    # ---------- 关系管理 ----------
    def add_relation(self, source_id: str, target_id: str,
                     relation_type: str = "包含", weight: float = 1.0,
                     explanation: str = "") -> bool:
        """添加关系（源/目标均支持 名称 或 ID）"""
        source = self.resolve(source_id)
        target = self.resolve(target_id)
        if not source or not target:
            return False
        if source.id == target.id:
            return False
        relation = {
            "type": relation_type,
            "target": target.id,
            "target_name": target.name,
            "weight": weight,
            "explanation": explanation,
        }
        for r in source.relations:
            if r.get("target") == target.id:
                return True
        source.relations.append(relation)
        self._save_node(source)
        return True

    def add_relation_by_name(self, source_name: str, target_name: str,
                             relation_type: str = "包含", weight: float = 1.0,
                             explanation: str = "") -> bool:
        return self.add_relation(source_name, target_name, relation_type, weight, explanation)

    def get_relations(self, node_id: str) -> List[Dict]:
        node = self.get_node(node_id)
        if not node:
            return []
        return node.relations

    # ---------- 树与路径 ----------
    def get_children(self, node_id: str) -> List[KnowledgeNode]:
        return [n for n in self.nodes.values() if n.parent_id == node_id]

    def get_tree(self, node_id: str, depth: int = 3) -> Dict:
        node = self.get_node(node_id)
        if not node:
            return {}
        tree = {
            "id": node.id,
            "name": node.name,
            "tiancai": node.tiancai,
            "domain_id": node.domain_id,
            "description": node.description,
            "children": [],
        }
        if depth > 0:
            for child in self.get_children(node_id):
                tree["children"].append(self.get_tree(child.id, depth - 1))
        return tree

    def get_tree_mermaid(self, node_id: str, depth: int = 5) -> str:
        """生成 Mermaid graph TD 知识树"""
        def _lines(nid: str, lvl: int) -> List[str]:
            node = self.get_node(nid)
            if not node or lvl > depth:
                return []
            out = []
            tag = node.tiancai
            out.append(f'    n{node.id.replace("-", "_")}["{node.name} | {tag}层"]')
            for child in self.get_children(nid):
                out.extend(_lines(child.id, lvl + 1))
                out.append(f'    n{node.id.replace("-", "_")} --> n{child.id.replace("-", "_")}')
            return out

        header = ["graph TD"]
        lines = _lines(node_id, 0)
        if lines:
            header.extend(lines)
            return "\n".join(header)
        return "graph TD\n    missing[\"节点不存在\"]"

    def get_path(self, node_id: str) -> List[str]:
        """节点从根到自身的名称路径"""
        path = []
        node = self.get_node(node_id)
        visited = set()
        while node and node.id not in visited:
            visited.add(node.id)
            path.insert(0, node.name)
            node = self.get_node(node.parent_id) if node.parent_id else None
        return path

    # ---------- 记忆集成 ----------
    def _update_memory(self, node: KnowledgeNode):
        """更新记忆摘要（追加式·不覆盖）"""
        try:
            mem_file = MEMORY_DIR / "knowledge_digest.json"
            if mem_file.exists():
                with open(mem_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {"nodes": [], "last_update": None}
            if isinstance(data.get("nodes"), list):
                # 去重：同ID不重复记
                if not any(item.get("id") == node.id for item in data["nodes"]):
                    data["nodes"].append({
                        "id": node.id,
                        "name": node.name,
                        "tiancai": node.tiancai,
                        "domain_id": node.domain_id,
                        "keywords": node.keywords,
                        "dna": node.dna,
                    })
                    if len(data["nodes"]) > 500:
                        data["nodes"] = data["nodes"][-500:]
            data["last_update"] = datetime.now().isoformat()
            with open(mem_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ 更新记忆失败: {e}")

    def export_to_clipboard(self, node_id: str) -> str:
        """导出节点为剪贴板格式（Markdown）"""
        node = self.get_node(node_id)
        if not node:
            return "节点不存在"
        parent = self.get_node(node.parent_id) if node.parent_id else None
        rel_lines = []
        for r in node.relations:
            tname = r.get("target_name", r.get("target"))
            rel_lines.append(f'- {r["type"]} → {tname}')
        path_str = " → ".join(self.get_path(node_id)) or node.name
        return f"""# 📚 {node.name}

**DNA:** `{node.dna}`
**三才分类:** {node.tiancai}层（{TIANCAI_DESC.get(node.tiancai, '')}）
**领域编号:** {node.domain_id or '无'}
**父节点:** {parent.name if parent else '无'}
**关键词:** {', '.join(node.keywords) if node.keywords else '无'}

{node.description}

---
**关系:**
{chr(10).join(rel_lines) if rel_lines else '无'}

**路径:** {path_str}
**DNA追溯:** {node.dna}
**确认码:** {CONFIRM}
"""


# ============================================================
# CNSH知识导出
# ============================================================

class CNSHKnowledgeExporter:
    """CNSH知识导出器"""

    @staticmethod
    def export_to_cnsh(engine: KnowledgeGraphEngine) -> str:
        lines = [
            "# 🐉 龍魂 · CNSH知识图谱",
            f"# DNA: {generate_dna('CNSH-KNOWLEDGE')}",
            f"# 导出时间: {datetime.now().isoformat()}",
            "# 三才分类: 天·地·人",
            "# 关联确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "",
        ]
        for tiancai in ["天", "地", "人"]:
            nodes = engine.get_by_tiancai(tiancai)
            if not nodes:
                continue
            lines.append("")
            lines.append("# ============================================================")
            lines.append(f"# {tiancai}层: {TIANCAI_DESC.get(tiancai, '')}")
            lines.append("# ============================================================")
            for node in sorted(nodes, key=lambda x: x.name):
                lines.append("")
                lines.append(f"知识节点 {node.name}:")
                lines.append(f"  ID: {node.id}")
                lines.append(f"  领域编号: {node.domain_id or '无'}")
                lines.append(f"  三才: {node.tiancai}")
                if node.parent_id:
                    parent = engine.get_node(node.parent_id)
                    lines.append(f"  父节点: {parent.name if parent else node.parent_id}")
                lines.append(f"  描述: {node.description}")
                if node.keywords:
                    lines.append(f"  关键词: {', '.join(node.keywords)}")
                if node.relations:
                    lines.append("  关系:")
                    for rel in node.relations:
                        tname = rel.get("target_name", rel.get("target"))
                        lines.append(f"    - {rel['type']} → {tname} (权重:{rel['weight']})")
                lines.append(f"  DNA: {node.dna}")
                lines.append(f"  CNSH文件: {node.cnsh_file or '待生成'}")
                lines.append("")
        lines.append("# ============================================================")
        lines.append("# 知识图谱索引")
        lines.append(f"# 总节点数: {len(engine.nodes)}")
        for tiancai in ["天", "地", "人"]:
            count = len(engine.get_by_tiancai(tiancai))
            lines.append(f"# {tiancai}层: {count} 个节点")
        lines.append("# ============================================================")
        return "\n".join(lines)

    @staticmethod
    def export_to_markdown(engine: KnowledgeGraphEngine) -> str:
        """导出 Markdown 知识索引（可读性）"""
        lines = [
            "# 🐉 龍魂 · CNSH知识图谱 · 索引",
            f"> DNA: {generate_dna('MD-KNOWLEDGE')} · 导出: {datetime.now().isoformat()}",
            "",
        ]
        for tiancai in ["天", "地", "人"]:
            nodes = engine.get_by_tiancai(tiancai)
            lines.append(f"## {tiancai}层 · {TIANCAI_DESC.get(tiancai, '')}（{len(nodes)}）")
            lines.append("")
            for node in sorted(nodes, key=lambda x: x.name):
                lines.append(f"- **{node.name}** `{node.domain_id}` — {node.description}")
            lines.append("")
        return "\n".join(lines)

    @staticmethod
    def export_to_json(engine: KnowledgeGraphEngine) -> Dict:
        """导出完整 JSON 数据"""
        return {
            "version": "2.0",
            "dna": generate_dna("JSON-KNOWLEDGE"),
            "exported_at": now_iso(),
            "total_nodes": len(engine.nodes),
            "nodes": [node.to_dict() for node in engine.nodes.values()],
            "index": engine.index,
        }


# ============================================================
# AI知识修复接口（供 Kimi/CodeBuddy 调用）
# ============================================================

class KnowledgeRepairInterface:
    """知识修复接口 — AI可调用的知识图修复API"""

    def __init__(self, engine: KnowledgeGraphEngine):
        self.engine = engine

    def suggest_repairs(self) -> List[Dict]:
        """自动检测需要修复的知识节点"""
        suggestions = []
        for node in self.engine.nodes.values():
            issues = []
            if not node.description:
                issues.append("缺少描述")
            if len(node.keywords) < 2:
                issues.append("关键词少于2个")
            if not node.relations and not self.engine.get_children(node.id):
                issues.append("孤立节点（无关系/子节点）")
            if node.tiancai not in ["天", "地", "人"]:
                issues.append("三才分类无效")
            if not node.domain_id:
                issues.append("缺少领域编号")
            if issues:
                suggestions.append({
                    "node_id": node.id,
                    "name": node.name,
                    "tiancai": node.tiancai,
                    "issues": issues,
                    "suggested_fixes": self._suggest_fixes(node, issues),
                })
        return suggestions

    def _suggest_fixes(self, node: KnowledgeNode, issues: List[str]) -> List[str]:
        fixes = []
        for issue in issues:
            if issue == "缺少描述":
                fixes.append("添加描述: 请提供此概念的简要说明")
            elif issue == "关键词少于2个":
                fixes.append("添加关键词: 建议2-5个核心关键词")
            elif issue == "孤立节点（无关系/子节点）":
                fixes.append("建立关系或添加子节点: 将此概念连接到知识图谱中")
            elif issue == "三才分类无效":
                fixes.append("重新分类: 根据内容选择天/地/人")
            elif issue == "缺少领域编号":
                fixes.append("补齐领域编号: 参照 T-xxx/D-xxx/R-xxx 规范")
        return fixes

    def apply_fix(self, node_id: str, field: str, value: Any) -> bool:
        """应用修复"""
        node = self.engine.get_node(node_id)
        if not node:
            return False
        if hasattr(node, field) and field not in ("id", "dna", "created_at"):
            old_value = getattr(node, field)
            if old_value == value:
                return True
            setattr(node, field, value)
            node.updated_at = datetime.now().isoformat()
            self.engine._save_node(node)
            self.engine._update_memory(node)
            return True
        return False

    def get_repair_report(self) -> Dict:
        """生成修复报告"""
        suggestions = self.suggest_repairs()
        return {
            "total_suggestions": len(suggestions),
            "critical": [s for s in suggestions if len(s["issues"]) >= 2],
            "minor": [s for s in suggestions if len(s["issues"]) == 1],
            "suggestions": suggestions,
            "timestamp": datetime.now().isoformat(),
        }


# ============================================================
# 知识图谱初始化（60领域全量·幂等）
# ============================================================

def initialize_knowledge_graph(engine: Optional[KnowledgeGraphEngine] = None) -> KnowledgeGraphEngine:
    """初始化知识图谱 — 创建三才顶层 + 60领域节点 + 领域间关系"""
    if engine is None:
        engine = KnowledgeGraphEngine()
    exporter = CNSHKnowledgeExporter()

    # ---- 顶层节点（三才）----
    tian_node = engine.create_node(
        name="天·元知识层",
        description="哲学、理论、范式 — 知识的源头和底层规律",
        keywords=["哲学", "理论", "范式", "认识论", "本体论"],
        tiancai="天", domain_id="TIAN",
    )
    di_node = engine.create_node(
        name="地·技术层",
        description="编程、算法、架构 — 知识的具体实现和工程化",
        keywords=["技术", "工程", "编程", "算法", "架构"],
        tiancai="地", domain_id="DI",
    )
    ren_node = engine.create_node(
        name="人·应用层",
        description="伦理、社会、交互 — 知识的应用和影响",
        keywords=["应用", "社会", "交互", "伦理", "治理"],
        tiancai="人", domain_id="REN",
    )

    # ---- 60领域节点（文档 §1.3 全量名单）----
    created = 0
    reused = 0
    for tiancai, domain_map in TIANCAI_MAP.items():
        top = {"天": tian_node, "地": di_node, "人": ren_node}[tiancai]
        for domain_id, (name, keywords) in domain_map.items():
            existing = engine.find_by_name(name)
            if existing:
                reused += 1
                continue
            engine.create_node(
                name=name,
                description=DOMAIN_DESC[tiancai].get(domain_id, ""),
                parent_id=top.id,
                keywords=keywords,
                tiancai=tiancai,
                domain_id=domain_id,
            )
            created += 1

    # ---- 领域间关系（文档 §4 示例关系·按名称建立·幂等）----
    engine.add_relation_by_name("认识论", "逻辑学", "引用", 1.0, "认识论依赖逻辑推理框架")
    engine.add_relation_by_name("系统论", "控制论", "包含", 0.9, "控制论是系统论的反馈分支")
    engine.add_relation_by_name("博弈论", "经济学", "引用", 0.9, "博弈论是经济学的决策数学框架")
    engine.add_relation_by_name("算法与数据结构", "编程语言理论", "依赖", 0.9, "算法实现依赖语言语义")
    engine.add_relation_by_name("分布式系统", "数据库系统", "引用", 0.8, "分布式一致性约束数据库")
    engine.add_relation_by_name("AI治理", "伦理学", "引用", 1.0, "AI治理扎根伦理判断")
    engine.add_relation_by_name("CNSH语言", "龍魂知识体系", "包含", 1.0, "CNSH是龍魂知识体系的索引语言")
    engine.add_relation_by_name("AI/ML基础", "NLP", "包含", 0.9, "NLP是AI的子领域")
    engine.add_relation_by_name("AI/ML基础", "计算机视觉", "包含", 0.9, "CV是AI的子领域")
    engine.add_relation_by_name("知识管理", "龍魂知识体系", "引用", 0.8, "知识管理支撑龍魂知识生长")
    engine.add_relation_by_name("数字主权", "龍魂知识体系", "包含", 1.0, "数字主权是龍魂底座天条")
    engine.add_relation_by_name("易经哲学", "道家哲学", "包含", 0.9, "道家哲学根植易经")
    engine.add_relation_by_name("易经哲学", "儒家哲学", "引用", 0.8, "儒家易学一脉")
    engine.add_relation_by_name("安全与加密", "龍魂系统架构", "引用", 0.9, "龍魂三色审计/五层黑洞依赖安全")
    engine.add_relation_by_name("编译器技术", "CNSH语言", "依赖", 1.0, "CNSH转译依赖编译器技术")

    # ---- CNSH导出 ----
    cnsh_code = exporter.export_to_cnsh(engine)
    CNSH_OUTPUT.write_text(cnsh_code, encoding="utf-8")
    try:
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
        (ARCHIVE_DIR / "cnsh_knowledge.cnsh").write_text(cnsh_code, encoding="utf-8")
        (ARCHIVE_DIR / "knowledge_index.json").write_text(
            json.dumps(engine.index, indent=2, ensure_ascii=False), encoding="utf-8")
        md_code = exporter.export_to_markdown(engine)
        (ARCHIVE_DIR / "knowledge_index.md").write_text(md_code, encoding="utf-8")
    except Exception as e:
        print(f"⚠️ 项目归档失败: {e}")

    print("✅ 知识图谱初始化完成!")
    print(f"  总节点: {len(engine.nodes)}（新建 {created} · 复用 {reused}）")
    print(f"  天层: {len(engine.get_by_tiancai('天'))}")
    print(f"  地层: {len(engine.get_by_tiancai('地'))}")
    print(f"  人层: {len(engine.get_by_tiancai('人'))}")
    print(f"  CNSH导出: {CNSH_OUTPUT}")
    print(f"  项目归档: {ARCHIVE_DIR}")
    return engine


# ============================================================
# HTTP API 服务（可选依赖 FastAPI）
# ============================================================

def run_api_server(engine: KnowledgeGraphEngine, port: int = 8767):
    """启动知识图谱API服务（独立进程）"""
    try:
        from fastapi import FastAPI, HTTPException
        from fastapi.middleware.cors import CORSMiddleware
        import uvicorn
    except ImportError:
        print("⚠️ FastAPI/uvicorn未安装，API服务不可用")
        print("   安装: pip3 install fastapi uvicorn")
        return

    app = FastAPI(title="龍魂知识图谱API", version="2.0.0")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    repair = KnowledgeRepairInterface(engine)

    @app.get("/")
    def root():
        return {
            "service": "龍魂知识图谱引擎",
            "version": "2.0.0",
            "dna": generate_dna("API"),
            "total_nodes": len(engine.nodes),
            "status": "🟢 运行中",
        }

    @app.get("/nodes")
    def list_nodes(tiancai: str = None, keyword: str = None):
        if tiancai:
            nodes = engine.get_by_tiancai(tiancai)
        elif keyword:
            nodes = engine.get_by_keyword(keyword)
        else:
            nodes = list(engine.nodes.values())
        return {
            "count": len(nodes),
            "nodes": [{"id": n.id, "name": n.name, "domain_id": n.domain_id,
                       "tiancai": n.tiancai, "description": n.description[:100]} for n in nodes],
        }

    @app.get("/node/{key}")
    def get_node(key: str):
        node = engine.resolve(key)
        if not node:
            raise HTTPException(status_code=404, detail="节点不存在")
        return node.to_dict()

    @app.get("/search")
    def search(q: str):
        nodes = engine.search(q)
        return {"count": len(nodes),
                "nodes": [{"id": n.id, "name": n.name, "domain_id": n.domain_id,
                           "tiancai": n.tiancai} for n in nodes]}

    @app.get("/repair/suggest")
    def repair_suggest():
        return repair.get_repair_report()

    @app.post("/repair/apply")
    def repair_apply(node_id: str, field: str, value: str):
        if repair.apply_fix(node_id, field, value):
            return {"status": "success", "message": f"已修复 {node_id}.{field}"}
        raise HTTPException(status_code=400, detail="修复失败")

    @app.get("/tree/{key}")
    def tree(key: str, depth: int = 3):
        node = engine.resolve(key)
        if not node:
            raise HTTPException(status_code=404, detail="节点不存在")
        return engine.get_tree(node.id, depth)

    @app.get("/export/cnsh")
    def export_cnsh():
        return {"content": CNSHKnowledgeExporter.export_to_cnsh(engine)}

    print(f"🚀 知识图谱API服务启动: http://0.0.0.0:{port}")
    print(f"   - /              状态")
    print(f"   - /nodes         列出节点(?tiancai=&keyword=)")
    print(f"   - /node/xxx      节点详情(名称或ID)")
    print(f"   - /search?q=xxx  搜索")
    print(f"   - /repair/suggest 修复建议")
    print(f"   - /tree/xxx      知识树")
    uvicorn.run(app, host="0.0.0.0", port=port)


# ============================================================
# 命令行接口
# ============================================================

def _print_tree_pretty(engine: KnowledgeGraphEngine, node: Dict, indent: str = "", is_last: bool = True):
    """树形打印"""
    prefix = indent + ("└─ " if is_last else "├─ ")
    print(f"{prefix}{node['name']} [{node['tiancai']}]{(' · ' + node['description'][:30]) if node.get('description') else ''}")
    children = node.get("children", [])
    for i, child in enumerate(children):
        _print_tree_pretty(engine, child, indent + ("   " if is_last else "│  "), i == len(children) - 1)


def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · CNSH知识图谱引擎 v2.0",
        epilog=f"DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-KNOWLEDGE-GRAPH-V2-UID9622"
    )
    parser.add_argument("--init", action="store_true", help="初始化知识图谱(60领域·幂等)")
    parser.add_argument("--list", action="store_true", help="列出所有知识节点")
    parser.add_argument("--list-tiancai", type=str, choices=["天", "地", "人"], help="列出指定三才分类")
    parser.add_argument("--search", type=str, help="搜索知识节点(名称/ID/关键词)")
    parser.add_argument("--tree", type=str, help="显示知识树(节点名称或ID)")
    parser.add_argument("--path", type=str, help="显示节点根路径(名称或ID)")
    parser.add_argument("--mermaid", type=str, help="生成Mermaid知识树(名称或ID)")
    parser.add_argument("--clipboard", type=str, help="导出节点到剪贴板格式(名称或ID)")
    parser.add_argument("--repair", action="store_true", help="检测需要修复的知识节点")
    parser.add_argument("--export", action="store_true", help="导出CNSH知识")
    parser.add_argument("--export-md", action="store_true", help="导出Markdown知识索引")
    parser.add_argument("--export-json", action="store_true", help="导出JSON全量数据")
    parser.add_argument("--server", type=int, nargs="?", const=8767, help="启动API服务(端口, 默认8767)")
    parser.add_argument("--status", action="store_true", help="显示系统状态")
    parser.add_argument("key", nargs="?", help="直接输入关键词 = 搜索（快捷用法）")

    args = parser.parse_args()

    engine = KnowledgeGraphEngine()
    exporter = CNSHKnowledgeExporter()
    repair = KnowledgeRepairInterface(engine)

    # 快捷用法: 直接传裸词 = 搜索
    if args.key and not any([args.init, args.list, args.list_tiancai, args.search,
                             args.tree, args.path, args.mermaid, args.clipboard,
                             args.repair, args.export, args.export_md, args.export_json,
                             args.server is not None, args.status]):
        args.search = args.key
        args.key = None

    if args.init:
        initialize_knowledge_graph(engine)
        return

    if args.server is not None:
        run_api_server(engine, args.server)
        return

    if args.export:
        cnsh_code = exporter.export_to_cnsh(engine)
        output_file = KNOWLEDGE_DIR / f"knowledge_export_{datetime.now().strftime('%Y%m%d')}.cnsh"
        output_file.write_text(cnsh_code, encoding="utf-8")
        try:
            (ARCHIVE_DIR / f"knowledge_export_{datetime.now().strftime('%Y%m%d')}.cnsh").write_text(
                cnsh_code, encoding="utf-8")
        except Exception:
            pass
        print(f"✅ CNSH知识已导出: {output_file}")
        return

    if args.export_md:
        md_code = exporter.export_to_markdown(engine)
        output_file = KNOWLEDGE_DIR / "knowledge_index.md"
        output_file.write_text(md_code, encoding="utf-8")
        print(f"✅ Markdown索引已导出: {output_file}")
        return

    if args.export_json:
        data = exporter.export_to_json(engine)
        output_file = KNOWLEDGE_DIR / f"knowledge_export_{datetime.now().strftime('%Y%m%d')}.json"
        output_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"✅ JSON全量已导出: {output_file}")
        return

    if args.clipboard:
        node = engine.resolve(args.clipboard)
        if not node:
            print(f"❌ 节点 {args.clipboard} 不存在")
            return
        content = engine.export_to_clipboard(node.id)
        print(content)
        CLIPBOARD_OUTPUT.write_text(content, encoding="utf-8")
        print(f"✅ 已导出到剪贴板文件: {CLIPBOARD_OUTPUT}")
        return

    if args.tree:
        node = engine.resolve(args.tree)
        if not node:
            print(f"❌ 节点 {args.tree} 不存在")
            return
        print(f"🐉 知识树: {node.name}")
        print("=" * 50)
        _print_tree_pretty(engine, engine.get_tree(node.id, depth=4))
        return

    if args.mermaid:
        node = engine.resolve(args.mermaid)
        if not node:
            print(f"❌ 节点 {args.mermaid} 不存在")
            return
        print(engine.get_tree_mermaid(node.id, depth=5))
        return

    if args.path:
        node = engine.resolve(args.path)
        if not node:
            print(f"❌ 节点 {args.path} 不存在")
            return
        path = engine.get_path(node.id)
        print(" → ".join(path))
        return

    if args.list:
        print("🐉 知识节点列表")
        print("=" * 50)
        for node in sorted(engine.nodes.values(), key=lambda x: (x.tiancai, x.domain_id)):
            print(f"{node.id} [{node.tiancai}] {node.name}{f' ({node.domain_id})' if node.domain_id else ''}")
        print(f"总计: {len(engine.nodes)} 个节点")
        return

    if args.list_tiancai:
        nodes = engine.get_by_tiancai(args.list_tiancai)
        print(f"🐉 {args.list_tiancai}层: {TIANCAI_DESC.get(args.list_tiancai, '')}")
        print("=" * 50)
        for node in sorted(nodes, key=lambda x: x.domain_id):
            print(f"{node.id} {node.name}{f' ({node.domain_id})' if node.domain_id else ''}")
        print(f"总计: {len(nodes)} 个节点")
        return

    if args.search:
        results = engine.search(args.search)
        print(f"🔍 搜索 '{args.search}': 找到 {len(results)} 个结果")
        print("=" * 50)
        for node in results:
            print(f"{node.id} [{node.tiancai}]{f' ({node.domain_id})' if node.domain_id else ''} {node.name}")
            if node.description:
                print(f"  {node.description[:100]}")
        return

    if args.repair:
        report = repair.get_repair_report()
        print("🔧 知识修复报告")
        print("=" * 50)
        print(f"待修复建议: {report['total_suggestions']}")
        print(f"严重问题: {len(report['critical'])}")
        print(f"轻微问题: {len(report['minor'])}")
        if report["suggestions"]:
            print("\n详情:")
            for s in report["suggestions"][:15]:
                print(f"\n  {s['name']} ({s['node_id']})")
                for issue in s["issues"]:
                    print(f"    ⚠️ {issue}")
                for fix in s["suggested_fixes"]:
                    print(f"    🔧 {fix}")
        return

    if args.status:
        print("🐉 知识图谱状态")
        print("=" * 40)
        print(f"总节点: {len(engine.nodes)}")
        print(f"  🌌 天层: {len(engine.get_by_tiancai('天'))}")
        print(f"  🌍 地层: {len(engine.get_by_tiancai('地'))}")
        print(f"  🌊 人层: {len(engine.get_by_tiancai('人'))}")
        print(f"索引文件: {INDEX_FILE}")
        print(f"CNSH导出: {CNSH_OUTPUT}")
        print(f"API服务: 未启动 (--server 8767)")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
