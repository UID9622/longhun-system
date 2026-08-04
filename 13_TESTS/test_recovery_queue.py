#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢复队列测试
DNA: #龍芯⚡️2026-06-29-LONGHUN-RECOVERY-QUEUE-TEST-UID9622
"""

import os
import sys
import json
import filecmp
import tempfile
import unittest
from pathlib import Path
from datetime import datetime

# 确保能导入 audit 目录下的恢复队列
sys.path.insert(0, str(Path(__file__).parent.parent / "audit"))
from recovery_queue import RecoveryQueue

# 引入备份管理器以创建测试快照
_BACKUP_SKILL_SCRIPTS = os.path.expanduser("~/.kimi-code/skills/longhun-backup/scripts")
if _BACKUP_SKILL_SCRIPTS not in sys.path:
    sys.path.insert(0, _BACKUP_SKILL_SCRIPTS)

from 备份管理器 import BackupManager


def 生成_dna(时间戳: int, 操作类型: str) -> str:
    """生成测试用 DNA，包含 UID9622。"""
    return f"#龍芯⚡️{时间戳}-{操作类型}-UID9622"


class TestRecoveryQueue(unittest.TestCase):
    def setUp(self):
        self.临时根目录 = tempfile.mkdtemp(prefix="longhun_recovery_queue_test_")
        self.源目录 = Path(self.临时根目录) / "source"
        self.源目录.mkdir(parents=True)
        self.恢复目标目录 = Path(self.临时根目录) / "restored"
        self.恢复目标目录.mkdir(parents=True)
        self.备份根目录 = Path(self.临时根目录) / "backups"
        self.备份根目录.mkdir(parents=True)

        # 写入一些测试文件
        (self.源目录 / "README.md").write_text("# 测试源\n", encoding="utf-8")
        (self.源目录 / "config.json").write_text(json.dumps({"key": "value"}, ensure_ascii=False), encoding="utf-8")
        子目录 = self.源目录 / "L2_scripts"
        子目录.mkdir()
        (子目录 / "main.py").write_text("print('hello longhun')\n", encoding="utf-8")

        # 创建快照
        self.备份管理器 = BackupManager(str(self.备份根目录))
        self.快照 = self.备份管理器.full_backup(str(self.源目录), layers=["L1", "L2", "L3"], label="test_snapshot")
        self.快照id = self.快照.id

        # 给 manifest 注入 dna_chain，满足 DNA 校验要求
        self._注入_dna链()

        self.队列 = RecoveryQueue(str(self.备份根目录))

    def tearDown(self):
        import shutil
        shutil.rmtree(self.临时根目录, ignore_errors=True)

    def _注入_dna链(self):
        manifest路径 = self.备份根目录 / self.快照id / "backup_manifest.json"
        with open(manifest路径, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        基础时间 = int(datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3])
        manifest["dna_chain"] = [
            生成_dna(基础时间, "BACKUP-CREATE"),
            生成_dna(基础时间 + 1, "BACKUP-VERIFY"),
            生成_dna(基础时间 + 2, "BACKUP-COMPLETE"),
        ]
        manifest["dna"] = manifest["dna_chain"][-1]

        with open(manifest路径, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

    def test_完整恢复流程(self):
        # 1. enqueue
        记录 = self.队列.enqueue(self.快照id)
        self.assertEqual(记录["snapshot_id"], self.快照id)
        self.assertEqual(记录["status"], "pending")
        self.assertTrue(记录["dna"].startswith("#龍芯⚡️"))

        # 2. verify_integrity
        完整性报告 = self.队列.verify_integrity(self.快照id)
        self.assertIn(完整性报告["overall_status"], ("ok", "warning"))
        self.assertTrue(完整性报告["archive_valid"])
        self.assertTrue(完整性报告["checksum_valid"])

        # 3. verify_dna_chain
        dna链报告 = self.队列.verify_dna_chain(self.快照id)
        self.assertTrue(dna链报告["valid"], msg=dna链报告.get("reason"))
        self.assertEqual(dna链报告["dna_count"], 3)

        # 4. 设置确认环境变量并执行恢复
        os.environ["LONGHUN_RECOVERY_CONFIRM"] = "YES"
        try:
            恢复结果 = self.队列.execute_restore(self.快照id, str(self.恢复目标目录))
        finally:
            os.environ.pop("LONGHUN_RECOVERY_CONFIRM", None)

        self.assertEqual(恢复结果["status"], "completed")
        self.assertEqual(len(恢复结果["failed_files"]), 0)
        self.assertEqual(恢复结果["post_restore_integrity"]["overall_status"], "ok")

        # 5. 断言恢复目录与源目录一致
        对比 = filecmp.dircmp(str(self.恢复目标目录), str(self.源目录))
        self.assertEqual(对比.left_only, [])
        self.assertEqual(对比.right_only, [])
        self.assertEqual(对比.diff_files, [])

    def test_队列状态(self):
        self.队列.enqueue(self.快照id)
        状态列表 = self.队列.status()
        self.assertTrue(len(状态列表) >= 1)
        self.assertTrue(any(记录["snapshot_id"] == self.快照id for 记录 in 状态列表))

    def test_human_confirm_环境变量(self):
        os.environ["LONGHUN_RECOVERY_CONFIRM"] = "YES"
        try:
            self.assertTrue(self.队列.human_confirm())
        finally:
            os.environ.pop("LONGHUN_RECOVERY_CONFIRM", None)

        os.environ["LONGHUN_RECOVERY_CONFIRM"] = "NO"
        try:
            self.assertFalse(self.队列.human_confirm())
        finally:
            os.environ.pop("LONGHUN_RECOVERY_CONFIRM", None)


if __name__ == "__main__":
    unittest.main()
