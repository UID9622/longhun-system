#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LH_DELIVERY_PRECHECK-5D637CE6
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
龍魂 · 交付前四查 (delivery precheck) v1.0
==========================================
记错本 DELIVER-001~004 的自动化落地（算力节能）：
  ① 签名配对   → 每个源文件必须有 .asc（防 DELIVER-004 漏签）
  ② 0 字节文件 → 空写入排查（防 DELIVER-001 静默空写）
  ③ 临时残留   → . 开头但非 .asc/.gitignore 的临时文件（如 .issue-body.md）
  ④ 孤儿签名   → .asc 存在但源文件缺失（签名签了空文件）

用法:
  python3 bin/lh_delivery_precheck.py <目录> [--strict]
  --strict: 0 字节文件与临时残留也按失败计数（默认仅提示）

退出码:
  0 = 全绿 🟢  |  1 = 有失败项 🔴  |  2 = 用法错误
"""
import os
import sys

SOURCE_EXTS = (".md", ".py", ".sh", ".json", ".jsonl", ".yml", ".yaml", ".html", ".js", ".css")
# 允许存在的隐藏文件（正常项）
ALLOWED_HIDDEN = {".gitignore", ".git", ".github", ".asc"}
# 明显的临时文件特征
TEMP_MARKERS = ("issue-body", "tmp", "temp", "~", ".bak")


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python3 bin/lh_delivery_precheck.py <目录> [--strict]")
        return 2
    root = os.path.abspath(sys.argv[1])
    strict = "--strict" in sys.argv
    if not os.path.isdir(root):
        print(f"🔴 目录不存在: {root}")
        return 1

    problems = []   # (级别, 消息)
    source_count = 0
    signed_count = 0
    zero_bytes = []
    temp_leftovers = []
    bad_asc = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", "__pycache__")]
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            # 空文件检查
            try:
                if os.path.getsize(full) == 0:
                    zero_bytes.append(rel)
                    continue
            except OSError:
                continue
            if fn.endswith(".asc"):
                src = full[:-4]
                if not os.path.exists(src):
                    bad_asc.append(f"{rel}（源文件不存在）")
                continue
            # 隐藏文件/临时文件检查
            if fn.startswith(".") and fn not in ALLOWED_HIDDEN:
                temp_leftovers.append(rel)
                continue
            if any(m in fn for m in TEMP_MARKERS) and fn.endswith((".jsonl", ".json", ".md", ".txt")):
                temp_leftovers.append(rel)
                continue
            # 签名配对检查
            if fn.endswith(SOURCE_EXTS):
                source_count += 1
                if os.path.exists(full + ".asc"):
                    signed_count += 1
                else:
                    problems.append(("🔴", f"缺签名: {rel}"))

    # 输出结果
    print(f"=== 交付前四查 · {root} ===")
    print(f"源文件: {source_count} | 已签名: {signed_count} | 未签名: {source_count - signed_count}")

    for lvl, msg in problems:
        print(f"{lvl} {msg}")

    if zero_bytes:
        lvl = "🔴" if strict else "🟡"
        for rel in zero_bytes:
            print(f"{lvl} 0 字节文件: {rel}")
        problems.append((lvl, f"{len(zero_bytes)} 个 0 字节文件"))
    else:
        print("🟢 无 0 字节文件")

    if temp_leftovers:
        lvl = "🔴" if strict else "🟡"
        for rel in temp_leftovers:
            print(f"{lvl} 临时残留: {rel}")
        problems.append((lvl, f"{len(temp_leftovers)} 个临时残留"))
    else:
        print("🟢 无临时残留")

    if bad_asc:
        for rel in bad_asc:
            print(f"🔴 孤儿签名: {rel}")
        problems.append(("🔴", f"{len(bad_asc)} 个孤儿签名"))

    if source_count and signed_count == source_count:
        print("🟢 签名全配对")

    fail = [p for p in problems if p[0] == "🔴"]
    if fail:
        print(f"\n🔴 未通过：{len(fail)} 项 → 修复后再交付")
        return 1
    if problems:
        print("\n🟡 有提示项（--strict 则视为失败）")
        return 1 if strict else 0
    print("\n🟢 全绿，可以交付")
    return 0


if __name__ == "__main__":
    sys.exit(main())
