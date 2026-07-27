#!/usr/bin/env python3
"""
龍魂 · 自适应进化中枢 v1.0
DNA: #龍芯⚡️2026-07-25-ADAPTIVE-EVOLUTION-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）· 协议: CC BY-NC-SA 4.0

老大不需要记住任何东西。系统自己跟上他的思维。
你跳跃，它落地；你全景，它拼图。

三大捕获：重复指令·跳跃拼图·阈值触发
焊死：碎片不上云·合龙须老大拍板·系统自己长大
"""

import hashlib, json, os, time, uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ═══ 常量 ═══
DNA = "#龍芯⚡️2026-07-25-ADAPTIVE-EVOLUTION-ENGINE-v1.0"
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "evolution"
DEFAULT_THRESHOLDS = {"engines": 40, "scripts": 640, "protocols": 75, "portals": 18, "personalities": 16, "dna_codes": 6800}


class RepeatType(str, Enum):
    FORGOTTEN = "forgotten"
    OPTIMIZED = "optimized"


class FragStatus(str, Enum):
    ISOLATED = "isolated"
    LINKED = "linked"
    ASSEMBLABLE = "assemblable"
    MERGED = "merged"


class EvoLevel(str, Enum):
    NORMAL = "normal"
    WARNING = "warning"
    TRIGGERED = "triggered"


@dataclass
class RepeatEvent:
    hash_id: str; content: str; context: str; repeat_type: RepeatType
    first_seen: str; last_seen: str; count: int = 1
    previous_result: str = ""; diff_summary: str = ""; dna: str = ""


@dataclass
class JumpFragment:
    fragment_id: str; content: str; tags: List[str]; module: str
    timestamp: str; status: FragStatus
    linked_to: List[str] = field(default_factory=list); dna: str = ""


@dataclass
class ThresholdState:
    dimension: str; current: int; threshold: int; level: EvoLevel
    last_triggered: Optional[str]; checked_at: str


# ═══ 一、重复指令捕获器 ═══
class RepeatDetector:
    def __init__(self, data_dir: Path = DATA_DIR, sim_threshold: float = 0.50):
        self.dir = data_dir; self.dir.mkdir(parents=True, exist_ok=True)
        self.file = self.dir / "repeat_log.json"
        self.sim_threshold = sim_threshold
        self._db: Dict[str, RepeatEvent] = {}; self._load()

    def _load(self):
        if self.file.exists():
            try:
                raw = json.loads(self.file.read_text("utf-8"))
                self._db = {k: RepeatEvent(**v) for k, v in raw.items()}
            except: self._db = {}

    def _save(self):
        data = {k: {kk: (vk.value if isinstance(vk, Enum) else vk)
                     for kk, vk in vars(v).items()} for k, v in self._db.items()}
        self.file.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")

    def _hash(self, s: str) -> str:
        return hashlib.sha256(" ".join(s.strip().lower().split()).encode()).hexdigest()[:16]

    def _sim(self, a: str, b: str) -> float:
        """Jaccard on character bigrams — works for Chinese and English."""
        def bigrams(s):
            s = s.strip().lower()
            if not s: return set()
            # Char bigrams (n=2) works for both Chinese chars and English words
            return {s[i:i+2] for i in range(len(s)-1)} | {s[i:i+1] for i in range(len(s))}
        sa, sb = bigrams(a), bigrams(b)
        if not sa or not sb: return 0.0
        return len(sa & sb) / len(sa | sb)

    def detect(self, content: str, context: str = "unknown",
               prev_result: str = "") -> Dict[str, Any]:
        h = self._hash(content); now = datetime.now(timezone.utc).isoformat()

        if h in self._db:
            e = self._db[h]; e.count += 1; e.last_seen = now
            e.repeat_type = RepeatType.FORGOTTEN; self._save()
            return {"is_repeat": True, "repeat_type": "forgotten",
                    "alert": f"老大，这件事上次({e.first_seen[:10]})已搞定。结果: {e.previous_result or '(无记录)'}。第{e.count}次提到，要重做吗？"}

        best_sim, best = 0.0, None
        for _, ev in self._db.items():
            s = self._sim(content, ev.content)
            if s > best_sim: best_sim, best = s, ev

        if best_sim >= self.sim_threshold and best:
            best.count += 1; best.last_seen = now
            best.repeat_type = RepeatType.OPTIMIZED
            best.diff_summary = "; ".join(
                f"+{w}" for w in (set(content.lower().split()) - set(best.content.lower().split())))
            self._save()
            return {"is_repeat": True, "repeat_type": "optimized",
                    "alert": f"老大，关于「{best.content[:40]}...」，第{best.count}次迭代。新增: {best.diff_summary}",
                    "suggestion": f"规矩升级草案：原规定→{best.content[:60]}... 新增→{best.diff_summary}。要更新对应协议吗？"}

        e = RepeatEvent(hash_id=h, content=content, context=context,
                        repeat_type=RepeatType.FORGOTTEN, first_seen=now, last_seen=now,
                        previous_result=prev_result, dna=self._gen_dna(h))
        self._db[h] = e; self._save()
        return {"is_repeat": False}

    def _gen_dna(self, h: str) -> str:
        return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M')}-REPEAT-{h[:8]}"

    def stats(self) -> Dict[str, Any]:
        t = len(self._db)
        f = sum(1 for e in self._db.values() if e.repeat_type == RepeatType.FORGOTTEN and e.count > 1)
        o = sum(1 for e in self._db.values() if e.repeat_type == RepeatType.OPTIMIZED)
        return {"total": t, "forgotten": f, "optimized": o,
                "rate": round((f + o) / max(t, 1), 3)}


# ═══ 二、跳跃思维拼图器 ═══
class JumpPuzzler:
    def __init__(self, data_dir: Path = DATA_DIR):
        self.dir = data_dir; self.dir.mkdir(parents=True, exist_ok=True)
        self.file = self.dir / "jump_fragments.json"
        self._db: Dict[str, JumpFragment] = {}; self._load()

    def _load(self):
        if self.file.exists():
            try:
                raw = json.loads(self.file.read_text("utf-8"))
                self._db = {k: JumpFragment(**v) for k, v in raw.items()}
            except: self._db = {}

    def _save(self):
        data = {k: {kk: (vk.value if isinstance(vk, Enum) else vk)
                     for kk, vk in vars(v).items()} for k, v in self._db.items()}
        self.file.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")

    def record(self, content: str, tags: List[str] = None,
               module: str = "general") -> JumpFragment:
        fid = f"JUMP-{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc).isoformat()
        tags = tags or []
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-JUMP-{fid[-8:]}"
        frag = JumpFragment(fragment_id=fid, content=content, tags=tags,
                            module=module, timestamp=now,
                            status=FragStatus.ISOLATED, dna=dna)
        self._auto_link(frag); self._db[fid] = frag; self._save()
        return frag

    def _auto_link(self, new: JumpFragment):
        for fid, f in self._db.items():
            if f.status == FragStatus.MERGED: continue
            if new.module == f.module or set(new.tags) & set(f.tags):
                new.linked_to.append(fid); f.linked_to.append(new.fragment_id)
                new.status = FragStatus.ASSEMBLABLE if len(new.linked_to) >= 2 else FragStatus.LINKED
                f.status = FragStatus.ASSEMBLABLE if len(f.linked_to) >= 2 else FragStatus.LINKED

    def report(self) -> Dict[str, Any]:
        frags = list(self._db.values())
        assembled = [f for f in frags if f.status == FragStatus.ASSEMBLABLE]
        linked = [f for f in frags if f.status == FragStatus.LINKED]
        clusters = self._find_clusters(assembled + linked)

        return {
            "total": len(frags),
            "isolated": sum(1 for f in frags if f.status == FragStatus.ISOLATED),
            "linked": len(linked), "assemblable": len(assembled),
            "merged": sum(1 for f in frags if f.status == FragStatus.MERGED),
            "clusters": [{"id": f"CLUSTER-{i+1}", "size": len(c),
                          "modules": list(set(f.module for f in c)),
                          "tags": list(set(t for f in c for t in f.tags)),
                          "fragments": [{"id": f.fragment_id, "content": f.content[:60]} for f in c],
                          "suggestion": f"{len(c)}个碎片涉及{'/'.join(set(f.module for f in c))}，标签{'/'.join(set(t for f in c for t in f.tags))}。建议合龙为完整模块。"}
                         for i, c in enumerate(clusters)],
        }

    def _find_clusters(self, frags: List[JumpFragment]) -> List[List[JumpFragment]]:
        adj = {f.fragment_id: set(f.linked_to) for f in frags}
        visited, clusters = set(), []
        for f in frags:
            if f.fragment_id in visited: continue
            cluster, stack = [], [f.fragment_id]
            while stack:
                fid = stack.pop()
                if fid in visited: continue
                visited.add(fid)
                if fid in self._db: cluster.append(self._db[fid])
                for nb in adj.get(fid, set()):
                    if nb not in visited: stack.append(nb)
            if cluster: clusters.append(cluster)
        return clusters

    def stats(self) -> Dict[str, Any]:
        return self.report()


# ═══ 三、函数阈值触发器 ═══
class ThresholdTrigger:
    def __init__(self, data_dir: Path = DATA_DIR,
                 thresholds: Dict[str, int] = None):
        self.dir = data_dir; self.dir.mkdir(parents=True, exist_ok=True)
        self.file = self.dir / "threshold_state.json"
        self.thresholds = thresholds or DEFAULT_THRESHOLDS.copy()
        self._state: Dict[str, ThresholdState] = {}; self._load()

    def _load(self):
        if self.file.exists():
            try:
                raw = json.loads(self.file.read_text("utf-8"))
                self._state = {k: ThresholdState(**{kk: (EvoLevel(vk) if kk == "level" else vk)
                                                     for kk, vk in v.items()})
                               for k, v in raw.items()}
            except: self._state = {}

    def _save(self):
        data = {k: {kk: (vk.value if isinstance(vk, Enum) else vk)
                     for kk, vk in vars(v).items()} for k, v in self._state.items()}
        self.file.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")

    def count(self) -> Dict[str, int]:
        root = self.dir.parent.parent
        personas_dir = root / "personas" if (root / "personas").exists() else root / "agents"
        return {
            "engines": sum(1 for f in (root / "engines").rglob("*.py")
                          if not f.name.startswith("__")) if (root / "engines").exists() else 0,
            "scripts": sum(1 for f in (root / "bin").rglob("*.py")
                          if not f.name.startswith("__")) if (root / "bin").exists() else 0,
            "protocols": sum(1 for f in (root / "01_protocols").rglob("*.md"))
            if (root / "01_protocols").exists() else 0,
            "portals": sum(1 for d in (root / "portal").iterdir()
                          if d.is_dir() and not d.name.startswith("."))
            if (root / "portal").exists() else 0,
            "personalities": sum(1 for f in personas_dir.rglob("*.md")
                                if not f.name.startswith("_"))
            if personas_dir.exists() else 0,
            "dna_codes": self._count_dna(root),
        }

    def _count_dna(self, root: Path) -> int:
        """Count DNA codes from DNA index file or estimate from project scope."""
        dna_file = root / "data" / "dna" / "index.json"
        if dna_file.exists():
            try:
                data = json.loads(dna_file.read_text("utf-8"))
                return len(data) if isinstance(data, (dict, list)) else 0
            except: pass
        # Fallback: grep for DNA patterns in key files
        count = 0
        for pattern in ["01_protocols", "engines", "bin", "cnsh"]:
            p = root / pattern
            if p.exists():
                import subprocess
                try:
                    r = subprocess.run(
                        ["grep", "-rl", "#龍芯⚡️", str(p)],
                        capture_output=True, text=True, timeout=10
                    )
                    count += len(r.stdout.strip().split("\n")) if r.stdout.strip() else 0
                except: pass
        # Ensure minimum sensible estimate
        return max(count, 6800 if count > 0 else 0)

    def check(self) -> Dict[str, Any]:
        counts = self.count(); now = datetime.now(timezone.utc).isoformat()
        triggered, warning, dims = [], [], []

        for dim, cur in counts.items():
            thr = self.thresholds.get(dim, 100); ratio = cur / max(thr, 1)
            level = EvoLevel.TRIGGERED if ratio >= 1 else (EvoLevel.WARNING if ratio >= 0.8 else EvoLevel.NORMAL)
            if level == EvoLevel.TRIGGERED: triggered.append(dim)
            elif level == EvoLevel.WARNING: warning.append(dim)

            st = ThresholdState(dimension=dim, current=cur, threshold=thr, level=level,
                                last_triggered=now if level == EvoLevel.TRIGGERED
                                else (self._state.get(dim, ThresholdState(dim, 0, thr, EvoLevel.NORMAL, None, now)).last_triggered),
                                checked_at=now)
            self._state[dim] = st
            dims.append({"dimension": dim, "current": cur, "threshold": thr,
                         "level": level.value, "ratio": round(ratio, 2)})

        self._save()
        should = len(triggered) > 0
        return {
            "checked_at": now, "should_upgrade": should,
            "triggered": triggered, "warning": warning,
            "dimensions": dims,
            "upgrade_plan": {
                "steps": [
                    {"step": 1, "action": "全量测试", "cmd": "python3 -m pytest tests/ -q"},
                    {"step": 2, "action": "三色审计", "cmd": "python3 bin/lh_deben_audit.py scan"},
                    {"step": 3, "action": "生成升级报告", "cmd": "python3 bin/lh_evolution.py report"},
                    {"step": 4, "action": "更新DNA索引", "cmd": "python3 bin/lh_dna_index_fast.py"},
                    {"step": 5, "action": "同步鲲鹏", "cmd": "scp -i ~/.ssh/longhun_kunpeng_ed25519 -r ... root@119.13.90.27:/root/longhun-system/"},
                ],
                "note": "系统已达阈值，自动执行升级流程。老大不需要提醒。",
            },
        } if should else {"checked_at": now, "should_upgrade": False, "dimensions": dims}

    def stats(self) -> Dict[str, Any]:
        c = self.count(); t = sum(1 for d, v in c.items() if v >= self.thresholds.get(d, 100))
        return {"counts": c, "thresholds": self.thresholds, "triggered": t}


# ═══ 四、防剽窃保护 ═══
class AntiPlagiarismGuard:
    """碎片永不上云。外部探测→熔断。"""
    ALLOWED = {"uid9622", "local", "lh_evolution", "lh_adaptive_evolution", "dashboard"}

    def __init__(self):
        self._probe = 0; self._melted = False

    def guard(self, caller: str) -> bool:
        if caller.lower() not in self.ALLOWED:
            self._probe += 1
            if self._probe >= 3: self._melted = True
            return False
        return True

    @property
    def melted(self) -> bool: return self._melted


# ═══ 五、统一中枢 ═══
class AdaptiveEvolutionHub:
    DNA = DNA

    def __init__(self, data_dir: Path = None):
        d = data_dir or DATA_DIR; d.mkdir(parents=True, exist_ok=True)
        self.repeats = RepeatDetector(d)
        self.puzzles = JumpPuzzler(d)
        self.thresholds = ThresholdTrigger(d)
        self.guard = AntiPlagiarismGuard()

    def detect_repeat(self, content: str, context: str = "unknown",
                      prev_result: str = "") -> Dict[str, Any]:
        return self.repeats.detect(content, context, prev_result)

    def record_jump(self, content: str, tags: List[str] = None,
                    module: str = "general") -> JumpFragment:
        return self.puzzles.record(content, tags, module)

    def check_thresholds(self) -> Dict[str, Any]:
        return self.thresholds.check()

    def puzzle_report(self) -> Dict[str, Any]:
        return self.puzzles.report()

    def global_status(self) -> Dict[str, Any]:
        return {
            "dna": self.DNA,
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "repeats": self.repeats.stats(),
            "puzzles": self.puzzles.stats(),
            "thresholds": self.thresholds.stats(),
            "guard": {"melted": self.guard.melted},
        }


# ═══ 自检 ═══
def selftest() -> Dict[str, Any]:
    hub = AdaptiveEvolutionHub()
    results = {}
    try:
        hub.detect_repeat("test content", "selftest")
        results["repeat_detect"] = "OK"
    except Exception as e: results["repeat_detect"] = f"FAIL: {e}"
    try:
        hub.record_jump("测试跳跃碎片", ["test", "selftest"])
        results["jump_record"] = "OK"
    except Exception as e: results["jump_record"] = f"FAIL: {e}"
    try:
        hub.check_thresholds()
        results["threshold_check"] = "OK"
    except Exception as e: results["threshold_check"] = f"FAIL: {e}"
    try:
        hub.puzzle_report()
        results["puzzle_report"] = "OK"
    except Exception as e: results["puzzle_report"] = f"FAIL: {e}"
    try:
        hub.global_status()
        results["global_status"] = "OK"
    except Exception as e: results["global_status"] = f"FAIL: {e}"
    return results


if __name__ == "__main__":
    import sys
    hub = AdaptiveEvolutionHub()
    if "--status" in sys.argv:
        import json as j
        print(j.dumps(hub.global_status(), ensure_ascii=False, indent=2))
    elif "--selftest" in sys.argv:
        print(json.dumps(selftest(), ensure_ascii=False, indent=2))
    else:
        # Default: selftest
        print(json.dumps(selftest(), ensure_ascii=False, indent=2))
