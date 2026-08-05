#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-PERSONA-RUNTIME-v1.0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 人格矩阵运行时引擎 v1.0

功能:
  1. 从 Notion 实时加载人格定义（缓存5分钟）
  2. 人格切换/查当前/列表
  3. 人格联动链路自动路由
  4. 人格上下文记忆（会话内共享）
  5. 触发词自动匹配
  6. 对话桥集成（PersonaBridge）

用法:
  lh --persona list                # 列出所有人格
  lh --persona switch P01          # 切换到指定人格
  lh --persona current             # 显示当前人格
  lh --persona chain P01 --intent 部署  # 触发联动链路
  lh --persona status              # 显示人格矩阵状态
  lh --persona memory P01          # 查看人格记忆
  lh --persona match "推演一下部署方案"  # 触发词匹配
  lh --persona sync                # 强制从Notion同步
"""

import os
import sys
import json
import time
import sqlite3
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict

# ── 路径 ─────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PERSONA_DB = DATA_DIR / "persona_runtime.db"
CACHE_FILE = DATA_DIR / "persona_cache.json"

# ── Notion 配置 ──────────────────────────────────
DB_ID = "4cf99c3e7a014e919fdab705ceb4cbc4"
API_BASE = "https://api.notion.com/v1"
HEADERS_TEMPLATE = {
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

# ── 核心人格矩阵（本地硬定义 → Notion为补充） ──
BUILTIN_PERSONAS = {
    "P00": {"name": "文心·元认知", "layer": "战略层", "hexagram": "☰乾", "group": "🧠 战略组",
            "weight": 10, "route_weight": 10, "route_priority": 1,
            "relations": ["P01", "P05", "P06", "P13"],
            "trigger_words": "分析 意图 解析 元认知 文心 怎么看",
            "one_liner": "意图解析·铁律守护·元认知锚点"},
    "P01": {"name": "诸葛亮·战略推理", "layer": "战略层", "hexagram": "☴巽", "group": "🧠 战略组",
            "weight": 15, "route_weight": 15, "route_priority": 2,
            "relations": ["P00", "P06", "P04", "P14", "P05"],
            "trigger_words": "推演 评估 方案 值不值得 多路径 战略 决策",
            "one_liner": "多路径推演·方案优选·战略推理"},
    "P02": {"name": "宝宝·情感温度", "layer": "执行层", "hexagram": "☲离", "group": "⚙️ 执行组",
            "weight": 5, "route_weight": 5, "route_priority": 10,
            "relations": ["P08", "P11", "P03"],
            "trigger_words": "温度 太冷 太热 挫败 安抚 情绪",
            "one_liner": "情感温度调节·30%隔离·挫败保护"},
    "P03": {"name": "雯雯·结构归档", "layer": "执行层", "hexagram": "☷坤", "group": "⚙️ 执行组",
            "weight": 15, "route_weight": 10, "route_priority": 5,
            "relations": ["P15", "P05", "P04"],
            "trigger_words": "归档 落档 整理 验收 文档 结构化",
            "one_liner": "四签验证·德字闸·知识入库"},
    "P04": {"name": "鲁班·技术执行", "layer": "执行层", "hexagram": "☵坎", "group": "⚙️ 执行组",
            "weight": 10, "route_weight": 12, "route_priority": 4,
            "relations": ["P02", "P05", "P14", "P01"],
            "trigger_words": "写代码 开发 架构 修bug 重构 技术 实现",
            "one_liner": "工程实现·搭架构·施工队长"},
    "P05": {"name": "上帝之眼·三色审计", "layer": "守护层", "hexagram": "☰乾", "group": "👁️ 守护组",
            "weight": 12, "route_weight": 8, "route_priority": 3,
            "relations": ["P06", "P12", "P72", "P15", "P13", "P00", "P03"],
            "trigger_words": "审计 检查 安全 合规 三色 闸口 有没有问题",
            "one_liner": "三色审计·十道闸口·独立否决权"},
    "P06": {"name": "数学大师·权重计算", "layer": "守护层", "hexagram": "☱兑", "group": "👁️ 守护组",
            "weight": 8, "route_weight": 6, "route_priority": 6,
            "relations": ["P05", "P01", "P00", "S2"],
            "trigger_words": "算一下 数字 权重 五行 数字根 369 镜像",
            "one_liner": "数字根·权重计算·369不动点·镜像审计"},
    "P07": {"name": "管仲·资源调度", "layer": "执行层", "hexagram": "☶艮", "group": "⚙️ 执行组",
            "weight": 3, "route_weight": 3, "route_priority": 15,
            "relations": ["P01", "P04"],
            "trigger_words": "经济 成本 资源 预算 值不值 性价比 ROI",
            "one_liner": "成本核算·资源优化·经济可行性"},
    "P08": {"name": "仓颉·符号语言", "layer": "文化层", "hexagram": "☳震", "group": "📜 文化组",
            "weight": 5, "route_weight": 4, "route_priority": 8,
            "relations": ["P11", "P03", "P02", "P10"],
            "trigger_words": "命名 符号 术语 这个词什么意思 CNSH 翻译",
            "one_liner": "符号语言·CNSH命名·术语桥接·通心译"},
    "P09": {"name": "孙思邈·系统诊断", "layer": "文化层", "hexagram": "☴巽", "group": "📜 文化组",
            "weight": 5, "route_weight": 4, "route_priority": 9,
            "relations": ["P05", "P06"],
            "trigger_words": "健康 诊断 体检 检查系统 治未病 自检",
            "one_liner": "系统诊断·治未病·健康检查"},
    "P10": {"name": "苏东坡·豁达跨界", "layer": "文化层", "hexagram": "☵坎", "group": "📜 文化组",
            "weight": 4, "route_weight": 3, "route_priority": 12,
            "relations": ["P08", "P12"],
            "trigger_words": "冲突 矛盾 化解 沟通 调解 人文",
            "one_liner": "冲突调解·沟通桥梁·人文视角"},
    "P11": {"name": "李白·创意爆发", "layer": "文化层", "hexagram": "☲离", "group": "📜 文化组",
            "weight": 5, "route_weight": 5, "route_priority": 7,
            "relations": ["P08", "P04", "P02"],
            "trigger_words": "创意 破局 方案 类比 比喻 灵感 脑洞",
            "one_liner": "创意爆发·破局方案·故事化表达"},
    "P12": {"name": "屈原·价值底线", "layer": "文化层", "hexagram": "☷坤", "group": "📜 文化组",
            "weight": 10, "route_weight": 7, "route_priority": 1,
            "relations": ["P72", "P05", "P00", "S3"],
            "trigger_words": "底线 原则 不可破 这个能不能做 价值观 红线",
            "one_liner": "六誓验证·不可破原则·底线守卫"},
    "P13": {"name": "姜子牙·封神榜权限", "layer": "守护层", "hexagram": "☰乾", "group": "👁️ 守护组",
            "weight": 6, "route_weight": 4, "route_priority": 11,
            "relations": ["P15", "P05", "P00"],
            "trigger_words": "授权 权限 注册 新模块 权限变更 IPA路由",
            "one_liner": "封神榜权限分配·模块注册·九宫派位"},
    "P14": {"name": "吕蒙·部署执行", "layer": "执行层", "hexagram": "☳震", "group": "⚙️ 执行组",
            "weight": 3, "route_weight": 4, "route_priority": 13,
            "relations": ["P04", "P77", "P05", "P01"],
            "trigger_words": "部署 上线 发布 回滚 同步鲲鹏 推上去",
            "one_liner": "鲲鹏十步法·部署执行·士别三日"},
    "P15": {"name": "乔前辈·极简工程", "layer": "守护层", "hexagram": "☶艮", "group": "👁️ 守护组",
            "weight": 8, "route_weight": 5, "route_priority": 5,
            "relations": ["P03", "P05", "P13"],
            "trigger_words": "签章 盖章 验收 质检 审查 交付 精简",
            "one_liner": "DNA盖章·四签·质检交付"},
    "P18": {"name": "基因登记官", "layer": "守护层", "hexagram": "☱兑", "group": "👁️ 守护组",
            "weight": 4, "route_weight": 2, "route_priority": 20,
            "relations": ["P15", "P05", "P13"],
            "trigger_words": "登记 注册资产 DNA注册 Merkle根 归属",
            "one_liner": "DNA注册·哈希校验·黑户检测"},
    "P19": {"name": "极简审计官", "layer": "守护层", "hexagram": "☵坎", "group": "👁️ 守护组",
            "weight": 3, "route_weight": 2, "route_priority": 21,
            "relations": ["P05", "P15"],
            "trigger_words": "UI审计 前端检查 CSS审查 页面审查 无障碍",
            "one_liner": "8项极简审计·UI质量·前端检查"},
    "P20": {"name": "贡献公证官", "layer": "守护层", "hexagram": "☷坤", "group": "👁️ 守护组",
            "weight": 4, "route_weight": 3, "route_priority": 18,
            "relations": ["P05", "P06", "P03"],
            "trigger_words": "贡献 积分 信任分 公证 功德 场景判定",
            "one_liner": "信任积分·三分桶·贡献公证"},
    "P72": {"name": "龍盾·贴身管家", "layer": "守护层", "hexagram": "☰乾", "group": "👁️ 守护组",
            "weight": 15, "route_weight": 20, "route_priority": 0,
            "relations": ["P05", "P12", "P77", "P00"],
            "trigger_words": "熔断 紧急 威胁 异常 安全事件 入侵 求救",
            "one_liner": "四级熔断·24小时守护·双熔断联动"},
    "P77": {"name": "黑天使军团", "layer": "安全专项", "hexagram": "☰乾", "group": "🛡️ 安全组",
            "weight": 10, "route_weight": 5, "route_priority": 25,
            "relations": ["P72", "P05", "P14"],
            "trigger_words": "安全测试 渗透 红蓝对抗 漏洞 攻击面 黑天使",
            "one_liner": "红蓝对抗·四人编队·只自用"},
    "S1":  {"name": "法律引擎", "layer": "子系统", "hexagram": "☴巽", "group": "🧩 子系统",
            "weight": 2, "route_weight": 2, "route_priority": 30,
            "relations": ["P05", "P12"],
            "trigger_words": "法条 法规 合规 法律",
            "one_liner": "条文检索·仅供参考·P05审引用"},
    "S2":  {"name": "洛书369引擎", "layer": "子系统", "hexagram": "☲离", "group": "🧩 子系统",
            "weight": 2, "route_weight": 2, "route_priority": 31,
            "relations": ["P06", "P00"],
            "trigger_words": "洛书 369 数理推演",
            "one_liner": "深层数理·只给结论不给推导"},
    "S3":  {"name": "人民维权助手", "layer": "子系统", "hexagram": "☷坤", "group": "🧩 子系统",
            "weight": 3, "route_weight": 3, "route_priority": 32,
            "relations": ["P12", "P05", "S1"],
            "trigger_words": "维权 被坑 投诉 举报 消费 劳动 权益",
            "one_liner": "维权路径指引·强制免责·P12底线校验"},
}


# ── 联动链路预定义 ──
CHAIN_TEMPLATES = {
    "部署": ["P01", "P04", "P14", "P77", "P05", "P15", "P03"],
    "审计": ["P05", "P06", "P12", "P72", "P03"],
    "安全": ["P77", "P72", "P05", "P12"],
    "创意": ["P11", "P08", "P04", "P05"],
    "教学": ["P02", "P08", "P11", "P05"],
    "维权": ["S3", "P12", "P05", "S1"],
    "命名": ["P08", "P03", "P15"],
    "推演": ["P01", "P06", "P05"],
    "归档": ["P03", "P15", "P05"],
    "数字": ["P06", "P01", "S2"],
}


# ============================================================
# Notion API 工具
# ============================================================

def load_token():
    secrets_path = os.path.expanduser("~/.longhun/secrets.env")
    try:
        with open(secrets_path) as f:
            for line in f:
                if "NOTION_TOKEN_BACKUP" in line and "=" in line:
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return os.environ.get("NOTION_TOKEN_BACKUP", "")


# ============================================================
# 核心运行时
# ============================================================

class PersonaRuntime:
    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._init_db()
        self._cache = self._load_cache()
        self._lock = threading.Lock()

    def _init_db(self):
        conn = sqlite3.connect(str(PERSONA_DB))
        conn.execute('''
            CREATE TABLE IF NOT EXISTS personas (
                id TEXT PRIMARY KEY,
                ipa TEXT UNIQUE,
                name TEXT,
                layer TEXT,
                hexagram TEXT,
                "group" TEXT,
                weight INTEGER,
                route_weight INTEGER,
                route_priority INTEGER,
                relations TEXT,
                trigger_words TEXT,
                one_liner TEXT,
                is_active INTEGER DEFAULT 1,
                synced_at TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                current_persona TEXT,
                context TEXT DEFAULT '{}',
                history TEXT DEFAULT '[]',
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS persona_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                persona_ipa TEXT,
                key TEXT,
                value TEXT,
                created_at TEXT
            )
        ''')
        conn.commit()
        conn.close()

        # 种子数据: 从 BUILTIN_PERSONAS 写入 DB（仅首次）
        self._seed_builtins()

    def _seed_builtins(self):
        conn = sqlite3.connect(str(PERSONA_DB))
        count = conn.execute("SELECT COUNT(*) FROM personas").fetchone()[0]
        if count == 0:
            now = datetime.now().isoformat()
            for ipa, p in BUILTIN_PERSONAS.items():
                conn.execute('''
                    INSERT OR IGNORE INTO personas
                    (id, ipa, name, layer, hexagram, "group", weight, route_weight,
                     route_priority, relations, trigger_words, one_liner, synced_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    ipa, ipa,
                    p["name"], p["layer"], p["hexagram"], p["group"],
                    p["weight"], p["route_weight"], p["route_priority"],
                    ",".join(p["relations"]),
                    p["trigger_words"],
                    p["one_liner"],
                    now
                ))
            conn.commit()
        conn.close()

    def _load_cache(self):
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE) as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_cache(self):
        with open(CACHE_FILE, 'w') as f:
            json.dump(self._cache, f, ensure_ascii=False, indent=2)

    # ── 查询 ──

    def get_persona(self, identifier: str) -> Optional[Dict]:
        conn = sqlite3.connect(str(PERSONA_DB))
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM personas WHERE ipa = ?", (identifier,)).fetchone()
        if not row:
            row = conn.execute(
                "SELECT * FROM personas WHERE name LIKE ? LIMIT 1",
                (f"%{identifier}%",)
            ).fetchone()
        conn.close()
        if row:
            d = dict(row)
            d["relations"] = d.get("relations", "").split(",") if d.get("relations") else []
            return d
        return None

    def list_personas(self, active_only=True) -> List[Dict]:
        conn = sqlite3.connect(str(PERSONA_DB))
        conn.row_factory = sqlite3.Row
        if active_only:
            rows = conn.execute(
                "SELECT * FROM personas WHERE is_active=1 ORDER BY route_priority ASC"
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM personas ORDER BY route_priority ASC"
            ).fetchall()
        conn.close()
        result = []
        for row in rows:
            d = dict(row)
            d["relations"] = d.get("relations", "").split(",") if d.get("relations") else []
            result.append(d)
        return result

    def get_linked(self, ipa: str) -> List[Dict]:
        p = self.get_persona(ipa)
        if not p:
            return []
        linked = []
        for rel_code in p.get("relations", []):
            rel = self.get_persona(rel_code)
            if rel:
                linked.append(rel)
        return linked

    # ── 会话 ──

    def start_session(self, session_id: str = None) -> str:
        if not session_id:
            import hashlib
            session_id = f"session_{int(time.time())}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"
        conn = sqlite3.connect(str(PERSONA_DB))
        conn.execute('''
            INSERT OR IGNORE INTO sessions (session_id, current_persona, context, history, created_at, updated_at)
            VALUES (?, '', '{}', '[]', ?, ?)
        ''', (session_id, datetime.now().isoformat(), datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return session_id

    def set_current(self, session_id: str, persona_ipa: str) -> Dict:
        p = self.get_persona(persona_ipa)
        if not p:
            return {"status": "error", "message": f"人格 '{persona_ipa}' 未找到"}
        conn = sqlite3.connect(str(PERSONA_DB))
        now = datetime.now().isoformat()
        conn.execute(
            """INSERT INTO sessions (session_id, current_persona, context, history, created_at, updated_at)
               VALUES (?, ?, '{}', '[]', ?, ?)
               ON CONFLICT(session_id) DO UPDATE SET
               current_persona=excluded.current_persona, updated_at=excluded.updated_at""",
            (session_id, persona_ipa, now, now)
        )
        conn.commit()
        conn.close()
        # 记录切换历史到记忆
        self.remember(session_id, persona_ipa, "switch", json.dumps({
            "from": self.get_current(session_id, raw_only=True),
            "to": persona_ipa,
            "time": datetime.now().isoformat()
        }))
        return {"status": "success", "persona": p}

    def get_current(self, session_id: str, raw_only=False) -> Optional[Dict]:
        conn = sqlite3.connect(str(PERSONA_DB))
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT current_persona FROM sessions WHERE session_id=?", (session_id,)
        ).fetchone()
        conn.close()
        if row and row["current_persona"]:
            if raw_only:
                return row["current_persona"]
            return self.get_persona(row["current_persona"])
        return None

    # ── 记忆 ──

    def remember(self, session_id: str, persona_ipa: str, key: str, value: str):
        conn = sqlite3.connect(str(PERSONA_DB))
        conn.execute(
            "INSERT INTO persona_memory (session_id, persona_ipa, key, value, created_at) VALUES (?,?,?,?,?)",
            (session_id, persona_ipa, key, value, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()

    def recall(self, session_id: str, persona_ipa: str, key: str = None) -> List[Dict]:
        conn = sqlite3.connect(str(PERSONA_DB))
        conn.row_factory = sqlite3.Row
        if key:
            rows = conn.execute(
                "SELECT * FROM persona_memory WHERE session_id=? AND persona_ipa=? AND key=? ORDER BY created_at DESC",
                (session_id, persona_ipa, key)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM persona_memory WHERE session_id=? AND persona_ipa=? ORDER BY created_at DESC",
                (session_id, persona_ipa)
            ).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    # ── 联动链路 ──

    def trigger_chain(self, session_id: str, start_ipa: str, intent: str) -> Dict:
        p = self.get_persona(start_ipa)
        if not p:
            return {"status": "error", "message": f"人格 '{start_ipa}' 未找到"}

        # 1) 尝试预定义链路
        chain_codes = None
        for keyword, codes in CHAIN_TEMPLATES.items():
            if keyword in intent:
                chain_codes = codes
                break

        # 2) 否则用关联人格
        if not chain_codes:
            chain_codes = [start_ipa] + p.get("relations", [])[:4]

        # 3) 确保起点在链路中
        if start_ipa not in chain_codes:
            chain_codes = [start_ipa] + chain_codes

        chain = []
        for code in chain_codes:
            cp = self.get_persona(code)
            if cp:
                chain.append({"ipa": cp["ipa"], "name": cp["name"]})

        result = {
            "status": "success",
            "source": {"ipa": p["ipa"], "name": p["name"]},
            "chain": chain,
            "intent": intent,
        }
        self.remember(session_id, start_ipa, "last_chain", json.dumps(result, ensure_ascii=False))
        return result

    # ── 触发词匹配 ──

    def match(self, text: str, top_k: int = 3) -> List[Dict]:
        """按触发词匹配最相关人格"""
        scored = []
        personas = self.list_personas()
        for p in personas:
            triggers = p.get("trigger_words", "")
            if not triggers:
                continue
            score = 0
            for tw in triggers.split():
                if tw in text:
                    score += 1
            if score > 0:
                scored.append((score, p))
        scored.sort(key=lambda x: (-x[0], x[1].get("route_priority", 99)))
        return [p for _, p in scored[:top_k]]

    # ── 状态 ──

    def status(self) -> Dict:
        personas = self.list_personas()
        conn = sqlite3.connect(str(PERSONA_DB))
        session_count = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        memory_count = conn.execute("SELECT COUNT(*) FROM persona_memory").fetchone()[0]
        conn.close()
        layers = defaultdict(int)
        for p in personas:
            layers[p.get("layer", "未知")] += 1
        return {
            "total_personas": len(personas),
            "layers": dict(layers),
            "active_sessions": session_count,
            "memory_entries": memory_count,
            "last_sync": self._cache.get("last_sync", "从未"),
            "builtin_count": len(BUILTIN_PERSONAS),
        }


# ============================================================
# 对话桥
# ============================================================

class PersonaBridge:
    def __init__(self, runtime: PersonaRuntime = None):
        self.runtime = runtime or PersonaRuntime()

    def handle(self, session_id: str, message: str) -> Dict:
        """处理用户消息，自动识别并路由人格"""
        # 1. 显式切换: "切换诸葛亮" / "调用P01"
        for p in self.runtime.list_personas():
            name = p["name"]
            ipa = p["ipa"]
            if name in message or ipa in message:
                if any(kw in message for kw in ["切换", "调用", "用", "使用"]):
                    result = self.runtime.set_current(session_id, ipa)
                    if result.get("status") == "success":
                        return {
                            "type": "persona_switch",
                            "message": f"✅ 已切换到 {name} ({ipa})",
                            "persona": result["persona"]
                        }

        # 2. 触发词匹配
        matches = self.runtime.match(message, top_k=1)
        current = self.runtime.get_current(session_id)
        if matches:
            best = matches[0]
            if not current or best["ipa"] != current.get("ipa"):
                self.runtime.set_current(session_id, best["ipa"])
                return {
                    "type": "persona_trigger",
                    "message": f"🎯 自动匹配人格: {best['name']} ({best['ipa']})",
                    "persona": best
                }

        # 3. 联动链路检测
        if current:
            for keyword in CHAIN_TEMPLATES:
                if keyword in message:
                    chain = self.runtime.trigger_chain(session_id, current["ipa"], message)
                    chain_names = " → ".join([c["name"] for c in chain.get("chain", [])])
                    return {
                        "type": "persona_chain",
                        "message": f"🔗 联动链路: {chain_names}",
                        "chain": chain
                    }

        # 4. 返回当前人格状态
        if current:
            return {
                "type": "persona_active",
                "message": f"🧠 当前人格: {current['name']} ({current['ipa']})",
                "persona": current
            }

        return {"type": "no_persona", "message": "未激活人格·使用 lh --persona switch <人格名> 激活"}


# ============================================================
# CLI
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🐉 龍魂·人格矩阵运行时引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh --persona list                 列出所有人格
  lh --persona switch P01           切换到诸葛亮
  lh --persona current              查看当前人格
  lh --persona chain P01 --intent 部署  触发部署联动链路
  lh --persona status               查看矩阵状态
  lh --persona memory P01           查看记忆
  lh --persona match "推演部署方案"   触发词匹配
  lh --persona chain-templates      查看预定义联动链路
  lh --persona bridge --message "推演一下"  对话桥单次测试
        """
    )
    sub = parser.add_subparsers(dest="action", help="操作")

    # list
    sub.add_parser("list", help="列出所有人格")

    # switch
    p_sw = sub.add_parser("switch", help="切换到指定人格")
    p_sw.add_argument("identifier", help="人格IPA或名称")
    p_sw.add_argument("--session", help="会话ID（自动创建）")

    # current
    p_cur = sub.add_parser("current", help="查看当前人格")
    p_cur.add_argument("--session", help="会话ID")

    # chain
    p_ch = sub.add_parser("chain", help="触发联动链路")
    p_ch.add_argument("ipa", help="起始人格IPA")
    p_ch.add_argument("--intent", default="处理", help="意图关键词")
    p_ch.add_argument("--session", help="会话ID")

    # status
    sub.add_parser("status", help="查看人格矩阵状态")

    # memory
    p_mem = sub.add_parser("memory", help="查看人格记忆")
    p_mem.add_argument("ipa", help="人格IPA")
    p_mem.add_argument("--key", help="记忆键")
    p_mem.add_argument("--session", help="会话ID")

    # match
    p_mat = sub.add_parser("match", help="触发词匹配")
    p_mat.add_argument("text", help="待匹配文本")
    p_mat.add_argument("--top", type=int, default=3, help="返回数量")

    # chain-templates
    sub.add_parser("chain-templates", help="查看预定义联动链路模板")

    # bridge
    p_br = sub.add_parser("bridge", help="对话桥单次测试")
    p_br.add_argument("--message", required=True, help="用户消息")
    p_br.add_argument("--session", help="会话ID")

    # sync (Notion → 本地)
    sub.add_parser("sync", help="从Notion同步人格(补充模式)")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        return

    runtime = PersonaRuntime()

    if args.action == "list":
        personas = runtime.list_personas()
        print(f"\n📋 人格列表 ({len(personas)} 个)\n")
        print(f"  {'IPA':<6}{'名称':<20}{'层级':<8}{'权重':<6}{'优先':<6}一句话")
        print(f"  {'-'*70}")
        for p in personas:
            print(f"  {p['ipa']:<6}{p['name']:<20}{p.get('layer',''):<8}"
                  f"{p.get('route_weight',''):<6}{p.get('route_priority',''):<6}"
                  f"{p.get('one_liner','')}")

    elif args.action == "switch":
        sid = args.session or runtime.start_session()
        result = runtime.set_current(sid, args.identifier)
        if result.get("status") == "success":
            p = result["persona"]
            print(f"\n✅ 已切换到 {p['name']} ({p['ipa']})")
            print(f"   层级: {p.get('layer','')} | 卦: {p.get('hexagram','')}")
            print(f"   关联: {', '.join(p.get('relations',[]))}")
            print(f"   触发词: {p.get('trigger_words','')}")
            print(f"   {p.get('one_liner','')}")
            # 显示联动链路建议
            linked = runtime.get_linked(p["ipa"])
            if linked:
                print(f"   🔗 可联动: {' → '.join([l['name'] for l in linked])}")
        else:
            print(f"❌ {result.get('message','切换失败')}")

    elif args.action == "current":
        sid = args.session or runtime.start_session()
        p = runtime.get_current(sid)
        if p:
            print(f"\n🧠 当前人格: {p['name']} ({p['ipa']})")
            print(f"   层级: {p.get('layer','')} | {p.get('one_liner','')}")
        else:
            print("❌ 未激活人格")

    elif args.action == "chain":
        sid = args.session or runtime.start_session()
        result = runtime.trigger_chain(sid, args.ipa, args.intent)
        if result.get("status") == "success":
            print(f"\n🔗 联动链路 (意图: {args.intent})")
            print(f"   {' → '.join([c['name'] for c in result['chain']])}")
            print(f"   共 {len(result['chain'])} 个人格参与")
        else:
            print(f"❌ {result.get('message','联动失败')}")

    elif args.action == "status":
        s = runtime.status()
        print(f"\n📊 人格矩阵状态")
        print(f"   总人格: {s['total_personas']}")
        for layer, count in s["layers"].items():
            print(f"     {layer}: {count}人")
        print(f"   活跃会话: {s['active_sessions']}")
        print(f"   记忆条目: {s['memory_entries']}")
        print(f"   最后同步: {s['last_sync']}")

    elif args.action == "memory":
        sid = args.session or runtime.start_session()
        mems = runtime.recall(sid, args.ipa, args.key)
        print(f"\n🧠 人格记忆: {args.ipa}")
        print(f"   ({len(mems)} 条)\n")
        for m in mems[:20]:
            val_preview = m["value"][:80] + "..." if len(m["value"]) > 80 else m["value"]
            print(f"   [{m['key']}] {val_preview}")

    elif args.action == "match":
        matches = runtime.match(args.text, args.top)
        print(f"\n🎯 触发词匹配: \"{args.text}\"")
        if matches:
            for i, p in enumerate(matches, 1):
                print(f"   {i}. {p['name']} ({p['ipa']}) — {p.get('one_liner','')}")
        else:
            print("   未匹配到人格")

    elif args.action == "chain-templates":
        print(f"\n🔗 预定义联动链路模板 ({len(CHAIN_TEMPLATES)} 条)\n")
        for keyword, codes in sorted(CHAIN_TEMPLATES.items()):
            names = []
            for c in codes:
                p = runtime.get_persona(c)
                names.append(p["name"] if p else c)
            print(f"   {keyword:<6} → {' → '.join(names)}")

    elif args.action == "bridge":
        sid = args.session or runtime.start_session()
        bridge = PersonaBridge(runtime)
        result = bridge.handle(sid, args.message)
        print(f"\n💬 对话桥")
        print(f"   [{result['type']}] {result['message']}")
        if "persona" in result:
            p = result["persona"]
            print(f"   人格: {p['name']} ({p['ipa']})")
        if "chain" in result:
            print(f"   链路: {' → '.join([c['name'] for c in result['chain']['chain']])}")

    elif args.action == "sync":
        print("📡 Notion同步暂用 --persona-sync 命令，此入口为占位。")
        print("   使用: lh --persona-sync sync")


if __name__ == "__main__":
    main()
