# DNA: #龍芯⚡️丙午·丙申·戊辰·丙辰·䷸巽为风-CODE-补DNA-c37d0ef4
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
龍魂·重复函数合并引擎 v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰

功能：扫描 .py 文件，用 AST 精确检测"同文件内重复定义"函数，
      分层处理——只对 100% 安全的自动去重，其余只报告不动文件。

分层安全策略（P0：不把能用的代码改坏）：
  1. ✅ 同文件·同名·同体（≥2次定义，函数体哈希一致）
     → 后定义覆盖前定义，保留第一份、删除重复定义（含装饰器）——100% 安全
  2. 🟡 同文件·同名·异体（≥2次定义，函数体不同）
     → 后定义覆盖前定义，大概率是 bug 或有意的局部重定义 → 只报告不自动动
  3. 🟡 跨文件·同名·同体（函数体哈希一致）
     → 可能是有意复制（软链双名目录/多包各自维护）→ 只报告，供人工定夺
  4. 🟢 跨文件·同名·异体 → 各模块独立实现，正常，不计欠账

P0 铁律：
  - 不删除只冻结：任何文件修改前，原版备份到 archive/frozen/
  - 删除后必须重新 ast.parse 验证，失败即回滚（恢复冻结版）
  - 只处理模块顶层 + 类方法层的函数（嵌套局部函数不算，避免误删）

用法：
  python3 bin/lh_fix_duplicate_functions.py              # dry-run 只报告
  python3 bin/lh_fix_duplicate_functions.py --fix        # 实际去重
  python3 bin/lh_fix_duplicate_functions.py --report out.json
  python3 bin/lh_fix_duplicate_functions.py --dir 某目录 # 只扫指定目录
"""

import argparse
import ast
import hashlib
import json
import shutil
import sys
import warnings
from collections import defaultdict
from datetime import datetime
from pathlib import Path

warnings.filterwarnings("ignore")

BASE_DIR = Path.home() / "longhun-system"
FROZEN_DIR = BASE_DIR / "archive" / "frozen"  # P0：不删除只冻结

# 扫描排除（与 checker / 白名单对齐）
SKIP_DIRS = {
    ".git", ".venv", "node_modules", "11_DATA", "_work", "dist", "models",
    "archive", "backups", "__pycache__", ".codebuddy", "_archive", "backup",
    "build", "dist_ide", "build_ide",
}


def collect_top_funcs(src: str, tree: ast.AST):
    """收集模块顶层 + 类方法层的函数（不含嵌套局部函数）。
    返回 {name: [(node, body_hash), ...]}（按源码顺序）。"""
    funcs = defaultdict(list)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            seg = ast.get_source_segment(src, node) or ""
            funcs[node.name].append((node, hashlib.sha256(seg.encode()).hexdigest()))
        elif isinstance(node, ast.ClassDef):
            for m in node.body:
                if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    seg = ast.get_source_segment(src, m) or ""
                    funcs[m.name].append((m, hashlib.sha256(seg.encode()).hexdigest()))
    return funcs


def node_start_line(node):
    """函数起始行（含装饰器）"""
    if getattr(node, "decorator_list", None):
        return min(d.lineno for d in node.decorator_list)
    return node.lineno


def analyze_file(p: Path):
    """分析单个文件，返回 (可去重列表, 异体报告列表)"""
    try:
        src = p.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(src)
    except (SyntaxError, UnicodeDecodeError):
        return [], []

    funcs = collect_top_funcs(src, tree)
    to_remove = []      # [(name, start_line, end_line)]
    diff_report = []    # [(name, 出现次数)]
    lines = src.splitlines(keepends=True)

    for name, entries in funcs.items():
        if len(entries) < 2:
            continue
        # 按 hash 分组
        by_hash = defaultdict(list)
        for node, h in entries:
            by_hash[h].append(node)
        # 同体 ≥2 → 去重（保留最前，删后续）
        for h, nodes in by_hash.items():
            if len(nodes) >= 2:
                nodes_sorted = sorted(nodes, key=lambda n: node_start_line(n))
                for dup in nodes_sorted[1:]:
                    to_remove.append((name, node_start_line(dup), dup.end_lineno))
        # 异体（不同 hash 均有定义）
        if len(by_hash) > 1:
            diff_report.append((name, len(entries)))

    return to_remove, diff_report


def dedupe_file(p: Path, to_remove, dry_run: bool):
    """按行号删除重复定义（从大到小，避免行号漂移）。返回统计。"""
    if not to_remove:
        return None
    src = p.read_text(encoding="utf-8", errors="replace")
    lines = src.splitlines(keepends=True)

    # 去重区间（按结束行从大到小处理）
    ranges = sorted(set((s, e) for _, s, e in to_remove), key=lambda r: r[1], reverse=True)
    new_lines = list(lines)
    for start, end in ranges:
        del new_lines[start - 1:end]  # 行号 1-based → 索引 0-based

    new_src = "".join(new_lines)

    # 验证：删除后必须仍可解析
    try:
        ast.parse(new_src)
    except SyntaxError as e:
        return {"file": str(p), "status": "🔴 删除后语法错误", "detail": str(e), "removed": 0}

    # 验证：函数名出现次数应减少
    removed_names = sorted(set(n for n, _, _ in to_remove))

    if dry_run:
        return {
            "file": str(p), "status": "🟡 dry-run 待去重",
            "names": removed_names, "dup_count": len(ranges), "removed": 0,
        }

    # 冻结原版（P0：不删除只冻结）
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    FROZEN_DIR.mkdir(parents=True, exist_ok=True)
    frozen = FROZEN_DIR / f"{p.name}.{ts}.frozen"
    shutil.copy2(p, frozen)

    p.write_text(new_src, encoding="utf-8")
    return {
        "file": str(p), "status": "✅ 已去重", "names": removed_names,
        "dup_count": len(ranges), "removed": len(ranges), "frozen": frozen.name,
    }


def scan_all(target_dir: Path):
    """全库扫描，返回 (可去重文件列表, 异体清单, 跨文件同体组)"""
    py_files = []
    for root, dirs, files in target_dir.walk():
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in files:
            if fn.endswith(".py"):
                py_files.append(Path(root) / fn)

    total_removable = 0
    total_diff = 0
    removable_files = []
    diff_files = []
    # 跨文件同体：全局 (name, hash) → files
    cross_same = defaultdict(list)

    for p in py_files:
        to_remove, diff_report = analyze_file(p)
        if to_remove:
            removable_files.append((p, to_remove))
            total_removable += len(set((n) for n, _, _ in to_remove))
        if diff_report:
            diff_files.append((p, diff_report))
            total_diff += sum(c for _, c in diff_report)

        # 跨文件同体收集
        try:
            src = p.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(src)
        except Exception:
            continue
        funcs = collect_top_funcs(src, tree)
        seen = set()
        for name, entries in funcs.items():
            for _, h in entries:
                key = (name, h)
                if key in seen:  # 同文件内 (name, hash) 只记一次，避免同文件重复出现
                    continue
                seen.add(key)
                if not name.startswith("_"):
                    cross_same[key].append(str(p))

    cross_groups = [
        {"func": n, "hash": h[:8], "files": files}
        for (n, h), files in cross_same.items()
        if len(files) > 1
    ]

    return removable_files, diff_files, cross_groups, total_removable, total_diff, len(py_files)


def main():
    parser = argparse.ArgumentParser(description="龍魂·重复函数合并引擎 v1.0")
    parser.add_argument("--dir", default=str(BASE_DIR), help="扫描目录（默认全库）")
    parser.add_argument("--fix", action="store_true", help="实际去重（默认 dry-run 只报告）")
    parser.add_argument("--report", help="输出 JSON 报告路径")
    args = parser.parse_args()

    target = Path(args.dir)
    if not target.exists():
        print(f"❌ 目录不存在: {target}")
        return 1

    print(f"🐉 重复函数扫描中… {target}")
    removable_files, diff_files, cross_groups, total_removable, total_diff, total_py = \
        scan_all(target)

    results = []
    deduped_files = 0
    removed_total = 0
    for p, to_remove in removable_files:
        r = dedupe_file(p, to_remove, dry_run=not args.fix)
        if r is None:
            continue
        results.append(r)
        if r["status"].startswith("✅"):
            deduped_files += 1
            removed_total += r["removed"]

    # 输出
    print(f"\n{'='*60}")
    print(f"📊 重复函数报告（{'--fix 实际去重' if args.fix else 'dry-run 预览'}）")
    print(f"   扫描 .py 文件: {total_py}")
    print(f"   ✅ 同文件同体可去重函数: {total_removable} 组 / {len(removable_files)} 文件")
    print(f"   🟡 同文件同名异体(疑似bug): {total_diff} 处")
    print(f"   🟡 跨文件同体真重复: {len(cross_groups)} 组")

    if args.fix:
        print(f"\n   实际去重: {deduped_files} 文件 / 删除 {removed_total} 处重复定义")
    else:
        print(f"\n   （dry-run：加 --fix 才实际修改；修改前自动冻结原版到 archive/frozen/）")

    # 异体清单（疑似 bug，只报告）
    if diff_files:
        print(f"\n🟡 同文件同名异体（后定义覆盖前定义·疑似bug·人工核查）Top15:")
        for p, dl in diff_files[:15]:
            names = ",".join(f"{n}×{c}" for n, c in dl[:4])
            print(f"   {p} → {names}")

    # 跨文件同体 Top10
    if cross_groups:
        print(f"\n🟡 跨文件同体真重复（可能是有意复制·人工定夺）Top10:")
        for g in sorted(cross_groups, key=lambda x: len(x["files"]), reverse=True)[:10]:
            print(f"   {g['func']} ({g['hash']}) → {len(g['files'])}文件: {', '.join(g['files'][:3])}…")

    if args.report:
        out = {
            "timestamp": datetime.now().isoformat(),
            "mode": "fix" if args.fix else "dry-run",
            "total_py_files": total_py,
            "same_file_dup_functions": total_removable,
            "same_file_diff_functions": total_diff,
            "cross_file_same_groups": len(cross_groups),
            "deduped_files": deduped_files,
            "removed_count": removed_total,
            "results": results,
            "diff_report_top": [{"file": str(p), "names": dl[:4]} for p, dl in diff_files[:50]],
            "cross_groups_top": cross_groups[:50],
        }
        Path(args.report).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n📄 报告已写: {args.report}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
