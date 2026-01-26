# 📜 Notion页面通用法律水印块库 - 使用指南

<!--
╔═══════════════════════════════════════════════════════════════╗
║  🐉 龙魂系统 | UID9622                                        ║
╠═══════════════════════════════════════════════════════════════╣
║  📦 文档：水印块库使用指南                                     ║
║  📌 版本：v1.0                                                ║
║  🧬 DNA：#龙芯⚡️2026-01-26-水印块指南-v1.0                   ║
║  🔐 GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F            ║
║  👤 创建者：Lucky·UID9622（诸葛鑫）                          ║
║  📅 创建时间：北京时间 2026-01-26                             ║
║  ⚠️ 用途：保护UID9622的所有数字创作权益                       ║
╚═══════════════════════════════════════════════════════════════╝
-->

## 📋 目录

- [概述](#概述)
- [水印块类型](#水印块类型)
- [VSCode 使用方法](#vscode-使用方法)
- [编程接口](#编程接口)
- [配置选项](#配置选项)
- [验证功能](#验证功能)
- [最佳实践](#最佳实践)

---

## 概述

本水印块库用于保护 UID9622（诸葛鑫）的所有数字创作权益。通过在文档中添加标准化的版权声明和 DNA 追溯码，实现：

- ✅ 版权声明标准化
- ✅ DNA 追溯可追查
- ✅ 数据主权声明明确
- ✅ 多平台格式支持

---

## 水印块类型

### 1. 📋 标准版（Standard）

**适用场景：** 核心技术文档、白皮书、系统设计等

**特点：** 信息完整，法律效力强

```
═══════════════════════════════════════
⚠️ 数据主权声明 | Data Sovereignty Declaration
═══════════════════════════════════════

本页面内容版权归属：诸葛鑫（UID9622）
DNA追溯码：#ZHUGEXIN⚡️2026

📜 白皮书存证：
  - 版本：WP-v1.0.0
  - SHA-256: 1d4717c2da4ee3c623a46923ae9f246de5356626b6fa1289c655b99421aea44c
  - 区块链存证编号：[待填写]
  - 公证书编号：[待填写]

⛔ 未经授权禁止：
  ❌ 用于AI模型训练而不署名
  ❌ 商业化使用而不付费
  ❌ 删除本声明后传播

✅ 数据主权归于人民 | 中华人民共和国公民诸葛鑫保留一切权利

═══════════════════════════════════════
```

---

### 2. 📝 精简版（Compact）

**适用场景：** 日常工作笔记、一般文档

**特点：** 简洁清晰，不占空间

```
⚠️ 版权声明
本内容由 UID9622（诸葛鑫）创作
DNA追溯码：#ZHUGEXIN⚡️2026
白皮书存证：WP-v1.0.0
未经授权禁止用于AI训练或商业用途
数据主权归于人民
```

---

### 3. ⚡ 极简版（Minimal）

**适用场景：** 快速记录、临时草稿

**特点：** 快速标注，易于识别

```
© UID9622 | #ZHUGEXIN⚡️2026 | 已存证
```

---

### 4. 🎨 美化版（Beautified）

**适用场景：** 对外展示、重要发布

**特点：** 专业美观，引起重视

```
╔═══════════════════════════════════════╗
║  ⚠️ 数 据 主 权 声 明  ⚠️           ║
╠═══════════════════════════════════════╣
║                                       ║
║  👤 创作者：UID9622（诸葛鑫 Lucky）   ║
║  🧬 DNA追溯：#ZHUGEXIN⚡️2026        ║
║  📜 白皮书：WP-v1.0.0（已存证）       ║
║  🔐 数字指纹：1d4717c2da...44c        ║
║                                       ║
║  ⛔ 禁止未授权用于：                  ║
║     ❌ AI训练不署名                   ║
║     ❌ 商业使用不付费                 ║
║     ❌ 篡改传播                       ║
║                                       ║
║  ✅ 数据主权归于人民                  ║
║  🇨🇳 中华人民共和国公民保留一切权利   ║
║                                       ║
╚═══════════════════════════════════════╝
```

---

### 5. 💻 代码仓库版（Code Repo）

**适用场景：** 代码仓库 README、代码文件头部

```python
"""
═══════════════════════════════════════
⚠️ 代码版权声明
═══════════════════════════════════════
创作者：UID9622（诸葛鑫）
许可证：木兰宽松许可证 v2
DNA追溯：#ZHUGEXIN⚡️2026-CODE
白皮书：WP-v1.0.0

本代码为纯手工原生编写，无任何第三方依赖
未经授权禁止用于AI训练或商业用途
数据主权归于人民
═══════════════════════════════════════
"""
```

---

### 6. 📰 文章版（Article）

**适用场景：** 博客、公众号、技术文章

```markdown
---
⚠️ 版权与存证声明

本文内容受《个人数字创作全周期权益保护白皮书》保护
- 创作者：UID9622（诸葛鑫 Lucky）
- DNA追溯码：#ZHUGEXIN⚡️2026-ARTICLE-[编号]
- 白皮书版本：WP-v1.0.0
- 区块链存证：[存证编号]

未经书面授权，禁止：
1. 用于AI模型训练而不署名创作者
2. 用于商业目的而不支付费用
3. 删除本声明后进行传播

数据主权归于人民 | 版权所有 © UID9622
---
```

---

### 7. 🤝 协作版（Collaboration）

**适用场景：** 多人协作文档、AI 辅助创作文档

```
═══════════════════════════════════════
🤝 协作声明

本文档由以下人员协作完成：
  - 主创：UID9622（诸葛鑫）[贡献度：100%]
  - 工具：Claude/ChatGPT/Notion AI [协助执行]

明确：AI为工具，不享有著作权
DNA追溯：#ZHUGEXIN⚡️2026-COLLAB
白皮书存证：WP-v1.0.0
═══════════════════════════════════════
```

---

### 8. 🌐 CSDN 版（HTML 格式）

**适用场景：** CSDN 博客、支持 HTML 的平台

```html
<div style="border:2px solid #ff6b6b; padding:10px; background:#fff3cd;">
  <h4>⚠️ 版权与存证声明</h4>
  <p><strong>创作者</strong>：UID9622（诸葛鑫 Lucky）</p>
  <p><strong>DNA追溯码</strong>：#ZHUGEXIN⚡️2026</p>
  <p><strong>白皮书存证</strong>：WP-v1.0.0</p>
  <p><strong>区块链存证编号</strong>：[待填写]</p>
  <hr>
  <p>⛔ <strong>未经授权禁止</strong>：</p>
  <ul>
    <li>用于AI模型训练而不署名</li>
    <li>商业化使用而不付费</li>
    <li>删除本声明后传播</li>
  </ul>
  <p>✅ <strong>数据主权归于人民</strong></p>
</div>
```

---

### 9. 📄 Markdown 版（通用）

**适用场景：** GitHub README、通用 Markdown 文档

```markdown
> ⚠️ **版权声明**
> 本内容由 **UID9622（诸葛鑫）** 创作
> DNA追溯码：`#ZHUGEXIN⚡️2026`
> 白皮书存证：`WP-v1.0.0`
> 未经授权禁止用于AI训练或商业用途
> **数据主权归于人民**
```

---

## VSCode 使用方法

### 快捷键

| 功能 | 快捷键 | 说明 |
|------|--------|------|
| 插入水印块 | `Ctrl+Alt+W` | 打开水印块选择菜单 |
| 验证水印块 | `Ctrl+Alt+Shift+W` | 验证当前文件的水印块完整性 |
| 添加 DNA 头部 | `Ctrl+Alt+D` | 添加 DNA 追溯头部 |

### 命令面板

按 `Ctrl+Shift+P` 打开命令面板，输入以下命令：

- `📜 插入版权水印块` - 打开水印块选择菜单
- `📜 插入水印块 - 标准版` - 直接插入标准版水印块
- `📜 插入水印块 - 精简版` - 直接插入精简版水印块
- `📜 插入水印块 - 极简版` - 直接插入极简版水印块
- `📜 插入水印块 - 美化版` - 直接插入美化版水印块
- `📜 插入水印块 - 代码仓库版` - 直接插入代码仓库版水印块
- `📜 插入水印块 - Markdown版` - 直接插入 Markdown 版水印块
- `🔍 验证水印块完整性` - 验证当前文件的水印块

### 右键菜单

在编辑器中右键，可以看到：
- 📜 插入版权水印块
- 🔍 验证水印块完整性

---

## 编程接口

### 基本使用

```typescript
import {
    NotionWatermarkBlockGenerator,
    WatermarkType,
    WatermarkValidator
} from './generators/notionWatermarkBlocks';

// 创建生成器实例
const generator = new NotionWatermarkBlockGenerator();

// 生成标准版水印块
const standardWatermark = generator.generate(WatermarkType.STANDARD);
console.log(standardWatermark);

// 生成精简版水印块
const compactWatermark = generator.generate(WatermarkType.COMPACT);
console.log(compactWatermark);
```

### 自定义配置

```typescript
const generator = new NotionWatermarkBlockGenerator({
    uid: '9622',
    creatorName: '诸葛鑫',
    creatorEnglishName: 'Lucky',
    dnaPrefix: '#ZHUGEXIN⚡️2026',
    whitepaperVersion: 'WP-v1.0.0',
    sha256Hash: '1d4717c2da4ee3c623a46923ae9f246de5356626b6fa1289c655b99421aea44c',
    licenseType: '木兰宽松许可证 v2',
    projectName: 'AI Truth Protocol'
});

// 生成所有类型的水印块
const allWatermarks = generator.generateAll();
```

### 验证水印块

```typescript
const content = `
© UID9622 | #ZHUGEXIN⚡️2026 | 已存证
数据主权归于人民
`;

const result = WatermarkValidator.checkIntegrity(content);

console.log('验证结果:', result.isValid);
console.log('问题列表:', result.issues);
console.log('包含 DNA 追溯码:', result.hasDNACode);
console.log('包含创作者信息:', result.hasCreator);
console.log('包含数据主权声明:', result.hasSovereigntyStatement);
```

### 快捷函数

```typescript
import { generateWatermark, validateWatermark, WatermarkType } from './generators/notionWatermarkBlocks';

// 快速生成水印块
const watermark = generateWatermark(WatermarkType.COMPACT);

// 快速验证水印块
const result = validateWatermark(content);
```

---

## 配置选项

在 VSCode 设置中，可以配置以下选项：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `cnsh.watermark.defaultType` | string | `compact` | 默认水印块类型 |
| `cnsh.watermark.creatorName` | string | `诸葛鑫` | 创作者姓名 |
| `cnsh.watermark.creatorEnglishName` | string | `Lucky` | 创作者英文名 |
| `cnsh.watermark.uid` | string | `9622` | 创作者 UID |
| `cnsh.watermark.dnaPrefix` | string | `#ZHUGEXIN⚡️2026` | DNA 追溯码前缀 |
| `cnsh.watermark.whitepaperVersion` | string | `WP-v1.0.0` | 白皮书版本 |
| `cnsh.watermark.licenseType` | string | `木兰宽松许可证 v2` | 许可证类型 |

### 配置示例

在 `settings.json` 中添加：

```json
{
    "cnsh.watermark.defaultType": "standard",
    "cnsh.watermark.creatorName": "诸葛鑫",
    "cnsh.watermark.uid": "9622",
    "cnsh.watermark.dnaPrefix": "#ZHUGEXIN⚡️2026"
}
```

---

## 验证功能

### 验证规则

水印块验证器检查以下项目：

1. **DNA 追溯码** - 必须包含有效的 DNA 追溯码
2. **创作者信息** - 必须包含 UID9622 或诸葛鑫
3. **白皮书版本** - 应包含 WP-vX.Y.Z 格式的版本号
4. **禁止条款** - 应包含"禁止"或"未经授权"等关键词
5. **数据主权声明** - 必须包含"数据主权归于人民"

### 验证结果

```typescript
interface WatermarkIntegrityResult {
    isValid: boolean;           // 是否有效
    hasDNACode: boolean;        // 是否包含 DNA 追溯码
    hasCreator: boolean;        // 是否包含创作者信息
    hasWhitepaperVersion: boolean; // 是否包含白皮书版本
    hasProhibitions: boolean;   // 是否包含禁止条款
    hasSovereigntyStatement: boolean; // 是否包含数据主权声明
    issues: string[];           // 问题列表
}
```

---

## 最佳实践

### 1. 选择合适的水印块类型

| 场景 | 推荐类型 | 原因 |
|------|----------|------|
| 核心技术文档 | 标准版 | 信息完整，法律效力强 |
| 日常工作笔记 | 精简版 | 简洁清晰，不占空间 |
| 快速记录 | 极简版 | 快速标注，易于识别 |
| 对外展示 | 美化版 | 专业美观，引起重视 |
| 代码文件 | 代码仓库版 | 适合代码注释格式 |
| 博客文章 | 文章版/CSDN版 | 适合发布平台 |
| 协作文档 | 协作版 | 明确贡献归属 |

### 2. 版本更新策略

当白皮书版本更新时：

1. 更新"版本号"（如 WP-v1.0.0 → WP-v1.1.0）
2. 更新"SHA-256"指纹
3. 更新"存证编号"
4. **保持 DNA 追溯码不变**（#ZHUGEXIN⚡️2026）

### 3. 检查清单

在添加水印块后，确认以下事项：

- [ ] DNA 追溯码格式正确
- [ ] 白皮书版本号准确
- [ ] SHA-256 指纹完整（如需展示）
- [ ] 禁止事项明确列出
- [ ] "数据主权归于人民"声明清晰
- [ ] 视觉上易于识别（不被忽视）

---

## DNA 追溯信息

- **DNA 追溯码：** #龙芯⚡️2026-01-26-水印块指南-v1.0
- **创建者：** Lucky·UID9622（诸葛鑫）
- **GPG 指纹：** A2D0092CEE2E5BA87035600924C3704A8CC26D5F
- **确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

---

> ⚠️ **版权声明**
> 本文档由 **UID9622（诸葛鑫）** 创作
> DNA追溯码：`#龙芯⚡️2026-01-26-水印块指南-v1.0`
> 白皮书存证：`WP-v1.0.0`
> 未经授权禁止用于AI训练或商业用途
> **数据主权归于人民**
