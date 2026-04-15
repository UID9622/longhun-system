# 🚀 CNSH 快速启动指南

> **5分钟上手，让每一个记忆都有价值**

## 🎯 适合人群

- 👨‍💻 **技术爱好者** - 想了解中国自主研发的安全技术
- 🏛️ **文化传承者** - 关注易经、甲骨文等传统文化
- 🔐 **隐私保护者** - 重视数据主权和个人隐私
- 🌱 **开源学习者** - 想参与中国开源项目
- 💼 **企业决策者** - 寻找自主可控的解决方案

## 📦 安装部署

### 1️⃣ 环境检查

```bash
# 检查Python版本 (需要3.8+)
python --version

# 如果没有Python，请访问:
# https://www.python.org/downloads/
```

### 2️⃣ 下载安装

```bash
# 克隆项目
git clone https://github.com/zhugexin/cnsh-web3-dna.git
cd cnsh-web3-dna

# 安装依赖
pip install -r requirements.txt
```

### 3️⃣ 启动系统

```bash
# 启动CNSH服务器
python3 simple_server.py
```

看到以下输出表示启动成功：

```
✅ CNSH本地引擎已启动 → http://localhost:8080
⚠️ 此服务完全离线，数据仅存于本机
🔐 支持易经八卦推理系统
==================================
```

### 4️⃣ 访问系统

打开浏览器访问：`http://localhost:8080`

## 🔐 首次使用

### 🧬 生成DNA身份

1. 打开浏览器访问系统
2. 点击"生成DNA"按钮
3. 选择内容类型（AIENGINE/MEMORY/DIALOG等）
4. 获得独特DNA签名：

```
#CNSH-ZHUGEXIN⚡️2025🇨🇳🐉☯️乾⚖️♠️🧚🏼‍♀️❤️♾️AIENGINE-v2.0-ACTIVE
```

### 🔍 验证DNA完整性

1. 复制生成的DNA代码
2. 点击"验证DNA"按钮
3. 粘贴DNA代码进行验证
4. 获得验证结果和易经解读

### 📖 体验易经智慧

1. 在推理框输入问题
2. 点击"易经推理"按钮
3. 获得卦象分析和智慧解读

示例输入：
- "我应该如何规划我的职业发展？"
- "我的项目遇到了困难，该怎么办？"
- "如何平衡工作与生活？"

## 🎨 界面介绍

### 🏛️ 主要功能区

| 区域 | 功能 | 文化元素 |
|-----|-----|---------|
| 🧬 DNA生成区 | 生成/验证DNA签名 | 甲骨文、龍图腾 |
| 🔮 易经推理区 | 智能问题分析 | 六十四卦、阴阳 |
| 📊 状态监控区 | 系统运行状态 | 青铜器纹样 |
| 📋 历史记录区 | 操作日志查看 | 竹简样式 |

### 🎨 视觉设计

- **背景**：水墨山水渐变
- **图标**：甲骨文符号
- **配色**：青花瓷、青铜金、玉石绿
- **字体**：思源宋体、马善政楷体

## 🔧 高级功能

### 📱 自定义配置

编辑`simple_server.py`中的配置：

```python
# 修改端口
PORT = 8080  # 改为其他端口避免冲突

# 修改认证密码
AUTH_PASSWORD = "CNSH2025"  # 改为您的密码

# 自定义DNA元素
self.dna_elements = {
    "country": "🇨🇳",
    "culture": "🐉",
    # 添加更多文化元素...
}
```

### 🔐 数据加密

CNSH默认使用AES-256-GCM加密：

```python
# 加密示例
from crypto_utils import CryptoUtils

crypto = CryptoUtils()
encrypted = crypto.aes256_encrypt("我的秘密记忆", "我的密码")

# 解密示例
decrypted = crypto.aes256_decrypt(encrypted, "我的密码")
```

### 🧬 自定义DNA签名

```python
from dna_verifier import CNSHDNAVerifier

verifier = CNSHDNAVerifier()

# 生成自定义DNA
custom_dna = verifier.generate_dna("CUSTOM_TYPE")

# 验证DNA
is_valid, message = verifier.verify_dna(custom_dna["dna_code"])
```

## 📚 API文档

### 🔗 核心接口

#### 生成DNA
```bash
curl -X POST http://localhost:8080/dna-generate \
  -H "Content-Type: application/json" \
  -d '{"content_type": "MEMORY"}'
```

#### 验证DNA
```bash
curl -X POST http://localhost:8080/dna-verify \
  -H "Content-Type: application/json" \
  -d '{"dna_code": "#CNSH-ZHUGEXIN..."}'
```

#### 易经推理
```bash
curl -X POST http://localhost:8080/infer \
  -H "Content-Type: application/json" \
  -d '{"text": "如何学习新技术？"}'
```

#### 系统状态
```bash
curl -X GET http://localhost:8080/status
```

## 🛠️ 故障排除

### ❌ 常见问题

#### 1. 端口被占用
```bash
# 查找占用端口的进程
lsof -i :8080

# 结束进程
kill -9 <PID>

# 或修改simple_server.py中的端口号
PORT = 8081  # 改为其他端口
```

#### 2. Python依赖缺失
```bash
# 重新安装依赖
pip install -r requirements.txt --upgrade

# 或使用虚拟环境
python -m venv cnsh_env
source cnsh_env/bin/activate  # Linux/Mac
cnsh_env\Scripts\activate     # Windows
pip install -r requirements.txt
```

#### 3. 浏览器兼容性问题
- 推荐使用：Chrome、Firefox、Safari最新版本
- 确保JavaScript已启用
- 清除浏览器缓存后重试

#### 4. DNA验证失败
- 检查DNA代码是否完整复制
- 确认没有多余空格或换行
- 尝试重新生成DNA

## 🆘 获取帮助

### 📞 联系渠道

- 📧 **邮箱**: [uid9622@petalmail.com](mailto:uid9622@petalmail.com)
- 🐙 **GitHub**: [提交Issue](https://github.com/zhugexin/cnsh-web3-dna/issues)
- 💬 **讨论**: [GitHub Discussions](https://github.com/zhugexin/cnsh-web3-dna/discussions)

### 📖 更多文档

- [完整API文档](../docs/API.md)
- [安全架构详解](../docs/SECURITY.md)
- [易经智慧集成](../docs/ICHING.md)
- [贡献指南](../CONTRIBUTING.md)

## 🌟 下一步

恭喜您成功启动CNSH系统！接下来您可以：

1. **深入探索** - 阅读[完整文档](../docs/)了解系统原理
2. **参与贡献** - 查看[贡献指南](../CONTRIBUTING.md)参与开源
3. **分享传播** - 帮助更多中国人了解自主技术
4. **创新应用** - 将CNSH应用到您的项目中

---

🌸 **让每一个记忆都有价值，让每一份数据都有主权** 🌸

🇨🇳 **中国智慧，世界共享** 🇨🇳

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:12
🧬 DNA追溯码: #CNSH-SIGNATURE-0ac1d9c0-20251218032412
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 坤卦：地势坤，君子以厚德载物
📜 内容哈希: 1d2d848150e02335
⚠️ 警告: 未经授权修改将触发DNA追溯系统
