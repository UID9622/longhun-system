# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 贡献指南

> DNA: `#龍芯⚡️2026-07-06-CONTRIBUTING-CREATE-v1.0-D9A4C1E8`

> **⚖️ 法律适用声明**：龍魂系统及其所有子项目、协议、文档，均以中华人民共和国法律为最高准则。贡献者提交的代码、文档及其他内容，均受 `LICENSE` 第七节（适用法律与争议解决）约束。任何与本系统相关的争议，均适用中国法律。

## 欢迎贡献

感谢你对龍魂系统的关注！龍魂系统是一个中国自主可控的 AI 行为治理框架与数字主权基础设施。

## 贡献方式

### 1. 报告问题

发现 Bug 或有改进建议？请通过以下方式报告：

- 详细描述问题或建议
- 提供复现步骤（如适用）
- 注明操作系统和 Python 版本

### 2. 提交代码

#### 开发环境准备

```bash
# 克隆仓库
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system

# 安装开发依赖
pip install -e ".[dev]"

# 安装 pre-commit 钩子
pre-commit install
```

#### 代码规范

1. **CNSH 命名规范**：变量命名遵循 `CNSH-PROTOCOL.md` 中的规则
2. **龍字必须繁体**：代码和文档中 `龍` 字必须使用繁体，简体 `龍` 视为不规范
3. **DNA 追溯码**：所有新文件必须包含 DNA 追溯码头部注释
4. **Python 风格**：遵循 `ruff` 配置（line-length=120）
5. **类型注解**：关键函数建议添加类型注解

#### 提交规范

```bash
# 提交信息格式
<类型>: <简短描述>

# 类型包括：
# feat:     新功能
# fix:      错误修复
# docs:     文档更新
# refactor: 代码重构（不改变功能）
# test:     添加或修改测试
# chore:    构建/工具/依赖更新
# audit:    审计相关
# security: 安全相关

# 示例
git commit -m "feat: 添加河图洛书 DNA 生成器"
git commit -m "fix: 修复三色审计引擎边界条件"
git commit -m "docs: 更新 API 文档"
```

### 3. 编写测试

- 测试目录：`tests/`
- 测试框架：pytest
- 运行测试：`pytest tests/`
- 覆盖率要求：新增代码应包含对应测试

### 4. 文档贡献

- 文档使用 Markdown 格式
- 文件命名使用下划线 `_` 连接
- 重要的架构文档需要包含 DNA 追溯码

## 审查流程

1. 提交前运行 `pre-commit run --all-files` 确保代码质量
2. 提交前运行 `pytest` 确保测试通过
3. 提交 PR 后等待审查
4. 所有变更需要通过三色审计

## 🏷 Good First Issue

如果你是第一次贡献，这些是最适合入手的任务——我们标注了 `good first issue` 标签：

1. **文档翻译** — 将中文文档翻译为英文（或反过来）
2. **添加单元测试** — 为现有模块补充测试用例
3. **修复 ruff 提示** — 运行 `ruff check` 并修复代码风格问题
4. **完善 README** — 补充模块的使用示例
5. **CNSH 示例** — 用 CNSH 语言写示例程序放到 `examples/`
6. **错误信息优化** — 让报错信息更友好、更易理解
7. **安装脚本测试** — 在不同系统上测试 `install.sh`
8. **日志格式统一** — 统一各模块的日志输出格式
9. **配置文件模板** — 为 `.env.example` 补充说明注释
10. **FAQ 整理** — 从 Discussions 中收集常见问题整理成 FAQ

👉 在 [Issues](https://github.com/UID9622/longhun-system/issues?q=label%3A%22good+first+issue%22) 页面找到标记 `good first issue` 的任务，评论说"我来做"即可认领。

## 🤝 贡献者荣誉墙

所有贡献者都会被收录进 README 的贡献者名单。贡献包括但不限于：
- 提交代码（PR）
- 报告 Bug（Issue）
- 改进文档
- 回答问题（Discussions）
- 分享使用案例

## 社区守则

- 尊重原创作者 UID9622（诸葛鑫·Lucky）的数字主权
- 讨论聚焦技术，避免政治敏感话题
- 建设性批评，尊重他人劳动

---

> 龍魂系统·数据主权归于人民 🐉
