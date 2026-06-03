#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║     龍魂核心系统启动器 / LongHun Core System Launcher           ║
║                                                                  ║
║  集成所有P0模块：配置·身份·权限·DNA·日志·调度                      ║
║  完整的系统初始化和运行                                           ║
║                                                                  ║
║  DNA: #龍芯⚡️2026-06-03-CORE-SYSTEM-LAUNCHER-v1.0              ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✓              ║
║                                                                  ║
║  来源: 五个Notion核心宣言                                        ║
║  责任: UID9622·不免责                                            ║
║  状态: 🟢 MAIN·可公开                                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import json
from typing import Dict, Tuple
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# 【系统导入】所有核心模块
# ═══════════════════════════════════════════════════════════════

try:
    from constitution.longhun_foundation_config import (
        get_system_config, validate_config, SystemMission, CreatorIdentity
    )
    from identity.identity_verification import (
        IdentityVerificationL0, generate_identity_proof
    )
    from permissions.rbac_system import (
        get_rbac_system, Role, Permission, SystemLayer
    )
    from dna.dna_system import (
        get_dna_generator, DNA, DNAStatus
    )
    from logging.append_only_logging import (
        get_system_log, log_operation, LogEventType, LogLevel
    )
    from scheduler.execution_schedule import (
        get_scheduler, create_default_tasks, TriggerType
    )
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    print("请确保所有核心模块都已安装")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════
# 【系统启动器】
# ═══════════════════════════════════════════════════════════════

class LongHunCoreSystem:
    """龍魂核心系统"""

    def __init__(self):
        self.config = None
        self.identity_verified = False
        self.rbac = None
        self.dna_generator = None
        self.system_log = None
        self.scheduler = None
        self.startup_timestamp = datetime.now().isoformat()

    def startup(self) -> Tuple[bool, Dict]:
        """系统启动过程"""
        startup_report = {
            "status": "initializing",
            "timestamp": self.startup_timestamp,
            "steps": [],
        }

        try:
            # 步骤1: 加载配置
            print("🔄 [1/6] 加载龍魂系统配置...")
            self.config = get_system_config()
            if validate_config():
                startup_report["steps"].append({"step": "load_config", "status": "✅"})
                print("   ✅ 配置加载成功")
            else:
                raise RuntimeError("配置验证失败")

            # 步骤2: 验证身份
            print("🔄 [2/6] 验证创始人身份 (三重验证)...")
            identity_verifier = IdentityVerificationL0()
            is_valid, verification_result = identity_verifier.verify_creator_identity()
            if is_valid:
                self.identity_verified = True
                startup_report["steps"].append({"step": "verify_identity", "status": "✅"})
                print("   ✅ 身份验证通过")
                print(f"      确认人: {verification_result['identity']['name']} ({verification_result['identity']['uid']})")
            else:
                raise RuntimeError(f"身份验证失败: {verification_result['error']}")

            # 步骤3: 初始化权限系统
            print("🔄 [3/6] 初始化权限控制系统 (RBAC)...")
            self.rbac = get_rbac_system()
            startup_report["steps"].append({"step": "init_rbac", "status": "✅"})
            print(f"   ✅ RBAC系统就绪 (创始人已初始化)")

            # 步骤4: 初始化DNA系统
            print("🔄 [4/6] 初始化DNA追溯码系统...")
            self.dna_generator = get_dna_generator()
            # 为核心系统本身生成DNA
            system_dna = self.dna_generator.generate_dna(
                subject="LONGHUN-CORE-SYSTEM",
                version="v1.0",
                description="龍魂核心系统启动DNA",
            )
            startup_report["steps"].append({
                "step": "init_dna",
                "status": "✅",
                "system_dna": system_dna.dna_code
            })
            print(f"   ✅ DNA系统就绪")
            print(f"      系统DNA: {system_dna.dna_code}")

            # 步骤5: 初始化日志系统
            print("🔄 [5/6] 初始化Append-Only日志系统...")
            self.system_log = get_system_log()
            log_operation(
                event_type=LogEventType.SYSTEM_START,
                message="龍魂核心系统启动",
                level=LogLevel.INFO,
                context={
                    "timestamp": self.startup_timestamp,
                    "system_dna": system_dna.dna_code,
                },
            )
            startup_report["steps"].append({"step": "init_logging", "status": "✅"})
            print(f"   ✅ 日志系统就绪")

            # 步骤6: 初始化执行调度器
            print("🔄 [6/6] 初始化执行调度器...")
            self.scheduler = create_default_tasks()
            startup_report["steps"].append({"step": "init_scheduler", "status": "✅"})
            print(f"   ✅ 调度器就绪 (已注册 {len(self.scheduler.tasks)} 个任务)")

            # 触发启动事件
            print("\n🚀 触发 STARTUP 事件...")
            executed_tasks = self.scheduler.trigger_event(TriggerType.STARTUP)
            print(f"   ✅ 执行了 {len(executed_tasks)} 个启动任务")

            startup_report["status"] = "✅ READY"
            startup_report["system_dna"] = system_dna.dna_code
            startup_report["identity"] = {
                "uid": "9622",
                "name": "诸葛鑫",
                "alias": "龍芯北辰",
                "verified": True,
            }

            return True, startup_report

        except Exception as e:
            startup_report["status"] = "❌ FAILED"
            startup_report["error"] = str(e)
            print(f"\n❌ 启动失败: {e}")
            return False, startup_report

    def get_system_status(self) -> Dict:
        """获取系统状态"""
        return {
            "timestamp": datetime.now().isoformat(),
            "startup_time": self.startup_timestamp,
            "identity_verified": self.identity_verified,
            "modules": {
                "config": self.config is not None,
                "rbac": self.rbac is not None,
                "dna": self.dna_generator is not None,
                "logging": self.system_log is not None,
                "scheduler": self.scheduler is not None,
            },
            "rbac_status": self.rbac.get_system_status() if self.rbac else None,
            "dna_statistics": self.dna_generator.get_statistics() if self.dna_generator else None,
            "log_statistics": self.system_log.get_statistics() if self.system_log else None,
            "scheduled_tasks": len(self.scheduler.tasks) if self.scheduler else 0,
        }

    def execute_operation(self, operation: str, params: Dict = None) -> Dict:
        """执行系统操作"""
        result = {
            "operation": operation,
            "timestamp": datetime.now().isoformat(),
            "status": "executing",
            "result": None,
        }

        try:
            if operation == "create_user":
                uid = params.get("uid")
                name = params.get("name")
                role = Role(params.get("role", "contributor"))
                success, msg = self.rbac.create_user(uid, name, role)
                result["status"] = "success" if success else "failed"
                result["result"] = msg
                log_operation(LogEventType.USER_CREATED, msg)

            elif operation == "generate_dna":
                subject = params.get("subject")
                version = params.get("version", "v1.0")
                dna = self.dna_generator.generate_dna(subject, version)
                result["status"] = "success"
                result["result"] = dna.dna_code
                log_operation(LogEventType.DNA_GENERATED, f"生成DNA: {dna.dna_code}")

            elif operation == "check_permission":
                uid = params.get("uid")
                permission = Permission(params.get("permission"))
                has_perm = self.rbac.check_access(uid, permission)
                result["status"] = "success"
                result["result"] = {"has_permission": has_perm}

            else:
                result["status"] = "failed"
                result["result"] = f"未知操作: {operation}"

        except Exception as e:
            result["status"] = "failed"
            result["result"] = str(e)
            log_operation(
                LogEventType.SYSTEM_ERROR,
                f"操作失败: {operation}",
                error_message=str(e),
            )

        return result


# ═══════════════════════════════════════════════════════════════
# 【主程序】
# ═══════════════════════════════════════════════════════════════

def main():
    """系统主函数"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "🐉 龍魂核心系統啟動".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    # 创建系统实例
    system = LongHunCoreSystem()

    # 执行启动
    success, startup_report = system.startup()

    print("\n")
    print("=" * 80)
    print("📋 系统启动报告")
    print("=" * 80)
    print(json.dumps(startup_report, ensure_ascii=False, indent=2))

    if success:
        print("\n")
        print("=" * 80)
        print("🟢 系统状态")
        print("=" * 80)
        status = system.get_system_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))

        print("\n")
        print("=" * 80)
        print("✅ 龍魂核心系統已就绪")
        print("=" * 80)
        print("""
配置文件位置:
  • 宪法和配置: ~/longhun-system/cnsh-core/constitution/
  • 身份验证: ~/longhun-system/cnsh-core/identity/
  • 权限系统: ~/longhun-system/cnsh-core/permissions/
  • DNA系统: ~/longhun-system/cnsh-core/dna/
  • 日志系统: ~/longhun-system/cnsh-core/logging/
  • 调度器: ~/longhun-system/cnsh-core/scheduler/

日志文件:
  • 系统审计: ~/longhun-system/logs/system_audit.jsonl
  • 工作流操作: ~/longhun-system/logs/workflow_operations.jsonl

下一步:
  1. 启用定时任务运行
  2. 集成工作流引擎
  3. 部署CNSH编译器
  4. 启动主控操作台

DNA标记:
  #龍芯⚡️2026-06-03-CORE-SYSTEM-LAUNCHER-v1.0
        """)

        return 0
    else:
        print("\n❌ 系统启动失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
