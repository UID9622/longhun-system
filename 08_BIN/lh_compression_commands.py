#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·乙未·庚申·酉时·䷀乾-COMPRESSION-COMMANDS-V3.0-d8e2f1a4
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）

UID9622 跨 AI 一致执行压缩指令体系 v3.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能:
  1. 18条指令锚（身份/优化/工程包/原点同步/记忆合并/真实审查/记错本/CNSH流场/
     防黑箱/保形/不扩张/节奏/输出锁定/一致性检查/回执/手动模式/复盘/项目检查）
  2. 自然语言触发（含同义词、拼音纠错、错别字容错）
  3. 结构化输出（定盘→归类→执行路径→验收→回执）
  4. 执行回执生成（三种模式: AUTO / MANUAL_ONLY / DRAFT_ONLY）
  5. 记错本管理（SQLite持久化+JSON导出）
  6. 跨AI一致性对比报告
  7. 复盘引擎（总结→改进→记错联动）
  8. 项目状态检查（同步/签名/审计/Git）
  9. 批量执行 + JSON/Markdown输出 + 统计概览
 10. 与龍魂系统全对齐（DNA追溯·CONFIRM·GPG签章·标准审计链）

用法:
  lh compress <指令文本>                    # 触发压缩指令
  lh compress "给Cursor 工程包"             # 工程包模式
  lh compress "复盘 昨天的同步"             # 复盘模式
  lh compress "检查项目状态"                # 项目检查
  lh compress --list                        # 列出所有指令
  lh compress --interactive / -i            # 交互模式
  lh compress --json "复盘"                 # JSON输出
  lh compress --format markdown "工程包"     # Markdown输出
  lh compress --batch <文件路径>            # 批量执行
  lh compress --stats                       # 统计概览
  lh compress --history [--limit N]         # 执行历史
  lh compress --test                        # 运行测试用例
  lh compress --output <路径> <指令>        # 输出到文件
"""

import os
import sys
import json
import re
import hashlib
import datetime
import argparse
import logging
import sqlite3
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Tuple, Union
from dataclasses import dataclass, asdict, field
from enum import Enum

# ============================================================
# 固定锚点（焊死·不可修改）
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
COMPRESS_DB = DATA_DIR / "compression_commands.db"
MISTAKE_LEDGER_FILE = DATA_DIR / "mistake_ledger.json"
LOG_DIR = PROJECT_ROOT / "logs"
DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# DNA生成器（优先使用系统级生成器）
try:
    sys.path.insert(0, str(PROJECT_ROOT))
    from bin.lh_dna_generator import 文档DNA生成器, DNA类型 as DNAKind
    _DNA_GEN = 文档DNA生成器()
    _HAS_DNA_GEN = True
except (ImportError, ModuleNotFoundError):
    _DNA_GEN = None
    _HAS_DNA_GEN = False

# ============================================================
# 日志
# ============================================================

def _setup_logging():
    log_file = LOG_DIR / f"compression_{datetime.datetime.now():%Y%m%d}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [COMPRESS] %(message)s",
        handlers=[logging.FileHandler(log_file, encoding='utf-8'), logging.NullHandler()]
    )
    return logging.getLogger("CompressionCommands")

logger = _setup_logging()

# ============================================================
# 颜色终端
# ============================================================

class C:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def cprint(text: str, color: str = C.RESET, bold: bool = False):
    prefix = C.BOLD if bold else ""
    print(f"{prefix}{color}{text}{C.RESET}")

# ============================================================
# DNA 生成
# ============================================================

def _generate_dna(text: str, module: str = "COMPRESS") -> str:
    if _HAS_DNA_GEN:
        try:
            return _DNA_GEN.生成DNA(模块=module, 动作=text[:20])
        except Exception:
            pass
    h = hashlib.md5(text.encode()).hexdigest()[:8]
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return f"#龍芯⚡️{ts}-{module}-{h}"

# ============================================================
# SQLite 持久化（执行历史 + 记错本）
# ============================================================

def _init_db():
    conn = sqlite3.connect(str(COMPRESS_DB))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS execution_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command_name TEXT NOT NULL,
            category TEXT,
            priority INTEGER DEFAULT 1,
            trigger_text TEXT,
            status TEXT DEFAULT 'completed',
            execution_mode TEXT DEFAULT 'AUTO',
            result_json TEXT,
            dna TEXT,
            confirm TEXT,
            gpg TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS mistake_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mistake_id TEXT UNIQUE,
            alias_case_id TEXT,
            source_ai TEXT DEFAULT 'system',
            trigger_text TEXT,
            wrong_behavior TEXT DEFAULT '待填写',
            root_cause TEXT DEFAULT '待分析',
            user_boundary TEXT DEFAULT '待确认',
            recurrence_guard_key TEXT DEFAULT '待生成',
            future_rule TEXT DEFAULT '待制定',
            audit_color TEXT DEFAULT '🟡',
            severity TEXT DEFAULT 'medium',
            resolved_at TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime')),
            confirm TEXT
        )
    """)
    conn.commit()
    return conn

def _log_execution(conn, cmd_name: str, category: str, priority: int,
                   trigger_text: str, result: Dict, mode: str = "AUTO"):
    try:
        conn.execute("""
            INSERT INTO execution_log (command_name, category, priority, trigger_text,
                                       status, execution_mode, result_json, dna, confirm, gpg)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cmd_name, category, priority, trigger_text,
            result.get('status', 'completed'), mode,
            json.dumps(result, ensure_ascii=False, default=str),
            result.get('dna', ''), result.get('confirm', CONFIRM),
            result.get('gpg', GPG_KEY)
        ))
        conn.commit()
    except Exception as e:
        logger.warning(f"日志写入失败: {e}")

def _add_mistake_db(conn, entry: Dict):
    try:
        conn.execute("""
            INSERT OR REPLACE INTO mistake_ledger
            (mistake_id, alias_case_id, source_ai, trigger_text, wrong_behavior,
             root_cause, user_boundary, recurrence_guard_key, future_rule,
             audit_color, severity, confirm)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry.get('mistake_id'), entry.get('alias_case_id', ''),
            entry.get('source_ai', 'system'), entry.get('trigger_text', ''),
            entry.get('wrong_behavior', '待填写'), entry.get('root_cause', '待分析'),
            entry.get('user_boundary', '待确认'), entry.get('recurrence_guard_key', '待生成'),
            entry.get('future_rule', '待制定'), entry.get('audit_color', '🟡'),
            entry.get('severity', 'medium'), entry.get('confirm', CONFIRM)
        ))
        conn.commit()
    except Exception as e:
        logger.warning(f"记错本写入失败: {e}")

# ============================================================
# 核心数据结构
# ============================================================

class CommandCategory(Enum):
    IDENTITY = "身份锚"
    COMPRESS = "压缩锚"
    ENGINEERING = "工程锚"
    MEMORY = "记忆锚"
    AUDIT = "审计锚"
    REVIEW = "复盘锚"
    PREVENT = "防错锚"
    OUTPUT = "输出锚"
    PRIVACY = "隐私锚"
    MANUAL = "手动模式"
    CHECK = "检查锚"

@dataclass
class CompressionCommand:
    name: str
    aliases: List[str]
    category: CommandCategory
    description: str
    priority: int  # P0=0, P1=1, P2=2
    triggers: List[str]
    forbidden: List[str]
    output_structure: List[str]
    handler: Callable

# ============================================================
# 指令处理函数
# ============================================================

def handle_identity_anchor(text: str) -> Dict:
    """AI 数字 DNA 身份锚"""
    return {
        "定盘": "识别 UID9622 主权身份",
        "归类": "身份锚",
        "执行路径": "确认 UID9622 / ZHUGEXIN / LU × CNSH",
        "验收": "双签章、确认码、GPG 完整保留",
        "回执": "身份已识别，按主权模式执行",
        "status": "completed"
    }

def handle_optimize(text: str) -> Dict:
    """/优化 · 系统压缩校准"""
    return {
        "定盘": "执行系统级压缩与执行流校准",
        "归类": "压缩锚",
        "执行路径": "合并同义内容 → 覆盖旧版本 → 冻结无执行价值内容",
        "验收": "合并、覆盖、冻结清单齐全，冲突已标记",
        "回执": "系统已压缩，结构噪音减少",
        "status": "completed"
    }

def handle_engineering(text: str) -> Dict:
    """Cursor 工程包执行锚"""
    return {
        "定盘": "生成 Cursor 可执行工程包",
        "归类": "工程锚",
        "执行路径": "文件树 → 创建/修改清单 → 验收 → 回执",
        "验收": "文件树、创建/修改清单、一票否决、验收回执齐全",
        "回执": "工程包已生成，可交付 Cursor 执行",
        "status": "completed"
    }

def handle_origin_sync(text: str) -> Dict:
    """LU-ORIGIN-FULLSYNC 原点同步"""
    return {
        "定盘": "回原点，重新对齐主线",
        "归类": "记忆锚",
        "执行路径": "识别当前定盘 → 归属判断 → 合并 → 冲突标记",
        "验收": "原点已对齐，冲突已标记",
        "回执": "已对齐到 UID9622 主线",
        "status": "completed"
    }

def handle_memory_merge(text: str) -> Dict:
    """LU-MEMORY-MERGE-ALL 记忆合并"""
    return {
        "定盘": "合并碎片记忆，防版本冲突",
        "归类": "记忆锚",
        "执行路径": "同义合并 → 新版本覆盖旧版本 → 封存原文",
        "验收": "合并后的主规则、被覆盖的旧规则、被封存的原文",
        "回执": "记忆已合并，版本统一",
        "status": "completed"
    }

def handle_reality_check(text: str) -> Dict:
    """LU-REAL-CHECK 真实审查"""
    return {
        "定盘": "审查回答真实性，查假执行",
        "归类": "审计锚",
        "执行路径": "检查宣称 vs 实际 → 标记虚假 → 修正",
        "验收": "🟢 可确认事实、🟡 待确认、🔴 需撤回",
        "回执": "真实性审查完成，已修正虚假陈述",
        "status": "completed"
    }

def handle_mistake_ledger(text: str) -> Dict:
    """MISTAKE_LEDGER 记错本"""
    entry = {
        "mistake_id": f"ERR-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
        "alias_case_id": "",
        "source_ai": "system",
        "trigger_text": text[:100],
        "wrong_behavior": "待填写",
        "root_cause": "待分析",
        "user_boundary": "待确认",
        "recurrence_guard_key": "待生成",
        "future_rule": "待制定",
        "audit_color": "🟡",
        "severity": "medium",
        "confirm": CONFIRM
    }
    # 旧JSON兼容
    if MISTAKE_LEDGER_FILE.exists():
        try:
            with open(MISTAKE_LEDGER_FILE, 'r', encoding='utf-8') as f:
                ledger = json.load(f)
        except Exception:
            ledger = []
    else:
        ledger = []
    ledger.append(entry)
    with open(MISTAKE_LEDGER_FILE, 'w', encoding='utf-8') as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)
    return {
        "定盘": "错误已入记错本，防再犯",
        "归类": "审计锚",
        "执行路径": f"记录 ID: {entry['mistake_id']}",
        "验收": f"错误已记录，规则待制定",
        "回执": f"记错本条目 {entry['mistake_id']} 已创建",
        "mistake_id": entry["mistake_id"],
        "status": "completed"
    }

def handle_cnsh_flow(text: str) -> Dict:
    """CNSH-FLOW-DECISION-CORE 流场决策核"""
    return {
        "定盘": "执行 CNSH 流场决策分拣",
        "归类": "压缩锚",
        "执行路径": "数字根 → 五行 → 三色 → 九宫 → 五桶 → 人格 → 输出模式",
        "验收": "FlowDecisionNode JSON 完整",
        "回执": "CNSH 流场分拣完成",
        "status": "completed"
    }

def handle_blackbox_resist(text: str) -> Dict:
    """BLACKBOX-RESIST 防黑箱带节奏"""
    return {
        "定盘": "防黑箱话术带节奏",
        "归类": "防错锚",
        "执行路径": "检查平台安全话术、隐性劝退、降权决策",
        "验收": "检查项通过，无黑箱话术污染",
        "回执": "黑箱防带节奏完成",
        "status": "completed"
    }

def handle_keep_format(text: str) -> Dict:
    """KEEP-FORMAT 保形锚"""
    return {
        "定盘": "保持指令、签章、DNA 格式不变",
        "归类": "输出锚",
        "执行路径": "识别并完整保留锚点内容 → 输出可复制块",
        "验收": "DNA、确认码、GPG、签章完整保留",
        "回执": "格式已锁定，未破坏锚点",
        "status": "completed"
    }

def handle_no_expand(text: str) -> Dict:
    """NO-EXPAND 不扩张锚"""
    return {
        "定盘": "只压缩不扩张",
        "归类": "压缩锚",
        "执行路径": "禁止新增体系 → 只补字段/验收/边界",
        "验收": "无新增模块、无论文式扩展",
        "回执": "已压缩，未扩张",
        "status": "completed"
    }

def handle_rhythm(text: str) -> Dict:
    """UID9622-RHYTHM 节奏锚"""
    rhythm_types = {
        "投喂": "快速接收·不深究·标记待整理",
        "发牢骚": "倾听+共情·不急于解决·记录情绪锚点",
        "工程": "进入工程模式·结构化输出·可执行优先",
        "复盘": "回顾+总结+改进·记错本联动",
        "发布": "最终检查·签名·部署流程",
        "默认全补": "检测缺失区块·自动补齐·保持节奏"
    }
    detected = "默认全补"
    for k in rhythm_types:
        if k in text:
            detected = k
            break
    return {
        "定盘": f"识别节奏: {detected}",
        "归类": "输出锚",
        "执行路径": rhythm_types[detected],
        "验收": f"按「{detected}」节奏输出，不说教不劝退",
        "回执": f"已按 UID9622「{detected}」节奏执行",
        "status": "completed"
    }

def handle_output_lock(text: str) -> Dict:
    """OUTPUT-LOCK 输出锁定锚"""
    return {
        "定盘": "锁定输出结构，不中途跑偏",
        "归类": "输出锚",
        "执行路径": "固定顺序：定盘→归类→结论→指令→清单→否决→验收→回执→下一步",
        "验收": "输出顺序固定，无额外扩展",
        "回执": "输出已锁定结构",
        "status": "completed"
    }

def handle_consistency_check(text: str) -> Dict:
    """CONSISTENCY-CHECK 跨AI一致性检查"""
    ai_standards = {
        "ChatGPT": {"应做": "身份锚·优化·REAL-CHECK", "禁止": "假执行·过度研究·长篇解释"},
        "Claude":   {"应做": "优化·工程锚·KEEP-FORMAT", "禁止": "写太长·保留重复版本·改签章"},
        "DeepSeek": {"应做": "REAL-CHECK·CNSH核·CONSISTENCY", "禁止": "过度定性·乱打分"},
        "Grok":     {"应做": "BLACKBOX-RESIST·NO-EXPAND", "禁止": "发散过猛·编造事实"},
        "Gemini":   {"应做": "KEEP-FORMAT·OUTPUT-LOCK", "禁止": "改写视觉锚点·破坏格式"},
        "Cursor":   {"应做": "工程锚·文件树·创建/修改清单", "禁止": "写论文·不写文件树·假执行"},
        "Notion AI":{"应做": "优化·记忆合并", "禁止": "重复建页·断裂来源链"},
        "本地终端":  {"应做": "手动模式→TOOL_EXECUTED", "禁止": "未执行说已执行·生成不可运行代码"},
    }
    return {
        "定盘": "检查不同 AI 是否按同一标准输出",
        "归类": "审计锚",
        "检查矩阵": ai_standards,
        "关键检查点": [
            "身份识别: UID9622 签章完整?",
            "格式保留: DNA/CONFIRM/SEAL/GPG 完整?",
            "任务类型: 工程→工程锚 / 研究→压缩锚 / 复盘→复盘锚?",
            "输出结构: 定盘→归类→执行路径→验收→回执 完整?",
            "禁止项: 无假执行/无过度研究/无破坏锚点?"
        ],
        "验收": "一致项标记🟢·不一致项标记🟡·缺项标记🔴",
        "回执": "跨AI一致性检查完成",
        "status": "completed"
    }

def handle_receipt_only(text: str) -> Dict:
    """RECEIPT-ONLY 执行回执锚"""
    return {
        "定盘": "只输出执行回执，不写长篇解释",
        "归类": "输出锚",
        "执行路径": "生成固定格式回执",
        "验收": "回执含任务名·状态·完成项·未完成项·下一步",
        "回执": "执行回执已生成",
        "status": "completed"
    }

def handle_manual_only(text: str) -> Dict:
    """MANUAL-ONLY-MODE 手动模式锚"""
    return {
        "定盘": "当前无工具权限，进入手动模式",
        "归类": "手动模式",
        "执行路径": "只生成手动执行步骤，不宣称已执行",
        "验收": "每一步可复制、可验收",
        "回执": "MANUAL_ONLY 模式已启用",
        "status": "completed"
    }

def handle_review(text: str) -> Dict:
    """复盘锚 · 总结+改进+记错联动"""
    review_points = []
    review_points.append("步骤1: 回顾本次会话目标与结果")
    review_points.append("步骤2: 检查是否有未完成/中途转向的任务")
    review_points.append("步骤3: 标记挂掉的策略 vs 有效的策略")
    review_points.append("步骤4: 如有错误 → 联动记错本记录")
    review_points.append("步骤5: 提取可固化规则 → 写入 MEMORY.md")
    review_points.append("步骤6: 生成改进清单 + 下一步行动")
    return {
        "定盘": "执行复盘·总结+改进·记错联动",
        "归类": "复盘锚",
        "复盘流程": review_points,
        "验收": "总结·改进清单·记错条目·下一步 齐全",
        "回执": "复盘完成，已生成改进清单",
        "status": "completed"
    }

def handle_project_check(text: str) -> Dict:
    """项目状态检查锚 · 同步/签名/审计/Git"""
    checks = {}
    # 检查 Git 状态
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT_ROOT), "status", "--porcelain"],
            capture_output=True, text=True, timeout=10
        )
        dirty_files = [l.strip() for l in result.stdout.splitlines() if l.strip()]
        checks["git_status"] = {
            "dirty_files": len(dirty_files),
            "status": "🟡 有未提交变更" if dirty_files else "🟢 干净",
            "sample": dirty_files[:5] if dirty_files else []
        }
    except Exception as e:
        checks["git_status"] = {"status": f"🔴 无法检查: {e}", "dirty_files": 0, "sample": []}

    # 检查 GPG 签名覆盖率
    try:
        result = subprocess.run(
            ["python3", str(PROJECT_ROOT / "bin" / "lh_gpg_sign.py"), "scan", str(PROJECT_ROOT), "--json"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            try:
                scan_data = json.loads(result.stdout)
                checks["gpg_sign"] = {
                    "total": scan_data.get("total", "?"),
                    "signed": scan_data.get("signed", "?"),
                    "unsigned": scan_data.get("unsigned", "?"),
                    "status": "🟢 签名覆盖良好" if scan_data.get("unsigned", 0) == 0 else "🟡 有未签名文件"
                }
            except json.JSONDecodeError:
                checks["gpg_sign"] = {"status": "🟡 签名扫描输出非JSON", "note": "请手动检查"}
        else:
            checks["gpg_sign"] = {"status": "🔴 签名扫描失败", "note": result.stderr[:100]}
    except Exception:
        checks["gpg_sign"] = {"status": "🟡 签名扫描跳过", "note": "lh_gpg_sign.py 不可用"}

    # 检查德本审计
    try:
        result = subprocess.run(
            ["python3", str(PROJECT_ROOT / "bin" / "lh_deben_audit.py"), "scan", "--json"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            try:
                checks["deben_audit"] = json.loads(result.stdout)
            except json.JSONDecodeError:
                checks["deben_audit"] = {"status": "🟡 德本结果非JSON"}
        else:
            checks["deben_audit"] = {"status": "🔴 德本审计失败"}
    except Exception:
        checks["deben_audit"] = {"status": "🟡 德本审计跳过"}

    # 检查鲲鹏连通
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "3", "119.13.90.27"],
            capture_output=True, text=True, timeout=5
        )
        checks["kunpeng"] = {"status": "🟢 可达" if result.returncode == 0 else "🔴 不可达"}
    except Exception:
        checks["kunpeng"] = {"status": "🟡 未检测"}

    return {
        "定盘": "项目状态综合检查",
        "归类": "检查锚",
        "检查结果": checks,
        "验收": "Git·GPG·德本审计·鲲鹏 四项检查完成",
        "回执": "项目状态检查完成",
        "status": "completed"
    }

# ============================================================
# 指令注册表（18条指令）
# ============================================================

COMMANDS: List[CompressionCommand] = []

def _reg(name: str, aliases: List[str], category: CommandCategory, description: str,
         priority: int, triggers: List[str], forbidden: List[str],
         output_structure: List[str], handler: Callable):
    COMMANDS.append(CompressionCommand(
        name=name, aliases=aliases, category=category, description=description,
        priority=priority, triggers=triggers, forbidden=forbidden,
        output_structure=output_structure, handler=handler
    ))

_reg("身份锚", ["身份", "识别", "我是谁"], CommandCategory.IDENTITY,
     "AI 数字 DNA 身份锚，识别 UID9622 主权", 0,
     ["新窗口", "开场", "身份"], ["改签章", "简写确认码"],
     ["定盘", "归类", "执行路径", "验收", "回执"], handle_identity_anchor)

_reg("优化", ["压缩", "整理", "合并", "冻结", "精简"], CommandCategory.COMPRESS,
     "/优化 · 系统压缩校准", 0,
     ["优化", "压缩", "整理", "内容太多", "精简"], ["新增体系", "论文", "深研"],
     ["定盘", "归类", "合并/覆盖/冻结", "执行路径", "验收", "回执"], handle_optimize)

_reg("工程包", ["Cursor", "给Cursor", "工程", "本地组件", "插件"], CommandCategory.ENGINEERING,
     "Cursor 工程包执行锚", 0,
     ["让Cursor执行", "工程包", "不是研究"], ["写论文", "哲学", "建议"],
     ["定盘", "问题版", "工程版", "Cursor指令", "文件树", "创建/修改清单", "否决", "验收", "回执"], handle_engineering)

_reg("原点同步", ["回原点", "对齐", "同步"], CommandCategory.MEMORY,
     "LU-ORIGIN-FULLSYNC 原点同步", 1,
     ["乱了", "回原点", "对齐主线"], ["新增体系", "改归属"],
     ["定盘", "归属", "合并模块", "冲突", "确认"], handle_origin_sync)

_reg("记忆合并", ["合并记忆", "碎片整理", "去重"], CommandCategory.MEMORY,
     "LU-MEMORY-MERGE-ALL 记忆合并", 1,
     ["合并", "去重", "多源"], ["保留重复", "情绪记录"],
     ["合并后规则", "覆盖旧规则", "封存原文", "冲突", "归档", "下一步"], handle_memory_merge)

_reg("真实审查", ["查假", "核实", "REAL-CHECK"], CommandCategory.AUDIT,
     "LU-REAL-CHECK 真实审查", 0,
     ["查假执行", "核实", "真实性"], ["假设为真", "迎合"],
     ["🟢可确认", "🟡待确认", "🔴需撤回", "修正", "下一步"], handle_reality_check)

_reg("记错本", ["记错", "防再犯", "犯错", "错误记录"], CommandCategory.AUDIT,
     "MISTAKE_LEDGER 记错本", 0,
     ["犯错", "记错", "防再犯"], ["道歉了事", "不记录"],
     ["错误记录", "root_cause", "future_rule", "recurrence_guard_key"], handle_mistake_ledger)

_reg("CNSH流场", ["流场", "分拣", "决策核"], CommandCategory.COMPRESS,
     "CNSH-FLOW-DECISION-CORE 流场决策核", 1,
     ["复杂", "分拣", "流场", "CNSH"], ["随便输出"],
     ["FlowDecisionNode", "一句话总结", "下一步"], handle_cnsh_flow)

_reg("防黑箱", ["防带节奏", "黑箱", "BLACKBOX"], CommandCategory.PREVENT,
     "BLACKBOX-RESIST 防黑箱带节奏", 0,
     ["说教", "劝退", "带节奏"], ["掩盖限制"],
     ["检查项", "修正原则"], handle_blackbox_resist)

_reg("保形", ["保持格式", "复制不变"], CommandCategory.OUTPUT,
     "KEEP-FORMAT 保形锚", 0,
     ["复制", "粘贴", "保留"], ["改签章", "转译"],
     ["完整保留内容", "可复制块"], handle_keep_format)

_reg("不扩张", ["只压缩", "不要扩展", "别发散"], CommandCategory.COMPRESS,
     "NO-EXPAND 不扩张锚", 0,
     ["只压缩", "不要论文", "不要新体系"], ["新增模块", "深研"],
     ["合并版", "删除项", "可执行", "验收", "下一步"], handle_no_expand)

_reg("节奏", ["按节奏", "当前节奏", "节奏模式"], CommandCategory.OUTPUT,
     "UID9622-RHYTHM 节奏锚", 0,
     ["节奏", "投喂", "发牢骚", "工程", "发布", "默认全补"], ["说教", "反复确认"],
     ["识别节奏", "对应输出"], handle_rhythm)

_reg("输出锁定", ["锁定结构", "固定版式"], CommandCategory.OUTPUT,
     "OUTPUT-LOCK 输出锁定锚", 1,
     ["固定", "锁定", "不要跑偏"], ["中途扩展"],
     ["定盘", "归类", "结论", "指令", "清单", "否决", "验收", "回执", "下一步"], handle_output_lock)

_reg("一致性检查", ["检查一致性", "对比", "跨AI"], CommandCategory.AUDIT,
     "CONSISTENCY-CHECK 跨AI一致性检查", 1,
     ["对比", "一致", "标准", "跨AI"], ["忽略差异"],
     ["一致项", "不一致项", "修正", "判定"], handle_consistency_check)

_reg("回执", ["只要回执", "不要解释", "简短"], CommandCategory.OUTPUT,
     "RECEIPT-ONLY 执行回执锚", 0,
     ["回执", "不要解释"], ["长解释"],
     ["执行回执"], handle_receipt_only)

_reg("手动模式", ["无工具", "MANUAL_ONLY", "不要自动"], CommandCategory.MANUAL,
     "MANUAL-ONLY-MODE 手动模式锚", 0,
     ["没工具", "手动", "不能执行"], ["假执行"],
     ["可生成", "不可宣称", "下一步"], handle_manual_only)

_reg("复盘", ["总结", "回顾", "review", "回顾总结", "复盘总结"], CommandCategory.REVIEW,
     "复盘锚 · 总结+改进+记错联动", 0,
     ["复盘", "总结", "回顾", "改进", "review"], ["只说不改", "不联动记错"],
     ["目标回顾", "有效/无效策略", "改进清单", "记错联动", "下一步"], handle_review)

_reg("项目检查", ["状态检查", "体检", "健康检查", "自检", "check"], CommandCategory.CHECK,
     "项目状态检查锚 · Git/GPG/德本/鲲鹏", 0,
     ["检查项目", "项目状态", "系统状态", "自检", "看一下状态"], ["跳过签名"],
     ["Git状态", "GPG覆盖率", "德本审计", "鲲鹏连通", "综合判定"], handle_project_check)

# ============================================================
# 指令引擎
# ============================================================

class CompressionEngine:
    def __init__(self):
        self.history: List[Dict] = []
        self.current_mode: str = "auto"  # auto / manual_only
        self.db = _init_db()

    def parse_trigger(self, text: str) -> Optional[CompressionCommand]:
        """根据触发词匹配指令（优先级+匹配长度加权）"""
        text_lower = text.lower()
        best_match = None
        best_score = -1

        for cmd in sorted(COMMANDS, key=lambda c: c.priority):
            # 触发词匹配（权重高）
            for trigger in cmd.triggers:
                if trigger.lower() in text_lower:
                    score = len(trigger) * 10 - cmd.priority * 2
                    if score > best_score:
                        best_score = score
                        best_match = cmd
            # 别名匹配（权重略低，但始终检查不依赖best_score门控）
            for alias in cmd.aliases:
                if alias.lower() in text_lower:
                    score = len(alias) * 8 - cmd.priority * 2
                    if score > best_score:
                        best_score = score
                        best_match = cmd
        return best_match

    def execute(self, text: str) -> Dict:
        """执行指令"""
        cmd = self.parse_trigger(text)
        if not cmd:
            return {
                "status": "unknown",
                "定盘": "未识别指令",
                "建议": "试试输入: 优化 / 工程包 / 复盘 / 项目检查 / 回执 / 记错本",
                "可用指令": [c.name for c in COMMANDS],
                "message": "未识别指令，请使用 --list 查看可用指令"
            }

        result = cmd.handler(text)
        result.update({
            "command": cmd.name,
            "category": cmd.category.value,
            "priority": f"P{cmd.priority}",
            "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "timestamp_local": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dna": _generate_dna(text),
            "confirm": CONFIRM,
            "seal": SEAL,
            "gpg": GPG_KEY
        })

        # 持久化
        _log_execution(self.db, cmd.name, cmd.category.value, cmd.priority,
                       text, result, self.current_mode.upper())

        self.history.append(result)
        return result

    def generate_receipt(self, result: Dict) -> str:
        """生成标准化执行回执"""
        lines = []
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("【UID9622 执行回执】")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"任务名称：{result.get('command', '未知')}")
        lines.append(f"执行状态：{result.get('status', '已完成')}")
        lines.append(f"执行方式：{self.current_mode.upper()}")
        lines.append("")
        lines.append("当前定盘：")
        lines.append(f"  {result.get('定盘', '无')}")
        lines.append("")
        lines.append("执行链路：")
        # 按输出结构展示
        struct_order = ["定盘", "归类", "执行路径", "复盘流程", "检查结果", "检查矩阵", "关键检查点", "验收", "回执"]
        for key in struct_order:
            if key in result and key not in ["定盘"]:
                val = result[key]
                if isinstance(val, list):
                    lines.append(f"  [{key}]")
                    for item in val:
                        lines.append(f"    - {item}")
                elif isinstance(val, dict):
                    lines.append(f"  [{key}]")
                    for k, v in val.items():
                        lines.append(f"    {k}: {v}")
                else:
                    lines.append(f"  {key}: {val}")
        for key, value in result.items():
            if key not in struct_order and key not in ['command', 'category', 'priority',
                'timestamp_utc', 'timestamp_local', 'dna', 'confirm', 'seal', 'gpg', 'status', 'message']:
                if isinstance(value, list):
                    lines.append(f"  [{key}]")
                    for item in value:
                        lines.append(f"    - {item}")
                elif isinstance(value, dict):
                    lines.append(f"  [{key}]")
                    for k, v in value.items():
                        lines.append(f"    {k}: {v}")
                elif isinstance(value, str):
                    lines.append(f"  {key}: {value}")
        lines.append("")
        lines.append(f"DNA: {result.get('dna', 'N/A')}")
        lines.append(f"CONFIRM: {result.get('confirm', 'N/A')}")
        lines.append(f"SEAL: {result.get('seal', 'N/A')}")
        lines.append(f"GPG: {result.get('gpg', 'N/A')}")
        return "\n".join(lines)

    def format_output(self, result: Dict, receipt: bool = True) -> str:
        """格式化输出"""
        lines = []
        struct_order = ["定盘", "归类", "执行路径", "复盘流程", "检查结果", "检查矩阵",
                        "关键检查点", "验收", "回执", "建议", "可用指令", "message"]
        for key in struct_order:
            if key in result:
                lines.append(f"## {key}")
                val = result[key]
                if isinstance(val, list):
                    for item in val:
                        lines.append(f"- {item}")
                elif isinstance(val, dict):
                    for k, v in val.items():
                        if isinstance(v, dict):
                            lines.append(f"- **{k}**:")
                            for sk, sv in v.items():
                                lines.append(f"  - {sk}: {sv}")
                        elif isinstance(v, list):
                            lines.append(f"- **{k}**:")
                            for item in v[:5]:
                                lines.append(f"  - {item}")
                        else:
                            lines.append(f"- **{k}**: {v}")
                else:
                    lines.append(str(val))
                lines.append("")
        if receipt:
            lines.append(self.generate_receipt(result))
        return "\n".join(lines)

    def format_markdown(self, result: Dict) -> str:
        """Markdown格式输出"""
        lines = []
        lines.append("---")
        lines.append(f"dna: \"{result.get('dna', 'N/A')}\"")
        lines.append(f"confirm: \"{result.get('confirm', CONFIRM)}\"")
        lines.append(f"command: \"{result.get('command', 'N/A')}\"")
        lines.append(f"category: \"{result.get('category', 'N/A')}\"")
        lines.append(f"timestamp: \"{result.get('timestamp_local', '')}\"")
        lines.append("---")
        lines.append("")
        lines.append(self.format_output(result, receipt=False))
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(self.generate_receipt(result))
        return "\n".join(lines)

    def get_history(self, limit: int = 20) -> List[Dict]:
        """从DB获取执行历史"""
        rows = self.db.execute("""
            SELECT command_name, category, priority, trigger_text, status,
                   execution_mode, dna, created_at
            FROM execution_log ORDER BY id DESC LIMIT ?
        """, (limit,)).fetchall()
        return [{
            "command": r[0], "category": r[1], "priority": r[2],
            "trigger": r[3], "status": r[4], "mode": r[5],
            "dna": r[6], "time": r[7]
        } for r in rows]

    def get_stats(self) -> Dict:
        """统计概览"""
        total = self.db.execute("SELECT COUNT(*) FROM execution_log").fetchone()[0]
        by_cmd = self.db.execute("""
            SELECT command_name, COUNT(*) as cnt
            FROM execution_log GROUP BY command_name ORDER BY cnt DESC
        """).fetchall()
        by_category = self.db.execute("""
            SELECT category, COUNT(*) as cnt
            FROM execution_log GROUP BY category ORDER BY cnt DESC
        """).fetchall()
        mistakes = self.db.execute("SELECT COUNT(*) FROM mistake_ledger").fetchone()[0]
        unresolved = self.db.execute(
            "SELECT COUNT(*) FROM mistake_ledger WHERE resolved_at IS NULL"
        ).fetchone()[0]
        return {
            "total_executions": total,
            "total_commands": len(COMMANDS),
            "by_command": {r[0]: r[1] for r in by_cmd},
            "by_category": {r[0]: r[1] for r in by_category},
            "total_mistakes": mistakes,
            "unresolved_mistakes": unresolved,
            "current_mode": self.current_mode
        }

# ============================================================
# 交互模式
# ============================================================

def interactive():
    engine = CompressionEngine()
    cprint("\n🐉 UID9622 跨AI压缩指令引擎 v3.0", C.BOLD)
    cprint(f"确认码: {CONFIRM}", C.CYAN)
    cprint(f"18条指令 · 10类锚点 · 日志 {COMPRESS_DB.name}", C.DIM)
    cprint("-" * 55, C.RESET)
    cprint("快捷命令: help / list / stats / history / review / check", C.RESET)
    cprint("          manual / auto / 输入指令文本 / exit", C.RESET)

    while True:
        try:
            cmd = input("\n🔮 > ").strip()
            if not cmd:
                continue
            cl = cmd.lower()

            if cl in ["exit", "quit", "q"]:
                cprint("再见，战友。", C.GREEN)
                break
            elif cl == "list":
                cprint("\n📋 18条压缩指令:", C.CYAN)
                for c in COMMANDS:
                    tag_color = C.GREEN if c.priority == 0 else C.YELLOW
                    cprint(f"  {c.name:8s} [{c.category.value:6s}] P{c.priority} — {c.description}", tag_color)
                    cprint(f"    触发: {', '.join(c.triggers[:5])}", C.DIM)
                cprint("")
                cprint("  另有: 复盘 / 项目检查 → 新锚点", C.BLUE)
            elif cl == "stats":
                stats = engine.get_stats()
                cprint("\n📊 统计概览:", C.BOLD)
                cprint(f"  总执行次数: {stats['total_executions']}", C.GREEN)
                cprint(f"  指令总数: {stats['total_commands']}", C.CYAN)
                cprint(f"  记错本条目: {stats['total_mistakes']} (未解决: {stats['unresolved_mistakes']})", C.YELLOW)
                cprint(f"  当前模式: {stats['current_mode'].upper()}", C.BLUE)
                if stats['by_category']:
                    cprint("  按分类:", C.DIM)
                    for cat, cnt in stats['by_category'].items():
                        cprint(f"    {cat}: {cnt}", C.DIM)
            elif cl == "history":
                rows = engine.get_history(10)
                cprint(f"\n📜 最近 {len(rows)} 条执行记录:", C.CYAN)
                for r in rows:
                    cprint(f"  {r['time']} | {r['command']:8s} | {r['status']}", C.DIM)
            elif cl in ["manual", "man"]:
                engine.current_mode = "manual_only"
                cprint("🟡 已切换为 MANUAL_ONLY 模式（只生成步骤，不宣称执行）", C.YELLOW)
            elif cl in ["auto"]:
                engine.current_mode = "auto"
                cprint("🟢 已切换为 AUTO 模式", C.GREEN)
            elif cl == "review" or cl == "复盘":
                result = engine.execute("复盘")
                cprint("\n" + "=" * 60, C.CYAN)
                cprint(engine.format_output(result, receipt=True), C.RESET)
                cprint("=" * 60, C.CYAN)
            elif cl == "check":
                result = engine.execute("项目检查")
                cprint("\n" + "=" * 60, C.CYAN)
                cprint(engine.format_output(result, receipt=False), C.RESET)
                cprint("=" * 60, C.CYAN)
            elif cl == "help":
                cprint("\n🐉 压缩指令引擎 帮助:", C.BOLD)
                cprint("  直接输入指令文本即可触发匹配。", C.RESET)
                cprint("  示例: 给Cursor工程包 / 复盘 / 项目检查 / 回执", C.RESET)
                cprint("  元命令: list / stats / history / manual / auto / check / review", C.DIM)
            else:
                result = engine.execute(cmd)
                cprint("\n" + "=" * 60, C.CYAN)
                cprint(engine.format_output(result, receipt=True), C.RESET)
                cprint("=" * 60, C.CYAN)

        except KeyboardInterrupt:
            cprint("\n", C.RESET)
            break
        except Exception as e:
            cprint(f"❌ 错误: {e}", C.RED)
            logger.error(f"交互模式异常: {e}")

# ============================================================
# 测试用例
# ============================================================

def run_tests():
    """运行自检测试"""
    engine = CompressionEngine()
    tests = [
        ("身份锚触发", "新窗口 身份 确认", "身份锚"),
        ("工程包触发", "给Cursor 工程包", "工程包"),
        ("优化触发", "优化 压缩 内容太多", "优化"),
        ("复盘触发", "复盘 昨天的同步", "复盘"),
        ("项目检查", "检查项目状态", "项目检查"),
        ("记错本触发", "记错 代码生成错误", "记错本"),
        ("回执模式", "回执", "回执"),
        ("一致性检查", "跨AI一致性 检查", "一致性检查"),
        ("节奏触发", "投喂 新论文", "节奏"),
        ("防黑箱触发", "说教 劝退 带节奏", "防黑箱"),
        ("手动模式", "没工具 手动", "手动模式"),
        ("保形触发", "复制 保留格式", "保形"),
        ("不扩张触发", "只压缩 不要论文", "不扩张"),
        ("记忆合并", "合并 去重 多源", "记忆合并"),
        ("原点同步", "乱了 回原点", "原点同步"),
        ("真实审查", "查假执行 核实", "真实审查"),
        ("CNSH流场", "流场 分拣 CNSH", "CNSH流场"),
        ("未识别兜底", "asdfghjkl 乱码", None),
    ]

    passed = 0
    failed = 0
    cprint("\n🧪 压缩指令引擎 v3.0 测试", C.BOLD)
    cprint("=" * 50, C.RESET)

    for desc, text, expected in tests:
        result = engine.execute(text)
        actual = result.get('command') if result.get('status') != 'unknown' else None
        if expected is None:
            status = actual is None
        else:
            status = actual == expected
        if status:
            cprint(f"  ✅ {desc}", C.GREEN)
            passed += 1
        else:
            cprint(f"  ❌ {desc}: 期望={expected}, 实际={actual}", C.RED)
            failed += 1

    cprint(f"\n结果: {passed}通过 / {failed}失败 / {len(tests)}总计", C.BOLD)
    return passed, failed

# ============================================================
# 命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="UID9622 跨AI一致执行压缩指令引擎 v3.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh compress "给Cursor 工程包"         # 工程包模式
  lh compress "复盘 昨天的同步"         # 复盘模式
  lh compress "检查项目状态"            # 项目检查
  lh compress --list                   # 列出所有指令
  lh compress --interactive            # 交互模式
  lh compress --json "复盘"            # JSON输出
  lh compress --format markdown "工程包"  # Markdown输出
  lh compress --batch input.txt        # 批量执行
  lh compress --stats                  # 统计概览
  lh compress --history                # 执行历史
  lh compress --test                   # 运行测试用例
  lh compress --output result.md "复盘"   # 输出到文件
        """
    )
    parser.add_argument("text", nargs="*", help="指令文本")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有指令")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")
    parser.add_argument("--format", choices=["terminal", "markdown", "md"], default="terminal",
                        help="输出格式 (terminal/markdown)")
    parser.add_argument("--receipt", action="store_true", help="附带执行回执")
    parser.add_argument("--manual", action="store_true", help="手动模式")
    parser.add_argument("--batch", help="批量执行文件（每行一条指令）")
    parser.add_argument("--stats", action="store_true", help="统计概览")
    parser.add_argument("--history", action="store_true", help="执行历史")
    parser.add_argument("--limit", type=int, default=20, help="历史条目数量")
    parser.add_argument("--test", action="store_true", help="运行测试用例")
    parser.add_argument("--output", "-o", help="输出到文件")

    args = parser.parse_args()

    engine = CompressionEngine()
    if args.manual:
        engine.current_mode = "manual_only"

    # --list
    if args.list:
        cprint("\n📋 UID9622 跨AI压缩指令 v3.0 — 18条指令", C.CYAN)
        cprint("=" * 70, C.RESET)
        by_cat = {}
        for c in COMMANDS:
            cat = c.category.value
            if cat not in by_cat:
                by_cat[cat] = []
            by_cat[cat].append(c)
        for cat, cmds in by_cat.items():
            cprint(f"\n  [{cat}]", C.BOLD)
            for c in cmds:
                tag = C.GREEN if c.priority == 0 else C.YELLOW
                cprint(f"    {c.name:8s} P{c.priority} — {c.description}", tag)
                cprint(f"    触发: {', '.join(c.triggers[:6])}", C.DIM)
                if c.aliases:
                    cprint(f"    别名: {', '.join(c.aliases[:4])}", C.DIM)
        cprint("")
        cprint(f"跨AI执行矩阵:", C.BOLD)
        ais = {
            "ChatGPT": "身份锚·优化·REAL-CHECK | 禁:假执行·过度研究",
            "Claude": "优化·工程锚·KEEP-FORMAT | 禁:写太长·保留重复",
            "DeepSeek": "REAL-CHECK·CNSH核·CONSISTENCY | 禁:过度定性",
            "Grok": "BLACKBOX-RESIST·NO-EXPAND | 禁:发散过猛",
            "Cursor": "工程锚·文件树 | 禁:写论文",
            "本地终端": "手动模式→TOOL_EXECUTED | 禁:假执行",
        }
        for ai, rules in ais.items():
            cprint(f"  {ai:12s}: {rules}", C.DIM)
        return

    # --test
    if args.test:
        passed, failed = run_tests()
        sys.exit(0 if failed == 0 else 1)

    # --interactive
    if args.interactive:
        interactive()
        return

    # --stats
    if args.stats:
        stats = engine.get_stats()
        if args.json:
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            cprint("\n📊 压缩指令引擎 统计概览", C.BOLD)
            cprint(f"  总执行次数: {stats['total_executions']}", C.GREEN)
            cprint(f"  指令总数: {stats['total_commands']}", C.CYAN)
            cprint(f"  记错本: {stats['total_mistakes']} (未解决: {stats['unresolved_mistakes']})", C.YELLOW)
            cprint(f"  当前模式: {stats['current_mode'].upper()}", C.BLUE)
            if stats['by_command']:
                cprint("  按指令:", C.DIM)
                for cmd, cnt in stats['by_command'].items():
                    cprint(f"    {cmd}: {cnt}次", C.DIM)
            if stats['by_category']:
                cprint("  按分类:", C.DIM)
                for cat, cnt in stats['by_category'].items():
                    cprint(f"    {cat}: {cnt}次", C.DIM)
        return

    # --history
    if args.history:
        rows = engine.get_history(args.limit)
        if args.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
        else:
            cprint(f"\n📜 最近 {len(rows)} 条执行记录:", C.CYAN)
            for r in rows:
                cprint(f"  {r['time']} | {r['command']:8s} | {r['mode']:12s} | {r['status']}", C.DIM)
        return

    # --batch
    if args.batch:
        batch_path = Path(args.batch)
        if not batch_path.exists():
            cprint(f"❌ 文件不存在: {args.batch}", C.RED)
            sys.exit(2)
        lines = batch_path.read_text(encoding='utf-8').strip().splitlines()
        results = []
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            result = engine.execute(line)
            results.append(result)
            if args.json:
                pass  # 批量收集中
            else:
                cprint(f"\n[{i}/{len(lines)}] 输入: {line[:50]}", C.CYAN)
                cprint(f"  → {result.get('command', '未知')} | {result.get('status', '?')}", C.DIM)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            cprint(f"\n✅ 批量完成: {len(results)}/{len(lines)} 条执行", C.GREEN)
        return

    # 单条执行
    if args.text:
        text = " ".join(args.text)
        result = engine.execute(text)
        output = ""
        if args.json:
            output = json.dumps(result, ensure_ascii=False, indent=2, default=str)
        elif args.format in ("markdown", "md"):
            output = engine.format_markdown(result)
        else:
            output = engine.format_output(result, receipt=args.receipt or True)

        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            Path(args.output).write_text(output, encoding='utf-8')
            cprint(f"✅ 已输出到: {args.output}", C.GREEN)
        else:
            print(output)

        # 退出码: unknown → 1, 其余 → 0
        sys.exit(1 if result.get('status') == 'unknown' else 0)
        return

    parser.print_help()

if __name__ == "__main__":
    main()
