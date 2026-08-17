#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌·申时·䷖剥-INDEX-VECTOR-INDEX-V1-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2
"""
龍魂 · 向量索引层（第2层多维锚定·内容锚语义检索）
轻量实现：字符2-gram + TF向量 + 余弦相似度
【零三方依赖】不引入 sentence-transformers/faiss（低算力）
用法:
  lh_vector_index.py index <path> [--id F-XXX] [--name 名]
  lh_vector_index.py search <词> [--top 5]
  lh_vector_index.py similar <file_id> [--top 5]
  lh_vector_index.py status
"""
import argparse, json, math, re
from collections import Counter
from pathlib import Path

VEC_FILE = Path.home() / ".longhun" / "index" / "vectors.json"
EMPTY = {"version": "1.0", "docs": {}}


def load() -> dict:
    if VEC_FILE.exists():
        try:
            return json.loads(VEC_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return EMPTY


def save(d):
    VEC_FILE.parent.mkdir(parents=True, exist_ok=True)
    VEC_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def gram2(text: str) -> Counter:
    c = Counter()
    for w in re.findall(r"[A-Za-z0-9_]+", text.lower()):
        if len(w) > 1:
            c[w] += 1
    for seg in re.findall(r"[\u4e00-\u9fff]+", text):
        for ch in seg:
            c[ch] += 1
        for i in range(len(seg) - 1):
            c[seg[i:i + 2]] += 1
    return c


def build_vector(text: str) -> dict:
    return dict(gram2(text).most_common(500))


def cosine(a: dict, b: dict) -> float:
    if not a or not b:
        return 0.0
    inter = set(a) & set(b)
    dot = sum(a[k] * b[k] for k in inter)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return round(dot / (na * nb), 4)


class VectorIndex:
    def __init__(self):
        self.data = load()

    def index(self, file_id: str, name: str, path: str, content: str):
        self.data["docs"][file_id] = {"name": name, "path": path, "vec": build_vector(content)}
        save(self.data)

    def search(self, query: str, top_k: int = 5) -> list:
        qv = build_vector(query)
        scored = [(cosine(qv, doc["vec"]), fid, doc["name"], doc["path"])
                  for fid, doc in self.data["docs"].items()]
        scored.sort(key=lambda x: -x[0])
        return [{"score": s, "file_id": fid, "name": n, "path": p}
                for s, fid, n, p in scored[:top_k] if s > 0.02]

    def similar(self, file_id: str, top_k: int = 5) -> list:
        doc = self.data["docs"].get(file_id)
        if not doc:
            return []
        scored = [(cosine(doc["vec"], other["vec"]), fid, other["name"], other["path"])
                  for fid, other in self.data["docs"].items() if fid != file_id]
        scored.sort(key=lambda x: -x[0])
        return [{"score": s, "file_id": fid, "name": n, "path": p}
                for s, fid, n, p in scored[:top_k] if s > 0.1]


def main():
    ap = argparse.ArgumentParser(description="龍魂向量索引（2-gram轻量版）")
    ap.add_argument("cmd", choices=["index", "search", "similar", "status"])
    ap.add_argument("arg", nargs="?", default="")
    ap.add_argument("--id", default="")
    ap.add_argument("--name", default="")
    ap.add_argument("--path", default="")
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()
    vi = VectorIndex()
    if args.cmd == "index":
        p = Path(args.arg)
        content = p.read_text(encoding="utf-8", errors="ignore") if p.exists() else args.arg
        name = args.name or (p.name if p.exists() else "query")
        fid = args.id or f"F-{name[:6].upper()}"
        vi.index(fid, name, args.path or str(p), content)
        print(f"🧬 向量已建: {name} [{fid}]")
    elif args.cmd == "search":
        for r in vi.search(args.arg, args.top):
            print(f"[{r['score']:.4f}] {r['name']}  {r['path']}")
    elif args.cmd == "similar":
        for r in vi.similar(args.arg, args.top):
            print(f"[{r['score']:.4f}] {r['name']}  {r['path']}")
    elif args.cmd == "status":
        print(f"📊 向量库: {len(vi.data['docs'])} 个文档")


if __name__ == "__main__":
    main()
