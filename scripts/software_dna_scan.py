#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·本地优先软件DNA密文回云协议 v1.0
入口脚本：software_dna_scan.py

核心原则：
  1. 本地优先：原始软件包永不上传。
  2. 云端只读密文：只上传 envelope（脱敏索引）和 cipher_blob（AES-GCM 密文）。
  3. 全程可审计：每个动作写入 traces/ 时间轴，带 DNA 追溯码。

DNA: #龍芯⚡️2026-06-27-LOCAL-SOFTWARE-DNA-SCAN-v1.0
"""

import os
import sys
import json
import re
import hashlib
import hmac
import base64
import argparse
import platform
import getpass
import uuid
import secrets
from datetime import datetime, timezone
from pathlib import Path

# 优先使用 cryptography 做 AES-GCM；未安装则熔断
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ---------- 本地路径 ----------
BASE = Path(os.environ.get("LONGHUN_ROOT", "~/longhun-system")).expanduser()
SOFTWARE_DNA = BASE / "software_dna"
INPUT_DIR = SOFTWARE_DNA / "input"
QUARANTINE = SOFTWARE_DNA / "quarantine"
UNPACKED = SOFTWARE_DNA / "unpacked"
SBOM_DIR = SOFTWARE_DNA / "sbom"
REPORTS = SOFTWARE_DNA / "reports"
REDACTED = SOFTWARE_DNA / "redacted"
ENVELOPES = SOFTWARE_DNA / "envelopes"
CIPHERBLOBS = SOFTWARE_DNA / "cipherblobs"
PLANS = SOFTWARE_DNA / "plans"
TRACES = SOFTWARE_DNA / "traces"
KEY_FILE = BASE / "schemas" / "software_dna_master.key"

# ---------- 秘密模式库（本地扫描，不上传） ----------
SECRET_PATTERNS = {
    "api_key_generic": re.compile(rb"[Aa][Pp][Ii][_\-]?[Kk][Ee][Yy]\s*[:=]\s*['\"]?([a-zA-Z0-9_\-]{16,80})['\"]?"),
    "openai_key": re.compile(rb"sk-[a-zA-Z0-9]{48}"),
    "anthropic_key": re.compile(rb"sk-ant-[a-zA-Z0-9]{32,}"),
    "aws_key": re.compile(rb"AKIA[0-9A-Z]{16}"),
    "github_token": re.compile(rb"gh[pousr]_[A-Za-z0-9_]{36,}"),
    "password_assignment": re.compile(rb"[Pp][Aa][Ss][Ss][Ww][Oo][Rr][Dd]\s*[:=]\s*['\"]([^'\"]{6,})['\"]"),
    "private_key_pem": re.compile(rb"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),
    "env_secret": re.compile(rb"(SECRET|TOKEN|PASSWORD|KEY)\s*=\s*['\"]?([a-zA-Z0-9_\-]{8,})['\"]?"),
}

# ---------- 辅助函数 ----------
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digital_root_from_hex(hex_str: str) -> int:
    digits = [int(c) for c in hex_str if c.isdigit()]
    if not digits:
        return 0
    n = sum(digits)
    while n >= 10:
        n = sum(int(c) for c in str(n))
    return n


def wuxing_from_dr(dr: int) -> str:
    mapping = {1: "水", 6: "水", 2: "火", 7: "火", 3: "木", 8: "木", 4: "金", 9: "金", 5: "土", 0: "土"}
    return mapping.get(dr, "土")


def tricolor(dr: int, risk_score: int = 0, secret_risk: bool = False) -> str:
    if secret_risk:
        return "🔴"
    if risk_score >= 80:
        return "🔴"
    if dr in (3, 9) or risk_score >= 50:
        return "🟡"
    return "🟢"


def route_from_audit(audit: str) -> str:
    return {"🟢": "enter", "🟡": "hold", "🔴": "fuse"}.get(audit, "hold")


def device_fingerprint() -> str:
    """本地设备指纹：hostname + username + 系统 UUID 派生，不上传原始值。"""
    node = platform.node() or "unknown"
    user = getpass.getuser() or "unknown"
    raw = f"{node}|{user}|{uuid.getnode()}"
    return "DF-" + hashlib.sha256(raw.encode()).hexdigest()[:24].upper()


def ensure_master_key() -> bytes:
    """确保本地主密钥存在。密钥只在本地，永不离开本机。"""
    KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    if KEY_FILE.exists():
        return base64.b64decode(KEY_FILE.read_text().strip())
    key = AESGCM.generate_key(bit_length=256)
    KEY_FILE.write_text(base64.b64encode(key).decode())
    os.chmod(KEY_FILE, 0o600)
    return key


def encrypt_local_report(plaintext: bytes, key: bytes, associated_data: bytes) -> dict[str, Any]:
    """AES-256-GCM 加密本地完整报告。"""
    aesgcm = AESGCM(key)
    nonce = secrets.token_bytes(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
    return {
        "algorithm": "AES-256-GCM",
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "aad_hash": sha256_bytes(associated_data),
    }


def detect_file_type(path: Path) -> dict[str, Any]:
    """基于魔数和扩展名做文件类型识别，不执行文件。"""
    ext = path.suffix.lower()
    name_lower = path.name.lower()
    if path.stat().st_size > 0:
        with open(path, "rb") as f:
            header = f.read(64)
    else:
        header = b""

    magic_map = {
        b"\x4d\x5a": ("windows_executable", "PE/Windows 可执行文件"),
        b"\xcf\xfa\xed\xfe": ("macos_mach_o", "macOS Mach-O 可执行文件"),
        b"\xca\xfe\xba\xbe": ("java_class", "Java Class"),
        b"PK\x03\x04": ("zip_archive", "ZIP/JAR/APK 压缩包"),
        b"\x1f\x8b\x08": ("gzip", "GZIP 压缩包"),
        b"BZh": ("bzip2", "BZIP2 压缩包"),
        b"\xfd7zXZ": ("xz", "XZ 压缩包"),
        b"Rar!": ("rar", "RAR 压缩包"),
        b"7z\xbc\xaf\x27\x1c": ("7z", "7-Zip 压缩包"),
        b"\xd0\xcf\x11\xe0": ("msi_old_office", "MSI/旧 Office 二进制"),
        b"!\x12\x02\x04": ("cab", "CAB 安装包"),
    }

    detected = None
    for magic, (ftype, desc) in magic_map.items():
        if header.startswith(magic):
            detected = {"type": ftype, "description": desc}
            break

    if detected is None:
        ext_map = {
            ".dmg": {"type": "macos_dmg", "description": "macOS DMG 镜像"},
            ".pkg": {"type": "macos_pkg", "description": "macOS PKG 安装包"},
            ".app": {"type": "macos_app", "description": "macOS 应用包"},
            ".deb": {"type": "linux_deb", "description": "Debian 软件包"},
            ".rpm": {"type": "linux_rpm", "description": "RPM 软件包"},
            ".exe": {"type": "windows_exe", "description": "Windows 可执行文件"},
            ".msi": {"type": "windows_msi", "description": "Windows 安装包"},
            ".apk": {"type": "android_apk", "description": "Android APK"},
            ".ipa": {"type": "ios_ipa", "description": "iOS IPA"},
            ".py": {"type": "python_script", "description": "Python 脚本"},
            ".sh": {"type": "shell_script", "description": "Shell 脚本"},
            ".js": {"type": "javascript", "description": "JavaScript 文件"},
            ".zip": {"type": "zip_archive", "description": "ZIP 压缩包"},
            ".tar": {"type": "tar_archive", "description": "TAR 归档"},
            ".gz": {"type": "gzip", "description": "GZIP 压缩包"},
        }
        detected = ext_map.get(ext, {"type": "unknown", "description": "未知文件类型"})
    return detected


def scan_secrets(path: Path, max_bytes: int = 5 * 1024 * 1024) -> dict[str, Any]:
    """本地扫描文件中是否包含敏感凭据，不上传命中内容。"""
    size = path.stat().st_size
    if size <= max_bytes:
        with open(path, "rb") as f:
            sample = f.read()
    else:
        with open(path, "rb") as f:
            sample = f.read(max_bytes)
    findings = {}
    total_hits = 0
    for name, pattern in SECRET_PATTERNS.items():
        matches = pattern.findall(sample)
        count = len(matches)
        if count:
            findings[name] = count
            total_hits += count
    return {
        "has_secrets": total_hits > 0,
        "secret_hits": total_hits,
        "pattern_counts": findings,
    }


def build_risk_score(file_type: dict[str, Any], secret_scan: dict[str, Any], size: int) -> int:
    score = 0
    # 可执行/安装包风险权重
    if file_type["type"] in ("windows_executable", "macos_mach_o", "macos_dmg", "macos_pkg",
                             "windows_exe", "windows_msi", "android_apk", "ios_ipa",
                             "linux_deb", "linux_rpm"):
        score += 35
    elif file_type["type"] in ("zip_archive", "gzip", "bzip2", "xz", "rar", "7z",
                               "tar_archive", "macos_app"):
        score += 20
    # 秘密泄露风险
    if secret_scan["has_secrets"]:
        score += min(50, secret_scan["secret_hits"] * 10)
    # 异常大文件
    if size > 500 * 1024 * 1024:
        score += 10
    return min(100, score)


def build_sbom(path: Path, file_hash: str, file_type: dict[str, Any]) -> dict[str, Any]:
    stat = path.stat()
    return {
        "filename": path.name,
        "size_bytes": stat.st_size,
        "sha256": file_hash,
        "file_type": file_type,
        "created": datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc).isoformat(),
        "modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        "scanner": "software_dna_scan.py",
        "scanner_version": "v1.0",
    }


def write_trace(dna: str, event: str, detail: dict[str, Any]):
    TRACES.mkdir(parents=True, exist_ok=True)
    trace = {
        "dna": dna,
        "event": event,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "detail": detail,
    }
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    trace_file = TRACES / f"{dna[:12]}_{ts}_{event}.json"
    trace_file.write_text(json.dumps(trace, indent=2, ensure_ascii=False))


# ---------- 主扫描逻辑 ----------
def scan_software(file_path: str, dry_run: bool = True):
    file_path = Path(file_path).expanduser().resolve()
    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return None

    # 1. 基础元数据
    size = file_path.stat().st_size
    timestamp = datetime.now(timezone.utc).isoformat()
    dev_fp = device_fingerprint()

    print(f"🔍 扫描: {file_path.name} ({size} bytes)")
    print(f"   设备指纹: {dev_fp}")
    print(f"   模式: {'dry-run（不执行）' if dry_run else 'live'}")

    # 2. 文件哈希与数字根
    file_hash = sha256_file(file_path)
    dr = digital_root_from_hex(file_hash)
    wuxing = wuxing_from_dr(dr)

    # 3. 文件类型识别
    file_type = detect_file_type(file_path)
    print(f"   文件类型: {file_type['description']} ({file_type['type']})")

    # 4. SBOM
    sbom = build_sbom(file_path, file_hash, file_type)
    SBOM_DIR.mkdir(parents=True, exist_ok=True)

    # 5. 秘密扫描
    secret_scan = scan_secrets(file_path)
    if secret_scan["has_secrets"]:
        print(f"   ⚠️  发现潜在敏感模式: {secret_scan['pattern_counts']}")

    # 6. 风险评分
    risk_score = build_risk_score(file_type, secret_scan, size)

    # 7. 软件 DNA = 多层哈希，绑定文件、类型、SBOM、设备、时间
    software_dna = hashlib.sha256(
        "|".join([
            file_hash,
            file_path.suffix,
            file_type["type"],
            json.dumps(sbom, sort_keys=True),
            str(risk_score),
            str(secret_scan["secret_hits"]),
            timestamp,
            dev_fp,
        ]).encode()
    ).hexdigest()

    # 8. 三色审计
    audit = tricolor(dr, risk_score=risk_score, secret_risk=secret_scan["has_secrets"])
    route = route_from_audit(audit)

    # 9. 本地完整报告（将被加密）
    full_report = {
        "software_dna": software_dna,
        "sbom": sbom,
        "secret_scan": secret_scan,
        "risk_score": risk_score,
        "audit_color": audit,
        "wuxing": wuxing,
        "digital_root": dr,
        "device_fingerprint": dev_fp,
        "timestamp": timestamp,
        "file_path": str(file_path),
        "route": route,
        "version": "v1.0",
    }
    report_json = json.dumps(full_report, indent=2, ensure_ascii=False).encode()

    # 10. 加密本地报告
    key = ensure_master_key()
    cipher_blob = encrypt_local_report(
        report_json,
        key,
        associated_data=software_dna.encode(),
    )
    cipher_blob.update({
        "id": f"CIPHER-9622-{datetime.now().strftime('%Y%m%d')}-{software_dna[:8]}",
        "local_only": True,
        "plaintext_never_uploaded": True,
    })

    # 11. 脱敏信封（可上传的索引）
    envelope = {
        "software_dna": software_dna,
        "file_hash": file_hash,
        "cipher_blob_id": cipher_blob["id"],
        "route": route,
        "audit_color": audit,
        "wuxing": wuxing,
        "digital_root": dr,
        "risk_score": risk_score,
        "has_secrets": secret_scan["has_secrets"],
        "file_type": file_type["type"],
        "file_size": size,
        "timestamp": timestamp,
        "device_fingerprint_prefix": dev_fp[:8] + "...",
        "version": "v1.0",
    }

    # 12. 保存
    ENVELOPES.mkdir(parents=True, exist_ok=True)
    CIPHERBLOBS.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    SBOM_DIR.mkdir(parents=True, exist_ok=True)

    prefix = software_dna[:12]
    (ENVELOPES / f"{prefix}_envelope.json").write_text(
        json.dumps(envelope, indent=2, ensure_ascii=False)
    )
    (CIPHERBLOBS / f"{prefix}_cipher.json").write_text(
        json.dumps(cipher_blob, indent=2, ensure_ascii=False)
    )
    (REPORTS / f"{prefix}_report.json").write_text(
        json.dumps(full_report, indent=2, ensure_ascii=False)
    )
    (SBOM_DIR / f"{prefix}_sbom.json").write_text(
        json.dumps(sbom, indent=2, ensure_ascii=False)
    )

    # 13. 路由动作：🔴 熔断 → 隔离
    if route == "fuse":
        QUARANTINE.mkdir(parents=True, exist_ok=True)
        quarantine_path = QUARANTINE / f"{prefix}_{file_path.name}"
        if not dry_run:
            # 硬链接/复制到隔离区；这里只做标记说明
            with open(quarantine_path, "wb") as out, open(file_path, "rb") as src:
                for chunk in iter(lambda: src.read(65536), b""):
                    out.write(chunk)
            print(f"   🚨 已隔离到: {quarantine_path}")
        else:
            print(f"   🚨 dry-run：本会隔离到 {quarantine_path}")

    # 14. 审计痕迹
    write_trace(software_dna, "scan_complete", {
        "route": route,
        "audit": audit,
        "risk_score": risk_score,
        "file_type": file_type["type"],
        "dry_run": dry_run,
    })

    # 15. 输出
    print(f"\n✅ 软件DNA: {software_dna}")
    print(f"   文件哈希: {file_hash}")
    print(f"   数字根: {dr} → 五行: {wuxing} → 三色: {audit}")
    print(f"   风险评分: {risk_score}/100")
    print(f"   路由决策: {route}")
    print(f"   密文包ID: {cipher_blob['id']}")
    print(f"   输出文件:")
    print(f"     - envelopes/{prefix}_envelope.json  （可上传的脱敏索引）")
    print(f"     - cipherblobs/{prefix}_cipher.json  （本地 AES-GCM 密文）")
    print(f"     - reports/{prefix}_report.json      （本地完整报告）")
    print(f"     - sbom/{prefix}_sbom.json           （本地 SBOM）")
    print(f"     - traces/{prefix}_*_scan_complete.json （审计痕迹）")

    return {
        "software_dna": software_dna,
        "envelope": envelope,
        "cipher_blob": cipher_blob,
        "report": full_report,
    }


# ---------- 命令行入口 ----------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="龍魂本地软件DNA扫描")
    parser.add_argument("file", help="要扫描的软件包路径")
    parser.add_argument(
        "--dry-run",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="默认 dry-run：只分析不隔离/不执行软件",
    )
    args = parser.parse_args()
    scan_software(args.file, dry_run=args.dry_run)
