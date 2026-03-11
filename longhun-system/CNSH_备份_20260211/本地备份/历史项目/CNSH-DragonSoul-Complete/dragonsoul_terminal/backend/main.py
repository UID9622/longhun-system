#!/usr/bin/env python3
"""
🐉 龙魂终端主程序 | DragonSoul Terminal Main
DNA追溯码: #龙芯⚡️2026-01-21-MAIN-v2.0

统一入口，整合所有功能
"""

import os
import sys
import asyncio
import argparse
from datetime import datetime
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入核心模块
from security_core.audit_engine import ThreeColorAuditEngine, AuditLevel
from security_core.dna_tracer import DNATracer, OperationType
from dragonsoul_terminal.backend.mac_manager import MacManager
from dragonsoul_terminal.backend.five_backends import FiveBackendsScheduler, TaskType


class DragonSoulTerminal:
    """龙魂终端主类"""
    
    def __init__(self):
        self.version = "2.0.0"
        self.dna_code = "#龙芯⚡️2026-01-21-DragonSoul-v2.0"
        
        # 初始化组件
        self.audit_engine = ThreeColorAuditEngine()
        self.dna_tracer = DNATracer()
        self.mac_manager = MacManager()
        self.ai_scheduler = FiveBackendsScheduler()
        
        # 记录启动
        self.startup_dna = self.dna_tracer.start_trace(
            operator="DragonSoul",
            operation_type=OperationType.SYSTEM,
            detail="系统启动"
        )
    
    def print_banner(self):
        """打印启动横幅"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🐉 龙魂终端 DragonSoul Terminal v{version}                  ║
║                                                              ║
║   CNSH编辑器 + 龙魂终端 + Notion扩展 = 完整体                ║
║                                                              ║
║   🛡️ 三色审计   🧬 DNA追溯   🔐 七维加密                     ║
║                                                              ║
║   DNA: {dna}                                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """.format(version=self.version, dna=self.dna_code[:40])
        
        print(banner)
    
    def show_status(self):
        """显示系统状态"""
        print("\n📊 系统状态")
        print("=" * 50)
        
        # 五大后台状态
        print("\n🤖 五大后台:")
        for name, status in self.ai_scheduler.get_status().items():
            print(f"   {status['status']} {status['name']} (优先级: {status['priority']})")
        
        # 系统信息
        print("\n🍎 Mac系统:")
        info = self.mac_manager.get_system_info()
        print(f"   系统版本: macOS {info.get('os_version', 'N/A')}")
        if "disk" in info:
            print(f"   磁盘使用: {info['disk']['used']} / {info['disk']['total']}")
        
        # 安全状态
        print("\n🛡️ 安全状态:")
        print("   三色审计: ✅ 已启用")
        print("   DNA追溯: ✅ 已启用")
        print("   数据主权: 🇨🇳 中国境内")
    
    async def interactive_mode(self):
        """交互模式"""
        print("\n💬 进入交互模式 (输入 'help' 查看命令, 'quit' 退出)")
        print("-" * 50)
        
        while True:
            try:
                # 获取用户输入
                user_input = input("\n🐉 龙魂> ").strip()
                
                if not user_input:
                    continue
                
                # 退出
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 再见！")
                    break
                
                # 帮助
                if user_input.lower() == 'help':
                    self.show_help()
                    continue
                
                # 状态
                if user_input.lower() == 'status':
                    self.show_status()
                    continue
                
                # 清理缓存
                if user_input.lower() in ['clean', 'clean cache', '清理缓存']:
                    await self.clean_cache_interactive()
                    continue
                
                # AI对话
                if user_input.startswith('ask ') or user_input.startswith('问 '):
                    prompt = user_input[4:] if user_input.startswith('ask ') else user_input[2:]
                    await self.ask_ai(prompt)
                    continue
                
                # 审计
                if user_input.startswith('audit ') or user_input.startswith('审计 '):
                    content = user_input[6:] if user_input.startswith('audit ') else user_input[3:]
                    self.audit_content(content)
                    continue
                
                # 未知命令
                print(f"❓ 未知命令: {user_input}")
                print("   输入 'help' 查看可用命令")
                
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 错误: {e}")
    
    def show_help(self):
        """显示帮助"""
        help_text = """
📖 可用命令:

  status          - 显示系统状态
  clean           - 清理Mac缓存
  ask <问题>      - 向AI提问
  问 <问题>       - 向AI提问（中文）
  audit <内容>    - 审计内容安全性
  审计 <内容>     - 审计内容安全性（中文）
  help            - 显示此帮助
  quit/exit/q     - 退出

示例:
  ask 帮我分析这段代码
  审计 rm -rf /
  clean
        """
        print(help_text)
    
    async def clean_cache_interactive(self):
        """交互式清理缓存"""
        # 预览
        print("\n🧹 正在分析可清理的缓存...")
        result = self.mac_manager.clean_cache(dry_run=True)
        
        size_str = self.mac_manager._format_size(result.cleaned_size)
        print(f"   可清理: {size_str} ({len(result.cleaned_items)} 项)")
        print(f"   DNA追溯码: {result.dna_code}")
        
        # 确认
        confirm = input("\n是否执行清理？[y/N] ").strip().lower()
        
        if confirm == 'y':
            result = self.mac_manager.clean_cache(dry_run=False)
            print(f"✅ 已清理 {self.mac_manager._format_size(result.cleaned_size)}")
        else:
            print("⏸️ 已取消")
    
    async def ask_ai(self, prompt: str):
        """向AI提问"""
        print(f"\n🤔 正在思考...")
        
        result = await self.ai_scheduler.execute_task(
            TaskType.CHAT,
            prompt
        )
        
        if result["success"]:
            print(f"\n🤖 [{result['backend']}]:")
            print(result["result"].get("response", "无响应"))
            print(f"\n🧬 DNA: {result['dna_code']}")
        else:
            print(f"❌ 错误: {result.get('error', '未知错误')}")
    
    def audit_content(self, content: str):
        """审计内容"""
        result = self.audit_engine.audit(content)
        
        print(f"\n🛡️ 审计结果: {result.level.value}")
        print(f"   原因: {result.reason}")
        print(f"   DNA: {result.dna_code}")
        
        if result.suggestions:
            print(f"   建议: {result.suggestions[0]}")
    
    def run(self, args):
        """运行终端"""
        self.print_banner()
        
        if args.status:
            self.show_status()
        elif args.clean:
            result = self.mac_manager.clean_cache(dry_run=args.dry_run)
            mode = "预览" if args.dry_run else "已清理"
            print(f"{mode}: {self.mac_manager._format_size(result.cleaned_size)}")
        elif args.interactive or not any([args.status, args.clean]):
            asyncio.run(self.interactive_mode())
        
        # 记录关闭
        self.dna_tracer.end_trace(
            self.startup_dna,
            audit_result="🟢 正常关闭"
        )


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="🐉 龙魂终端 - CNSH编辑器完整体",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-s', '--status', action='store_true',
                        help='显示系统状态')
    parser.add_argument('-c', '--clean', action='store_true',
                        help='清理Mac缓存')
    parser.add_argument('--dry-run', action='store_true',
                        help='预览模式，不实际执行')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='进入交互模式')
    parser.add_argument('--dev', action='store_true',
                        help='开发模式')
    
    args = parser.parse_args()
    
    terminal = DragonSoulTerminal()
    terminal.run(args)


if __name__ == "__main__":
    main()
