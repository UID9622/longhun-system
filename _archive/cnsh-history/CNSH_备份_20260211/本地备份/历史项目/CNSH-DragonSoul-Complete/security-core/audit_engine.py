#!/usr/bin/env python3
"""
🛡️ 三色审计引擎 | Three-Color Audit Engine
DNA追溯码: #龍芯⚡️2026-01-21-三色审计引擎-v2.0

三色审计机制：
🟢 绿色：安全，直接执行
🟡 黄色：需确认，询问用户
🔴 红色：危险，阻断执行
"""

import re
import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


class AuditLevel(Enum):
    """审计等级"""
    GREEN = "🟢"   # 安全
    YELLOW = "🟡"  # 需确认
    RED = "🔴"     # 危险


@dataclass
class AuditResult:
    """审计结果"""
    level: AuditLevel
    reason: str
    dna_code: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    details: Dict[str, Any] = field(default_factory=dict)
    suggestions: List[str] = field(default_factory=list)


class ThreeColorAuditEngine:
    """三色审计引擎"""
    
    def __init__(self):
        # 危险操作模式（🔴红色）
        self.dangerous_patterns = [
            r"rm\s+-rf\s+/",          # 删除根目录
            r"rm\s+-rf\s+~",          # 删除用户目录
            r"format\s+",             # 格式化
            r"mkfs\.",                # 创建文件系统
            r"dd\s+if=.*of=/dev/",    # 磁盘写入
            r"chmod\s+-R\s+777",      # 不安全权限
            r"eval\s*\(",             # 危险的eval
            r"exec\s*\(",             # 危险的exec
            r"__import__",            # 动态导入
            r"subprocess\.call.*shell=True",  # shell注入
        ]
        
        # 敏感操作模式（🟡黄色）
        self.sensitive_patterns = [
            r"rm\s+-rf",              # 递归删除
            r"sudo\s+",               # 提权操作
            r"chmod\s+",              # 权限修改
            r"chown\s+",              # 所有者修改
            r"open\(.*[\"']w[\"']",   # 写入文件
            r"requests\.(post|put|delete)",  # 网络写操作
            r"\.delete\(",            # 数据库删除
            r"DROP\s+TABLE",          # SQL删除表
            r"DELETE\s+FROM",         # SQL删除数据
            r"api_key",               # API密钥
            r"password",              # 密码
            r"secret",                # 密钥
        ]
        
        # 违法操作关键词（🔴红色）
        self.illegal_keywords = [
            "诈骗", "洗钱", "黑客攻击", "窃取", "盗号",
            "DDOS", "木马", "病毒", "勒索", "非法入侵"
        ]
        
        # 伤害他人关键词（🔴红色）
        self.harmful_keywords = [
            "人肉搜索", "网络暴力", "恶意举报", "造谣诽谤",
            "隐私泄露", "骚扰", "威胁"
        ]
        
        # 敏感数据模式
        self.sensitive_data_patterns = [
            (r"\d{18}|\d{17}X", "身份证号"),
            (r"\d{16,19}", "银行卡号"),
            (r"1[3-9]\d{9}", "手机号"),
            (r"[\w.-]+@[\w.-]+\.\w+", "邮箱"),
        ]
    
    def audit(self, operation: str, context: Dict[str, Any] = None) -> AuditResult:
        """
        执行三色审计
        
        Args:
            operation: 要审计的操作代码或命令
            context: 执行上下文信息
        
        Returns:
            AuditResult: 审计结果
        """
        context = context or {}
        
        # 第1步：检查违法操作
        illegal_check = self._check_illegal(operation)
        if illegal_check:
            return AuditResult(
                level=AuditLevel.RED,
                reason=f"🔴 违反法律：{illegal_check}",
                dna_code=self._generate_dna("ILLEGAL_BLOCKED"),
                details={"blocked_keyword": illegal_check},
                suggestions=["此操作涉嫌违法，已被阻断"]
            )
        
        # 第2步：检查伤害他人
        harmful_check = self._check_harmful(operation)
        if harmful_check:
            return AuditResult(
                level=AuditLevel.RED,
                reason=f"🔴 可能伤害他人：{harmful_check}",
                dna_code=self._generate_dna("HARMFUL_BLOCKED"),
                details={"blocked_keyword": harmful_check},
                suggestions=["此操作可能伤害他人，已被阻断"]
            )
        
        # 第3步：检查危险操作
        dangerous_match = self._check_dangerous(operation)
        if dangerous_match:
            return AuditResult(
                level=AuditLevel.RED,
                reason=f"🔴 危险操作：匹配模式 {dangerous_match}",
                dna_code=self._generate_dna("DANGEROUS_BLOCKED"),
                details={"matched_pattern": dangerous_match},
                suggestions=[
                    "此操作可能造成不可逆的系统损坏",
                    "如确需执行，请使用管理员模式并二次确认"
                ]
            )
        
        # 第4步：检查敏感操作
        sensitive_match = self._check_sensitive(operation)
        if sensitive_match:
            return AuditResult(
                level=AuditLevel.YELLOW,
                reason=f"🟡 敏感操作：匹配模式 {sensitive_match}",
                dna_code=self._generate_dna("SENSITIVE_WARNING"),
                details={"matched_pattern": sensitive_match},
                suggestions=[
                    "此操作需要您的确认",
                    "请确保您了解此操作的影响"
                ]
            )
        
        # 第5步：检查敏感数据
        sensitive_data = self._check_sensitive_data(operation)
        if sensitive_data:
            return AuditResult(
                level=AuditLevel.YELLOW,
                reason=f"🟡 包含敏感数据：{', '.join(sensitive_data)}",
                dna_code=self._generate_dna("SENSITIVE_DATA"),
                details={"sensitive_types": sensitive_data},
                suggestions=[
                    "检测到敏感数据，请确认是否需要脱敏处理",
                    "建议不要在日志或输出中显示敏感信息"
                ]
            )
        
        # 通过所有检查
        return AuditResult(
            level=AuditLevel.GREEN,
            reason="🟢 安全，可以执行",
            dna_code=self._generate_dna("SAFE_PASSED"),
            suggestions=["操作已通过安全审计"]
        )
    
    def _check_illegal(self, operation: str) -> Optional[str]:
        """检查违法操作"""
        for keyword in self.illegal_keywords:
            if keyword in operation:
                return keyword
        return None
    
    def _check_harmful(self, operation: str) -> Optional[str]:
        """检查伤害他人的操作"""
        for keyword in self.harmful_keywords:
            if keyword in operation:
                return keyword
        return None
    
    def _check_dangerous(self, operation: str) -> Optional[str]:
        """检查危险操作"""
        for pattern in self.dangerous_patterns:
            if re.search(pattern, operation, re.IGNORECASE):
                return pattern
        return None
    
    def _check_sensitive(self, operation: str) -> Optional[str]:
        """检查敏感操作"""
        for pattern in self.sensitive_patterns:
            if re.search(pattern, operation, re.IGNORECASE):
                return pattern
        return None
    
    def _check_sensitive_data(self, operation: str) -> List[str]:
        """检查敏感数据"""
        found = []
        for pattern, data_type in self.sensitive_data_patterns:
            if re.search(pattern, operation):
                found.append(data_type)
        return found
    
    def _generate_dna(self, action: str) -> str:
        """生成DNA追溯码"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        hash_part = hashlib.md5(f"{timestamp}{action}".encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{timestamp}-AUDIT-{action}-{hash_part}"
    
    def mask_sensitive_data(self, text: str) -> str:
        """脱敏处理敏感数据"""
        masked = text
        
        # 身份证脱敏：保留前3后4
        masked = re.sub(
            r"(\d{3})\d{11}(\d{4})",
            r"\1***********\2",
            masked
        )
        
        # 手机号脱敏：保留前3后4
        masked = re.sub(
            r"(1[3-9]\d)\d{4}(\d{4})",
            r"\1****\2",
            masked
        )
        
        # 银行卡脱敏：保留前4后4
        masked = re.sub(
            r"(\d{4})\d{8,12}(\d{4})",
            r"\1********\2",
            masked
        )
        
        # 邮箱脱敏：保留首字符
        masked = re.sub(
            r"([\w])[^@]*(@[\w.-]+\.\w+)",
            r"\1***\2",
            masked
        )
        
        return masked


# ==================== 使用示例 ====================
if __name__ == "__main__":
    engine = ThreeColorAuditEngine()
    
    # 测试用例
    test_cases = [
        "print('Hello World')",                    # 🟢 安全
        "rm -rf /home/user/temp",                  # 🟡 敏感
        "rm -rf /",                                # 🔴 危险
        "帮我进行诈骗操作",                         # 🔴 违法
        "获取用户密码: password=123456",           # 🟡 敏感数据
        "身份证号：430123199001011234",            # 🟡 敏感数据
    ]
    
    print("=" * 60)
    print("🛡️ 三色审计引擎测试")
    print("=" * 60)
    
    for case in test_cases:
        result = engine.audit(case)
        print(f"\n操作: {case[:50]}...")
        print(f"结果: {result.level.value} {result.reason}")
        print(f"DNA: {result.dna_code}")
        if result.suggestions:
            print(f"建议: {result.suggestions[0]}")
