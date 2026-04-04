# 语雀Token配置 - 完整指南

**生成时间**：2025-12-24 18:50

---

## 📖 语雀在说什么？

### 语雀的安全机制

**简单说**：语雀有自动安全检测，**一旦发现API Token被公开分享，会立即销毁这个Token**。

### 为什么会发生？

1. **你在对话中分享了Token**
   ```
   例如：dLMet3MWMtW01iU6SOISLLdrqDCm6bjFGmhErnTA
   ```

2. **语雀检测到泄露**
   - 语雀的安全系统监控公开平台
   - 检测到Token出现在对话中
   - 立即标记为"已泄露"

3. **自动销毁**
   - Token立即失效
   - 无法再用于API调用
   - 保护你的账户安全

### 结果

- ❌ 你在对话中提供的任何Token都会失效
- ❌ 即使重新生成也不行
- ❌ 不能在聊天框里粘贴Token

---

## 🔧 如何正确配置语雀Token

### 第1步：创建配置文件

**执行命令**：
```bash
cp ~/.dragonsoul/.env.example ~/.dragonsoul/.env
```

### 第2步：编辑配置文件

**打开配置文件**：
```bash
vim ~/.dragonsoul/.env
# 或者用其他编辑器
open ~/.dragonsoul/.env
```

**填写内容**：

```bash
# 找到这一行，替换成你的真实Token
YUQUE_TOKEN=请在此处填写你的语雀API令牌

# 替换为：
YUQUE_TOKEN=你在语雀网站复制的新Token
```

### 第3步：获取语雀空间ID

**获取方法**：

1. **登录语雀**
   - 访问：https://www.yuque.com
   - 登录你的账户

2. **进入你的知识库**
   - 点击进入任意一个知识库
   - 查看浏览器地址栏

3. **提取空间ID**
   ```
   地址示例：
   https://www.yuque.com/your-name/space-name/docs

   空间ID就是：your-name
   ```

**填写到配置文件**：
```bash
YUQUE_SPACE_ID=你的空间ID
```

### 第4步：保存配置

**vim编辑器**：
```
按 ESC 键
输入 :wq
按 Enter 键
```

**其他编辑器**：
```
保存文件
```

---

## 🚀 配置n8n连接语雀

### 自动配置脚本

```bash
bash ~/.dragonsoul/scripts/setup_yuque_n8n.sh
```

### 手动配置

**第1步：访问n8n**
```
http://localhost:5678
用户名: lucky
密码: jiaqi5201314
```

**第2步：创建Workflow**

1. 点击"New workflow"
2. 添加"HTTP Request"节点

**第3步：配置HTTP Request节点**

```
Method: GET
URL: https://www.yuque.com/api/v2/repos/{你的空间ID}/docs
Authentication: Header Auth
Header Name: X-Auth-Token
Header Value: {{ $env.YUQUE_TOKEN }}
```

**第4步：测试**

1. 点击"Execute Workflow"
2. 查看返回结果
3. 如果成功，会返回文档列表

---

## 📝 示例Workflow

### Workflow 1：获取语雀文档列表

**节点配置**：

**HTTP Request 1**
```
Method: GET
URL: https://www.yuque.com/api/v2/repos/{{ $env.YUQUE_SPACE_ID }}/docs
Headers:
  X-Auth-Token: {{ $env.YUQUE_TOKEN }}
```

**输出**：
```json
[
  {
    "id": "文档ID",
    "title": "文档标题",
    "slug": "文档slug",
    "created_at": "创建时间",
    "updated_at": "更新时间"
  }
]
```

---

### Workflow 2：导出单个文档

**节点配置**：

**HTTP Request 1**
```
Method: GET
URL: https://www.yuque.com/api/v2/repos/{{ $env.YUQUE_SPACE_ID }}/docs/{{ $json.doc_id }}/export
Query Parameters:
  format: markdown
Headers:
  X-Auth-Token: {{ $env.YUQUE_TOKEN }}
```

**输出**：
- Markdown格式的文档内容
- 可以保存到本地或Obsidian

---

### Workflow 3：同步到Obsidian

**节点配置**：

**HTTP Request 1**（获取文档）
```
Method: GET
URL: https://www.yuque.com/api/v2/repos/{{ $env.YUQUE_SPACE_ID }}/docs/{{ $json.doc_id }}
Headers:
  X-Auth-Token: {{ $env.YUQUE_TOKEN }}
```

**Code节点**（格式化）
```javascript
const doc = $input.first().json;

// 添加元数据
const markdown = `# ${doc.title}

---

原文链接: ${doc.url}
导出时间: ${new Date().toISOString()}

${doc.body}

---

📝 导出自语雀
`;

return {
  json: {
    filename: `${doc.title}.md`,
    content: markdown
  }
};
```

**Write Binary File节点**（保存）
```
File Name: {{ $json.filename }}
Directory: /Users/zuimeidedeyihan/UID9622-Memory
```

---

## 🛡️ 安全最佳实践

### 1. Token管理

- ✅ 使用.env文件存储（不要在代码中硬编码）
- ✅ 定期更换Token（建议30天）
- ✅ 设置Token有效期
- ❌ 不要在对话中分享
- ❌ 不要在公开代码中使用

### 2. 权限控制

创建Token时，只勾选必要权限：
- ✅ 读取
- ✅ 导出
- ❌ 不要勾选"完全访问"

### 3. 本地存储

- ✅ 使用macOS Keychain（高级用户）
- ✅ 加密.env文件（可选）
- ✅ 定期备份配置

---

## ✅ 配置检查清单

- [x] 创建.env配置文件
- [x] 填写语雀Token
- [x] 填写空间ID
- [ ] 测试n8n连接
- [ ] 获取文档列表
- [ ] 导出单个文档
- [ ] 同步到Obsidian

---

## 🆘 故障排除

### Q: n8n无法访问
**A**:
1. 检查Docker是否启动
   ```bash
   docker ps | grep n8n
   ```

2. 重启n8n
   ```bash
   docker restart n8n-lucky
   ```

### Q: 语雀API返回401
**A**: Token无效或过期
1. 重新生成Token
2. 更新.env文件
3. 重启n8n

### Q: 空间ID错误
**A**:
1. 登录语雀
2. 进入知识库
3. 查看浏览器地址栏
4. 提取空间ID（第一个/和第二个/之间的部分）

### Q: Token一直失效
**A**: 语雀检测到泄露
- 确保Token只在本地使用
- 不要在对话中分享
- 检查.env文件是否被意外公开

---

## 📊 配置示例

### .env文件完整示例

```bash
# 龍魂系统环境配置

# 语雀配置
YUQUE_TOKEN=你的语雀API令牌（从网站复制）
YUQUE_SPACE_ID=your-space-name

# n8n配置
N8N_BASIC_AUTH_USER=lucky
N8N_BASIC_AUTH_PASSWORD=jiaqi5201314
N8N_PORT=5678

# Ollama配置
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b

# Obsidian配置
OBSIDIAN_VAULT_PATH=/Users/zuimeidedeyihan/UID9622-Memory

# 日志配置
LOG_LEVEL=info
LOG_PATH=~/.dragonsoul/audit
```

---

## 🎉 总结

**已完成**：
- ✅ 配置文件模板
- ✅ 配置脚本
- ✅ n8n配置说明

**待完成**：
- ⏳ 用户填写真实Token
- ⏳ 填写空间ID
- ⏳ 测试n8n连接

---

**DNA追溯码**：`#ZHUGEXIN⚡️2025-YUQUE-TOKEN-CONFIG-GUIDE-V1.0`

**状态**：✅ 配置指南已生成

**最后更新**：2025-12-24 18:50
