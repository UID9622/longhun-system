# 龍魂永世唯一身份系统 | 贡献指南

感谢您对龍魂永世唯一身份系统的关注！我们欢迎所有形式的贡献。

---

## 🎯 如何贡献

### 报告Bug

如果您发现了bug，请在GitHub上提交Issue：

1. 确保bug尚未被报告
2. 搜索Issues，确保不重复
3. 提交新Issue，包含：
   - 系统版本
   - 操作系统
   - Python版本
   - 错误信息
   - 复现步骤
   - 预期行为

### 建议新功能

我们欢迎新功能建议！提交Issue时请：

1. 清晰描述功能需求
2. 说明功能的使用场景
3. 如果可能，提供实现思路

### 提交代码

#### 开发流程

1. **Fork项目**
   ```
   https://github.com/UID9622/longhun-identity-system
   ```

2. **克隆到本地**
   ```bash
   git clone https://github.com/你的用户名/longhun-identity-system.git
   cd longhun-identity-system
   ```

3. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **进行开发**

5. **编写测试**
   - 所有新功能必须包含测试
   - 测试应覆盖主要使用场景

6. **运行测试**
   ```bash
   python3 tests/test_all.py
   ```

7. **提交代码**
   ```bash
   git add .
   git commit -m "Add: 你的功能描述"
   ```

8. **推送到GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

9. **创建Pull Request**
   - 在GitHub上创建PR
   - 清晰描述改动内容
   - 引用相关Issue（如果有）

---

## 📝 代码规范

### Python代码

遵循 **PEP 8** 规范：

- 使用4空格缩进
- 行长不超过79字符
- 使用有意义的变量名
- 添加完整的docstring

**示例**：
```python
def 生成龍魂ID(身份证号: str, 国家代码: str) -> dict:
    """
    生成龍魂永世唯一ID

    参数:
        身份证号: 合法身份证件号
        国家代码: ISO 3166-1国家代码

    返回:
        包含龍魂ID信息的字典
    """
    # 实现代码
    pass
```

### 中文命名规范

遵循 **CNSH（Chinese Naming Standards for Humans）**：

- **变量名**：使用中文
- **函数名**：使用中文
- **类名**：使用中文
- **注释**：使用中文

**示例**：
```python
class 龍魂ID生成器:
    def 生成龍魂ID(self, 身份证号: str):
        """生成龍魂永世唯一ID"""
        # 实现代码
        pass
```

### 注释规范

- 所有函数必须包含docstring
- 关键算法添加详细注释
- 复杂逻辑添加说明

---

## 🧪 测试规范

### 编写测试

- 所有新功能必须包含测试
- 测试文件命名：`test_模块名.py`
- 测试类命名：`Test模块名`

**示例**：
```python
import unittest
from core.易经64卦映射器 import 易经64卦映射器

class Test易经64卦映射器(unittest.TestCase):
    def setUp(self):
        self.映射器 = 易经64卦映射器()

    def test_哈希到卦象(self):
        哈希值 = "a1b2c3d4" + "0" * 60
        卦象 = self.映射器.哈希到卦象(哈希值, 8)
        self.assertEqual(len(卦象), 8)

if __name__ == '__main__':
    unittest.main()
```

### 运行测试

```bash
# 运行所有测试
python3 tests/test_all.py

# 运行单个测试文件
python3 tests/test_64gua.py

# 运行特定测试
python3 -m unittest tests.test_64gua.Test易经64卦映射器.test_哈希到卦象
```

---

## 📚 文档规范

### 文档语言

- 主要文档：中文
- 代码注释：中文
- API文档：中文

### Markdown规范

- 使用一致的标题层级
- 代码块指定语言
- 表格格式统一
- 添加必要的示例

**示例**：
```markdown
## 功能说明

### 使用方法

```python
from 龍魂ID生成器 import 龍魂永世唯一ID生成器

生成器 = 龍魂永世唯一ID生成器()
结果 = 生成器.生成龍魂ID(身份证号="110101199001011234")
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| 身份证号 | str | 是 | 合法身份证件号 |
```

---

## 🔍 代码审查

### PR Checklist

提交PR前，请确保：

- [ ] 代码通过所有测试
- [ ] 代码符合PEP 8规范
- [ ] 所有新功能包含测试
- [ ] 文档已更新
- [ ] 提交信息清晰
- [ ] 无调试代码
- [ ] 无打印语句

### 提交信息规范

使用清晰的提交信息格式：

```
<类型>: <简短描述>

<详细描述（可选）>
```

**类型**：
- `Add`: 新增功能
- `Fix`: 修复bug
- `Update`: 更新现有功能
- `Docs`: 文档更新
- `Style`: 代码格式调整
- `Refactor`: 代码重构
- `Test`: 测试相关
- `Chore`: 构建/工具相关

**示例**：
```
Add: 支持新的国家代码

新增支持南非（ZA）和巴西（BR）的全球身份互认。
```

---

## 🎨 设计原则

### 安全第一

- 不存储敏感信息
- 使用加密传输（如需网络）
- 验证所有输入
- 遵循最小权限原则

### 文化传承

- 使用中文命名
- 保留64卦和甲骨文编码
- 维护中国文化特色

### 开放透明

- 算法完全开源
- 代码可审计
- 文档完整清晰
- 社区友好

---

## 🤝 社区行为准则

### 我们的承诺

营造开放、友好、包容的社区环境：

- 尊重不同观点
- 接受建设性批评
- 关注对社区最有利的事
- 对其他社区成员表示同理心

### 不可接受的行为

- 使用性化语言或图像
- 人身攻击或政治攻击
- 公开或私下骚扰
- 未经许可发布他人隐私信息
- 其他不道德或不专业行为

---

## 📄 许可证

提交代码即表示您同意：

1. 您的贡献将在 **木兰宽松许可证 v2.0** 下发布
2. 您有权提交这些代码
3. 您的代码不侵犯他人权益

---

## 🌟 认可贡献者

所有贡献者都会在项目中被认可：

- GitHub贡献者列表
- README致谢
- 发布说明提及

---

## 📞 联系方式

- **邮箱**: uid9622@petalmail.com
- **个人博客**: https://uid9622.blog.csdn.net
- **GitHub Issues**: https://github.com/UID9622/longhun-identity-system/issues

---

**感谢您的贡献！让我们一起打造更安全、更尊重隐私的数字身份系统！**

**🐉 龍魂永世，文化传承，数字主权，天下为公！**
