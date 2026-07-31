#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·量子卦象引擎 v2.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-量子卦象-v2.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 64卦象 -> 6量子比特希尔伯特空间 (Bra-Ket)
  2. CNSH编译器集成 (执行.cnsh卦象分析脚本)
  3. SQLite持久化 (用户·会话·历史·审计)
  4. FastAPI Web接口 (RESTful + Swagger文档)
  5. 可调耦合哈密顿量 (chain/all-to-all/cluster拓扑)
  6. 多量子比特纠缠 (Bell态/GHZ态/W态)
  7. 易经卦象关系 (互卦·变卦·错卦·综卦)
  8. JWT认证 (登录·注册·受保护路由)
"""

import os, sys, json, sqlite3, hashlib, subprocess
import numpy as np
from scipy.linalg import expm
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from fastapi import FastAPI, HTTPException, Query, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import uvicorn
import argparse
import jwt
from jwt import PyJWTError
from passlib.context import CryptContext

# ============================================================
# 一、64卦象量子态定义
# ============================================================

HEXAGRAM_NAMES = [
    "乾", "坤", "屯", "蒙", "需", "讼", "师", "比", "小畜", "履",
    "泰", "否", "同人", "大有", "谦", "豫", "随", "蛊", "临", "观",
    "噬嗑", "贲", "剥", "复", "无妄", "大畜", "颐", "大过", "坎", "离",
    "咸", "恒", "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解",
    "损", "益", "夬", "姤", "萃", "升", "困", "井", "革", "鼎",
    "震", "艮", "渐", "归妹", "丰", "旅", "巽", "兑", "涣", "节",
    "中孚", "小过", "既济", "未济",
]

HEXAGRAM_UNICODE = [
    "䷀","䷁","䷂","䷃","䷄","䷅","䷆","䷇","䷈","䷉",
    "䷊","䷋","䷌","䷍","䷎","䷏","䷐","䷑","䷒","䷓",
    "䷔","䷕","䷖","䷗","䷘","䷙","䷚","䷛","䷜","䷝",
    "䷞","䷟","䷠","䷡","䷢","䷣","䷤","䷥","䷦","䷧",
    "䷨","䷩","䷪","䷫","䷬","䷭","䷮","䷯","䷰","䷱",
    "䷲","䷳","䷴","䷵","䷶","䷷","䷸","䷹","䷺","䷻",
    "䷼","䷽","䷾","䷿",
]

HEXAGRAM_DESCRIPTIONS = {
    0:  "乾为天·元亨利贞·天行健，君子以自强不息",
    1:  "坤为地·元亨·地势坤，君子以厚德载物",
    2:  "水雷屯·刚柔始交而难生·动乎险中",
    3:  "山水蒙·山下有险·险而止",
    4:  "水天需·险在前也·刚健而不陷",
    5:  "天水讼·天与水违行",
    6:  "地水师·地中有水·师，众也",
    7:  "水地比·地上有水·先王以建万国亲诸侯",
    62: "水火既济·水在火上·既济亨小",
    63: "火水未济·火在水上·未济亨",
}
for i in range(64):
    if i not in HEXAGRAM_DESCRIPTIONS:
        HEXAGRAM_DESCRIPTIONS[i] = f"{HEXAGRAM_NAMES[i]}{HEXAGRAM_UNICODE[i]}"


# ============================================================
# 二、易经卦象关系函数
# ============================================================

def hexagram_complement(index: int) -> int:
    """错卦：六爻全变（阴阳互换）"""
    b = format(index, '06b')
    return int(''.join('1' if c == '0' else '0' for c in b), 2)

def hexagram_reverse(index: int) -> int:
    """综卦：上下颠倒"""
    return int(format(index, '06b')[::-1], 2)

def hexagram_interlock(index: int) -> int:
    """互卦：二三四爻为下卦·三四五爻为上卦"""
    b = format(index, '06b')
    return int(b[2:5] + b[1:4], 2)

def hexagram_change(index: int, line_idx: int) -> int:
    """变爻：指定爻位变阴阳 (0=初爻, 5=上爻)"""
    lst = list(format(index, '06b'))
    lst[line_idx] = '1' if lst[line_idx] == '0' else '0'
    return int(''.join(lst), 2)

def hexagram_relation(index: int) -> Dict:
    """获取卦象的完整关系"""
    def fmt(i): return f"{HEXAGRAM_NAMES[i]}{HEXAGRAM_UNICODE[i]}"
    return {
        "index": index,
        "本卦": fmt(index),
        "binary": format(index, '06b'),
        "错卦": fmt(hexagram_complement(index)),
        "综卦": fmt(hexagram_reverse(index)),
        "互卦": fmt(hexagram_interlock(index)),
        "变卦_初爻": fmt(hexagram_change(index, 0)),
        "变卦_上爻": fmt(hexagram_change(index, 5)),
        "卦辞": HEXAGRAM_DESCRIPTIONS.get(index, ""),
    }


# ============================================================
# 三、量子引擎
# ============================================================

class QuantumEngine:
    """64维希尔伯特空间量子操作引擎"""
    DIM = 64

    @staticmethod
    def ket(index: int) -> np.ndarray:
        if not 0 <= index < QuantumEngine.DIM:
            raise ValueError(f"索引 {index} 超出 0-{QuantumEngine.DIM-1}")
        state = np.zeros(QuantumEngine.DIM, dtype=complex)
        state[index] = 1.0
        return state

    @staticmethod
    def superposition(amplitudes: np.ndarray) -> np.ndarray:
        if len(amplitudes) != QuantumEngine.DIM:
            raise ValueError(f"振幅数组长度必须为{QuantumEngine.DIM}")
        state = np.array(amplitudes, dtype=complex)
        norm = np.linalg.norm(state)
        return state / norm if norm > 0 else state

    @staticmethod
    def measure(state: np.ndarray) -> Tuple[int, float]:
        probs = np.abs(state) ** 2
        probs = probs / probs.sum()
        index = np.random.choice(QuantumEngine.DIM, p=probs)
        return int(index), float(probs[index])

    @staticmethod
    def evolve(state: np.ndarray, hamiltonian: np.ndarray, time: float) -> np.ndarray:
        U = expm(-1j * hamiltonian * time)
        new_state = U @ state
        norm = np.linalg.norm(new_state)
        return new_state / norm if norm > 0 else new_state

    @staticmethod
    def hamiltonian(topology: str = 'all-to-all', g: float = 0.1,
                    cluster_size: int = 4, seed: int = 42) -> np.ndarray:
        np.random.seed(seed)
        n = QuantumEngine.DIM
        H = np.diag(np.random.normal(0, g * 0.1, n))  # 对角项

        if topology == 'chain':
            for i in range(n - 1):
                H[i, i+1] = g; H[i+1, i] = g
        elif topology == 'all-to-all':
            for i in range(n):
                for j in range(i+1, n):
                    val = g * (0.8 + 0.4 * np.random.random())
                    H[i, j] = val; H[j, i] = val
        elif topology == 'cluster':
            for i in range(0, n, cluster_size):
                end = min(i + cluster_size, n)
                for a in range(i, end):
                    for bb in range(a+1, end):
                        H[a, bb] = g; H[bb, a] = g
        else:
            raise ValueError(f"未知拓扑: {topology}")
        return (H + H.conj().T) / 2

    @staticmethod
    def bell_state(a: int, b: int) -> np.ndarray:
        if a == b: b = (a + 1) % QuantumEngine.DIM
        state = np.zeros(QuantumEngine.DIM, dtype=complex)
        state[a] = 1.0 / np.sqrt(2)
        state[b] = 1.0 / np.sqrt(2)
        return state

    @staticmethod
    def ghz_state() -> np.ndarray:
        state = np.zeros(QuantumEngine.DIM, dtype=complex)
        state[0] = 1.0 / np.sqrt(2)
        state[63] = 1.0 / np.sqrt(2)
        return state

    @staticmethod
    def w_state() -> np.ndarray:
        state = np.zeros(QuantumEngine.DIM, dtype=complex)
        for i in range(6):
            state[1 << i] = 1.0 / np.sqrt(6)
        return state

    @staticmethod
    def uniform_superposition() -> np.ndarray:
        return np.ones(QuantumEngine.DIM, dtype=complex) / np.sqrt(QuantumEngine.DIM)

    @staticmethod
    def entropy(state: np.ndarray) -> float:
        probs = np.abs(state) ** 2
        probs = probs[probs > 1e-12]
        return float(-np.sum(probs * np.log(probs)))

    @staticmethod
    def top_hexagrams(state: np.ndarray, k: int = 5) -> List[Dict]:
        probs = np.abs(state) ** 2
        indices = np.argsort(probs)[::-1][:k]
        return [{"index": int(i), "name": f"{HEXAGRAM_NAMES[i]}{HEXAGRAM_UNICODE[i]}",
                 "probability": float(probs[i]), "binary": format(i, '06b')}
                for i in indices]


# ============================================================
# 四、CNSH编译器集成
# ============================================================

class CNSHCompiler:
    def __init__(self):
        self.base_dir = Path.home() / "longhun-system"
        self.compiler_py = self.base_dir / "bin" / "CNSH_执行器.py"
        self.cnsh_cli = self.base_dir / "bin" / "cnsh"
        self.available = self.compiler_py.exists() or self.cnsh_cli.exists()

    def execute(self, code: str, filename: str = "temp_q.cnsh") -> Dict:
        if not self.available:
            return {"status": "unavailable", "message": "CNSH编译器未找到"}
        tmp = Path("/tmp") / filename
        with open(tmp, 'w', encoding='utf-8') as f:
            f.write(code)
        try:
            if self.compiler_py.exists():
                cmd = [sys.executable, str(self.compiler_py), str(tmp)]
            else:
                cmd = [str(self.cnsh_cli), "run", str(tmp)]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=15,
                                 cwd=str(self.base_dir))
            return {"status": "success" if res.returncode == 0 else "error",
                    "stdout": res.stdout.strip(), "stderr": res.stderr.strip()}
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "超时(15s)"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            tmp.unlink(missing_ok=True)

    def analyze_hexagram(self, index: int) -> Dict:
        code = f"""导入 系统
功能 分析() {{
    idx = {index}
    打印("══ CNSH卦象分析: {HEXAGRAM_NAMES[index]} ══")
    打印("索引:", idx)
}}
分析()"""
        return self.execute(code, f"hexagram_{index}.cnsh")


# ============================================================
# 五、SQLite持久化
# ============================================================

class QuantumDB:
    def __init__(self, db_path: Path = None):
        self.db_path = db_path or (Path.home() / ".longhun" / "quantum.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _init(self):
        c = sqlite3.connect(str(self.db_path))
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("PRAGMA foreign_keys=ON")
        c.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                uid TEXT UNIQUE NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TEXT
            );
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                user_id INTEGER,
                state_vector TEXT,
                description TEXT,
                topology TEXT DEFAULT 'all-to-all',
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT, operation TEXT,
                params TEXT, result TEXT, dna TEXT,
                created_at TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            );
            CREATE TABLE IF NOT EXISTS audit (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT, action TEXT,
                color TEXT, detail TEXT,
                created_at TEXT
            );
        """)
        c.commit(); c.close()

    def get_user(self, username: str) -> Optional[Dict]:
        c = sqlite3.connect(str(self.db_path))
        row = c.execute("SELECT id,username,password_hash,uid,role FROM users WHERE username=?",
                        (username,)).fetchone()
        c.close()
        return {"id": row[0], "username": row[1], "password_hash": row[2],
                "uid": row[3], "role": row[4]} if row else None

    def create_user(self, username: str, pwd_hash: str, uid: str) -> int:
        c = sqlite3.connect(str(self.db_path))
        try:
            cur = c.execute("INSERT INTO users(username,password_hash,uid,created_at) VALUES(?,?,?,?)",
                            (username, pwd_hash, uid, datetime.now().isoformat()))
            c.commit(); return cur.lastrowid
        except sqlite3.IntegrityError:
            c.close(); raise ValueError(f"用户名 {username} 已存在")

    def save_session(self, sid: str, uid: int, state: np.ndarray,
                     desc: str = "", topo: str = "all-to-all") -> bool:
        c = sqlite3.connect(str(self.db_path))
        now = datetime.now().isoformat()
        try:
            c.execute("INSERT OR REPLACE INTO sessions VALUES(?,?,?,?,?,?,?,?)",
                      (None, sid, uid, json.dumps(state.tolist()), desc, topo, now, now))
            c.commit(); return True
        except Exception: return False
        finally: c.close()

    def get_session(self, sid: str) -> Optional[Dict]:
        c = sqlite3.connect(str(self.db_path))
        row = c.execute("SELECT session_id,user_id,state_vector,description,topology,created_at "
                        "FROM sessions WHERE session_id=?", (sid,)).fetchone()
        c.close()
        return {"session_id": row[0], "user_id": row[1],
                "state_vector": np.array(json.loads(row[2]), dtype=complex),
                "description": row[3], "topology": row[4], "created_at": row[5]} if row else None

    def update_state(self, sid: str, state: np.ndarray):
        c = sqlite3.connect(str(self.db_path))
        c.execute("UPDATE sessions SET state_vector=?,updated_at=? WHERE session_id=?",
                  (json.dumps(state.tolist()), datetime.now().isoformat(), sid))
        c.commit(); c.close()

    def list_sessions(self, uid: int, limit: int = 20) -> List[Dict]:
        c = sqlite3.connect(str(self.db_path))
        rows = c.execute("SELECT session_id,description,topology,created_at FROM sessions "
                         "WHERE user_id=? ORDER BY updated_at DESC LIMIT ?",
                         (uid, limit)).fetchall()
        c.close()
        return [{"session_id": r[0], "description": r[1], "topology": r[2], "created_at": r[3]}
                for r in rows]

    def add_history(self, sid: str, op: str, params: Dict, result: Dict, dna: str = ""):
        c = sqlite3.connect(str(self.db_path))
        c.execute("INSERT INTO history VALUES(?,?,?,?,?,?,?)",
                  (None, sid, op, json.dumps(params), json.dumps(result), dna,
                   datetime.now().isoformat()))
        c.commit(); c.close()

    def get_history(self, sid: str, limit: int = 20) -> List[Dict]:
        c = sqlite3.connect(str(self.db_path))
        rows = c.execute("SELECT operation,params,result,dna,created_at FROM history "
                         "WHERE session_id=? ORDER BY created_at DESC LIMIT ?",
                         (sid, limit)).fetchall()
        c.close()
        return [{"operation": r[0], "params": json.loads(r[1]) if r[1] else {},
                 "result": json.loads(r[2]) if r[2] else {}, "dna": r[3], "created_at": r[4]}
                for r in rows]

    def add_audit(self, sid: str, action: str, color: str, detail: str = ""):
        c = sqlite3.connect(str(self.db_path))
        c.execute("INSERT INTO audit VALUES(?,?,?,?,?,?)",
                  (None, sid, action, color, detail, datetime.now().isoformat()))
        c.commit(); c.close()

    def get_audit(self, sid: str, limit: int = 50) -> List[Dict]:
        c = sqlite3.connect(str(self.db_path))
        rows = c.execute("SELECT action,color,detail,created_at FROM audit "
                         "WHERE session_id=? ORDER BY created_at DESC LIMIT ?",
                         (sid, limit)).fetchall()
        c.close()
        return [{"action": r[0], "color": r[1], "detail": r[2], "created_at": r[3]}
                for r in rows]

    def stats(self) -> Dict:
        c = sqlite3.connect(str(self.db_path))
        u = c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        s = c.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        h = c.execute("SELECT COUNT(*) FROM history").fetchone()[0]
        a = c.execute("SELECT COUNT(*) FROM audit").fetchone()[0]
        c.close()
        return {"users": u, "sessions": s, "history": h, "audit_logs": a}


# ============================================================
# 六、JWT认证
# ============================================================

SECRET_KEY = os.environ.get("LH_JWT_SECRET", "龍魂量子引擎JWT-v2.0")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security_scheme = HTTPBearer()

def hash_pw(pw: str) -> str: return pwd_context.hash(pw)
def verify_pw(pw, h): return pwd_context.verify(pw, h)

def create_token(data: dict, expires: Optional[timedelta] = None) -> str:
    d = data.copy()
    d["exp"] = datetime.utcnow() + (expires or timedelta(minutes=60))
    d["type"] = "access"
    return jwt.encode(d, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Optional[Dict]:
    try: return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except PyJWTError: return None

async def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security_scheme)) -> Dict:
    payload = decode_token(creds.credentials)
    if not payload or payload.get("type") != "access":
        raise HTTPException(401, detail="无效或过期的token")
    user = QuantumDB().get_user(payload.get("sub", ""))
    if not user: raise HTTPException(401, detail="用户不存在")
    return user

def gen_dna(prefix: str, seed: str) -> str:
    return f"#量子⚡️{hashlib.sha256((prefix+seed+datetime.now().isoformat()).encode()).hexdigest()[:8]}"


# ============================================================
# 七、FastAPI应用
# ============================================================

app = FastAPI(title="龍魂·量子卦象引擎 API", version="2.0",
              description="64卦象·6量子比特希尔伯特空间·酉演化·CNSH·JWT认证",
              docs_url="/api/docs", redoc_url="/api/redoc")

db = QuantumDB()
qe = QuantumEngine()
cnsh = CNSHCompiler()

# ---- Pydantic Models ----

class LoginReq(BaseModel):
    username: str
    password: str

class SessionCreate(BaseModel):
    description: str = ""

class EvolveReq(BaseModel):
    session_id: str
    topology: str = "all-to-all"
    g: float = 0.1
    time: float = 1.0

class EntangleReq(BaseModel):
    session_id: str
    type: str = "bell"
    a: int = 0
    b: int = 63

# ---- 公开路由 ----

@app.get("/api/status")
async def api_status():
    s = db.stats()
    return {"status": "online", "version": "2.0", "dimension": qe.DIM,
            "hexagrams": 64, "cnsh_available": cnsh.available, "db_stats": s,
            "dna": "#龍芯⚡️丙午·乙未·甲辰·离为火-量子卦象-v2.0"}

@app.post("/api/auth/register")
async def register(req: LoginReq):
    if len(req.username) < 2: raise HTTPException(400, "用户名至少2字符")
    if len(req.password) < 4: raise HTTPException(400, "密码至少4字符")
    if db.get_user(req.username): raise HTTPException(409, "用户名已存在")
    uid = f"lhq_{req.username}"
    user_id = db.create_user(req.username, hash_pw(req.password), uid)
    return {"message": "注册成功", "uid": uid, "user_id": user_id}

@app.post("/api/auth/login")
async def login(req: LoginReq):
    user = db.get_user(req.username)
    if not user or not verify_pw(req.password, user["password_hash"]):
        raise HTTPException(401, "用户名或密码错误")
    token = create_token({"sub": user["username"], "uid": user["uid"]})
    return {"access_token": token, "token_type": "bearer", "uid": user["uid"]}

# ---- 受保护路由 ----

@app.post("/api/session/create")
async def create_session(data: SessionCreate, u: Dict = Depends(get_current_user)):
    sid = hashlib.sha256(f"{datetime.now().isoformat()}{os.urandom(16)}".encode()).hexdigest()[:20]
    state = qe.uniform_superposition()
    db.save_session(sid, u["id"], state, data.description)
    db.add_audit(sid, "create", "🟢", f"用户{u['username']}创建会话")
    return {"session_id": sid, "user": u["username"], "description": data.description,
            "top_hexagrams": qe.top_hexagrams(state, 3)}

@app.get("/api/session/list")
async def list_sessions(limit: int = Query(20, le=100), u: Dict = Depends(get_current_user)):
    sessions = db.list_sessions(u["id"], limit)
    return {"user": u["username"], "count": len(sessions), "sessions": sessions}

@app.get("/api/session/{session_id}")
async def get_session(session_id: str, u: Dict = Depends(get_current_user)):
    sess = db.get_session(session_id)
    if not sess or sess["user_id"] != u["id"]:
        raise HTTPException(404, "会话不存在或无权访问")
    return {"session_id": sess["session_id"], "description": sess["description"],
            "topology": sess["topology"], "created_at": sess["created_at"],
            "entropy": round(qe.entropy(sess["state_vector"]), 4),
            "top_hexagrams": qe.top_hexagrams(sess["state_vector"], 10)}

@app.post("/api/measure")
async def measure(session_id: str = Query(...), u: Dict = Depends(get_current_user)):
    sess = db.get_session(session_id)
    if not sess or sess["user_id"] != u["id"]:
        raise HTTPException(404, "会话不存在或无权访问")
    idx, prob = qe.measure(sess["state_vector"])
    collapsed = qe.ket(idx)
    db.update_state(session_id, collapsed)
    dna = gen_dna("measure", f"{session_id}_{idx}")
    db.add_history(session_id, "measure", {}, {"index": idx, "probability": prob}, dna)
    db.add_audit(session_id, "measure", "🟢",
                 f"坍缩到 {HEXAGRAM_NAMES[idx]}{HEXAGRAM_UNICODE[idx]} ({idx})")
    return {"session_id": session_id, "index": idx,
            "hexagram_name": HEXAGRAM_NAMES[idx],
            "hexagram_symbol": HEXAGRAM_UNICODE[idx],
            "probability": round(prob, 4), "binary": format(idx, '06b'), "dna": dna}

@app.post("/api/evolve")
async def evolve(req: EvolveReq, u: Dict = Depends(get_current_user)):
    sess = db.get_session(req.session_id)
    if not sess or sess["user_id"] != u["id"]:
        raise HTTPException(404, "会话不存在或无权访问")
    H = qe.hamiltonian(topology=req.topology, g=req.g)
    new_state = qe.evolve(sess["state_vector"], H, req.time)
    db.update_state(req.session_id, new_state)
    ent = qe.entropy(new_state)
    dna = gen_dna("evolve", f"{req.session_id}_{req.topology}")
    db.add_history(req.session_id, "evolve",
                   {"topology": req.topology, "g": req.g, "time": req.time},
                   {"entropy": ent}, dna)
    db.add_audit(req.session_id, "evolve", "🟢",
                 f"拓扑={req.topology} g={req.g} t={req.time} 熵={ent:.3f}")
    return {"session_id": req.session_id, "topology": req.topology,
            "g": req.g, "time": req.time, "entropy": round(ent, 4),
            "top_hexagrams": qe.top_hexagrams(new_state, 5), "dna": dna}

@app.post("/api/entangle")
async def create_entangled(req: EntangleReq, u: Dict = Depends(get_current_user)):
    sess = db.get_session(req.session_id)
    if not sess or sess["user_id"] != u["id"]:
        raise HTTPException(404, "会话不存在或无权访问")
    if req.type == "bell":
        a, b = req.a % qe.DIM, req.b % qe.DIM
        if a == b: b = (a + 1) % qe.DIM
        state = qe.bell_state(a, b)
        label = f"Bell态 |{HEXAGRAM_NAMES[a]}⟩+|{HEXAGRAM_NAMES[b]}⟩"
    elif req.type == "ghz":
        state = qe.ghz_state()
        label = "GHZ态 (|乾⟩+|未济⟩)/√2"
    elif req.type == "w":
        state = qe.w_state()
        label = "W态 (单激发态)"
    else:
        raise HTTPException(400, "不支持的纠缠类型: bell/ghz/w")
    db.update_state(req.session_id, state)
    ent = qe.entropy(state)
    dna = gen_dna("entangle", f"{req.session_id}_{req.type}")
    db.add_history(req.session_id, "entangle", {"type": req.type}, {"entropy": ent}, dna)
    db.add_audit(req.session_id, "entangle", "🟢", label)
    return {"session_id": req.session_id, "type": req.type, "label": label,
            "entropy": round(ent, 4), "top_hexagrams": qe.top_hexagrams(state, 5), "dna": dna}

@app.get("/api/hexagram/{index}")
async def get_hexagram(index: int):
    if index < 0 or index >= 64: raise HTTPException(400, "索引需在 0-63 之间")
    return {"index": index, "name": HEXAGRAM_NAMES[index],
            "symbol": HEXAGRAM_UNICODE[index], "binary": format(index, '06b'),
            "description": HEXAGRAM_DESCRIPTIONS.get(index, "")}

@app.get("/api/hexagram/all")
async def list_all_hexagrams():
    return {"total": 64, "hexagrams": [
        {"index": i, "name": f"{HEXAGRAM_NAMES[i]}{HEXAGRAM_UNICODE[i]}",
         "binary": format(i, '06b')} for i in range(64)]}

@app.get("/api/hexagram/relation/{index}")
async def hexagram_relations(index: int, u: Dict = Depends(get_current_user)):
    if index < 0 or index >= 64: raise HTTPException(400, "索引需在 0-63 之间")
    return hexagram_relation(index)

@app.post("/api/cnsh/run")
async def run_cnsh(request: dict):
    code = request.get("code", "")
    if not code: raise HTTPException(400, "缺少 'code' 字段")
    return cnsh.execute(code)

@app.get("/api/cnsh/hexagram/{index}")
async def cnsh_analyze_hexagram(index: int, u: Dict = Depends(get_current_user)):
    if index < 0 or index >= 64: raise HTTPException(400, "索引需在 0-63 之间")
    return {"hexagram": {"index": index, "name": f"{HEXAGRAM_NAMES[index]}{HEXAGRAM_UNICODE[index]}"},
            "cnsh_result": cnsh.analyze_hexagram(index)}

@app.get("/api/history/{session_id}")
async def get_history(session_id: str, limit: int = Query(20, le=100),
                      u: Dict = Depends(get_current_user)):
    sess = db.get_session(session_id)
    if not sess or sess["user_id"] != u["id"]:
        raise HTTPException(404, "会话不存在或无权访问")
    return {"session_id": session_id,
            "history": db.get_history(session_id, limit),
            "audit_logs": db.get_audit(session_id, limit)}


# ============================================================
# 八、启动入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="龍魂量子卦象API服务器 v2.0")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--reload", action="store_true")
    parser.add_argument("--name", default="lh_quantum_api_v2", help="模块名(用于reload)")
    args = parser.parse_args()

    print(f"""
╔══════════════════════════════════════════════════════╗
║  🐉 龍魂·量子卦象引擎 API v2.0                      ║
║  📍 http://{args.host}:{args.port}                        ║
║  📖 API文档: http://{args.host}:{args.port}/api/docs     ║
║  🔐 JWT认证 · 64卦希尔伯特空间 · CNSH集成              ║
╚══════════════════════════════════════════════════════╝
""")
    uvicorn.run(f"{args.name}:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
