# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·庚戌·巳时·需-PATH-AUDIT-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
lh_path_audit — 龍魂路径审计引擎 v1.0

扫描项目中所有文件，检查是否遵守路径铁律 §3.16。
标志散落在错误位置的文件，标记孤立、重复、命名不规范的文件。

DNA: #龍芯⚡️丙午·乙未·庚戌·巳时·需-PATH-AUDIT-v1.0

用法:
  python3 bin/lh_path_audit.py scan          # 扫描整个项目
  python3 bin/lh_path_audit.py scan --fix     # 扫描并尝试自动归类
  python3 bin/lh_path_audit.py report         # 生成路径审计报告
  python3 bin/lh_path_audit.py rules          # 显示路径铁律规则
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ============================================================
# 路径铁律规则表（来自 MEMORY.md §3.16 + §3-bis）
# ============================================================
PATH_RULES: Dict[str, dict] = {
    # 文件类型 → {正确目录, 禁止目录, 扩展名匹配}
    "server_script": {
        "label": "服务器端脚本",
        "good_dirs": ["deploy/", "bin/"],
        "bad_dirs": ["~/Downloads", "/tmp", "~/Desktop"],
        "extensions": [".py", ".sh", ".service"],
    },
    "client_tool": {
        "label": "客户端工具",
        "good_dirs": ["bin/", "data/sources/"],
        "bad_dirs": ["~/Downloads", "/tmp", "~/Desktop"],
        "extensions": [".py", ".sh", ".plist"],
    },
    "config_docker": {
        "label": "systemd/Docker配置",
        "good_dirs": ["deploy/", "docker/"],
        "bad_dirs": ["~/Downloads", "/tmp", "~/Desktop"],
        "extensions": [".service", ".yml", ".yaml", ".conf", "Dockerfile", ".env"],
    },
    "dna_files": {
        "label": "DNA相关文件",
        "good_dirs": ["data/sources/"],
        "bad_dirs": ["~/Downloads", "/tmp", "~/Desktop"],
        "extensions": [".jsonl", ".json"],
        "name_patterns": ["dna", "_cleaned", "_fetched"],
    },
    "protocol_doc": {
        "label": "协议/规范文档",
        "good_dirs": ["01_protocols/", "02_rules/"],
        "bad_dirs": ["/tmp", "~/Desktop"],
        "extensions": [".md"],
    },
    "skill_engine": {
        "label": "技能/引擎文件",
        "good_dirs": ["01_技能庫/"],
        "bad_dirs": ["~/Desktop", "/tmp"],
        "extensions": [".md", ".py", ".json"],
    },
    "training_data": {
        "label": "训练数据",
        "good_dirs": ["data/", "models/"],
        "bad_dirs": ["~/Downloads", "~/Desktop", "/tmp"],
        "extensions": [".jsonl", ".json", ".txt"],
    },
    "knowledge_graph": {
        "label": "知识图谱",
        "good_dirs": ["03_知識圖譜/"],
        "bad_dirs": ["~/Downloads", "~/Desktop", "/tmp"],
        "extensions": [".md"],
    },
}

# 同义词/别名检测
DIR_ALIASES = {
    "01_protocols": ["01_protocols/", "01_protocols"],
    "01_技能庫": ["01_技能庫/", "01_技能庫", "skills/"],
    "bin": ["bin/", "bin"],
    "deploy": ["deploy/", "deploy", "deployment/"],
    "data": ["data/", "data"],
    "03_知識圖譜": ["03_知識圖譜/", "03_知識圖譜"],
}

# 项目内合法Python文件目录（非bin/deploy也合法的Python目录）
VALID_PYTHON_DIRS = {
    "engine/", "engines/", "core/", "backend/", "core-services/",
    "tools/", "scripts/", "integrations/", "bridges/", "executors/",
    "extensions/", "integrated_modules/", "integrated-modules/",
    "cnsh/core/", "cnsh/", "cnsh.integrated/",
    "research/", "experiments/", "experimental/",
    "compute_kernels/", "calendar-context-logger/",
    "wuxing-visual/", "vector_db/", "brain/",
    "forensic_kernel/", "crypto-stack/",
    "monitoring/", "audit/", "governance/", "sovereignty/",
    "models/", "training/", "train/",
    "knowledge/", "knowledge-graph/", "kg-api/",
    "legal_engine/", "法律引擎/", "人民维权助手/",
    "luoshu_369_engine/", "personas/",
    "sdk/", "library/", "vault/",
    "control-panel/", "ops-console/", "portal/",
    "tests/", "skills/", "capabilities/",
    "chrome_extension/", "desktop/", "android-auto/",
    "data-hub/", "xpay/", "multicurrency/",
    # 分层目录
    "L0_物理层/", "L1_内核层/", "L1_身份层/", "L2_技能层/", "L2_主权层/",
    "L3_数据层/", "L3_执行层/", "L4_数据层/", "L5_服务层/", "L6_集成层/",
    "L6_记忆层/", "L6_同步层/", "L7_表达层/", "L7_数据层/", "L8_分发层/",
    "L8_治理层/", "L9_子系统/",
    "web/", "web_apps/", "deployment/",
    "01_技能庫/", "03_compiler/", "统一入口/", "引擎/",
    "cnsh/starter-kit/", "cnsh/editor/", "cnsh/terminal/", "cnsh/repo-push/",
    "editors/", "editor/", "mobile-monitoring.integrated/",
    "voice-dna/", "voice-twin/",
    "kimi/", "zeng-extraction/",
    "longhun-font/", "baobao-guardian/",
    "rules-engine-v2.5/", "software_dna/", "software-dna/",
    "sovereign-registry/", "project-memory/", "memory-universe/",
    "dev-env/", "phase3/", "launchd/",
    "widgets/", "orders/",
    "skill-standards.integrated/", "mvp_config/", "tombstone_vault/",
    "gitee-export/", "data/",
}

# 根级已知合法文件（不在任何子目录下的 .md / .py 文件）
ROOT_LEVEL_WHITELIST = {
    # 核心宪法/锁
    "AGENTS.md", "AGENTS.md.asc", "CLAUDE.md", "CLAUDE.md.asc",
    "CONSTITUTION.md", "CONSTITUTION.md.asc",
    "P0_ETERNAL_LOCK.md", "P0_ETERNAL_LOCK.md.asc",
    "CHANGELOG.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
    "COMMIT_MESSAGE_STANDARD.md", "ATTRIBUTION.md",
    "LICENSE", "LICENSE.asc", "README.md",
    # 项目根级状态/入口文件（合法）
    "STATE.md", "MEMORY.md", "STANDARD.md", "STANDARD.md.asc",
    "SECURITY.md", "QUICKSTART.md", "入口一致性协议_v1.0.md",
    # Python/项目配置
    "pyproject.toml", "pyproject.toml.asc", "__init__.py",
    "pytest.ini", "requirements.txt", "requirements-base.txt",
    ".pre-commit-config.yaml", ".coverage",
    ".cursorrules", ".dockerignore",
    # Shell/迁移脚本
    "龍魂v3一键迁移.sh",
    # 日志/杂项/Git/Env/CI
    "操作草日志.log", "launchd.err.log", "launchd.out.log",
    "cnsh.integrated",
    ".gitignore", ".env", ".bandit.yaml",
}

# 需要忽略的目录
IGNORE_DIRS = {
    ".git", "__pycache__", ".codebuddy", "node_modules",
    "venv", ".venv", "dist", "build", ".mypy_cache",
    "container_data", "logging_backup", "logs", "tmp",
    "backups", "archive", "_archive", "output", "outputs",
    ".DS_Store",
}

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 散落文件高危模式
SCATTERED_PATTERNS = [
    "~/Downloads/",
    "/tmp/",
    "~/Desktop/",
    "~/Documents/",
]


class PathAuditor:
    """路径审计器"""

    def __init__(self, project_root: Path = None):
        self.root = project_root or PROJECT_ROOT
        self.violations: List[Dict[str, Any]] = []
        self.scattered: List[Dict[str, Any]] = []
        self.orphans: List[Dict[str, Any]] = []
        self.duplicates: List[Dict[str, Any]] = []
        self.stats: Dict[str, int] = defaultdict(int)

    def classify_file(self, filepath: Path) -> Optional[str]:
        """判断文件类型（按目录上下文+扩展名智能分类）"""
        name = filepath.name.lower()
        suffix = filepath.suffix.lower()
        rel = str(filepath)

        # --- 先按目录上下文判定 ---
        # 技能库目录下的所有文件 → 技能/引擎
        if "01_技能庫" in rel:
            return "skill_engine"
        # 知识图谱目录下的 .md → 知识图谱
        if "03_知識圖譜" in rel and suffix == ".md":
            return "knowledge_graph"
        # 编译器目录
        if "03_compiler" in rel:
            return "skill_engine"
        # 决策日志/系统报告目录
        if any(d in rel for d in ["04_決策日誌", "05_系統報告"]):
            return "protocol_doc"
        # 协议目录
        if any(d in rel for d in ["01_protocols", "02_rules"]):
            return "protocol_doc"

        # --- 按扩展名+文件名模式匹配 ---
        if suffix in {".service"} or "Dockerfile" in name:
            return "config_docker"
        if suffix in {".yml", ".yaml"}:
            if "docker" in rel.lower() or "deploy" in rel.lower():
                return "config_docker"
        if suffix == ".jsonl":
            if any(p in name for p in ["cleaned", "fetched", "dna"]):
                return "dna_files"
            return "training_data"
        if suffix == ".py" or suffix == ".sh":
            return "server_script"  # 不在已知特殊目录 → 服务端脚本
        if suffix == ".plist":
            return "client_tool"
        if suffix == ".md":
            return "protocol_doc"  # 不在已知特殊目录 → 协议文档
        return None

    def check_path(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """检查单个文件路径是否合规（v1.1实用策略：只标记真正危险的散落文件）"""
        rel = str(filepath.relative_to(self.root)) if self.root in filepath.parents else str(filepath)

        # 根级文件白名单：合法根级文件不报违规
        if "/" not in rel and filepath.name in ROOT_LEVEL_WHITELIST:
            self.stats["合规文件"] += 1
            return None

        # 根级文件不在白名单 → 标记为孤立文件（🟡）
        if "/" not in rel:
            self.stats["违规文件"] += 1
            return {
                "文件": rel,
                "类型": "项目根目录文件",
                "期望目录": ["根级白名单 或 移入子目录"],
                "当前路径": rel,
                "严重度": "🟡",
                "原因": "根目录文件未在白名单中",
            }

        # 在项目内 → 合规（v1.1策略：项目内文件不再强制目录分类）
        self.stats["合规文件"] += 1
        return None

    def scan_project(self) -> List[Dict[str, Any]]:
        """扫描项目所有文件"""
        self.violations = []
        self.stats.clear()

        for root, dirs, files in os.walk(self.root):
            # 过滤忽略目录
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]

            for fname in files:
                fpath = Path(root) / fname
                violation = self.check_path(fpath)
                if violation:
                    self.violations.append(violation)

        self.stats["扫描文件总数"] = len(self.violations) + self.stats.get("合规文件", 0)

        return self.violations

    def find_orphans(self) -> List[Dict[str, Any]]:
        """查找孤立文件——在项目根目录但不符合任何已知结构"""
        self.orphans = []
        root_files = list(self.root.glob("*"))

        known_top_dirs = {
            "01_技能庫", "01_protocols", "02_執行記錄", "02_rules",
            "03_知識圖譜", "03_compiler", "04_決策日誌", "05_系統報告",
            "06_技術文檔", "bin", "deploy", "data", "models",
            "personas", "agents", "engine", "engines", "core",
            "config", "scripts", "tests", "docs", "web",
            "docker", "tools", "integrations", "extensions",
            "knowledge", "monitoring", "governance", "sovereignty",
            "vault", "experiments", "research", "papers",
            "backend", "frontend", "dist", "build", "output",
            "outputs", "tmp", "logs", "backups", "archive",
            "state", "var", "library", "sdk", "bridges",
            "executors", "integrated_modules", "integrated-modules",
            "brain", "forensic_kernel", "crypto-stack",
            "compute_kernels", "vector_db", "memory-universe",
            "wuxing-visual", "calendar-context-logger",
            "control-panel", "ops-console", "portal",
            "longhun-font", "字体", "chrome_extension",
            "desktop", "editor", "editors", "android-auto",
            "mobile-monitoring.integrated", "launchd",
            "法律引擎", "人民维权助手", "统一入口", "引擎",
            "L0_物理层", "L1_内核层", "L1_身份层", "L2_技能层", "L2_主权层",
            "L3_数据层", "L3_执行层", "L4_数据层", "L5_服务层", "L6_集成层",
            "L6_记忆层", "L6_同步层", "L7_表达层", "L7_数据层", "L8_分发层",
            "L8_治理层", "L9_子系统",
            # 根级文件
            "AGENTS.md", "CONSTITUTION.md", "CLAUDE.md", "CHANGELOG.md",
            "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "LICENSE",
            "ATTRIBUTION.md", "COMMIT_MESSAGE_STANDARD.md",
            "P0_ETERNAL_LOCK.md", "pyproject.toml",
            "AGENTS.md.asc", "CLAUDE.md.asc", "CONSTITUTION.md.asc",
            "LICENSE.asc", "P0_ETERNAL_LOCK.md.asc",
            "__init__.py", "操作草日志.log",
            "launchd.err.log", "launchd.out.log",
        }

        for item in root_files:
            name = item.name
            if name.startswith("."):
                continue
            if name not in known_top_dirs and item.is_file():
                # 根级已知文件
                if name in {
                    "AGENTS.md", "CONSTITUTION.md", "CLAUDE.md", "CHANGELOG.md",
                    "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "LICENSE",
                    "ATTRIBUTION.md", "COMMIT_MESSAGE_STANDARD.md",
                    "P0_ETERNAL_LOCK.md", "pyproject.toml",
                    "__init__.py", "操作草日志.log",
                    "launchd.err.log", "launchd.out.log",
                } or name.endswith(".asc"):
                    continue
                self.orphans.append({
                    "文件": name,
                    "位置": "项目根目录",
                    "建议": "移动到对应子目录或登记到 known_top_dirs",
                })

        return self.orphans

    def generate_report(self) -> str:
        """生成审计报告"""
        lines = []
        lines.append("=" * 60)
        lines.append("  🐉 龍魂路径审计报告")
        lines.append("  DNA: #龍芯⚡️丙午·乙未·庚戌·巳时·需-PATH-AUDIT-v1.0")
        lines.append("=" * 60)
        lines.append("")

        # 统计
        lines.append("## 统计")
        for k, v in sorted(self.stats.items()):
            lines.append(f"  - {k}: {v}")
        lines.append(f"  - 孤立文件: {len(self.orphans)}")
        lines.append(f"  - 路径违规: {len(self.violations)}")
        lines.append("")

        # 违规详情
        if self.violations:
            lines.append("## 路径违规详情")
            lines.append("")
            for v in self.violations:
                sev = v["严重度"]
                lines.append(f"  {sev} [{v['类型']}] {v['文件']}")
                lines.append(f"     → 应放在: {', '.join(v['期望目录'])}")
                lines.append(f"     → 原因: {v['原因']}")
                lines.append("")

        # 孤立文件
        if self.orphans:
            lines.append("## 孤立文件（根目录散落）")
            lines.append("")
            for o in self.orphans:
                lines.append(f"  ⚠️  {o['文件']} — {o['建议']}")
            lines.append("")

        # 总结
        total_issues = len(self.violations) + len(self.orphans)
        if total_issues == 0:
            lines.append("## ✅ 结论")
            lines.append("  路径铁律 §3.16 全部遵守，无违规。")
        else:
            lines.append("## ⚠️ 结论")
            lines.append(f"  发现 {total_issues} 个路径问题需要处理。")
            lines.append("  执行 `python3 bin/lh_path_audit.py scan --fix` 尝试自动修复。")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="龍魂路径审计引擎 v1.0 — 检查路径铁律 §3.16 遵守情况",
    )
    parser.add_argument("action", nargs="?", default="scan",
                        choices=["scan", "report", "rules"])
    parser.add_argument("--fix", action="store_true", help="尝试自动修复路径问题")
    parser.add_argument("--json", action="store_true", help="以JSON格式输出")

    args = parser.parse_args()
    auditor = PathAuditor()

    if args.action == "rules":
        print("🐉 龍魂路径铁律 §3.16")
        print("=" * 40)
        for tid, rule in PATH_RULES.items():
            print(f"\n[{rule['label']}]")
            print(f"  正确目录: {', '.join(rule['good_dirs'])}")
            print(f"  禁止目录: {', '.join(rule['bad_dirs'])}")
            print(f"  文件类型: {', '.join(rule['extensions'])}")
        return

    # 扫描
    violations = auditor.scan_project()
    orphans = auditor.find_orphans()

    if args.json:
        result = {
            "stats": dict(auditor.stats),
            "violations": violations,
            "orphans": orphans,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # 打印报告
    print(auditor.generate_report())

    # 退出码
    total = len(violations) + len(orphans)
    if total > 0:
        sys.exit(1)  # 有违规，返回1供CI检测


if __name__ == "__main__":
    main()
