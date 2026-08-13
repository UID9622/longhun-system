# Mac安装Ollama（AI引擎）

> Notion URL: https://app.notion.com/p/Mac-Ollama-AI-a586614ea2b34783b2188325c3ed9ddc
> Created: 2025-12-19T17:54:00.000Z
> Last edited: 2026-07-01T15:22:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
## ⚠️ 重要提示：Mac安装方式不同
你遇到的错误是因为那个命令是给Linux系统用的。Mac需要用另一种方式安装。
## ✅ Mac正确安装步骤
1. 方式1：直接下载安装包（推荐，最简单）
1. 方式2：用Homebrew安装（如果你装了Homebrew）
## 🔧 安装完成后
无论用哪种方式，安装完成后都要在终端执行：
```bash
ollama pull qwen:7b-chat
```
这个命令会下载AI模型（约4GB），需要等10分钟左右。
## ✅ 验证安装
下载完成后，在终端输入：
```bash
ollama list
```
如果能看到qwen:7b-chat，就说明全部成功了！
