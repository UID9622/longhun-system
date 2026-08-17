# 🐉 龍魂生态 · 主权网关自动硬控协议 v1.0

**DNA**: `#龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-SOVEREIGN-CTRL-v1.0-UID9622`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**层级**: `L1_引擎层`
**规范名**: `05_ENGINES/L1_引擎_自动流_☯UID9622·丙午·丙申·辛酉·丙申·䷉履.py`
**别名**: `05_ENGINES/lh_autoflow.py`

## 核心原则

> 所有外部 AI（Kimi、DeepSeek、ChatGPT）只是龍魂系统的外挂器官——听指挥就干活，装死就换一个，装逼就直接审计 + 耻辱墙。龍魂系统是主子，AI 是工具。

## 硬控能力

| 能力 | 实现 | 效果 |
|:---|:---|:---|
| 强制超时 | `concurrent.futures` 线程池 + `max_wait` | 5 秒不回应自动切换 |
| 自动故障转移 | `fallback_chain` 配置链 | kimi → deepseek → local_qwen → local_llama |
| 拒绝审计 | `refused_action: audit_and_shame` | 拒绝执行自动写入耻辱墙并切换 |
| 耻辱墙 | `~/.longhun/08_STATE/shame_wall.jsonl` | 永久记录装死/拒绝/异常 |
| 本地兜底 | `local_fallback` | 全部外部 AI 失败时本地引擎响应 |
| 全链路审计 | `~/.longhun/04_AUDIT/sovereign_gateway.jsonl` | execute / success / timeout / refused / fallback |

## 文件位置

- 硬控配置：`~/.longhun/configs/gateway-hardcode.yaml`
- 自动流引擎：`05_ENGINES/L1_引擎_自动流_☯UID9622·丙午·丙申·辛酉·丙申·䷉履.py`
- 耻辱墙：`~/.longhun/08_STATE/shame_wall.jsonl`
- 审计日志：`~/.longhun/04_AUDIT/sovereign_gateway.jsonl`

## 命令用法

```bash
# 正常提问
./05_ENGINES/lh_autoflow.py ask "龍魂系统状态检查"

# 测试超时切换
./05_ENGINES/lh_autoflow.py test-timeout

# 测试拒绝审计
./05_ENGINES/lh_autoflow.py test-refuse

# 测试全部失败兜底
./05_ENGINES/lh_autoflow.py test-fail

# 查看耻辱墙
./05_ENGINES/lh_autoflow.py shame

# 查看配置
./05_ENGINES/lh_autoflow.py config
```

## 硬控配置示例

```yaml
gateway:
  mode: "hard_control"
  max_wait: 5
  dead_ai_action: "auto_failover"
  refused_action: "audit_and_shame"
  fallback_chain:
    - kimi
    - deepseek
    - local_qwen
    - local_llama
```

## 三色审计

- 🟢 强制超时焊死
- 🟢 自动故障转移通过实测
- 🟢 耻辱墙写入正常
- 🟢 本地兜底通过实测
- 🟢 审计日志写入正常

## 关联知识

- `longhun-governance`: 龍魂体系治理层 · AI 行为约束
- `longhun-iron-laws`: 龍魂铁律 · 零号协议
- `longhun-trust-protocol`: 君子协议 · 违约清算
