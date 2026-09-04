#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
================================================================================
⚡ 龍魂系統·全自動機槍 v2.0
================================================================================
名稱: lh_auto_cannon.py
定位: 一键扫描·修复·报告 — 全系统健康自检+自动修复
DNA: #龍芯⚡️丙午·丙申·丙辰·巳时·䷄需-AUTO-CANNON-v2.0
協議: 君子協議 + 絕對防禦憲法 v1.0

來源: 從 Kimi Agent-2 "全自动机枪" 對齊至龍魂系統本地
      適配系統實際目錄結構，掃描真實的技能/協議/數據層

功能:
  1. 系统全量扫描（技能/协议/数据/服务/依赖/DNA）
  2. DNA对齐检查
  3. 六维度健康评估
  4. 自动修复缺失项
  5. 一键启动守护进程
  6. 生成完整报告

用法:
  python3 bin/lh_auto_cannon.py            # 全自动模式
  python3 bin/lh_auto_cannon.py --scan     # 仅扫描
  python3 bin/lh_auto_cannon.py --fix      # 扫描+修复
  python3 bin/lh_auto_cannon.py --report   # 仅生成报告
  python3 bin/lh_auto_cannon.py --health   # 仅健康评估

效果: 双击一下，去抽根烟，回来全搞定。
================================================================================
"""

import os
import sys
import json
import time
import hashlib
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum

# ==============================================================================
# 🌌 龍魂核心配置（對齊真實系統目錄結構）
# ==============================================================================

VERSION = "2.0.0"
DNA = "#龍芯⚡️丙午·丙申·丙辰·巳时·䷄需-AUTO-CANNON-v2.0"
UID = "UID9622"

# 系統根目錄
SYSTEM_ROOT = Path(__file__).resolve().parent.parent

# 掃描目標目錄
SCAN_DIRS = {
    "protocols": SYSTEM_ROOT / "01_protocols",
    "skills": SYSTEM_ROOT / "01_技能庫",
    "data_layer": SYSTEM_ROOT / "L7_数据层",
    "service_layer": SYSTEM_ROOT / "L5_服务层",
    "governance": SYSTEM_ROOT / "L8_治理层",
    "kernel": SYSTEM_ROOT / "L1_内核层",
    "bin": SYSTEM_ROOT / "bin",
    "config": SYSTEM_ROOT / "config",
    "models": SYSTEM_ROOT / "models",
    "train": SYSTEM_ROOT / "train",
    "integrations": SYSTEM_ROOT / "integrations",
    "backend": SYSTEM_ROOT / "backend",
    "web": SYSTEM_ROOT / "web",
    "portal": SYSTEM_ROOT / "portal",
}

# 必須存在的核心文件
REQUIRED_FILES = [
    "AGENTS.md",
    "CONSTITUTION.md.asc",
    "P0_ETERNAL_LOCK.md.asc",
    "STANDARD.md.asc",
    "web_server.py",
    "backend/main.py",
    "backend/config.py",
    "backend/routes.py",
    "requirements.txt",
    "docker-compose.yml",
    "pyproject.toml",
    ".env.example",
]

# 必須存在的目錄
REQUIRED_DIRS = [
    "01_protocols",
    "01_技能庫",
    "bin",
    "backend",
    "config",
    "web",
    "portal",
    "train",
    "models",
    "integrations",
    "L7_数据层",
]

# 必須存在的技能腳本
REQUIRED_BIN_SCRIPTS = [
    "bin/lh_memory_load.py",
    "bin/lh_anti_tamper.py",
    "bin/lh_persona_orchestrator.py",
    "bin/lh_auto_cannon.py",
    "bin/lh_self-heal.py",
    "bin/lh_auto_sync.py",
    "bin/lh_cnsh_gatekeeper.py",
]

OUTPUT_DIR = SYSTEM_ROOT / "reports"
LOG_DIR = SYSTEM_ROOT / "logs"


class StatusCode(Enum):
    OK = 0
    WARNING = 1
    FAILED = 2
    SKIPPED = 3


@dataclass
class CheckResult:
    name: str
    status: StatusCode
    message: str = ""
    dna_tag: str = ""
    version: str = ""
    elapsed: float = 0.0
    fix_action: str = ""


# ==============================================================================
# 🎨 终端彩色输出
# ==============================================================================

class Color:
    GOLD = "\033[38;5;220m"
    RED = "\033[38;5;196m"
    GREEN = "\033[38;5;82m"
    BLUE = "\033[38;5;81m"
    PURPLE = "\033[38;5;141m"
    GRAY = "\033[38;5;240m"
    BOLD = "\033[1m"
    BLINK = "\033[5m"
    RESET = "\033[0m"


def log_print(level: str, msg: str):
    color_map = {
        "INFO": Color.BLUE,
        "OK": Color.GREEN,
        "WARN": Color.GOLD,
        "ERROR": Color.RED,
        "DNA": Color.PURPLE,
        "TITLE": Color.GOLD + Color.BOLD,
        "DONE": Color.GREEN + Color.BOLD,
    }
    c = color_map.get(level, Color.GRAY)
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"{Color.GRAY}[{ts}]{Color.RESET} {c}{msg}{Color.RESET}")


# ==============================================================================
# 🐉 核心引擎
# ==============================================================================

class AutoCannon:
    """龍魂系统全自动扫描修复引擎 v2.0"""

    def __init__(self):
        self.results: List[CheckResult] = []
        self.start_time = time.time()
        self.fix_count = 0
        self._init_dirs()

    def _init_dirs(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        LOG_DIR.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------------------------
    # 阶段一: 系统全量扫描
    # --------------------------------------------------------------------------

    def phase1_scan(self) -> List[CheckResult]:
        log_print("TITLE", "🐉 ========== 阶段一: 系统全量扫描 ==========")

        # 1.1 扫描核心目录
        for dir_name, dir_path in SCAN_DIRS.items():
            t0 = time.time()
            if dir_path.exists():
                file_count = len(list(dir_path.rglob("*")))
                self.results.append(CheckResult(
                    name=f"目录/{dir_name}",
                    status=StatusCode.OK,
                    message=f"存在 ({file_count} 文件)",
                    elapsed=time.time() - t0,
                ))
                log_print("OK", f"✅ 目录/{dir_name} | {file_count} 文件")
            else:
                self.results.append(CheckResult(
                    name=f"目录/{dir_name}",
                    status=StatusCode.FAILED,
                    message="目录不存在",
                    elapsed=time.time() - t0,
                ))
                log_print("ERROR", f"❌ 目录/{dir_name} | 不存在!")

        # 1.2 扫描核心文件
        for file_path in REQUIRED_FILES:
            t0 = time.time()
            full_path = SYSTEM_ROOT / file_path
            if full_path.exists():
                self.results.append(CheckResult(
                    name=f"文件/{file_path}",
                    status=StatusCode.OK,
                    message=f"存在 ({full_path.stat().st_size} 字节)",
                    elapsed=time.time() - t0,
                ))
                log_print("OK", f"✅ 文件/{file_path}")
            else:
                self.results.append(CheckResult(
                    name=f"文件/{file_path}",
                    status=StatusCode.FAILED,
                    message="文件缺失",
                    elapsed=time.time() - t0,
                ))
                log_print("ERROR", f"❌ 文件/{file_path} | 缺失!")

        # 1.3 扫描关键脚本
        for script_path in REQUIRED_BIN_SCRIPTS:
            t0 = time.time()
            full_path = SYSTEM_ROOT / script_path
            if full_path.exists():
                self.results.append(CheckResult(
                    name=f"脚本/{script_path}",
                    status=StatusCode.OK,
                    message=f"存在 ({full_path.stat().st_size} 字节)",
                    elapsed=time.time() - t0,
                ))
                log_print("OK", f"✅ 脚本/{script_path}")
            else:
                self.results.append(CheckResult(
                    name=f"脚本/{script_path}",
                    status=StatusCode.FAILED,
                    message="脚本缺失",
                    elapsed=time.time() - t0,
                ))
                log_print("ERROR", f"❌ 脚本/{script_path} | 缺失!")

        # 1.4 扫描 Python 依赖
        self._scan_dependencies()

        # 1.5 扫描模型文件
        self._scan_models()

        # 1.6 扫描服务运行状态
        self._scan_services()

        return self.results

    def _scan_dependencies(self):
        """检查核心Python依赖是否可导入"""
        t0 = time.time()
        core_deps = [
            ("fastapi", "Web框架"),
            ("uvicorn", "ASGI服务器"),
            ("torch", "深度学习框架"),
            ("aiohttp", "异步HTTP"),
            ("jinja2", "模板引擎"),
            ("jwt", "JWT认证"),
            ("requests", "HTTP客户端"),
            ("websockets", "WebSocket"),
            ("aiofiles", "异步文件"),
            ("cryptography", "加密库"),
            ("yaml", "YAML解析"),
        ]

        for module_name, description in core_deps:
            try:
                __import__(module_name)
                self.results.append(CheckResult(
                    name=f"依赖/{module_name}",
                    status=StatusCode.OK,
                    message=f"{description} - 已安装",
                    elapsed=0,
                ))
            except ImportError:
                self.results.append(CheckResult(
                    name=f"依赖/{module_name}",
                    status=StatusCode.WARNING,
                    message=f"{description} - 未安装",
                    elapsed=0,
                ))

        elapsed = time.time() - t0
        log_print("INFO", f"📦 依赖扫描完成 ({elapsed:.1f}s)")

    def _scan_models(self):
        """检查模型文件状态"""
        t0 = time.time()
        model_dir = SYSTEM_ROOT / "models"
        if model_dir.exists():
            safetensors = list(model_dir.rglob("*.safetensors"))
            pt_files = list(model_dir.rglob("*.pt"))
            total_size = sum(f.stat().st_size for f in safetensors + pt_files)
            self.results.append(CheckResult(
                name="模型/权重文件",
                status=StatusCode.OK,
                message=f"{len(safetensors)} safetensors + {len(pt_files)} pt ({total_size / 1024**3:.1f} GB)",
                elapsed=time.time() - t0,
            ))
            log_print("OK", f"✅ 模型文件 | {total_size / 1024**3:.1f} GB")
        else:
            self.results.append(CheckResult(
                name="模型/权重文件",
                status=StatusCode.WARNING,
                message="models/ 目录不存在",
                elapsed=time.time() - t0,
            ))
            log_print("WARN", "⚠️ 模型目录不存在")

    def _scan_services(self):
        """检查服务运行状态"""
        t0 = time.time()
        services = [
            (9622, "API后端 (FastAPI)"),
            (8777, "Web门户"),
        ]
        for port, desc in services:
            try:
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('127.0.0.1', port))
                sock.close()
                if result == 0:
                    self.results.append(CheckResult(
                        name=f"服务/{desc}",
                        status=StatusCode.OK,
                        message=f"端口 {port} 运行中",
                        elapsed=0,
                    ))
                    log_print("OK", f"✅ 服务/{desc} | :{port} 🟢")
                else:
                    self.results.append(CheckResult(
                        name=f"服务/{desc}",
                        status=StatusCode.WARNING,
                        message=f"端口 {port} 未响应",
                        elapsed=0,
                    ))
                    log_print("WARN", f"⚠️ 服务/{desc} | :{port} 🔴")
            except Exception:
                pass

    # --------------------------------------------------------------------------
    # 阶段二: DNA对齐检查
    # --------------------------------------------------------------------------

    def phase2_dna_align(self) -> float:
        log_print("TITLE", "🧬 ========== 阶段二: DNA对齐检查 ==========")

        # 扫描所有 .py 和 .md 文件中的 DNA 标记
        dna_files = []
        no_dna_files = []
        scan_extensions = [".py", ".md", ".json"]

        for root, dirs, files in os.walk(SYSTEM_ROOT):
            # 排除不需要扫描的目录
            dirs[:] = [d for d in dirs if d not in [
                "__pycache__", ".git", "node_modules", "venv", ".venv",
                "venv_longhun_math", "backups", "tmp", "logs", "dist",
                ".codebuddy",
            ]]
            for file in files:
                if any(file.endswith(ext) for ext in scan_extensions):
                    filepath = Path(root) / file
                    try:
                        content = filepath.read_text(encoding="utf-8", errors="ignore")
                        if "龍芯" in content and "⚡" in content:
                            dna_files.append(str(filepath.relative_to(SYSTEM_ROOT)))
                        elif filepath.suffix in [".py", ".md"]:
                            no_dna_files.append(str(filepath.relative_to(SYSTEM_ROOT)))
                    except Exception:
                        pass

        total = len(dna_files) + len(no_dna_files)
        align_rate = len(dna_files) / max(total, 1) * 100

        log_print("INFO", f"有DNA标记: {len(dna_files)} / 无DNA标记: {len(no_dna_files)}")
        log_print("INFO", f"📊 DNA对齐率: {align_rate:.1f}%")

        self.results.append(CheckResult(
            name="DNA对齐",
            status=StatusCode.OK if align_rate > 60 else StatusCode.WARNING,
            message=f"对齐率 {align_rate:.1f}% ({len(dna_files)}/{total})",
            elapsed=0,
        ))

        return align_rate

    # --------------------------------------------------------------------------
    # 阶段三: 六维度健康评估
    # --------------------------------------------------------------------------

    def phase3_health(self) -> Dict[str, Any]:
        log_print("TITLE", "🏥 ========== 阶段三: 六维度健康评估 ==========")

        ok_count = sum(1 for r in self.results if r.status == StatusCode.OK)
        warn_count = sum(1 for r in self.results if r.status == StatusCode.WARNING)
        failed_count = sum(1 for r in self.results if r.status == StatusCode.FAILED)
        total = max(ok_count + warn_count + failed_count, 1)

        # 六维度评分（0-10）
        dna_item = [r for r in self.results if r.name == "DNA对齐"]
        dna_score = 10 if not dna_item else (10 if dna_item[0].status == StatusCode.OK else (6 if dna_item[0].status == StatusCode.WARNING else 3))

        dimensions = {
            "目录完整性": ok_count / total * 10,
            "文件可用性": ok_count / total * 10,
            "DNA对齐度": dna_score,
            "依赖完整性": sum(1 for r in self.results if r.name.startswith("依赖/") and r.status == StatusCode.OK) / max(sum(1 for r in self.results if r.name.startswith("依赖/")), 1) * 10,
            "服务可用性": sum(1 for r in self.results if r.name.startswith("服务/") and r.status == StatusCode.OK) / max(sum(1 for r in self.results if r.name.startswith("服务/")), 1) * 10,
            "模型就绪": sum(1 for r in self.results if r.name.startswith("模型/") and r.status == StatusCode.OK) / max(sum(1 for r in self.results if r.name.startswith("模型/")), 1) * 10,
        }

        total_score = sum(dimensions.values()) / max(len(dimensions), 1)

        for name, score in dimensions.items():
            color = Color.GREEN if score >= 8 else Color.GOLD if score >= 6 else Color.RED
            log_print("INFO", f"  {name}: {color}{score:.1f}/10{Color.RESET}")

        rating = "🟢 生产级" if total_score >= 8 else "🟡 需改进" if total_score >= 6 else "🔴 不推荐"
        log_print("DONE", f"🏆 综合评分: {total_score:.1f}/10 | {rating}")

        return {
            "dimensions": dimensions,
            "total_score": total_score,
            "rating": rating,
            "ok": ok_count,
            "warning": warn_count,
            "failed": failed_count,
        }

    # --------------------------------------------------------------------------
    # 阶段四: 自动修复
    # --------------------------------------------------------------------------

    def phase4_fix(self, enable_fix: bool = True):
        log_print("TITLE", "🔧 ========== 阶段四: 自动修复 ==========")

        pending = [r for r in self.results if r.status == StatusCode.FAILED]

        if not pending:
            log_print("OK", "✅ 无需修复，所有项目正常!")
            return

        log_print("WARN", f"⚠️ 发现 {len(pending)} 个待修复项")

        if not enable_fix:
            log_print("INFO", "ℹ️ 修复模式未启用，仅列出问题:")
            for r in pending:
                log_print("WARN", f"  - {r.name}: {r.message}")
            return

        for r in pending:
            log_print("INFO", f"🔧 修复中: {r.name}...")
            fix_result = self._fix_item(r)
            if fix_result:
                if fix_result.startswith("创建占位"):
                    # 占位 ≠ 修复：标 WARNING，不冒充 ✅（防假启动/误导巡检）
                    r.status = StatusCode.WARNING
                    r.message = "已生成占位，待补充实现"
                    r.fix_action = fix_result
                    log_print("WARN", f"⚠️ {r.name} 仅占位修复，需手动补充")
                else:
                    r.status = StatusCode.OK
                    r.message = "已自动修复"
                    r.fix_action = fix_result
                    self.fix_count += 1
                    log_print("OK", f"✅ {r.name} 修复完成")
            else:
                log_print("ERROR", f"❌ {r.name} 修复失败，需手动处理")

        log_print("DONE", f"🔧 修复完成: {self.fix_count}/{len(pending)} 项成功")

    def _fix_item(self, item: CheckResult) -> Optional[str]:
        """修复单个项目"""
        try:
            if item.name.startswith("目录/"):
                dir_name = item.name.split("/")[-1]
                if dir_name in SCAN_DIRS:
                    SCAN_DIRS[dir_name].mkdir(parents=True, exist_ok=True)
                    return f"创建目录 {SCAN_DIRS[dir_name]}"

            elif item.name.startswith("文件/"):
                file_path = item.name.split("/", 1)[-1]
                full_path = SYSTEM_ROOT / file_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                # 创建占位文件
                placeholder = f"""# 龍魂系统 · 自动生成占位文件
# DNA: #龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{file_path.replace('/', '-')}-AUTO-v1.0
# 修复工具: lh_auto_cannon.py v{VERSION}
# 修复时间: {datetime.now().isoformat()}
#
# TODO: 需要补充实际内容
"""
                full_path.write_text(placeholder, encoding="utf-8")
                return f"创建占位文件 {file_path}"

            elif item.name.startswith("脚本/"):
                script_path = item.name.split("/", 1)[-1]
                full_path = SYSTEM_ROOT / script_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                placeholder = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍魂系统 · 自动生成占位脚本
# DNA: #龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{script_path.replace('/', '-')}-AUTO-v1.0
# 修复工具: lh_auto_cannon.py v{VERSION}
print("TODO: 实现 {script_path}")
"""
                full_path.write_text(placeholder, encoding="utf-8")
                full_path.chmod(0o755)
                return f"创建占位脚本 {script_path}"

            return None
        except Exception as e:
            return None

    # --------------------------------------------------------------------------
    # 阶段五: 守护进程 + 服务检查
    # --------------------------------------------------------------------------

    def phase5_daemon(self):
        log_print("TITLE", "🚀 ========== 阶段五: 守护进程 & 服务状态 ==========")

        # 检查并报告各服务状态
        service_scripts = [
            ("bin/start_all.sh", "一键启动脚本"),
            ("deploy/longhun-api-ctl.sh", "API控制脚本"),
            ("deploy/longhun-api.service", "systemd服务配置"),
            ("launchd/com.longhun.*.plist", "launchd配置"),
        ]

        for script_path, desc in service_scripts:
            full_path = SYSTEM_ROOT / script_path
            if "*" in script_path:
                parent = full_path.parent
                if parent.exists():
                    matches = list(parent.glob(full_path.name))
                    if matches:
                        log_print("OK", f"✅ {desc} | {len(matches)} 个配置")
                    else:
                        log_print("WARN", f"⚠️ {desc} | 无匹配")
            elif full_path.exists():
                log_print("OK", f"✅ {desc} | 存在")
            else:
                log_print("WARN", f"⚠️ {desc} | 未找到")

        # 尝试重启服务
        web_server = SYSTEM_ROOT / "web_server.py"
        api_server = SYSTEM_ROOT / "backend" / "main.py"

        if web_server.exists():
            log_print("INFO", f"📌 Web服务入口: {web_server}")
        if api_server.exists():
            log_print("INFO", f"📌 API服务入口: {api_server}")

    # --------------------------------------------------------------------------
    # 阶段六: 报告生成
    # --------------------------------------------------------------------------

    def phase6_report(self, health: Dict[str, Any]) -> Tuple[str, str]:
        log_print("TITLE", "📊 ========== 阶段六: 报告生成 ==========")

        report_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        total_elapsed = time.time() - self.start_time

        # JSON报告
        json_report = {
            "DNA": DNA,
            "UID": UID,
            "version": VERSION,
            "exec_time": datetime.now().isoformat(),
            "total_elapsed_sec": round(total_elapsed, 2),
            "health": health,
            "fix_stats": {"fixed": self.fix_count},
            "details": [asdict(r) for r in self.results],
        }

        json_path = OUTPUT_DIR / f"CANNON_REPORT_{report_time}.json"
        json_path.write_text(
            json.dumps(json_report, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8"
        )

        # Markdown报告
        md_path = OUTPUT_DIR / f"CANNON_REPORT_{report_time}.md"
        self._gen_md_report(md_path, health, total_elapsed)

        log_print("OK", f"✅ JSON报告: {json_path}")
        log_print("OK", f"✅ MD报告: {md_path}")

        return str(json_path), str(md_path)

    def _gen_md_report(self, path: Path, health: Dict, elapsed: float):
        ok_count = sum(1 for r in self.results if r.status == StatusCode.OK)
        failed_count = sum(1 for r in self.results if r.status == StatusCode.FAILED)
        warn_count = sum(1 for r in self.results if r.status == StatusCode.WARNING)

        md = f"""# ⚡ 龍魂系統·全自動機槍 執行報告 v{VERSION}

**DNA**: `{DNA}`
**執行時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**總耗時**: {elapsed:.1f}秒
**執行人**: {UID}

---

## 📊 執行摘要

| 指標 | 數值 |
|------|------|
| 檢查總數 | {len(self.results)} |
| 檢查通過 | {ok_count} ✅ |
| 警告 | {warn_count} ⚠️ |
| 檢查失敗 | {failed_count} ❌ |
| 自動修復 | {self.fix_count} 🔧 |
| 綜合評分 | {health['total_score']:.1f}/10 |
| 健康評級 | {health['rating']} |

## 🏥 六維度健康評估

| 維度 | 評分 | 狀態 |
|------|------|------|
"""
        for name, score in health['dimensions'].items():
            mark = "🟢" if score >= 8 else "🟡" if score >= 6 else "🔴"
            md += f"| {name} | {score:.1f}/10 | {mark} |\n"

        md += "\n## 📋 檢查詳情\n\n| # | 項目名稱 | 狀態 | 說明 | 耗時 |\n|---|----------|------|------|------|\n"

        for i, r in enumerate(self.results, 1):
            status_mark = "✅" if r.status == StatusCode.OK else "❌" if r.status == StatusCode.FAILED else "⚠️"
            md += f"| {i} | `{r.name}` | {status_mark} | {r.message} | {r.elapsed:.2f}s |\n"

        md += f"\n---\n*報告由龍魂全自動機槍 v{VERSION} 生成 · DNA: {DNA}*\n"

        path.write_text(md, encoding="utf-8")

    # --------------------------------------------------------------------------
    # 主控流程
    # --------------------------------------------------------------------------

    def full_auto_fire(self, enable_fix: bool = True, enable_daemon: bool = False) -> float:
        """全自动执行全部六阶段"""
        log_print("TITLE", "╔══════════════════════════════════════════════════════════════╗")
        log_print("TITLE", f"║     ⚡ 龍魂系統·全自動機槍 v{VERSION} 開火!           ║")
        log_print("TITLE", f"║     {DNA[:48]}           ║")
        log_print("TITLE", "╚══════════════════════════════════════════════════════════════╝")
        log_print("INFO", "🎯 目标: 系统全量扫描 · 六维度评估 · 自动修复 · 一键搞定")
        log_print("INFO", "💡 提示: 现在可以去抽根烟，回来全搞定\n")

        # 六阶段流水线
        self.phase1_scan()
        self.phase2_dna_align()
        health = self.phase3_health()
        self.phase4_fix(enable_fix)

        if enable_daemon:
            self.phase5_daemon()

        json_path, md_path = self.phase6_report(health)

        # 最终摘要
        total_elapsed = time.time() - self.start_time
        ok_count = sum(1 for r in self.results if r.status == StatusCode.OK)
        total = len(self.results)

        print()
        log_print("DONE", "╔══════════════════════════════════════════════════════════════╗")
        log_print("DONE", f"║  ✅ 全自動機槍執行完成! 耗時: {total_elapsed:.1f}秒           ║")
        log_print("DONE", f"║  📊 通過: {ok_count}/{total} | 修復: {self.fix_count} | 評分: {health['total_score']:.1f}/10    ║")
        log_print("DONE", f"║  📁 報告: {md_path.split('/')[-1]}                  ║")
        log_print("DONE", "╚══════════════════════════════════════════════════════════════╝")

        return health['total_score']


# ==============================================================================
# 🚀 入口
# ==============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="龍魂系統·全自動機槍 v2.0")
    parser.add_argument("--scan", action="store_true", help="仅扫描")
    parser.add_argument("--fix", action="store_true", help="扫描+修复")
    parser.add_argument("--report", action="store_true", help="仅生成报告")
    parser.add_argument("--health", action="store_true", help="仅健康评估")
    parser.add_argument("--daemon", action="store_true", help="启动守护进程检查")
    parser.add_argument("--no-fix", action="store_true", help="不执行修复")
    parser.add_argument("--version", action="store_true", help="显示版本")

    args = parser.parse_args()

    if args.version:
        print(f"lh_auto_cannon.py v{VERSION}")
        print(f"DNA: {DNA}")
        print(f"系统路径: {SYSTEM_ROOT}")
        sys.exit(0)

    cannon = AutoCannon()

    if args.health:
        cannon.phase1_scan()
        health = cannon.phase3_health()
        cannon.phase6_report(health)
    elif args.scan:
        cannon.phase1_scan()
        cannon.phase2_dna_align()
    elif args.report:
        cannon.phase1_scan()
        health = cannon.phase3_health()
        cannon.phase6_report(health)
    else:
        # 全自动模式 (默认)
        cannon.full_auto_fire(
            enable_fix=not args.no_fix,
            enable_daemon=args.daemon,
        )
