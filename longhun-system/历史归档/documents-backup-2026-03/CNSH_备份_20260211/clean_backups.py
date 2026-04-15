#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 清理备份文件脚本 - Python版本
DNA追溯码: #ZHUGEXIN⚡️2026-02-09-CLEAN-BACKUPS-v1.1
功能: 清理系统中的备份文件，释放磁盘空间
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path("/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器")

def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def clean_backup_files():
    """清理备份文件"""
    print("\n" + "=" * 70)
    print("🔥 清理备份文件脚本")
    print("=" * 70)
    print(f"\n项目目录: {PROJECT_ROOT}")
    print(f"扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. 查找 .backup 文件
    print("📊 统计备份文件...")
    backup_files = []
    total_size = 0
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # 跳过 .git 和 node_modules 目录
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__']]
        
        for file in files:
            if file.endswith('.backup'):
                file_path = Path(root) / file
                file_size = file_path.stat().st_size
                backup_files.append(file_path)
                total_size += file_size
    
    print(f"   备份文件数量: {len(backup_files)}")
    print(f"   备份文件总大小: {format_size(total_size)}")
    print()
    
    if len(backup_files) == 0:
        print("✅ 没有找到备份文件，无需清理")
        return
    
    # 2. 询问用户
    print("⚠️  将要删除以下备份文件:")
    for i, file_path in enumerate(backup_files[:10], 1):
        file_size = file_path.stat().st_size
        print(f"   {i}. {file_path.relative_to(PROJECT_ROOT)} ({format_size(file_size)})")
    
    if len(backup_files) > 10:
        print(f"   ... 还有 {len(backup_files) - 10} 个文件")
    
    print()
    
    # 3. 确认删除
    print("是否继续？[y/N]")
    confirm = input("> ").strip().lower()
    
    if confirm != 'y' and confirm != 'Y':
        print("⏸️ 已取消")
        return
    
    print()
    print("🧹 开始清理...")
    
    # 4. 删除备份文件
    deleted_count = 0
    deleted_size = 0
    
    for file_path in backup_files:
        try:
            file_size = file_path.stat().st_size
            file_path.unlink()
            print(f"   ✓ 已删除: {file_path.relative_to(PROJECT_ROOT)}")
            deleted_count += 1
            deleted_size += file_size
        except Exception as e:
            print(f"   ✗ 删除失败: {file_path.relative_to(PROJECT_ROOT)} - {e}")
    
    # 5. 清理 backups/ 目录
    backup_dir = PROJECT_ROOT / "backups"
    if backup_dir.exists():
        print()
        print(f"🧹 清理 backups/ 目录...")
        try:
            dir_size = sum(f.stat().st_size for f in backup_dir.rglob('*') if f.is_file())
            shutil.rmtree(backup_dir)
            print(f"   ✓ 已删除: {backup_dir.relative_to(PROJECT_ROOT)} ({format_size(dir_size)})")
            deleted_size += dir_size
        except Exception as e:
            print(f"   ✗ 删除失败: {backup_dir} - {e}")
    
    # 6. 完成
    print()
    print("=" * 70)
    print(f"✅ 清理完成！")
    print(f"   删除文件: {deleted_count} 个")
    print(f"   释放空间: {format_size(deleted_size)}")
    print("=" * 70)
    print()
    print("💡 提示:")
    print("   1. cnsh_cleaner.py 现在默认不会创建备份")
    print("   2. 如需备份，请使用: python cnsh_cleaner.py clean 文件名.md --backup")
    print()

if __name__ == "__main__":
    clean_backup_files()
