#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌·申时·䷖剥-INDEX-IMPLICIT-RETRIEVAL-V1-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2
"""
龍魂 · 无意识索引（第5层 Zero-Click Retrieval）
哲学⑤无意识索引 → 不点搜索 → 按上下文自动推送 → 无感知获得
引擎: 上下文关键词 → 匹配锚点 → 结合行为权重 → 推送 top
用法:
  lh_implicit_retrieval.py suggest --context "写快速索引" [--top 5]
  lh_implicit_retrieval.py status
"""
import argparse, json, re
from pathlib import Path

ANCHORS_FILE = Path.home() / ".longhun" / "index" / "anchors.json"
WEIGHTS_FILE = Path.home() / ".longhun" / "index" / "weights.json"


def load_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return default


class ImplicitRetrieval:
    def __init__(self):
        self.anchors = load_json(ANCHORS_FILE, {"files": {}})
        self.weights = load_json(WEIGHTS_FILE, {"files": {}})

    def suggest(self, context: str = "", top_k: int = 5) -> list:
        if not context:
            return []
        words = []
        for seg in re.findall(r"[\u4e00-\u9fff]+", context):
            words.extend(seg)
            words.extend(seg[i:i + 2] for i in range(len(seg) - 1))
        for w in re.findall(r"[A-Za-z0-9_]+", context.lower()):
            if len(w) > 1:
                words.append(w)
        if not words:
            return []
        scored = []
        for fid, a in self.anchors["files"].items():
            toks = set(a.get("content_anchors", {}).get("tokens", []))
            overlap = sum(1 for w in words if w in toks)
            if overlap > 0:
                w = self.weights["files"].get(fid, {}).get("weight", 0.1)
                scored.append((overlap, w, fid, a.get("file_name", ""), a.get("file_path", "")))
        scored.sort(key=lambda x: (-x[0], -x[1]))
        return [{"file_id": s[2], "name": s[3], "path": s[4], "match": s[0], "weight": round(s[1], 3)}
                for s in scored[:top_k]]


def main():
    ap = argparse.ArgumentParser(description="龍魂无意识检索引擎")
    ap.add_argument("cmd", choices=["suggest", "status"])
    ap.add_argument("arg", nargs="?", default="")
    ap.add_argument("--context", default="")
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()
    ir = ImplicitRetrieval()
    if args.cmd == "suggest":
        ctx = args.context or args.arg
        for r in ir.suggest(ctx, args.top):
            print(f"🔮 [{r['match']}·w{r['weight']}] {r['name']}  {r['path']}")
        if not ctx:
            print("⚠️ 请提供 --context 或参数")
    elif args.cmd == "status":
        print(f"📊 锚点库: {len(ir.anchors['files'])} 个文件")


if __name__ == "__main__":
    main()
