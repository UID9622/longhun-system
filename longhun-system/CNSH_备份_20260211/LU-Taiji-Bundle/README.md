# LU-Taiji Bundle v2.1

**DNA:** #ZHUGEXIN⚡️2025-01-27-LU-TAIJI-BUNDLE-v2.1
**License:** CC BY-NC-SA 4.0

基于龙魂 DNA 追溯与太极哲学的完整知识组织系统部署包。

## 快速开始

```bash
# 一键初始化
bash scripts/quickstart.sh
```

## 目录结构

```
LU-Taiji-Bundle/
├── manifest.json          # 包清单
├── placeholders.json      # 占位符配置（安全中心）
├── content/
│   ├── LU-Taiji-2.1.json  # 内容模型
│   └── LU-Taiji-Graph.json # 知识图谱
├── scripts/
│   ├── validate_schema.mjs  # Schema 验证
│   ├── checksum.sh         # 校验和生成
│   ├── import_notion.mjs   # Notion 导入
│   └── quickstart.sh       # 快速启动
└── docs/
    └── README.md           # 详细文档
```

## 安全配置

1. 创建 `.env` 文件：
```bash
NOTION_API_KEY=your_integration_token_here
NOTION_DATABASE_ID=your_database_id_here
```

2. 从 [Notion Integrations](https://www.notion.so/my-integrations) 获取 API Key
3. 从 Notion 数据库 URL 提取 Database ID

## 验证

```bash
# Schema 验证
node scripts/validate_schema.mjs

# 生成校验和
bash scripts/checksum.sh

# 导入到 Notion
node scripts/import_notion.mjs
```

## 作者

- Lucky·UID9622 (主创)
- 开源大师 (技术负责)
- 工匠 (工程实施)
