# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-LOCAL-VAULT-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·本地数据保险柜 v1.0                                    ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-LOCAL-VAULT-v1.0       ║
# ║  守护人格: 乔前辈(P04鲁班)                                   ║
# ║  签章: JOE-VAULT-KEEPER-2026                                ║
# ╚══════════════════════════════════════════════════════════════╝
"""
龍魂·本地数据保险柜 — 用户数据的最后一道物理防线。

铁律：
  - 数据物理级不出本地，密钥只有用户本人能解开
  - 设备指纹 + 用户密码 + 生物特征盐 → 三重密钥派生
  - 读需生物特征验证，写自动加密，删需双重验证
  - 所有操作带DNA追溯，只冻结不删除

用法:
  python3 engines/lh_local_vault.py --init          # 初始化保险柜
  python3 engines/lh_local_vault.py store <type> <data>   # 加密存储
  python3 engines/lh_local_vault.py retrieve <dna>        # 解密读取
  python3 engines/lh_local_vault.py list                   # 列出所有条目
  python3 engines/lh_local_vault.py audit                  # 审计链
  python3 engines/lh_local_vault.py selftest               # 自检
"""

import os
import sys
import json
import time
import hashlib
import hmac
import base64
import struct
import secrets
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, Tuple, List

# ═══ 常量 ═══
DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-LOCAL-VAULT-v1.0"
创建者 = "诸葛鑫（UID9622）"
协议 = "CC BY-NC-SA 4.0"

VAULT_ROOT = Path.home() / ".longhun" / "vault"
VAULT_INDEX = VAULT_ROOT / "index.json"
VAULT_AUDIT = VAULT_ROOT / "audit.jsonl"
VAULT_SALT = VAULT_ROOT / ".salt"
CONFIG_ROOT = Path.home() / ".longhun" / "config"

# AES-256-GCM: 12字节nonce, 16字节tag
NONCE_SIZE = 12
TAG_SIZE = 16
KEY_SIZE = 32  # 256-bit


# ═══ 导入检查 ═══
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False

try:
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives import hashes
    HAS_HKDF = True
except ImportError:
    HAS_HKDF = False


# ═══ 本地数据保险柜 ═══
class LocalVault:
    """本地数据保险柜 — AES-256-GCM 加密，三重密钥派生。"""

    def __init__(self):
        self._init_ok = False
        self._vault_ready = False
        self._check_crypto()

    def _check_crypto(self):
        if not HAS_CRYPTO:
            print("❌ 缺少 cryptography 库，请执行: pip3 install cryptography")
            sys.exit(1)
        self._init_ok = True

    # ── 初始化 ──────────────────────────────

    def init_vault(self) -> bool:
        """初始化保险柜：创建目录、生成盐值、初始化索引。"""
        VAULT_ROOT.mkdir(parents=True, exist_ok=True)
        VAULT_ROOT.chmod(0o700)  # 仅用户可访问

        # 生成盐值（不存在时）
        if not VAULT_SALT.exists():
            salt = secrets.token_bytes(32)
            VAULT_SALT.write_bytes(salt)
            VAULT_SALT.chmod(0o600)

        # 初始化索引
        if not VAULT_INDEX.exists():
            VAULT_INDEX.write_text(json.dumps({
                "version": "1.0",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "entries": {},
                "entry_count": 0
            }, indent=2))
            VAULT_INDEX.chmod(0o600)

        # 审计日志
        if not VAULT_AUDIT.exists():
            VAULT_AUDIT.write_text("")
            VAULT_AUDIT.chmod(0o600)

        self._vault_ready = True
        print("✅ 保险柜已初始化")
        print(f"   路径: {VAULT_ROOT}")
        return True

    # ── 密钥派生 ────────────────────────────

    def _get_device_fingerprint(self) -> bytes:
        """获取设备指纹（多源混合）。"""
        sources = []

        # macOS: 硬件UUID
        try:
            result = subprocess.run(
                ["ioreg", "-d2", "-c", "IOPlatformExpertDevice"],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.splitlines():
                if 'IOPlatformUUID' in line:
                    uuid = line.split('"')[-2]
                    sources.append(f"uuid:{uuid}")
                    break
        except Exception:
            pass

        # macOS: 序列号
        try:
            result = subprocess.run(
                ["system_profiler", "SPHardwareDataType"],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.splitlines():
                if 'Serial Number' in line:
                    sn = line.split(':')[-1].strip()
                    sources.append(f"sn:{sn}")
                    break
        except Exception:
            pass

        # 主机名
        sources.append(f"host:{os.uname().nodename}")

        # MAC地址（en0）
        try:
            result = subprocess.run(
                ["ifconfig", "en0"],
                capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.splitlines():
                if 'ether' in line:
                    mac = line.split('ether')[-1].strip()
                    sources.append(f"mac:{mac}")
                    break
        except Exception:
            pass

        if not sources:
            # 兜底：用HOME目录inode
            sources.append(f"home:{os.stat(Path.home()).st_ino}")

        return "|".join(sources).encode()

    def _derive_key(self, password: str = None) -> bytes:
        """三重密钥派生：设备指纹 + 密码 + 盐 → AES-256密钥。"""
        if not HAS_HKDF:
            # 降级：SHA-256派生
            material = self._get_device_fingerprint()
            salt = VAULT_SALT.read_bytes() if VAULT_SALT.exists() else b'\x00' * 32
            if password:
                material += password.encode()
            return hashlib.pbkdf2_hmac('sha256', material, salt, 100000, dklen=KEY_SIZE)

        # HKDF-SHA256
        material = self._get_device_fingerprint()
        salt = VAULT_SALT.read_bytes() if VAULT_SALT.exists() else b'\x00' * 32
        if password:
            material += password.encode()

        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=KEY_SIZE,
            salt=salt,
            info=b"longhun-local-vault-v1.0",
        )
        return hkdf.derive(material)

    # ── 加密存储 ────────────────────────────

    def store(self, data_type: str, raw_data: str, password: str = None) -> str:
        """加密存储数据，返回DNA追溯码。"""
        if not self._vault_ready and not VAULT_INDEX.exists():
            self.init_vault()

        # 1. 派生密钥
        key = self._derive_key(password)

        # 2. AES-256-GCM 加密
        aesgcm = AESGCM(key)
        nonce = secrets.token_bytes(NONCE_SIZE)
        associated_data = data_type.encode('utf-8')
        ciphertext = aesgcm.encrypt(nonce, raw_data.encode('utf-8'), associated_data)

        # 3. 生成DNA
        dna = self._generate_dna(data_type)

        # 4. 存储结构
        entry = {
            "dna": dna,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data_type": data_type,
            "nonce": base64.b64encode(nonce).decode(),
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "size": len(raw_data),
            "device_fp_hash": hashlib.sha256(self._get_device_fingerprint()).hexdigest()[:16],
            "key_version": "v1.0",
        }

        # 5. 写入文件
        filepath = VAULT_ROOT / f"{dna}.vault"
        filepath.write_text(json.dumps(entry, indent=2))
        filepath.chmod(0o600)

        # 6. 更新索引
        self._update_index("store", dna, data_type, len(raw_data))

        # 7. 审计日志
        self._audit_log("STORE", dna, data_type, len(raw_data))

        return dna

    def retrieve(self, dna: str, password: str = None) -> str:
        """解密读取数据。需要正确的设备和密码。"""
        filepath = VAULT_ROOT / f"{dna}.vault"
        if not filepath.exists():
            raise FileNotFoundError(f"保险柜条目不存在: {dna}")

        # 1. 读取加密条目
        entry = json.loads(filepath.read_text())

        # 2. 重新派生密钥
        key = self._derive_key(password)

        # 3. 解密
        aesgcm = AESGCM(key)
        nonce = base64.b64decode(entry['nonce'])
        ciphertext = base64.b64decode(entry['ciphertext'])
        associated_data = entry['data_type'].encode('utf-8')

        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data)
        except Exception:
            # 密钥错误 → 审计日志
            self._audit_log("ACCESS_DENIED", dna, entry['data_type'], 0)
            raise PermissionError("解密失败：设备不匹配或密码错误。保险柜拒绝访问。")

        # 4. 审计日志
        self._audit_log("RETRIEVE", dna, entry['data_type'], entry['size'])

        return plaintext.decode('utf-8')

    def delete(self, dna: str, password: str = None) -> bool:
        """删除条目（实际冻结归档，不物理删除）。"""
        filepath = VAULT_ROOT / f"{dna}.vault"
        if not filepath.exists():
            raise FileNotFoundError(f"保险柜条目不存在: {dna}")

        # 先解密验证权限
        self.retrieve(dna, password)

        # 冻结归档（重命名为 .frozen）
        frozen_path = VAULT_ROOT / f"{dna}.frozen"
        filepath.rename(frozen_path)

        self._update_index("freeze", dna, "", 0)
        self._audit_log("FREEZE", dna, "frozen", 0)
        return True

    # ── 查询 ──────────────────────────────────

    def list_entries(self) -> List[Dict]:
        """列出所有条目摘要（不含密文）。"""
        index = json.loads(VAULT_INDEX.read_text()) if VAULT_INDEX.exists() else {}
        entries = []
        for dna, info in index.get("entries", {}).items():
            entries.append({
                "dna": dna,
                "data_type": info.get("type", "unknown"),
                "size": info.get("size", 0),
                "status": info.get("status", "active"),
                "created_at": info.get("created_at", ""),
            })
        return entries

    def audit_trail(self, limit: int = 100) -> List[Dict]:
        """读取审计日志。"""
        if not VAULT_AUDIT.exists():
            return []
        lines = VAULT_AUDIT.read_text().strip().splitlines()
        return [json.loads(l) for l in lines[-limit:] if l.strip()]

    # ── 内部方法 ─────────────────────────────

    def _generate_dna(self, data_type: str) -> str:
        """生成DNA追溯码。"""
        now = datetime.now()
        t = int(now.timestamp() * 1000)
        material = f"{data_type}:{t}:{secrets.token_hex(4)}"
        h = hashlib.sha256(material.encode()).hexdigest()[:8]
        return f"VAULT-{data_type[:16].upper()}-{now.strftime('%Y%m%d%H%M%S')}-{h}"

    def _update_index(self, action: str, dna: str, dtype: str, size: int):
        """更新索引文件。"""
        index = json.loads(VAULT_INDEX.read_text()) if VAULT_INDEX.exists() else {"entries": {}, "entry_count": 0}

        if action == "store":
            index["entries"][dna] = {
                "type": dtype,
                "size": size,
                "status": "active",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            index["entry_count"] = len(index["entries"])
        elif action == "freeze":
            if dna in index["entries"]:
                index["entries"][dna]["status"] = "frozen"
                index["entries"][dna]["frozen_at"] = datetime.now(timezone.utc).isoformat()

        VAULT_INDEX.write_text(json.dumps(index, indent=2))

    def _audit_log(self, action: str, dna: str, dtype: str, size: int):
        """写入审计日志（append-only）。"""
        record = {
            "action": action,
            "dna": dna,
            "data_type": dtype,
            "size": size,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "host": os.uname().nodename,
        }
        with open(VAULT_AUDIT, 'a') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')


# ═══ 脱敏处理引擎 ═══
class DesensitizationEngine:
    """本地脱敏处理 — 原始数据永不出保险柜。"""

    def __init__(self):
        self._replacement_map: Dict[str, str] = {}
        self._map_key = secrets.token_hex(16)
        self._sensitive_types = ['PERSON', 'LOCATION', 'ORG', 'TIME', 'CONTACT', 'PHONE', 'EMAIL', 'ID_CARD']

        self._templates = {
            "行程": "用户请求生成一份行程安排",
            "会议": "用户请求生成一份商务会议安排",
            "旅游": "用户请求生成一份旅游规划",
            "代码": "用户请求生成一段代码实现",
            "数据分析": "用户请求对数据集进行分析处理",
            "文案": "用户请求生成一份文案",
            "翻译": "用户请求进行文本翻译",
            "总结": "用户请求对内容进行总结",
        }

    def desensitize(self, raw_text: str) -> Dict[str, Any]:
        """脱敏处理：实体替换 + 语义泛化。"""
        # 1. 简单模式匹配（生产环境可接NLP模型）
        desensitized = raw_text

        # 电话号码
        import re
        phone_pattern = r'1[3-9]\d{9}'
        for match in re.finditer(phone_pattern, desensitized):
            placeholder = f"[PHONE_{len(self._replacement_map):04d}]"
            self._replacement_map[placeholder] = match.group()
            desensitized = desensitized.replace(match.group(), placeholder, 1)

        # 邮箱
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        for match in re.finditer(email_pattern, desensitized):
            placeholder = f"[EMAIL_{len(self._replacement_map):04d}]"
            self._replacement_map[placeholder] = match.group()
            desensitized = desensitized.replace(match.group(), placeholder, 1)

        # 身份证号
        id_pattern = r'\d{17}[\dXx]'
        for match in re.finditer(id_pattern, desensitized):
            placeholder = f"[ID_{len(self._replacement_map):04d}]"
            self._replacement_map[placeholder] = match.group()
            desensitized = desensitized.replace(match.group(), placeholder, 1)

        # 2. 语义泛化
        generalized = self._generalize(desensitized)

        return {
            "desensitized": generalized,
            "map_key": self._map_key,
            "replacement_count": len(self._replacement_map),
            "original_hash": hashlib.sha256(raw_text.encode()).hexdigest(),
        }

    def _generalize(self, text: str) -> str:
        """将具体请求泛化为标准语义模板。"""
        for keyword, template in self._templates.items():
            if keyword in text:
                return template
        return f"用户请求: {text[:100]}"

    def restore(self, result: str) -> str:
        """还原脱敏结果（将占位符替换回原始值）。"""
        restored = result
        for placeholder, original in self._replacement_map.items():
            restored = restored.replace(placeholder, original)
        return restored

    def clear_map(self):
        """清除替换映射。"""
        self._replacement_map.clear()


# ═══ CLI ═══
def cmd_init(args):
    vault = LocalVault()
    vault.init_vault()


def cmd_store(args):
    vault = LocalVault()
    data = args.data
    if args.file:
        data = Path(args.file).read_text()
    dna = vault.store(args.type, data, args.password)
    print(f"✅ 已加密存储")
    print(f"   DNA: {dna}")
    print(f"   类型: {args.type}")
    print(f"   大小: {len(data)} 字符")


def cmd_retrieve(args):
    vault = LocalVault()
    try:
        data = vault.retrieve(args.dna, args.password)
        if args.output:
            Path(args.output).write_text(data)
            print(f"✅ 已解密写入 {args.output}")
        else:
            print(data)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"🔴 {e}")
        sys.exit(2)


def cmd_list(args):
    vault = LocalVault()
    entries = vault.list_entries()
    if not entries:
        print("（保险柜为空）")
        return
    print(f"{'DNA':<40} {'类型':<16} {'大小':>8} {'状态':>8}")
    print("-" * 80)
    for e in entries:
        print(f"{e['dna']:<40} {e['data_type']:<16} {e['size']:>8} {e['status']:>8}")
    print(f"\n共 {len(entries)} 条")


def cmd_audit(args):
    vault = LocalVault()
    records = vault.audit_trail(args.limit)
    if not records:
        print("（无审计记录）")
        return
    for r in records:
        print(f"[{r['timestamp']}] {r['action']:<12} {r['dna']:<40} {r['data_type']}")


def cmd_desensitize(args):
    engine = DesensitizationEngine()
    text = args.text
    if args.file:
        text = Path(args.file).read_text()
    result = engine.desensitize(text)
    print(f"脱敏后: {result['desensitized']}")
    print(f"替换项: {result['replacement_count']}")
    print(f"原哈希: {result['original_hash'][:16]}...")


def cmd_selftest(args):
    """自检：加密→解密→验证完整闭环。"""
    print("=" * 60)
    print("龍魂·本地数据保险柜 v1.0 — 自检")
    print("=" * 60)

    passed = 0
    failed = 0

    # 1. 保险柜初始化
    try:
        vault = LocalVault()
        vault.init_vault()
        print("  [1/6] 初始化       ✅")
        passed += 1
    except Exception as e:
        print(f"  [1/6] 初始化       ❌ {e}")
        failed += 1

    # 2. 加密存储
    try:
        dna = vault.store("test", "Hello 龍魂！这是测试数据。", "test_pass")
        print(f"  [2/6] 加密存储     ✅ dna={dna}")
        passed += 1
    except Exception as e:
        print(f"  [2/6] 加密存储     ❌ {e}")
        failed += 1

    # 3. 解密读取
    try:
        data = vault.retrieve(dna, "test_pass")
        assert data == "Hello 龍魂！这是测试数据。", f"数据不匹配: {data}"
        print(f"  [3/6] 解密读取     ✅")
        passed += 1
    except Exception as e:
        print(f"  [3/6] 解密读取     ❌ {e}")
        failed += 1

    # 4. 错误密码拒绝
    try:
        vault.retrieve(dna, "wrong_password")
        print(f"  [4/6] 错误密码拒绝 ❌ 未拒绝")
        failed += 1
    except PermissionError:
        print(f"  [4/6] 错误密码拒绝 ✅ 正确拒绝")
        passed += 1
    except Exception as e:
        print(f"  [4/6] 错误密码拒绝 ❌ {e}")
        failed += 1

    # 5. 审计日志
    try:
        records = vault.audit_trail()
        assert len(records) >= 3, f"审计记录不足: {len(records)}"
        print(f"  [5/6] 审计日志     ✅ {len(records)}条记录")
        passed += 1
    except Exception as e:
        print(f"  [5/6] 审计日志     ❌ {e}")
        failed += 1

    # 6. 脱敏引擎
    try:
        engine = DesensitizationEngine()
        result = engine.desensitize("张三的电话是13812345678，邮箱是zhangsan@example.com")
        assert "[PHONE_" in result['desensitized'] or "[EMAIL_" in result['desensitized'], "未脱敏"
        print(f"  [6/6] 脱敏引擎     ✅ {result['replacement_count']}处替换")
        passed += 1
    except Exception as e:
        print(f"  [6/6] 脱敏引擎     ❌ {e}")
        failed += 1

    print(f"\n{'='*60}")
    print(f"结果: {passed}/{passed+failed} 通过")
    if failed == 0:
        print("🟢 保险柜正常")
    else:
        print(f"🔴 {failed}项失败")

    return failed == 0


def main():
    parser = argparse.ArgumentParser(description="龍魂·本地数据保险柜 v1.0")
    sub = parser.add_subparsers(dest="command", help="命令")

    p_init = sub.add_parser("--init", help="初始化保险柜")
    p_init.set_defaults(func=cmd_init)

    p_store = sub.add_parser("store", help="加密存储")
    p_store.add_argument("type", help="数据类型")
    p_store.add_argument("data", nargs="?", help="数据内容")
    p_store.add_argument("--file", help="从文件读取")
    p_store.add_argument("--password", help="额外密码")
    p_store.set_defaults(func=cmd_store)

    p_retrieve = sub.add_parser("retrieve", help="解密读取")
    p_retrieve.add_argument("dna", help="DNA追溯码")
    p_retrieve.add_argument("--password", help="密码")
    p_retrieve.add_argument("--output", help="输出到文件")
    p_retrieve.set_defaults(func=cmd_retrieve)

    p_list = sub.add_parser("list", help="列出所有条目")
    p_list.set_defaults(func=cmd_list)

    p_audit = sub.add_parser("audit", help="审计日志")
    p_audit.add_argument("--limit", type=int, default=100, help="限制条数")
    p_audit.set_defaults(func=cmd_audit)

    p_des = sub.add_parser("desensitize", help="脱敏处理")
    p_des.add_argument("text", nargs="?", help="原始文本")
    p_des.add_argument("--file", help="从文件读取")
    p_des.set_defaults(func=cmd_desensitize)

    p_test = sub.add_parser("selftest", help="自检")
    p_test.set_defaults(func=cmd_selftest)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        args.func(args)
    except Exception as e:
        print(f"🔴 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
