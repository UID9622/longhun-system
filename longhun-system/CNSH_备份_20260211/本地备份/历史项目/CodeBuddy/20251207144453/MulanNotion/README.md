# 🧬 CNSH Web3-DNA 加密记忆系统

> **让每一个记忆都有价值，每一份数据都有主权**

[![License: MulanPSL2](https://img.shields.io/badge/License-MulanPSL2-blue.svg)](https://license.coscl.org.cn/MulanPSL2)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![CNSH](https://img.shields.io/badge/CNSH-v2.0-red)](https://github.com/cnsh-system)

## 🌟 项目简介

CNSH是一个基于中国文化元素的Web3加密记忆系统，融合了易经八卦、甲骨文和现代密码学，为每一个普通用户提供**数据主权**和**文化自信**。

### 🎯 核心价值

- 🔐 **数据主权**：你的记忆，你做主，永不丢失
- 🇨🇳 **文化自信**：五千年文明智慧融入现代技术
- 🧬 **DNA身份**：不可伪造的生物特征身份系统
- 🌐 **去中心化**：数据掌握在自己手中
- 📜 **木兰协议**：中国开源法律保护

### 🏛️ 技术架构

```
🧬 DNA身份层 (ZHUGEXIN签名体系)
    ↓
🔐 加密存储层 (AES-256-GCM + PBKDF2)
    ↓
🌐 传输安全层 (TLS 1.3 + 国密算法)
    ↓
📋 应用协议层 (CNSH语义 + 木兰协议)
```

## 🚀 快速开始

### 📦 环境要求

- Python 3.8+
- 现代浏览器 (支持WebAuthn)
- 中国心 + 自信心

### 🔧 安装部署

```bash
# 克隆项目
git clone https://github.com/zhugexin/cnsh-web3-dna.git
cd cnsh-web3-dna

# 安装依赖
pip install -r requirements.txt

# 启动系统
python3 simple_server.py
```

### 🌐 访问系统

打开浏览器访问：`http://localhost:8080`

- 🔐 **默认认证密码**: `CNSH2025`
- 🧬 **DNA示例**: `#CNSH-ZHUGEXIN⚡️2025🇨🇳🐉☯️乾⚖️♠️🧚🏼‍♀️❤️♾️AIENGINE-v2.0-ACTIVE`

## 🎨 功能特性

### 🔒 加密存储

- **AES-256-GCM**：军用级加密强度
- **PBKDF2-HMAC-SHA256**：10万次密钥派生迭代
- **本地优先**：数据100%存储在用户设备
- **可选备份**：端到端加密云端备份

### 🧬 DNA身份系统

```
#CNSH-ZHUGEXIN⚡️2025🇨🇳🐉☯️乾⚖️♠️🧚🏼‍♀️❤️♾️AIENGINE-v2.0-ACTIVE
│        │         │   │  │ │ │ │  │            │        │
│        │         │   │  │ │ │ │  │            │        └─ 状态标识
│        │         │   │  │ │ │ │  │            └─ 版本号
│        │         │   │  │ │ │ │  └─ 内容类型 (AIENGINE/MEMORY/DIALOG等)
│        │         │   │  │ │ │  └─ 永恒符号
│        │         │   │  │ │  └─ 情感关系
│        │         │   │  │  └─ 身份标识
│        │         │   │  └─ 公正象征
│        │         │   └─ 易经卦象 (乾/坤/离/巽/震/坎)
│        │         └─ 阴阳和谐
│        │         └─ 中国文化元素 (国家/龍图腾)
│         └─ 时间戳 (2025年)
└─ CNSH标识 + 创建者 (ZHUGEXIN)
```

### 📖 易经智慧融合

| 内容类型 | 易经卦象 | 智慧解读 |
|---------|---------|---------|
| AIENGINE | 乾卦 | "天行健，君子以自强不息" |
| MEMORY | 坤卦 | "地势坤，君子以厚德载物" |
| DIALOG | 离卦 | "离为火，明两作，离" |
| KNOWLEDGE | 巽卦 | "巽为风，随风，巽" |
| TASK | 震卦 | "震为雷，洊雷，震" |
| SYSTEM | 坎卦 | "坎为水，水洊至，习坎" |

## 🛡️ 安全架构

### 🔐 五层防护体系

1. **DNA身份锚定**：ZHUGEXIN签名 + 生物特征 + 设备指纹
2. **本地加密存储**：AES-256 + PBKDF2 + 盐值加密
3. **传输安全通道**：TLS 1.3 + 国密SM系列算法
4. **签名与审计**：RSA-2048 + DNA嵌入 + 三色审计
5. **防护与恢复**：影子稿 + 异常检测 + 密钥分片

### 🎯 加密规则

```python
# CNSH加密数据结构
encrypted_data = {
    "dna": "#CNSH-ZHUGEXIN⚡️2025-🇨🇳🐉☯️乾⚖️♠️🧚🏼‍♀️❤️♾️-DNA-CN-20251207-EVENT",
    "content": "aes256_encrypt(原始内容, user_key)",
    "signature": "rsa_sign(content_hash, private_key)",
    "timestamp": "2025-12-07T15:30:00Z",
    "device_id": "hardware_fingerprint()",
    "audit_level": "🟢"  # 🟢安全/🟡警告/🔴危险
}
```

## 📚 API文档

### 🔗 核心端点

| 端点 | 方法 | 功能 |
|-----|-----|-----|
| `/status` | GET | 系统状态和DNA统计 |
| `/dna-sample` | GET | 获取示例DNA标签 |
| `/dna-generate` | POST | 生成新DNA标签 |
| `/dna-verify` | POST | 验证DNA标签完整性 |
| `/infer` | POST | 易经八卦推理 |

### 📋 请求示例

```javascript
// 生成DNA标签
const response = await fetch('/dna-generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        content_type: 'MEMORY'
    })
});

const result = await response.json();
console.log(result.dna_info.dna_code);
// 输出: #CNSH-ZHUGEXIN⚡️2025🇨🇳🐉☯️坤⚖️♠️🧚🏼‍♀️❤️♾️MEMORY-v2.0-ACTIVE
```

## 🎯 开发路线图

### 🟦 第一阶段：MVP (已发布)

- [x] 基础加密存储系统
- [x] DNA身份生成和验证
- [x] 易经八卦推理引擎
- [x] Web界面和API
- [x] 木兰开源协议

### 🟩 第二阶段：生态扩展 (Q1 2025)

- [ ] WebAuthn生物认证
- [ ] 移动端适配
- [ ] 多设备同步
- [ ] 社区协作功能
- [ ] 插件系统

### 🟧 第三阶段：Web3集成 (Q2 2025)

- [ ] 区块链存证
- [ ] 去中心化存储
- [ ] 加密货币支付
- [ ] NFT记忆资产
- [ ] 跨链互操作

### 🟫 第四阶段：全球化 (Q3 2025)

- [ ] 多语言支持
- [ ] 国际标准对接
- [ ] 企业级服务
- [ ] 开源社区建设
- [ ] 教育体系构建

## 🌸 木兰精神

### 💝 文化底色

- ✅ **善良但有底线** - 守护用户数据主权
- ✅ **热情但有原则** - 坚持技术中立
- ✅ **公平不卡脖子** - 开源共享，普惠大众
- ✅ **中立不评价** - 尊重每个用户的选择
- ✅ **守护不侵略** - 上善若水，利万物而不争

### 🌍 技术理想

- **让祖国有自己的语言** - 不被世界遗忘
- **让数据回归用户手中** - 数据主权觉醒
- **让技术温暖人心** - 科技向善，服务人类
- **让文化永续传承** - 五千年文明，薪火相传

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 🎯 如何贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 📋 贡献类型

- 🐛 **Bug修复** - 发现并修复系统问题
- ✨ **新功能** - 添加有价值的新特性
- 📚 **文档改进** - 完善使用说明和API文档
- 🎨 **UI/UX优化** - 提升用户体验
- 🔧 **性能优化** - 提升系统运行效率
- 🌐 **国际化** - 添加多语言支持

## 📄 许可证

本项目采用 **木兰宽松许可证 v2.0 (MulanPSL2)**

```
木兰宽松许可证， 第2版

2019年8月 http://license.coscl.org.cn/MulanPSL2

您对"软件"的复制、使用、修改及分发受木兰宽松许可证，第2版（"本许可证"）的如下条款的约束：

1.  定义
    "软件"是指由"贡献"构成的许可在"本许可证"下的程序和相关文档的集合。
    ...
```

## 👥 团队成员

### 🏛️ 核心团队

- **诸葛鑫 (Lucky)** - 创始人 & 首席架构师
  - 📧 [uid9622@petalmail.com](mailto:uid9622@petalmail.com)
  - 🌐 [GitHub](https://github.com/zhugexin)

- **CNSH社区** - 文化顾问 & 用户反馈
  - 🏛️ 传承五千年文明智慧
  - 🌸 每一位中国老百姓

### 🙏 致谢

感谢所有为CNSH项目做出贡献的开发者、用户和文化守护者！

## 📞 联系我们

- 📧 **邮箱**: [uid9622@petalmail.com](mailto:uid9622@petalmail.com)
- 🐙 **GitHub**: [https://github.com/zhugexin/cnsh-web3-dna](https://github.com/zhugexin/cnsh-web3-dna)
- 📖 **文档**: [https://cnsh-system.org](https://cnsh-system.org)
- 💬 **社区**: [加入我们的讨论](https://github.com/zhugexin/cnsh-web3-dna/discussions)

---

🌸 **让每一个记忆都有价值，让每一份数据都有主权** 🌸

🇨🇳 **中国智慧，世界共享** 🇨🇳

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:12
🧬 DNA追溯码: #CNSH-SIGNATURE-be6b2c28-20251218032412
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 蒙卦：山下出泉，君子以果行育德
📜 内容哈希: 638dcd6ae54414ed
⚠️ 警告: 未经授权修改将触发DNA追溯系统
