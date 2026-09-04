#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·丁酉·乙酉·午时·䷾既济-CNSH-PM-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）· License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

CNSH 包管理器 v1.0 —— init/install/publish/list/registry
- 中央仓库默认: ~/.cnsh-pkgs/（本地文件系统；后续可指 GitHub Releases 等远程源）
- 项目依赖目录: <project>/.cnsh_pkgs/<name>/
- 依赖声明: <project>/cnsh.json → dependencies
纯标准库 · M77 零中间层。

用法:
  cnsh pm init                                    # 生成 cnsh.json
  cnsh pm install <name>[@version]                # 安装包到 .cnsh_pkgs/ + 登记依赖
  cnsh pm publish [--repo <中央仓库目录>]           # 发布当前包（读 cnsh.json + src/）
  cnsh pm list                                    # 列出已安装依赖
  cnsh pm registry [path]                         # 显示/切换中央仓库源
"""
import sys
import json
import shutil
import argparse
from pathlib import Path

VERSION = "1.0.0"
UID = "UID9622"
DEFAULT_REPO = Path.home() / ".cnsh-pkgs"
DEPS_DIR = ".cnsh_pkgs"
MANIFEST = "cnsh.json"


def _load_manifest(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_manifest(path: Path, data: dict):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def cmd_init(args):
    manifest = Path(MANIFEST)
    if manifest.exists():
        print(f"🟡 已存在: {manifest}（不覆盖）")
        return 0
    data = {
        "name": Path.cwd().name,
        "version": "0.1.0",
        "description": "",
        "license": "CC BY-NC-SA 4.0",
        "entry": "src/main.cnsh",
        "author": {"name": "诸葛鑫", "uid": UID},
        "dependencies": {},
    }
    _save_manifest(manifest, data)
    print(f"✅ 已生成 {manifest}")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def _resolve_repo(repo_arg) -> Path:
    return Path(repo_arg).expanduser() if repo_arg else DEFAULT_REPO


def cmd_publish(args):
    manifest = Path(MANIFEST)
    data = _load_manifest(manifest)
    if not data or "name" not in data:
        print(f"❌ 缺少 {MANIFEST}（先运行: cnsh pm init）")
        return 1
    name, ver = data["name"], data.get("version", "0.1.0")
    if not all(c.isalnum() or c in "-_" for c in name):
        print(f"❌ 非法包名: {name}（仅字母数字-_）")
        return 1
    repo = _resolve_repo(args.repo)
    entry = Path(data.get("entry", "src/main.cnsh"))
    if not entry.exists():
        print(f"❌ 入口缺失: {entry}")
        return 1

    dst = repo / name / ver
    if dst.exists() and not args.force:
        print(f"🟡 该版本已存在: {name}@{ver}（--force 覆盖）")
        return 1
    dst.mkdir(parents=True, exist_ok=True)
    # 发布 src/ 全目录 + entry + 额外 files（对齐 cnsh init 骨架）
    src_dir = Path("src")
    files = data.get("files", [])
    rels = []
    if src_dir.is_dir():
        rels.append(src_dir)
    for rel in [Path(entry)] + [Path(f) for f in files if isinstance(f, str)]:
        if rel.exists() and rel.resolve() not in [x.resolve() for x in rels]:
            rels.append(rel)
    for rel in rels:
        tgt = dst / rel
        tgt.parent.mkdir(parents=True, exist_ok=True)
        if rel.is_dir():
            shutil.copytree(rel, tgt, dirs_exist_ok=True)
        else:
            shutil.copy2(rel, tgt)
    (dst / MANIFEST).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # 写 registry 索引
    registry = repo / "registry.json"
    idx = json.loads(registry.read_text(encoding="utf-8")) if registry.exists() else {}
    idx.setdefault(name, {})[ver] = {"entry": str(entry), "desc": data.get("description", "")}
    registry.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✅ 已发布 {name}@{ver} → {dst}")
    print(f"   仓库: {repo}")
    return 0


def cmd_install(args):
    spec = args.name
    name = spec
    want_ver = None
    if "@" in spec:
        name, want_ver = spec.rsplit("@", 1)
    repo = _resolve_repo(args.repo)
    versions = sorted((repo / name).iterdir()) if (repo / name).is_dir() else []
    if not versions:
        print(f"❌ 中央仓库未找到包: {name}（仓库: {repo}）")
        return 1
    ver_dir = None
    if want_ver:
        cand = repo / name / want_ver
        ver_dir = cand if cand.is_dir() else None
    else:
        ver_dir = versions[-1]  # 最高版本（按字典序即语义版本序）
    if ver_dir is None:
        print(f"❌ 版本不存在: {name}@{want_ver or 'latest'}")
        return 1

    proj = Path.cwd()
    deps = proj / DEPS_DIR / name
    if deps.exists():
        shutil.rmtree(deps)
    shutil.copytree(ver_dir, deps)
    print(f"✅ 已安装 {name}@{ver_dir.name} → {deps.relative_to(proj)}")

    # 登记依赖
    manifest = proj / MANIFEST
    data = _load_manifest(manifest)
    if data:
        data.setdefault("dependencies", {})[name] = ver_dir.name
        _save_manifest(manifest, data)
        print(f"   📝 已登记依赖: {name}@{ver_dir.name} → {MANIFEST}")
    return 0


def cmd_list(args):
    proj = Path.cwd()
    deps = proj / DEPS_DIR
    if not deps.is_dir():
        print("（未安装任何 CNSH 包）")
        return 0
    n = 0
    for d in sorted(deps.iterdir()):
        if d.is_dir():
            mf = d / MANIFEST
            ver = json.loads(mf.read_text(encoding="utf-8")).get("version", "?") if mf.exists() else "?"
            print(f"  {d.name}@{ver}  →  {d.relative_to(proj)}")
            n += 1
    print(f"共 {n} 个依赖")
    return 0


def cmd_registry(args):
    repo = _resolve_repo(args.repo)
    if args.repo and args.repo not in (None, ""):
        print(f"（仓库源已指向: {repo}）")
    else:
        print(f"中央仓库源: {repo}")
    repo.mkdir(parents=True, exist_ok=True)
    reg = repo / "registry.json"
    if reg.exists():
        idx = json.loads(reg.read_text(encoding="utf-8"))
        for name, vers in idx.items():
            print(f"  📦 {name}: {', '.join(vers.keys())}")
    else:
        print("  （仓库暂无包，cnsh pm publish 首个包后自动建立索引）")
    return 0


def main():
    ap = argparse.ArgumentParser(
        prog="cnsh pm", description=f"🐉 CNSH 包管理器 v{VERSION} · UID9622",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n  cnsh pm init\n  cnsh pm install 龍魂核心\n  cnsh pm publish\n  cnsh pm list\n  cnsh pm registry")
    sub = ap.add_subparsers(dest="cmd")

    i = sub.add_parser("init")
    i.set_defaults(fn=cmd_init)

    p = sub.add_parser("publish")
    p.add_argument("--repo", help="中央仓库目录（默认 ~/.cnsh-pkgs）")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_publish)

    ins = sub.add_parser("install")
    ins.add_argument("name", help="包名[版本]，如 龍魂核心@1.0.0")
    ins.add_argument("--repo", help="中央仓库目录")
    ins.set_defaults(fn=cmd_install)

    l = sub.add_parser("list")
    l.set_defaults(fn=cmd_list)

    rg = sub.add_parser("registry")
    rg.add_argument("repo", nargs="?", help="切换中央仓库源")
    rg.set_defaults(fn=cmd_registry)

    args = ap.parse_args()
    if not getattr(args, "cmd", None):
        ap.print_help()
        return 0
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
