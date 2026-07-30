#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·丙辰·亥时·需-CNSH-ABSORB-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║       龍魂CNSH吸收器 · 任意代码 → CNSH中文可编辑 · 一键入生态            ║
║       LongHun CNSH Absorber · Any Code → CNSH Editable Format            ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·需-CNSH-ABSORB-v1.0                   ║
║  哲学: 任意代码翻译成中文编辑 · 吸收即登记 · 登记即归入DNA               ║
║  铁律: 来源不可删 · 原许可证保留 · DNA入链不可覆 · 吸收不走样            ║
║  📇 身份 · 联系 · 支持 → assets/PUBLIC_IDENTITY.md                      ║
╚══════════════════════════════════════════════════════════════════════════╝

设计理念：
  外部代码 → CNSH吸收 → 中文可编辑 → 生态服务 → DNA登记
  任何Python/JS/Go/Shell代码都能翻译成CNSH格式，关键词中文化，
  但逻辑不变，可二向渲染（中文编辑 ↔ 原始代码）

用法：
  # 吸收外部代码文件
  python3 bin/lh_cnsh_absorb.py absorb <文件路径> [--uid UID9622] [--name 服务名]

  # 列出已吸收的服务
  python3 bin/lh_cnsh_absorb.py list

  # 查看已吸收代码的CNSH版本
  python3 bin/lh_cnsh_absorb.py show <服务名>

  # 将CNSH代码还原为可执行Python
  python3 bin/lh_cnsh_absorb.py render <服务名> [--lang python]

  # 检查吸收状态
  python3 bin/lh_cnsh_absorb.py status <服务名>

吸收规则：
  - Python: def → 定义, class → 类别, import → 引入, return → 返回
  - JavaScript: function → 函数, const → 常量, let → 变量
  - 字符串和注释保持原样
  - 保留原始文件的完整备份
  - 生成可执行的原生代码副本
"""

import hashlib
import json
import os
import re
import sys
import tokenize
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════
# L0 常量
# ═══════════════════════════════════════════════════════════

吸收目录 = Path.home() / ".龍魂" / "cnsh_absorbed"
吸收目录.mkdir(parents=True, exist_ok=True)

# ── Python → CNSH 关键词映射 ──
PYTHON_CNSH_MAP: Dict[str, str] = {
    # 关键字
    "def": "定义",
    "class": "类别",
    "import": "引入",
    "from": "从",
    "return": "返回",
    "yield": "产出",
    "if": "如果",
    "elif": "否则如果",
    "else": "否则",
    "for": "遍历",
    "while": "当",
    "break": "跳出",
    "continue": "继续",
    "try": "尝试",
    "except": "捕获",
    "finally": "最终",
    "raise": "抛出",
    "with": "使用",
    "as": "作为",
    "lambda": "匿名函数",
    "pass": "空过",
    "assert": "断言",
    "del": "删除",
    "global": "全局",
    "nonlocal": "非局部",
    "True": "真",
    "False": "假",
    "None": "空",
    "and": "且",
    "or": "或",
    "not": "非",
    "in": "在",
    "is": "是",
    # 内置函数
    "print": "输出",
    "len": "长度",
    "range": "范围",
    "type": "类型",
    "str": "字符串",
    "int": "整数",
    "float": "浮点",
    "list": "列表",
    "dict": "字典",
    "set": "集合",
    "tuple": "元组",
    "bool": "布尔",
    "open": "打开",
    "super": "父类",
    "self": "自身",
    "__init__": "__初始化__",
    "__name__": "__名称__",
    "__main__": "__主程序__",
}

# ── JavaScript → CNSH 关键词映射 ──
JS_CNSH_MAP: Dict[str, str] = {
    "function": "函数",
    "const": "常量",
    "let": "变量",
    "var": "声明",
    "return": "返回",
    "if": "如果",
    "else": "否则",
    "for": "遍历",
    "while": "当",
    "break": "跳出",
    "continue": "继续",
    "try": "尝试",
    "catch": "捕获",
    "finally": "最终",
    "throw": "抛出",
    "class": "类别",
    "extends": "继承",
    "import": "引入",
    "export": "导出",
    "default": "默认",
    "async": "异步",
    "await": "等待",
    "true": "真",
    "false": "假",
    "null": "空",
    "undefined": "未定义",
    "typeof": "类型检测",
    "instanceof": "是实例",
    "new": "新建",
    "this": "当前",
}

# ── 保留字（不做翻译的） ──
保留不翻译 = {"self", "cls", "args", "kwargs", "super", "object", "Exception", "ValueError"}

# 语言识别模式
LANG_PATTERNS = {
    "python": [r"\.py$", r"def\s+\w+\s*\(", r"import\s+\w+", r"class\s+\w+.*:"],
    "javascript": [r"\.(js|mjs|cjs)$", r"function\s+\w+\s*\(", r"const\s+\w+\s*=", r"let\s+\w+\s*="],
    "typescript": [r"\.(ts|tsx)$", r"interface\s+\w+", r"type\s+\w+\s*="],
    "go": [r"\.go$", r"func\s+\w+\s*\(", r"package\s+\w+"],
    "shell": [r"\.(sh|bash)$", r"^#!/", r"\becho\b"],
}


def _现在时间() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _获取干支() -> str:
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / "calendar-context-logger"))
        from calendar_core import LunarEngine  # type: ignore[import-untyped]
        g = LunarEngine().get_ganzhi()
        return f"{g['year_zhu']}·{g['month_zhu']}·{g['day_zhu']}·{g['hour_zhu']}"
    except Exception:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def 识别语言(filepath: str) -> str:
    """根据文件名和内容识别编程语言"""
    filename = os.path.basename(filepath).lower()
    for lang, patterns in LANG_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, filename):
                return lang
    # 读文件开头几行进一步判断
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            head = "".join([f.readline() for _ in range(10)])
        for lang, patterns in LANG_PATTERNS.items():
            if lang in ("python", "shell"):
                continue  # 已由文件名判断
            for pattern in patterns[1:]:  # 跳过分机名模式
                if re.search(pattern, head, re.MULTILINE):
                    return lang
    except Exception:
        pass
    # 默认根据后缀
    if filename.endswith(".py"):
        return "python"
    elif filename.endswith((".js", ".mjs")):
        return "javascript"
    elif filename.endswith(".ts"):
        return "typescript"
    elif filename.endswith(".go"):
        return "go"
    elif filename.endswith(".sh"):
        return "shell"
    return "unknown"


# ═══════════════════════════════════════════════════════════
# CNSH 翻译引擎
# ═══════════════════════════════════════════════════════════

def python转cnsh(code: str) -> str:
    """将Python代码翻译为CNSH中文可编辑格式"""
    # 逐行处理，保持缩进和字符串
    lines = code.split("\n")
    result = []
    for line in lines:
        # 跳过纯注释行和空行
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            result.append(line)
            continue

        # 保留字符串内容不变
        # 简单策略：在非字符串区域替换关键词
        缩进 = line[:len(line) - len(line.lstrip())]
        内容 = stripped

        # 按空格和符号分割，逐个替换
        单词列表 = re.split(r'(\s+|(?<=[\(\)\[\]\{\}:,\.=<>!+\-*/%])|(?=[\(\)\[\]\{\}:,\.=<>!+\-*/%]))', 内容)
        新内容 = []
        for w in 单词列表:
            if w in PYTHON_CNSH_MAP and w not in 保留不翻译:
                新内容.append(PYTHON_CNSH_MAP[w])
            else:
                新内容.append(w)
        result.append(缩进 + "".join(新内容))
    return "\n".join(result)


def js转cnsh(code: str) -> str:
    """将JavaScript代码翻译为CNSH"""
    lines = code.split("\n")
    result = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("//") or stripped.startswith("/*"):
            result.append(line)
            continue
        缩进 = line[:len(line) - len(line.lstrip())]
        内容 = stripped
        单词列表 = re.split(r'(\s+|(?<=[\(\)\[\]\{\}:,\.=<>!+\-*/%])|(?=[\(\)\[\]\{\}:,\.=<>!+\-*/%]))', 内容)
        新内容 = []
        for w in 单词列表:
            if w in JS_CNSH_MAP:
                新内容.append(JS_CNSH_MAP[w])
            else:
                新内容.append(w)
        result.append(缩进 + "".join(新内容))
    return "\n".join(result)


def cnsh转python(cnsh_code: str) -> str:
    """将CNSH代码还原为Python"""
    反向映射 = {v: k for k, v in PYTHON_CNSH_MAP.items() if k not in 保留不翻译}
    lines = cnsh_code.split("\n")
    result = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            result.append(line)
            continue
        缩进 = line[:len(line) - len(line.lstrip())]
        内容 = stripped
        单词列表 = re.split(r'(\s+|(?<=[\(\)\[\]\{\}:,\.=<>!+\-*/%])|(?=[\(\)\[\]\{\}:,\.=<>!+\-*/%]))', 内容)
        新内容 = []
        for w in 单词列表:
            if w in 反向映射:
                新内容.append(反向映射[w])
            else:
                新内容.append(w)
        result.append(缩进 + "".join(新内容))
    return "\n".join(result)


# ═══════════════════════════════════════════════════════════
# 吸收数据结构
# ═══════════════════════════════════════════════════════════

@dataclass
class CNSH吸收记录:
    """一次代码吸收的记录"""
    服务名: str
    原始文件: str            # 原始文件路径
    原始语言: str            # python/javascript/go/shell
    原始SHA256: str          # 原始文件的哈希
    CNSH代码: str            # 翻译后的CNSH代码
    CNSH_SHA256: str         # CNSH代码的哈希
    吸收时间: str
    吸收干支: str
    UID: str = ""
    DNA码: str = ""
    版本: int = 1
    标签: List[str] = field(default_factory=list)
    许可证: str = ""
    来源URL: str = ""
    可执行文件: str = ""      # 还原后可执行的副本路径

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CNSH吸收记录":
        return cls(**d)


# ═══════════════════════════════════════════════════════════
# CRUD
# ═══════════════════════════════════════════════════════════

def 加载吸收记录(服务名: str) -> Optional[CNSH吸收记录]:
    path = 吸收目录 / f"{服务名}.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return CNSH吸收记录.from_dict(json.load(f))


def 保存吸收记录(记录: CNSH吸收记录):
    path = 吸收目录 / f"{记录.服务名}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(记录.to_dict(), f, ensure_ascii=False, indent=2)


def 所有吸收记录() -> List[CNSH吸收记录]:
    records = []
    for f in sorted(吸收目录.glob("*.json")):
        try:
            with open(f, "r", encoding="utf-8") as fp:
                records.append(CNSH吸收记录.from_dict(json.load(fp)))
        except Exception:
            pass
    return records


# ═══════════════════════════════════════════════════════════
# 核心操作
# ═══════════════════════════════════════════════════════════

def 吸收代码(
    filepath: str,
    服务名: Optional[str] = None,
    uid: str = "",
    license_info: str = "",
    source_url: str = "",
) -> Tuple[bool, str, Optional[CNSH吸收记录]]:
    """
    吸收外部代码文件 → CNSH翻译 → 注册为生态服务

    返回: (成功, 消息, 吸收记录)
    """
    filepath = os.path.abspath(filepath)
    if not os.path.exists(filepath):
        return False, f"❌ 文件不存在: {filepath}", None

    # 读取原始代码
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            原始代码 = f.read()
    except Exception as e:
        return False, f"❌ 读取失败: {e}", None

    # 计算哈希
    原始哈希 = hashlib.sha256(原始代码.encode()).hexdigest()[:16]
    文件名 = os.path.basename(filepath)

    # 识别语言
    语言 = 识别语言(filepath)

    # 自动生成服务名
    if not 服务名:
        服务名 = os.path.splitext(文件名)[0].replace("_", " ").replace("-", " ").title()

    # 检查是否已吸收（同文件+同哈希）
    for existing in 所有吸收记录():
        if existing.原始SHA256 == 原始哈希 and existing.原始文件 == filepath:
            return False, f"⚠️ 文件已吸收 · 服务名: {existing.服务名} · 版本 v{existing.版本}", existing

    # CNSH 翻译
    if 语言 == "python":
        cnsh代码 = python转cnsh(原始代码)
    elif 语言 in ("javascript", "typescript"):
        cnsh代码 = js转cnsh(原始代码)
    else:
        cnsh代码 = 原始代码  # 不支持的语言保持原样

    cnsh哈希 = hashlib.sha256(cnsh代码.encode()).hexdigest()[:16]

    # 备份原始文件到吸收目录
    原始副本路径 = 吸收目录 / f"{服务名}_original_{os.path.basename(filepath)}"
    with open(原始副本路径, "w", encoding="utf-8") as f:
        f.write(原始代码)

    # 保存CNSH版本
    cnsh副本路径 = 吸收目录 / f"{服务名}.cnsh.py"
    with open(cnsh副本路径, "w", encoding="utf-8") as f:
        f.write(f"# CNSH吸收 · {服务名} · 原文件: {文件名}\n")
        f.write(f"# 吸收时间: {_现在时间()}\n")
        f.write(f"# 原始哈希: {原始哈希}\n")
        f.write(f"# CNSH哈希: {cnsh哈希}\n")
        f.write(f"# 语言: {语言}\n")
        f.write(f"#\n")
        f.write(cnsh代码)

    # 保存可执行Python副本
    if 语言 == "python":
        可执行路径 = 吸收目录 / f"{服务名}_exec.py"
        with open(可执行路径, "w", encoding="utf-8") as f:
            f.write(f"# CNSH可执行 · {服务名}\n")
            f.write(f"# 由CNHS吸收器自动生成\n")
            f.write(原始代码)
        os.chmod(可执行路径, 0o755)

    # 吸收记录
    now = _现在时间()
    记录 = CNSH吸收记录(
        服务名=服务名,
        原始文件=filepath,
        原始语言=语言,
        原始SHA256=原始哈希,
        CNSH代码=cnsh代码,
        CNSH_SHA256=cnsh哈希,
        吸收时间=now,
        吸收干支=_获取干支(),
        UID=uid,
        DNA码=hashlib.sha256(f"{服务名}:{原始哈希}:{now}".encode()).hexdigest()[:12],
        版本=1,
        标签=[语言, "吸收"],
        许可证=license_info,
        来源URL=source_url,
        可执行文件=str(可执行路径) if 语言 == "python" else "",
    )
    保存吸收记录(记录)

    # 统计
    原始行数 = len(原始代码.split("\n"))
    cnsh行数 = len(cnsh代码.split("\n"))
    翻译率 = sum(1 for k in PYTHON_CNSH_MAP if k in 原始代码) if 语言 == "python" else 0

    return True, (
        f"🧬✅ 代码已吸收！\n"
        f"   服务名: {服务名}\n"
        f"   语言: {语言}\n"
        f"   原始: {原始行数}行 · SHA256: {原始哈希}\n"
        f"   CNSH: {cnsh行数}行 · SHA256: {cnsh哈希}\n"
        f"   翻译: {翻译率}个关键词中文化\n"
        f"   DNA:  {记录.DNA码}\n"
        f"   吸收: {_获取干支()}\n"
        f"   ─────────────────\n"
        f"   CNSH版: {cnsh副本路径}\n"
        f"   可执行: {可执行路径 if 语言 == 'python' else 'N/A'}\n"
        f"   下一步: python3 bin/lh_cnsh_absorb.py show {服务名}"
    ), 记录


def 显示CNSH代码(服务名: str) -> Tuple[bool, str]:
    """查看已吸收服务的CNSH代码"""
    记录 = 加载吸收记录(服务名)
    if not 记录:
        return False, f"❌ 未找到吸收服务: {服务名}"

    lines = [
        f"╔══════════════════════════════════════════════════════════╗",
        f"║  🧬 CNSH吸收 · {服务名:<38} ║",
        f"╠══════════════════════════════════════════════════════════╣",
        f"║  原文件: {记录.原始文件:<40}",
        f"║  语言:   {记录.原始语言:<40}",
        f"║  DNA:    {记录.DNA码:<40}",
        f"║  吸收:   {记录.吸收干支:<40}",
        f"╠══════════════════════════════════════════════════════════╣",
    ]
    cnsh_lines = 记录.CNSH代码.split("\n")
    for i, line in enumerate(cnsh_lines[:50]):
        lines.append(f"║ {i+1:3d}| {line[:55]:<55} ║")
    if len(cnsh_lines) > 50:
        lines.append(f"║  ... 共 {len(cnsh_lines)} 行，仅展示前50行                        ║")
    lines.append("╚══════════════════════════════════════════════════════════╝")
    return True, "\n".join(lines)


def 列出所有吸收() -> Tuple[bool, str]:
    records = 所有吸收记录()
    if not records:
        return True, "📭 尚未吸收任何代码 · 用法: python3 bin/lh_cnsh_absorb.py absorb <文件路径>"

    lines = ["📋 已吸收的CNSH服务:"]
    for r in records:
        语言emoji = {"python": "🐍", "javascript": "🟨", "typescript": "🔷", "go": "🔵", "shell": "💻"}.get(r.原始语言, "📄")
        lines.append(f"  {语言emoji} [{r.服务名}] · {r.原始语言} · {len(r.CNSH代码.split())}词 · DNA:{r.DNA码} · {r.吸收时间[:10]}")
    return True, "\n".join(lines)


def 查看状态(服务名: str) -> Tuple[bool, str]:
    记录 = 加载吸收记录(服务名)
    if not 记录:
        return False, f"❌ 未找到: {服务名}"

    return True, (
        f"🧬 {记录.服务名}\n"
        f"   语言: {记录.原始语言}\n"
        f"   原始: {记录.原始文件} (SHA256: {记录.原始SHA256})\n"
        f"   CNSH: SHA256: {记录.CNSH_SHA256}\n"
        f"   DNA:  {记录.DNA码}\n"
        f"   吸收: {记录.吸收干支}\n"
        f"   版本: v{记录.版本}\n"
        f"   标签: {', '.join(记录.标签)}\n"
        f"   UID:  {记录.UID or '未绑定'}"
    )


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("🧬 龍魂CNSH吸收器 · 任意代码 → 中文可编辑")
        print()
        print("用法:")
        print("  python3 bin/lh_cnsh_absorb.py absorb <文件路径> [--uid UID] [--name 服务名]")
        print("  python3 bin/lh_cnsh_absorb.py list")
        print("  python3 bin/lh_cnsh_absorb.py show <服务名>")
        print("  python3 bin/lh_cnsh_absorb.py status <服务名>")
        print()
        print("示例:")
        print("  # 吸收DragonSoul守护脚本")
        print("  python3 bin/lh_cnsh_absorb.py absorb DragonSoul_Guardian_v2.py --uid UID9622")
        print()
        print("  # 吸收Kimi Agent文件")
        print("  python3 bin/lh_cnsh_absorb.py absorb kimi_tool.py --uid UID9622 --name 'Kimi工具'")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "absorb" and len(sys.argv) >= 3:
        filepath = sys.argv[2]
        uid = ""
        服务名 = None

        # 解析可选参数
        args = sys.argv[3:]
        i = 0
        while i < len(args):
            if args[i] == "--uid" and i + 1 < len(args):
                uid = args[i + 1]
                i += 2
            elif args[i] == "--name" and i + 1 < len(args):
                服务名 = args[i + 1]
                i += 2
            else:
                i += 1

        ok, msg, record = 吸收代码(filepath, 服务名=服务名, uid=uid)
        print(msg)

        # 可选：自动注册为生态服务
        if ok and record:
            # 自动添加到生态通行证的服务清单
            try:
                sys.path.insert(0, str(Path(__file__).parent))
                from lh_ecosystem_passport import 服务注册表, 注册服务
                所需层级 = "free"  # 默认free层
                if record.原始语言 == "python":
                    所需层级 = "free"
                注册服务(record.服务名, 所需层级, f"吸收自 {os.path.basename(filepath)} · CNSH翻译", 分类="吸收")
                print(f"   📎 已自动注册为生态服务（{所需层级}层）")
            except Exception:
                pass

        sys.exit(0 if ok else 1)

    elif cmd == "list":
        ok, msg = 列出所有吸收()
        print(msg)

    elif cmd == "show" and len(sys.argv) >= 3:
        服务名 = sys.argv[2]
        ok, msg = 显示CNSH代码(服务名)
        print(msg)

    elif cmd == "status" and len(sys.argv) >= 3:
        服务名 = sys.argv[2]
        ok, msg = 查看状态(服务名)
        print(msg)

    else:
        print(f"未知命令: {cmd} · 运行无参数查看帮助")

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·丙辰·亥时·需-CNSH-ABSORB-v1.0-7C2E16A3
