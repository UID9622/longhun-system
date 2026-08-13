# 身份认证方案 | DNA标签 + 设备绑定

> Notion URL: https://app.notion.com/p/DNA-4cb1ae7d177f4d9eb1967ea008ea8b4e
> Created: 2025-11-17T08:15:00.000Z
> Last edited: 2026-07-01T14:51:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
## 🔐 敏感度标注
🟡 中敏感 - 架构可分享，具体密钥必须保密
✅ 可以公开：
- ✅ 认证架构设计
- ✅ DNA标签生成逻辑
- ✅ 设备绑定方案
❌ 绝对保密：
- ❌ 实际的DNA标签
- ❌ 设备指纹数据
- ❌ 加密密钥
---
## 📦 详细依赖清单
### Python依赖
```bash
pip install hashlib  # Python标准库
pip install uuid     # Python标准库
pip install cryptography==41.0.7
pip install PyJWT==2.8.0
pip install python-dotenv==1.0.0
```
### JavaScript依赖（前端）
```bash
npm install fingerprint2  # 设备指纹
npm install crypto-js     # 加密
```
---
## 💻 完整认证系统
### 1. DNA标签生成器
```python
# dna_generator.py
import hashlib
import uuid
from datetime import datetime
from typing import Dict, List

class DNATagGenerator:
    """UID9622 DNA标签生成器"""
    
    def __init__(self, master_seed: str):
        self.master_seed = master_seed
    
    def generate_dna_tag(self, 
                         user_id: str,
                         device_info: Dict,
                         additional_factors: List[str] = None) -> str:
        """
        生成唯一DNA标签
        
        格式：#ZHUGEXIN⚡️{YEAR}-{EMOJI_CHAIN}-{SIGNATURE}
        """
        # 1. 收集因子
        factors = [
            user_id,
            device_info.get('device_id', ''),
            device_info.get('os', ''),
            device_info.get('browser', ''),
            str(datetime.now().year),
            self.master_seed
        ]
        
        if additional_factors:
            factors.extend(additional_factors)
        
        # 2. 生成基础哈希
        combined = '|'.join(factors)
        base_hash = hashlib.sha256(combined.encode()).hexdigest()
        
        # 3. 生成emoji链（基于哈希值）
        emoji_chain = self._hash_to_emoji_chain(base_hash)
        
        # 4. 生成签名（前8位哈希）
        signature = base_hash[:8].upper()
        
        # 5. 组装DNA标签
        year = datetime.now().year
        dna_tag = f"#ZHUGEXIN⚡️{year}-{emoji_chain}-{signature}"
        
        return dna_tag
    
    def _hash_to_emoji_chain(self, hash_str: str) -> str:
        """将哈希值转换为emoji链"""
        emoji_pool = [
            '🇨🇳', '🐉', '⚖️', '♠️', '🧚🏼\u200d♀️', '❤️', '♾️',
            '🌌', '🧬', '⚡', '🔥', '💎', '🎯', '🚀'
        ]
        
        # 从哈希值中选择emoji
        selected = []
        for i in range(0, min(len(hash_str), 14), 2):
            idx = int(hash_str[i:i+2], 16) % len(emoji_pool)
            selected.append(emoji_pool[idx])
        
        return ''.join(selected[:7])  # 取前7个emoji
    
    def generate_confirm_code(self, 
                             dna_tag: str,
                             action: str,
                             timestamp: str = None) -> str:
        """
        生成一次性确认码
        
        格式：#CONFIRM🌌9622-ONLY-ONCE🧬{CODE}
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        # 组合因子
        combined = f"{dna_tag}|{action}|{timestamp}|{self.master_seed}"
        code_hash = hashlib.sha256(combined.encode()).hexdigest()
        
        # 生成短码
        short_code = code_hash[:12].upper()
        # 添加分隔符提高可读性
        formatted_code = f"{short_code[:4]}-{short_code[4:8]}-{short_code[8:12]}"
        
        confirm_code = f"#CONFIRM🌌9622-ONLY-ONCE🧬{formatted_code}"
        
        return confirm_code
    
    def verify_dna_tag(self, 
                       provided_tag: str,
                       user_id: str,
                       device_info: Dict) -> bool:
        """验证DNA标签"""
        # 重新生成标签
        expected_tag = self.generate_dna_tag(user_id, device_info)
        
        # 比对（忽略年份变化）
        provided_core = provided_tag.split('-', 2)[1:]
        expected_core = expected_tag.split('-', 2)[1:]
        
        return provided_core == expected_core

# 使用示例
if __name__ == "__main__":
    # 初始化（🔴 master_seed必须保密！）
    generator = DNATagGenerator(master_seed="YOUR_SECRET_SEED_HERE")
    
    # 生成DNA标签
    device_info = {
        'device_id': 'MacBook-Pro-M4-Max',
        'os': 'macOS-15.1',
        'browser': 'Chrome-120'
    }
    
    dna_tag = generator.generate_dna_tag(
        user_id="UID9622",
        device_info=device_info,
        additional_factors=['TAIJI-2.1-COMPLETE']
    )
    
    print(f"🧬 DNA标签: {dna_tag}")
    
    # 生成确认码
    confirm_code = generator.generate_confirm_code(
        dna_tag=dna_tag,
        action="DATABASE_UPDATE"
    )
    
    print(f"✅ 确认码: {confirm_code}")
    
    # 验证
    is_valid = generator.verify_dna_tag(dna_tag, "UID9622", device_info)
    print(f"🔐 验证结果: {is_valid}")
```
### 2. 设备指纹识别
```javascript
// device_fingerprint.js
import Fingerprint2 from 'fingerprintjs2';

class DeviceFingerprint {
    constructor() {
        this.fingerprint = null;
    }
    
    async generateFingerprint() {
        return new Promise((resolve) => {
            Fingerprint2.get((components) => {
                // 提取关键组件
                const values = components.map(c => c.value);
                
                // 生成哈希
                const murmur = Fingerprint2.x64hash128(values.join(''), 31);
                
                // 构建设备信息
                const deviceInfo = {
                    fingerprint: murmur,
                    device_id: this._getDeviceId(components),
                    os: this._getOS(components),
                    browser: this._getBrowser(components),
                    screen: this._getScreen(components),
                    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
                };
                
                this.fingerprint = deviceInfo;
                resolve(deviceInfo);
            });
        });
    }
    
    _getDeviceId(components) {
        // 组合多个稳定特征
        const canvas = components.find(c => c.key === 'canvas')?.value;
        const webgl = components.find(c => c.key === 'webgl')?.value;
        const fonts = components.find(c => c.key === 'fonts')?.value;
        
        return Fingerprint2.x64hash128(`${canvas}|${webgl}|${fonts}`, 31);
    }
    
    _getOS(components) {
        const ua = components.find(c => c.key === 'userAgent')?.value || '';
        
        if (ua.includes('Mac')) return 'macOS';
        if (ua.includes('Windows')) return 'Windows';
        if (ua.includes('Linux')) return 'Linux';
        if (ua.includes('Android')) return 'Android';
        if (ua.includes('iOS')) return 'iOS';
        
        return 'Unknown';
    }
    
    _getBrowser(components) {
        const ua = components.find(c => c.key === 'userAgent')?.value || '';
        
        if (ua.includes('Chrome')) return 'Chrome';
        if (ua.includes('Firefox')) return 'Firefox';
        if (ua.includes('Safari')) return 'Safari';
        if (ua.includes('Edge')) return 'Edge';
        
        return 'Unknown';
    }
    
    _getScreen(components) {
        const screen = components.find(c => c.key === 'screenResolution')?.value;
        return screen ? screen.join('x') : 'Unknown';
    }
    
    // 将设备信息发送到后端验证
    async verifyWithBackend(userId) {
        const deviceInfo = await this.generateFingerprint();
        
        const response = await fetch('/api/auth/verify-device', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_id: userId,
                device_info: deviceInfo
            })
        });
        
        const result = await response.json();
        return result;
    }
}

// 使用示例
const device = new DeviceFingerprint();
device.generateFingerprint().then(info => {
    console.log('🖥️ 设备指纹:', info);
});
```
### 3. JWT令牌认证
```python
# jwt_auth.py
import jwt
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

class JWTAuthenticator:
    """JWT令牌认证器"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.algorithm = 'HS256'
    
    def generate_token(self, 
                      user_id: str,
                      dna_tag: str,
                      device_fingerprint: str,
                      expires_hours: int = 24) -> str:
        """生成JWT令牌"""
        payload = {
            'user_id': user_id,
            'dna_tag': dna_tag,
            'device_fingerprint': device_fingerprint,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=expires_hours),
            'system': 'UID9622',
            'version': 'v2.0'
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verify_token(self, token: str) -> dict:
        """验证JWT令牌"""
        try:
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm]
            )
            return {'valid': True, 'payload': payload}
        except jwt.ExpiredSignatureError:
            return {'valid': False, 'error': 'Token已过期'}
        except jwt.InvalidTokenError:
            return {'valid': False, 'error': 'Token无效'}
    
    def refresh_token(self, old_token: str) -> str:
        """刷新令牌"""
        result = self.verify_token(old_token)
        
        if not result['valid']:
            raise ValueError("无法刷新无效token")
        
        payload = result['payload']
        
        # 生成新令牌
        new_token = self.generate_token(
            user_id=payload['user_id'],
            dna_tag=payload['dna_tag'],
            device_fingerprint=payload['device_fingerprint']
        )
        
        return new_token

# 使用示例
if __name__ == "__main__":
    auth = JWTAuthenticator(secret_key="YOUR_SECRET_KEY")
    
    # 生成令牌
    token = auth.generate_token(
        user_id="UID9622",
        dna_tag="#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️-ABC12345",
        device_fingerprint="a1b2c3d4e5f6"
    )
    
    print(f"🎫 令牌: {token}")
    
    # 验证令牌
    result = auth.verify_token(token)
    print(f"✅ 验证: {result['valid']}")
```
---
## 🎯 UID9622四层认证
安全等级从低到高：
### Level 1: 公开访问
- 无需认证
- 只能查看公开内容
### Level 2: 基础认证
- DNA标签验证
- 设备指纹识别
- 访问基础功能
### Level 3: 强认证
- DNA标签 + 设备绑定
- 确认码验证
- 访问H武器、71人格
### Level 4: 核心权限
- 多因子认证
- 生物特征（未来）
- 系统管理权限
### Level 5: 创始人权限（Lucky专属）
- 所有认证层
- 灵魂锁验证
- 完全控制权
---
## 📚 参考资料
- 🔐 JWT官方: https://jwt.io/
- 🖥️ FingerprintJS: https://github.com/fingerprintjs/fingerprintjs
- 🔒 Cryptography库: https://cryptography.io/
---
## 💡 安全建议
1. ✅ 定期轮换密钥（每90天）
1. ✅ 使用HTTPS加密传输
1. ✅ 记录所有认证日志
1. ✅ 异常登录自动告警
1. ✅ DNA标签仅存储哈希值
