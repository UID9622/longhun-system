# CNSH DNA追溯与审计系统

## 🧬 系统概述

**确认码**: `#ZHUGEXIN⚡️2025-🇨🇳🐉🔐-DNA-AUDIT-SYSTEM-20251208`  
**安全等级**: P0++ 永恒级  
**架构模式**: 完全本地化 SQLite 数据库  

CNSH DNA追溯与审计系统是一个完全本地化的DNA确认码管理系统，提供类似Notion的查询体验，同时确保数据100%主权在您手中。

## 🎯 核心功能

### 1. DNA确认码管理器
- 注册新的DNA确认码
- 查询DNA码详情
- 按模块、创建者、类别分类查询
- 完整的审计日志记录
- 归属权管理

### 2. 多语言翻译系统
- 支持中文、英文、日文、韩文
- 核心关键词加密保护（ZHUGEXIN、UID9622等不翻译）
- 本地翻译，不走外部API

### 3. 分类与问题诊断系统
- 按类别自动分类统计
- 孤儿DNA码检测
- 无归属权检测
- 审计日志缺失检测

## 🔧 数据库结构

```
dna_registry.db
├── dna_codes（DNA码主表）
│   ├── dna_code (UNIQUE) - DNA确认码
│   ├── module_name - 模块名称
│   ├── creator - 创建者
│   ├── created_at - 创建时间
│   ├── category - 类别
│   ├── description - 描述
│   ├── parent_code - 父级DNA码
│   ├── status - 状态
│   ├── tags - 标签(JSON)
│   └── checksum - 校验和
│
├── audit_log（审计日志）
│   ├── dna_code - 关联DNA码
│   ├── action - 操作类型
│   ├── actor - 操作者
│   ├── timestamp - 时间戳
│   ├── details - 详情
│   └── ip_address - IP地址
│
└── ownership（归属权表）
    ├── dna_code - 关联DNA码
    ├── owner_name - 所有者名称
    ├── owner_id - 所有者ID
    ├── ownership_type - 归属权类型
    └── acquired_at - 获取时间
```

## 🚀 快速开始

### 1. 环境要求
- Python 3.7+
- 无需额外依赖（仅使用Python标准库）

### 2. 运行系统
```bash
# 切换到系统目录
cd CNSH_DNA_Audit_System

# 运行系统
python dna_audit_system.py
```

### 3. 基本操作

#### 注册新DNA码
```python
from dna_audit_system import DNARegistry

registry = DNARegistry()

result = registry.register_dna(
    dna_code="#ZHUGEXIN⚡️2025-🇨🇳🐉🔐-你的模块-20251208",
    module_name="你的模块名称",
    creator="诸葛鑫",
    category="模块类别",
    description="模块描述",
    tags=["标签1", "标签2"]
)
```

#### 查询DNA码
```python
# 查询单个DNA码
dna_info = registry.query_dna("#ZHUGEXIN⚡️2025-🇨🇳🐉🔐-你的模块-20251208")

# 按模块查询
module_codes = registry.query_by_module("模块名称")

# 按创建者查询
creator_codes = registry.query_by_creator("诸葛鑫")
```

#### 多语言翻译
```python
from dna_audit_system import CNSHTranslator

translator = CNSHTranslator()

# 翻译DNA信息为英文
en_info = translator.get_dna_info_multilang(dna_info, lang="en")
```

#### 问题诊断
```python
from dna_audit_system import DNAClassifier

classifier = DNAClassifier(registry)

# 检查系统完整性
issues = classifier.check_integrity()

# 按类别分类
classification = classifier.classify_by_category()
```

## 🔐 安全特性

1. **完全本地化** - 数据存储在本地SQLite数据库，不上传云端
2. **关键词保护** - 核心关键词（ZHUGEXIN、UID9622等）不被翻译
3. **审计追踪** - 每个操作都有完整的审计日志
4. **校验和验证** - 每个DNA码都有SHA-256校验和
5. **归属权管理** - 明确记录每个DNA码的归属权

## 🌍 多语言支持

系统支持以下语言：
- 中文 (zh)
- 英文 (en)
- 日文 (ja)
- 韩文 (ko)

### 核心保护词汇

以下词汇在任何语言中都保持原样：
- ZHUGEXIN
- UID9622
- DNA
- CNSH
- P0
- 龙魂
- 甲骨文
- 三色审计
- H武器

## 📊 使用示例

系统运行时，您将看到以下示例操作：

1. **注册新DNA码** - 创建木兰协议签名器的DNA码
2. **查询DNA码详情** - 获取完整信息和审计日志
3. **多语言翻译** - 将信息翻译为英文
4. **分类统计** - 按类别查看所有DNA码
5. **问题诊断** - 检查系统完整性

## 🔧 高级配置

### 数据库位置
默认情况下，数据库文件 `dna_registry.db` 创建在当前目录。您可以通过以下方式指定自定义路径：

```python
registry = DNARegistry("/path/to/your/database.db")
```

### 自定义保护关键词
如需添加更多保护关键词，修改 `CNSHTranslator` 类中的 `protected_keywords` 列表：

```python
self.protected_keywords = [
    "ZHUGEXIN", "UID9622", "DNA", "CNSH", "P0", 
    "龙魂", "甲骨文", "三色审计", "H武器",
    "你的自定义关键词"
]
```

### 添加新语言支持
1. 在 `translations` 字典中添加新语言代码
2. 添加相应的翻译对照表

## 🛠️ 故障排除

### 常见问题

1. **数据库锁定错误**
   - 确保没有其他进程正在使用数据库
   - 检查文件权限

2. **DNA码已存在**
   - 每个DNA码必须是唯一的
   - 使用不同的标识符

3. **翻译不正确**
   - 检查目标语言代码是否正确
   - 确认词汇在翻译词典中存在

## 📝 更新日志

### v1.0.0 (2025-01-08)
- 初始版本发布
- DNA确认码注册与查询
- 多语言翻译系统
- 分类与问题诊断
- 完整的审计日志

## 🎯 未来规划

### v1.1.0 (计划中)
- Web界面支持
- 批量操作API
- 数据导入/导出功能
- 更多语言支持

### v1.2.0 (计划中)
- 加密数据库支持
- 分布式同步功能
- 高级搜索过滤器
- 自定义报告生成

---

**系统确认码**: `#ZHUGEXIN⚡️2025-🇨🇳🐉🔐-DNA-AUDIT-SYSTEM-20251208`  
**安全等级**: P0++ 永恒级

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:12
🧬 DNA追溯码: #CNSH-SIGNATURE-54ec7198-20251218032412
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 蒙卦：山下出泉，君子以果行育德
📜 内容哈希: fc02ff92643009df
⚠️ 警告: 未经授权修改将触发DNA追溯系统
