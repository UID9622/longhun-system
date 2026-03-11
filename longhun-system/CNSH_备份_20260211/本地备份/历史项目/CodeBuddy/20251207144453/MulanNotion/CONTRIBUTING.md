# 🤝 CNSH 贡献指南

> **让每一个贡献都有价值，让每一位贡献者都有尊严**

## 🌸 贡献原则

### 💝 木兰精神

- ✅ **善良但有底线** - 守护用户数据主权
- ✅ **热情但有原则** - 坚持技术中立
- ✅ **公平不卡脖子** - 开源共享，普惠大众
- ✅ **中立不评价** - 尊重每个用户的选择
- ✅ **守护不侵略** - 上善若水，利万物而不争

### 🎯 技术原则

- **中国优先** - 中文语义为主，英文为辅
- **简洁明了** - 代码可读性大于一切
- **安全第一** - 用户数据主权不可侵犯
- **文化自信** - 五千年文明融入现代技术
- **开放包容** - 欢迎全球开发者参与

## 🚀 如何贡献

### 1️⃣ 环境准备

```bash
# 克隆项目
git clone https://github.com/zhugexin/cnsh-web3-dna.git
cd cnsh-web3-dna

# 安装依赖
pip install -r requirements.txt

# 运行测试
python -m pytest
```

### 2️⃣ 选择贡献类型

#### 🐛 Bug修复

1. 检查[Issues](https://github.com/zhugexin/cnsh-web3-dna/issues)确认bug未被修复
2. Fork仓库并创建特性分支
3. 修复bug并添加测试用例
4. 提交Pull Request

#### ✨ 新功能开发

1. 在Issues中讨论新功能设计
2. 确保功能符合CNSH价值观
3. 编写代码和文档
4. 添加测试用例
5. 提交Pull Request

#### 📚 文档改进

1. 识别文档不足之处
2. 改进或补充相关内容
3. 确保文档准确易懂
4. 提交Pull Request

#### 🌐 国际化

1. 添加多语言支持
2. 翻译界面和文档
3. 测试本地化效果
4. 提交Pull Request

## 📋 代码规范

### 🎨 Python代码风格

```python
# CNSH Python代码规范示例

# 文件头部 - 必须包含
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块名称 - 简短描述
木兰开源协议 v2.0 - 中国自主可控技术栈
"""

# 导入标准库
import hashlib
import datetime
from typing import Dict, List, Optional

# 导入第三方库
import cryptography

# CNSH相关导入
from cnsh_core import DNAVerifier, CulturalElements

class CNSHClass:
    """类描述 - 使用中文注释，体现文化自信"""
    
    def __init__(self, config: Dict):
        """初始化方法 - 包含易经元素"""
        self.config = config
        self.hexagram = "乾"  # 默认卦象
        self.dna_signature = self._generate_dna()
    
    def method_name(self, parameter: str) -> str:
        """
        方法描述 - 包含中国智慧
        
        Args:
            parameter: 参数描述
            
        Returns:
            返回值描述
        """
        # 实现代码 - 注释使用中文
        result = f"处理{parameter}，融合易经智慧"
        return result
```

### 📝 提交信息规范

```
# 提交格式
<类型>(<范围>): <主题>

# 示例
feat(dna): 添加易经坤卦支持
fix(encrypt): 修复AES-256加密错误
docs(readme): 更新安装说明
style(ui): 调整甲骨文显示效果
refactor(server): 重构DNA验证逻辑
test(unit): 添加DNA完整性测试
chore(deps): 更新依赖版本
```

### 🏛️ DNA签名要求

所有重要提交必须包含DNA签名：

```python
# 在相关代码中添加DNA验证
dna_signature = "#CNSH-ZHUGEXIN⚡️2025🇨🇳🐉☯️乾⚖️♠️🧚🏼‍♀️❤️♾️-DNA-CN-20251207-CONTRIBUTION"
# 确保贡献可追溯、不可抵赖
```

## 🔍 审核流程

### 📋 Pull Request清单

提交PR前请确认：

- [ ] 代码符合CNSH规范
- [ ] 包含必要的测试用例
- [ ] 文档已更新
- [ ] 包含DNA签名验证
- [ ] 通过所有自动化测试
- [ ] 签署木兰开源协议

### 🧪 测试要求

```python
# 测试用例示例
def test_dna_verification():
    """测试DNA验证功能"""
    verifier = CNSHDNAVerifier()
    dna_info = verifier.generate_dna("MEMORY")
    
    # 验证DNA格式
    assert dna_info["dna_code"].startswith("#CNSH-")
    assert "🇨🇳" in dna_info["dna_code"]
    assert "🐉" in dna_info["dna_code"]
    
    # 验证DNA完整性
    is_valid, message = verifier.verify_dna(dna_info["dna_code"])
    assert is_valid
    assert "通过" in message
```

## 🌟 贡献者权益

### 🏆 贡献认可

- **贡献者名单** - 在README中永久记录
- **DNA签名** - 每个贡献都有独特DNA标识
- **社区影响力** - 参与项目决策讨论
- **技术成长** - 学习前沿安全技术

### 💎 特殊贡献

- **核心贡献者** - 获得项目维护权限
- **文化推广** - 参与国际标准制定
- **技术创新** - 专利申请和论文发表
- **社区建设** - 组织技术交流活动

## 📞 联系我们

### 🎯 主要联系渠道

- 📧 **邮箱**: [uid9622@petalmail.com](mailto:uid9622@petalmail.com)
- 🐙 **GitHub**: [提交Issue](https://github.com/zhugexin/cnsh-web3-dna/issues)
- 💬 **讨论**: [GitHub Discussions](https://github.com/zhugexin/cnsh-web3-dna/discussions)

### 🌐 社区参与

- **技术讨论**: 在GitHub中参与技术交流
- **文化分享**: 分享易经、甲骨文等文化见解
- **用户反馈**: 提供使用体验和改进建议
- **国际推广**: 帮助项目走向世界

## 🎉 致谢

感谢每一位为CNSH项目做出贡献的开发者！您的每一次贡献都是：

- 🇨🇳 **对中国技术的支持**
- 🧬 **对数据主权的守护**
- 🌸 **对木兰精神的传承**
- 🌍 **对开源世界的贡献**

---

🌸 **让每一个贡献都有价值，让每一位贡献者都有尊严** 🌸

🇨🇳 **中国智慧，世界共享** 🇨🇳

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:12
🧬 DNA追溯码: #CNSH-SIGNATURE-f6d5f4dc-20251218032412
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 屯卦：云雷屯，君子以经纶
📜 内容哈希: b741b9dc0ca65928
⚠️ 警告: 未经授权修改将触发DNA追溯系统
