# DeepSeek 对话 · 本地终端可执行方案

**DNA**: `#龍芯⚡️20260701052429041921-DEEPSEEK-TERMINAL-PLAN-129A1E55`

## 目标

让 UID9622 在本地终端通过一条命令完成龍智守飞书推送环境的检查、初始化与验证，
且默认 **dry-run**，只有显式加 `--run --test` 才会真正发送消息。

## 可执行脚本

```bash
# 干跑检查（安全，不会发消息）
~/longhun-system/scripts/setup_longzhishou_push_env.sh

# 真正初始化配置并发送测试消息
~/longhun-system/scripts/setup_longzhishou_push_env.sh --run --test
```

## 脚本内部逻辑

| 步骤 | 动作 | 输出 |
|---|---|---|
| 1. 检查核心文件 | 确认 `~/Downloads/龍智守_本地控制接口_v2.0.py` 存在 | 🟢/🔴 |
| 2. 初始化配置 | 若 `~/.longhun/config/龍智守_config.json` 缺失，从 `.example` 复制 | 🟢/🟡 |
| 3. 检查环境变量 | 检查 `FEISHU_WEBHOOK_URL`、`FEISHU_WEBHOOK_SECRET` | 🟢/🟡 |
| 4. 扫描敏感信息 | 在 `~/Downloads` 搜索包含 `open.feishu.cn`/`hook/` 的文件，**只列文件名** | 🟢/🟡 |
| 5. 发送验证消息 | `--run --test` 时执行 `python3 龍智守_本地控制接口_v2.0.py 发送测试消息` | 🟢/🔴 |

## CNSH 变量映射

```text
@@channel.feishu.webhook_url        → ${FEISHU_WEBHOOK_URL}
@@channel.feishu.webhook_secret     → ${FEISHU_WEBHOOK_SECRET}
@@channel.feishu.config_path        → ~/.longhun/config/龍智守_config.json
@@channel.feishu.config_example_path → ~/.longhun/config/龍智守_config.example.json
@@channel.longzhishou.script        → ~/Downloads/龍智守_本地控制接口_v2.0.py
@@channel.longzhishou.log           → ~/.longhun/logs/bot_command.jsonl
```

## 下一步动作

1. 运行干跑检查：
   ```bash
   ~/longhun-system/scripts/setup_longzhishou_push_env.sh
   ```
2. 若配置缺失，用 `--run` 创建模板后编辑真实值。
3. 确认配置正确后，用 `--run --test` 发送验证消息。
4. 开源前再次运行扫描，确保无硬编码密钥残留。
