#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☴巽-LEARN-ENGINE-v1.0-f7a2c1e9
# 创建者: 诸葛鑫 (UID9622)
# 协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
"""
🐉 龍魂 · 自主学习引擎 v1.0
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☴巽-LEARN-ENGINE-v1.0

功能：
  1. 六大核心数据库管理（Inbox / DNA / Tasks / Signals / Projects / Army）
  2. 自动化管道：净化 → DNA拆解 → 任务生成 → 项目推荐
  3. 趋势绑定（DNA ↔ Future Signals）
  4. 数字大军编制 + 战力评估
  5. 可视化看板（Notion/HTML）

用法：
  lh learn -i                    # 交互模式
  lh learn --add --title "标题"   # 快速添加
  lh learn --run                  # 自动化管道
  lh learn --dashboard            # 生成看板

确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""

import os
import sys
import json
import sqlite3
import hashlib
import datetime
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict

# ============================================================
# 路径 & 常量
# ============================================================
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "bin"))

DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "learning_engine.db"
DASHBOARD_HTML = DATA_DIR / "learning_dashboard.html"

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
DNA = "#龍芯⚡️丙午·乙巳·癸酉·亥时·☴巽-LEARN-ENGINE-v1.0"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 一、数据库初始化
# ============================================================

def init_db():
    """初始化所有数据库表"""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # 1. Learning Inbox — 原始输入
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inbox (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            link TEXT,
            source TEXT DEFAULT '',
            status TEXT DEFAULT '待净化',
            raw_content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            purified_at TIMESTAMP
        )
    ''')

    # 2. Knowledge DNA — 拆解后的知识基因
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dna (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dna_id TEXT UNIQUE NOT NULL,
            direction TEXT,
            core_concept TEXT NOT NULL,
            tech_points TEXT,
            example_code TEXT,
            reusable INTEGER DEFAULT 0,
            difficulty INTEGER DEFAULT 1,
            pollution_index INTEGER DEFAULT 0,
            source_inbox_id INTEGER,
            status TEXT DEFAULT '待理解',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(source_inbox_id) REFERENCES inbox(id)
        )
    ''')

    # 3. Learning Tasks — 自动/手动生成的学习任务
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            related_dna_id INTEGER,
            learning_mode TEXT DEFAULT '扫盲',
            energy_cost TEXT DEFAULT '低',
            status TEXT DEFAULT 'Todo',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY(related_dna_id) REFERENCES dna(id)
        )
    ''')

    # 4. Future Signals — 世界趋势信号
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            signal_name TEXT NOT NULL,
            direction TEXT,
            signal_strength INTEGER DEFAULT 5,
            uncertainty INTEGER DEFAULT 5,
            time_scale TEXT DEFAULT '5年',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 5. Signal-DNA 关联
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS signal_dna (
            signal_id INTEGER,
            dna_id INTEGER,
            PRIMARY KEY(signal_id, dna_id),
            FOREIGN KEY(signal_id) REFERENCES signals(id),
            FOREIGN KEY(dna_id) REFERENCES dna(id)
        )
    ''')

    # 6. Projects — 实验项目
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            problem_statement TEXT,
            maturity TEXT DEFAULT '构思',
            scalable INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 7. Project-DNA 关联
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_dna (
            project_id INTEGER,
            dna_id INTEGER,
            PRIMARY KEY(project_id, dna_id),
            FOREIGN KEY(project_id) REFERENCES projects(id),
            FOREIGN KEY(dna_id) REFERENCES dna(id)
        )
    ''')

    # 8. Digital Army — 数字大军编制
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS army (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_name TEXT NOT NULL,
            capability_source TEXT,
            expertise TEXT,
            problem_type TEXT,
            combat_power INTEGER DEFAULT 1,
            dna_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(dna_id) REFERENCES dna(id)
        )
    ''')

    # 索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_inbox_status ON inbox(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_dna_direction ON dna(direction)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_army_dna ON army(dna_id)')

    conn.commit()
    conn.close()
    return str(DB_PATH)

# ============================================================
# 二、工具函数
# ============================================================

def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def generate_dna_id(core_concept: str, direction: str = "未知") -> str:
    """生成唯一 DNA-ID"""
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    raw = f"{direction}{core_concept}{ts}"
    h = hashlib.md5(raw.encode()).hexdigest()[:8]
    return f"DNA-{direction[:2].upper()}-{h}"

# ============================================================
# 三、Inbox 操作
# ============================================================

def add_inbox(title: str, type_: str = "Website", link: str = "",
              raw_content: str = "", source: str = "") -> int:
    """添加学习资源到 Inbox"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO inbox (title, type, link, raw_content, source, status)
           VALUES (?, ?, ?, ?, ?, '待净化')""",
        (title, type_, link, raw_content, source)
    )
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id

def list_inbox(status: str = None, limit: int = 50) -> List[Dict]:
    """列出 Inbox 条目"""
    conn = get_db()
    if status:
        rows = conn.execute(
            "SELECT * FROM inbox WHERE status = ? ORDER BY created_at DESC LIMIT ?",
            (status, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM inbox ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_inbox(inbox_id: int) -> Optional[Dict]:
    """获取单个 Inbox 条目"""
    conn = get_db()
    row = conn.execute("SELECT * FROM inbox WHERE id = ?", (inbox_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

# ============================================================
# 四、DNA 操作
# ============================================================

def create_dna(inbox_id: int, core_concept: str, direction: str = "未知",
               tech_points: str = "", example_code: str = "",
               reusable: bool = False, difficulty: int = 1,
               pollution_index: int = 0) -> Dict:
    """
    净化 Inbox 条目，自动拆解 DNA 并生成学习任务。
    返回: {inbox_id, dna_id, dna_row_id, task_id, status}
    """
    conn = get_db()

    # 更新 inbox 状态
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE inbox SET status = '已净化', purified_at = CURRENT_TIMESTAMP WHERE id = ?",
        (inbox_id,)
    )
    if cursor.rowcount == 0:
        conn.close()
        return {"error": f"Inbox #{inbox_id} 不存在"}

    # 创建 DNA
    dna_id = generate_dna_id(core_concept, direction)
    cursor.execute('''
        INSERT INTO dna (dna_id, direction, core_concept, tech_points, example_code,
                         reusable, difficulty, pollution_index, source_inbox_id, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, '待理解')
    ''', (dna_id, direction, core_concept, tech_points, example_code,
          1 if reusable else 0, difficulty, pollution_index, inbox_id))
    dna_row_id = cursor.lastrowid
    conn.commit()

    # 自动生成学习任务
    task_id = add_task(
        task_name=f"理解 {core_concept}",
        dna_id=dna_row_id,
        mode="扫盲" if difficulty <= 2 else "精读" if difficulty <= 4 else "攻坚"
    )

    conn.close()

    return {
        "inbox_id": inbox_id,
        "dna_id": dna_id,
        "dna_row_id": dna_row_id,
        "task_id": task_id,
        "status": "purified"
    }

def list_dna(direction: str = None, limit: int = 100) -> List[Dict]:
    """列出 DNA"""
    conn = get_db()
    if direction:
        rows = conn.execute(
            "SELECT * FROM dna WHERE direction = ? ORDER BY created_at DESC LIMIT ?",
            (direction, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM dna ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_dna(identifier) -> Optional[Dict]:
    """按 row id 或 dna_id 查 DNA"""
    conn = get_db()
    if str(identifier).startswith("DNA-"):
        row = conn.execute("SELECT * FROM dna WHERE dna_id = ?", (identifier,)).fetchone()
    else:
        row = conn.execute("SELECT * FROM dna WHERE id = ?", (int(identifier),)).fetchone()
    conn.close()
    return dict(row) if row else None

# ============================================================
# 五、Tasks 操作
# ============================================================

def add_task(task_name: str, dna_id: int, mode: str = "扫盲",
             energy: str = "低") -> int:
    """生成学习任务"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO tasks (task_name, related_dna_id, learning_mode, energy_cost, status)
           VALUES (?, ?, ?, ?, 'Todo')""",
        (task_name, dna_id, mode, energy)
    )
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id

def list_tasks(status: str = None, limit: int = 50) -> List[Dict]:
    """列出任务"""
    conn = get_db()
    if status:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC LIMIT ?",
            (status, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM tasks ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def complete_task(task_id: int) -> Dict:
    """标记任务完成"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET status = 'Done', completed_at = CURRENT_TIMESTAMP WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return {"status": "completed", "task_id": task_id} if affected else {"error": "任务不存在"}

# ============================================================
# 六、Signals 操作
# ============================================================

def add_signal(name: str, direction: str = "未知", strength: int = 5,
               uncertainty: int = 5, scale: str = "5年") -> int:
    """添加趋势信号"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO signals (signal_name, direction, signal_strength, uncertainty, time_scale)
           VALUES (?, ?, ?, ?, ?)""",
        (name, direction, strength, uncertainty, scale)
    )
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id

def bind_signal_dna(signal_id: int, dna_id: int):
    """绑定信号与 DNA"""
    conn = get_db()
    conn.execute("INSERT OR IGNORE INTO signal_dna (signal_id, dna_id) VALUES (?, ?)",
                 (signal_id, dna_id))
    conn.commit()
    conn.close()

def list_signals(limit: int = 50) -> List[Dict]:
    """列出趋势信号"""
    conn = get_db()
    rows = conn.execute("SELECT * FROM signals ORDER BY created_at DESC LIMIT ?",
                        (limit,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ============================================================
# 七、Army 操作
# ============================================================

def add_army(role: str, dna_id: int, expertise: str = "",
             problem_type: str = "") -> int:
    """编制数字兵种"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO army (role_name, dna_id, expertise, problem_type, combat_power)
           VALUES (?, ?, ?, ?, 1)""",
        (role, dna_id, expertise, problem_type)
    )
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id

def list_army(limit: int = 50) -> List[Dict]:
    """列出数字大军"""
    conn = get_db()
    rows = conn.execute(
        """SELECT a.*, d.core_concept, d.direction
           FROM army a LEFT JOIN dna d ON a.dna_id = d.id
           ORDER BY a.combat_power DESC LIMIT ?""",
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ============================================================
# 八、Projects 操作
# ============================================================

def add_project(name: str, problem: str = "", maturity: str = "构思",
                scalable: bool = False) -> int:
    """添加实验项目"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO projects (project_name, problem_statement, maturity, scalable)
           VALUES (?, ?, ?, ?)""",
        (name, problem, maturity, 1 if scalable else 0)
    )
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id

def bind_project_dna(project_id: int, dna_id: int):
    """绑定项目与 DNA"""
    conn = get_db()
    conn.execute("INSERT OR IGNORE INTO project_dna (project_id, dna_id) VALUES (?, ?)",
                 (project_id, dna_id))
    conn.commit()
    conn.close()

# ============================================================
# 九、自动化管道
# ============================================================

def run_pipeline(interactive_input: bool = True):
    """
    自动化管道：检查待净化 inbox → 引导拆解 DNA → 自动生成任务
    """
    items = list_inbox(status="待净化")
    if not items:
        print("📭 没有待净化的内容")
        return []

    results = []
    print(f"\n📥 发现 {len(items)} 条待净化内容\n")

    for item in items:
        print(f"[{item['id']}] {item['title']} ({item['type']})")
        if item.get('link'):
            print(f"    链接: {item['link']}")
        if item.get('raw_content'):
            preview = item['raw_content'][:120].replace('\n', ' ')
            print(f"    预览: {preview}...")
        print()

        if interactive_input:
            core = input("  核心概念: ").strip()
            if not core:
                print("  跳过\n")
                continue
            direction = input("  方向 (AI/Web/元宇宙/系统/哲学/未知): ").strip() or "未知"
            tech = input("  技术点 (逗号分隔): ").strip()
            example = input("  示例代码 (可选): ").strip()
            reusable = input("  可复用? (y/n): ").strip().lower() == 'y'
            try:
                difficulty = int(input("  难度 (1-5): ").strip() or "1")
            except ValueError:
                difficulty = 1
            try:
                pollution = int(input("  污染指数 (0-10): ").strip() or "0")
            except ValueError:
                pollution = 0

            result = create_dna(item['id'], core, direction, tech, example,
                                reusable, difficulty, pollution)
        else:
            # 非交互模式：自动根据标题生成基础DNA
            result = create_dna(item['id'], item['title'], "未知", "", "",
                                False, 1, 0)

        if 'error' not in result:
            print(f"  ✅ 净化完成 → DNA: {result['dna_id']} | 任务: #{result['task_id']}\n")
            results.append(result)
        else:
            print(f"  ❌ {result['error']}\n")

    print(f"🎯 管道完成: {len(results)}/{len(items)} 条净化")
    return results

# ============================================================
# 九-B、AI 自动拆解（规则回退 + LLM 可选）
# ============================================================

def _extract_dna_with_rules(content: str, title: str) -> Dict:
    """基于规则的 DNA 提取（无 LLM 时回退）"""
    direction_keywords = {
        "AI": ["AI", "LLM", "模型", "训练", "推理", "agent", "多模态", "transformer"],
        "Web": ["Web", "前端", "后端", "API", "HTTP", "浏览器", "JavaScript", "HTML"],
        "元宇宙": ["元宇宙", "虚拟", "空间计算", "3D", "AR", "VR", "数字人"],
        "系统": ["系统", "架构", "分布式", "微服务", "Kubernetes", "容器"],
        "哲学": ["哲学", "伦理", "道德", "存在", "意识", "认知"],
    }
    direction = "未知"
    for dir_name, keywords in direction_keywords.items():
        if any(kw in content or kw in title for kw in keywords):
            direction = dir_name
            break

    tech_patterns = [r'(\w+)\s*框架', r'(\w+)\s*引擎', r'(\w+)\s*算法',
                     r'(\w+)\s*协议', r'(\w+)\s*模型', r'(\w+)\s*架构']
    tech_points = []
    for pat in tech_patterns:
        tech_points.extend(re.findall(pat, content))

    difficulty = 1
    if len(content) > 1000:
        difficulty = 3
    if any(kw in content for kw in ["数学", "推导", "证明", "定理"]):
        difficulty = 4
    if any(kw in content for kw in ["量子", "黎曼", "拓扑", "微分"]):
        difficulty = 5

    pollution = 0
    for kw in ["震惊", "惊艳", "颠覆", "革命性", "全球首发", "独家"]:
        if kw in content:
            pollution += 2
    pollution = min(10, pollution)

    return {
        "core_concept": title or "未命名知识",
        "direction": direction,
        "tech_points": ",".join(tech_points[:5]),
        "example_code": "",
        "reusable": len(tech_points) > 0,
        "difficulty": difficulty,
        "pollution_index": pollution
    }

def auto_digest_inbox(inbox_id: int = None, use_llm: bool = False) -> Dict:
    """
    自动拆解 Inbox 条目。
    - 有 LLM API 且 use_llm=True → LLM 提取
    - 否则 → 规则回退
    """
    if inbox_id:
        items = [get_inbox(inbox_id)]
        if items[0] is None:
            return {"error": f"Inbox #{inbox_id} 不存在"}
    else:
        items = list_inbox(status="待净化", limit=1)
        if not items:
            return {"status": "no_items", "message": "没有待净化条目"}

    item = items[0]
    content = item.get('raw_content', '')
    title = item.get('title', '')

    # 尝试 LLM 提取
    dna_info = None
    if use_llm:
        dna_info = _try_llm_extract(content, title)
    if not dna_info:
        dna_info = _extract_dna_with_rules(content, title)

    result = create_dna(
        item['id'], dna_info['core_concept'], dna_info['direction'],
        dna_info['tech_points'], dna_info['example_code'],
        dna_info['reusable'], dna_info['difficulty'], dna_info['pollution_index']
    )
    return {"status": "digested", "inbox_id": item['id'], "dna_info": dna_info, "result": result}

def _try_llm_extract(content: str, title: str) -> Optional[Dict]:
    """尝试用 LLM 提取 DNA，失败返回 None"""
    api_key = os.environ.get("LLM_API_KEY", "")
    api_base = os.environ.get("LLM_API_BASE", "https://api.moonshot.cn/v1")
    model = os.environ.get("LLM_MODEL", "moonshot-v1-8k")
    if not api_key or not content.strip():
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=api_base)
        prompt = f"""分析以下内容，提取知识DNA。返回纯JSON（不要markdown代码块）：

标题: {title}
内容: {content[:2000]}

提取字段：
- core_concept: 核心概念（一句话）
- direction: 所属方向（AI/Web/元宇宙/系统/哲学/未知）
- tech_points: 技术点（逗号分隔，最多5个）
- example_code: 代码示例或伪代码（如果有）
- reusable: 是否可复用（true/false）
- difficulty: 难度等级（1-5）
- pollution_index: 污染指数（0-10，营销水份越高分越高）"""

        resp = client.chat.completions.create(
            model=model, temperature=0.3, max_tokens=500,
            messages=[{"role": "system", "content": "你是知识萃取专家。"},
                      {"role": "user", "content": prompt}]
        )
        text = resp.choices[0].message.content.strip()
        m = re.search(r'\{[\s\S]*\}', text)
        if m:
            data = json.loads(m.group())
            return {
                "core_concept": data.get("core_concept", title),
                "direction": data.get("direction", "未知"),
                "tech_points": data.get("tech_points", ""),
                "example_code": data.get("example_code", ""),
                "reusable": data.get("reusable", False),
                "difficulty": min(5, max(1, int(data.get("difficulty", 1)))),
                "pollution_index": min(10, max(0, int(data.get("pollution_index", 0))))
            }
    except ImportError:
        pass
    except Exception as e:
        print(f"  ⚠️ LLM 提取失败: {e}")
    return None

# ============================================================
# 十、趋势自动绑定
# ============================================================

SIGNAL_KEYWORDS = {
    "AGI / 大模型瓶颈": ["LLM", "大模型", "AGI", "通用AI", "推理", "Scaling", "算力"],
    "AI 对齐 & 安全": ["对齐", "安全", "价值观", "Alignment", "Safety", "伦理"],
    "Agent 社会": ["Agent", "智能体", "协作", "自治"],
    "数字人 / 虚拟文明": ["数字人", "虚拟人", "文明", "元宇宙", "化身"],
    "3D Web / 空间计算": ["3D", "空间计算", "WebXR", "三维", "虚拟"],
    "算力 / 能源极限": ["算力", "能源", "功耗", "芯片", "GPU", "能耗"],
    "人机融合": ["脑机", "BCI", "人机", "神经", "增强"],
    "去中心化 vs 平台化": ["去中心化", "Web3", "区块链", "DAI", "主权"],
    "新生产关系": ["生产关系", "数字劳动", "平台", "创作者", "价值分配"],
}

def auto_bind_signals() -> Dict:
    """自动将 DNA 绑定到趋势信号"""
    conn = get_db()
    dna_rows = conn.execute(
        "SELECT id, dna_id, direction, core_concept, tech_points FROM dna"
    ).fetchall()

    bound_count = 0
    for dna in dna_rows:
        text = f"{dna['direction'] or ''} {dna['core_concept'] or ''} {dna['tech_points'] or ''}"
        for signal_name, keywords in SIGNAL_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                sig_row = conn.execute(
                    "SELECT id FROM signals WHERE signal_name = ?", (signal_name,)
                ).fetchone()
                if sig_row:
                    conn.execute(
                        "INSERT OR IGNORE INTO signal_dna (signal_id, dna_id) VALUES (?, ?)",
                        (sig_row['id'], dna['id'])
                    )
                    if conn.execute("SELECT changes()").fetchone()[0] > 0:
                        bound_count += 1

    conn.commit()
    conn.close()
    return {"bound_count": bound_count}

def seed_default_signals():
    """种子默认趋势信号"""
    defaults = [
        ("AGI / 大模型瓶颈", "AI", 8, 6, "3年"),
        ("AI 对齐 & 安全", "AI", 7, 5, "5年"),
        ("Agent 社会", "AI", 7, 7, "5年"),
        ("数字人 / 虚拟文明", "元宇宙", 6, 8, "10年"),
        ("3D Web / 空间计算", "Web", 6, 6, "5年"),
        ("算力 / 能源极限", "系统", 5, 7, "5年"),
        ("人机融合", "AI", 4, 9, "10年"),
        ("去中心化 vs 平台化", "Web", 6, 6, "5年"),
        ("新生产关系", "哲学", 5, 7, "10年"),
    ]
    conn = get_db()
    for name, direction, strength, uncertainty, scale in defaults:
        exists = conn.execute(
            "SELECT id FROM signals WHERE signal_name = ?", (name,)
        ).fetchone()
        if not exists:
            conn.execute(
                """INSERT INTO signals (signal_name, direction, signal_strength,
                   uncertainty, time_scale) VALUES (?, ?, ?, ?, ?)""",
                (name, direction, strength, uncertainty, scale)
            )
    conn.commit()
    conn.close()

# ============================================================
# 十一、战力评估
# ============================================================

def evaluate_army() -> List[Dict]:
    """评估数字大军战力（1-100分）"""
    conn = get_db()
    army_rows = conn.execute("SELECT * FROM army").fetchall()
    results = []

    for army in army_rows:
        dna_id = army['dna_id']
        if not dna_id:
            results.append({"id": army['id'], "role": army['role_name'], "combat_power": 1})
            continue

        dna = conn.execute("SELECT * FROM dna WHERE id = ?", (dna_id,)).fetchone()
        if not dna:
            results.append({"id": army['id'], "role": army['role_name'], "combat_power": 1})
            continue

        # 各维度评分
        pollution = dna['pollution_index'] or 0
        purity_score = max(0, 1 - pollution / 10) * 0.25

        difficulty = dna['difficulty'] or 1
        complexity_score = min(1, difficulty / 5) * 0.15

        task_row = conn.execute(
            """SELECT COUNT(*) as total,
               SUM(CASE WHEN status='Done' THEN 1 ELSE 0 END) as done
               FROM tasks WHERE related_dna_id = ?""", (dna_id,)
        ).fetchone()
        total_t = task_row['total'] or 1
        done_t = task_row['done'] or 0
        task_score = (done_t / total_t) * 0.35

        reuse_score = (1.0 if dna['reusable'] else 0.3) * 0.15

        sig_count = conn.execute(
            "SELECT COUNT(*) FROM signal_dna WHERE dna_id = ?", (dna_id,)
        ).fetchone()[0]
        sig_score = min(1, sig_count / 3) * 0.10

        total = (purity_score + complexity_score + task_score + reuse_score + sig_score) * 100
        combat_power = max(1, min(100, int(total)))

        conn.execute("UPDATE army SET combat_power = ? WHERE id = ?", (combat_power, army['id']))
        results.append({
            "id": army['id'], "role": army['role_name'],
            "combat_power": combat_power,
            "core_concept": dna['core_concept'], "direction": dna['direction']
        })

    conn.commit()
    conn.close()
    results.sort(key=lambda x: x['combat_power'], reverse=True)
    return results

# ============================================================
# 十二、项目推荐
# ============================================================

_PROJECT_TEMPLATES = [
    {"name": "AI 推理优化实验", "problem": "如何降低 LLM 推理延迟和成本",
     "directions": ["AI"], "concepts": ["LLM", "推理", "优化"]},
    {"name": "多模态 Agent 原型", "problem": "构建能处理文本+图像+语音的 Agent",
     "directions": ["AI"], "concepts": ["多模态", "Agent", "融合"]},
    {"name": "数字人身份系统", "problem": "为虚拟世界构建主权身份体系",
     "directions": ["元宇宙", "Web"], "concepts": ["数字人", "身份", "主权"]},
    {"name": "去中心化协作平台", "problem": "构建无中心的团队协作工具",
     "directions": ["Web", "系统"], "concepts": ["去中心化", "协作", "平台"]},
    {"name": "AI 价值观对齐实验", "problem": "让 AI 理解并执行人类价值观",
     "directions": ["AI", "哲学"], "concepts": ["对齐", "价值观", "伦理"]},
    {"name": "空间计算 Web 引擎", "problem": "在浏览器中实现 3D 空间计算",
     "directions": ["Web", "元宇宙"], "concepts": ["空间计算", "3D", "WebXR"]},
]

def recommend_projects(dna_id: int = None) -> List[Dict]:
    """根据 DNA 推荐项目"""
    conn = get_db()
    if dna_id:
        dna_rows = conn.execute("SELECT * FROM dna WHERE id = ?", (dna_id,)).fetchall()
    else:
        dna_rows = conn.execute("SELECT * FROM dna ORDER BY id DESC LIMIT 20").fetchall()
    conn.close()

    recommendations = []
    for dna in dna_rows:
        text = f"{dna['direction'] or ''} {dna['core_concept'] or ''} {dna['tech_points'] or ''}"
        for tpl in _PROJECT_TEMPLATES:
            score = 0.0
            if dna['direction'] in tpl['directions']:
                score += 0.4
            for kw in tpl['concepts']:
                if kw in text:
                    score += 0.15

            if score > 0.3:
                recommendations.append({
                    "dna_id": dna['id'],
                    "dna_concept": dna['core_concept'],
                    "project": tpl['name'],
                    "problem": tpl['problem'],
                    "match_score": round(min(1.0, score), 2)
                })

    recommendations.sort(key=lambda x: x['match_score'], reverse=True)
    return recommendations[:10]

# ============================================================
# 十三、可视化看板
# ============================================================

def generate_notion_dashboard() -> str:
    """生成 Notion 格式看板"""
    conn = get_db()
    inbox_count = conn.execute("SELECT COUNT(*) FROM inbox").fetchone()[0]
    dna_count = conn.execute("SELECT COUNT(*) FROM dna").fetchone()[0]
    todo_count = conn.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Todo'").fetchone()[0]
    done_count = conn.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Done'").fetchone()[0]
    army_count = conn.execute("SELECT COUNT(*) FROM army").fetchone()[0]
    signal_count = conn.execute("SELECT COUNT(*) FROM signals").fetchone()[0]

    dir_dist = conn.execute(
        "SELECT direction, COUNT(*) as cnt FROM dna GROUP BY direction ORDER BY cnt DESC"
    ).fetchall()

    recent = conn.execute(
        "SELECT title, type, created_at FROM inbox ORDER BY created_at DESC LIMIT 5"
    ).fetchall()

    tasks = conn.execute(
        "SELECT task_name, status, learning_mode FROM tasks WHERE status != 'Done' ORDER BY created_at DESC LIMIT 10"
    ).fetchall()
    conn.close()

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    lines = [
        f"# 🐉 龍魂 · 学习引擎看板",
        f"",
        f"> DNA: #龍芯⚡️{now}-DASHBOARD-UID9622",
        f"",
        f"## 📊 概览",
        f"",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 📥 学习资源 | {inbox_count} |",
        f"| 🧬 DNA 基因 | {dna_count} |",
        f"| 📋 待完成任务 | {todo_count} |",
        f"| ✅ 已完成任务 | {done_count} |",
        f"| 🤖 数字大军 | {army_count} |",
        f"| 🌍 趋势信号 | {signal_count} |",
        f"",
        f"## 📈 方向分布",
        f"",
        f"| 方向 | 数量 |",
        f"|------|------|",
    ]
    for row in dir_dist:
        lines.append(f"| {row[0] or '未知'} | {row[1]} |")

    lines += [
        f"",
        f"## 🔥 最近学习资源",
        f"",
    ]
    for row in recent:
        lines.append(f"- {row[0]} ({row[1]}) — {row[2]}")

    lines += [
        f"",
        f"## 🎯 当前任务",
        f"",
    ]
    for row in tasks:
        icon = "🟡" if row[1] == "Todo" else "🟢" if row[1] == "Doing" else "⚪"
        lines.append(f"- {icon} {row[0]} [{row[2]}] — {row[1]}")

    lines += [
        f"",
        f"---",
        f"📋 刷新: {now}",
        f"🔑 {CONFIRM_CODE}",
    ]
    return "\n".join(lines)

def generate_html_dashboard() -> str:
    """生成 HTML 仪表盘"""
    conn = get_db()
    inbox_count = conn.execute("SELECT COUNT(*) FROM inbox").fetchone()[0]
    dna_count = conn.execute("SELECT COUNT(*) FROM dna").fetchone()[0]
    todo_count = conn.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Todo'").fetchone()[0]
    done_count = conn.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Done'").fetchone()[0]
    army_count = conn.execute("SELECT COUNT(*) FROM army").fetchone()[0]

    dir_dist = conn.execute(
        "SELECT direction, COUNT(*) as cnt FROM dna GROUP BY direction ORDER BY cnt DESC"
    ).fetchall()

    tasks = conn.execute(
        "SELECT task_name, status, learning_mode FROM tasks WHERE status != 'Done' ORDER BY created_at DESC LIMIT 5"
    ).fetchall()
    conn.close()

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dir_rows = "\n".join(
        f"<tr><td>{r[0] or '未知'}</td><td>{r[1]}</td></tr>" for r in dir_dist
    )
    task_rows = "\n".join(
        f"""<div style='padding:8px 0;border-bottom:1px solid #21262d;'>
        <span class='badge {"badge-todo" if r[1]=="Todo" else "badge-doing"}'>{r[1]}</span>
        {r[0]} <span style='color:#8b949e;font-size:0.8em;'>[{r[2]}]</span></div>"""
        for r in tasks
    )

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🐉 龙魂 · 学习引擎看板</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#0d1117;color:#c9d1d9;padding:20px;}}
.container{{max-width:1200px;margin:0 auto;}}
h1{{color:#f0f6fc;font-size:2em;margin-bottom:4px;}}
.subtitle{{color:#8b949e;font-size:0.85em;margin-bottom:20px;}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:16px;margin:20px 0;}}
.card{{background:#161b22;border-radius:12px;padding:20px;border:1px solid #30363d;text-align:center;}}
.card .number{{font-size:2.2em;font-weight:700;color:#f0f6fc;}}
.card .label{{color:#8b949e;font-size:0.85em;margin-top:4px;}}
.section{{margin:24px 0;}}
.section h2{{font-size:1.2em;margin-bottom:12px;border-bottom:1px solid #30363d;padding-bottom:8px;}}
.table{{width:100%;border-collapse:collapse;}}
.table td,.table th{{padding:8px 12px;border-bottom:1px solid #21262d;}}
.table th{{text-align:left;color:#8b949e;font-weight:400;}}
.badge{{display:inline-block;padding:2px 10px;border-radius:12px;font-size:0.75em;margin-right:6px;}}
.badge-todo{{background:#d29922;color:#0d1117;}}
.badge-done{{background:#2ea043;color:#0d1117;}}
.badge-doing{{background:#1f6feb;color:#fff;}}
.footer{{margin-top:40px;padding-top:20px;border-top:1px solid #30363d;color:#8b949e;font-size:0.78em;text-align:center;}}
.dna{{font-family:monospace;color:#f0c040;font-size:0.85em;}}
</style>
</head>
<body>
<div class="container">
<h1>🐉 龙魂 · 学习引擎看板</h1>
<div class="subtitle">{now} · DNA: #龍芯⚡️{now[:10].replace('-','')}-DASHBOARD</div>

<div class="grid">
<div class="card"><div class="number">{inbox_count}</div><div class="label">📥 学习资源</div></div>
<div class="card"><div class="number">{dna_count}</div><div class="label">🧬 DNA 基因</div></div>
<div class="card"><div class="number">{todo_count}</div><div class="label">📋 待完成</div></div>
<div class="card"><div class="number">{done_count}</div><div class="label">✅ 已完成</div></div>
<div class="card"><div class="number">{army_count}</div><div class="label">🤖 数字大军</div></div>
</div>

<div class="section">
<h2>📈 方向分布</h2>
<table class="table">
<tr><th>方向</th><th>数量</th></tr>
{dir_rows}
</table>
</div>

<div class="section">
<h2>🎯 当前任务</h2>
{task_rows}
</div>

<div class="footer">
<span class="dna">DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☴巽-LEARN-ENGINE-v1.0</span><br>
确认码: {CONFIRM_CODE}
</div>
</div>
</body>
</html>"""
    return html

# ============================================================
# 十四、统计摘要
# ============================================================

def stats_summary() -> Dict:
    """数据库统计摘要"""
    conn = get_db()
    return {
        "inbox_total": conn.execute("SELECT COUNT(*) FROM inbox").fetchone()[0],
        "inbox_pending": conn.execute("SELECT COUNT(*) FROM inbox WHERE status='待净化'").fetchone()[0],
        "inbox_purified": conn.execute("SELECT COUNT(*) FROM inbox WHERE status='已净化'").fetchone()[0],
        "dna_total": conn.execute("SELECT COUNT(*) FROM dna").fetchone()[0],
        "tasks_todo": conn.execute("SELECT COUNT(*) FROM tasks WHERE status='Todo'").fetchone()[0],
        "tasks_done": conn.execute("SELECT COUNT(*) FROM tasks WHERE status='Done'").fetchone()[0],
        "signals_total": conn.execute("SELECT COUNT(*) FROM signals").fetchone()[0],
        "army_total": conn.execute("SELECT COUNT(*) FROM army").fetchone()[0],
        "projects_total": conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0],
        "db_path": str(DB_PATH),
    }

# ============================================================
# 十五、交互控制台
# ============================================================

def interactive():
    """交互式菜单"""
    while True:
        print("\n" + "=" * 48)
        print("🐉 自主学习引擎 v1.0")
        print("=" * 48)
        print("1.  添加学习资源 (Inbox)")
        print("2.  查看待净化内容")
        print("3.  运行自动化管道 (净化 → DNA → 任务)")
        print("4.  查看 DNA 库")
        print("5.  查看任务列表")
        print("6.  完成任务")
        print("7.  添加趋势信号")
        print("8.  编制数字大军")
        print("9.  自动绑定趋势信号")
        print("10. 战力评估")
        print("11. 项目推荐")
        print("12. 统计摘要")
        print("13. 生成看板 (Notion/HTML)")
        print("14. 查看 Inbox 全部")
        print("0.  退出")
        choice = input("\n选择: ").strip()

        if choice == "0":
            print("🐉 退出了，战友。")
            break

        elif choice == "1":
            title = input("标题: ").strip()
            if not title:
                continue
            type_ = input("类型 (Website/Paper/Video/Idea/Code/Trend) [Website]: ").strip() or "Website"
            link = input("链接 (可选): ").strip()
            source = input("来源 (可选): ").strip()
            raw = input("原始内容摘要 (可选): ").strip()
            rid = add_inbox(title, type_, link, raw, source)
            print(f"  ✅ 已加入 Inbox #{rid}")

        elif choice == "2":
            items = list_inbox(status="待净化")
            if items:
                for i in items:
                    print(f"  [{i['id']}] {i['title']} ({i['type']}) - {i['created_at']}")
            else:
                print("  📭 没有待净化内容")

        elif choice == "3":
            run_pipeline(interactive_input=True)

        elif choice == "4":
            dna_list = list_dna()
            if dna_list:
                for d in dna_list:
                    reuse = "♻️" if d['reusable'] else ""
                    print(f"  🧬 {d['dna_id']} | {d['core_concept']} ({d['direction']}) {reuse}")
            else:
                print("  📭 暂无 DNA")

        elif choice == "5":
            tasks = list_tasks()
            if tasks:
                for t in tasks:
                    icon = "🟡" if t['status'] == "Todo" else "🟢" if t['status'] == "Done" else "🔵"
                    print(f"  {icon} #{t['id']} {t['task_name']} [{t['learning_mode']}]")
            else:
                print("  📭 暂无任务")

        elif choice == "6":
            tid = input("任务 ID: ").strip()
            if tid.isdigit():
                result = complete_task(int(tid))
                print(f"  {'✅ 已完成' if 'completed' in result.get('status','') else '❌ ' + result.get('error','')}")
            else:
                print("  ❌ 无效 ID")

        elif choice == "7":
            name = input("信号名称: ").strip()
            direction = input("方向: ").strip() or "未知"
            try:
                strength = int(input("信号强度 (1-10) [5]: ").strip() or "5")
                uncertainty = int(input("不确定性 (1-10) [5]: ").strip() or "5")
            except ValueError:
                strength, uncertainty = 5, 5
            scale = input("时间尺度 (3年/5年/10年) [5年]: ").strip() or "5年"
            sid = add_signal(name, direction, strength, uncertainty, scale)
            print(f"  ✅ 信号 #{sid} 已添加")

        elif choice == "8":
            role = input("兵种角色: ").strip()
            dna_list = list_dna()
            if not dna_list:
                print("  📭 请先创建 DNA")
                continue
            for i, d in enumerate(dna_list[:15]):
                print(f"    {i+1}. {d['core_concept']} ({d['dna_id']})")
            sel = input("选择 DNA 编号: ").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(dna_list):
                dna_row = dna_list[int(sel) - 1]
                expertise = input("擅长领域: ").strip()
                problem_type = input("可解决问题类型: ").strip()
                aid = add_army(role, dna_row['id'], expertise, problem_type)
                print(f"  ✅ 兵种 #{aid} 已编制")
            else:
                print("  ❌ 无效选择")

        elif choice == "9":
            result = auto_bind_signals()
            print(f"  ✅ 已绑定 {result['bound_count']} 条关联")

        elif choice == "10":
            results = evaluate_army()
            if results:
                print("\n  🤖 战力评估:")
                for r in results:
                    bar = "█" * (r['combat_power'] // 10) + "░" * (10 - r['combat_power'] // 10)
                    print(f"  {r['role']:12s} {bar} {r['combat_power']}/100")
            else:
                print("  📭 暂无数字大军")

        elif choice == "11":
            recs = recommend_projects()
            if recs:
                print("\n  📋 推荐项目:")
                for r in recs[:8]:
                    print(f"  [{r['match_score']:.0%}] {r['project']}")
                    print(f"     DNA: {r['dna_concept'][:40]}")
            else:
                print("  📭 暂无推荐")

        elif choice == "12":
            stats = stats_summary()
            print(f"\n  📊 统计摘要:")
            print(f"    学习资源: {stats['inbox_total']} (待净化: {stats['inbox_pending']})")
            print(f"    DNA基因:  {stats['dna_total']}")
            print(f"    任务:     {stats['tasks_todo']} 待做 / {stats['tasks_done']} 已完成")
            print(f"    趋势信号: {stats['signals_total']}")
            print(f"    数字大军: {stats['army_total']}")
            print(f"    实验项目: {stats['projects_total']}")
            print(f"    数据库:   {stats['db_path']}")

        elif choice == "13":
            fmt = input("格式 (notion/html) [html]: ").strip().lower() or "html"
            if fmt == "notion":
                content = generate_notion_dashboard()
                print(content)
            else:
                html = generate_html_dashboard()
                DASHBOARD_HTML.write_text(html, encoding='utf-8')
                print(f"  ✅ HTML 看板已生成: {DASHBOARD_HTML}")

        elif choice == "14":
            items = list_inbox()
            for i in items:
                st_icon = "📥" if i['status'] == "待净化" else "✅"
                print(f"  {st_icon} [{i['id']}] {i['title']} ({i['type']}) - {i['status']}")

        else:
            print("  ❌ 无效选择")

# ============================================================
# 十六、CLI 入口
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 自主学习引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  lh learn -i                             交互模式
  lh learn --add --title "Transformer论文" --type Paper
  lh learn --run                           自动化管道
  lh learn --stats                         统计摘要
  lh learn --dashboard --format html       生成HTML看板
  lh learn --dashboard --format notion     生成Notion看板
  lh learn --evaluate                      战力评估
  lh learn --recommend                     项目推荐
  lh learn --bind-signals                  自动绑定趋势

确认码: {CONFIRM_CODE}
"""
    )
    parser.add_argument("--init", action="store_true", help="初始化数据库 + 种子信号")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--add", action="store_true", help="快速添加 Inbox")
    parser.add_argument("--title", type=str, help="标题")
    parser.add_argument("--type", type=str, default="Website", help="类型")
    parser.add_argument("--link", type=str, default="", help="链接")
    parser.add_argument("--content", type=str, default="", help="原始内容")
    parser.add_argument("--source", type=str, default="", help="来源")
    parser.add_argument("--run", action="store_true", help="运行自动化管道")
    parser.add_argument("--non-interactive", action="store_true", help="非交互管道")
    parser.add_argument("--stats", action="store_true", help="统计摘要")
    parser.add_argument("--dashboard", action="store_true", help="生成看板")
    parser.add_argument("--format", default="html", choices=["html", "notion"], help="看板格式")
    parser.add_argument("--evaluate", action="store_true", help="战力评估")
    parser.add_argument("--recommend", action="store_true", help="项目推荐")
    parser.add_argument("--dna-id", type=int, help="指定DNA ID推荐")
    parser.add_argument("--auto-digest", action="store_true", help="AI自动拆解（规则+可选LLM）")
    parser.add_argument("--use-llm", action="store_true", help="启用LLM提取（需设置LLM_API_KEY）")
    parser.add_argument("--inbox-id", type=int, help="指定Inbox ID")
    parser.add_argument("--bind-signals", action="store_true", help="自动绑定趋势信号")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 输出")

    args = parser.parse_args()

    if args.init:
        db_path = init_db()
        seed_default_signals()
        print(f"✅ 数据库初始化: {db_path}")
        print(f"✅ 已种子 9 个默认趋势信号")
        return

    if args.interactive:
        interactive()
        return

    if args.add:
        if not args.title:
            print("❌ 请提供 --title")
            return
        rid = add_inbox(args.title, args.type, args.link, args.content, args.source)
        print(f"✅ Inbox #{rid}: {args.title}")
        return

    if args.run:
        results = run_pipeline(interactive_input=not args.non_interactive)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    if args.stats:
        stats = stats_summary()
        if args.json:
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            for k, v in stats.items():
                print(f"  {k}: {v}")
        return

    if args.dashboard:
        if args.format == "notion":
            print(generate_notion_dashboard())
        else:
            html = generate_html_dashboard()
            DASHBOARD_HTML.write_text(html, encoding='utf-8')
            print(f"✅ HTML 看板: {DASHBOARD_HTML}")
        return

    if args.evaluate:
        results = evaluate_army()
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for r in results:
                print(f"  {r['role']}: {r['combat_power']}/100")
        return

    if args.recommend:
        recs = recommend_projects(args.dna_id)
        if args.json:
            print(json.dumps(recs, ensure_ascii=False, indent=2))
        else:
            for r in recs:
                print(f"  [{r['match_score']:.0%}] {r['project']} — {r['problem'][:60]}")
        return

    if args.auto_digest:
        result = auto_digest_inbox(args.inbox_id, use_llm=args.use_llm)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            if 'error' in result:
                print(f"❌ {result['error']}")
            elif result.get('status') == 'no_items':
                print(f"📭 {result.get('message')}")
            else:
                print(f"✅ 自动拆解完成: {result['result']['dna_id']}")
        return

    if args.bind_signals:
        result = auto_bind_signals()
        if args.json:
            print(json.dumps(result, ensure_ascii=False))
        else:
            print(f"✅ 已绑定 {result['bound_count']} 条关联")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
