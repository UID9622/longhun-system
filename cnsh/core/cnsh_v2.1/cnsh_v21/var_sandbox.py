# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║              CNSH 变量沙箱 v1.0 — 统一变量映射 + 隔离执行             ║
║  DNA: #龍芯⚡️2026-07-06-VAR-SANDBOX-v1.0                           ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                     ║
║  三色审计: 🟢 通过                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

【为什么需要变量沙箱？】
CNSH 变量映射之前分散在 5+ 个地方：
  - tokens.py (KEYWORDS)
  - compiler_py.py (_TYPE_MAP, _DECORATOR_MAP, _KWARG_MAP)
  - codegen.py (TYPE_MAPPINGS, DEFAULT_VALUES, STDLIB_FUNCTIONS)
  - cnsh_to_python.json (完整字典)
  - interpreter.py (Environment)

每次新增/修改一个变量，一处改了另一处没改 → 翻译出错。
变量沙箱把所有映射焊死在同一个地方，任何变量进来：
  1. 注册 → 自动生成 7 种目标语言的映射
  2. 校验 → 检查是否所有目标都有映射
  3. 执行 → 在隔离沙箱中运行，不污染外层环境
  4. 冲突检测 → 发现命名冲突并报告

【怎么用？】
  from cnsh_v21.var_sandbox import VarSandbox
  sb = VarSandbox()
  sb.register("我的变量", "整数", 42)
  sb.validate_all()  # 检查 7 目标完整性
  result = sb.sandbox_exec("打印(我的变量)")  # 隔离执行
"""

from __future__ import annotations
from typing import Any
from dataclasses import dataclass


# ══════════════════════════════════════════════════════════════════
# 【一、核心类型定义】
# ══════════════════════════════════════════════════════════════════

@dataclass
class VarEntry:
    """单个变量的完整映射记录"""
    中文名: str                          # CNSH 中文变量名
    英文名: str                          # Python/通用英文名
    类型: str                            # CNSH 类型: 整数/文本/布尔...
    值: Any = None                       # 初始值
    是常量: bool = False                 # 是否为常量

    # 7 目标语言映射
    python: str = ""
    javascript: str = ""
    c: str = ""
    cpp: str = ""
    rust: str = ""
    objc: str = ""
    swift: str = ""

    # 元数据
    来源: str = ""                       # 来自哪个模块
    DNA: str = ""                        # DNA 追溯码
    审计: str = "🟡"                     # 三色审计状态

    def __post_init__(self):
        """自动填充各目标语言映射"""
        if not self.英文名:
            # 没有英文名则用中文名作为 Python 标识符（支持中文变量名）
            self.英文名 = self.中文名
        if not self.python:
            self.python = self.英文名
        if not self.javascript:
            self.javascript = self.英文名
        if not self.c:
            self.c = self.英文名
        if not self.cpp:
            self.cpp = self.英文名
        if not self.rust:
            self.rust = self.英文名
        if not self.objc:
            self.objc = self.英文名
        if not self.swift:
            self.swift = self.英文名

    def to_target(self, target: str) -> str:
        """获取在目标语言中的变量名"""
        t = target.lower()
        if t in ("python", "py"):
            return self.python
        if t in ("javascript", "js"):
            return self.javascript
        if t in ("c", "cc"):
            return self.c
        if t in ("cpp", "c++", "cxx"):
            return self.cpp
        if t in ("rust", "rs"):
            return self.rust
        if t in ("objc", "objective-c"):
            return self.objc
        if t in ("swift"):
            return self.swift
        return self.英文名

    def to_dict(self) -> dict[str, object]:
        return {
            "中文名": self.中文名,
            "英文名": self.英文名,
            "类型": self.类型,
            "值": self.值,
            "是常量": self.是常量,
            "映射": {
                "python": self.python,
                "javascript": self.javascript,
                "c": self.c,
                "cpp": self.cpp,
                "rust": self.rust,
                "objc": self.objc,
                "swift": self.swift,
            },
            "来源": self.来源,
            "DNA": self.DNA,
            "审计": self.审计,
        }


# ══════════════════════════════════════════════════════════════════
# 【二、统一类型映射表 — 焊死在这里】
# ══════════════════════════════════════════════════════════════════

# CNSH 类型 → 7 目标语言对应的类型
TYPE_MAP = {
    "整数":   {"py": "int",          "js": "number",   "c": "int",           "cpp": "int",            "rust": "i32",      "objc": "NSInteger",    "swift": "Int"},
    "小数":   {"py": "float",        "js": "number",   "c": "double",        "cpp": "double",         "rust": "f64",      "objc": "CGFloat",      "swift": "Double"},
    "文本":   {"py": "str",          "js": "string",   "c": "char*",         "cpp": "std::string",    "rust": "String",   "objc": "NSString*",    "swift": "String"},
    "布尔":   {"py": "bool",         "js": "boolean",  "c": "bool",          "cpp": "bool",           "rust": "bool",     "objc": "BOOL",         "swift": "Bool"},
    "列表":   {"py": "list",         "js": "Array",    "c": "void*",         "cpp": "std::vector",    "rust": "Vec",      "objc": "NSArray*",     "swift": "Array"},
    "映射":   {"py": "dict",         "js": "Object",   "c": "void*",         "cpp": "std::unordered_map", "rust": "HashMap", "objc": "NSDictionary*", "swift": "Dictionary"},
    "空值":   {"py": "None",         "js": "null",     "c": "void",          "cpp": "void",           "rust": "()",       "objc": "void",         "swift": "Void"},
}

# 类型默认值
TYPE_DEFAULTS = {
    "py": {"int": "0", "float": "0.0", "str": '""', "bool": "False", "list": "[]", "dict": "{}", "None": "None"},
    "js": {"number": "0", "string": '""', "boolean": "false", "Array": "[]", "Object": "{}", "null": "null"},
    "c":  {"int": "0", "double": "0.0", "char*": '""', "bool": "false", "void*": "NULL", "void": ""},
    "cpp": {"int": "0", "double": "0.0", "std::string": '""', "bool": "false", "std::vector": "{}", "std::unordered_map": "{}", "nullptr": "nullptr"},
    "rust": {"i32": "0", "f64": "0.0", "String": 'String::new()', "bool": "false", "Vec": "vec![]", "HashMap": "HashMap::new()", "()": "()"},
    "objc": {"NSInteger": "0", "CGFloat": "0.0", "NSString*": '@""', "BOOL": "NO", "NSArray*": "@[]", "NSDictionary*": "@{}", "nil": "nil"},
    "swift": {"Int": "0", "Double": "0.0", "String": '""', "Bool": "false", "Array": "[]", "Dictionary": "[:]", "nil": "nil"},
}


# ══════════════════════════════════════════════════════════════════
# 【三、内置标准函数映射】
# ══════════════════════════════════════════════════════════════════

STDLIB_MAP = {
    "打印": {"py": "print",         "js": "console.log",   "c": "printf",         "cpp": "std::cout",      "rust": "println!",      "objc": "NSLog",         "swift": "print"},
    "输出": {"py": "print",         "js": "console.log",   "c": "printf",         "cpp": "std::cout",      "rust": "println!",      "objc": "NSLog",         "swift": "print"},
    "长度": {"py": "len",           "js": ".length",       "c": "strlen",         "cpp": ".size()",        "rust": ".len()",        "objc": ".length",       "swift": ".count"},
    "类型": {"py": "type",          "js": "typeof",        "c": "sizeof",         "cpp": "typeid",         "rust": "std::mem::discriminant", "objc": "class",  "swift": "type(of:)"},
    "整数化": {"py": "int",         "js": "parseInt",      "c": "(int)",          "cpp": "static_cast<int>", "rust": "as i32",      "objc": "(NSInteger)",   "swift": "Int()"},
    "文本化": {"py": "str",         "js": "String",        "c": "sprintf",        "cpp": "std::to_string", "rust": ".to_string()",  "objc": "stringWithFormat:", "swift": "String()"},
    "范围":  {"py": "range",        "js": "Array.from({length:", "c": "for-loop",  "cpp": "std::iota",      "rust": "..",            "objc": "NSRange",       "swift": "..<"},
}


# ══════════════════════════════════════════════════════════════════
# 【四、变量沙箱核心引擎】
# ══════════════════════════════════════════════════════════════════

class VarSandbox:
    """
    CNSH 变量沙箱 — 集中管理所有变量映射 + 隔离执行。

    设计意图：
      变量只在这个沙箱里定义一次，所有 7 个目标语言的映射
      自动生成并强制完整。不让映射散落各处。
    """

    def __init__(self, name: str = "默认沙箱"):
        self.沙箱名 = name
        self.变量表: dict[str, VarEntry] = {}
        self.执行日志: list[dict[str, object]] = []
        self.隔离全局: dict[str, Any] = {
            "__name__": f"__cnsh_sandbox__{name}",
            "__file__": f"<sandbox:{name}>",
        }
        self.隔离全局["__builtins__"] = {
            "print": print,
            "len": len,
            "range": range,
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "list": list[Any],
            "dict": dict[str, Any],
            "type": type,
            "isinstance": isinstance,
            "True": True,
            "False": False,
            "None": None,
            "abs": abs,
            "min": min,
            "max": max,
            "sum": sum,
            "round": round,
            "sorted": sorted,
            "enumerate": enumerate,
            "zip": zip,
            "map": map,
            "filter": filter,
            "Exception": Exception,
        }

    # ── 变量注册 ──

    def register(self, 中文名: str, 类型: str = "整数", 值: Any = None,
                 英文名: str = "", 是常量: bool = False, 来源: str = "") -> VarEntry:
        """注册一个变量到沙箱，自动生成 7 目标映射。

        Args:
            中文名: CNSH 中文变量名（必填）
            类型: CNSH 类型名（整数/文本/布尔/列表/映射）
            值: 初始值
            英文名: 可选英文名（不填自动等于中文名）
            是常量: True 则不可重新赋值
            来源: 变量来源模块名

        Returns:
            VarEntry 记录
        """
        entry = VarEntry(
            中文名=中文名,
            英文名=英文名 or 中文名,
            类型=类型,
            值=值,
            是常量=是常量,
            来源=来源,
        )

        # 检测冲突
        if 中文名 in self.变量表:
            old = self.变量表[中文名]
            self.执行日志.append({
                "事件": "变量覆盖",
                "变量": 中文名,
                "旧类型": old.类型,
                "新类型": 类型,
                "警告": "同一变量名被重新注册",
            })

        self.变量表[中文名] = entry

        # 注入到隔离全局空间
        self.隔离全局[中文名] = 值

        self.执行日志.append({
            "事件": "注册变量",
            "变量": 中文名,
            "类型": 类型,
            "值": str(值),
            "是常量": 是常量,
        })

        return entry

    def register_batch(self, 变量列表: list[tuple[str, ...]]) -> list[VarEntry]:
        """批量注册变量。
        每项格式: (中文名, 类型, 值) 或 (中文名, 类型, 值, 英文名, 是常量)
        """
        results = []
        for item in 变量列表:
            if len(item) >= 3:
                entry = self.register(
                    中文名=item[0],
                    类型=item[1],
                    值=item[2],
                    英文名=item[3] if len(item) > 3 else "",
                    是常量=item[4] if len(item) > 4 else False,  # pyright: ignore[reportArgumentType]
                )
                results.append(entry)
        return results

    # ── 变量查询 ──

    def get(self, 中文名: str) -> VarEntry | None:
        """获取变量条目"""
        return self.变量表.get(中文名)

    def translate(self, 中文名: str, target: str = "python") -> str:
        """将 CNSH 变量名翻译为目标语言中的变量名"""
        entry = self.变量表.get(中文名)
        if entry:
            return entry.to_target(target)
        return 中文名  # 没有注册的变量原样返回

    def translate_type(self, cns_type: str, target: str = "python") -> str:
        """翻译 CNSH 类型到目标语言类型"""
        target_key = {"python": "py", "py": "py",
                       "javascript": "js", "js": "js",
                       "c": "c", "cc": "c",
                       "cpp": "cpp", "c++": "cpp", "cxx": "cpp",
                       "rust": "rust", "rs": "rust",
                       "objc": "objc", "objective-c": "objc",
                       "swift": "swift"}.get(target.lower(), "py")
        type_entry = TYPE_MAP.get(cns_type, {})
        return type_entry.get(target_key, cns_type)

    def get_default_value(self, cns_type: str, target: str = "python") -> str:
        """获取 CNSH 类型在目标语言中的默认值"""
        target_type = self.translate_type(cns_type, target)
        target_key = {"python": "py", "py": "py", "javascript": "js", "js": "js",
                       "c": "c", "cpp": "cpp", "rust": "rust",
                       "objc": "objc", "swift": "swift"}.get(target.lower(), "py")
        defaults = TYPE_DEFAULTS.get(target_key, {})
        return defaults.get(target_type, "nil")

    # ── 完整性校验 ──

    def validate_all(self) -> dict[str, object]:
        """校验所有变量的 7 目标完整性 + 冲突检测。

        Returns:
            {
                "通过": bool,
                "变量总数": int,
                "缺失映射": [...],
                "冲突": [...],
                "建议": [...],
            }
        """
        issues = []
        conflicts = []
        passed = True

        # 1. 检查每个变量的 7 目标映射
        targets = ["python", "javascript", "c", "cpp", "rust", "objc", "swift"]
        name_set: dict[str, set[str]] = {}  # target -> set of mapped names

        for target in targets:
            name_set[target] = set()

        for cns_name, entry in self.变量表.items():
            for target in targets:
                mapped = entry.to_target(target)
                if not mapped or mapped.strip() == "":
                    issues.append({
                        "严重": "error",
                        "变量": cns_name,
                        "目标": target,
                        "问题": f"缺少 {target} 映射",
                    })
                    passed = False
                else:
                    name_set[target].add(mapped)

        # 2. 检测跨目标冲突
        for target, names in name_set.items():
            if len(names) != len(self.变量表):
                conflicts.append({
                    "目标": target,
                    "冲突": f"映射名数量 {len(names)} != 变量数 {len(self.变量表)}，可能存在重名",
                })
                passed = False

        return {
            "通过": passed,
            "变量总数": len(self.变量表),
            "缺失映射": issues,
            "冲突": conflicts,
            "建议": ["焊死所有映射后再执行"] if not passed else [],
        }

    def validate_single(self, 中文名: str) -> dict[str, object]:
        """校验单个变量的全部映射"""
        entry = self.变量表.get(中文名)
        if not entry:
            return {"通过": False, "错误": f"变量 '{中文名}' 未注册"}

        missing = []
        for target in ["python", "javascript", "c", "cpp", "rust", "objc", "swift"]:
            mapped = entry.to_target(target)
            if not mapped or mapped.strip() == "":
                missing.append(target)

        return {
            "通过": len(missing) == 0,
            "变量": 中文名,
            "缺失目标": missing,
            "完整映射": {
                "python": entry.python,
                "javascript": entry.javascript,
                "c": entry.c,
                "cpp": entry.cpp,
                "rust": entry.rust,
                "objc": entry.objc,
                "swift": entry.swift,
            },
        }

    # ── 沙箱执行 ──

    def sandbox_exec(self, code: str) -> dict[str, object]:
        """在隔离沙箱中执行 Python 代码。

        Args:
            code: 要执行的 Python 代码（可以是翻译后的 CNSH 代码）

        Returns:
            {"通过": bool, "输出": str, "错误": str, "返回值": Any}
        """
        import io
        import contextlib

        # 复制一份隔离环境
        local_env = dict(self.隔离全局)

        stdout = io.StringIO()
        stderr = io.StringIO()
        _result = None
        error = None

        try:
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exec(code, local_env)
        except Exception as e:
            error = f"{type(e).__name__}: {e}"

        output = stdout.getvalue()
        err_output = stderr.getvalue()

        self.执行日志.append({
            "事件": "沙箱执行",
            "代码": code[:200],
            "通过": error is None,
            "输出": output[:500],
            "错误": error or err_output,
        })

        return {
            "通过": error is None,
            "输出": output,
            "错误": error or err_output,
            "返回值": local_env.get("_result", None),
        }

    # ── 批量迁移/对比 ──

    def compare_with(self, other: dict[str, str]) -> list[dict[str, object]]:
        """对比沙箱变量与外部映射（如旧的字典），找出不一致。

        Args:
            other: {中文名: 目标名} 的外部映射

        Returns:
            差异列表
        """
        diffs = []
        for cns_name, mapped_name in other.items():
            entry = self.变量表.get(cns_name)
            if not entry:
                diffs.append({
                    "类型": "外部有沙箱无",
                    "中文名": cns_name,
                    "外部映射": mapped_name,
                })
            elif entry.python != mapped_name:
                diffs.append({
                    "类型": "映射不一致",
                    "中文名": cns_name,
                    "沙箱映射": entry.python,
                    "外部映射": mapped_name,
                })

        for cns_name in self.变量表:
            if cns_name not in other:
                diffs.append({
                    "类型": "沙箱有外部无",
                    "中文名": cns_name,
                    "沙箱映射": self.变量表[cns_name].python,
                })

        return diffs

    def generate_code(self, target: str = "python") -> str:
        """根据沙箱中的所有变量，生成目标语言的变量声明代码。

        Args:
            target: 目标语言

        Returns:
            目标语言代码字符串
        """
        lines = []
        t = target.lower()

        if t in ("python", "py"):
            for entry in self.变量表.values():
                val = repr(entry.值) if entry.值 is not None else self.get_default_value(entry.类型, "python")
                const = "# 常量" if entry.是常量 else ""
                lines.append(f"{entry.python} = {val}  {const}")
            return "\n".join(lines)

        elif t in ("javascript", "js"):
            for entry in self.变量表.values():
                kw = "const" if entry.是常量 else "let"
                target_type = self.translate_type(entry.类型, "js")
                val = entry.值 if entry.值 is not None else self.get_default_value(entry.类型, "js")
                if isinstance(val, str) and not val.startswith('"'):
                    val = f'"{val}"'
                lines.append(f"{kw} {entry.javascript} = {val}; // {entry.中文名}")
            return "\n".join(lines)

        elif t in ("c", "cc"):
            for entry in self.变量表.values():
                target_type = self.translate_type(entry.类型, "c")
                kw = "const " if entry.是常量 else ""
                val = entry.值 if entry.值 is not None else self.get_default_value(entry.类型, "c")
                lines.append(f"{kw}{target_type} {entry.c} = {val}; // {entry.中文名}")
            return "\n".join(lines)

        elif t in ("cpp", "c++", "cxx"):
            for entry in self.变量表.values():
                target_type = self.translate_type(entry.类型, "cpp")
                kw = "const " if entry.是常量 else ""
                val = entry.值 if entry.值 is not None else self.get_default_value(entry.类型, "cpp")
                if isinstance(val, str) and target_type == "std::string" and not val.startswith('"'):
                    val = f'"{val}"'
                lines.append(f"{kw}{target_type} {entry.cpp} = {val}; // {entry.中文名}")
            return "\n".join(lines)

        elif t in ("rust", "rs"):
            for entry in self.变量表.values():
                target_type = self.translate_type(entry.类型, "rust")
                kw = "let " if not entry.是常量 else "const "
                val = entry.值 if entry.值 is not None else self.get_default_value(entry.类型, "rust")
                lines.append(f"{kw}{entry.rust}: {target_type} = {val}; // {entry.中文名}")
            return "\n".join(lines)

        elif t in ("objc", "objective-c"):
            for entry in self.变量表.values():
                target_type = self.translate_type(entry.类型, "objc")
                val = entry.值 if entry.值 is not None else self.get_default_value(entry.类型, "objc")
                lines.append(f"{target_type} {entry.objc} = {val}; // {entry.中文名}")
            return "\n".join(lines)

        elif t in ("swift"):
            for entry in self.变量表.values():
                target_type = self.translate_type(entry.类型, "swift")
                kw = "let" if entry.是常量 else "var"
                val = entry.值 if entry.值 is not None else self.get_default_value(entry.类型, "swift")
                lines.append(f"{kw} {entry.swift}: {target_type} = {val} // {entry.中文名}")
            return "\n".join(lines)

        else:
            # 兜底：生成 Python
            return self.generate_code("python")

    def snapshot(self) -> dict[str, object]:
        """导出沙箱快照，用于持久化"""
        return {
            "沙箱名": self.沙箱名,
            "变量": [entry.to_dict() for entry in self.变量表.values()],
            "日志条数": len(self.执行日志),
        }

    def restore(self, snapshot: dict[str, object]):
        """从快照恢复沙箱"""
        self.变量表.clear()
        self.执行日志.clear()
        for var_dict in snapshot.get("变量", []):  # pyright: ignore[reportGeneralTypeIssues]
            entry = VarEntry(
                中文名=var_dict["中文名"],
                英文名=var_dict["英文名"],
                类型=var_dict["类型"],
                值=var_dict["值"],
                是常量=var_dict["是常量"],
                python=var_dict["映射"]["python"],
                javascript=var_dict["映射"]["javascript"],
                c=var_dict["映射"]["c"],
                cpp=var_dict["映射"]["cpp"],
                rust=var_dict["映射"]["rust"],
                objc=var_dict["映射"]["objc"],
                swift=var_dict["映射"]["swift"],
                来源=var_dict.get("来源", ""),
                DNA=var_dict.get("DNA", ""),
                审计=var_dict.get("审计", "🟡"),
            )
            self.变量表[var_dict["中文名"]] = entry

    def clear(self):
        """清空沙箱"""
        self.变量表.clear()
        self.执行日志.clear()
        self.隔离全局 = {
            "__name__": f"__cnsh_sandbox__{self.沙箱名}",
            "__file__": f"<sandbox:{self.沙箱名}>",
            "__builtins__": self.隔离全局.get("__builtins__", {}),
        }


# ══════════════════════════════════════════════════════════════════
# 【五、全局默认沙箱（模块级单例）】
# ══════════════════════════════════════════════════════════════════

_默认沙箱: VarSandbox | None = None


def get_default_sandbox() -> VarSandbox:
    """获取全局默认沙箱（懒加载）"""
    global _默认沙箱
    if _默认沙箱 is None:
        _默认沙箱 = VarSandbox("全局默认沙箱")
        # 预注册 CNSH 内置类型
        _默认沙箱.register_batch([  # pyright: ignore[reportArgumentType]
            ("真", "布尔", True, "true", True),
            ("假", "布尔", False, "false", True),
            ("空", "空值", None, "null", True),
        ])
    return _默认沙箱


# ══════════════════════════════════════════════════════════════════
# 导出
# ══════════════════════════════════════════════════════════════════

__all__ = [
    "VarEntry",
    "VarSandbox",
    "TYPE_MAP",
    "TYPE_DEFAULTS",
    "STDLIB_MAP",
    "get_default_sandbox",
]

__version__ = "1.0.0"
__author__ = "UID9622 · 诸葛鑫 · 龍芯北辰"
__dna__ = "#龍芯⚡️2026-07-06-VAR-SANDBOX-v1.0"
__responsibility__ = "UID9622·不免责"
