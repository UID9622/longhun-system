# DNA: #龍芯⚡️2026-08-31-QUANTUM-TEMPLATE-04-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# 来源: Notion「🧬 量子模板引擎」库


## 🎯 模板定位

为所有开源仓库提供标准化 GitHub Issue 模板，放入 .github/ISSUE_TEMPLATE/ 目录，让全球贡献者用统一格式反馈问题——零门槛参与，有序协作。


---


## 📁 目录结构


```javascript
.github/
└── ISSUE_TEMPLATE/
    ├── bug_report.md          # Bug 报告
    ├── feature_request.md     # 功能请求
    ├── docs_feedback.md       # 文档反馈
    └── config.yml             # Issue 选择器配置
```


---


## 🐛 文件1：bug_report.md


```markdown
---
name: 🐛 Bug 报告 | Bug Report
about: 报告一个可复现的错误 | Report a reproducible bug
title: '[BUG] '
labels: ['bug', 'needs-triage']
assignees: ''
---

## 🐛 Bug 描述 | Description

<!-- 用一两句话描述这个 Bug | Describe the bug in 1-2 sentences -->

## 📋 复现步骤 | Steps to Reproduce

1. 执行 `...` | Run `...`
2. 输入 `...` | Input `...`
3. 看到错误 `...` | See error `...`

## ✅ 期望行为 | Expected Behavior

<!-- 应该发生什么 | What should happen -->

## ❌ 实际行为 | Actual Behavior

<!-- 实际发生了什么 | What actually happens -->

## 🖥️ 环境信息 | Environment

| Item | Value |
|------|-------|
| OS | [ ] Windows [ ] macOS [ ] Linux [ ] Android |
| Python | x.x.x |
| Package Version | x.x.x |
| Branch/Commit | main / `abc1234` |

## 📋 错误日志 | Error Log

```

[粘贴完整错误信息 / Paste full error here]


```javascript

## 📎 附加信息 | Additional Context

<!-- 截图、相关 Issue、参考链接等 | Screenshots, related issues, links -->

---

> **DNA:** 本 Issue 受龍魂三色审计保护 | This Issue is protected by LongHun Tricolor Audit  
> **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
```


---


## ✨ 文件2：feature_request.md


```markdown
---
name: ✨ 功能请求 | Feature Request
about: 建议新功能或改进 | Suggest a new feature or improvement
title: '[FEAT] '
labels: ['enhancement', 'needs-discussion']
assignees: ''
---

## ✨ 功能描述 | Feature Description

<!-- 用一句话描述你想要的功能 | Describe the feature in one sentence -->

## 💡 解决的问题 | Problem it Solves

<!-- 这个功能解决了什么痛点？ | What pain point does this solve? -->
**目前的情况 / Current situation:**  
当我尝试 `...` 时，我需要 `...`  
When I try to `...`, I need to `...`

## 🎯 期望的解决方案 | Proposed Solution

<!-- 你期望如何实现这个功能？ | How would you like this to work? -->

## 🔄 替代方案 | Alternatives Considered

<!-- 你考虑过哪些替代方案？ | What alternatives have you considered? -->

## 📊 影响范围 | Impact

- [ ] 核心功能 | Core functionality
- [ ] 文档 | Documentation
- [ ] 性能 | Performance
- [ ] 安全 | Security
- [ ] 可访问性 | Accessibility

## 🌍 受益人群 | Who Benefits

<!-- 哪些用户会受益？有多少人？ | Who benefits? How many users? -->

## 📎 参考资料 | References

<!-- 相关链接、截图、原型图等 | Links, screenshots, mockups -->
```


---


## 📖 文件3：docs_feedback.md


```markdown
---
name: 📖 文档反馈 | Documentation Feedback
about: 报告文档错误或建议改进 | Report doc errors or suggest improvements
title: '[DOCS] '
labels: ['documentation']
assignees: ''
---

## 📍 文档位置 | Document Location

- **文件 / File:** `docs/xxx.md` 或链接 / or URL
- **章节 / Section:** [具体章节 / Specific section]

## 🔴 问题描述 | Issue Description

- [ ] 内容有误 | Incorrect content
- [ ] 内容过时 | Outdated content
- [ ] 缺少内容 | Missing content
- [ ] 翻译问题 | Translation issue
- [ ] 格式问题 | Formatting issue

**具体说明 / Details:**
<!-- 描述具体问题 | Describe the specific issue -->

## ✅ 建议改进 | Suggested Improvement

<!-- 你建议如何改进？ | How would you improve it? -->

## 🌍 语言 | Language

- [ ] 中文 / Chinese
- [ ] English
- [ ] 其他 / Other: ___
```


---


## ⚙️ 文件4：config.yml（Issue 选择器）


```yaml
blank_issues_enabled: false
contact_links:
  - name: 💬 社区讨论 | Community Discussion
    url: https://github.com/UID9622/longhun-system/discussions
    about: 一般性问题和想法 | General questions and ideas
  - name: 🔐 安全漏洞 | Security Vulnerability
    url: https://github.com/UID9622/longhun-system/security/advisories/new
    about: 请通过安全通道报告 | Please report via secure channel
  - name: 📓 Notion 知识库 | Knowledge Base
    url: https://uid9622.notion.site
    about: 完整文档和教程 | Full docs and tutorials
```


---


## 🚀 一键部署脚本


```bash
#!/bin/bash
# 在任意仓库根目录执行，自动创建 Issue 模板
# DNA: #龍芯⚡️2026-08-31-Issue模板部署-v1.0

mkdir -p .github/ISSUE_TEMPLATE

# 从龍魂模板库拉取
curl -sL https://raw.githubusercontent.com/UID9622/longhun-system/orphan_main/.github/ISSUE_TEMPLATE/bug_report.md \
  > .github/ISSUE_TEMPLATE/bug_report.md

curl -sL https://raw.githubusercontent.com/UID9622/longhun-system/orphan_main/.github/ISSUE_TEMPLATE/feature_request.md \
  > .github/ISSUE_TEMPLATE/feature_request.md

curl -sL https://raw.githubusercontent.com/UID9622/longhun-system/orphan_main/.github/ISSUE_TEMPLATE/config.yml \
  > .github/ISSUE_TEMPLATE/config.yml

echo "✅ Issue 模板已部署！"
```


---

> 💬 DNA： #龍芯⚡️2026-08-31-GitHub-Issue模板集-v1.0-UID9622