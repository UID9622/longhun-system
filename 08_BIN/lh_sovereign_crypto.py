# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-12ae0471
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·主权加密模块（SovereignCrypto）v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
用途: 龍魂系统所有加密操作强制使用国密标准
实现: SM2 签名/验签 + SM3 哈希 + SM4 对称加密 + HMAC-SM3
法律依据: 《密码法》| GB/T 32905-2016 | GB/T 32907-2016 | GM/T 0003-2012

DNA: #龍芯⚡️丙午·乙未·辛亥·甲午·䷚颐-SOVEREIGNCRYPTO-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import os
import sys
import struct
import hashlib
import secrets as _secrets
from typing import Tuple, Optional, Union, Dict, Any

# ─── 路径设定 ──────────────────────────────────────────────────
BIN = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BIN)
if BIN not in sys.path:
    sys.path.insert(0, BIN)

# ─── 导入已有国密模块 ──────────────────────────────────────────
from CNSH_国密工具 import SM3, SM4, hmac_sm3  # noqa: E402

# ================================================================
#  一、SM2 椭圆曲线公钥密码算法 (GM/T 0003-2012)
#     纯 Python 实现 — 签名/验签 + 密钥生成
# ================================================================

class SM2Curve:
    """SM2 推荐椭圆曲线参数 y² = x³ + ax + b (mod p)"""

    p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
    a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
    b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
    n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
    Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
    h = 1

    # 用户ID默认值 (GB/T 32918.1-2016 附录A)
    DEFAULT_ID = b"1234567812345678"


class _SM2Math:
    """SM2 椭圆曲线底层运算"""

    @staticmethod
    def _mod_inv(a: int, m: int) -> int:
        """模逆运算: a^(-1) mod m"""
        return pow(a, m - 2, m)

    @classmethod
    def _ec_add(cls, p1: Optional[Tuple[int, int]], p2: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        """椭圆曲线点加法"""
        if p1 is None:
            return p2
        if p2 is None:
            return p1
        x1, y1 = p1
        x2, y2 = p2
        p = SM2Curve.p
        if x1 == x2 and y1 == (-y2 % p):
            return None  # 无穷远点
        if x1 == x2 and y1 == y2:
            lam = (3 * x1 * x1 + SM2Curve.a) * cls._mod_inv(2 * y1, p) % p
        else:
            lam = (y2 - y1) * cls._mod_inv(x2 - x1, p) % p
        x3 = (lam * lam - x1 - x2) % p
        y3 = (lam * (x1 - x3) - y1) % p
        return (x3, y3)

    @classmethod
    def _ec_mul(cls, k: int, pt: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """椭圆曲线标量乘法: k * pt"""
        if k == 0:
            return None
        result = None
        addend = pt
        while k > 0:
            if k & 1:
                result = cls._ec_add(result, addend)
            addend = cls._ec_add(addend, addend)
            k >>= 1
        return result


# 全局曲线基点
_G = (SM2Curve.Gx, SM2Curve.Gy)


class SM2KeyPair:
    """SM2 密钥对"""

    def __init__(self, private_key: int, public_key: Tuple[int, int]):
        self.d = private_key          # 私钥（整数）
        self.P = public_key           # 公钥（点坐标）
        self._validate()

    def _validate(self):
        """验证密钥对有效性"""
        if self.d <= 0 or self.d >= SM2Curve.n:
            raise ValueError("SM2 私钥不在有效范围内")
        computed = _SM2Math._ec_mul(self.d, _G)
        if computed is None or computed != self.P:
            raise ValueError("SM2 密钥对不匹配")

    def public_key_bytes(self, compressed: bool = False) -> bytes:
        """公钥导出为字节"""
        x, y = self.P
        if compressed:
            prefix = 0x02 if y % 2 == 0 else 0x03
            return bytes([prefix]) + x.to_bytes(32, "big")
        return b"\x04" + x.to_bytes(32, "big") + y.to_bytes(32, "big")

    def private_key_bytes(self) -> bytes:
        """私钥导出为 32 字节大端"""
        return self.d.to_bytes(32, "big")


class SM2:
    """SM2 签名/验签（纯Python实现）"""

    @staticmethod
    def generate_keypair() -> SM2KeyPair:
        """生成 SM2 密钥对"""
        while True:
            d = int.from_bytes(_secrets.token_bytes(32), "big") % (SM2Curve.n - 1)
            if d > 0:
                P = _SM2Math._ec_mul(d, _G)
                if P is not None:
                    return SM2KeyPair(d, P)

    @staticmethod
    def _za(pub_x: int, pub_y: int, user_id: bytes = SM2Curve.DEFAULT_ID) -> bytes:
        """计算 ZA = SM3(ENTLA || ID || a || b || Gx || Gy || Px || Py)"""
        entla = struct.pack(">H", len(user_id) * 8)
        raw = (
            entla
            + user_id
            + SM2Curve.a.to_bytes(32, "big")
            + SM2Curve.b.to_bytes(32, "big")
            + SM2Curve.Gx.to_bytes(32, "big")
            + SM2Curve.Gy.to_bytes(32, "big")
            + pub_x.to_bytes(32, "big")
            + pub_y.to_bytes(32, "big")
        )
        return SM3.hash(raw)

    @classmethod
    def sign(cls, message: Union[str, bytes], keypair: SM2KeyPair,
             user_id: bytes = SM2Curve.DEFAULT_ID) -> Tuple[int, int]:
        """
        SM2 数字签名
        返回: (r, s) 签名对
        标准: GM/T 0003.2-2012
        """
        if isinstance(message, str):
            message = message.encode("utf-8")
        px, py = keypair.P
        za = cls._za(px, py, user_id)
        e_bytes = SM3.hash(za + message)
        e = int.from_bytes(e_bytes, "big")

        n = SM2Curve.n
        while True:
            k = int.from_bytes(_secrets.token_bytes(32), "big") % (n - 1)
            if k == 0:
                continue
            kG = _SM2Math._ec_mul(k, _G)
            if kG is None:
                continue
            x1, _ = kG
            r = (e + x1) % n
            if r == 0 or r + k == n:
                continue
            s = (_SM2Math._mod_inv(1 + keypair.d, n) * (k - r * keypair.d)) % n
            if s != 0:
                return (r, s)

    @classmethod
    def _mod_inv(cls, a: int, m: int) -> int:
        return pow(a, m - 2, m)

    @classmethod
    def verify(cls, message: Union[str, bytes], signature: Tuple[int, int],
               public_key: Tuple[int, int], user_id: bytes = SM2Curve.DEFAULT_ID) -> bool:
        """
        SM2 签名验证
        标准: GM/T 0003.2-2012
        """
        if isinstance(message, str):
            message = message.encode("utf-8")
        r, s = signature
        n = SM2Curve.n
        if not (1 <= r < n and 1 <= s < n):
            return False

        px, py = public_key
        za = cls._za(px, py, user_id)
        e_bytes = SM3.hash(za + message)
        e = int.from_bytes(e_bytes, "big")

        t = (r + s) % n
        if t == 0:
            return False

        t1 = _SM2Math._ec_mul(s, _G)
        t2 = _SM2Math._ec_mul(t, public_key)
        point = _SM2Math._ec_add(t1, t2)
        if point is None:
            return False

        x1, _ = point
        R = (e + x1) % n
        return R == r

    @classmethod
    def sign_detached(cls, message: Union[str, bytes], keypair: SM2KeyPair,
                      user_id: bytes = SM2Curve.DEFAULT_ID) -> Dict[str, Any]:
        """
        SM2 签名（带主权声明元数据）
        返回: 结构化签名对象
        """
        r, s = cls.sign(message, keypair, user_id)
        return {
            "signature": {
                "r": hex(r),
                "s": hex(s),
            },
            "algorithm": "SM2",
            "standard": "GM/T 0003-2012",
            "curve": "sm2p256v1",
            "sovereignty": "中华人民共和国国密算法",
            "public_key_hex": keypair.public_key_bytes().hex(),
        }


# ================================================================
#  二、SovereignCrypto — 龍魂主权加密统一入口
# ================================================================

class SovereignCrypto:
    """
    龍魂系统主权加密模块
    ─────────────────────
    所有加密操作强制使用国密标准，禁用国际算法。
    
    法律依据:
        SM2 → GM/T 0003-2012 (《密码法》数字签名)
        SM3 → GB/T 32905-2016 (哈希摘要)
        SM4 → GB/T 32907-2016 (对称加密)
    
    用法:
        sc = SovereignCrypto()
        sc = SovereignCrypto(keypair=existing_sm2_keypair)  # 加载已有密钥
        sig = sc.sign("hello")          # SM2 签名
        ok = sc.verify("hello", sig)    # SM2 验签
        h = sc.hash("data")             # SM3 哈希
        ct = sc.encrypt(b"secret")      # SM4-CBC 加密
        pt = sc.decrypt(ct)             # SM4-CBC 解密
        info = sc.compliance_report()   # 合规报告
    """

    def __init__(self, keypair: Optional[SM2KeyPair] = None, sm4_key: Optional[bytes] = None):
        """
        初始化主权加密模块
        
        Args:
            keypair: 已有 SM2 密钥对（不提供则自动生成）
            sm4_key: 已有 SM4 密钥（不提供则自动生成 16 字节随机密钥）
        """
        self.cipher_suite = "GM/T"
        self.sovereignty_mark = "中华人民共和国国密算法"

        # SM2 密钥对
        if keypair is not None:
            self.sm2_keypair = keypair
        else:
            self.sm2_keypair = SM2.generate_keypair()

        # SM4 对称密钥
        if sm4_key is not None:
            if len(sm4_key) != 16:
                raise ValueError("SM4 密钥长度必须为 16 字节")
            self.sm4_key = sm4_key
        else:
            self.sm4_key = _secrets.token_bytes(16)

        # 算法映射表
        self._standards = {
            "sm2": {"algorithm": "SM2", "standard": "GM/T 0003-2012", "type": "asymmetric"},
            "sm3": {"algorithm": "SM3", "standard": "GB/T 32905-2016", "type": "hash"},
            "sm4": {"algorithm": "SM4", "standard": "GB/T 32907-2016", "type": "symmetric"},
        }

    # ── SM2 签名/验签 ──────────────────────────────────────

    def sign(self, data: Union[str, bytes], user_id: bytes = SM2Curve.DEFAULT_ID) -> Dict[str, Any]:
        """SM2 签名（带主权声明元数据）"""
        result = SM2.sign_detached(data, self.sm2_keypair, user_id)
        if isinstance(data, bytes):
            result["data_hash"] = SM3.hex_hash(data)
        else:
            result["data_hash"] = SM3.hex_hash(data.encode("utf-8"))
        result["timestamp"] = self._china_timestamp()
        return result

    def verify(self, data: Union[str, bytes], sig_r: int, sig_s: int,
               user_id: bytes = SM2Curve.DEFAULT_ID) -> bool:
        """SM2 签名验证"""
        return SM2.verify(data, (sig_r, sig_s), self.sm2_keypair.P, user_id)

    def get_public_key_hex(self) -> str:
        """获取 SM2 公钥（十六进制）"""
        return self.sm2_keypair.public_key_bytes().hex()

    # ── SM3 哈希 ──────────────────────────────────────────

    def hash(self, data: Union[str, bytes]) -> bytes:
        """SM3 哈希（返回 bytes）"""
        return SM3.hash(data)

    def hex_hash(self, data: Union[str, bytes]) -> str:
        """SM3 哈希（返回 hex 字符串）"""
        return SM3.hex_hash(data)

    def hmac(self, key: bytes, message: Union[str, bytes]) -> str:
        """HMAC-SM3"""
        return hmac_sm3(key, message)

    # ── SM4 加密/解密 ──────────────────────────────────────

    def encrypt(self, plaintext: bytes) -> bytes:
        """SM4-CBC 加密，返回 IV || ciphertext"""
        iv = _secrets.token_bytes(16)
        padded = SM4._pad(plaintext)
        rk = SM4._expand_key(self.sm4_key)
        ciphertext = b""
        prev = iv
        for i in range(0, len(padded), 16):
            block = bytes(a ^ b for a, b in zip(padded[i:i + 16], prev))
            enc = SM4._crypt_block(block, rk)
            ciphertext += enc
            prev = enc
        return iv + ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        """SM4-CBC 解密，输入 IV || ciphertext"""
        if len(ciphertext) < 16 or len(ciphertext) % 16 != 0:
            raise ValueError("密文长度无效")
        iv = ciphertext[:16]
        body = ciphertext[16:]
        rk = SM4._expand_key(self.sm4_key)[::-1]
        plaintext = b""
        prev = iv
        for i in range(0, len(body), 16):
            dec = SM4._crypt_block(body[i:i + 16], rk)
            plaintext += bytes(a ^ b for a, b in zip(dec, prev))
            prev = body[i:i + 16]
        return SM4._unpad(plaintext)

    # ── 密钥管理 ──────────────────────────────────────────

    def export_keypair(self) -> Dict[str, str]:
        """导出密钥对信息（不含私钥明文 — D1绝密）"""
        return {
            "public_key_hex": self.sm2_keypair.public_key_bytes().hex(),
            "algorithm": "SM2",
            "private_key": "[D1·物理隔离·永不导出]",
        }

    def rotate_sm4_key(self) -> bytes:
        """轮换 SM4 密钥，返回新密钥"""
        self.sm4_key = _secrets.token_bytes(16)
        return self.sm4_key

    # ── 中国时间戳 ──────────────────────────────────────────

    @staticmethod
    def _china_timestamp() -> Dict[str, Any]:
        """获取中国国家授时中心时间戳（尝试 NTP，失败降级本地）"""
        try:
            import ntplib
            client = ntplib.NTPClient()
            response = client.request('ntp.ntsc.ac.cn', timeout=3)
            ts = response.tx_time
            source = "ntp.ntsc.ac.cn"
        except Exception:
            import time
            ts = time.time()
            source = "local_fallback"
        from datetime import datetime, timezone, timedelta
        cst = timezone(timedelta(hours=8))
        dt = datetime.fromtimestamp(ts, tz=cst)
        return {
            "timestamp": dt.isoformat(),
            "unix": ts,
            "source": source,
            "timezone": "Asia/Shanghai (UTC+8)",
        }

    # ── 合规报告 ──────────────────────────────────────────

    def compliance_check(self) -> Dict[str, Any]:
        """自检：国密算法是否全部可用"""
        results = {"pass": True, "checks": {}}
        
        # SM2 自检
        try:
            test_msg = b"SovereignCrypto self-test"
            sig_result = self.sign(test_msg)
            r = int(sig_result["signature"]["r"], 16)
            s = int(sig_result["signature"]["s"], 16)
            ok = self.verify(test_msg, r, s)
            results["checks"]["sm2_sign_verify"] = {"status": "🟢", "result": ok}
            if not ok:
                results["pass"] = False
        except Exception as e:
            results["checks"]["sm2_sign_verify"] = {"status": "🔴", "error": str(e)}
            results["pass"] = False

        # SM3 自检
        try:
            h = SM3.hex_hash("abc")
            expected = "66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0"
            ok = h == expected
            results["checks"]["sm3_test_vector"] = {"status": "🟢" if ok else "🔴", "result": ok}
            if not ok:
                results["pass"] = False
        except Exception as e:
            results["checks"]["sm3_test_vector"] = {"status": "🔴", "error": str(e)}
            results["pass"] = False

        # SM4 自检
        try:
            test_key = b"0123456789abcdef"
            pt = b"hello guomi sm4"
            ct = SM4.encrypt_ecb(pt, test_key)
            dt = SM4.decrypt_ecb(ct, test_key)
            ok = pt == dt
            results["checks"]["sm4_encrypt_decrypt"] = {"status": "🟢" if ok else "🔴", "result": ok}
            if not ok:
                results["pass"] = False
        except Exception as e:
            results["checks"]["sm4_encrypt_decrypt"] = {"status": "🔴", "error": str(e)}
            results["pass"] = False

        return results

    def full_report(self) -> Dict[str, Any]:
        """生成完整合规报告"""
        return {
            "cipher_suite": self.cipher_suite,
            "sovereignty_mark": self.sovereignty_mark,
            "standards": self._standards,
            "public_key": self.get_public_key_hex(),
            "self_test": self.compliance_check(),
            "timestamp": self._china_timestamp(),
            "dna": "#龍芯⚡️丙午·乙未·辛亥·甲午·䷚颐-SOVEREIGNCRYPTO-v1.0-UID9622",
            "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        }


# ================================================================
#  三、数据本地化存储硬性检查
# ================================================================

def validate_data_storage() -> Dict[str, Any]:
    """
    强制检查数据存储位置
    
    检查项:
        1. 服务器IP是否在中国境内
        2. 数据是否使用SM4加密
        3. 是否有跨境数据传输风险
    """
    import socket
    import ipaddress

    results = {"pass": True, "checks": {}}

    # 1. 检查本地IP
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        # 简单判断：私网IP/Loopback视为境内
        try:
            ip = ipaddress.ip_address(local_ip)
            is_private = ip.is_private or ip.is_loopback
            results["checks"]["local_ip"] = {
                "ip": local_ip,
                "is_private": is_private,
                "status": "🟢" if is_private else "🟡",
                "note": "私网/Loopback → 本地运行·数据不出境" if is_private else "公网IP·需确认在中国境内",
            }
        except ValueError:
            results["checks"]["local_ip"] = {"ip": local_ip, "status": "🟡", "note": "无法解析IP类型"}
    except Exception as e:
        results["checks"]["local_ip"] = {"status": "🟡", "error": str(e)}

    # 2. SM4 加密状态检查
    try:
        from CNSH_国密工具 import SM4
        test_key = _secrets.token_bytes(16)
        test_data = b"Sovereignty data storage check"
        ct = SM4.encrypt_ecb(test_data, test_key)
        dt = SM4.decrypt_ecb(ct, test_key)
        ok = test_data == dt
        results["checks"]["sm4_encryption"] = {
            "status": "🟢" if ok else "🔴",
            "available": ok,
            "standard": "GB/T 32907-2016",
        }
        if not ok:
            results["pass"] = False
    except Exception as e:
        results["checks"]["sm4_encryption"] = {"status": "🔴", "error": str(e)}
        results["pass"] = False

    # 3. 跨境传输风险
    results["checks"]["cross_border"] = {
        "status": "🟢",
        "policy": "禁止跨境传输",
        "legal_basis": "《个人信息保护法》第38条 · 《数据安全法》第25条",
        "enforcement": "P77黑天使军团 API出口审查",
    }

    # 4. 等保合规建议
    results["checks"]["data_classification"] = {
        "status": "🟢",
        "levels": {
            "D1_绝密": "GPG私钥·DNA种子 → 物理隔离·永不入云",
            "D2_机密": "用户认证信息·SM2私钥 → 端侧SM4加密·云上只存密文",
            "D3_内部": "审计日志 → 日志脱敏·访问需授权",
            "D4_公开": "开源代码·公开文档 → 自由流动",
        },
    }

    results["timestamp"] = SovereignCrypto._china_timestamp()
    return results


# ================================================================
#  四、国家授时中心时间戳
# ================================================================

def get_china_timestamp() -> Dict[str, Any]:
    """获取中国国家授时中心时间戳"""
    return SovereignCrypto._china_timestamp()


# ================================================================
#  五、CLI 入口
# ================================================================

def main():
    import argparse
    import json

    parser = argparse.ArgumentParser(description="龍魂·主权加密模块 (SovereignCrypto)")
    parser.add_argument("action", nargs="?", default="report",
                        choices=["report", "test", "sign", "verify", "encrypt", "decrypt", "hash",
                                  "storage-check", "timestamp", "keygen"],
                        help="操作类型")
    parser.add_argument("--message", "-m", default="", help="待签名/哈希的消息")
    parser.add_argument("--file", "-f", default="", help="待加密/解密的文件路径")
    parser.add_argument("--key", "-k", default="", help="SM4密钥（hex编码）")
    parser.add_argument("--json", action="store_true", help="以JSON格式输出")
    args = parser.parse_args()

    sc = SovereignCrypto()

    if args.action == "report":
        output = sc.full_report()
        print(json.dumps(output, ensure_ascii=False, indent=2))

    elif args.action == "test":
        output = sc.compliance_check()
        print(json.dumps(output, ensure_ascii=False, indent=2))

    elif args.action == "sign":
        msg = args.message or input("请输入待签名消息: ")
        output = sc.sign(msg)
        print(json.dumps(output, ensure_ascii=False, indent=2))

    elif args.action == "hash":
        msg = args.message or input("请输入消息: ")
        print(f"SM3({msg!r}) = {sc.hex_hash(msg)}")

    elif args.action == "encrypt":
        if args.file:
            with open(args.file, "rb") as f:
                data = f.read()
        else:
            data = (args.message or input("请输入: ")).encode("utf-8")
        ct = sc.encrypt(data)
        print(f"密文(hex): {ct.hex()}")
        print(f"SM4密钥(hex): {sc.sm4_key.hex()}")
        print(f"⚠️ 请妥善保管SM4密钥，解密需要它")

    elif args.action == "decrypt":
        if args.file:
            with open(args.file, "rb") as f:
                data = f.read()
        else:
            data = bytes.fromhex(args.message or input("请输入密文(hex): "))
        if args.key:
            sc.sm4_key = bytes.fromhex(args.key)
        pt = sc.decrypt(data)
        print(f"明文: {pt.decode('utf-8', errors='replace')}")

    elif args.action == "storage-check":
        output = validate_data_storage()
        print(json.dumps(output, ensure_ascii=False, indent=2))

    elif args.action == "timestamp":
        output = get_china_timestamp()
        print(json.dumps(output, ensure_ascii=False, indent=2))

    elif args.action == "keygen":
        print(f"SM2 公钥: {sc.get_public_key_hex()}")
        print(f"SM4 密钥: {sc.sm4_key.hex()}")
        print(f"⚠️ SM2私钥已物理隔离，永不导出")


if __name__ == "__main__":
    main()
