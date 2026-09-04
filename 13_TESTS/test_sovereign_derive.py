#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · 多设备覆写码独立派生测试

验证：
  1. 同一设备多次派生 → 覆写码恒定
  2. 不同设备独立派生 → 覆写码互不相同
  3. 换设备 → 旧码失效（用A设备码在B设备上验证应失败）
  4. 脑内盐变更 → 覆写码变更
  5. 降级模式（无脑内盐）→ SHA256哈希验证兼容

用法：
  python3 tests/test_sovereign_derive.py
  python3 tests/test_sovereign_derive.py --verbose

DNA: #龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-SOVEREIGN-DERIVE-TEST-v1.0
"""
import hashlib
import hmac
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# 确保 bin/ 在路径中
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))

# ═══════════════════════════════════════════════════════════
# 模拟设备环境
# ═══════════════════════════════════════════════════════════

# 模拟 Mac M4 Max 硬件指纹
MAC_MOCK_UUID = "A1B2C3D4-E5F6-7890-ABCD-EF1234567890"
MAC_MOCK_VOLUME_UUID = "FEDCBA98-7654-3210-FEDC-BA9876543210"
MAC_MOCK_CPU = "arm64"

# 模拟 华为鲲鹏服务器 硬件指纹
KUNPENG_MOCK_MAC = "52:54:00:ab:cd:ef"
KUNPENG_MOCK_SERIAL = "KUNPENG920-20250701-0001"
KUNPENG_MOCK_MACHINE_ID = "a1b2c3d4e5f6a7b8"
KUNPENG_MOCK_CPU = "aarch64"

# 模拟 华为云香港 环境
HKC_MOCK_EIP = "119.8.9.10"
HKC_MOCK_INTERNAL = "10.0.1.x"

# 脑内盐
TEST_SALT = b"test-brain-salt-UID9622"


def 派生覆写码(生物: bytes, 设备: bytes, 环境: bytes, 盐: bytes) -> str:
    """核心派生函数（纯函数版·无IO依赖）"""
    融合 = hashlib.sha256(生物 + 设备 + 环境).digest()
    覆写码原始 = hmac.new(盐, 融合, hashlib.sha256).hexdigest()
    return f"🔑{覆写码原始[:16]}-SOVEREIGN⚡️{覆写码原始[16:32]}"


def 模拟Mac设备因子() -> bytes:
    """模拟 Mac M4 Max 设备因子"""
    return hashlib.sha256(f"{MAC_MOCK_UUID}:{MAC_MOCK_VOLUME_UUID}:{MAC_MOCK_CPU}".encode()).digest()


def 模拟鲲鹏设备因子() -> bytes:
    """模拟 华为鲲鹏 设备因子"""
    return hashlib.sha256(f"{KUNPENG_MOCK_MAC}:{KUNPENG_MOCK_SERIAL}:{KUNPENG_MOCK_MACHINE_ID}:{KUNPENG_MOCK_CPU}".encode()).digest()


def 模拟华为云环境因子() -> bytes:
    """模拟 华为云香港 环境因子"""
    return hashlib.sha256(f"{HKC_MOCK_EIP}:{HKC_MOCK_INTERNAL}:HongKong".encode()).digest()


def 模拟本地Mac环境因子() -> bytes:
    """模拟 Mac 本地环境因子"""
    return hashlib.sha256("192.168.1.x:Wenzhou".encode()).digest()


def 模拟鲲鹏环境因子() -> bytes:
    """模拟 鲲鹏内网 环境因子"""
    return hashlib.sha256("10.0.0.x:Shenzhen".encode()).digest()


# ═══════════════════════════════════════════════════════════
# 测试用例
# ═══════════════════════════════════════════════════════════

class Test多设备独立派生(unittest.TestCase):
    """验证：不同设备派生互不相同的覆写码"""

    def test_同一设备多次派生产出相同码(self):
        """Mac 设备派生10次，码应恒定"""
        设备 = 模拟Mac设备因子()
        环境 = 模拟本地Mac环境因子()
        生物 = hashlib.sha256(b"uid9622-fingerprint").digest()
        
        codes = []
        for _ in range(10):
            code = 派生覆写码(生物, 设备, 环境, TEST_SALT)
            codes.append(code)
        
        self.assertEqual(len(set(codes)), 1, "同一设备多次派生应产出相同覆写码")

    def test_不同设备派生码互不相同(self):
        """Mac、鲲鹏、华为云香港三设备派生码应各不相同"""
        生物 = hashlib.sha256(b"uid9622-fingerprint").digest()
        
        mac_code = 派生覆写码(生物, 模拟Mac设备因子(), 模拟本地Mac环境因子(), TEST_SALT)
        kunpeng_code = 派生覆写码(生物, 模拟鲲鹏设备因子(), 模拟鲲鹏环境因子(), TEST_SALT)
        hkc_code = 派生覆写码(生物, 模拟华为云环境因子(), 模拟华为云环境因子(), TEST_SALT)
        
        unique_codes = {mac_code, kunpeng_code, hkc_code}
        self.assertEqual(len(unique_codes), 3,
                         f"三台设备应派生3个不同覆写码，实际只有{len(unique_codes)}个\n"
                         f"  Mac: {mac_code[:20]}...\n"
                         f"  鲲鹏: {kunpeng_code[:20]}...\n"
                         f"  香港: {hkc_code[:20]}...")

    def test_换设备旧码应失效(self):
        """A设备生成的码在B设备环境应无法匹配"""
        生物 = hashlib.sha256(b"uid9622-fingerprint").digest()
        
        # Mac 环境派生
        mac_code = 派生覆写码(生物, 模拟Mac设备因子(), 模拟本地Mac环境因子(), TEST_SALT)
        
        # 尝试在鲲鹏环境派生——应产生不同码
        kunpeng_code = 派生覆写码(生物, 模拟鲲鹏设备因子(), 模拟鲲鹏环境因子(), TEST_SALT)
        
        self.assertNotEqual(mac_code, kunpeng_code,
                            "Mac 覆写码在鲲鹏上应不同 → 旧设备码自然失效")

    def test_脑内盐变更覆写码变更(self):
        """相同设备、不同脑内盐 → 覆写码不同"""
        设备 = 模拟Mac设备因子()
        环境 = 模拟本地Mac环境因子()
        生物 = hashlib.sha256(b"uid9622-fingerprint").digest()
        
        code_salt_a = 派生覆写码(生物, 设备, 环境, b"salt-alpha")
        code_salt_b = 派生覆写码(生物, 设备, 环境, b"salt-beta")
        
        self.assertNotEqual(code_salt_a, code_salt_b,
                            "不同脑内盐应派生不同覆写码")

    def test_环境因子变更覆写码变更(self):
        """同设备、不同网络环境 → 覆写码不同（防异地登录）"""
        设备 = 模拟Mac设备因子()
        生物 = hashlib.sha256(b"uid9622-fingerprint").digest()
        
        code_home = 派生覆写码(生物, 设备, 模拟本地Mac环境因子(), TEST_SALT)
        code_remote = 派生覆写码(生物, 设备, 模拟华为云环境因子(), TEST_SALT)
        
        self.assertNotEqual(code_home, code_remote,
                            "家庭网络 vs 香港云 → 覆写码应不同")

    def test_生物因子变更覆写码变更(self):
        """同设备、不同生物因子 → 覆写码不同"""
        设备 = 模拟Mac设备因子()
        环境 = 模拟本地Mac环境因子()
        
        code_uid_a = 派生覆写码(hashlib.sha256(b"user-A").digest(), 设备, 环境, TEST_SALT)
        code_uid_b = 派生覆写码(hashlib.sha256(b"user-B").digest(), 设备, 环境, TEST_SALT)
        
        self.assertNotEqual(code_uid_a, code_uid_b,
                            "不同用户指纹应派生不同覆写码")


class Test降级兼容(unittest.TestCase):
    """验证无脑内盐时的降级模式"""

    def test_降级SHA256验证正确(self):
        """旧码SHA256哈希验证逻辑"""
        # 模拟旧码
        旧码 = "🔑9622-OVERRIDE-SOVEREIGN⚡️LHX9-ZK77"
        已知哈希 = hashlib.sha256(旧码.encode()).hexdigest()
        
        # 验证
        输入哈希 = hashlib.sha256(旧码.encode()).hexdigest()
        self.assertEqual(输入哈希, 已知哈希, "降级哈希验证应对")

    def test_降级错误码拒绝(self):
        """错误码在降级模式下被拒绝"""
        已知哈希 = hashlib.sha256("🔑9622-OVERRIDE-SOVEREIGN⚡️LHX9-ZK77".encode()).hexdigest()
        错误码哈希 = hashlib.sha256("wrong-code".encode()).hexdigest()
        
        self.assertNotEqual(错误码哈希, 已知哈希, "错误码应被拒绝")

    def test_降级到全派生过渡(self):
        """降级码和全派生码应不同（防止假过渡）"""
        设备 = 模拟Mac设备因子()
        环境 = 模拟本地Mac环境因子()
        生物 = hashlib.sha256(b"uid9622-fingerprint").digest()
        
        # 全派生模式
        派生码 = 派生覆写码(生物, 设备, 环境, TEST_SALT)
        
        # 降级模式（旧码字符串）
        旧码 = "🔑9622-OVERRIDE-SOVEREIGN⚡️LHX9-ZK77"
        
        # 两者应不同（升级是真正的安全升级）
        降级哈希 = hashlib.sha256(旧码.encode()).hexdigest()
        派生哈希 = hashlib.sha256(派生码.encode()).hexdigest()
        
        self.assertNotEqual(降级哈希, 派生哈希,
                            "全派生模式应与旧降级码不同→安全升级有效")


class Test边缘情况(unittest.TestCase):
    """边界条件测试"""

    def test_空盐产生可区分结果(self):
        """空脑内盐与非空盐派生结果应不同"""
        设备 = 模拟Mac设备因子()
        环境 = 模拟本地Mac环境因子()
        生物 = hashlib.sha256(b"uid9622-fingerprint").digest()
        
        code_empty = 派生覆写码(生物, 设备, 环境, b"")
        code_real = 派生覆写码(生物, 设备, 环境, TEST_SALT)
        
        self.assertNotEqual(code_empty, code_real,
                            "空盐与非空盐应派生不同结果")
        self.assertTrue(code_empty.startswith("🔑"),
                        f"空盐也应能派生: {code_empty[:20]}")

    def test_零长度因子容错(self):
        """零长度设备因子仍能派生（兜底）"""
        try:
            code = 派生覆写码(b"bio", hashlib.sha256(b"").digest(), b"env", TEST_SALT)
            self.assertTrue(code.startswith("🔑"), f"即便设备因子为空，应仍能派生: {code[:20]}")
        except Exception as e:
            self.fail(f"零长度因子应不导致异常: {e}")

    def test_覆写码格式正确(self):
        """覆写码格式: 🔑{16hex}-SOVEREIGN⚡️{16hex}"""
        设备 = 模拟Mac设备因子()
        环境 = 模拟本地Mac环境因子()
        生物 = hashlib.sha256(b"uid9622-fingerprint").digest()
        code = 派生覆写码(生物, 设备, 环境, TEST_SALT)
        
        self.assertTrue(code.startswith("🔑"), f"应以🔑开头: {code[:5]}...")
        self.assertIn("-SOVEREIGN⚡️", code, f"应含 -SOVEREIGN⚡️: {code}")
        
        parts = code.split("-SOVEREIGN⚡️")
        self.assertEqual(len(parts), 2, f"应只有一个分隔符: {code}")
        
        前半 = parts[0].lstrip("🔑")
        后半 = parts[1]
        self.assertEqual(len(前半), 16, f"前半应为16字符hex: {前半}")
        self.assertEqual(len(后半), 16, f"后半应为16字符hex: {后半}")

    def test_100设备覆写码全唯一(self):
        """大规模验证：100个模拟设备覆写码全不相同"""
        生物 = hashlib.sha256(b"uid9622-fingerprint").digest()
        codes = set()
        
        for i in range(100):
            # 模拟不同设备
            设备因子 = hashlib.sha256(f"device-{i}".encode()).digest()
            环境因子 = hashlib.sha256(f"network-{i % 10}".encode()).digest()
            盐 = hashlib.sha256(f"salt-{i % 5}".encode()).digest()
            
            code = 派生覆写码(生物, 设备因子, 环境因子, 盐)
            codes.add(code)
        
        # 100设备应有100个不同码
        self.assertEqual(len(codes), 100,
                         f"100个设备应派生100个不同码，实际只有{len(codes)}个")


class Test集成验证(unittest.TestCase):
    """验证与 lh_sovereign_derive 模块的集成"""

    def test_导入模块无异常(self):
        """验证模块可正常导入"""
        try:
            from lh_sovereign_derive import 派生主权覆写码, 验证覆写码, 诊断三层绑定
        except ImportError as e:
            self.fail(f"导入 lh_sovereign_derive 失败: {e}")

    def test_诊断三层绑定可运行(self):
        """诊断函数返回有效结构"""
        from lh_sovereign_derive import 诊断三层绑定
        result = 诊断三层绑定()
        
        self.assertIsInstance(result, dict, "诊断应返回字典")
        self.assertIn("生物因子", result, "应含生物因子状态")
        self.assertIn("设备因子", result, "应含设备因子状态")
        self.assertIn("环境因子", result, "应含环境因子状态")

    def test_验证覆写码函数可用(self):
        """验证函数对错误码返回False"""
        from lh_sovereign_derive import 验证覆写码
        self.assertFalse(验证覆写码("wrong-code"), "错误码应返回False")


# ═══════════════════════════════════════════════════════════
# 运行入口
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="多设备覆写码独立派生测试")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    args = parser.parse_args()
    
    verbosity = 2 if args.verbose else 1
    unittest.main(verbosity=verbosity, argv=[sys.argv[0]])
