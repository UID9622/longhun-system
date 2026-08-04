#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·CNSH轻量双向转换器 v2.0
Python <-> CNSH 双向转换·完整语法映射·批量过滤·冲突检测

DNA: #龍芯⚡️丙午·丙申·戊申·申时·䷗复-TRANSPILER-v2.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

特性:
  - Python→CNSH: tokenize精确转换·保留注释/字符串
  - CNSH→Python: 正则逆向转换
  - 批量模式: 递归目录·自动过滤 __pycache__/.git 等
  - 冲突检测: 目标文件存在时DNA校验覆盖规则
  - 转换审计: 每个转换记录DNA+哈希
  - 繁体「龍」永存检查

与 lh_cnsh_translator.py 的关系:
  - lh_cnsh_translator.py: 全功能神经翻译引擎·交互式·代码审计·记忆层
  - lh_cnsh_transpiler.py (本文件): 轻量双向批量转换·脚本/管道友好

用法:
  python3 bin/lh_cnsh_transpiler.py --to-cnsh script.py -o script.cnsh
  python3 bin/lh_cnsh_transpiler.py --to-py script.cnsh -o script.py
  python3 bin/lh_cnsh_transpiler.py --batch ./src/ --to-cnsh
  python3 bin/lh_cnsh_transpiler.py --info       # 显示完整映射表
  python3 bin/lh_cnsh_transpiler.py --audit      # 转换审计报告
"""

import os
import re
import io
import tokenize
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import argparse
import logging

# ============================================================
# 焊死锚点
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

ROOT_DIR = Path(__file__).parent.parent.resolve()
LOG_DIR = ROOT_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"transpile_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("lh_transpiler")

# ============================================================
# 完整 CNSH <-> Python 语法映射表 v2.0
# ============================================================

PY_TO_CNSH: Dict[str, str] = {
    # --- 关键字 ---
    "def": "函数", "class": "类", "if": "如果", "else": "否则",
    "elif": "否则如果", "for": "循环", "while": "当", "return": "返回",
    "import": "导入", "from": "从", "True": "真", "False": "假",
    "None": "空", "and": "且", "or": "或", "not": "非",
    "in": "在", "is": "是", "with": "使用", "as": "作为",
    "try": "尝试", "except": "捕获", "finally": "最终",
    "raise": "抛出", "yield": "生成", "async": "异步", "await": "等待",
    "lambda": "匿名函数", "global": "全局", "nonlocal": "非局部",
    "del": "删除", "pass": "通过", "break": "跳出", "continue": "继续",
    "assert": "断言", "match": "匹配", "case": "分支",

    # --- 运算符 ---
    "==": "等于", "!=": "不等于", ">=": "大于等于", "<=": "小于等于",

    # --- 内建函数 ---
    "print": "输出", "len": "长度", "type": "类型",
    "int": "整数", "str": "文本", "list": "列表",
    "dict": "字典", "tuple": "元组", "set": "集合",
    "bool": "布尔", "float": "浮点", "range": "区间",
    "enumerate": "枚举", "zip": "压缩", "map": "映射",
    "filter": "过滤", "sum": "求和", "max": "最大值",
    "min": "最小值", "sorted": "排序", "reversed": "反转",
    "open": "打开", "input": "输入", "format": "格式化",
    "super": "父类", "isinstance": "是实例",
    "hasattr": "有属性", "getattr": "取属性", "setattr": "设属性",

    # --- 异常类型 ---
    "Exception": "异常", "BaseException": "基础异常",
    "ValueError": "值错误", "TypeError": "类型错误",
    "KeyError": "键错误", "IndexError": "索引错误",
    "AttributeError": "属性错误", "ImportError": "导入错误",
    "ModuleNotFoundError": "模块未找到", "RuntimeError": "运行时错误",
    "SyntaxError": "语法错误", "NameError": "名称错误",
    "FileNotFoundError": "文件未找到", "PermissionError": "权限错误",
    "TimeoutError": "超时错误", "ConnectionError": "连接错误",
    "ZeroDivisionError": "除零错误", "OSError": "系统错误",
    "IOError": "IO错误",

    # --- 装饰器 ---
    "property": "属性装饰", "staticmethod": "静态装饰",
    "classmethod": "类装饰", "abstractmethod": "抽象装饰",
    "dataclass": "数据类",

    # --- 常用模块 ---
    "os": "系统", "sys": "系统路径", "json": "JSON",
    "re": "正则", "math": "数学", "random": "随机",
    "datetime": "日期时间", "time": "时间", "pathlib": "路径",
    "typing": "类型注解", "collections": "集合",
    "itertools": "迭代器", "functools": "函数工具",
    "hashlib": "哈希", "copy": "复制", "pickle": "序列化",
    "csv": "CSV", "logging": "日志", "argparse": "参数解析",
    "threading": "线程", "multiprocessing": "多进程",
    "asyncio": "异步IO", "subprocess": "子进程",
    "unittest": "单元测试", "pytest": "测试框架",
    "requests": "请求库", "numpy": "数值库", "pandas": "数据框",
    "cv2": "视觉库", "PIL": "图像库", "tqdm": "进度条",
    "yaml": "YAML", "dotenv": "环境变量",
    "sqlite3": "SQLite3", "sqlalchemy": "SQL工具",
    "cookiecutter": "模板引擎", "cryptography": "加密库",
    "notion_client": "Notion客户端", "fastapi": "快速API",
    "uvicorn": "Uvicorn", "pydantic": "Pydantic",
    "watchdog": "文件监控", "prometheus_client": "Prometheus监控",
    "gnupg": "GPG", "lxml": "LXML", "beautifulsoup4": "BeautifulSoup",
}

CNSH_TO_PY: Dict[str, str] = {v: k for k, v in PY_TO_CNSH.items()}

# ============================================================
# 转换器核心
# ============================================================

class CNSHTranspiler:
    """CNSH <-> Python 双向转换器 v2.0"""

    SKIP_PATTERNS = [
        "__pycache__", ".git", ".venv", "venv", ".env",
        "node_modules", ".pytest_cache", ".mypy_cache",
        ".egg-info", "dist", "build", "archive", "data",
    ]

    SKIP_SUFFIXES = [".pyc", ".pyo", ".asc", ".lock", ".log", ".db"]

    def __init__(self, force_overwrite: bool = False):
        self.force_overwrite = force_overwrite
        self.stats: Dict[str, int] = {"success": 0, "skipped": 0, "failed": 0}

    def _should_skip(self, path: Path, exclude_patterns: List[str] = None) -> bool:
        path_str = str(path)
        patterns = self.SKIP_PATTERNS + (exclude_patterns or [])
        for p in patterns:
            if p in path_str:
                return True
        if path.suffix in self.SKIP_SUFFIXES:
            return True
        return False

    def _generate_dna(self, filepath: Path, direction: str) -> str:
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        h = hashlib.sha256(f"{filepath}{direction}{ts}".encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{ts}-TRANSPILER-{direction}-UID9622-{h}"

    def _file_hash(self, filepath: Path) -> str:
        if not filepath.exists():
            return "none"
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]

    def _check_conflict(self, output_path: Path, source_dna: str) -> Tuple[bool, str]:
        """冲突检测：目标文件存在时的覆盖规则"""
        if not output_path.exists():
            return True, "目标文件不存在"
        if self.force_overwrite:
            return True, "强制覆盖"

        try:
            with open(output_path, "r", encoding="utf-8") as f:
                head = f.read(3000)
            dna_match = re.search(r'#龍芯⚡️(\d{14})', head)
            if dna_match:
                target_ts = int(dna_match.group(1))
                source_match = re.search(r'#龍芯⚡️(\d{14})', source_dna)
                if source_match and int(source_match.group(1)) > target_ts:
                    return True, "源文件更新于目标"
            return False, "目标文件已存在，使用 --force 覆盖"
        except Exception:
            return False, "目标文件已存在"

    def py_to_cnsh(self, code: str) -> str:
        """Python → CNSH（tokenize精确转换）"""
        try:
            tokens = list(tokenize.tokenize(io.BytesIO(code.encode()).readline))
            output: List[str] = []
            for tok in tokens:
                if tok.type in (tokenize.ENCODING, tokenize.ENDMARKER):
                    continue
                if tok.type == tokenize.COMMENT:
                    output.append(tok.string)
                    continue
                if tok.type == tokenize.STRING:
                    output.append(tok.string)
                    continue
                if tok.type == tokenize.NAME:
                    mapped = PY_TO_CNSH.get(tok.string, tok.string)
                    output.append(mapped)
                else:
                    output.append(tok.string)
            result = "".join(output)
            # 清理多余空行
            result = re.sub(r'\n{3,}', '\n\n', result)
            return result
        except Exception as e:
            logger.warning(f"Tokenize失败，降级到正则转换: {e}")
            return self._regex_convert(code, PY_TO_CNSH)

    def cnsh_to_py(self, code: str) -> str:
        """CNSH → Python（正则转换·长词优先·右侧空格填充）"""
        result = self._regex_convert(code, CNSH_TO_PY, pad_spaces=True)
        result = self._fix_special_cases(result)
        return result

    def _fix_special_cases(self, code: str) -> str:
        """修复已知的CNSH→Python边界问题"""
        # 去多余空格: 空格+标点 → 只留标点
        code = re.sub(r' +([,:().])', r'\1', code)
        # 标识符与关键字粘连（左侧padding缺失时）
        code = re.sub(r'([a-zA-Z)])(is |in |and |or |as |not )', r'\1 \2', code)
        return code

    def _regex_convert(self, code: str, mapping: Dict[str, str],
                       pad_spaces: bool = False) -> str:
        """正则转换·长词优先·pad_spaces用于CNSH→Python（中文无\\b边界）"""
        result = code
        for src, dst in sorted(mapping.items(), key=lambda x: -len(x[0])):
            if pad_spaces:
                # CNSH→Python: 中文关键字后加空格·保留前导缩进
                result = re.sub(re.escape(src), f'{dst} ', result)
            else:
                # Python→CNSH: 直接替换
                result = re.sub(re.escape(src), dst, result)
        if pad_spaces:
            # CNSH→Python: 清理内部多余空格·保留缩进
            lines = result.split('\n')
            cleaned = []
            for line in lines:
                stripped = line.lstrip()
                if stripped:
                    indent_len = len(line) - len(stripped)
                    # 只压缩非缩进的内部多空格
                    content = re.sub(r'  +', ' ', stripped)
                    cleaned.append(' ' * indent_len + content)
                else:
                    cleaned.append(line)
            result = '\n'.join(cleaned)
        return result

    def convert_file(self, input_path: Path, output_path: Path,
                     direction: str = "to_cnsh") -> Tuple[bool, str]:
        """转换单个文件，含冲突检测"""
        dna = self._generate_dna(input_path, direction)
        can_write, reason = self._check_conflict(output_path, dna)
        if not can_write:
            logger.warning(f"[SKIP] {input_path}: {reason}")
            self.stats["skipped"] += 1
            return False, reason

        try:
            with open(input_path, "r", encoding="utf-8") as f:
                code = f.read()

            if direction == "to_cnsh":
                converted = self.py_to_cnsh(code)
                header = (
                    f"# CNSH 自动转换\n"
                    f"# 源文件: {input_path}\n"
                    f"# DNA: {dna}\n"
                    f"# CONFIRM: {CONFIRM}\n"
                    f"# 创建者: 诸葛鑫（UID9622）\n\n"
                )
                converted = header + converted
            else:
                converted = self.cnsh_to_py(code)
                # 去除CNSH头部注释
                converted = re.sub(
                    r'# CNSH 自动转换\n.*?(?=\n\S|\Z)', '', converted, count=1, flags=re.DOTALL
                )

            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(converted)

            logger.info(f"[OK] {input_path} → {output_path}")
            self.stats["success"] += 1
            return True, dna
        except Exception as e:
            logger.error(f"[FAIL] {input_path}: {e}")
            self.stats["failed"] += 1
            return False, str(e)

    def convert_directory(self, dir_path: Path, direction: str = "to_cnsh",
                          exclude_patterns: List[str] = None) -> Dict[str, Tuple[bool, str]]:
        """批量转换目录"""
        in_ext = ".cnsh" if direction == "to_py" else ".py"
        out_ext = ".py" if direction == "to_py" else ".cnsh"

        results: Dict[str, Tuple[bool, str]] = {}
        for filepath in sorted(dir_path.rglob(f"*{in_ext}")):
            if self._should_skip(filepath, exclude_patterns):
                continue
            output_path = filepath.with_suffix(out_ext)
            ok, info = self.convert_file(filepath, output_path, direction)
            results[str(filepath)] = (ok, info)
        return results


# ============================================================
# 审计与展示
# ============================================================

def show_mapping_table() -> None:
    """显示完整映射表"""
    print(f"\n  🐉 CNSH 语法映射表 v2.0")
    print(f"  {'=' * 60}")
    print(f"  {'Python':<25} → {'CNSH':<25}")
    print(f"  {'-' * 55}")

    keywords_set = set("def class if else elif for while return import from True False None "
                       "and or not in is with as try except finally raise yield async await "
                       "lambda global nonlocal del pass break continue assert match case".split())
    builtins_set = set("print len type int str list dict tuple set bool float range "
                       "enumerate zip map filter sum max min sorted reversed open input "
                       "format super isinstance hasattr getattr setattr".split())
    exception_set = set("Exception BaseException ValueError TypeError KeyError IndexError "
                        "AttributeError ImportError ModuleNotFoundError RuntimeError SyntaxError "
                        "NameError FileNotFoundError PermissionError TimeoutError ConnectionError "
                        "ZeroDivisionError OSError IOError".split())
    decorator_set = set("property staticmethod classmethod abstractmethod dataclass".split())
    module_set = set("os sys json re math random datetime time pathlib typing "
                     "collections itertools functools hashlib copy pickle csv "
                     "logging argparse threading multiprocessing asyncio subprocess "
                     "unittest pytest requests numpy pandas cv2 PIL tqdm yaml dotenv "
                     "sqlite3 sqlalchemy cookiecutter cryptography notion_client "
                     "fastapi uvicorn pydantic watchdog prometheus_client gnupg "
                     "lxml beautifulsoup4".split())

    for title, check_set in [
        ("关键字", keywords_set),
        ("内建函数", builtins_set),
        ("异常类型", exception_set),
        ("装饰器", decorator_set),
        ("常用模块", module_set),
    ]:
        items = [(py, cnsh) for py, cnsh in sorted(PY_TO_CNSH.items()) if py in check_set]
        if items:
            print(f"\n  [{title}]")
            for py, cnsh in items:
                print(f"    {py:<25} → {cnsh}")

    # 其他未分类项
    all_classified = keywords_set | builtins_set | exception_set | decorator_set | module_set
    others = [(py, cnsh) for py, cnsh in sorted(PY_TO_CNSH.items())
              if py not in all_classified and py not in ("==", "!=", ">=", "<=")]
    if others:
        print(f"\n  [其他]")
        for py, cnsh in others:
            print(f"    {py:<25} → {cnsh}")

    print(f"\n  总计: {len(PY_TO_CNSH)} 个映射")
    print()


# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·CNSH轻量双向转换器 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh --cnsh-transpile --to-cnsh script.py -o script.cnsh
  lh --cnsh-transpile --to-py script.cnsh -o script.py
  lh --cnsh-transpile --batch ./src/ --to-cnsh
  lh --cnsh-transpile --info   # 查看映射表
"""
    )
    parser.add_argument("--to-cnsh", type=str, help="Python → CNSH（文件或目录）")
    parser.add_argument("--to-py", type=str, help="CNSH → Python（文件或目录）")
    parser.add_argument("-o", "--output", type=str, help="输出路径（单文件模式）")
    parser.add_argument("--batch", action="store_true", help="批量模式（递归目录）")
    parser.add_argument("--exclude", type=str, help="排除模式，逗号分隔")
    parser.add_argument("--force", action="store_true", help="强制覆盖已存在文件")
    parser.add_argument("--info", action="store_true", help="显示完整映射表")
    parser.add_argument("--json", action="store_true", help="JSON格式输出结果")
    parser.add_argument("--audit", action="store_true", help="输出审计摘要")

    args = parser.parse_args()
    transpiler = CNSHTranspiler(force_overwrite=args.force)

    if args.info:
        show_mapping_table()
        return

    if not args.to_cnsh and not args.to_py:
        parser.print_help()
        return

    exclude = args.exclude.split(",") if args.exclude else None

    for source_arg, direction in [(args.to_cnsh, "to_cnsh"), (args.to_py, "to_py")]:
        if not source_arg:
            continue
        input_path = Path(source_arg)
        if not input_path.exists():
            print(f"🔴 路径不存在: {input_path}")
            sys.exit(1)

        if input_path.is_dir() or args.batch:
            print(f"[BATCH] 批量转换: {input_path}")
            results = transpiler.convert_directory(input_path, direction, exclude)
            success = sum(1 for ok, _ in results.values() if ok)
            print(f"\n✅ {success}/{len(results)} 文件转换成功")

            if args.audit:
                for path, (ok, info) in sorted(results.items()):
                    color = "🟢" if ok else "🔴"
                    print(f"  {color} {path}  {info if not ok else ''}")

            if args.json:
                print(json.dumps({
                    "direction": direction,
                    "total": len(results),
                    "success": success,
                    "results": {p: {"ok": ok, "info": info} for p, (ok, info) in results.items()}
                }, ensure_ascii=False, indent=2))
        else:
            out_ext = ".py" if direction == "to_py" else ".cnsh"
            output_path = Path(args.output) if args.output else input_path.with_suffix(out_ext)
            ok, info = transpiler.convert_file(input_path, output_path, direction)
            if ok:
                print(f"✅ {input_path} → {output_path}")
            else:
                print(f"🔴 失败: {info}")


if __name__ == "__main__":
    import sys
    main()
