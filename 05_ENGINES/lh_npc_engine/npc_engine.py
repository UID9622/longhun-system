#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·丁巳·恒卦-NPC-ENGINE-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""🐉 龍魂·24人格可持续互动NPC引擎 v1.0
三层引擎：行为层(状态机) + 对话层(人格化生成) + 记忆层(短期/长期/情感)
知人者智，自知者明。——《道德经》第33章
纯标准库零依赖 · 断网可跑 · 可插Ollama/云端LLM
"""
import json, os, sqlite3, time, random, datetime
from dataclasses import dataclass, field, asdict

# ============================================================
# 人格模板 (Persona Template) —— 24人格的"性格剧本"
# ============================================================

@dataclass
class 人格模板:
    代号: str            # 如 P01
    名字: str
    头衔: str            # 职务/部门
    性格: list           # 性格特质
    口头禅: list         # 说话风格锚
    语气: str            # 语气描述
    价值观: str          # 行为准则
    喜好: list = field(default_factory=list)   # 好感度+事件
    厌恶: list = field(default_factory=list)   # 好感度-事件
    卦象: str = "太极"

    def 人设提示词(self) -> str:
        return (f"你是{self.名字}，{self.头衔}。性格：{'、'.join(self.性格)}。"
                f"说话风格：{self.语气}。价值观：{self.价值观}。"
                f"记住与玩家的每段互动，态度随好感度变化，永不跳出人设。")

# ============================================================
# 记忆层 —— NPC的"灵魂"
# ============================================================

class 记忆层:
    """短期记忆(内存) + 长期记忆(SQLite) + 情感记忆(好感度+情绪向量)"""
    def __init__(self, db路径: str, npc代号: str, 短期容量: int = 20):
        self.npc = npc代号
        self.短期 = []
        self.容量 = 短期容量
        self.db = sqlite3.connect(db路径)
        self.db.execute("""CREATE TABLE IF NOT EXISTS 长期记忆(
            id INTEGER PRIMARY KEY AUTOINCREMENT, npc TEXT, 时间 REAL,
            玩家 TEXT, 事件 TEXT, 情感 REAL, 摘要 TEXT)""")
        self.db.execute("""CREATE TABLE IF NOT EXISTS 情感(
            npc TEXT, 玩家 TEXT, 好感度 REAL DEFAULT 0,
            信任 REAL DEFAULT 0.5, 情绪 TEXT DEFAULT '平静',
            互动次数 INTEGER DEFAULT 0, PRIMARY KEY(npc, 玩家))""")
        self.db.commit()

    def 记住(self, 玩家: str, 事件: str, 情感分: float = 0.0):
        条目 = {"时间": time.time(), "玩家": 玩家, "事件": 事件, "情感": 情感分}
        self.短期.append(条目)
        if len(self.短期) > self.容量:
            旧 = self.短期.pop(0)
            self._压入长期(旧)
        if abs(情感分) >= 0.3:   # 强情感事件直接进长期
            self._压入长期(条目)
        self._更新情感(玩家, 情感分)

    def _压入长期(self, 条目):
        self.db.execute("INSERT INTO 长期记忆(npc,时间,玩家,事件,情感,摘要) VALUES(?,?,?,?,?,?)",
            (self.npc, 条目["时间"], 条目["玩家"], 条目["事件"], 条目["情感"], 条目["事件"][:60]))
        self.db.commit()

    def _更新情感(self, 玩家: str, 情感分: float):
        self.db.execute("""INSERT INTO 情感(npc,玩家,好感度,互动次数) VALUES(?,?,?,1)
            ON CONFLICT(npc,玩家) DO UPDATE SET
            好感度=MAX(-100,MIN(100,好感度+?)), 互动次数=互动次数+1""",
            (self.npc, 玩家, 情感分, 情感分))
        # 情绪随好感度流动
        row = self.db.execute("SELECT 好感度 FROM 情感 WHERE npc=? AND 玩家=?",
                              (self.npc, 玩家)).fetchone()
        g = row[0]
        情绪 = '亲近' if g >= 60 else ('友善' if g >= 20 else ('平静' if g > -20 else ('戒备' if g > -60 else '敌视')))
        信任 = min(1.0, max(0.0, 0.5 + g / 200))
        self.db.execute("UPDATE 情感 SET 情绪=?, 信任=? WHERE npc=? AND 玩家=?",
                        (情绪, 信任, self.npc, 玩家))
        self.db.commit()

    def 情感状态(self, 玩家: str) -> dict:
        row = self.db.execute("SELECT 好感度,信任,情绪,互动次数 FROM 情感 WHERE npc=? AND 玩家=?",
                              (self.npc, 玩家)).fetchone()
        if not row:
            return {"好感度": 0, "信任": 0.5, "情绪": "陌生", "互动次数": 0}
        return {"好感度": row[0], "信任": round(row[1], 2), "情绪": row[2], "互动次数": row[3]}

    def 回忆(self, 玩家: str, 关键词: str = "", 条数: int = 3) -> list:
        """语义回忆：先短期，再长期按关键词/情感强度检索"""
        命中 = [m for m in self.短期 if m["玩家"] == 玩家 and (not 关键词 or 关键词 in m["事件"])]
        if len(命中) < 条数:
            like = f"%{关键词}%" if 关键词 else "%"
            rows = self.db.execute(
                """SELECT 事件,情感,时间 FROM 长期记忆 WHERE npc=? AND 玩家=? AND 事件 LIKE ?
                   ORDER BY ABS(情感) DESC, 时间 DESC LIMIT ?""",
                (self.npc, 玩家, like, 条数 - len(命中))).fetchall()
            命中 += [{"事件": r[0], "情感": r[1], "时间": r[2]} for r in rows]
        return 命中[-条数:]

# ============================================================
# 行为层 —— NPC的"身体"（状态机+作息）
# ============================================================

class 行为层:
    状态表 = ["休眠", "待命", "工作", "巡逻", "交流", "冥想"]
    def __init__(self, 人格: 人格模板):
        self.人格 = 人格
        self.状态 = "待命"
        self.精力 = 100.0

    def tick(self) -> str:
        """自主决策：按时段作息+精力流转"""
        时 = datetime.datetime.now().hour
        if 0 <= 时 < 6:
            目标 = "休眠"
        elif self.精力 < 20:
            目标 = "冥想"      # 精力低自主回气
        elif 6 <= 时 < 9 or 18 <= 时 < 22:
            目标 = "巡逻"
        else:
            目标 = "工作"
        self.状态 = 目标
        self.精力 = min(100, self.精力 + (10 if 目标 in ("休眠","冥想") else -2))
        return self.状态

    def 状态报告(self) -> str:
        return f"[{self.状态}|精力{self.精力:.0f}]"

# ============================================================
# 对话层 —— NPC的"嘴巴和大脑"
# ============================================================

class 对话层:
    """人格化对话生成：本地模板引擎兜底，可插LLM（Ollama/云端）"""
    def __init__(self, llm钩子=None):
        self.llm = llm钩子   # callable(人设提示词, 上下文, 玩家输入) -> str

    def 生成(self, npc: 'NPC', 玩家: str, 输入: str) -> str:
        if self.llm:
            try:
                上下文 = npc.记忆.回忆(玩家, 条数=5)
                return self.llm(npc.人格.人设提示词(), 上下文, 输入)
            except Exception:
                pass  # LLM挂了自动落本地引擎，永不断话
        return self._本地生成(npc, 玩家, 输入)

    def _本地生成(self, npc: 'NPC', 玩家: str, 输入: str) -> str:
        p = npc.人格
        情感 = npc.记忆.情感状态(玩家)
        回忆 = npc.记忆.回忆(玩家, 关键词=self._提关键词(输入))
        # 情绪决定语气温度
        温度 = {"亲近": "热切", "友善": "温和", "平静": "平和", "陌生": "客气", "戒备": "冷淡", "敌视": "生硬"}[情感["情绪"]]
        口头禅 = random.choice(p.口头禅)
        回应 = [f"{npc.行为.状态报告()}"]
        # 有共同回忆就提起——不做复读机
        if 回忆 and random.random() < 0.6:
            旧 = random.choice(回忆)
            回应.append(f"我记得你说过「{旧['事件'][:30]}」……")
        # 喜好/厌恶命中影响
        if any(k in 输入 for k in p.喜好):
            npc.记忆.记住(玩家, f"玩家聊到{输入[:20]}(喜好命中)", 情感分=+2.0)
            回应.append(f"（眼睛一亮）这正是我所好！")
        elif any(k in 输入 for k in p.厌恶):
            npc.记忆.记住(玩家, f"玩家提到{输入[:20]}(厌恶命中)", 情感分=-3.0)
            回应.append(f"（皱眉）此事……不提也罢。")
        else:
            npc.记忆.记住(玩家, f"玩家说：{输入[:30]}", 情感分=+0.5)
        回应.append(f"{口头禅}，{玩家}。（{温度}）{self._内容回应(输入, p)}")
        return "".join(回应)

    def _提关键词(self, 输入: str) -> str:
        for k in ("部署","审计","DNA","算力","记忆","签名","路由","估值","花名册","干支"):
            if k in 输入: return k
        return ""

    def _内容回应(self, 输入: str, p: 人格模板) -> str:
        if "?" in 输入 or "？" in 输入:
            return f"你问之事，依我看当从「{p.价值观[:12]}」处着眼。"
        return f"你说的我记下了，来日方长。"

# ============================================================
# NPC 主体 —— 三层合一
# ============================================================

class NPC:
    def __init__(self, 人格: 人格模板, db路径: str = ":memory:", llm钩子=None):
        self.人格 = 人格
        self.记忆 = 记忆层(db路径, 人格.代号)
        self.行为 = 行为层(人格)
        self.对话 = 对话层(llm钩子)

    def 互动(self, 玩家: str, 输入: str) -> dict:
        self.行为.tick()
        回应 = self.对话.生成(self, 玩家, 输入)
        return {"npc": self.人格.名字, "状态": self.行为.状态,
                "回应": 回应, "情感": self.记忆.情感状态(玩家)}

    def 自主一刻(self) -> str:
        """无玩家时NPC自主生活"""
        状态 = self.行为.tick()
        自语 = {"工作": f"{self.人格.名字}正在处理{random.choice(self.人格.喜好 or ['公务'])}相关事务。",
                "巡逻": f"{self.人格.名字}巡视辖区，一切如常。",
                "冥想": f"{self.人格.名字}静坐回气，默念：{self.人格.价值观[:16]}……",
                "休眠": f"{self.人格.名字}休眠中，呼吸绵长。",
                "待命": f"{self.人格.名字}待命，偶尔翻检旧档。",
                "交流": f"{self.人格.名字}与邻家NPC寒暄。"}
        return 自语.get(状态, "")
