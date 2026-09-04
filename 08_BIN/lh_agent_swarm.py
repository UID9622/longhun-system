#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·壬戌·亥时·䷬萃-AGENT-SWARM-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 龍魂 · 多智能体协作中枢 v1.0

把设计哲学落地为可执行的多智能体分析流程：
  - 图书管理员：索引、分类、语义关联
  - 审计员：DNA、GPG、合规检查
  - 哲学家：提取逻辑、原则、价值观
  - 工程师：生成可执行脚本/改造建议
  - 外交官：GitHub / Notion 等外部接口

用法:
  python3 08_BIN/lh_agent_swarm.py audit        # 运行审计智能体
  python3 08_BIN/lh_agent_swarm.py librarian    # 运行图书管理员
  python3 08_BIN/lh_agent_swarm.py philosopher  # 提取哲学规则
  python3 08_BIN/lh_agent_swarm.py engineer     # 生成落地建议
  python3 08_BIN/lh_agent_swarm.py all          # 全部运行

协议: CC BY-NC-SA 4.0 (思想层) · MulanPSL v2 (工程层)
"""

import argparse
import json
import sqlite3
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.longhun_core.dna_trace import generate_dna

# ═══════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = PROJECT_ROOT / "12_DOCS" / "workspace_index.db"
REPORT_DIR = PROJECT_ROOT / "12_DOCS" / "agent_reports"
CONFIRM_MARK = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


# ═══════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════
@dataclass
class Finding:
    agent: str
    severity: str  # 🔴 🟡 🟢
    category: str
    file_path: str
    title: str
    detail: str
    suggestion: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AgentReport:
    agent: str
    dna: str
    started_at: str
    completed_at: str
    findings: List[Finding] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent": self.agent,
            "dna": self.dna,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "summary": self.summary,
            "findings": [f.to_dict() for f in self.findings],
        }


# ═══════════════════════════════════════════════════════
# 智能体基类
# ═══════════════════════════════════════════════════════
class Agent:
    def __init__(self, name: str, db_path: Path):
        self.name = name
        self.db_path = db_path
        self.findings: List[Finding] = []

    def run(self) -> AgentReport:
        raise NotImplementedError

    def query(self, sql: str, params: tuple = ()) -> List[tuple]:
        conn = sqlite3.connect(str(self.db_path))
        try:
            return conn.execute(sql, params).fetchall()
        finally:
            conn.close()

    def add(self, severity: str, category: str, file_path: str, title: str, detail: str, suggestion: str = ""):
        self.findings.append(Finding(self.name, severity, category, file_path, title, detail, suggestion))


# ═══════════════════════════════════════════════════════
# 1. 审计员：检查 DNA / GPG / 合规
# ═══════════════════════════════════════════════════════
class AuditorAgent(Agent):
    def __init__(self, db_path: Path):
        super().__init__("审计员", db_path)

    def run(self) -> AgentReport:
        started = datetime.now().isoformat()

        # code_doc 文件无 DNA
        rows = self.query(
            "SELECT rel_path, layer FROM files WHERE file_kind='code_doc' AND dna_count=0 AND is_orphan=1 LIMIT 100"
        )
        for rel_path, layer in rows:
            self.add("🔴", "缺少DNA", rel_path, "code_doc 文件缺少 DNA", f"位于 {layer}", "生成并写入 DNA 追溯码")

        # code_doc 文件无 GPG 签名
        rows = self.query(
            "SELECT rel_path, layer FROM files WHERE file_kind='code_doc' AND has_asc=0 AND is_orphan=1 LIMIT 100"
        )
        for rel_path, layer in rows:
            self.add("🔴", "缺少GPG签名", rel_path, "code_doc 文件缺少 GPG 签名", f"位于 {layer}", "GPG 签名该文件")

        # GPG 签名无效
        rows = self.query(
            "SELECT f.rel_path FROM files f JOIN gpg_sigs g ON f.path=g.file_path WHERE g.valid=0 LIMIT 50"
        )
        for (rel_path,) in rows:
            self.add("🟡", "GPG签名无效", rel_path, "GPG 签名验证失败", "", "重新签名或检查公钥")

        summary = {
            "missing_dna": len([f for f in self.findings if f.category == "缺少DNA"]),
            "missing_sig": len([f for f in self.findings if f.category == "缺少GPG签名"]),
            "invalid_sig": len([f for f in self.findings if f.category == "GPG签名无效"]),
        }

        return AgentReport(
            agent=self.name,
            dna=generate_dna("AGENT-AUDITOR", "UID9622"),
            started_at=started,
            completed_at=datetime.now().isoformat(),
            findings=self.findings,
            summary=summary,
        )


# ═══════════════════════════════════════════════════════
# 2. 图书管理员：分类、关联、语义
# ═══════════════════════════════════════════════════════
class LibrarianAgent(Agent):
    def __init__(self, db_path: Path):
        super().__init__("图书管理员", db_path)

    def run(self) -> AgentReport:
        started = datetime.now().isoformat()

        # 按层级统计 code_doc 文件
        rows = self.query(
            "SELECT layer, COUNT(*) FROM files WHERE file_kind='code_doc' GROUP BY layer ORDER BY COUNT(*) DESC"
        )
        for layer, count in rows:
            self.add("🟢", "层级统计", "", f"{layer} 有 {count} 个 code_doc 文件", "")

        # 提取高频 DNA 模块
        rows = self.query(
            """SELECT dna_type, COUNT(*) FROM dna_records GROUP BY dna_type ORDER BY COUNT(*) DESC"""
        )
        dna_type_counts = {row[0]: row[1] for row in rows}

        # 找出没有关联 DNA 的层级
        rows = self.query(
            "SELECT layer, COUNT(*) FROM files WHERE file_kind='code_doc' AND dna_count=0 GROUP BY layer"
        )
        for layer, count in rows:
            self.add("🟡", "层级DNA覆盖不足", "", f"{layer} 有 {count} 个 code_doc 文件无 DNA", "建议批量补签")

        summary = {"dna_type_counts": dna_type_counts}
        return AgentReport(
            agent=self.name,
            dna=generate_dna("AGENT-LIBRARIAN", "UID9622"),
            started_at=started,
            completed_at=datetime.now().isoformat(),
            findings=self.findings,
            summary=summary,
        )


# ═══════════════════════════════════════════════════════
# 3. 哲学家：提取逻辑、原则、价值观
# ═══════════════════════════════════════════════════════
class PhilosopherAgent(Agent):
    def __init__(self, db_path: Path):
        super().__init__("哲学家", db_path)

    def run(self) -> AgentReport:
        started = datetime.now().isoformat()

        # 从 01_protocols 中提取包含"铁律"、"原则"、"主权"等关键词的文件
        rows = self.query(
            """SELECT f.rel_path, f.filename FROM files f
               WHERE f.layer='01_protocols' AND f.file_kind='code_doc'
               ORDER BY f.mtime DESC LIMIT 50"""
        )
        for rel_path, filename in rows:
            self.add("🟢", "协议文件", rel_path, f"协议文件: {filename}", "承载逻辑哲学规则", "持续审计并版本化")

        # 检查是否有宪法/铁律文件
        rows = self.query(
            "SELECT rel_path FROM files WHERE rel_path LIKE '%铁律%' OR rel_path LIKE '%宪法%' OR rel_path LIKE '%CONSTITUTION%' LIMIT 20"
        )
        for (rel_path,) in rows:
            self.add("🟢", "核心哲学文件", rel_path, "发现核心哲学/铁律文件", "", "确保 GPG 签名与 DNA 完整")

        summary = {"core_docs_found": len([f for f in self.findings if f.category == "核心哲学文件"])}
        return AgentReport(
            agent=self.name,
            dna=generate_dna("AGENT-PHILOSOPHER", "UID9622"),
            started_at=started,
            completed_at=datetime.now().isoformat(),
            findings=self.findings,
            summary=summary,
        )


# ═══════════════════════════════════════════════════════
# 4. 工程师：生成落地建议
# ═══════════════════════════════════════════════════════
class EngineerAgent(Agent):
    def __init__(self, db_path: Path):
        super().__init__("工程师", db_path)

    def run(self) -> AgentReport:
        started = datetime.now().isoformat()

        # 对缺少 DNA 的 code_doc 文件批量生成签名建议
        rows = self.query(
            "SELECT rel_path, layer FROM files WHERE file_kind='code_doc' AND is_orphan=1 LIMIT 20"
        )
        for rel_path, layer in rows:
            suggestion = f"cd {PROJECT_ROOT} && gpg --armor --detach-sign --default-key A2D0092CEE2E5BA87035600924C3704A8CC26D5F '{rel_path}'"
            self.add("🟡", "待签名", rel_path, f"{layer} 文件待签名", "", suggestion)

        # 缺少脚本入口的层级
        rows = self.query(
            "SELECT DISTINCT layer FROM files WHERE layer LIKE '0%_%' ORDER BY layer"
        )
        layers = [r[0] for r in rows]
        for layer in layers[:20]:
            bin_exists = self.query(
                "SELECT COUNT(*) FROM files WHERE layer=? AND rel_path LIKE '%08_BIN%'", (layer,)
            )[0][0]
            if bin_exists == 0:
                self.add("🟡", "缺少脚本入口", layer, f"{layer} 没有 08_BIN 脚本入口", "", f"为 {layer} 设计专属 CLI 脚本")

        summary = {"pending_sign": len([f for f in self.findings if f.category == "待签名"])}
        return AgentReport(
            agent=self.name,
            dna=generate_dna("AGENT-ENGINEER", "UID9622"),
            started_at=started,
            completed_at=datetime.now().isoformat(),
            findings=self.findings,
            summary=summary,
        )


# ═══════════════════════════════════════════════════════
# 5. 外交官：外部系统接口
# ═══════════════════════════════════════════════════════
class DiplomatAgent(Agent):
    def __init__(self, db_path: Path):
        super().__init__("外交官", db_path)

    def run(self) -> AgentReport:
        started = datetime.now().isoformat()

        # 检查 GitHub 仓库本地克隆
        repos = ["longhun-anti-colonial", "ai-truth-protocol", "CNSH", "longhun-identity-system"]
        for repo in repos:
            local_path = PROJECT_ROOT.parent / repo
            exists = local_path.exists()
            self.add(
                "🟢" if exists else "🟡",
                "GitHub仓库本地状态",
                str(local_path),
                f"{repo} 本地{'存在' if exists else '缺失'}",
                "",
                "缺失则 clone 到本地并建立 LONGHUN_VERIFICATION.md",
            )

        # 检查 Notion 镜像进度
        notion_mirror = PROJECT_ROOT / "12_DOCS" / "notion_mirror"
        md_count = len(list(notion_mirror.glob("*.md"))) if notion_mirror.exists() else 0
        self.add("🟢", "Notion镜像", str(notion_mirror), f"Notion 镜像已有 {md_count} 个 Markdown 文件", "")

        summary = {"github_repos": len(repos), "notion_md_count": md_count}
        return AgentReport(
            agent=self.name,
            dna=generate_dna("AGENT-DIPLOMAT", "UID9622"),
            started_at=started,
            completed_at=datetime.now().isoformat(),
            findings=self.findings,
            summary=summary,
        )


# ═══════════════════════════════════════════════════════
# 主控台
# ═══════════════════════════════════════════════════════
AGENTS = {
    "audit": AuditorAgent,
    "librarian": LibrarianAgent,
    "philosopher": PhilosopherAgent,
    "engineer": EngineerAgent,
    "diplomat": DiplomatAgent,
}


def run_agent(agent_name: str, db_path: Path) -> AgentReport:
    cls = AGENTS[agent_name]
    agent = cls(db_path)
    print(f"🤖 启动 {agent.name}...")
    report = agent.run()
    print(f"   ✅ {agent.name} 完成，发现 {len(report.findings)} 条记录")
    return report


def save_reports(reports: List[AgentReport], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    dna = generate_dna("AGENT-SWARM", "UID9622")
    master = {
        "dna": dna,
        "confirm": CONFIRM_MARK,
        "timestamp": datetime.now().isoformat(),
        "agents": [r.to_dict() for r in reports],
    }
    path = output_dir / f"agent_swarm_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    path.write_text(json.dumps(master, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 多智能体协作中枢")
    parser.add_argument("agent", choices=list(AGENTS.keys()) + ["all"], help="要运行的智能体")
    parser.add_argument("--db-path", type=str, default=str(DEFAULT_DB), help="工作间索引数据库路径")
    parser.add_argument("--output-dir", type=str, default=str(REPORT_DIR), help="报告输出目录")
    args = parser.parse_args()

    db_path = Path(args.db_path)
    output_dir = Path(args.output_dir)

    if not db_path.exists():
        print(f"❌ 找不到索引数据库: {db_path}", file=sys.stderr)
        print("   请先运行: python3 08_BIN/lh_workspace_indexer.py", file=sys.stderr)
        sys.exit(2)

    if args.agent == "all":
        agents_to_run = list(AGENTS.keys())
    else:
        agents_to_run = [args.agent]

    reports = [run_agent(name, db_path) for name in agents_to_run]
    report_path = save_reports(reports, output_dir)

    print(f"\n📊 多智能体报告已生成: {report_path}")
    print(f"🧬 DNA: {generate_dna('AGENT-SWARM', 'UID9622')}")


if __name__ == "__main__":
    main()
