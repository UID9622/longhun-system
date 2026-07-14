# 贡献指南

## 提交前必读

1. 必须遵守 [龍魂宪法](../../../../01_protocols/BEICHEN-MOTHER-PROTOCOL-v2.0.md)
2. 不得引入境外依赖或上传云端的服务
3. 所有代码变更必须包含 DNA 锚定或主权声明
4. 不修改底座锚点（369/河图洛书/易经/道德经等）

## 开发流程

```bash
cd editors/codebuddy/<extension-name>
npm install
npm run watch    # 开发模式
npm run compile  # 生产编译
npx vsce package # 打包 VSIX
```

## 提交规范

- 提交信息使用中文
- 包含 DNA 追溯码
- 大改动先开 Issue 讨论

## 行为准则

- 为人民服务
- 数据主权归用户
- 技术服务于中国自主可控
