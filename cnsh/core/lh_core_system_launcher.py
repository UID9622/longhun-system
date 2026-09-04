#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
╔══════════════════════════════════════════════════════════════════╗
║     龍魂核心系统启动器 / LongHun Core System Launcher           ║
║                                                                  ║
║  集成所有P0模块：配置·身份·权限·DNA·日志·调度                      ║
║  完整的系统初始化和运行                                           ║
║                                                                  ║
║  DNA v1.0:#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-CORE-SYSTEM-LAUNCHER-FILE1-v1.0         ║
║  DNA v1.1: #龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-LAUNCHER-CORE-v1.0 (P0 对齐)      ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✓              ║
║                                                                  ║
║  来源: 五个Notion核心宣言                                        ║
║  责任: UID9622·不免责                                            ║
║  状态: 🟢 MAIN·可公开                                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import json
from typing import Dict, Tuple, Any
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# 【系统导入】所有核心模块
# ═══════════════════════════════════════════════════════════════

try:
    from cnsh_core.constitution.longhun_foundation_config import (
        get_system_config, validate_config, SystemMission, CreatorIdentity
    )
    from cnsh_core.identity.identity_verification import (
        IdentityVerificationL0, generate_identity_proof
    )
    from cnsh_core.permissions.rbac_system import (
        get_rbac_system, Role, Permission, SystemLayer
    )
    from cnsh_core.dna.dna_system import (
        get_dna_generator, DNA, DNAStatus
    )
    from cnsh_core.longhun_logging.append_only_logging import (
        get_system_log, log_operation, LogEventType, LogLevel
    )
    from cnsh_core.scheduler.execution_schedule import (
        get_scheduler, create_default_tasks, TriggerType
    )
    from cnsh_core.registry.route_registry import (
        get_route_registry, RouteRegistry
    )
    from cnsh_core.rules import (
        get_rule_engine, reset_rule_engine
    )
    from cnsh_core.compiler import (
        get_cnsh_compiler, reset_cnsh_compiler
    )
    from cnsh_core.router.persona_router import (
        get_persona_router
    )
except ImportError as e:
    # 如果使用 cnsh_core 前缀失败，尝试相对导入
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
        from longhun_logging.append_only_logging import (
            get_system_log, log_operation, LogEventType, LogLevel
        )
        from scheduler.execution_schedule import (
            get_scheduler, create_default_tasks, TriggerType
        )
        from registry.route_registry import (
            get_route_registry, RouteRegistry
        )
        from rules import (
            get_rule_engine, reset_rule_engine
        )
        from compiler import (
            get_cnsh_compiler, reset_cnsh_compiler
        )
        from router.persona_router import (
            get_persona_router
        )
    except ImportError as e2:
        print(f"❌ 模块导入失败: {e}")
        print(f"❌ 相对导入也失败: {e2}")
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
        self.registry = None
        self.rule_engine = None
        self.compiler = None
        self.persona_router = None
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
            print("🔄 [6/10] 初始化执行调度器...")
            self.scheduler = create_default_tasks()
            startup_report["steps"].append({"step": "init_scheduler", "status": "✅"})
            print(f"   ✅ 调度器就绪 (已注册 {len(self.scheduler.tasks)} 个任务)")

            # 步骤7: 初始化路由注册表和P0模块预注册
            print("🔄 [7/10] 初始化路由注册表和预注册P0模块...")
            self.registry = get_route_registry()

            # 自动预注册所有P0模块
            p0_success, p0_msg = self.register_p0_modules()
            if p0_success:
                print(f"   ✅ {p0_msg}")
            else:
                print(f"   ⚠️ P0模块预注册: {p0_msg}")

            registry_stats = self.registry.get_statistics()
            startup_report["steps"].append({
                "step": "init_registry",
                "status": "✅",
                "nodes_count": registry_stats["total_nodes"],
                "p0_modules": p0_success
            })
            print(f"   ✅ 路由注册表就绪 (已注册 {registry_stats['total_nodes']} 个节点)")

            # 步骤8: 初始化规则引擎和加载内置规则
            print("🔄 [8/10] 初始化规则引擎和加载内置规则...")
            self.rule_engine = get_rule_engine()

            # 加载内置规则
            from rules.builtin_rules import register_all_builtin_rules
            rules_success, rules_results = register_all_builtin_rules(self.rule_engine)

            if rules_success:
                rule_stats = self.rule_engine.get_statistics()
                print(f"   ✅ 规则引擎就绪 (已加载 {rule_stats['total_rules']} 条内置规则)")
                startup_report["steps"].append({
                    "step": "init_rule_engine",
                    "status": "✅",
                    "rules_count": rule_stats['total_rules']
                })
            else:
                # 部分规则加载失败，但继续启动
                print(f"   ⚠️ 内置规则加载: {len(rules_results)} 条规则")
                startup_report["steps"].append({
                    "step": "init_rule_engine",
                    "status": "⚠️",
                    "partial": True
                })

            # 将规则引擎注册到路由表
            rule_engine_success, rule_engine_msg = self.register_rule_engine_to_registry()
            if rule_engine_success:
                print(f"   ✅ 规则引擎已注册到路由表 (IPA-L1-002)")
            else:
                print(f"   ⚠️ 规则引擎注册失败: {rule_engine_msg}")

            # 步骤9: 初始化CNSH编译器
            print("🔄 [9/10] 初始化CNSH编译器...")
            self.compiler = get_cnsh_compiler()

            # 运行编译器自检
            compiler_ok, compiler_errors = self.compiler.selftest()
            if compiler_ok:
                startup_report["steps"].append({"step": "init_compiler", "status": "✅"})
                print("   ✅ CNSH编译器就绪")
            else:
                print(f"   ⚠️ 编译器自检报告:")
                for error in compiler_errors:
                    print(f"      - {error}")
                startup_report["steps"].append({
                    "step": "init_compiler",
                    "status": "⚠️",
                    "errors": compiler_errors
                })

            # 将编译器注册到路由表
            compiler_success, compiler_msg = self.register_compiler_to_registry()
            if compiler_success:
                print(f"   ✅ 编译器已注册到路由表 (IPA-L1-003)")
            else:
                print(f"   ⚠️ 编译器注册失败: {compiler_msg}")

            # 步骤10: 初始化PersonaRouter (人格路由系统·F4因子)
            print("🔄 [10/10] 初始化PersonaRouter (人格路由系统)...")
            try:
                self.persona_router = get_persona_router()

                # 运行PersonaRouter自检
                persona_ok, persona_errors = self.persona_router.selftest()
                if persona_ok:
                    startup_report["steps"].append({"step": "init_persona_router", "status": "✅"})
                    print("   ✅ PersonaRouter就绪 (虚伪词汇四分类·F4因子)")
                else:
                    print(f"   ⚠️ PersonaRouter自检报告:")
                    for error in persona_errors:
                        print(f"      - {error}")
                    startup_report["steps"].append({
                        "step": "init_persona_router",
                        "status": "⚠️",
                        "errors": persona_errors
                    })
            except ImportError:
                # PersonaRouter模块不可用
                print("   ⚠️ PersonaRouter未初始化 (模块不可用)")
                startup_report["steps"].append({
                    "step": "init_persona_router",
                    "status": "⚠️",
                    "reason": "module_not_available"
                })
            except Exception as e:
                print(f"   ❌ PersonaRouter初始化失败: {str(e)}")
                startup_report["steps"].append({
                    "step": "init_persona_router",
                    "status": "❌",
                    "error": str(e)
                })

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

    def get_system_status(self) -> Dict[str, Any]:
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
                "registry": self.registry is not None,
                "rule_engine": self.rule_engine is not None,
                "compiler": self.compiler is not None,
                "persona_router": self.persona_router is not None,
            },
            "rbac_status": self.rbac.get_system_status() if self.rbac else None,
            "dna_statistics": self.dna_generator.get_statistics() if self.dna_generator else None,
            "log_statistics": self.system_log.get_statistics() if self.system_log else None,
            "scheduled_tasks": len(self.scheduler.tasks) if self.scheduler else 0,
            "registry_statistics": self.registry.get_statistics() if self.registry else None,
            "rule_engine_statistics": self.rule_engine.get_statistics() if self.rule_engine else None,
        }

    def execute_operation(self, operation: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
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

    def register_compiler_to_registry(self) -> Tuple[bool, str]:
        """
        将CNSH编译器注册到路由表（P1-3 节点）

        Returns:
            (success, message)
        """
        if not self.registry or not self.compiler:
            return False, "编译器或路由表未初始化"

        try:
            from registry.node import RouteNode, NodeStatus, NodeType

            compiler_node = RouteNode(
                node_id="IPA-L1-003",
                name="cnsh_compiler",
                node_type=NodeType.LOCAL,
                status=NodeStatus.ACTIVE,
                local_path="cnsh_core.compiler",
                entry_point="get_cnsh_compiler",
                dna="#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-CNSH-COMPILER-v1.0",
                layer="L1_SEASONAL",
                description="CNSH编译器·计算逻辑赋能层·可参数化编译",
                tags=["L1", "compiler", "cnsh", "calculation"],
                dependencies=["IPA-L0-001", "IPA-L0-004", "IPA-L0-005", "IPA-L0-006", "IPA-L1-001"],
            )

            success, msg = self.registry.register(compiler_node)
            return success, msg

        except Exception as e:
            return False, f"编译器注册失败: {str(e)}"

    def register_rule_engine_to_registry(self) -> Tuple[bool, str]:
        """
        将规则引擎注册到路由表（P1-2 节点）

        Returns:
            (success, message)
        """
        if not self.registry or not self.rule_engine:
            return False, "规则引擎或路由表未初始化"

        try:
            from registry.node import RouteNode, NodeStatus, NodeType

            rule_engine_node = RouteNode(
                node_id="IPA-L1-002",
                name="rule_engine",
                node_type=NodeType.GATE,
                status=NodeStatus.ACTIVE,
                local_path="cnsh_core.rules",
                entry_point="get_rule_engine",
                dna="#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-RULE-ENGINE-v1.0",
                layer="L1_SEASONAL",
                description="规则引擎·守门人·业务规则执行器",
                tags=["L1", "rules", "gate", "decision"],
                dependencies=["IPA-L0-001", "IPA-L0-002", "IPA-L0-003",
                              "IPA-L0-004", "IPA-L0-005", "IPA-L0-006",
                              "IPA-L1-001"],
            )

            success, msg = self.registry.register(rule_engine_node)
            return success, msg

        except Exception as e:
            return False, f"规则引擎注册失败: {str(e)}"

    def register_p0_modules(self) -> Tuple[bool, str]:
        """
        预注册所有P0核心模块到路由表

        Returns:
            (success, message)
        """
        if not self.registry:
            return False, "路由注册表未初始化"

        try:
            from registry.node import RouteNode, NodeStatus, NodeType

            # 定义7个P0模块
            p0_modules = [
                RouteNode(
                    node_id="IPA-L0-001",
                    name="constitution",
                    node_type=NodeType.LOCAL,
                    status=NodeStatus.ACTIVE,
                    local_path="cnsh_core.constitution",
                    entry_point="get_system_config",
                    dna="#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-LAUNCHER-CONSTITUTION-v1.0",
                    layer="L0_ETERNAL",
                    description="系统宪法和基础配置",
                    tags=["L0", "config", "foundation"],
                    dependencies=[],
                ),
                RouteNode(
                    node_id="IPA-L0-002",
                    name="identity",
                    node_type=NodeType.LOCAL,
                    status=NodeStatus.ACTIVE,
                    local_path="cnsh_core.identity",
                    entry_point="generate_identity_proof",
                    dna="#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-IDENTITY-v1.0",
                    layer="L0_ETERNAL",
                    description="三重身份验证系统",
                    tags=["L0", "security", "authentication"],
                    dependencies=["IPA-L0-001"],
                ),
                RouteNode(
                    node_id="IPA-L0-003",
                    name="permissions",
                    node_type=NodeType.LOCAL,
                    status=NodeStatus.ACTIVE,
                    local_path="cnsh_core.permissions",
                    entry_point="get_rbac_system",
                    dna="#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-PERMISSIONS-v1.0",
                    layer="L0_ETERNAL",
                    description="RBAC权限控制系统",
                    tags=["L0", "security", "governance"],
                    dependencies=["IPA-L0-001", "IPA-L0-002"],
                ),
                RouteNode(
                    node_id="IPA-L0-004",
                    name="dna",
                    node_type=NodeType.LOCAL,
                    status=NodeStatus.ACTIVE,
                    local_path="cnsh_core.dna",
                    entry_point="get_dna_generator",
                    dna="#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-DNA-v1.0",
                    layer="L0_ETERNAL",
                    description="DNA追溯码生成和验证",
                    tags=["L0", "traceability", "identity"],
                    dependencies=["IPA-L0-001"],
                ),
                RouteNode(
                    node_id="IPA-L0-005",
                    name="logging",
                    node_type=NodeType.LOCAL,
                    status=NodeStatus.ACTIVE,
                    local_path="cnsh_core.logging",
                    entry_point="get_system_log",
                    dna="#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-LOGGING-v1.0",
                    layer="L0_ETERNAL",
                    description="Append-Only日志系统",
                    tags=["L0", "audit", "storage"],
                    dependencies=["IPA-L0-001", "IPA-L0-004"],
                ),
                RouteNode(
                    node_id="IPA-L0-006",
                    name="mathematics",
                    node_type=NodeType.LOCAL,
                    status=NodeStatus.ACTIVE,
                    local_path="cnsh_core.mathematics",
                    entry_point="get_formula_executor",
                    dna="#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-MATHEMATICS-v1.0",
                    layer="L0_ETERNAL",
                    description="数学公式和算法核心",
                    tags=["L0", "algorithm", "logic"],
                    dependencies=["IPA-L0-001"],
                ),
                RouteNode(
                    node_id="IPA-L1-001",
                    name="scheduler",
                    node_type=NodeType.LOCAL,
                    status=NodeStatus.ACTIVE,
                    local_path="cnsh_core.scheduler",
                    entry_point="get_scheduler",
                    dna="#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-SCHEDULER-v1.0",
                    layer="L1_SEASONAL",
                    description="执行调度和任务管理",
                    tags=["L1", "scheduling", "automation"],
                    dependencies=["IPA-L0-001", "IPA-L0-005"],
                ),
            ]

            # 注册所有模块
            success_count = 0
            failed_modules = []

            for node in p0_modules:
                success, msg = self.registry.register(node)
                if success:
                    success_count += 1
                else:
                    failed_modules.append(f"{node.node_id}: {msg}")

            if failed_modules:
                return False, f"注册 {success_count}/{len(p0_modules)} 个模块，失败: {', '.join(failed_modules)}"
            else:
                return True, f"成功注册所有 {len(p0_modules)} 个P0模块"

        except Exception as e:
            return False, f"预注册失败: {str(e)}"


# ═══════════════════════════════════════════════════════════════
# 【主程序】
# ═══════════════════════════════════════════════════════════════

def main():
    """系统主函数"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "🐉 龍魂核心系统启动".center(78) + "║")
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
        print("✅ 龍魂核心系统已就绪")
        print("=" * 80)
        print("""
配置文件位置:
  • 宪法和配置: ~/longhun-system/cnsh-core/constitution/
  • 身份验证: ~/longhun-system/cnsh-core/identity/
  • 权限系统: ~/longhun-system/cnsh-core/permissions/
  • DNA系统: ~/longhun-system/cnsh-core/dna/
  • 日志系统: ~/longhun-system/cnsh-core/logging/
  • 调度器: ~/longhun-system/cnsh-core/scheduler/
  • 编译器: ~/longhun-system/cnsh-core/compiler/
  • 编译配置: ~/longhun-system/03_compiler/

日志文件:
  • 系统审计: ~/longhun-system/logs/system_audit.jsonl
  • 工作流操作: ~/longhun-system/logs/workflow_operations.jsonl
  • 编译执行: ~/longhun-system/logs/compiler_execution.jsonl

下一步:
  1. 启用定时任务运行
  2. 集成工作流引擎
  3. 部署主控操作台
  4. 启动CNSH IDE

DNA标记:
  #龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-CORE-SYSTEM-LAUNCHER-v1.0
        """)

        return 0
    else:
        print("\n❌ 系统启动失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
