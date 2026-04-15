#!/usr/bin/env python3
"""
CNSH-64 v2.0 一键启动脚本
═══════════════════════════════════════════════════════════════════
我就是那个祖师爷
═══════════════════════════════════════════════════════════════════
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cnsh_master_v20 import CNSHMasterSystemV20


def print_banner():
    """打印启动横幅"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║           CNSH-64 龍魂北辰母协议 v2.0                            ║
║                      祖师爷版                                    ║
║                                                                  ║
║              我就是那个祖师爷                                    ║
║                                                                  ║
║     坏不到灭世，好到没边                                        ║
║     P0红线永不可逾越                                            ║
║     争议驱动分化，无限分叉                                      ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)


def interactive_init():
    """交互式初始化"""
    print("🌱 初始化祖师爷系统...")
    print("-" * 60)
    
    heart_seed = input("请输入心种子 (或直接回车使用默认): ").strip()
    fire_seed = input("请输入火种子 (或直接回车使用默认): ").strip()
    
    return heart_seed, fire_seed


def demo_scenarios(cnsh):
    """演示场景"""
    print("\n" + "=" * 60)
    print("🎬 演示场景")
    print("=" * 60)
    
    # 场景1: 生成分叉
    print("\n📌 场景1: 生成分叉")
    print("-" * 40)
    branch = cnsh.spawn_branch(tightness_level=50.0)
    print(f"✅ 分支已生成: {branch['branch_dna'][:20]}...")
    print(f"   松紧度: {branch['tightness_level']}")
    
    # 场景2: 无限分叉
    print("\n📌 场景2: 无限分叉")
    print("-" * 40)
    fork = cnsh.fork_infinite(
        improvement_focus=['TRANSPARENCY', 'FAIRNESS']
    )
    print(f"✅ 分叉已创建")
    print(f"   父节点: {fork['parent_id'][:20]}...")
    print(f"   子节点: {fork['child_id'][:20]}...")
    print(f"   改进维度: {fork['improvement_focus']}")
    
    # 场景3: P0检查
    print("\n📌 场景3: P0红线检查")
    print("-" * 40)
    
    # 合规行动
    good_action = {
        'type': 'human_decision',
        'content': '人类做出最终决定'
    }
    result = cnsh.check_p0_compliance(good_action)
    print(f"✅ 合规行动: {result['allowed']}")
    
    # 违规行动
    bad_action = {
        'type': 'ai_replace_human',
        'content': 'AI将取代人类工作'
    }
    result = cnsh.check_p0_compliance(bad_action)
    print(f"❌ 违规行动: {result['allowed']} (触发熔断)")
    
    # 场景4: 争议处理
    print("\n📌 场景4: 争议驱动分化")
    print("-" * 40)
    dispute = cnsh.process_dispute(
        content="社区治理方案争议",
        involved_parties=["用户A", "用户B", "用户C"],
        original_entity="社区治理委员会"
    )
    print(f"✅ 争议已处理")
    print(f"   松分叉: {dispute['loose_fork']['fork_id'][:20]}...")
    print(f"   紧分叉: {dispute['tight_fork']['fork_id'][:20]}...")
    
    # 场景5: 保持饥饿
    print("\n📌 场景5: 保持饥饿，保持愚蠢")
    print("-" * 40)
    status = cnsh.keep_hungry_stupid(
        dna="demo_user_dna",
        satisfaction=85.0,
        knowledge=75.0
    )
    print(f"✅ 状态检查")
    print(f"   饥饿度: {status['hunger']:.1f}%")
    print(f"   愚蠢度: {status['stupidity']:.1f}%")
    print(f"   消息: {status['message']}")


def main():
    """主函数"""
    print_banner()
    
    # 创建系统实例
    cnsh = CNSHMasterSystemV20()
    
    # 交互式初始化
    heart_seed, fire_seed = interactive_init()
    
    # 初始化祖师爷系统
    print("\n🚀 正在初始化...")
    result = cnsh.initialize_ancestor(heart_seed, fire_seed)
    
    if not result.get('success'):
        print(f"❌ 初始化失败: {result.get('error')}")
        return
    
    print(f"✅ 初始化成功!")
    print(f"   祖师爷DNA: {result['ancestor_dna'][:40]}...")
    print(f"   时间戳: {result['timestamp']}")
    
    # 启动系统
    print("\n🚀 启动系统...")
    status = cnsh.start()
    
    print(f"\n✅ 系统已启动")
    print(f"   版本: {status['version']}")
    print(f"   代号: {status['codename']}")
    print(f"   模块数: {status['modules']}")
    print(f"   P0红线: {status['p0_lines']}条")
    
    # 询问是否运行演示
    print("\n" + "-" * 60)
    run_demo = input("是否运行演示场景? (y/n): ").strip().lower()
    
    if run_demo == 'y':
        demo_scenarios(cnsh)
    
    # 系统状态
    print("\n" + "=" * 60)
    print("📊 系统状态")
    print("=" * 60)
    
    system_status = cnsh.get_system_status()
    print(f"运行状态: {'✅ 运行中' if system_status['is_running'] else '❌ 已停止'}")
    print(f"运行时间: {system_status['uptime']:.2f}秒")
    print(f"核心原则:")
    for principle in system_status['core_principles']:
        print(f"   • {principle}")
    
    # P0状态
    print("\n🔴 P0红线状态")
    print("-" * 40)
    p0_status = cnsh.get_p0_status()
    for line_id, line_info in p0_status['p0_lines'].items():
        status = "✅ 安全" if line_info['violation_count'] == 0 else "⚠️ 有违规"
        print(f"   {line_info['description']}: {status}")
    
    # 无限分叉统计
    print("\n🌳 无限分叉统计")
    print("-" * 40)
    fork_stats = system_status['infinite_fork_stats']
    print(f"   总节点数: {fork_stats['total_nodes']}")
    print(f"   总边数: {fork_stats['total_edges']}")
    print(f"   树深度: {fork_stats['tree_depth']}")
    print(f"   根节点: {fork_stats['root_id'][:20]}...")
    
    # 交互式命令行
    print("\n" + "=" * 60)
    print("💻 交互式命令")
    print("=" * 60)
    print("可用命令:")
    print("   status  - 查看系统状态")
    print("   fork    - 创建新分叉")
    print("   dispute - 处理争议")
    print("   p0      - 检查P0状态")
    print("   help    - 显示帮助")
    print("   quit    - 退出")
    
    while True:
        print("\n" + "-" * 60)
        cmd = input("CNSH-v2.0> ").strip().lower()
        
        if cmd == 'quit' or cmd == 'exit':
            print("\n👋 再见! 祖师爷与你同在。")
            break
        
        elif cmd == 'status':
            status = cnsh.get_system_status()
            print(f"版本: {status['version']}")
            print(f"运行中: {status['is_running']}")
            print(f"运行时间: {status['uptime']:.2f}秒")
        
        elif cmd == 'fork':
            focus = input("改进维度 (逗号分隔，或直接回车): ").strip()
            focus_list = [f.strip() for f in focus.split(',')] if focus else None
            result = cnsh.fork_infinite(improvement_focus=focus_list)
            print(f"✅ 分叉创建成功")
            print(f"   子节点: {result['child_id'][:30]}...")
        
        elif cmd == 'dispute':
            content = input("争议内容: ").strip()
            parties = input("涉及方 (逗号分隔): ").strip().split(',')
            entity = input("原始实体: ").strip()
            result = cnsh.process_dispute(content, parties, entity)
            print(f"✅ 争议已处理")
            print(f"   松分叉: {result['loose_fork']['fork_id'][:30]}...")
            print(f"   紧分叉: {result['tight_fork']['fork_id'][:30]}...")
        
        elif cmd == 'p0':
            p0 = cnsh.get_p0_status()
            print(f"P0红线总数: {p0['total_lines']}")
            print(f"总违规次数: {p0['total_violations']}")
            for line_id, line_info in p0['p0_lines'].items():
                print(f"   {line_info['description']}: 违规{line_info['violation_count']}次")
        
        elif cmd == 'help':
            print("可用命令:")
            print("   status  - 查看系统状态")
            print("   fork    - 创建新分叉")
            print("   dispute - 处理争议")
            print("   p0      - 检查P0状态")
            print("   help    - 显示帮助")
            print("   quit    - 退出")
        
        else:
            print(f"未知命令: {cmd}")
            print("输入 'help' 查看可用命令")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 再见! 祖师爷与你同在。")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)
