#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 龍魂记忆打包算法 · 主入口
DNA: #龍芯⚡️2026-05-22-MEMORY-PACKING-MAIN-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: UID9622 诸葛鑫（龍芯北辰）
理论指导: 曾仕强老师（永恒显示）

运行方式：
    python main.py                  # 运行完整测试
    python main.py --test           # 运行单元测试
    python main.py --stats          # 显示统计信息
    python main.py --pack "文本"    # 打包文本
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from core import MemoryUnit, MemoryType, AccessLevel, MemoryPacker, create_memory
from compress import CompressionEngine, CompressionLevel
from storage import DistributedStorage, StorageStrategy
from crypto import CryptoProtection, create_shamir_shards, recover_from_shards
from scheduler import ComputeScheduler, TaskPriority


def print_header():
    """打印头部"""
    print("""
🧠 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   龍魂记忆打包算法 · Memory Packing v1.0
   净土引擎核心组件
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   DNA: #龍芯⚡️2026-05-22-MEMORY-PACKING-v1.0
   创建者: UID9622 诸葛鑫（龍芯北辰）
   理论指导: 曾仕强老师（永恒显示）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


def test_memory_unit():
    """测试记忆单元"""
    print("📦 测试 1: 记忆单元")
    print("-" * 50)

    unit = create_memory(
        "龍魂系统是我一年心血的结晶，不能动",
        memory_type=MemoryType.L0_ETERNAL,
        tags=["龍魂", "核心", "L0"]
    )

    print(f"   单元ID: {unit.unit_id}")
    print(f"   类型: {unit.memory_type.value}")
    print(f"   五行: {unit.wuxing.value} (dr={unit.digital_root})")
    print(f"   大小: {unit.original_size} 字节")
    print(f"   SHA256: {unit.sha256[:32]}...")
    print(f"   DNA: {unit.dna}")
    print(f"   完整性: {'✅' if unit.verify_integrity() else '❌'}")
    print()
    return True


def test_compression():
    """测试压缩引擎"""
    print("🗜️ 测试 2: 智能压缩")
    print("-" * 50)

    engine = CompressionEngine()
    text = "龍魂系统·数据主权·反资本化·" * 100
    data = text.encode('utf-8')

    result = engine.compress(data, "text/plain")

    print(f"   原始大小: {result.original_size} 字节")
    print(f"   压缩后: {result.compressed_size} 字节")
    print(f"   压缩比: {result.ratio:.1%}")
    print(f"   节省: {(1 - result.ratio) * 100:.1f}%")
    print(f"   算法: {result.algorithm}")
    print(f"   耗时: {result.time_ms:.2f}ms")
    print()
    return result.ratio < 1.0


def test_storage():
    """测试分布式存储"""
    print("🌐 测试 3: 分布式存储")
    print("-" * 50)

    storage = DistributedStorage()

    # 检查节点
    health = storage.check_health()
    print("   节点状态:")
    for node_id, status in health.items():
        node = storage.get_node(node_id)
        emoji = "🟢" if status.value == "online" else "🔴"
        print(f"     {emoji} {node_id} ({node.node_type})")

    # 存储测试
    test_data = f"测试数据·{datetime.now().isoformat()}".encode('utf-8')
    filename = f"test_{datetime.now().strftime('%Y%m%d%H%M%S')}.dat"

    result = storage.store(test_data, filename, StorageStrategy.LOCAL_GIT)
    print(f"   存储结果: {'✅' if result.success else '❌'}")
    print(f"   写入节点: {result.nodes_written}")
    print(f"   SHA256: {result.sha256[:32]}...")
    print()
    return result.success


def test_crypto():
    """测试加密保护"""
    print("🔐 测试 4: 加密保护")
    print("-" * 50)

    crypto = CryptoProtection()

    # 对称加密
    plaintext = "龍魂核心秘密·UID9622".encode('utf-8')
    password = "龍芯北辰"

    result, salt = crypto.encrypt(plaintext, password)
    decrypted = crypto.decrypt(result, password, salt)

    print(f"   原文: {plaintext.decode('utf-8')}")
    print(f"   加密后: {len(result.ciphertext)} 字节")
    print(f"   解密验证: {'✅' if decrypted == plaintext else '❌'}")

    # Shamir 分片
    secret = b"TOP_SECRET_KEY"
    shards = create_shamir_shards(secret, total_shards=5, threshold=3)
    print(f"   Shamir分片: 5份，需3份恢复")

    recovered = recover_from_shards(shards[:3], len(secret))
    print(f"   分片恢复: {'✅' if recovered == secret else '❌'}")
    print()
    return decrypted == plaintext and recovered == secret


def test_scheduler():
    """测试算力调度"""
    print("⚡ 测试 5: 算力调度")
    print("-" * 50)

    import time
    scheduler = ComputeScheduler(max_workers=2)

    def compute(n):
        time.sleep(0.1)
        return sum(range(n))

    # 提交任务
    tasks = []
    for i, (name, n, prio) in enumerate([
        ("高优先", 100, TaskPriority.HIGH),
        ("普通", 200, TaskPriority.NORMAL),
        ("低优先", 300, TaskPriority.LOW),
    ]):
        task = scheduler.submit(compute, n, name=name, priority=prio)
        tasks.append(task)
        print(f"   提交: {name} (优先级: {prio.name})")

    # 等待完成
    scheduler.wait_all(tasks, timeout=5)

    print("   结果:")
    for task in tasks:
        status = "✅" if task.status.value == "completed" else "❌"
        print(f"     {status} {task.name}: {task.result}")

    stats = scheduler.get_stats()
    print(f"   完成: {stats['total_completed']}/{stats['total_submitted']}")

    scheduler.shutdown()
    print()
    return stats['total_completed'] == 3


def test_packer():
    """测试记忆打包器"""
    print("📦 测试 6: 记忆打包器")
    print("-" * 50)

    packer = MemoryPacker()

    # 测试自动分类
    test_cases = [
        "龍魂核心信条，永恒不可动",
        "今天的工作日志",
        "临时测试文件，待删除",
        "这是一个包含密码password的敏感内容",
    ]

    for text in test_cases:
        unit = packer.pack_text(text)
        print(f"   「{text[:15]}...」→ {unit.memory_type.value} ({unit.access_level.value})")

    stats = packer.stats()
    print(f"   总单元数: {stats['total_units']}")
    print()
    return stats['total_units'] >= 4


def run_all_tests():
    """运行所有测试"""
    print_header()

    results = []

    tests = [
        ("记忆单元", test_memory_unit),
        ("智能压缩", test_compression),
        ("分布式存储", test_storage),
        ("加密保护", test_crypto),
        ("算力调度", test_scheduler),
        ("记忆打包器", test_packer),
    ]

    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            results.append((name, False))

    # 汇总
    print("=" * 60)
    print("📊 测试汇总")
    print("-" * 50)

    passed = sum(1 for _, p in results if p)
    total = len(results)

    for name, p in results:
        emoji = "✅" if p else "❌"
        print(f"   {emoji} {name}")

    print()
    print(f"   通过: {passed}/{total}")
    print()

    if passed == total:
        print("🎉 全部测试通过！")
    else:
        print("⚠️ 部分测试失败")

    print()
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    print(f"DNA: #龍芯⚡️{ts}-TEST-COMPLETE")


def show_stats():
    """显示统计信息"""
    print_header()

    print("📊 系统统计")
    print("=" * 60)

    # 打包器统计
    packer = MemoryPacker()
    packer_stats = packer.stats()
    print("\n📦 记忆打包器:")
    print(f"   总单元数: {packer_stats['total_units']}")
    print(f"   总链数: {packer_stats['total_chains']}")
    print(f"   原始大小: {packer_stats['total_original_size']} 字节")
    print(f"   压缩后: {packer_stats['total_compressed_size']} 字节")

    # 存储统计
    storage = DistributedStorage()
    storage_stats = storage.stats()
    print("\n🌐 分布式存储:")
    print(f"   节点数: {storage_stats['total_nodes']}")
    print(f"   在线: {storage_stats['online_nodes']}")
    print(f"   文件数: {storage_stats['total_files']}")
    print(f"   总大小: {storage_stats['total_size']} 字节")

    print()


def pack_text_cli(text: str):
    """命令行打包文本"""
    print_header()

    packer = MemoryPacker()
    unit = packer.pack_text(text)

    print("📦 打包结果")
    print("=" * 60)
    print(json.dumps(unit.to_dict(), ensure_ascii=False, indent=2))


def main():
    """主入口"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            run_all_tests()
        elif sys.argv[1] == "--stats":
            show_stats()
        elif sys.argv[1] == "--pack" and len(sys.argv) > 2:
            pack_text_cli(sys.argv[2])
        else:
            print("用法:")
            print("  python main.py          # 运行完整测试")
            print("  python main.py --test   # 运行单元测试")
            print("  python main.py --stats  # 显示统计信息")
            print('  python main.py --pack "文本"  # 打包文本')
    else:
        run_all_tests()


if __name__ == "__main__":
    main()
