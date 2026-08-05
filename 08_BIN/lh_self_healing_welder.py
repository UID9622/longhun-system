#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 自愈焊接引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-SELF-HEALING-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  1. 执行焊接脚本（生成日志、DNA存根、错误记录）
  2. 分析日志 → 诊断错误类型 → 生成修复命令
  3. 循环修复直到成功（左右互搏）
  4. 验证DNA完整性
  5. 生成自愈报告

用法：
  lh 焊接                     # 执行一次完整焊接
  lh 焊接 --loop              # 循环模式（左右互搏）
  lh 焊接 --analyze <日志>    # 分析已有日志
  lh 焊接 --fix <错误>        # 生成特定错误的修复命令
  lh 焊接 --status            # 查看当前焊接状态
  lh 焊接 --report            # 生成自愈报告
"""

import os
import sys
import json
import re
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum

# ============================================================
# 配置
# ============================================================

PROJECT_ROOT = Path.home() / "longhun-system"
XPAY_CLI = PROJECT_ROOT / "xpay" / "src" / "cli.py"
LOG_DIR = PROJECT_ROOT / "xpay" / "logs"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

LOG_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 数据结构
# ============================================================

class ErrorType(Enum):
    """错误类型枚举"""
    MODULE_NOT_FOUND = "ModuleNotFoundError"
    IMPORT_ERROR = "ImportError"
    SYNTAX_ERROR = "SyntaxError"
    SQL_ERROR = "SQLiteError"
    DB_LOCKED = "DatabaseLocked"
    NETWORK_ERROR = "NetworkError"
    PERMISSION_ERROR = "PermissionError"
    TRANSACTION_ERROR = "TransactionError"
    DNA_ERROR = "DNACodecError"
    UNKNOWN = "UnknownError"

@dataclass
class WeldingResult:
    """焊接结果"""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    success: bool = False
    transactions: List[Dict] = field(default_factory=list)
    errors: List[Dict] = field(default_factory=list)
    dna_stubs: List[Dict] = field(default_factory=list)
    log_file: str = ""
    error_file: str = ""
    dna_file: str = ""
    repair_attempts: int = 0

@dataclass
class RepairCommand:
    """修复命令"""
    step: int
    description: str
    command: str
    reason: str
    executed: bool = False
    success: bool = False

# ============================================================
# 核心引擎
# ============================================================

class SelfHealingWelder:
    """自愈焊接引擎 - 左右互搏核心"""

    def __init__(self):
        self.result = WeldingResult()
        self.repair_commands: List[RepairCommand] = []
        self._error_patterns = self._build_error_patterns()

    def _build_error_patterns(self) -> Dict[ErrorType, List[str]]:
        """构建错误模式映射"""
        return {
            ErrorType.MODULE_NOT_FOUND: [
                r"ModuleNotFoundError: No module named '(\w+)'",
                r"ImportError: No module named '(\w+)'",
            ],
            ErrorType.IMPORT_ERROR: [
                r"ImportError: cannot import name '(\w+)'",
            ],
            ErrorType.SYNTAX_ERROR: [
                r"SyntaxError: invalid syntax",
                r"SyntaxError: (.*?) at line (\d+)",
            ],
            ErrorType.SQL_ERROR: [
                r"sqlite3\.OperationalError: (.*?)",
                r"sqlite3\.IntegrityError: (.*?)",
            ],
            ErrorType.DB_LOCKED: [
                r"database is locked",
                r"unable to open database file",
            ],
            ErrorType.NETWORK_ERROR: [
                r"ConnectionError",
                r"TimeoutError",
                r"Failed to connect",
            ],
            ErrorType.PERMISSION_ERROR: [
                r"Permission denied",
                r"Operation not permitted",
            ],
            ErrorType.TRANSACTION_ERROR: [
                r"TransactionValidationError",
                r"Amount exceeds maximum",
                r"Invalid transaction",
            ],
            ErrorType.DNA_ERROR: [
                r"DNACodecError",
                r"compression failed",
                r"DNA verification failed",
            ],
        }

    # ============================================================
    # 1. 执行焊接脚本
    # ============================================================

    def run_welding(self) -> WeldingResult:
        """执行焊接脚本 → 调用 xpay CLI pay 命令"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = LOG_DIR / f"welding_{timestamp}.log"
        error_file = LOG_DIR / f"errors_{timestamp}.log"
        dna_file = LOG_DIR / f"dna_stubs_{timestamp}.json"

        print(f"🔧 开始焊接...")
        print(f"📁 日志: {log_file}")
        print(f"📁 错误: {error_file}")
        print(f"📁 DNA: {dna_file}")

        # 构建焊接命令 → 对齐真实 xpay CLI 接口
        cmd = [
            "python3",
            str(XPAY_CLI),
            "pay",
            "100", "CNY", "UID1001",
            "--sender", "UID9622",
            "--memo", "焊接测试"
        ]

        try:
            start_time = time.time()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(PROJECT_ROOT),
            )
            duration = time.time() - start_time

            log_content = f"""
=== 焊接执行日志 ===
时间: {datetime.now().isoformat()}
命令: {' '.join(cmd)}
退出码: {result.returncode}
耗时: {duration:.2f}s
--- stdout ---
{result.stdout}
--- stderr ---
{result.stderr}
==================
"""
            log_file.write_text(log_content, encoding='utf-8')

            errors = self.parse_errors(result.stderr + result.stdout)
            error_file.write_text(json.dumps(errors, ensure_ascii=False, indent=2), encoding='utf-8')

            dna_stubs = self.generate_dna_stubs(result)
            dna_file.write_text(json.dumps(dna_stubs, ensure_ascii=False, indent=2), encoding='utf-8')

            self.result.log_file = str(log_file)
            self.result.error_file = str(error_file)
            self.result.dna_file = str(dna_file)
            self.result.success = result.returncode == 0
            self.result.errors = errors
            self.result.dna_stubs = dna_stubs

            if self.result.success:
                print(f"✅ 焊接成功！耗时 {duration:.2f}s")
            else:
                print(f"❌ 焊接失败，发现 {len(errors)} 个错误")

            return self.result

        except subprocess.TimeoutExpired:
            print(f"⏰ 焊接超时 (30s)")
            self.result.success = False
            self.result.errors.append({"type": "TimeoutExpired", "message": "焊接超时"})
            return self.result
        except Exception as e:
            print(f"❌ 焊接异常: {e}")
            self.result.success = False
            self.result.errors.append({"type": "Exception", "message": str(e)})
            return self.result

    # ============================================================
    # 2. 日志分析器
    # ============================================================

    def parse_errors(self, text: str) -> List[Dict]:
        """解析日志中的错误"""
        errors = []
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue

            for error_type, patterns in self._error_patterns.items():
                for pattern in patterns:
                    match = re.search(pattern, line)
                    if match:
                        errors.append({
                            "type": error_type.value,
                            "message": line,
                            "matched": match.groups() if match.groups() else line,
                            "raw": line
                        })
                        break
                else:
                    continue
                break
            else:
                if any(kw in line.lower() for kw in ["error", "exception", "fail"]):
                    errors.append({
                        "type": ErrorType.UNKNOWN.value,
                        "message": line,
                        "matched": None,
                        "raw": line
                    })

        return errors

    def diagnose(self, errors: List[Dict]) -> List[RepairCommand]:
        """根据错误生成修复命令"""
        commands = []
        step = 1

        for error in errors:
            error_type = error.get("type", "")
            message = error.get("message", "")

            if error_type == ErrorType.MODULE_NOT_FOUND.value:
                module = error.get("matched", [""])[0] if isinstance(error.get("matched"), tuple) else ""
                commands.append(RepairCommand(
                    step=step,
                    description=f"安装缺失模块: {module}",
                    command=f"pip install {module}" if module else "pip install -r requirements.txt",
                    reason=f"模块 '{module}' 未安装"
                ))
                step += 1

            elif error_type == ErrorType.IMPORT_ERROR.value:
                name = error.get("matched", [""])[0] if isinstance(error.get("matched"), tuple) else ""
                commands.append(RepairCommand(
                    step=step,
                    description=f"修复导入错误: {name}",
                    command=f"python3 -c 'import {name}'",
                    reason=f"无法导入 '{name}'"
                ))
                step += 1

            elif error_type == ErrorType.SYNTAX_ERROR.value:
                commands.append(RepairCommand(
                    step=step,
                    description="检查Python版本兼容性",
                    command="python3 --version",
                    reason="语法错误，可能Python版本不兼容"
                ))
                step += 1

            elif error_type in (ErrorType.SQL_ERROR.value, ErrorType.DB_LOCKED.value):
                db_path = PROJECT_ROOT / "xpay" / "data" / "xpay.db"
                commands.append(RepairCommand(
                    step=step,
                    description="初始化数据库",
                    command=f"python3 -c \"import sqlite3; sqlite3.connect('{db_path}').close(); print('OK')\"",
                    reason="数据库未初始化或被锁定"
                ))
                step += 1

            elif error_type == ErrorType.PERMISSION_ERROR.value:
                commands.append(RepairCommand(
                    step=step,
                    description="修复文件权限",
                    command=f"chmod -R 755 {PROJECT_ROOT}/xpay",
                    reason="权限不足"
                ))
                step += 1

            elif error_type == ErrorType.TRANSACTION_ERROR.value:
                commands.append(RepairCommand(
                    step=step,
                    description="检查交易参数",
                    command=f"python3 {XPAY_CLI} pay 100 CNY UID1001 --sender UID9622 --memo '修复测试'",
                    reason="交易参数无效或超限"
                ))
                step += 1

            elif error_type == ErrorType.DNA_ERROR.value:
                commands.append(RepairCommand(
                    step=step,
                    description="重新生成DNA",
                    command=f"python3 {XPAY_CLI} stats",
                    reason="DNA签名生成失败"
                ))
                step += 1

            else:
                commands.append(RepairCommand(
                    step=step,
                    description="通用修复: 重新初始化支付网关",
                    command=f"python3 -c \"from xpay.src.core import SovereignGateway; g = SovereignGateway(); print('OK')\"",
                    reason=f"未知错误: {message[:50]}..."
                ))
                step += 1

        return commands

    # ============================================================
    # 3. DNA 存根生成器
    # ============================================================

    def generate_dna_stubs(self, result: subprocess.CompletedProcess) -> List[Dict]:
        """生成DNA存根"""
        stubs = []
        dna_pattern = r'#(?:龍芯|龍芯)⚡️[^\s]+'
        matches = re.findall(dna_pattern, result.stdout + result.stderr)

        for dna in matches:
            stubs.append({
                "dna": dna,
                "timestamp": datetime.now().isoformat(),
                "source": "stdout" if dna in result.stdout else "stderr"
            })

        if not stubs:
            stubs.append({
                "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-焊接存根-UID9622",
                "timestamp": datetime.now().isoformat(),
                "source": "generated"
            })

        return stubs

    # ============================================================
    # 4. 修复执行器（左右互搏核心循环）
    # ============================================================

    def heal(self, max_attempts: int = 10) -> Dict:
        """左右互搏自愈循环"""
        print(f"\n🐉 开始自愈循环 (最多 {max_attempts} 轮)")
        print("=" * 50)

        attempts = 0
        all_commands = []

        while attempts < max_attempts:
            attempts += 1
            print(f"\n🔄 第 {attempts} 轮")

            result = self.run_welding()
            self.result.repair_attempts = attempts

            if result.success:
                print(f"\n✅ 自愈成功！共 {attempts} 轮")
                break

            errors = self.parse_errors(
                (Path(result.log_file).read_text(encoding='utf-8') if Path(result.log_file).exists() else "")
            )
            commands = self.diagnose(errors)

            if not commands:
                print("⚠️ 未生成修复命令，尝试重新执行")
                continue

            print(f"\n📋 生成 {len(commands)} 条修复命令:")
            for cmd in commands:
                print(f"  {cmd.step}. {cmd.description}")
                print(f"    命令: {cmd.command}")
                print(f"    原因: {cmd.reason}")

            for cmd in commands:
                print(f"\n🔧 执行修复 #{cmd.step}: {cmd.description}")
                try:
                    repair_result = subprocess.run(
                        cmd.command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30,
                        cwd=str(PROJECT_ROOT)
                    )
                    cmd.executed = True
                    cmd.success = repair_result.returncode == 0

                    if cmd.success:
                        print(f"  ✅ 修复成功")
                    else:
                        print(f"  ❌ 修复失败: {repair_result.stderr[:200]}")
                except Exception as e:
                    print(f"  ❌ 修复异常: {e}")

            all_commands.extend(commands)
            time.sleep(1)

        final_status = {
            "attempts": attempts,
            "success": self.result.success,
            "commands_executed": len([c for c in all_commands if c.executed]),
            "commands_successful": len([c for c in all_commands if c.success]),
            "result": asdict(self.result)
        }

        return final_status

    # ============================================================
    # 5. 报告生成器
    # ============================================================

    def generate_report(self, status: Dict) -> str:
        """生成自愈报告"""
        lines = []
        lines.append("=" * 60)
        lines.append("🐉 龍魂 · 自愈焊接报告")
        lines.append("=" * 60)
        lines.append(f"时间: {datetime.now().isoformat()}")
        lines.append(f"DNA: #龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-WELD-UID9622")
        lines.append(f"确认码: {CONFIRM_CODE}")
        lines.append("-" * 60)
        lines.append(f"焊接状态: {'✅ 成功' if status['success'] else '❌ 失败'}")
        lines.append(f"尝试轮次: {status['attempts']}")
        lines.append(f"修复命令: {status['commands_executed']} 执行, {status['commands_successful']} 成功")
        lines.append("-" * 60)

        if status['result']['errors']:
            lines.append("\n📋 错误详情:")
            for error in status['result']['errors'][:5]:
                lines.append(f"  • {error['type']}: {error['message'][:80]}...")

        if status['result']['dna_stubs']:
            lines.append("\n🧬 DNA存根:")
            for stub in status['result']['dna_stubs'][:3]:
                lines.append(f"  • {stub['dna']}")

        lines.append("-" * 60)
        lines.append(f"日志文件: {status['result']['log_file']}")
        lines.append(f"错误文件: {status['result']['error_file']}")
        lines.append(f"DNA文件: {status['result']['dna_file']}")
        lines.append("=" * 60)

        return "\n".join(lines)

    def export_report(self, status: Dict, path: Optional[Path] = None) -> str:
        """导出报告为JSON"""
        if path is None:
            path = LOG_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        report = {
            "timestamp": datetime.now().isoformat(),
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-WELD-UID9622",
            "status": status,
            "version": "1.0",
            "confirm": CONFIRM_CODE
        }

        path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        return str(path)

# ============================================================
# 命令行入口
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 自愈焊接引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh 焊接                      # 执行一次完整焊接
  lh 焊接 --loop               # 循环模式（左右互搏）
  lh 焊接 --analyze <日志>     # 分析已有日志
  lh 焊接 --status             # 查看当前焊接状态
  lh 焊接 --report             # 生成自愈报告
        """
    )

    parser.add_argument("--loop", "-l", action="store_true", help="循环修复模式（左右互搏）")
    parser.add_argument("--analyze", "-a", type=str, help="分析已有日志文件")
    parser.add_argument("--status", "-s", action="store_true", help="查看当前状态")
    parser.add_argument("--report", "-r", action="store_true", help="生成报告")
    parser.add_argument("--max-attempts", type=int, default=10, help="最大修复轮次（默认10）")
    parser.add_argument("--json", "-j", action="store_true", help="以JSON格式输出")

    args = parser.parse_args()

    welder = SelfHealingWelder()

    if args.analyze:
        print(f"📋 分析日志: {args.analyze}")
        path = Path(args.analyze)
        if path.exists():
            content = path.read_text(encoding='utf-8')
            errors = welder.parse_errors(content)
            commands = welder.diagnose(errors)
            print(f"发现 {len(errors)} 个错误")
            print(f"生成 {len(commands)} 条修复命令")
            if args.json:
                print(json.dumps({
                    "errors": errors,
                    "commands": [asdict(c) for c in commands]
                }, ensure_ascii=False, indent=2))
            else:
                for cmd in commands:
                    print(f"  [{cmd.step}] {cmd.description}")
                    print(f"    > {cmd.command}")
        else:
            print(f"❌ 日志文件不存在: {args.analyze}")
        return

    if args.status:
        print("📊 当前焊接状态")
        print(f"  最后焊接: {welder.result.timestamp}")
        print(f"  成功: {welder.result.success}")
        print(f"  错误数: {len(welder.result.errors)}")
        print(f"  修复尝试: {welder.result.repair_attempts}")
        return

    if args.loop:
        status = welder.heal(max_attempts=args.max_attempts)
        if args.json:
            print(json.dumps(status, ensure_ascii=False, indent=2))
        else:
            print(welder.generate_report(status))
        return

    if args.report:
        status = {
            "attempts": welder.result.repair_attempts,
            "success": welder.result.success,
            "commands_executed": 0,
            "commands_successful": 0,
            "result": asdict(welder.result)
        }
        if args.json:
            print(json.dumps(status, ensure_ascii=False, indent=2))
        else:
            print(welder.generate_report(status))
        return

    # 默认：执行一次焊接
    result = welder.run_welding()
    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print(f"\n{'✅' if result.success else '❌'} 焊接完成")
        print(f"  日志: {result.log_file}")
        print(f"  错误: {len(result.errors)}")
        print(f"  DNA存根: {len(result.dna_stubs)}")

if __name__ == "__main__":
    main()
