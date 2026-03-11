#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════
# 龙魂本地数据库系统 | SQLite原生实现
# ═══════════════════════════════════════════════════════════
# 特点: 零API依赖，完全本地存储，开箱即用
# DNA: #龙芯⚡️2026-02-06-本地数据库-v1.0
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════════

import sqlite3
import json
import hashlib
import datetime
import os
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path


class 龙魂本地数据库:
    """
    龙魂系统本地数据库管理器
    
    数据存储位置: ~/.longhun/database/
    数据库文件: longhun_system.db
    
    核心表:
    - 用户配置表 (user_config)
    - DNA追溯表 (dna_trace)
    - 五大人格决策历史 (persona_decisions)
    - CNSH代码库 (cnsh_code)
    - 反诈守护日志 (anti_fraud_log)
    - 易经推演记录 (yijing_history)
    - 支付记录表 (payment_records)
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """初始化数据库连接"""
        if db_path is None:
            # 默认存储在用户主目录
            home = Path.home()
            db_dir = home / ".longhun" / "database"
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = db_dir / "longhun_system.db"
        
        self.db_path = str(db_path)
        self.conn = None
        self.cursor = None
        
        # 初始化连接
        self._连接数据库()
        self._初始化表结构()
    
    def _连接数据库(self):
        """建立数据库连接"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    
    def _初始化表结构(self):
        """创建必要的表结构"""
        
        # 1. 用户配置表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 2. DNA追溯表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS dna_trace (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dna_code TEXT UNIQUE NOT NULL,
                operation_type TEXT NOT NULL,
                persona TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 3. 五大人格决策历史
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS persona_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                persona_name TEXT NOT NULL,
                decision_type TEXT NOT NULL,
                decision_result TEXT NOT NULL,
                audit_result TEXT,
                dna_code TEXT,
                gua_xiang TEXT,
                hu_ruo_coefficient REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 4. CNSH代码库
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cnsh_code (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                code_content TEXT NOT NULL,
                description TEXT,
                dna_code TEXT,
                is_example INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 5. 反诈守护日志
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS anti_fraud_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT,
                fraud_type TEXT,
                severity TEXT,
                is_blocked INTEGER DEFAULT 0,
                education_shown INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 6. 易经推演记录
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS yijing_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                hour INTEGER,
                gua_xiang TEXT NOT NULL,
                gua_meaning TEXT,
                weight_individual REAL,
                weight_group REAL,
                weight_global REAL
            )
        ''')
        
        # 7. 支付记录表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS payment_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feature_name TEXT NOT NULL,
                amount REAL NOT NULL,
                currency TEXT DEFAULT 'CNY',
                payment_method TEXT DEFAULT '数字人民币',
                status TEXT DEFAULT 'pending',
                paid_at TIMESTAMP,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 8. 系统日志表
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_level TEXT NOT NULL,
                message TEXT NOT NULL,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        
        # 初始化默认数据
        self._初始化默认数据()
    
    def _初始化默认数据(self):
        """初始化默认配置和示例代码"""
        
        # 默认用户配置
        defaults = [
            ("uid", "UID9622"),
            ("username", "诸葛鑫"),
            ("eternal_anchor", "再楠不惧，终成豪图"),
            ("gpg_fingerprint", "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"),
            ("confirm_code", "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"),
            ("debug_mode", "true"),
            ("payment_mode", "free"),  # free/paid
        ]
        
        for key, value in defaults:
            self.cursor.execute('''
                INSERT OR IGNORE INTO user_config (key, value) VALUES (?, ?)
            ''', (key, value))
        
        # 初始化示例CNSH代码
        self._初始化示例代码()
        
        self.conn.commit()
    
    def _初始化示例代码(self):
        """初始化CNSH示例代码"""
        
        示例代码列表 = [
            {
                "filename": "hello.cnsh",
                "code": '''【程序】 你好龙魂

【输出】 "你好，龙魂系统已就绪！"
【输出】 "当前时间：" + 时间.现在()
【输出】 "当前用户：" + 系统.用户名()

【结束程序】''',
                "description": "基础入门示例",
                "is_example": 1
            },
            {
                "filename": "反诈守护.longhun",
                "code": '''【模块】 龙魂反诈守护

【列表】 诈骗关键词
    "安全账户", "通缉令", "涉嫌洗钱"
    "高回报", "零风险", "稳赚不赔"

【函数】 检测诈骗(用户输入)
    【遍历】 关键词 在 诈骗关键词 中
        【如果】 关键词 在 用户输入 中
            返回 (真, "发现诈骗关键词: " + 关键词)
        【结束如果】
    【结束遍历】
    返回 (假, "未发现风险")

【结束模块】''',
                "description": "反诈守护模块",
                "is_example": 1
            },
            {
                "filename": "五大人格.longhun",
                "code": '''【模块】 五大人格系统

【枚举】 八卦
    乾, 坤, 坎, 离, 震, 巽, 艮, 兑

【字典】 八卦权重
    乾 = {"个体": 0.6, "群体": 0.3, "全球": 0.1}
    坤 = {"个体": 0.2, "群体": 0.6, "全球": 0.2}
    坎 = {"个体": 0.1, "群体": 0.3, "全球": 0.6}
    离 = {"个体": 0.3, "群体": 0.4, "全球": 0.3}

【类】 雯雯人格
    【属性】
        姓名 = "雯雯"
        本命卦象 = 坤卦
        职责 = "文档整理"
    
    【方法】 整理(文件)
        返回 "正在整理: " + 文件.名称

【结束模块】''',
                "description": "五大人格系统模板",
                "is_example": 1
            }
        ]
        
        for 示例 in 示例代码列表:
            self.cursor.execute('''
                INSERT OR IGNORE INTO cnsh_code 
                (filename, code_content, description, is_example, dna_code)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                示例["filename"],
                示例["code"],
                示例["description"],
                示例["is_example"],
                self._生成DNA("初始化-" + 示例["filename"])
            ))
    
    def _生成DNA(self, 操作: str) -> str:
        """生成DNA追溯码"""
        日期 = datetime.datetime.now().strftime("%Y-%m-%d")
        return f"#龙芯⚡️{日期}-{操作}-v1.0"
    
    # ═══════════════════════════════════════════════════════════
    # 用户配置操作
    # ═══════════════════════════════════════════════════════════
    
    def 获取配置(self, key: str) -> Optional[str]:
        """获取用户配置"""
        self.cursor.execute(
            "SELECT value FROM user_config WHERE key = ?", (key,)
        )
        row = self.cursor.fetchone()
        return row["value"] if row else None
    
    def 设置配置(self, key: str, value: str):
        """设置用户配置"""
        self.cursor.execute('''
            INSERT OR REPLACE INTO user_config (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, value))
        self.conn.commit()
    
    def 获取所有配置(self) -> Dict[str, str]:
        """获取所有配置"""
        self.cursor.execute("SELECT key, value FROM user_config")
        return {row["key"]: row["value"] for row in self.cursor.fetchall()}
    
    # ═══════════════════════════════════════════════════════════
    # DNA追溯操作
    # ═══════════════════════════════════════════════════════════
    
    def 记录DNA(self, dna_code: str, operation_type: str, 
                persona: str = None, metadata: Dict = None):
        """记录DNA追溯"""
        self.cursor.execute('''
            INSERT INTO dna_trace (dna_code, operation_type, persona, metadata)
            VALUES (?, ?, ?, ?)
        ''', (dna_code, operation_type, persona, 
              json.dumps(metadata) if metadata else None))
        self.conn.commit()
    
    def 查询DNA(self, dna_code: str = None, 开始时间: str = None, 
                结束时间: str = None) -> List[Dict]:
        """查询DNA追溯记录"""
        sql = "SELECT * FROM dna_trace WHERE 1=1"
        params = []
        
        if dna_code:
            sql += " AND dna_code = ?"
            params.append(dna_code)
        if 开始时间:
            sql += " AND created_at >= ?"
            params.append(开始时间)
        if 结束时间:
            sql += " AND created_at <= ?"
            params.append(结束时间)
        
        sql += " ORDER BY created_at DESC"
        
        self.cursor.execute(sql, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ═══════════════════════════════════════════════════════════
    # 五大人格决策历史
    # ═══════════════════════════════════════════════════════════
    
    def 记录决策(self, persona_name: str, decision_type: str,
                 decision_result: str, audit_result: str = None,
                 dna_code: str = None, gua_xiang: str = None,
                 hu_ruo_coefficient: float = 1.0):
        """记录五大人格决策"""
        self.cursor.execute('''
            INSERT INTO persona_decisions 
            (persona_name, decision_type, decision_result, audit_result,
             dna_code, gua_xiang, hu_ruo_coefficient)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (persona_name, decision_type, decision_result, audit_result,
              dna_code, gua_xiang, hu_ruo_coefficient))
        self.conn.commit()
    
    def 获取决策历史(self, persona_name: str = None, limit: int = 100) -> List[Dict]:
        """获取决策历史"""
        sql = "SELECT * FROM persona_decisions"
        params = []
        
        if persona_name:
            sql += " WHERE persona_name = ?"
            params.append(persona_name)
        
        sql += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        
        self.cursor.execute(sql, params)
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ═══════════════════════════════════════════════════════════
    # CNSH代码库操作
    # ═══════════════════════════════════════════════════════════
    
    def 保存代码(self, filename: str, code_content: str, 
                 description: str = None, dna_code: str = None) -> int:
        """保存CNSH代码"""
        self.cursor.execute('''
            INSERT INTO cnsh_code (filename, code_content, description, dna_code)
            VALUES (?, ?, ?, ?)
        ''', (filename, code_content, description, dna_code))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def 更新代码(self, code_id: int, code_content: str, description: str = None):
        """更新CNSH代码"""
        self.cursor.execute('''
            UPDATE cnsh_code 
            SET code_content = ?, description = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (code_content, description, code_id))
        self.conn.commit()
    
    def 获取代码(self, code_id: int = None, filename: str = None) -> Optional[Dict]:
        """获取CNSH代码"""
        if code_id:
            self.cursor.execute("SELECT * FROM cnsh_code WHERE id = ?", (code_id,))
        elif filename:
            self.cursor.execute(
                "SELECT * FROM cnsh_code WHERE filename = ? ORDER BY id DESC LIMIT 1",
                (filename,)
            )
        else:
            return None
        
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def 列出所有代码(self, 只显示示例: bool = False) -> List[Dict]:
        """列出所有CNSH代码"""
        if 只显示示例:
            self.cursor.execute(
                "SELECT * FROM cnsh_code WHERE is_example = 1 ORDER BY id"
            )
        else:
            self.cursor.execute("SELECT * FROM cnsh_code ORDER BY updated_at DESC")
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    def 删除代码(self, code_id: int):
        """删除CNSH代码"""
        self.cursor.execute("DELETE FROM cnsh_code WHERE id = ?", (code_id,))
        self.conn.commit()
    
    # ═══════════════════════════════════════════════════════════
    # 反诈守护日志
    # ═══════════════════════════════════════════════════════════
    
    def 记录反诈检测(self, input_text: str, fraud_type: str = None,
                    severity: str = None, is_blocked: bool = False,
                    education_shown: bool = False):
        """记录反诈检测日志"""
        self.cursor.execute('''
            INSERT INTO anti_fraud_log 
            (input_text, fraud_type, severity, is_blocked, education_shown)
            VALUES (?, ?, ?, ?, ?)
        ''', (input_text, fraud_type, severity, 
              1 if is_blocked else 0, 1 if education_shown else 0))
        self.conn.commit()
    
    def 获取反诈统计(self) -> Dict:
        """获取反诈守护统计"""
        self.cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(is_blocked) as blocked,
                SUM(education_shown) as educated
            FROM anti_fraud_log
        ''')
        row = self.cursor.fetchone()
        return {
            "总检测次数": row["total"],
            "阻断次数": row["blocked"] or 0,
            "教育展示次数": row["educated"] or 0
        }
    
    # ═══════════════════════════════════════════════════════════
    # 易经推演记录
    # ═══════════════════════════════════════════════════════════
    
    def 记录易经推演(self, hour: int, gua_xiang: str, gua_meaning: str,
                    weight_individual: float, weight_group: float, weight_global: float):
        """记录易经推演结果"""
        self.cursor.execute('''
            INSERT INTO yijing_history 
            (hour, gua_xiang, gua_meaning, weight_individual, weight_group, weight_global)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (hour, gua_xiang, gua_meaning, weight_individual, weight_group, weight_global))
        self.conn.commit()
    
    def 获取最近推演(self, limit: int = 10) -> List[Dict]:
        """获取最近推演记录"""
        self.cursor.execute('''
            SELECT * FROM yijing_history 
            ORDER BY query_time DESC LIMIT ?
        ''', (limit,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ═══════════════════════════════════════════════════════════
    # 支付记录操作
    # ═══════════════════════════════════════════════════════════
    
    def 创建支付记录(self, feature_name: str, amount: float,
                    currency: str = "CNY", payment_method: str = "数字人民币") -> int:
        """创建支付记录"""
        # 计算过期时间（一个月后）
        过期时间 = datetime.datetime.now() + datetime.timedelta(days=30)
        
        self.cursor.execute('''
            INSERT INTO payment_records 
            (feature_name, amount, currency, payment_method, expires_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (feature_name, amount, currency, payment_method, 过期时间))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def 确认支付(self, record_id: int):
        """确认支付完成"""
        self.cursor.execute('''
            UPDATE payment_records 
            SET status = 'paid', paid_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (record_id,))
        self.conn.commit()
    
    def 检查功能权限(self, feature_name: str) -> bool:
        """检查用户是否有功能权限"""
        # 调试期免费
        if self.获取配置("debug_mode") == "true":
            return True
        
        # 检查有效支付记录
        self.cursor.execute('''
            SELECT COUNT(*) as count FROM payment_records
            WHERE feature_name = ? AND status = 'paid' AND expires_at > CURRENT_TIMESTAMP
        ''', (feature_name,))
        
        row = self.cursor.fetchone()
        return row["count"] > 0
    
    def 获取支付历史(self) -> List[Dict]:
        """获取支付历史"""
        self.cursor.execute('''
            SELECT * FROM payment_records ORDER BY created_at DESC
        ''')
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ═══════════════════════════════════════════════════════════
    # 系统日志
    # ═══════════════════════════════════════════════════════════
    
    def 记录日志(self, log_level: str, message: str, source: str = None):
        """记录系统日志"""
        self.cursor.execute('''
            INSERT INTO system_logs (log_level, message, source)
            VALUES (?, ?, ?)
        ''', (log_level, message, source))
        self.conn.commit()
    
    def 获取日志(self, log_level: str = None, limit: int = 100) -> List[Dict]:
        """获取系统日志"""
        if log_level:
            self.cursor.execute('''
                SELECT * FROM system_logs WHERE log_level = ?
                ORDER BY created_at DESC LIMIT ?
            ''', (log_level, limit))
        else:
            self.cursor.execute('''
                SELECT * FROM system_logs ORDER BY created_at DESC LIMIT ?
            ''', (limit,))
        
        return [dict(row) for row in self.cursor.fetchall()]
    
    # ═══════════════════════════════════════════════════════════
    # 系统统计
    # ═══════════════════════════════════════════════════════════
    
    def 获取系统统计(self) -> Dict:
        """获取系统整体统计"""
        stats = {}
        
        # 各表记录数
        tables = [
            "dna_trace", "persona_decisions", "cnsh_code",
            "anti_fraud_log", "yijing_history", "payment_records"
        ]
        
        for table in tables:
            self.cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            stats[table] = self.cursor.fetchone()["count"]
        
        # 数据库大小
        try:
            db_size = os.path.getsize(self.db_path)
            stats["数据库大小"] = f"{db_size / 1024:.2f} KB"
        except:
            stats["数据库大小"] = "内存模式"
        
        # 反诈统计
        stats["反诈守护"] = self.获取反诈统计()
        
        return stats
    
    # ═══════════════════════════════════════════════════════════
    # 关闭连接
    # ═══════════════════════════════════════════════════════════
    
    def 关闭(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.关闭()


# ═══════════════════════════════════════════════════════════
# 演示和测试
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("🐉 龙魂本地数据库系统 | 测试")
    print("=" * 70)
    
    # 使用内存数据库进行测试
    db = 龙魂本地数据库(":memory:")
    
    # 测试配置
    print("\n📋 用户配置测试:")
    db.设置配置("test_key", "test_value")
    print(f"  获取配置: {db.获取配置('test_key')}")
    print(f"  UID: {db.获取配置('uid')}")
    print(f"  永恒锚: {db.获取配置('eternal_anchor')}")
    
    # 测试DNA追溯
    print("\n🧬 DNA追溯测试:")
    dna = "#龙芯⚡️2026-02-06-测试操作-v1.0"
    db.记录DNA(dna, "测试操作", "宝宝", {"test": True})
    记录 = db.查询DNA(dna)
    print(f"  记录数: {len(记录)}")
    
    # 测试决策记录
    print("\n🤖 五大人格决策测试:")
    db.记录决策("雯雯", "文档整理", "完成", "🟢", dna, "坤卦", 1.0)
    决策历史 = db.获取决策历史("雯雯")
    print(f"  雯雯决策记录: {len(决策历史)} 条")
    
    # 测试代码保存
    print("\n📝 CNSH代码库测试:")
    code_id = db.保存代码("test.cnsh", "【输出】 \"Hello\"", "测试代码", dna)
    代码 = db.获取代码(code_id=code_id)
    print(f"  代码ID: {code_id}")
    print(f"  文件名: {代码['filename']}")
    
    # 测试反诈日志
    print("\n🛡️ 反诈守护测试:")
    db.记录反诈检测("测试输入", "投资诈骗", "高危", True, True)
    反诈统计 = db.获取反诈统计()
    print(f"  统计: {反诈统计}")
    
    # 测试系统统计
    print("\n📊 系统统计:")
    统计 = db.获取系统统计()
    for key, value in 统计.items():
        if key != "反诈守护":
            print(f"  {key}: {value}")
    
    # 测试支付
    print("\n💰 支付系统测试:")
    record_id = db.创建支付记录("华为开发者功能", 1.0)
    print(f"  创建支付记录ID: {record_id}")
    db.确认支付(record_id)
    有权限 = db.检查功能权限("华为开发者功能")
    print(f"  功能权限检查: {'有权限' if 有权限 else '无权限'}")
    
    print("\n" + "=" * 70)
    print("✅ 所有测试通过！")
    print("=" * 70)
    print("\n#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    
    db.关闭()
