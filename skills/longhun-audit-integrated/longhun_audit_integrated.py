#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════╗
║  龍魂完整审计系统 v2.0 (Integrated)                         ║
║  CNSH对齐检查 + 10维系统审计 融合版                         ║
║                                                             ║
║  DNA:#龍芯⚡️2026-06-02-LONGHUN-AUDIT-INTEGRATED-FILE3-v2.0   ║
║  GPG: "0000000000000000000000000000000000000000"             ║
║  CONFIRM: "#CONFIRM🌌YOUR-UID-ONLY-ONCE🧬XXXX-XXXX"              ║
╚══════════════════════════════════════════════════════════════╝

用法:
  python3 longhun_audit_integrated.py --full      # 完整审计
  python3 longhun_audit_integrated.py --script    # 仅CNSH检查
  python3 longhun_audit_integrated.py --system    # 仅系统审计
  python3 longhun_audit_integrated.py --graph     # 图形化输出
"""

import os
import sys
import json
import hashlib
import sqlite3
import time
import datetime
import platform
import subprocess
import shutil
import re
from pathlib import Path
from collections import defaultdict
from enum import Enum

# ═══════════════════════════════════════════════════════════════
# 审计颜色和置信度
# ═══════════════════════════════════════════════════════════════

class AuditColor(Enum):
    """三色审计"""
    GREEN = "🟢"    # conf >= 0.85
    YELLOW = "🡡"   # 0.60 <= conf < 0.85
    RED = "🔴"      # conf < 0.60

def tricolor(score: float) -> str:
    """分数转三色"""
    if score >= 0.85:
        return "🟢"
    elif score >= 0.60:
        return "🡡"
    else:
        return "🔴"

def score_to_bar(score: float, width: int = 20) -> str:
    """分数转ASCII进度条"""
    filled = int(score * width)
    return "█" * filled + "░" * (width - filled)

# ═══════════════════════════════════════════════════════════════
# 第一层：CNSH对齐检查（语言合规性）
# ═══════════════════════════════════════════════════════════════

class CNSHChecker:
    """CNSH语言合规性检查"""
    
    def __init__(self):
        self.dna = "#龍芯⚡️2026-06-02-CNSH-CHECKER-v2.0"
        
        # 黑名单字符
        self.banned_chars = {
            '龙': ('龍', 'L1:简体龙->繁体龍-FUSE_3'),
        }
        
        # 保留关键字
        self.cnsh_keywords = {
            '检·健·度', '路·树·构', '芯·溯·根', '生·成·器',
            '验·语法·系', '修·复·链', '冲·突·检', '注册表',
            '调节', '熔断', '草日志',
        }
        
        # 违禁词（底座检查）
        self.foundation_violations = {
            '蒸馏': 'L4:违反不蒸馏原则',
            '平均': 'L4:违反人永远是1',
            '数据点': 'L4:违反人永远是1',
            '投机': 'L4:违反不走捷径',
            '用户': 'L4:应改为某个具体的人',
        }
    
    def check(self, text: str) -> dict:
        """完整的CNSH检查"""
        result = {
            'type': 'CNSH对齐',
            'issues': [],
            'confidence': 0.85,
            'color': '🟢',
        }
        
        # L1: 字符检查
        for banned, (replacement, reason) in self.banned_chars.items():
            if banned in text:
                if banned == '龙':
                    result['confidence'] = 0.0
                    result['color'] = '🔴'
                    result['issues'].append(f'🔴 FUSE_3熔断: {reason}')
                    return result
                text = text.replace(banned, replacement)
                result['issues'].append(f'L1纠正: {banned}->{replacement}')
                result['confidence'] = 0.70
        
        # L4: 语义检查（底座原则）
        for violation_kw, reason in self.foundation_violations.items():
            if violation_kw in text:
                result['issues'].append(f'🔴 {reason}')
                result['confidence'] = 0.0
                result['color'] = '🔴'
                return result
        
        # 计算最终颜色
        result['color'] = tricolor(result['confidence'])
        return result


# ═══════════════════════════════════════════════════════════════
# 第二层：10维系统审计
# ═══════════════════════════════════════════════════════════════

class SystemAuditor:
    """10维系统审计"""
    
    def __init__(self):
        self.dna = "#龍芯⚡️2026-06-02-SYSTEM-AUDITOR-v2.0"
        self.dimensions = {
            '文件审计': self.audit_files,
            '健康审计': self.audit_health,
            '安全审计': self.audit_security,
            '合规审计': self.audit_compliance,
            '性能审计': self.audit_performance,
            '行为审计': self.audit_behavior,
            '代码审计': self.audit_code,
            '网络审计': self.audit_network,
            '依赖审计': self.audit_dependencies,
            '日志审计': self.audit_logs,
        }
    
    def audit_files(self) -> dict:
        """维度1: 文件完整性"""
        root = Path(os.path.expanduser('~/longhun-system'))
        if not root.exists():
            return {'name': '文件审计', 'confidence': 0.0, 'issues': ['系统根目录不存在']}
        
        py_files = list(root.rglob('*.py'))
        dna_count = 0
        
        for f in py_files:
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                if '#龍芯⚡️' in content:
                    dna_count += 1
            except:
                pass
        
        total = len(py_files)
        rate = dna_count / total if total > 0 else 0
        
        return {
            'name': '文件审计',
            'confidence': rate,
            'issues': [f'DNA覆盖率: {rate:.0%} ({dna_count}/{total})'],
            'details': f'共{total}个Python文件'
        }
    
    def audit_health(self) -> dict:
        """维度2: 系统健康"""
        scores = []
        issues = []
        
        # 磁盘空间
        try:
            disk = shutil.disk_usage('/')
            pct = disk.free / disk.total
            scores.append(pct if pct > 0.1 else 0)
            if pct < 0.1:
                issues.append(f'磁盘剩余不足: {pct:.0%}')
        except:
            scores.append(0.5)
        
        # 关键目录
        for d in ['~/longhun-system', '~/.龍魂']:
            if Path(os.path.expanduser(d)).exists():
                scores.append(1.0)
            else:
                scores.append(0.5)
                issues.append(f'目录缺失: {d}')
        
        conf = sum(scores) / len(scores) if scores else 0.5
        
        return {
            'name': '健康审计',
            'confidence': conf,
            'issues': issues or ['系统健康'],
            'details': f'检查{len(scores)}项'
        }
    
    def audit_security(self) -> dict:
        """维度3: 安全性"""
        issues = []
        score = 1.0
        
        # 检查权限
        db_path = os.path.expanduser('~/.龍魂/audit_cache.db')
        if os.path.exists(db_path):
            mode = oct(os.stat(db_path).st_mode)[-3:]
            if mode != '444':
                issues.append(f'数据库权限错误: {mode} (应为444)')
                score = 0.3
        
        # 检查简体字污染
        root = Path(os.path.expanduser('~/longhun-system'))
        if root.exists():
            polluted = 0
            for f in list(root.rglob('*.py'))[:50]:
                try:
                    content = f.read_text(encoding='utf-8', errors='ignore')
                    if '龙芯' in content and '#龍芯' not in content:
                        polluted += 1
                except:
                    pass
            if polluted > 0:
                issues.append(f'简体字污染: {polluted}个文件')
                score = 0.1
        
        return {
            'name': '安全审计',
            'confidence': score,
            'issues': issues or ['安全状态良好'],
            'details': '权限检查·字符检查'
        }
    
    def audit_compliance(self) -> dict:
        """维度4: 合规性（六层来源链）"""
        layers = {
            '道统': ['道德经', '易经', '曾仕强'],
            '精神': ['UID9622', '龍芯北辰', '不免责'],
            '技术': ['Python', 'CNSH', 'DNA'],
            '系统': ['权重算法', '自适应调节器'],
            '生命': ['家人', '责任', '守护'],
        }
        
        root = Path(os.path.expanduser('~/longhun-system'))
        if not root.exists():
            return {'name': '合规审计', 'confidence': 0.5, 'issues': ['系统根不存在']}
        
        layer_scores = {}
        for layer, keywords in layers.items():
            hits = 0
            total = 0
            for f in list(root.rglob('*'))[:100]:
                if f.is_file():
                    total += 1
                    try:
                        content = f.read_text(encoding='utf-8', errors='ignore')[:2000]
                        for kw in keywords:
                            if kw in content:
                                hits += 1
                                break
                    except:
                        pass
            if total > 0:
                layer_scores[layer] = hits / total
        
        overall = sum(layer_scores.values()) / len(layer_scores) if layer_scores else 0.5
        
        return {
            'name': '合规审计',
            'confidence': overall,
            'issues': [f'{k}: {v:.0%}' for k, v in layer_scores.items()],
            'details': f'{len(layer_scores)}层检查'
        }
    
    def audit_performance(self) -> dict:
        """维度5: 性能"""
        start = time.time()
        for _ in range(1000):
            hashlib.sha256(b'test').hexdigest()[:8]
        elapsed = time.time() - start
        
        rate = 1000 / elapsed if elapsed > 0 else 5000
        score = 1.0 if rate > 5000 else 0.8 if rate > 1000 else 0.5
        
        return {
            'name': '性能审计',
            'confidence': score,
            'issues': [f'DNA生成速度: {rate:.0f}次/秒'],
            'details': f'{elapsed*1000:.0f}ms/1000次'
        }
    
    def audit_behavior(self) -> dict:
        """维度6: 行为审计"""
        log_path = os.path.expanduser('~/.龍魂/audit_master.log')
        if not os.path.exists(log_path):
            return {'name': '行为审计', 'confidence': 0.8, 'issues': ['日志未创建']}
        
        try:
            with open(log_path, 'r') as f:
                lines = f.readlines()
            
            errors = sum(1 for l in lines if '🔴' in l or 'error' in l)
            conf = 1.0 if errors == 0 else max(0.5, 1.0 - errors/len(lines))
            
            return {
                'name': '行为审计',
                'confidence': conf,
                'issues': [f'日志条目: {len(lines)}条', f'错误: {errors}条'],
                'details': '审计日志完整'
            }
        except:
            return {'name': '行为审计', 'confidence': 0.6, 'issues': ['日志读取失败']}
    
    def audit_code(self) -> dict:
        """维度7: 代码审计"""
        root = Path(os.path.expanduser('~/longhun-system'))
        if not root.exists():
            return {'name': '代码审计', 'confidence': 0.0, 'issues': ['系统根不存在']}
        
        py_files = list(root.rglob('*.py'))[:50]
        syntax_ok = 0
        
        for f in py_files:
            try:
                source = f.read_text(encoding='utf-8', errors='ignore')
                compile(source, str(f), 'exec')
                syntax_ok += 1
            except SyntaxError:
                pass
        
        rate = syntax_ok / len(py_files) if py_files else 0.5
        
        return {
            'name': '代码审计',
            'confidence': rate,
            'issues': [f'语法通过: {syntax_ok}/{len(py_files)}'],
            'details': '采样检查'
        }
    
    def audit_network(self) -> dict:
        """维度8: 网络审计"""
        # 简化版：只检查基本连通性
        import socket
        
        tests = [
            ('8.8.8.8', 53, 'DNS'),
        ]
        
        success = 0
        for host, port, name in tests:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((host, port))
                sock.close()
                if result == 0:
                    success += 1
            except:
                pass
        
        conf = success / len(tests) if tests else 0.5
        
        return {
            'name': '网络审计',
            'confidence': conf,
            'issues': [f'连通性: {success}/{len(tests)}'],
            'details': '基础连接测试'
        }
    
    def audit_dependencies(self) -> dict:
        """维度9: 依赖审计"""
        required = ['hashlib', 'json', 'sqlite3', 'datetime', 'pathlib', 'os', 'sys']
        missing = []
        
        for mod in required:
            try:
                __import__(mod)
            except ImportError:
                missing.append(mod)
        
        conf = 1.0 if not missing else 0.5
        
        return {
            'name': '依赖审计',
            'confidence': conf,
            'issues': [f'必备依赖: {len(required)-len(missing)}/{len(required)}'],
            'details': (f'缺失: {missing}' if missing else '完整')
        }
    
    def audit_logs(self) -> dict:
        """维度10: 日志审计"""
        log_files = [
            os.path.expanduser('~/.龍魂/audit_master.log'),
            os.path.expanduser('~/.龍魂/草日志.jsonl'),
        ]
        
        total_size = 0
        exists = 0
        
        for lf in log_files:
            if os.path.exists(lf):
                total_size += os.path.getsize(lf)
                exists += 1
        
        conf = min(1.0, exists / len(log_files) * 0.8 + 0.2)
        
        return {
            'name': '日志审计',
            'confidence': conf,
            'issues': [f'日志文件: {exists}/{len(log_files)}'],
            'details': f'总量: {total_size/1024:.0f}KB'
        }
    
    def audit_all(self) -> list:
        """审计所有维度"""
        results = []
        for dim_name, dim_func in self.dimensions.items():
            try:
                result = dim_func()
                results.append(result)
            except Exception as e:
                results.append({
                    'name': dim_name,
                    'confidence': 0.0,
                    'issues': [f'检查异常: {str(e)[:50]}']
                })
        return results


# ═══════════════════════════════════════════════════════════════
# 融合审计主控
# ═══════════════════════════════════════════════════════════════

class LonghunIntegratedAudit:
    """龍魂完整审计系统 v2.0"""
    
    def __init__(self):
        self.dna = "#龍芯⚡️2026-06-02-LONGHUN-AUDIT-INTEGRATED-v2.0"
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cnsh_checker = CNSHChecker()
        self.system_auditor = SystemAuditor()
    
    def audit_script(self, script_path: str) -> dict:
        """审计单个脚本"""
        result = {
            'path': script_path,
            'name': os.path.basename(script_path),
            'dna': self.dna,
            'timestamp': self.timestamp,
            'layers': {}
        }
        
        # 第一层：CNSH对齐检查
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            cnsh_result = self.cnsh_checker.check(content)
            result['layers']['CNSH对齐'] = cnsh_result
        except Exception as e:
            result['layers']['CNSH对齐'] = {
                'confidence': 0.0,
                'color': '🔴',
                'issues': [f'检查失败: {str(e)[:50]}']
            }
        
        # 计算综合置信度
        result['overall_confidence'] = result['layers']['CNSH对齐']['confidence']
        result['overall_color'] = result['layers']['CNSH对齐']['color']
        result['can_execute'] = result['overall_color'] != '🔴'
        
        return result
    
    def audit_system(self) -> dict:
        """审计整个系统"""
        result = {
            'dna': self.dna,
            'timestamp': self.timestamp,
            'dimensions': {},
            'summary': {}
        }
        
        # 运行所有10维审计
        dim_results = self.system_auditor.audit_all()
        
        for dim in dim_results:
            result['dimensions'][dim['name']] = {
                'confidence': dim['confidence'],
                'color': tricolor(dim['confidence']),
                'issues': dim.get('issues', []),
                'details': dim.get('details', '')
            }
        
        # 计算汇总
        confs = [d['confidence'] for d in dim_results]
        overall = sum(confs) / len(confs) if confs else 0.5
        
        result['summary']['overall_confidence'] = overall
        result['summary']['overall_color'] = tricolor(overall)
        result['summary']['healthy_dimensions'] = sum(1 for c in confs if c >= 0.85)
        result['summary']['warning_dimensions'] = sum(1 for c in confs if 0.60 <= c < 0.85)
        result['summary']['critical_dimensions'] = sum(1 for c in confs if c < 0.60)
        
        return result
    
    def print_dashboard(self, script_result: dict = None, system_result: dict = None):
        """打印仪表盘"""
        print("\n" + "="*70)
        print("  🐉 龍魂完整审计系统 v2.0 仪表盘")
        print("="*70)
        
        if script_result:
            print("\n【脚本层CNSH对齐】")
            for layer, data in script_result['layers'].items():
                conf = data['confidence']
                color = data['color']
                print(f"  {color} {layer:20s} {score_to_bar(conf)} {conf:.0%}")
            print(f"\n  总体: {script_result['overall_color']} "
                  f"{'✅ 可执行' if script_result['can_execute'] else '❌ 拒绝'}")
        
        if system_result:
            print("\n【系统层10维审计】")
            dims = system_result['dimensions']
            for name, data in dims.items():
                conf = data['confidence']
                color = data['color']
                print(f"  {color} {name:20s} {score_to_bar(conf)} {conf:.0%}")
            
            print(f"\n【系统整体评分】")
            overall = system_result['summary']['overall_confidence']
            color = system_result['summary']['overall_color']
            print(f"  {color} 综合评分: {score_to_bar(overall)} {overall:.0%}")
            print(f"  🟢 健康维度: {system_result['summary']['healthy_dimensions']}/10")
            print(f"  🡡 警告维度: {system_result['summary']['warning_dimensions']}/10")
            print(f"  🔴 严重维度: {system_result['summary']['critical_dimensions']}/10")
        
        print("\n" + "="*70)


# ═══════════════════════════════════════════════════════════════
# CLI入口
# ═══════════════════════════════════════════════════════════════

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="龍魂完整审计系统 v2.0")
    parser.add_argument('--full', action='store_true', help='完整审计（脚本+系统）')
    parser.add_argument('--script', action='store_true', help='仅CNSH脚本审计')
    parser.add_argument('--system', action='store_true', help='仅系统10维审计')
    parser.add_argument('--graph', action='store_true', help='图形化输出')
    parser.add_argument('--file', help='指定脚本路径')
    args = parser.parse_args()
    
    if not any([args.full, args.script, args.system]):
        args.full = True
    
    auditor = LonghunIntegratedAudit()
    
    if args.full or args.script:
        if args.file:
            script_result = auditor.audit_script(args.file)
            if args.graph or args.full:
                auditor.print_dashboard(script_result=script_result)
            else:
                print(json.dumps(script_result, ensure_ascii=False, indent=2))
    
    if args.full or args.system:
        system_result = auditor.audit_system()
        if args.graph or args.full:
            auditor.print_dashboard(system_result=system_result)
        else:
            print(json.dumps(system_result, ensure_ascii=False, indent=2))
    
    print(f"\n✅ 审计完成")
    print(f"DNA: {auditor.dna}")


if __name__ == '__main__':
    main()
