#!/usr/bin/env python3
"""
🧬 DNA追溯系统 | DNA Tracing System
DNA追溯码: #龍芯⚡️2026-01-21-DNA追溯系统-v2.0

每个操作都有唯一的DNA追溯码，可追溯：
- 谁执行的
- 什么时候
- 执行了什么
- 结果是什么
- 有什么副作用
"""

import hashlib
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class OperationType(Enum):
    """操作类型"""
    READ = "读取"
    WRITE = "写入"
    DELETE = "删除"
    EXECUTE = "执行"
    NETWORK = "网络"
    AI_CALL = "AI调用"
    SYSTEM = "系统"


@dataclass
class DNARecord:
    """DNA记录"""
    dna_code: str
    timestamp: str
    operator: str           # 操作者（用户/AI名称）
    operation_type: str
    operation_detail: str   # 操作详情
    input_data: str         # 输入数据（脱敏后）
    output_data: str        # 输出数据（脱敏后）
    side_effects: List[str] # 副作用（文件改动、网络请求等）
    audit_result: str       # 审计结果
    parent_dna: Optional[str] = None  # 父操作DNA（用于调用链追溯）


class DNATracer:
    """DNA追溯系统"""
    
    def __init__(self, db_path: str = None):
        self.prefix = "#龍芯⚡️"
        self.owner = "UID9622"
        self.version = "v2.0"
        
        # 数据库路径
        if db_path is None:
            db_path = Path.home() / ".dragonsoul" / "dna_trace.db"
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化数据库
        self._init_database()
        
        # 当前调用链
        self._call_stack: List[str] = []
    
    def _init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dna_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dna_code TEXT UNIQUE NOT NULL,
                timestamp TEXT NOT NULL,
                operator TEXT NOT NULL,
                operation_type TEXT NOT NULL,
                operation_detail TEXT,
                input_data TEXT,
                output_data TEXT,
                side_effects TEXT,
                audit_result TEXT,
                parent_dna TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON dna_records(timestamp)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_operator ON dna_records(operator)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_parent ON dna_records(parent_dna)
        """)
        
        conn.commit()
        conn.close()
    
    def generate_dna(self, operation_type: OperationType, detail: str = "") -> str:
        """
        生成DNA追溯码
        
        格式: #龍芯⚡️YYYYMMDDHHMMSS-TYPE-HASH
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:17]
        content = f"{timestamp}-{operation_type.value}-{detail}-{self.owner}"
        hash_part = hashlib.sha256(content.encode()).hexdigest()[:12].upper()
        
        return f"{self.prefix}{timestamp}-{operation_type.name}-{hash_part}"
    
    def start_trace(self, 
                    operator: str,
                    operation_type: OperationType,
                    detail: str,
                    input_data: Any = None) -> str:
        """
        开始追溯一个操作
        
        Returns:
            str: DNA追溯码
        """
        dna_code = self.generate_dna(operation_type, detail)
        parent_dna = self._call_stack[-1] if self._call_stack else None
        self._call_stack.append(dna_code)
        
        # 创建初始记录
        record = DNARecord(
            dna_code=dna_code,
            timestamp=datetime.now().isoformat(),
            operator=operator,
            operation_type=operation_type.value,
            operation_detail=detail,
            input_data=self._safe_serialize(input_data),
            output_data="",
            side_effects=[],
            audit_result="进行中",
            parent_dna=parent_dna
        )
        
        self._save_record(record)
        return dna_code
    
    def end_trace(self,
                  dna_code: str,
                  output_data: Any = None,
                  side_effects: List[str] = None,
                  audit_result: str = "🟢 完成"):
        """结束追溯"""
        if self._call_stack and self._call_stack[-1] == dna_code:
            self._call_stack.pop()
        
        self._update_record(
            dna_code,
            output_data=self._safe_serialize(output_data),
            side_effects=side_effects or [],
            audit_result=audit_result
        )
    
    def trace(self, 
              operator: str,
              operation_type: OperationType,
              detail: str):
        """
        装饰器：自动追溯函数调用
        
        Usage:
            @tracer.trace("Claude", OperationType.AI_CALL, "分析邮件")
            def analyze_email(content):
                ...
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                # 序列化输入参数
                input_data = {
                    "args": [str(a)[:100] for a in args],
                    "kwargs": {k: str(v)[:100] for k, v in kwargs.items()}
                }
                
                dna_code = self.start_trace(operator, operation_type, detail, input_data)
                
                try:
                    result = func(*args, **kwargs)
                    self.end_trace(dna_code, result, audit_result="🟢 成功")
                    return result
                except Exception as e:
                    self.end_trace(
                        dna_code, 
                        str(e), 
                        side_effects=[f"异常: {type(e).__name__}"],
                        audit_result="🔴 失败"
                    )
                    raise
            
            return wrapper
        return decorator
    
    def query_by_dna(self, dna_code: str) -> Optional[DNARecord]:
        """通过DNA码查询记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM dna_records WHERE dna_code = ?",
            (dna_code,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_record(row)
        return None
    
    def query_call_chain(self, dna_code: str) -> List[DNARecord]:
        """查询完整调用链"""
        chain = []
        current = self.query_by_dna(dna_code)
        
        while current:
            chain.insert(0, current)
            if current.parent_dna:
                current = self.query_by_dna(current.parent_dna)
            else:
                break
        
        return chain
    
    def query_by_time_range(self, 
                            start: datetime, 
                            end: datetime) -> List[DNARecord]:
        """按时间范围查询"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM dna_records 
            WHERE timestamp BETWEEN ? AND ?
            ORDER BY timestamp DESC
        """, (start.isoformat(), end.isoformat()))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_record(row) for row in rows]
    
    def query_by_operator(self, operator: str) -> List[DNARecord]:
        """按操作者查询"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM dna_records 
            WHERE operator = ?
            ORDER BY timestamp DESC
            LIMIT 100
        """, (operator,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_record(row) for row in rows]
    
    def generate_report(self, dna_code: str) -> Dict[str, Any]:
        """生成追溯报告"""
        record = self.query_by_dna(dna_code)
        if not record:
            return {"error": "未找到记录"}
        
        call_chain = self.query_call_chain(dna_code)
        
        return {
            "dna_code": dna_code,
            "record": asdict(record),
            "call_chain": [asdict(r) for r in call_chain],
            "chain_length": len(call_chain),
            "generated_at": datetime.now().isoformat()
        }
    
    def _save_record(self, record: DNARecord):
        """保存记录到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO dna_records 
            (dna_code, timestamp, operator, operation_type, operation_detail,
             input_data, output_data, side_effects, audit_result, parent_dna)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            record.dna_code,
            record.timestamp,
            record.operator,
            record.operation_type,
            record.operation_detail,
            record.input_data,
            record.output_data,
            json.dumps(record.side_effects, ensure_ascii=False),
            record.audit_result,
            record.parent_dna
        ))
        
        conn.commit()
        conn.close()
    
    def _update_record(self, dna_code: str, **kwargs):
        """更新记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates = []
        values = []
        
        for key, value in kwargs.items():
            if key == "side_effects":
                value = json.dumps(value, ensure_ascii=False)
            updates.append(f"{key} = ?")
            values.append(value)
        
        values.append(dna_code)
        
        cursor.execute(f"""
            UPDATE dna_records 
            SET {', '.join(updates)}
            WHERE dna_code = ?
        """, values)
        
        conn.commit()
        conn.close()
    
    def _row_to_record(self, row) -> DNARecord:
        """将数据库行转换为记录对象"""
        return DNARecord(
            dna_code=row[1],
            timestamp=row[2],
            operator=row[3],
            operation_type=row[4],
            operation_detail=row[5],
            input_data=row[6],
            output_data=row[7],
            side_effects=json.loads(row[8]) if row[8] else [],
            audit_result=row[9],
            parent_dna=row[10]
        )
    
    def _safe_serialize(self, data: Any) -> str:
        """安全序列化数据"""
        if data is None:
            return ""
        try:
            if isinstance(data, (dict, list)):
                return json.dumps(data, ensure_ascii=False, default=str)[:1000]
            return str(data)[:1000]
        except:
            return str(type(data))


# ==================== 使用示例 ====================
if __name__ == "__main__":
    tracer = DNATracer()
    
    # 示例1：手动追溯
    print("=" * 60)
    print("🧬 DNA追溯系统测试")
    print("=" * 60)
    
    # 开始一个操作
    dna = tracer.start_trace(
        operator="老大",
        operation_type=OperationType.EXECUTE,
        detail="清理Mac缓存",
        input_data={"target": "/Library/Caches"}
    )
    print(f"\n生成DNA追溯码: {dna}")
    
    # 模拟操作完成
    tracer.end_trace(
        dna,
        output_data={"cleaned_size": "1.2GB"},
        side_effects=["删除了 /Library/Caches/temp"],
        audit_result="🟢 成功"
    )
    
    # 查询记录
    record = tracer.query_by_dna(dna)
    print(f"\n查询记录:")
    print(f"  操作者: {record.operator}")
    print(f"  操作类型: {record.operation_type}")
    print(f"  操作详情: {record.operation_detail}")
    print(f"  审计结果: {record.audit_result}")
    
    # 示例2：使用装饰器
    @tracer.trace("Claude", OperationType.AI_CALL, "分析文本")
    def analyze_text(text: str) -> Dict:
        return {"sentiment": "positive", "keywords": ["龍魂", "CNSH"]}
    
    result = analyze_text("龍魂终端太棒了！")
    print(f"\n装饰器追溯测试完成")
    print(f"分析结果: {result}")
