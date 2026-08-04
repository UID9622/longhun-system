#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 代码审查引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-CODE-REVIEW-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能:
  - 圈复杂度检测
  - 注释率统计
  - 命名规范检查（PEP8风格）
  - 重复代码检测
  - 文件头DNA检查

用法:
  lh 代码审查 bin/lh_*.py
  lh 代码审查 --dir bin/
  lh 代码审查 --report            # 生成审查报告
  lh 代码审查 --dna-check         # 只检查DNA文件头
"""

import ast
import re
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

PROJECT_ROOT = Path.home() / "longhun-system"
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# 评分阈值
THRESHOLD_COMPLEXITY_MAX = 15       # 单函数圈复杂度黄线
THRESHOLD_COMMENT_RATE_MIN = 0.05   # 注释率底线
THRESHOLD_DOCSTRING_RATE_MIN = 0.3  # 函数文档字符串覆盖率


def _parse_file_safe(file_path: Path) -> Optional[ast.AST]:
    try:
        return ast.parse(file_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def check_complexity(file_path: Path) -> Dict:
    """检查函数圈复杂度"""
    tree = _parse_file_safe(file_path)
    if not tree:
        return {"functions": 0, "total_complexity": 0, "avg": 0, "max": 0, "complex_funcs": []}

    funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    results = []
    for func in funcs:
        complexity = 1  # 基础复杂度
        for node in ast.walk(func):
            if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        results.append({"name": func.name, "line": func.lineno, "complexity": complexity})

    total = sum(r["complexity"] for r in results)
    return {
        "functions": len(results),
        "total_complexity": total,
        "avg": round(total / max(1, len(results)), 1),
        "max": max((r["complexity"] for r in results), default=0),
        "complex_funcs": [r for r in results if r["complexity"] > THRESHOLD_COMPLEXITY_MAX],
    }


def check_documentation(file_path: Path) -> Dict:
    """检查注释率与文档字符串"""
    content = file_path.read_text(encoding="utf-8")
    lines = content.split('\n')
    total_lines = len(lines)
    blank_lines = sum(1 for l in lines if not l.strip())
    code_lines = total_lines - blank_lines

    comment_lines = len(re.findall(r'^\s*#.*$', content, re.MULTILINE))
    # 文档字符串（粗略）+ 多行
    docstring_count = len(re.findall(r'"""[\s\S]*?"""', content)) + len(re.findall(r"'''[\s\S]*?'''", content))

    comment_rate = round(comment_lines / max(1, code_lines), 3)

    # 函数文档字符串覆盖率
    tree = _parse_file_safe(file_path)
    func_total = 0
    func_documented = 0
    if tree:
        funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        func_total = len(funcs)
        func_documented = sum(1 for f in funcs if ast.get_docstring(f))

    docstring_coverage = round(func_documented / max(1, func_total), 2)

    return {
        "total_lines": total_lines,
        "code_lines": code_lines,
        "comment_lines": comment_lines,
        "comment_rate": comment_rate,
        "docstrings": docstring_count,
        "func_total": func_total,
        "func_documented": func_documented,
        "docstring_coverage": docstring_coverage,
    }


def check_naming(file_path: Path) -> Dict:
    """检查命名规范"""
    content = file_path.read_text(encoding="utf-8")
    class_names = re.findall(r'class\s+(\w+)', content)
    func_names = re.findall(r'def\s+(\w+)', content)
    var_names = re.findall(r'^\s*([a-z_]\w*)\s*=', content, re.MULTILINE)

    bad_class = [n for n in class_names if not re.match(r'^[A-Z][a-zA-Z0-9]*$', n)]
    bad_func = [n for n in func_names if not re.match(r'^[a-z_][a-z0-9_]*$', n) and not n.startswith('_')]

    return {
        "classes": len(class_names),
        "functions": len(func_names),
        "bad_class_names": bad_class[:10],
        "bad_func_names": bad_func[:10],
        "naming_ok": len(bad_class) == 0 and len(bad_func) == 0,
    }


def check_dna_header(file_path: Path) -> Dict:
    """检查文件头DNA"""
    content = file_path.read_text(encoding="utf-8")
    has_dna = "DNA:" in content[:500] or "#龍芯" in content[:500]
    has_creator = "UID9622" in content[:500] or "诸葛鑫" in content[:500]
    has_license = "CC BY-NC-SA" in content[:500] or "协议:" in content[:500]
    return {
        "has_dna": has_dna,
        "has_creator": has_creator,
        "has_license": has_license,
        "header_ok": has_dna and has_creator and has_license,
    }


def check_duplicates(files: List[Path]) -> Dict:
    """检测重复代码（简化：函数签名哈希）"""
    sig_map = {}
    for fp in files:
        tree = _parse_file_safe(fp)
        if not tree:
            continue
        funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        for func in funcs:
            sig = hashlib.md5(ast.dump(func).encode()).hexdigest()[:12]
            if sig not in sig_map:
                sig_map[sig] = []
            sig_map[sig].append({"file": str(fp), "func": func.name, "line": func.lineno})

    dupes = {sig: locs for sig, locs in sig_map.items() if len(locs) > 1}
    return {"total_funcs": sum(len(v) for v in sig_map.values()), "duplicate_groups": len(dupes), "details": dupes}


def review_file(file_path: Path) -> Dict:
    """审查单个文件"""
    return {
        "file": str(file_path),
        "size_kb": round(file_path.stat().st_size / 1024, 1),
        "complexity": check_complexity(file_path),
        "documentation": check_documentation(file_path),
        "naming": check_naming(file_path),
        "dna_header": check_dna_header(file_path),
    }


def compute_score(review: Dict) -> int:
    """计算文件评分 0-100"""
    score = 100
    c = review.get("complexity", {})
    d = review.get("documentation", {})
    n = review.get("naming", {})
    h = review.get("dna_header", {})

    # 复杂度扣分
    if c.get("max", 0) > THRESHOLD_COMPLEXITY_MAX:
        score -= min((c["max"] - THRESHOLD_COMPLEXITY_MAX) * 2, 20)

    # 注释率扣分
    if d.get("comment_rate", 0) < THRESHOLD_COMMENT_RATE_MIN:
        score -= 10

    # 文档字符串扣分
    if d.get("docstring_coverage", 0) < THRESHOLD_DOCSTRING_RATE_MIN:
        score -= 10

    # 命名扣分
    if not n.get("naming_ok", True):
        score -= 10

    # 文件头扣分
    if not h.get("header_ok", False):
        score -= 15

    return max(0, min(100, score))


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·代码审查引擎")
    parser.add_argument("path", nargs="*", help="文件或glob模式")
    parser.add_argument("--dir", help="目录")
    parser.add_argument("--report", action="store_true", help="生成审查报告")
    parser.add_argument("--dna-check", action="store_true", help="只检查DNA文件头")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    files = []
    if args.dir:
        files.extend(sorted(Path(args.dir).glob("*.py")))
    elif args.path:
        for p in args.path:
            pp = Path(p)
            if pp.is_file():
                files.append(pp)
            elif pp.is_dir():
                files.extend(sorted(pp.glob("*.py")))
            elif '*' in p or '?' in p:
                files.extend(sorted(Path.cwd().glob(p)))
    else:
        files = sorted(Path.cwd().glob("lh_*.py"))

    if not files:
        print("❌ 未找到 .py 文件")
        return

    # 审查
    results = []
    for f in files:
        r = review_file(f)
        r["score"] = compute_score(r)
        results.append(r)

    # 重复检测（多个文件时）
    dupes = {}
    if len(files) > 1:
        dupes = check_duplicates(files)

    if args.dna_check:
        print("\n🔍 DNA文件头检查\n" + "-" * 50)
        for r in results:
            h = r["dna_header"]
            s = "✅" if h["header_ok"] else "❌"
            missing = []
            if not h["has_dna"]: missing.append("DNA")
            if not h["has_creator"]: missing.append("创建者")
            if not h["has_license"]: missing.append("协议")
            detail = f" (缺: {','.join(missing)})" if missing else ""
            print(f"  {s} {Path(r['file']).name}{detail}")
        print("-" * 50)
        ok = sum(1 for r in results if r["dna_header"]["header_ok"])
        print(f"  通过: {ok}/{len(results)}")
        return

    if args.json:
        output = {"files": results, "duplicates": dupes, "timestamp": datetime.now().isoformat()}
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    # 终端输出
    print("\n🐉 代码审查报告")
    print("=" * 65)
    for r in results:
        name = Path(r["file"]).name
        score = r["score"]
        grade = "🟢" if score >= 85 else ("🟡" if score >= 60 else "🔴")
        c = r["complexity"]
        d = r["documentation"]
        print(f"\n  {grade} {name} (评分: {score}/100)  {r['size_kb']}KB")
        print(f"    复杂度: 函数{c['functions']} avg{c['avg']} max{c['max']}")
        bad = c.get("complex_funcs", [])
        if bad:
            for bf in bad[:3]:
                print(f"      ⚠️ {bf['name']}(L{bf['line']}) 复杂度={bf['complexity']}")
        print(f"    文档: 代码{d['code_lines']}行 注释率{d['comment_rate']} 函数文档{d['docstring_coverage']}")
        if d["comment_rate"] < THRESHOLD_COMMENT_RATE_MIN:
            print(f"      ⚠️ 注释率过低")

    if dupes.get("duplicate_groups", 0) > 0:
        print(f"\n  🔁 重复函数组: {dupes['duplicate_groups']}")
        for sig, locs in list(dupes.get("details", {}).items())[:5]:
            names = [f"{l['file'].split('/')[-1]}:{l['func']}" for l in locs]
            print(f"    → {', '.join(names)}")

    avg_score = int(sum(r["score"] for r in results) / max(1, len(results)))
    print(f"\n{'=' * 65}")
    print(f"  平均评分: {avg_score}/100 | 文件: {len(results)}")
    print(f"{'=' * 65}")

    # 生成HTML报告
    if args.report:
        report_path = REPORTS_DIR / "code_review_report.json"
        with open(report_path, 'w') as f:
            json.dump({"files": results, "duplicates": dupes, "timestamp": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
        print(f"✅ 审查报告: {report_path}")


if __name__ == "__main__":
    main()
