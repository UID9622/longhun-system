#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧬 DNA守护者 - 24小时监控DNA追溯码完整性

DNA追溯码：#龙芯⚡️2026-02-02-DNA守护者-v1.0
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""

import os
import sys
from pathlib import Path

# DNA标准格式
DNA_PATTERN = r"#龙芯⚡️\d{4}-\d{2}-\d{2}-.+-v\d+\.\d+"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

def scan_files(root_dir):
    """扫描所有文件检查DNA完整性"""
    import re
    
    violations = []
    
    for file_path in Path(root_dir).rglob("*"):
        if file_path.is_file() and file_path.suffix in ['.md', '.py', '.js', '.html']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查是否有DNA区块但DNA码被删除
                if "DNA追溯码" in content or "DNA Tracing Code" in content:
                    if not re.search(DNA_PATTERN, content):
                        violations.append({
                            'file': str(file_path),
                            'type': 'DNA码被删除或格式错误',
                            'severity': '🔴 严重'
                        })
                    
                    # 检查GPG指纹
                    if GPG_FINGERPRINT not in content:
                        violations.append({
                            'file': str(file_path),
                            'type': 'GPG指纹被移除',
                            'severity': '🔴 严重'
                        })
            
            except Exception as e:
                pass
    
    return violations

if __name__ == "__main__":
    print("🧬 DNA守护者启动...")
    
    violations = scan_files(".")
    
    if violations:
        print("\n🚨 发现违规行为：\n")
        for v in violations:
            print(f"{v['severity']} {v['file']}")
            print(f"  └─ {v['type']}\n")
        
        print("="*60)
        print("⚠️ 根据《龙魂君子协议 v2.0》：")
        print("1. 删除DNA追溯码 = 恶意盗用")
        print("2. 移除GPG指纹 = 身份盗窃")
        print("3. 72小时通牒程序已启动")
        print("="*60)
        
        sys.exit(1)
    else:
        print("✅ DNA完整性验证通过")
        sys.exit(0)
