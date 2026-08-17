#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌·申时·䷖剥-INDEX-COLLECTIVE-INTEL-V1-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2
"""
龍魂 · 协同涌现层（第4层 Collective Intelligence）
哲学④协同涌现 → 群体行为聚合 → 模式识别 → 自组织推荐
算法: 用户×文件共现矩阵 → 相似用户 → 未看过的推荐
用法:
  lh_collective_intel.py record <file_id> --user UID9622
  lh_collective_intel.py recommend <user> [--top 5]
  lh_collective_intel.py peers <user> [--top 3]
  lh_collective_intel.py status
"""
import argparse, json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

COL_FILE = Path.home() / ".longhun" / "index" / "collective.json"
EMPTY = {"version": "1.0", "user_files": {}}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load() -> dict:
    if COL_FILE.exists():
        try:
            return json.loads(COL_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return EMPTY


def save(d):
    COL_FILE.parent.mkdir(parents=True, exist_ok=True)
    COL_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


class CollectiveIntel:
    def __init__(self):
        self.data = load()

    def record(self, file_id: str, user: str) -> None:
        uf = self.data["user_files"].setdefault(user, {})
        uf[file_id] = uf.get(file_id, 0) + 1
        save(self.data)

    def recommend(self, user: str, top_k: int = 5) -> list:
        mine = set(self.data["user_files"].get(user, {}).keys())
        if not mine:
            return []
        scores = {}
        for other, files in self.data["user_files"].items():
            if other == user:
                continue
            ov = len(mine & set(files.keys()))
            if ov > 0:
                scores[other] = ov
        rec = defaultdict(float)
        for other, ov in scores.items():
            for fid, cnt in self.data["user_files"][other].items():
                if fid not in mine:
                    rec[fid] += cnt * ov
        ranked = sorted(rec.items(), key=lambda x: -x[1])[:top_k]
        return [{"file_id": fid, "strength": round(s, 2)} for fid, s in ranked]

    def peers(self, user: str, top_k: int = 3) -> list:
        mine = set(self.data["user_files"].get(user, {}).keys())
        peers = []
        for other, files in self.data["user_files"].items():
            if other == user:
                continue
            ov = len(mine & set(files.keys()))
            if ov > 0:
                peers.append((ov, other))
        peers.sort(key=lambda x: -x[0])
        return [{"user": u, "overlap": o} for o, u in peers[:top_k]]

    def status(self) -> dict:
        return {"users": len(self.data["user_files"]),
                "records": sum(len(f) for f in self.data["user_files"].values())}


def main():
    ap = argparse.ArgumentParser(description="龍魂协同涌现引擎")
    ap.add_argument("cmd", choices=["record", "recommend", "peers", "status"])
    ap.add_argument("arg", nargs="?", default="")
    ap.add_argument("--user", default="UID9622")
    ap.add_argument("--top", type=int, default=5)
    args = ap.parse_args()
    ci = CollectiveIntel()
    if args.cmd == "record":
        ci.record(args.arg, args.user)
        print(f"🐝 已记录: {args.user} 访问 {args.arg}")
    elif args.cmd == "recommend":
        for r in ci.recommend(args.user, args.top):
            print(f"🌟 {r['file_id']} (强度{r['strength']})")
    elif args.cmd == "peers":
        for p in ci.peers(args.user, args.top):
            print(f"👥 {p['user']} (共现{p['overlap']})")
    elif args.cmd == "status":
        s = ci.status()
        print(f"📊 用户 {s['users']} · 记录 {s['records']}")


if __name__ == "__main__":
    main()
