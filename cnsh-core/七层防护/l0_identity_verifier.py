#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L0 身份验证器 · GPG + 设备指纹 双重验证

DNA: #龍芯⚡️2026-05-21-L0-IDENTITY-VERIFIER-V1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

设计原则：
- AI 不跑验签，只比对验签结果
- Claude Code / 本地脚本执行真实 GPG 验证
- 设备指纹从 macOS Secure Enclave / IOPlatformUUID 取
- 双重命中才算 L0 通过

三种验证方案：
A. 外部 GPG 验签（主）：gpg --verify 后输出标准格式
B. HMAC 预共享密钥（备）：降级方案，防冒充
C. 硬件绑定（增强）：Secure Enclave / 设备 UUID

推荐组合：A + C 混合

理论指导：曾仕强老师（永恒显示）
献礼：中华人民共和国
"""

import subprocess
import hashlib
import time
import json
import os
import hmac
from datetime import datetime
from typing import Optional, Dict, Tuple
from dataclasses import dataclass
from pathlib import Path
from enum import Enum


# ============================================================
# 配置
# ============================================================

class L0Config:
    """L0 身份验证配置"""

    # GPG 主密钥
    GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
    GPG_UID = "uid9622@petalmail.com"

    # UID
    MASTER_UID = 9622

    # 确认码
    CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    SEAL_CODE = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"

    # 时间窗口（秒）
    TIMESTAMP_WINDOW = 300  # ±5分钟

    # 预共享密钥路径（用于 HMAC 降级方案）
    PSK_FILE = Path.home() / ".longhun" / "psk.key"

    # 验证结果缓存（秒）
    CACHE_TTL = 60


class VerifyResult(Enum):
    """验证结果"""
    PASSED = "PASSED"           # 通过
    FAILED = "FAILED"           # 失败
    DEGRADED = "DEGRADED"       # 降级通过
    PENDING = "PENDING"         # 等待验证


@dataclass
class L0VerifyReport:
    """L0 验证报告"""
    overall: VerifyResult
    gpg_status: str
    device_status: str
    timestamp_status: str
    details: Dict

    def to_ai_format(self) -> str:
        """输出 AI 可消费的标准格式"""
        emoji = {
            VerifyResult.PASSED: "✅",
            VerifyResult.FAILED: "❌",
            VerifyResult.DEGRADED: "⚠️",
            VerifyResult.PENDING: "⏳",
        }
        return f"""
─── L0 身份验证报告 ───
结果: {emoji[self.overall]} {self.overall.value}
GPG:  {self.gpg_status}
设备: {self.device_status}
时间: {self.timestamp_status}
───────────────────────
"""


# ============================================================
# A. GPG 外部验签
# ============================================================

class GPGVerifier:
    """
    GPG 外部验签器
    Claude Code / 本地脚本调用 gpg --verify
    输出标准格式给 AI 消费
    """

    @staticmethod
    def verify_signature(file_path: str, sig_path: Optional[str] = None) -> Tuple[bool, str]:
        """
        验证文件的 GPG 签名

        Args:
            file_path: 被签名的文件路径
            sig_path: 签名文件路径（默认 file_path + .asc）

        Returns:
            (是否通过, 详细信息)
        """
        if sig_path is None:
            sig_path = file_path + ".asc"

        if not os.path.exists(file_path):
            return False, f"文件不存在: {file_path}"

        if not os.path.exists(sig_path):
            return False, f"签名不存在: {sig_path}"

        try:
            result = subprocess.run(
                ["gpg", "--verify", sig_path, file_path],
                capture_output=True,
                text=True,
                timeout=10
            )

            # GPG 验证输出在 stderr
            output = result.stderr

            # 检查是否包含正确的指纹
            if L0Config.GPG_FINGERPRINT in output:
                if "Good signature" in output or "正确的签名" in output:
                    return True, f"GPG 验签通过 · {L0Config.GPG_FINGERPRINT[:16]}..."

            return False, f"GPG 验签失败: {output[:100]}"

        except subprocess.TimeoutExpired:
            return False, "GPG 验签超时"
        except FileNotFoundError:
            return False, "GPG 未安装"
        except Exception as e:
            return False, f"GPG 验签异常: {str(e)}"

    @staticmethod
    def verify_inline_signature(signed_text: str) -> Tuple[bool, str]:
        """
        验证内联签名的文本

        Args:
            signed_text: 包含 -----BEGIN PGP SIGNED MESSAGE----- 的文本

        Returns:
            (是否通过, 详细信息)
        """
        if "-----BEGIN PGP SIGNED MESSAGE-----" not in signed_text:
            return False, "不是有效的 PGP 签名消息"

        try:
            result = subprocess.run(
                ["gpg", "--verify"],
                input=signed_text,
                capture_output=True,
                text=True,
                timeout=10
            )

            output = result.stderr

            if L0Config.GPG_FINGERPRINT in output:
                if "Good signature" in output or "正确的签名" in output:
                    return True, f"内联签名验证通过 · {L0Config.GPG_FINGERPRINT[:16]}..."

            return False, f"内联签名验证失败: {output[:100]}"

        except Exception as e:
            return False, f"内联签名验证异常: {str(e)}"

    @staticmethod
    def check_key_exists() -> Tuple[bool, str]:
        """检查 GPG 密钥是否存在"""
        try:
            result = subprocess.run(
                ["gpg", "--list-keys", L0Config.GPG_FINGERPRINT],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0 and L0Config.GPG_FINGERPRINT in result.stdout:
                return True, f"GPG 密钥存在: {L0Config.GPG_FINGERPRINT[:16]}..."

            return False, "GPG 密钥不存在"

        except Exception as e:
            return False, f"GPG 检查异常: {str(e)}"


# ============================================================
# B. HMAC 预共享密钥（降级方案）
# ============================================================

class HMACVerifier:
    """
    HMAC 预共享密钥验证器
    降级方案：防冒充，不防重放
    """

    @staticmethod
    def _load_psk() -> Optional[bytes]:
        """加载预共享密钥"""
        if L0Config.PSK_FILE.exists():
            with open(L0Config.PSK_FILE, "rb") as f:
                return f.read()
        return None

    @staticmethod
    def generate_token(uid: int, device_fp: str, timestamp: float) -> str:
        """
        生成 HMAC token

        token = HMAC(PSK, UID + 设备指纹 + 时间戳)
        """
        psk = HMACVerifier._load_psk()
        if not psk:
            return ""

        message = f"{uid}:{device_fp}:{int(timestamp)}".encode()
        return hmac.new(psk, message, hashlib.sha256).hexdigest()

    @staticmethod
    def verify_token(token: str, uid: int, device_fp: str, timestamp: float) -> Tuple[bool, str]:
        """
        验证 HMAC token

        Returns:
            (是否通过, 详细信息)
        """
        psk = HMACVerifier._load_psk()
        if not psk:
            return False, "PSK 未配置"

        # 时间窗口检查
        current_time = time.time()
        if abs(current_time - timestamp) > L0Config.TIMESTAMP_WINDOW:
            return False, f"时间戳过期: {abs(current_time - timestamp):.0f}s > {L0Config.TIMESTAMP_WINDOW}s"

        # 计算期望的 token
        expected = HMACVerifier.generate_token(uid, device_fp, timestamp)

        if hmac.compare_digest(token, expected):
            return True, "HMAC 验证通过（降级方案）"

        return False, "HMAC 验证失败"

    @staticmethod
    def init_psk() -> str:
        """初始化预共享密钥"""
        L0Config.PSK_FILE.parent.mkdir(parents=True, exist_ok=True)

        psk = os.urandom(32)
        with open(L0Config.PSK_FILE, "wb") as f:
            f.write(psk)

        # 设置权限
        os.chmod(L0Config.PSK_FILE, 0o600)

        return f"PSK 已生成: {L0Config.PSK_FILE}"


# ============================================================
# C. 硬件绑定 · 设备指纹
# ============================================================

class DeviceVerifier:
    """
    设备指纹验证器
    macOS: IOPlatformUUID / Secure Enclave
    """

    # 绑定的设备指纹（首次运行时自动写入）
    BOUND_DEVICES_FILE = Path.home() / ".longhun" / "bound_devices.json"

    @staticmethod
    def get_device_uuid() -> str:
        """获取 macOS 设备 UUID (IOPlatformUUID)"""
        try:
            result = subprocess.run(
                ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
                capture_output=True,
                text=True,
                timeout=5
            )

            for line in result.stdout.split("\n"):
                if "IOPlatformUUID" in line:
                    # 提取 UUID
                    uuid = line.split('"')[-2]
                    return uuid

            return ""
        except Exception:
            return ""

    @staticmethod
    def get_device_fingerprint() -> str:
        """
        生成设备指纹
        = SHA256(IOPlatformUUID + 硬件型号 + 用户名)
        """
        uuid = DeviceVerifier.get_device_uuid()
        if not uuid:
            return ""

        # 获取硬件型号
        try:
            hw_result = subprocess.run(
                ["sysctl", "-n", "hw.model"],
                capture_output=True,
                text=True,
                timeout=5
            )
            hw_model = hw_result.stdout.strip()
        except:
            hw_model = "unknown"

        # 用户名
        username = os.environ.get("USER", "unknown")

        # 组合并哈希
        combined = f"{uuid}:{hw_model}:{username}"
        return hashlib.sha256(combined.encode()).hexdigest()

    @staticmethod
    def bind_current_device(device_name: str = "default") -> Tuple[bool, str]:
        """绑定当前设备"""
        fp = DeviceVerifier.get_device_fingerprint()
        if not fp:
            return False, "无法获取设备指纹"

        # 加载现有绑定
        bound = {}
        if DeviceVerifier.BOUND_DEVICES_FILE.exists():
            with open(DeviceVerifier.BOUND_DEVICES_FILE, "r") as f:
                bound = json.load(f)

        # 添加绑定
        bound[device_name] = {
            "fingerprint": fp,
            "bound_at": datetime.now().isoformat(),
            "uuid": DeviceVerifier.get_device_uuid(),
        }

        # 保存
        DeviceVerifier.BOUND_DEVICES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DeviceVerifier.BOUND_DEVICES_FILE, "w") as f:
            json.dump(bound, f, indent=2)

        os.chmod(DeviceVerifier.BOUND_DEVICES_FILE, 0o600)

        return True, f"设备已绑定: {device_name} ({fp[:16]}...)"

    @staticmethod
    def verify_device() -> Tuple[bool, str]:
        """验证当前设备是否已绑定"""
        current_fp = DeviceVerifier.get_device_fingerprint()
        if not current_fp:
            return False, "无法获取设备指纹"

        if not DeviceVerifier.BOUND_DEVICES_FILE.exists():
            return False, "无绑定设备记录"

        with open(DeviceVerifier.BOUND_DEVICES_FILE, "r") as f:
            bound = json.load(f)

        for name, info in bound.items():
            if info.get("fingerprint") == current_fp:
                return True, f"设备已绑定: {name}"

        return False, f"设备未绑定: {current_fp[:16]}..."


# ============================================================
# L0 综合验证器
# ============================================================

class L0IdentityVerifier:
    """
    L0 综合身份验证器
    协调 GPG + 设备 + 时间戳 三重验证
    """

    @staticmethod
    def full_verify(
        gpg_signature: Optional[str] = None,
        signed_file: Optional[str] = None,
        hmac_token: Optional[str] = None,
        uid: int = L0Config.MASTER_UID,
        timestamp: Optional[float] = None
    ) -> L0VerifyReport:
        """
        完整 L0 验证

        验证流程：
        1. 设备指纹验证（必须）
        2. GPG 签名验证（主）或 HMAC 验证（备）
        3. 时间戳窗口检查

        双重命中才算通过
        """
        timestamp = timestamp or time.time()
        details = {}

        # 1. 设备验证（必须）
        device_ok, device_msg = DeviceVerifier.verify_device()
        device_status = f"{'✅' if device_ok else '❌'} {device_msg}"
        details["device"] = {"ok": device_ok, "msg": device_msg}

        # 2. 时间戳验证
        current_time = time.time()
        time_diff = abs(current_time - timestamp)
        timestamp_ok = time_diff <= L0Config.TIMESTAMP_WINDOW
        timestamp_status = f"{'✅' if timestamp_ok else '❌'} Δt={time_diff:.0f}s"
        details["timestamp"] = {"ok": timestamp_ok, "diff": time_diff}

        # 3. 身份验证（GPG 或 HMAC）
        gpg_ok = False
        gpg_msg = "未提供签名"

        if signed_file:
            gpg_ok, gpg_msg = GPGVerifier.verify_signature(signed_file)
        elif gpg_signature:
            gpg_ok, gpg_msg = GPGVerifier.verify_inline_signature(gpg_signature)
        elif hmac_token:
            # 降级到 HMAC
            device_fp = DeviceVerifier.get_device_fingerprint()
            gpg_ok, gpg_msg = HMACVerifier.verify_token(hmac_token, uid, device_fp, timestamp)

        gpg_status = f"{'✅' if gpg_ok else '❌'} {gpg_msg}"
        details["gpg"] = {"ok": gpg_ok, "msg": gpg_msg}

        # 4. 综合判断
        if device_ok and gpg_ok and timestamp_ok:
            overall = VerifyResult.PASSED
        elif device_ok and timestamp_ok and "降级" in gpg_msg:
            overall = VerifyResult.DEGRADED
        else:
            overall = VerifyResult.FAILED

        return L0VerifyReport(
            overall=overall,
            gpg_status=gpg_status,
            device_status=device_status,
            timestamp_status=timestamp_status,
            details=details
        )

    @staticmethod
    def quick_check() -> L0VerifyReport:
        """
        快速检查（仅设备 + GPG 密钥存在性）
        用于 System Prompt 启动时
        """
        details = {}

        # 设备验证
        device_ok, device_msg = DeviceVerifier.verify_device()
        device_status = f"{'✅' if device_ok else '❌'} {device_msg}"

        # GPG 密钥检查
        gpg_ok, gpg_msg = GPGVerifier.check_key_exists()
        gpg_status = f"{'✅' if gpg_ok else '❌'} {gpg_msg}"

        # 时间戳（当前时间有效）
        timestamp_status = "✅ 当前时间"

        if device_ok and gpg_ok:
            overall = VerifyResult.PASSED
        else:
            overall = VerifyResult.FAILED

        return L0VerifyReport(
            overall=overall,
            gpg_status=gpg_status,
            device_status=device_status,
            timestamp_status=timestamp_status,
            details=details
        )


# ============================================================
# 命令行工具
# ============================================================

def main():
    """命令行入口"""
    import sys

    print("🔐 L0 身份验证器 v1.0")
    print("=" * 50)

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "bind":
            # 绑定当前设备
            name = sys.argv[2] if len(sys.argv) > 2 else "default"
            ok, msg = DeviceVerifier.bind_current_device(name)
            print(f"{'✅' if ok else '❌'} {msg}")

        elif cmd == "verify":
            # 完整验证
            report = L0IdentityVerifier.quick_check()
            print(report.to_ai_format())

        elif cmd == "init-psk":
            # 初始化预共享密钥
            msg = HMACVerifier.init_psk()
            print(f"✅ {msg}")

        elif cmd == "fingerprint":
            # 显示设备指纹
            fp = DeviceVerifier.get_device_fingerprint()
            uuid = DeviceVerifier.get_device_uuid()
            print(f"设备 UUID: {uuid}")
            print(f"设备指纹: {fp}")

        elif cmd == "gpg-check":
            # 检查 GPG 密钥
            ok, msg = GPGVerifier.check_key_exists()
            print(f"{'✅' if ok else '❌'} {msg}")

        else:
            print(f"未知命令: {cmd}")
            print("可用命令: bind, verify, init-psk, fingerprint, gpg-check")
    else:
        # 默认：快速检查
        print("\n📋 快速检查...")
        report = L0IdentityVerifier.quick_check()
        print(report.to_ai_format())

        # 设备信息
        print("📱 设备信息:")
        fp = DeviceVerifier.get_device_fingerprint()
        print(f"   指纹: {fp[:32]}...")


if __name__ == "__main__":
    main()
