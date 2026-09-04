**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 🐉 龍魂 · DeepSeek Harness 鲲鹏 ARM64 部署方案 v1.1

**DNA**: `#龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-DSH-KUNPENG-DEPLOY-v1.1-UID9622`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**三色**: 🟢 通过

> v1.1 (2026-08-16): 精修 — ① Mac 本地命令改名 `lh-dsh`（不再覆盖真实 lh）② 模型切换真生效（改 env_file + 重建容器）③ dsh 容器去除无效 `ollama pull` ④ 看板改用独立 python 镜像 ⑤ SSH 全程走鲲鹏专用密钥 ⑥ 确认码支持非交互 ⑦ 审计日志脱敏 ⑧ CPU/昇腾训练参数区分

---

## 核心判断

> DeepSeek Harness 终端执行配置以本地 Ollama 为核心，零 API 调用费用，鲲鹏 ARM64 自主计算。外部模型只作为可选 fallback，龍魂主权网关掌握切换权。

---

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                     Mac M4 Max (本地)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ VSCode +     │  │ lh-dsh 终端  │  │ SSH 隧道/        │  │
│  │ CodeBuddy    │  │ 命令(独立)   │  │ WireGuard        │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘  │
│         │                  │                    │            │
│         └──────────────────┴────────────────────┘            │
│                            │                                 │
│                     127.0.0.1:2283/2284                      │
│                            │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │ SSH 隧道
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                  华为云鲲鹏 ECS (ARM64)                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Docker Compose 网络                       │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │  │
│  │  │ deepseek-   │  │   Ollama    │  │   龍魂看板   │  │  │
│  │  │ harness     │◄─┤  + deepseek │  │  (可选)      │  │  │
│  │  │ (dsh)       │  │  -r1:14b    │  │              │  │  │
│  │  └──────┬──────┘  └─────────────┘  └──────────────┘  │  │
│  │         │                                             │  │
│  │         └────► 127.0.0.1:2283 (Web UI / API)         │  │
│  │              127.0.0.1:2284 (headless API)           │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 设计决策

| 决策 | 选择 | 理由 |
|:---|:---|:---|
| 推理后端 | **Ollama** | 官方原生支持 `linux/arm64`，拉取即用；vLLM 在 ARM 上编译灾难多 |
| 默认模型 | `deepseek-r1:14b` | 9GB 左右，鲲鹏 4C8G 可跑；可按需切 7b/32b |
| 网络暴露 | **仅 127.0.0.1** | P0 安全基线：不直接暴露公网，外部走 SSH 隧道 |
| 费用 | **零 API 费用** | 全部本地推理，彻底脱离外部模型依赖 |
| 人格注入 | `longhun-system-prompt.md` | DSH_SYSTEM_PROMPT_FILE 挂载，零代码侵入 |

---

## 文件清单

| 文件 | 用途 |
|:---|:---|
| `Makefile` | 统一命令入口 |
| `docker-compose.kunpeng.yml` | 鲲鹏全栈编排 |
| `scripts/deploy-kunpeng.sh` | 鲲鹏上一键部署 |
| `scripts/local-mac-setup.sh` | Mac 本地 `lh-dsh` 命令与隧道脚本 |
| `scripts/huaweicloud-monitor.sh` | 扣费与资源监控 |
| `configs/codebuddy-settings.json` | VSCode CodeBuddy 接入配置 |
| `configs/longhun-system-prompt.md` | 龍魂人格系统提示词 |
| `configs/terminal-writer.yaml` | 多模型终端写作配置 |
| `scripts/lh-dsh` | 终端命令封装（DSH + 写作） |
| `TERMINAL-WRITER.md` | 多模型终端写作部署说明 |
| `training/llama-factory-lora.sh` | 昇腾/鲲鹏 LoRA 微调指引 |

---

## 三步部署

### 1. 鲲鹏服务器部署

```bash
# Mac 上传
scp -r deploy/deepseek-harness-kunpeng root@<鲲鹏IP>:/opt/

# SSH 上执行
ssh root@<鲲鹏IP>
cd /opt/deepseek-harness-kunpeng
chmod +x scripts/*.sh
./scripts/deploy-kunpeng.sh
```

### 2. Mac 本地配置

```bash
./scripts/local-mac-setup.sh <鲲鹏IP>
```

### 3. 日常使用

```bash
# 建立 SSH 隧道 (Ctrl+C 断开)
lh-dsh dsh-tunnel

# 打开 Web UI
lh-dsh dsh

# headless 任务
lh-dsh dsh-headless "审查这段代码的内存泄漏"

# 切换模型 (改 env_file + 重建容器, 真正生效)
lh-dsh dsh-model deepseek-r1:7b

# 查看状态 / 日志
lh-dsh dsh-status
lh-dsh dsh-logs

# 启动状态看板 (需要 docker compose --profile dashboard)
lh-dsh dsh-dashboard
```

> 💡 命令名 `lh-dsh` 为独立封装，**不覆盖真实 `lh` 命令**（`python3 ~/longhun-system/bin/lh.py`），避免 PATH 冲突。审计日志统一写入 `~/.longhun/04_AUDIT/lh_dsh_audit.jsonl`，提示词只记前 60 字符摘要（P0 隐私）。

---

## ✍️ 多模型终端写作（v1.0 新增）

```bash
# 一键写作：DSH → Ollama → Kimi → CodeBuddy → 自定义模型，自动故障转移
lh-dsh write "帮我写一段龍魂系统介绍"

# 自动触发：检测到 TODO/FIXME/待补充 时自动补全
lh-dsh write-auto ./README.md

# 查看各模型可用性
python3 ~/longhun-system/05_ENGINES/lh_terminal_writer.py status
```

详见 [`TERMINAL-WRITER.md`](TERMINAL-WRITER.md)。

---

## P0 安全基线

1. **确认码闸门**：关键操作需 `龍魂9622` 确认；自动化可 `CONFIRM_CODE=龍魂9622` 或 `DSH_NONINTERACTIVE=1` 跳过交互。
2. **密钥环境变量隔离**：不在脚本中硬编码 AK/SK；`dsh-kunpeng.env` 仅含模型名与日志级别。
3. **SSH 密钥-only**：全部脚本/`make` 走 `~/.ssh/longhun_kunpeng_ed25519`，禁密码登录。
4. **127.0.0.1 本地监听**：dsh 与 Ollama 仅绑定 127.0.0.1，不直接暴露公网。
5. **审计日志**：所有 `lh-dsh *` 操作写入 `~/.longhun/04_AUDIT/lh_dsh_audit.jsonl`（脱敏）。

---

## 故障排查

| 症状 | 原因 | 处理 |
|:---|:---|:---|
| `docker compose config` 报 env_file 缺失 | 未生成 `configs/dsh-kunpeng.env` | 已随仓库提供默认文件；部署脚本会自动覆盖 |
| dsh 容器不断重启 | 社区 arm64 镜像路径/启动命令与声明不符 | `docker compose logs dsh` 看报错；README 已注明该镜像 🟡 待实测，可换官方镜像或自行构建 |
| headless 返回空 | SSH 隧道未建立 或 模型未拉取 | 先 `lh-dsh dsh-tunnel`；再 `lh-dsh dsh-status` 确认 ollama 内已有模型 |
| `dsh-model` 切换后不生效 | 旧版本只 export 子进程 | v1.1 起改 env_file + `up -d --force-recreate dsh`，重启后必生效 |
| Ollama 拉模型卡 9GB 下载 | 鲲鹏带宽限制 | 耐心等待；断点续传：`docker compose exec ollama ollama pull deepseek-r1:14b` |
| 看板 2285 打不开 | dashboard 服务未启动 | `lh-dsh dsh-dashboard`（需 `--profile dashboard`） |

---

## 状态与备注

| 项目 | 状态 |
|:---|:---:|
| Docker Compose 语法校验 | 🟢 通过 |
| Ollama `linux/arm64` 镜像确认 | 🟢 存在 |
| dsh 社区 arm64 镜像声明 | 🟡 需实测 |
| 真实鲲鹏 ECS 运行 | 🔴 待实测 |
| CodeBuddy 插件联动 | 🔴 待实测（`codebuddy-settings.json` 为字段语义参考） |
| `lh-dsh` 终端封装 | 🟢 已提供 |
| 模型切换真生效 | 🟢 v1.1 已修（env_file + 重建容器） |

---

## 训练指引

- **昇腾 NPU**：`training/llama-factory-lora.sh` 示例 A（`--fp16` 可用）。
- **鲲鹏纯 CPU**：示例 B（`--use_cpu True`，**必须去掉 `--fp16`**——CUDA/昇腾专属参数）。7B LoRA CPU 极慢，建议先用 1.5B/3B 小模型验证流程。
- **零算力人格注入**：直接改 `configs/longhun-system-prompt.md` 即可，无需微调。

---

🐉 **丙午·丙申·辛酉·丙申·䷉履·🟢**
