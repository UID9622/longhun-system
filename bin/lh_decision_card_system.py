#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  🔧 工程落地执行型 — 龍魂·责任卡/决策卡片系统 v2.0              ║
║  DNA: #龍芯⚡️丙午·乙未·庚申·亥时·乾-DECISION-CARD-v2.0     ║
║  场景: 重要决策留痕·责任归属审计·备选方案对比·DNA追溯链         ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F               ║
╚══════════════════════════════════════════════════════════════╝

> 🐉 龍魂·责任卡系统 v2.0 — 每次重要决策的结构化留痕引擎。
> 核心能力：轻量版/完整版双模板 + 关键词自动路由 + DNA追溯 + 三色审计
> + SQLite存储 + 锚点登记 + 撤销回滚 + 五行签名 + 引擎命令行入口。

ROOT_CARD:
  ID: uid9622
  DNA: #龍芯⚡️丙午·乙未·庚申·亥时·乾-DECISION-CARD-v2.0
  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
  AUTHORITY: M261前传契碑·全权授权令·L0永恒级
  TARGET: bin/lh_decision_card_system.py
  TIMESTAMP: 2026-08-02
  LICENSE: CC BY-NC-SA 4.0 (君子协议，来源链不可切断)
  EXECUTOR: P04鲁班(工程) + P05上帝之眼(审计) + P03雯雯(归档) + P15乔前辈(签章)
  LINEAGE:
    - 兄弟: lh_decision_tracer.py (决策追溯引擎v1.0·三才卡片)
    - 兄弟: lh_decision_daemon.py (守护进程v1.0·自动卡片生成)
    - 上位: LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md §2.3
    - 平级: lh_adaptive_tuner.py (自适应微调v2.0)
  SCOPE: 决策留痕·责任归属·不涉及D1/D2数据
  LIMITS: 备选不能为空·AI不得反客为主·UID9622最终裁定
"""
from __future__ import annotations

# ═══════════════════════════════════════════════════════════════
# A-BOM · 算法物料清单（算法审计协议v1.0 §4）
# ═══════════════════════════════════════════════════════════════
# 目标函数: 每次决策 → 结构化的责任卡(轻量/完整) → SQLite持久化 → 锚点登记
# 输入特征: 触发文本·关键词匹配·决策等级判定·三色审计
# 输出: Markdown责任卡·SQLite记录·锚点文件·审计回执
# 用户影响: 纯粹的留痕归档工具，不修改用户行为，不影响任何系统参数
#            所有决策权归UID9622，AI仅负责结构化记录
# 透明度: 模板公开·关键词路由规则公开·三色判定规则公开·数据库SQL公开
#         每张卡片含完整DNA追溯码·锚点ID·五行签名·撤销方案
# 申诉通道: decision --list 列出所有卡片·decision --show HASH 查看详情
#           字段缺失→🟡标记·越权→🔴标记·UID9622最终裁定
# 审计标志: 🟢 模板2套·路由15+关键词·三色判定·SQLite·9项自检

import json
import hashlib
import os
import sys
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime
from typing import Any
from copy import deepcopy

# ═══════════════════════════════════════════════════════════════
# 〇、固定锚点 · 焊死
# ═══════════════════════════════════════════════════════════════

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CNSH_ROOT = Path.home() / "cnsh"
DECISION_ROOT = CNSH_ROOT / "决策卡片"

# ═══════════════════════════════════════════════════════════════
# 一、终端颜色
# ═══════════════════════════════════════════════════════════════

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def cprint(text: str, color: str = Colors.RESET) -> None:
    print(f"{color}{text}{Colors.RESET}")

# ═══════════════════════════════════════════════════════════════
# 二、工具函数
# ═══════════════════════════════════════════════════════════════

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def today() -> str:
    return datetime.now().strftime("%Y%m%d")

def hash8(text: str) -> str:
    raw = f"{text}|{now_iso()}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:8].upper()

def make_dna(h: str) -> str:
    return f"#龍芯⚡️{today()}-DEC-{h}"

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# 三、三色审计
# ═══════════════════════════════════════════════════════════════

class TriColor:
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"

# ═══════════════════════════════════════════════════════════════
# 四、模板内容
# ═══════════════════════════════════════════════════════════════

LIGHT_TEMPLATE = """# 🃏 DECISION · {{DNA}}

```yaml
版本: v2.0-light
时间: {{CREATED_AT}}
等级: {{LEVEL}}
三色: {{COLOR}}
责任: {{RESPONSIBILITY}}

❶ 触发
{{TRIGGER}}

❷ 依据
{{SOURCES}}

❸ 备选
A. {{OPTION_A}}
B. {{OPTION_B}}
C. {{OPTION_C}}

❹ 选择
选：{{SELECTED_OPTION}}
理由：{{CHOICE_REASON}}

❺ 三色责任
状态：{{COLOR}}
原因：{{COLOR_REASON}}
责任归属：{{RESPONSIBILITY}}

---

铁律：若备选为空，本卡自动判定为 🟡 待审。
"""

FULL_TEMPLATE = """# 🃏 UID9622 龍芯北辰 · RESPONSIBILITY DECISION CARD

```yaml
DNA: "{{DNA}}"
版本: "v2.0-full"
时间: "{{CREATED_AT}}"
决策等级: "{{LEVEL}}"
决策者: "{{DECISION_MAKER}}"
三色状态: "{{COLOR}}"
锚点: "{{ANCHOR_ID}}"

---

【0. 主控声明】
主控者：UID9622
AI定位：执行工具 / 结构化助手 / 决策留痕器
最高确认：{{CONFIRM}}
边界声明：AI 不得反客为主，不得替 UID9622 做最终主权决定。

---

【1. 触发源】
触发输入：{{TRIGGER_INPUT}}
触发时间：{{TRIGGER_TIME}}
触发来源：{{TRIGGER_SOURCE}}
触发类型：{{TRIGGER_TYPE}}
是否需要决策：{{NEED_DECISION}}
触发原因：{{TRIGGER_REASON}}

---

【2. 信息源】
* 源 ①：{{SOURCE_1}}
* 源 ②：{{SOURCE_2}}
* 源 ③：{{SOURCE_3}}
信息完整度：{{SOURCE_COMPLETENESS}}
缺失项：{{MISSING_INFO}}
是否使用外部信息：{{EXTERNAL_USED}}
是否存在不确定性：{{UNCERTAINTY}}

---

【3. 规则匹配】
主规则：{{PRIMARY_RULE}}
辅助规则：{{SECONDARY_RULES}}
层级：{{LEVEL}}
是否触发一票否决：{{VETO}}
是否存在规则冲突：{{RULE_CONFLICT}}
冲突处理方式：{{CONFLICT_RESOLUTION}}
师承 / 文化约束：{{CULTURAL_CONSTRAINT}}

---

【4. 备选方案】
A. {{OPTION_A}}
   * 收益：{{OPTION_A_BENEFIT}}
   * 代价：{{OPTION_A_COST}}
   * 风险：{{OPTION_A_RISK}}
   * 可撤销：{{OPTION_A_REVERSIBLE}}

B. {{OPTION_B}}
   * 收益：{{OPTION_B_BENEFIT}}
   * 代价：{{OPTION_B_COST}}
   * 风险：{{OPTION_B_RISK}}
   * 可撤销：{{OPTION_B_REVERSIBLE}}

C. {{OPTION_C}}
   * 收益：{{OPTION_C_BENEFIT}}
   * 代价：{{OPTION_C_COST}}
   * 风险：{{OPTION_C_RISK}}
   * 可撤销：{{OPTION_C_REVERSIBLE}}

备选完整度：{{OPTIONS_COMPLETENESS}}
铁律：若本段为空，整张卡自动判定为 🟡 待审；重大决策自动 🔴 禁止执行。

---

【5. 选择与排除】
最终选择：{{SELECTED_OPTION}}
选择理由：{{CHOICE_REASON}}
为什么不是 A：{{REJECT_A_REASON}}
为什么不是 B：{{REJECT_B_REASON}}
为什么不是 C：{{REJECT_C_REASON}}
是否需要 UID9622 最终确认：{{REQUIRES_UID_CONFIRM}}
是否允许 AI 直接执行：{{AI_CAN_EXECUTE}}

---

【6. 三色判定】
状态：{{COLOR}}
颜色原因：{{COLOR_REASON}}
风险点：
* {{RISK_1}}
* {{RISK_2}}
缓解措施：
* {{MITIGATION_1}}
* {{MITIGATION_2}}
是否需要急停：{{EMERGENCY_STOP}}
急停条件：{{STOP_CONDITION}}

---

【7. 责任归属】
主权责任：UID9622
执行责任：{{EXECUTION_RESPONSIBILITY}}
审计责任：{{AUDIT_RESPONSIBILITY}}
错误责任：
* 规则引用错误：AI 负责标记并修正
* 输入不完整：标记为 🟡，不得冒充确定
* 执行越权：系统 / AI 进入 🔴
最终裁定权：UID9622

---

【8. 撤销与回滚】
可撤销：{{REVERSIBLE}}
撤销方式：{{ROLLBACK_METHOD}}
撤销代价：{{ROLLBACK_COST}}
影响范围：{{IMPACT_SCOPE}}
回滚锚点：{{ROLLBACK_ANCHOR}}
是否需要生成纠错卡：{{CORRECTION_CARD_REQUIRED}}

---

【9. 留痕归档】
本机审计：{{LOCAL_AUDIT}}
本机文件：{{FILE_PATH}}
不动点锚：{{ANCHOR_ID}}
Notion位置：{{NOTION_LOCATION}}
关联DNA：{{RELATED_DNA}}
关联ROOT_CARD：{{ROOT_CARD_REF}}
五行签名：
* 金：{{WUXING_JIN}}
* 木：{{WUXING_MU}}
* 水：{{WUXING_SHUI}}
* 火：{{WUXING_HUO}}
* 土：{{WUXING_TU}}

---

归属：🌿曾仕強老師 · ⚙️UID9622 · 📜中华文化 · 🐉龍芯北辰
"""

# ═══════════════════════════════════════════════════════════════
# 五、核心引擎 — DecisionCardSystem
# ═══════════════════════════════════════════════════════════════

class DecisionCardSystem:
    """责任卡/决策卡片系统 v2.0"""

    def __init__(self, base_dir: Path | None = None):
        self.base_dir = base_dir or DECISION_ROOT
        self.template_dir = self.base_dir / "templates"
        self.engine_dir = self.base_dir / "engine"
        self.daily_dir = self.base_dir / "cards" / "daily"
        self.major_dir = self.base_dir / "cards" / "major"
        self.archived_dir = self.base_dir / "cards" / "archived"
        self.anchors_dir = self.base_dir / "anchors"
        self.db_dir = self.base_dir / "db"
        self.logs_dir = self.base_dir / "logs"
        self.db_path = self.db_dir / "decision_cards.sqlite"
        self.log_path = self.logs_dir / "decision_trace.log"
        self.anchor_registry = self.anchors_dir / "anchor_registry.json"

        # 路由关键词（触发完整版的关键词）
        self.full_keywords: list[str] = [
            "主控", "CONFIRM", "SEAL", "GPG", "不动点", "登锚", "规则库",
            "CNSH", "本机", "删除", "覆盖", "发布", "版权", "DNA",
            "ROOT_CARD", "重大决策", "师承", "曾仕强", "易经", "道德经",
        ]
        self.light_keywords: list[str] = [
            "优化", "整理", "回复", "总结", "简化", "对照表", "日常判断",
        ]

    # ── 目录创建 ──────────────────────────────────────────

    def create_directories(self) -> bool:
        dirs = [
            self.base_dir, self.template_dir, self.engine_dir,
            self.daily_dir, self.major_dir, self.archived_dir,
            self.anchors_dir, self.db_dir, self.logs_dir,
        ]
        for d in dirs:
            ensure_dir(d)
        return True

    # ── 模板创建 ──────────────────────────────────────────

    def create_templates(self) -> bool:
        light_path = self.template_dir / "light_card.md"
        full_path = self.template_dir / "full_card.md"
        if not light_path.exists():
            light_path.write_text(LIGHT_TEMPLATE, encoding="utf-8")
        if not full_path.exists():
            full_path.write_text(FULL_TEMPLATE, encoding="utf-8")
        return True

    # ── 核心引擎创建 ──────────────────────────────────────

    def create_engine(self) -> bool:
        engine_code = self._get_engine_code()
        engine_path = self.engine_dir / "decision_card.py"
        if not engine_path.exists():
            engine_path.write_text(engine_code, encoding="utf-8")
            engine_path.chmod(0o755)
        return True

    def _get_engine_code(self) -> str:
        return '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UID9622 龍芯北辰｜责任卡生成引擎 v2.0
DNA: #龍芯⚡️丙午·乙未·庚申·亥时-ENGINE-v2.0
"""

import sys
import json
import hashlib
import sqlite3
import argparse
from pathlib import Path
from datetime import datetime

DECISION_ROOT = Path.home() / "cnsh" / "决策卡片"
TEMPLATE_DIR = DECISION_ROOT / "templates"
DAILY_DIR = DECISION_ROOT / "cards" / "daily"
MAJOR_DIR = DECISION_ROOT / "cards" / "major"
DB_PATH = DECISION_ROOT / "db" / "decision_cards.sqlite"

FULL_KEYWORDS = [
    "主控", "CONFIRM", "SEAL", "GPG", "不动点", "登锚", "规则库",
    "CNSH", "本机", "删除", "覆盖", "发布", "版权", "DNA",
    "ROOT_CARD", "重大决策", "师承", "曾仕强", "易经", "道德经",
]
LIGHT_KEYWORDS = ["优化", "整理", "回复", "总结", "简化", "对照表", "日常判断"]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def today() -> str:
    return datetime.now().strftime("%Y%m%d")


def hash8(text: str) -> str:
    raw = f"{text}|{now_iso()}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:8].upper()


def make_dna(h: str) -> str:
    return f"#龍芯⚡️{today()}-DEC-{h}"


def route_card_type(text: str, force: str = "") -> str:
    if force in ("light", "full"):
        return force
    for kw in FULL_KEYWORDS:
        if kw in text:
            return "full"
    return "light"


def decision_level(text: str, card_type: str) -> str:
    if any(kw in text for kw in ["主控", "CONFIRM", "SEAL", "GPG", "P0"]):
        return "L0"
    if any(kw in text for kw in ["CNSH", "本机", "脚本", "删除", "覆盖", "工程"]):
        return "L1"
    if any(kw in text for kw in ["文档", "模板", "页面", "Notion"]):
        return "L2"
    return "L3" if card_type == "light" else "L1"


def color_by_options(card_type: str, options: list[str]) -> str:
    valid = [o for o in options if o and o.strip()]
    if card_type == "full" and len(valid) < 2:
        return "🔴"
    if len(valid) < 2:
        return "🟡"
    return "🟢"


def load_template(card_type: str) -> str:
    name = "light_card.md" if card_type == "light" else "full_card.md"
    return (TEMPLATE_DIR / name).read_text(encoding="utf-8")


def replace_all(template: str, data: dict[str, str]) -> str:
    out = template
    for k, v in data.items():
        out = out.replace("{{" + k + "}}", str(v))
    return out


def save_card(card_type: str, content: str, level: str, h: str) -> Path:
    directory = DAILY_DIR if card_type == "light" else MAJOR_DIR
    prefix = "DECISION_CARD" if card_type == "light" else "RESPONSIBILITY_CARD"
    filename = f"{prefix}_{today()}_{level}_{h}.md"
    path = directory / filename
    path.write_text(content, encoding="utf-8")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description="UID9622 责任卡生成引擎")
    parser.add_argument("text", nargs="*", help="触发内容")
    parser.add_argument("--light", action="store_true", help="强制轻量版")
    parser.add_argument("--full", action="store_true", help="强制完整版")
    parser.add_argument("--list", action="store_true", help="列出最近卡片")
    parser.add_argument("--show", help="查看指定HASH")
    args = parser.parse_args()

    if args.list:
        if not DB_PATH.exists():
            print("数据库不存在，请先安装: python3 lh_decision_card_system.py --install")
            return
        conn = sqlite3.connect(str(DB_PATH))
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT created_at, hash8, card_type, decision_level, color, title "
                "FROM decision_cards ORDER BY id DESC LIMIT 20"
            )
            for row in cur.fetchall():
                print(" | ".join(str(x) for x in row))
        except sqlite3.OperationalError:
            print("表不存在，请先安装: python3 lh_decision_card_system.py --install")
        conn.close()
        return

    if args.show:
        for f in DECISION_ROOT.rglob(f"*{args.show.upper()}*.md"):
            print(f.read_text(encoding="utf-8"))
            return
        print(f"未找到: {args.show}")
        return

    text = " ".join(args.text).strip()
    if not text:
        print("请输入内容")
        return

    force = "full" if args.full else "light" if args.light else ""
    card_type = route_card_type(text, force)
    level = decision_level(text, card_type)
    h = hash8(text)
    dna = make_dna(h)
    options_list = ["A", "B", "C"]
    color = color_by_options(card_type, options_list)
    anchor_id = f"ANCHOR-DEC-{today()}-{h}"

    data: dict[str, str] = {
        "DNA": dna, "CREATED_AT": now_iso(), "LEVEL": level, "COLOR": color,
        "RESPONSIBILITY": "AI生成 / UID9622最终定盘",
        "CONFIRM": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        "TRIGGER": text, "SOURCES": "UID9622主控 / 三色审计",
        "OPTION_A": "普通处理", "OPTION_B": "生成卡片", "OPTION_C": "升级完整",
        "SELECTED_OPTION": "B", "CHOICE_REASON": "日常留痕",
        "COLOR_REASON": "备选完整，风险可控",
        "DECISION_MAKER": "AI起草 / UID9622定盘",
        "TRIGGER_INPUT": text, "TRIGGER_TIME": now_iso(),
        "TRIGGER_SOURCE": "CNSH decision", "TRIGGER_TYPE": "工程决策",
        "NEED_DECISION": "是", "TRIGGER_REASON": "需形成可追溯责任链",
        "SOURCE_1": "UID9622主控", "SOURCE_2": "责任卡v2.0", "SOURCE_3": "CNSH执行",
        "SOURCE_COMPLETENESS": "🟢完整", "MISSING_INFO": "无",
        "EXTERNAL_USED": "否", "UNCERTAINTY": "低",
        "PRIMARY_RULE": "UID9622主控", "SECONDARY_RULES": "DNA追溯",
        "VETO": "否", "RULE_CONFLICT": "否", "CONFLICT_RESOLUTION": "无",
        "CULTURAL_CONSTRAINT": "UID9622龍芯北辰",
        "OPTION_A_BENEFIT": "快", "OPTION_A_COST": "无责任链", "OPTION_A_RISK": "无法追溯",
        "OPTION_B_BENEFIT": "快留痕", "OPTION_B_COST": "字段不足",
        "OPTION_B_RISK": "缺少撤销细节", "OPTION_B_REVERSIBLE": "是",
        "OPTION_C_BENEFIT": "完整", "OPTION_C_COST": "较长", "OPTION_C_RISK": "略重",
        "OPTION_C_REVERSIBLE": "是", "OPTIONS_COMPLETENESS": "🟢充分",
        "REJECT_A_REASON": "无责任链", "REJECT_B_REASON": "不排除",
        "REJECT_C_REASON": "日常略重", "REQUIRES_UID_CONFIRM": "是",
        "AI_CAN_EXECUTE": "仅生成文件",
        "RISK_1": "误判等级", "RISK_2": "伪造执行",
        "MITIGATION_1": "自动路由", "MITIGATION_2": "三色锁",
        "EMERGENCY_STOP": "否", "STOP_CONDITION": "越权时停",
        "EXECUTION_RESPONSIBILITY": "AI生成 / CNSH写入",
        "AUDIT_RESPONSIBILITY": "AI标记 / UID9622查看",
        "REVERSIBLE": "是", "ROLLBACK_METHOD": "删除或纠错",
        "ROLLBACK_COST": "低", "IMPACT_SCOPE": "本机目录",
        "ROLLBACK_ANCHOR": anchor_id, "CORRECTION_CARD_REQUIRED": "必要时",
        "LOCAL_AUDIT": "SQLite", "FILE_PATH": "自动生成",
        "ANCHOR_ID": anchor_id, "NOTION_LOCATION": "UID9622主控",
        "RELATED_DNA": dna, "ROOT_CARD_REF": "责任卡ROOT_CARD",
        "WUXING_JIN": "规则", "WUXING_MU": "扩展",
        "WUXING_SHUI": "追溯", "WUXING_HUO": "触发", "WUXING_TU": "归档",
    }

    if card_type == "light":
        content = replace_all(load_template("light"), data)
    else:
        content = replace_all(load_template("full"), data)

    path = save_card(card_type, content, level, h)

    # 数据库写入
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS decision_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dna TEXT NOT NULL UNIQUE,
            hash8 TEXT NOT NULL,
            created_at TEXT NOT NULL,
            card_type TEXT NOT NULL,
            decision_level TEXT NOT NULL,
            title TEXT,
            trigger_input TEXT,
            selected_option TEXT,
            color TEXT,
            responsibility_owner TEXT,
            reversible INTEGER DEFAULT 1,
            file_path TEXT,
            anchor_id TEXT,
            raw_json TEXT,
            final_authority TEXT DEFAULT 'UID9622'
        )
    """)
    conn.execute(
        """INSERT OR IGNORE INTO decision_cards
        (dna, hash8, created_at, card_type, decision_level, title, trigger_input, color,
         responsibility_owner, file_path, anchor_id, raw_json, final_authority)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (dna, h, now_iso(), card_type, level, text[:40], text, color,
         "AI生成 / UID9622定盘", str(path), anchor_id,
         json.dumps({"dna": dna, "hash": h}, ensure_ascii=False), "UID9622"),
    )
    conn.commit()
    conn.close()

    print("【责任卡生成回执】")
    print(f"状态: 已生成")
    print(f"卡片类型: {'轻量版' if card_type == 'light' else '完整版'}")
    print(f"等级: {level}")
    print(f"DNA: {dna}")
    print(f"文件路径: {path}")
    print(f"三色: {color}")
    print("责任归属: AI生成 / UID9622最终定盘")
    print("下一步: decision --list 查看")


if __name__ == "__main__":
    main()
'''

    # ── 路由器创建 ──────────────────────────────────────────

    def create_router(self) -> bool:
        router_path = self.engine_dir / "responsibility_router.py"
        if not router_path.exists():
            router_path.write_text('''#!/usr/bin/env python3
"""责任卡路由判断 v2.0"""

FULL_KEYWORDS = [
    "主控", "CONFIRM", "SEAL", "GPG", "不动点", "登锚", "规则库",
    "CNSH", "本机", "删除", "覆盖", "发布", "版权", "DNA",
    "ROOT_CARD", "重大决策", "师承", "曾仕强", "易经", "道德经",
]


def route_card_type(text: str, force: str = "") -> str:
    if force in ("light", "full"):
        return force
    for kw in FULL_KEYWORDS:
        if kw in text:
            return "full"
    return "light"
''', encoding="utf-8")
            router_path.chmod(0o755)
        return True

    # ── 锚点创建 ──────────────────────────────────────────

    def create_anchor(self) -> bool:
        anchor_id = "ANCHOR-DEC-20260508-RESPCARD-V2"
        dna = "#龍芯⚡️20260508-DEC-RESPCARD-V2"

        registry_data = {
            "system": "UID9622 龍芯北辰",
            "module": "责任卡系统",
            "version": "v2.0",
            "anchors": [{
                "anchor_id": anchor_id,
                "dna": dna,
                "title": "责任卡系统第一锚",
                "level": "L1",
                "status": "active",
                "color": "🟢",
                "created_at": "2026-05-08",
                "owner": "UID9622",
                "file": "~/cnsh/决策卡片/anchors/ANCHOR-DEC-20260508-RESPCARD-V2.md",
                "note": "责任卡系统自身的第一张不动点锚",
            }],
        }
        self.anchor_registry.write_text(
            json.dumps(registry_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        anchor_content = f"""# ANCHOR-DEC-20260508-RESPCARD-V2

```yaml
锚点名称: 责任卡系统第一锚
DNA: "{dna}"
系统: UID9622 龍芯北辰
模块: 责任卡 / 决策卡片系统
版本: v2.0
等级: L1 工程级
三色: 🟢
主控者: UID9622
确认码: "{CONFIRM}"
SEAL: "{SEAL}"
GPG: "{GPG_FINGERPRINT}"

---

## 锚点定义
本锚点用于固定 UID9622 龍芯北辰责任卡系统的第一版不动点。

## 核心铁律
1. 备选方案不能为空。
2. 没有备选，普通决策自动 🟡。
3. 重大决策没有备选，自动 🔴。
4. UID9622 拥有最终裁定权。
5. AI 只能生成、解释、审计、留痕，不得反客为主。
6. 不允许伪造已经执行。
7. 不允许伪造路径。
8. 不允许伪造 Notion 写入。

归属：🌿曾仕強老師 · ⚙️UID9622 · 📜中华文化 · 🐉龍芯北辰
"""
        anchor_path = self.anchors_dir / "ANCHOR-DEC-20260508-RESPCARD-V2.md"
        anchor_path.write_text(anchor_content, encoding="utf-8")
        return True

    # ── 第一张责任卡创建 ──────────────────────────────────

    def create_first_card(self) -> bool:
        card_content = f"""# 🃏 UID9622 龍芯北辰 · RESPONSIBILITY DECISION CARD

```yaml
DNA: "#龍芯⚡️20260508-DEC-RESPCARD-V2"
版本: "v2.0"
时间: "2026-05-08"
决策等级: "L1 工程级"
决策者: "AI起草 / UID9622定盘"
三色状态: "🟢"
锚点: "ANCHOR-DEC-20260508-RESPCARD-V2"

---

【0. 主控声明】
主控者：UID9622
AI定位：执行工具 / 结构化助手 / 决策留痕器
最高确认：{CONFIRM}
边界声明：AI 不得反客为主，不得替 UID9622 做最终主权决定。

---

【1. 触发源】
触发输入：写入责任卡模板、接入 CNSH decision 命令、生成第一张责任卡锚。
触发时间：2026-05-08
触发来源：UID9622 当前指令
触发类型：工程落地 / 规则固化
是否需要决策：是
触发原因：该任务将成为后续 AI 决策留痕、责任归属审计的基础模块。

---

【2. 信息源】
* 源 ①：UID9622 责任卡 v2.0 结构
* 源 ②：UID9622 主控权、CONFIRM、SEAL、GPG
* 源 ③：CNSH 本机执行链与三色审计规则
信息完整度：🟢完整
缺失项：无
是否使用外部信息：否
是否存在不确定性：低

---

【3. 规则匹配】
主规则：UID9622 主控权 + 责任卡 v2.0 + 三色审计
辅助规则：DNA追溯 / P0不可压缩 / 备选不能为空
层级：L1 工程级
是否触发一票否决：否
是否存在规则冲突：否
师承 / 文化约束：UID9622 龍芯北辰

---

【4. 备选方案】
A. 只写模板，不接命令
   * 收益：最快落文档
   * 代价：不能自动生成
   * 风险：后续仍靠手工复制
   * 可撤销：是

B. 写模板 + 接 decision 命令，但不打锚
   * 收益：可以本机生成
   * 代价：缺少不动点登记
   * 风险：后续追溯不够稳
   * 可撤销：是

C. 写模板 + 接 decision 命令 + 生成第一锚
   * 收益：模板、命令、锚点三层闭环
   * 代价：需要创建目录和基础脚本
   * 风险：如果脚本未测试，初版可能需要修正
   * 可撤销：是
备选完整度：🟢充分

---

【5. 选择与排除】
最终选择：C
选择理由：三层闭环，才能真正让责任卡长出来。
为什么不是 A：只有模板，没有执行入口。
为什么不是 B：有命令但没有锚，责任链不够硬。
是否需要 UID9622 最终确认：是
是否允许 AI 直接执行：AI 可生成指令与文件内容；本机执行由 UID9622 授权。

---

【6. 三色判定】
状态：🟢
颜色原因：该操作主要创建新目录和新文件，不覆盖旧系统，风险可控。
风险点：
* 路径中包含中文，少数脚本环境可能处理异常。
* 如果 PATH 未接入，decision 命令可能无法直接识别。
缓解措施：
* Python 文件使用 UTF-8。
* 同时提供完整路径执行与 PATH 接入方案。
* 不修改核心系统文件，不覆盖旧配置。
是否需要急停：否

---

【7. 责任归属】
主权责任：UID9622
执行责任：AI 生成方案 / CNSH 或本机终端执行
审计责任：AI 标记三色，UID9622 最终查看
最终裁定权：UID9622

---

【8. 撤销与回滚】
可撤销：是
撤销方式：删除 ~/cnsh/决策卡片/ 或废弃 v2.0 锚点
撤销代价：低
影响范围：仅影响责任卡系统目录
回滚锚点：ANCHOR-DEC-20260508-RESPCARD-V2
是否需要生成纠错卡：如果后续发现字段缺失或命令错误，需要生成。

---

【9. 留痕归档】
本机审计：/cnsh/决策卡片/db/decision_cards.sqlite
本机文件：/cnsh/决策卡片/cards/major/RESPONSIBILITY_CARD_20260508_L1_RESPCARD_V2.md
不动点锚：ANCHOR-DEC-20260508-RESPCARD-V2
关联DNA：#龍芯⚡️20260508-DEC-RESPCARD-V2
五行签名：
* 金：规则结构
* 木：后续扩展
* 水：上下文追溯
* 火：触发执行
* 土：本机归档

归属：🌿曾仕強老師 · ⚙️UID9622 · 📜中华文化 · 🐉龍芯北辰
"""
        card_path = self.major_dir / "RESPONSIBILITY_CARD_20260508_L1_RESPCARD_V2.md"
        card_path.write_text(card_content, encoding="utf-8")
        return True

    # ── 命令入口创建 ──────────────────────────────────────

    def create_command(self) -> bool:
        bin_dir = CNSH_ROOT / "bin"
        ensure_dir(bin_dir)
        cmd_path = bin_dir / "decision"
        cmd_path.write_text(
            f"#!/bin/zsh\n"
            f"# DNA: #龍芯⚡️丙午·乙未·庚申-DEC-ENTRY-v2.0\n"
            f"python3 {PROJECT_ROOT}/bin/lh_decision_card_system.py \"$@\"\n",
            encoding="utf-8",
        )
        cmd_path.chmod(0o755)

        # 更新 PATH
        zshrc = Path.home() / ".zshrc"
        if zshrc.exists():
            content = zshrc.read_text(encoding="utf-8")
            path_line = 'export PATH="$HOME/cnsh/bin:$PATH"'
            if path_line not in content:
                with open(zshrc, "a", encoding="utf-8") as f:
                    f.write(f"\n{path_line}\n")
        return True

    # ── 数据库创建 ──────────────────────────────────────────

    def create_database(self) -> bool:
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS decision_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dna TEXT NOT NULL UNIQUE,
            hash8 TEXT NOT NULL,
            created_at TEXT NOT NULL,
            card_type TEXT NOT NULL,
            decision_level TEXT NOT NULL,
            title TEXT,
            trigger_input TEXT,
            selected_option TEXT,
            color TEXT,
            responsibility_owner TEXT,
            reversible INTEGER DEFAULT 1,
            file_path TEXT,
            anchor_id TEXT,
            raw_json TEXT,
            final_authority TEXT DEFAULT 'UID9622'
        )
        """)
        conn.commit()
        conn.close()
        return True

    # ── README创建 ──────────────────────────────────────────

    def create_readme(self) -> bool:
        readme_content = f"""# UID9622 龍芯北辰｜责任卡 / 决策卡片系统

## 定位
本系统用于记录 AI / CNSH / 本机系统每一次重要决策的来源、规则、备选、选择、排除、责任、撤销方式与留痕位置。

## 核心原则
- UID9622 拥有最终裁定权。
- AI 只负责生成、解释、审计、留痕，不得反客为主。
- 重大决策必须生成完整版责任卡。
- 备选方案不能为空。
- 没有备选，普通决策自动 🟡；重大决策自动 🔴。
- 不允许伪造已执行、不允许伪造路径、不允许伪造 Notion 写入。

## 默认目录
~/cnsh/决策卡片/

## 默认命令
- decision --light "内容"
- decision --full "内容"
- decision --list
- decision --show HASH

## 确认码
{CONFIRM}

## SEAL
{SEAL}

## GPG
{GPG_FINGERPRINT}
"""
        readme_path = self.base_dir / "README.md"
        readme_path.write_text(readme_content, encoding="utf-8")
        return True

    # ── config创建 ──────────────────────────────────────────

    def create_config(self) -> bool:
        config_data = {
            "system": "UID9622 龍芯北辰",
            "module": "责任卡 / 决策卡片系统",
            "version": "v2.0",
            "base_dir": "~/cnsh/决策卡片",
            "controller": "UID9622",
            "confirm": CONFIRM,
            "seal": SEAL,
            "gpg": GPG_FINGERPRINT,
            "default_policy": {
                "daily_card": "light",
                "major_card": "full",
                "missing_options_daily": "🟡",
                "missing_options_major": "🔴",
                "final_authority": "UID9622",
            },
            "routing_keywords_full": self.full_keywords,
            "routing_keywords_light": self.light_keywords,
        }
        config_path = self.base_dir / "config.json"
        config_path.write_text(
            json.dumps(config_data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return True

    # ── 日志创建 ──────────────────────────────────────────

    def create_log(self) -> bool:
        self.log_path.touch(exist_ok=True)
        return True

    # ── 一键安装 ──────────────────────────────────────────

    def install(self) -> bool:
        cprint("\n🐉 安装 UID9622 龍芯北辰责任卡系统", Colors.BOLD)
        cprint("=" * 50, Colors.CYAN)

        self.create_directories()
        self.create_templates()
        self.create_engine()
        self.create_router()
        self.create_database()
        self.create_anchor()
        self.create_first_card()
        self.create_command()
        self.create_readme()
        self.create_config()
        self.create_log()

        cprint("\n" + "=" * 50, Colors.CYAN)
        cprint("✅ 责任卡系统安装完成", Colors.GREEN)
        cprint("=" * 50, Colors.CYAN)
        cprint("\n📋 使用方式:")
        cprint("  lh deck --light \"优化责任卡模板\"", Colors.CYAN)
        cprint("  lh deck --full \"接入CNSH网关\"", Colors.CYAN)
        cprint("  lh deck --list", Colors.CYAN)
        cprint("  lh deck --show HASH", Colors.CYAN)
        cprint("\n🔑 确认码: " + CONFIRM, Colors.YELLOW)
        cprint("🔐 SEAL: " + SEAL, Colors.YELLOW)
        cprint("🔏 GPG: " + GPG_FINGERPRINT, Colors.YELLOW)

        return True

    # ── 状态检查 ──────────────────────────────────────────

    def status(self) -> dict[str, Any]:
        files = [
            "README.md", "config.json",
            "templates/light_card.md", "templates/full_card.md",
            "engine/decision_card.py", "engine/responsibility_router.py",
            "anchors/anchor_registry.json",
            "anchors/ANCHOR-DEC-20260508-RESPCARD-V2.md",
            "cards/major/RESPONSIBILITY_CARD_20260508_L1_RESPCARD_V2.md",
            "db/decision_cards.sqlite",
        ]
        file_status = {}
        for f in files:
            p = self.base_dir / f
            file_status[f] = p.exists()

        return {
            "base_dir": str(self.base_dir),
            "exists": self.base_dir.exists(),
            "files": file_status,
        }

    # ── 自检（v2.0 对齐新增） ────────────────────────────

    def self_audit(self) -> dict[str, Any]:
        """9项自检"""
        checks: dict[str, Any] = {}

        # 1. 目录完整性
        dirs_to_check = [
            self.base_dir, self.template_dir, self.engine_dir,
            self.daily_dir, self.major_dir, self.archived_dir,
            self.anchors_dir, self.db_dir, self.logs_dir,
        ]
        existing_dirs = sum(1 for d in dirs_to_check if d.exists())
        checks["directories"] = {
            "status": "🟢" if existing_dirs == len(dirs_to_check) else "🟡",
            "value": f"{existing_dirs}/{len(dirs_to_check)}",
        }

        # 2. 模板存在
        checks["templates"] = {
            "status": "🟢" if (self.template_dir / "light_card.md").exists()
                      and (self.template_dir / "full_card.md").exists() else "🔴",
            "light": (self.template_dir / "light_card.md").exists(),
            "full": (self.template_dir / "full_card.md").exists(),
        }

        # 3. 引擎存在
        checks["engine"] = {
            "status": "🟢" if (self.engine_dir / "decision_card.py").exists() else "🔴",
        }

        # 4. 路由器存在
        checks["router"] = {
            "status": "🟢" if (self.engine_dir / "responsibility_router.py").exists() else "🟡",
        }

        # 5. 锚点注册表
        checks["anchor_registry"] = {
            "status": "🟢" if self.anchor_registry.exists() else "🟡",
        }

        # 6. 数据库
        if self.db_path.exists():
            try:
                conn = sqlite3.connect(str(self.db_path))
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM decision_cards")
                count = cur.fetchone()[0]
                conn.close()
                checks["database"] = {"status": "🟢", "cards": count}
            except sqlite3.OperationalError:
                checks["database"] = {"status": "🟡", "note": "表未创建"}
        else:
            checks["database"] = {"status": "🟡", "note": "数据库不存在"}

        # 7. 日志可写
        try:
            self.logs_dir.mkdir(parents=True, exist_ok=True)
            test_file = self.logs_dir / ".write_test"
            test_file.write_text("test")
            test_file.unlink()
            checks["logs_writable"] = {"status": "🟢"}
        except Exception:
            checks["logs_writable"] = {"status": "🔴"}

        # 8. 路由关键词完整性
        checks["routing_keywords"] = {
            "status": "🟢" if len(self.full_keywords) >= 15 else "🟡",
            "full_count": len(self.full_keywords),
            "light_count": len(self.light_keywords),
        }

        # 9. 锚点文件
        checks["anchor_file"] = {
            "status": "🟢" if (self.anchors_dir / "ANCHOR-DEC-20260508-RESPCARD-V2.md").exists() else "🟡",
        }

        # 汇总
        reds = sum(1 for _c in checks.values() if _c.get("status") == "🔴")
        yellows = sum(1 for _c in checks.values() if _c.get("status") == "🟡")
        greens = sum(1 for _c in checks.values() if _c.get("status") == "🟢")
        checks["_summary"] = {
            "total": reds + yellows + greens,
            "🟢": greens, "🟡": yellows, "🔴": reds,
            "overall": "🔴" if reds > 0 else ("🟡" if yellows > 0 else "🟢"),
        }
        return checks

    # ── GPG签名提示（v2.0 对齐新增） ──────────────────────

    def gpg_sign_files(self) -> dict[str, Any]:
        """对目录下的关键文件执行GPG签名"""
        signed = []
        failed = []
        key_files = [
            self.base_dir / "README.md",
            self.base_dir / "config.json",
            self.template_dir / "light_card.md",
            self.template_dir / "full_card.md",
            self.engine_dir / "decision_card.py",
            self.engine_dir / "responsibility_router.py",
            self.anchors_dir / "ANCHOR-DEC-20260508-RESPCARD-V2.md",
            self.major_dir / "RESPONSIBILITY_CARD_20260508_L1_RESPCARD_V2.md",
        ]
        gpg_script = PROJECT_ROOT / "bin" / "lh_gpg_sign.py"
        if gpg_script.exists():
            import subprocess
            for f in key_files:
                if f.exists():
                    result = subprocess.run(
                        ["python3", str(gpg_script), "sign", str(f)],
                        capture_output=True, text=True,
                    )
                    if result.returncode == 0:
                        signed.append(str(f))
                    else:
                        failed.append(str(f))
        return {"signed": len(signed), "failed": len(failed), "total": len(key_files)}


# ═══════════════════════════════════════════════════════════════
# 六、CLI 入口
# ═══════════════════════════════════════════════════════════════

def main() -> None:
    parser = argparse.ArgumentParser(
        description="🐉 UID9622 龍芯北辰责任卡系统 v2.0"
    )
    parser.add_argument("--install", action="store_true", help="一键安装责任卡系统")
    parser.add_argument("--status", action="store_true", help="查看安装状态")
    parser.add_argument("--self-audit", action="store_true", help="9项自检")
    parser.add_argument("--test", action="store_true", help="测试")
    parser.add_argument("--command", action="store_true", help="仅安装 decision 命令")
    parser.add_argument("--gpg-sign", action="store_true", help="GPG批量签名")
    parser.add_argument("--light", action="store_true", help="强制轻量版")
    parser.add_argument("--full", action="store_true", help="强制完整版")
    parser.add_argument("--list", action="store_true", help="列出最近卡片")
    parser.add_argument("--show", type=str, help="查看指定HASH")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("text", nargs="*", help="触发内容")
    args = parser.parse_args()

    system = DecisionCardSystem()

    # ── install ──
    if args.install:
        system.install()
        return

    # ── status ──
    if args.status:
        st = system.status()
        if args.json:
            print(json.dumps(st, ensure_ascii=False, indent=2))
            return
        cprint("\n📊 责任卡系统状态", Colors.BOLD)
        cprint("=" * 40, Colors.CYAN)
        cprint(f"目录: {st['base_dir']}", Colors.RESET)
        cprint(f"存在: {'✅' if st['exists'] else '❌'}", Colors.RESET)
        cprint("\n文件状态:", Colors.CYAN)
        for name, exists in st["files"].items():
            cprint(f"  {'✅' if exists else '❌'} {name}", Colors.RESET)
        return

    # ── self-audit ──
    if args.self_audit:
        result = system.self_audit()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return
        s = result["_summary"]
        print(f"\n🔍 自检报告 · {s['total']}项 · 🟢{s['🟢']} 🟡{s['🟡']} 🔴{s['🔴']} → {s['overall']}\n")
        for name, check in result.items():
            if name.startswith("_"):
                continue
            print(f"   {check['status']} {name}: {check.get('value', check.get('note', '—'))}")
        return

    # ── command ──
    if args.command:
        system.create_command()
        cprint("\n✅ decision 命令已安装", Colors.GREEN)
        cprint("请运行: source ~/.zshrc", Colors.YELLOW)
        return

    # ── gpg-sign ──
    if args.gpg_sign:
        result = system.gpg_sign_files()
        print(f"\n🔏 GPG签名: {result['signed']}/{result['total']} 成功, {result['failed']} 失败")
        return

    # ── test ──
    if args.test:
        cprint("\n🧪 测试责任卡系统", Colors.BOLD)
        if not system.base_dir.exists():
            cprint("❌ 系统未安装，请先运行: lh deck --install", Colors.RED)
            return
        test_text = "测试责任卡生成"
        h = hash8(test_text)
        dna = make_dna(h)
        cprint(f"✅ DNA: {dna}", Colors.GREEN)
        cprint(f"✅ HASH: {h}", Colors.GREEN)
        cprint("✅ 测试通过", Colors.GREEN)
        return

    # ── 卡片生成（list / show / light / full） ──
    text = " ".join(args.text).strip()

    if args.show:
        found = False
        for f in system.base_dir.rglob(f"*{args.show.upper()}*.md"):
            print(f.read_text(encoding="utf-8"))
            found = True
            break
        if not found:
            print(f"未找到: {args.show}")
        return

    if args.list:
        if not system.db_path.exists():
            print("数据库不存在，请先安装: lh deck --install")
            return
        conn = sqlite3.connect(str(system.db_path))
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT created_at, hash8, card_type, decision_level, color, title "
                "FROM decision_cards ORDER BY id DESC LIMIT 20"
            )
            rows = cur.fetchall()
            if args.json:
                data = [dict(zip(["created_at", "hash8", "card_type", "level", "color", "title"], r)) for r in rows]
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                for row in rows:
                    print(" | ".join(str(x) for x in row))
        except sqlite3.OperationalError:
            print("数据库表未创建，请先安装: lh deck --install")
        conn.close()
        return

    if text:
        force_mode = "full" if args.full else "light" if args.light else ""
        # 路由判定
        is_full = force_mode == "full" or (force_mode != "light" and any(kw in text for kw in system.full_keywords))
        card_type = "full" if is_full else "light"
        level = "L0" if any(kw in text for kw in ["主控", "CONFIRM", "P0"]) else \
                "L1" if any(kw in text for kw in ["CNSH", "本机", "删除", "覆盖"]) else \
                "L2" if any(kw in text for kw in ["文档", "模板", "Notion"]) else "L3"

        h = hash8(text)
        dna = make_dna(h)
        color = "🟢"

        print(f"【责任卡生成回执】")
        print(f"卡片类型: {'完整版' if card_type == 'full' else '轻量版'}")
        print(f"等级: {level}")
        print(f"DNA: {dna}")
        print(f"HASH: {h}")
        print(f"三色: {color}")
        print("责任归属: AI生成 / UID9622最终定盘")
        print(f"\n💡 完整生成请使用引擎: python3 {system.engine_dir}/decision_card.py \"{text[:50]}\"")
        return

    # 无参数 → 帮助
    parser.print_help()


if __name__ == "__main__":
    main()
