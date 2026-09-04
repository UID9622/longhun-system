# DNA: #龍芯⚡️2026-08-31-QUANTUM-TEMPLATE-06-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# 来源: Notion「🧬 量子模板引擎」库


## 🎯 模板定位

遵循 Keep a Changelog 规范和语义化版本的标准变更日志模板。让每一次发布都有迹可循，让用户知道升级会发生什么。

> 理念：不记录变更，就是不尊重用户的时间。

---


## 📐 语义化版本速记（SemVer）


```javascript
版本号格式：MAJOR.MINOR.PATCH（主.次.修）

MAJOR（主版本）：有不兼容的 API 变更 → 用户必须修改代码
MINOR（次版本）：新增向下兼容的功能 → 用户无需修改代码
PATCH（修订版）：修复向下兼容的 Bug  → 用户无需修改代码

示例：
  1.0.0 → 1.0.1  修复了一个崩溃 Bug
  1.0.1 → 1.1.0  新增了一个 API 方法
  1.1.0 → 2.0.0  重命名了核心类（Breaking Change!）
```

预发布版本：

- 1.0.0-alpha.1 — 内部测试
- 1.0.0-beta.1  — 公开测试
- 1.0.0-rc.1    — 候选发布

---


## 📄 CHANGELOG.md 模板正文


```markdown
# 变更日志 | Changelog

本文件记录 **[项目名称]** 的所有重要变更。

All notable changes to **[Project Name]** will be documented in this file.

格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，  
版本遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

This project adheres to [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**DNA:** `#龍芯⚡️项目名-CHANGELOG-v1.0-UID9622`

---

## [Unreleased · 未发布]

### ✨ 新增 | Added
- [新功能描述 | New feature description]

### 🔄 变更 | Changed
- [行为变更描述 | Behavior change description]

### 🗑️ 废弃 | Deprecated
- [即将在未来版本移除的功能 | Features to be removed in future]

### ❌ 移除 | Removed
- [已移除的功能 | Removed features]

### 🐛 修复 | Fixed
- [Bug 修复描述 | Bug fix description]

### 🔒 安全 | Security
- [安全漏洞修复 | Security vulnerability fixes]

---

## [2.0.0] - 2026-08-31

> ⚠️ **Breaking Changes** — 升级前请阅读迁移指南 | Please read migration guide before upgrading  
> 📖 [迁移指南 / Migration Guide](./docs/MIGRATION_v2.md)

**DNA:** `#龍芯⚡️2026-08-31-项目名-v2.0.0-UID9622`

### ✨ 新增 | Added
- 🌍 多语言支持（中/英/日/韩） | Multilingual support (CN/EN/JA/KR)
- 📡 新增 REST API v2 端点 | New REST API v2 endpoints
- 🐉 DNA 追溯码 v∞ 格式支持 | DNA trace code v∞ format support

### 🔄 变更 | Changed
- ⚠️ **[BREAKING]** `LongHunAdapter()` 构造函数参数重命名：
  - `user_id` → `uid`（必须更新 | Must update）
  - `machine_id` → `device`（必须更新 | Must update）
- 性能提升：`wrap()` 方法速度提升 40% | Performance: `wrap()` 40% faster

### 🐛 修复 | Fixed
- 修复 Unicode 字符导致 DNA 生成失败的问题 | Fix DNA generation failure with Unicode chars
- 修复 Windows 下时区计算错误 | Fix timezone calculation error on Windows

### 🔒 安全 | Security
- 升级依赖版本，修复已知 CVE | Upgrade dependencies, fix known CVEs

---

## [1.2.1] - 2026-07-24

**DNA:** `#龍芯⚡️2026-07-24-项目名-v1.2.1-UID9622`

### 🐛 修复 | Fixed
- 修复 `validate()` 在空 payload 时崩溃 | Fix `validate()` crash on empty payload
- 修复文档中的错误代码示例 | Fix incorrect code examples in docs

---

## [1.2.0] - 2026-06-18

**DNA:** `#龍芯⚡️2026-06-18-项目名-v1.2.0-UID9622`

### ✨ 新增 | Added
- 新增 `get_schemas()` 方法返回 JSON Schema | Add `get_schemas()` to return JSON Schema
- 新增批量处理支持 | Add batch processing support
- 新增详细错误消息 | Add detailed error messages

### 🔄 变更 | Changed
- 改进 `wrap()` 性能，减少 30% 内存占用 | Improved `wrap()` performance, 30% less memory

---

## [1.0.0] - 2026-01-01

**DNA:** `#龍芯⚡️2026-01-01-项目名-v1.0.0-UID9622`

### ✨ 新增 | Added
- 🎉 首次正式发布 | Initial stable release
- 核心 `LongHunAdapter` 类 | Core `LongHunAdapter` class
- DNA 追溯码生成 | DNA trace code generation
- 七因子行为审计 | Seven-factor behavioral audit
- 零依赖实现 | Zero external dependencies

---

<!-- 版本链接 | Version Links -->
[Unreleased]: https://github.com/UID9622/PROJECT/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/UID9622/PROJECT/compare/v1.2.1...v2.0.0
[1.2.1]: https://github.com/UID9622/PROJECT/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/UID9622/PROJECT/compare/v1.0.0...v1.2.0
[1.0.0]: https://github.com/UID9622/PROJECT/releases/tag/v1.0.0
```


---


## 🔧 自动化工具：生成变更条目


```bash
# 从 Git log 自动提取变更（基于 Conventional Commits）
git log --oneline --no-merges v1.2.1..HEAD | \
  grep -E '^[a-f0-9]+ (feat|fix|docs|perf|refactor|security)' | \
  awk '{
    if ($2 == "feat") prefix = "✨ 新增"
    else if ($2 == "fix") prefix = "🐛 修复"
    else if ($2 == "docs") prefix = "📖 文档"
    else if ($2 == "perf") prefix = "⚡ 性能"
    else if ($2 == "security") prefix = "🔒 安全"
    else prefix = "🔄 变更"
    print "- [" prefix "] " $0
  }'
```


---

> 💬 DNA： #龍芯⚡️2026-08-31-CHANGELOG规范模板-v1.0-UID9622