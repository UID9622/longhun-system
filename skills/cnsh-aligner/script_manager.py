#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-

"""
龍魂脚本管理器 (LongHun Script Manager)
自动扫描、对齐、验证所有系统脚本

DNA:#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-SCRIPT-MANAGER-FILE1-v1.0
主权人: UID9622 · 龍芯北辰
"""

import os
import json
import glob
from datetime import datetime
from pathlib import Path
from cnsh_aligner import CNSHAligner, AuditColor

class ScriptManager:
    """脚本管理和对齐系统"""
    
    def __init__(self, script_dir: str = '/mnt/user-data/outputs'):
        self.script_dir = script_dir
        self.aligner = CNSHAligner()
        self.dna = "#龍芯⚡️丙午·癸巳·丁未·丙午·䷖剥-SCRIPT-MANAGER-v1.0"
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 脚本分类
        self.script_categories = {
            'shell': {
                'patterns': ['*.sh'],
                'priority': 'P1',
                'description': '系统基础脚本'
            },
            'python': {
                'patterns': ['*.py'],
                'priority': 'P1',
                'description': 'Python执行脚本'
            },
            'html': {
                'patterns': ['*.html'],
                'priority': 'P2',
                'description': '前端交互页面'
            },
            'markdown': {
                'patterns': ['*.md'],
                'priority': 'P3',
                'description': '文档和说明'
            },
            'json': {
                'patterns': ['*.json'],
                'priority': 'P3',
                'description': '配置和数据'
            }
        }
        
        # 扫描结果
        self.scan_results = {
            'dna': self.dna,
            'timestamp': self.timestamp,
            'total_scripts': 0,
            'by_category': {},
            'alignment_status': {},
            'recommendations': []
        }
    
    def scan_all_scripts(self) -> Dict[str, Any]:
        """扫描所有脚本"""
        print(f"\n{'='*70}")
        print(f"龍魂系统脚本扫描和对齐 [{self.timestamp}]")
        print(f"{'='*70}\n")
        
        all_scripts = []
        
        for category, meta in self.script_categories.items():
            scripts_in_category = []
            
            for pattern in meta['patterns']:
                full_pattern = os.path.join(self.script_dir, pattern)
                scripts = glob.glob(full_pattern)
                scripts_in_category.extend(scripts)
            
            if scripts_in_category:
                self.scan_results['by_category'][category] = {
                    'count': len(scripts_in_category),
                    'priority': meta['priority'],
                    'description': meta['description'],
                    'scripts': scripts_in_category
                }
                all_scripts.extend(scripts_in_category)
                print(f"✓ {category.upper()}: {len(scripts_in_category)} 个脚本")
        
        self.scan_results['total_scripts'] = len(all_scripts)
        return all_scripts
    
    def align_script(self, script_path: str) -> Dict[str, Any]:
        """对齐单个脚本"""
        
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {
                'path': script_path,
                'status': '🔴 读取失败',
                'error': str(e)
            }
        
        # 获取脚本信息
        script_name = os.path.basename(script_path)
        ext = os.path.splitext(script_name)[1]
        
        # 执行对齐
        result = self.aligner.align_and_correct(
            content,
            context=script_name
        )
        
        # 提取关键信息
        alignment_report = {
            'path': script_path,
            'name': script_name,
            'type': ext,
            'confidence': result['confidence'],
            'color': result['color'].value,
            'issues_count': len(result['all_issues']),
            'issues': result['all_issues'][:5],  # 前5个问题
            'suggestion': result['suggestion'],
            'can_execute': result['color'] != AuditColor.RED
        }
        
        return alignment_report
    
    def generate_alignment_report(self, all_results: List[Dict]) -> str:
        """生成总体对齐报告"""
        
        report = []
        report.append('\n' + '='*70)
        report.append('龍魂系统对齐报告 (CNSH Alignment Report)')
        report.append('='*70)
        report.append(f"执行时间: {self.timestamp}")
        report.append(f"DNA: {self.dna}\n")
        
        # 统计
        total = len(all_results)
        green_count = sum(1 for r in all_results if r['color'] == '🟢')
        yellow_count = sum(1 for r in all_results if r['color'] == '🡡')
        red_count = sum(1 for r in all_results if r['color'] == '🔴')
        
        report.append('【总体统计】')
        report.append(f"  总脚本数: {total}")
        report.append(f"  🟢 通过: {green_count} ({green_count/total*100:.0f}%)")
        report.append(f"  🡡 警告: {yellow_count} ({yellow_count/total*100:.0f}%)")
        report.append(f"  🔴 失败: {red_count} ({red_count/total*100:.0f}%)")
        
        report.append('\n【按类别统计】')
        for category, info in self.scan_results['by_category'].items():
            scripts = info['scripts']
            cat_results = [r for r in all_results if any(s in r['path'] for s in scripts)]
            if cat_results:
                avg_conf = sum(r['confidence'] for r in cat_results) / len(cat_results)
                report.append(f"  {category.upper()}: {len(cat_results)} 个 | "
                            f"平均信度 {avg_conf:.0%} | {info['priority']}")
        
        report.append('\n【需要修正的脚本】')
        for r in all_results:
            if r['color'] != '🟢':
                report.append(f"  {r['color']} {r['name']}")
                if r['issues']:
                    for issue in r['issues'][:2]:
                        report.append(f"      ⚠️  {issue}")
        
        report.append('\n【执行建议】')
        report.append('  优先级: SYS (P1) > RUN (P2) > SEM (P3)')
        report.append('  通过条件: 🟢绿灯或🡡黄灯可执行; 🔴红灯必须修正')
        report.append('  修正流程: 查看问题 → 运行修复命令 → 重新扫描')
        
        report.append('\n' + '='*70)
        return '\n'.join(report)
    
    def get_task_execution_order(self) -> str:
        """获取任务执行顺序"""
        order = """
【推荐执行顺序】(基于CNSH对齐优先级)

🔥 第一轮 (P1基础设施):
  1. SYS-002: dna_verify.sh       (DNA验证核心)
  2. SYS-001: health_check.sh     (依赖dna_verify)
  3. SYS-003: system_registry     (并行运行)

⚡ 第二轮 (P2运行时):
  4. RUN-002: DNA生成引擎         (依赖dna_verify)
  5. RUN-003: 动态调节器v3.1      (依赖DNA生成)
  6. RUN-001: m262_console        (前端对接)

📚 第三轮 (P3语义层):
  7. SEM-001: 权重算法v3.1        (理论验证)
  8. SEM-002: 草日志审计          (日志系统)
  9. SEM-003: 熔断规则检查        (安全底线)

【快速检查】:
  bash health_check.sh --quick
  # 如果所有都是🟢，说明系统对齐了
  
【完整检查】:
  python3 script_manager.py --full
  # 生成详细报告，包含所有问题和修复建议
"""
        return order


# ═══ CLI接口 ═══
def main():
    import sys
    
    manager = ScriptManager()
    
    # 扫描所有脚本
    scripts = manager.scan_all_scripts()
    
    print(f"\n开始对齐 {len(scripts)} 个脚本...\n")
    
    all_results = []
    for i, script_path in enumerate(scripts, 1):
        result = manager.align_script(script_path)
        all_results.append(result)
        
        # 进度显示
        status = result.get('color', '❓')
        name = result.get('name', '未知')
        conf = result.get('confidence', 0)
        
        print(f"  [{i:2d}/{len(scripts)}] {status} {name:30s} | "
              f"信度 {conf:.0%} | {result.get('issues_count', 0)} 问题")
    
    # 生成报告
    report = manager.generate_alignment_report(all_results)
    print(report)
    
    # 保存报告
    report_path = '/mnt/user-data/outputs/cnsh_alignment_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✅ 报告已保存: {report_path}")
    
    # 打印执行顺序
    print(manager.get_task_execution_order())
    
    # 返回状态码
    red_count = sum(1 for r in all_results if r['color'] == '🔴')
    return 0 if red_count == 0 else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
