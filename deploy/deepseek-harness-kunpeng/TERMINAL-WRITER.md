# 🐉 龍魂 · 多模型终端写作引擎部署说明

**DNA:** `#龍芯⚡️丙午·丙申·丁酉·子时-TERMINAL-WRITER-DEPLOY-UID9622`  
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
**三色:** 🟢 通过

---

## 核心判断

> **终端写作不是「打开一个模型网页」，而是「在命令行里喊一声，多个模型抢着干活，一个装死就换下一个」。龍魂主权网关掌握切换权，AI 只是工具。**

---

## 支持模型

| 模型 | 接入方式 | 默认启用 | 说明 |
|:---|:---|:---:|:---|
| DeepSeek Harness (DSH) | 本地 / 鲲鹏 `127.0.0.1:2284` | ✅ | 零 API 费用，本地推理 |
| Ollama | 本地 / 鲲鹏 `127.0.0.1:11434` | ✅ | 零 API 费用，ARM64 原生 |
| Kimi | Moonshot API | ❌ | 需 `KIMI_API_KEY` |
| CodeBuddy | VSCode 扩展命令 | ❌ | 需安装 CodeBuddy 插件 |
| 自定义模型 | OpenAI 兼容 API | ❌ | 需 `CUSTOM_MODEL_URL` |

---

## 部署步骤

### 1. 鲲鹏上部署 DSH（已有时跳过）

```bash
ssh root@<鲲鹏IP>
cd /opt/deepseek-harness-kunpeng
./scripts/deploy-kunpeng.sh
```

部署脚本会自动把 `configs/terminal-writer.yaml` 复制到 `~/.longhun/configs/`。

### 2. Mac 本地初始化

```bash
cd ~/longhun-system
deploy/deepseek-harness-kunpeng/scripts/local-mac-setup.sh <鲲鹏IP> [SSH密钥]
```

### 3. 启用 Kimi / 自定义模型（可选）

```bash
export KIMI_API_KEY=sk-...
# 或
export CUSTOM_MODEL_URL=https://your-model.com/v1/chat/completions
export CUSTOM_API_KEY=sk-...

# 启用配置
python3 05_ENGINES/lh_terminal_writer.py config --set providers.kimi.enabled=true
python3 05_ENGINES/lh_terminal_writer.py config --set providers.custom.enabled=true
```

---

## 使用方式

```bash
# 建立 SSH 隧道
lh-dsh dsh-tunnel

# 多模型终端写作（自动故障转移）
lh-dsh write "帮我写一段龍魂系统介绍"

# 自动触发：检测 TODO/FIXME/待补充 或文件过短
lh-dsh write-auto ./README.md

# 查看模型可用性
python3 05_ENGINES/lh_terminal_writer.py status

# 耻辱墙看板：最近10条装死记录 + 装死排行
lh-dsh shame-wall
lh-dsh shame-wall --limit 20   # 自定义条数

# 模型健康检查：测试所有已启用模型是否可用
lh-dsh health

# 统计看板：各模型调用次数/成功率/平均耗时/装死次数
lh-dsh stats
```

---

## 看板三件套（v1.2 新增）

### 耻辱墙看板 `lh-dsh shame-wall`

装死模型全量排行 + 最近 10 条记录，一眼看出哪个模型最不靠谱：

```
📋 耻辱墙看板 · 最近 10 条
====================================================================
🏆 装死排行（全量，谁最不靠谱一目了然）:
  🔴 1. dsh        12 次  ████████████
  🟡 2. kimi        3 次  ███
====================================================================
🕐 最近记录:
  1. [dsh] 2026-08-17T... 
     原因: HTTPError: ...
```

### 模型健康检查 `lh-dsh health`

逐个探测所有已启用模型，提前发现问题，不用等装死才察觉：

```
🧪 模型健康检查 · 超时 8s
====================================================================
  [dsh      ] 🟢 可用   (探测 42ms)
  [ollama   ] 🟢 可用   (探测 15ms)
  [kimi     ] 🟡 未启用（跳过）
====================================================================
结果: 2/2 个模型可用
```

### 统计看板 `lh-dsh stats`

各模型调用次数、成功率、平均耗时、装死次数一屏看完：

```
📊 写作统计看板 · 总调用 56 次
====================================================================
模型          调用   成功   失败  成功率  平均耗时   装死
--------------------------------------------------------------------
dsh            30    28     2   93.3%      820ms    12
ollama         26    25     1   96.2%      410ms     3
====================================================================
🏆 最靠谱: ollama（成功率 96.2%）
😾 最装死: dsh（耻辱墙 12 次）
```

---

## 自动触发配置

配置文件：`~/.longhun/configs/terminal-writer.yaml`

```yaml
auto_trigger:
  enabled: true
  watch_dirs: [".", "docs", "12_DOCS"]
  patterns: ["*.md", "*.txt"]
  keywords: ["TODO", "FIXME", "待补充"]
  on_git_commit: true   # git commit 前自动检查
  cooldown_seconds: 60  # 同一文件冷却时间
```

### 安装 git 钩子

```bash
# 在 longhun-system 仓库
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
python3 05_ENGINES/lh_terminal_writer.py pre-commit
EOF
chmod +x .git/hooks/pre-commit
```

---

## 故障转移行为

| 情况 | 动作 | 结果 |
|:---|:---|:---|
| 模型 8 秒内无响应 | 记录耻辱墙 + 切换下一个 | ✅ |
| 模型拒绝执行 | 记录耻辱墙 + 切换下一个 | ✅ |
| 模型 API 密钥未设置 | 标记为不可用，跳过 | ✅ |
| 全部模型失败 | 输出最后错误 + 耻辱墙记录 | ❌ |

---

## 耻辱墙查看

```bash
# 推荐：一键看板（排行 + 最近10条）
lh-dsh shame-wall

# 底层数据直接查（调试用）
sqlite3 .state/terminal_writer/writer.sqlite \
  "SELECT timestamp, provider, reason FROM shame_wall ORDER BY timestamp DESC LIMIT 20;"
```

---

## 与主权网关的关系

本引擎继承 `03_KNOWLEDGE_GRAPH/03_龍魂主权网关自动硬控协议_☯UID9622..._SOVEREIGN-CTRL-v1.0.md` 的核心原则：

- 所有外部 AI 只是工具
- 超时硬控 = 8 秒
- 拒绝/超时 = 耻辱墙 + 自动切换
- 龍魂系统是主子，AI 是器官

---

## 文件清单

| 文件 | 用途 |
|:---|:---|
| `05_ENGINES/lh_terminal_writer.py` | 多模型写作引擎（v1.2：+shame-wall/health/stats） |
| `deploy/deepseek-harness-kunpeng/scripts/lh-dsh` | 终端命令封装（v1.2：+三个看板命令） |
| `deploy/deepseek-harness-kunpeng/configs/terminal-writer.yaml` | 配置文件 |
| `03_KNOWLEDGE_GRAPH/03_多模型终端写作引擎_☯UID9622..._TERMINAL-WRITER-v1.0.md` | 知识图谱入口 |

---

🔐 **最终签名**

```
DNA:        #龍芯⚡️丙午·丙申·丁酉·子时-TERMINAL-WRITER-DEPLOY-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟢 通过
状态:       可执行 · 鲲鹏就绪 · v1.2（看板三件套）
```

🐉 **丙午·丙申·丁酉·子时·🟢**
