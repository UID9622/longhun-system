#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌·申时·䷖剥-INDEX-BEHAVIOR-LEARNER-V1-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2
"""
龍魂 · 动态加权引擎（第3层 Adaptive Weighting）
哲学③动态演化 → 访问加权 + 时间衰减 + 热冷归档
算法: weight = (旧weight·e^{-λΔt}) + 0.05 每次访问，7天半衰期，上限1.0
用法:
  lh_behavior_learner.py learn <file_id> [--user UID9622]
  lh_behavior_learner.py decay [--days 30]
  lh_behavior_learner.py rank [--top 10]
  lh_behavior_learner.py status
"""
import argparse, json, math
from datetime import datetime, timezone
from pathlib import Path

LEARN_FILE = Path.home() / ".longhun" / "index" / "weights.json"
EMPTY = {"version": "1.0", "files": {}}
LAMBDA = math.log(2) / 7.0  # 7天半衰期
GAIN, MAX_W, BASE_W = 0.05, 1.0, 0.10


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def days_since(iso: str) -> float:
    try:
        t = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - t).total_seconds() / 86400.0
    except Exception:
        return 0.0


def load() -> dict:
    if LEARN_FILE.exists():
        try:
            return json.loads(LEARN_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return EMPTY


def save(d):
    LEARN_FILE.parent.mkdir(parents=True, exist_ok=True)
    LEARN_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


class BehaviorLearner:
    def __init__(self):
        self.data = load()

    def learn(self, file_id: str, user: str = "UID9622") -> dict:
        now = now_iso()
        f = self.data["files"].get(file_id, {"weight": BASE_W, "count": 0, "last_access": None, "users": []})
        if f["last_access"]:
            f["weight"] *= math.exp(-LAMBDA * days_since(f["last_access"]))
        f["weight"] = min(MAX_W, f["weight"] + GAIN)
        f["count"] += 1
        f["last_access"] = now
        if user not in f["users"]:
            f["users"].append(user)
        self.data["files"][file_id] = f
        save(self.data)
        return {"file_id": file_id, "weight": round(f["weight"], 3), "count": f["count"]}

    def decay_all(self, days: float = 30.0) -> int:
        for fid, f in self.data["files"].items():
            if f.get("last_access"):
                f["weight"] = round(f["weight"] * math.exp(-LAMBDA * days_since(f["last_access"])), 4)
        save(self.data)
        return len(self.data["files"])

    def rank(self, top_k: int = 10) -> list:
        scored = sorted(((f["weight"], fid, f["count"]) for fid, f in self.data["files"].items()), key=lambda x: -x[0])
        return [{"weight": round(w, 3), "file_id": fid, "count": c} for w, fid, c in scored[:top_k]]

    def status(self) -> dict:
        fs = self.data["files"]
        return {"total": len(fs), "hot": sum(1 for f in fs.values() if f["weight"] > 0.5), "cold": sum(1 for f in fs.values() if f["weight"] < 0.2)}


def main():
    ap = argparse.ArgumentParser(description="龍魂动态加权引擎")
    ap.add_argument("cmd", choices=["learn", "decay", "rank", "status"])
    ap.add_argument("arg", nargs="?", default="")
    ap.add_argument("--user", default="UID9622")
    ap.add_argument("--days", type=float, default=30.0)
    ap.add_argument("--top", type=int, default=10)
    args = ap.parse_args()
    bl = BehaviorLearner()
    if args.cmd == "learn":
        r = bl.learn(args.arg, args.user)
        print(f"📈 已学习 {r['file_id']} · weight={r['weight']} · count={r['count']}")
    elif args.cmd == "decay":
        n = bl.decay_all(args.days)
        print(f"⏳ 已衰减 {n} 个文件权重")
    elif args.cmd == "rank":
        for i, r in enumerate(bl.rank(args.top), 1):
            print(f"#{i} [{r['weight']}] {r['file_id']} (访问{r['count']}次)")
    elif args.cmd == "status":
        s = bl.status()
        print(f"📊 共 {s['total']} 个 · 热 {s['hot']} · 冷 {s['cold']}")


if __name__ == "__main__":
    main()
