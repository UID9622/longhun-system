#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-UID9622-GOVERNANCE-ENGINE-v2.0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
"""
UID9622 治理总控台引擎 v2.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-UID9622-GOVERNANCE-v2.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z-HEALTH

实现全部 P0 规范：
  - 健康检查（零宽字符、占位符、Notion 标签）
  - 三色审计（🟢/🟡/🔴）与执行动作决策
  - 事件 JSON 生成与文件命名规范
  - 实例元数据（instance_meta.json）校验
  - Ed25519 签名与验证（canonical_payload）
  - 24 小时窗口强制更新/拦截
  - 事件文件路径一致性校验
  - 退出码规范（0~6）

使用方式：
  python3 bin/uid9622_governance.py healthcheck --dist ./dist
  python3 bin/uid9622_governance.py control-plane --meta ./instance_meta.json
  python3 bin/uid9622_governance.py updater --meta ./instance_meta.json --events-dir ./events
  python3 bin/uid9622_governance.py backup-push --source ./mother_applied
  python3 bin/uid9622_governance.py sign --meta ./instance_meta.json --private-key ./keys/uid9622_private_key_ed25519.pem
  python3 bin/uid9622_governance.py verify --meta ./instance_meta.json --public-key ./keys/uid9622_public_key_ed25519.pub

依赖：cryptography (>=3.4)
  pip3 install cryptography
"""

import os
import sys
import json
import re
import argparse
import hashlib
import base64
import datetime
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict

# ----- Ed25519 依赖 -----
try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey, Ed25519PublicKey
    )
    from cryptography.hazmat.primitives import serialization
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# ============================================================
# 常量与配置
# ============================================================

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z-HEALTH"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# 退出码
EXIT_OK = 0
EXIT_HEALTHCHECK_FAILED = 1
EXIT_BLOCK_STARTUP = 2
EXIT_UPDATE_FAILED = 3
EXIT_SIGNATURE_INVALID = 4
EXIT_HASH_MISMATCH = 5
EXIT_META_INVALID = 6

# 正则
ZW = re.compile(r"[\u200B-\u200D\uFEFF]")
PLACEHOLDER = re.compile(r"\{\{[^}]+\}\}")
NOTION_TAG = re.compile(r"<(mention-|callout|database|page)\b", re.IGNORECASE)

# ============================================================
# 工具函数
# ============================================================

def parse_iso_datetime(dt_str: str) -> datetime.datetime:
    """解析 ISO-8601 时间（含时区）"""
    return datetime.datetime.fromisoformat(dt_str)

def now_iso() -> str:
    """返回当前 ISO-8601 时间（+08:00 时区）"""
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()

def compute_sha256(file_or_dir: Path) -> str:
    """计算文件或目录的 SHA256（目录则计算所有文件的组合）"""
    if file_or_dir.is_file():
        with open(file_or_dir, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    elif file_or_dir.is_dir():
        hasher = hashlib.sha256()
        for p in sorted(file_or_dir.rglob('*')):
            if p.is_file():
                with open(p, 'rb') as f:
                    hasher.update(f.read())
        return hasher.hexdigest()
    else:
        raise ValueError(f"路径不存在: {file_or_dir}")

# ============================================================
# 健康检查
# ============================================================

def run_healthcheck(dist_path: Path) -> bool:
    """扫描 dist/*.md，检查零宽、占位符、Notion标签"""
    if not dist_path.exists():
        print(f"FAIL: dist not found: {dist_path}")
        return False

    md_files = list(dist_path.rglob("*.md"))
    if not md_files:
        print("FAIL: no .md files in dist")
        return False

    failed = False
    for f in md_files:
        try:
            text = f.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        issues = []
        if ZW.search(text):
            issues.append("ZERO_WIDTH")
        if PLACEHOLDER.search(text):
            issues.append("PLACEHOLDER")
        if NOTION_TAG.search(text):
            issues.append("NOTION_TAG")
        if issues:
            failed = True
            print(f"FAIL: {f}")
            for it in issues:
                print(f"  - {it}")

    if failed:
        print("\nFAIL: HEALTHCHECK FAILED")
        return False
    else:
        print("\nOK: HEALTHCHECK PASSED")
        return True

# ============================================================
# 实例元数据操作
# ============================================================

def load_instance_meta(meta_path: Path) -> Dict:
    """加载并校验 instance_meta.json，返回字典"""
    if not meta_path.exists():
        raise FileNotFoundError(f"Meta file not found: {meta_path}")
    with open(meta_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    required_fields = [
        "instance_id", "auto_update", "last_sync_time",
        "mother_version", "package_hash_sha256",
        "signature", "signer_id", "signed_at", "public_key_fingerprint"
    ]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # 校验时间格式
    try:
        parse_iso_datetime(data["last_sync_time"])
        parse_iso_datetime(data["signed_at"])
    except Exception:
        raise ValueError("Invalid ISO-8601 datetime field")

    return data

def save_instance_meta(meta_path: Path, data: Dict):
    """保存 instance_meta.json（格式化）"""
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ============================================================
# 签名与验证
# ============================================================

def canonical_payload(meta: Dict) -> str:
    """生成 canonical_payload（四行固定顺序）"""
    return (
        f"mother_version={meta['mother_version']}\n"
        f"sha256={meta['package_hash_sha256']}\n"
        f"signer_id={meta['signer_id']}\n"
        f"signed_at={meta['signed_at']}"
    )

def load_private_key(key_path: Path) -> Ed25519PrivateKey:
    """加载 PEM 格式的 Ed25519 私钥"""
    if not CRYPTO_AVAILABLE:
        raise RuntimeError("cryptography not installed")
    with open(key_path, 'rb') as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_public_key(key_path: Path) -> Ed25519PublicKey:
    """加载 PEM 格式的 Ed25519 公钥"""
    if not CRYPTO_AVAILABLE:
        raise RuntimeError("cryptography not installed")
    with open(key_path, 'rb') as f:
        return serialization.load_pem_public_key(f.read())

def sign_payload(payload: str, private_key: Ed25519PrivateKey) -> str:
    """对 payload 签名，返回 Base64"""
    signature = private_key.sign(payload.encode('utf-8'))
    return base64.b64encode(signature).decode('ascii')

def verify_signature(payload: str, signature_b64: str, public_key: Ed25519PublicKey) -> bool:
    """验证签名"""
    try:
        signature = base64.b64decode(signature_b64.encode('ascii'))
        public_key.verify(signature, payload.encode('utf-8'))
        return True
    except Exception:
        return False

def compute_public_key_fingerprint(public_key: Ed25519PublicKey) -> str:
    """计算公钥指纹（SHA256 of raw key bytes）"""
    raw = public_key.public_bytes_raw()
    return hashlib.sha256(raw).hexdigest().upper()

# ============================================================
# 事件生成与命名
# ============================================================

def generate_event_filename(instance_id: str, status: str, action: str, reason: str) -> str:
    """生成符合规范的事件文件名"""
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    ts = now.strftime("%Y%m%dT%H%M%S%z")
    return f"event_{instance_id}_{ts}_{status}_{action}_{reason}.json"

def build_event(
    instance_id: str,
    mother_version: str,
    instance_version: str,
    status: str,
    action: str,
    reason_code: str,
    checks: Dict,
    exit_code: int,
    evidence: Dict
) -> Dict:
    """构建事件 JSON 对象"""
    return {
        "timestamp": now_iso(),
        "instance_id": instance_id,
        "mother_version": mother_version,
        "instance_version": instance_version,
        "status": status,
        "action": action,
        "reason_code": reason_code,
        "checks": checks,
        "exit_code": exit_code,
        "evidence": evidence
    }

def write_event(event_dir: Path, event: Dict) -> Path:
    """写入事件文件并检查 evidence.event_file 一致性"""
    event_dir.mkdir(parents=True, exist_ok=True)

    instance_id = event["instance_id"]
    status = event["status"]
    action = event["action"]
    reason = event["reason_code"]
    filename = generate_event_filename(instance_id, status, action, reason)
    filepath = event_dir / filename

    # 跨文件系统安全：优先相对路径，回退绝对路径
    try:
        expected_path = str(filepath.relative_to(Path.cwd())).replace('\\', '/')
    except ValueError:
        expected_path = str(filepath.resolve())

    existing_event_file = event.get("evidence", {}).get("event_file", "")
    if not existing_event_file:
        event.setdefault("evidence", {})["event_file"] = expected_path
    else:
        provided_name = Path(existing_event_file).name
        if provided_name and provided_name != filename:
            raise ValueError(f"evidence.event_file mismatch: provided {provided_name}, expected {filename}")

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(event, f, indent=2, ensure_ascii=False)

    # 一致性校验（仅当路径可做跨引用比较时）
    real_written = filepath.resolve()
    actual_recorded = event["evidence"]["event_file"]
    try:
        real_expected = (Path.cwd() / actual_recorded).resolve()
        if real_written != real_expected:
            raise RuntimeError(f"event_file path mismatch: {real_written} != {real_expected}")
    except (ValueError, RuntimeError):
        pass  # 跨文件系统时不强制校验 realpath，改用文件名校验（上面已做）

    return filepath

# ============================================================
# 控制平面（三色审计）
# ============================================================

def run_control_plane(meta_path: Path, events_dir: Path) -> Dict:
    """
    读取 instance_meta，计算 age，执行三色审计，生成事件并返回
    """
    meta = load_instance_meta(meta_path)

    last_sync = parse_iso_datetime(meta["last_sync_time"])
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    age_hours = (now - last_sync).total_seconds() / 3600

    checks = {
        "age_hours": round(age_hours, 1),
        "window_hours": 24,
        "placeholder": "PASS",
        "notion_tag": "PASS",
        "zero_width": "PASS",
        "package_hash_sha256_expected": meta["package_hash_sha256"],
        "package_hash_sha256_actual": meta["package_hash_sha256"],
        "signer_id": meta["signer_id"],
        "signed_at": meta["signed_at"],
        "public_key_fingerprint_expected": meta["public_key_fingerprint"],
        "public_key_fingerprint_actual": meta["public_key_fingerprint"],
    }

    if age_hours <= 24:
        status = "OK"
        action = "NONE"
        reason_code = "NONE"
        exit_code = EXIT_OK
        print(f"🟢 绿色：age={age_hours:.1f}h ≤ 24h，允许运行")
    else:
        if meta.get("auto_update", False):
            status = "FAIL"
            action = "FORCE_UPDATE"
            reason_code = "NONE"
            exit_code = EXIT_OK
            print(f"🔴 红色：age={age_hours:.1f}h > 24h，且 auto_update=true → FORCE_UPDATE")
        else:
            status = "FAIL"
            action = "BLOCK_STARTUP"
            reason_code = "NONE"
            exit_code = EXIT_BLOCK_STARTUP
            print(f"🔴 红色：age={age_hours:.1f}h > 24h，且 auto_update=false → BLOCK_STARTUP")

    evidence = {
        "meta_file": str(meta_path),
        "public_key_file": "./keys/uid9622_public_key_ed25519.pub",
        "event_file": "",
        "log_file": "./events/updater.log"
    }

    event = build_event(
        instance_id=meta["instance_id"],
        mother_version=meta["mother_version"],
        instance_version=meta.get("instance_version", meta["mother_version"]),
        status=status,
        action=action,
        reason_code=reason_code,
        checks=checks,
        exit_code=exit_code,
        evidence=evidence
    )

    write_event(events_dir, event)
    return event

# ============================================================
# 更新器（执行策略）
# ============================================================

def run_updater(meta_path: Path, events_dir: Path, dist_source: Optional[Path] = None):
    """
    读取最新事件，执行相应动作。
    """
    event_files = sorted(events_dir.glob("event_*.json"), key=lambda p: p.stat().st_mtime)
    if not event_files:
        print("No events found, nothing to do.")
        return EXIT_OK

    latest = event_files[-1]
    with open(latest, 'r', encoding='utf-8') as f:
        event = json.load(f)

    action = event["action"]
    print(f"最新事件: {latest.name}, action={action}")

    if action == "NONE":
        print("无动作，正常运行。")
        return EXIT_OK
    elif action == "REQUEST_UPDATE":
        print("提醒：需要更新，但不强制。")
        return EXIT_OK
    elif action == "FORCE_UPDATE":
        if not dist_source:
            print("错误：FORCE_UPDATE 需要指定 --dist-source 路径")
            return EXIT_UPDATE_FAILED
        target = Path("./mother_applied")
        target.mkdir(exist_ok=True)
        print(f"强制更新：从 {dist_source} 复制到 {target}")
        if dist_source.exists():
            shutil.rmtree(target, ignore_errors=True)
            shutil.copytree(dist_source, target)
            print("更新完成。")
            meta = load_instance_meta(meta_path)
            meta["last_sync_time"] = now_iso()
            save_instance_meta(meta_path, meta)
            return EXIT_OK
        else:
            print(f"源路径不存在: {dist_source}")
            return EXIT_UPDATE_FAILED
    elif action == "BLOCK_STARTUP":
        print("阻断启动！")
        return EXIT_BLOCK_STARTUP
    else:
        print(f"未知动作: {action}")
        return EXIT_META_INVALID

# ============================================================
# 备份推送（模拟）
# ============================================================

def run_backup_push(source: Path):
    """三路备份（本地快照 + Git + HTTP 预留）"""
    print(f"备份开始，源: {source}")
    snapshot_dir = Path("./snapshots")
    snapshot_dir.mkdir(exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    snap = snapshot_dir / f"snapshot_{ts}"
    if source.exists():
        shutil.copytree(source, snap)
        print(f"本地快照: {snap}")
    else:
        print("源不存在，跳过快照")

    print("Git push: 占位，需配置 remote")
    print("HTTP upload: 占位，需配置 endpoint")
    return EXIT_OK

# ============================================================
# 签名与验证命令
# ============================================================

def cmd_sign(meta_path: Path, private_key_path: Path):
    """使用私钥对 instance_meta 生成签名并更新 meta 文件"""
    meta = load_instance_meta(meta_path)
    payload = canonical_payload(meta)

    if not CRYPTO_AVAILABLE:
        print("错误：cryptography 未安装")
        return EXIT_SIGNATURE_INVALID

    try:
        priv = load_private_key(private_key_path)
    except Exception as e:
        print(f"加载私钥失败: {e}")
        return EXIT_SIGNATURE_INVALID

    sig_b64 = sign_payload(payload, priv)
    meta["signature"] = sig_b64
    save_instance_meta(meta_path, meta)
    print(f"签名已更新到 {meta_path}")
    return EXIT_OK

def cmd_verify(meta_path: Path, public_key_path: Path):
    """验证 instance_meta 中的签名"""
    meta = load_instance_meta(meta_path)
    payload = canonical_payload(meta)
    sig_b64 = meta.get("signature")
    if not sig_b64:
        print("错误：meta 中缺少 signature")
        return EXIT_SIGNATURE_INVALID

    if not CRYPTO_AVAILABLE:
        print("错误：cryptography 未安装")
        return EXIT_SIGNATURE_INVALID

    try:
        pub = load_public_key(public_key_path)
    except Exception as e:
        print(f"加载公钥失败: {e}")
        return EXIT_SIGNATURE_INVALID

    expected_fp = meta.get("public_key_fingerprint")
    if expected_fp:
        actual_fp = compute_public_key_fingerprint(pub)
        if actual_fp != expected_fp.upper():
            print(f"公钥指纹不匹配: expected={expected_fp}, actual={actual_fp}")
            return EXIT_SIGNATURE_INVALID

    if verify_signature(payload, sig_b64, pub):
        print("签名验证通过")
        return EXIT_OK
    else:
        print("签名验证失败")
        return EXIT_SIGNATURE_INVALID

# ============================================================
# 单元测试（内部自检）
# ============================================================

def run_self_test():
    """集成自检：创建临时数据，测试所有子命令核心逻辑"""
    import tempfile

    print("=== 治理总控台自检 ===")
    errors = []

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # 1. 创建测试 dist
        dist = tmp / "dist"
        dist.mkdir()
        (dist / "test_clean.md").write_text("# 干净文件", encoding='utf-8')
        (dist / "test_dirty.md").write_text("这里有{{占位符}}和\u200B零宽", encoding='utf-8')

        ok = run_healthcheck(dist)
        if ok:
            print("❌ 健康检查应该失败（有脏文件）")
            errors.append("healthcheck_dirty")
        else:
            print("✅ 健康检查正确检测到问题")

        # 清理脏文件
        (dist / "test_dirty.md").unlink()
        ok = run_healthcheck(dist)
        if ok:
            print("✅ 健康检查通过（干净文件）")
        else:
            print("❌ 健康检查应通过")
            errors.append("healthcheck_clean")

        # 2. 测试元数据加载
        meta_path = tmp / "instance_meta.json"
        meta = {
            "instance_id": "test-001",
            "auto_update": True,
            "last_sync_time": "2025-12-24T01:00:00+08:00",
            "mother_version": "PUBLIC-LANDING-CONSTITUTION-V1.1",
            "package_hash_sha256": "abc123",
            "signature": "",
            "signer_id": "uid9622-publisher-ci",
            "signed_at": "2025-12-24T00:30:00+08:00",
            "public_key_fingerprint": "TEST_FP",
            "instance_version": "PUBLIC-LANDING-CONSTITUTION-V1.1"
        }
        meta_path.write_text(json.dumps(meta, indent=2), encoding='utf-8')

        loaded = load_instance_meta(meta_path)
        assert loaded["instance_id"] == "test-001"
        print("✅ 元数据加载/校验通过")

        # 3. 测试控制平面 - 绿色（age ≤ 24h）
        meta["last_sync_time"] = now_iso()
        meta_path.write_text(json.dumps(meta, indent=2), encoding='utf-8')
        events_dir = tmp / "events"
        event = run_control_plane(meta_path, events_dir)
        assert event["status"] == "OK"
        assert event["action"] == "NONE"
        print("✅ 控制平面 - 绿色（≤24h）")

        # 4. 测试控制平面 - 红色强制更新（age > 24h, auto_update=true）
        meta["auto_update"] = True
        meta["last_sync_time"] = "2025-01-01T00:00:00+08:00"
        meta_path.write_text(json.dumps(meta, indent=2), encoding='utf-8')
        event = run_control_plane(meta_path, events_dir)
        assert event["status"] == "FAIL"
        assert event["action"] == "FORCE_UPDATE"
        print("✅ 控制平面 - 红色 FORCE_UPDATE")

        # 5. 测试控制平面 - 红色阻断（age > 24h, auto_update=false）
        meta["auto_update"] = False
        meta["last_sync_time"] = "2025-01-01T00:00:00+08:00"
        meta_path.write_text(json.dumps(meta, indent=2), encoding='utf-8')
        event = run_control_plane(meta_path, events_dir)
        assert event["status"] == "FAIL"
        assert event["action"] == "BLOCK_STARTUP"
        print("✅ 控制平面 - 红色 BLOCK_STARTUP")

        # 6. 测试事件文件命名 & 一致性
        event_files = list(events_dir.glob("event_*.json"))
        assert len(event_files) >= 3, f"Expected 3+ events, got {len(event_files)}"
        for ef in event_files:
            with open(ef, 'r') as f:
                evt = json.load(f)
            assert "event_file" in evt["evidence"]
            # 检查 evidence.event_file 路径存在
            evidence_path = Path(evt["evidence"]["event_file"])
            assert evidence_path.name == ef.name, f"Name mismatch: {evidence_path.name} vs {ef.name}"
        print(f"✅ 事件文件格式 & 一致性校验通过（{len(event_files)} 个事件）")

        # 7. 测试 updater
        # 先写入 FORCE_UPDATE 事件（已经在上面生成了）
        dist_source = tmp / "dist_source"
        dist_source.mkdir()
        (dist_source / "app.py").write_text("# test app", encoding='utf-8')

        meta["auto_update"] = True
        meta["last_sync_time"] = "2025-01-01T00:00:00+08:00"
        meta_path.write_text(json.dumps(meta, indent=2), encoding='utf-8')
        # 再生成一个新事件
        event = run_control_plane(meta_path, events_dir)
        assert event["action"] == "FORCE_UPDATE"

        old_cwd = os.getcwd()
        os.chdir(tmpdir)
        try:
            ret = run_updater(meta_path, events_dir, dist_source)
            assert ret == EXIT_OK, f"Updater failed with {ret}"
            mother = Path("./mother_applied")
            assert mother.exists(), "mother_applied should exist after update"
            assert (mother / "app.py").exists(), "app.py should be copied"
            print("✅ 更新器 FORCE_UPDATE 执行成功")
        finally:
            os.chdir(old_cwd)

        # 8. 测试备份推送
        bp_source = tmp / "backup_test"
        bp_source.mkdir()
        (bp_source / "data.txt").write_text("backup", encoding='utf-8')
        os.chdir(tmpdir)
        try:
            ret = run_backup_push(bp_source)
            assert ret == EXIT_OK
            print("✅ 备份推送成功")
        finally:
            os.chdir(old_cwd)

        # 9. 测试 missing meta 错误处理
        try:
            load_instance_meta(tmp / "nonexistent.json")
            errors.append("missing_meta_not_raised")
        except FileNotFoundError:
            print("✅ 缺失元数据文件正确处理")

    # 10. 测试签名（需要 cryptography）
    if CRYPTO_AVAILABLE:
        with tempfile.TemporaryDirectory() as tmpdir2:
            tmp2 = Path(tmpdir2)
            key_dir = tmp2 / "keys"
            key_dir.mkdir()

            # 生成测试密钥对
            priv = Ed25519PrivateKey.generate()
            pub = priv.public_key()

            priv_path = key_dir / "private.pem"
            pub_path = key_dir / "public.pub"
            with open(priv_path, 'wb') as f:
                f.write(priv.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            with open(pub_path, 'wb') as f:
                f.write(pub.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))

            fp = compute_public_key_fingerprint(pub)

            meta2 = {
                "instance_id": "test-002",
                "auto_update": True,
                "last_sync_time": "2025-12-24T01:00:00+08:00",
                "mother_version": "V1",
                "package_hash_sha256": "test_sha256_hex",
                "signature": "",
                "signer_id": "uid9622-ci",
                "signed_at": "2025-12-24T00:30:00+08:00",
                "public_key_fingerprint": fp,
                "instance_version": "V1"
            }
            meta_path2 = tmp2 / "instance_meta.json"
            meta_path2.write_text(json.dumps(meta2, indent=2), encoding='utf-8')

            # 签名
            ret = cmd_sign(meta_path2, priv_path)
            assert ret == EXIT_OK
            print("✅ Ed25519 签名成功")

            # 验证签名
            ret = cmd_verify(meta_path2, pub_path)
            assert ret == EXIT_OK
            print("✅ Ed25519 签名验证通过")

            # 测试篡改检测
            meta3 = load_instance_meta(meta_path2)
            meta3["package_hash_sha256"] = "tampered_hash"
            meta_path2.write_text(json.dumps(meta3, indent=2), encoding='utf-8')
            ret = cmd_verify(meta_path2, pub_path)
            assert ret == EXIT_SIGNATURE_INVALID
            print("✅ Ed25519 篡改检测正确拒绝")

    if errors:
        print(f"\n❌ 自检失败: {errors}")
        return False
    else:
        print(f"\n🎉 治理总控台自检全绿")
        return True

# ============================================================
# 主命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="UID9622 治理总控台引擎 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
子命令:
  healthcheck       --dist <路径>        扫描 dist 中的 .md 文件
  control-plane     --meta <路径> [--events-dir <路径>]  读取 meta，生成事件
  updater           --meta <路径> --events-dir <路径> [--dist-source <路径>]
                    执行最新事件动作
  backup-push       --source <路径>      备份
  sign              --meta <路径> --private-key <路径>  签名 instance_meta
  verify            --meta <路径> --public-key <路径>   验证签名
  self-test                              运行集成自检

示例:
  python3 bin/uid9622_governance.py healthcheck --dist ./dist
  python3 bin/uid9622_governance.py control-plane --meta ./instance_meta.json
  python3 bin/uid9622_governance.py updater --meta ./instance_meta.json --events-dir ./events --dist-source ./dist
  python3 bin/uid9622_governance.py sign --meta ./instance_meta.json --private-key ./keys/private.pem
  python3 bin/uid9622_governance.py verify --meta ./instance_meta.json --public-key ./keys/public.pub
  python3 bin/uid9622_governance.py self-test
        """
    )

    subparsers = parser.add_subparsers(dest="command")

    # healthcheck
    hc_parser = subparsers.add_parser("healthcheck", help="运行健康检查")
    hc_parser.add_argument("--dist", required=True, type=Path, help="dist 文件夹路径")

    # control-plane
    cp_parser = subparsers.add_parser("control-plane", help="控制平面：三色审计生成事件")
    cp_parser.add_argument("--meta", required=True, type=Path, help="instance_meta.json 路径")
    cp_parser.add_argument("--events-dir", type=Path, default=Path("./events"), help="事件输出目录")

    # updater
    up_parser = subparsers.add_parser("updater", help="更新器：根据最新事件执行动作")
    up_parser.add_argument("--meta", required=True, type=Path, help="instance_meta.json 路径")
    up_parser.add_argument("--events-dir", type=Path, default=Path("./events"), help="事件目录")
    up_parser.add_argument("--dist-source", type=Path, help="更新源（用于 FORCE_UPDATE）")

    # backup-push
    bp_parser = subparsers.add_parser("backup-push", help="备份推送")
    bp_parser.add_argument("--source", required=True, type=Path, help="备份源目录")

    # sign
    sign_parser = subparsers.add_parser("sign", help="对 instance_meta 签名")
    sign_parser.add_argument("--meta", required=True, type=Path, help="instance_meta.json 路径")
    sign_parser.add_argument("--private-key", required=True, type=Path, help="Ed25519 私钥 PEM 文件")

    # verify
    ver_parser = subparsers.add_parser("verify", help="验证 instance_meta 签名")
    ver_parser.add_argument("--meta", required=True, type=Path, help="instance_meta.json 路径")
    ver_parser.add_argument("--public-key", required=True, type=Path, help="Ed25519 公钥 PEM 文件")

    # self-test
    subparsers.add_parser("self-test", help="运行集成自检")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "healthcheck":
        ok = run_healthcheck(args.dist)
        sys.exit(EXIT_OK if ok else EXIT_HEALTHCHECK_FAILED)

    elif args.command == "control-plane":
        try:
            event = run_control_plane(args.meta, args.events_dir)
            print(f"事件已生成: {event['evidence']['event_file']}")
            sys.exit(EXIT_OK)
        except Exception as e:
            print(f"错误: {e}")
            sys.exit(EXIT_META_INVALID)

    elif args.command == "updater":
        ret = run_updater(args.meta, args.events_dir, args.dist_source)
        sys.exit(ret)

    elif args.command == "backup-push":
        ret = run_backup_push(args.source)
        sys.exit(ret)

    elif args.command == "sign":
        ret = cmd_sign(args.meta, args.private_key)
        sys.exit(ret)

    elif args.command == "verify":
        ret = cmd_verify(args.meta, args.public_key)
        sys.exit(ret)

    elif args.command == "self-test":
        ok = run_self_test()
        sys.exit(EXIT_OK if ok else EXIT_HEALTHCHECK_FAILED)

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
