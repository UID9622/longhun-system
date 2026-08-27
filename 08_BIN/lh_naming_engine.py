#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
🐉 龍魂生态 · 统一命名引擎 v1.2
# 层级: L2_工具层
# DNA: #龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-NAMING-ENGINE-525329b4
# 别名DNA: #龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-NAMING-ALIAS-1c857e60
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 版本: v1.2
# 状态: 🟢 生效
# 修改需: 创始人
# 协议: 01_protocols/LH-NAMING-STANDARD-v1.1.md
# 用法: lh naming check / fix / convert / dashboard / alias

命令:
  lh naming             → 看板（总览）
  lh naming check       → 扫描违规命名（--json 结构化 / --dir 指定目录）
  lh naming fix         → 修复（--dry-run 预演 / --yes 跳过确认 / --dir 指定目录）
  lh naming convert     → .cnsh ↔ .md 映射（--dir 指定目录 / --to-md / --to-cnsh / --force）
  lh naming dashboard   → 命名看板
  lh naming alias       → 别名映射环境（v1.2）· 老文件物理不动·环境变量识别
     alias                       → 别名看板
     alias register              → 注册映射 --old 老名 --canonical 规范名 [--layer Lx] [--note]
     alias unregister            → 注销映射 --old 老名
     alias resolve               → 解析 --name 名字 [--dir]（老名↔规范名双向）
     alias scan                  → 扫描未注册老文件 --dir [--dry-run] 生成建议
     alias import                → 批量导入 --file x.json [--yes]（合并进注册表）
"""

import argparse
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

# ============================================================
# 焊死锚点
# ============================================================
DNA = "#龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-NAMING-ENGINE-525329b4"
ALIAS_DNA = "#龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-NAMING-ALIAS-1c857e60"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
ROOT_NAME = "龍魂系统"
ROOT_NAME_EN = "longhun-system"
PROTOCOL_PATH = "01_protocols/LH-NAMING-STANDARD-v1.1.md"
REGISTRY_PATH = "01_protocols/P0_根目录注册表.md"
ALIAS_REGISTRY_PATH = "config/naming_alias_registry.json"   # 默认别名注册表
ALIAS_ENV = "LH_NAMING_ALIAS_FILE"                          # 环境变量·自定义别名文件

# 层级映射表（显式配置，非启发式猜测）· 与 P0_根目录注册表 同源
LAYER_MAP = [
    ("protocol", "L0"), ("constitution", "L0"), ("宪法", "L0"), ("协议", "L0"),
    ("engine", "L1"), ("引擎", "L1"), ("生成器", "L1"),
    ("tool", "L2"), ("工具", "L2"),
    ("app", "L3"), ("应用", "L3"),
    ("data", "L4"), ("数据", "L4"), ("config", "L4"), ("配置", "L4"),
]

# 协议文件规范: NN_主体_☯UID9622·DNA_SUFFIX.ext（新增）
# 存量 LH-* 老规范兼容（已被索引/引用链焊死）
PROTOCOL_RE = re.compile(r"^[0-9]{2}_.*_☯UID9622.*\.(md|cnsh)$")
LEGACY_RE = re.compile(r"^LH-.+\.(md|cnsh)$")
# 代码文件规范: L[0-4]_功能.py
CODE_RE = re.compile(r"^L[0-4]_.*\.py$")
# 生态标识头
HEADER_MARK = "🐉 龍魂生态"

# 头部模板
def header_for(path: str, layer: str) -> str:
    name = Path(path).name
    return (
        f"# {HEADER_MARK} · {name}\n"
        f"# 层级: {layer}\n"
        f"# DNA: #龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-{name.replace('.', '_')[:24]}-UID9622\n"
        f"# 确认码: {CONFIRM_CODE}\n"
        f"# GPG: {GPG_KEY}\n"
        f"# 版本: v1.0\n"
        f"# 状态: 🟡 自动注入\n"
        f"# 修改需: 创始人\n"
    )


def detect_layer(filename: str) -> str:
    """显式映射表判断层级；未匹配返回 ''（交由交互确认）"""
    low = filename.lower()
    for keyword, layer in LAYER_MAP:
        if keyword.lower() in low:
            return layer
    return ""


def ensure_dir(path: Path) -> None:
    if not path.exists() or not path.is_dir():
        print(f"🔴 断言失败: 目录不存在: {path}")
        sys.exit(1)


# ============================================================
# 别名映射环境（v1.2）· 老文件物理不动·环境变量识别
# ============================================================
def alias_registry_file() -> Path:
    """别名注册表路径：环境变量 LH_NAMING_ALIAS_FILE 优先，默认 config/"""
    env = os.environ.get(ALIAS_ENV, "").strip()
    if env:
        p = Path(env).expanduser()
        if not p.exists():
            print(f"🟡 环境变量 {ALIAS_ENV} 指向的文件不存在: {p} → 回退默认")
        else:
            return p.resolve()
    return Path(ALIAS_REGISTRY_PATH).resolve()


def load_alias_registry(path: Path | None = None) -> dict:
    """加载别名注册表（容错：文件缺失/损坏返回空 aliases）"""
    p = path or alias_registry_file()
    empty = {"meta": {"dna": ALIAS_DNA, "version": "v1.2"}, "aliases": {}}
    if not p.exists():
        return empty
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("aliases"), dict):
            return data
        return empty
    except Exception:
        print(f"🔴 别名注册表解析失败: {p}")
        return empty


def save_alias_registry(data: dict, path: Path | None = None) -> Path:
    """保存别名注册表，返回实际写入路径"""
    p = path or alias_registry_file()
    p.parent.mkdir(parents=True, exist_ok=True)
    data.setdefault("meta", {})
    data["meta"].update({
        "dna": ALIAS_DNA,
        "version": "v1.2",
        "updated": datetime.now().isoformat(timespec="seconds"),
    })
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return p


def resolve_alias(name: str, aliases: dict) -> dict | None:
    """双向解析：老名→规范名 / 规范名→老名。返回 {'old','canonical','layer','status','note'} 或 None"""
    name = Path(name).name
    for old, meta in aliases.items():
        if old == name:
            return {"old": old, **meta}
    for old, meta in aliases.items():
        if meta.get("canonical") and Path(meta["canonical"]).name == name:
            return {"old": old, **meta}
    return None


# ============================================================
# 子命令: check — 扫描违规命名
# ============================================================
def cmd_check(args) -> int:
    root = Path(args.dir).resolve()
    ensure_dir(root)
    violations = []
    aliases = load_alias_registry()["aliases"]
    alias_hits = 0

    # 1. 协议文件
    proto_dir = root / "01_protocols"
    if proto_dir.exists():
        for f in sorted(proto_dir.glob("*")):
            if not f.is_file() or f.name.endswith(".asc"):
                continue
            if f.suffix not in (".md", ".cnsh"):
                continue
            # 兼容存量 LH-* 老规范（已被索引/引用链焊死）；新规范约束新增
            if PROTOCOL_RE.match(f.name) or re.match(r"^LH-.+\.(md|cnsh)$", f.name):
                continue
            # 别名映射环境：已注册别名=合规（老文件物理不动·环境变量识别）
            if f.name in aliases:
                alias_hits += 1
                continue
            violations.append({
                "type": "协议文件", "path": str(f),
                "issue": "不符合新规范 [NN]_主体_☯UID9622·DNA.ext（存量 LH-* 兼容·可 lh naming alias register 别名识别）", "severity": "🟡",
            })

    # 2. 代码文件（bin/ 08_BIN/）
    for code_dir_name in ("bin", "08_BIN"):
        code_dir = root / code_dir_name
        if not code_dir.exists():
            continue
        for f in sorted(code_dir.glob("*.py")):
            if f.name.startswith("lh_naming_"):
                continue
            if not CODE_RE.match(f.name):
                if f.name in aliases:
                    alias_hits += 1
                    continue
                violations.append({
                    "type": "代码文件", "path": str(f),
                    "issue": "不符合 L[0-4]_功能.py（可 lh naming alias register 别名识别）", "severity": "🟡",
                })

    # 3. 生态标识头缺失
    scan_dirs = [root]
    for d in scan_dirs:
        for f in d.rglob("*"):
            if not f.is_file():
                continue
            if f.suffix not in (".py", ".md", ".cnsh"):
                continue
            if ".git" in f.parts or "node_modules" in f.parts or "dist" in f.parts:
                continue
            if f.name.endswith(".asc"):
                continue
            try:
                with f.open(encoding="utf-8", errors="replace") as fp:
                    first = fp.readline().strip()
                    # Python 脚本允许 shebang 行，标识头可在第二行
                    if f.suffix == ".py" and first.startswith("#!"):
                        first = fp.readline().strip()
            except Exception:
                continue
            if HEADER_MARK not in first:
                violations.append({
                    "type": "标识头", "path": str(f),
                    "issue": "缺少龍魂生态标识头", "severity": "🟡",
                })

    total = len(violations)
    red = sum(1 for v in violations if v["severity"] == "🔴")
    yellow = sum(1 for v in violations if v["severity"] == "🟡")

    print(f"🐉 龍魂生态 · 命名检查 · {root}")
    print("=" * 56)
    if alias_hits:
        print(f"  🟢 别名识别: {alias_hits} 个老文件已注册映射（物理不动·环境变量识别）")
    print(f"  违规总数: {total}（🔴 {red} · 🟡 {yellow}）")
    for v in violations[:60]:
        print(f"  {v['severity']} [{v['type']}] {v['path']}")
        print(f"      → {v['issue']}")
    if total > 60:
        print(f"  …（共 {total} 条，仅显示前 60）")

    if args.json:
        print(json.dumps({"total": total, "red": red, "yellow": yellow,
                          "violations": violations[:500]}, ensure_ascii=False, indent=2))

    # 审计
    _audit("naming_check", {"dir": str(root), "violations": total, "red": red})
    return 0 if red == 0 else 1


# ============================================================
# 子命令: fix — 修复（--dry-run / 备份 / 回滚）
# ============================================================
def cmd_fix(args) -> int:
    root = Path(args.dir).resolve()
    ensure_dir(root)
    dry_run = args.dry_run
    backup_dir = None

    print(f"🐉 龍魂生态 · 统一命名修复 v1.1 · {root}")
    print("=" * 56)
    if dry_run:
        print("🟡 DRY-RUN 模式：仅预览，不执行任何修改")
    else:
        print("⚠️  警告：此操作将批量重命名/注入文件头！")
        if not args.yes:
            ans = input("确认执行？输入 [龍魂9622] 继续: ").strip()
            if ans != "龍魂9622":
                print("❌ 已取消")
                return 1
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = root / f"_龍魂命名修复备份_{ts}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ 备份目录已创建: {backup_dir}")

    moved = injected = skipped = 0

    # 1. 协议文件重命名
    proto_dir = root / "01_protocols"
    if proto_dir.exists():
        print(f"\n📂 处理协议文件: {proto_dir}")
        for f in sorted(proto_dir.glob("*")):
            if not f.is_file() or f.name.endswith(".asc"):
                continue
            if f.suffix not in (".md", ".cnsh"):
                continue
            if PROTOCOL_RE.match(f.name):
                skipped += 1
                continue
            name = re.sub(r"\.[^.]*$", "", f.name)
            # 提取 DNA 干支卦主标签（去掉前缀 #龍芯⚡️ 与后缀）
            tag = re.sub(r"^#龍芯⚡️", "", DNA).split("-")[0]
            new_name = f"99_{name}_☯UID9622·{tag}.cnsh"
            dst = f.parent / new_name
            if _safe_move(f, dst, dry_run, backup_dir):
                moved += 1

    # 2. 代码文件重命名
    for code_dir_name in ("bin", "08_BIN"):
        code_dir = root / code_dir_name
        if not code_dir.exists():
            continue
        print(f"\n📂 处理代码文件: {code_dir}")
        for f in sorted(code_dir.glob("*.py")):
            if f.name.startswith("lh_naming_"):
                continue
            if CODE_RE.match(f.name):
                skipped += 1
                continue
            layer = detect_layer(f.name)
            if not layer:
                print(f"🟡 无法自动判断层级: {f.name}")
                print("   L0=协议层 L1=引擎层 L2=工具层 L3=应用层 L4=数据层")
                try:
                    layer = input("   请手动输入层级 (L0/L1/L2/L3/L4) [回车跳过]: ").strip()
                except EOFError:
                    layer = ""
                if not layer:
                    print(f"   ⏭️  跳过: {f.name}")
                    continue
                if not re.match(r"^L[0-4]$", layer):
                    print(f"   🔴 无效层级，跳过: {f.name}")
                    continue
            dst = f.parent / f"{layer}_{f.name}"
            if _safe_move(f, dst, dry_run, backup_dir):
                moved += 1

    # 3. 生态标识头注入（仅非修复目录）
    if not dry_run:
        print(f"\n📂 检查生态标识头...")
    for f in root.rglob("*"):
        if not f.is_file():
            continue
        if f.suffix not in (".py", ".md", ".cnsh"):
            continue
        if ".git" in f.parts or "node_modules" in f.parts or "dist" in f.parts:
            continue
        if f.name.endswith(".asc"):
            continue
        if backup_dir and f.parent == backup_dir:
            continue
        try:
            first = f.open(encoding="utf-8", errors="replace").readline().strip()
        except Exception:
            continue
        if HEADER_MARK in first:
            continue
        layer = detect_layer(f.name) or "L2"
        if dry_run:
            print(f"  [DRY-RUN] 将注入头部: {f}")
        else:
            header = header_for(str(f), layer)
            tmp = f.with_suffix(f.suffix + ".tmp")
            tmp.write_text(header + f.read_text(encoding="utf-8", errors="replace"),
                           encoding="utf-8")
            tmp.replace(f)
            print(f"  ✅ 已注入头部: {f}")
        injected += 1

    print("\n" + "=" * 56)
    print(f"  重命名: {moved} · 注入头部: {injected} · 已规范跳过: {skipped}")
    if dry_run:
        print("🟡 DRY-RUN 完成，以上为预览，未执行任何修改")
        print("👉 确认无误后执行: lh naming fix")
    else:
        print(f"✅ 统一命名修复完成 · 备份位置: {backup_dir}")
        if backup_dir:
            print(f"🔄 回滚指令: cp {backup_dir}/*.bak <对应目录>/")
        print("🔍 验证指令: lh naming check")
    print("=" * 56)

    _audit("naming_fix", {"dir": str(root), "dry_run": dry_run,
                          "moved": moved, "injected": injected})
    return 0


def _safe_move(src: Path, dst: Path, dry_run: bool, backup_dir: Path | None) -> bool:
    if src == dst or dst.exists():
        if dst.exists() and src != dst:
            print(f"  🟡 目标已存在，跳过: {dst.name}")
        return False
    if dry_run:
        print(f"  [DRY-RUN] 将移动: {src.name} → {dst.name}")
        return True
    if backup_dir:
        shutil.copy2(src, backup_dir / (src.name + ".bak"))
    src.rename(dst)
    print(f"  ✅ {src.name} → {dst.name}")
    return True


# ============================================================
# 子命令: convert — .cnsh ↔ .md 映射
# ============================================================
def cmd_convert(args) -> int:
    root = Path(args.dir).resolve()
    ensure_dir(root)
    to_md = args.to_md or not args.to_cnsh
    converted = skipped = 0

    print(f"🐉 龍魂生态 · .cnsh ↔ .md 映射 · {root}")
    print("=" * 56)
    for f in sorted(root.rglob("*.cnsh")):
        if ".git" in f.parts or "dist" in f.parts:
            skipped += 1
            continue
        if to_md:
            dst = f.with_suffix(".md")
        else:
            dst = f.with_suffix(".cnsh")
        if dst.exists() and not args.force:
            skipped += 1
            continue
        if args.dry_run:
            print(f"  [DRY-RUN] 将映射: {f} → {dst}")
        else:
            dst.write_text(f.read_text(encoding="utf-8", errors="replace"),
                           encoding="utf-8")
            print(f"  ✅ {f} → {dst}")
        converted += 1

    print("=" * 56)
    print(f"  映射: {converted} · 跳过: {skipped}")
    if args.dry_run:
        print("🟡 DRY-RUN 完成，未写入任何文件")
    _audit("naming_convert", {"dir": str(root), "to_md": to_md, "converted": converted})
    return 0


# ============================================================
# 子命令: dashboard — 看板
# ============================================================
def cmd_dashboard(args) -> int:
    root = Path(args.dir).resolve()
    cnsh_total = len(list(root.rglob("*.cnsh")))
    md_total = len(list(root.rglob("*.md")))
    py_total = len(list(root.rglob("*.py")))

    proto_dir = root / "01_protocols"
    proto_total = proto_violation = 0
    if proto_dir.exists():
        for f in proto_dir.glob("*"):
            if not f.is_file() or f.name.endswith(".asc"):
                continue
            if f.suffix not in (".md", ".cnsh"):
                continue
            proto_total += 1
            if not PROTOCOL_RE.match(f.name) and not LEGACY_RE.match(f.name):
                proto_violation += 1

    root_ok = (root.name in (ROOT_NAME, ROOT_NAME_EN))
    reg_ok = (root / REGISTRY_PATH).exists()
    aliases = load_alias_registry()["aliases"]

    print("🐉 龍魂生态 · 命名看板")
    print("=" * 50)
    print(f"  生态根: {root.name} · {'✅ 合规' if root_ok else '🔴 不合规'}")
    print(f"  根目录注册表: {'✅ 已登记' if reg_ok else '🔴 未登记'} → {REGISTRY_PATH}")
    print(f"  协议文件: {proto_total} · 违规 {proto_violation}")
    print(f"  别名映射: {len(aliases)} 个老文件已注册（物理不动·环境变量识别）")
    print(f"  .cnsh 文件: {cnsh_total} | .md: {md_total} | .py: {py_total}")
    if proto_violation:
        print("\n  ⚠️ 有违规命名，运行: lh naming fix --dry-run 或 lh naming alias scan")
    print("=" * 50)

    _audit("naming_dashboard", {"root": root.name, "proto_total": proto_total,
                                "proto_violation": proto_violation})
    return 0 if root_ok and reg_ok and proto_violation == 0 else 1


# ============================================================
# 子命令: alias — 别名映射环境（v1.2）
# ============================================================
def cmd_alias(args) -> int:
    if not getattr(args, "sub", None) or args.sub == "list":
        return _alias_dashboard(args)

    data = load_alias_registry()
    aliases = data["aliases"]

    # --- register: 注册单条映射 ---
    if args.sub == "register":
        old = getattr(args, "old", "").strip()
        canonical = getattr(args, "canonical", "").strip()
        if not old or not canonical:
            print("🔴 register 需要 --old 老名 与 --canonical 规范名")
            return 1
        layer = getattr(args, "layer", "").strip() or "L2"
        if not re.match(r"^L[0-4]$", layer):
            print(f"🔴 无效层级: {layer}（应为 L0-L4）")
            return 1
        note = getattr(args, "note", "").strip()
        old_name = Path(old).name
        aliases[old_name] = {
            "canonical": canonical,
            "layer": layer,
            "status": getattr(args, "status", "legacy"),
            "note": note or "别名识别·老文件物理不动",
        }
        p = save_alias_registry(data)
        print(f"✅ 已注册别名: {old_name} → {canonical}（{layer}）")
        print(f"   写入: {p}")
        _audit("alias_register", {"old": old_name, "canonical": canonical, "layer": layer})
        return 0

    # --- unregister: 注销 ---
    if args.sub == "unregister":
        old = getattr(args, "old", "").strip()
        if not old:
            print("🔴 unregister 需要 --old 老名")
            return 1
        old_name = Path(old).name
        if old_name not in aliases:
            print(f"🟡 未注册的别名: {old_name}")
            return 1
        if not getattr(args, "yes", False):
            try:
                ans = input(f"确认注销 [{old_name}] ? 输入 [龍魂9622] 继续: ").strip()
            except EOFError:
                ans = ""
            if ans != "龍魂9622":
                print("❌ 已取消")
                return 1
        del aliases[old_name]
        p = save_alias_registry(data)
        print(f"✅ 已注销别名: {old_name}")
        print(f"   写入: {p}")
        _audit("alias_unregister", {"old": old_name})
        return 0

    # --- resolve: 双向解析 ---
    if args.sub == "resolve":
        name = getattr(args, "name", "").strip()
        if not name:
            print("🔴 resolve 需要 --name 名字")
            return 1
        hit = resolve_alias(name, aliases)
        if not hit:
            print(f"🟡 未命中别名: {name}")
            print(f"   提示: 运行 lh naming alias scan --dir . 生成建议映射")
            return 1
        root = Path(getattr(args, "dir", ".")).resolve()
        # 递归查找物理文件（老文件可能在任意子目录）
        phys_list = [p for p in root.rglob(hit["old"]) if p.is_file()]
        phys = phys_list[0] if phys_list else root / hit["old"]
        exists = phys.exists()
        print(f"🐉 别名解析 · {name}")
        print("=" * 56)
        print(f"  老文件名:  {hit['old']}")
        print(f"  规范名:    {hit['canonical']}")
        print(f"  层级:      {hit.get('layer', 'L2')} · 状态: {hit.get('status', 'legacy')}")
        print(f"  备注:      {hit.get('note', '')}")
        print(f"  物理路径:  {phys} · {'✅ 存在' if exists else '🟡 不存在'}")
        print("=" * 56)
        return 0 if exists else 1

    # --- scan: 扫描未注册老文件，生成建议映射 ---
    if args.sub == "scan":
        root = Path(getattr(args, "dir", ".")).resolve()
        ensure_dir(root)
        suggested = []
        for f in sorted(root.rglob("*")):
            if not f.is_file() or f.name.endswith(".asc"):
                continue
            if ".git" in f.parts or "node_modules" in f.parts or "dist" in f.parts:
                continue
            if f.name in aliases:
                continue
            # 协议层老规范（非 LH-* 但不符合新规范）
            if f.suffix in (".md", ".cnsh") and f.parent.name == "01_protocols":
                if PROTOCOL_RE.match(f.name) or LEGACY_RE.match(f.name):
                    continue
                suggested.append({"path": str(f), "layer": "L0",
                                  "canonical": f"99_{f.stem}_☯UID9622·丙午·丙申·辛酉·丙申·䷉履_{f.suffix[1:].upper()}.md"})
            # 代码层：bin/ 08_BIN/ 下非规范 .py
            elif f.suffix == ".py" and (f.parent.name in ("bin", "08_BIN")):
                if CODE_RE.match(f.name):
                    continue
                layer = detect_layer(f.name) or "L2"
                suggested.append({"path": str(f), "layer": layer,
                                  "canonical": f"{layer}_{f.stem}_☯UID9622·丙午·丙申·辛酉·丙申·䷉履.py"})
        if not suggested:
            print("🟢 未发现需映射的老文件（全部合规或已注册别名）")
            return 0
        print(f"🐉 别名扫描 · 建议映射 {len(suggested)} 条 · {root}")
        print("=" * 56)
        for s in suggested:
            print(f"  🟡 [{s['layer']}] {Path(s['path']).name}")
            print(f"      → {Path(s['canonical']).name}")
        print("=" * 56)
        if getattr(args, "dry_run", False):
            print("🟡 DRY-RUN：仅预览。确认后执行:")
            print("   lh naming alias scan --dir <目录> --import --yes")
        elif getattr(args, "import_", False):
            if not getattr(args, "yes", False):
                try:
                    ans = input(f"确认导入 {len(suggested)} 条映射? 输入 [龍魂9622] 继续: ").strip()
                except EOFError:
                    ans = ""
                if ans != "龍魂9622":
                    print("❌ 已取消")
                    return 1
            for s in suggested:
                old_name = Path(s["path"]).name
                aliases[old_name] = {"canonical": Path(s["canonical"]).name,
                                     "layer": s["layer"], "status": "legacy",
                                     "note": "scan批量导入·老文件物理不动"}
            p = save_alias_registry(data)
            print(f"✅ 已导入 {len(suggested)} 条映射 · 写入: {p}")
            _audit("alias_scan_import", {"imported": len(suggested), "dir": str(root)})
        return 0

    # --- import: 批量导入 JSON ---
    if args.sub == "import":
        fpath = Path(getattr(args, "file", "")).expanduser()
        if not fpath.exists():
            print(f"🔴 导入文件不存在: {fpath}")
            return 1
        try:
            ext = json.loads(fpath.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"🔴 导入文件解析失败: {e}")
            return 1
        if not isinstance(ext, dict):
            print("🔴 导入格式错误：需 JSON 对象（key=老名, value={canonical,layer,note}）")
            return 1
        added = 0
        for old, meta in ext.items():
            if not isinstance(meta, dict) or not meta.get("canonical"):
                continue
            aliases[str(old)] = {
                "canonical": str(meta["canonical"]),
                "layer": str(meta.get("layer", "L2")),
                "status": str(meta.get("status", "legacy")),
                "note": str(meta.get("note", "外部导入")),
            }
            added += 1
        p = save_alias_registry(data)
        print(f"✅ 已导入 {added} 条映射 · 写入: {p}")
        _audit("alias_import", {"file": str(fpath), "imported": added})
        return 0

    parser.print_help()
    return 1


def _alias_dashboard(args) -> int:
    data = load_alias_registry()
    aliases = data["aliases"]
    legacy = sum(1 for m in aliases.values() if m.get("status") == "legacy")
    migrated = sum(1 for m in aliases.values() if m.get("status") == "migrated")
    env = os.environ.get(ALIAS_ENV, "(默认 config/naming_alias_registry.json)")
    reg_file = alias_registry_file()

    print("🐉 龍魂生态 · 别名映射环境看板")
    print("=" * 56)
    print(f"  注册表:  {reg_file} {'✅' if reg_file.exists() else '🔴 缺失'}")
    print(f"  环境变量: {ALIAS_ENV} = {env}")
    print(f"  映射总数: {len(aliases)}（legacy {legacy} · migrated {migrated}）")
    print("=" * 56)
    for i, (old, meta) in enumerate(sorted(aliases.items()), 1):
        print(f"  {i:>2}. {old}")
        print(f"      → {meta.get('canonical', '?')}  [{meta.get('layer', 'L2')}·{meta.get('status', 'legacy')}]")
    if not aliases:
        print("  （空）运行 lh naming alias register --old ... --canonical ... 注册")
    print("=" * 56)
    print("  用法: register / unregister / resolve / scan / import")
    _audit("alias_dashboard", {"count": len(aliases), "env": env})
    return 0


# ============================================================
# 审计
# ============================================================
def _audit(action: str, detail: dict) -> None:
    try:
        audit_file = Path("audit_log.jsonl")
        entry = {
            "ts": datetime.now().isoformat(),
            "action": f"naming_{action}",
            "dna": DNA,
            "detail": detail,
        }
        with audit_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


# ============================================================
# 主入口
# ============================================================
def main() -> int:
    parser = argparse.ArgumentParser(
        prog="lh naming",
        description="🐉 龍魂生态 · 统一命名引擎 v1.1")
    sub = parser.add_subparsers(dest="cmd")

    p_check = sub.add_parser("check", help="扫描违规命名")
    p_check.add_argument("--dir", default=".", help="目标目录（默认当前）")
    p_check.add_argument("--json", action="store_true", help="JSON 输出")

    p_fix = sub.add_parser("fix", help="修复命名（--dry-run 预演）")
    p_fix.add_argument("--dir", default=".", help="目标目录（默认当前）")
    p_fix.add_argument("--dry-run", action="store_true", help="仅预览不执行")
    p_fix.add_argument("--yes", action="store_true", help="跳过交互确认")

    p_conv = sub.add_parser("convert", help=".cnsh ↔ .md 映射")
    p_conv.add_argument("--dir", default=".", help="目标目录（默认当前）")
    p_conv.add_argument("--to-md", action="store_true", help=".cnsh → .md")
    p_conv.add_argument("--to-cnsh", action="store_true", help=".md → .cnsh")
    p_conv.add_argument("--force", action="store_true", help="覆盖已存在")
    p_conv.add_argument("--dry-run", action="store_true", help="仅预览")

    p_dash = sub.add_parser("dashboard", help="命名看板")
    p_dash.add_argument("--dir", default=".", help="目标目录（默认当前）")

    p_alias = sub.add_parser("alias", help="别名映射环境（老文件物理不动·环境变量识别）")
    a_sub = p_alias.add_subparsers(dest="sub")

    a_list = a_sub.add_parser("list", help="别名看板")
    a_list.add_argument("--dir", default=".", help="目标目录（默认当前）")

    a_reg = a_sub.add_parser("register", help="注册单条映射")
    a_reg.add_argument("--old", required=True, help="老文件名")
    a_reg.add_argument("--canonical", required=True, help="规范名")
    a_reg.add_argument("--layer", default="L2", help="层级 L0-L4")
    a_reg.add_argument("--note", default="", help="备注")
    a_reg.add_argument("--status", default="legacy", help="状态 legacy/migrated")

    a_unreg = a_sub.add_parser("unregister", help="注销映射")
    a_unreg.add_argument("--old", required=True, help="老文件名")
    a_unreg.add_argument("--yes", action="store_true", help="跳过确认")

    a_res = a_sub.add_parser("resolve", help="双向解析（老名↔规范名）")
    a_res.add_argument("--name", required=True, help="老名或规范名")
    a_res.add_argument("--dir", default=".", help="物理路径基准目录")

    a_scan = a_sub.add_parser("scan", help="扫描未注册老文件，生成建议映射")
    a_scan.add_argument("--dir", default=".", help="目标目录（默认当前）")
    a_scan.add_argument("--dry-run", action="store_true", help="仅预览")
    a_scan.add_argument("--import", dest="import_", action="store_true", help="确认后导入建议")
    a_scan.add_argument("--yes", action="store_true", help="跳过确认")

    a_imp = a_sub.add_parser("import", help="批量导入 JSON 映射文件")
    a_imp.add_argument("--file", required=True, help="JSON 文件路径")
    a_imp.add_argument("--yes", action="store_true", help="跳过确认")

    args = parser.parse_args()
    if not args.cmd or args.cmd == "dashboard":
        if not args.cmd:
            args = parser.parse_args(["dashboard"] + sys.argv[1:])
        return cmd_dashboard(args)
    if args.cmd == "check":
        return cmd_check(args)
    if args.cmd == "fix":
        return cmd_fix(args)
    if args.cmd == "convert":
        return cmd_convert(args)
    if args.cmd == "alias":
        return cmd_alias(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n❌ 已取消")
        sys.exit(130)
