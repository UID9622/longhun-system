#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂协议审计器 L2 v1.0

焊死级别 (priority=0.90)
特性: 每次访问协议都要审计，追溯每个改动

审计协议文件的访问、修改、备份等所有操作。

DNA:#龍芯⚡️2026-06-07-PROTOCOL-AUDITOR-L2-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
UID: 9622

理论指导: 曾仕强老师 - 透明即信任
献礼: 献给龍魂 - 没有审计的权力就没有责任
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))

from dna import DNAVerifier
from logger import get_logger
from config import get_config


class ProtocolAuditor:
    """
    协议审计器 - 记录每一次接触

    意图: 透明度是龍魂系统的生命线
    """

    PROTOCOL_PATHS = [
        "~/longhun-system/protocols/CNSH_v2.0_ROOT_PROTOCOL.md",
        "~/longhun-system/protocols/CNSH_v2.0_ROOT_PROTOCOL_BILINGUAL.md",
    ]

    def __init__(self):
        """初始化审计器"""
        self.logger = get_logger()
        self.config = get_config()
        self.dna = DNAVerifier.generate("PROTOCOL-AUDITOR", "L2")

    def audit_protocol_access(self, protocol_path: str) -> Dict[str, Any]:
        """
        审计协议文件访问

        意图: 记录谁在什么时候访问了协议
        """
        path = Path(protocol_path).expanduser()

        if not path.exists():
            self.logger.log_error(
                "PROTOCOL_NOT_FOUND",
                f"协议文件不存在: {protocol_path}",
                self.dna
            )
            return {"success": False, "error": "File not found"}

        try:
            stat = path.stat()
            with open(path, 'rb') as f:
                content = f.read()
                fingerprint = hashlib.md5(content).hexdigest()

            audit_record = {
                "timestamp": datetime.now().isoformat(),
                "protocol": str(path),
                "file_size": stat.st_size,
                "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "fingerprint": fingerprint,
                "permissions": oct(stat.st_mode)[-3:],
                "dna": self.dna,
            }

            self.logger.log_operation(
                "L2",
                "protocol_accessed",
                self.dna,
                audit_record
            )

            return {"success": True, "audit_record": audit_record}

        except Exception as e:
            self.logger.log_error(
                "AUDIT_FAILED",
                str(e),
                self.dna,
                {"protocol": protocol_path}
            )
            return {"success": False, "error": str(e)}

    def audit_protocol_modification(
        self,
        protocol_path: str,
        previous_fingerprint: str,
        current_fingerprint: str
    ) -> Dict[str, Any]:
        """
        审计协议文件修改

        意图: 检测和记录所有改动
        """
        if previous_fingerprint == current_fingerprint:
            self.logger.log_operation(
                "L2",
                "protocol_unchanged",
                self.dna,
                {"protocol": protocol_path}
            )
            return {"success": True, "changed": False}

        # 如果指纹不同，这是一次修改
        self.logger.log_error(
            "PROTOCOL_MODIFICATION_DETECTED",
            f"协议文件被修改: {protocol_path}",
            self.dna,
            {
                "previous": previous_fingerprint,
                "current": current_fingerprint,
                "action": "INVESTIGATE"
            }
        )

        return {
            "success": True,
            "changed": True,
            "previous_fingerprint": previous_fingerprint,
            "current_fingerprint": current_fingerprint,
        }

    def audit_all_protocols(self) -> Dict[str, Any]:
        """
        审计所有协议文件

        意图: 定期全面扫描
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "protocols": [],
            "all_pass": True,
        }

        for protocol_path in self.PROTOCOL_PATHS:
            result = self.audit_protocol_access(protocol_path)
            results["protocols"].append(result)

            if not result.get("success"):
                results["all_pass"] = False

        self.logger.log_operation(
            "L2",
            "audit_completed",
            self.dna,
            {
                "total_protocols": len(self.PROTOCOL_PATHS),
                "success_count": sum(1 for r in results["protocols"] if r.get("success")),
                "all_pass": results["all_pass"],
            }
        )

        return results

    def generate_audit_report(self) -> str:
        """
        生成审计报告

        意图: 给老大一份清晰的审计总结
        """
        results = self.audit_all_protocols()

        report = f"""
{'='*60}
龍魂协议审计报告
{'='*60}

时间: {results['timestamp']}
DNA: {self.dna}

审计结果: {'✅ 全部通过' if results['all_pass'] else '❌ 存在问题'}

协议文件:
"""

        for i, protocol_result in enumerate(results["protocols"], 1):
            if protocol_result.get("success"):
                record = protocol_result["audit_record"]
                report += f"""
  {i}. {record['protocol']}
     - 大小: {record['file_size']} 字节
     - 指纹: {record['fingerprint']}
     - 权限: {record['permissions']}
     - 修改时间: {record['modified_time']}
"""

        report += f"\n{'='*60}\n"
        return report


if __name__ == "__main__":
    auditor = ProtocolAuditor()

    print("🐉 龍魂协议审计器 L2 v1.0")
    print("=" * 60)

    report = auditor.generate_audit_report()
    print(report)
