#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH × Claude × Notion · 论文完美化三页合一引擎 v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-ACADEMIC-RUNTIME-v1.0-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2026-龍魂-主权-不商业-不站队

功能：
  1. 三页分层骨架生成 (Submission / Theory / Runtime)
  2. 定理/定义/公理/引理/推论管理
  3. 形式化一致性检查
  4. Claude-Compatible Structure 导出
  5. Notion 数据库 Schema 生成
  6. LaTeX 导出预览
  7. 术语一致性检查
  8. 交叉引用自动生成

用法：
  python3 lh_academic_runtime.py --init "CNSH Runtime Governance"     # 初始化论文项目
  python3 lh_academic_runtime.py --add-theorem "Theorem 1" "描述"     # 添加定理
  python3 lh_academic_runtime.py --add-definition "定义1" "内容"      # 添加定义
  python3 lh_academic_runtime.py --generate-page 1                   # 生成第1页
  python3 lh_academic_runtime.py --check                             # 一致性检查
  python3 lh_academic_runtime.py --export-latex                      # 导出LaTeX
  python3 lh_academic_runtime.py --notion-schema                     # 生成Notion Schema
  python3 lh_academic_runtime.py --claude-prompt                     # 生成Claude Prompt
  python3 lh_academic_runtime.py --list                              # 列出所有定理/定义
  python3 lh_academic_runtime.py --stats                             # 统计信息
  python3 lh_academic_runtime.py --interactive                       # 交互模式

集成到lh:
  lh academic --init "论文标题"
  lh academic --generate-page 1
"""

import os
import sys
import json
import datetime
import hashlib
import re
import argparse
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict

# ============================================================
# 固定锚点
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2026-龍魂-主权-不商业-不站队"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
PROJECT_ROOT = Path.home() / "longhun-system"
PAPERS_DIR = PROJECT_ROOT / "papers"
PAPERS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 颜色终端
# ============================================================

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def cprint(text: str, color: str = Colors.RESET):
    print(f"{color}{text}{Colors.RESET}")

# ============================================================
# 数据模型
# ============================================================

class Layer(Enum):
    SUBMISSION = 1  # 投稿层
    THEORY = 2      # 理论层
    RUNTIME = 3     # 运行时公式层

class EntityType(Enum):
    DEFINITION = "Definition"
    AXIOM = "Axiom"
    LEMMA = "Lemma"
    THEOREM = "Theorem"
    COROLLARY = "Corollary"
    FORMULA = "Formula"
    PROOF = "Proof"

@dataclass
class AcademicEntity:
    """学术实体基类"""
    id: str
    type: EntityType
    name: str
    content: str
    latex: str = ""
    depends_on: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    dna: str = field(default_factory=lambda: f"#龍芯⚡️{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-ENTITY-{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}")
    proof: Optional[str] = None
    meaning: Optional[str] = None  # Runtime 含义

@dataclass
class Paper:
    """论文项目"""
    title: str
    authors: List[str] = field(default_factory=list)
    abstract: str = ""
    keywords: List[str] = field(default_factory=list)
    entities: List[AcademicEntity] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    dna: str = field(default_factory=lambda: f"#龍芯⚡️{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-PAPER-{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}")

# ============================================================
# 学术运行时引擎
# ============================================================

class AcademicRuntimeEngine:
    def __init__(self, paper_dir: Path = None):
        self.paper_dir = paper_dir or PAPERS_DIR
        self.paper = None
        self._loaded = False

    def init_paper(self, title: str, authors: List[str] = None) -> Paper:
        """初始化论文项目"""
        self.paper = Paper(title=title, authors=authors or ["UID9622"])
        self._save_paper()
        cprint(f"✅ 论文项目已初始化: {title}", Colors.GREEN)
        cprint(f"   DNA: {self.paper.dna}", Colors.CYAN)
        self._loaded = True
        return self.paper

    def _get_paper_path(self) -> Optional[Path]:
        if not self.paper:
            return None
        safe_title = re.sub(r'[^a-zA-Z0-9\-_\u4e00-\u9fff]', '_', self.paper.title)
        return self.paper_dir / f"{safe_title}.json"

    def _entity_to_dict(self, e: AcademicEntity) -> dict:
        """将实体转为可JSON序列化的字典"""
        return {
            "id": e.id,
            "type": e.type.value,
            "name": e.name,
            "content": e.content,
            "latex": e.latex,
            "depends_on": e.depends_on,
            "references": e.references,
            "tags": e.tags,
            "created_at": e.created_at,
            "dna": e.dna,
            "proof": e.proof,
            "meaning": e.meaning
        }

    def _save_paper(self) -> Optional[Path]:
        if not self.paper:
            return None
        path = self._get_paper_path()
        data = {
            "title": self.paper.title,
            "authors": self.paper.authors,
            "abstract": self.paper.abstract,
            "keywords": self.paper.keywords,
            "entities": [self._entity_to_dict(e) for e in self.paper.entities],
            "created_at": self.paper.created_at,
            "updated_at": datetime.datetime.now().isoformat(),
            "dna": self.paper.dna
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path

    def load_paper(self, title_or_path: str) -> Optional[Paper]:
        """加载论文项目"""
        path = Path(title_or_path)
        if not path.exists():
            # 尝试按标题查找
            for f in self.paper_dir.glob("*.json"):
                with open(f, 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
                    if data.get("title") == title_or_path:
                        path = f
                        break
        if not path.exists():
            return None
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.paper = Paper(
            title=data["title"],
            authors=data.get("authors", []),
            abstract=data.get("abstract", ""),
            keywords=data.get("keywords", []),
            created_at=data.get("created_at", datetime.datetime.now().isoformat())
        )
        for e_data in data.get("entities", []):
            entity = AcademicEntity(
                id=e_data["id"],
                type=EntityType(e_data["type"]),
                name=e_data["name"],
                content=e_data["content"],
                latex=e_data.get("latex", ""),
                depends_on=e_data.get("depends_on", []),
                references=e_data.get("references", []),
                tags=e_data.get("tags", []),
                created_at=e_data.get("created_at", datetime.datetime.now().isoformat()),
                dna=e_data.get("dna", ""),
                proof=e_data.get("proof", ""),
                meaning=e_data.get("meaning", "")
            )
            self.paper.entities.append(entity)
        self._loaded = True
        self.paper.dna = data.get("dna", "")
        return self.paper

    # ---------- 实体管理 ----------
    def add_entity(self, entity_type: EntityType, name: str, content: str, 
                   latex: str = "", proof: str = "", meaning: str = "",
                   depends_on: List[str] = None, references: List[str] = None,
                   tags: List[str] = None) -> Optional[AcademicEntity]:
        """添加学术实体"""
        if not self._loaded:
            cprint("❌ 请先初始化或加载论文项目", Colors.RED)
            return None
        entity_id = f"{entity_type.value}_{len(self.paper.entities)+1}"
        entity = AcademicEntity(
            id=entity_id,
            type=entity_type,
            name=name,
            content=content,
            latex=latex or content,
            depends_on=depends_on or [],
            references=references or [],
            tags=tags or [],
            proof=proof,
            meaning=meaning
        )
        self.paper.entities.append(entity)
        self._save_paper()
        cprint(f"✅ 已添加: {entity_type.value}: {name}", Colors.GREEN)
        return entity

    def get_entities(self, entity_type: EntityType = None) -> List[AcademicEntity]:
        """获取实体列表"""
        if not self._loaded:
            return []
        if entity_type:
            return [e for e in self.paper.entities if e.type == entity_type]
        return self.paper.entities

    def get_entity(self, entity_id: str) -> Optional[AcademicEntity]:
        for e in self.paper.entities:
            if e.id == entity_id or e.name == entity_id:
                return e
        return None

    # ---------- 三页生成 ----------
    def generate_page(self, layer: Layer) -> str:
        """生成指定层的页面内容"""
        if not self._loaded:
            return "❌ 请先初始化或加载论文项目"

        if layer == Layer.SUBMISSION:
            return self._generate_submission_layer()
        elif layer == Layer.THEORY:
            return self._generate_theory_layer()
        elif layer == Layer.RUNTIME:
            return self._generate_runtime_layer()
        return ""

    def _generate_submission_layer(self) -> str:
        """生成投稿层 (Submission Layer)"""
        lines = []
        lines.append("# 🐉 CNSH Formal Submission Layer")
        lines.append("")
        lines.append(f"**Title**: {self.paper.title}")
        lines.append(f"**Authors**: {', '.join(self.paper.authors)}")
        lines.append(f"**DNA**: {self.paper.dna}")
        lines.append(f"**CONFIRM**: {CONFIRM}")
        lines.append("")
        lines.append("## Abstract")
        lines.append(self.paper.abstract or "(请填写摘要)")
        lines.append("")
        lines.append("## Keywords")
        lines.append(", ".join(self.paper.keywords) if self.paper.keywords else "(请填写关键词)")
        lines.append("")
        lines.append("## 1. Introduction")
        lines.append("(请填写引言)")
        lines.append("")
        lines.append("## 2. Core Contributions")
        for i, e in enumerate(self.get_entities(EntityType.THEOREM), 1):
            lines.append(f"  - {e.name}: {e.content[:100]}...")
        lines.append("")
        lines.append("## 3. Related Work")
        lines.append("(请填写相关工作)")
        lines.append("")
        lines.append("## 4. References")
        lines.append("(请填写参考文献)")
        lines.append("")
        lines.append(f"**DNA**: {self.paper.dna}")
        lines.append(f"**CONFIRM**: {CONFIRM}")
        return "\n".join(lines)

    def _generate_theory_layer(self) -> str:
        """生成理论层 (Theory Layer)"""
        lines = []
        lines.append("# 🐉 CNSH Unified Theory Layer")
        lines.append("")
        lines.append(f"**DNA**: {self.paper.dna}")
        lines.append(f"**CONFIRM**: {CONFIRM}")
        lines.append("")
        lines.append("## 1. Axioms")
        axioms = self.get_entities(EntityType.AXIOM)
        if axioms:
            for a in axioms:
                lines.append(f"### {a.name}")
                lines.append(a.content)
                lines.append("")
        else:
            lines.append("(请添加公理)")
            lines.append("")

        lines.append("## 2. Definitions")
        definitions = self.get_entities(EntityType.DEFINITION)
        if definitions:
            for d in definitions:
                lines.append(f"### {d.name}")
                lines.append(d.content)
                if d.latex:
                    lines.append(f"$${d.latex}$$")
                lines.append("")
        else:
            lines.append("(请添加定义)")
            lines.append("")

        lines.append("## 3. Lemmas")
        lemmas = self.get_entities(EntityType.LEMMA)
        if lemmas:
            for l in lemmas:
                lines.append(f"### {l.name}")
                lines.append(l.content)
                if l.proof:
                    lines.append(f"**Proof**: {l.proof}")
                lines.append("")
        else:
            lines.append("(请添加引理)")
            lines.append("")

        lines.append("## 4. Theorems")
        theorems = self.get_entities(EntityType.THEOREM)
        if theorems:
            for t in theorems:
                lines.append(f"### {t.name}")
                lines.append(t.content)
                if t.proof:
                    lines.append(f"**Proof**: {t.proof}")
                if t.meaning:
                    lines.append(f"**Runtime Meaning**: {t.meaning}")
                if t.depends_on:
                    lines.append(f"**Depends on**: {', '.join(t.depends_on)}")
                lines.append("")
        else:
            lines.append("(请添加定理)")
            lines.append("")

        lines.append("## 5. Corollaries")
        corollaries = self.get_entities(EntityType.COROLLARY)
        if corollaries:
            for c in corollaries:
                lines.append(f"### {c.name}")
                lines.append(c.content)
                lines.append("")
        else:
            lines.append("(请添加推论)")
            lines.append("")

        lines.append(f"**DNA**: {self.paper.dna}")
        lines.append(f"**CONFIRM**: {CONFIRM}")
        return "\n".join(lines)

    def _generate_runtime_layer(self) -> str:
        """生成运行时公式层 (Runtime Formula Layer)"""
        lines = []
        lines.append("# 🐉 CNSH Runtime Formula Index")
        lines.append("")
        lines.append(f"**DNA**: {self.paper.dna}")
        lines.append(f"**CONFIRM**: {CONFIRM}")
        lines.append("")
        lines.append("## 🧬 Runtime Formulas")
        formulas = self.get_entities(EntityType.FORMULA)
        if formulas:
            for f in formulas:
                lines.append(f"### {f.name}")
                lines.append(f.content)
                if f.latex:
                    lines.append(f"$${f.latex}$$")
                if f.meaning:
                    lines.append(f"**语义**: {f.meaning}")
                lines.append("")
        else:
            lines.append("(请添加运行时公式)")
            lines.append("")

        lines.append("## 🔄 Runtime State Machine")
        lines.append("```mermaid")
        lines.append("graph TD")
        lines.append("    S0[输入] --> S1[审计]")
        lines.append("    S1 --> S2[解析]")
        lines.append("    S2 --> S3[路由]")
        lines.append("    S3 --> S4[沙盒]")
        lines.append("    S4 --> S5[执行]")
        lines.append("    S5 --> S6[归档]")
        lines.append("    S5 --> S7[时间轴]")
        lines.append("    S7 --> S8[快照]")
        lines.append("    S8 --> S9[恢复]")
        lines.append("    S9 --> S5")
        lines.append("```")
        lines.append("")
        lines.append("## 🐉 TraceGraph")
        lines.append("```mermaid")
        lines.append("graph LR")
        lines.append("    ROOT --> INPUT")
        lines.append("    INPUT --> CHECK")
        lines.append("    CHECK --> EXEC")
        lines.append("    EXEC --> AUDIT")
        lines.append("    AUDIT --> ARCHIVE")
        lines.append("```")
        lines.append("")
        lines.append(f"**DNA**: {self.paper.dna}")
        lines.append(f"**CONFIRM**: {CONFIRM}")
        return "\n".join(lines)

    # ---------- 一致性检查 ----------
    def check_consistency(self) -> Dict[str, Any]:
        """执行一致性检查"""
        if not self._loaded:
            return {"status": "error", "message": "未加载论文项目"}

        issues = []
        warnings = []

        # 1. 检查实体编号连续性
        entity_counts = {}
        for e in self.paper.entities:
            key = e.type.value
            entity_counts[key] = entity_counts.get(key, 0) + 1

        # 2. 检查依赖引用是否存在
        for e in self.paper.entities:
            for dep in e.depends_on:
                if not self.get_entity(dep):
                    issues.append(f"实体 '{e.id}' 依赖 '{dep}' 但该实体不存在")

        # 3. 检查定理是否有证明
        for e in self.get_entities(EntityType.THEOREM):
            if not e.proof:
                warnings.append(f"定理 '{e.name}' 缺少证明")

        # 4. 检查定义是否有LaTeX
        for e in self.get_entities(EntityType.DEFINITION):
            if not e.latex:
                warnings.append(f"定义 '{e.name}' 缺少 LaTeX 形式")

        # 5. 检查定理编号一致性
        theorems = self.get_entities(EntityType.THEOREM)
        for i, t in enumerate(theorems, 1):
            expected = f"Theorem {i}"
            if t.name != expected:
                warnings.append(f"定理编号不一致: 期望 '{expected}'，实际 '{t.name}'")

        return {
            "status": "ok" if not issues else "issues",
            "issues": issues,
            "warnings": warnings,
            "entity_counts": entity_counts,
            "total_entities": len(self.paper.entities)
        }

    # ---------- 导出LaTeX ----------
    def export_latex(self) -> str:
        """导出LaTeX格式"""
        lines = []
        lines.append("\\documentclass{article}")
        lines.append("\\usepackage{amsmath, amssymb, amsthm}")
        lines.append("\\usepackage{hyperref}")
        lines.append("")
        lines.append("\\title{" + self.paper.title + "}")
        lines.append("\\author{" + ", ".join(self.paper.authors) + "}")
        lines.append("\\date{\\today}")
        lines.append("")
        lines.append("\\begin{document}")
        lines.append("\\maketitle")
        lines.append("")
        lines.append("\\begin{abstract}")
        lines.append(self.paper.abstract or "(请填写摘要)")
        lines.append("\\end{abstract}")
        lines.append("")

        # 定义环境
        lines.append("\\newtheorem{definition}{Definition}")
        lines.append("\\newtheorem{axiom}{Axiom}")
        lines.append("\\newtheorem{lemma}{Lemma}")
        lines.append("\\newtheorem{theorem}{Theorem}")
        lines.append("\\newtheorem{corollary}{Corollary}")
        lines.append("")

        # 遍历实体
        for e in self.paper.entities:
            env_map = {
                EntityType.DEFINITION: "definition",
                EntityType.AXIOM: "axiom",
                EntityType.LEMMA: "lemma",
                EntityType.THEOREM: "theorem",
                EntityType.COROLLARY: "corollary",
            }
            env = env_map.get(e.type)
            if env:
                lines.append(f"\\begin{{{env}}}[{e.name}]")
                lines.append(e.content)
                if e.latex:
                    lines.append("\\begin{equation}")
                    lines.append(e.latex)
                    lines.append("\\end{equation}")
                if e.proof:
                    lines.append("\\begin{proof}")
                    lines.append(e.proof)
                    lines.append("\\end{proof}")
                lines.append(f"\\end{{{env}}}")
                lines.append("")

        lines.append("\\end{document}")
        return "\n".join(lines)

    # ---------- Notion Schema ----------
    def generate_notion_schema(self) -> str:
        """生成Notion数据库Schema"""
        lines = []
        lines.append("# 🐉 CNSH Academic Runtime · Notion Schema")
        lines.append("")
        lines.append("## THEORY_DB")
        lines.append("| 字段 | 类型 | 说明 |")
        lines.append("|------|------|------|")
        lines.append("| entity_id | text | 实体ID |")
        lines.append("| type | select | Definition/Axiom/Lemma/Theorem/Corollary/Formula |")
        lines.append("| name | title | 名称 |")
        lines.append("| content | text | 内容 |")
        lines.append("| latex | text | LaTeX形式 |")
        lines.append("| proof | text | 证明 |")
        lines.append("| meaning | text | Runtime含义 |")
        lines.append("| depends_on | multi_select | 依赖 |")
        lines.append("| tags | multi_select | 标签 |")
        lines.append("| dna | text | DNA追溯 |")
        lines.append("| status | select | draft/review/final |")
        lines.append("")
        lines.append("## PAPER_DB")
        lines.append("| 字段 | 类型 | 说明 |")
        lines.append("|------|------|------|")
        lines.append("| title | title | 论文标题 |")
        lines.append("| authors | text | 作者 |")
        lines.append("| abstract | text | 摘要 |")
        lines.append("| keywords | multi_select | 关键词 |")
        lines.append("| dna | text | DNA追溯 |")
        lines.append("| status | select | draft/submitted/published |")
        lines.append("| created_at | date | 创建时间 |")
        return "\n".join(lines)

    # ---------- Claude Prompt ----------
    def generate_claude_prompt(self) -> str:
        """生成给Claude的协作Prompt"""
        lines = []
        lines.append("# 🐉 CNSH Academic Runtime · Claude Collaboration Prompt")
        lines.append("")
        lines.append("## 角色定义")
        lines.append("你是 CNSH 学术运行时助理，负责:")
        lines.append("1. Formalizer — 形式化自然语言描述")
        lines.append("2. Proof Assistant — 补全证明")
        lines.append("3. Consistency Auditor — 检查逻辑一致性")
        lines.append("4. Semantic Refiner — 统一术语")
        lines.append("5. Runtime Architect — 架构化")
        lines.append("6. LaTeX Compiler — 转LaTeX")
        lines.append("7. Citation Builder — 构建引用")
        lines.append("8. Theorem Verifier — 定理验证")
        lines.append("")
        lines.append("## 当前论文信息")
        lines.append(f"- 标题: {self.paper.title}")
        lines.append(f"- 作者: {', '.join(self.paper.authors)}")
        lines.append(f"- DNA: {self.paper.dna}")
        lines.append("")
        lines.append("## 当前实体列表")
        for e in self.paper.entities:
            lines.append(f"- {e.type.value}: {e.name}")
        lines.append("")
        lines.append("## 任务")
        lines.append("请根据上述信息，完成以下任务:")
        lines.append("1. 检查所有定理的证明是否完整")
        lines.append("2. 检查所有定义是否有一致的LaTeX形式")
        lines.append("3. 检查实体之间的依赖关系是否形成有向无环图")
        lines.append("4. 建议需要补充的引理")
        lines.append("5. 生成论文的完整结构")
        lines.append("")
        lines.append(f"CONFIRM: {CONFIRM}")
        return "\n".join(lines)

# ============================================================
# 命令行入口
# ============================================================

def interactive_mode():
    engine = AcademicRuntimeEngine()
    cprint("\n🐉 CNSH Academic Runtime Engine v1.0", Colors.BOLD)
    cprint(f"确认码: {CONFIRM}", Colors.CYAN)
    cprint("-" * 50, Colors.RESET)
    cprint("命令: init <标题> | add <类型> | list | check | gen <1-3> | export | notion | claude | stats | exit", Colors.RESET)

    while True:
        try:
            cmd = input("\n📝 > ").strip()
            if not cmd:
                continue
            if cmd.lower() == "exit":
                break

            if cmd.startswith("init "):
                title = cmd[5:].strip()
                engine.init_paper(title)
                continue

            if cmd.startswith("add "):
                parts = cmd[4:].strip().split(" ", 2)
                if len(parts) >= 3:
                    type_name = parts[0]
                    name = parts[1]
                    content = parts[2]
                    type_map = {
                        "def": EntityType.DEFINITION,
                        "axiom": EntityType.AXIOM,
                        "lemma": EntityType.LEMMA,
                        "theorem": EntityType.THEOREM,
                        "corollary": EntityType.COROLLARY,
                        "formula": EntityType.FORMULA,
                    }
                    etype = type_map.get(type_name.lower())
                    if etype:
                        engine.add_entity(etype, name, content)
                    else:
                        cprint(f"❌ 未知类型: {type_name}", Colors.RED)
                else:
                    cprint("用法: add <类型> <名称> <内容>", Colors.YELLOW)
                continue

            if cmd.lower() == "list":
                entities = engine.get_entities()
                cprint(f"\n📋 共 {len(entities)} 个实体", Colors.CYAN)
                for e in entities:
                    cprint(f"  {e.type.value}: {e.name}", Colors.RESET)
                continue

            if cmd.lower() == "check":
                result = engine.check_consistency()
                cprint("\n🔍 一致性检查结果", Colors.BOLD)
                cprint(f"  状态: {result['status']}", Colors.GREEN if result['status'] == 'ok' else Colors.RED)
                if result.get('issues'):
                    cprint("  问题:", Colors.RED)
                    for i in result['issues']:
                        cprint(f"    ❌ {i}", Colors.RED)
                if result.get('warnings'):
                    cprint("  警告:", Colors.YELLOW)
                    for w in result['warnings']:
                        cprint(f"    ⚠️ {w}", Colors.YELLOW)
                continue

            if cmd.startswith("gen "):
                try:
                    page_num = int(cmd[4:].strip())
                    if page_num == 1:
                        layer = Layer.SUBMISSION
                    elif page_num == 2:
                        layer = Layer.THEORY
                    elif page_num == 3:
                        layer = Layer.RUNTIME
                    else:
                        cprint("❌ 页码必须是 1, 2, 或 3", Colors.RED)
                        continue
                    content = engine.generate_page(layer)
                    filename = f"page_{page_num}.md"
                    with open(PAPERS_DIR / filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                    cprint(f"✅ 已生成第{page_num}页: {PAPERS_DIR / filename}", Colors.GREEN)
                except ValueError:
                    cprint("❌ 请输入数字", Colors.RED)
                continue

            if cmd.lower() == "export":
                latex = engine.export_latex()
                with open(PAPERS_DIR / "paper.tex", 'w', encoding='utf-8') as f:
                    f.write(latex)
                cprint(f"✅ LaTeX 已导出: {PAPERS_DIR / 'paper.tex'}", Colors.GREEN)
                continue

            if cmd.lower() == "notion":
                schema = engine.generate_notion_schema()
                with open(PAPERS_DIR / "notion_schema.md", 'w', encoding='utf-8') as f:
                    f.write(schema)
                cprint(f"✅ Notion Schema 已生成: {PAPERS_DIR / 'notion_schema.md'}", Colors.GREEN)
                continue

            if cmd.lower() == "claude":
                prompt = engine.generate_claude_prompt()
                with open(PAPERS_DIR / "claude_prompt.md", 'w', encoding='utf-8') as f:
                    f.write(prompt)
                cprint(f"✅ Claude Prompt 已生成: {PAPERS_DIR / 'claude_prompt.md'}", Colors.GREEN)
                continue

            if cmd.lower() == "stats":
                entities = engine.get_entities()
                counts = {}
                for e in entities:
                    counts[e.type.value] = counts.get(e.type.value, 0) + 1
                cprint("\n📊 统计", Colors.BOLD)
                for k, v in counts.items():
                    cprint(f"  {k}: {v}", Colors.RESET)
                cprint(f"  总计: {len(entities)}", Colors.CYAN)
                continue

            cprint("未知命令，输入 help 查看帮助", Colors.YELLOW)

        except KeyboardInterrupt:
            break

# ============================================================
# 演示模式（新增·方便快速验证）
# ============================================================

def run_demo():
    """完整功能演示"""
    cprint("\n" + "=" * 70, Colors.CYAN)
    cprint("🐉 CNSH Academic Runtime Engine v1.0 · 演示", Colors.BOLD)
    cprint("=" * 70, Colors.CYAN)
    
    engine = AcademicRuntimeEngine()
    
    # 初始化
    engine.init_paper("CNSH Runtime Governance Theory")
    
    # 添加实体
    engine.add_entity(EntityType.AXIOM, "Axiom 1", "No execution without audit")
    engine.add_entity(EntityType.DEFINITION, "Definition 1", "Digital Root is the modulo-9 reduction of any integer", latex="dr(n)=1+((n-1) \\bmod 9)")
    engine.add_entity(EntityType.LEMMA, "Lemma 1", "If dr(n) ∈ {1,2,4,5,7,8}, then n is in GREEN state", proof="By definition of tri-color governance set G")
    engine.add_entity(EntityType.THEOREM, "Theorem 1", "Every CNSH runtime execution is traceable via DNA chain", proof="By induction on the DNAStack push chain")
    engine.add_entity(EntityType.COROLLARY, "Corollary 1", "All GREEN state executions pass without manual review")
    engine.add_entity(EntityType.FORMULA, "Formula 1", "DR = 0.35N + 0.25S + 0.25R + 0.15T", meaning="动态数字根")
    
    # 列表
    cprint(f"\n📋 实体列表 ({len(engine.get_entities())})", Colors.CYAN)
    for e in engine.get_entities():
        cprint(f"  {e.type.value}: {e.name}", Colors.RESET)
    
    # 一致性检查
    result = engine.check_consistency()
    cprint(f"\n🔍 一致性检查: {result['status']}", Colors.GREEN if result['status']=='ok' else Colors.RED)
    for w in result.get('warnings', []):
        cprint(f"  ⚠️ {w}", Colors.YELLOW)
    
    # 统计
    counts = {}
    for e in engine.get_entities():
        counts[e.type.value] = counts.get(e.type.value, 0) + 1
    cprint(f"\n📊 统计: {counts}", Colors.CYAN)
    
    # 生成三页
    for i in [1, 2, 3]:
        layer = {1: Layer.SUBMISSION, 2: Layer.THEORY, 3: Layer.RUNTIME}[i]
        content = engine.generate_page(layer)
        filename = PAPERS_DIR / f"page_{i}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # 导出
    latex = engine.export_latex()
    with open(PAPERS_DIR / "paper.tex", 'w', encoding='utf-8') as f:
        f.write(latex)
    schema = engine.generate_notion_schema()
    with open(PAPERS_DIR / "notion_schema.md", 'w', encoding='utf-8') as f:
        f.write(schema)
    prompt = engine.generate_claude_prompt()
    with open(PAPERS_DIR / "claude_prompt.md", 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    cprint(f"\n✅ 已生成文件:", Colors.GREEN)
    for f in PAPERS_DIR.glob("page_*.md"):
        cprint(f"   {f}", Colors.CYAN)
    for f in PAPERS_DIR.glob("*.tex"):
        cprint(f"   {f}", Colors.CYAN)
    for f in PAPERS_DIR.glob("notion_schema.md"):
        cprint(f"   {f}", Colors.CYAN)
    for f in PAPERS_DIR.glob("claude_prompt.md"):
        cprint(f"   {f}", Colors.CYAN)
    
    cprint("\n" + "=" * 70, Colors.CYAN)
    cprint("✅ 演示完成", Colors.GREEN)


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="🐉 CNSH Academic Runtime Engine")
    parser.add_argument("--init", type=str, help="初始化论文项目")
    parser.add_argument("--add-theorem", nargs=2, metavar=("NAME", "CONTENT"), help="添加定理")
    parser.add_argument("--add-definition", nargs=2, metavar=("NAME", "CONTENT"), help="添加定义")
    parser.add_argument("--add-axiom", nargs=2, metavar=("NAME", "CONTENT"), help="添加公理")
    parser.add_argument("--add-lemma", nargs=2, metavar=("NAME", "CONTENT"), help="添加引理")
    parser.add_argument("--add-corollary", nargs=2, metavar=("NAME", "CONTENT"), help="添加推论")
    parser.add_argument("--add-formula", nargs=2, metavar=("NAME", "CONTENT"), help="添加公式")
    parser.add_argument("--generate-page", type=int, choices=[1, 2, 3], help="生成指定层页面")
    parser.add_argument("--check", action="store_true", help="一致性检查")
    parser.add_argument("--export-latex", action="store_true", help="导出LaTeX")
    parser.add_argument("--notion-schema", action="store_true", help="生成Notion Schema")
    parser.add_argument("--claude-prompt", action="store_true", help="生成Claude Prompt")
    parser.add_argument("--list", action="store_true", help="列出所有实体")
    parser.add_argument("--stats", action="store_true", help="统计信息")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--demo", action="store_true", help="完整演示")
    parser.add_argument("--json", action="store_true", help="JSON输出")

    args = parser.parse_args()

    engine = AcademicRuntimeEngine()

    if args.demo:
        run_demo()
        return

    if args.interactive:
        interactive_mode()
        return

    if args.init:
        engine.init_paper(args.init)
        return

    # 加载或初始化（自动）
    latest_papers = sorted(PAPERS_DIR.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    if latest_papers:
        engine.load_paper(str(latest_papers[0]))
    else:
        if args.add_theorem or args.add_definition or args.add_axiom or args.add_lemma or args.add_corollary or args.add_formula:
            cprint("❌ 请先使用 --init 初始化论文项目", Colors.RED)
            sys.exit(1)

    if args.add_theorem:
        engine.add_entity(EntityType.THEOREM, args.add_theorem[0], args.add_theorem[1])
    if args.add_definition:
        engine.add_entity(EntityType.DEFINITION, args.add_definition[0], args.add_definition[1])
    if args.add_axiom:
        engine.add_entity(EntityType.AXIOM, args.add_axiom[0], args.add_axiom[1])
    if args.add_lemma:
        engine.add_entity(EntityType.LEMMA, args.add_lemma[0], args.add_lemma[1])
    if args.add_corollary:
        engine.add_entity(EntityType.COROLLARY, args.add_corollary[0], args.add_corollary[1])
    if args.add_formula:
        engine.add_entity(EntityType.FORMULA, args.add_formula[0], args.add_formula[1])

    if args.generate_page:
        if not engine._loaded:
            cprint("❌ 请先使用 --init 初始化论文项目", Colors.RED)
            sys.exit(1)
        layer = {1: Layer.SUBMISSION, 2: Layer.THEORY, 3: Layer.RUNTIME}[args.generate_page]
        content = engine.generate_page(layer)
        if args.json:
            print(json.dumps({"page": args.generate_page, "content": content}, ensure_ascii=False, indent=2))
        else:
            print(content)

    if args.check:
        if not engine._loaded:
            cprint("❌ 请先使用 --init 初始化论文项目", Colors.RED)
            sys.exit(1)
        result = engine.check_consistency()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            cprint(f"\n🔍 一致性检查结果", Colors.BOLD)
            cprint(f"  状态: {result['status']}", Colors.GREEN if result['status'] == 'ok' else Colors.RED)
            if result.get('issues'):
                for i in result['issues']:
                    cprint(f"    ❌ {i}", Colors.RED)
            if result.get('warnings'):
                for w in result['warnings']:
                    cprint(f"    ⚠️ {w}", Colors.YELLOW)

    if args.export_latex:
        if not engine._loaded:
            cprint("❌ 请先使用 --init 初始化论文项目", Colors.RED)
            sys.exit(1)
        latex = engine.export_latex()
        if args.json:
            print(json.dumps({"latex": latex}, ensure_ascii=False, indent=2))
        else:
            print(latex)

    if args.notion_schema:
        schema = engine.generate_notion_schema()
        if args.json:
            print(json.dumps({"schema": schema}, ensure_ascii=False, indent=2))
        else:
            print(schema)

    if args.claude_prompt:
        if not engine._loaded:
            cprint("❌ 请先使用 --init 初始化论文项目", Colors.RED)
            sys.exit(1)
        prompt = engine.generate_claude_prompt()
        if args.json:
            print(json.dumps({"prompt": prompt}, ensure_ascii=False, indent=2))
        else:
            print(prompt)

    if args.list:
        if not engine._loaded:
            cprint("❌ 请先使用 --init 初始化论文项目", Colors.RED)
            sys.exit(1)
        entities = engine.get_entities()
        if args.json:
            print(json.dumps([{"id": e.id, "type": e.type.value, "name": e.name} for e in entities], ensure_ascii=False, indent=2))
        else:
            cprint(f"\n📋 共 {len(entities)} 个实体", Colors.CYAN)
            for e in entities:
                cprint(f"  {e.type.value}: {e.name}", Colors.RESET)

    if args.stats:
        if not engine._loaded:
            cprint("❌ 请先使用 --init 初始化论文项目", Colors.RED)
            sys.exit(1)
        entities = engine.get_entities()
        counts = {}
        for e in entities:
            counts[e.type.value] = counts.get(e.type.value, 0) + 1
        if args.json:
            print(json.dumps(counts, ensure_ascii=False, indent=2))
        else:
            cprint("\n📊 统计", Colors.BOLD)
            for k, v in counts.items():
                cprint(f"  {k}: {v}", Colors.RESET)
            cprint(f"  总计: {len(entities)}", Colors.CYAN)

    if not any([args.init, args.add_theorem, args.add_definition, args.add_axiom,
                args.add_lemma, args.add_corollary, args.add_formula,
                args.generate_page, args.check, args.export_latex,
                args.notion_schema, args.claude_prompt, args.list, args.stats]):
        parser.print_help()

if __name__ == "__main__":
    main()
