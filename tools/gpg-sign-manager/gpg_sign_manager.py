#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍魂 GPG签署管理工具 · CNSH v2.0

功能：统一管理CNSH协议文档与核心代码的GPG签名

DNA:#龍芯⚡️2026-06-08-GPG-SIGN-MANAGER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

from integrated_modules.longhun_config import getenv

# 配置
GPG_KEY_ID = getenv("GPG_FINGERPRINT", "A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
SIGN_FILES = [
    "CNSH_v2.0_SIGNATURE.md",
    "CNSH_v2.0_FULL_PROTOCOL_SIGNATURE.md",
    "cnsh_gateway.py",
    "cnsh.py",
]

class GPGSignManager:
    def __init__(self, work_dir=None):
        self.work_dir = Path(work_dir or os.getcwd())
        self.log_file = self.work_dir / "gpg_sign_log.json"
        self.logs = self._load_logs()

    def _load_logs(self):
        """读取签名日志"""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except:
                return {"signatures": []}
        return {"signatures": []}

    def _save_logs(self):
        """保存签名日志"""
        with open(self.log_file, 'w') as f:
            json.dump(self.logs, f, indent=2, ensure_ascii=False)

    def check_gpg_key(self):
        """检查GPG密钥是否存在"""
        try:
            result = subprocess.run(
                ["gpg", "--list-keys", GPG_KEY_ID],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            print(f"❌ 无法检查GPG密钥: {e}")
            return False

    def sign_file(self, filename):
        """签署单个文件"""
        file_path = self.work_dir / filename

        if not file_path.exists():
            print(f"⚠️  文件不存在: {filename}")
            return False

        # 删除旧的签名文件
        asc_path = file_path.parent / f"{filename}.asc"
        if asc_path.exists():
            asc_path.unlink()

        try:
            print(f"签名: {filename}")
            result = subprocess.run(
                [
                    "gpg",
                    "--yes",
                    "--batch",
                    "--detach-sign",
                    "--armor",
                    "--default-key", GPG_KEY_ID,
                    str(file_path)
                ],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print(f"❌ 签名失败: {filename}")
                print(result.stderr)
                return False

            print(f"✅ 已签名: {filename}.asc")

            # 记录日志
            self.logs["signatures"].append({
                "file": filename,
                "timestamp": datetime.now().isoformat(),
                "gpg_key": GPG_KEY_ID,
                "status": "success"
            })
            self._save_logs()

            return True
        except Exception as e:
            print(f"❌ 异常: {e}")
            return False

    def sign_all(self):
        """签署所有文件"""
        if not self.check_gpg_key():
            print(f"🔴 未找到 GPG key: {GPG_KEY_ID}")
            print("请先确认该密钥已导入本机。")
            return False

        print(f"📦 目录: {self.work_dir}")
        print(f"🔐 使用 GPG key: {GPG_KEY_ID}")
        print("开始签名...\n")

        success_count = 0
        for filename in SIGN_FILES:
            if self.sign_file(filename):
                success_count += 1

        print(f"\n✅ 完成: {success_count}/{len(SIGN_FILES)} 个文件签名成功")
        print(f"签名日志已保存: {self.log_file}")

        return success_count == len(SIGN_FILES)

    def verify_signatures(self):
        """验证已有的签名"""
        print(f"验证签名...\n")

        for filename in SIGN_FILES:
            asc_path = self.work_dir / f"{filename}.asc"
            if not asc_path.exists():
                print(f"⚠️  签名文件不存在: {filename}.asc")
                continue

            try:
                result = subprocess.run(
                    ["gpg", "--verify", str(asc_path), str(self.work_dir / filename)],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    print(f"✅ 验证通过: {filename}")
                else:
                    print(f"❌ 验证失败: {filename}")
            except Exception as e:
                print(f"❌ 异常: {e}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🐉 龍魂 GPG签署管理工具"
    )
    parser.add_argument(
        "--sign",
        action="store_true",
        help="签署所有文件"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="验证现有签名"
    )
    parser.add_argument(
        "--dir",
        default=None,
        help="工作目录（默认为当前目录）"
    )

    args = parser.parse_args()

    manager = GPGSignManager(work_dir=args.dir)

    if args.sign:
        success = manager.sign_all()
        sys.exit(0 if success else 1)
    elif args.verify:
        manager.verify_signatures()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
