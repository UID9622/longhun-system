# Notion API 接入指南

## 第一步：获取你的 Notion API 密钥

### 1. 打开 Notion 网页
访问：https://www.notion.so/my-integrations

### 2. 创建新的集成
- 点击 "+ New integration"（新建集成）
- 给它起个名字，比如："龍魂助手"
- 选择你的工作区
- 点击 "Submit"（提交）

### 3. 复制 API 密钥
- 创建完成后，会显示 **Internal Integration Token**
- 这就是你的 API 密钥，格式像这样：
  ```
  secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```
- **复制它！** 待会要用

### 4. 给集成授权访问你的数据库
- 打开你存放26张卡片的 Notion 页面
- 点击右上角的 "..." 菜单
- 选择 "Add connections"（添加连接）
- 选择你刚创建的"龍魂助手"集成
- 点击 "Confirm"（确认）

---

## 第二步：获取你的数据库 ID

### 打开你的 Notion 数据库页面
- 浏览器地址栏会显示类似这样的网址：
  ```
  https://www.notion.so/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?v=yyyyyy
  ```
- 那一串 `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` 就是你的**数据库 ID**
- **复制它！** 待会要用

---

## 第三步：把密钥保存到代码里

下一步我会给你写代码，你只需要：
1. 把 API 密钥粘贴进去
2. 把数据库 ID 粘贴进去
3. 运行代码

就这么简单！

---

## 常见问题

### Q: 我找不到我的数据库在哪？
**A:** 
- 如果你用的是 Notion 页面（Page），需要先把它转成数据库（Database）
- 或者告诉我你的 Notion 是怎么组织的，我帮你找

### Q: API 密钥会不会被别人看到？
**A:**
- 密钥保存在你本地设备的钥匙串（Keychain）里
- 不会上传到任何地方
- 只有你的设备能用

### Q: 26张卡片在哪个数据库？
**A:**
- 根据你之前说的，卡片分类是：
  - 🤖 龍魂核心算法（14张）
  - 💻 Swift 语言基础（6张）
  - 🏗️ Swift 服务端架构（2张）
  - 🔒 Swift 安全（1张）
  - ⚡ Swift 并发（1张）
  - 🌐 Swift 嵌入式（2张）
- 如果都在一个数据库里，只需要一个 ID
- 如果分散在多个数据库，需要多个 ID

---

**准备好了吗？**
把你的 API 密钥和数据库 ID 告诉我，我立即写代码！

或者你先去 Notion 获取，然后回来告诉我。
