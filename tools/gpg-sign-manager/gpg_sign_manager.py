#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍魂 GPG簽署管理工具 · CNSH v2.0

功能：統一管理CNSH協議文檔與核心代碼的GPG簽名

DNA: #龍芯⚡️2026-06-08-GPG-SIGN-MANAGER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

# 配置
GPG_KEY_ID = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
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
        """讀取簽名日誌"""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except:
                return {"signatures": []}
        return {"signatures": []}

    def _save_logs(self):
        """保存簽名日誌"""
        with open(self.log_file, 'w') as f:
            json.dump(self.logs, f, indent=2, ensure_ascii=False)

    def check_gpg_key(self):
        """檢查GPG密鑰是否存在"""
        try:
            result = subprocess.run(
                ["gpg", "--list-keys", GPG_KEY_ID],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception as e:
            print(f"❌ 無法檢查GPG密鑰: {e}")
            return False

    def sign_file(self, filename):
        """簽署單個文件"""
        file_path = self.work_dir / filename

        if not file_path.exists():
            print(f"⚠️  文件不存在: {filename}")
            return False

        # 刪除舊的簽名文件
        asc_path = file_path.parent / f"{filename}.asc"
        if asc_path.exists():
            asc_path.unlink()

        try:
            print(f"簽名: {filename}")
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
                print(f"❌ 簽名失敗: {filename}")
                print(result.stderr)
                return False

            print(f"✅ 已簽名: {filename}.asc")

            # 記錄日誌
            self.logs["signatures"].append({
                "file": filename,
                "timestamp": datetime.now().isoformat(),
                "gpg_key": GPG_KEY_ID,
                "status": "success"
            })
            self._save_logs()

            return True
        except Exception as e:
            print(f"❌ 異常: {e}")
            return False

    def sign_all(self):
        """簽署所有文件"""
        if not self.check_gpg_key():
            print(f"🔴 未找到 GPG key: {GPG_KEY_ID}")
            print("請先確認該密鑰已導入本機。")
            return False

        print(f"📦 目錄: {self.work_dir}")
        print(f"🔐 使用 GPG key: {GPG_KEY_ID}")
        print("開始簽名...\n")

        success_count = 0
        for filename in SIGN_FILES:
            if self.sign_file(filename):
                success_count += 1

        print(f"\n✅ 完成: {success_count}/{len(SIGN_FILES)} 個文件簽名成功")
        print(f"簽名日誌已保存: {self.log_file}")

        return success_count == len(SIGN_FILES)

    def verify_signatures(self):
        """驗證已有的簽名"""
        print(f"驗證簽名...\n")

        for filename in SIGN_FILES:
            asc_path = self.work_dir / f"{filename}.asc"
            if not asc_path.exists():
                print(f"⚠️  簽名文件不存在: {filename}.asc")
                continue

            try:
                result = subprocess.run(
                    ["gpg", "--verify", str(asc_path), str(self.work_dir / filename)],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    print(f"✅ 驗證通過: {filename}")
                else:
                    print(f"❌ 驗證失敗: {filename}")
            except Exception as e:
                print(f"❌ 異常: {e}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🐉 龍魂 GPG簽署管理工具"
    )
    parser.add_argument(
        "--sign",
        action="store_true",
        help="簽署所有文件"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="驗證現有簽名"
    )
    parser.add_argument(
        "--dir",
        default=None,
        help="工作目錄（默認為當前目錄）"
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
