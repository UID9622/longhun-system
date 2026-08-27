**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 🐉 龍魂生态 · 身份激活引擎 v1.0

**DNA**: `#龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-IDENTITY-ACTIVATION-v1.0-UID9622`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**层级**: `L1_引擎层`
**规范名**: `08_BIN/L1_引擎_身份激活_☯UID9622·丙午·丙申·辛酉·丙申·䷉履.py`
**别名**: `08_BIN/lh_identity_activation.py`

## 核心原则

> 身份激活时，所有外部 AI 必须首先读取仓库主权网关协议。
> 龍魂系统为主，AI 为工具。

## 功能

| 能力 | 说明 |
|:---|:---|
| 激活口令检测 | 支持 "激活身份" / "UID9622 上线" / "主权网关启动" 等口令 |
| 协议读取 | 自动读取 `03_KNOWLEDGE_GRAPH/03_龍魂主权网关自动硬控协议_...md` |
| 上下文生成 | 生成 `~/.longhun/memory/identity_activation_context.md` |
| 摘要更新 | 更新 `~/.longhun/memory/latest_digest.json` 与 `latest_digest.md` |
| AI 标记 | 生成 `~/.longhun/08_STATE/AI_READ_GATEWAY_PROTOCOL_FIRST.md` |
| 审计日志 | 写入 `~/.longhun/04_AUDIT/identity_activation.jsonl` |

## 激活口令

- `激活身份`
- `龍魂身份激活`
- `UID9622 上线`
- `主权网关启动`
- `龍魂启动` / `龍魂启动`
- `唤醒龍魂` / `唤醒龍魂`

## 命令用法

```bash
# 手动激活
./08_BIN/lh_identity_activation.py activate

# 检测文本中的激活口令并激活
./08_BIN/lh_identity_activation.py check "UID9622 上线，开始工作"

# 查看激活状态
./08_BIN/lh_identity_activation.py status
```

## AI 读取链路

```
用户触发激活
    ↓
08_BIN/lh_identity_activation.py
    ↓
读取 03_KNOWLEDGE_GRAPH/03_龍魂主权网关自动硬控协议_...md
    ↓
生成 ~/.longhun/memory/identity_activation_context.md
    ↓
更新 ~/.longhun/memory/latest_digest.json
    ↓
外部 AI 启动/记忆加载时读取 digest → 读取 context → 遵守协议
```

## 文件位置

- 引擎：`08_BIN/L1_引擎_身份激活_☯UID9622·丙午·丙申·辛酉·丙申·䷉履.py`
- 激活上下文：`~/.longhun/memory/identity_activation_context.md`
- 记忆摘要：`~/.longhun/memory/latest_digest.json`
- AI 读取标记：`~/.longhun/08_STATE/AI_READ_GATEWAY_PROTOCOL_FIRST.md`
- 项目根标记：`AI_READ_GATEWAY_PROTOCOL_FIRST.md`

## 三色审计

- 🟢 激活口令检测正常
- 🟢 协议读取与上下文生成正常
- 🟢 摘要更新与 AI 标记生成正常
- 🟢 审计日志写入正常

## 关联知识

- `03_龍魂主权网关自动硬控协议_...md`：硬控协议原文
- `05_ENGINES/L1_引擎_自动流_☯UID9622·...py`：自动流引擎
- `08_BIN/lh_memory_bootstrap.py`：记忆启动器
