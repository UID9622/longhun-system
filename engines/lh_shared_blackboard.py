# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-SHARED-BLACKBOARD-v1.0"""
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""龍魂 SharedBlackboard v1.0 — 多智能体共享上下文黑板
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-SHARED-BLACKBOARD-v1.0"""
import json, threading, time, uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum

class EntryType(Enum):
    VARIABLE="variable"; FACT="fact"; DECISION="decision"; TASK="task"; ALERT="alert"

class Visibility(Enum):
    ALL="all"; LAYER="layer"; GROUP="group"; PRIVATE="private"

@dataclass
class Entry:
    eid: str; key: str; value: Any; etype: EntryType; writer: str
    visibility: Visibility=Visibility.ALL; visible_to: Set[str]=field(default_factory=set)
    ts: str=field(default_factory=lambda: datetime.now().isoformat())
    ttl: Optional[int]=None; version: int=0; meta: Dict[str, Any] =field(default_factory=dict)
    def expired(self) -> bool:
        if self.ttl is None: return False
        return datetime.now() > datetime.fromisoformat(self.ts)+timedelta(seconds=self.ttl)
    def can_read(self, pid: str, layer: str="") -> bool:
        if self.visibility==Visibility.ALL: return True
        if self.visibility==Visibility.PRIVATE: return pid==self.writer
        if self.visibility==Visibility.GROUP: return pid in self.visible_to
        if self.visibility==Visibility.LAYER: return layer==self.meta.get("layer","")
        return False

class SharedBlackboard:
    """线程安全多智能体共享黑板"""
    MAX = 10000
    def __init__(self):
        self._e: Dict[str,Entry] = {}
        self._idx: Dict[str,List[str]] = {}
        self._lk = threading.RLock()
        self._obs: Dict[str,List] = {}
        self._st = {"w":0,"r":0,"err":0,"cln":0}
        threading.Thread(target=self._loop, daemon=True).start()
    def _loop(self):
        while True: time.sleep(300); self.cleanup()
    def cleanup(self) -> int:
        with self._lk:
            ex = [eid for eid,e in self._e.items() if e.expired()]
            for eid in ex: del self._e[eid]
            self._st["cln"] += len(ex)
        return len(ex)
    def _evict(self, n=100):
        s = sorted(self._e.keys(),key=lambda k:self._e[k].ts)
        for eid in s[:n]: del self._e[eid]
    def _notify(self,k,entry):
        for cb in self._obs.get(k,[]):
            try: cb(entry)
            except: self._st["err"]+=1
    def put(self,key,value,writer,etype=EntryType.FACT,visibility=Visibility.ALL,
            visible_to=None,ttl=None,meta=None) -> str:
        with self._lk:
            if len(self._e)>=self.MAX: self._evict(100)
            eid=uuid.uuid4().hex[:16]; ver=len(self._idx.get(key,[]))
            e=Entry(eid=eid,key=key,value=value,etype=etype,writer=writer,
                    visibility=visibility,visible_to=visible_to or set(),
                    ttl=ttl,version=ver,meta=meta or {})
            self._e[eid]=e; self._idx.setdefault(key,[]).append(eid)
            self._st["w"]+=1; self._notify(key,e); return eid
    def update(self,key,value,writer) -> str:
        return self.put(key,value,writer,EntryType.VARIABLE)
    def decide(self,key,decision,writer,reason="") -> str:
        return self.put(key,decision,writer,EntryType.DECISION,meta={"reason":reason})
    def announce(self,key,value,writer,ttl=3600) -> str:
        return self.put(key,value,writer,EntryType.ALERT,ttl=ttl)
    def get(self,key,pid="system",layer="") -> Optional[Any]:
        with self._lk:
            eids=self._idx.get(key,[])
            for eid in reversed(eids):
                e=self._e.get(eid)
                if e and not e.expired() and e.can_read(pid,layer):
                    self._st["r"]+=1; return e.value
            return None
    def get_all(self,key,pid="system",layer="") -> List[Any]:
        with self._lk:
            eids=self._idx.get(key,[]); r=[]
            for eid in eids:
                e=self._e.get(eid)
                if e and not e.expired() and e.can_read(pid,layer):
                    r.append({"value":e.value,"version":e.version,"writer":e.writer,"ts":e.ts})
            self._st["r"]+=len(r); return r
    def watch(self,key,callback):
        self._obs.setdefault(key,[]).append(callback)
    def unwatch(self,key,callback):
        if key in self._obs: self._obs[key]=[c for c in self._obs[key] if c!=callback]
    def query(self,etype:EntryType=None,writer:str=None,pattern:str=None) -> List[Dict]:
        with self._lk:
            r=[]
            for eid,e in self._e.items():
                if e.expired(): continue
                if etype and e.etype!=etype: continue
                if writer and e.writer!=writer: continue
                if pattern and pattern not in e.key: continue
                r.append({"eid":e.eid,"key":e.key,"value":e.value,
                          "etype":e.etype.value,"writer":e.writer,"ts":e.ts,"version":e.version})
            return r
    def delete(self,eid,writer="system") -> bool:
        with self._lk:
            if eid in self._e: del self._e[eid]; return True
            return False
    def delete_key(self,key,writer="system") -> int:
        with self._lk:
            eids=self._idx.pop(key,[]); n=0
            for eid in eids:
                if eid in self._e: del self._e[eid]; n+=1
            return n
    def clear(self):
        with self._lk: self._e.clear(); self._idx.clear()
    @property
    def stats(self): return dict(self._st)
    @property
    def size(self): return len(self._e)
    @property
    def keys(self) -> List[str]: return list(self._idx.keys())

# 全局单例
_bb: Optional[SharedBlackboard] = None
_bb_lock = threading.Lock()

def get_blackboard() -> SharedBlackboard:
    global _bb
    with _bb_lock:
        if _bb is None: _bb = SharedBlackboard()
        return _bb

# ── 自检 ──
if __name__ == "__main__":
    print("="*50)
    print("龍魂 SharedBlackboard v1.0 自检")
    print("="*50)
    bb = SharedBlackboard()
    # 写入测试
    eid = bb.put("test.key", {"msg":"hello"}, "P00")
    print(f"✅ 写入: {eid}")
    # 读取测试
    val = bb.get("test.key", "P00")
    print(f"✅ 读取: {val}")
    # 更新测试
    bb.update("test.key", {"msg":"updated"}, "P01")
    vals = bb.get_all("test.key")
    print(f"✅ 版本链({len(vals)}版本): {[v['version'] for v in vals]}")
    # 查询测试
    bb.put("test.fact", "some fact", "P05", EntryType.FACT)
    facts = bb.query(etype=EntryType.FACT)
    print(f"✅ 查询 FACT: {len(facts)}条")
    # 清理测试
    bb.put("expire.key", "will die", "P00", ttl=1)
    time.sleep(2)
    assert bb.get("expire.key") is None, "TTL应已过期"
    print("✅ TTL过期清理正常")
    print(f"\n统计: {bb.stats}")
    print("自检全部通过 ✅")
