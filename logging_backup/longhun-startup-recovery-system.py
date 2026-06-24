#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂 启动初始化系统 v1.0
Longhun Startup & Log Recovery System

DNA:#龍芯⚡️2026-06-07-STARTUP-RECOVERY-FILE1-v1.0
"""

import sqlite3
import json
import gzip
from datetime import datetime
from typing import Dict, List, Optional
import os

class StartupManager:
    """启动管理器 - 启动时恢复日志、检测异常、初始化系统"""
    
    def __init__(self, db_path: str = "~/.龍魂/logs/longhun.db"):
        self.db_path = os.path.expanduser(db_path)
        self.startup_time = datetime.now()
        self.startup_log = []
    
    def startup(self) -> Dict:
        """完整启动流程"""
        print("\n" + "=" * 70)
        print("🐉 龍魂系统启动")
        print("=" * 70)
        
        result = {
            "timestamp": self.startup_time.isoformat(),
            "status": "initializing",
            "phases": {}
        }
        
        # 阶段 1: 数据库检查
        print("\n[1/5] 检查数据库...")
        db_status = self._check_database()
        result["phases"]["database"] = db_status
        print(f"✅ 数据库检查完成: {db_status['status']}")
        
        # 阶段 2: 恢复日志
        print("\n[2/5] 恢复上次运行日志...")
        logs_recovered = self._recover_logs()
        result["phases"]["logs_recovered"] = logs_recovered
        print(f"✅ 恢复 {logs_recovered['successful']} 条成功日志, {logs_recovered['failed']} 条失败日志")
        
        # 阶段 3: 检测异常
        print("\n[3/5] 检测异常和未处理的错误...")
        anomalies = self._detect_anomalies()
        result["phases"]["anomalies"] = anomalies
        if anomalies["critical_count"] > 0:
            print(f"⚠️  发现 {anomalies['critical_count']} 个严重问题")
        else:
            print("✅ 未发现异常")
        
        # 阶段 4: 压缩和清理
        print("\n[4/5] 压缩日志和清理空间...")
        cleanup_result = self._compress_and_cleanup()
        result["phases"]["cleanup"] = cleanup_result
        print(f"✅ 压缩 {cleanup_result['compressed']} 条日志, 节省 {cleanup_result['saved_kb']:.2f} KB")
        
        # 阶段 5: 生成启动报告
        print("\n[5/5] 生成启动报告...")
        report = self._generate_startup_report(result)
        result["phases"]["report"] = report
        
        result["status"] = "ready"
        
        print("\n" + "=" * 70)
        print("🟢 龍魂系统已就绪！")
        print("=" * 70)
        print(f"运行ID: {report['session_id']}")
        print(f"系统健康: {report['system_health']:.1f}%")
        print(f"需要关注的问题: {report['issues_to_review']} 个")
        print("=" * 70 + "\n")
        
        return result
    
    def _check_database(self) -> Dict:
        """检查数据库完整性"""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            if not os.path.exists(self.db_path):
                return {
                    "status": "created",
                    "message": "新数据库已创建",
                    "size_kb": 0
                }
            
            size_kb = os.path.getsize(self.db_path) / 1024
            
            # 检查表
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table'
            """)
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            return {
                "status": "healthy",
                "size_kb": size_kb,
                "tables": tables,
                "message": f"数据库正常，包含 {len(tables)} 个表"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _recover_logs(self) -> Dict:
        """恢复上次运行的日志"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 统计日志
            cursor.execute("SELECT COUNT(*) FROM logs WHERE status = 'success'")
            successful = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM logs WHERE status = 'failure'")
            failed = cursor.fetchone()[0]
            
            # 获取最后10条日志
            cursor.execute("""
                SELECT timestamp, operation, category, status, message 
                FROM logs 
                ORDER BY timestamp DESC 
                LIMIT 10
            """)
            
            recent_logs = [
                {
                    "timestamp": row[0],
                    "operation": row[1],
                    "category": row[2],
                    "status": row[3],
                    "message": row[4]
                }
                for row in cursor.fetchall()
            ]
            
            conn.close()
            
            return {
                "successful": successful,
                "failed": failed,
                "total": successful + failed,
                "recent_logs": recent_logs
            }
        except Exception as e:
            return {
                "successful": 0,
                "failed": 0,
                "total": 0,
                "error": str(e)
            }
    
    def _detect_anomalies(self) -> Dict:
        """检测系统异常"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            anomalies = {
                "critical": [],
                "warnings": [],
                "critical_count": 0,
                "warning_count": 0
            }
            
            # 检查 1: 连续失败
            cursor.execute("""
                SELECT category, COUNT(*) as count
                FROM logs
                WHERE status = 'failure'
                AND timestamp > datetime('now', '-24 hours')
                GROUP BY category
                HAVING count > 3
            """)
            
            for row in cursor.fetchall():
                anomalies["critical"].append(
                    f"[严重] {row[0]} 在24小时内失败 {row[1]} 次"
                )
                anomalies["critical_count"] += 1
            
            # 检查 2: 未压缩的旧日志
            cursor.execute("""
                SELECT COUNT(*) FROM logs
                WHERE compressed = 0
                AND status = 'success'
                AND timestamp < datetime('now', '-7 days')
            """)
            
            old_logs = cursor.fetchone()[0]
            if old_logs > 100:
                anomalies["warnings"].append(
                    f"[警告] 有 {old_logs} 条旧日志未压缩，可以清理"
                )
                anomalies["warning_count"] += 1
            
            # 检查 3: 错误日志
            cursor.execute("""
                SELECT COUNT(*) FROM logs
                WHERE level = 'critical'
                AND timestamp > datetime('now', '-1 hour')
            """)
            
            critical_logs = cursor.fetchone()[0]
            if critical_logs > 0:
                anomalies["critical"].append(
                    f"[严重] 最近1小时有 {critical_logs} 条关键日志"
                )
                anomalies["critical_count"] += 1
            
            conn.close()
            
            return anomalies
        except Exception as e:
            return {
                "error": str(e),
                "critical": [],
                "warnings": [],
                "critical_count": 0,
                "warning_count": 0
            }
    
    def _compress_and_cleanup(self) -> Dict:
        """自动压缩和清理日志"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 查找需要压缩的日志
            cursor.execute("""
                SELECT id, message, details FROM logs
                WHERE status = 'success'
                AND compressed = 0
                AND timestamp < datetime('now', '-3 days')
                LIMIT 50
            """)
            
            logs_to_compress = cursor.fetchall()
            compressed_count = 0
            total_saved = 0
            
            for log_id, message, details in logs_to_compress:
                content = f"{message}|{details}".encode('utf-8')
                original_size = len(content)
                
                compressed = gzip.compress(content)
                compressed_size = len(compressed)
                
                # 保存压缩数据
                cursor.execute("""
                    INSERT INTO compressed_logs
                    (original_log_id, compressed_data, original_size, 
                     compressed_size, compression_ratio)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    log_id,
                    compressed,
                    original_size,
                    compressed_size,
                    compressed_size / original_size
                ))
                
                cursor.execute(
                    "UPDATE logs SET compressed = 1 WHERE id = ?",
                    (log_id,)
                )
                
                compressed_count += 1
                total_saved += (original_size - compressed_size)
            
            conn.commit()
            conn.close()
            
            return {
                "compressed": compressed_count,
                "saved_kb": total_saved / 1024,
                "status": "success"
            }
        except Exception as e:
            return {
                "compressed": 0,
                "saved_kb": 0,
                "status": "error",
                "error": str(e)
            }
    
    def _generate_startup_report(self, result: Dict) -> Dict:
        """生成启动报告"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 统计
            cursor.execute("SELECT COUNT(DISTINCT category) FROM logs")
            active_skills = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM versions")
            total_versions = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(*) FROM logs 
                WHERE status = 'success'
            """)
            success_logs = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM logs")
            total_logs = cursor.fetchone()[0]
            
            conn.close()
            
            # 计算健康度
            success_rate = (success_logs / total_logs * 100) if total_logs > 0 else 100
            
            issues = result["phases"]["anomalies"]["critical_count"] + \
                     result["phases"]["anomalies"]["warning_count"]
            
            return {
                "session_id": self.startup_time.strftime("%Y%m%d_%H%M%S"),
                "active_skills": active_skills,
                "total_versions": total_versions,
                "total_logs": total_logs,
                "success_rate": success_rate,
                "system_health": min(100, success_rate),
                "issues_to_review": issues,
                "startup_time": self.startup_time.isoformat()
            }
        except Exception as e:
            return {
                "error": str(e)
            }


# ═══════════════════════════════════════════════════════════════════════════
# 使用示例
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🐉 龍魂启动管理系统 v1.0")
    print("DNA:#龍芯⚡️2026-06-07-STARTUP-RECOVERY-v1.0\n")
    
    startup = StartupManager()
    result = startup.startup()
    
    # 显示详细报告
    print("\n📊 详细启动报告:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
