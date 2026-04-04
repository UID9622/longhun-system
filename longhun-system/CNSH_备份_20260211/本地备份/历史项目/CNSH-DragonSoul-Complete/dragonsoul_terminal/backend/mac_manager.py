#!/usr/bin/env python3
"""
🍎 Mac系统管理器 | Mac System Manager
DNA追溯码: #龍芯⚡️2026-01-21-Mac管理-v2.0

功能：
- 清理系统缓存
- 管理启动项
- 监控系统资源
- 自动化操作
"""

import os
import shutil
import subprocess
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# 导入安全模块
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from security_core.audit_engine import ThreeColorAuditEngine, AuditLevel
from security_core.dna_tracer import DNATracer, OperationType


@dataclass
class CleanResult:
    """清理结果"""
    success: bool
    cleaned_size: int  # 字节
    cleaned_items: List[str]
    errors: List[str]
    dna_code: str


class MacManager:
    """Mac系统管理器"""
    
    def __init__(self):
        self.audit_engine = ThreeColorAuditEngine()
        self.dna_tracer = DNATracer()
        self.home = Path.home()
        
        # 安全的缓存目录（可清理）
        self.safe_cache_dirs = [
            self.home / "Library/Caches",
            self.home / "Library/Logs",
            Path("/private/var/folders"),  # 需要sudo
        ]
        
        # 危险目录（不能清理）
        self.dangerous_dirs = [
            self.home / "Documents",
            self.home / "Desktop",
            self.home / "Downloads",
            self.home / "Library/Application Support",
            self.home / "Library/Preferences",
            Path("/System"),
            Path("/usr"),
            Path("/bin"),
        ]
    
    def clean_cache(self, dry_run: bool = True) -> CleanResult:
        """
        清理系统缓存
        
        Args:
            dry_run: 如果为True，只预览不实际删除
        """
        dna_code = self.dna_tracer.start_trace(
            operator="MacManager",
            operation_type=OperationType.DELETE,
            detail=f"清理缓存 (dry_run={dry_run})"
        )
        
        cleaned_items = []
        errors = []
        total_size = 0
        
        for cache_dir in self.safe_cache_dirs:
            if not cache_dir.exists():
                continue
            
            # 审计
            audit = self.audit_engine.audit(f"清理目录: {cache_dir}")
            if audit.level == AuditLevel.RED:
                errors.append(f"审计不通过: {cache_dir}")
                continue
            
            try:
                # 遍历缓存目录
                for item in cache_dir.iterdir():
                    try:
                        # 跳过系统关键文件
                        if self._is_system_critical(item):
                            continue
                        
                        # 计算大小
                        size = self._get_size(item)
                        total_size += size
                        
                        if not dry_run:
                            # 实际删除
                            if item.is_dir():
                                shutil.rmtree(item, ignore_errors=True)
                            else:
                                item.unlink(missing_ok=True)
                        
                        cleaned_items.append(str(item))
                        
                    except PermissionError:
                        errors.append(f"权限不足: {item}")
                    except Exception as e:
                        errors.append(f"错误 {item}: {e}")
                        
            except PermissionError:
                errors.append(f"无法访问: {cache_dir}")
        
        # 记录结果
        self.dna_tracer.end_trace(
            dna_code,
            output_data={
                "cleaned_size": total_size,
                "cleaned_count": len(cleaned_items),
                "dry_run": dry_run
            },
            side_effects=cleaned_items if not dry_run else [],
            audit_result="🟢 成功" if not errors else "🟡 部分成功"
        )
        
        return CleanResult(
            success=len(errors) == 0,
            cleaned_size=total_size,
            cleaned_items=cleaned_items,
            errors=errors,
            dna_code=dna_code
        )
    
    def clean_trash(self, dry_run: bool = True) -> CleanResult:
        """清空回收站"""
        trash_dir = self.home / ".Trash"
        
        dna_code = self.dna_tracer.start_trace(
            operator="MacManager",
            operation_type=OperationType.DELETE,
            detail=f"清空回收站 (dry_run={dry_run})"
        )
        
        cleaned_items = []
        total_size = 0
        errors = []
        
        if trash_dir.exists():
            for item in trash_dir.iterdir():
                try:
                    size = self._get_size(item)
                    total_size += size
                    
                    if not dry_run:
                        if item.is_dir():
                            shutil.rmtree(item)
                        else:
                            item.unlink()
                    
                    cleaned_items.append(item.name)
                    
                except Exception as e:
                    errors.append(f"错误: {item.name} - {e}")
        
        self.dna_tracer.end_trace(
            dna_code,
            output_data={"cleaned_size": total_size, "dry_run": dry_run},
            side_effects=cleaned_items if not dry_run else [],
            audit_result="🟢 成功"
        )
        
        return CleanResult(
            success=True,
            cleaned_size=total_size,
            cleaned_items=cleaned_items,
            errors=errors,
            dna_code=dna_code
        )
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        dna_code = self.dna_tracer.start_trace(
            operator="MacManager",
            operation_type=OperationType.READ,
            detail="获取系统信息"
        )
        
        info = {}
        
        try:
            # 系统版本
            info["os_version"] = subprocess.check_output(
                ["sw_vers", "-productVersion"],
                text=True
            ).strip()
            
            # 主机名
            info["hostname"] = subprocess.check_output(
                ["hostname"],
                text=True
            ).strip()
            
            # 磁盘使用
            disk = shutil.disk_usage(self.home)
            info["disk"] = {
                "total": self._format_size(disk.total),
                "used": self._format_size(disk.used),
                "free": self._format_size(disk.free),
                "percent": f"{disk.used / disk.total * 100:.1f}%"
            }
            
            # 内存信息（通过vm_stat）
            try:
                vm_stat = subprocess.check_output(["vm_stat"], text=True)
                info["memory"] = self._parse_vm_stat(vm_stat)
            except:
                info["memory"] = "无法获取"
            
            # CPU信息
            try:
                cpu_info = subprocess.check_output(
                    ["sysctl", "-n", "machdep.cpu.brand_string"],
                    text=True
                ).strip()
                info["cpu"] = cpu_info
            except:
                info["cpu"] = "无法获取"
                
        except Exception as e:
            info["error"] = str(e)
        
        self.dna_tracer.end_trace(dna_code, output_data=info, audit_result="🟢 成功")
        
        return info
    
    def get_startup_items(self) -> List[Dict[str, Any]]:
        """获取启动项"""
        items = []
        
        # 用户登录项
        login_items_dir = self.home / "Library/LaunchAgents"
        if login_items_dir.exists():
            for plist in login_items_dir.glob("*.plist"):
                items.append({
                    "name": plist.stem,
                    "path": str(plist),
                    "type": "LaunchAgent (用户)",
                    "enabled": True
                })
        
        # 系统启动项
        system_agents = Path("/Library/LaunchAgents")
        if system_agents.exists():
            for plist in system_agents.glob("*.plist"):
                items.append({
                    "name": plist.stem,
                    "path": str(plist),
                    "type": "LaunchAgent (系统)",
                    "enabled": True
                })
        
        return items
    
    def run_applescript(self, script: str) -> str:
        """
        运行AppleScript（需要审计）
        """
        # 审计
        audit = self.audit_engine.audit(f"AppleScript: {script}")
        
        if audit.level == AuditLevel.RED:
            return f"🔴 审计不通过: {audit.reason}"
        
        if audit.level == AuditLevel.YELLOW:
            print(f"⚠️ {audit.reason}")
            # 实际应用中应等待用户确认
        
        dna_code = self.dna_tracer.start_trace(
            operator="MacManager",
            operation_type=OperationType.EXECUTE,
            detail="运行AppleScript",
            input_data=script[:200]
        )
        
        try:
            result = subprocess.check_output(
                ["osascript", "-e", script],
                text=True,
                stderr=subprocess.STDOUT
            )
            
            self.dna_tracer.end_trace(
                dna_code,
                output_data=result,
                audit_result="🟢 成功"
            )
            
            return result.strip()
            
        except subprocess.CalledProcessError as e:
            self.dna_tracer.end_trace(
                dna_code,
                output_data=e.output,
                audit_result="🔴 失败"
            )
            return f"错误: {e.output}"
    
    def _is_system_critical(self, path: Path) -> bool:
        """检查是否是系统关键文件"""
        critical_names = [
            "com.apple",
            "CloudKit",
            "Safari",
            "Finder",
            "SystemUIServer",
            "Dock"
        ]
        
        name = path.name.lower()
        return any(c.lower() in name for c in critical_names)
    
    def _get_size(self, path: Path) -> int:
        """获取文件/目录大小"""
        if path.is_file():
            return path.stat().st_size
        
        total = 0
        try:
            for p in path.rglob("*"):
                if p.is_file():
                    total += p.stat().st_size
        except:
            pass
        return total
    
    def _format_size(self, size: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"
    
    def _parse_vm_stat(self, vm_stat: str) -> Dict[str, str]:
        """解析vm_stat输出"""
        # 简化解析
        lines = vm_stat.strip().split('\n')
        result = {}
        
        for line in lines[1:]:  # 跳过第一行
            if ':' in line:
                key, value = line.split(':')
                result[key.strip()] = value.strip().rstrip('.')
        
        return result


# ==================== 便捷函数 ====================
_manager = None

def get_manager() -> MacManager:
    """获取管理器单例"""
    global _manager
    if _manager is None:
        _manager = MacManager()
    return _manager


def clean_cache(dry_run: bool = True) -> str:
    """
    便捷函数：清理缓存
    
    Usage:
        result = clean_cache(dry_run=True)  # 预览
        result = clean_cache(dry_run=False)  # 实际清理
    """
    m = get_manager()
    result = m.clean_cache(dry_run)
    
    mode = "预览" if dry_run else "已清理"
    return f"{mode} {m._format_size(result.cleaned_size)}，共 {len(result.cleaned_items)} 项"


# ==================== 使用示例 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("🍎 Mac系统管理器测试")
    print("=" * 60)
    
    manager = MacManager()
    
    # 获取系统信息
    print("\n📊 系统信息:")
    info = manager.get_system_info()
    print(f"  系统版本: macOS {info.get('os_version', 'N/A')}")
    print(f"  主机名: {info.get('hostname', 'N/A')}")
    print(f"  CPU: {info.get('cpu', 'N/A')}")
    
    if "disk" in info:
        disk = info["disk"]
        print(f"  磁盘: {disk['used']} / {disk['total']} ({disk['percent']})")
    
    # 预览清理缓存
    print("\n🧹 缓存清理预览:")
    result = manager.clean_cache(dry_run=True)
    print(f"  可清理: {manager._format_size(result.cleaned_size)}")
    print(f"  项目数: {len(result.cleaned_items)}")
    print(f"  DNA追溯码: {result.dna_code}")
    
    # 预览清空回收站
    print("\n🗑️ 回收站预览:")
    trash_result = manager.clean_trash(dry_run=True)
    print(f"  可清理: {manager._format_size(trash_result.cleaned_size)}")
    print(f"  项目数: {len(trash_result.cleaned_items)}")
    
    # 获取启动项
    print("\n🚀 启动项:")
    startup_items = manager.get_startup_items()
    for item in startup_items[:5]:  # 只显示前5个
        print(f"  - {item['name']} ({item['type']})")
    if len(startup_items) > 5:
        print(f"  ... 还有 {len(startup_items) - 5} 项")
