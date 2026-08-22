# 🐉 龍魂 · 多模型终端写作引擎 v1.0

**DNA:** `#龍芯⚡️丙午·丙申·丁酉·庚子·䷉履-TERMINAL-WRITER-UID9622`  
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
**三色:** 🟢 通过  
**类型:** 系统底座 / 多模型写作 / 自动触发  
**别名:** `terminal-writer`, `lh-write`, `多模型写作`, `终端写作`

---

## 一句话

在终端里一键调用 DeepSeek / Kimi / CodeBuddy / Ollama / 自定义模型 进行写作，模型装死自动切换，文件保存或提交前自动触发补全。

---

## 三句话

1. **多模型融合**：DSH（鲲鹏本地）→ Ollama → Kimi API → CodeBuddy VSCode → 自定义模型，按可用性自动回退。
2. **主权网关**：8 秒超时、拒绝/超时自动记录耻辱墙、切换下一个模型，龍魂是主子，AI 是工具。
3. **自动触发**：检测到 `TODO/FIXME/待补充` 或文件过短、git commit 前，自动调用写作引擎补全内容。

---

## 技术栈

| 组件 | 路径 | 依赖 |
|:---|:---|:---|
| 终端写作引擎 | `05_ENGINES/lh_terminal_writer.py` | 纯 Python + SQLite |
| 命令封装 | `deploy/deepseek-harness-kunpeng/scripts/lh-dsh` | bash |
| 配置文件 | `~/.longhun/configs/terminal-writer.yaml` | yaml |
| 系统提示词 | `~/.longhun/configs/longhun-system-prompt.md` | markdown |
| 耻辱墙日志 | `.state/terminal_writer/writer.sqlite` | SQLite |

---

## 快速命令

```bash
# 直接调用（自动故障转移）
python3 05_ENGINES/lh_terminal_writer.py ask "帮我写一段龍魂系统介绍"

# 通过 lh-dsh（推荐）
lh-dsh write "帮我写一段龍魂系统介绍"

# 自动触发文件写作
lh-dsh write-auto ./README.md

# 查看模型状态
python3 05_ENGINES/lh_terminal_writer.py status

# 耻辱墙看板：装死排行 + 最近10条记录
lh-dsh shame-wall

# 模型健康检查：测试所有已启用模型
lh-dsh health

# 统计看板：调用次数/成功率/平均耗时/装死
lh-dsh stats

# 查看/修改配置
python3 05_ENGINES/lh_terminal_writer.py config
python3 05_ENGINES/lh_terminal_writer.py config --set providers.kimi.enabled=true

# git commit 前自动触发（供钩子调用）
python3 05_ENGINES/lh_terminal_writer.py pre-commit
```

> **看板三件套（v1.2）**：`shame-wall` 看哪个模型最装死、`health` 提前发现模型不可用、`stats` 一屏看全调用统计。三个命令都从 `.state/terminal_writer/writer.sqlite` 读取真实数据。

---

## 环境变量

```bash
# 启用 Kimi
export KIMI_API_KEY=sk-...

# 启用自定义模型
export CUSTOM_MODEL_URL=https://your-model.com/v1/chat/completions
export CUSTOM_API_KEY=sk-...
```

---

## 关联文件

- 引擎实现：`05_ENGINES/lh_terminal_writer.py`
- 配置模板：`deploy/deepseek-harness-kunpeng/configs/terminal-writer.yaml`
- 命令封装：`deploy/deepseek-harness-kunpeng/scripts/lh-dsh`
- 部署方案：`deploy/deepseek-harness-kunpeng/README.md`
- 主权网关：`03_KNOWLEDGE_GRAPH/03_龍魂主权网关自动硬控协议_☯UID9622..._SOVEREIGN-CTRL-v1.0.md`

---

*归档于 龍魂知识图谱 · 03_KNOWLEDGE_GRAPH*
