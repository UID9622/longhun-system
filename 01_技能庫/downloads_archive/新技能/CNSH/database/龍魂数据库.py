#龍芯⚡️2026-06-18-CNSH-database-龍魂数据库-v1.0
"""
通心译 | TongXinYi: LongHun Database
龍魂体系·龍魂数据库 — 轻量级本地数据持久化引擎

基于SQLite的本地数据库封装，提供面向对象的CRUD操作接口
SQLite-based local database wrapper with OOP-style CRUD operations
"""
# 🟢 君子协议 | JunZi Protocol: CC BY-NC-SA 4.0
# 🟡 AI Truth Protocol: All outputs must be verifiable and traceable
# 🔴 DNA Trace: #龍芯⚡️2026-06-18-CNSH-database-龍魂数据库-v1.0

from datetime import datetime
from typing import Dict, Any, List, Optional
import sqlite3
import json
import os

__版本__ = "v1.0"
__dna__ = "#龍芯⚡️2026-06-18-CNSH-database-龍魂数据库-v1.0"


class 龍魂数据库:
    """通心译 | TongXinYi: LongHun Database — 龍魂轻量级数据库引擎"""

    def __init__(自身, 数据库路径: str = "./cnsh.db"):
        自身.数据库路径 = 数据库路径
        自身.连接 = None
        自身.游标 = None
        自身.表字典 = {}
        自身.查询计数 = 0
        print(f"[龍魂数据库] 🐉 数据库引擎已初始化 | 路径: {{数据库路径}} | {{__dna__}}")

    def 连接(自身) -> bool:
        """🟢 连接数据库 | Connect to database"""
        try:
            os.makedirs(os.path.dirname(os.path.abspath(自身.数据库路径)) if os.path.dirname(自身.数据库路径) else ".", exist_ok=True)
            自身.连接 = sqlite3.connect(自身.数据库路径)
            自身.连接.row_factory = sqlite3.Row
            自身.游标 = 自身.连接.cursor()
            print(f"[龍魂数据库] 🟢 数据库已连接: {{自身.数据库路径}}")
            return True
        except Exception as 错误:
            print(f"[龍魂数据库] 🔴 连接失败: {{错误}}")
            return False

    def 创建表(自身, 表名: str, 字段定义: Dict[str, str]):
        """🟢 创建数据表 | Create table"""
        if not 自身.连接:
            自身.连接()

        字段列表 = ", ".join([f"{{名}} {{类型}}" for 名, 类型 in 字段定义.items()])
        SQL = f"CREATE TABLE IF NOT EXISTS {{表名}} (id INTEGER PRIMARY KEY AUTOINCREMENT, {{字段列表}}, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"

        自身.游标.execute(SQL)
        自身.连接.commit()
        自身.表字典[表名] = list(字段定义.keys())
        print(f"[龍魂数据库] 🟢 表已创建: {{表名}} ({{len(字段定义)}} 个字段)")

    def 插入(自身, 表名: str, 数据: Dict[str, Any]) -> int:
        """🟢 插入数据 | Insert data"""
        if not 自身.连接:
            自身.连接()

        字段 = ", ".join(数据.keys())
        占位 = ", ".join(["?" for _ in 数据])
        SQL = f"INSERT INTO {{表名}} ({{字段}}) VALUES ({{占位}})"

        自身.游标.execute(SQL, list(数据.values()))
        自身.连接.commit()
        新ID = 自身.游标.lastrowid
        print(f"[龍魂数据库] 🟢 数据已插入: {{表名}} #{{新ID}}")
        return 新ID

    def 查询(自身, 表名: str, 条件: str = None, 参数: tuple = None) -> List[Dict]:
        """🟡 查询数据 | Query data"""
        if not 自身.连接:
            自身.连接()

        SQL = f"SELECT * FROM {{表名}}"
        if 条件:
            SQL += f" WHERE {{条件}}"

        自身.查询计数 += 1
        自身.游标.execute(SQL, 参数 or ())
        行列表 = 自身.游标.fetchall()

        结果 = []
        for 行 in 行列表:
            结果.append({键: 行[键] for 键 in 行.keys()})

        print(f"[龍魂数据库] 🟢 查询完成: {{len(结果)}} 条记录")
        return 结果

    def 更新(自身, 表名: str, 数据: Dict[str, Any], 条件: str, 参数: tuple):
        """🟡 更新数据 | Update data"""
        if not 自身.连接:
            自身.连接()

        设置 = ", ".join([f"{{k}} = ?" for k in 数据.keys()])
        SQL = f"UPDATE {{表名}} SET {{设置}} WHERE {{条件}}"
        完整参数 = list(数据.values()) + list(参数)

        自身.游标.execute(SQL, 完整参数)
        自身.连接.commit()
        影响行数 = 自身.游标.rowcount
        print(f"[龍魂数据库] 🟡 数据已更新: {{表名}} ({{影响行数}} 行)")
        return 影响行数

    def 删除(自身, 表名: str, 条件: str, 参数: tuple):
        """🔴 删除数据 | Delete data"""
        if not 自身.连接:
            自身.连接()

        SQL = f"DELETE FROM {{表名}} WHERE {{条件}}"
        自身.游标.execute(SQL, 参数)
        自身.连接.commit()
        影响行数 = 自身.游标.rowcount
        print(f"[龍魂数据库] 🔴 数据已删除: {{表名}} ({{影响行数}} 行)")
        return 影响行数

    def 关闭(自身):
        """🟢 关闭数据库连接 | Close database connection"""
        if 自身.连接:
            自身.连接.close()
            自身.连接 = None
            print("[龍魂数据库] 🟢 数据库连接已关闭")

    def 获取统计(自身) -> Dict:
        """🟡 获取数据库统计 | Get database statistics"""
        return {
            "数据库路径": 自身.数据库路径,
            "已连接": 自身.连接 is not None,
            "表数量": len(自身.表字典),
            "查询次数": 自身.查询计数,
            "表列表": list(自身.表字典.keys())
        }


if __name__ == "__main__":
    print("=== 龍魂数据库 · 独立执行演示 ===")
    db = 龍魂数据库("./test_cnsh.db")
    db.连接()
    db.创建表("模块表", {
        "名称": "TEXT NOT NULL",
        "路径": "TEXT",
        "版本": "TEXT DEFAULT 'v1.0'",
        "状态": "TEXT DEFAULT '活跃'"
    })
    db.插入("模块表", {"名称": "runtime", "路径": "/CNSH/runtime", "版本": "v1.0", "状态": "活跃"})
    db.插入("模块表", {"名称": "governance", "路径": "/CNSH/governance", "版本": "v1.0", "状态": "活跃"})
    结果 = db.查询("模块表")
    for 行 in 结果:
        print(f"  模块: {{行['名称']}} @ {{行['路径']}}")
    print(f"统计: {{db.获取统计()}}")
    db.关闭()
