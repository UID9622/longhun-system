#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂脚本管理器 (LongHun Script Manager)
自动扫描·对齐·验证·修复·审计·签名——全链路一体

DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能:
  - 扫描指定目录下所有脚本（.py/.sh/.html/.md/.json/.yaml/.cnsh）
  - 按龍魂命名规范校验文件名
  - 检查头部 DNA/CONFIRM/SEAL/GPG 四锚
  - 检查函数/类命名风格
  - 检测一票否决词与危险命令
  - 检测 GPG 签名文件 (.asc) 配对状态
  - 生成三色审计报告 🟢/🟡/🔴
  - 自动修复可修复项（DNA补全·命名建议）
  - 联动 lh_time_engine（输出时间戳）
  - 联动 lh_gpg_sign（自动签名报告）
  - 联动 lh_three_color_audit（审计钩子）
  - 联动 lh_deben_audit（修复前德本预检）
  - 联动 lh_dna_generator（动态DNA生成）
  - 输出 Markdown / JSON 报告
  - --full 全流程管道: scan→fix→audit→sign→deben
  - 审计日志 append-only

用法:
  python3 lh_script_manager.py --scan              # 扫描并生成报告
  python3 lh_script_manager.py --scan --fix        # 扫描后自动修复
  python3 lh_script_manager.py --scan --dry-run    # 预览修复（不改文件）
  python3 lh_script_manager.py --report json       # JSON格式报告
  python3 lh_script_manager.py --full              # 全流程管道
  python3 lh_script_manager.py --stamp             # 输出时间戳
  python3 lh_script_manager.py --watch             # 监视模式（持续）
  python3 lh_script_manager.py --init              # 生成龍魂脚本模板

集成到 lh:
  lh script-align --scan
  lh script-align --full
  lh script-align --stamp
"""

import os
import sys
import re
import json
import glob
import argparse
import hashlib
import logging
import time as time_mod
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum

# ============================================================
# 固定锚点（焊死·不可修改）
# ============================================================

DNA = "#龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
VERSION = "1.2"
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ============================================================
# 日志（logs/ 目录，append-only）
# ============================================================

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"script_manager_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("script_manager")

# ============================================================
# 审计日志（audit/ 目录，append-only）
# ============================================================

AUDIT_DIR = PROJECT_ROOT / "audit"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_TRAIL = AUDIT_DIR / "script_manager_audit_trail.jsonl"

# ============================================================
# 枚举与数据类
# ============================================================

class AuditColor(Enum):
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"

class FixAction(Enum):
    """可自动修复的动作类型"""
    ADD_DNA = "add_dna"               # 补 DNA 追溯码
    ADD_CONFIRM = "add_confirm"       # 补确认码
    ADD_SEAL = "add_seal"             # 补主权锚定
    ADD_GPG_ANCHOR = "add_gpg_anchor" # 补 GPG 锚点注释
    ADD_HEADER = "add_header"         # 补完整头三行
    GEN_ASC = "gen_asc"              # 生成 GPG .asc 签名（需 gpg 可用）
    FIX_SHEBANG = "fix_shebang"      # 修正 shebang

@dataclass
class ScriptInfo:
    """脚本完整信息"""
    path: Path
    name: str
    ext: str
    category: str
    priority: str                          # P1/P2/P3
    # 四锚检查
    dna_found: Optional[str] = None
    confirm_found: Optional[str] = None
    seal_found: Optional[str] = None
    gpg_found: bool = False
    has_shebang: bool = False
    has_main_guard: bool = False
    # 签名状态
    asc_exists: bool = False
    asc_size: int = 0
    # 命名
    naming_valid: bool = False
    naming_issues: List[str] = field(default_factory=list)
    # 问题/建议
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    fixable_actions: List[FixAction] = field(default_factory=list)
    # 统计
    line_count: int = 0
    func_count: int = 0
    class_count: int = 0
    # 审计结果
    color: str = "🟢"
    confidence: float = 1.0

# ============================================================
# CNSH 对齐引擎（内联实现·零外部依赖）
# ============================================================

class CNSHAlignEngine:
    """CNSH 对齐引擎——命名规范·锚点检查·危险检测"""

    # ── 文件头锚点检测 ──
    DNA_RE = re.compile(r'(?:DNA|dna)[:：]\s*(#龍芯⚡️[^\s\n]+)', re.MULTILINE)
    CONFIRM_RE = re.compile(r'(?:CONFIRM|confirm)[:：]\s*(#CONFIRM🌌[^\s\n]+)', re.MULTILINE)
    SEAL_RE = re.compile(r'(?:SEAL|seal)[:：]\s*(#ZHUGEXIN⚡️[^\s\n]+)', re.MULTILINE)
    GPG_RE = re.compile(r'(?:GPG|gpg)[:：]\s*([A-F0-9]{40})', re.MULTILINE)

    # ── 文件名检测 ──
    # 龍魂标准: lh_<模块>_<功能>.py / lh_<功能>.py
    LH_NAME_RE = re.compile(r'^lh_[a-z][a-z0-9_]*(?:_[a-z][a-z0-9_]*)*\.(py|sh)$')
    # 检测是否含繁体「龍」（应为「龍」而非「龍」）
    LONG_SIMP_RE = re.compile(r'龍魂|龍芯|龍盾')

    # ── 一票否决词（来自对齐规则第十层）──
    VETO_WORDS = [
        "技术无国界", "用户体验优先", "灵活处理",
        "国际接轨", "简化管理", "商业化需要",
        "平衡各方", "行业标准",
    ]

    # ── 危险命令 ──
    DANGER_PATTERNS = [
        (r'\brm\s+-rf\s+/', "🔴 危险: rm -rf /"),
        (r'\bsudo\s+rm\b', "🔴 危险: sudo rm"),
        (r'\bchmod\s+777\b', "🟡 警告: chmod 777"),
        (r'\bcurl\s+.*\|\s*(?:ba)?sh\b', "🔴 危险: curl|sh 管道执行"),
        (r'\beval\s*\(', "🟡 警告: eval()"),
    ]

    # ── 函数/类命名规范 ──
    FUNC_SNAKE = re.compile(r'^[a-z][a-z0-9_]*$')
    CLASS_CAMEL = re.compile(r'^[A-Z][a-zA-Z0-9]*$')

    # ── 排除目录 ──
    EXCLUDE_DIRS = {
        '.git', '__pycache__', '.venv', 'venv', 'node_modules',
        '.idea', '.vscode', 'dist', 'build', 'egg-info', '.codebuddy',
        'archive', '_work', 'tombstone_vault', 'models',
    }

    # ── 排除文件 ──
    EXCLUDE_FILES = {
        '__init__.py', 'conftest.py', 'setup.py',
    }

    # ── 扫描后缀 ──
    SCAN_EXTS = {'.py', '.sh', '.html', '.htm', '.md', '.json', '.yaml', '.yml', '.cnsh'}

    @classmethod
    def is_excluded(cls, path: Path, root: Path) -> bool:
        """判断路径是否应排除"""
        parts = path.relative_to(root).parts if path != root else []
        for part in parts:
            if part in cls.EXCLUDE_DIRS or part.startswith('.'):
                return True
        if path.name in cls.EXCLUDE_FILES:
            return True
        if path.suffix not in cls.SCAN_EXTS:
            return True
        # 排除 .asc 签名文件（作为独立实体不审计）
        if path.suffix == '.asc':
            return True
        return False

    @classmethod
    def _detect_category(cls, ext: str) -> str:
        mapping = {
            '.sh': 'shell', '.py': 'python', '.html': 'html',
            '.htm': 'html', '.md': 'markdown', '.json': 'json',
            '.yaml': 'yaml', '.yml': 'yaml', '.cnsh': 'cnsh',
        }
        return mapping.get(ext, 'other')

    @classmethod
    def _get_priority(cls, category: str) -> str:
        mapping = {
            'shell': 'P1', 'python': 'P1', 'cnsh': 'P1',
            'html': 'P2', 'yaml': 'P2',
            'markdown': 'P3', 'json': 'P3',
        }
        return mapping.get(category, 'P3')

    @classmethod
    def analyze(cls, filepath: Path, project_root: Path) -> ScriptInfo:
        """完整分析单个文件"""
        name = filepath.name
        ext = filepath.suffix.lower()
        category = cls._detect_category(ext)

        info = ScriptInfo(
            path=filepath,
            name=name,
            ext=ext,
            category=category,
            priority=cls._get_priority(category),
        )

        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            info.issues.append(f"无法读取文件: {e}")
            info.color = "🔴"
            info.confidence = 0.0
            return info

        lines = content.splitlines()
        info.line_count = len(lines)

        # ── 1. shebang 检测 ──
        info.has_shebang = content.startswith('#!')

        # ── 2. main guard 检测（Python）──
        if ext == '.py':
            info.has_main_guard = 'if __name__' in content
            if not info.has_main_guard and info.line_count > 20:
                info.issues.append("缺少 if __name__ == '__main__' 入口保护")
                info.suggestions.append("添加 if __name__ == '__main__': main()")

        # ── 3. 四锚检测 ──
        dm = cls.DNA_RE.search(content)
        if dm:
            info.dna_found = dm.group(1)
        else:
            info.issues.append("缺少 DNA 追溯码 (#龍芯⚡️...)")
            info.suggestions.append("在文件头部添加 DNA 追溯码")
            info.fixable_actions.append(FixAction.ADD_DNA)

        cm = cls.CONFIRM_RE.search(content)
        if cm:
            info.confirm_found = cm.group(1)
        else:
            info.issues.append("缺少确认码 (#CONFIRM🌌...)")
            info.suggestions.append("在文件头部添加确认码")
            info.fixable_actions.append(FixAction.ADD_CONFIRM)

        sm = cls.SEAL_RE.search(content)
        if sm:
            info.seal_found = sm.group(1)
        else:
            info.issues.append("缺少主权锚定 (#ZHUGEXIN⚡️...)")
            info.suggestions.append("在文件头部添加主权锚定")
            info.fixable_actions.append(FixAction.ADD_SEAL)

        gm = cls.GPG_RE.search(content)
        if gm:
            info.gpg_found = True

        # ── 4. 文件命名检测 ──
        info.naming_valid = bool(cls.LH_NAME_RE.match(name))
        if not info.naming_valid and ext in ('.py', '.sh'):
            info.naming_issues.append(f"文件名不符合 lh_ 规范: {name}")
            info.issues.append(f"文件名不符合 lh_ 规范: {name}")
            info.suggestions.append(f"建议重命名为 lh_<功能>.py 格式")

        # 检测繁体「龍」
        long_simp = cls.LONG_SIMP_RE.findall(content)
        if long_simp:
            info.issues.append(f"发现简体「龍」: {set(long_simp)}，应为繁体「龍」")
            info.suggestions.append("将「龍魂/龍芯/龍盾」改为「龍魂/龍芯/龍盾」")

        # ── 5. 一票否决词检测 ──
        for word in cls.VETO_WORDS:
            if word in content:
                info.issues.append(f"🔴 一票否决词: 「{word}」")
                info.color = "🔴"

        # ── 6. 危险命令检测 ──
        for pattern, msg in cls.DANGER_PATTERNS:
            if re.search(pattern, content):
                info.issues.append(msg)
                if "🔴" in msg:
                    info.color = "🔴"

        # ── 7. 函数/类命名检测（Python）──
        if ext == '.py':
            funcs = re.findall(r'^def\s+(\w+)\s*\(', content, re.MULTILINE)
            info.func_count = len(funcs)
            for f in funcs:
                if not cls.FUNC_SNAKE.match(f) and not f.startswith('_'):
                    info.issues.append(f"函数命名不规范: {f}（应为 snake_case）")
                    info.suggestions.append(f"将函数 {f} 改为小写+下划线格式")

            classes = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)
            info.class_count = len(classes)

        # ── 8. .asc 签名检测 ──
        asc_path = filepath.with_suffix(filepath.suffix + '.asc')
        info.asc_exists = asc_path.exists()
        if info.asc_exists:
            info.asc_size = asc_path.stat().st_size

        if not info.asc_exists and ext in ('.py', '.sh', '.md'):
            info.issues.append("缺少 GPG 分离签名 (.asc)")
            info.suggestions.append(f"运行: python3 bin/lh_gpg_sign.py sign {filepath.name}")
            info.fixable_actions.append(FixAction.GEN_ASC)

        # ── 9. shebang 缺失（可执行脚本）──
        if ext in ('.py', '.sh') and not info.has_shebang:
            info.issues.append("缺少 shebang")
            info.suggestions.append("在首行添加 #!/usr/bin/env python3 或 #!/bin/bash")
            info.fixable_actions.append(FixAction.FIX_SHEBANG)

        # ── 10. 综合评分 ──
        info.confidence = max(0.0, 1.0 - len(info.issues) * 0.12)
        if info.color != "🔴":
            n = len(info.issues)
            if n == 0:
                info.color = "🟢"
            elif n <= 3:
                info.color = "🟡"
            else:
                info.color = "🔴"

        return info

# ============================================================
# 外部引擎集成（优雅降级·不阻塞主流程）
# ============================================================

class ExternalEngines:
    """联动 lh_time_engine / lh_gpg_sign / lh_three_color_audit / lh_deben_audit / lh_dna_generator"""

    @staticmethod
    def get_time_stamp() -> str:
        """调用 lh_time_engine 获取时间戳"""
        script = PROJECT_ROOT / "bin" / "lh_time_engine.py"
        if not script.exists():
            return f"[{datetime.now().isoformat()}] ⚠️ 时间引擎不可用"
        try:
            result = subprocess.run(
                [sys.executable, str(script), "--stamp"],
                capture_output=True, text=True, timeout=10,
                cwd=str(PROJECT_ROOT)
            )
            return result.stdout.strip() or f"[{datetime.now().isoformat()}]"
        except Exception as e:
            return f"[{datetime.now().isoformat()}] ⚠️ 时间引擎调用失败: {e}"

    @staticmethod
    def generate_dna(title: str, category: str, actor: str = "UID9622") -> str:
        """调用 lh_dna_generator 动态生成 DNA"""
        script = PROJECT_ROOT / "bin" / "lh_dna_generator.py"
        if not script.exists():
            return DNA  # 降级为硬编码DNA
        try:
            result = subprocess.run(
                [sys.executable, str(script),
                 "--title", title, "--category", category,
                 "--action", "创建", "--actor", actor,
                 "--output-format", "json"],
                capture_output=True, text=True, timeout=15,
                cwd=str(PROJECT_ROOT)
            )
            data = json.loads(result.stdout)
            return data.get("dna", DNA)
        except Exception:
            return DNA

    @staticmethod
    def sign_file(filepath: Path) -> Tuple[bool, str]:
        """调用 lh_gpg_sign 对文件签名"""
        script = PROJECT_ROOT / "bin" / "lh_gpg_sign.py"
        if not script.exists():
            return False, "GPG 签名引擎不可用"
        try:
            result = subprocess.run(
                [sys.executable, str(script), "sign", str(filepath), "--force"],
                capture_output=True, text=True, timeout=30,
                cwd=str(PROJECT_ROOT)
            )
            ok = "✅" in result.stdout or "sign" in result.stdout.lower()
            return ok, result.stdout.strip()[:200]
        except Exception as e:
            return False, str(e)

    @staticmethod
    def run_deben_audit() -> Tuple[bool, str]:
        """运行德本审计预检"""
        script = PROJECT_ROOT / "bin" / "lh_deben_audit.py"
        if not script.exists():
            return True, "⚠️ 德本审计不可用（跳过）"
        try:
            result = subprocess.run(
                [sys.executable, str(script), "scan", "--quick"],
                capture_output=True, text=True, timeout=30,
                cwd=str(PROJECT_ROOT)
            )
            passed = "通过" in result.stdout or "🟢" in result.stdout
            return passed, result.stdout.strip()[:500]
        except Exception as e:
            return True, f"⚠️ 德本审计异常（跳过）: {e}"

# ============================================================
# 脚本管理器核心
# ============================================================

class ScriptManager:
    """龍魂脚本管理器——扫描·审计·修复·签名·报告"""

    def __init__(self, target_dir: str = "."):
        self.target_dir = Path(target_dir).resolve()
        self.aligner = CNSHAlignEngine()
        self.engines = ExternalEngines()
        self.results: List[ScriptInfo] = []
        self.scan_time: str = datetime.now().isoformat()
        self.time_stamp: str = ""

    # ── 扫描 ──

    def scan(self, pattern: Optional[str] = None) -> List[ScriptInfo]:
        """递归扫描目录下所有符合条件的脚本"""
        root = self.target_dir
        logger.info(f"🔍 扫描目录: {root}")

        all_files: List[Path] = []
        for ext in self.aligner.SCAN_EXTS:
            if pattern:
                all_files.extend(root.rglob(f"*{pattern}*{ext}"))
            else:
                all_files.extend(root.rglob(f"*{ext}"))

        # 去重 + 过滤
        all_files = list(set(all_files))
        all_files = [f for f in all_files if not self.aligner.is_excluded(f, root)]
        all_files.sort()

        self.results = []
        total = len(all_files)
        for i, f in enumerate(all_files):
            if total > 50 and i % max(1, total // 20) == 0:
                pct = int(i / total * 100)
                print(f"\r  扫描进度: {pct}% ({i}/{total})", end="", file=sys.stderr)
            info = self.aligner.analyze(f, root)
            self.results.append(info)

        if total > 50:
            print(f"\r  扫描完成: 100% ({total}/{total})   ", file=sys.stderr)

        self.scan_time = datetime.now().isoformat()
        self.time_stamp = self.engines.get_time_stamp()

        logger.info(f"✅ 扫描完成: {total} 文件, 🟢{self._count('🟢')} 🟡{self._count('🟡')} 🔴{self._count('🔴')}")
        return self.results

    def _count(self, color: str) -> int:
        return sum(1 for r in self.results if r.color == color)

    # ── 修复 ──

    def auto_fix(self, dry_run: bool = False) -> Dict[str, Any]:
        """自动修复可修复项（仅执行安全的自动补全）"""
        if not self.results:
            return {"fixed": [], "failed": [], "skipped": [], "message": "无扫描结果"}

        # 修复前德本审计预检
        deben_ok, deben_msg = self.engines.run_deben_audit()
        if not deben_ok:
            return {
                "fixed": [], "failed": [], "skipped": [],
                "message": f"🔴 德本审计未通过，修复中止\n{deben_msg}"
            }

        fixed = []
        failed = []
        skipped = []

        dna_blocks = {
            FixAction.ADD_DNA: f"# DNA: {DNA}",
            FixAction.ADD_CONFIRM: f"# CONFIRM: {CONFIRM}",
            FixAction.ADD_SEAL: f"# SEAL: {SEAL}",
            FixAction.ADD_GPG_ANCHOR: f"# GPG: {GPG}",
        }

        for r in self.results:
            if r.color == "🟢" and FixAction.GEN_ASC not in r.fixable_actions:
                skipped.append(str(r.path))
                continue

            path = r.path
            try:
                content = path.read_text(encoding='utf-8')
                lines = content.split('\n')
                modified = False

                # 在 shebang 后插入缺失的头部锚点
                insert_pos = 1 if lines and lines[0].startswith('#!') else 0

                for action in r.fixable_actions:
                    if action == FixAction.GEN_ASC:
                        if not dry_run:
                            ok, msg = self.engines.sign_file(path)
                            if ok:
                                fixed.append(f"{path.name} (.asc 签名)")
                                # 更新 asc_exists
                                r.asc_exists = True
                            else:
                                failed.append(f"{path.name} (签名失败: {msg})")
                        else:
                            fixed.append(f"{path.name} (.asc 签名) [dry-run]")
                        continue

                    if action == FixAction.FIX_SHEBANG:
                        if r.ext == '.py' and not content.startswith('#!/usr/bin/env python3'):
                            line = "#!/usr/bin/env python3"
                        elif r.ext == '.sh' and not content.startswith('#!/bin/bash'):
                            line = "#!/bin/bash"
                        else:
                            continue
                        if not dry_run:
                            lines.insert(0, line)
                            modified = True
                        fixed.append(f"{path.name} (shebang) {'[dry-run]' if dry_run else ''}")
                        continue

                    block = dna_blocks.get(action)
                    if block and block not in content:
                        if not dry_run:
                            lines.insert(insert_pos, block)
                            insert_pos += 1
                            modified = True
                        fixed.append(f"{path.name} ({action.value}) {'[dry-run]' if dry_run else ''}")

                if modified and not dry_run:
                    path.write_text('\n'.join(lines), encoding='utf-8')
                    logger.info(f"✅ 已修复: {path.name}")

            except Exception as e:
                failed.append(f"{path.name} ({e})")
                logger.error(f"修复失败 {path}: {e}")

        # 写入审计日志
        self._write_audit_trail("auto_fix", {
            "dry_run": dry_run,
            "fixed": len(fixed),
            "failed": len(failed),
            "skipped": len(skipped),
            "deben_passed": deben_ok,
        })

        return {
            "fixed": fixed,
            "failed": failed,
            "skipped": skipped,
            "time_stamp": self.time_stamp,
            "deben": {"passed": deben_ok, "detail": deben_msg},
        }

    def _write_audit_trail(self, action: str, detail: dict):
        """写入审计日志（append-only）"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "detail": detail,
            "dna": DNA,
        }
        try:
            with open(AUDIT_TRAIL, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        except Exception:
            pass

    # ── 报告生成 ──

    def generate_report(self, fmt: str = 'md') -> str:
        """生成三色审计报告"""
        if not self.results:
            self.scan()

        total = len(self.results)
        green = self._count('🟢')
        yellow = self._count('🟡')
        red = self._count('🔴')

        if fmt == 'json':
            return json.dumps({
                "dna": DNA,
                "confirm": CONFIRM,
                "timestamp": self.scan_time,
                "time_stamp": self.time_stamp,
                "summary": {
                    "total": total,
                    "green": green, "yellow": yellow, "red": red,
                    "pass_rate": f"{green/total*100:.1f}%" if total else "N/A",
                },
                "by_category": self._by_category(),
                "details": [self._serialize(r) for r in self.results],
            }, ensure_ascii=False, indent=2)

        # ── Markdown 报告 ──
        ts = self.time_stamp or f"[{self.scan_time}]"
        lines = [
            "# 🐉 龍魂脚本对齐审计报告",
            "",
            f"**DNA:** `{DNA}`",
            f"**时间戳:** {ts}",
            f"**扫描时间:** {self.scan_time}",
            f"**扫描目录:** `{self.target_dir}`",
            "",
            "---",
            "",
            "## 📊 总体统计",
            "",
            "| 状态 | 数量 | 占比 |",
            "|:---|:---:|:---:|",
            f"| 🟢 通过 | {green} | {green/total*100:.1f}% |" if total else "| 🟢 通过 | 0 | 0% |",
            f"| 🟡 待核 | {yellow} | {yellow/total*100:.1f}% |" if total else "",
            f"| 🔴 红线 | {red} | {red/total*100:.1f}% |" if total else "",
            f"| **总计** | **{total}** | **100%** |",
            "",
            f"**通过率:** {green/total*100:.1f}% ({green}/{total})" if total else "",
            "",
            "---",
            "",
            "## 📁 按类别统计",
            "",
        ]

        by_cat = {}
        for r in self.results:
            by_cat.setdefault(r.category, []).append(r)

        for cat in ['python', 'shell', 'cnsh', 'html', 'markdown', 'json', 'yaml', 'other']:
            items = by_cat.get(cat, [])
            if not items:
                continue
            g = sum(1 for x in items if x.color == '🟢')
            yl = sum(1 for x in items if x.color == '🟡')
            rd = sum(1 for x in items if x.color == '🔴')
            lines.append(f"### {cat.upper()} ({len(items)} 个)")
            lines.append(f"🟢{g} 🟡{yl} 🔴{rd}")
            lines.append("")
            for r in sorted(items, key=lambda x: (x.color, x.name)):
                lines.append(f"- {r.color} `{r.name}` ({r.line_count}行)")
                if r.issues:
                    lines.append(f"  - {r.issues[0]}")
            lines.append("")

        # ── 需要修复的脚本 ──
        needs_fix = [r for r in self.results if r.color != '🟢']
        if needs_fix:
            lines.append("---")
            lines.append("")
            lines.append("## 🚨 需要修复的脚本")
            lines.append("")
            for r in sorted(needs_fix, key=lambda x: (0 if x.color=='🔴' else 1, -len(r.issues))):
                lines.append(f"### {r.color} `{r.name}`")
                lines.append(f"- **路径:** `{r.path.relative_to(self.target_dir)}`")
                lines.append(f"- **类别:** {r.category} | **优先级:** {r.priority}")
                lines.append(f"- **行数:** {r.line_count} | **函数:** {r.func_count} | **类:** {r.class_count}")
                lines.append("")
                lines.append("**问题:**")
                for issue in r.issues:
                    lines.append(f"- {issue}")
                if r.suggestions:
                    lines.append("")
                    lines.append("**建议:**")
                    for s in r.suggestions:
                        lines.append(f"- {s}")
                if r.fixable_actions:
                    lines.append("")
                    lines.append("**可自动修复:**")
                    for a in r.fixable_actions:
                        lines.append(f"- `{a.value}`")
                lines.append("")

        # ── GPG 签名状态 ──
        unsigned = [r for r in self.results if not r.asc_exists and r.ext in ('.py', '.sh', '.md')]
        if unsigned:
            lines.append("---")
            lines.append("")
            lines.append("## 🔐 缺少 GPG 签名的文件")
            lines.append("")
            lines.append(f"共 {len(unsigned)} 个文件缺少 .asc 签名:")
            lines.append("")
            for r in unsigned[:30]:
                lines.append(f"- `{r.name}`")
            if len(unsigned) > 30:
                lines.append(f"- ... 还有 {len(unsigned)-30} 个")
            lines.append("")
            lines.append("**一键签名:** `python3 bin/lh_gpg_sign.py sign .`")

        # ── 执行顺序建议 ──
        lines.append("---")
        lines.append("")
        lines.append("## 📋 修复优先级建议")
        lines.append("")
        for pri in ['P1', 'P2', 'P3']:
            items = [r for r in self.results if r.priority == pri and r.color != '🟢']
            if items:
                lines.append(f"**{pri}** ({len(items)} 个):")
                for r in items:
                    lines.append(f"- {r.color} `{r.name}` — {r.issues[0] if r.issues else '待检'}")
                lines.append("")

        # ── 页脚 ──
        lines.append("---")
        lines.append("")
        lines.append(f"*报告由 龍魂脚本管理器 v{VERSION} 生成*")
        lines.append(f"*GPG: {GPG}*")
        lines.append(f"*{ts}*")

        return '\n'.join(lines)

    def save_report(self, fmt: str = 'md', output: Optional[str] = None) -> Path:
        """保存报告到 audit/ 目录"""
        report = self.generate_report(fmt)
        ext = '.json' if fmt == 'json' else '.md'
        filename = output or f"script_align_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
        out_path = AUDIT_DIR / filename
        out_path.write_text(report, encoding='utf-8')
        logger.info(f"✅ 报告已保存: {out_path}")
        return out_path

    # ── 辅助 ──

    def _by_category(self) -> dict:
        cats = {}
        for r in self.results:
            c = r.category
            if c not in cats:
                cats[c] = {"total": 0, "🟢": 0, "🟡": 0, "🔴": 0}
            cats[c]["total"] += 1
            cats[c][r.color] = cats[c].get(r.color, 0) + 1
        return cats

    @staticmethod
    def _serialize(r: ScriptInfo) -> dict:
        d = asdict(r)
        d['path'] = str(d['path'])
        d['fixable_actions'] = [a.value for a in d['fixable_actions']]
        return d

# ============================================================
# 命令行接口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂脚本管理器 — 扫描·审计·修复·签名·全链路",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
示例:
  %(prog)s --scan                    扫描并生成 Markdown 报告
  %(prog)s --scan --fix              扫描后自动修复
  %(prog)s --scan --fix --dry-run    预览修复（不改文件）
  %(prog)s --scan --report json      生成 JSON 报告
  %(prog)s --full                    全流程: 德本→扫描→修复→审计→签名
  %(prog)s --scan --output my_report.md  保存报告到指定文件
  %(prog)s --stamp                   输出当前时间戳
  %(prog)s --watch                   监视模式（每分钟）
  %(prog)s --init                    生成龍魂脚本模板

版本: {VERSION}
DNA: {DNA}
"""
    )

    parser.add_argument("--dir", "-d", type=str, default=str(PROJECT_ROOT),
                        help=f"扫描目录（默认: {PROJECT_ROOT}）")
    parser.add_argument("--scan", "-s", action="store_true",
                        help="扫描并生成审计报告")
    parser.add_argument("--fix", "-f", action="store_true",
                        help="自动修复可修复项（需配合 --scan）")
    parser.add_argument("--dry-run", "-n", action="store_true",
                        help="预览修复内容，不实际修改文件")
    parser.add_argument("--report", "-r", type=str, choices=['md', 'json'],
                        default='md', help="报告格式（默认: md）")
    parser.add_argument("--output", "-o", type=str,
                        help="报告输出文件名（保存到 audit/ 目录）")
    parser.add_argument("--full", "-F", action="store_true",
                        help="全流程: 德本→扫描→修复→签名→报告")
    parser.add_argument("--sign", action="store_true",
                        help="对生成的报告自动 GPG 签名")
    parser.add_argument("--watch", "-w", action="store_true",
                        help="监视模式（每60秒扫描一次）")
    parser.add_argument("--init", "-i", action="store_true",
                        help="在当前目录生成龍魂脚本模板")
    parser.add_argument("--stamp", action="store_true",
                        help="输出当前时间戳")
    parser.add_argument("--pattern", "-p", type=str,
                        help="文件名过滤模式（如 lh_）")
    parser.add_argument("--version", "-v", action="store_true",
                        help="显示版本信息")

    args = parser.parse_args()

    # ── --version ──
    if args.version:
        print(f"🐉 龍魂脚本管理器 v{VERSION}")
        print(f"DNA: {DNA}")
        print(f"GPG: {GPG}")
        return 0

    # ── --stamp ──
    if args.stamp:
        ts = ExternalEngines.get_time_stamp()
        print(ts)
        return 0

    # ── --init ──
    if args.init:
        template = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
🐉 龍魂脚本模板
DNA: {DNA}
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: {CONFIRM}
SEAL: {SEAL}
GPG: {GPG}

功能: [在此描述脚本功能]

用法:
  python3 [script_name].py --help
\"\"\"

import argparse
import sys
from pathlib import Path


def main():
    print("🐉 龍魂脚本已就绪")


if __name__ == "__main__":
    main()
"""
        target = Path.cwd() / "template_script.py"
        target.write_text(template, encoding='utf-8')
        print(f"✅ 模板已生成: {target}")
        # 自动签名
        ok, msg = ExternalEngines.sign_file(target)
        if ok:
            print(f"✅ 模板已签名: {target}.asc")
        return 0

    # ── --full 全流程管道 ──
    if args.full:
        manager = ScriptManager(args.dir)
        print("🐉 全流程管道启动...")
        print()

        # 1. 德本审计
        print("📋 [1/5] 德本审计预检...")
        deben_ok, deben_msg = ExternalEngines.run_deben_audit()
        print(f"   结果: {'🟢 通过' if deben_ok else '🔴 未通过'}")
        if not deben_ok:
            print(deben_msg[:300])
            print()
            print("🔴 德本审计未通过，全流程中止。请先修复底线问题。")
            return 1
        print()

        # 2. 扫描
        print("🔍 [2/5] 扫描脚本...")
        manager.scan(pattern=args.pattern)
        total = len(manager.results)
        print(f"   完成: {total} 文件 🟢{manager._count('🟢')} 🟡{manager._count('🟡')} 🔴{manager._count('🔴')}")
        print()

        # 3. 修复
        print("🔧 [3/5] 自动修复...")
        fix_result = manager.auto_fix(dry_run=False)
        print(f"   已修复: {len(fix_result['fixed'])}")
        print(f"   失败: {len(fix_result['failed'])}")
        if fix_result['fixed']:
            for f in fix_result['fixed'][:10]:
                print(f"     ✅ {f}")
            if len(fix_result['fixed']) > 10:
                print(f"     ... 还有 {len(fix_result['fixed'])-10} 个")
        print()

        # 4. 签名报告
        print("🔐 [4/5] 生成并签名报告...")
        report_path = manager.save_report(fmt=args.report, output=args.output)
        ok, msg = ExternalEngines.sign_file(report_path)
        print(f"   报告: {report_path.name}")
        print(f"   签名: {'✅' if ok else '⚠️ ' + msg[:80]}")
        print()

        # 5. 最终审计
        print("📊 [5/5] 最终审计状态...")
        print(f"   🟢 通过: {manager._count('🟢')}/{total}")
        print(f"   🟡 待核: {manager._count('🟡')}/{total}")
        print(f"   🔴 红线: {manager._count('🔴')}/{total}")
        print()
        print(f"📄 报告: {report_path}")
        if ok:
            print(f"🔐 签名: {report_path}.asc")
        print()
        print(manager.time_stamp)

        # 全流程审计日志
        manager._write_audit_trail("full_pipeline", {
            "scan_total": total,
            "fix_fixed": len(fix_result['fixed']),
            "deben_passed": deben_ok,
            "report": str(report_path.name),
        })

        return 0 if manager._count('🔴') == 0 else 1

    # ── --watch 监视模式 ──
    if args.watch:
        manager = ScriptManager(args.dir)
        print("🔄 监视模式启动（每60秒扫描，Ctrl+C 停止）")
        try:
            while True:
                manager.scan(pattern=args.pattern)
                report = manager.generate_report(args.report)
                # 覆盖写入最近报告
                watch_path = AUDIT_DIR / "script_align_watch_report.md"
                watch_path.write_text(report, encoding='utf-8')
                print(f"\r[{datetime.now().strftime('%H:%M:%S')}] 🟢{manager._count('🟢')} 🟡{manager._count('🟡')} 🔴{manager._count('🔴')} — {watch_path.name}", end='')
                time_mod.sleep(60)
        except KeyboardInterrupt:
            print("\n⏹️ 监视停止")
        return 0

    # ── --scan（默认模式）──
    manager = ScriptManager(args.dir)
    manager.scan(pattern=args.pattern)

    if args.fix:
        print("🔧 自动修复中...")
        result = manager.auto_fix(dry_run=args.dry_run)
        if result['fixed']:
            print("\n✅ 已修复:")
            for f in result['fixed']:
                print(f"   {f}")
        if result['failed']:
            print("\n❌ 修复失败:")
            for f in result['failed']:
                print(f"   {f}")
        print()

    report = manager.generate_report(args.report)

    if args.output or args.fix:
        out_path = manager.save_report(fmt=args.report, output=args.output)
        print(f"📄 报告已保存: {out_path}")
        if args.sign:
            ok, msg = ExternalEngines.sign_file(out_path)
            print(f"🔐 签名: {'✅' if ok else '⚠️ ' + msg}")
    else:
        print(report)

    print()
    print(manager.time_stamp)

    return 0

if __name__ == "__main__":
    sys.exit(main())
