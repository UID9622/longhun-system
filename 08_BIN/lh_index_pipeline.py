#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌·申时·䷖剥-INDEX-PIPELINE-V1-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2
"""
龍魂 · 快速索引流水线（集成入口）
串联五层: 主动感知 → 多维锚定 → 动态演化 → 协同涌现 → 无意识检索
用法:
  lh_index_pipeline.py init
  lh_index_pipeline.py build [<目录|文件>]
  lh_index_pipeline.py search <词> [--top 5]
  lh_index_pipeline.py touch <file_id> [--user UID9622]
  lh_index_pipeline.py suggest --context <词> [--top 5]
  lh_index_pipeline.py rank [--top 10]
  lh_index_pipeline.py status
"""
import argparse, re, sys
from pathlib import Path

# 复用五层引擎（同目录）
sys.path.insert(0, str(Path(__file__).parent))
from lh_anchor_model import AnchorModel
from lh_vector_index import VectorIndex
from lh_behavior_learner import BehaviorLearner
from lh_collective_intel import CollectiveIntel
from lh_implicit_retrieval import ImplicitRetrieval

# 哲学③关系锚·自动发现：识别正文中引用的 .md / .py 文件名
REL_PATTERN = re.compile(r"(?:LH-|CNSH)[A-Za-z0-9_-]*\.md|\.codebuddy/[\w./-]+\.(?:md|json)|[\w./-]+\.(?:md|py|json)")

HOME = Path.home()
DEFAULT_TARGETS = [
    HOME / "longhun-system" / "01_protocols",
    HOME / "longhun-system" / "12_DOCS",
    HOME / "longhun-system" / "bin",
]
IGNORE = {"__pycache__", ".git", "node_modules", ".asc", ".tmp", ".pyc"}


def walk_files(paths) -> list:
    files = []
    for p in paths:
        p = Path(p).expanduser()
        if not p.exists():
            continue
        if p.is_file():
            files.append(p)
        else:
            for f in p.rglob("*"):
                if f.is_file() and not any(ig in f.name for ig in IGNORE):
                    files.append(f)
    return files


def build(targets=None) -> dict:
    am = AnchorModel()
    vi = VectorIndex()
    am.init()
    files = walk_files(targets or DEFAULT_TARGETS)
    n = 0
    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            content = ""
        if not content.strip():
            continue
        meta = {"file_name": f.name, "file_path": str(f)}
        for line in content.splitlines()[:5]:
            if line.startswith("DNA:"):
                meta["dna"] = line[4:].strip()
                break
        a = am.add_file(str(f), content, meta)
        vi.index(a["file_id"], f.name, str(f), content)
        n += 1
    # 哲学③关系锚·自动发现：扫描已索引文件的引用，建关系边
    rel_added = auto_relations(am, files)
    return {"indexed": n, "total_seen": len(files), "relations_added": rel_added}


def auto_relations(am: AnchorModel, files: list) -> int:
    """从文件内容自动提取引用关系（哲学③关系索引 How·自动发现）"""
    # file_name → file_id 映射（含不含路径后缀）
    id_by_name = {}
    for fid, a in am.anchors["files"].items():
        id_by_name[a["file_name"]] = fid
    edges = []
    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        fid = id_by_name.get(f.name)
        if not fid:
            continue
        # 在正文前 80 行找引用（正文引用一般出现在前部·避免目录噪声）
        head = "\n".join(content.splitlines()[:80])
        for ref in REL_PATTERN.findall(head):
            ref_name = ref.split("/")[-1] if "/" in ref else ref
            ref_id = id_by_name.get(ref_name)
            if ref_id and ref_id != fid:
                edges.append((fid, ref_id, "references"))
    return am.add_relations_bulk(edges)


def search(query: str, top_k: int = 5) -> list:
    return AnchorModel().search(query)[:top_k]


def main():
    ap = argparse.ArgumentParser(description="龍魂快速索引流水线")
    ap.add_argument("cmd", nargs="?", default="status", help="init/build/search/touch/suggest/rank/related/tag/by-tags/status")
    ap.add_argument("arg", nargs="?", default="")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--user", default="UID9622")
    ap.add_argument("--context", default="")
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--match-all", action="store_true", default=False)
    args = ap.parse_args()
    # 🔧 智能兜底：第一参数不是已知子命令 → 自动当作搜索词（兼容 `lh idx-search 词` / `lh idx 词`）
    known = {"init", "build", "search", "touch", "suggest", "rank", "related", "tag", "by-tags", "status"}
    if args.cmd not in known:
        if args.arg:
            args.cmd, args.arg = args.arg, args.cmd
        else:
            args.cmd, args.arg = "search", args.cmd
    # 🔧 兜底2：提供了 --context 但未指定子命令（lh idx-suggest --context 词）→ 转 suggest
    if args.cmd in ("status", "search") and args.context and args.arg == "" and args.top <= 5:
        args.cmd = "suggest"

    if args.cmd == "init":
        print(AnchorModel().init())
    elif args.cmd == "build":
        r = build([args.arg] if args.arg else None)
        print(f"🏗️ 索引完成: {r['indexed']} 个文件（扫描 {r['total_seen']}）· 关系边 +{r['relations_added']}")
    elif args.cmd == "search":
        for s in search(args.arg, args.top):
            print(f"[{s['score']}] {s['file_name']}  {s['file_path']}  (w={s['weight']})")
    elif args.cmd == "touch":
        am, bl, ci = AnchorModel(), BehaviorLearner(), CollectiveIntel()
        a = am.touch(args.arg, args.user)
        bl.learn(args.arg, args.user)
        ci.record(args.arg, args.user)
        print(f"👣 已记录 {args.arg} · count={a.get('behavior_anchors', {}).get('access_count')}")
    elif args.cmd == "suggest":
        ctx = args.context or args.arg
        for r in ImplicitRetrieval().suggest(ctx, args.top):
            print(f"🔮 [{r['match']}·w{r['weight']}] {r['name']}  {r['path']}")
    elif args.cmd == "rank":
        for i, r in enumerate(BehaviorLearner().rank(args.top), 1):
            print(f"#{i} [{r['weight']}] {r['file_id']} (访问{r['count']}次)")
    elif args.cmd == "related":
        for r in AnchorModel().related(args.arg, args.depth):
            print(f"⛓️ d={r['depth']} [{r['rel_type']}] {r['file_name']}  {r['file_path']}")
    elif args.cmd == "tag":
        am = AnchorModel()
        parts = [p.strip() for p in args.arg.split(",") if p.strip()]
        if len(parts) < 2:
            print("🏷️ 用法: idx tag <file_id>,<tag1>[,<tag2>...]")
        else:
            a = am.tag(parts[0], parts[1:])
            if "error" in a:
                print(a["error"])
            else:
                print(f"🏷️ 已打标签 {a['file_name']}: {a['content_anchors'].get('tags')}")
    elif args.cmd == "by-tags":
        tags = [p.strip() for p in args.arg.split(",") if p.strip()]
        for r in AnchorModel().get_by_tags(tags, match_all=args.match_all):
            print(f"🏷️ {r['file_name']}  {r['file_path']}")
    elif args.cmd == "status":
        am, vi, bl, ci = AnchorModel(), VectorIndex(), BehaviorLearner(), CollectiveIntel()
        print(f"📊 锚点: {len(am.anchors['files'])} 文件")
        print(f"🧬 向量: {len(vi.data['docs'])} 文档")
        print(f"📈 权重: {bl.status()['total']} 文件")
        print(f"🐝 协同: {ci.status()['users']} 用户 · {ci.status()['records']} 记录")


if __name__ == "__main__":
    main()
