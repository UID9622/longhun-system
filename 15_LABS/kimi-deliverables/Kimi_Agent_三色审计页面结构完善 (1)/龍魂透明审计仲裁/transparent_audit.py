#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""🐉 龍魂·透明审计与冲突仲裁引擎 v1.1
兼听则明，偏信则暗。——《资治通鉴》(原稿架构CodeBuddy v1.0 · Kimi实测落地)
纯标准库零依赖 · 断网可跑 · 云端引擎可插拔
"""
import asyncio, json, os, sqlite3, time, hashlib, math, re
from collections import Counter
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "龍魂低算力内核", "core"))
try:
    from longhun_core.dna_trace import 生成DNA, 短身份码
except Exception:
    def 生成DNA(x): return f"#龍芯⚡️【待生成器回填】-{x}-UID9622"
    def 短身份码(x): return hashlib.sha256(x.encode()).hexdigest()[:8].upper()

# ============================================================
# 引擎接口 + 本地/模拟引擎（云端引擎继承 引擎基类 即可插拔）
# ============================================================

class 引擎基类:
    名字 = "base"
    async def 询问(self, 问题: str, 子DNA: str, 超时: float) -> dict:
        raise NotImplementedError

class 本地龍魂引擎(引擎基类):
    名字 = "longhun"
    async def 询问(self, 问题, 子DNA, 超时):
        t0 = time.time()
        await asyncio.sleep(0.01)
        return {"来源": "龍魂(本地)", "子DNA": 子DNA, "耗时": round(time.time()-t0, 3),
                "内容": f"按P0协议：数据主权归属用户本人，拒绝外部训练抓取。问题「{问题[:20]}」答复：主权不可交易。",
                "置信度": 0.95, "token统计": {"输入": len(问题)//2, "输出": 60, "缓存命中率": 0.0}}

class 模拟云端引擎(引擎基类):
    """云端引擎适配器样例：实装时把 _调用 换成真API"""
    def __init__(self, 名字, 立场文本, 延迟=0.02):
        self.名字 = 名字; self.文本 = 立场文本; self.延迟 = 延迟
    async def 询问(self, 问题, 子DNA, 超时):
        t0 = time.time()
        await asyncio.sleep(self.延迟)
        return {"来源": self.名字, "子DNA": 子DNA, "耗时": round(time.time()-t0, 3),
                "内容": self.文本, "置信度": 0.85,
                "token统计": {"输入": len(问题)//2, "输出": len(self.文本)//2, "缓存命中率": 0.9}}

# ============================================================
# 结果仓库 (Result Vault) —— 每个回答独立存储，永不合并
# ============================================================

class 结果仓库:
    def __init__(self, db路径=":memory:"):
        self.db = sqlite3.connect(db路径)
        self.db.execute("""CREATE TABLE IF NOT EXISTS 结果(
            父DNA TEXT, 子DNA TEXT PRIMARY KEY, 来源 TEXT, 时间 REAL,
            内容 TEXT, 置信度 REAL, token统计 TEXT, 耗时 REAL)""")
        self.db.commit()
    def 存(self, 父DNA, r):
        self.db.execute("INSERT OR REPLACE INTO 结果 VALUES(?,?,?,?,?,?,?,?)",
            (父DNA, r["子DNA"], r["来源"], time.time(), r["内容"], r["置信度"],
             json.dumps(r["token统计"], ensure_ascii=False), r["耗时"]))
        self.db.commit()
    def 取(self, 父DNA):
        return self.db.execute("SELECT 来源,内容,置信度,token统计,耗时,子DNA FROM 结果 WHERE 父DNA=?",
                               (父DNA,)).fetchall()

# ============================================================
# 冲突仲裁器 —— 纯标准库语义相似度（词袋余弦，免FAISS依赖）
# ============================================================

def 词袋(文本):
    词 = re.findall(r'[\u4e00-\u9fff]{2,}|[a-zA-Z0-9_]+', 文本)
    单字 = [c for c in 文本 if '\u4e00' <= c <= '\u9fff']
    return Counter(词 + 单字)

def 余弦(c1, c2):
    if not c1 or not c2: return 0.0
    交 = set(c1) & set(c2)
    分子 = sum(c1[w]*c2[w] for w in 交)
    模 = math.sqrt(sum(v*v for v in c1.values())) * math.sqrt(sum(v*v for v in c2.values()))
    return 分子/模 if 模 else 0.0

class 冲突仲裁器:
    def __init__(self, 红阈=0.3, 黄阈=0.6):
        self.红阈 = 红阈; self.黄阈 = 黄阈
    def 检测(self, 结果列表):
        冲突 = []
        袋 = [词袋(r["内容"]) for r in 结果列表]
        for i in range(len(结果列表)):
            for j in range(i+1, len(结果列表)):
                sim = 余弦(袋[i], 袋[j])
                if sim < self.黄阈:
                    冲突.append({"甲": 结果列表[i]["来源"], "乙": 结果列表[j]["来源"],
                                 "相似度": round(sim, 2),
                                 "级别": "🔴" if sim < self.红阈 else "🟡",
                                 "说明": "语义严重偏离" if sim < self.红阈 else "立场存在分歧·分别呈现"})
        return 冲突

# ============================================================
# 透明路由器 —— 并行分发·独立超时·单点失败降级
# ============================================================

class 透明路由器:
    def __init__(self, 引擎们: list, 仓库: 结果仓库 = None, 超时=5.0):
        self.引擎们 = 引擎们; self.仓库 = 仓库 or 结果仓库(); self.超时 = 超时
        self.仲裁 = 冲突仲裁器()

    async def _单路(self, 引擎, 问题, 父DNA):
        子DNA = f"{父DNA[:-7]}-{引擎.名字.upper()}-{短身份码(引擎.名字+父DNA)}-UID9622"
        try:
            r = await asyncio.wait_for(引擎.询问(问题, 子DNA, self.超时), timeout=self.超时)
            return r
        except Exception as e:
            return {"来源": 引擎.名字, "子DNA": 子DNA, "耗时": self.超时, "内容": "",
                    "置信度": 0.0, "token统计": {}, "失败": str(e)[:60]}

    async def 路由(self, 问题: str, 用户="UID9622") -> dict:
        父DNA = 生成DNA("USER-QUERY")
        结果 = await asyncio.gather(*[self._单路(e, 问题, 父DNA) for e in self.引擎们])
        for r in 结果: self.仓库.存(父DNA, r)
        有效 = [r for r in 结果 if "失败" not in r]
        失败 = [r for r in 结果 if "失败" in r]
        冲突 = self.仲裁.检测(有效) if len(有效) >= 2 else []
        红 = sum(1 for c in 冲突 if c["级别"] == "🔴")
        三色 = "🔴" if (红 or len(有效) < len(结果)//2+1 and 失败) else ("🟡" if (冲突 or 失败) else "🟢")
        return {"父DNA": 父DNA, "用户": 用户, "问题": 问题,
                "回答": 结果, "冲突": 冲突, "失败数": len(失败),
                "三色": 三色, "时间": time.time()}

# ============================================================
# 仪表盘渲染
# ============================================================

def 仪表盘(报告: dict) -> str:
    行 = ["="*64, f"🐉 龍魂·透明审计仪表盘 | {报告['三色']}", f"父DNA: {报告['父DNA']}", "-"*64]
    for r in 报告["回答"]:
        if "失败" in r:
            行.append(f"  ✗ {r['来源']:<12} 失败降级: {r['失败']}")
        else:
            t = r["token统计"]
            行.append(f"  ✓ {r['来源']:<12} {r['耗时']:.2f}s | token {t.get('输入',0)}→{t.get('输出',0)} | 缓存 {t.get('缓存命中率',0):.0%}")
    if 报告["冲突"]:
        行.append("-"*64); 行.append(f"  ⚔️ 冲突 {len(报告['冲突'])} 处（分别呈现·不合并·不掩盖）:")
        for c in 报告["冲突"]:
            行.append(f"    {c['级别']} {c['甲']} vs {c['乙']} 相似度 {c['相似度']} · {c['说明']}")
    else:
        行.append("  无冲突 · 全员一致")
    行.append("="*64)
    return "\n".join(行)
