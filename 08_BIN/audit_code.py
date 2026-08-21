#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂代码审计节点 v1.0
DNA: #龍芯⚡️2026-08-21-AUDIT-CODE-v1.0
功能:
  静态分析 — 危险模式 / 硬编码密钟 / 不安全导入
  动态分析 — 导入测试 / 语法检查
  写入 audit_log.jsonl，关联 DNA
"""

import ast
import json
import sys
import re
import importlib
import argparse
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "08_BIN"))

AUDIT_LOG = ROOT / "audit_log.jsonl"

try:
    from lh_dna_ref_impl import generate as dna_generate
    DNA_OK = True
except ImportError:
    DNA_OK = False


# ────────────────────────────────────────────────
# 审计对象：08_BIN 下所有核心模块
# ────────────────────────────────────────────────

CORE_MODULES = [
    "lh_dna_ref_impl",
    "dna_helper",
    "voice_input_cpp",
    "vision_input",
    "audit_status",
    "audit_report",
    "audit_code",
    "audit_protocol",
    "audit_red_blue",
]

# ────────────────────────────────────────────────
# 静态分析规则
# ────────────────────────────────────────────────

# P0 熔断——必须立即驳回的危险模式
P0_PATTERNS = [
    (r"\beval\s*\(",          "P0: eval() 禁止使用"),
    (r"\bexec\s*\(",          "P0: exec() 禁止使用"),
    (r"__import__\s*\(",      "P0: __import__ 禁止使用"),
    (r"pickle\.loads",        "P0: pickle.loads 存在反序列化风险"),
    (r"os\.system\s*\(",      "P0: os.system() 建议替换为 subprocess"),
    (r"subprocess.*shell\s*=\s*True", "P0: shell=True 存在注入风险"),
    (r"\bpassword\s*=\s*['\"][^'\"]{4,}['\"]\b", "P0: 硬编码密码字段"),
    (r"\bsecret\s*=\s*['\"][^'\"]{4,}['\"]\b",   "P0: 硬编码密钟字段"),
]

# P1 警告——建议修改
P1_PATTERNS = [
    (r"print\s*\(.{80,}\)",          "P1: print 语句过长，建议使用日志"),
    (r"except\s*:\s*$",               "P1: 裸 except 找不到具体异常"),
    (r"except\s+Exception\s*:",       "P1: 过广的 Exception 捕获"),
    (r"#\s*TODO",                     "P1: TODO 未完成项"),
    (r"time\.sleep\((?:[5-9]|[1-9]\d)",  "P1: sleep 超过 5s 可能阻塞"),
]

# 信息语句——不计分只记录
INFO_PATTERNS = [
    (r"\bimport\s+(requests|urllib)",   "信息: 网络请求库，确认超时已设置"),
    (r"\bopen\s*\(.+['\"]w['\"]\)",     "信息: 文件写操作，确认路径合法"),
]


# ────────────────────────────────────────────────
# 静态分析函数
# ────────────────────────────────────────────────

def static_audit(path: Path) -> dict:
    """对单个 .py 文件做静态分析"""
    issues = []   # {level, line, msg}
    source = ""

    try:
        source = path.read_text(encoding="utf-8")
    except Exception as e:
        return {"status": "red", "p0": True,
                "issues": [{"level": "P0", "line": 0,
                            "msg": f"读取文件失败: {e}"}]}

    # 语法检查
    try:
        ast.parse(source)
    except SyntaxError as e:
        return {"status": "red", "p0": True,
                "issues": [{"level": "P0", "line": e.lineno,
                            "msg": f"语法错误: {e.msg}"}]}

    lines = source.splitlines()

    # 逐行模式匹配
    for lineno, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#"):   # 跳过纯注释行
            continue

        for pattern, msg in P0_PATTERNS:
            if re.search(pattern, line):
                issues.append({"level": "P0", "line": lineno, "msg": msg,
                               "snippet": line.strip()[:80]})

        for pattern, msg in P1_PATTERNS:
            if re.search(pattern, line):
                issues.append({"level": "P1", "line": lineno, "msg": msg,
                               "snippet": line.strip()[:80]})

        for pattern, msg in INFO_PATTERNS:
            if re.search(pattern, line):
                issues.append({"level": "INFO", "line": lineno, "msg": msg,
                               "snippet": line.strip()[:80]})

        # 行长检查
        if len(line) > 120:
            issues.append({"level": "P1", "line": lineno,
                           "msg": f"行长 {len(line)} 字符，超过 120 限制",
                           "snippet": line.strip()[:80]})

    p0_count = sum(1 for i in issues if i["level"] == "P0")
    p1_count = sum(1 for i in issues if i["level"] == "P1")

    if p0_count > 0:
        status = "red"
    elif p1_count > 0:
        status = "yellow"
    else:
        status = "green"

    return {
        "status": status,
        "p0": p0_count > 0,
        "p0_count": p0_count,
        "p1_count": p1_count,
        "total_lines": len(lines),
        "issues": issues,
    }


# ────────────────────────────────────────────────
# 动态分析（导入测试）
# ────────────────────────────────────────────────

def dynamic_audit(module_name: str) -> dict:
    """尝试导入模块并检查关键属性"""
    try:
        mod = importlib.import_module(module_name)
        # 检查关键属性
        checks = []
        if module_name == "lh_dna_ref_impl":
            checks = ["GONG_TABLE", "GUA_NAMES", "generate", "selftest"]
        elif module_name == "dna_helper":
            checks = ["make_dna", "make_dna_full", "append_with_dna"]
        elif module_name == "voice_input_cpp":
            checks = ["transcribe_file", "start_streaming"]
        elif module_name == "vision_input":
            checks = ["describe_image", "analyze_screenshot", "extract_text_from_image"]
        elif module_name in ("audit_status", "audit_report",
                             "audit_code", "audit_protocol", "audit_red_blue"):
            checks = []   # 审计工具自身不检查属性

        missing = [c for c in checks if not hasattr(mod, c)]
        if missing:
            return {"status": "yellow", "p0": False,
                    "msg": f"导入成功，但缺少属性: {missing}"}
        return {"status": "green", "p0": False,
                "msg": f"导入成功，关键属性全部存在"}
    except ImportError as e:
        # 除了外部依赖缺失，其他导入错误是 P1
        if "whisper" in str(e) or "PIL" in str(e) or "requests" in str(e) or "ollama" in str(e):
            return {"status": "yellow", "p0": False,
                    "msg": f"外部依赖未安装（可接受）: {e}"}
        return {"status": "red", "p0": False,
                "msg": f"导入失败: {e}"}
    except Exception as e:
        return {"status": "red", "p0": True,
                "msg": f"运行时异常: {e}"}


# ────────────────────────────────────────────────
# 写入日志
# ────────────────────────────────────────────────

def write_log(record: dict):
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ────────────────────────────────────────────────
# 主审计函数
# ────────────────────────────────────────────────

def run_audit(modules: list, verbose: bool = False):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print()
    print("╔" + "═" * 65 + "╗")
    print("║  🐉 代码审计节点 v1.0" + " " * 44 + "║")
    print("╠" + "═" * 65 + "╣")
    print(f"║  时间: {ts}" + " " * (57 - len(ts)) + "║")
    print("║  模块: " + ", ".join(modules)[:55] + " " * max(0, 56 - len(", ".join(modules))) + "║")
    print("╠" + "═" * 65 + "╣")
    print("║  {:<24} {:^8} {:^8} {:^8}  ║".format("模块", "静态", "动态", "综合"))
    print("╠" + "═" * 65 + "╣")

    total_p0 = 0
    total_p1 = 0
    all_green = True

    for mod_name in modules:
        py_path = ROOT / "08_BIN" / f"{mod_name}.py"

        # 静态
        if py_path.exists():
            s_result = static_audit(py_path)
        else:
            s_result = {"status": "yellow", "p0": False,
                        "p0_count": 0, "p1_count": 0,
                        "issues": [{"level": "INFO", "line": 0,
                                    "msg": "文件不存在"}]}

        # 动态
        d_result = dynamic_audit(mod_name)

        # 综合
        p0 = s_result.get("p0") or d_result.get("p0")
        if p0 or s_result["status"] == "red" or d_result["status"] == "red":
            combined = "red"
        elif s_result["status"] == "yellow" or d_result["status"] == "yellow":
            combined = "yellow"
        else:
            combined = "green"

        if combined != "green":
            all_green = False

        p0_c = s_result.get("p0_count", 0)
        p1_c = s_result.get("p1_count", 0)
        total_p0 += p0_c
        total_p1 += p1_c

        ICONS = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
        s_icon = ICONS.get(s_result["status"], "⚪")
        d_icon = ICONS.get(d_result["status"], "⚪")
        c_icon = ICONS.get(combined, "⚪")
        print("║  {:<24}  {}      {}      {}    ║".format(
            mod_name[:24], s_icon, d_icon, c_icon))

        # 生成 DNA
        dna_str = ""
        if DNA_OK:
            r = dna_generate(title=f"{mod_name}-代码审计",
                             category="audit", action="代码审计")
            dna_str = r["dna_string"]

        # 写入日志
        log_entry = {
            "timestamp": ts,
            "dimension": "code",
            "module": mod_name,
            "status": combined,
            "p0": p0,
            "p0_count": p0_c,
            "p1_count": p1_c,
            "static_status": s_result["status"],
            "dynamic_status": d_result["status"],
            "dynamic_msg": d_result.get("msg", ""),
            "issues": s_result.get("issues", []),
            "dna": dna_str,
        }
        write_log(log_entry)

        if verbose and s_result.get("issues"):
            for issue in s_result["issues"]:
                if issue["level"] in ("P0", "P1"):
                    print(f"║    L{issue['line']:>4} [{issue['level']}] {issue['msg'][:50]}")

    print("╠" + "═" * 65 + "╣")
    overall = "🟢 全部通过" if all_green else (
              "🔴 存在 P0" if total_p0 > 0 else "🟡 存在警告")
    print("║  综合结果: {:<55}║".format(overall))
    print("║  P0 数量: {:>3}  P1 数量: {:>3}" .format(
          total_p0, total_p1) + " " * 34 + "║")
    print("╚" + "═" * 65 + "╝")
    print(f"\n💾 审计日志已写入: {AUDIT_LOG}")

    if total_p0 > 0:
        print("⚠️  P0 熔断触发！请立即处理。")
        sys.exit(1)


# ────────────────────────────────────────────────
# 入口
# ────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="龍魂代码审计节点")
    parser.add_argument(
        "--module", default="all",
        help="审计目标： all | 模块名（多个用逗号分隔）"
    )
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="输出详细问题列表")
    args = parser.parse_args()

    if args.module == "all":
        targets = CORE_MODULES
    else:
        targets = [m.strip() for m in args.module.split(",")]

    run_audit(targets, verbose=args.verbose)
