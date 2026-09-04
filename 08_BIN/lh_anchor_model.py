#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌·申时·䷖剥-INDEX-ANCHOR-MODEL-V1-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2
# 协议: CC BY-NC-SA 4.0（核心思想层）
"""
龍魂 · 多维锚点数据模型（第2层多维锚定的数据底座）
哲学②多维锚定 → 六类锚点：时间/内容/关系/行为/上下文
存储: ~/.longhun/index/（本地优先·数据主权）
零三方依赖 · Python 3.8+
用法:
  lh_anchor_model.py init | add <path> | show <id> | list | search <词>
"""
import argparse, hashlib, json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path

INDEX_DIR = Path.home() / ".longhun" / "index"
ANCHORS_FILE = INDEX_DIR / "anchors.json"
RELATIONS_FILE = INDEX_DIR / "relations.json"
ACCESS_FILE = INDEX_DIR / "access.json"

EMPTY_ANCHORS = {"version": "1.0", "files": {}}
EMPTY_RELATIONS = {"version": "1.0", "edges": []}
EMPTY_ACCESS = {"version": "1.0", "logs": []}

STOPWORDS = set("的了是在我你他她它我们你们他们这个那个一个没有就是不是什么怎么可以因为所以如果然后但是以及并且或者与和对把被让向从到于为以".split())


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def make_file_id(path: str) -> str:
    p = Path(path).resolve()
    h = hashlib.sha256(str(p).encode()).hexdigest()[:6].upper()
    return f"F-{datetime.now().strftime('%Y%m%d')}-{h}"


def tokenize(text: str) -> list:
    """中英分词：英文词 + 中文单字/2-gram"""
    tokens = []
    for w in re.findall(r"[A-Za-z0-9_]+", text.lower()):
        if len(w) > 1:
            tokens.append(w)
    for seg in re.findall(r"[\u4e00-\u9fff]+", text):
        tokens.extend(seg)
        tokens.extend(seg[i:i + 2] for i in range(len(seg) - 1))
    return tokens


def extract_keywords(text: str, top_k: int = 10) -> list:
    freq = {}
    for t in tokenize(text):
        if t not in STOPWORDS:
            freq[t] = freq.get(t, 0) + 1
    return [t for t, _ in sorted(freq.items(), key=lambda x: -x[1])[:top_k]]


def load_json(path: Path, default: dict) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return default


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


class AnchorModel:
    def __init__(self):
        self.anchors = load_json(ANCHORS_FILE, EMPTY_ANCHORS)
        self.relations = load_json(RELATIONS_FILE, EMPTY_RELATIONS)
        self.access = load_json(ACCESS_FILE, EMPTY_ACCESS)

    def init(self):
        INDEX_DIR.mkdir(parents=True, exist_ok=True)
        save_json(ANCHORS_FILE, EMPTY_ANCHORS)
        save_json(RELATIONS_FILE, EMPTY_RELATIONS)
        save_json(ACCESS_FILE, EMPTY_ACCESS)
        return f"✅ 索引库已初始化: {INDEX_DIR}"

    def add_file(self, path: str, content: str = None, meta: dict = None) -> dict:
        p = Path(path)
        if p.exists() and content is None:
            content = p.read_text(encoding="utf-8", errors="ignore")
        content = content or ""
        if meta is None:
            meta = {"file_name": p.name, "file_path": str(p)}
        file_id = make_file_id(str(p))
        now = now_iso()
        old = self.anchors["files"].get(file_id, {})
        anchor = {
            "file_id": file_id,
            "file_name": meta.get("file_name", p.name),
            "file_path": str(p),
            "dna": meta.get("dna", ""),
            "time_anchors": {
                "created": old.get("time_anchors", {}).get("created", now),
                "modified": now,
                "accessed": old.get("time_anchors", {}).get("accessed", []),
            },
            "content_anchors": {
                "title": meta.get("title", p.stem),
                "keywords": extract_keywords(content, 12),
                "tags": meta.get("tags", []),
                "summary": content.strip().splitlines()[0][:80] if content.strip() else "",
                "tokens": tokenize(content)[:2000],
            },
            "relation_anchors": old.get("relation_anchors", {
                "references": [], "referenced_by": [], "version_chain": {"current": "v1.0"}}),
            "behavior_anchors": old.get("behavior_anchors", {
                "access_count": 0, "access_users": [], "avg_duration": 0, "weight": 0.1}),
            "context_anchors": old.get("context_anchors", {"common_with": [], "triggered_by": []}),
        }
        self.anchors["files"][file_id] = anchor
        save_json(ANCHORS_FILE, self.anchors)
        return anchor

    def touch(self, file_id: str, user: str = "UID9622", duration: int = 0) -> dict:
        """记录访问行为（行为锚·动态演化）"""
        a = self.anchors["files"].get(file_id)
        if not a:
            return {"error": f"锚点不存在: {file_id}"}
        b = a["behavior_anchors"]
        b["access_count"] = b.get("access_count", 0) + 1
        if user not in b["access_users"]:
            b["access_users"].append(user)
        b["weight"] = round(min(1.0, b.get("weight", 0.1) + 0.02 * b.get("weight", 0.1) + 0.01), 3)
        b["avg_duration"] = int((b.get("avg_duration", 0) * (b["access_count"] - 1) + duration) / b["access_count"]) if b["access_count"] > 0 else duration
        a["time_anchors"]["accessed"].append({"at": now_iso(), "duration": duration})
        if len(a["time_anchors"]["accessed"]) > 50:
            a["time_anchors"]["accessed"] = a["time_anchors"]["accessed"][-50:]
        self.access["logs"].append({"file_id": file_id, "user": user, "duration": duration, "at": now_iso()})
        if len(self.access["logs"]) > 5000:
            self.access["logs"] = self.access["logs"][-5000:]
        save_json(ANCHORS_FILE, self.anchors)
        save_json(ACCESS_FILE, self.access)
        return a

    def add_relation(self, from_id: str, to_id: str, rel_type: str = "references"):
        self.relations["edges"].append({"from": from_id, "to": to_id, "type": rel_type, "at": now_iso()})
        save_json(RELATIONS_FILE, self.relations)

    def add_relations_bulk(self, edges: list) -> int:
        """批量写关系边（build 自动提取用·去重）"""
        existing = set((e["from"], e["to"], e.get("type")) for e in self.relations.get("edges", []))
        added = 0
        for f, t, rtype in edges:
            if (f, t, rtype) in existing:
                continue
            self.relations["edges"].append({"from": f, "to": t, "type": rtype, "at": now_iso()})
            existing.add((f, t, rtype))
            added += 1
        if added:
            save_json(RELATIONS_FILE, self.relations)
        return added

    def related(self, file_id: str, depth: int = 2) -> list:
        """关系锚·图遍历（哲学③关系索引 How）：返回深度 depth 内的关联文件（BFS）"""
        graph = {}
        for e in self.relations.get("edges", []):
            graph.setdefault(e["from"], []).append((e["to"], e.get("type", "references")))
            graph.setdefault(e["to"], []).append((e["from"], e.get("type", "references")))
        if file_id not in graph:
            return []
        seen, queue, results = {file_id}, [(file_id, 0)], []
        while queue:
            cur, d = queue.pop(0)
            if d >= depth:
                continue
            for nxt, rel in graph.get(cur, []):
                if nxt in seen:
                    continue
                seen.add(nxt)
                a = self.anchors["files"].get(nxt, {})
                results.append({"file_id": nxt, "file_name": a.get("file_name", nxt),
                                "file_path": a.get("file_path", ""), "rel_type": rel, "depth": d + 1})
                queue.append((nxt, d + 1))
        return results

    def tag(self, file_id: str, tags: list) -> dict:
        """结构索引·多维标签（哲学②结构索引 Where）：为文件打标签"""
        a = self.anchors["files"].get(file_id)
        if not a:
            return {"error": f"锚点不存在: {file_id}"}
        existing = a["content_anchors"].setdefault("tags", [])
        for t in tags:
            if t not in existing:
                existing.append(t)
        save_json(ANCHORS_FILE, self.anchors)
        return a

    def get_by_tags(self, tags: list, match_all: bool = True) -> list:
        """按标签检索：match_all=True 需含全部标签，False 任一即可"""
        want = set(tags)
        hits = []
        for fid, a in self.anchors["files"].items():
            have = set(a["content_anchors"].get("tags", []))
            ok = (have >= want) if match_all else bool(have & want)
            if ok:
                hits.append({"file_id": fid, "file_name": a["file_name"], "file_path": a["file_path"]})
        return hits

    def search(self, query: str) -> list:
        """按关键词/路径粗检索"""
        q = set(tokenize(query))
        if not q:
            return []
        scored = []
        for fid, a in self.anchors["files"].items():
            hay = set(a["content_anchors"].get("tokens", [])) | set(a["content_anchors"].get("keywords", []))
            score = len(q & hay)
            if score > 0:
                scored.append((score, a["behavior_anchors"].get("weight", 0), fid, a["file_name"], a["file_path"]))
        scored.sort(key=lambda x: (-x[0], -x[1]))
        return [{"file_id": s[2], "file_name": s[3], "file_path": s[4], "score": s[0], "weight": s[1]} for s in scored[:20]]

    def show(self, file_id: str) -> dict:
        a = self.anchors["files"].get(file_id)
        return a or {"error": f"锚点不存在: {file_id}"}

    def list(self) -> list:
        return [{"file_id": fid, "file_name": a["file_name"], "file_path": a["file_path"], "weight": a["behavior_anchors"].get("weight", 0)}
                for fid, a in self.anchors["files"].items()]


def main():
    ap = argparse.ArgumentParser(description="龍魂多维锚点数据模型")
    ap.add_argument("cmd", choices=["init", "add", "show", "list", "search", "touch", "relation", "related", "tag", "by-tags"])
    ap.add_argument("arg", nargs="?", default="")
    ap.add_argument("--user", default="UID9622")
    ap.add_argument("--rel", default="references")
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--match-all", action="store_true", default=False)
    args = ap.parse_args()
    m = AnchorModel()
    if args.cmd == "init":
        print(m.init())
    elif args.cmd == "add":
        a = m.add_file(args.arg)
        print(f"✅ 已索引 {a['file_name']} [{a['file_id']}]")
    elif args.cmd == "show":
        print(json.dumps(m.show(args.arg), ensure_ascii=False, indent=2))
    elif args.cmd == "list":
        for it in m.list():
            print(f"{it['file_id']}  {it['file_name']}  w={it['weight']}")
    elif args.cmd == "search":
        for r in m.search(args.arg):
            print(f"[{r['score']}] {r['file_name']}  {r['file_path']}")
    elif args.cmd == "touch":
        a = m.touch(args.arg, args.user)
        print(f"👣 已记录访问 {args.arg} · count={a.get('behavior_anchors', {}).get('access_count')}")
    elif args.cmd == "relation":
        parts = args.arg.split(",")
        if len(parts) == 2:
            m.add_relation(parts[0].strip(), parts[1].strip(), args.rel)
            print(f"🔗 关系已记录: {parts[0]} --{args.rel}--> {parts[1]}")
    elif args.cmd == "related":
        for r in m.related(args.arg, args.depth):
            print(f"⛓️ d={r['depth']} [{r['rel_type']}] {r['file_name']}  {r['file_path']}")
    elif args.cmd == "tag":
        tags = [t.strip() for t in args.arg.split(",") if t.strip()]
        a = m.tag(tags.pop(0), tags) if tags else {"error": "用法: tag <file_id>,<tag1>,<tag2>"}
        if "error" not in a:
            print(f"🏷️ 已打标签 {a['file_name']}: {a['content_anchors'].get('tags')}")
        else:
            print(a["error"])
    elif args.cmd == "by-tags":
        tags = [t.strip() for t in args.arg.split(",") if t.strip()]
        for r in m.get_by_tags(tags, match_all=args.match_all):
            print(f"🏷️ {r['file_name']}  {r['file_path']}")


if __name__ == "__main__":
    main()
