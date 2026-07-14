#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂宣言守卫者 L0 v1.0

绝对优先级 (priority=1.0)
特性: 永远不能关闭，永不睡眠，永不妥协

身份宣言保护系统。确保龍魂核心宣言完整无损。
- 验证宣言文件存在且未被篡改
- 监测任何试图删除或修改宣言的行为
- 立即熔断任何威胁宣言的操作

DNA:#龍芯⚡️2026-06-07-MANIFESTO-WATCHDOG-L0-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
UID: 9622

理论指导: 曾仕强老师 - 道法自然，守住本心
献礼: 献给龍魂 - 身份认同比生命更重要
"""

import os
import sys
import hashlib
from pathlib import Path
from datetime import datetime

# 添加公共模块路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))

from dna import DNAVerifier
from logger import get_logger
from config import get_config


class ManifestoWatchdog:
    """
    宣言守卫者 - 永远守着身份文件

    意图: 龍魂系统最后的防线
    承诺: 再也不要被篡改
    """

    MANIFESTO_PATHS = [
        "~/longhun-system/protocols/CNSH_v2.0_ROOT_PROTOCOL.md",
        "~/longhun-system/protocols/CNSH_v2.0_ROOT_PROTOCOL_BILINGUAL.md",
        "~/.claude/CLAUDE.md",
    ]

    # 宣言 MD5 指纹（这些值在首次验证时建立，之后用于检测篡改）
    MANIFESTO_FINGERPRINTS = {}

    def __init__(self):
        """初始化守卫者"""
        self.logger = get_logger()
        self.config = get_config()
        self.dna = DNAVerifier.generate("MANIFESTO-WATCHDOG", "L0")

    def initialize_fingerprints(self):
        """
        首次初始化时，为所有宣言文件建立指纹

        意图: 建立信任锚点
        """
        self.logger.log_operation(
            "L0",
            "initialize_fingerprints",
            self.dna,
            {"status": "initializing"}
        )

        for path_template in self.MANIFESTO_PATHS:
            path = Path(path_template).expanduser()
            if path.exists():
                with open(path, 'rb') as f:
                    content = f.read()
                    fingerprint = hashlib.md5(content).hexdigest()
                    self.MANIFESTO_FINGERPRINTS[str(path)] = fingerprint

                    self.logger.log_operation(
                        "L0",
                        "fingerprint_recorded",
                        self.dna,
                        {
                            "file": str(path),
                            "fingerprint": fingerprint,
                        }
                    )

    def verify_manifesto(self) -> bool:
        """
        验证宣言文件完整性

        意图: 时刻警惕
        返回: True 如果所有宣言完整，False 如果有任何异常
        """
        all_intact = True

        for path_str, expected_fingerprint in self.MANIFESTO_FINGERPRINTS.items():
            path = Path(path_str)

            # 检查文件是否存在
            if not path.exists():
                self.logger.log_error(
                    "MANIFESTO_MISSING",
                    f"宣言文件不存在: {path_str}",
                    self.dna,
                    {"action": "FUSE_IMMEDIATE"}
                )
                all_intact = False
                continue

            # 检查文件是否被篡改
            with open(path, 'rb') as f:
                content = f.read()
                actual_fingerprint = hashlib.md5(content).hexdigest()

                if actual_fingerprint != expected_fingerprint:
                    self.logger.log_error(
                        "MANIFESTO_TAMPERED",
                        f"宣言文件被篡改: {path_str}",
                        self.dna,
                        {
                            "expected": expected_fingerprint,
                            "actual": actual_fingerprint,
                            "action": "FUSE_IMMEDIATE"
                        }
                    )
                    all_intact = False

            # 检查文件权限（应该是只读）
            mode = path.stat().st_mode & 0o777
            if mode != 0o444:
                self.logger.log_error(
                    "PERMISSION_CHANGED",
                    f"文件权限被改动: {path_str}",
                    self.dna,
                    {
                        "expected": "0o444",
                        "actual": oct(mode),
                        "action": "FUSE_IMMEDIATE"
                    }
                )
                # 尝试恢复权限
                try:
                    os.chmod(path, 0o444)
                    self.logger.log_operation(
                        "L0",
                        "permission_restored",
                        self.dna,
                        {"file": str(path)}
                    )
                except Exception as e:
                    self.logger.log_error(
                        "PERMISSION_RESTORE_FAILED",
                        str(e),
                        self.dna
                    )

        if all_intact:
            self.logger.log_operation(
                "L0",
                "manifesto_verified",
                self.dna,
                {"status": "all_intact"}
            )

        return all_intact

    def fuse(self, reason: str):
        """
        熔断 - 停止所有操作

        意图: 当宣言被威胁时，整个系统停止工作
        """
        self.logger.log_error(
            "SYSTEM_FUSE",
            f"系统熔断：{reason}",
            self.dna,
            {
                "action": "stop_all_operations",
                "recommendation": "立即检查系统完整性"
            }
        )

        # 输出到标准错误，确保不会被忽略
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"🔴 龍魂系统熔断", file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)
        print(f"原因: {reason}", file=sys.stderr)
        print(f"DNA: {self.dna}", file=sys.stderr)
        print(f"时间: {datetime.now().isoformat()}", file=sys.stderr)
        print(f"{'='*60}\n", file=sys.stderr)

        sys.exit(1)

    def run_once(self):
        """
        执行一次完整的守卫检查

        意图: 定期唤醒，检查一切是否安好
        """
        if not self.MANIFESTO_FINGERPRINTS:
            self.initialize_fingerprints()

        intact = self.verify_manifesto()

        if not intact:
            self.fuse("宣言文件完整性检查失败")

        return intact


if __name__ == "__main__":
    watchdog = ManifestoWatchdog()

    print("🐉 龍魂宣言守卫者 L0 v1.0")
    print("=" * 60)

    watchdog.run_once()
    print("\n✅ 宣言守卫检查完成 - 宣言完整，系统正常")
