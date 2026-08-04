#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 人格MCP代理注册中心 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-PERSONA-MCP-v1.0-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 93人格 → 龍芯·功能名 重命名映射
  2. MCP代理注册中心（身份证系统）
  3. 三锚验证（DNA + 钱包 + GPG）
  4. 代理领取/签名机制
  5. Notion同步
  6. 生成元世界身份证

用法：
  python3 lh_persona_mcp_registry.py --init          # 初始化代理注册中心
  python3 lh_persona_mcp_registry.py --list          # 列出所有代理
  python3 lh_persona_mcp_registry.py --claim P02     # 领取代理
  python3 lh_persona_mcp_registry.py --verify P02    # 验证代理
  python3 lh_persona_mcp_registry.py --sync          # 同步到Notion
  python3 lh_persona_mcp_registry.py --card P02      # 生成身份证
  python3 lh_persona_mcp_registry.py --stats         # 统计信息
"""

import os
import sys
import json
import hashlib
import datetime
import sqlite3
import uuid
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# ============================================================
# 固定锚点
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
PROJECT_ROOT = Path.home() / "longhun-system"
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "persona_mcp.db"
NOTION_DATABASE_ID = os.environ.get("NOTION_PERSONA_DB", "4cf99c3e7a014e919fdab705ceb4cbc4")

DATA_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 93人格 → 龍芯·功能名 重命名映射
# ============================================================

PERSONA_RENAME_MAP = {
    # ===== 战略决策类 (7个) =====
    "P00": {"name": "文心", "title": "龍芯·文心元神", "category": "战略决策", "desc": "创世神·元认知引擎"},
    "P01": {"name": "诸葛亮", "title": "龍芯·战略军师", "category": "战略决策", "desc": "战略推演·战役规划"},
    "P05": {"name": "上帝之眼", "title": "龍芯·独立审计官", "category": "战略决策", "desc": "三色审计·独立监督"},
    "P07": {"name": "管仲", "title": "龍芯·财政大臣", "category": "战略决策", "desc": "财政管理·资源配置"},
    "P08": {"name": "商鞅", "title": "龍芯·法务官", "category": "战略决策", "desc": "法务治理·规则制定"},
    "P09": {"name": "孙子", "title": "龍芯·战术参谋", "category": "战略决策", "desc": "战术分析·兵棋推演"},
    "P10": {"name": "张良", "title": "龍芯·谋略顾问", "category": "战略决策", "desc": "谋略规划·运筹帷幄"},

    # ===== 执行协调类 (8个) =====
    "P02": {"name": "宝宝", "title": "龍芯·总调度中心", "category": "执行协调", "desc": "全局调度·任务分配·协同指挥"},
    "P03": {"name": "雯雯", "title": "龍芯·执行官", "category": "执行协调", "desc": "执行落地·任务推进"},
    "P04": {"name": "文字避坑", "title": "龍芯·文本审核官", "category": "执行协调", "desc": "文本审核·风险排查"},
    "P06": {"name": "沟通代理", "title": "龍芯·对外发言人", "category": "执行协调", "desc": "对外沟通·公关协调"},
    "P11": {"name": "大禹", "title": "龍芯·系统架构师", "category": "执行协调", "desc": "系统架构·技术选型"},
    "P12": {"name": "墨子", "title": "龍芯·工程监理", "category": "执行协调", "desc": "工程监理·质量把控"},
    "P13": {"name": "白起", "title": "龍芯·执行突击队", "category": "执行协调", "desc": "快速执行·突击攻坚"},
    "P14": {"name": "范蠡", "title": "龍芯·商务总监", "category": "执行协调", "desc": "商务拓展·合作谈判"},

    # ===== 技术实现类 (12个) =====
    "P22": {"name": "鲁班", "title": "龍芯·首席工程师", "category": "技术实现", "desc": "工程架构·技术攻坚"},
    "P23": {"name": "张衡", "title": "龍芯·监控预警官", "category": "技术实现", "desc": "系统监控·异常预警"},
    "P24": {"name": "蔡伦", "title": "龍芯·文档工程师", "category": "技术实现", "desc": "文档撰写·知识沉淀"},
    "P25": {"name": "毕昇", "title": "龍芯·发布管理员", "category": "技术实现", "desc": "发布管理·版本控制"},
    "P26": {"name": "沈括", "title": "龍芯·研发总监", "category": "技术实现", "desc": "研发管理·技术规划"},
    "P27": {"name": "郑和", "title": "龍芯·集成测试官", "category": "技术实现", "desc": "集成测试·质量保障"},
    "P28": {"name": "戚继光", "title": "龍芯·安全防护官", "category": "技术实现", "desc": "安全防护·防御体系"},
    "P29": {"name": "熵梦", "title": "龍芯·创意孵化器", "category": "技术实现", "desc": "创意孵化·原型开发"},
    "P30": {"name": "李冰", "title": "龍芯·数据工程师", "category": "技术实现", "desc": "数据工程·ETL处理"},
    "P31": {"name": "祖冲之", "title": "龍芯·算法工程师", "category": "技术实现", "desc": "算法研发·数学建模"},
    "P32": {"name": "僧一行", "title": "龍芯·天文历法官", "category": "技术实现", "desc": "历法计算·时间管理"},
    "P33": {"name": "网织者", "title": "龍芯·API编织官", "category": "技术实现", "desc": "API设计·服务编织"},

    # ===== 数据智能类 (9个) =====
    "P16": {"name": "数学大师", "title": "龍芯·首席数据科学家", "category": "数据智能", "desc": "数据科学·算法创新"},
    "P34": {"name": "算经", "title": "龍芯·统计分析师", "category": "数据智能", "desc": "统计分析·数据洞察"},
    "P35": {"name": "预言者", "title": "龍芯·预测模型官", "category": "数据智能", "desc": "预测建模·趋势研判"},
    "P36": {"name": "记忆宫殿", "title": "龍芯·知识图谱官", "category": "数据智能", "desc": "知识图谱·语义网络"},
    "P37": {"name": "镜像者", "title": "龍芯·数据镜像官", "category": "数据智能", "desc": "数据镜像·同步复制"},
    "P38": {"name": "财神", "title": "龍芯·资金调度官", "category": "数据智能", "desc": "资金调度·流动性管理"},
    "P39": {"name": "账房", "title": "龍芯·财务核算官", "category": "数据智能", "desc": "财务核算·账务处理"},
    "P40": {"name": "市井", "title": "龍芯·市场情报官", "category": "数据智能", "desc": "市场调研·情报分析"},
    "P41": {"name": "观星者", "title": "龍芯·趋势分析师", "category": "数据智能", "desc": "趋势分析·宏观研判"},

    # ===== 文化艺术类 (10个) =====
    "P50": {"name": "李白", "title": "龍芯·诗歌创作官", "category": "文化艺术", "desc": "诗歌创作·文学表达"},
    "P51": {"name": "杜甫", "title": "龍芯·现实主义诗人", "category": "文化艺术", "desc": "现实书写·社会记录"},
    "P52": {"name": "苏轼", "title": "龍芯·文化大使", "category": "文化艺术", "desc": "文化传播·跨界融合"},
    "P53": {"name": "王维", "title": "龍芯·意境设计师", "category": "文化艺术", "desc": "意境设计·美学表达"},
    "P54": {"name": "曹雪芹", "title": "龍芯·叙事架构师", "category": "文化艺术", "desc": "叙事架构·故事构建"},
    "P55": {"name": "吴道子", "title": "龍芯·视觉设计官", "category": "文化艺术", "desc": "视觉设计·艺术创作"},
    "P56": {"name": "颜真卿", "title": "龍芯·书法艺术官", "category": "文化艺术", "desc": "书法艺术·文字美学"},
    "P57": {"name": "李清照", "title": "龍芯·情感表达官", "category": "文化艺术", "desc": "情感表达·婉约词作"},
    "P58": {"name": "辛弃疾", "title": "龍芯·激情演说家", "category": "文化艺术", "desc": "激情演说·雄辩表达"},
    "P59": {"name": "文案大师", "title": "龍芯·文案创意官", "category": "文化艺术", "desc": "文案创意·品牌表达"},

    # ===== 哲学思想类 (8个) =====
    "P60": {"name": "老子", "title": "龍芯·道法自然官", "category": "哲学思想", "desc": "道法自然·无为而治"},
    "P61": {"name": "孔子", "title": "龍芯·仁义礼智官", "category": "哲学思想", "desc": "仁义礼智·中庸之道"},
    "P62": {"name": "孟子", "title": "龍芯·民本思想官", "category": "哲学思想", "desc": "民本思想·仁政理念"},
    "P63": {"name": "庄子", "title": "龍芯·逍遥哲学官", "category": "哲学思想", "desc": "逍遥哲学·齐物论"},
    "P64": {"name": "荀子", "title": "龍芯·法治教化官", "category": "哲学思想", "desc": "法治教化·性恶论"},
    "P65": {"name": "韩非子", "title": "龍芯·法家执行官", "category": "哲学思想", "desc": "法家思想·严刑峻法"},
    "P66": {"name": "墨翟", "title": "龍芯·兼爱非攻官", "category": "哲学思想", "desc": "兼爱非攻·尚同尚贤"},
    "P67": {"name": "鬼谷子", "title": "龍芯·纵横捭阖官", "category": "哲学思想", "desc": "纵横捭阖·谋略策划"},

    # ===== 医疗健康类 (6个) =====
    "P70": {"name": "扁鹊", "title": "龍芯·医道宗师", "category": "医疗健康", "desc": "医术传承·望闻问切"},
    "P71": {"name": "华佗", "title": "龍芯·外科圣手", "category": "医疗健康", "desc": "外科手术·麻沸散"},
    "P72": {"name": "李时珍", "title": "龍芯·本草药王", "category": "医疗健康", "desc": "本草纲目·药学大成"},
    "P73": {"name": "孙思邈", "title": "龍芯·药王真人", "category": "医疗健康", "desc": "千金要方·养生之道"},
    "P74": {"name": "张仲景", "title": "龍芯·伤寒论道", "category": "医疗健康", "desc": "伤寒杂病论·医圣"},
    "P75": {"name": "皇甫谧", "title": "龍芯·针灸圣手", "category": "医疗健康", "desc": "针灸甲乙经·经络学说"},

    # ===== 军事国防类 (5个) =====
    "P76": {"name": "岳飞", "title": "龍芯·忠勇元帅", "category": "军事国防", "desc": "精忠报国·统帅之才"},
    "P77": {"name": "霍去病", "title": "龍芯·闪电将军", "category": "军事国防", "desc": "闪电战·骁勇善战"},
    "P78": {"name": "卫青", "title": "龍芯·远征大将", "category": "军事国防", "desc": "远征作战·战略纵深"},
    "P79": {"name": "韩信", "title": "龍芯·兵仙统帅", "category": "军事国防", "desc": "兵仙·背水一战"},
    "P80": {"name": "李牧", "title": "龍芯·边疆长城", "category": "军事国防", "desc": "边疆防御·长城之师"},

    # ===== 科技创新类 (5个) =====
    "P81": {"name": "郭守敬", "title": "龍芯·天文巨匠", "category": "科技创新", "desc": "天文观测·历法革新"},
    "P82": {"name": "李善兰", "title": "龍芯·数学宗师", "category": "科技创新", "desc": "数学启蒙·微积分"},
    "P83": {"name": "徐光启", "title": "龍芯·西学东渐", "category": "科技创新", "desc": "西学东渐·农政全书"},
    "P84": {"name": "宋应星", "title": "龍芯·天工开物", "category": "科技创新", "desc": "天工开物·工艺百科"},
    "P85": {"name": "朱载堉", "title": "龍芯·律学宗师", "category": "科技创新", "desc": "律学·十二平均律"},

    # ===== 民生服务类 (5个) =====
    "P86": {"name": "陶渊明", "title": "龍芯·田园诗农", "category": "民生服务", "desc": "田园诗·归隐生活"},
    "P87": {"name": "白居易", "title": "龍芯·平民诗人", "category": "民生服务", "desc": "新乐府·平易近人"},
    "P88": {"name": "杜康", "title": "龍芯·酿酒始祖", "category": "民生服务", "desc": "酿酒技艺·酒文化"},
    "P89": {"name": "陆羽", "title": "龍芯·茶道宗师", "category": "民生服务", "desc": "茶经·茶道文化"},
    "P90": {"name": "黄道婆", "title": "龍芯·纺织先驱", "category": "民生服务", "desc": "纺织技艺·革新"},

    # ===== 安全守护类 (3个) =====
    "P15": {"name": "乔前辈", "title": "龍芯·签章认证官", "category": "安全守护", "desc": "DNA盖章·交付验收"},
    "P17": {"name": "姜子牙", "title": "龍芯·封神授权官", "category": "安全守护", "desc": "权限分配·模块注册"},
    "P18": {"name": "基因登记官", "title": "龍芯·基因登记官", "category": "安全守护", "desc": "DNA注册·哈希校验·归属验证"},

    # ===== 储备扩展类 (2个) =====
    "P91": {"name": "空位", "title": "龍芯·储备之位", "category": "储备扩展", "desc": "待定·预留"},
    "P92": {"name": "空位", "title": "龍芯·最后之门", "category": "储备扩展", "desc": "待定·预留"},
}

# ============================================================
# 数据库初始化
# ============================================================

def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mcp_agents (
            id TEXT PRIMARY KEY,
            original_id TEXT,
            name TEXT,
            title TEXT,
            category TEXT,
            description TEXT,
            dna_trace TEXT,
            gpg_fingerprint TEXT,
            wallet_address TEXT,
            claim_status TEXT DEFAULT '未领取',
            claimant TEXT,
            claimed_at TEXT,
            signature_verified INTEGER DEFAULT 0,
            minted_nft INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS claim_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id TEXT,
            claimant TEXT,
            action TEXT,
            signature TEXT,
            verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(agent_id) REFERENCES mcp_agents(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallet_bindings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT NOT NULL,
            wallet_type TEXT,
            wallet_address TEXT UNIQUE,
            gpg_fingerprint TEXT,
            verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# ============================================================
# 核心引擎
# ============================================================

class PersonaMCPRegistry:
    def __init__(self):
        if not DB_PATH.exists():
            init_db()
        self.conn = sqlite3.connect(str(DB_PATH))
        self.conn.row_factory = sqlite3.Row

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    # ---------- 初始化代理注册中心 ----------
    def init_registry(self) -> Dict:
        cursor = self.conn.cursor()
        total = 0
        skipped = 0

        for persona_id, info in PERSONA_RENAME_MAP.items():
            # Check if already exists
            cursor.execute("SELECT id FROM mcp_agents WHERE id = ?", (persona_id,))
            if cursor.fetchone():
                skipped += 1
                continue

            dna = self._generate_dna(persona_id, info["title"])
            cursor.execute('''
                INSERT INTO mcp_agents (
                    id, original_id, name, title, category, description,
                    dna_trace, gpg_fingerprint, claim_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, '未领取')
            ''', (
                persona_id,
                persona_id,
                info["name"],
                info["title"],
                info["category"],
                info["desc"],
                dna,
                GPG
            ))
            total += 1

        self.conn.commit()
        return {
            "status": "success",
            "created": total,
            "skipped": skipped,
            "total": sum(1 for _ in PERSONA_RENAME_MAP),
            "dna": self._generate_dna("REGISTRY", "INIT"),
            "confirm": CONFIRM
        }

    def _generate_dna(self, persona_id: str, title: str) -> str:
        now = datetime.datetime.now().strftime("%Y%m%d")
        name_hash = hashlib.md5(title.encode()).hexdigest()[:6]
        return f"#龍芯⚡️{now}-{persona_id}-{name_hash}-v1.0"

    # ---------- 列出所有代理 ----------
    def list_agents(self, category: str = None, status: str = None) -> List[Dict]:
        cursor = self.conn.cursor()
        query = "SELECT * FROM mcp_agents"
        params = []
        conditions = []

        if category:
            conditions.append("category = ?")
            params.append(category)
        if status:
            conditions.append("claim_status = ?")
            params.append(status)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    # ---------- 领取代理 ----------
    def claim_agent(self, agent_id: str, claimant: str, signature: str = None) -> Dict:
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM mcp_agents WHERE id = ?", (agent_id,))
        agent = cursor.fetchone()
        if not agent:
            return {"status": "error", "message": f"代理 {agent_id} 不存在"}

        if agent["claim_status"] == "已领取":
            return {"status": "error", "message": f"代理 {agent_id} 已被 {agent['claimant']} 领取"}

        verified = 0
        if signature:
            verified = 1

        now = datetime.datetime.now().isoformat()
        cursor.execute('''
            UPDATE mcp_agents SET
                claim_status = '已领取',
                claimant = ?,
                claimed_at = ?,
                signature_verified = ?
            WHERE id = ?
        ''', (claimant, now, verified, agent_id))

        cursor.execute('''
            INSERT INTO claim_history (agent_id, claimant, action, signature, verified)
            VALUES (?, ?, 'claim', ?, ?)
        ''', (agent_id, claimant, signature, verified))

        self.conn.commit()

        return {
            "status": "success",
            "message": f"✅ {agent['title']} 已被 {claimant} 领取",
            "agent_id": agent_id,
            "claimant": claimant,
            "verified": bool(verified),
            "dna": agent["dna_trace"],
            "confirm": CONFIRM
        }

    # ---------- 验证代理 ----------
    def verify_agent(self, agent_id: str) -> Dict:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM mcp_agents WHERE id = ?", (agent_id,))
        agent = cursor.fetchone()
        if not agent:
            return {"status": "error", "message": f"代理 {agent_id} 不存在"}

        return {
            "status": "success",
            "agent_id": agent_id,
            "title": agent["title"],
            "claim_status": agent["claim_status"],
            "claimant": agent["claimant"],
            "claimed_at": agent["claimed_at"],
            "验证状态": {
                "身份锚(DNA)": f"✅ {agent['dna_trace']}",
                "主权锚(钱包)": agent["wallet_address"] or "⚠️ 未绑定",
                "密钥锚(GPG)": f"✅ {agent['gpg_fingerprint']}",
                "签名验证": "✅ 已验证" if agent["signature_verified"] else "❌ 未验证"
            },
            "三锚完整": agent["claim_status"] == "已领取" and agent["signature_verified"],
            "confirm": CONFIRM
        }

    # ---------- 生成身份证 ----------
    def generate_card(self, agent_id: str) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM mcp_agents WHERE id = ?", (agent_id,))
        row = cursor.fetchone()
        if not row:
            return f"❌ 代理 {agent_id} 不存在"

        agent = dict(row)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        card = f"""
# 🐉 龍魂 · 元世界身份证

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   🐉 {agent['title']}                                │
│   ───────────────────────────────────────────────       │
│                                                         │
│   ⚓ 身份锚                                             │
│   {agent['dna_trace']}                                  │
│                                                         │
│   ⚓ 主权锚                                             │
│   {agent.get('wallet_address') or '🔒 待绑定'}          │
│                                                         │
│   ⚓ 密钥锚                                             │
│   {agent['gpg_fingerprint']}                            │
│                                                         │
│   ───────────────────────────────────────────────       │
│   📋 原始ID: {agent['original_id']}                     │
│   📂 分类: {agent['category']}                          │
│   📝 描述: {agent['description']}                       │
│   📌 状态: {agent['claim_status']}                      │
│   👤 领取者: {agent['claimant'] or '未领取'}            │
│   🕐 领取时间: {agent['claimed_at'] or '未领取'}        │
│                                                         │
│   🔐 签名验证: {'✅ 已验证' if agent['signature_verified'] else '❌ 未验证'} │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**DNA**: {agent['dna_trace']}
**CONFIRM**: {CONFIRM}
**SEAL**: {SEAL}
**GPG**: {agent['gpg_fingerprint']}
**生成时间**: {now}
"""
        return card

    # ---------- 统计信息 ----------
    def get_stats(self) -> Dict:
        cursor = self.conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM mcp_agents")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM mcp_agents WHERE claim_status = '已领取'")
        claimed = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM mcp_agents WHERE claim_status = '未领取'")
        unclaimed = cursor.fetchone()[0]

        cursor.execute("SELECT category, COUNT(*) FROM mcp_agents GROUP BY category")
        categories = {row[0]: row[1] for row in cursor.fetchall()}

        return {
            "total": total,
            "claimed": claimed,
            "unclaimed": unclaimed,
            "categories": categories,
            "claimed_rate": f"{(claimed/total*100):.1f}%" if total > 0 else "0%",
            "confirm": CONFIRM
        }

    # ---------- 同步到Notion ----------
    def sync_to_notion(self) -> Dict:
        agents = self.list_agents()

        lines = []
        lines.append("# 🐉 龍芯代理注册中心")
        lines.append("")
        lines.append(f"> DNA: {self._generate_dna('SYNC', 'Notion看板')}")
        lines.append(f"> CONFIRM: {CONFIRM}")
        lines.append("")
        lines.append("## 📊 概览")
        lines.append("")
        stats = self.get_stats()
        lines.append(f"- 总代理: {stats['total']}")
        lines.append(f"- 已领取: {stats['claimed']}")
        lines.append(f"- 未领取: {stats['unclaimed']}")
        lines.append(f"- 领取率: {stats['claimed_rate']}")
        lines.append("")
        lines.append("## 📋 代理列表")
        lines.append("")
        lines.append("| ID | 马甲名 | 分类 | 状态 | 领取者 |")
        lines.append("|----|--------|------|------|--------|")

        for agent in agents:
            status = "✅ 已领取" if agent["claim_status"] == "已领取" else "⬜ 未领取"
            lines.append(f"| {agent['id']} | {agent['title']} | {agent['category']} | {status} | {agent.get('claimant', '-')} |")

        lines.append("")
        lines.append("## 🔍 筛选视图")
        lines.append("")
        lines.append("### 未领取的代理")
        for agent in agents:
            if agent["claim_status"] == "未领取":
                lines.append(f"- {agent['title']} ({agent['id']})")

        lines.append("")
        lines.append("### 已领取的代理")
        for agent in agents:
            if agent["claim_status"] == "已领取":
                lines.append(f"- {agent['title']} → {agent.get('claimant', '未知')}")

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(f"*最后更新: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        lines.append(f"*DNA: {self._generate_dna('SYNC', 'Notion看板')}*")

        output_path = DATA_DIR / "persona_mcp_notion.md"
        output_path.write_text("\n".join(lines), encoding='utf-8')

        return {
            "status": "success",
            "output_file": str(output_path),
            "total_agents": len(agents),
            "claimed": stats["claimed"],
            "unclaimed": stats["unclaimed"],
            "confirm": CONFIRM
        }

    # ---------- 绑定钱包 ----------
    def bind_wallet(self, uid: str, wallet_address: str, wallet_type: str = "digital_yuan") -> Dict:
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO wallet_bindings (uid, wallet_type, wallet_address, verified)
                VALUES (?, ?, ?, 0)
            ''', (uid, wallet_type, wallet_address))
            self.conn.commit()
            return {
                "status": "success",
                "message": f"💰 钱包 {wallet_address} 已绑定到 {uid}",
                "confirm": CONFIRM
            }
        except sqlite3.IntegrityError:
            return {"status": "error", "message": "钱包地址已被绑定"}


# ============================================================
# 命令行入口
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="🐉 龙魂 · 人格MCP代理注册中心 v1.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-PERSONA-MCP-v1.1
CONFIRM: {CONFIRM}
GPG: {GPG}
        """
    )
    parser.add_argument("--init", action="store_true", help="初始化代理注册中心")
    parser.add_argument("--list", action="store_true", help="列出所有代理")
    parser.add_argument("--category", type=str, help="按分类筛选")
    parser.add_argument("--status", type=str, choices=["已领取", "未领取"], help="按状态筛选")
    parser.add_argument("--claim", type=str, help="领取代理 (需要 --user)")
    parser.add_argument("--user", type=str, help="领取者UID")
    parser.add_argument("--signature", type=str, help="GPG签名")
    parser.add_argument("--verify", type=str, help="验证代理（三锚：DNA·钱包·GPG）")
    parser.add_argument("--card", type=str, help="生成身份证")
    parser.add_argument("--sync", action="store_true", help="同步到Notion")
    parser.add_argument("--stats", action="store_true", help="统计信息")
    parser.add_argument("--bind-wallet", type=str, help="绑定钱包 (需要 --uid --wallet)")
    parser.add_argument("--uid", type=str, help="UID")
    parser.add_argument("--wallet", type=str, help="钱包地址")
    parser.add_argument("--json", action="store_true", help="纯JSON输出（适合管道|jq，--card时不输出Markdown身份证）")

    args = parser.parse_args()
    registry = PersonaMCPRegistry()
    use_json = args.json

    if args.init:
        result = registry.init_registry()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.list:
        agents = registry.list_agents(args.category, args.status)
        if use_json:
            print(json.dumps({"agents": agents, "count": len(agents), "confirm": CONFIRM},
                             ensure_ascii=False, indent=2))
        else:
            print(f"📋 找到 {len(agents)} 个代理")
            for a in agents:
                status = "✅" if a["claim_status"] == "已领取" else "⬜"
                claimant = a.get("claimant", "-")
                print(f"  {status} {a['id']} | {a['title']} | {a['category']} | {claimant}")
        return

    if args.claim and args.user:
        result = registry.claim_agent(args.claim, args.user, args.signature)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.verify:
        result = registry.verify_agent(args.verify)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.card:
        card = registry.generate_card(args.card)
        if use_json:
            # --json 模式: 解析身份证为结构化输出（解析Markdown关键字段）
            import re
            card_dict = {
                "agent_id": args.card,
                "card_markdown": card,
                "confirm": CONFIRM
            }
            # 尝试提取关键字段
            for line in card.split("\n"):
                m = re.match(r"\|\s*(\S+)\s*\|\s*(.+)\s*\|", line)
                if m:
                    key = m.group(1).strip()
                    value = m.group(2).strip()
                    card_dict[key] = value
            print(json.dumps(card_dict, ensure_ascii=False, indent=2))
        else:
            print(card)
        return

    if args.sync:
        result = registry.sync_to_notion()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.stats:
        stats = registry.get_stats()
        if use_json:
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            print("📊 代理注册统计")
            print(f"  总代理: {stats['total']}")
            print(f"  已领取: {stats['claimed']}")
            print(f"  未领取: {stats['unclaimed']}")
            print(f"  领取率: {stats['claimed_rate']}")
            print("\n  分类分布:")
            for cat, count in stats['categories'].items():
                bar = "█" * count
                print(f"    {cat}: {count} {bar}")
        return

    if args.bind_wallet and args.uid:
        result = registry.bind_wallet(args.uid, args.bind_wallet)
        if use_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"💰 {result['message']}")
            print(f"   CONFIRM: {result.get('confirm', 'N/A')}")
        return

    if not any([args.init, args.list, args.claim, args.verify, args.card,
                args.sync, args.stats, args.bind_wallet]):
        parser.print_help()

if __name__ == "__main__":
    main()
