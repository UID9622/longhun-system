#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
muse_index.py — 绮华·私密素材 DNA 索引器 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
归属  : UID9622 一个人 · P-VIS-001 附属工具
师承  : 🌿 曾仕強老師（永恒显示）
铁律  : 本机运行·不走网关·不进主审计·不推 Notion
════════════════════════════════════════════

老大原话：
  "这些帧都可以打散·DNA 归类·以后组装文件和题材
   因为路径设计懂不起·哈哈"

这工具就是干这个：
  1. 扫描 ~/cnsh/私密空间/ 下所有文件
  2. 每个文件一个 DNA（内容哈希·唯一）
  3. 自动分类（图/视频/音频/脚本/文档/其他）
  4. 你用 DNA 操作，我帮你管路径
  5. 组装合集：把 N 个 DNA 软链到一个新文件夹（不移动原文件）

命令：
  muse-scan                   扫描私密空间·建索引（可反复跑·增量）
  muse-list [--kind img]      列出素材（按类型筛）
  muse-search "关键词"         按文件名/标签搜
  muse-show <dna>             看某条的详情
  muse-tag <dna> "标签1,标签2" 打标
  muse-pack <名字> <dna> ...   组装合集·软链·原文件不动
  muse-stats                  统计
  muse-clean                  清掉引用不存在的索引条目（文件删了但索引还在）

索引存放：
  ~/cnsh/私密空间/index/registry.jsonl   主索引（chmod 600）
  ~/cnsh/私密空间/packs/                  组装好的合集
"""

import os, sys, json, hashlib
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════
HOME = Path.home()
PRIV_DIR = HOME / "cnsh" / "私密空间"
INDEX_DIR = PRIV_DIR / "index"
REGISTRY = INDEX_DIR / "registry.jsonl"
PACKS_DIR = PRIV_DIR / "packs"

# 系统目录（扫描时跳过）
SKIP_DIR_NAMES = {
    "sessions", "index", "packs",
    ".git", ".DS_Store", "__pycache__", ".venv", "node_modules", ".cache",
}
SKIP_FILE_PREFIXES = (".", "_")

for d in (INDEX_DIR, PACKS_DIR):
    d.mkdir(parents=True, exist_ok=True)
    try:
        d.chmod(0o700)
    except Exception:
        pass

# 文件类型
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".bmp", ".tiff", ".avif", ".svg"}
VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".flv", ".m4v"}
AUDIO_EXTS = {".mp3", ".wav", ".ogg", ".m4a", ".flac", ".aac"}
DOC_EXTS = {".md", ".txt", ".pdf", ".docx", ".doc", ".rtf", ".epub"}
CODE_EXTS = {".py", ".sh", ".zsh", ".js", ".ts", ".tsx", ".jsx", ".rb", ".go", ".rs",
             ".c", ".cpp", ".h", ".hpp", ".java", ".kt", ".swift",
             ".html", ".css", ".scss", ".json", ".yaml", ".yml", ".toml", ".ini"}

KIND_MAP = [
    ("img", IMAGE_EXTS),
    ("vid", VIDEO_EXTS),
    ("aud", AUDIO_EXTS),
    ("doc", DOC_EXTS),
    ("code", CODE_EXTS),
]

KIND_EMOJI = {"img": "🎨", "vid": "🎬", "aud": "🎧", "doc": "📄", "code": "💻", "other": "📦"}

# 颜色
C, G, Y, R, D, B, M, NC = (
    "\033[36m", "\033[32m", "\033[33m", "\033[31m",
    "\033[2m", "\033[1m", "\033[35m", "\033[0m"
)


# ═══════════════════════════════════════════════
# 工具
# ═══════════════════════════════════════════════
def classify(path: Path) -> str:
    ext = path.suffix.lower()
    for kind, exts in KIND_MAP:
        if ext in exts:
            return kind
    return "other"


def sha12_of_file(path: Path) -> str:
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while True:
                b = f.read(65536)
                if not b:
                    break
                h.update(b)
        return h.hexdigest()[:12].upper()
    except Exception:
        return None


def human_size(n: int) -> str:
    for unit in ("B", "K", "M", "G", "T"):
        if n < 1024:
            return f"{n:.1f}{unit}" if unit != "B" else f"{n}{unit}"
        n /= 1024
    return f"{n:.1f}P"


# ═══════════════════════════════════════════════
# 索引 CRUD
# ═══════════════════════════════════════════════
def load_registry() -> list:
    if not REGISTRY.exists():
        return []
    out = []
    with open(REGISTRY, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except Exception:
                    pass
    return out


def save_registry(records: list):
    with open(REGISTRY, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    try:
        REGISTRY.chmod(0o600)
    except Exception:
        pass


def build_record(path: Path) -> dict:
    try:
        st = path.stat()
    except Exception:
        return None

    sha = sha12_of_file(path)
    if not sha:
        return None

    kind = classify(path)
    return {
        "dna": f"PRIV-{kind.upper()}-{sha}",
        "sha12": sha,
        "kind": kind,
        "ext": path.suffix.lower(),
        "name": path.name,
        "rel_path": str(path.relative_to(PRIV_DIR)),
        "size": st.st_size,
        "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
        "scanned_at": datetime.now().isoformat(timespec="seconds"),
        "tags": [],
        "notes": "",
    }


# ═══════════════════════════════════════════════
# 命令
# ═══════════════════════════════════════════════
def cmd_scan():
    print(f"{C}━━━ 🔍 扫描 ~/cnsh/私密空间/ ━━━{NC}")
    if not PRIV_DIR.exists():
        print(f"{R}🔴 私密空间不存在{NC}")
        return

    existing = load_registry()
    by_sha = {r["sha12"]: r for r in existing}
    by_path = {r["rel_path"]: r for r in existing}

    new_count = 0
    update_count = 0
    skip_count = 0

    for p in PRIV_DIR.rglob("*"):
        if p.is_dir():
            continue
        # 跳过系统目录里的文件
        if any(name in p.parts for name in SKIP_DIR_NAMES):
            continue
        # 跳过隐藏文件
        if p.name.startswith(SKIP_FILE_PREFIXES):
            continue

        rel = str(p.relative_to(PRIV_DIR))

        # 如果路径已经在索引里·看文件有没变
        if rel in by_path:
            old = by_path[rel]
            try:
                size_now = p.stat().st_size
            except Exception:
                continue
            if old.get("size") == size_now:
                skip_count += 1
                continue
            # 文件变了·重新打 DNA
            new_rec = build_record(p)
            if new_rec:
                by_path[rel] = new_rec
                by_sha.pop(old["sha12"], None)
                by_sha[new_rec["sha12"]] = new_rec
                # 保留标签
                new_rec["tags"] = old.get("tags", [])
                new_rec["notes"] = old.get("notes", "")
                update_count += 1
                print(f"  {Y}~{NC} [{new_rec['kind']}] {new_rec['dna']}  {new_rec['name']}  (内容变了·重新打码)")
            continue

        # 新文件
        rec = build_record(p)
        if not rec:
            continue
        # 同内容不同路径·复用 DNA 但多路径
        if rec["sha12"] in by_sha:
            skip_count += 1
            continue

        by_path[rel] = rec
        by_sha[rec["sha12"]] = rec
        new_count += 1
        print(f"  {G}+{NC} {KIND_EMOJI[rec['kind']]} [{rec['kind']}] {rec['dna']}  {D}{human_size(rec['size']):>8}{NC}  {rec['name']}")

    all_records = list(by_path.values())
    save_registry(all_records)

    print()
    print(f"{G}✅ 扫描完成{NC}")
    print(f"  新增: {new_count}  ·  更新: {update_count}  ·  已存在跳过: {skip_count}")
    print(f"  总索引: {len(all_records)}")
    print(f"  索引位置: {D}{REGISTRY}{NC}")


def cmd_list(kind_filter=None, limit=50):
    recs = load_registry()
    if kind_filter:
        recs = [r for r in recs if r.get("kind") == kind_filter]
    recs = sorted(recs, key=lambda r: r.get("mtime", ""), reverse=True)[:limit]

    if not recs:
        print(f"{Y}（没有匹配的素材·先跑 muse-scan 扫一下）{NC}")
        return

    print(f"{C}━━━ 素材清单 · {len(recs)} 条 ━━━{NC}")
    for r in recs:
        emoji = KIND_EMOJI.get(r["kind"], "📦")
        tags = " ".join(f"#{t}" for t in r.get("tags", []))
        print(f"  {emoji} {B}{r['dna']}{NC}  {human_size(r['size']):>8}  {r['name']}")
        if tags:
            print(f"        {C}{tags}{NC}")


def cmd_search(keyword):
    recs = load_registry()
    kw = keyword.lower()
    hits = []
    for r in recs:
        hay = (r.get("name", "") + " " + " ".join(r.get("tags", [])) + " " + r.get("notes", "")).lower()
        if kw in hay:
            hits.append(r)
    if not hits:
        print(f"{Y}（没命中「{keyword}」）{NC}")
        return
    print(f"{C}━━━ 命中 {len(hits)} 条「{keyword}」━━━{NC}")
    for r in hits:
        emoji = KIND_EMOJI.get(r["kind"], "📦")
        print(f"  {emoji} {B}{r['dna']}{NC}  {r['name']}")
        if r.get("tags"):
            print(f"        {C}{' '.join('#'+t for t in r['tags'])}{NC}")


def _find_by_dna(dna_prefix: str):
    """支持短前缀匹配·输入 PRIV-IMG-ABC1 也行，甚至 ABC1 也行"""
    recs = load_registry()
    up = dna_prefix.upper()
    # 完整匹配
    for r in recs:
        if r["dna"] == up:
            return r
    # 尾部哈希匹配（PRIV-IMG-ABC1 只写了 ABC1）
    hits = [r for r in recs if r["sha12"].startswith(up) or r["dna"].endswith(up)]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        print(f"{Y}🟡 匹配多条（{len(hits)} 条），请给更长的 DNA 前缀：{NC}")
        for r in hits[:10]:
            print(f"  · {r['dna']}  {r['name']}")
        return None
    return None


def cmd_show(dna_prefix):
    r = _find_by_dna(dna_prefix)
    if not r:
        print(f"{R}🔴 没找到 {dna_prefix}{NC}")
        return
    print(f"{C}━━━ {r['dna']} ━━━{NC}")
    print(f"  文件名  : {r['name']}")
    print(f"  类型    : {r['kind']} {KIND_EMOJI.get(r['kind'],'')}")
    print(f"  大小    : {human_size(r['size'])}")
    print(f"  修改时间: {r.get('mtime','?')}")
    print(f"  扫描时间: {r.get('scanned_at','?')}")
    print(f"  相对路径: {D}{r['rel_path']}{NC}")
    print(f"  绝对路径: {D}{PRIV_DIR / r['rel_path']}{NC}")
    tags = r.get("tags", [])
    print(f"  标签    : {' '.join('#'+t for t in tags) if tags else '（无）'}")
    notes = r.get("notes", "")
    print(f"  笔记    : {notes or '（无）'}")


def cmd_tag(dna_prefix, tags_str):
    r = _find_by_dna(dna_prefix)
    if not r:
        print(f"{R}🔴 没找到 {dna_prefix}{NC}")
        return
    # 支持中文逗号和英文逗号
    new_tags = [t.strip() for t in tags_str.replace("，", ",").split(",") if t.strip()]
    recs = load_registry()
    for rec in recs:
        if rec["dna"] == r["dna"]:
            merged = list(dict.fromkeys(rec.get("tags", []) + new_tags))
            rec["tags"] = merged
            break
    save_registry(recs)
    print(f"{G}✅ {r['dna']} 标签 → {' '.join('#'+t for t in merged)}{NC}")


def cmd_pack(pack_name, dna_list):
    if not dna_list:
        print(f"{R}用法: muse-pack 合集名 <dna1> <dna2> ...{NC}")
        return

    pack_dir = PACKS_DIR / f"pack_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{pack_name}"
    pack_dir.mkdir(exist_ok=True)
    try:
        pack_dir.chmod(0o700)
    except Exception:
        pass
    links_dir = pack_dir / "links"
    links_dir.mkdir(exist_ok=True)

    manifest = {
        "pack_name": pack_name,
        "created": datetime.now().isoformat(),
        "items": [],
    }

    found = 0
    missing = 0
    for d in dna_list:
        r = _find_by_dna(d)
        if not r:
            print(f"  {R}❌ 未找到 {d}{NC}")
            missing += 1
            continue
        src = PRIV_DIR / r["rel_path"]
        if not src.exists():
            print(f"  {R}❌ 源文件丢了 {src}{NC}")
            missing += 1
            continue
        # 软链（macOS 支持）
        link = links_dir / r["name"]
        # 同名防撞
        if link.exists():
            link = links_dir / f"{r['sha12']}_{r['name']}"
        try:
            link.symlink_to(src.resolve())
        except Exception as e:
            print(f"  {R}❌ 软链失败 {r['name']}: {e}{NC}")
            continue

        manifest["items"].append({
            "dna": r["dna"],
            "name": r["name"],
            "rel_path": r["rel_path"],
            "kind": r["kind"],
        })
        print(f"  {G}+{NC} {r['dna']}  {r['name']}")
        found += 1

    with open(pack_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    try:
        (pack_dir / "manifest.json").chmod(0o600)
    except Exception:
        pass

    print()
    print(f"{G}✅ 合集打好：{pack_dir}{NC}")
    print(f"   包含 {found} 件 · 缺失 {missing} 件 · 原文件一动没动（软链）")


def cmd_stats():
    recs = load_registry()
    if not recs:
        print(f"{Y}（索引是空的·先跑 muse-scan）{NC}")
        return
    from collections import Counter
    kinds = Counter(r["kind"] for r in recs)
    exts = Counter(r.get("ext", "?") for r in recs)
    total_size = sum(r.get("size", 0) for r in recs)

    print(f"{C}━━━ 📊 私密空间素材统计 ━━━{NC}")
    print(f"  总素材数: {len(recs)}")
    print(f"  总大小  : {human_size(total_size)}")
    print()
    print(f"  按类型:")
    for k in ("img", "vid", "aud", "doc", "code", "other"):
        n = kinds.get(k, 0)
        bar = "█" * min(n, 40)
        print(f"    {KIND_EMOJI[k]} {k:6s} {n:4d}  {bar}")
    print()
    # 前 5 扩展名
    print(f"  Top 5 扩展名:")
    for ext, n in exts.most_common(5):
        print(f"    {ext or '(无)':8s} {n}")
    print()
    # 标签统计
    tag_counter = Counter()
    for r in recs:
        for t in r.get("tags", []):
            tag_counter[t] += 1
    if tag_counter:
        print(f"  已用标签:")
        for t, n in tag_counter.most_common(10):
            print(f"    #{t}  ({n})")
    else:
        print(f"  {D}（还没打过标签·用 muse-tag <dna> \"标签1,标签2\"）{NC}")


def cmd_clean():
    recs = load_registry()
    alive = []
    dead = 0
    for r in recs:
        if (PRIV_DIR / r["rel_path"]).exists():
            alive.append(r)
        else:
            print(f"  {Y}- {r['dna']}  {r['name']}  (文件已不在){NC}")
            dead += 1
    if dead:
        save_registry(alive)
        print(f"{G}✅ 清理 {dead} 条失效索引·剩 {len(alive)}{NC}")
    else:
        print(f"{G}✅ 没有失效的索引·{len(alive)} 条全活{NC}")


# ═══════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════
def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    cmd = args[0]
    if cmd == "scan":
        cmd_scan()
    elif cmd == "list":
        kind = None
        limit = 50
        i = 1
        while i < len(args):
            if args[i] == "--kind" and i+1 < len(args):
                kind = args[i+1]; i += 2
            elif args[i] == "--limit" and i+1 < len(args):
                limit = int(args[i+1]); i += 2
            else:
                i += 1
        cmd_list(kind_filter=kind, limit=limit)
    elif cmd == "search":
        if len(args) < 2:
            print("用法: search 关键词")
            return
        cmd_search(args[1])
    elif cmd == "show":
        if len(args) < 2:
            print("用法: show <dna>")
            return
        cmd_show(args[1])
    elif cmd == "tag":
        if len(args) < 3:
            print("用法: tag <dna> \"标签1,标签2\"")
            return
        cmd_tag(args[1], args[2])
    elif cmd == "pack":
        if len(args) < 3:
            print("用法: pack <合集名> <dna1> <dna2> ...")
            return
        cmd_pack(args[1], args[2:])
    elif cmd == "stats":
        cmd_stats()
    elif cmd == "clean":
        cmd_clean()
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
