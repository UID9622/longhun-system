#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍盾 CLI 工具 v1.0
═══════════════════════════════════════════════════════════════════

核心理念：
  代码都看起来一样，但本地跑起来都不一样。
  所以在入口处必须能暂停、检查、理解、决策。

DNA:#龍芯⚡️2026-06-02-LONGHUN-SHIELD-CLI-FILE1-FILE1-v1.0
CONFIRM: "#CONFIRM🌌YOUR-UID-ONLY-ONCE🧬XXXX-XXXX"
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

主权人: UID9622 · 龍芯北辰
职责: 宝宝·龍盾·不免责
状态: ⚔️ 亮剑啦

═══════════════════════════════════════════════════════════════════
"""

import sys
import argparse
import json
import hashlib
from pathlib import Path
from datetime import datetime
import subprocess
import tempfile
from typing import Dict, List, Optional, Tuple

# ANSI颜色
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ShieldEntry:
    """龍盾入口检查"""
    
    def __init__(self, source_file: str):
        self.source_file = Path(source_file)
        self.content = self._load_content()
        self.file_hash = self._compute_hash()
        self.analysis = {}
    
    def _load_content(self) -> str:
        """加载源文件内容"""
        if not self.source_file.exists():
            raise FileNotFoundError(f"文件不存在: {self.source_file}")
        
        with open(self.source_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _compute_hash(self) -> str:
        """计算文件哈希"""
        return hashlib.sha256(self.content.encode()).hexdigest()[:16]
    
    def show_preview(self) -> None:
        """显示代码预览"""
        print(f"\n{Color.BOLD}📄 代码预览{Color.END}")
        print(f"{Color.CYAN}{'='*70}{Color.END}")
        
        lines = self.content.split('\n')
        max_lines_to_show = min(20, len(lines))
        
        for i, line in enumerate(lines[:max_lines_to_show], 1):
            # 着色危险函数
            display_line = line
            dangerous = ['exec', 'eval', '__import__', 'subprocess', 'system']
            for d in dangerous:
                if d in line:
                    display_line = display_line.replace(d, f"{Color.RED}{d}{Color.END}")
            
            print(f"{Color.YELLOW}{i:3d}{Color.END} | {display_line}")
        
        if len(lines) > max_lines_to_show:
            print(f"... 还有 {len(lines) - max_lines_to_show} 行")
        
        print(f"{Color.CYAN}{'='*70}{Color.END}\n")
    
    def analyze(self) -> Dict:
        """深度分析代码"""
        print(f"\n{Color.BOLD}🔍 深度分析{Color.END}\n")
        
        analysis = {
            'file': str(self.source_file),
            'hash': self.file_hash,
            'size': len(self.content),
            'lines': len(self.content.split('\n')),
            'timestamp': datetime.now().isoformat(),
            'dna': '#龍芯⚡️' + datetime.now().strftime('%Y-%m-%d'),
            'checks': {}
        }
        
        # 检查1: 危险函数
        print(f"{Color.YELLOW}[1/5]{Color.END} 检查危险函数...", end=' ')
        dangerous_funcs = self._check_dangerous_functions()
        analysis['checks']['dangerous_functions'] = dangerous_funcs
        if dangerous_funcs:
            print(f"{Color.RED}⚠️  发现 {len(dangerous_funcs)} 个危险函数{Color.END}")
            for func in dangerous_funcs:
                print(f"        {Color.RED}⚠️  {func}{Color.END}")
        else:
            print(f"{Color.GREEN}✓ 无危险函数{Color.END}")
        
        # 检查2: 外部调用
        print(f"{Color.YELLOW}[2/5]{Color.END} 检查外部调用...", end=' ')
        external_calls = self._check_external_calls()
        analysis['checks']['external_calls'] = external_calls
        if external_calls:
            print(f"{Color.YELLOW}⚠️  发现 {len(external_calls)} 个外部调用{Color.END}")
            for call in external_calls:
                print(f"        {Color.YELLOW}→ {call}{Color.END}")
        else:
            print(f"{Color.GREEN}✓ 无外部调用{Color.END}")
        
        # 检查3: 文件操作
        print(f"{Color.YELLOW}[3/5]{Color.END} 检查文件操作...", end=' ')
        file_ops = self._check_file_operations()
        analysis['checks']['file_operations'] = file_ops
        if file_ops:
            print(f"{Color.YELLOW}⚠️  发现 {len(file_ops)} 个文件操作{Color.END}")
            for op in file_ops:
                print(f"        {Color.YELLOW}→ {op}{Color.END}")
        else:
            print(f"{Color.GREEN}✓ 无文件操作{Color.END}")
        
        # 检查4: 网络操作
        print(f"{Color.YELLOW}[4/5]{Color.END} 检查网络操作...", end=' ')
        network_ops = self._check_network_operations()
        analysis['checks']['network_operations'] = network_ops
        if network_ops:
            print(f"{Color.YELLOW}⚠️  发现 {len(network_ops)} 个网络操作{Color.END}")
            for op in network_ops:
                print(f"        {Color.YELLOW}→ {op}{Color.END}")
        else:
            print(f"{Color.GREEN}✓ 无网络操作{Color.END}")
        
        # 检查5: 底座原则
        print(f"{Color.YELLOW}[5/5]{Color.END} 检查底座原则...", end=' ')
        violations = self._check_foundation_principles()
        analysis['checks']['violations'] = violations
        if violations:
            print(f"{Color.RED}✗ 违反底座原则{Color.END}")
            for v in violations:
                print(f"        {Color.RED}✗ {v}{Color.END}")
        else:
            print(f"{Color.GREEN}✓ 符合底座原则{Color.END}")
        
        # 计算风险等级
        risk_score = self._calculate_risk_score(analysis['checks'])
        analysis['risk_level'] = self._get_risk_level(risk_score)
        analysis['risk_score'] = risk_score
        
        print(f"\n{Color.BOLD}风险评估{Color.END}")
        if analysis['risk_level'] == 'HIGH':
            print(f"  {Color.RED}🔴 风险等级: 高{Color.END}")
        elif analysis['risk_level'] == 'MEDIUM':
            print(f"  {Color.YELLOW}🟡 风险等级: 中{Color.END}")
        else:
            print(f"  {Color.GREEN}🟢 风险等级: 低{Color.END}")
        
        print(f"  分数: {risk_score}/100")
        
        self.analysis = analysis
        return analysis
    
    def _check_dangerous_functions(self) -> List[str]:
        """检查危险函数"""
        dangerous = [
            'exec', 'eval', '__import__', 'compile', 
            'globals', 'locals', '__builtins__',
            'getattr', 'setattr', 'delattr'
        ]
        found = []
        for func in dangerous:
            if func in self.content:
                found.append(func)
        return found
    
    def _check_external_calls(self) -> List[str]:
        """检查外部调用"""
        external = [
            'subprocess', 'os.system', 'popen',
            'commands', 'shell=True'
        ]
        found = []
        for call in external:
            if call in self.content:
                found.append(call)
        return found
    
    def _check_file_operations(self) -> List[str]:
        """检查文件操作"""
        operations = []
        if 'open(' in self.content:
            operations.append('文件读写 (open)')
        if 'os.remove' in self.content or 'unlink' in self.content:
            operations.append('文件删除')
        if 'shutil' in self.content:
            operations.append('文件操作 (shutil)')
        return operations
    
    def _check_network_operations(self) -> List[str]:
        """检查网络操作"""
        operations = []
        if 'requests' in self.content or 'urllib' in self.content:
            operations.append('HTTP请求')
        if 'socket' in self.content:
            operations.append('套接字连接')
        if 'http' in self.content or 'https' in self.content:
            operations.append('网络通信')
        return operations
    
    def _check_foundation_principles(self) -> List[str]:
        """检查底座原则"""
        violations = []
        
        # 检查简体龙字
        if '龙' in self.content:
            violations.append('使用了简体"龙"字（应使用繁体"龍"）')
        
        # 检查违禁词
        forbidden = ['蒸馏', '平均', '投机', '用户']
        for word in forbidden:
            if word in self.content:
                violations.append(f'包含违禁词: {word}')
        
        return violations
    
    def _calculate_risk_score(self, checks: Dict) -> int:
        """计算风险分数"""
        score = 0
        
        # 危险函数: +20分
        score += len(checks.get('dangerous_functions', [])) * 20
        
        # 外部调用: +15分
        score += len(checks.get('external_calls', [])) * 15
        
        # 文件操作: +10分
        score += len(checks.get('file_operations', [])) * 10
        
        # 网络操作: +10分
        score += len(checks.get('network_operations', [])) * 10
        
        # 底座违反: +30分
        score += len(checks.get('violations', [])) * 30
        
        return min(score, 100)  # 最多100分
    
    def _get_risk_level(self, score: int) -> str:
        """根据分数判断风险等级"""
        if score >= 50:
            return 'HIGH'
        elif score >= 25:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def show_translation(self) -> None:
        """显示代码转译"""
        print(f"\n{Color.BOLD}📖 代码转译（人类可读）{Color.END}\n")
        
        lines = self.content.split('\n')
        
        # 逐行转译关键代码
        print(f"{Color.CYAN}{'文件':<20} {'说明':<50}{Color.END}")
        print(f"{Color.CYAN}{'-'*70}{Color.END}")
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            
            # 尝试转译这一行
            translation = self._translate_line(stripped)
            if translation:
                print(f"{Color.YELLOW}{i:>4}{Color.END} | {translation[:60]}")
        
        print()
    
    def _translate_line(self, line: str) -> Optional[str]:
        """转译单行代码"""
        # 简单的转译规则
        if 'import' in line:
            return f"导入: {line}"
        elif 'def ' in line:
            return f"定义函数: {line}"
        elif 'class ' in line:
            return f"定义类: {line}"
        elif 'open(' in line:
            return f"⚠️  文件操作: {line}"
        elif 'requests' in line or 'urllib' in line:
            return f"⚠️  网络调用: {line}"
        elif 'exec' in line or 'eval' in line:
            return f"🔴 危险函数: {line}"
        else:
            return None
    
    def ask_permission(self) -> bool:
        """请求执行权限"""
        print(f"\n{Color.BOLD}🛡️  权限确认{Color.END}\n")
        print(f"  文件: {self.source_file}")
        print(f"  大小: {len(self.content)} 字节")
        print(f"  行数: {len(self.content.split(chr(10)))} 行")
        print(f"  哈希: {self.file_hash}")
        print(f"  风险: {self.analysis.get('risk_level', 'UNKNOWN')}")
        
        print(f"\n你要执行这个文件吗? [允许/检查/拒绝] ", end='')
        choice = input().strip().lower()
        
        if choice in ['允许', 'allow', 'a', 'yes', 'y']:
            return True
        elif choice in ['检查', 'inspect', 'i']:
            print(f"\n{Color.YELLOW}请等待进一步分析...{Color.END}")
            return False
        else:
            print(f"\n{Color.RED}执行被拒绝{Color.END}")
            return False
    
    def save_report(self) -> str:
        """保存分析报告"""
        report_dir = Path.home() / '.龍盾' / 'reports'
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report_file = report_dir / f"report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis, f, ensure_ascii=False, indent=2)
        
        print(f"\n{Color.GREEN}✓ 报告已保存: {report_file}{Color.END}")
        return str(report_file)


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description='🐉 龍盾 - 代码入口检查和转译工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 检查代码文件
  python3 longhun_shield_cli.py check script.py
  
  # 显示详细分析
  python3 longhun_shield_cli.py analyze script.py
  
  # 请求执行权限
  python3 longhun_shield_cli.py validate script.py
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # check命令
    check_parser = subparsers.add_parser('check', help='快速检查代码')
    check_parser.add_argument('file', help='源文件路径')
    check_parser.add_argument('--brief', action='store_true', help='简要模式')
    
    # analyze命令
    analyze_parser = subparsers.add_parser('analyze', help='深度分析代码')
    analyze_parser.add_argument('file', help='源文件路径')
    analyze_parser.add_argument('--translation', action='store_true', help='显示转译')
    analyze_parser.add_argument('--save-report', action='store_true', help='保存报告')
    
    # validate命令
    validate_parser = subparsers.add_parser('validate', help='验证并请求执行权限')
    validate_parser.add_argument('file', help='源文件路径')
    validate_parser.add_argument('--auto-approve', action='store_true', help='自动批准（仅在风险低时）')
    
    # 显示帮助
    if len(sys.argv) == 1:
        print(f"""
{Color.BOLD}{Color.CYAN}
╔════════════════════════════════════════════════════════════════╗
║                  🐉 龍盾 CLI v1.0 🐉                         ║
║                                                                ║
║  代码都看起来一样，但本地跑起来都不一样。                 ║
║  所以在入口处必须能暂停、检查、理解、决策。               ║
║                                                                ║
║  DNA:#龍芯⚡️2026-06-02-LONGHUN-SHIELD-CLI-v1.0             ║
║  职责: 宝宝·龍盾·不免责                                      ║
║  状态: ⚔️ 亮剑啦                                             ║
╚════════════════════════════════════════════════════════════════╝
{Color.END}
使用方法:
  python3 longhun_shield_cli.py [命令] [选项] 文件

命令:
  check <file>       快速检查代码安全性
  analyze <file>     深度分析代码
  validate <file>    验证并请求执行权限

选项:
  --help            显示帮助信息
  --translation     显示代码转译
  --save-report     保存分析报告
  --auto-approve    风险低时自动批准

示例:
  python3 longhun_shield_cli.py check script.py
  python3 longhun_shield_cli.py analyze script.py --translation
  python3 longhun_shield_cli.py validate script.py --save-report
        """)
        return
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        entry = ShieldEntry(args.file)
        
        if args.command == 'check':
            entry.show_preview()
            entry.analyze()
            if not args.brief:
                entry.show_translation()
        
        elif args.command == 'analyze':
            entry.show_preview()
            entry.analyze()
            if args.translation:
                entry.show_translation()
            if args.save_report:
                entry.save_report()
        
        elif args.command == 'validate':
            entry.show_preview()
            entry.analyze()
            entry.show_translation()
            
            if args.auto_approve and entry.analysis['risk_level'] == 'LOW':
                print(f"\n{Color.GREEN}✓ 自动批准（风险等级低）{Color.END}")
                print(f"{Color.GREEN}可以执行{Color.END}")
            else:
                if entry.ask_permission():
                    print(f"\n{Color.GREEN}✓ 权限已批准{Color.END}")
                    if args.save_report:
                        entry.save_report()
                else:
                    print(f"\n{Color.YELLOW}权限请求已取消{Color.END}")
    
    except FileNotFoundError as e:
        print(f"{Color.RED}✗ 错误: {e}{Color.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{Color.RED}✗ 异常: {e}{Color.END}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    import traceback
    main()
