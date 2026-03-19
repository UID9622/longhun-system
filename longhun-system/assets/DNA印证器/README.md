# 龙魂DNA存证系统 | 完整使用说明

## 🔐 创作者数字身份认证

**UID**: 9622  
**身份**: 诸葛鑫 (Lucky)  
**GPG指纹**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

**DNA追溯码**: #ZHUGEXIN⚡️2026-01-06-LONGHUN-DNA-SYSTEM-README-001

**确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

---

## 📋 文件清单

```yaml
完整系统包含以下文件:
  ✅ longhun_dna.js (核心引擎 - JavaScript版本)
  ✅ generator.html (DNA生成器网页)
  ✅ verifier.html (DNA验证器网页)
  ✅ README.md (本文件 - 使用说明)
  
可选文件:
  📄 longhun_dna.cnsh (CNSH源代码 - 用于学习)
```

---

## 🚀 快速开始

### 方法1：双击打开（最简单）

```bash
1. 将所有文件放在同一个文件夹
2. 双击 generator.html 生成存证
3. 双击 verifier.html 验证存证
```

### 方法2：本地HTTP服务器（推荐）

```bash
# 如果安装了Python
python -m http.server 8000

# 如果安装了Node.js
npx http-server

# 然后在浏览器访问
http://localhost:8000/generator.html
http://localhost:8000/verifier.html
```

### 方法3：部署到网站

```bash
将所有文件上传到:
  - GitHub Pages
  - Vercel
  - Netlify
  - 任何静态网站托管服务
```

---

## 📖 使用教程

### 1. 生成DNA存证

**步骤：**

1. 打开 `generator.html`
2. 填写以下信息：
   - **创作者ID**: 你的唯一标识（例如：ZHUGEXIN）
   - **项目名称**: 项目分类（例如：TEST, ARTICLE, CODE）
   - **文本内容**: 需要存证的内容
3. 点击 **"🔐 生成DNA存证"**
4. 系统将显示：
   - DNA追溯码
   - 数字指纹
   - 创建时间
5. 点击 **"📥 下载存证文件"** 保存JSON文件
6. 或点击 **"📋 复制DNA码"** 复制DNA追溯码

**示例：**

```yaml
创作者ID: ZHUGEXIN
项目名称: TEST
文本内容: "这是我的第一个DNA存证测试"

生成结果:
  DNA追溯码: #ZHUGEXIN⚡️2026-01-06-TEST-001
  数字指纹: a1b2c3d4e5f6... (64位十六进制)
  创建时间: 2026-01-06T12:00:00.000Z
```

---

### 2. 验证DNA存证

**方式A：通过DNA码验证**

1. 打开 `verifier.html`
2. 选择 **"通过DNA码验证"** 标签
3. 输入DNA追溯码（例如：#ZHUGEXIN⚡️2026-01-06-TEST-001）
4. 点击 **"🔐 验证DNA码"**
5. 系统将显示验证结果

**方式B：通过文件验证**

1. 打开 `verifier.html`
2. 选择 **"通过文件验证"** 标签
3. 点击 **"选择存证文件"** 上传之前下载的JSON文件
4. 点击 **"🔐 验证文件"**
5. 系统将显示验证结果

**验证结果：**

```yaml
验证通过 ✅:
  - 显示绿色
  - 说明: "验证通过 - 内容真实可信"
  - 显示完整信息

验证失败 ⚠️:
  - 显示红色
  - 说明: "验证失败 - 内容可能被篡改"
  - 显示原因和指纹对比
```

---

## 🧠 工作原理

### DNA追溯码格式

```
格式: #创作者ID⚡️日期-项目名称-序号

示例:
  #ZHUGEXIN⚡️2026-01-06-TEST-001
  #ZHUGEXIN⚡️2026-01-06-ARTICLE-002
  #ZHUGEXIN⚡️2026-01-06-CODE-003

组成:
  # - 固定前缀
  ZHUGEXIN - 创作者ID
  ⚡️ - 分隔符
  2026-01-06 - 创建日期
  TEST - 项目名称
  001 - 三位序号（自动递增）
```

### 数字指纹生成

```javascript
// 1. 组合内容
组合内容 = 文本内容 + DNA追溯码

// 2. 计算SHA-256哈希
数字指纹 = SHA256(组合内容)

// 3. 转为十六进制
数字指纹 = "a1b2c3d4e5f6..." (64位)
```

### 验证机制

```yaml
验证步骤:
  1. 读取存证（从本地存储或文件）
  2. 提取：文本内容 + DNA追溯码
  3. 重新计算数字指纹
  4. 对比：原始指纹 vs 计算指纹
  
验证通过条件:
  原始指纹 == 计算指纹
  
验证失败条件:
  原始指纹 != 计算指纹
  或 DNA码不存在
```

---

## 💾 数据存储

### 存储位置

```yaml
双重存储机制:

1. localStorage (快速访问)
   - 位置: 浏览器本地存储
   - 容量: 约5-10MB
   - 特点: 快速、永久

2. IndexedDB (持久化)
   - 位置: 浏览器数据库
   - 容量: 几百MB+
   - 特点: 可靠、结构化

数据结构:
  键: DNA追溯码
  值: 完整存证对象（JSON格式）
```

### 数据安全

```yaml
安全特性:
  ✅ 本地优先: 数据不上传任何服务器
  ✅ 不可篡改: 任何修改导致指纹失效
  ✅ 可以验证: 随时验证真伪
  ✅ 可以导出: JSON文件备份
  ✅ 可以导入: 恢复到其他浏览器

注意事项:
  ⚠️ 清除浏览器数据会删除存证
  ⚠️ 建议定期下载备份文件
  ⚠️ 隐私浏览模式下数据不持久
```

---

## 🔧 高级功能

### 批量导出

```javascript
// 在浏览器控制台执行
const allEvidences = await LonghunDNA.queryAllEvidence();
console.log(`共有 ${allEvidences.count} 条存证`);

// 导出所有存证
allEvidences.evidences.forEach(evidence => {
    LonghunDNA.exportEvidence(evidence.dnaCode);
});
```

### 按创作者查询

```javascript
// 查询特定创作者的所有存证
const result = await LonghunDNA.queryAllEvidence("ZHUGEXIN");
console.log(`找到 ${result.count} 条存证`);
```

### 按项目查询

```javascript
// 查询特定项目的所有存证
const result = await LonghunDNA.queryAllEvidence(null, "TEST");
console.log(`找到 ${result.count} 条存证`);
```

### 删除存证

```javascript
// 慎用！删除存证
const result = await LonghunDNA.deleteEvidence("#ZHUGEXIN⚡️2026-01-06-TEST-001");
if (result.success) {
    console.log("存证已删除");
}
```

---

## 🐛 常见问题

### Q1: 生成的DNA存证在哪里？

**A:** 存证保存在浏览器本地存储中，不会上传到任何服务器。

**位置:**
- localStorage（快速访问）
- IndexedDB（持久化存储）

**建议:** 点击"下载存证文件"保存JSON文件作为备份。

---

### Q2: 清除浏览器数据会怎样？

**A:** 会删除所有本地存储的存证。

**解决方案:**
- 定期下载存证文件备份
- 可以通过"文件验证"重新导入

---

### Q3: 验证失败是什么原因？

**A:** 可能的原因：

1. **DNA码不存在**
   - 从未创建过此存证
   - 或者已被删除

2. **内容被篡改**
   - 文本内容被修改
   - 数字指纹不匹配

3. **文件损坏**
   - JSON文件格式错误
   - 文件传输过程损坏

---

### Q4: 如何在其他电脑上验证？

**A:** 两种方式：

**方式1: 通过文件**
1. 下载存证JSON文件
2. 在其他电脑打开 `verifier.html`
3. 上传JSON文件验证

**方式2: 通过DNA码**
1. 复制DNA追溯码
2. 同时需要有完整的存证JSON文件
3. 先导入文件，再用DNA码验证

---

### Q5: 如何分享给别人验证？

**A:** 两种方式：

**方式1: 分享JSON文件**
```
1. 导出存证JSON文件
2. 发送给对方
3. 对方用verifier.html验证
```

**方式2: 分享DNA码（需要先导入）**
```
1. 对方需要先导入JSON文件
2. 然后可以用DNA码查询验证
```

---

### Q6: 系统支持哪些浏览器？

**A:** 支持所有现代浏览器：

```yaml
推荐浏览器:
  ✅ Chrome 90+
  ✅ Firefox 88+
  ✅ Edge 90+
  ✅ Safari 14+

不支持:
  ❌ IE 11及以下
```

---

### Q7: 数据会同步到云端吗？

**A:** **不会！**

```yaml
本系统特点:
  ✅ 完全本地
  ✅ 不上传数据
  ✅ 不需要账号
  ✅ 不需要网络
  ✅ 完全可控
```

---

### Q8: 如何备份所有存证？

**A:** 使用浏览器控制台：

```javascript
// 1. 打开generator.html或verifier.html
// 2. 按F12打开控制台
// 3. 输入以下代码

// 查询所有存证
const result = await LonghunDNA.queryAllEvidence();
console.log(`共有 ${result.count} 条存证`);

// 批量导出
result.evidences.forEach((evidence, index) => {
    setTimeout(() => {
        LonghunDNA.exportEvidence(evidence.dnaCode);
    }, index * 500); // 每0.5秒导出一个
});
```

---

## 🎯 使用场景

### 场景1: 创作内容存证

```yaml
用途: 证明某个时间创作了某个内容

步骤:
  1. 创作完成后，复制全文
  2. 粘贴到DNA生成器
  3. 生成DNA存证
  4. 下载存证文件保存

好处:
  - 证明创作时间
  - 证明原创性
  - 防止抄袭
```

### 场景2: 重要承诺存证

```yaml
用途: 对重要承诺进行不可篡改的记录

步骤:
  1. 写下承诺内容
  2. 生成DNA存证
  3. 公开DNA追溯码
  4. 任何人都可以验证

好处:
  - 承诺可验证
  - 不可抵赖
  - 公开透明
```

### 场景3: 文档版本管理

```yaml
用途: 记录文档的每个重要版本

步骤:
  1. 每次重大修改后生成存证
  2. DNA码作为版本号
  3. 可以追溯任何版本
  4. 可以验证任何版本

好处:
  - 完整的版本历史
  - 可以验证真伪
  - 不可篡改
```

---

## 🔒 隐私与安全

### 隐私保护

```yaml
本系统的隐私承诺:

✅ 本地优先:
  - 所有数据保存在浏览器本地
  - 不上传到任何服务器
  - 不收集任何用户信息

✅ 完全可控:
  - 用户完全掌控数据
  - 可以随时导出
  - 可以随时删除

✅ 不需要账号:
  - 不需要注册
  - 不需要登录
  - 不需要联网（生成和验证时）
```

### 安全提醒

```yaml
注意事项:

⚠️ 敏感信息:
  - 不要在存证中包含密码、私钥等敏感信息
  - 存证可以被任何获得JSON文件的人查看

⚠️ 备份:
  - 定期下载存证文件备份
  - 浏览器数据可能被清除

⚠️ 验证:
  - 重要存证建议多次验证
  - 保存多份备份
```

---

## 📚 技术规范

### DNA追溯码规范

```yaml
格式定义:
  模式: #创作者ID⚡️YYYY-MM-DD-项目名称-序号
  
组成部分:
  前缀: # (必须)
  创作者ID: 字母数字组合 (必须)
  分隔符: ⚡️ (必须)
  日期: YYYY-MM-DD格式 (必须)
  项目名称: 字母数字下划线 (必须)
  序号: 001-999三位数字 (必须)
  
限制:
  - 总长度不超过200字符
  - 创作者ID不超过50字符
  - 项目名称不超过50字符
```

### 数字指纹规范

```yaml
算法: SHA-256
输入: 文本内容 + DNA追溯码
输出: 64位十六进制字符串

特性:
  - 确定性: 相同输入 → 相同输出
  - 唯一性: 不同输入 → 不同输出（极高概率）
  - 不可逆: 无法从输出推导输入
  - 雪崩效应: 微小改动 → 完全不同输出
```

### 存证对象结构

```json
{
  "content": "文本内容",
  "timestamp": "2026-01-06T12:00:00.000Z",
  "timestampUnix": 1704542400000,
  "creatorId": "ZHUGEXIN",
  "projectName": "TEST",
  "sequence": 1,
  "dnaCode": "#ZHUGEXIN⚡️2026-01-06-TEST-001",
  "digitalFingerprint": "a1b2c3d4...",
  "metadata": {
    "toolVersion": "龙魂DNA存证系统 v1.0",
    "systemNote": "本存证基于SHA-256算法生成，任何修改都会导致指纹失效",
    "creatorStatement": "技术主权·数据主权·中文原生"
  }
}
```

---

## 🌟 核心理念

```yaml
技术主权:
  - 核心技术在中国
  - 中文原生设计
  - 不依赖外国平台

数据主权:
  - 数据在用户手里
  - 完全本地存储
  - 用户完全掌控

为人民服务:
  - 完全开源
  - 完全免费
  - 不设付费墙
  - 不收割用户

君子协议:
  - 承诺可验证
  - 不可篡改
  - 公开透明
```

---

## 📞 联系与支持

```yaml
创作者: 诸葛鑫 (Lucky)
UID: 9622
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

开源地址:
  - Gitee: gitee.com/zhugexin/longhun-dna-system
  - GitHub: github.com/zhugexin/longhun-dna-system

反馈方式:
  - 在开源仓库提Issue
  - 发送邮件（见仓库）
```

---

## 📜 许可协议

```
MIT License

Copyright (c) 2026 诸葛鑫 (Lucky) | UID9622

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

**[敬礼] 退伍军人！**

**技术主权 · 数据主权 · 中文原生**

**龙魂DNA存证系统 v1.0**

**完全开源 · 完全免费 · 完全可控**

**北辰老兵致敬！** 🫡🇨🇳
