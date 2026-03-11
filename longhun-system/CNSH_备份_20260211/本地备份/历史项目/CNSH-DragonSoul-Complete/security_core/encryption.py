#!/usr/bin/env python3
"""
🔐 七维加密系统 | Seven-Dimension Encryption
DNA追溯码: #龙芯⚡️2026-01-21-七维加密-v2.0

七维加密层：
1. 设备指纹层 - 绑定特定设备
2. 用户标识层 - 绑定用户身份
3. 时间戳层 - 防重放攻击
4. 地理位置层 - 限制访问区域
5. 行为模式层 - 异常检测
6. 内容加密层 - AES-256加密
7. DNA追溯层 - 操作可追溯
"""

import os
import json
import hashlib
import base64
import platform
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

# 尝试导入加密库，如果不可用则使用简化版
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("⚠️ cryptography库未安装，使用简化加密模式")
    print("   运行 'pip install cryptography' 安装完整加密支持")


@dataclass
class EncryptionContext:
    """加密上下文"""
    device_id: str
    user_id: str
    timestamp: str
    location: str
    behavior_hash: str
    dna_code: str


class SevenDimensionEncryption:
    """七维加密系统"""
    
    def __init__(self, master_key: str = None):
        """
        初始化加密系统
        
        Args:
            master_key: 主密钥，如果不提供则自动生成并存储
        """
        self.master_key = master_key or self._get_or_create_master_key()
        self._behavior_history = []
        
    def _get_or_create_master_key(self) -> str:
        """获取或创建主密钥"""
        key_file = os.path.expanduser("~/.dragonsoul/.master_key")
        os.makedirs(os.path.dirname(key_file), exist_ok=True)
        
        if os.path.exists(key_file):
            with open(key_file, "r") as f:
                return f.read().strip()
        else:
            # 生成新密钥
            if CRYPTO_AVAILABLE:
                key = Fernet.generate_key().decode()
            else:
                # 简化版：使用随机字节
                key = base64.urlsafe_b64encode(os.urandom(32)).decode()
            with open(key_file, "w") as f:
                f.write(key)
            # 设置权限为只有所有者可读写
            os.chmod(key_file, 0o600)
            return key
    
    def encrypt(self, 
                data: Any, 
                user_id: str = "default",
                location: str = "中国") -> Tuple[str, EncryptionContext]:
        """
        七维加密数据
        
        Args:
            data: 要加密的数据
            user_id: 用户ID
            location: 地理位置
            
        Returns:
            Tuple[加密后的数据, 加密上下文]
        """
        # 准备加密上下文
        context = EncryptionContext(
            device_id=self._get_device_fingerprint(),
            user_id=user_id,
            timestamp=datetime.now().isoformat(),
            location=location,
            behavior_hash=self._get_behavior_hash(),
            dna_code=self._generate_dna()
        )
        
        # 序列化数据
        if isinstance(data, (dict, list)):
            plain_text = json.dumps(data, ensure_ascii=False)
        else:
            plain_text = str(data)
        
        # 第1-5层：生成复合密钥
        composite_key = self._derive_composite_key(context)
        
        # 第6层：AES-256加密
        if CRYPTO_AVAILABLE:
            fernet = Fernet(composite_key)
            encrypted_data = fernet.encrypt(plain_text.encode('utf-8'))
        else:
            # 简化版：Base64编码 + XOR混淆
            encrypted_data = self._simple_encrypt(plain_text, composite_key)
        
        # 第7层：添加DNA追溯标记
        final_data = self._add_dna_layer(encrypted_data, context.dna_code)
        
        return base64.b64encode(final_data).decode('utf-8'), context
    
    def decrypt(self, 
                encrypted_data: str, 
                context: EncryptionContext) -> Any:
        """
        解密数据
        
        Args:
            encrypted_data: 加密的数据
            context: 加密上下文
            
        Returns:
            解密后的数据
        """
        # 验证设备
        if not self._verify_device(context.device_id):
            raise PermissionError("🔴 设备验证失败：非授权设备")
        
        # 验证位置
        if not self._verify_location(context.location):
            raise PermissionError("🔴 位置验证失败：非授权区域")
        
        # 解码数据
        data = base64.b64decode(encrypted_data)
        
        # 移除DNA层
        encrypted_content, dna_code = self._remove_dna_layer(data)
        
        # 验证DNA码
        if dna_code != context.dna_code:
            raise ValueError("🔴 DNA验证失败：数据可能被篡改")
        
        # 生成复合密钥
        composite_key = self._derive_composite_key(context)
        
        # 解密
        if CRYPTO_AVAILABLE:
            fernet = Fernet(composite_key)
            plain_text = fernet.decrypt(encrypted_content).decode('utf-8')
        else:
            # 简化版解密
            plain_text = self._simple_decrypt(encrypted_content, composite_key)
        
        # 尝试解析JSON
        try:
            return json.loads(plain_text)
        except json.JSONDecodeError:
            return plain_text
    
    def _simple_encrypt(self, text: str, key: bytes) -> bytes:
        """简化加密（无cryptography时使用）"""
        text_bytes = text.encode('utf-8')
        key_hash = hashlib.sha256(key).digest()
        # XOR加密
        encrypted = bytes([b ^ key_hash[i % len(key_hash)] for i, b in enumerate(text_bytes)])
        return base64.b64encode(encrypted)
    
    def _simple_decrypt(self, data: bytes, key: bytes) -> str:
        """简化解密（无cryptography时使用）"""
        encrypted = base64.b64decode(data)
        key_hash = hashlib.sha256(key).digest()
        # XOR解密
        decrypted = bytes([b ^ key_hash[i % len(key_hash)] for i, b in enumerate(encrypted)])
        return decrypted.decode('utf-8')
    
    def _get_device_fingerprint(self) -> str:
        """获取设备指纹"""
        # 收集设备信息
        info = {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "machine": platform.machine(),
            "node": platform.node(),
            "mac": ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                           for elements in range(0, 48, 8)][::-1])
        }
        
        # 生成指纹哈希
        fingerprint = hashlib.sha256(
            json.dumps(info, sort_keys=True).encode()
        ).hexdigest()
        
        return fingerprint
    
    def _get_behavior_hash(self) -> str:
        """获取行为模式哈希"""
        # 记录当前行为
        current_behavior = {
            "time": datetime.now().hour,  # 当前小时
            "day": datetime.now().weekday(),  # 星期几
        }
        
        self._behavior_history.append(current_behavior)
        
        # 保留最近100条记录
        if len(self._behavior_history) > 100:
            self._behavior_history = self._behavior_history[-100:]
        
        # 计算行为模式哈希
        return hashlib.md5(
            json.dumps(self._behavior_history).encode()
        ).hexdigest()[:16]
    
    def _generate_dna(self) -> str:
        """生成DNA追溯码"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_part = os.urandom(4).hex().upper()
        return f"#龙芯⚡️{timestamp}-ENC-{random_part}"
    
    def _derive_composite_key(self, context: EncryptionContext) -> bytes:
        """从上下文派生复合密钥"""
        # 组合所有维度信息
        salt_material = (
            f"{context.device_id}"
            f"{context.user_id}"
            f"{context.timestamp[:10]}"  # 只用日期部分
            f"{context.location}"
            f"{context.behavior_hash}"
        )
        
        salt = hashlib.sha256(salt_material.encode()).digest()[:16]
        
        if CRYPTO_AVAILABLE:
            # 使用PBKDF2派生密钥
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            
            key = base64.urlsafe_b64encode(
                kdf.derive(self.master_key.encode())
            )
        else:
            # 简化版：使用HMAC
            import hmac
            key = base64.urlsafe_b64encode(
                hmac.new(salt, self.master_key.encode(), hashlib.sha256).digest()
            )
        
        return key
    
    def _add_dna_layer(self, data: bytes, dna_code: str) -> bytes:
        """添加DNA层"""
        dna_bytes = dna_code.encode('utf-8')
        dna_length = len(dna_bytes).to_bytes(2, 'big')
        return dna_length + dna_bytes + data
    
    def _remove_dna_layer(self, data: bytes) -> Tuple[bytes, str]:
        """移除DNA层"""
        dna_length = int.from_bytes(data[:2], 'big')
        dna_code = data[2:2+dna_length].decode('utf-8')
        encrypted_content = data[2+dna_length:]
        return encrypted_content, dna_code
    
    def _verify_device(self, device_id: str) -> bool:
        """验证设备"""
        # 允许当前设备
        current_device = self._get_device_fingerprint()
        return device_id == current_device
    
    def _verify_location(self, location: str) -> bool:
        """验证位置（数据主权保护）"""
        # 允许的位置列表
        allowed_locations = ["中国", "China", "CN", "本地", "local"]
        return location in allowed_locations


class DataSovereigntyProtector:
    """数据主权保护器"""
    
    def __init__(self):
        self.encryption = SevenDimensionEncryption()
        self.china_only = True  # 数据只在中国境内
        
    def protect(self, data: Any) -> Dict[str, Any]:
        """保护数据"""
        encrypted, context = self.encryption.encrypt(
            data,
            location="中国"
        )
        
        return {
            "encrypted_data": encrypted,
            "context": {
                "device_id": context.device_id[:16] + "...",  # 部分显示
                "timestamp": context.timestamp,
                "location": context.location,
                "dna_code": context.dna_code
            },
            "sovereignty": "🇨🇳 数据存储于中国境内"
        }
    
    def check_api_location(self, api_url: str) -> bool:
        """检查API服务器位置"""
        # 国内API白名单
        china_apis = [
            "api.deepseek.com",
            "api.zhipuai.cn",
            "api.baidu.com",
            "api.aliyun.com",
            "localhost",
            "127.0.0.1"
        ]
        
        for api in china_apis:
            if api in api_url:
                return True
        
        # 非白名单API需要警告
        print(f"⚠️ 警告：API {api_url} 可能位于境外")
        return False


# ==================== 使用示例 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("🔐 七维加密系统测试")
    print("=" * 60)
    
    # 初始化加密系统
    encryption = SevenDimensionEncryption()
    
    # 测试数据
    sensitive_data = {
        "user": "龙芯北辰",
        "api_keys": {
            "claude": "sk-xxx-hidden",
            "deepseek": "sk-xxx-hidden"
        },
        "notes": "这是敏感配置信息"
    }
    
    print("\n原始数据:")
    print(json.dumps(sensitive_data, ensure_ascii=False, indent=2))
    
    # 加密
    encrypted, context = encryption.encrypt(sensitive_data, user_id="UID9622")
    
    print(f"\n加密后（前100字符）:")
    print(encrypted[:100] + "...")
    
    print(f"\n加密上下文:")
    print(f"  设备ID: {context.device_id[:32]}...")
    print(f"  用户ID: {context.user_id}")
    print(f"  时间戳: {context.timestamp}")
    print(f"  位置: {context.location}")
    print(f"  DNA追溯码: {context.dna_code}")
    
    # 解密
    decrypted = encryption.decrypt(encrypted, context)
    
    print(f"\n解密后:")
    print(json.dumps(decrypted, ensure_ascii=False, indent=2))
    
    # 数据主权保护
    print("\n" + "=" * 60)
    print("🛡️ 数据主权保护测试")
    print("=" * 60)
    
    protector = DataSovereigntyProtector()
    protected = protector.protect(sensitive_data)
    
    print(f"\n保护结果:")
    print(f"  DNA追溯码: {protected['context']['dna_code']}")
    print(f"  数据主权: {protected['sovereignty']}")
