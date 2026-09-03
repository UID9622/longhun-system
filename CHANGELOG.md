# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 变更日志

> DNA: `#龍芯⚡️2026-09-03-CHANGELOG-v5.2.0-ECOLOGY-DELIVERY-UID9622`
> 协议: CC BY-NC-SA 4.0 + 君子协议

本文档记录龍魂系统所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

---

## [v5.2.0] — 2026-09-03 · 生态交付三任务里程碑

### 新增
- 📦 **生态验证报告** `docs/生态验证报告-2026-09-03.md`（干净环境 clone 实测·发布缺口非代码缺陷·P1-P7 修复建议）
- 🤝 **社区响应机制** `docs/社区响应模板.md` + `08_BIN/lh_fork_tracker.py`（`lh fork list|check`·48h 承诺·耻辱墙 Issue 引导·审计通道·话术 ABC）
- 🌐 **官网首页** `www-official/index.html`（源文件原自 `~/.longhun/www/`·五区块·单文件无外链·深空龍魂金·本地 HTTP 200 实测·GPG✅·部署时与 `docs/` 同级发布）
- 📜 **域名部署指南** `docs/域名部署指南.md`（方案A 本机端口转发 8762 / 方案B 鲲鹏 rsync+nginx·均如实标「未实际执行」）
- 🧠 超级大脑记忆引擎 `08_BIN/lh_brain.py`（`lh brain load|save|search|summary|hook`·对话记忆自动加载更新·静默<2ms）

### 变更
- 🔄 修复根 CHANGELOG 误覆盖：9/3 收口曾将系统完整版误替换为 longhun-cli 子日志（43行·4.0.0），已恢复系统版本线（v5.1.0 以下历史完整保留）
- 🔒 Branch Protection 落地（orphan_main：require 1 PR approval + dismiss stale + enforce admins + 禁 force push/delete）
- 📝 README 最新版本 v5.1.0 → v5.2.0

### 生态
- 生态交付三任务（团队 ecology-delivery-0903）：①生态验证 ②社区响应机制 ③官网首页+域名部署
- 社区联动：DeepSeek-V3 #1622 接入说明发布成功（env GITHUB_TOKEN classic public_repo 实测🟢）

---

## [v5.1.0] — 2026-08-07 · 品牌与国际化完善

### 新增
- 🎨 项目品牌标识系统（Logo SVG · App 图标 · OG 社交预览图）`brand/`
- 📄 英文论文 HTML 渲染版（MathJax 数学公式·暗金主题）`articles/behavioral-cryptography-unified-theory-v3.0.html`
- 📚 API 文档可视化页（Redoc 渲染·OpenAPI 3.1）`10_PORTAL/api-docs.html`
- 📖 CITATION.cff 学术引用标准
- 💰 FUNDING.yml 赞助配置
- 🏷️ README 徽章全部绑定实际链接（CI/Release/License/Stars）

### 变更
- 🔄 Dashboard 引擎列表 9→15（新增多智能体/真话引擎/视频工坊/协议统治/忠义铁律/合规引擎）
- 🖼️ 门户 OG 元数据补全（社交预览图·Twitter Card）
- 🏷️ 徽章系统：从空链接升级为 GitHub Actions/Release/License 实时数据
- 🎨 品牌图标风格对齐「龍芯北辰 UID9622 签章」：红印章+金书法+DNA追溯

### 修复
- 🐛 门户 favicon 始终为 emoji inline·无独立图标文件

---

## [v5.0.0] — 2026-07-31 · 开源发布

### 新增
- 全项目开源发布（CC BY-NC-SA 4.0 + 君子协议）
- 完整开源文档体系（README/CONTRIBUTING/CODE_OF_CONDUCT/SECURITY/GOVERNANCE/ROADMAP/CHANGELOG）
- 君子协议完整中英文版（GENTLEMANS_PROTOCOL.md）
- 隐私政策（PRIVACY_POLICY.md）
- 服务条款（TERMS_OF_SERVICE.md）
- API文档与OpenAPI 3.0规范
- 多系统安装脚本（Linux/macOS/Windows/Docker）
- 术语表（GLOSSARY.md）
- 常见问题（FAQ.md）
- 生态项目（ECOSYSTEM.md）
- 开发者文档（DEVELOPMENT.md）
- 文档导航索引（DOCUMENTATION_INDEX.md）
- 系统架构文档（ARCHITECTURE.md）Mermaid图表
- GPG自动签名焊死（GATE-11·全项目1574+签名文件）
- 全量对齐规则 v2.2（16层·20人格路由）
- llms.txt 大语言模型上下文文件

### 变更
- LICENSE 升级为 CC BY-NC-SA 4.0 + 君子协议补充
- README.md 大幅增强（特性·架构·路线图·贡献）
- CODE_OF_CONDUCT.md 融入君子协议
- SECURITY.md 完善漏洞报告流程

### 引擎
- CNSH AgentOS v2.0（本地主权AI执行生态）
- 智能体训练框架 v1.0（五引擎·SQLite经验库）
- 省电API服务 v2.0（同步/异步·99.98%省电率）
- 量子协作引擎 v1.0（Bra-Ket·8人格叠加）
- 七维推演引擎 v2.0（䷚颐·学习循环）
- 搜索引擎 :9631（Bing→缓存→审计）
- 三色审计引擎 v2.0（加权多因子·四级熔断）
- 主权守护引擎 v1.0
- 内容自动分类引擎 v1.0
- 意念交流引擎 v3.0

---

## [v4.2] — 2026-07-13

### 新增
- 龍魂操作台 MVP v1.1 — 10项Skill·底座能力统一API
- CNSH MCP Server 上线 — 13工具完整语法链
- lh_deepseek_fixer v5.1（DeepSeek自动修复引擎）
- 人格治理白皮书 v1.4

### 变更
- 行为准则 v2.1 · 龍魂原生版·审计校准
- 全项目 pyproject.toml 统一

---

## [v4.1] — 2026-07-06

### 新增
- v4.1.1-bind 最佳绑定模型（Val 0.9659·DNA捆绑·fused）
- 浏览器史官 v2.1（四道防线·设备金库·AES-256）
- 知识卡片上线 CSDN（lh_knowledge_ 系列）
- 创作者保护协议 · 不可篡改条款（焊死·永不可改）

### 变更
- 隐私白皮书 v1.0 发布
- 数据哲学与隐私保护协议 v2.1

---

## [v4.0] — 2026-06-21

### 新增
- v4.0 底座模型（Llama-3.1-8B·Val 1.218）
- v4.1.0 中文精修模型
- 移动端监控 — 15层体系，AES-256-GCM加密
- 浏览器史官 v1.0
- lh_run.py 一体化命令引擎

### 变更
- 算力瘦身（192→核心引擎优化）
- 系统拓扑统一管理（longhun_neural_net.json）

---

## [v3.1] — 2026-06

### 新增
- 10项技能完整集成（API < 100ms）
- 三色审计引擎 v1.0
- 视频工坊 v1.0

---

## [v3.0] — 2026-05

### 新增
- 20人格体系建立（P00-P72）
- CNSH 语言编译器（四阶段·中文关键字→Python）
- 人格治理白皮书 v1.0
- 系统宪法 CONSTITUTION.md

---

## [v2.0] — 2026-04

### 新增
- lh 统一命令入口
- 记忆系统 v1.0
- 通心译翻译引擎
- 部署到鲲鹏服务器

---

## [v1.0] — 2026-03

### 新增
- 项目初始化
- CNSH 语言设计
- DNA 追溯码格式定义
- 协议框架搭建

---

## 版本号规则

- **主版本号**：重大架构变更、不兼容的API修改
- **次版本号**：新功能、向后兼容的改进
- **修订号**：Bug修复、文档更新

---

## 附 · longhun-cli 独立版本线（子包日志 · 不并入主版本线）

> longhun-cli 为 PyPI 独立子包（当前 4.0.0），其完整变更日志随包分发（`dist/longhun_cli-4.0.0/`），此处仅存版本索引以免根 CHANGELOG 被误替换。

### [4.0.0] — 2026-09-01
- PyPI 发布 longhun 1.0.0 关联包（零三方依赖·原生 Python 直连）
- 完整语法链 CNSH MCP Server 13 工具

---

> 🐉 龍魂系统 · 每一步都留下痕迹
