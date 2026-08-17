# 🐉 龍魂生态 · DeepSeek Harness 鲲鹏 ARM64 部署 v1.0

**DNA**: `#龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-DSH-KUNPENG-DEPLOY-v1.0-UID9622`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**层级**: `L3_应用层`
**规范名**: `deploy/deepseek-harness-kunpeng/`

## 核心判断

> DeepSeek Harness 终端执行配置以本地 Ollama 为核心，零 API 调用费用，鲲鹏 ARM64 自主计算。外部模型只作为可选 fallback，龍魂主权网关掌握切换权。

## 架构

```
Mac M4 Max (本地)  <── SSH 隧道 ──>  华为云鲲鹏 ECS (ARM64)
  VSCode/CodeBuddy                         Docker Compose
  lh 终端命令                              ├─ Ollama + deepseek-r1:14b
                                           ├─ DeepSeek Harness (dsh)
                                           └─ 龍魂看板 (可选)
```

## 文件位置

| 文件 | 用途 |
|:---|:---|
| `deploy/deepseek-harness-kunpeng/README.md` | 总纲与快速开始 |
| `deploy/deepseek-harness-kunpeng/Makefile` | 统一命令入口 |
| `deploy/deepseek-harness-kunpeng/docker-compose.kunpeng.yml` | 鲲鹏全栈编排 |
| `deploy/deepseek-harness-kunpeng/scripts/deploy-kunpeng.sh` | 鲲鹏上一键部署 |
| `deploy/deepseek-harness-kunpeng/scripts/local-mac-setup.sh` | Mac 本地 `lh` 命令 |
| `deploy/deepseek-harness-kunpeng/scripts/huaweicloud-monitor.sh` | 扣费与资源监控 |
| `deploy/deepseek-harness-kunpeng/configs/codebuddy-settings.json` | VSCode CodeBuddy 配置 |
| `deploy/deepseek-harness-kunpeng/configs/longhun-system-prompt.md` | 龍魂人格系统提示词 |
| `deploy/deepseek-harness-kunpeng/training/llama-factory-lora.sh` | LoRA 微调指引 |

## 部署流程

```bash
# 1. 上传到鲲鹏
make deploy KUNPENG_IP=<IP>

# 2. Mac 本地配置
make setup-mac IP=<IP>
# 或
./deploy/deepseek-harness-kunpeng/scripts/local-mac-setup.sh <IP>

# 3. 日常使用
lh dsh-tunnel    # 建立 SSH 隧道
lh dsh           # 打开 Web UI
lh dsh-headless "审查这段代码"
lh dsh-model deepseek-r1:7b
```

## 关键设计决策

| 决策 | 选择 | 理由 |
|:---|:---|:---|
| 推理后端 | Ollama | 官方原生支持 `linux/arm64`，拉取即用 |
| 默认模型 | `deepseek-r1:14b` | 9GB 左右，鲲鹏 4C8G 可跑 |
| 网络暴露 | 仅 `127.0.0.1` | P0 安全基线，外部走 SSH 隧道 |
| 费用 | 零 API 费用 | 全部本地推理，彻底脱离外部模型 |
| 人格注入 | `longhun-system-prompt.md` | `DSH_SYSTEM_PROMPT_FILE` 挂载，零侵入 |

## P0 安全基线

1. 确认码闸门：部署需输入 `龍魂9622`
2. 密钥环境变量隔离：脚本中不硬编码 AK/SK
3. SSH 密钥-only：禁用密码登录
4. 127.0.0.1 本地监听：dsh 与 Ollama 不直接暴露公网
5. 审计日志：`~/.longhun/04_AUDIT/lh_dsh_audit.jsonl`

## 模型训练阶段

| 阶段 | 能力 | 状态 |
|:---|:---|:---:|
| 一 | 系统提示词人格注入 | 🟢 现在就能做 |
| 二 | LoRA 微调（鲲鹏 CPU / 昇腾 NPU） | 🟡 数据积累后 |
| 三 | 昇腾 NPU 全量训练 | 🔴 未来 |

## 实测状态

| 项目 | 状态 |
|:---|:---:|
| Shell 脚本语法 | 🟢 通过 |
| Docker Compose 语法 | 🟢 CodeBuddy 已验证 |
| Ollama `linux/arm64` 镜像 | 🟢 官方确认 |
| dsh 社区 arm64 镜像 | 🟡 声明支持，待实测 |
| 真实鲲鹏 ECS 运行 | 🔴 待实测 |
| CodeBuddy 插件联动 | 🔴 待实测 |

## 三色审计

- 🟢 部署方案完整
- 🟢 安全基线已焊死
- 🟢 Mac 本地 `lh` 命令已封装
- 🟢 监控脚本已提供
- 🟡 真实鲲鹏环境待实测

## 关联知识

- `05_ENGINES/L1_引擎_自动流_☯UID9622·...py`：主权网关多模型故障转移
- `08_BIN/L1_引擎_身份激活_☯UID9622·...py`：身份激活与协议加载
- `deploy/`：龍魂部署目录
