# DNA: #龍芯⚡️2026-08-31-QUANTUM-TEMPLATE-03-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# 来源: Notion「🧬 量子模板引擎」库


# 🏷️ GitHub Release Notes 发版说明模板 v1.0

> 适用范围：所有 UID9622 开源仓库发版说明 | Scope: All UID9622 open source repository releases

---


## 📋 使用说明 / How to Use

1. 复制下方模板内容到 GitHub Release 描述框
1. 替换 [版本号]、[日期]、[功能描述] 等占位符
1. 删除本次发版中不适用的章节
1. 中文在前，英文在后

---


## 🚀 发版模板 / Release Template


```markdown
## [版本号] - [YYYY-MM-DD]

> 🐉 DNA: #龍芯⚡️[YYYY-MM-DD]-[主题]-[版本号]-UID9622

### ✨ 新功能 / New Features

- **[功能名称]**：[简短描述功能的作用和价值]
  > *[Feature Name]: [Brief description of the feature's purpose and value]*

### 🐛 Bug 修复 / Bug Fixes

- 修复了 [问题描述] (#Issue号)
  > *Fixed [issue description] (#issue_number)*

### 🔧 改进优化 / Improvements

- [改进内容描述]
  > *[Improvement description]*
- 性能优化：[优化说明]
  > *Performance: [optimization details]*

### 📦 依赖更新 / Dependency Updates

- 升级 `[依赖名]` 从 `[旧版本]` 到 `[新版本]`
  > *Upgraded `[dependency]` from `[old]` to `[new]`*

### ⚠️ 破坏性变更 / Breaking Changes

> ⚠️ 如无破坏性变更，删除此章节 / Remove if no breaking changes

- **[变更内容]**：[迁移方式说明]
  > *[Change]: [Migration guide]*

### 📚 文档更新 / Documentation

- 更新了 [文档名称]
  > *Updated [document name]*

### 🙏 致谢 / Acknowledgements

感谢以下贡献者 / Thanks to the following contributors:
@[GitHub用户名] - [贡献内容]

---

**完整更新日志 / Full Changelog**: https://github.com/UID9622/[仓库名]/compare/[上一版本]...[本版本]
```


---


## 📌 版本号规范 / Versioning Convention

遵循 语义化版本 SemVer：


---


## ✅ 发版前检查清单 / Pre-Release Checklist

- [ ] CHANGELOG.md 已更新 [Unreleased] → [版本号]
- [ ] 所有测试通过（pytest / npm test）
- [ ] 版本号已在 pyproject.toml / package.json 中更新
- [ ] PR 已合并到 main 分支
- [ ] Tag 已打：git tag vX.Y.Z && git push --tags
- [ ] Release Notes 中英双语已填写
- [ ] 如有 PyPI 包：python -m build && twine upload dist/*

---

模板维护者：@UID9622 · DNA: #龍芯⚡️2026-08-31-ReleaseNotes-v1.0-UID9622
