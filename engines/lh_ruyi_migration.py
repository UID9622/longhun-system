#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH·如意 代码迁移引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-RUYI-MIGRATION-v1.0

代码跨语言迁移 + 变量冲突检测 + 转移报告生成。

能力:
  - Python ↔ JavaScript 变量映射
  - 依赖检测与转换
  - 常见坑点自动检测 (异步/作用域/类型差异)
  - 生成完整迁移报告

🐉 心意所指·万物皆成
"""

import ast
import json
import re
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# ─── 数据类型 ───────────────────────────────────────────

@dataclass
class VariableMapping:
    """变量映射条目"""
    source_name: str
    source_type: str
    target_name: str
    target_type: str
    notes: str = ""
    risk_level: str = "🟢"  # 🟢低 🟡中 🔴高

@dataclass
class DependencyChange:
    """依赖变更"""
    source_dep: str
    target_dep: str
    category: str = "library"  # library/framework/builtin
    notes: str = ""

@dataclass
class MigrationPitfall:
    """迁移坑点"""
    location: str          # 代码位置
    description: str       # 坑点描述
    severity: str = "🟡"   # 🟡警告 🔴错误
    mitigation: str = ""   # 缓解方案

@dataclass
class MigrationReport:
    """完整迁移报告"""
    source_path: str = ""
    target_path: str = ""
    source_lang: str = ""
    target_lang: str = ""
    variable_mappings: List[VariableMapping] = field(default_factory=list)
    dependency_changes: List[DependencyChange] = field(default_factory=list)
    pitfalls: List[MigrationPitfall] = field(default_factory=list)
    audit_mark: str = "🟡"
    dna: str = ""
    generated_at: str = ""
    summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_markdown(self) -> str:
        """生成Markdown格式转移报告"""
        lines = []
        lines.append(f"# CNSH·如意 代码转移报告")
        lines.append(f"")
        lines.append(f"| 项目 | 值 |")
        lines.append(f"|:---|:---|")
        lines.append(f"| DNA | {self.dna} |")
        lines.append(f"| 源语言 | {self.source_lang} |")
        lines.append(f"| 目标语言 | {self.target_lang} |")
        lines.append(f"| 源路径 | {self.source_path} |")
        lines.append(f"| 目标路径 | {self.target_path} |")
        lines.append(f"| 审计 | {self.audit_mark} |")
        lines.append(f"| 生成时间 | {self.generated_at} |")
        lines.append(f"")

        if self.summary:
            lines.append(f"## 摘要")
            lines.append(f"{self.summary}")
            lines.append(f"")

        if self.variable_mappings:
            lines.append(f"## 变量映射表")
            lines.append(f"| 源变量 | 源类型 | 目标变量 | 目标类型 | 风险 | 备注 |")
            lines.append(f"|:---|:---|:---|:---|:---:|:---|")
            for m in self.variable_mappings:
                lines.append(f"| `{m.source_name}` | {m.source_type} | `{m.target_name}` | {m.target_type} | {m.risk_level} | {m.notes} |")
            lines.append(f"")

        if self.dependency_changes:
            lines.append(f"## 依赖变更")
            lines.append(f"| 源依赖 | 目标依赖 | 类型 | 备注 |")
            lines.append(f"|:---|:---|:---|:---|")
            for d in self.dependency_changes:
                lines.append(f"| `{d.source_dep}` | `{d.target_dep}` | {d.category} | {d.notes} |")
            lines.append(f"")

        if self.pitfalls:
            lines.append(f"## ⚠️ 迁移坑点")
            for i, p in enumerate(self.pitfalls, 1):
                lines.append(f"### {p.severity} 坑点 {i}: {p.description}")
                lines.append(f"- 位置: `{p.location}`")
                lines.append(f"- 缓解: {p.mitigation}")
                lines.append(f"")

        return "\n".join(lines)


# ─── 迁移引擎 ──────────────────────────────────────────

class RuyiMigrationEngine:
    """
    CNSH·如意 代码迁移引擎。

    核心功能:
    1. 分析源代码 → 提取变量/依赖/结构
    2. 目标语言映射 → 生成等价代码骨架
    3. 坑点检测 → 标注常见跨语言陷阱
    4. 生成转移报告 → Markdown格式
    """

    # Python → JavaScript 类型映射
    PY_TO_JS_TYPE_MAP = {
        "int": "number",
        "float": "number",
        "str": "string",
        "bool": "boolean",
        "list": "Array",
        "dict": "Object",
        "tuple": "Array",  # 不可变性需额外处理
        "set": "Set",
        "None": "null",
        "NoneType": "null",
        "bytes": "Uint8Array",
        "callable": "Function",
        "function": "function",
        "class": "class",
    }

    # Python → JavaScript 关键字映射
    PY_TO_JS_KEYWORD_MAP = {
        "True": "true",
        "False": "false",
        "None": "null",
        "and": "&&",
        "or": "||",
        "not": "!",
        "is": "===",
        "is not": "!==",
        "elif": "else if",
        "def": "function",
        "self": "this",
        "__init__": "constructor",
        "print": "console.log",
    }

    # 常见依赖映射
    DEPENDENCY_MAP = {
        "python": {
            "requests": ("axios", "HTTP client"),
            "flask": ("express", "Web framework"),
            "fastapi": ("express + zod", "API framework"),
            "sqlalchemy": ("knex.js / prisma", "ORM"),
            "pandas": ("danfo.js / arquero", "Data analysis"),
            "numpy": ("numjs / tensorflow.js", "Numerical computing"),
            "pillow": ("sharp", "Image processing"),
            "beautifulsoup4": ("cheerio", "HTML parsing"),
            "celery": ("bull", "Task queue"),
            "pytest": ("jest", "Testing"),
            "redis-py": ("ioredis", "Redis client"),
            "pymongo": ("mongoose", "MongoDB ODM"),
            "pyyaml": ("js-yaml", "YAML"),
            "python-dotenv": ("dotenv", "Environment variables"),
        },
        "javascript": {
            "axios": ("requests", "HTTP client"),
            "express": ("flask / fastapi", "Web framework"),
            "lodash": ("toolz / builtins", "Utility"),
            "moment": ("datetime + python-dateutil", "Date/time"),
            "jest": ("pytest", "Testing"),
            "prisma": ("sqlalchemy", "ORM"),
            "cheerio": ("beautifulsoup4", "HTML parsing"),
        },
    }

    # 常见迁移坑点
    COMMON_PITFALLS = {
        "python_to_js": [
            {
                "pattern": r"\basync\s+def\b",
                "description": "Python async/await 与 JS 的差异",
                "severity": "🟡",
                "mitigation": "Python asyncio 改为 JS async/await；事件循环模型不同，注意 run_until_complete → 自动执行"
            },
            {
                "pattern": r"\byield\b",
                "description": "Python generator 在 JS 中需用 function*",
                "severity": "🟡",
                "mitigation": "yield → function* / yield*；可迭代对象需转为 Array"
            },
            {
                "pattern": r"\b__\w+__\b",
                "description": "Python dunder 方法在 JS 中无直接等价",
                "severity": "🔴",
                "mitigation": "__init__ → constructor, __str__ → toString(), 其他需手动实现"
            },
            {
                "pattern": r"\bclass\s+\w+\(.*\):",
                "description": "Python 多继承 vs JS 单继承+混入",
                "severity": "🟡",
                "mitigation": "多继承 → 用 mixin 模式或 Object.assign 组合"
            },
            {
                "pattern": r"\bexcept\s+\w+\s+as\b",
                "description": "异常处理语义差异",
                "severity": "🟡",
                "mitigation": "except → catch；Python 的 except Exception as e → catch(e)"
            },
            {
                "pattern": r"\bfor\s+\w+\s+in\s+range\b",
                "description": "range() 在 JS 中无直接等价",
                "severity": "🟢",
                "mitigation": "for i in range(n) → for (let i = 0; i < n; i++)"
            },
            {
                "pattern": r"\[.*for.*in.*\]",
                "description": "列表推导式需转为 .map()/.filter()",
                "severity": "🟢",
                "mitigation": "[x for x in arr if cond] → arr.filter(x => cond).map(x => x)"
            },
            {
                "pattern": r"\bf-string\b|\bf['\"]",
                "description": "f-string 需转为模板字符串",
                "severity": "🟢",
                "mitigation": 'f"Hello {name}" → `Hello ${name}`'
            },
        ],
        "js_to_python": [
            {
                "pattern": r"\bconst\b|\blet\b|\bvar\b",
                "description": "JS 的 const/let 在 Python 中无直接声明等价",
                "severity": "🟢",
                "mitigation": "const → 用大写命名约定；let/var → 普通变量"
            },
            {
                "pattern": r"\.then\(|\.catch\(|async\s+function",
                "description": "Promise 链 vs async/await",
                "severity": "🟡",
                "mitigation": ".then().catch() → try/except + await；错误处理模型不同"
            },
            {
                "pattern": r"===|!==",
                "description": "严格相等 vs 宽松比较",
                "severity": "🟡",
                "mitigation": "=== → ==（Python 无类型强制比较）；注意 is vs =="
            },
            {
                "pattern": r"console\.log",
                "description": "调试输出转为 print",
                "severity": "🟢",
                "mitigation": "console.log → print"
            },
        ],
    }

    def __init__(self):
        pass

    # ─── 主入口 ─────────────────────────────────────

    def analyze_and_migrate(self,
                            source_code: str,
                            source_lang: str = "python",
                            target_lang: str = "javascript",
                            source_path: str = "",
                            target_path: str = "",
                            ) -> MigrationReport:
        """
        分析源代码并生成迁移报告。

        Args:
            source_code: 源代码文本
            source_lang: 源语言 (python/javascript)
            target_lang: 目标语言 (javascript/python)
            source_path: 源文件路径
            target_path: 目标文件路径

        Returns:
            MigrationReport: 完整迁移报告
        """
        report = MigrationReport(
            source_path=source_path,
            target_path=target_path,
            source_lang=source_lang,
            target_lang=target_lang,
            generated_at=datetime.now().isoformat(),
        )

        # 1. 提取变量
        variables = self._extract_variables(source_code, source_lang)
        report.variable_mappings = self._map_variables(variables, source_lang, target_lang)

        # 2. 提取依赖
        dependencies = self._extract_dependencies(source_code, source_lang)
        report.dependency_changes = self._map_dependencies(dependencies, source_lang, target_lang)

        # 3. 坑点检测
        report.pitfalls = self._detect_pitfalls(source_code, source_lang, target_lang)

        # 4. 审计标记
        report.audit_mark = self._calculate_audit(report)

        # 5. 摘要
        report.summary = self._generate_summary(report)

        # 6. DNA
        import hashlib
        report.dna = f"#MIG⚡️{hashlib.sha256(source_code.encode()).hexdigest()[:12]}"

        return report

    # ─── 变量提取 ────────────────────────────────────

    def _extract_variables(self, code: str, lang: str) -> List[Tuple[str, str]]:
        """提取变量名和推断类型"""
        variables = []

        if lang == "python":
            try:
                tree = ast.parse(code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                var_type = self._infer_type_python(node.value)
                                variables.append((target.id, var_type))
                    elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                        type_str = self._get_type_string(node.annotation)
                        variables.append((node.target.id, type_str or "unknown"))
            except SyntaxError:
                # 回退到正则
                variables.extend(self._extract_variables_regex(code, lang))
        else:
            variables.extend(self._extract_variables_regex(code, lang))

        return variables

    def _infer_type_python(self, node) -> str:
        """从AST节点推断类型"""
        if isinstance(node, ast.Constant):
            if isinstance(node.value, int):
                return "int"
            elif isinstance(node.value, float):
                return "float"
            elif isinstance(node.value, str):
                return "str"
            elif isinstance(node.value, bool):
                return "bool"
            elif node.value is None:
                return "NoneType"
        elif isinstance(node, ast.List):
            return "list"
        elif isinstance(node, ast.Dict):
            return "dict"
        elif isinstance(node, ast.Tuple):
            return "tuple"
        elif isinstance(node, ast.Set):
            return "set"
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                type_hints = {
                    "dict": "dict", "list": "list", "set": "set",
                    "tuple": "tuple", "int": "int", "str": "str",
                    "float": "float", "bool": "bool",
                }
                return type_hints.get(node.func.id, "unknown")
        return "unknown"

    def _get_type_string(self, annotation) -> str:
        """从类型注解提取字符串"""
        if isinstance(annotation, ast.Name):
            return annotation.id
        return ""

    def _extract_variables_regex(self, code: str, lang: str) -> List[Tuple[str, str]]:
        """正则回退提取变量"""
        if lang == "python":
            patterns = [
                (r'^(\w+)\s*=\s*(["\'])(.*?)\2', "str"),
                (r'^(\w+)\s*=\s*(\d+\.\d+)', "float"),
                (r'^(\w+)\s*=\s*(\d+)', "int"),
                (r'^(\w+)\s*=\s*\[', "list"),
                (r'^(\w+)\s*=\s*\{', "dict"),
                (r'^(\w+)\s*=\s*True|False', "bool"),
                (r'^(\w+)\s*=\s*None', "NoneType"),
            ]
        else:
            patterns = [
                (r'(?:const|let|var)\s+(\w+)\s*=\s*(["\'])(.*?)\2', "string"),
                (r'(?:const|let|var)\s+(\w+)\s*=\s*(\d+\.\d+)', "number"),
                (r'(?:const|let|var)\s+(\w+)\s*=\s*(\d+)', "number"),
                (r'(?:const|let|var)\s+(\w+)\s*=\s*\[', "Array"),
                (r'(?:const|let|var)\s+(\w+)\s*=\s*\{', "Object"),
                (r'(?:const|let|var)\s+(\w+)\s*=\s*true|false', "boolean"),
                (r'(?:const|let|var)\s+(\w+)\s*=\s*null', "null"),
            ]

        results = []
        for line in code.split("\n"):
            line = line.strip()
            for pattern, type_str in patterns:
                m = re.match(pattern, line)
                if m:
                    results.append((m.group(1), type_str))
                    break
        return results

    # ─── 变量映射 ────────────────────────────────────

    def _map_variables(self, variables: List[Tuple[str, str]],
                       source_lang: str, target_lang: str) -> List[VariableMapping]:
        """将源语言变量映射到目标语言"""
        mappings = []

        if source_lang == "python" and target_lang == "javascript":
            type_map = self.PY_TO_JS_TYPE_MAP
        else:
            type_map = {v: k for k, v in self.PY_TO_JS_TYPE_MAP.items()}

        for var_name, var_type in variables:
            target_type = type_map.get(var_type, var_type)

            # 命名风格转换
            target_name = self._convert_naming(var_name, source_lang, target_lang)

            # 风险评估
            risk = "🟢"
            notes = ""
            if var_type == "tuple" and target_lang == "javascript":
                risk = "🟡"
                notes = "元组不可变性在JS中需手动保证"
            elif var_type == "NoneType" and target_lang == "javascript":
                risk = "🟡"
                notes = "JS中null与undefined语义不同"

            mappings.append(VariableMapping(
                source_name=var_name,
                source_type=var_type,
                target_name=target_name,
                target_type=target_type,
                risk_level=risk,
                notes=notes,
            ))

        return mappings

    def _convert_naming(self, name: str, source_lang: str, target_lang: str) -> str:
        """命名风格转换"""
        # Python snake_case → JS camelCase
        if source_lang == "python" and target_lang == "javascript":
            if "_" in name:
                parts = name.split("_")
                return parts[0] + "".join(p.capitalize() for p in parts[1:])
        # JS camelCase → Python snake_case
        elif source_lang == "javascript" and target_lang == "python":
            return re.sub(r'([A-Z])', r'_\1', name).lower().lstrip("_")
        return name

    # ─── 依赖提取与映射 ─────────────────────────────

    def _extract_dependencies(self, code: str, lang: str) -> List[str]:
        """提取代码依赖"""
        deps = []

        if lang == "python":
            # import xxx / from xxx import yyy
            deps.extend(re.findall(r'^import\s+(\w+)', code, re.MULTILINE))
            deps.extend(re.findall(r'^from\s+(\w+)', code, re.MULTILINE))
        else:
            # require('xxx') / import xxx from 'xxx'
            deps.extend(re.findall(r"require\(['\"](\S+?)['\"]", code))
            deps.extend(re.findall(r"from\s+['\"](\S+?)['\"]", code))

        return list(set(deps))

    def _map_dependencies(self, deps: List[str],
                          source_lang: str, target_lang: str) -> List[DependencyChange]:
        """映射依赖"""
        changes = []
        dep_map = self.DEPENDENCY_MAP.get(source_lang, {})

        for dep in deps:
            # 跳过标准库
            if self._is_stdlib(dep, source_lang):
                continue

            if dep in dep_map:
                target_dep, category = dep_map[dep]
                changes.append(DependencyChange(
                    source_dep=dep,
                    target_dep=target_dep,
                    category=category,
                    notes=f"自动映射: {dep} → {target_dep}",
                ))
            else:
                changes.append(DependencyChange(
                    source_dep=dep,
                    target_dep=f"待定 ({dep} 的 {target_lang} 等价库)",
                    category="library",
                    notes="未在已知映射表中，需手动查找等价库",
                ))

        return changes

    def _is_stdlib(self, dep: str, lang: str) -> bool:
        """检查是否标准库"""
        if lang == "python":
            stdlib = {"os", "sys", "re", "json", "math", "time", "datetime",
                      "collections", "itertools", "functools", "typing",
                      "pathlib", "hashlib", "random", "subprocess", "io",
                      "csv", "xml", "html", "http", "logging", "unittest"}
            return dep in stdlib
        return False

    # ─── 坑点检测 ────────────────────────────────────

    def _detect_pitfalls(self, code: str, source_lang: str, target_lang: str) -> List[MigrationPitfall]:
        """检测迁移坑点"""
        pitfalls = []
        key = f"{source_lang}_to_{target_lang[:2]}"

        patterns = self.COMMON_PITFALLS.get(key, [])

        for pitfall_def in patterns:
            if re.search(pitfall_def["pattern"], code, re.MULTILINE):
                # 找第一个匹配位置
                m = re.search(pitfall_def["pattern"], code, re.MULTILINE)
                loc = f"行{m.group(0)[:40]}..." if m else "未知"

                pitfalls.append(MigrationPitfall(
                    location=loc,
                    description=pitfall_def["description"],
                    severity=pitfall_def["severity"],
                    mitigation=pitfall_def["mitigation"],
                ))

        return pitfalls

    # ─── 审计 ────────────────────────────────────────

    def _calculate_audit(self, report: MigrationReport) -> str:
        """计算审计标记"""
        red_count = sum(1 for p in report.pitfalls if p.severity == "🔴")
        yellow_count = sum(1 for p in report.pitfalls if p.severity == "🟡")

        if red_count > 0:
            return "🔴"
        elif yellow_count > 3:
            return "🟡"
        return "🟢"

    def _generate_summary(self, report: MigrationReport) -> str:
        """生成摘要"""
        parts = []
        parts.append(f"从 {report.source_lang} 迁移到 {report.target_lang}")
        parts.append(f"共 {len(report.variable_mappings)} 个变量映射")
        parts.append(f"{len(report.dependency_changes)} 个依赖变更")
        parts.append(f"{len(report.pitfalls)} 个潜在坑点")

        red = sum(1 for p in report.pitfalls if p.severity == "🔴")
        yellow = sum(1 for p in report.pitfalls if p.severity == "🟡")
        if red > 0:
            parts.append(f"⚠️ {red}个严重问题需处理")
        if yellow > 0:
            parts.append(f"⚠️ {yellow}个中等风险需关注")

        parts.append(f"审计: {report.audit_mark}")
        return "；".join(parts)


# ─── 便捷函数 ──────────────────────────────────────────

def migrate_code(source_code: str,
                 source_lang: str = "python",
                 target_lang: str = "javascript",
                 source_path: str = "",
                 target_path: str = "") -> MigrationReport:
    """一键迁移代码并生成报告"""
    engine = RuyiMigrationEngine()
    return engine.analyze_and_migrate(
        source_code, source_lang, target_lang, source_path, target_path
    )


# ─── 自测 ──────────────────────────────────────────────

if __name__ == "__main__":
    print("🧪 CNSH·如意 代码迁移引擎 自测")
    print("=" * 60)

    # 测试Python代码
    test_py = '''
import requests
import json

class UserService:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.cache = {}

    async def get_user(self, user_id: int):
        if user_id in self.cache:
            return self.cache[user_id]
        response = requests.get(f"{self.base_url}/users/{user_id}")
        user_data = response.json()
        self.cache[user_id] = user_data
        return user_data

    def get_all_users(self) -> list:
        names = [u["name"] for u in self.cache.values() if u.get("active")]
        return names

config = {
    "debug": True,
    "timeout": 30,
    "retries": 3,
}
'''

    engine = RuyiMigrationEngine()
    report = engine.analyze_and_migrate(
        test_py,
        source_lang="python",
        target_lang="javascript",
        source_path="services/user_service.py",
        target_path="services/userService.js",
    )

    print(report.to_markdown())
    print("\n✅ 迁移引擎自测完成")
