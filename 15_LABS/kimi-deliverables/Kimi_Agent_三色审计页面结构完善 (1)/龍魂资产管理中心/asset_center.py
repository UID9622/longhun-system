#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""🐉 龍魂·历史资产管理中心 lh asset v1.0
治国有常，而利民为本。——《淮南子》
所有资产的记忆中枢：注册/检索/关系/历史/导出/注销(只冻结不删除)
纯标准库零依赖 · 幂等扫描 · SM3/SHA-256哈希链 · DNA算法生成
"""
import json, os, sqlite3, sys, time, hashlib, argparse, fnmatch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "龍魂低算力内核", "core"))
try:
    from longhun_core.dna_trace import 生成DNA, 短身份码
except Exception:
    def 生成DNA(x): return f"#龍芯⚡️【待生成器回填】-{x}-UID9622"
    def 短身份码(x): return hashlib.sha256(x.encode()).hexdigest()[:8].upper()

资产类型 = {".py":("ENGINE_","引擎"), ".md":("PROTO_","协议"), ".sh":("ENGINE_","脚本"),
            ".json":("CODE_","配置"), ".yaml":("DEPLOY_","部署"), ".yml":("DEPLOY_","部署"),
            ".asc":("SIG_","签章"), ".html":("KNOW_","页面"), ".db":("ROSTER_","数据")}
状态 = ("🟢active","🟡frozen","🔴violated","⚪retired")

class 资产中心:
    def __init__(self, db路径):
        self.db = sqlite3.connect(db路径)
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS assets(
            asset_id TEXT PRIMARY KEY, dna TEXT, type TEXT, name TEXT, version TEXT,
            created_at REAL, last_modified REAL, hash TEXT, status TEXT DEFAULT '🟢active',
            location TEXT UNIQUE, description TEXT, tags TEXT, prev_hash TEXT, chain_hash TEXT);
        CREATE TABLE IF NOT EXISTS edges(
            from_id TEXT, to_id TEXT, rel TEXT, PRIMARY KEY(from_id,to_id,rel));
        CREATE TABLE IF NOT EXISTS history(
            id INTEGER PRIMARY KEY AUTOINCREMENT, asset_id TEXT, 时间 REAL, 事件 TEXT, hash TEXT);
        CREATE VIRTUAL TABLE IF NOT EXISTS assets_fts USING fts5(name, description, tags, content='');
        """)
        self.db.commit()
        self._链尾 = self.db.execute("SELECT chain_hash FROM assets ORDER BY created_at DESC, asset_id DESC LIMIT 1").fetchone()
        self._链尾 = self._链尾[0] if self._链尾 else "0"*64

    def _哈希(self, b): 
        return hashlib.sha256(b).hexdigest()
    def _类型(self, fn):
        return 资产类型.get(os.path.splitext(fn)[1].lower(), ("CODE_","文件"))

    def 注册(self, 路径, 描述="", 标签=None, 来源="scan"):
        with open(路径,'rb') as f: 内容 = f.read()
        h = self._哈希(内容)
        名 = os.path.basename(路径)
        前缀, 类名 = self._类型(名)
        今 = self.db.execute("SELECT asset_id,hash,status FROM assets WHERE location=?", (路径,)).fetchone()
        now = time.time()
        if 今:
            if 今[0] and 今[1] == h:
                self.db.execute("UPDATE assets SET last_modified=? WHERE asset_id=?", (now, 今[0]))
                self.db.commit()
                return ("跳过·幂等", 今[0])
            aid = 今[0]
            self.db.execute("UPDATE assets SET hash=?, last_modified=?, version=? WHERE asset_id=?",
                            (h, now, time.strftime("v%Y%m%d%H%M"), aid))
            self.db.execute("INSERT INTO history(asset_id,时间,事件,hash) VALUES(?,?,?,?)",
                            (aid, now, "内容更新", h))
            self.db.commit()
            return ("更新", aid)
        当日序号 = self.db.execute("SELECT COUNT(*) FROM assets WHERE asset_id LIKE ?",
                                (f"AST-{time.strftime('%Y%m%d')}-%",)).fetchone()[0] + 1
        aid = f"AST-{time.strftime('%Y%m%d')}-{当日序号:03d}"
        dna = 生成DNA(f"{前缀}{当日序号:03d}")
        chain = self._哈希((self._链尾 + h).encode())
        self.db.execute("INSERT INTO assets VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (aid, dna, 类名, 名, "v1.0", now, now, h, "🟢active", 路径, 描述 or f"{类名}·{来源}注册",
             json.dumps(标签 or [类名], ensure_ascii=False), self._链尾, chain))
        self.db.execute("INSERT INTO assets_fts(rowid,name,description,tags) VALUES((SELECT rowid FROM assets WHERE asset_id=?),?,?,?)",
                        (aid, 名, 描述 or 类名, " ".join(标签 or [类名])))
        self.db.execute("INSERT INTO history(asset_id,时间,事件,hash) VALUES(?,?,?,?)", (aid, now, "注册", h))
        self.db.commit()
        self._链尾 = chain
        return ("注册", aid)

    def 扫描(self, 目录, 模式=("*",)):
        统计 = {"注册":0,"更新":0,"跳过·幂等":0}
        for dp,_,fns in os.walk(目录):
            if any(x in dp for x in ('.git','__pycache__','node_modules')): continue
            for fn in fns:
                if not any(fnmatch.fnmatch(fn,m) for m in 模式): continue
                动作,_ = self.注册(os.path.join(dp,fn), 来源="init --scan")
                统计[动作] += 1
        return 统计

    def 关联(self, 甲, 乙, 关系):
        self.db.execute("INSERT OR IGNORE INTO edges VALUES(?,?,?)", (甲,乙,关系)); self.db.commit()

    def 查询(self, 关键词="", 类型=None, 状态过滤="🟢active", 限=50):
        sql = "SELECT asset_id,type,name,status,location FROM assets WHERE status=?"
        args = [状态过滤]
        if 类型: sql += " AND type=?"; args.append(类型)
        if 关键词:
            sql += " AND (name LIKE ? OR description LIKE ? OR tags LIKE ?)"
            args += [f"%{关键词}%"]*3
        return self.db.execute(sql+f" LIMIT {限}", args).fetchall()

    def 详情(self, 键):
        row = self.db.execute("SELECT * FROM assets WHERE asset_id=? OR name=?", (键,键)).fetchone()
        if not row: return None
        史 = self.db.execute("SELECT 时间,事件,hash FROM history WHERE asset_id=? ORDER BY id", (row[0],)).fetchall()
        边 = self.db.execute("SELECT from_id,to_id,rel FROM edges WHERE from_id=? OR to_id=?", (row[0],row[0])).fetchall()
        return {"记录": row, "历史": 史, "关系": 边}

    def 图(self, 键, 深=2):
        row = self.db.execute("SELECT asset_id FROM assets WHERE asset_id=? OR name=?", (键,键)).fetchone()
        if not row: return []
        起点, 结果, 已到 = row[0], [], {row[0]}
        前沿 = [起点]
        for _ in range(深):
            新 = []
            for n in 前沿:
                for f,t,r in self.db.execute("SELECT from_id,to_id,rel FROM edges WHERE from_id=? OR to_id=?", (n,n)):
                    结果.append((f,t,r))
                    for x in (f,t):
                        if x not in 已到: 已到.add(x); 新.append(x)
            前沿 = 新
        return list(dict.fromkeys(结果))

    def 注销(self, 键, 原因):
        row = self.db.execute("SELECT asset_id FROM assets WHERE asset_id=? OR name=?", (键,键)).fetchone()
        if not row: return None
        self.db.execute("UPDATE assets SET status='⚪retired' WHERE asset_id=?", (row[0],))
        self.db.execute("INSERT INTO history(asset_id,时间,事件,hash) VALUES(?,?,?,?)",
                        (row[0], time.time(), f"注销(只冻结不删除): {原因}", ""))
        self.db.commit(); return row[0]

    def 复活(self, 键):
        self.db.execute("UPDATE assets SET status='🟢active' WHERE asset_id=? OR name=?", (键,键))
        self.db.commit()

    def 验链(self):
        prev = "0"*64; n = 0
        for aid,h,ph,ch in self.db.execute("SELECT asset_id,hash,prev_hash,chain_hash FROM assets ORDER BY created_at, asset_id"):
            if ph != prev or self._哈希((prev+h).encode()) != ch:
                return {"完整": False, "断点": aid, "三色": "🔴"}
            prev = ch; n += 1
        return {"完整": True, "长度": n, "三色": "🟢"}

    def 导出(self):
        return [dict(zip(["asset_id","dna","type","name","version","created_at","last_modified","hash","status","location","description","tags"],
                         r)) for r in self.db.execute("SELECT asset_id,dna,type,name,version,created_at,last_modified,hash,status,location,description,tags FROM assets")]
