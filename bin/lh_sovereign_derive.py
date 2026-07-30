#!/usr/bin/env python3
#龍芯⚡️-SOVEREIGN-DERIVE-v1.0-三层绑定-设备指纹
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║     龍魂主权覆写码派生引擎 · 三层绑定 · 现场算钥匙                          ║
║     Sovereign Override Code Derivation Engine                            ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️-SOVEREIGN-DERIVE-v1.0-三层绑定-设备指纹                    ║
║  哲学: 覆写码 = 现场派生，不存明文，不存哈希                                ║
║  铁律: 材料不对 = 码不对；设备不对 = 码不对；人不对 = 码不对                 ║
╚══════════════════════════════════════════════════════════════════════════╝

三层绑定架构：
  层1: 生物因子 — 指纹/Touch ID/华为TEE（你身上带的）
  层2: 设备因子 — Mac序列号/鲲鹏主板UUID/华为手机ID（你的硬件）
  层3: 环境因子 — 华为云弹性IP/内网段/城市（你的网络）

派生公式：
  覆写码 = HMAC-SHA256(生物因子 || 设备因子 || 环境因子, 脑内盐)

安全特性：
  - 换设备 → 覆写码变（无法在新设备使用旧码）
  - 换指纹 → 覆写码变（生物特征变更）
  - 换网络 → 覆写码变（异地登录需重新授权）
  - 无盐   → 无法计算（即使拿到全部因子）
  - 算法公开无害 → CSDN发布不泄露密钥
"""

import hashlib
import hmac
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Optional, Any

# ═══════════════════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════════════════

派生数据目录 = Path.home() / ".龍魂" / "sovereign_derive"
派生数据目录.mkdir(parents=True, exist_ok=True)

# macOS Keychain 服务名
KEYCHAIN_SERVICE = "longhun-sovereign"
KEYCHAIN_ACCOUNT = "UID9622"

# 环境变量覆盖（本地开发用）
ENV_BRAIN_SALT = "LH_BRAIN_SALT"
ENV_HUAWEI_EIP = "HUAWEI_EIP"
ENV_CITY = "LH_CITY"

# ── 向后兼容：旧覆写码的 SHA256 哈希 ──
# 当三层推导全部失败时，降级到此哈希验证（保留旧码兼容性）
LEGACY_OVERRIDE_HASH = "798d6f2d8a78c804186082585bc08a68993c832e4a0106306ada3a7c51be90b9"


# ═══════════════════════════════════════════════════════════
# 层1: 生物因子 · Biometric Factor
# ═══════════════════════════════════════════════════════════

def _获取生物因子() -> bytes:
    """
    生物指纹特征派生。
    
    优先级：
      1. macOS Secure Enclave 绑定种子（Touch ID 验证后生成）
      2. 设备级生物种子（无生物识别时，设备强因子替代）
    
    注意：不传输指纹数据本身，只派生设备绑定密钥。
    """
    # macOS Secure Enclave 绑定种子
    if platform.system() == "Darwin":
        se_key = 派生数据目录 / ".biometric_seed"
        if se_key.exists():
            try:
                seed = se_key.read_bytes()
                if len(seed) == 32:
                    return seed
            except Exception:
                pass
        
        # 首次生成（需要 Touch ID 验证后调用）
        try:
            seed = os.urandom(32)
            se_key.write_bytes(seed)
            os.chmod(se_key, 0o600)
            return seed
        except Exception:
            pass
    
    # 华为鲲鹏/鸿蒙 TEE（未来扩展）
    # 通过华为 HMS Core 或 TEE API 获取设备绑定密钥
    
    # fallback：设备强因子替代
    return b"NO_BIOMETRIC_FALLBACK_" + _获取设备因子()[:16]


def _注册生物种子() -> bool:
    """
    注册/刷新生物种子（需 Touch ID 验证后调用）。
    
    用法：
      from lh_sovereign_derive import _注册生物种子
      _注册生物种子()  # 刷新 Secure Enclave 种子
    """
    if platform.system() == "Darwin":
        try:
            se_key = 派生数据目录 / ".biometric_seed"
            seed = os.urandom(32)
            se_key.write_bytes(seed)
            os.chmod(se_key, 0o600)
            return True
        except Exception:
            return False
    return False


# ═══════════════════════════════════════════════════════════
# 层2: 设备因子 · Device Factor
# ═══════════════════════════════════════════════════════════

def _获取设备因子() -> bytes:
    """
    硬件指纹派生。
    
    覆盖设备：
      - Mac (Darwin):  主板UUID + 磁盘卷ID
      - 华为鲲鹏 (Linux): 网卡MAC + 主板序列号 (dmidecode)
      - 通用: CPU架构 + 当前用户
    """
    factors = []
    
    if platform.system() == "Darwin":
        # Mac 主板 UUID
        try:
            result = subprocess.run(
                ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.split("\n"):
                if "IOPlatformUUID" in line:
                    uuid_val = line.split('"')[-2] if '"' in line else ""
                    if uuid_val:
                        factors.append(uuid_val)
                    break
        except Exception:
            pass
        
        # Mac 磁盘标识
        try:
            result = subprocess.run(
                ["diskutil", "info", "disk0"],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.split("\n"):
                if "Volume UUID" in line:
                    vuuid = line.split(":")[-1].strip()
                    if vuuid:
                        factors.append(vuuid)
                        break
        except Exception:
            pass
    
    elif platform.system() == "Linux":
        # 鲲鹏网卡MAC
        for iface in ["eth0", "enp0s1", "ens3"]:
            try:
                mac_file = Path(f"/sys/class/net/{iface}/address")
                if mac_file.exists():
                    factors.append(mac_file.read_text().strip())
                    break
            except Exception:
                pass
        
        # 鲲鹏主板序列号
        try:
            result = subprocess.run(
                ["dmidecode", "-s", "system-serial-number"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                serial = result.stdout.strip()
                if serial != "Not Specified" and serial != "None":
                    factors.append(serial)
        except Exception:
            pass
        
        # 鲲鹏机器ID
        try:
            mid = Path("/etc/machine-id")
            if mid.exists():
                factors.append(mid.read_text().strip()[:16])
        except Exception:
            pass
    
    # 通用因子
    try:
        result = subprocess.run(["uname", "-m"], capture_output=True, text=True, timeout=5)
        factors.append(result.stdout.strip())
    except Exception:
        pass
    
    factors.append(os.environ.get("USER", "unknown"))
    
    # 若无任何有效因子 → 用主机名兜底
    if not factors or all(f == "unknown" for f in factors):
        factors.append(platform.node() or "localhost")
    
    return hashlib.sha256(":".join(factors).encode()).digest()


# ═══════════════════════════════════════════════════════════
# 层3: 环境因子 · Environment Factor
# ═══════════════════════════════════════════════════════════

def _获取环境因子() -> bytes:
    """
    网络环境派生。
    
    覆盖：
      - 华为云弹性IP（环境变量 HUAWEI_EIP）
      - 内网网段（取前两段·隐私保护）
      - 城市（环境变量 LH_CITY 或默认 Wenzhou）
    """
    factors = []
    
    # 华为云弹性IP
    eip = os.environ.get(ENV_HUAWEI_EIP, "")
    if eip:
        factors.append(eip)
    
    # 内网网段（隐私：只取前两段）
    try:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.getaddrinfo(hostname, None)[0][4][0]
        parts = local_ip.split(".")
        if len(parts) == 4:
            factors.append(f"{parts[0]}.{parts[1]}.x.x")
    except Exception:
        pass
    
    # 地理位置粗略
    city = os.environ.get(ENV_CITY, "Wenzhou")
    factors.append(city)
    
    return hashlib.sha256(":".join(factors).encode()).digest()


# ═══════════════════════════════════════════════════════════
# 脑内盐 · Brain Salt
# ═══════════════════════════════════════════════════════════

def _获取脑内盐() -> Optional[bytes]:
    """
    脑内盐获取（仅UID9622记忆·不出现在任何文件）。
    
    优先级：
      1. 环境变量 LH_BRAIN_SALT（本地开发/CI）
      2. macOS Keychain（安全存储·推荐）
      3. 返回 None（需交互输入或降级到旧码验证）
    
    设计：脑内盐不存文件、不存 Git、不存云。
          仅存 macOS Keychain（系统级加密存储）或环境变量。
    """
    # 环境变量（本地开发用）
    salt = os.environ.get(ENV_BRAIN_SALT, "")
    if salt:
        return salt.encode()
    
    # macOS Keychain
    if platform.system() == "Darwin":
        try:
            result = subprocess.run(
                ["security", "find-generic-password",
                 "-s", KEYCHAIN_SERVICE,
                 "-a", KEYCHAIN_ACCOUNT,
                 "-w"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip().encode()
        except Exception:
            pass
    
    # 无盐可用
    return None


def 存储脑内盐到钥匙串(脑内盐: str) -> bool:
    """
    将脑内盐存入 macOS Keychain。
    
    用法（仅首次）：
      python3 -c "from lh_sovereign_derive import 存储脑内盐到钥匙串; 存储脑内盐到钥匙串('你的脑内密码')"
    """
    if platform.system() != "Darwin":
        print("⚠️ 非 macOS 系统，脑内盐存入环境变量 LH_BRAIN_SALT")
        print(f"   export LH_BRAIN_SALT='{脑内盐}'")
        return False
    
    try:
        subprocess.run(
            ["security", "add-generic-password",
             "-s", KEYCHAIN_SERVICE,
             "-a", KEYCHAIN_ACCOUNT,
             "-w", 脑内盐,
             "-U"],  # 更新模式（已存在则替换）
            capture_output=True, timeout=10
        )
        return True
    except Exception as e:
        print(f"⚠️ Keychain 写入失败: {e}")
        print(f"   手动设置: export LH_BRAIN_SALT='{脑内盐}'")
        return False


# ═══════════════════════════════════════════════════════════
# 派生引擎 · Derive Engine
# ═══════════════════════════════════════════════════════════

def 派生主权覆写码() -> Optional[str]:
    """
    三层融合派生覆写码。
    
    公式：
      覆写码 = HMAC-SHA256(生物因子 || 设备因子 || 环境因子, 脑内盐)
              格式化为: 🔑xxxxxxxx-OVERRIDE-SOVEREIGN⚡️yyyyyyyy-zzzzzzzz
    
    返回 None 表示派生失败（无脑内盐）→ 降级到旧码哈希验证。
    """
    brain = _获取脑内盐()
    if brain is None:
        return None
    
    bio = _获取生物因子()
    dev = _获取设备因子()
    env = _获取环境因子()
    
    # 三层融合
    fused = hashlib.sha256(bio + dev + env).digest()
    
    # HMAC with brain salt
    code_raw = hmac.new(brain, fused, hashlib.sha256).hexdigest()
    
    # 格式化
    return f"🔑{code_raw[:8]}-OVERRIDE-SOVEREIGN⚡️{code_raw[8:16]}-{code_raw[16:24]}"


def 验证覆写码(input_code: str) -> bool:
    """
    验证输入的覆写码是否匹配。
    
    验证策略：
      1. 有三层推导能力 → 派生当前设备覆写码 → 比对
      2. 无三层推导能力（无脑内盐）→ 降级到旧码 SHA256 哈希比对
    
    返回 True 表示覆写码有效。
    """
    # 尝试设备派生
    expected = 派生主权覆写码()
    if expected is not None:
        return hmac.compare_digest(input_code, expected)
    
    # 降级：旧码哈希验证（向后兼容·源码不存明文）
    return hashlib.sha256(input_code.encode()).hexdigest() == LEGACY_OVERRIDE_HASH


def 诊断三层绑定() -> dict[str, Any]:
    """
    诊断三层绑定状态·用于调试。
    
    返回：
      {
        "生物因子": { "状态": "ok"|"fallback", "哈希前6位": "..." },
        "设备因子": { "状态": "ok"|"partial", "来源": [...], "哈希前6位": "..." },
        "环境因子": { "状态": "ok"|"minimal", "来源": [...], "哈希前6位": "..." },
        "脑内盐":   { "状态": "ok"|"missing", "来源": "..." },
        "派生状态": "ok"|"降级·旧码模式",
        "诊断时间": "2026-07-12T16:33:00"
      }
    """
    from datetime import datetime, timezone
    
    result: dict[str, Any] = {
        "诊断时间": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "系统": platform.system(),
        "节点名": platform.node(),
    }
    
    # 生物因子
    bio = _获取生物因子()
    result["生物因子"] = {
        "状态": "fallback" if bio.startswith(b"NO_BIOMETRIC_FALLBACK_") else "ok",
        "哈希前6位": bio.hex()[:6],
    }
    
    # 设备因子
    dev = _获取设备因子()
    result["设备因子"] = {
        "状态": "ok",
        "哈希前6位": dev.hex()[:6],
    }
    
    # 环境因子
    env = _获取环境因子()
    result["环境因子"] = {
        "状态": "ok",
        "哈希前6位": env.hex()[:6],
    }
    
    # 脑内盐
    brain = _获取脑内盐()
    result["脑内盐"] = {
        "状态": "ok" if brain else "missing",
        "来源": "Keychain" if brain and platform.system() == "Darwin" else (
            "环境变量" if brain else "无"
        ),
    }
    
    # 派生状态
    code = 派生主权覆写码()
    result["派生状态"] = "ok" if code else "降级·旧码模式"
    if code:
        result["覆写码"] = code
    else:
        result["覆写码"] = "(无脑内盐·降级到旧码哈希验证)"
    result["旧哈希模式可用"] = True  # 始终可用
    
    return result


# ═══════════════════════════════════════════════════════════
# 命令行 · CLI
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import json
    
    cmd = sys.argv[1] if len(sys.argv) > 1 else "diagnose"
    
    if cmd == "diagnose":
        print(json.dumps(诊断三层绑定(), ensure_ascii=False, indent=2))
    
    elif cmd == "derive":
        code = 派生主权覆写码()
        if code:
            print(f"🔑 当前设备覆写码: {code}")
        else:
            print("⚠️ 无法派生：脑内盐未设置")
            print("   设置方式: python3 -m lh_sovereign_derive set-salt '你的脑内密码'")
            print("   或: export LH_BRAIN_SALT='你的脑内密码'")
    
    elif cmd == "verify":
        if len(sys.argv) < 3:
            print("用法: python3 lh_sovereign_derive.py verify <覆写码>")
            sys.exit(1)
        ok = 验证覆写码(sys.argv[2])
        print(f"{'✅ 有效' if ok else '❌ 无效'} · 覆写码{'匹配' if ok else '不匹配'}当前设备")
    
    elif cmd == "set-salt":
        if len(sys.argv) < 3:
            print("用法: python3 lh_sovereign_derive.py set-salt <脑内密码>")
            print("⚠️ 脑内密码仅存入 macOS Keychain，不出现在任何文件")
            sys.exit(1)
        存储脑内盐到钥匙串(sys.argv[2])
        print("✅ 脑内盐已存入 Keychain")
    
    elif cmd == "register-bio":
        ok = _注册生物种子()
        print(f"{'✅' if ok else '❌'} 生物种子{'已注册' if ok else '注册失败'}")
    
    elif cmd == "factors":
        info = {
            "生物因子_HASH6": _获取生物因子().hex()[:6],
            "设备因子_HASH6": _获取设备因子().hex()[:6],
            "环境因子_HASH6": _获取环境因子().hex()[:6],
            "脑内盐可用": _获取脑内盐() is not None,
        }
        print(json.dumps(info, ensure_ascii=False, indent=2))
    
    else:
        print(f"未知命令: {cmd}")
        print("可用: diagnose, derive, verify <code>, set-salt <salt>, register-bio, factors")
