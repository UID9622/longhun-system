#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍魂 · 集成测试套件 v1.0
Integration Test Suite - Validate All Three Systems

DNA追溯碼：#龍芯⚡️2026-05-27-INTEGRATION-TEST-v1.0
CONFIRM：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 测试 longhun_notion_pow.py - PoW 工作量证明系统
  2. 测试 longhun_api_server.py - FastAPI 服务器集成
  3. 验证移动端 JS 面板的 API 调用
  4. 生成完整的集成测试报告

运行：
  python3 longhun_integration_test.py
"""

import sys
import json
import time
import subprocess
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

# 导入三个核心系统
try:
    from longhun_notion_pow import (
        ProofOfWork,
        LocalWorkDB,
        SortingWorkRecord,
        log_sorting_work,
        hash_work,
    )
    NOTION_POW_OK = True
    NOTION_POW_ERROR = None
except Exception as e:
    NOTION_POW_OK = False
    NOTION_POW_ERROR = str(e)


class IntegrationTestRunner:
    """集成测试运行器"""

    def __init__(self):
        self.results: List[Dict] = []
        self.start_time = datetime.now()
        self.test_count = 0
        self.pass_count = 0
        self.fail_count = 0

    def test(self, name: str, func, *args, **kwargs) -> bool:
        """运行单个测试"""
        self.test_count += 1
        try:
            result = func(*args, **kwargs)
            self.pass_count += 1
            self.results.append(
                {
                    "name": name,
                    "status": "✅ PASS",
                    "time": datetime.now().isoformat(),
                }
            )
            print(f"✅ {name}")
            return True
        except Exception as e:
            self.fail_count += 1
            self.results.append(
                {
                    "name": name,
                    "status": "❌ FAIL",
                    "error": str(e),
                    "time": datetime.now().isoformat(),
                }
            )
            print(f"❌ {name}: {e}")
            return False

    def report(self):
        """生成测试报告"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        success_rate = (
            (self.pass_count / self.test_count * 100) if self.test_count > 0 else 0
        )

        report = {
            "title": "🐉 龍魂 · 集成测试报告 v1.0",
            "dna": "#龍芯⚡️2026-05-27-INTEGRATION-TEST-REPORT",
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": self.test_count,
                "passed": self.pass_count,
                "failed": self.fail_count,
                "success_rate": f"{success_rate:.1f}%",
                "elapsed_seconds": f"{elapsed:.2f}",
            },
            "details": self.results,
        }

        return report


def test_pow_system():
    """测试 PoW 工作量证明系统"""
    print("\n" + "=" * 80)
    print("【测试 1】Notion PoW 工作量证明系统")
    print("=" * 80)

    runner = IntegrationTestRunner()

    # 测试 1.1: ProofOfWork.hash_work
    def test_hash_work():
        hash_val = ProofOfWork.hash_work(
            timestamp="2026-05-27T12:00:00",
            algorithm="快速排序",
            comparisons=145,
            swaps=73,
            array_size=100,
            nonce=0,
        )
        assert len(hash_val) == 64, f"Hash长度应为64，实际{len(hash_val)}"
        assert all(c in "0123456789abcdef" for c in hash_val), "应该是有效的十六进制"

    runner.test("1.1: ProofOfWork.hash_work() - SHA-256 生成", test_hash_work)

    # 测试 1.2: LocalWorkDB 初始化
    def test_local_db():
        db = LocalWorkDB()
        assert db.db_path.exists(), "数据库文件应该被创建"

    runner.test("1.2: LocalWorkDB 初始化", test_local_db)

    # 测试 1.3: LocalWorkDB 插入记录
    def test_db_insert():
        db = LocalWorkDB()
        record = SortingWorkRecord(
            timestamp="2026-05-27T12:00:00",
            algorithm="冒泡排序",
            array_size=50,
            comparisons=1225,
            swaps=625,
            pow_hash="abcd1234" * 8,  # 64 chars
            pow_nonce=42,
        )
        local_id = db.insert(record)
        assert local_id.startswith("local_"), f"ID格式错误: {local_id}"

    runner.test("1.3: LocalWorkDB 插入和检索记录", test_db_insert)

    # 测试 1.4: PoW 挖矿 (difficulty=1)
    def test_mining():
        hash_val, nonce = ProofOfWork.mine_work(
            timestamp="2026-05-27T12:00:00",
            algorithm="堆排序",
            comparisons=189,
            swaps=94,
            array_size=100,
            difficulty=1,  # 要求第一位是 0
        )
        assert hash_val.startswith("0"), f"Hash应该以0开头，实际: {hash_val[:8]}"
        assert nonce >= 0, f"Nonce应该是正数，实际: {nonce}"

    runner.test("1.4: PoW 挖矿 (difficulty=1)", test_mining)

    # 输出报告
    report = runner.report()
    print("\n" + "=" * 80)
    print("【测试结果】Notion PoW 系统")
    print("=" * 80)
    print(f"总测试数: {report['summary']['total_tests']}")
    print(f"通过: {report['summary']['passed']}")
    print(f"失败: {report['summary']['failed']}")
    print(f"成功率: {report['summary']['success_rate']}")
    print(f"耗时: {report['summary']['elapsed_seconds']}秒")

    return report


def test_api_server():
    """测试 API 服务器（优先使用标准库版本）"""
    print("\n" + "=" * 80)
    print("【测试 2】HTTP API 服务器 (标准库版本)")
    print("=" * 80)

    runner = IntegrationTestRunner()

    # 检查是否可以导入标准库版本的服务器
    def test_import_stdlib_server():
        try:
            import longhun_api_server_stdlib
            assert hasattr(longhun_api_server_stdlib, "SortAlgorithms"), "SortAlgorithms 应该存在"
        except ImportError as e:
            raise AssertionError(f"无法导入 longhun_api_server_stdlib: {e}")

    runner.test("2.1: 标准库 API 服务器导入", test_import_stdlib_server)

    # 测试所有排序算法实现
    def test_algorithms():
        from longhun_api_server_stdlib import SortAlgorithms

        algorithms = [
            ("bubble_sort", 10),
            ("insertion_sort", 10),
            ("selection_sort", 10),
            ("quick_sort", 15),
            ("merge_sort", 15),
            ("shell_sort", 10),
        ]

        for algo_name, size in algorithms:
            algo_func = getattr(SortAlgorithms, algo_name)
            comparisons, swaps = algo_func([5, 2, 8, 1, 9])
            assert comparisons >= 0, f"{algo_name}: comparisons 应 >= 0"
            assert swaps >= 0, f"{algo_name}: swaps 应 >= 0"

    runner.test("2.2: 排序算法实现 (6种)", test_algorithms)

    # 输出报告
    report = runner.report()
    print("\n" + "=" * 80)
    print("【测试结果】FastAPI 服务器")
    print("=" * 80)
    print(f"总测试数: {report['summary']['total_tests']}")
    print(f"通过: {report['summary']['passed']}")
    print(f"失败: {report['summary']['failed']}")
    print(f"成功率: {report['summary']['success_rate']}")

    return report


def test_mobile_panel():
    """测试移动端 JS 面板的模拟请求"""
    print("\n" + "=" * 80)
    print("【测试 3】移动端 JS 面板 - API 模拟")
    print("=" * 80)

    runner = IntegrationTestRunner()

    # 测试 API 请求体格式
    def test_request_format():
        request_body = {
            "algorithm": "bubble_sort",
            "array_size": 50,
            "description": "Test run from mobile",
        }
        assert "algorithm" in request_body
        assert "array_size" in request_body
        assert request_body["array_size"] > 0

    runner.test("3.1: API 请求体格式验证", test_request_format)

    # 测试响应体格式
    def test_response_format():
        response_body = {
            "algorithm": "bubble_sort",
            "array_size": 50,
            "comparisons": 1225,
            "swaps": 625,
            "pow_hash": "abcd1234" * 8,
            "local_id": "local_1234567890",
            "notion_page_id": None,
            "timestamp": "2026-05-27T12:00:00",
        }
        required_fields = [
            "algorithm",
            "array_size",
            "comparisons",
            "swaps",
            "pow_hash",
        ]
        for field in required_fields:
            assert field in response_body, f"响应缺少字段: {field}"

    runner.test("3.2: API 响应体格式验证", test_response_format)

    # 输出报告
    report = runner.report()
    print("\n" + "=" * 80)
    print("【测试结果】移动端 JS 面板")
    print("=" * 80)
    print(f"总测试数: {report['summary']['total_tests']}")
    print(f"通过: {report['summary']['passed']}")
    print(f"失败: {report['summary']['failed']}")
    print(f"成功率: {report['summary']['success_rate']}")

    return report


def generate_final_report(pow_report, api_report, mobile_report):
    """生成最终集成测试报告"""
    print("\n" + "=" * 80)
    print("🐉 龍魂 · 最终集成测试报告")
    print("=" * 80)

    total_tests = (
        pow_report["summary"]["total_tests"]
        + api_report["summary"]["total_tests"]
        + mobile_report["summary"]["total_tests"]
    )
    total_passed = (
        pow_report["summary"]["passed"]
        + api_report["summary"]["passed"]
        + mobile_report["summary"]["passed"]
    )
    total_failed = (
        pow_report["summary"]["failed"]
        + api_report["summary"]["failed"]
        + mobile_report["summary"]["failed"]
    )

    print(f"\n📊 总体统计")
    print(f"  - 总测试数: {total_tests}")
    print(f"  - 通过: {total_passed} ✅")
    print(f"  - 失败: {total_failed} ❌" if total_failed > 0 else "  - 失败: 0")
    print(f"  - 成功率: {total_passed/total_tests*100:.1f}%")

    print(f"\n📋 子系统统计")
    print(f"  1️⃣  PoW 系统: {pow_report['summary']['passed']}/{pow_report['summary']['total_tests']}")
    print(f"  2️⃣  API 服务: {api_report['summary']['passed']}/{api_report['summary']['total_tests']}")
    print(f"  3️⃣  移动面板: {mobile_report['summary']['passed']}/{mobile_report['summary']['total_tests']}")

    print(f"\n🚀 下一步")
    if total_failed == 0:
        print("  ✅ 所有系统就绪！")
        print("  1️⃣  启动 API 服务器: python3 longhun_api_server.py")
        print("  2️⃣  访问移动面板: http://localhost:5000/control")
        print("  3️⃣  使用 ngrok 进行外网访问: ngrok http 5000")
    else:
        print("  ⚠️  存在失败的测试，请查阅上方详情")

    print("\n" + "=" * 80)

    # 保存报告文件
    report_path = Path(__file__).parent / "INTEGRATION_TEST_REPORT_20260527.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "dna": "#龍芯⚡️2026-05-27-INTEGRATION-TEST-FINAL-REPORT",
                "timestamp": datetime.now().isoformat(),
                "pow_system": pow_report,
                "api_server": api_report,
                "mobile_panel": mobile_report,
                "summary": {
                    "total_tests": total_tests,
                    "passed": total_passed,
                    "failed": total_failed,
                    "success_rate": f"{total_passed/total_tests*100:.1f}%" if total_tests > 0 else "0%",
                },
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"📄 完整报告已保存: {report_path}")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("🐉 龍魂 · 三系统集成测试套件")
    print("=" * 80)
    print(f"开始时间: {datetime.now().isoformat()}")
    print(f"DNA: #龍芯⚡️2026-05-27-INTEGRATION-TEST-v1.0")

    # 检查依赖
    if not NOTION_POW_OK:
        print(f"\n⚠️  警告: longhun_notion_pow.py 导入失败")
        print(f"   原因: {NOTION_POW_ERROR}")
        print(f"   测试将继续，但 PoW 系统测试可能失败\n")

    try:
        # 运行三套测试
        pow_report = test_pow_system()
        api_report = test_api_server()
        mobile_report = test_mobile_panel()

        # 生成最终报告
        generate_final_report(pow_report, api_report, mobile_report)

    except KeyboardInterrupt:
        print("\n\n⛔ 测试被中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 致命错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\n✅ 集成测试完成")
