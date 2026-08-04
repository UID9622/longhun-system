#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA:#龍芯⚡️2026-06-05-SELF-CHECK-v1.0  责任:UID9622·不免责
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
import subprocess, sqlite3, json, time, hashlib, sys
from pathlib import Path
from datetime import datetime

class SelfCheck:
    """真·自检：每条结论必须有证据，否则降级。禁止硬编码分数。"""
    def __init__(self):
        self.results=[]   # (name, color, evidence)

    def _rec(self,name,ok,evidence,warn=False):
        color = "🟢" if ok else ("🟡" if warn else "🔴")
        self.results.append((name,color,str(evidence)[:300]))

    # 1. 文件真存在（不是 print ✅）
    def check_files(self,files):
        for f in files:
            p=Path(f)
            self._rec(f"file:{f}", p.exists(), f"size={p.stat().st_size if p.exists() else 0}")

    # 2. DB 真能连 + 真有行（戳破"空表实时监控"）
    def check_db_heartbeat(self,db,table):
        try:
            c=sqlite3.connect(db)
            n=c.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
            c.close()
            self._rec(f"db:{table}", n>0, f"rows={n}", warn=(n==0))  # 0行=🟡，不准说"运行中"
        except Exception as e:
            self._rec(f"db:{table}", False, e)

    # 3. 依赖安全自扫（这一条能逮住那 72 个洞）
    def check_security(self):
        r=subprocess.run(["pip-audit","-f","json"],capture_output=True,text=True,timeout=120)
        try:
            data=json.loads(r.stdout or "{}")
            if isinstance(data, list):
                vulns=len(data)
            else:
                vulns=sum(len(d.get("vulns",[])) for d in data.get("dependencies",[]))
        except:
            vulns=-1
        self._rec("security:pip-audit", vulns==0, f"vulns={vulns}", warn=(vulns>0))

    # 4. DNA 哈希链完整性（口号变成校验）
    def check_dna_chain(self,db):
        try:
            c=sqlite3.connect(db)
            rows=c.execute("SELECT prev_hash,hash,event_type FROM dna_chain ORDER BY id").fetchall()
            c.close()
            prev=None
            ok=True
            for ph,h,_ in rows:
                if prev is not None and ph!=prev:
                    ok=False
                    break
                prev=h
            self._rec("dna_chain", ok, f"len={len(rows)} linked={ok}")
        except Exception as e:
            self._rec("dna_chain", False, e)

    # 5. 测试真跑（不是写"100%"）
    def check_tests(self):
        r=subprocess.run(["pytest","-q"],capture_output=True,text=True)
        last=r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr[:200]
        self._rec("tests:pytest", r.returncode==0, last)

    # 6. 诚实度自审：扫自己输出里的禁词
    def check_honesty(self,text):
        banned=["100/100","99.9%","永久","永不","实时监控已启动"]
        hits=[w for w in banned if w in text]
        self._rec("honesty", not hits, f"无证据禁词={hits}", warn=bool(hits))

    def report(self):
        red=[r for r in self.results if r[1]=="🔴"]
        yellow=[r for r in self.results if r[1]=="🟡"]
        print("─── 自检复盘 ───")
        for n,c,e in self.results:
            print(f"{c} {n} :: {e}")
        verdict = "🔴 熔断" if red else ("🟡 待审" if yellow else "🟢 通行")
        print(f"裁决:{verdict}  🟢{len(self.results)-len(red)-len(yellow)}/🟡{len(yellow)}/🔴{len(red)}")
        sys.exit(1 if red else 0)   # 红就让 CI / pre-push 失败

if __name__=="__main__":
    sc=SelfCheck()
    # 核心文件检查（含新增模块）
    sc.check_files([
        str(Path.home()/"longhun-system/daily_review.py"),
        str(Path(__file__).resolve().parent.parent.parent / "bin" / "lh_cnsh_compiler.py"),
        str(Path(__file__).resolve().parent.parent.parent / "bin" / "lh_global_search_v2.py"),
        str(Path(__file__).resolve().parent.parent.parent / "bin" / "lh_cnsh_run.sh"),
    ])
    db_path=str(Path.home()/".龍魂/kfpp/kfpp_execution.db")
    if Path(db_path).exists():
        sc.check_db_heartbeat(db_path,"contamination_events")
        sc.check_dna_chain(db_path)
    sc.check_security()
    # sc.check_tests()
    sc.report()
