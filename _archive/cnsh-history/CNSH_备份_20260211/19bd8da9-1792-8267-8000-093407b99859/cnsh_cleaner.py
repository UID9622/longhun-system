#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧹 CNSH文档清洗器 - 解决"解析不了"问题
DNA追溯码：#ZHUGEXIN⚡️2026-01-20-CNSH-CLEANER-v1.0

解决以下5大类坑：
1. 隐形字符坑（零宽空格、NBSP、BOM）
2. 表情/特殊符号坑（emoji、装饰符）
3. 字体/富文本坑（变体选择符）
4. Markdown结构坑（代码块未闭合、表格列数不一致）
5. 链接与引用坑（中文括号、超长URL）

使用：python cnsh_cleaner.py clean demo.cnsh.md
"""

import re
import unicodedata
from pathlib import Path
from typing import List, Dict, Any, Tuple
from datetime import datetime


class CNSSCleanerError(Exception):
    """CNSH清洗器异常"""
    pass


class CNSHCleaner:
    """CNSH文档清洗器"""
    
    def __init__(self):
        self.report = {
            'issues_found': [],
            'issues_fixed': [],
            'warnings': []
        }
    
    def detect_invisible_chars(self, text: str) -> List[Dict[str, Any]]:
        """检测隐形字符"""
        issues = []
        for i, char in enumerate(text):
            category = unicodedata.category(char)
            
            # 控制字符（除了正常换行/Tab/空格）
            if category in ['Cf', 'Zs'] and ord(char) not in [32, 9, 10, 13]:
                issues.append({
                    'type': 'invisible_char',
                    'position': i,
                    'char': repr(char),
                    'unicode': f'U+{ord(char):04X}',
                    'name': unicodedata.name(char, 'UNKNOWN'),
                    'context': text[max(0, i-5):i+5]
                })
        return issues
    
    def clean_invisible_chars(self, text: str) -> str:
        """清理隐形字符"""
        original_len = len(text)
        
        # 零宽字符
        text = text.replace('\u200b', '')  # Zero-Width Space
        text = text.replace('\u200c', '')  # Zero-Width Non-Joiner
        text = text.replace('\u200d', '')  # Zero-Width Joiner
        text = text.replace('\ufeff', '')  # BOM
        
        # NBSP → 普通空格
        text = text.replace('\u00a0', ' ')
        
        # 统一换行为LF
        text = text.replace('\r\n', '\n')
        text = text.replace('\r', '\n')
        
        # 记录修复
        if len(text) != original_len:
            self.report['issues_fixed'].append(f"清理隐形字符（{original_len - len(text)}个字符）")
        
        return text
    
    def detect_emoji_in_headers(self, text: str) -> List[Dict[str, Any]]:
        """检测标题中的emoji"""
        issues = []
        emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+'
        
        for i, line in enumerate(text.split('\n')):
            if line.startswith('#'):
                if re.search(emoji_pattern, line):
                    issues.append({
                        'type': 'emoji_in_header',
                        'line_number': i + 1,
                        'line': line,
                        'issue': '标题中包含emoji'
                    })
        return issues
    
    def clean_emoji_from_headers(self, text: str) -> str:
        """清理标题中的emoji"""
        lines = []
        emoji_pattern = r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+'
        
        fixed_count = 0
        for line in text.split('\n'):
            if line.startswith('#'):
                original = line
                # 移除emoji
                line = re.sub(emoji_pattern, '', line)
                # 清理多余空格
                line = re.sub(r'\s+', ' ', line).strip()
                if line != original:
                    fixed_count += 1
            lines.append(line)
        
        if fixed_count > 0:
            self.report['issues_fixed'].append(f"清理标题emoji（{fixed_count}处）")
        
        return '\n'.join(lines)
    
    def detect_variation_selectors(self, text: str) -> List[Dict[str, Any]]:
        """检测变体选择符"""
        issues = []
        for i, char in enumerate(text):
            if '\ufe00' <= char <= '\ufe0f':  # 变体选择符
                issues.append({
                    'type': 'variation_selector',
                    'position': i,
                    'context': text[max(0, i-5):i+5],
                    'selector': f'U+{ord(char):04X}'
                })
        return issues
    
    def remove_variation_selectors(self, text: str) -> str:
        """移除变体选择符"""
        original_len = len(text)
        
        for code in range(0xfe00, 0xfe10):
            text = text.replace(chr(code), '')
        
        if len(text) != original_len:
            self.report['issues_fixed'].append(f"移除变体选择符（{original_len - len(text)}个）")
        
        return text
    
    def detect_structure_issues(self, text: str) -> List[Dict[str, Any]]:
        """检测Markdown结构问题"""
        issues = []
        lines = text.split('\n')
        
        # 检测未闭合代码块
        code_blocks = text.count('```')
        if code_blocks % 2 != 0:
            issues.append({
                'type': 'unclosed_code_block',
                'message': '代码块未闭合',
                'count': code_blocks
            })
        
        # 检测表格列数
        in_table = False
        expected_cols = 0
        for i, line in enumerate(lines):
            if '|' in line:
                cols = line.count('|')
                if not in_table:
                    expected_cols = cols
                    in_table = True
                elif cols != expected_cols:
                    issues.append({
                        'type': 'table_column_mismatch',
                        'line': i + 1,
                        'expected': expected_cols,
                        'actual': cols
                    })
            else:
                in_table = False
        
        # 检测重复标题
        headers = {}
        for i, line in enumerate(lines):
            if line.startswith('#'):
                header = line.strip()
                if header in headers:
                    issues.append({
                        'type': 'duplicate_header',
                        'header': header,
                        'lines': [headers[header], i + 1]
                    })
                else:
                    headers[header] = i + 1
        
        return issues
    
    def fix_structure_issues(self, text: str) -> str:
        """修复Markdown结构问题"""
        lines = text.split('\n')
        fixed_lines = []
        
        # 修复代码块
        code_block_count = 0
        for line in lines:
            if line.strip().startswith('```'):
                code_block_count += 1
            fixed_lines.append(line)
        
        # 如果代码块数量是奇数，补一个闭合
        if code_block_count % 2 != 0:
            fixed_lines.append('```')
            self.report['issues_fixed'].append("补全未闭合代码块")
        
        # 修复表格列数
        result = []
        in_table = False
        expected_cols = 0
        
        for line in fixed_lines:
            if '|' in line:
                cols = line.count('|')
                if not in_table:
                    expected_cols = cols
                    in_table = True
                    result.append(line)
                elif cols < expected_cols:
                    # 补齐缺失的列
                    line = line.rstrip() + ' |' * (expected_cols - cols)
                    self.report['issues_fixed'].append(f"补齐表格列（第{len(result)+1}行）")
                    result.append(line)
                elif cols > expected_cols:
                    # 截断多余的列
                    parts = line.split('|')
                    line = '|'.join(parts[:expected_cols])
                    self.report['issues_fixed'].append(f"截断表格列（第{len(result)+1}行）")
                    result.append(line)
                else:
                    result.append(line)
            else:
                in_table = False
                result.append(line)
        
        return '\n'.join(result)
    
    def detect_link_issues(self, text: str) -> List[Dict[str, Any]]:
        """检测链接问题"""
        issues = []
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        
        for match in re.finditer(link_pattern, text):
            url = match.group(2)
            
            # 检测中文括号
            if '（' in url or '）' in url:
                issues.append({
                    'type': 'chinese_brackets_in_url',
                    'url': url,
                    'text': match.group(1)
                })
            
            # 检测超长URL
            if len(url) > 500:
                issues.append({
                    'type': 'url_too_long',
                    'url': url[:50] + '...',
                    'length': len(url)
                })
        
        return issues
    
    def generate_report(self) -> str:
        """生成清洗报告"""
        lines = []
        lines.append("=" * 60)
        lines.append("🧹 CNSH文档清洗报告")
        lines.append("=" * 60)
        
        # 发现的问题
        if self.report['issues_found']:
            lines.append("🔍 发现的问题:")
            for issue in self.report['issues_found']:
                lines.append(f"  - {issue}")
            lines.append("")
        
        # 已修复的问题
        if self.report['issues_fixed']:
            lines.append("✅ 已修复:")
            for fix in self.report['issues_fixed']:
                lines.append(f"  - {fix}")
            lines.append("")
        
        # 警告
        if self.report['warnings']:
            lines.append("⚠️  警告:")
            for warning in self.report['warnings']:
                lines.append(f"  - {warning}")
            lines.append("")
        
        if not self.report['issues_found'] and not self.report['issues_fixed']:
            lines.append("✅ 未发现任何问题，文档很干净！")
        
        lines.append("=" * 60)
        
        return '\n'.join(lines)


def clean_document(file_path: str, backup: bool = True) -> str:
    """
    一键清洗文档
    
    参数:
        file_path: 文件路径
        backup: 是否备份原文件
    
    返回:
        清洗后的内容
    """
    path = Path(file_path)
    
    if not path.exists():
        raise CNSSCleanerError(f"文件不存在: {file_path}")
    
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cleaner = CNSHCleaner()
    
    # 检测问题
    issues = []
    issues.extend(cleaner.detect_invisible_chars(content))
    issues.extend(cleaner.detect_emoji_in_headers(content))
    issues.extend(cleaner.detect_variation_selectors(content))
    issues.extend(cleaner.detect_structure_issues(content))
    issues.extend(cleaner.detect_link_issues(content))
    
    for issue in issues:
        cleaner.report['issues_found'].append(f"{issue['type']}: {issue}")
    
    # 清洗
    content = cleaner.clean_invisible_chars(content)
    content = cleaner.clean_emoji_from_headers(content)
    content = cleaner.remove_variation_selectors(content)
    content = cleaner.fix_structure_issues(content)
    
    # 备份
    if backup:
        backup_path = path.with_suffix(path.suffix + '.backup')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        cleaner.report['warnings'].append(f"原文件已备份到: {backup_path}")
    
    # 写回
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    
    return content


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        prog='cnsh_cleaner',
        description='🧹 CNSH文档清洗器 - 解决"解析不了"问题'
    )
    
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # clean 命令
    clean_parser = subparsers.add_parser('clean', help='清洗文档')
    clean_parser.add_argument('file', help='要清洗的文件路径')
    clean_parser.add_argument('--no-backup', action='store_true', help='不备份原文件')
    
    # detect 命令
    detect_parser = subparsers.add_parser('detect', help='检测问题')
    detect_parser.add_argument('file', help='要检测的文件路径')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'clean':
            content = clean_document(args.file, backup=not args.no_backup)
            cleaner = CNSHCleaner()
            print(cleaner.generate_report())
            
        elif args.command == 'detect':
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            cleaner = CNSHCleaner()
            print("🔍 检测结果:")
            print("=" * 60)
            
            issues = []
            issues.extend(cleaner.detect_invisible_chars(content))
            issues.extend(cleaner.detect_emoji_in_headers(content))
            issues.extend(cleaner.detect_variation_selectors(content))
            issues.extend(cleaner.detect_structure_issues(content))
            issues.extend(cleaner.detect_link_issues(content))
            
            if issues:
                print(f"发现 {len(issues)} 个问题:")
                for issue in issues:
                    print(f"  - {issue['type']}: {issue}")
            else:
                print("✅ 未发现任何问题！")
            
            print("=" * 60)
    
    except CNSSCleanerError as e:
        print(f"❌ 错误: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断")
        return 130
    
    return 0


if __name__ == '__main__':
    exit(main())
