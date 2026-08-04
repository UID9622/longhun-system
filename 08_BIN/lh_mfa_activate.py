#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# 龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-MFA-ACTIVATE-v2.0-9E1D4C7B
# CREATOR: 诸葛鑫（UID9622）
# PROTOCOL: CC BY-NC-SA 4.0
# 功能: 龍魂系统 · MFA/TOTP 扫码激活引擎 v2.0
# 说明: 标准 RFC 6238 TOTP，纯本地校验，兼容华为账号/任何 TOTP App
"""
龍魂系统 · MFA/TOTP 扫码激活引擎 v2.0

使用方式:
  ① python bin/lh_mfa_bind.py --generate          # 生成二维码+密钥
  ② 手机扫码或手动输入密钥（华为账号 / Google Authenticator / Authy 等）
  ③ python bin/lh_mfa_activate.py --code 123456   # 输入动态码激活
  ④ python bin/lh_mfa_activate.py --status        # 查看激活状态
  ⑤ python bin/lh_mfa_activate.py --test-code     # 查看当前应输入的动态码（调试用）
  ⑥ python bin/lh_mfa_activate.py --unbind <设备ID> # 解绑设备

DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-MFA-ACTIVATE-v2.0-9E1D4C7B
"""

import os
import sys
import json
import hashlib
import time
import re
import hmac
import base64
import struct
from datetime import datetime, timedelta
from pathlib import Path

# 依赖 qrcode 仅用于生成二维码图片；未安装时降级为文本密钥
try:
    import qrcode
except ImportError:
    qrcode = None

# ═══════════════════════════════════════════════════════════════════════════════
# P0 焊死配置
# ═══════════════════════════════════════════════════════════════════════════════

P0_CONFIG = {
    "uid": "9622",
    "founder": "龍芯北辰 UID9622",
    "issuer": "龍魂系统-UID9622",
    "account": "longhun@uid9622.cn",
    "log_dir": os.path.expanduser("~/.longhun"),
    "registry_file": "mfa_registry.json",
    "audit_log": "mfa_activate.log",
    "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
}


# ═══════════════════════════════════════════════════════════════════════════════
# TOTP 算法（RFC 6238）
# ═══════════════════════════════════════════════════════════════════════════════

def generate_totp_secret():
    """生成 20 字节随机密钥并 Base32 编码"""
    return base64.b32encode(os.urandom(20)).decode("utf-8")


def _totp_code(secret: str, counter: int) -> str:
    """给定计数器生成 TOTP 码"""
    key = base64.b32decode(secret.upper())
    counter_bytes = struct.pack(">Q", counter)
    hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()
    offset = hmac_hash[-1] & 0x0F
    code = struct.unpack(">I", hmac_hash[offset:offset + 4])[0]
    code = code & 0x7FFFFFFF
    return str(code % 1000000).zfill(6)


def get_totp_code(secret: str, time_step: int = 30) -> str:
    """基于当前时间生成 TOTP 动态码"""
    return _totp_code(secret, int(time.time() // time_step))


def verify_totp_code(secret: str, code: str, time_step: int = 30, window: int = 1) -> bool:
    """验证 TOTP 动态码，允许前后 window 个时间窗口"""
    counter = int(time.time() // time_step)
    for i in range(-window, window + 1):
        if _totp_code(secret, counter + i) == code:
            return True
    return False


# ═══════════════════════════════════════════════════════════════════════════════
# 龍魂 MFA 核心类
# ═══════════════════════════════════════════════════════════════════════════════

class LonghunMFA:
    """龍魂系统 MFA/TOTP 扫码激活引擎"""

    def __init__(self):
        self.log_dir = Path(P0_CONFIG["log_dir"])
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.registry_path = self.log_dir / P0_CONFIG["registry_file"]
        self.audit_path = self.log_dir / P0_CONFIG["audit_log"]
        self.registry = self._load_registry()

    def _load_registry(self):
        if self.registry_path.exists():
            try:
                with open(self.registry_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        return {
            "bindings": {},      # 已绑定设备
            "used_codes": [],    # 已使用动态码（防重放）
            "dna_chain": [],     # DNA 追溯链
            "failed_attempts": 0, # 连续失败次数
            "lock_until": None,  # 锁定截止时间
        }

    def _save_registry(self):
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(self.registry, f, ensure_ascii=False, indent=2)

    def _audit(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}"
        with open(self.audit_path, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
        print(entry)

    def _is_locked(self):
        if self.registry.get("lock_until"):
            lock_time = datetime.fromisoformat(self.registry["lock_until"])
            if datetime.now() < lock_time:
                return True, (lock_time - datetime.now()).seconds
            self.registry["lock_until"] = None
            self.registry["failed_attempts"] = 0
            self._save_registry()
        return False, 0

    def _lock_account(self, minutes: int = 15):
        lock_until = datetime.now() + timedelta(minutes=minutes)
        self.registry["lock_until"] = lock_until.isoformat()
        self._save_registry()

    @staticmethod
    def _now_ganzhi():
        """获取当前农历干支四柱（简化版）"""
        now = datetime.now()
        gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        year_g = gan[(now.year - 4) % 10]
        year_z = zhi[(now.year - 4) % 12]
        month_g = gan[(now.year * 12 + now.month + 12) % 10]
        month_z = zhi[(now.month + 1) % 12]
        day_g = gan[(now.toordinal() + 40) % 10]
        day_z = zhi[(now.toordinal() + 40) % 12]
        return f"{year_g}{year_z}·{month_g}{month_z}·{day_g}{day_z}"

    @staticmethod
    def _gua_name():
        now = datetime.now()
        gua_list = [
            "乾", "坤", "屯", "蒙", "需", "讼", "师", "比", "小畜", "履",
            "泰", "否", "同人", "大有", "谦", "豫", "随", "蛊", "临", "观",
            "噬嗑", "贲", "剥", "复", "无妄", "大畜", "颐", "大过", "坎", "离",
            "咸", "恒", "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解",
            "损", "益", "夬", "姤", "萃", "升", "困", "井", "革", "鼎",
            "震", "艮", "渐", "归妹", "丰", "旅", "巽", "兑", "涣", "节",
            "中孚", "小过", "既济", "未济",
        ]
        return gua_list[now.minute % 64]

    def _generate_dna(self, device_id: str, code: str) -> str:
        """生成 DNA 追溯码"""
        dev_hash = hashlib.sha256(device_id.encode()).hexdigest()[:8]
        return f"#龍芯⚡️{self._now_ganzhi()}·{self._gua_name()}-MFA激活-v2.0-{dev_hash}"

    def _generate_seven_factor(self, dna: str, device_id: str, code: str) -> dict:
        return {
            "timestamp": datetime.now().isoformat(),
            "device_id": device_id,
            "device_fp": hashlib.sha256(device_id.encode()).hexdigest()[:16],
            "operator": P0_CONFIG["founder"],
            "action_type": "MFA_ACTIVATE",
            "input_hash": hashlib.sha256(code.encode()).hexdigest()[:16],
            "output_hash": hashlib.sha256(dna.encode()).hexdigest()[:16],
            "random_salt": hashlib.sha256(os.urandom(16)).hexdigest()[:16],
        }

    def _hash_chain(self, data: str) -> str:
        prev = "0" * 64
        if self.registry["dna_chain"]:
            prev = self.registry["dna_chain"][-1].get("chain_hash", prev)
        return hashlib.sha256((prev + data + str(time.time())).encode()).hexdigest()

    def _header(self, title: str):
        print("=" * 72)
        print(f"🐉 {title}")
        print("=" * 72)

    def generate_binding_qr(self):
        """生成绑定二维码与密钥"""
        self._header("龍魂系统 · MFA/TOTP 绑定二维码生成")

        secret = generate_totp_secret()
        device_id = hashlib.sha256(os.urandom(32)).hexdigest()[:16]

        totp_uri = (
            f"otpauth://totp/{P0_CONFIG['issuer']}:{P0_CONFIG['account']}?"
            f"secret={secret}&issuer={P0_CONFIG['issuer']}&"
            f"algorithm=SHA1&digits=6&period=30"
        )

        img_path = self.log_dir / f"longhun_mfa_bind_{device_id}.png"
        key_path = self.log_dir / f"longhun_mfa_secret_{device_id}.txt"

        if qrcode:
            qr = qrcode.QRCode(version=1, box_size=10, border=2)
            qr.add_data(totp_uri)
            qr.make(fit=True)
            qr.make_image(fill_color="black", back_color="white").save(img_path)
        else:
            img_path = None
            print("⚠️ 未安装 qrcode，仅输出文本密钥，可手动输入到 TOTP App。")

        with open(key_path, "w", encoding="utf-8") as f:
            f.write("龍魂系统 MFA 绑定密钥\n")
            f.write(f"设备ID: {device_id}\n")
            f.write(f"密钥: {secret}\n")
            f.write("说明: 在华为账号App、Google Authenticator、Authy 等 TOTP App 中手动输入此密钥\n")

        self.registry["bindings"][device_id] = {
            "secret": secret,
            "created_at": datetime.now().isoformat(),
            "status": "pending",
            "device_info": platform_info(),
        }
        self._save_registry()

        print(f"\n✅ 绑定信息已生成")
        if img_path:
            print(f"   二维码图片: {img_path}")
        print(f"   密钥文本:   {key_path}")
        print(f"   设备ID:     {device_id}")
        print(f"   密钥:       {secret}")
        print(f"\n📱 操作步骤:")
        print(f"   1. 打开 TOTP App（华为账号 / Google Authenticator / Authy / Microsoft Authenticator）")
        print(f"   2. 扫描二维码或手动输入密钥")
        print(f"   3. 输入 App 显示的6位动态码:")
        print(f"      python bin/lh_mfa_activate.py --code xxxxxx")
        print(f"\n⚠️  密钥只显示一次，请妥善保存！")
        print(f"\n🔒 确认码: {P0_CONFIG['confirm']}")

        self._audit(f"生成绑定二维码: device_id={device_id}")
        return device_id, secret

    def test_code(self):
        """输出当前最新的 pending/active 设备应显示的动态码（仅用于调试/无手机场景）"""
        self._header("龍魂系统 · MFA 当前动态码（调试）")

        candidates = [
            (did, info) for did, info in self.registry["bindings"].items()
            if info["status"] in ("pending", "active")
        ]
        if not candidates:
            print("\n❌ 失效速121 · 设备未绑定 · 请先执行: python bin/lh_mfa_bind.py --generate")
            return False

        for device_id, info in candidates:
            secret = info["secret"]
            code = get_totp_code(secret)
            remaining = 30 - (int(time.time()) % 30)
            print(f"\n设备ID: {device_id}")
            print(f"当前动态码: {code}")
            print(f"有效期剩余: {remaining} 秒")
        self._audit("查询当前动态码（调试）")
        return True

    def activate(self, code: str, confirm_code: str = None):
        """MFA 激活主流程"""
        self._header("龍魂系统 · MFA/TOTP 激活")

        locked, remaining = self._is_locked()
        if locked:
            print(f"\n❌ 失效速120 · 账号已锁定")
            print(f"   剩余锁定时间: {remaining} 秒")
            self._audit(f"激活失败: 账号锁定中, 剩余{remaining}秒", "WARN")
            return False

        if confirm_code and confirm_code != P0_CONFIG["confirm"]:
            print("\n❌ 失效速120 · 确认码无效")
            self._audit(f"激活失败: 确认码无效", "WARN")
            return False

        if not re.match(r"^\d{6}$", code):
            print("\n❌ 失效速120 · 动态码格式错误 · 应为6位数字")
            self._audit(f"激活失败: 动态码格式错误 - {code}", "WARN")
            return False

        if code in self.registry["used_codes"]:
            print("\n❌ 失效速120 · 动态码已使用 · 防重放拒绝")
            self._audit(f"激活失败: 动态码已使用 - {code}", "WARN")
            return False

        if not self.registry["bindings"]:
            print("\n❌ 失效速121 · 设备未绑定 · 请先执行: python bin/lh_mfa_bind.py --generate")
            self._audit("激活失败: 无绑定设备", "WARN")
            return False

        matched_device = None
        matched_secret = None
        for device_id, binding in self.registry["bindings"].items():
            if binding["status"] in ("pending", "active"):
                if verify_totp_code(binding["secret"], code):
                    matched_device = device_id
                    matched_secret = binding["secret"]
                    break

        if not matched_device:
            self.registry["failed_attempts"] += 1
            self._save_registry()
            remaining_attempts = 3 - self.registry["failed_attempts"]

            if self.registry["failed_attempts"] >= 3:
                self._lock_account(minutes=15)
                print("\n❌ 失效速120 · 连续3次错误，账号锁定15分钟")
                self._audit("激活失败: 连续3次错误, 账号锁定15分钟", "ERROR")
            else:
                print(f"\n❌ 失效速120 · 动态码错误 · 剩余尝试次数: {remaining_attempts}")
                self._audit(f"激活失败: 动态码错误, 剩余{remaining_attempts}次", "WARN")
            return False

        # 校验通过
        self.registry["failed_attempts"] = 0
        self.registry["used_codes"].append(code)
        self.registry["bindings"][matched_device]["status"] = "active"
        self.registry["bindings"][matched_device]["last_activated"] = datetime.now().isoformat()

        dna = self._generate_dna(matched_device, code)
        sig = self._generate_seven_factor(dna, matched_device, code)
        chain_hash = self._hash_chain(dna + code + json.dumps(sig, sort_keys=True))

        record = {
            "code": code,
            "dna": dna,
            "device_id": matched_device,
            "time": datetime.now().isoformat(),
            "signature": sig,
            "chain_hash": chain_hash,
        }
        self.registry["dna_chain"].append(record)
        self._save_registry()

        print(f"\n✅ 龍魂人格激活成功")
        print(f"   设备ID:   {matched_device}")
        print(f"   DNA追溯:  {dna}")
        print(f"   确认码:   {P0_CONFIG['confirm']}")
        print(f"   激活时间: {sig['timestamp']}")
        print(f"   链上哈希: {chain_hash}")
        print(f"\n   【龍魂人格矩阵已加载】")
        print(f"   · 16人格矩阵: 就绪")
        print(f"   · 本地模型:   Ollama / llama.cpp")
        print(f"   · 数据主权:   本地校验，密钥在用户手机")

        self._audit(f"激活成功: DNA={dna}, device={matched_device}", "SUCCESS")
        return True

    def unbind(self, device_id: str):
        """解绑设备"""
        self._header("龍魂系统 · MFA 设备解绑")

        if device_id not in self.registry["bindings"]:
            print(f"\n❌ 失效速121 · 设备未找到: {device_id}")
            self._audit(f"解绑失败: 设备不存在 - {device_id}", "WARN")
            return False

        self.registry["bindings"][device_id]["status"] = "revoked"
        self.registry["bindings"][device_id]["revoked_at"] = datetime.now().isoformat()
        self._save_registry()

        print(f"\n✅ 设备已解绑: {device_id}")
        self._audit(f"设备解绑: {device_id}", "SUCCESS")
        return True

    def status(self):
        """查询激活状态"""
        self._header("龍魂系统 · MFA 激活状态")

        print(f"\n已绑定设备: {len(self.registry['bindings'])}")
        print(f"已激活次数: {len(self.registry['dna_chain'])}")
        print(f"连续失败:   {self.registry['failed_attempts']}")

        locked, remaining = self._is_locked()
        if locked:
            print(f"账号锁定:   剩余 {remaining} 秒")
        else:
            print("账号锁定:   无")

        print("\n设备列表:")
        if not self.registry["bindings"]:
            print("  （无）")
        for did, info in self.registry["bindings"].items():
            icon = {"active": "🟢", "pending": "🟡", "revoked": "🔴"}.get(info["status"], "⚪")
            last = info.get("last_activated", "未激活")
            created = info.get("created_at", "未知")
            print(f"  {icon} {did} | {info['status']:8s} | 创建 {created} | 最近激活 {last}")

        if self.registry["dna_chain"]:
            last = self.registry["dna_chain"][-1]
            print(f"\n最近一次激活:")
            print(f"  DNA:  {last['dna']}")
            print(f"  时间: {last['time']}")
            print(f"  哈希: {last['chain_hash']}")


def platform_info():
    return {
        "system": os.name,
        "platform": sys.platform,
        "time": datetime.now().isoformat(),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂系统 MFA/TOTP 扫码激活引擎 v2.0")
    parser.add_argument("--generate", action="store_true", help="生成绑定二维码")
    parser.add_argument("--code", help="输入6位 MFA 动态码激活")
    parser.add_argument("--test-code", action="store_true", help="查看当前应输入的动态码（调试）")
    parser.add_argument("--status", action="store_true", help="查询激活状态")
    parser.add_argument("--unbind", help="解绑指定设备ID")
    parser.add_argument("--confirm", help=f"确认码（可选，正确值: {P0_CONFIG['confirm']}）")
    args = parser.parse_args()

    mfa = LonghunMFA()

    if args.generate:
        mfa.generate_binding_qr()
    elif args.test_code:
        mfa.test_code()
    elif args.code:
        mfa.activate(args.code, args.confirm)
    elif args.status:
        mfa.status()
    elif args.unbind:
        mfa.unbind(args.unbind)
    else:
        parser.print_help()
        print(f"\nDNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-MFA-ACTIVATE-v2.0-9E1D4C7B")
        print(f"确认码: {P0_CONFIG['confirm']}")


if __name__ == "__main__":
    main()
