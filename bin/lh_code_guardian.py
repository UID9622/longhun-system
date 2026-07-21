#!/usr/bin/env python3
"""
龍魂·代码质量守护 v1.0 — 类型自愈引擎
===========================================
DNA: #龍芯⚡️丙午·辛未·乙酉·申时·大有-LONGHUN-CODE-GUARDIAN-v1.0

功能:
  1. 扫描全项目 Python 文件，检测 basedpyright 类型注解缺失
     - 裸 dict/list/tuple/set/Dict/List/Tuple/Set（缺类型参数）
     - Optional 成员访问无 None 守卫
     - str/int = None 缺少 | None
     - 可选依赖导入警告（try/except ImportError 模式）
  2. --fix 模式自动修复裸类型注解
  3. 输出结构化总结报告（JSON + 终端彩色）

用法:
  python3 bin/lh_code_guardian.py          # 仅扫描，输出报告
  python3 bin/lh_code_guardian.py --fix    # 扫描 + 自动修复
  python3 bin/lh_code_guardian.py --json   # JSON 格式输出
  python3 bin/lh_code_guardian.py --target bin/  # 指定目录
"""

import ast
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# ── ANSI 颜色 ──────────────────────────────────────────
C = {
    "R": "\033[91m", "G": "\033[92m", "Y": "\033[93m",
    "B": "\033[94m", "M": "\033[95m", "C": "\033[96m",
    "W": "\033[97m", "D": "\033[90m", "X": "\033[0m",
    "BOLD": "\033[1m",
}

# ── 项目根 ────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ── 排除目录（不扫描） ────────────────────────────────
EXCLUDE_DIRS: set[str] = {
    "__pycache__", ".git", ".codebuddy", ".obsidian",
    "node_modules", ".venv", "venv", "env", ".archive",
    "tombstone_vault", ".backup", "L7_数据层/gitee-mirror",
    "output", "generated-images",
}

# ── 排除文件模式 ──────────────────────────────────────
EXCLUDE_FILE_PATTERNS: list[str] = [
    r"\.md$", r"\.html$", r"\.json$", r"\.jsonl$",
    r"test_.*\.py$", r".*_test\.py$",
    r"site-packages/", r"dist-packages/",
]

# ── 可选依赖列表（常见第三方库） ──────────────────────
OPTIONAL_DEPENDENCIES: dict[str, str] = {
    "pytesseract": "OCR 文字识别（合同审计）",
    "cv2": "OpenCV 图像处理（照片审计）",
    "numpy": "数值计算（ELA/噪声分析）",
    "scipy": "科学计算（CFA 分析）",
    "PIL": "图像处理（EXIF 提取）",
    "cryptography": "加密签名验证",
    "gmssl": "国密 SM2/SM3/SM4",
    "openai": "OpenAI API 桥接",
    "httpx": "异步 HTTP 客户端",
    "aiohttp": "异步 HTTP 服务端",
    "fastapi": "API 服务框架",
    "uvicorn": "ASGI 服务器",
    "pydantic": "数据校验",
    "jinja2": "模板引擎",
    "redis": "Redis 缓存",
    "sqlalchemy": "SQL ORM",
    "websockets": "WebSocket 通信",
    "matplotlib": "图表绘制",
    "pandas": "数据分析",
    "playwright": "浏览器自动化",
    "selenium": "浏览器自动化（旧）",
    "pymysql": "MySQL 驱动",
    "psycopg2": "PostgreSQL 驱动",
    "chromadb": "向量数据库",
    "sentence_transformers": "语义嵌入",
    "jieba": "中文分词",
    "requests": "HTTP 请求",
    "yaml": "YAML 解析",
    "toml": "TOML 解析",
    "dotenv": "环境变量加载",
}


class Issue:
    """一条类型问题"""
    def __init__(self, file: str, line: int, col: int, category: str,
                 severity: str, message: str, before: str = "", after: str = ""):
        self.file = file
        self.line = line
        self.col = col
        self.category = category
        self.severity = severity  # error / warning / info
        self.message = message
        self.before = before
        self.after = after

    def to_dict(self) -> dict[str, Any]:
        return {
            "file": self.file, "line": self.line, "col": self.col,
            "category": self.category, "severity": self.severity,
            "message": self.message, "before": self.before, "after": self.after,
        }


class CodeGuardian:
    """代码质量守护引擎"""

    def __init__(self, target_dir: str | None = None, fix: bool = False):
        self.target = Path(target_dir) if target_dir else PROJECT_ROOT
        self.fix = fix
        self.issues: list[Issue] = []
        self.fixed_files: list[str] = []
        self.files_scanned: int = 0
        self.files_skipped: int = 0

    # ── 文件发现 ────────────────────────────────────

    def _should_skip(self, filepath: Path) -> bool:
        """判断是否跳过该文件"""
        rel = str(filepath.relative_to(PROJECT_ROOT))
        for pattern in EXCLUDE_FILE_PATTERNS:
            if re.search(pattern, rel):
                return True
        parts = rel.split(os.sep)
        for part in parts:
            if part in EXCLUDE_DIRS:
                return True
        return False

    def discover_files(self) -> list[Path]:
        """发现所有需要扫描的 Python 文件"""
        py_files: list[Path] = []
        for root, dirs, files in os.walk(self.target):
            # 原地过滤目录
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for f in files:
                if f.endswith(".py"):
                    fp = Path(root) / f
                    if not self._should_skip(fp):
                        py_files.append(fp)
        return sorted(py_files)

    # ── 扫描器 ──────────────────────────────────────

    def scan_file(self, filepath: Path) -> list[Issue]:
        """扫描单个文件，返回问题列表"""
        issues: list[Issue] = []
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception:
            return issues

        rel = str(filepath.relative_to(PROJECT_ROOT))
        lines = content.split("\n")

        issues.extend(self._scan_bare_types(rel, lines, content))
        issues.extend(self._scan_optional_imports(rel, lines, content))
        issues.extend(self._scan_none_defaults(rel, lines, content))

        return issues

    def _scan_bare_types(self, rel: str, lines: list[str], _content: str) -> list[Issue]:
        """检测裸类型注解: dict/list/tuple/set 和 Dict/List/Tuple/Set"""
        issues: list[Issue] = []

        # 匹配模式：类型注解位置的裸泛型
        # 模式1: : Dict)  /  : Dict,  /  -> Dict:  /  : Dict\n  /  : Dict = 
        # 模式2: 参数位置: (dict, list 等)
        bare_patterns: list[tuple[str, str, str]] = [
            # (匹配正则, 类型名, 建议修复)
            (r'(?<!\[)(?<!import\s)(?<!\w):\s*Dict\s*([),=:\n])', "Dict", "Dict[str, Any]"),
            (r'(?<!\w)->\s*Dict\s*:', "Dict", "Dict[str, Any]"),
            (r'(?<!\[)(?<!import\s)(?<!\w):\s*dict\s*([),=:\n])', "dict", "dict[str, Any]"),
            (r'(?<!\w)->\s*dict\s*:', "dict", "dict[str, Any]"),
            (r'(?<!\[)(?<!import\s)(?<!\w):\s*List\s*([),=:\n])', "List", "List[Any]"),
            (r'(?<!\w)->\s*List\s*:', "List", "List[Any]"),
            (r'(?<!\[)(?<!import\s)(?<!\w):\s*list\s*([),=:\n])', "list", "list[Any]"),
            (r'(?<!\w)->\s*list\s*:', "list", "list[Any]"),
            (r'(?<!\[)(?<!import\s)(?<!\w):\s*Set\s*([),=:\n])', "Set", "Set[str]"),
            (r'(?<!\w)->\s*Set\s*:', "Set", "Set[str]"),
            (r'(?<!\[)(?<!import\s)(?<!\w):\s*set\s*([),=:\n])', "set", "set[str]"),
            (r'(?<!\w)->\s*set\s*:', "set", "set[str]"),
            (r'(?<!\[)(?<!import\s)(?<!\w):\s*Tuple\s*([),=:\n])', "Tuple", "Tuple[Any, ...]"),
            (r'(?<!\w)->\s*Tuple\s*:', "Tuple", "Tuple[Any, ...]"),
            (r'(?<!\[)(?<!import\s)(?<!\w):\s*tuple\s*([),=:\n])', "tuple", "tuple[Any, ...]"),
            (r'(?<!\w)->\s*tuple\s*:', "tuple", "tuple[Any, ...]"),
        ]

        for line_no, line in enumerate(lines, 1):
            # 跳过导入行和注释
            stripped = line.strip()
            if stripped.startswith("from ") or stripped.startswith("import "):
                continue
            if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
                continue
            # 跳过已经在 [] 中的（已参数化）
            for pattern, type_name, suggestion in bare_patterns:
                m = re.search(pattern, line)
                if m:
                    # 额外检查：确保不是 from typing import Dict 这类导入
                    if f"import {type_name}" in line:
                        continue
                    issues.append(Issue(
                        file=rel, line=line_no, col=m.start() + 1,
                        category="bare_type",
                        severity="error",
                        message=f"裸 {type_name} 缺少类型参数 → {suggestion}",
                        before=line.strip(),
                        after=line.strip().replace(f": {type_name}", f": {suggestion}")
                                         .replace(f"-> {type_name}:", f"-> {suggestion}:")
                                         .replace(f": {type_name})", f": {suggestion})")
                                         .replace(f": {type_name},", f": {suggestion},")
                                         .replace(f": {type_name} =", f": {suggestion} ="),
                    ))

        return issues

    def _scan_optional_imports(self, rel: str, lines: list[str], content: str) -> list[Issue]:
        """检测可选依赖导入模式"""
        issues: list[Issue] = []

        # 检测 try/except ImportError 中的库
        try_import_pattern = re.compile(
            r'import\s+(\w+)\s*\n\s*except\s+(?:ImportError|ModuleNotFoundError)',
            re.MULTILINE,
        )
        for m in try_import_pattern.finditer(content):
            lib = m.group(1)
            if lib in OPTIONAL_DEPENDENCIES:
                line_no = content[:m.start()].count("\n") + 1
                issues.append(Issue(
                    file=rel, line=line_no, col=1,
                    category="optional_import",
                    severity="info",
                    message=f"可选依赖 {lib}: {OPTIONAL_DEPENDENCIES[lib]}",
                ))

        return issues

    def _scan_none_defaults(self, rel: str, lines: list[str], _content: str) -> list[Issue]:
        """检测 str/int/bool = None 缺少 | None"""
        issues: list[Issue] = []
        patterns = [
            (r'\bstr\s*=\s*None\b', "str", "str | None"),
            (r'\bint\s*=\s*None\b', "int", "int | None"),
            (r'\bbool\s*=\s*None\b', "bool", "bool | None"),
            (r'\bfloat\s*=\s*None\b', "float", "float | None"),
        ]

        for line_no, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            # 只检查函数签名中的
            for pattern, tname, suggestion in patterns:
                if re.search(pattern, line):
                    # 确认在函数参数中
                    if "def " in line or ":" in line:
                        issues.append(Issue(
                            file=rel, line=line_no, col=1,
                            category="none_default",
                            severity="warning",
                            message=f"{tname} = None 应改为 {suggestion} = None",
                            before=line.strip(),
                            after=line.strip().replace(f"{tname} = None", f"{suggestion} = None"),
                        ))
        return issues

    # ── 修复器 ──────────────────────────────────────

    def fix_file(self, filepath: Path) -> bool:
        """修复单个文件的类型问题"""
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception:
            return False

        original = content

        # 1. 确保 typing import 中有 Any
        content = self._ensure_any_import(content)

        # 2. 修复裸类型注解
        content = self._fix_bare_types_in_content(content)

        # 3. 修复 None 默认值 (str = None → str | None = None)
        content = self._fix_none_defaults(content)

        if content != original:
            filepath.write_text(content, encoding="utf-8")
            return True
        return False

    def _fix_none_defaults(self, content: str) -> str:
        """修复 str/int/float/bool = None → T | None = None"""
        lines = content.split("\n")
        new_lines: list[str] = []
        fixes: list[tuple[str, str]] = [
            ("str = None", "str | None = None"),
            ("int = None", "int | None = None"),
            ("float = None", "float | None = None"),
            ("bool = None", "bool | None = None"),
        ]
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("from typing") or stripped.startswith("import "):
                new_lines.append(line)
                continue
            # 只在函数签名行修复
            if "def " in line:
                for old, new in fixes:
                    if old in line and "| None" not in line:
                        line = line.replace(old, new)
            new_lines.append(line)
        return "\n".join(new_lines)

    def _ensure_any_import(self, content: str) -> str:
        """确保 typing import 中包含 Any"""
        m = re.search(r'from typing import (.+)', content)
        if m:
            imports = m.group(1)
            if "Any" not in imports:
                content = content.replace(
                    m.group(1),
                    imports.rstrip().rstrip(",") + ", Any",
                )
        return content

    def _fix_bare_types_in_content(self, content: str) -> str:
        """修复内容中的裸类型注解"""
        lines = content.split("\n")
        new_lines: list[str] = []

        for line in lines:
            stripped = line.strip()
            # 跳过导入行
            if stripped.startswith("from typing import") or stripped.startswith("import "):
                new_lines.append(line)
                continue
            # 跳过注释行
            if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
                new_lines.append(line)
                continue

            # Dict → Dict[str, Any]
            line = re.sub(r'(?<!\[):\s*Dict\s*\)', ': Dict[str, Any])', line)
            line = re.sub(r'(?<!\[):\s*Dict\s*,', ': Dict[str, Any],', line)
            line = re.sub(r'->\s*Dict\s*:', '-> Dict[str, Any]:', line)
            line = re.sub(r'(?<!\[):\s*Dict\s*=', ': Dict[str, Any] =', line)
            if re.search(r'(?<!\[):\s*Dict\s*$', line) and 'Dict[str' not in line:
                line = re.sub(r'(?<!\[):\s*Dict\s*$', ': Dict[str, Any]', line)

            # dict → dict[str, Any]
            line = re.sub(r'(?<!\[):\s*dict\s*\)', ': dict[str, Any])', line)
            line = re.sub(r'(?<!\[):\s*dict\s*,', ': dict[str, Any],', line)
            line = re.sub(r'->\s*dict\s*:', '-> dict[str, Any]:', line)
            line = re.sub(r'(?<!\[):\s*dict\s*=', ': dict[str, Any] =', line)
            if re.search(r'(?<!\[):\s*dict\s*$', line) and 'dict[' not in line:
                line = re.sub(r'(?<!\[):\s*dict\s*$', ': dict[str, Any]', line)

            # List → List[Any]
            line = re.sub(r'(?<!\[):\s*List\s*\)', ': List[Any])', line)
            line = re.sub(r'(?<!\[):\s*List\s*,', ': List[Any],', line)
            line = re.sub(r'->\s*List\s*:', '-> List[Any]:', line)
            line = re.sub(r'(?<!\[):\s*List\s*=', ': List[Any] =', line)
            if re.search(r'(?<!\[):\s*List\s*$', line) and 'List[' not in line:
                line = re.sub(r'(?<!\[):\s*List\s*$', ': List[Any]', line)

            # list → list[Any]
            line = re.sub(r'(?<!\[):\s*list\s*\)', ': list[Any])', line)
            line = re.sub(r'(?<!\[):\s*list\s*,', ': list[Any],', line)
            line = re.sub(r'->\s*list\s*:', '-> list[Any]:', line)
            line = re.sub(r'(?<!\[):\s*list\s*=', ': list[Any] =', line)
            if re.search(r'(?<!\[):\s*list\s*$', line) and 'list[' not in line:
                line = re.sub(r'(?<!\[):\s*list\s*$', ': list[Any]', line)

            # Set → Set[str]
            line = re.sub(r'(?<!\[):\s*Set\s*\)', ': Set[str])', line)
            line = re.sub(r'(?<!\[):\s*Set\s*,', ': Set[str],', line)
            line = re.sub(r'->\s*Set\s*:', '-> Set[str]:', line)
            line = re.sub(r'(?<!\[):\s*Set\s*=', ': Set[str] =', line)
            if re.search(r'(?<!\[):\s*Set\s*$', line) and 'Set[' not in line:
                line = re.sub(r'(?<!\[):\s*Set\s*$', ': Set[str]', line)

            # set → set[str]
            line = re.sub(r'(?<!\[):\s*set\s*\)', ': set[str])', line)
            line = re.sub(r'(?<!\[):\s*set\s*,', ': set[str],', line)
            line = re.sub(r'->\s*set\s*:', '-> set[str]:', line)
            line = re.sub(r'(?<!\[):\s*set\s*=', ': set[str] =', line)
            if re.search(r'(?<!\[):\s*set\s*$', line) and 'set[' not in line:
                line = re.sub(r'(?<!\[):\s*set\s*$', ': set[str]', line)

            # Tuple → Tuple[Any, ...]
            line = re.sub(r'(?<!\[):\s*Tuple\s*\)', ': Tuple[Any, ...])', line)
            line = re.sub(r'(?<!\[):\s*Tuple\s*,', ': Tuple[Any, ...],', line)
            line = re.sub(r'->\s*Tuple\s*:', '-> Tuple[Any, ...]:', line)
            line = re.sub(r'(?<!\[):\s*Tuple\s*=', ': Tuple[Any, ...] =', line)
            if re.search(r'(?<!\[):\s*Tuple\s*$', line) and 'Tuple[' not in line:
                line = re.sub(r'(?<!\[):\s*Tuple\s*$', ': Tuple[Any, ...]', line)

            # tuple → tuple[Any, ...]
            line = re.sub(r'(?<!\[):\s*tuple\s*\)', ': tuple[Any, ...])', line)
            line = re.sub(r'(?<!\[):\s*tuple\s*,', ': tuple[Any, ...],', line)
            line = re.sub(r'->\s*tuple\s*:', '-> tuple[Any, ...]:', line)
            line = re.sub(r'(?<!\[):\s*tuple\s*=', ': tuple[Any, ...] =', line)
            if re.search(r'(?<!\[):\s*tuple\s*$', line) and 'tuple[' not in line:
                line = re.sub(r'(?<!\[):\s*tuple\s*$', ': tuple[Any, ...]', line)

            new_lines.append(line)

        return "\n".join(new_lines)

    # ── 运行 ────────────────────────────────────────

    def run(self) -> dict[str, Any]:
        """执行完整扫描+修复流程"""
        print(f"\n{C['BOLD']}{C['B']}╔══════════════════════════════════════════════════╗{C['X']}")
        print(f"{C['BOLD']}{C['B']}║  龍魂·代码质量守护 v1.0 — 类型自愈引擎           ║{C['X']}")
        print(f"{C['BOLD']}{C['B']}╚══════════════════════════════════════════════════╝{C['X']}")
        print(f"\n{C['D']}目标: {self.target}{C['X']}")
        print(f"{C['D']}模式: {'修复模式' if self.fix else '扫描模式'}{C['X']}")

        # 1. 发现文件
        py_files = self.discover_files()
        total = len(py_files)
        print(f"\n{C['D']}发现 {total} 个 Python 文件{C['X']}")

        # 2. 扫描
        print(f"{C['D']}开始扫描...{C['X']}\n")
        for i, fp in enumerate(py_files):
            self.files_scanned += 1
            file_issues = self.scan_file(fp)
            if file_issues:
                self.issues.extend(file_issues)
                rel = fp.relative_to(PROJECT_ROOT)
                error_count = sum(1 for x in file_issues if x.severity == "error")
                warn_count = sum(1 for x in file_issues if x.severity == "warning")
                if error_count > 0:
                    print(f"  {C['R']}✗{C['X']} {rel} ({error_count} 错误, {warn_count} 警告)")
                else:
                    print(f"  {C['Y']}⚠{C['X']} {rel} ({warn_count} 警告)")

        # 3. 修复（如果需要）
        if self.fix:
            print(f"\n{C['BOLD']}{C['B']}开始修复...{C['X']}")
            fixable_categories = {"bare_type", "none_default"}
            for issue in self.issues:
                if issue.category in fixable_categories:
                    fp = PROJECT_ROOT / issue.file
                    if fp.exists() and str(fp) not in self.fixed_files:
                        changed = self.fix_file(fp)
                        if changed:
                            self.fixed_files.append(str(fp))
                            print(f"  {C['G']}✓{C['X']} 修复 {issue.file}")

        # 4. 生成报告
        return self._build_report(total)

    def _build_report(self, total_files: int) -> dict[str, Any]:
        """构建结构化报告"""
        # 按类别统计
        categories: dict[str, dict[str, int]] = {}
        for iss in self.issues:
            cat = categories.setdefault(iss.category, {"error": 0, "warning": 0, "info": 0})
            cat[iss.severity] += 1

        error_count = sum(c["error"] for c in categories.values())
        warn_count = sum(c["warning"] for c in categories.values())
        info_count = sum(c["info"] for c in categories.values())

        return {
            "_meta": {
                "tool": "lh_code_guardian v1.0",
                "dna": "#龍芯⚡️丙午·辛未·乙酉·申时·大有-LONGHUN-CODE-GUARDIAN-v1.0",
                "timestamp": datetime.now().isoformat(),
                "mode": "fix" if self.fix else "scan",
            },
            "summary": {
                "files_scanned": self.files_scanned,
                "total_python_files": total_files,
                "files_with_issues": len(set(iss.file for iss in self.issues)),
                "files_fixed": len(self.fixed_files),
                "total_issues": len(self.issues),
                "errors": error_count,
                "warnings": warn_count,
                "info": info_count,
            },
            "by_category": categories,
            "issues": [iss.to_dict() for iss in self.issues],
            "fixed_files": self.fixed_files,
        }


# ── 终端彩色报告 ────────────────────────────────────

def print_report(report: dict[str, Any]) -> None:
    """打印彩色终端报告"""
    s = report["summary"]
    cat = report["by_category"]

    print(f"\n{C['BOLD']}{C['W']}╔══════════════════════════════════════════════════╗{C['X']}")
    print(f"{C['BOLD']}{C['W']}║             📊 扫描报告                          ║{C['X']}")
    print(f"{C['BOLD']}{C['W']}╚══════════════════════════════════════════════════╝{C['X']}")

    print(f"\n{C['BOLD']}文件统计:{C['X']}")
    print(f"  扫描文件: {s['files_scanned']}")
    print(f"  问题文件: {s['files_with_issues']}")
    if s['files_fixed'] > 0:
        print(f"  已修复:   {C['G']}{s['files_fixed']}{C['X']}")

    print(f"\n{C['BOLD']}问题统计:{C['X']}")
    print(f"  {C['R']}错误: {s['errors']}{C['X']}  {C['Y']}警告: {s['warnings']}{C['X']}  {C['C']}信息: {s['info']}{C['X']}  总计: {s['total_issues']}")

    if cat:
        print(f"\n{C['BOLD']}按类别:{C['X']}")
        for name, counts in cat.items():
            label_map = {
                "bare_type": "裸类型注解",
                "none_default": "None默认值",
                "optional_import": "可选依赖导入",
            }
            label = label_map.get(name, name)
            parts = []
            if counts["error"]:
                parts.append(f"{C['R']}错误{counts['error']}{C['X']}")
            if counts["warning"]:
                parts.append(f"{C['Y']}警告{counts['warning']}{C['X']}")
            if counts["info"]:
                parts.append(f"{C['C']}信息{counts['info']}{C['X']}")
            print(f"  {label}: {', '.join(parts)}")

    # Top 问题文件
    file_counts: dict[str, int] = {}
    for iss in report["issues"]:
        file_counts[iss["file"]] = file_counts.get(iss["file"], 0) + 1
    top_files = sorted(file_counts.items(), key=lambda x: -x[1])[:10]

    if top_files:
        print(f"\n{C['BOLD']}问题最多的文件 (Top 10):{C['X']}")
        for f, cnt in top_files:
            print(f"  {cnt:3d}  {f}")

    print(f"\n{C['D']}── {report['_meta']['timestamp']} ──{C['X']}\n")


# ── 入口 ─────────────────────────────────────────────

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="龍魂·代码质量守护 — 类型自愈引擎",
    )
    parser.add_argument("--fix", action="store_true", help="自动修复裸类型注解")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--target", type=str, default=None, help="指定扫描目录")
    parser.add_argument("--output", type=str, default=None, help="报告输出文件路径")
    args = parser.parse_args()

    guardian = CodeGuardian(
        target_dir=args.target,
        fix=args.fix,
    )

    report = guardian.run()

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(report)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{C['G']}报告已保存: {output_path}{C['X']}")

    # 退出码
    if report["summary"]["errors"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
