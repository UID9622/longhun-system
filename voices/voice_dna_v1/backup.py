#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂声纹备份与导出模块
Dragon Soul Voice Backup & Export

功能（321 原则）：
  - 本地备份：每天自动备份 manifest.json 到 ~/.龍魂/voice_anchors/backup/
  - 异地/用户备份：用户可手动导出自己的加密声纹DNA包
  - 关键快照：每季度或系统更新时导出完整快照

DNA: #龍芯⚡️20260628-VOICE-BACKUP-v1.0
"""

import os
import json
import zipfile
import shutil
import hashlib
import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

from voice_anchor import (
    BASE_DIR,
    MANIFEST_PATH,
    AUDIT_LOG_PATH,
    load_manifest,
    ensure_dirs,
)
from crypto import encrypt_export_payload, decrypt_export_payload

BACKUP_DIR = BASE_DIR / "backup"
SNAPSHOT_DIR = BASE_DIR / "snapshots"
EXPORT_DIR = BASE_DIR / "exports"


def ensure_backup_dirs() -> None:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def daily_backup() -> Dict[str, Any]:
    """
    本地备份：将 manifest.json 复制到 backup/，按日期命名。
    同一天多次执行会覆盖为最新版本。
    """
    ensure_backup_dirs()
    today = datetime.datetime.now().strftime("%Y%m%d")
    backup_path = BACKUP_DIR / f"manifest_backup_{today}.json"
    audit_backup_path = BACKUP_DIR / f"audit_backup_{today}.jsonl"

    if MANIFEST_PATH.exists():
        shutil.copy2(MANIFEST_PATH, backup_path)
    if AUDIT_LOG_PATH.exists():
        shutil.copy2(AUDIT_LOG_PATH, audit_backup_path)

    return {
        "status": "success",
        "type": "daily",
        "manifest_backup": str(backup_path),
        "audit_backup": str(audit_backup_path),
        "timestamp": datetime.datetime.now().isoformat(),
    }


def create_snapshot(label: Optional[str] = None) -> Dict[str, Any]:
    """
    关键快照：备份整个 voice_anchors 目录（含 manifest、音频、密钥、审计日志）。
    注意：快照包含解密密钥，需妥善保管。
    """
    ensure_backup_dirs()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"voice_anchors_snapshot_{ts}"
    if label:
        name += f"_{label}"
    snapshot_path = SNAPSHOT_DIR / f"{name}.zip"

    with zipfile.ZipFile(snapshot_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(BASE_DIR):
            # 跳过 exports 和 snapshots 自身，避免循环打包
            if any(x in Path(root).parts for x in ["exports", "snapshots"]):
                continue
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(BASE_DIR)
                zf.write(file_path, arcname)

    return {
        "status": "success",
        "type": "snapshot",
        "snapshot_path": str(snapshot_path),
        "timestamp": datetime.datetime.now().isoformat(),
    }


def list_backups() -> Dict[str, Any]:
    """列出所有本地备份与快照。"""
    ensure_backup_dirs()
    daily = sorted(BACKUP_DIR.glob("manifest_backup_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    snapshots = sorted(SNAPSHOT_DIR.glob("*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)
    return {
        "daily_backups": [{"path": str(p), "mtime": datetime.datetime.fromtimestamp(p.stat().st_mtime).isoformat()} for p in daily],
        "snapshots": [{"path": str(p), "mtime": datetime.datetime.fromtimestamp(p.stat().st_mtime).isoformat()} for p in snapshots],
    }


def export_user_package(
    user_id: str,
    persona_id: Optional[str] = None,
    password: str = "longhun-voice",
    output_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    用户自由导出：生成加密的声纹DNA包（ZIP）。

    包内含：
      - manifest_entry.json：该用户的身份记录（含加密特征）
      - voice_hash.txt：声纹哈希
      - dna.txt：DNA追溯码
      - payload.enc：使用用户密码加密的敏感载荷（便于用户二次迁移）
      - README.txt：说明

    Args:
        user_id: 用户ID
        persona_id: 可选，指定某条记录；None 则导出该用户全部
        password: 导出包加密密码
        output_path: 导出路径；None 则自动生成

    Returns:
        导出结果字典
    """
    from register import sanitize_user_id

    uid = sanitize_user_id(user_id)
    manifest = load_manifest()
    records = [
        r for r in manifest.get("anchors", [])
        if r.get("user_id", "system") == uid
        and (persona_id is None or r.get("persona_id") == persona_id)
    ]

    if not records:
        return {"status": "error", "message": "未找到该用户的声纹记录"}

    ensure_backup_dirs()
    if output_path is None:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        suffix = f"_{persona_id}" if persona_id else ""
        output_path = EXPORT_DIR / f"{uid}_voice_dna{suffix}_{ts}.zip"

    # 构建导出载荷
    export_payload = {
        "user_id": uid,
        "exported_at": datetime.datetime.now().isoformat(),
        "records": records,
    }
    payload_bytes = json.dumps(export_payload, ensure_ascii=False, indent=2).encode("utf-8")
    encrypted_payload = encrypt_export_payload(payload_bytes, uid, password)

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("manifest_entry.json", json.dumps(records, ensure_ascii=False, indent=2))
        zf.writestr("voice_hash.txt", "\n".join(r.get("voice_hash", "") for r in records))
        zf.writestr("dna.txt", "\n".join(r.get("dna", "") for r in records))
        zf.writestr("payload.enc", encrypted_payload)
        zf.writestr(
            "README.txt",
            "龍魂声纹DNA导出包\n"
            "- manifest_entry.json: 身份记录（特征向量已加密）\n"
            "- payload.enc: 使用导出密码二次加密的全量载荷\n"
            "- 用户可自行保存到任何位置，不影响龍魂系统内部锚定\n",
        )

    return {
        "status": "success",
        "user_id": uid,
        "records": len(records),
        "export_path": str(output_path),
        "password_protected": True,
        "timestamp": datetime.datetime.now().isoformat(),
    }


def import_user_package(
    zip_path: Path,
    user_id: str,
    password: str = "longhun-voice",
) -> Dict[str, Any]:
    """
    从加密导出包恢复用户声纹记录（导入到当前系统）。
    注意：仅导入元数据，不会覆盖已有相同 persona_id 的记录。
    """
    from register import sanitize_user_id

    uid = sanitize_user_id(user_id)
    with zipfile.ZipFile(zip_path, "r") as zf:
        encrypted_payload = zf.read("payload.enc").decode("utf-8")

    payload_bytes = decrypt_export_payload(encrypted_payload, uid, password)
    payload = json.loads(payload_bytes.decode("utf-8"))
    records = payload.get("records", [])

    manifest = load_manifest()
    existing_ids = {r.get("persona_id") for r in manifest.get("anchors", [])}
    imported = 0
    skipped = 0

    for record in records:
        if record.get("persona_id") in existing_ids:
            skipped += 1
            continue
        # 强制归属为当前用户
        record["user_id"] = uid
        manifest["anchors"].append(record)
        imported += 1

    from voice_anchor import save_manifest
    save_manifest(manifest)

    return {
        "status": "success",
        "imported": imported,
        "skipped": skipped,
    }


def should_run_daily_backup() -> bool:
    """检查今天是否已执行过本地备份。"""
    ensure_backup_dirs()
    today = datetime.datetime.now().strftime("%Y%m%d")
    return (BACKUP_DIR / f"manifest_backup_{today}.json").exists()


def auto_backup_if_needed() -> Optional[Dict[str, Any]]:
    """若今天未备份，则执行一次本地备份。"""
    if should_run_daily_backup():
        return None
    return daily_backup()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python backup.py <daily|snapshot|list|export> [args...]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "daily":
        print(json.dumps(daily_backup(), ensure_ascii=False, indent=2))
    elif cmd == "snapshot":
        label = sys.argv[2] if len(sys.argv) > 2 else None
        print(json.dumps(create_snapshot(label), ensure_ascii=False, indent=2))
    elif cmd == "list":
        print(json.dumps(list_backups(), ensure_ascii=False, indent=2))
    elif cmd == "export":
        if len(sys.argv) < 3:
            print("用法: python backup.py export <user_id> [persona_id]")
            sys.exit(1)
        uid = sys.argv[2]
        pid = sys.argv[3] if len(sys.argv) > 3 else None
        print(json.dumps(export_user_package(uid, pid), ensure_ascii=False, indent=2))
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)
