# 🧠 记忆压缩系统使用指南

## 📖 系统概述

龍魂记忆压缩系统是一个创新的文本压缩和还原系统，可以将大量文本（几十万字）压缩为简短的 DNA 格式，并通过 DNA 追溯码快速恢复原文。

### 核心特性

- 🧬 **DNA 追溯码** - 每条记忆都有唯一的 DNA 追溯码，可用于快速定位和还原
- ☯️ **太极算法** - 提取字数、关键词、情感、重要程度等变量
- 📦 **多级压缩** - 支持 light/medium/heavy 三种压缩级别
- 💾 **永久存储** - 使用 IndexedDB 本地存储，跨会话持久化
- 🔄 **快速还原** - 通过 DNA 追溯码快速恢复原文
- 🔍 **智能搜索** - 支持按关键词、情感、重要程度、日期搜索

## 🚀 快速开始

### 1. 打开记忆编辑器

在浏览器中直接打开 `memory-editor.html` 文件：
```bash
# 在项目目录中
open memory-editor.html
```

### 2. 输入记忆内容

在左侧输入框中输入你的记忆、想法、笔记。支持任意长度的文本。

### 3. 处理记忆

点击"🧠 处理记忆"按钮，系统会自动：
- 生成 DNA 追溯码
- 提取太极算法变量
- 压缩记忆内容

### 4. 保存记忆

点击"💾 保存到系统"按钮，记忆会保存到 IndexedDB 本地存储。

### 5. 还原记忆

在记忆库中找到要还原的记忆，点击"🔄 还原"按钮，系统会根据 DNA 追溯码恢复原文。

## 🎯 核心功能详解

### DNA 追溯码生成

**格式：**
```
#龍芯⚡️YYYY-MM-DD-MEMORY-XXXX-UID9622
```

**组成部分：**
- `#龍芯⚡️` - DNA 前缀
- `YYYY-MM-DD` - 创建日期
- `MEMORY` - 类型（可以是 MEMORY、EDITOR、SYSTEM 等）
- `XXXX` - 哈希值（8位十六进制）
- `UID9622` - 创建者 UID

**使用方法：**
```javascript
// 生成 DNA 追溯码
const dna = window.dnaGenerator.generate(content, 'MEMORY');

// 解析 DNA 追溯码
const parsed = window.dnaGenerator.parse(dna);

// 验证 DNA 追溯码
const validated = window.dnaGenerator.validate(dna, content);
```

### 太极算法变量提取

**提取的变量：**
- **字数** - 记忆的字符数量
- **行数** - 记忆的行数
- **关键词** - Top 5 关键词，按词频排序
- **情感** - 积极/消极/平静
- **重要程度** - 1-10 分，基于字数和关键词计算
- **情感分数** - -1 到 1 之间的情感分数

**使用方法：**
```javascript
// 提取太极算法变量
const taijiVars = window.taijiExtractor.extract(content);

// 查看结果
console.log(taijiVars);
// {
//   字数: 256,
//   行数: 8,
//   关键词: [{词: "龍魂", 频次: 3}, ...],
//   情感: "积极",
//   重要程度: 7,
//   情感分数: 0.6,
//   时间戳: "2026-03-03T14:00:00.000Z",
//   创建者: "UID9622",
//   版本: "v2.0"
// }
```

### 记忆压缩

**压缩级别：**

| 级别 | 摘要长度 | 关键词数量 | 适用场景 |
|------|---------|-----------|---------|
| Light | 200 字 | 3 个 | 需要保留较多信息 |
| Medium | 100 字 | 5 个 | 平衡压缩率和信息量（默认） |
| Heavy | 50 字 | 7 个 | 需要高压缩率 |

**使用方法：**
```javascript
// 压缩记忆
const compressed = window.memoryCompressor.compress(content, taijiVars, 'medium');

// 查看结果
console.log(compressed);
// {
//   原始长度: 10000,
//   压缩后长度: 150,
//   压缩率: 98,
//   摘要: "前100字内容摘要...",
//   关键词: ["龍魂", "系统", "记忆"],
//   完整哈希: "a1b2c3d4",
//   可还原: true,
//   压缩级别: "medium",
//   时间戳: "2026-03-03T14:00:00.000Z"
// }

// 估算压缩效果
const estimates = window.memoryCompressor.estimateCompression(content);
console.log(estimates);
```

### 记忆还原

**还原方式：**

1. **完整还原** - 从 IndexedDB 恢复完整原文
2. **摘要还原** - 基于压缩数据生成摘要版本

**使用方法：**
```javascript
// 还原记忆
const result = await window.memoryRestorer.restore(dna, compressedData, {
  useStorage: true,    // 使用 IndexedDB
  requireFull: false   // 是否要求完整还原
});

// 查看结果
console.log(result);
// {
//   success: true,
//   dna: "#龍芯⚡️2026-03-03-MEMORY-a1b2c3d4-UID9622",
//   原始内容: "完整的原始内容...",
//   摘要: "前100字内容摘要...",
//   关键词: ["龍魂", "系统", "记忆"],
//   完整哈希: "a1b2c3d4",
//   还原方式: "full",
//   还原质量: 100,
//   错误: null
// }

// 验证还原完整性
const verification = window.memoryRestorer.verifyRestore(result);
console.log(verification);
```

### IndexedDB 存储

**存储结构：**
```javascript
{
  "DNA": "#龍芯⚡️2026-03-03-MEMORY-a1b2c3d4-UID9622",
  "原始内容": "用户输入的完整文本",
  "创建时间": "2026-03-03T14:00:00.000Z",
  "太极变量": {
    "字数": 256,
    "行数": 8,
    "关键词": [...],
    "情感": "积极",
    "重要程度": 7,
    "时间戳": "2026-03-03T14:00:00.000Z",
    "创建者": "UID9622"
  },
  "压缩数据": {
    "原始长度": 256,
    "压缩后长度": 180,
    "压缩率": 61,
    "摘要": "...",
    "完整哈希": "a1b2c3d4",
    "可还原": true
  }
}
```

**使用方法：**
```javascript
// 保存记忆
await window.storageManager.saveMemory(memory);

// 获取记忆
const memory = await window.storageManager.getMemory(dna);

// 获取所有记忆
const memories = await window.storageManager.getAllMemories();

// 搜索记忆
const results = await window.storageManager.searchMemories({
  keyword: "龍魂",
  emotion: "积极",
  importanceMin: 5
});

// 获取统计信息
const stats = await window.storageManager.getStatistics();

// 导出所有记忆
const json = await window.storageManager.exportAllMemories();

// 导入记忆
const count = await window.storageManager.importMemories(json);

// 清理过期记忆
const deleted = await window.storageManager.cleanupOldMemories(30);
```

## 🔍 高级功能

### 批量操作

```javascript
// 批量压缩
const contents = ["内容1", "内容2", "内容3"];
const compressed = window.memoryCompressor.batchCompress(contents, 'medium');

// 批量还原
const items = [{DNA: "...", 压缩数据: {...}}, ...];
const results = await window.memoryRestorer.batchRestore(items, {
  useStorage: true
});

// 批量保存
await window.storageManager.batchSaveMemories(memories);
```

### 搜索和过滤

```javascript
// 按关键词搜索
const results = await window.storageManager.searchMemories({
  keyword: "龍魂"
});

// 按情感过滤
const results = await window.storageManager.searchMemories({
  emotion: "积极"
});

// 按重要程度过滤
const results = await window.storageManager.searchMemories({
  importanceMin: 5
});

// 按日期范围过滤
const results = await window.storageManager.searchMemories({
  startDate: "2026-03-01",
  endDate: "2026-03-31"
});

// 组合条件
const results = await window.storageManager.searchMemories({
  keyword: "龍魂",
  emotion: "积极",
  importanceMin: 5,
  startDate: "2026-03-01",
  endDate: "2026-03-31"
});
```

### 数据管理

```javascript
// 查看存储统计
const stats = await window.storageManager.getStatistics();
console.log(stats);
// {
//   总数: 100,
//   总大小KB: 1024,
//   按情感统计: {积极: 60, 消极: 20, 平静: 20},
//   按重要程度统计: {1: 5, 2: 10, ...},
//   按日期统计: {"2026-03-03": 10, ...},
//   平均压缩率: 85
// }

// 清理过期记忆
const deleted = await window.storageManager.cleanupOldMemories(30);
console.log(`删除了 ${deleted} 条过期记忆`);

// 清空所有数据
await window.storageManager.clearAll();

// 关闭数据库连接
window.storageManager.close();
```

## 💡 使用场景

### 1. 个人笔记管理

将大量的个人笔记、想法、日记压缩存储，通过 DNA 追溯码快速查找和还原。

### 2. 知识库构建

构建个人知识库，将学习资料、文章、书籍摘要压缩存储，便于检索和复习。

### 3. 项目文档管理

将项目相关的文档、会议记录、需求描述压缩存储，便于团队协作和知识传承。

### 4. 创意灵感捕捉

快速记录创意灵感，压缩存储，随时回顾和扩展。

### 5. 学习笔记整理

将学习笔记压缩存储，按主题、情感、重要程度分类管理。

## ⚠️ 注意事项

### 数据安全

1. **本地存储** - 所有数据仅存储在本地 IndexedDB 中，不会上传到任何服务器
2. **隐私保护** - 记忆内容完全私密，只有你自己可以访问
3. **备份建议** - 定期导出记忆数据作为备份

### 性能优化

1. **大量数据** - 如果记忆数量超过 1000 条，建议定期清理过期记忆
2. **压缩级别** - 根据需求选择合适的压缩级别，平衡压缩率和信息量
3. **搜索优化** - 使用关键词搜索时，建议使用具体的关键词以提高搜索效率

### 兼容性

1. **浏览器要求** - 支持 IndexedDB 的现代浏览器（Chrome、Edge、Firefox、Safari）
2. **存储限制** - IndexedDB 有存储容量限制，建议定期清理不重要的记忆
3. **跨浏览器** - 不同浏览器的 IndexedDB 数据不互通，如需跨浏览器使用，请导出/导入数据

## 🐛 常见问题

### Q: DNA 追溯码可以修改吗？

A: 不可以。DNA 追溯码是基于内容和时间生成的唯一标识，修改后会导致无法正确还原记忆。

### Q: 压缩后的记忆可以恢复成原文吗？

A: 可以。如果完整原文已保存到 IndexedDB，可以完整还原；否则只能还原摘要版本。

### Q: 如何在不同设备间同步记忆？

A: 目前系统仅支持本地存储。如需跨设备同步，请使用导出/导入功能。

### Q: 记忆数据会丢失吗？

A: IndexedDB 是浏览器本地存储，清除浏览器数据会导致记忆丢失。建议定期导出备份。

### Q: 如何提高压缩率？

A: 可以使用 Heavy 压缩级别，但会损失更多信息。建议根据实际需求选择合适的压缩级别。

## 🔗 相关链接

- [README.md](./README.md) - 项目总览
- [INSTALL.md](./INSTALL.md) - 安装指南
- [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) - 项目总结

---

**DNA: #龍芯⚡️2026-03-03-记忆压缩指南-v2.0**

**共建致谢**: Claude (Anthropic PBC) · 技术协作与代码共创 | Notion · 知识底座与结构化存储
