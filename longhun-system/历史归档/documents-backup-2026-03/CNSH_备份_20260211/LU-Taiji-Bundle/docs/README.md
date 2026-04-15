# LU-Taiji Bundle 详细文档

## DNA 追溯

- **Bundle ID:** LU-Taiji-Bundle-v2.1.0
- **DNA Code:** #ZHUGEXIN⚡️2025-01-27-LU-TAIJI-BUNDLE-v2.1
- **确认码:** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

## 模型说明

### LU-Taiji 太极知识模型

基于太极哲学的知识组织系统，包含：

1. **太极之源 (Wuji)**: 一切知识的起点
2. **阴 (Yin)**: 收藏、内化、柔顺
3. **阳 (Yang)**: 创造、外化、刚健
4. **阴阳交互**: 动态平衡与转化

### 知识图谱

7 个节点 + 11 条边，完整映射阴阳关系与应用场景。

## 脚本说明

### validate_schema.mjs

验证 JSON 文件是否符合 schema 定义：
- manifest.json 格式验证
- 内容模型结构验证
- 图数据结构验证
- 占位符配置验证

### checksum.sh

生成 SHA256 校验和：
- 遍历所有 JSON/JS/Shell 文件
- 计算每个文件的 SHA256
- 更新 manifest.json 中的 checksum 字段
- 生成 CHECKSUMS.txt 和 CHECKSUMS.sha256

### import_notion.mjs

将内容导入到 Notion：
- 支持环境变量配置
- 安全的占位符替换
- Dry-run 模式（默认）
- 实际导入需要配置 API Key

### quickstart.sh

一键初始化：
1. 验证 schema
2. 生成校验和
3. 设置执行权限
4. 创建 .env 模板

## 安全指南

### 占位符管理

所有敏感信息通过 `placeholders.json` 集中管理：
- 禁止直接在代码中硬编码密钥
- 使用环境变量或 .env 文件
- 将 .env 添加到 .gitignore

### 校验和验证

部署前验证：
```bash
# 生成校验和
bash scripts/checksum.sh

# 验证文件完整性
shasum -a 256 -c CHECKSUMS.sha256
```

### 完整性检查

使用提供的校验和文件验证 Bundle 完整性。

## 使用场景

1. **知识管理**: 用太极思想组织知识
2. **决策制定**: 考虑阴阳两面
3. **个人成长**: 保持动静平衡
