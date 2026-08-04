#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ═══════════════════════════════════════════
# 龍魂体系 | 目录吸收命名统一引擎 v1.0
# ═══════════════════════════════════════════
# DNA追溯码：#龍芯⚡️丙午·辛未·乙酉·ABSORB-v1.0
# 创建者：UID9622（诸葛鑫）
# 功能：将分散目录的脚本/文档全部按四层命名法吸收统一
# ═══════════════════════════════════════════
"""
目录吸收引擎 v1.0
===============
将以下目录中的文件吸收到龍魂主命名体系：
  1. 统一入口/CNSH核心/    → bin/ + 01_protocols/ + L9_子系统/
  2. agents/                → bin/ (lh_前缀)
  3. android-auto/          → L9_子系统/android_auto/
  4. 龍魂洛书369引擎/       → L9_子系统/luoshu_369_engine/
  5. 龍魂取证内核/          → L9_子系统/forensic_kernel/
  6. articles/              → articles/ (规范化日期前缀)
  7. baobao-guardian/       → L9_子系统/baobao_guardian/
"""

import os, re, sys, json, shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Any, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ABSORB_TARGETS = {
    "cns_core": PROJECT_ROOT / "统一入口/CNSH核心",
    "agents": PROJECT_ROOT / "agents",
    "android_auto": PROJECT_ROOT / "android-auto",
    "luoshu_369": PROJECT_ROOT / "龍魂洛书369引擎",
    "forensic": PROJECT_ROOT / "龍魂取证内核",
    "articles": PROJECT_ROOT / "articles",
    "baobao_guardian": PROJECT_ROOT / "baobao-guardian",
}

# ═══════════════════════════════════════════
# 中文→英文映射表
# ═══════════════════════════════════════════
CN_TO_EN_MAP = {
    # 目录名
    "龍魂洛书369引擎": "luoshu_369_engine",
    "龍魂取证内核": "forensic_kernel",
    "统一入口": "unified_entry",
    "CNSH核心": "cnsh_core",
    "功能模块": "functional_modules",
    "规范": "specs",
    "龍魂-决策流场-自动化优化": "decision_flow_auto_optimize",
    "人性密码学_v2.0": "human_crypto_v2",
    "人性密码学": "human_crypto",
    "可视化版": "visual_edition",
    "CSDN发布版": "csdn_edition",
    # 文件词根
    "龍魂": "longhun",
    "宝宝": "baobao",
    "启动器": "launcher",
    "技能内核": "skill_kernel",
    "技能收集器": "skill_collector",
    "取证内核": "forensic_kernel",
    "决策流场": "decision_flow",
    "自动化优化": "auto_optimize",
    "人性": "human_nature",
    "密码学": "cryptography",
    "易经": "yijing",
    "算法": "algorithm",
    "神经网络": "neural_network",
    "系统全景": "system_panorama",
    "真正含义": "true_meaning",
    "钥匙交接书": "key_handover",
    "待整理目录深度分析": "pending_cleanup_analysis",
    "主权": "sovereignty",
    "理念": "concept",
    "论文": "thesis",
    "体系": "system",
    "学术": "academic",
    "精读": "deep_read",
    "战略框架": "strategic_framework",
    "理论基础": "theoretical_basis",
    "深化框架": "deep_framework",
    "七维人性": "seven_dimension_human",
    "详细档案": "detailed_profile",
    "实践基础": "practical_foundation",
    "工作规划": "work_plan",
    "旧账处理": "old_debt_handling",
    "公式卡片": "formula_card",
    "旧账怎么算": "how_to_settle_old_debts",
    "主权追溯版": "sovereignty_tracing_edition",
    "发布版": "publish_edition",
    "孤立文件治理": "orphan_file_governance",
    "技能落地报告": "skill_landing_report",
    "三才算法": "sancai_algorithm",
    "统一算法根基": "unified_algorithm_foundation",
    "算法对齐声明": "algorithm_alignment_statement",
    "行为密码学": "behavioral_crypto",
    "七因子视角": "seven_factor_perspective",
    "老实人": "honest_person",
    "算计者": "schemer",
    "全资产审查看板": "full_asset_audit_dashboard",
    "灵活与原则": "flexibility_and_principles",
    "无底线即虚无": "no_bottom_line_is_void",
    "价值观": "values",
    "窮則變創新引擎": "innovation_engine",
    "三才對齊說明": "sancai_alignment_explanation",
    "算法公司": "algorithm_company",
    "护城河规范": "moat_specification",
    "优化版": "optimized_edition",
    "天道系统": "tiandao_system",
    "心法": "heart_method",
    "归源": "return_to_source",
    "隐私白皮书": "privacy_whitepaper",
    "时间轴": "timeline",
    "分层架构": "layered_architecture",
    "伦理量子": "ethical_quantum",
    "中式价值对齐方案": "chinese_value_alignment",
    "展示页": "showcase_page",
    "龍芯北辰": "longxin_beichen",
    "提前消费的真相": "truth_of_advance_consumption",
    "离火运觉醒": "li_fire_awakening",
    "资料与模板设计": "materials_and_template_design",
    "初心之翼": "wings_of_original_intent",
    "本地大脑": "local_brain",
    "历史投喂归档": "historical_feed_archive",
    "面向护童的人性优先人工智能系统": "child_protection_human_first_ai",
    "上帝之眼": "eye_of_god",
    "卦审计算法引擎": "hexagram_audit_engine",
    "永恒级监管标准": "eternal_supervision_standard",
    "文化语义流场总协议": "cultural_semantic_flow_protocol",
    "数学落地版": "math_implementation_edition",
    "权重伦理熔断": "weighted_ethical_circuit_breaker",
    "底座模型训练架构": "base_model_training_architecture",
    "专项技术解析": "technical_analysis",
    "量子态人格触角架构": "quantum_persona_antenna_architecture",
    "搜索关键字算法": "search_keyword_algorithm",
    "驱动时空织网": "spacetime_weave_driven",
    "哲学落地版": "philosophy_implementation",
    "数字主权": "digital_sovereignty",
    "诸葛亮": "zhugeliang",
    "鋰電技術推演": "lithium_battery_tech_deduction",
    "完整版": "full_edition",
    "发微": "elucidation",
    "为曾老师正名": "vindicate_master_zeng",
    # 洛书369术语
    "六十四卦编码": "hexagram64_encoder",
    "数字根与不动点": "digital_root_fixpoint",
    "洛书矩阵": "luoshu_matrix",
    "统一验证器": "unified_validator",
    "量子态熵值": "quantum_entropy",
    "宇宙编码": "cosmic_code",
    "道德经公理": "daodejing_axiom",
    "上帝之眼": "eye_of_god",
    "八门金锁": "eight_gate_lock",
    "九宫格": "nine_grid",
    "星宿算法": "constellation_algo",
    "信息传播断层": "info_propagation_fault",
    "量子态映射": "quantum_state_mapping",
    "太极递归与五行图论": "taiji_recursion_wuxing_graph",
    "特征值分布": "eigenvalue_distribution",
    "伦理权重系统": "ethics_weight_system",
    "西游记人性模型": "journey_west_human_model",
    "私域主权定理": "private_domain_sovereignty_theorem",
    "易经": "yijing",
    "易經": "yijing",  # 繁体
    "諸葛亮": "zhugeliang",  # 繁体
    "諸葛": "zhuge",
    "亮易": "liang_yi",
    "鋰電": "lithium_battery",
    "技術": "tech",
    "推演": "deduction",
    "當我們": "when_we",
    "使用工具": "use_tools",
    "是誰在使用誰": "who_is_using_whom",
    # 通用词
    "引擎": "engine",
    "系统": "system",
    "协议": "protocol",
    "报告": "report",
    "记录": "record",
    "数据": "data",
    "核心": "core",
    "基础": "base",
    "测试": "test",
    "工具": "tool",
    "配置": "config",
    "文档": "doc",
    "日志": "log",
    "备份": "backup",
    "归档": "archive",
}

# 已知的不要动的文件（特殊例外，按basename匹配）
DO_NOT_RENAME_BASENAMES = {
    "README.md", "INDEX.md", "AGENTS.md", "CHANGELOG.md", "ATTRIBUTION.md",
    "__init__.py", "main_fearless_steve.cpp",  # __init__是Python包必须文件
}
DO_NOT_RENAME_DIRS = {
    "__pycache__",  # Python字节码缓存
    ".git", "node_modules", ".venv", "venv",
}

# 文件类型处理策略
SKIP_PATTERNS = [
    r'node_modules/',
    r'\.git/',
    r'__pycache__/',
    r'\.venv/',
    r'venv/',
    r'\.next/',
    r'dist/',
    r'build/',
    r'\.codebuddy/',
    r'\.claude/',  # Claude 配置文件不动
    r'\.DS_Store',
]

# ═══════════════════════════════════════════
# 命名规范化工具函数
# ═══════════════════════════════════════════

def should_skip(rel_path: str, is_dir: bool = False) -> bool:
    """检查是否应跳过"""
    basename = os.path.basename(rel_path)
    if is_dir and basename in DO_NOT_RENAME_DIRS:
        return True
    if basename in DO_NOT_RENAME_BASENAMES:
        return True
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, rel_path):
            return True
    return False


def cn_to_en(name: str) -> str:
    """中文→英文映射（大词优先，词间加下划线分隔）"""
    # 先精确匹配
    if name in CN_TO_EN_MAP:
        return CN_TO_EN_MAP[name]
    
    result = name
    # 按长度降序替换（长词优先）
    sorted_keys = sorted(CN_TO_EN_MAP.keys(), key=len, reverse=True)
    
    # 使用占位符避免交叉替换
    replacements = []
    for i, cn_word in enumerate(sorted_keys):
        placeholder = f"__CNREP{i}__"
        if cn_word in result:
            result = result.replace(cn_word, placeholder)
            replacements.append((placeholder, CN_TO_EN_MAP[cn_word]))
    
    # 执行替换
    for placeholder, en_word in replacements:
        result = result.replace(placeholder, f"_{en_word}_")
    
    # 去掉残留中文
    cleaned = []
    for char in result:
        if '\u4e00' <= char <= '\u9fff' or '\u3000' <= char <= '\u303f':
            continue
        cleaned.append(char)
    
    result = ''.join(cleaned)
    
    # 清理标点
    for ch in '，。、（）《》·∞— ':
        result = result.replace(ch, '_')
    
    # 去连续下划线、首尾下划线
    result = re.sub(r'_+', '_', result)
    result = result.strip('_')
    
    return result.lower() if result else name


def normalize_filename(filename: str, is_py: bool = False) -> str:
    """
    规范化文件名
    - 驼峰→蛇形
    - 大写→小写
    - 中文→英文
    - longhun_ → lh_
    """
    name, ext = os.path.splitext(filename)
    
    # 处理中文
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', name))
    if has_chinese:
        name = cn_to_en(name)
    
    # longhun_ → lh_ (但保留 longhun 在其他位置)
    if name.startswith('longhun_'):
        name = 'lh_' + name[8:]
    elif name.startswith('LONGHUN_'):
        name = 'lh_' + name[8:].lower()
    elif name.startswith('LONGHUN-'):
        name = 'lh_' + name[8:].lower()
    
    # 全大写→小写 (但保留首字母缩写如 CNSH, DNA 等已知缩写)
    # 如果全部大写且长度>3且不是已知缩写
    known_acronyms = {'CNSH', 'DNA', 'GPG', 'UID', 'AI', 'API', 'CSV', 'JSON', 'YAML', 'XML', 'HTML', 'CSS', 'JS', 'TS'}
    parts = name.split('_')
    new_parts = []
    for part in parts:
        if part in known_acronyms:
            new_parts.append(part)  # 保留已知缩写
        elif part.isupper() and len(part) > 1:
            new_parts.append(part.lower())
        else:
            new_parts.append(part)
    name = '_'.join(new_parts)
    
    # 驼峰→蛇形 (camelCase → snake_case)
    name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    
    # 去连字符
    name = name.replace('-', '_')
    
    # 清理
    name = name.lower()
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    
    # 确保 lh_ 前缀 (仅对 py/sh 文件)
    if is_py and ext in ('.py', '.sh') and not name.startswith('lh_'):
        name = 'lh_' + name
    
    return name + ext


def normalize_dirname(dirname: str) -> str:
    """规范化目录名"""
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', dirname))
    if has_chinese:
        dirname = cn_to_en(dirname)
    
    dirname = dirname.replace('-', '_')
    dirname = dirname.replace(' ', '_')
    dirname = re.sub(r'_+', '_', dirname)
    dirname = dirname.strip('_')
    return dirname.lower()


# ═══════════════════════════════════════════
# 审计扫描器
# ═══════════════════════════════════════════

class AbsorbAuditor:
    """目录吸收审计器"""
    
    def __init__(self, root: Path):
        self.root = root
        self.rename_plan = []  # [(source_rel, dest_rel, reason)]
        self.skip_list = []
        self.stats = {"total": 0, "rename": 0, "skip": 0}
    
    def scan_directory(self, dir_path: Path, target_dest: str, 
                       process_py_sh: bool = True, process_md: bool = True,
                       rename_dirs: bool = True):
        """递归扫描目录"""
        if not dir_path.exists():
            return
        
        for item in sorted(dir_path.rglob('*')):
            rel = str(item.relative_to(self.root))
            
            if should_skip(rel):
                continue
            
            if item.is_dir():
                if rename_dirs:
                    if should_skip(rel, is_dir=True):
                        continue
                    new_name = normalize_dirname(item.name)
                    if new_name != item.name:
                        dest_rel = str((item.parent / new_name).relative_to(self.root))
                        self.rename_plan.append((rel, dest_rel, "目录中文/不规范命名"))
                        self.stats["total"] += 1
                        self.stats["rename"] += 1
                continue
            
            if should_skip(rel):
                continue
            
            self.stats["total"] += 1
            
            ext = item.suffix.lower()
            is_py_sh = ext in ('.py', '.sh', '.bat')
            is_md = ext in ('.md', '.txt')
            
            if (is_py_sh and not process_py_sh) or (is_md and not process_md):
                self.skip_list.append(rel)
                self.stats["skip"] += 1
                continue
            
            # 检查是否需要重命名
            name = item.name
            has_violations = self._check_violations(name, is_py_sh)
            
            if has_violations:
                new_name = normalize_filename(name, is_py=is_py_sh)
                if new_name != name:
                    dest_rel = str((item.parent / new_name).relative_to(self.root))
                    reason = ', '.join(has_violations)
                    self.rename_plan.append((rel, dest_rel, reason))
                    self.stats["rename"] += 1
            else:
                self.skip_list.append(rel)
                self.stats["skip"] += 1
    
    def _check_violations(self, filename: str, is_py_sh: bool) -> list[Any]:
        """检查命名违规"""
        violations = []
        name_without_ext = os.path.splitext(filename)[0]
        
        if re.search(r'[\u4e00-\u9fff]', filename):
            violations.append("中文字符")
        
        if re.search(r'[A-Z]', filename) and not filename.startswith('LONGHUN-'):
            violations.append("大写字母")
        
        if '-' in name_without_ext:
            violations.append("连字符")
        
        if is_py_sh and not filename.startswith('lh_'):
            violations.append("缺少lh_前缀")
        
        if re.search(r'[A-Z][a-z]', name_without_ext):
            violations.append("驼峰命名")
        
        return violations
    
    def scan_all(self):
        """全量扫描"""
        print("=" * 60)
        print("  龍魂·目录吸收审计引擎 v1.0")
        print("=" * 60)
        
        # 1. 统一入口/CNSH核心 — 根级.py/.sh + 重要.md
        cns = ABSORB_TARGETS["cns_core"]
        if cns.exists():
            print(f"\n📂 扫描: 统一入口/CNSH核心/")
            # 根级文件
            for item in sorted(cns.iterdir()):
                if item.is_dir():
                    dir_rel = str(item.relative_to(self.root))
                    if should_skip(dir_rel, is_dir=True):
                        continue
                    # 子目录重命名
                    new_dir_name = normalize_dirname(item.name)
                    if new_dir_name != item.name:
                        dest_rel = str((item.parent / new_dir_name).relative_to(self.root))
                        self.rename_plan.append((dir_rel, dest_rel, "目录中文/不规范命名"))
                        self.stats["total"] += 1
                        self.stats["rename"] += 1
                elif item.is_file():
                    rel = str(item.relative_to(self.root))
                    if should_skip(rel):
                        continue
                    self.stats["total"] += 1
                    ext = item.suffix.lower()
                    is_py_sh = ext in ('.py', '.sh')
                    violations = self._check_violations(item.name, is_py_sh)
                    if violations:
                        new_name = normalize_filename(item.name, is_py=is_py_sh)
                        dest_rel = str((item.parent / new_name).relative_to(self.root))
                        self.rename_plan.append((rel, dest_rel, ', '.join(violations)))
                        self.stats["rename"] += 1
                    else:
                        self.skip_list.append(rel)
                        self.stats["skip"] += 1
        
        # 2. agents/ — .py + .md 根级文件
        agents = ABSORB_TARGETS["agents"]
        if agents.exists():
            print(f"📂 扫描: agents/")
            for item in sorted(agents.iterdir()):
                if item.is_file():
                    rel = str(item.relative_to(self.root))
                    if should_skip(rel):
                        continue
                    self.stats["total"] += 1
                    ext = item.suffix.lower()
                    is_py_sh = ext in ('.py', '.sh')
                    violations = self._check_violations(item.name, is_py_sh)
                    if violations:
                        new_name = normalize_filename(item.name, is_py=is_py_sh)
                        dest_rel = str((item.parent / new_name).relative_to(self.root))
                        self.rename_plan.append((rel, dest_rel, ', '.join(violations)))
                        self.stats["rename"] += 1
                    else:
                        self.skip_list.append(rel)
                        self.stats["skip"] += 1
        
        # 3. android-auto/
        aa = ABSORB_TARGETS["android_auto"]
        if aa.exists():
            print(f"📂 扫描: android-auto/")
            for item in sorted(aa.rglob('*')):
                if item.is_file():
                    rel = str(item.relative_to(self.root))
                    if should_skip(rel):
                        continue
                    self.stats["total"] += 1
                    violations = self._check_violations(item.name, is_py_sh=False)
                    if violations:
                        new_name = normalize_filename(item.name, is_py=False)
                        dest_rel = str((item.parent / new_name).relative_to(self.root))
                        self.rename_plan.append((rel, dest_rel, ', '.join(violations)))
                        self.stats["rename"] += 1
                    else:
                        self.skip_list.append(rel)
                        self.stats["skip"] += 1
        
        # 4. 龍魂洛书369引擎/
        l369 = ABSORB_TARGETS["luoshu_369"]
        if l369.exists():
            print(f"📂 扫描: 龍魂洛书369引擎/")
            # 先重命名目录本身
            dir_rel = str(l369.relative_to(self.root))
            new_dir_name = normalize_dirname(l369.name)
            if new_dir_name != l369.name:
                dest_dir_rel = str((l369.parent / new_dir_name).relative_to(self.root))
                self.rename_plan.append((dir_rel, dest_dir_rel, "目录中文"))
                self.stats["total"] += 1
                self.stats["rename"] += 1
            
            for item in sorted(l369.rglob('*')):
                if item.is_file():
                    rel = str(item.relative_to(self.root))
                    if should_skip(rel):
                        continue
                    self.stats["total"] += 1
                    ext = item.suffix.lower()
                    is_py_sh = ext in ('.py', '.sh')
                    violations = self._check_violations(item.name, is_py_sh)
                    if violations:
                        new_name = normalize_filename(item.name, is_py=is_py_sh)
                        # 前缀替换：所有在旧目录下的文件都迁移到新目录
                        if rel.startswith(dir_rel + '/'):
                            rest = rel[len(dir_rel) + 1:]  # 去掉旧目录前缀
                            parent_rest = os.path.dirname(rest)
                            dest_rel = f"{dest_dir_rel}/{parent_rest}/{new_name}" if parent_rest else f"{dest_dir_rel}/{new_name}"
                            dest_rel = dest_rel.replace('//', '/')
                        else:
                            parent_rel = str(item.parent.relative_to(self.root))
                            dest_rel = str((self.root / parent_rel / new_name).relative_to(self.root))
                        self.rename_plan.append((rel, dest_rel, ', '.join(violations)))
                        self.stats["rename"] += 1
                    else:
                        self.skip_list.append(rel)
                        self.stats["skip"] += 1
        
        # 5. 龍魂取证内核/
        fk = ABSORB_TARGETS["forensic"]
        if fk.exists():
            print(f"📂 扫描: 龍魂取证内核/")
            dir_rel = str(fk.relative_to(self.root))
            new_dir_name = normalize_dirname(fk.name)
            if new_dir_name != fk.name:
                dest_dir_rel = str((fk.parent / new_dir_name).relative_to(self.root))
                self.rename_plan.append((dir_rel, dest_dir_rel, "目录中文"))
                self.stats["total"] += 1
                self.stats["rename"] += 1
            
            for item in sorted(fk.rglob('*')):
                if item.is_file():
                    rel = str(item.relative_to(self.root))
                    if should_skip(rel):
                        continue
                    self.stats["total"] += 1
                    ext = item.suffix.lower()
                    is_py_sh = ext in ('.py', '.sh')
                    violations = self._check_violations(item.name, is_py_sh)
                    if violations:
                        new_name = normalize_filename(item.name, is_py=is_py_sh)
                        # 前缀替换
                        if rel.startswith(dir_rel + '/'):
                            rest = rel[len(dir_rel) + 1:]
                            parent_rest = os.path.dirname(rest)
                            dest_rel = f"{dest_dir_rel}/{parent_rest}/{new_name}" if parent_rest else f"{dest_dir_rel}/{new_name}"
                            dest_rel = dest_rel.replace('//', '/')
                        else:
                            parent_rel = str(item.parent.relative_to(self.root))
                            dest_rel = str((self.root / parent_rel / new_name).relative_to(self.root))
                        self.rename_plan.append((rel, dest_rel, ', '.join(violations)))
                        self.stats["rename"] += 1
                    else:
                        self.skip_list.append(rel)
                        self.stats["skip"] += 1
        
        # 6. articles/ — 根级 .md
        arts = ABSORB_TARGETS["articles"]
        if arts.exists():
            print(f"📂 扫描: articles/ (根级文件)")
            for item in sorted(arts.iterdir()):
                if item.is_file() and item.suffix.lower() in ('.md', '.txt'):
                    rel = str(item.relative_to(self.root))
                    if should_skip(rel):
                        continue
                    self.stats["total"] += 1
                    violations = self._check_violations(item.name, is_py_sh=False)
                    if violations:
                        new_name = normalize_filename(item.name, is_py=False)
                        dest_rel = str((item.parent / new_name).relative_to(self.root))
                        self.rename_plan.append((rel, dest_rel, ', '.join(violations)))
                        self.stats["rename"] += 1
                    else:
                        self.skip_list.append(rel)
                        self.stats["skip"] += 1
        
        # 7. baobao-guardian/ — 根级文件
        bbg = ABSORB_TARGETS["baobao_guardian"]
        if bbg.exists():
            print(f"📂 扫描: baobao-guardian/ (根级文件)")
            for item in sorted(bbg.iterdir()):
                if item.is_file():
                    rel = str(item.relative_to(self.root))
                    if should_skip(rel):
                        continue
                    self.stats["total"] += 1
                    violations = self._check_violations(item.name, is_py_sh=False)
                    if violations:
                        new_name = normalize_filename(item.name, is_py=(item.suffix in ('.py', '.sh', '.bat')))
                        dest_rel = str((item.parent / new_name).relative_to(self.root))
                        self.rename_plan.append((rel, dest_rel, ', '.join(violations)))
                        self.stats["rename"] += 1
                    else:
                        self.skip_list.append(rel)
                        self.stats["skip"] += 1
        
        print(f"\n{'='*60}")
        print(f"审计完成: {self.stats['total']} 文件")
        print(f"  需重命名: {self.stats['rename']} 件")
        print(f"  合规跳过: {self.stats['skip']} 件")
        print(f"{'='*60}")
    
    def print_plan(self, max_display: int = 50):
        """打印重命名计划"""
        if not self.rename_plan:
            print("\n✅ 无需重命名，所有文件已合规！")
            return
        
        print(f"\n{'='*60}")
        print(f"  重命名计划 ({len(self.rename_plan)} 件)")
        print(f"{'='*60}")
        
        for i, (src, dst, reason) in enumerate(self.rename_plan[:max_display]):
            print(f"\n  [{i+1}] {reason}")
            print(f"    {src}")
            print(f"    → {dst}")
        
        if len(self.rename_plan) > max_display:
            print(f"\n  ... 还有 {len(self.rename_plan) - max_display} 件")
    
    def export_json(self, output_path: Optional[str] = None) -> str:
        """导出JSON"""
        data = {
            "engine": "lh_absorb_directories v1.0",
            "timestamp": datetime.now().isoformat(),
            "stats": self.stats,
            "plan": [{"source": s, "dest": d, "reason": r} for s, d, r in self.rename_plan],
        }
        result = json.dumps(data, ensure_ascii=False, indent=2)
        if output_path:
            Path(output_path).write_text(result)
        return result


# ═══════════════════════════════════════════
# 迁移执行器
# ═══════════════════════════════════════════

class AbsorbExecutor:
    """目录吸收执行器"""
    
    def __init__(self, root: Path, dry_run: bool = True):
        self.root = root
        self.dry_run = dry_run
        self.log = []
        self.errors = []
        self.renamed = 0
        self.renamed_dirs = 0
    
    def _log(self, msg: str):
        self.log.append(msg)
        mode = "DRY-RUN" if self.dry_run else "EXEC"
        print(f"  [{mode}] {msg}")
    
    def _is_same_file(self, src: Path, dst: Path) -> bool:
        """检查是否同一文件（macOS大小写不敏感）"""
        try:
            return src.resolve() == dst.resolve()
        except Exception:
            return src == dst
    
    def execute(self, plan: list[Any]) -> bool:
        """执行重命名计划（深度优先：先处理子文件，再处理父目录）"""
        print(f"\n{'='*60}")
        print(f"  龍魂·目录吸收执行器 v1.0")
        print(f"  模式: {'DRY-RUN (预览)' if self.dry_run else 'EXEC (执行)'}")
        print(f"{'='*60}\n")
        
        if not plan:
            print("无重命名任务")
            return True
        
        # 按路径深度排序：深的先处理（子文件→父目录）
        # 目录重命名放在最后
        file_renames = []
        dir_renames = []
        
        for src_rel, dst_rel, reason in plan:
            src_path = self.root / src_rel
            dst_path = self.root / dst_rel
            
            if not src_path.exists():
                self.errors.append(f"源不存在: {src_rel}")
                continue
            
            # 判断是否是目录重命名
            if src_path.is_dir():
                dir_renames.append((src_rel, dst_rel, reason))
            else:
                file_renames.append((src_rel, dst_rel, reason))
        
        # 先执行文件重命名
        if file_renames:
            print(f"\n📄 阶段1: 文件重命名 ({len(file_renames)} 件)")
            for src_rel, dst_rel, reason in file_renames:
                src = self.root / src_rel
                dst = self.root / dst_rel
                
                if self._is_same_file(src, dst):
                    # macOS大小写不敏感：src和dst是同一文件，只改大小写
                    if not self.dry_run:
                        # 两步rename绕过大小写不敏感
                        tmp = src.with_name(f".tmp_{src.name}")
                        shutil.move(str(src), str(tmp))
                        shutil.move(str(tmp), str(dst))
                    self._log(f"{src_rel} → {dst_rel}  [大小写, {reason}]")
                    self.renamed += 1
                    continue
                
                if dst.exists():
                    self.errors.append(f"目标已存在: {dst_rel}")
                    continue
                
                if not self.dry_run:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                
                self._log(f"{src_rel} → {dst_rel}  [{reason}]")
                self.renamed += 1
        
        # 再执行目录重命名
        if dir_renames:
            print(f"\n📁 阶段2: 目录重命名 ({len(dir_renames)} 件)")
            for src_rel, dst_rel, reason in dir_renames:
                src = self.root / src_rel
                dst = self.root / dst_rel
                
                if self._is_same_file(src, dst):
                    if not self.dry_run:
                        tmp = src.parent / f".tmp_{src.name}"
                        shutil.move(str(src), str(tmp))
                        shutil.move(str(tmp), str(dst))
                    self._log(f"{src_rel} → {dst_rel}  [大小写, {reason}]")
                    self.renamed_dirs += 1
                    continue
                
                if dst.exists():
                    self.errors.append(f"目录目标已存在: {dst_rel}")
                    continue
                
                if not self.dry_run:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                
                self._log(f"{src_rel} → {dst_rel}  [{reason}]")
                self.renamed_dirs += 1
        
        # 汇总
        print(f"\n{'='*60}")
        print(f"执行完成: 文件 {self.renamed} 件, 目录 {self.renamed_dirs} 个")
        if self.errors:
            print(f"⚠️  错误: {len(self.errors)} 条")
            for e in self.errors[:10]:
                print(f"  ❌ {e}")
        print(f"{'='*60}")
        
        if self.dry_run:
            print("\n💡 预览模式。加 --execute 确认执行。")
        
        return len(self.errors) == 0


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="龍魂·目录吸收命名统一引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_absorb_directories.py --audit        # 审计所有目录
  python3 bin/lh_absorb_directories.py --audit --json # JSON输出
  python3 bin/lh_absorb_directories.py --dry-run      # 预览迁移计划
  python3 bin/lh_absorb_directories.py --execute      # 执行迁移
        """
    )
    parser.add_argument("--audit", action="store_true", help="审计扫描")
    parser.add_argument("--dry-run", action="store_true", help="预览迁移")
    parser.add_argument("--execute", action="store_true", help="执行迁移")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--export", type=str, help="导出JSON到文件")
    parser.add_argument("--max-display", type=int, default=100, help="最多显示条数")
    
    args = parser.parse_args()
    
    if not any([args.audit, args.dry_run, args.execute]):
        parser.print_help()
        return
    
    auditor = AbsorbAuditor(PROJECT_ROOT)
    auditor.scan_all()
    
    if args.audit:
        auditor.print_plan(max_display=args.max_display)
        if args.json:
            print(auditor.export_json())
        if args.export:
            auditor.export_json(args.export)
            print(f"\n📁 报告已导出: {args.export}")
    
    elif args.dry_run:
        auditor.print_plan(max_display=args.max_display)
        executor = AbsorbExecutor(PROJECT_ROOT, dry_run=True)
        executor.execute(auditor.rename_plan)
    
    elif args.execute:
        auditor.print_plan(max_display=args.max_display)
        
        if not auditor.rename_plan:
            print("无需执行")
            return
        
        print(f"\n⚠️  即将执行 {len(auditor.rename_plan)} 个重命名操作")
        confirm = input("\n确认执行? 输入 YES 继续: ")
        if confirm != "YES":
            print("已取消")
            return
        
        executor = AbsorbExecutor(PROJECT_ROOT, dry_run=False)
        success = executor.execute(auditor.rename_plan)
        
        # 保存日志
        log_path = PROJECT_ROOT / "data" / "absorb_migration_log.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "mode": "execute",
            "renamed_files": executor.renamed,
            "renamed_dirs": executor.renamed_dirs,
            "errors": executor.errors,
            "log": executor.log,
        }
        log_path.write_text(json.dumps(log_data, ensure_ascii=False, indent=2))
        print(f"\n📄 迁移日志: {log_path}")


if __name__ == "__main__":
    main()
