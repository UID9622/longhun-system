> **P0焊死**: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
# 🖥️ Mac AI 工程师工作环境配置指南（标准版）

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技术文档 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-DOC-MAC-AI_1C4B-v1.0`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

<!--#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-DOC-MAC-AI_1C4B-v1.0 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# 🖥️ Mac AI 工程师工作环境配置指南（标准版）

🖥️ Mac AI 工程师工作环境配置指南（标准版）

---

## 📌 系统设置建议

- 关闭“自动大写”、“自动拼写更正”
- 启用开发者工具（Safari、终端）
- 快捷键自定义（建议使用 Karabiner）

---

## 🧩 必装插件（效率+AI）

| 插件名 | 功能简述 | 安装方式 |
| --- | --- | --- |
| Raycast | 快捷命令执行器 | brew install --cask raycast |
| iTerm2 | 替代终端，支持分屏 | brew install --cask iterm2 |
| Warp | AI 辅助终端 | 官网下载安装 |
| Obsidian | 本地知识库管理 | brew install --cask obsidian |
| Notion | 云端协作+数据库 | Mac App Store 安装 |
| 1Password | 密码管理 | 官网下载，支持 CLI |

---

## 🧠 AI 工具集推荐

- ChatGPT 插件（浏览器扩展）
- Whisper 本地语音识别
- Ollama / LM Studio（本地大模型部署）

---

## 🧰 常用脚本（建议加到 alias）

```bash
# 打开 Notion 工作区
alias notion='open -a "Notion"'

# 快速清理缓存
alias cleanmac='sudo purge && echo "🧹 清理完成"'

# 一键同步脚本
alias syncai='sh ~/scripts/ai_sync.sh'

```

使用方法：复制整个代码块后，在终端执行：

```bash
pbpaste >> ~/.zshrc && source ~/.zshrc
```

或者直接运行（临时生效）：

```bash
eval "$(pbpaste)"
```

---

## 📂 脚本文件建议结构

📁 scripts/

- ├── [setup.sh](http://setup.sh/)          # 初始化环境
- ├── ai_sync.sh        # 同步本地→云
- ├── update_tools.sh   # 检查并更新所有工具

---

## ✅ 建议执行顺序

1. 安装 Homebrew
2. 安装插件
3. 配置 alias（可写入 ~/.zshrc）
4. 建立 scripts 文件夹
5. 下载并运行辅助脚本

[✅ 插件模板脚本（ plugin_template.sh ）](%F0%9F%96%A5%EF%B8%8F%20Mac%20AI%20%E5%B7%A5%E7%A8%8B%E5%B8%88%E5%B7%A5%E4%BD%9C%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE%E6%8C%87%E5%8D%97%EF%BC%88%E6%A0%87%E5%87%86%E7%89%88%EF%BC%89/%E2%9C%85%20%E6%8F%92%E4%BB%B6%E6%A8%A1%E6%9D%BF%E8%84%9A%E6%9C%AC%EF%BC%88%E2%81%A0%20plugin_template%20sh%20%E2%81%A0%EF%BC%89%<POTENTIAL_SECRET_PLACEHOLDER>.md)

---

## 摘要

（请在此用不超过 256 字说明本文档的核心内容、性质与局限。）

## 关键词

（请列出 5–10 个关键词，中英文对照优先。）

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] （请填写）
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 诚实局限

1. （请列出本分析的第一条局限或不确定性。）
2. （请列出第二条。）
3. （请列出第三条。）

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |

## 分类标签

- 总纲模块：（请勾选，例如 #知识矩阵 #安全域）
- 对外状态：（请勾选，例如 #Gitee #GitHub #CSDN）
- 审计色：#黄色待审

## DNA 签名

```
#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-DOC-MAC-AI_1C4B-v1.0
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
