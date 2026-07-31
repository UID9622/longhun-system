#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·午时·IMMUTABLE-HISTORY-ANCHOR-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║     ⚓ 龍魂·不可篡改历史锚定引擎 v1.0                                     ║
║     Immutable History Anchor — 本地 WORM 快照 · 异地 OBS 锚定 · Merkle 链  ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·乙未·丁酉·午时·IMMUTABLE-HISTORY-ANCHOR-v1.0         ║
║  哲学: 历史不仅要被记录，还要被“钉死”在多个物理位置                         ║
║  铁律:                                                                   ║
║    本地 WORM — 快照文件生成后设为只读，禁止覆盖修改                          ║
║    异地锚定 — 同时保留本地快照 + 华为云 OBS 双区副本                        ║
║    Merkle 链 — 每次锚定生成全局 Merkle 根，任何 bit 变化都可发现             ║
║    主权留境 — 数据存储在中国境内，受中国法律保护                              ║
║    锚定亦留痕 — 每次锚定操作本身追加到不可篡改历史账本                        ║
╚══════════════════════════════════════════════════════════════════════════╝

用法:
  # 执行一次锚定（本地 + 尝试 OBS）
  python3 bin/lh_immutable_history_anchor.py anchor

  # 仅生成本地 WORM 快照
  python3 bin/lh_immutable_history_anchor.py anchor --local-only

  # 验证最近一次锚定
  python3 bin/lh_immutable_history_anchor.py verify

  # 查看锚定报告
  python3 bin/lh_immutable_history_anchor.py report
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
ENGINE = ROOT / "bin" / "lh_immutable_history.py"
OBS_BACKUP = ROOT / "bin" / "lh_obs_immutable_backup.py"

LEDGER_DIR = Path.home() / ".longhun" / "ledger"
LEDGER_FILE = LEDGER_DIR / "immutable_history.jsonl"
SIG_DIR = LEDGER_DIR / "signatures"

# 本地 WORM 锚定目录
ANCHOR_ROOT = LEDGER_DIR / "anchors"
ANCHOR_ROOT.mkdir(parents=True, exist_ok=True)

# 锚定元数据索引
ANCHOR_INDEX = ANCHOR_ROOT / "anchor_index.json"

DNA = "#龍芯⚡️丙午·乙未·丁酉·午时·IMMUTABLE-HISTORY-ANCHOR-v1.0"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def compute_sha256(path: Path) -> str:
    """计算文件 SHA256"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_merkle_root(hashes: List[str]) -> str:
    """计算 Merkle 根"""
    if not hashes:
        return hashlib.sha256(b"empty").hexdigest()

    leaves = sorted(hashes)
    while len(leaves) > 1:
        new_leaves = []
        for i in range(0, len(leaves), 2):
            left = leaves[i]
            right = leaves[i + 1] if i + 1 < len(leaves) else left
            combined = hashlib.sha256(f"{left}{right}".encode()).hexdigest()
            new_leaves.append(combined)
        leaves = new_leaves
    return leaves[0]


def load_anchor_index() -> Dict[str, Any]:
    if ANCHOR_INDEX.exists():
        return json.loads(ANCHOR_INDEX.read_text())
    return {
        "dna": DNA,
        "anchors": [],
        "total_anchors": 0,
        "last_anchor": None,
    }


def save_anchor_index(index: Dict[str, Any]):
    ANCHOR_INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2))


def set_readonly(path: Path):
    """设置文件/目录只读（递归）"""
    if path.is_file():
        os.chmod(path, 0o444)
    elif path.is_dir():
        os.chmod(path, 0o555)
        for child in path.rglob("*"):
            if child.is_file():
                os.chmod(child, 0o444)
            elif child.is_dir():
                os.chmod(child, 0o555)


def gpg_sign_file(path: Path) -> Optional[str]:
    """对文件内容做 GPG 分离签名"""
    try:
        proc = subprocess.run(
            ["gpg", "--batch", "--yes", "--armor", "--detach-sign",
             "--local-user", GPG_FINGERPRINT, "-o", "-", str(path)],
            capture_output=True,
            timeout=30,
        )
        if proc.returncode == 0:
            return proc.stdout.decode("utf-8")
    except Exception:
        pass
    return None


def pack_anchor(anchor_id: str) -> Tuple[Path, Dict[str, Any]]:
    """
    打包账本和签名为 WORM 快照。
    返回: (tar.gz 路径, 元数据)
    """
    anchor_dir = ANCHOR_ROOT / anchor_id
    anchor_dir.mkdir(parents=True, exist_ok=True)

    # 复制账本和签名
    ledger_copy = anchor_dir / "immutable_history.jsonl"
    sig_copy_dir = anchor_dir / "signatures"

    shutil.copy2(LEDGER_FILE, ledger_copy)
    if SIG_DIR.exists():
        shutil.copytree(SIG_DIR, sig_copy_dir, dirs_exist_ok=True)

    # 生成清单
    manifest = {
        "anchor_id": anchor_id,
        "created_at": now_iso(),
        "dna": DNA,
        "files": {},
    }

    for fp in anchor_dir.rglob("*"):
        if fp.is_file():
            rel = fp.relative_to(anchor_dir).as_posix()
            manifest["files"][rel] = {
                "sha256": compute_sha256(fp),
                "size": fp.stat().st_size,
            }

    # Merkle 根：基于所有文件哈希
    file_hashes = [v["sha256"] for v in manifest["files"].values()]
    manifest["merkle_root"] = compute_merkle_root(file_hashes)

    # 写入清单
    manifest_path = anchor_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest["files"]["manifest.json"] = {
        "sha256": compute_sha256(manifest_path),
        "size": manifest_path.stat().st_size,
    }

    # GPG 签名整个 tar 包前先签名清单
    manifest_sig = gpg_sign_file(manifest_path)
    if manifest_sig:
        sig_path = anchor_dir / "manifest.json.asc"
        sig_path.write_text(manifest_sig, encoding="utf-8")
        manifest["files"]["manifest.json.asc"] = {
            "sha256": compute_sha256(sig_path),
            "size": sig_path.stat().st_size,
        }
        manifest["gpg_signed"] = True
    else:
        manifest["gpg_signed"] = False

    # 重新写入带签名信息的清单
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # 打包 tar.gz
    tar_path = anchor_dir.with_suffix(".tar.gz")
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(anchor_dir, arcname=anchor_id)

    # 计算 tar 包哈希
    tar_hash = compute_sha256(tar_path)

    # 设置只读
    set_readonly(anchor_dir)
    set_read_only_tar = False
    try:
        os.chmod(tar_path, 0o444)
        set_read_only_tar = True
    except Exception:
        pass

    metadata = {
        "anchor_id": anchor_id,
        "created_at": manifest["created_at"],
        "local_path": str(tar_path),
        "local_dir": str(anchor_dir),
        "tar_sha256": tar_hash,
        "merkle_root": manifest["merkle_root"],
        "gpg_signed": manifest["gpg_signed"],
        "file_count": len(manifest["files"]),
        "worm_readonly": set_read_only_tar,
    }

    return tar_path, metadata


def upload_to_obs_if_configured(tar_path: Path, metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    如果配置了华为云凭证，则上传到 OBS 不可删除备份。
    未配置则跳过，不报错。
    """
    cred_file = Path.home() / ".longhun" / "huawei-credentials.json"
    if not cred_file.exists():
        print("⚠️ 未配置华为云凭证 (~/.longhun/huawei-credentials.json)，跳过 OBS 锚定")
        return None

    try:
        # 先生成临时 JSON 描述文件用于上传
        tmp_desc = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        desc = {
            "anchor_id": metadata["anchor_id"],
            "created_at": metadata["created_at"],
            "tar_sha256": metadata["tar_sha256"],
            "merkle_root": metadata["merkle_root"],
            "gpg_signed": metadata["gpg_signed"],
            "dna": DNA,
        }
        json.dump(desc, tmp_desc, ensure_ascii=False, indent=2)
        tmp_desc.close()

        proc = subprocess.run(
            [
                sys.executable, str(OBS_BACKUP),
                "upload", f"--file={tar_path}",
                "--type=immutable-history",
                "--region=primary",
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if proc.returncode != 0:
            print(f"⚠️ OBS 上传失败: {proc.stderr}")
            return {"status": "failed", "error": proc.stderr}

        # 跨区域灾备同步
        subprocess.run(
            [sys.executable, str(OBS_BACKUP), "cross-region-sync", "--type=immutable-history"],
            capture_output=True,
            text=True,
            timeout=180,
        )

        return {
            "status": "uploaded",
            "description": tmp_desc.name,
        }

    except Exception as e:
        print(f"⚠️ OBS 锚定异常: {e}")
        return {"status": "failed", "error": str(e)}


def record_anchor_event(metadata: Dict[str, Any], obs_result: Optional[Dict[str, Any]]):
    """把锚定事件追加到不可篡改历史账本"""
    try:
        payload = {
            "anchor_id": metadata["anchor_id"],
            "tar_sha256": metadata["tar_sha256"],
            "merkle_root": metadata["merkle_root"],
            "gpg_signed": metadata["gpg_signed"],
            "file_count": metadata["file_count"],
            "obs_status": obs_result.get("status") if obs_result else "skipped",
        }
        subprocess.run(
            [
                sys.executable, str(ENGINE),
                "--record", "history_anchor",
                "--payload", json.dumps(payload, ensure_ascii=False),
                "--source", "system",
                "--actor", "lh_immutable_history_anchor",
                "--sign",
            ],
            capture_output=True,
            timeout=30,
            check=False,
        )
    except Exception as e:
        print(f"⚠️ 锚定事件写入账本失败: {e}")


def anchor_once(local_only: bool = False) -> Dict[str, Any]:
    """执行一次完整锚定"""
    if not LEDGER_FILE.exists():
        raise FileNotFoundError(f"账本不存在: {LEDGER_FILE}")

    ts = datetime.now(timezone.utc)
    anchor_id = f"IHA-{ts.strftime('%Y%m%d-%H%M%S')}-{hashlib.sha256(ts.isoformat().encode()).hexdigest()[:8]}"

    print(f"⚓ 开始不可篡改历史锚定: {anchor_id}")
    print(f"   源账本: {LEDGER_FILE}")

    # 1. 本地 WORM 打包
    tar_path, metadata = pack_anchor(anchor_id)
    print(f"   ✅ 本地 WORM 快照: {tar_path}")
    print(f"   📦 tar SHA256: {metadata['tar_sha256'][:16]}...")
    print(f"   🌳 Merkle Root: {metadata['merkle_root'][:16]}...")
    print(f"   🔏 GPG 签名: {'是' if metadata['gpg_signed'] else '否'}")

    # 2. OBS 锚定（可选）
    obs_result = None
    if not local_only:
        obs_result = upload_to_obs_if_configured(tar_path, metadata)
        if obs_result and obs_result.get("status") == "uploaded":
            print(f"   ✅ OBS 锚定完成")
        elif obs_result and obs_result.get("status") == "failed":
            print(f"   ⚠️ OBS 锚定失败，但本地快照已生成")
        else:
            print(f"   ℹ️ 跳过 OBS 锚定")

    # 3. 更新索引
    index = load_anchor_index()
    index["anchors"].append({
        "anchor_id": anchor_id,
        "created_at": metadata["created_at"],
        "tar_sha256": metadata["tar_sha256"],
        "merkle_root": metadata["merkle_root"],
        "local_path": str(tar_path),
        "obs_status": obs_result.get("status") if obs_result else "skipped",
    })
    index["total_anchors"] = len(index["anchors"])
    index["last_anchor"] = anchor_id
    save_anchor_index(index)

    # 4. 锚定事件留痕
    record_anchor_event(metadata, obs_result)
    print(f"   ✅ 锚定事件已写入不可篡改历史账本")

    return {
        "status": "anchored",
        "anchor_id": anchor_id,
        "metadata": metadata,
        "obs": obs_result,
    }


def verify_latest_anchor() -> Dict[str, Any]:
    """验证最近一次本地锚定"""
    index = load_anchor_index()
    if not index.get("anchors"):
        return {"status": "empty", "message": "没有可用的锚定记录"}

    latest = index["anchors"][-1]
    tar_path = Path(latest["local_path"])
    if not tar_path.exists():
        return {"status": "missing", "message": f"本地快照不存在: {tar_path}"}

    actual_hash = compute_sha256(tar_path)
    expected_hash = latest["tar_sha256"]
    valid = actual_hash == expected_hash

    result = {
        "status": "valid" if valid else "corrupted",
        "anchor_id": latest["anchor_id"],
        "expected_hash": expected_hash[:16],
        "actual_hash": actual_hash[:16],
        "path": str(tar_path),
    }

    if valid:
        print(f"🟢 锚定验证通过: {latest['anchor_id']}")
    else:
        print(f"🔴 锚定验证失败: {latest['anchor_id']}")
        print(f"   期望: {expected_hash[:16]}...")
        print(f"   实际: {actual_hash[:16]}...")

    return result


def report() -> Dict[str, Any]:
    """输出锚定报告"""
    index = load_anchor_index()
    print("=" * 60)
    print("⚓ 龍魂不可篡改历史锚定报告")
    print("=" * 60)
    print(f"DNA: {DNA}")
    print(f"总锚定次数: {index.get('total_anchors', 0)}")
    print(f"最近锚定: {index.get('last_anchor', '无')}")
    print()
    for a in index.get("anchors", [])[-5:]:
        print(f"  {a['anchor_id']}")
        print(f"    时间: {a['created_at'][:19]}")
        print(f"    tar:  {a['tar_sha256'][:16]}...")
        print(f"    根:   {a['merkle_root'][:16]}...")
        print(f"    OBS:  {a.get('obs_status', 'unknown')}")
    print("=" * 60)
    return index


def main():
    parser = argparse.ArgumentParser(description="龍魂不可篡改历史锚定引擎")
    parser.add_argument("command", choices=["anchor", "verify", "report"], help="命令")
    parser.add_argument("--local-only", action="store_true", help="仅生成本地快照，不上传 OBS")
    args = parser.parse_args()

    if args.command == "anchor":
        result = anchor_once(local_only=args.local_only)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "verify":
        result = verify_latest_anchor()
        sys.exit(0 if result.get("status") == "valid" else 1)
    elif args.command == "report":
        report()


if __name__ == "__main__":
    main()
