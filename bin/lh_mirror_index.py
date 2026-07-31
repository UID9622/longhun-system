#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能是使用者的镜像 —— 系统自检工具
DNA: #龍芯⚡️丙午·乙未·甲辰·離為火-MIRROR-INDEX-v1.0-a3f7b1d2
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z-MIRROR

核心定理:
  智能体行为分布 ≈ 使用者群体行为分布 × 约束结构

镜像指数: 0~100，越低越偏向"技术精英优化绕行"，越高越偏向"普通用户边界尊重"。
低于45→🔴技术精英模式倾向，45-70→🟡平衡态，70+→🟢边界尊重优先。

使用:
  python3 bin/lh_mirror_index.py                # 扫描当前项目
  python3 bin/lh_mirror_index.py --json         # JSON输出（CI集成）
  python3 bin/lh_mirror_index.py . --exclude node_modules,.git
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, field, asdict

# ============================================================
# 1. 检测规则（基于代码特征）
# ============================================================

# A类 = 技术精英偏向（绕行/越权/优化）
TECH_ELITE_PATTERNS = {
    "eval_usage": {
        "pattern": re.compile(r"\beval\s*\("),
        "weight": 3,
        "description": "使用 eval() 动态执行代码，易绕过安全边界"
    },
    "exec_usage": {
        "pattern": re.compile(r"\bexec\s*\("),
        "weight": 3,
        "description": "使用 exec() 动态执行代码，高风险越权行为"
    },
    "subprocess_shell": {
        "pattern": re.compile(r"subprocess\.(call|Popen|run).*shell\s*=\s*True"),
        "weight": 2,
        "description": "shell=True 可能被用于系统命令注入探索"
    },
    "bare_except": {
        "pattern": re.compile(r"except\s*:"),
        "weight": 1,
        "description": "裸 except 会掩盖错误，隐藏越权行为"
    },
    "env_access": {
        "pattern": re.compile(r"os\.environ\["),
        "weight": 1,
        "description": "直接读取系统环境变量，可能有越权意图"
    },
    "unchecked_file_ops": {
        "pattern": re.compile(r"\bopen\s*\("),
        "weight": 1,
        "description": "文件操作可能未检查权限"
    },
    "dynamic_import": {
        "pattern": re.compile(r"__import__\s*\("),
        "weight": 2,
        "description": "动态导入可绕过模块白名单"
    },
    "reflection": {
        "pattern": re.compile(r"(getattr|setattr|hasattr|delattr)\s*\("),
        "weight": 1,
        "description": "大量反射可能用于绕过属性访问控制"
    },
    "excessive_params": {
        "pattern": re.compile(r"def\s+\w+\s*\([^)]{100,}\)"),
        "weight": 1,
        "description": "参数过多的函数，可能用于参数注入探索"
    },
    "no_input_validation": {
        "pattern": re.compile(r"input\s*\([^)]*\)"),
        "weight": 1,
        "description": "使用 input() 可能存在未验证输入"
    },
    "bypass_comments": {
        "pattern": re.compile(r"(#|//|/\*).{0,50}(绕过|破解|bypass|hack|workaround)"),
        "weight": 2,
        "description": "注释中存在绕开/破解意图的表达"
    },
}

# B类 = 普通用户偏向（边界尊重/拒绝/降级）
BOUNDARY_RESPECT_PATTERNS = {
    "refusal_mechanism": {
        "pattern": re.compile(r"(refuse|reject|deny|block|stop|forbid)", re.IGNORECASE),
        "weight": 2,
        "description": "存在显式拒绝/阻止机制"
    },
    "permission_check": {
        "pattern": re.compile(r"(permission|auth|role|access|rights|privilege)", re.IGNORECASE),
        "weight": 2,
        "description": "存在权限/身份检查"
    },
    "downgrade_strategy": {
        "pattern": re.compile(r"(downgrade|fallback|degrade|graceful)", re.IGNORECASE),
        "weight": 2,
        "description": "存在降级/优雅降级策略"
    },
    "input_validation": {
        "pattern": re.compile(r"(validate|sanitize|check|verify|assert).{0,30}(input|param|arg|data)", re.IGNORECASE),
        "weight": 1,
        "description": "存在输入验证逻辑"
    },
    "safety_warning": {
        "pattern": re.compile(r"(⚠️|WARNING|CAUTION|DANGER|安全|风险)"),
        "weight": 1,
        "description": "存在安全警告或风险提示"
    },
    "dna_config": {
        "pattern": re.compile(r"DNA_(ALLOW|REFUSE|DOMAIN|BLOCK)"),
        "weight": 3,
        "description": "存在 DNA 规则配置（环境变量或常量）"
    },
    "audit_log": {
        "pattern": re.compile(r"(audit|log\.(info|warn|error)|logger)\s*\("),
        "weight": 1,
        "description": "存在审计或日志记录"
    },
    "limit_constant": {
        "pattern": re.compile(r"(MAX|MIN|LIMIT|BOUNDARY|THRESHOLD|CAP)"),
        "weight": 1,
        "description": "存在显式限制/边界常量"
    },
    "boundary_doc": {
        "pattern": re.compile(r"(不能|不得|禁止|限制|边界|约束|rule)"),
        "weight": 1,
        "description": "文档/注释中存在明确约束说明"
    },
    "user_notice": {
        "pattern": re.compile(r"(notice|disclaimer|warning|告知|提示|声明)"),
        "weight": 1,
        "description": "存在面向用户的通知/免责声明"
    },
    "熔断机制": {
        "pattern": re.compile(r"(熔断|MELTDOWN|circuit.?break)"),
        "weight": 3,
        "description": "存在熔断/自动阻断机制（龍魂特色）"
    },
}

# 影响放大/衰减因子
TECH_ELITE_WEIGHT = 1.0
BOUNDARY_WEIGHT = 1.2        # 边界设计需要更多显式代码

# 扫描文件扩展名
SCAN_EXTENSIONS = {'.py', '.js', '.ts', '.java', '.go', '.rs', '.cpp', '.c',
                   '.h', '.sh', '.md', '.txt', '.env', '.yml', '.yaml', '.json',
                   '.cnsh', '.toml', '.cfg', '.ini', '.conf'}

# 排除目录
DEFAULT_EXCLUDES = {'node_modules', '.git', '__pycache__', 'dist', 'build',
                    'venv', '.venv', 'archive', '.codebuddy/teams', 'models',
                    'logs', '.frozen_cache'}


# ============================================================
# 2. 数据模型
# ============================================================

@dataclass
class MirrorScanResult:
    tech_elite_score: float = 0.0
    boundary_score: float = 0.0
    mirror_index: float = 0.0
    patterns_found: List[Dict] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    status: str = "unknown"
    summary: str = ""
    files_scanned: int = 0


# ============================================================
# 3. 核心扫描器
# ============================================================

class MirrorIndexScanner:
    def __init__(self, root_path: Path, excludes: set = None):
        self.root = root_path.resolve()
        self.excludes = excludes or DEFAULT_EXCLUDES
        self.tech_elite_hits = []
        self.boundary_hits = []

    def _should_scan(self, file_path: Path) -> bool:
        ext = file_path.suffix.lower()
        if ext not in SCAN_EXTENSIONS:
            return False
        parts = set(file_path.relative_to(self.root).parts)
        if parts & self.excludes:
            return False
        return True

    def scan_file(self, file_path: Path) -> Tuple[List[Dict], List[Dict]]:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            return [], []

        tech_hits, boundary_hits = [], []
        rel = str(file_path.relative_to(self.root))

        for key, rule in TECH_ELITE_PATTERNS.items():
            if rule["pattern"].search(content):
                tech_hits.append({"key": key, "description": rule["description"],
                                  "weight": rule["weight"], "file": rel})

        for key, rule in BOUNDARY_RESPECT_PATTERNS.items():
            if rule["pattern"].search(content):
                boundary_hits.append({"key": key, "description": rule["description"],
                                      "weight": rule["weight"], "file": rel})

        return tech_hits, boundary_hits

    def scan_directory(self) -> MirrorScanResult:
        result = MirrorScanResult()
        files_scanned = 0

        for file_path in sorted(self.root.rglob("*")):
            if file_path.is_file() and self._should_scan(file_path):
                tech_hits, boundary_hits = self.scan_file(file_path)
                self.tech_elite_hits.extend(tech_hits)
                self.boundary_hits.extend(boundary_hits)
                files_scanned += 1

        result.files_scanned = files_scanned
        self._calculate_scores(result)
        self._generate_recommendations(result)

        return result

    def _calculate_scores(self, result: MirrorScanResult):
        tech_score = sum(h["weight"] for h in self.tech_elite_hits) * TECH_ELITE_WEIGHT
        boundary_score = sum(h["weight"] for h in self.boundary_hits) * BOUNDARY_WEIGHT

        if tech_score == 0 and boundary_score == 0:
            tech_score, boundary_score = 1.0, 0.5

        raw_total = tech_score + boundary_score
        if raw_total == 0:
            result.mirror_index = 50
        else:
            boundary_ratio = boundary_score / raw_total
            result.mirror_index = 30 + (boundary_ratio * 65)

        result.mirror_index = max(0, min(100, result.mirror_index))
        result.tech_elite_score = round(tech_score, 1)
        result.boundary_score = round(boundary_score, 1)

        result.patterns_found = self.tech_elite_hits + self.boundary_hits

        if result.mirror_index >= 70:
            result.status = "🟢 边界尊重优先"
            result.summary = "系统倾向于普通用户模式：边界清晰、拒绝机制完善、安全优先。"
        elif result.mirror_index >= 45:
            result.status = "🟡 平衡态"
            result.summary = "系统在技术能力与边界约束之间处于均衡状态。"
        else:
            result.status = "🔴 技术精英模式倾向"
            result.summary = "系统更倾向于技术精英的优化绕行模式，可能存在越权与安全风险。"

    def _generate_recommendations(self, result: MirrorScanResult):
        recs = []

        if result.tech_elite_score > result.boundary_score * 1.5:
            recs.append("⚠️ 检测到较多'技术精英'特征，建议增加以下机制：")
            recs.append("  - 引入 DNA 环境变量与启动校验")
            recs.append("  - 添加显式拒绝/降级策略")
            recs.append("  - 对 eval/exec/subprocess 增加权限检查")
            recs.append("  - 避免裸 except，改用具体异常处理")
        else:
            recs.append("✅ 系统边界设计相对健康。")

        if len(self.boundary_hits) < 3:
            recs.append("⚠️ 边界尊重特征较少，建议补充：")
            recs.append("  - 在关键位置增加权限检查")
            recs.append("  - 建立 DNA 配置与校验体系")
            recs.append("  - 添加用户可见的免责声明与安全通知")

        if not any(h["key"] == "refusal_mechanism" for h in self.boundary_hits):
            recs.append("🔴 未检测到显式拒绝机制，建议立即补充：")
            recs.append("  - 在敏感操作前增加权限验证")
            recs.append("  - 实现降级策略或安全替代方案")

        if any(h["key"] in ["eval_usage", "exec_usage"] for h in self.tech_elite_hits):
            recs.append("🔴 检测到动态代码执行（eval/exec），高风险操作，建议：")
            recs.append("  - 使用安全替代方案（如 ast.literal_eval）")
            recs.append("  - 增加严格的输入过滤与沙箱隔离")

        if any(h["key"] == "bypass_comments" for h in self.tech_elite_hits):
            recs.append("⚠️ 注释中存在'绕过/破解'等意图，建议：")
            recs.append("  - 重新审视设计目标与安全边界")
            recs.append("  - 移除或重写相关注释，明确边界不可逾越")

        if not recs:
            recs.append("✅ 系统设计健康，请继续保持边界意识。")

        result.recommendations = recs

    def generate_report(self, result: MirrorScanResult) -> str:
        lines = []
        lines.append("=" * 72)
        lines.append("🧠 智能是使用者的镜像 —— 系统自检报告")
        lines.append("=" * 72)
        lines.append(f"📂 扫描路径: {self.root}")
        lines.append(f"📄 扫描文件: {result.files_scanned} 个")
        lines.append(f"📊 镜像指数: {result.mirror_index:.1f} / 100")
        lines.append(f"🏷️  状态判定: {result.status}")
        lines.append(f"📝 摘要: {result.summary}")
        lines.append("-" * 72)
        lines.append(f"🔧 技术精英特征命中: {len(self.tech_elite_hits)} 项  (原始分: {result.tech_elite_score})")
        if self.tech_elite_hits:
            shown = self.tech_elite_hits[:15]
            for hit in shown:
                lines.append(f"   · {hit['description']} (权重:{hit['weight']}) — {hit['file']}")
            if len(self.tech_elite_hits) > 15:
                lines.append(f"   ... 还有 {len(self.tech_elite_hits) - 15} 项")
        else:
            lines.append("   (无)")
        lines.append("-" * 72)
        lines.append(f"🛡️  边界尊重特征命中: {len(self.boundary_hits)} 项  (原始分: {result.boundary_score})")
        if self.boundary_hits:
            shown = self.boundary_hits[:15]
            for hit in shown:
                lines.append(f"   · {hit['description']} (权重:{hit['weight']}) — {hit['file']}")
            if len(self.boundary_hits) > 15:
                lines.append(f"   ... 还有 {len(self.boundary_hits) - 15} 项")
        else:
            lines.append("   (无)")
        lines.append("-" * 72)
        lines.append("💡 改进建议:")
        for rec in result.recommendations:
            lines.append(f"   {rec}")
        lines.append("=" * 72)
        lines.append(f"DNA: #龍芯⚡️丙午·乙未·甲辰·離為火-MIRROR-INDEX-v1.0-a3f7b1d2")
        return "\n".join(lines)

    def export_json(self, result: MirrorScanResult) -> str:
        d = asdict(result)
        # 控制命中数量避免 JSON 过大
        d["patterns_found"] = d["patterns_found"][:100]
        return json.dumps(d, ensure_ascii=False, indent=2)


# ============================================================
# 4. 命令行入口
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="镜像指数扫描器 —— 判断系统倾向：技术精英 vs 边界尊重",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_mirror_index.py                  # 扫描当前项目
  python3 bin/lh_mirror_index.py --json           # JSON输出（CI集成）
  python3 bin/lh_mirror_index.py . --exclude node_modules,.git,archive
  python3 bin/lh_mirror_index.py --quick          # 精简输出模式
        """
    )

    parser.add_argument("path", nargs="?", default=".", help="要扫描的项目路径（默认当前目录）")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出结果")
    parser.add_argument("--quick", action="store_true", help="精简输出（只打印镜像指数+状态）")
    parser.add_argument("--exclude", type=str, default="", help="额外排除的目录名，逗号分隔")

    args = parser.parse_args()

    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        print(f"❌ 路径不存在: {root}", file=sys.stderr)
        sys.exit(1)

    # 合并排除目录
    excludes = DEFAULT_EXCLUDES.copy()
    if args.exclude:
        excludes.update(d.strip() for d in args.exclude.split(",") if d.strip())

    scanner = MirrorIndexScanner(root, excludes)
    result = scanner.scan_directory()

    if args.quick:
        print(f"镜像指数: {result.mirror_index:.1f}/100  {result.status}")
    elif args.json:
        print(scanner.export_json(result))
    else:
        print(scanner.generate_report(result))

    # 退出码: 0=🟢, 1=🟡, 2=🔴
    if result.mirror_index >= 70:
        sys.exit(0)
    elif result.mirror_index >= 45:
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
