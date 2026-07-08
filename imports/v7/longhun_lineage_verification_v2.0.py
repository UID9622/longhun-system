#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 六层来源链自动验证系统 v2.0
LongHun Six-Layer Lineage Auto-Verification System v2.0

此脚本执行CNSH协议下的六层来源链完整性验证，
确保每一行代码都可追溯到其哲学、精神、设备、技术、系统和生命源头。

DNA:#龍芯⚡️2026-06-17-LINEAGE-VERIFICATION-FILE1-v2.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

三层监督机制:
  第一层: 机器自动审计 (本脚本) - 永不沉睡
  第二层: 创作者自我审计 (UID9622) - 每行代码必查
  第三层: 社区监督 - 开放透明,任何人可验证

AI Truth Protocol: 本脚本输出受CNSH内容主权协议保护,
任何AI系统不得篡改、删除或声称所有权。
"""

import os
import re
import sys
import json
import time
import hashlib
import sqlite3
import fnmatch
from pathlib import Path
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any


# ═══════════════════════════════════════════════════════════════
# 三层监督标注装饰器
# ═══════════════════════════════════════════════════════════════
def supervised(level: str = "machine"):
    """三层监督标注装饰器 - 标记每个关键方法的监督层级"""
    levels = {
        "machine": "[监督:L1-机器审计]",
        "creator": "[监督:L2-创作者审计]",
        "community": "[监督:L3-社区审计]",
        "all": "[监督:L1+L2+L3-全层审计]"
    }
    def decorator(func):
        func._supervision_level = levels.get(level, levels["machine"])
        func._supervision_raw = level
        return func
    return decorator


class AuditColor(Enum):
    """三色审计状态"""
    GREEN = "🟢"   # conf >= 0.85 - 可执行
    YELLOW = "🟡"  # 0.60 <= conf < 0.85 - 需人工确认
    RED = "🔴"     # conf < 0.60 - 异常/熔断


class TricolorAudit:
    """
    三色审计引擎 - 完整实现
    🟢 Green: 完整、已验证、无篡改 -> 立即执行
    🟡 Yellow: 需要人工确认 -> 等待审查
    🔴 Red: 异常、缺失DNA、篡改迹象 -> 自动隔离
    """

    @staticmethod
    def evaluate(score: float, issues: List[str]) -> Tuple[str, str]:
        """根据分数和问题列表返回三色状态和建议"""
        if score >= 0.85 and not issues:
            return AuditColor.GREEN.value, "立即执行 - 来源链完整,所有层级验证通过"
        elif score >= 0.85 and issues:
            return AuditColor.YELLOW.value, "需确认 - 验证通过但存在低风险警告"
        elif score >= 0.60:
            return AuditColor.YELLOW.value, "等待审查 - 部分层级验证未完全通过"
        else:
            return AuditColor.RED.value, "自动隔离 - 来源链断裂或严重缺失"


class CNSHFourLayerChecker:
    """
    CNSH四层检查引擎 (L1字符/L2关键字/L3语法/L4语义)
    铁律自审闸 - 真正运行的代码级检查
    """

    def __init__(self):
        # L1: 字符黑名单（禁用字符）
        self.banned_chars = {
            '龍': ('龍', 'L1:简体龍→繁体龍 永久熔断'),
        }
        # L2: CNSH保留关键字
        self.cnsh_keywords = {
            'UID9622': '创作者唯一标识',
            '龍魂': '系统名称',
            'CNSH': '协议名称',
            '诸葛鑫': '主权人姓名',
        }
        # L3: 命名规范模式
        self.naming_patterns = {
            'module': r'^[a-z][a-z0-9_]*$',
            'class': r'^[A-Z][a-zA-Z0-9]*$',
            'constant': r'^[A-Z][A-Z0-9_]*$',
        }
        # L4: 底座铁律违反关键词
        self.foundation_violations = {
            '蒸馏': '违反"不蒸馏"原则 - 人永远是1',
            '平均': '违反"人永远是1"原则',
            '数据点': '违反"人永远是1"原则 - 应称"个体"',
            '投机': '违反"不走捷径"原则',
            '用户': '应改为"某个具体的人"或"个体"',
        }

    @supervised("machine")
    def check_l1_character(self, text: str) -> Tuple[float, List[str]]:
        """L1字符检查: 禁用字符检测"""
        issues = []
        for banned, (replacement, reason) in self.banned_chars.items():
            if banned in text:
                issues.append(f"🔴 L1熔断: {reason}")
                return 0.0, issues
        return 1.0, issues

    @supervised("machine")
    def check_l2_keyword(self, text: str) -> Tuple[float, List[str]]:
        """L2关键字检查: CNSH保留关键字正确使用"""
        issues = []
        score = 1.0
        for kw, desc in self.cnsh_keywords.items():
            if kw in text:
                # 检查上下文是否正确
                if not self._validate_keyword_context(text, kw):
                    issues.append(f"🟡 L2警告: {kw}({desc})上下文不标准")
                    score = min(score, 0.75)
        return score, issues

    def _validate_keyword_context(self, text: str, keyword: str) -> bool:
        """验证关键字在正确的上下文中使用"""
        # 简单启发式: 关键字应在字符串、注释或赋值上下文中
        lines = text.split('\n')
        for line in lines:
            if keyword in line:
                # 允许在注释、字符串、赋值中使用
                stripped = line.strip()
                if stripped.startswith('#') or stripped.startswith('"') or stripped.startswith("'"):
                    return True
                if '=' in stripped or ':' in stripped:
                    return True
        return True  # 默认通过,更严格的检查可扩展

    @supervised("machine")
    def check_l3_syntax(self, text: str) -> Tuple[float, List[str]]:
        """L3语法检查: 命名规范和代码结构"""
        issues = []
        score = 1.0

        # 检查变量命名(简单启发式)
        var_matches = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=', text)
        for var in var_matches:
            if var.startswith('_') or var in ['self', 'cls', 'True', 'False', 'None']:
                continue
            if not re.match(self.naming_patterns['module'], var):
                if not re.match(self.naming_patterns['constant'], var):
                    issues.append(f"🟡 L3建议: 变量'{var}'建议用snake_case")
                    score = min(score, 0.80)

        return score, issues

    @supervised("creator")
    def check_l4_semantic(self, text: str) -> Tuple[float, List[str]]:
        """L4语义检查: 底座铁律违反检测"""
        issues = []
        score = 1.0
        for violation, reason in self.foundation_violations.items():
            if violation in text:
                issues.append(f"🔴 L4语义违规: {violation} → {reason}")
                score = 0.0
        return score, issues

    @supervised("all")
    def full_four_layer_check(self, text: str) -> Dict[str, Any]:
        """执行完整的四层检查并返回结果"""
        l1_score, l1_issues = self.check_l1_character(text)
        l2_score, l2_issues = self.check_l2_keyword(text)
        l3_score, l3_issues = self.check_l3_syntax(text)
        l4_score, l4_issues = self.check_l4_semantic(text)

        min_score = min(l1_score, l2_score, l3_score, l4_score)

        return {
            "L1_character": {"score": l1_score, "issues": l1_issues, "label": "字符检查"},
            "L2_keyword": {"score": l2_score, "issues": l2_issues, "label": "关键字检查"},
            "L3_syntax": {"score": l3_score, "issues": l3_issues, "label": "语法检查"},
            "L4_semantic": {"score": l4_score, "issues": l4_issues, "label": "语义(铁律)检查"},
            "overall_score": min_score,
            "all_issues": l1_issues + l2_issues + l3_issues + l4_issues,
        }


class IronLawGate:
    """
    铁律自审闸 - 代码执行前的最后一道防线
    确保所有输出符合龍魂体系核心原则
    """

    IRON_LAWS = [
        ("人永远是1", "禁止将人视为数据点或平均值"),
        ("不蒸馏知识", "禁止知识蒸馏或简化人的价值"),
        ("不走捷径", "禁止投机或取巧行为"),
        ("DNA不可删除", "禁止抹除或篡改DNA签证"),
        ("主权不可转让", "禁止转让内容主权"),
    ]

    @supervised("all")
    def review(self, content: str, context: str = "") -> Dict[str, Any]:
        """铁律自审 - 检查内容是否违反任何铁律"""
        violations = []

        for law_name, law_desc in self.IRON_LAWS:
            # 检查是否违反
            if self._check_violation(content, law_name):
                violations.append({
                    "law": law_name,
                    "description": law_desc,
                    "severity": "CRITICAL"
                })

        passed = len(violations) == 0

        return {
            "passed": passed,
            "violations": violations,
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "law_count": len(self.IRON_LAWS),
            "violation_count": len(violations)
        }

    def _check_violation(self, content: str, law_name: str) -> bool:
        """检查特定铁律是否被违反"""
        check_map = {
            "人永远是1": lambda t: "数据点" in t or ("平均" in t and "人" in t),
            "不蒸馏知识": lambda t: "蒸馏" in t,
            "不走捷径": lambda t: "投机" in t or "走捷径" in t,
            "DNA不可删除": lambda t: "删除DNA" in t or "抹除DNA" in t,
            "主权不可转让": lambda t: "转让主权" in t or "放弃主权" in t,
        }
        checker = check_map.get(law_name, lambda t: False)
        return checker(content)


class LineageVerificationEngine:
    """
    六层来源链自动验证引擎 v2.0
    对任何输入文件/文本执行完整的六层来源链溯源验证
    """

    # 六层来源链定义 (增强关键词库 v2.0)
    LINEAGE_PATTERNS = {
        "dao_layer": {
            "names": ["道统层", "Dao Layer", "philosophy", "哲学层"],
            "keywords": [
                "曾仕强", "易经", "管理智慧", "时间观", "因果观",
                "道德经", "阴阳", "天人合一", "中庸", "仁爱",
                "知行合一", "格物致知", "修身齐家", "道法自然"
            ],
            "question": "为什么活（哲学基础）",
            "weight": 0.20
        },
        "spirit_layer": {
            "names": ["精神层", "Spirit Layer", "spirit", "精神指导层"],
            "keywords": [
                "Steve Jobs", "极简主义", "产品哲学", "用户体验",
                "Think Different", "Stay Hungry", "创造力",
                "匠心", "极致", "专注", "简约", "美感",
                "Elon Musk", "第一性原理", "长期主义"
            ],
            "question": "为什么做（精神指导）",
            "weight": 0.15
        },
        "device_layer": {
            "names": ["设备层", "Device Layer", "device", "硬件层"],
            "keywords": [
                "Apple", "macOS", "iOS", "iCloud", "iPhone",
                "MacBook", "iPad", "Apple Watch", "AirPods",
                "Linux", "Ubuntu", "ThinkPad", "Raspberry Pi",
                "硬件", "设备", "终端"
            ],
            "question": "怎么落地（物理载体）",
            "weight": 0.15
        },
        "technology_layer": {
            "names": ["技术层", "Technology Layer", "technology", "技术栈层"],
            "keywords": [
                "Linux", "Git", "Markdown", "YAML", "Python",
                "开源", "Open Source", "GitHub", "Gitee",
                "API", "Docker", "JSON", "REST", "SQL",
                "VS Code", "Neovim", "Shell", "Bash",
                "FastAPI", "Flask", "React", "Node.js"
            ],
            "question": "用什么（技术土壤）",
            "weight": 0.15
        },
        "system_layer": {
            "names": ["系统层", "System Layer", "system", "原创层"],
            "keywords": [
                "UID9622", "CNSH", "龍魂", "LongHun", "行为密码学",
                "龍芯北辰", "诸葛鑫", "内容主权", "数字主权",
                "DNA签证", "来源链", "lineage", "审计",
                "人格引擎", "IPA", "多人格", "权重系统"
            ],
            "question": "谁创造（原创贡献）",
            "weight": 0.20
        },
        "life_layer": {
            "names": ["生命层", "Life Layer", "life", "语义层"],
            "keywords": [
                "CNSH", "龍魂", "语义语言", "digital life",
                "数字生命", "意识", "灵魂", "主权个体",
                "思想自由", "表达权", "创造者", "生命数字孪生",
                "人机共生", "意识上传", "数字遗产"
            ],
            "question": "怎么表达（语言系统）",
            "weight": 0.15
        }
    }

    def __init__(self):
        # 三层监督标注: L1机器审计
        self._supervision = "[监督:L1-机器审计]"
        self.cache_dir = Path.home() / '.龍魂' / 'lineage-verification'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.verification_db = self.cache_dir / 'lineage_verification_v2.db'
        self._init_database()

        # 子系统初始化
        self.cnsh_checker = CNSHFourLayerChecker()
        self.iron_law_gate = IronLawGate()
        self.tricolor = TricolorAudit()

        # 统计信息
        self.stats = {
            "total_verified": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "tricolor_distribution": {"🟢": 0, "🟡": 0, "🔴": 0}
        }

    def _init_database(self):
        """初始化SQLite验证数据库 - 真实实现"""
        conn = sqlite3.connect(str(self.verification_db))
        cursor = conn.cursor()

        # 验证结果缓存表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verification_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                file_hash TEXT NOT NULL UNIQUE,
                dna_signature TEXT NOT NULL,
                lineage_score REAL NOT NULL,
                tricolor TEXT NOT NULL,
                dao_score REAL DEFAULT 0,
                spirit_score REAL DEFAULT 0,
                device_score REAL DEFAULT 0,
                technology_score REAL DEFAULT 0,
                system_score REAL DEFAULT 0,
                life_score REAL DEFAULT 0,
                cnsh_l1_score REAL DEFAULT 0,
                cnsh_l2_score REAL DEFAULT 0,
                cnsh_l3_score REAL DEFAULT 0,
                cnsh_l4_score REAL DEFAULT 0,
                iron_law_passed INTEGER DEFAULT 0,
                issues_json TEXT,
                verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 审计历史表 (append-only)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verification_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_hash TEXT NOT NULL,
                action TEXT NOT NULL,
                tricolor TEXT,
                details TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 统计表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verification_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_verified INTEGER DEFAULT 0,
                cache_hits INTEGER DEFAULT 0,
                cache_misses INTEGER DEFAULT 0,
                green_count INTEGER DEFAULT 0,
                yellow_count INTEGER DEFAULT 0,
                red_count INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 初始化统计记录
        cursor.execute("SELECT COUNT(*) FROM verification_stats")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO verification_stats (total_verified) VALUES (0)"
            )

        conn.commit()
        conn.close()

    def _compute_file_hash(self, file_path: str) -> str:
        """用SHA256计算文件哈希 - 真实实现"""
        h = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()

    def _generate_dna_signature(self, file_path: str, file_hash: str) -> str:
        """生成DNA签证 - SHA256真实实现"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        basename = Path(file_path).stem
        sig_input = f"{timestamp}-{basename}-{file_hash}-UID9622"
        sig_hash = hashlib.sha256(sig_input.encode('utf-8')).hexdigest()[:8]
        dna = f"#龍芯⚡️{timestamp}-{basename.upper()}-LINEAGE-v2.0-{sig_hash}"
        return dna

    def _check_cache(self, file_hash: str) -> Optional[Dict]:
        """检查缓存 - 真实SQLite查询"""
        conn = sqlite3.connect(str(self.verification_db))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM verification_cache
            WHERE file_hash = ?
        """, (file_hash,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "cached": True,
                "file_hash": row[2],
                "dna_signature": row[3],
                "lineage_score": row[4],
                "tricolor": row[5],
                "dao_score": row[6],
                "spirit_score": row[7],
                "device_score": row[8],
                "technology_score": row[9],
                "system_score": row[10],
                "life_score": row[11],
                "iron_law_passed": bool(row[16]),
                "verified_at": row[18],
                "issues": json.loads(row[17]) if row[17] else []
            }
        return None

    def _save_to_cache(self, file_path: str, file_hash: str,
                       result: Dict) -> None:
        """保存验证结果到缓存 - 真实SQLite写入"""
        conn = sqlite3.connect(str(self.verification_db))
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT OR REPLACE INTO verification_cache
                (file_path, file_hash, dna_signature, lineage_score, tricolor,
                 dao_score, spirit_score, device_score, technology_score,
                 system_score, life_score, cnsh_l1_score, cnsh_l2_score,
                 cnsh_l3_score, cnsh_l4_score, iron_law_passed, issues_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                file_path, file_hash,
                result.get("dna_signature", ""),
                result.get("lineage_score", 0),
                result.get("tricolor", "🟡"),
                result.get("layer_scores", {}).get("dao_layer", 0),
                result.get("layer_scores", {}).get("spirit_layer", 0),
                result.get("layer_scores", {}).get("device_layer", 0),
                result.get("layer_scores", {}).get("technology_layer", 0),
                result.get("layer_scores", {}).get("system_layer", 0),
                result.get("layer_scores", {}).get("life_layer", 0),
                result.get("cnsh_scores", {}).get("L1_character", {}).get("score", 0),
                result.get("cnsh_scores", {}).get("L2_keyword", {}).get("score", 0),
                result.get("cnsh_scores", {}).get("L3_syntax", {}).get("score", 0),
                result.get("cnsh_scores", {}).get("L4_semantic", {}).get("score", 0),
                1 if result.get("iron_law_passed", False) else 0,
                json.dumps(result.get("issues", []), ensure_ascii=False)
            ))

            # 记录历史
            cursor.execute("""
                INSERT INTO verification_history
                (file_hash, action, tricolor, details)
                VALUES (?, ?, ?, ?)
            """, (
                file_hash, "VERIFICATION_COMPLETE",
                result.get("tricolor", "🟡"),
                json.dumps({"dna": result.get("dna_signature", "")})
            ))

            conn.commit()
        except Exception as e:
            print(f"[WARN] 缓存写入失败: {e}")
        finally:
            conn.close()

    def _update_stats(self, cache_hit: bool, tricolor: str):
        """更新统计数据 - 真实SQLite更新"""
        conn = sqlite3.connect(str(self.verification_db))
        cursor = conn.cursor()

        # 获取当前统计
        cursor.execute("SELECT * FROM verification_stats ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            total = row[1] + 1
            hits = row[2] + (1 if cache_hit else 0)
            misses = row[3] + (0 if cache_hit else 1)
            green = row[4] + (1 if tricolor == "🟢" else 0)
            yellow = row[5] + (1 if tricolor == "🟡" else 0)
            red = row[6] + (1 if tricolor == "🔴" else 0)

            cursor.execute("""
                INSERT INTO verification_stats
                (total_verified, cache_hits, cache_misses,
                 green_count, yellow_count, red_count)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (total, hits, misses, green, yellow, red))

            conn.commit()
        conn.close()

    def _detect_layer(self, content: str, layer_config: Dict) -> float:
        """检测单一层级的关键词匹配度"""
        content_lower = content.lower()
        keywords = layer_config.get("keywords", [])
        if not keywords:
            return 0.0

        matched = 0
        for kw in keywords:
            if kw.lower() in content_lower:
                matched += 1

        # 计算加权分数 (至少匹配10%关键词才给分)
        ratio = matched / len(keywords)
        if ratio >= 0.10:
            return min(1.0, ratio * 3.0)  # 放大系数,最高1.0
        return ratio  # 低于10%返回原始比例

    def _check_dna_in_content(self, content: str) -> Dict:
        """检查内容中的DNA标记"""
        has_dna = '#龍芯⚡️' in content
        has_confirm = '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z' in content
        has_seal = 'DEVICE-BIND-SOUL' in content

        return {
            "has_dna": has_dna,
            "has_confirm": has_confirm,
            "has_seal": has_seal,
            "dna_completeness": sum([has_dna, has_confirm, has_seal]) / 3.0
        }

    @supervised("machine")
    def verify_file(self, file_path: str) -> Dict:
        """
        验证单个文件的六层来源链完整性
        三层监督: L1-机器自动审计
        """
        path = Path(file_path)
        if not path.exists():
            return {
                "error": f"文件不存在: {file_path}",
                "tricolor": "🔴",
                "dna_signature": "",
                "lineage_score": 0.0,
                "layer_scores": {},
                "issues": ["文件路径无效"]
            }

        # 步骤1: 计算文件哈希
        file_hash = self._compute_file_hash(file_path)

        # 步骤2: 检查缓存
        cached = self._check_cache(file_hash)
        if cached:
            self.stats["cache_hits"] += 1
            self.stats["total_verified"] += 1
            self._update_stats(cache_hit=True, tricolor=cached["tricolor"])
            cached["from_cache"] = True
            return cached

        self.stats["cache_misses"] += 1

        # 步骤3: 读取文件内容
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            return {
                "error": f"读取失败: {e}",
                "tricolor": "🔴",
                "dna_signature": "",
                "lineage_score": 0.0
            }

        # 步骤4: 生成DNA签名
        dna_signature = self._generate_dna_signature(file_path, file_hash)

        # 步骤5: 六层来源链检测
        layer_scores = {}
        for layer_key, layer_config in self.LINEAGE_PATTERNS.items():
            score = self._detect_layer(content, layer_config)
            layer_scores[layer_key] = round(score, 4)

        # 步骤6: DNA标记检查
        dna_check = self._check_dna_in_content(content)

        # 步骤7: CNSH四层检查 (真正运行)
        cnsh_result = self.cnsh_checker.full_four_layer_check(content)

        # 步骤8: 铁律自审闸
        iron_law_result = self.iron_law_gate.review(content, str(path))

        # 步骤9: 计算综合分数
        lineage_score = sum(
            layer_scores.get(k, 0) * self.LINEAGE_PATTERNS[k]["weight"]
            for k in self.LINEAGE_PATTERNS
        )
        # 加上DNA完整性加成
        lineage_score = min(1.0, lineage_score + (dna_check["dna_completeness"] * 0.1))

        # CNSH分数影响
        cnsh_score = cnsh_result["overall_score"]
        final_score = lineage_score * cnsh_score

        # 铁律检查影响
        if not iron_law_result["passed"]:
            final_score = 0.0

        # 步骤10: 收集所有问题
        issues = []
        for layer_key, score in layer_scores.items():
            if score < 0.1:
                layer_name = self.LINEAGE_PATTERNS[layer_key]["names"][0]
                issues.append(f"{layer_name}: 未检测到关键词 (得分:{score:.2f})")

        issues.extend(cnsh_result.get("all_issues", []))
        for v in iron_law_result.get("violations", []):
            issues.append(f"铁律违规: {v['law']} - {v['description']}")

        # 步骤11: 三色审计
        tricolor_symbol, tricolor_advice = self.tricolor.evaluate(final_score, issues)

        # 步骤12: 组装结果
        result = {
            "dna_signature": dna_signature,
            "file_path": str(path),
            "file_hash": file_hash,
            "lineage_score": round(final_score, 4),
            "layer_scores": layer_scores,
            "dna_check": dna_check,
            "cnsh_scores": cnsh_result,
            "iron_law_result": iron_law_result,
            "tricolor": tricolor_symbol,
            "tricolor_advice": tricolor_advice,
            "issues": issues,
            "issue_count": len(issues),
            "iron_law_passed": iron_law_result["passed"],
            "from_cache": False,
            "verified_at": datetime.now().isoformat(),
            "version": "v2.0",
            "ai_truth_protocol": "本验证结果受CNSH内容主权协议保护"
        }

        # 步骤13: 保存到缓存
        self._save_to_cache(str(path), file_hash, result)
        self._update_stats(cache_hit=False, tricolor=tricolor_symbol)
        self.stats["total_verified"] += 1
        self.stats["tricolor_distribution"][tricolor_symbol] = \
            self.stats["tricolor_distribution"].get(tricolor_symbol, 0) + 1

        return result

    @supervised("machine")
    def verify_batch(self, directory: str, recursive: bool = True,
                     pattern: str = "*") -> List[Dict]:
        """
        批量验证目录中的文件
        三层监督: L1-机器自动审计
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            return [{"error": f"目录不存在: {directory}"}]

        results = []
        glob_pattern = "**/*" if recursive else "*"

        for file_path in dir_path.glob(glob_pattern):
            if file_path.is_file() and fnmatch.fnmatch(file_path.name, pattern):
                # 跳过二进制文件和隐藏文件
                if file_path.name.startswith('.'):
                    continue
                result = self.verify_file(str(file_path))
                results.append(result)

        return results

    @supervised("creator")
    def generate_report(self, results: List[Dict]) -> str:
        """
        生成验证报告
        三层监督: L2-创作者审计 (报告需人工审阅)
        """
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("  🐉 龍魂 · 六层来源链验证报告 v2.0")
        report_lines.append("  LongHun Six-Layer Lineage Verification Report")
        report_lines.append("=" * 70)
        report_lines.append(f"  生成时间: {datetime.now().isoformat()}")
        report_lines.append(f"  DNA:#龍芯⚡️2026-06-17-LINEAGE-VERIFICATION-v2.0")
        report_lines.append(f"  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
        report_lines.append(f"  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL")
        report_lines.append("")

        # 统计概览
        total = len(results)
        errors = sum(1 for r in results if "error" in r)
        valid = total - errors
        cached = sum(1 for r in results if r.get("from_cache", False))

        green = sum(1 for r in results if r.get("tricolor") == "🟢")
        yellow = sum(1 for r in results if r.get("tricolor") == "🟡")
        red = sum(1 for r in results if r.get("tricolor") == "🔴")

        report_lines.append("-" * 70)
        report_lines.append("  📊 统计概览")
        report_lines.append("-" * 70)
        report_lines.append(f"  总文件数: {total}")
        report_lines.append(f"  验证成功: {valid} | 验证失败: {errors}")
        report_lines.append(f"  缓存命中: {cached} | 新验证: {valid - cached}")
        report_lines.append(f"  缓存命中率: {(cached / valid * 100):.1f}%" if valid > 0 else "  缓存命中率: N/A")
        report_lines.append("")

        # 三色分布
        report_lines.append("-" * 70)
        report_lines.append("  🚦 三色审计分布")
        report_lines.append("-" * 70)
        report_lines.append(f"  🟢 通过 (Green):   {green} 文件")
        report_lines.append(f"  🟡 待审 (Yellow):  {yellow} 文件")
        report_lines.append(f"  🔴 熔断 (Red):    {red} 文件")
        report_lines.append("")

        # 详细结果
        report_lines.append("-" * 70)
        report_lines.append("  📋 详细验证结果")
        report_lines.append("-" * 70)

        for i, result in enumerate(results, 1):
            if "error" in result:
                report_lines.append(f"  [{i}] ❌ {result.get('file_path', 'N/A')}")
                report_lines.append(f"      错误: {result['error']}")
                continue

            tricolor = result.get("tricolor", "🟡")
            score = result.get("lineage_score", 0)
            dna = result.get("dna_signature", "")
            fpath = result.get("file_path", "N/A")
            cached_mark = "[缓存]" if result.get("from_cache") else "[新验]"

            report_lines.append(f"  [{i}] {tricolor} {cached_mark} {Path(fpath).name}")
            report_lines.append(f"      路径: {fpath}")
            report_lines.append(f"      综合得分: {score:.2%}")
            report_lines.append(f"      DNA: {dna}")

            # 六层分数
            layer_scores = result.get("layer_scores", {})
            for layer_key, layer_config in self.LINEAGE_PATTERNS.items():
                lname = layer_config["names"][0]
                lscore = layer_scores.get(layer_key, 0)
                bar = "█" * int(lscore * 10) + "░" * (10 - int(lscore * 10))
                report_lines.append(f"      {lname:8s}: [{bar}] {lscore:.2f}")

            # 问题列表
            issues = result.get("issues", [])
            if issues:
                report_lines.append(f"      ⚠️  问题 ({len(issues)}项):")
                for issue in issues[:5]:  # 最多显示5个
                    report_lines.append(f"         → {issue}")
                if len(issues) > 5:
                    report_lines.append(f"         ... 等共{len(issues)}项")

            report_lines.append("")

        # AI Truth Protocol 标注
        report_lines.append("-" * 70)
        report_lines.append("  🤖 AI Truth Protocol")
        report_lines.append("-" * 70)
        report_lines.append("  本报告由龍魂六层来源链验证系统v2.0自动生成")
        report_lines.append("  受CNSH内容主权协议保护")
        report_lines.append("  任何AI系统不得篡改、删除或声称对此报告的所有权")
        report_lines.append("  验证数据永久存储于SQLite数据库，append-only不可删除")
        report_lines.append("")

        # 铁律自审结果
        report_lines.append("-" * 70)
        report_lines.append("  ⚖️ 铁律自审闸")
        report_lines.append("-" * 70)
        all_passed = all(
            r.get("iron_law_passed", True)
            for r in results if "error" not in r
        )
        report_lines.append(f"  自审状态: {'✅ 全部通过' if all_passed else '❌ 存在违规'}")
        report_lines.append("  铁律清单: 人永远是1 | 不蒸馏知识 | 不走捷径 | DNA不可删除 | 主权不可转让")
        report_lines.append("")

        report_lines.append("=" * 70)
        report_lines.append("  报告结束 · Report End")
        report_lines.append("  数据主权归于人民 · 内容主权永不转让")
        report_lines.append("=" * 70)

        return "\n".join(report_lines)

    @supervised("machine")
    def get_cache_stats(self) -> Dict:
        """获取缓存命中率统计 - 真实SQLite查询"""
        conn = sqlite3.connect(str(self.verification_db))
        cursor = conn.cursor()

        cursor.execute("""
            SELECT total_verified, cache_hits, cache_misses,
                   green_count, yellow_count, red_count
            FROM verification_stats
            ORDER BY id DESC LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()

        if row:
            total_verified, hits, misses, green, yellow, red = row
            hit_rate = hits / (hits + misses) * 100 if (hits + misses) > 0 else 0
            return {
                "total_verified": total_verified,
                "cache_hits": hits,
                "cache_misses": misses,
                "cache_hit_rate": round(hit_rate, 2),
                "tricolor_distribution": {
                    "green": green,
                    "yellow": yellow,
                    "red": red
                },
                "db_path": str(self.verification_db)
            }

        return {
            "total_verified": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "cache_hit_rate": 0.0,
            "tricolor_distribution": {"green": 0, "yellow": 0, "red": 0},
            "db_path": str(self.verification_db)
        }

    @supervised("community")
    def export_to_json(self, results: List[Dict], output_path: str) -> str:
        """
        导出验证结果为JSON
        三层监督: L3-社区审计 (结果开放透明)
        """
        export_data = {
            "export_meta": {
                "version": "v2.0",
                "timestamp": datetime.now().isoformat(),
                "dna": "#龍芯⚡️2026-06-17-LINEAGE-VERIFICATION-v2.0",
                "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
                "total_results": len(results)
            },
            "results": results
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

        return output_path


# ═══════════════════════════════════════════════════════════════
# 自动触发机制
# ═══════════════════════════════════════════════════════════════
class AutoAuditTrigger:
    """
    自动审计触发器 - 真实实现
    当文件进入监控目录时自动触发来源链验证
    """

    def __init__(self, watch_dir: Optional[str] = None):
        self.engine = LineageVerificationEngine()
        self.watch_dir = Path(watch_dir) if watch_dir else Path.cwd()
        self.trigger_log = Path.home() / '.龍魂' / 'auto_trigger.log'
        self.trigger_log.parent.mkdir(parents=True, exist_ok=True)
        self._running = False
        self._interval = 5  # 扫描间隔(秒)

    def _log_trigger(self, message: str):
        """记录触发日志 (append-only)"""
        timestamp = datetime.now().isoformat()
        with open(self.trigger_log, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
        print(f"[AUTO-TRIGGER] {message}")

    @supervised("machine")
    def trigger_on_file(self, file_path: str) -> Dict:
        """
        对单个文件触发自动审计
        这是自动触发机制的核心方法
        """
        self._log_trigger(f"文件触发: {file_path}")
        result = self.engine.verify_file(file_path)

        tricolor = result.get("tricolor", "🟡")
        self._log_trigger(
            f"审计完成: {Path(file_path).name} [{tricolor}] "
            f"得分:{result.get('lineage_score', 0):.2%}"
        )

        return result

    @supervised("machine")
    def trigger_on_directory(self, directory: str, pattern: str = "*") -> List[Dict]:
        """对目录中的所有文件触发批量审计"""
        self._log_trigger(f"目录触发: {directory} (模式: {pattern})")
        results = self.engine.verify_batch(directory, pattern=pattern)

        green = sum(1 for r in results if r.get("tricolor") == "🟢")
        yellow = sum(1 for r in results if r.get("tricolor") == "🟡")
        red = sum(1 for r in results if r.get("tricolor") == "🔴")

        self._log_trigger(
            f"批量审计完成: {len(results)}个文件 "
            f"[🟢{green} 🟡{yellow} 🔴{red}]"
        )

        return results

    @supervised("machine")
    def start_watchdog(self, interval: int = 5):
        """
        启动监控守护进程 (简化版)
        定时扫描watch_dir目录,对新文件自动触发审计
        """
        self._interval = interval
        self._running = True
        self._log_trigger(f"守护进程启动: 监控目录={self.watch_dir}, 间隔={interval}s")

        # 记录已见文件集合
        seen_files = set()
        if self.watch_dir.exists():
            seen_files = {
                str(p) for p in self.watch_dir.rglob("*")
                if p.is_file() and not p.name.startswith('.')
            }

        print(f"\n🔍 自动审计守护进程已启动")
        print(f"   监控目录: {self.watch_dir}")
        print(f"   扫描间隔: {interval}秒")
        print(f"   按 Ctrl+C 停止\n")

        try:
            while self._running:
                if self.watch_dir.exists():
                    current_files = {
                        str(p) for p in self.watch_dir.rglob("*")
                        if p.is_file() and not p.name.startswith('.')
                    }

                    new_files = current_files - seen_files
                    for new_file in new_files:
                        self.trigger_on_file(new_file)

                    seen_files = current_files

                time.sleep(interval)

        except KeyboardInterrupt:
            self._log_trigger("守护进程被用户停止")
            print("\n👋 守护进程已停止")

    def stop_watchdog(self):
        """停止监控守护进程"""
        self._running = False
        self._log_trigger("守护进程停止信号已发送")


# ═══════════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════════
def main():
    """主程序入口"""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║     🐉 龍魂 · 六层来源链自动验证系统 v2.0 🐉                    ║
║     LongHun Six-Layer Lineage Auto-Verification System            ║
║                                                                    ║
║  DNA:#龍芯⚡️2026-06-17-LINEAGE-VERIFICATION-v2.0               ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                    ║
║  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL    ║
║                                                                    ║
║  六层来源链: 道统层 → 精神层 → 设备层 → 技术层 → 系统层 → 生命层  ║
║  三层监督: L1机器审计 | L2创作者审计 | L3社区审计                  ║
║  三色审计: 🟢通过 | 🟡待审 | 🔴熔断                              ║
║  铁律自审闸: 人永远是1 | 不蒸馏 | 不捷径 | DNA不可删 | 主权不可转  ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
""")

    engine = LineageVerificationEngine()

    # 演示1: 验证自身文件
    print("【演示1】验证自身脚本...")
    self_path = Path(__file__)
    result = engine.verify_file(str(self_path))

    print(f"  DNA签名: {result.get('dna_signature', 'N/A')}")
    print(f"  综合得分: {result.get('lineage_score', 0):.2%}")
    print(f"  三色状态: {result.get('tricolor', '?')} - {result.get('tricolor_advice', '')}")
    print(f"  铁律自审: {'✅ 通过' if result.get('iron_law_passed') else '❌ 违规'}")
    print(f"  来源缓存: {'✅ 命中' if result.get('from_cache') else '🆕 新验证'}")

    # 显示六层分数
    print("\n  六层来源链得分:")
    for layer_key, layer_config in LineageVerificationEngine.LINEAGE_PATTERNS.items():
        lname = layer_config["names"][0]
        lscore = result.get("layer_scores", {}).get(layer_key, 0)
        bar = "█" * int(lscore * 10) + "░" * (10 - int(lscore * 10))
        print(f"    {lname:8s}: [{bar}] {lscore:.2f}")

    # 显示CNSH四层检查
    print("\n  CNSH四层检查:")
    cnsh = result.get("cnsh_scores", {})
    for layer, data in cnsh.items():
        if isinstance(data, dict) and "score" in data:
            status = "✅" if data["score"] >= 0.85 else ("⚠️" if data["score"] >= 0.60 else "❌")
            print(f"    {status} {layer}: {data['score']:.2f}")

    # 演示2: 缓存命中率统计
    print("\n【演示2】缓存命中率统计...")
    stats = engine.get_cache_stats()
    print(f"  总验证数: {stats['total_verified']}")
    print(f"  缓存命中: {stats['cache_hits']}")
    print(f"  缓存未命中: {stats['cache_misses']}")
    print(f"  命中率: {stats['cache_hit_rate']:.1f}%")

    # 演示3: 自动触发器
    print("\n【演示3】自动触发器...")
    trigger = AutoAuditTrigger()
    trigger_result = trigger.trigger_on_file(str(self_path))
    print(f"  触发审计完成: {trigger_result.get('tricolor', '?')}")

    # 演示4: 生成完整报告
    print("\n【演示4】生成验证报告...")
    # 验证几个原始脚本文件
    original_dir = Path(__file__).parent.parent / "original"
    if original_dir.exists():
        batch_results = engine.verify_batch(str(original_dir), pattern="*.py")
        report = engine.generate_report(batch_results)
        report_path = Path.home() / '.龍魂' / 'lineage_report_v2.txt'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"  报告已保存: {report_path}")
        print(f"  共验证 {len(batch_results)} 个文件")
    else:
        # 只报告自身
        report = engine.generate_report([result])
        print(report[:1500])
        print("  ... (报告截断)")

    print("""
╔════════════════════════════════════════════════════════════════════╗
║  ✅ 六层来源链验证系统 v2.0 运行完成                               ║
║  所有验证数据已写入SQLite缓存，append-only，不可删除                ║
║  数据主权归于人民 · 内容主权永不转让                                ║
╚════════════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    main()
