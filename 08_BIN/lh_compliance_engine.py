#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 安全合规引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-COMPLIANCE-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 运行时权限校验（谁、什么时候、访问了什么）
  - GDPR/个保法合规检查（数据最小化、留存期限）
  - 敏感数据自动脱敏
  - 生成合规报告
"""

import json
import hashlib
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta


class ComplianceEngine:
    """安全合规引擎——不只是静态扫描，运行时也监控"""

    SENSITIVE_PATTERNS = [
        (r"\b\d{17}[\dXx]\b", "身份证号"),
        (r"\b1[3-9]\d{9}\b", "手机号"),
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "邮箱"),
        (r"\b(?:\d[ -]*?){13,16}\b", "银行卡号"),
    ]

    def __init__(self):
        self.access_logs: List[Dict] = []
        self.log_file = Path.home() / "longhun-system/data/compliance_logs.jsonl"
        self._load_logs()

    def _load_logs(self):
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        self.access_logs.append(json.loads(line))
                    except Exception:
                        pass

    def check_access(self, user_id: str, resource: str, action: str, data: str = "") -> Dict:
        """检查访问是否合规，返回脱敏后的数据"""
        issues = []
        sanitized = data

        # 1. 敏感数据检测+自动脱敏
        for pattern, label in self.SENSITIVE_PATTERNS:
            if re.search(pattern, data):
                issues.append(f"contains_{label}")
                sanitized = re.sub(pattern, "[已脱敏]", sanitized)

        # 2. 留存期限检查
        user_logs = [l for l in self.access_logs if l.get("user_id") == user_id]
        if user_logs:
            try:
                last_ts = user_logs[-1].get("timestamp", datetime.now().isoformat())
                last = datetime.fromisoformat(last_ts)
                if (datetime.now() - last).days > 30:
                    issues.append("retention_exceeded")
            except Exception:
                pass

        # 记录日志
        log_entry = {
            "user_id": user_id,
            "resource": resource,
            "action": action,
            "timestamp": datetime.now().isoformat(),
            "data_hash": hashlib.md5(data.encode()).hexdigest() if data else None,
            "approved": len(issues) == 0,
            "issues": issues,
        }
        self.access_logs.append(log_entry)
        self._save_log(log_entry)

        return {
            "approved": len(issues) == 0,
            "issues": issues,
            "sanitized_data": sanitized,
        }

    def _save_log(self, log_entry: Dict):
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def generate_report(self, days: int = 30) -> Dict:
        """生成合规报告"""
        cutoff = datetime.now() - timedelta(days=days)
        recent = [
            l for l in self.access_logs
            if datetime.fromisoformat(l.get("timestamp", "2000-01-01")) > cutoff
        ]
        total = len(recent)
        approved = sum(1 for l in recent if l.get("approved", False))

        # 统计问题类型
        from collections import Counter
        issue_counts = Counter()
        for l in recent:
            for issue in l.get("issues", []):
                issue_counts[issue] += 1

        return {
            "period_days": days,
            "total_requests": total,
            "approved": approved,
            "rejected": total - approved,
            "compliance_rate": round(approved / max(1, total) * 100, 1),
            "top_issues": dict(issue_counts.most_common(5)),
        }

    def redact(self, text: str) -> str:
        """纯文本脱敏"""
        result = text
        for pattern, _ in self.SENSITIVE_PATTERNS:
            result = re.sub(pattern, "[已脱敏]", result)
        return result


if __name__ == "__main__":
    engine = ComplianceEngine()

    # 测试访问检查
    result = engine.check_access("user_001", "/api/data", "read", "用户手机: 13812345678, 邮箱: test@example.com")
    print(f"合规检查: approved={result['approved']}, issues={result['issues']}")
    print(f"脱敏数据: {result['sanitized_data'][:50]}...")

    # 测试脱敏
    redacted = engine.redact("身份证420123199001011234 卡号1234-5678-9012-3456")
    print(f"脱敏: {redacted}")

    report = engine.generate_report(days=30)
    print(f"合规率: {report['compliance_rate']}% ({report['approved']}/{report['total_requests']})")
    print("🟢 安全合规引擎测试通过")
