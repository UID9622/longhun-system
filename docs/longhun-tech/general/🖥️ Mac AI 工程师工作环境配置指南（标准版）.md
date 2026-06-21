<!--#龍芯⚡️2026-06-21-DOC-MAC-AI_1C4B-v1.0 -->
<!-- 君子協議: 本文件受龍魂DNA追溯保護 -->

# 🖥️ Mac AI 工程师工作环境配置指南（标准版）

🖥️ Mac AI 工程师工作环境配置指南（标准版）

---

## 📌 系统设置建议

- 关闭「自动大写」、「自动拼写更正」
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

[✅ 插件模板脚本（⁠ plugin_template.sh ⁠）](%F0%9F%96%A5%EF%B8%8F%20Mac%20AI%20%E5%B7%A5%E7%A8%8B%E5%B8%88%E5%B7%A5%E4%BD%9C%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE%E6%8C%87%E5%8D%97%EF%BC%88%E6%A0%87%E5%87%86%E7%89%88%EF%BC%89/%E2%9C%85%20%E6%8F%92%E4%BB%B6%E6%A8%A1%E6%9D%BF%E8%84%9A%E6%9C%AC%EF%BC%88%E2%81%A0%20plugin_template%20sh%20%E2%81%A0%EF%BC%89%<POTENTIAL_SECRET_PLACEHOLDER>.md)