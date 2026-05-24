# n8n + 语雀 连接安全指南

**生成时间**：2025-12-24 18:45

---

## ⚠️ 重要安全提示

### 语雀API Token已失效

你提供的语雀API Token：
```
FBTte5WHp9KyrzXodfT8XT2qa6NzYFc05ObeBAyV
```

**根据语雀回复，这个Token已经被识别为泄露并自动失效。**

### 为什么失效？

1. **公开分享** - API Token不应在对话中暴露
2. **安全机制** - 语雀检测到泄露后立即销毁
3. **保护账户** - 防止他人访问你的语雀数据

### 如何处理？

**不要使用这个Token**，它已经无法工作。

---

## 🔒 正确的操作方式

### 第1步：创建新Token

**访问语雀令牌页面**：
https://www.yuque.com/settings/tokens

**创建新令牌**：
1. 点击"新建令牌"
2. 令牌描述：`n8n自动化`
3. 权限勾选：
   - ✅ 读取
   - ✅ 导出
4. 有效期：30天（建议）
5. 点击"确定"

**重要**：
- ⚠️ 不要公开分享新Token
- ⚠️ 不要在聊天记录中粘贴
- ✅ 只在需要时使用

---

### 第2步：配置n8n连接语雀

#### 方法1：在n8n中配置HTTP Request节点

**n8n访问地址**：
http://localhost:5678
用户名：lucky
密码：jiaqi5201314

**配置步骤**：

1. **登录n8n**
   - 打开 http://localhost:5678
   - 输入用户名：lucky
   - 输入密码：jiaqi5201314

2. **创建新Workflow**
   - 点击"Add workflow"
   - 选择"HTTP Request"节点

3. **配置HTTP Request节点**
   ```
   Method: GET
   URL: https://www.yuque.com/api/v2/repos/{你的空间ID}/docs
   Authentication: Generic Credential Type
   Auth: Header Auth
   Name: Yuque API
   Name: X-Auth-Token
   Value: [粘贴你的新Token]
   ```

4. **保存并测试**
   - 点击"Save"
   - 点击"Execute Workflow"
   - 查看返回结果

---

### 第3步：n8n + 语雀常见用例

#### 用例1：自动导出语雀文档

**Workflow配置**：

1. **HTTP Request节点**（获取文档列表）
   ```
   Method: GET
   URL: https://www.yuque.com/api/v2/repos/{空间ID}/docs
   Headers:
     X-Auth-Token: [你的新Token]
   ```

2. **Code节点**（处理数据）
   ```javascript
   // 遍历文档列表
   const docs = $input.all();
   const processedDocs = docs.map(doc => {
     return {
       id: doc.id,
       title: doc.title,
       url: doc.url
     };
   });
   return processedDocs;
   ```

3. **HTTP Request节点**（导出文档）
   ```
   Method: GET
   URL: https://www.yuque.com/api/v2/repos/{空间ID}/docs/{文档ID}/export
   Query Parameters:
     format: markdown
   Headers:
     X-Auth-Token: [你的新Token]
   ```

---

#### 用例2：同步语雀文档到Obsidian

**Workflow配置**：

1. **HTTP Request节点**（获取文档）
   ```
   Method: GET
   URL: https://www.yuque.com/api/v2/repos/{空间ID}/docs/{文档ID}
   Headers:
     X-Auth-Token: [你的新Token]
   ```

2. **Code节点**（转换为Markdown）
   ```javascript
   const doc = $input.first().json;
   const markdown = `# ${doc.title}\n\n${doc.body}\n\n---\n\n来源: 语雀\n时间: ${new Date().toISOString()}`;
   return { markdown };
   ```

3. **Write Binary File节点**（保存到Obsidian）
   ```
   File Name: {{ $json.title }}.md
   Binary Property: data
   Directory: /Users/zuimeidedeyihan/UID9622-Memory
   ```

---

## 🛡️ 安全最佳实践

### Token管理

1. **定期更换**
   - 建议每30天更换一次
   - 如果怀疑泄露，立即更换

2. **最小权限**
   - 只勾选必要的权限
   - 避免使用"完全访问"

3. **本地存储**
   - 使用macOS Keychain存储
   - 不要在代码中硬编码

4. **不要分享**
   - ❌ 不要在聊天记录中粘贴
   - ❌ 不要在公开代码中使用
   - ❌ 不要在文档中记录

---

## 🚀 快速开始

### 今天可以做的

1. **创建新Token**
   - 访问：https://www.yuque.com/settings/tokens
   - 创建新令牌

2. **测试n8n**
   - 等待Docker启动
   - 访问：http://localhost:5678

3. **配置第一个Workflow**
   - 获取语雀文档列表
   - 导出到本地

---

## 🆘 故障排除

### Q: n8n无法访问
**A**: 检查Docker状态
```bash
docker ps | grep n8n
docker logs n8n-lucky
```

### Q: 语雀API返回401
**A**: Token无效或过期
- 创建新Token
- 检查Token权限
- 确认Token未过期

### Q: 导出格式混乱
**A**: 使用正确的导出参数
```
Query Parameters:
  format: markdown
  use_lakebook: true
```

---

## 📊 n8n + 语雀 架构图

```
┌─────────────┐
│  语雀云端    │
│  (API)     │
└──────┬──────┘
       │
       │ X-Auth-Token
       │
┌──────▼──────┐
│   n8n       │
│ (自动化平台) │
│  localhost: │
│  5678       │
└──────┬──────┘
       │
       │
┌──────▼──────┐
│   Obsidian  │
│  (本地笔记) │
└─────────────┘
```

---

## ✅ 检查清单

- [x] 语雀API Token已失效
- [x] 安全指南已生成
- [ ] 创建新Token
- [ ] n8n启动并可访问
- [ ] 配置第一个Workflow
- [ ] 测试文档导出

---

## 🎉 总结

**已完成**：
- ✅ 识别语雀Token泄露
- ✅ 生成安全操作指南
- ✅ n8n配置说明

**待完成**：
- ⏳ 创建新语雀Token
- ⏳ n8n服务启动
- ⏳ 配置自动化Workflow

---

**DNA追溯码**：`#ZHUGEXIN⚡️2025-N8N-YUQUE-SECURITY-GUIDE-V1.0`

**状态**：✅ 安全指南已生成

**最后更新**：2025-12-24 18:45
