#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂恢复队列 (LongHun Recovery Queue)
DNA: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-LONGHUN-RECOVERY-QUEUE-v3.0

模块三：带 DNA 校验的恢复队列
"""

import os
import sys
import json
import shutil
import tarfile
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# 将 longhun-backup 脚本目录加入 sys.path
_BACKUP_SKILL_SCRIPTS = os.path.expanduser("~/.kimi-code/skills/longhun-backup/scripts")
if _BACKUP_SKILL_SCRIPTS not in sys.path:
    sys.path.insert(0, _BACKUP_SKILL_SCRIPTS)

from 备份管理器 import BackupManager
from 恢复系统 import RecoverySystem


DEFAULT_BACKUP_ROOT = os.path.expanduser("~/.longhun/backups")
QUEUE_FILE = os.path.expanduser("~/.longhun/audit/recovery_queue.jsonl")


def 生成_dna(操作类型: str) -> str:
    """生成标准 DNA 追溯码。"""
    时间戳 = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    return f"#龍芯⚡️{时间戳}-{操作类型}-UID9622"


class RecoveryQueue:
    """恢复队列：管理待恢复快照、完整性校验、DNA 链校验与执行。"""

    def __init__(self, backup_root: Optional[str] = None):
        self.备份根目录 = Path(backup_root) if backup_root else Path(DEFAULT_BACKUP_ROOT)
        self.备份根目录.mkdir(parents=True, exist_ok=True)
        self.队列文件 = Path(QUEUE_FILE)
        self.队列文件.parent.mkdir(parents=True, exist_ok=True)
        self.备份管理器 = BackupManager(str(self.备份根目录))
        self.恢复系统 = RecoverySystem(str(self.备份根目录))

    def _写入队列记录(self, 记录: Dict[str, Any]):
        """以 JSONL 形式追加队列记录。"""
        with open(self.队列文件, "a", encoding="utf-8") as f:
            f.write(json.dumps(记录, ensure_ascii=False) + "\n")

    def _读取队列记录(self) -> List[Dict]:
        """读取全部队列记录。"""
        记录列表 = []
        if not self.队列文件.exists():
            return 记录列表
        with open(self.队列文件, "r", encoding="utf-8") as f:
            for 行 in f:
                行 = 行.strip()
                if not 行:
                    continue
                try:
                    记录列表.append(json.loads(行))
                except json.JSONDecodeError:
                    continue
        return 记录列表

    def enqueue(self, snapshot_id: str) -> Dict[str, Any]:
        """把快照加入恢复队列，状态 pending。"""
        快照 = self.备份管理器.get_snapshot(snapshot_id)
        if not 快照:
            raise ValueError(f"快照不存在: {snapshot_id}")

        记录 = {
            "snapshot_id": snapshot_id,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "dna": 生成_dna("RECOVERY-ENQUEUE"),
        }
        self._写入队列记录(记录)
        return 记录

    def verify_integrity(self, snapshot_id: str, deep_check: bool = True) -> dict[str, Any]:
        """调用 RecoverySystem.verify_integrity()，返回验证报告（转 dict）。"""
        报告 = self.恢复系统.verify_integrity(snapshot_id, deep_check=deep_check)
        return {
            "snapshot_id": 报告.snapshot_id,
            "overall_status": 报告.overall_status,
            "archive_valid": 报告.archive_valid,
            "checksum_valid": 报告.checksum_valid,
            "manifest_valid": 报告.manifest_valid,
            "missing_files": 报告.missing_files,
            "corrupted_files": 报告.corrupted_files,
            "details": 报告.details,
        }

    def verify_dna_chain(self, snapshot_id: str) -> Dict[str, Any]:
        """
        读取快照的 manifest，检查其中 DNA 列表是否都以 #龍芯⚡️ 开头且按时间连续。
        同时要求 DNA 包含 UID9622。
        """
        快照目录 = self.备份根目录 / snapshot_id
        manifest路径 = 快照目录 / "backup_manifest.json"
        if not manifest路径.exists():
            return {
                "snapshot_id": snapshot_id,
                "valid": False,
                "reason": "manifest 不存在",
            }

        with open(manifest路径, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        dna链 = manifest.get("dna_chain")
        if not dna链:
            # 兼容旧 manifest：若只有单条 dna，则构造单元素列表
            单dna = manifest.get("dna")
            if 单dna:
                dna链 = [单dna]
            else:
                return {
                    "snapshot_id": snapshot_id,
                    "valid": False,
                    "reason": "manifest 中缺少 DNA 链",
                }

        if not isinstance(dna链, list):
            return {
                "snapshot_id": snapshot_id,
                "valid": False,
                "reason": "dna_chain 不是列表",
            }

        前缀 = "#龍芯⚡️"
        时间序列 = []
        for idx, dna in enumerate(dna链):
            if not isinstance(dna, str) or not dna.startswith(前缀):
                return {
                    "snapshot_id": snapshot_id,
                    "valid": False,
                    "reason": f"第 {idx + 1} 条 DNA 前缀不符合要求: {dna}",
                }
            if "UID9622" not in dna:
                return {
                    "snapshot_id": snapshot_id,
                    "valid": False,
                    "reason": f"第 {idx + 1} 条 DNA 缺少 UID9622: {dna}",
                }
            # 尝试提取时间戳：#龍芯⚡️<timestamp>-...
            主体 = dna[len(前缀):]
            时间部分 = 主体.split("-")[0]
            try:
                时间序列.append(int(时间部分))
            except ValueError:
                return {
                    "snapshot_id": snapshot_id,
                    "valid": False,
                    "reason": f"第 {idx + 1} 条 DNA 时间戳不可解析: {dna}",
                }

        # 检查时间连续（非递减）
        for i in range(1, len(时间序列)):
            if 时间序列[i] < 时间序列[i - 1]:
                return {
                    "snapshot_id": snapshot_id,
                    "valid": False,
                    "reason": f"DNA 链时间戳不连续: 第 {i} 条 > 第 {i + 1} 条",
                }

        return {
            "snapshot_id": snapshot_id,
            "valid": True,
            "dna_count": len(dna链),
            "dna_chain": dna链,
        }

    def human_confirm(self) -> bool:
        """
        人工确认恢复。
        若环境变量 LONGHUN_RECOVERY_CONFIRM=YES 则返回 True；
        否则向 stdin 询问，非交互环境下默认 False。
        """
        if os.environ.get("LONGHUN_RECOVERY_CONFIRM", "").strip().upper() == "YES":
            return True

        if not sys.stdin.isatty():
            return False

        try:
            回答 = input("确认恢复？(y/N) ").strip().lower()
        except EOFError:
            return False

        return 回答 in ("y", "yes")

    def execute_restore(self, snapshot_id: str, target_path: str) -> Dict[str, Any]:
        """
        先创建恢复点（把当前 target_path 备份到临时目录），
        再调用 RecoverySystem.restore_snapshot() 恢复，
        恢复后再次验证完整性。
        """
        快照 = self.备份管理器.get_snapshot(snapshot_id)
        if not 快照:
            raise ValueError(f"快照不存在: {snapshot_id}")

        目标路径 = Path(target_path)
        恢复点路径 = None

        # 1. 创建恢复点
        if 目标路径.exists() and any(目标路径.iterdir()):
            恢复点根目录 = self.备份根目录 / "recovery_points"
            恢复点根目录.mkdir(parents=True, exist_ok=True)
            恢复点id = f"RP_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]}"
            恢复点路径 = 恢复点根目录 / 恢复点id
            恢复点路径.mkdir(parents=True, exist_ok=True)
            恢复点归档 = 恢复点路径 / f"{恢复点id}.tar.gz"
            with tarfile.open(str(恢复点归档), "w:gz") as tar:
                tar.add(str(目标路径), arcname=".")

        # 2. 执行恢复
        恢复结果 = self.恢复系统.restore_snapshot(
            snapshot_id,
            target_path,
            verify_before=True,
            dry_run=False,
        )

        # 3. 恢复后再次验证完整性
        二次校验报告 = self.verify_integrity(snapshot_id, deep_check=True)

        return {
            "restore_id": 恢复结果.restore_id,
            "snapshot_id": snapshot_id,
            "target_path": target_path,
            "status": 恢复结果.status,
            "restored_files": 恢复结果.restored_files,
            "failed_files": 恢复结果.failed_files,
            "recovery_point": str(恢复点路径) if 恢复点路径 else None,
            "post_restore_integrity": 二次校验报告,
            "timestamp": datetime.now().isoformat(),
            "dna": 生成_dna("RECOVERY-EXECUTE"),
        }

    def status(self) -> List[Dict]:
        """返回队列中所有快照状态。"""
        return self._读取队列记录()


def main():
    parser = argparse.ArgumentParser(description="龍魂恢复队列")
    parser.add_argument("--root", default=DEFAULT_BACKUP_ROOT, help="备份根目录")
    parser.add_argument("--enqueue", metavar="SNAPSHOT_ID", help="把快照加入恢复队列")
    parser.add_argument("--status", action="store_true", help="显示队列状态")
    parser.add_argument("--verify", metavar="SNAPSHOT_ID", help="验证快照完整性")
    parser.add_argument("--restore", metavar="SNAPSHOT_ID", help="执行恢复")
    parser.add_argument("--target", help="恢复目标路径（与 --restore 联用）")
    parser.add_argument("--confirm", action="store_true", help="与 --restore 联用时自动设置确认")

    args = parser.parse_args()

    队列 = RecoveryQueue(args.root)

    if args.enqueue:
        记录 = 队列.enqueue(args.enqueue)
        print(f"已加入队列: {记录['snapshot_id']} | 状态: {记录['status']} | DNA: {记录['dna']}")

    elif args.status:
        状态列表 = 队列.status()
        print(f"队列共 {len(状态列表)} 条记录:")
        for 记录 in 状态列表:
            print(f"  - {记录}")

    elif args.verify:
        完整性 = 队列.verify_integrity(args.verify)
        dna链 = 队列.verify_dna_chain(args.verify)
        print("完整性验证:")
        for k, v in 完整性.items():
            print(f"  {k}: {v}")
        print("DNA 链验证:")
        for k, v in dna链.items():
            print(f"  {k}: {v}")

    elif args.restore:
        if not args.target:
            parser.error("--restore 必须搭配 --target")
        if args.confirm:
            os.environ["LONGHUN_RECOVERY_CONFIRM"] = "YES"
        if not 队列.human_confirm():
            print("未获得确认，取消恢复。")
            return
        结果 = 队列.execute_restore(args.restore, args.target)
        print("恢复结果:")
        for k, v in 结果.items():
            print(f"  {k}: {v}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
