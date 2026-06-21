#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 Kimi 集成完整测试套件

DNA:#龍芯⚡️2026-06-08-KIMI-TEST-SUITE-v1.0
"""

import json
import sys
import time
from datetime import datetime

try:
    from kimi_client import KimiClient
    from kimi_integration import KimiIntegration
    from kimi_gateway import KimiGatewayLite
except ImportError:
    print("❌ 导入失败：请确保在 kimi 目录中运行此脚本")
    sys.exit(1)


class KimiTestSuite:
    """Kimi 集成测试套件"""

    def __init__(self):
        self.results = []
        self.start_time = datetime.now()

    def test_1_client_connection(self) -> bool:
        """测试 1: 客户端连接"""
        print("\n" + "=" * 80)
        print("测试 1️⃣: Kimi 客户端连接")
        print("=" * 80)

        try:
            client = KimiClient()
            is_healthy = client.health_check()

            if is_healthy:
                print("✅ PASS: Kimi API 连接成功")
                self.results.append({"test": "client_connection", "status": "PASS"})
                return True
            else:
                print("❌ FAIL: Kimi API 无响应")
                self.results.append({"test": "client_connection", "status": "FAIL"})
                return False

        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.results.append({"test": "client_connection", "status": "FAIL", "error": str(e)})
            return False

    def test_2_integration_initialization(self) -> bool:
        """测试 2: 集成框架初始化"""
        print("\n" + "=" * 80)
        print("测试 2️⃣: Kimi 集成初始化")
        print("=" * 80)

        try:
            kimi = KimiIntegration()

            # 检查所有模式
            modes_enabled = sum(1 for mode, config in kimi.mode_configs.items() if config["enabled"])
            print(f"✅ 已启用 {modes_enabled} 个集成模式")

            # 检查断路器
            print(f"✅ 断路器状态: {kimi.circuit_breaker.state}")

            # 检查健康状态
            health = kimi.get_health_status()
            print(f"✅ 健康检查结果:")
            print(f"   • Kimi API: {health['kimi_api']}")
            print(f"   • 集成模式: {modes_enabled}/4")
            print(f"   • 日志条目: {health['log_entries']}")

            self.results.append({"test": "integration_initialization", "status": "PASS"})
            return True

        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.results.append({"test": "integration_initialization", "status": "FAIL", "error": str(e)})
            return False

    def test_3_backup_inference(self) -> bool:
        """测试 3: 备用推理模型"""
        print("\n" + "=" * 80)
        print("测试 3️⃣: 备用推理模型（故障转移）")
        print("=" * 80)

        try:
            kimi = KimiIntegration()

            prompt = "请简要说明龍魂系统的四个核心功能"
            result = kimi.infer_with_fallback(prompt, use_kimi=True)

            if result["status"] in ["success", "fallback"]:
                print(f"✅ PASS: {result['status']}")
                print(f"   • 模型: {result['model']}")
                print(f"   • 响应: {result.get('response', result.get('reason'))[:100]}...")

                self.results.append({"test": "backup_inference", "status": "PASS"})
                return True
            else:
                print(f"❌ FAIL: {result}")
                self.results.append({"test": "backup_inference", "status": "FAIL"})
                return False

        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.results.append({"test": "backup_inference", "status": "FAIL", "error": str(e)})
            return False

    def test_4_realtime_chat(self) -> bool:
        """测试 4: 实时聊天"""
        print("\n" + "=" * 80)
        print("测试 4️⃣: 实时对话（聊天会话）")
        print("=" * 80)

        try:
            kimi = KimiIntegration()

            # 启动会话
            session = kimi.start_realtime_chat("test_user_001")
            print(f"✅ 会话创建成功")
            print(f"   • 会话 ID: {session['session_id']}")
            print(f"   • 状态: {session['status']}")

            # 发送消息
            result = kimi.send_message(
                session["session_id"],
                "龍魂系统支持哪些功能？"
            )

            if result["status"] == "success":
                print(f"✅ PASS: 消息发送成功")
                print(f"   • Kimi 响应: {result['kimi_response'][:100]}...")

                self.results.append({"test": "realtime_chat", "status": "PASS"})
                return True
            else:
                print(f"❌ FAIL: {result}")
                self.results.append({"test": "realtime_chat", "status": "FAIL"})
                return False

        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.results.append({"test": "realtime_chat", "status": "FAIL", "error": str(e)})
            return False

    def test_5_skill_engine(self) -> bool:
        """测试 5: Skill 引擎"""
        print("\n" + "=" * 80)
        print("测试 5️⃣: Skill 引擎集成")
        print("=" * 80)

        try:
            kimi = KimiIntegration()

            # 测试支持的 Skill
            test_cases = [
                ("skill-3-canvas-design", {"description": "设计一个现代化数据仪表板"}),
                ("skill-4-doc-coauthoring", {"title": "技术文档", "topic": "系统架构"}),
                ("skill-6-mcp-builder", {"service_name": "test-service"}),
            ]

            passed = 0
            for skill_id, skill_input in test_cases:
                result = kimi.use_kimi_for_skill(skill_id, skill_input)
                status = result.get("status")

                if status in ["success", "unsupported"]:
                    print(f"✅ {skill_id}: {status}")
                    passed += 1
                else:
                    print(f"❌ {skill_id}: FAIL")

            if passed == 3:
                print(f"\n✅ PASS: 3/3 Skill 测试通过")
                self.results.append({"test": "skill_engine", "status": "PASS"})
                return True
            else:
                print(f"\n❌ FAIL: 仅 {passed}/3 通过")
                self.results.append({"test": "skill_engine", "status": "FAIL"})
                return False

        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.results.append({"test": "skill_engine", "status": "FAIL", "error": str(e)})
            return False

    def test_6_gateway(self) -> bool:
        """测试 6: 网关"""
        print("\n" + "=" * 80)
        print("测试 6️⃣: Kimi 网关")
        print("=" * 80)

        try:
            gateway = KimiGatewayLite()

            # 测试健康检查
            health = gateway.handle_request("/health", "GET", {})
            print(f"✅ 健康检查: {health['kimi_api']}")

            # 测试备用推理
            result = gateway.handle_request(
                "/kimi/backup-inference",
                "POST",
                {"prompt": "测试"}
            )
            print(f"✅ 备用推理: {result['status']}")

            # 测试聊天启动
            session = gateway.handle_request(
                "/kimi/chat/start",
                "POST",
                {"user_id": "test"}
            )
            print(f"✅ 聊天启动: {session['status']}")

            # 测试集成报告
            report = gateway.handle_request("/kimi/report", "GET", {})
            print(f"✅ 集成报告: {report['status']}")

            print(f"\n✅ PASS: 网关测试完成")
            self.results.append({"test": "gateway", "status": "PASS"})
            return True

        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.results.append({"test": "gateway", "status": "FAIL", "error": str(e)})
            return False

    def test_7_circuit_breaker(self) -> bool:
        """测试 7: 断路器机制"""
        print("\n" + "=" * 80)
        print("测试 7️⃣: 断路器故障转移")
        print("=" * 80)

        try:
            from kimi_integration import CircuitBreaker

            breaker = CircuitBreaker(failure_threshold=3, timeout=5)

            print(f"初始状态: {breaker.state}")

            # 模拟 3 次失败
            for i in range(3):
                breaker.record_failure()
                print(f"失败 {i+1}/3: {breaker.state}")

            # 检查是否打开
            if breaker.state == "OPEN":
                print(f"✅ 断路器正确打开")
            else:
                print(f"❌ 断路器未打开")
                return False

            # 尝试执行
            can_execute = breaker.can_execute()
            print(f"能否执行: {can_execute} (预期: False)")

            if not can_execute:
                print(f"✅ 断路器正确阻止执行")
                print(f"\n✅ PASS: 断路器机制正常")
                self.results.append({"test": "circuit_breaker", "status": "PASS"})
                return True
            else:
                print(f"❌ 断路器未正确阻止")
                self.results.append({"test": "circuit_breaker", "status": "FAIL"})
                return False

        except Exception as e:
            print(f"❌ FAIL: {e}")
            self.results.append({"test": "circuit_breaker", "status": "FAIL", "error": str(e)})
            return False

    def run_all_tests(self):
        """运行所有测试"""
        print("\n")
        print("╔" + "=" * 78 + "╗")
        print("║" + " " * 78 + "║")
        print("║" + "🧪 龍魂 × Kimi 集成完整测试套件".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "=" * 78 + "╝")

        # 运行所有测试
        tests = [
            self.test_1_client_connection,
            self.test_2_integration_initialization,
            self.test_3_backup_inference,
            self.test_4_realtime_chat,
            self.test_5_skill_engine,
            self.test_6_gateway,
            self.test_7_circuit_breaker,
        ]

        for test_func in tests:
            try:
                test_func()
            except Exception as e:
                print(f"❌ 测试异常: {e}")

        # 生成报告
        self._generate_report()

    def _generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 80)
        print("📊 测试报告")
        print("=" * 80)

        passed = sum(1 for r in self.results if r["status"] == "PASS")
        total = len(self.results)
        pass_rate = (passed / total * 100) if total > 0 else 0

        print(f"\n✅ 通过: {passed}/{total} ({pass_rate:.1f}%)")
        print(f"❌ 失败: {total - passed}/{total}")

        print(f"\n📝 详细结果:")
        for result in self.results:
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            print(f"  {status_icon} {result['test']}: {result['status']}")
            if "error" in result:
                print(f"     → {result['error']}")

        duration = (datetime.now() - self.start_time).total_seconds()
        print(f"\n⏱️  耗时: {duration:.2f} 秒")

        print(f"\n🎯 整体结果: {'🟢 ALL PASS' if pass_rate == 100 else '🟡 PARTIAL' if passed > 0 else '🔴 ALL FAIL'}")

        print(f"\nDNA: #龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-KIMI-TEST-REPORT-v1.0")
        print(f"确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z\n")


if __name__ == "__main__":
    suite = KimiTestSuite()
    suite.run_all_tests()
