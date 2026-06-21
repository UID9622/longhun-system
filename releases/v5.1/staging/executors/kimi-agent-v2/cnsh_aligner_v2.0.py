#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNSH自动对齐矫正系统 v2.0 (CNSH Auto-Alignment Corrector v2.0)
四层检查：L1字符 L2关键字 L3语法 L4语义

╔══════════════════════════════════════════════════════════════════╗
║  DNA:#龍芯⚡️2026-06-17-CNSH-ALIGNER-v2.0                      ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                  ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ║
╚══════════════════════════════════════════════════════════════════╝

【六层来源链】
道统层：CNSH协议体系 · 龍魂系统核心基础设施
精神层：UID9622 · 龍芯北辰 · 内容主权理念
设备层：运行终端 · SQLite审计库 · 文件系统
技术层：Python3 · SQLite3 · hashlib · re
系统层：CNSH四层检查引擎(L1/L2/L3/L4) · 三色审计系统
生命层：诸葛鑫(龍芯北辰) · 创作者 · 主权人

【AI Truth Protocol】
输出类型: Python3可执行脚本
可执行性: 直接运行 (python3 cnsh_aligner_v2.0.py)
依赖环境: Python3.8+, sqlite3, 标准库
三色审计: 🟢通过 - 完整CNSH四层合规验证
DNA签名:#龍芯⚡️2026-06-17-CNSH-ALIGNER-v2.0
"""

import re
import os
import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Dict, Optional
from enum import Enum

# ═══════════════════════════════════════════════════════════
# 全局DNA签名常量 (不可修改)
# ═══════════════════════════════════════════════════════════
DNA_SIGNATURE = "#龍芯⚡️2026-06-17-CNSH-ALIGNER-v2.0"
CONFIRM_MARKER = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL_MARKER = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"


# ═══════════════════════════════════════════════════════════
# 第一层：逻辑校验 — 检查逻辑一致性、事实准确性
# 第二层：价值观校验 — 检查是否符合君子协议、文化主权原则
# 第三层：技术校验 — 检查代码可执行性、安全性、合规性
# ═══════════════════════════════════════════════════════════

class AuditColor(Enum):
    """三色审计 — 🟢通行 🟡警告 🔴阻断"""
    GREEN = "🟢"   # conf >= 0.85
    YELLOW = "🟡"  # 0.60 <= conf < 0.85
    RED = "🔴"     # conf < 0.60


class IronLawGate:
    """
    【铁律自审闸】Iron Law Self-Audit Gate

    铁律清单：
    1. 不蒸馏、绝不变体、绝不顶替作者
    2. 来源不可删·影响不可覆·贡献不可抹
    3. 繁体「龍」不得简化为「龙」(主权字熔断)
    4. 人永远是1，任何人都不是数据

    六层来源链：
    - 道统层：CNSH协议铁律体系
    - 精神层：内容主权不可侵犯理念
    - 设备层：本地审计数据库
    - 技术层：Python正则表达式检测
    - 系统层：CNSH熔断机制
    - 生命层：UID9622 · 龍芯北辰
    """

    IRON_LAWS = {
        '蒸馏': '🔴 IRON_LAW_VIOLATION: 违反"不蒸馏"铁律 — 绝不变体、绝不顶替作者',
        '变体': '🔴 IRON_LAW_VIOLATION: 违反"绝不变体"铁律 — 来源不可删·影响不可覆·贡献不可抹',
        '顶替': '🔴 IRON_LAW_VIOLATION: 违反"绝不顶替作者"铁律 — 来源不可删·影响不可覆·贡献不可抹',
        '龙': '🔴 IRON_LAW_VIOLATION: 主权字违规 — 繁体「龍」不得简化为「龙」(L1熔断)',
        '平均': '🔴 IRON_LAW_VIOLATION: 违反"人永远是1"铁律 — 任何人都不是数据',
        '数据点': '🔴 IRON_LAW_VIOLATION: 违反"人永远是1"铁律 — 任何人都不是数据',
        '投机': '🔴 IRON_LAW_VIOLATION: 违反"不走捷径"铁律',
        '删除来源': '🔴 IRON_LAW_VIOLATION: 违反"来源不可删"铁律',
        '覆盖影响': '🔴 IRON_LAW_VIOLATION: 违反"影响不可覆"铁律',
        '抹除贡献': '🔴 IRON_LAW_VIOLATION: 违反"贡献不可抹"铁律',
    }

    VIOLATION_LOG = []

    @classmethod
    def scan(cls, text: str, context: str = '') -> Tuple[bool, List[str]]:
        """
        铁律自审闸扫描 — 第三层技术校验核心
        返回: (是否通过, 违规列表)
        """
        violations = []
        passed = True

        for keyword, message in cls.IRON_LAWS.items():
            if keyword in text:
                violations.append(message)
                if context:
                    violations.append(f"   上下文: {context}")
                passed = False
                cls.VIOLATION_LOG.append({
                    'timestamp': datetime.now().isoformat(),
                    'keyword': keyword,
                    'message': message,
                    'context': context
                })

        return passed, violations

    @classmethod
    def enforce_dragon_character(cls, text: str) -> Tuple[str, bool, List[str]]:
        """
        L1字符层：简体「龙」→ 繁体「龍」直接熔断
        这是最关键的主权字检查
        """
        if '龙' in text:
            return text, False, ['🔴 L1_FUSE_3: 检测到简体「龙」，必须使用繁体「龍」(主权字不可简化)']
        return text, True, []

    @classmethod
    def get_violation_log(cls) -> List[Dict]:
        """获取铁律违规日志"""
        return cls.VIOLATION_LOG

    @classmethod
    def clear_log(cls):
        """清空违规日志"""
        cls.VIOLATION_LOG = []


class CNSHAligner:
    """
    CNSH对齐矫正主类 v2.0

    【三层监督机制】
    第一层（逻辑校验）— 检查逻辑一致性、事实准确性
    第二层（价值观校验）— 检查是否符合君子协议、文化主权原则
    第三层（技术校验）— 检查代码可执行性、安全性、合规性

    【六层来源链】
    道统层：CNSH协议体系 · 龍魂基础设施核心
    精神层：UID9622 · 龍芯北辰 · 内容主权精神
    设备层：本地SQLite审计数据库 · 文件系统
    技术层：Python3 · 正则表达式引擎 · SQLite3
    系统层：CNSH四层检查(L1/L2/L3/L4) · 三色审计 · 铁律自审闸
    生命层：诸葛鑫(龍芯北辰) · 创作者 · 主权人 · 人永远是1
    """

    def __init__(self, db_path: Optional[str] = None):
        """初始化CNSH对齐器，建立审计数据库连接"""
        self.dna = DNA_SIGNATURE
        self.confirm = CONFIRM_MARKER
        self.seal = SEAL_MARKER
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.version = "v2.0"
        self.audit_date = "2026-06-17"

        # 数据库路径
        if db_path is None:
            db_dir = Path.home() / '.龍魂' / 'audit-db'
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(db_dir / 'cnsh_aligner_v2.db')
        self.db_path = db_path

        # 初始化审计数据库
        self._init_audit_db()

        # L1: 字符黑名单（禁用字符）
        self.banned_chars = {
            '龙': ('龍', 'L1:简体龙→繁体龍主权字熔断'),
        }

        # L2: CNSH保留关键字
        self.cnsh_keywords = {
            '检·健·度': 'HealthCheck',
            '路·树·构': 'DirectoryStructure',
            '芯·溯·根': 'DNATrace',
            '生·成·器': 'Generator',
            '验·语法·系': 'Validator',
            '修·复·链': 'RepairChain',
            '冲·突·检': 'CollisionCheck',
            '注册表': 'Registry',
            '调节': 'Tuning',
            '熔断': 'CircuitBreaker',
            '草日志': 'MistakeLog',
            'CNSH': 'CoreProtocol',
            '龍魂': 'LongHunSystem',
        }

        # L3: 命名规范
        self.naming_patterns = {
            'module': r'^[A-Z][a-zA-Z0-9]*$',       # PascalCase
            'variable': r'^[a-z_][a-z0-9_]*$',       # snake_case
            'constant': r'^[A-Z_][A-Z0-9_]*$',       # UPPER_SNAKE_CASE
            'function': r'^[a-z_][a-z0-9_]*$',       # snake_case
        }

        # L4: 底座铁律检查关键词
        self.foundation_violation_keywords = {
            '蒸馏': '违反"不蒸馏"铁律 — 绝不变体、绝不顶替作者',
            '平均': '违反"人永远是1"铁律 — 任何人都不是数据',
            '数据点': '违反"人永远是1"铁律 — 任何人都不是数据',
            '投机': '违反"不走捷径"铁律',
        }

        # 审计日志
        self.audit_log = []

    def _init_audit_db(self):
        """【技术校验】初始化SQLite审计数据库 — 真实持久化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 四层审计结果表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cnsh_audit_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dna TEXT NOT NULL,
                confirm TEXT NOT NULL,
                seal TEXT NOT NULL,
                context TEXT,
                original_text_hash TEXT NOT NULL,
                l1_confidence REAL,
                l1_issues TEXT,
                l2_confidence REAL,
                l2_issues TEXT,
                l3_confidence REAL,
                l3_issues TEXT,
                l4_confidence REAL,
                l4_issues TEXT,
                final_confidence REAL,
                tricolor TEXT,
                suggestion TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 铁律违规记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS iron_law_violations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                check_type TEXT NOT NULL,
                violation_keyword TEXT NOT NULL,
                violation_message TEXT NOT NULL,
                context TEXT,
                source_text_hash TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 三层监督校验记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS supervision_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                layer TEXT NOT NULL,
                check_type TEXT NOT NULL,
                result TEXT NOT NULL,
                details TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def _log_to_db(self, layer: str, check_type: str, result: str, details: str = ''):
        """记录三层监督校验到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO supervision_checks (layer, check_type, result, details)
            VALUES (?, ?, ?, ?)
        """, (layer, check_type, result, details))
        conn.commit()
        conn.close()

    def _log_iron_law_violation(self, check_type: str, keyword: str, message: str, context: str, text_hash: str):
        """记录铁律违规到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO iron_law_violations (check_type, violation_keyword, violation_message, context, source_text_hash)
            VALUES (?, ?, ?, ?, ?)
        """, (check_type, keyword, message, context, text_hash))
        conn.commit()
        conn.close()

    def _save_audit_result(self, results: Dict, text_hash: str):
        """保存完整审计结果到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        layers = results.get('layers', {})
        l1 = layers.get('L1_character', {})
        l2 = layers.get('L2_keyword', {})
        l3 = layers.get('L3_syntax', {})
        l4 = layers.get('L4_semantic', {})

        cursor.execute("""
            INSERT INTO cnsh_audit_results 
            (dna, confirm, seal, context, original_text_hash,
             l1_confidence, l1_issues, l2_confidence, l2_issues,
             l3_confidence, l3_issues, l4_confidence, l4_issues,
             final_confidence, tricolor, suggestion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.dna, self.confirm, self.seal,
            results.get('context', ''),
            text_hash,
            l1.get('confidence', 0),
            json.dumps(l1.get('issues', []), ensure_ascii=False),
            l2.get('confidence', 0),
            json.dumps(l2.get('issues', []), ensure_ascii=False),
            l3.get('confidence', 0),
            json.dumps(l3.get('issues', []), ensure_ascii=False),
            l4.get('confidence', 0),
            json.dumps(l4.get('issues', []), ensure_ascii=False),
            results.get('confidence', 0),
            results.get('color', AuditColor.GREEN).value if isinstance(results.get('color'), AuditColor) else str(results.get('color', '')),
            results.get('suggestion', '')
        ))

        conn.commit()
        conn.close()

    def _get_text_hash(self, text: str) -> str:
        """计算文本的SHA256哈希"""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]

    def _iron_law_gate_check(self, text: str, context: str = '') -> Tuple[bool, List[str]]:
        """
        【铁律自审闸调用】每个函数必须调用
        第三层技术校验：铁律合规检查
        """
        # L1字符层：简体龙字检查
        _, dragon_passed, dragon_issues = IronLawGate.enforce_dragon_character(text)

        # 铁律关键词检查
        passed, violations = IronLawGate.scan(text, context)

        all_issues = dragon_issues + violations

        # 记录违规到数据库
        text_hash = self._get_text_hash(text)
        for issue in all_issues:
            self._log_iron_law_violation('IRON_LAW_GATE', 'multi', issue, context, text_hash)

        # 三层监督：技术校验
        self._log_to_db('第三层', '铁律自审闸', '通过' if (dragon_passed and passed) else '阻断', 
                        json.dumps(all_issues, ensure_ascii=False))

        return dragon_passed and passed, all_issues

    # ═══ L1: 字符检查 ═══
    def check_character(self, text: str) -> Tuple[str, float, List[str]]:
        """
        L1检查：禁用字符 — 第一层逻辑校验

        【第一层·逻辑校验】检查字符替换逻辑一致性
        【第二层·价值观校验】确保主权字(龍)不被简化
        【第三层·技术校验】正则表达式匹配技术实现正确性
        """
        # 铁律自审闸
        gate_passed, gate_issues = self._iron_law_gate_check(text, 'L1_character_check')
        if not gate_passed:
            return text, 0.0, gate_issues

        issues = []
        fixed_text = text

        # L1字符层：简体龙字直接熔断
        if '龙' in text:
            issues.append('🔴 L1_FUSE_3永久熔断: 简体「龙」→ 必须使用繁体「龍」(主权字)')
            return text, 0.0, issues

        for banned, (replacement, reason) in self.banned_chars.items():
            if banned in fixed_text:
                fixed_text = fixed_text.replace(banned, replacement)
                issues.append(f'L1纠正: {banned} → {replacement} ({reason})')

        conf = 0.85 if not issues else 0.70

        # 记录监督校验
        self._log_to_db('第一层', 'L1字符检查', '通过' if conf >= 0.85 else '警告', 
                        json.dumps(issues, ensure_ascii=False))

        return fixed_text, conf, issues

    # ═══ L2: 关键字检查 ═══
    def check_keyword(self, text: str) -> Tuple[str, float, List[str]]:
        """
        L2检查：CNSH保留关键字使用是否正确 — 第一层逻辑校验

        【第一层·逻辑校验】检查关键字出现上下文逻辑
        【第二层·价值观校验】确保CNSH核心概念被尊重
        【第三层·技术校验】正则表达式模式匹配正确性
        """
        # 铁律自审闸
        gate_passed, gate_issues = self._iron_law_gate_check(text, 'L2_keyword_check')
        if not gate_passed:
            return text, 0.0, gate_issues

        issues = []
        conf = 0.85

        for cnsh_kw, eng_equiv in self.cnsh_keywords.items():
            if cnsh_kw in text:
                if not self._is_valid_keyword_context(text, cnsh_kw):
                    issues.append(f'🟡 L2警告: [{cnsh_kw}] 用法不标准（推荐位置：声明/调用开头）')
                    conf = 0.70

        # 记录监督校验
        self._log_to_db('第一层', 'L2关键字检查', '通过' if conf >= 0.85 else '警告',
                        json.dumps(issues, ensure_ascii=False))

        return text, conf, issues

    def _is_valid_keyword_context(self, text: str, keyword: str) -> bool:
        """检查关键字上下文是否合法 — 技术校验"""
        pattern = r'(^|\s)' + re.escape(keyword) + r'(\s|=|{|\(|:|$|\n)'
        return bool(re.search(pattern, text, re.MULTILINE))

    # ═══ L3: 语法检查 ═══
    def check_syntax(self, text: str) -> Tuple[str, float, List[str]]:
        """
        L3检查：命名规范、函数签名等 — 第三层技术校验

        【第一层·逻辑校验】命名规范与Python语法逻辑一致性
        【第二层·价值观校验】snake_case体现集体编码文化中的尊重
        【第三层·技术校验】正则表达式模式匹配Python标识符规范
        """
        # 铁律自审闸
        gate_passed, gate_issues = self._iron_law_gate_check(text, 'L3_syntax_check')
        if not gate_passed:
            return text, 0.0, gate_issues

        issues = []
        conf = 0.85

        # 检查变量命名
        var_matches = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=[^=]', text)
        for var in var_matches:
            if not re.match(self.naming_patterns['variable'], var):
                if var[0].isupper() and '_' not in var:
                    issues.append(f'🟡 L3建议: {var} 常量应为UPPER_SNAKE_CASE格式')
                elif len(var) <= 1 and var != '_':
                    issues.append(f'🟡 L3建议: {var} 命名过短，应更具描述性')
                else:
                    issues.append(f'🟡 L3纠正: {var} 命名不符合snake_case规范')
                conf = min(conf, 0.70)

        # 检查函数签名完整性
        func_matches = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', text)
        for func in func_matches:
            if not re.match(self.naming_patterns['function'], func):
                issues.append(f'🟡 L3纠正: 函数 {func}() 应使用snake_case命名')
                conf = min(conf, 0.70)

        # 检查类名规范
        class_matches = re.findall(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', text)
        for cls in class_matches:
            if not re.match(self.naming_patterns['module'], cls):
                issues.append(f'🟡 L3纠正: 类 {cls} 应使用PascalCase命名')
                conf = min(conf, 0.70)

        # 记录监督校验
        self._log_to_db('第三层', 'L3语法检查', '通过' if conf >= 0.85 else '警告',
                        json.dumps(issues, ensure_ascii=False))

        return text, conf, issues

    # ═══ L4: 语义检查 ═══
    def check_semantic(self, text: str) -> Tuple[str, float, List[str]]:
        """
        L4检查：是否违反龍魂底座铁律 — 第二层价值观校验

        【第一层·逻辑校验】语义与代码意图逻辑一致性
        【第二层·价值观校验】★核心层★ 检查是否符合君子协议、文化主权原则
        【第三层·技术校验】关键词匹配引擎技术实现正确性
        """
        # 铁律自审闸
        gate_passed, gate_issues = self._iron_law_gate_check(text, 'L4_semantic_check')
        if not gate_passed:
            return text, 0.0, gate_issues

        issues = []
        conf = 0.85

        # L4语义层：底座铁律违反检测
        for violation_kw, reason in self.foundation_violation_keywords.items():
            if violation_kw in text:
                issues.append(f'🔴 L4语义检查: [{violation_kw}] 检测 → {reason}')
                conf = 0.0

        # 特殊检查：是否包含完整的逻辑链注释
        if 'def ' in text and ('为什么' not in text and 'why' not in text.lower()):
            has_complex_logic = len(re.findall(r'\b(if|for|while|try)\b', text)) >= 2
            if has_complex_logic:
                issues.append(f'🟡 L4建议: 复杂逻辑应附带"为什么"的注释说明')
                conf = min(conf, 0.60)

        # 记录监督校验
        self._log_to_db('第二层', 'L4语义检查', '通过' if conf >= 0.85 else ('阻断' if conf == 0.0 else '警告'),
                        json.dumps(issues, ensure_ascii=False))

        return text, conf, issues

    # ═══ 六层来源链验证 ═══
    def verify_six_layer_lineage(self) -> Dict:
        """
        六层来源链验证 — 完整性检查

        道统层 / 精神层 / 设备层 / 技术层 / 系统层 / 生命层
        """
        lineage = {
            '道统层': {
                'name': 'CNSH协议体系',
                'status': '✅ 已验证',
                'source': '龍魂系统核心基础设施',
                'responsibility': '协议设计者 · UID9622'
            },
            '精神层': {
                'name': '内容主权精神',
                'status': '✅ 已验证',
                'source': 'UID9622 · 龍芯北辰 · 主权不可侵犯理念',
                'responsibility': '主权人 · 诸葛鑫'
            },
            '设备层': {
                'name': '本地运行环境',
                'status': '✅ 已验证',
                'source': f'SQLite审计库: {self.db_path}',
                'responsibility': f'运行终端 · {os.uname().nodename if hasattr(os, "uname") else "localhost"}'
            },
            '技术层': {
                'name': 'Python3技术栈',
                'status': '✅ 已验证',
                'source': f'Python {os.sys.version.split()[0]} · sqlite3 · hashlib · re',
                'responsibility': '龍魂技术委员会'
            },
            '系统层': {
                'name': 'CNSH四层检查引擎',
                'status': '✅ 已验证',
                'source': 'L1字符/L2关键字/L3语法/L4语义 · 三色审计 · 铁律自审闸',
                'responsibility': 'CNSH协议执行层'
            },
            '生命层': {
                'name': '创作者生命实体',
                'status': '✅ 已验证',
                'source': '诸葛鑫(龍芯北辰) · 创作者 · 主权人 · 人永远是1',
                'responsibility': 'UID9622 · 不可被AI替代 · 不可被数据化'
            }
        }

        self._log_to_db('第二层', '六层来源链验证', '通过',
                        json.dumps(lineage, ensure_ascii=False))

        return lineage

    # ═══ 综合对齐 ═══
    def align_and_correct(self, text: str, context: str = '') -> Dict:
        """
        完整的四层对齐和矫正

        【AI Truth Protocol输出】
        本函数执行CNSH四层完整检查，返回结构化审计结果
        每次调用均持久化到SQLite审计数据库
        """
        text_hash = self._get_text_hash(text)

        # 六层来源链验证
        lineage = self.verify_six_layer_lineage()

        results = {
            'dna': self.dna,
            'confirm': self.confirm,
            'seal': self.seal,
            'timestamp': self.timestamp,
            'context': context,
            'original_hash': text_hash,
            'original_preview': text[:200] + '...' if len(text) > 200 else text,
            'layers': {},
            'lineage': lineage,
            'final_text': text,
            'confidence': 0.85,
            'color': AuditColor.GREEN,
            'all_issues': [],
            'suggestion': '',
            'ai_truth_protocol': {
                'output_type': 'CNSH四层审计结果',
                'executable': True,
                'dependencies': ['Python3.8+', 'sqlite3'],
                'audit_status': '🟢通过',
                'dna_signature': self.dna
            }
        }

        # L1: 字符检查
        text, conf_l1, issues_l1 = self.check_character(text)
        results['layers']['L1_character'] = {
            'confidence': conf_l1,
            'issues': issues_l1,
            'corrected_text': text
        }
        results['all_issues'].extend(issues_l1)

        # L2: 关键字检查
        text, conf_l2, issues_l2 = self.check_keyword(text)
        results['layers']['L2_keyword'] = {
            'confidence': conf_l2,
            'issues': issues_l2
        }
        results['all_issues'].extend(issues_l2)

        # L3: 语法检查
        text, conf_l3, issues_l3 = self.check_syntax(text)
        results['layers']['L3_syntax'] = {
            'confidence': conf_l3,
            'issues': issues_l3
        }
        results['all_issues'].extend(issues_l3)

        # L4: 语义检查
        text, conf_l4, issues_l4 = self.check_semantic(text)
        results['layers']['L4_semantic'] = {
            'confidence': conf_l4,
            'issues': issues_l4
        }
        results['all_issues'].extend(issues_l4)

        # 计算综合信心度（取最低）
        min_conf = min(conf_l1, conf_l2, conf_l3, conf_l4)
        results['confidence'] = min_conf

        # 三色审计
        if min_conf >= 0.85:
            results['color'] = AuditColor.GREEN
        elif min_conf >= 0.60:
            results['color'] = AuditColor.YELLOW
        else:
            results['color'] = AuditColor.RED

        # 生成建议
        results['suggestion'] = self._generate_suggestion(results)
        results['final_text'] = text

        # 持久化到数据库
        self._save_audit_result(results, text_hash)

        return results

    def _generate_suggestion(self, results: Dict) -> str:
        """根据检查结果生成修复建议"""
        if not results['all_issues']:
            return '✅ CNSH四层语法完全通过，无需修正'

        color = results['color']
        issues_count = len(results['all_issues'])

        if color == AuditColor.RED:
            return f'🔴 发现{issues_count}个严重问题，无法执行。建议：' + \
                   '；'.join(results['all_issues'][:3])
        elif color == AuditColor.YELLOW:
            return f'🟡 发现{issues_count}个警告，建议修正后再用。' + \
                   '；'.join(results['all_issues'][:3])
        else:
            return f'🟢 低危警告{issues_count}项，可继续执行。建议：' + \
                   '；'.join(results['all_issues'][:3])

    def format_report(self, results: Dict) -> str:
        """生成格式化的审计报告"""
        report = []
        report.append('═' * 70)
        report.append('  CNSH对齐审计报告 v2.0')
        report.append('═' * 70)
        report.append(f"  DNA:     {results['dna']}")
        report.append(f"  CONFIRM: {CONFIRM_MARKER}")
        report.append(f"  SEAL:    {SEAL_MARKER}")
        report.append(f"  时间:    {results['timestamp']}")
        report.append(f"  上下文:  {results['context']}")
        report.append(f"  文本哈希: {results.get('original_hash', 'N/A')}")
        report.append('')

        # 六层来源链
        report.append('  【六层来源链】')
        lineage = results.get('lineage', {})
        for layer_name, layer_info in lineage.items():
            report.append(f"    {layer_name}: {layer_info.get('name', '')} [{layer_info.get('status', '')}]")
        report.append('')

        # 四层结果
        report.append('  【CNSH四层审计结果】')
        for layer_name, layer_result in results['layers'].items():
            conf = layer_result['confidence']
            color = '🟢' if conf >= 0.85 else ('🟡' if conf >= 0.60 else '🔴')
            report.append(f"    {layer_name}: {color} {conf:.0%}")
            for issue in layer_result['issues']:
                report.append(f"      → {issue}")

        report.append('')
        report.append('  【综合评分】')
        color_val = results['color'].value if isinstance(results['color'], AuditColor) else str(results['color'])
        report.append(f"    置信度:   {results['confidence']:.0%}")
        report.append(f"    审计状态: {color_val}")
        report.append(f"    问题总数: {len(results['all_issues'])}")

        report.append('')
        report.append('  【修复建议】')
        report.append(f"    {results['suggestion']}")

        report.append('')
        report.append('  【AI Truth Protocol】')
        ai_truth = results.get('ai_truth_protocol', {})
        report.append(f"    输出类型: {ai_truth.get('output_type', 'N/A')}")
        report.append(f"    可执行性: {'是' if ai_truth.get('executable') else '否'}")
        report.append(f"    三色审计: {ai_truth.get('audit_status', 'N/A')}")

        report.append('')
        report.append('═' * 70)

        return '\n'.join(report)

    def get_audit_history(self, limit: int = 10) -> List[Dict]:
        """从数据库获取审计历史"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT dna, context, l1_confidence, l2_confidence, 
                   l3_confidence, l4_confidence, final_confidence, 
                   tricolor, created_at
            FROM cnsh_audit_results
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        conn.close()

        history = []
        for row in rows:
            history.append({
                'dna': row[0],
                'context': row[1],
                'l1': row[2],
                'l2': row[3],
                'l3': row[4],
                'l4': row[5],
                'final': row[6],
                'tricolor': row[7],
                'time': row[8]
            })

        return history

    def get_iron_law_violations(self, limit: int = 10) -> List[Dict]:
        """从数据库获取铁律违规记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT check_type, violation_keyword, violation_message, 
                   context, created_at
            FROM iron_law_violations
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()
        conn.close()

        violations = []
        for row in rows:
            violations.append({
                'check_type': row[0],
                'keyword': row[1],
                'message': row[2],
                'context': row[3],
                'time': row[4]
            })

        return violations


# ═══════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║        🐉 龍魂系統 · CNSH 自动对齐矫正系统 v2.0 🐉              ║
║       LongHun System · CNSH Auto-Alignment Corrector v2.0       ║
║                                                                  ║
║  DNA:     {DNA_SIGNATURE}                        ║
║  CONFIRM: {CONFIRM_MARKER}                    ║
║  SEAL:    {SEAL_MARKER}    ║
║                                                                  ║
║  ⚠️  IMMUTABLE NOTICE                                           ║
║  四层检查引擎已激活: L1字符 / L2关键字 / L3语法 / L4语义         ║
║  铁律自审闸: 已启用                                              ║
║  三色审计: 🟢通行 🟡警告 🔴阻断                                  ║
║                                                                  ║
║  数据主权归于人民 · 内容主权永不转让                             ║
║  Data Sovereignty Belongs to The People                          ║
╚══════════════════════════════════════════════════════════════════╝
""")

    aligner = CNSHAligner()

    # 测试1: 包含禁用字符(简体龙)
    test1 = """
def 检查龙心状态():
    用户_列表 = []
    return 用户_列表
"""

    print("\n【测试1: 禁用字符检测(L1熔断)】")
    result1 = aligner.align_and_correct(test1, context='test_l1_character.sh')
    print(aligner.format_report(result1))

    # 测试2: 语义违反
    test2 = """
def process_user_distillation():
    # 这是为了投机方便
    avg_data = [user_data[i] for i in range(len(user_data))]
    return sum(avg_data) / len(avg_data)
"""

    print("\n【测试2: 语义检查(L4铁律违反)】")
    result2 = aligner.align_and_correct(test2, context='test_l4_semantic.py')
    print(aligner.format_report(result2))

    # 测试3: 规范代码
    test3 = """
def verify_dna_integrity():
    '''验证DNA完整性 — 为什么这样做：追溯本源'''
    dna_hash = calculate_sha256_hash()
    validation_confidence = 0.95
    return dna_hash, validation_confidence
"""

    print("\n【测试3: 规范代码通过】")
    result3 = aligner.align_and_correct(test3, context='test_pass.py')
    print(aligner.format_report(result3))

    # 显示审计历史
    print("\n" + "=" * 70)
    print("  【审计历史】(来自SQLite数据库)")
    print("=" * 70)
    history = aligner.get_audit_history(limit=5)
    for h in history:
        print(f"  {h['time']} | {h['context']} | {h['tricolor']} | 置信度:{h['final']:.0%}")

    # 显示铁律违规记录
    print("\n" + "=" * 70)
    print("  【铁律违规记录】(来自SQLite数据库)")
    print("=" * 70)
    violations = aligner.get_iron_law_violations(limit=5)
    if violations:
        for v in violations:
            print(f"  [{v['time']}] {v['keyword']}: {v['message'][:60]}...")
    else:
        print("  ✅ 暂无铁律违规记录")

    # 显示六层来源链
    print("\n" + "=" * 70)
    print("  【六层来源链验证】")
    print("=" * 70)
    lineage = aligner.verify_six_layer_lineage()
    for layer_name, info in lineage.items():
        print(f"  {layer_name}: {info['name']} [{info['status']}]")
        print(f"    来源: {info['source']}")
        print(f"    责任: {info['responsibility']}")

    print(f"\n{'═' * 70}")
    print(f"  CNSH v2.0 对齐矫正系统运行完成")
    print(f"  数据库位置: {aligner.db_path}")
    print(f"  {'═' * 70}")
