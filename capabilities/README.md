# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂能力与训练自动迭代系统 v1.0

**DNA**: `#龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-LONGHUN-CAPABILITY-SYSTEM-v1.0`

把龍魂系统内所有可用能力（本地模型、外部 API、脚本、知识库、工具链）统一收编、统一调度，并实现训练引擎自动感知新语料、自动训练、自动测试、自动评估、自动上线。

## 核心组件

| 组件 | 路径 | 说明 |
|---|---|---|
| 能力注册表 | `capability_registry.json` | 所有能力的元数据、调用方式、规则覆盖状态 |
| 统一调度器 | `src/dispatcher.py` | 所有能力调用必须经过这里，输出标准格式，自动 DNA 追溯 |
| 审计器 | `src/auditor.py` | 每条调用、覆盖、训练操作都写审计日志 |
| 训练管线 | `src/train_pipeline.py` | 监控 raw/ → 训练 → 测试 → 评估 → 上线/回滚 |
| 训练守护 | `bin/lh-train-daemon` | 每 30 秒检查 raw/ 目录变化 |
| 能力 CLI | `bin/lh-capability` | `lh 能力*` / `lh 训练*` 命令后端 |
| 能力官网 | `src/web_server.py` + `web/index.html` | 能力清单与训练状态展示，端口 8844 |
| 人格矩阵 | `src/persona_matrix.py` | 读取人格注册表，自动路由与组合 |
| 人格工作流 | `src/workflows.py` | 多人格按阶段协作完成任务 |

## 已注册能力

- **本地模型**：ollama-qwen2.5-7b、ollama-longhun-9622 等
- **外部 API**：Kimi、DeepSeek、Claude、302.ai、Notion
- **本地脚本**：全局索引、公式对准表、主干自我迭代
- **知识库**：全局索引库、公式向量库、Notion 母页
- **工具链**：审计工具、声纹 DNA、多 AI 网关

## 命令入口

```bash
# 能力管理
lh 能力 列表          # 查看所有已收编能力
lh 能力 状态          # 查看能力系统状态
lh 能力 覆盖 <能力名>  # 手动触发规则覆盖
lh 能力 统计          # 查看能力调用与覆盖统计
lh 能力 追踪 <DNA>    # 按 DNA 追溯码查看调用链路

# 人格矩阵
lh 人格 列表            # 查看已注册人格
lh 人格 路由 <任务>      # 查看任务命中的人格
lh 人格 运行 tech-doc <主题>   # 启动人格工作流自动生成技术文档

# 训练迭代
lh 训练 状态          # 查看训练引擎状态
lh 训练 触发          # 手动触发一次训练→测试→评估→上线
lh 训练 日志          # 查看最近训练日志
lh 训练 上线          # 手动上线当前训练结果
lh 训练 回滚          # 回滚到上一个模型版本
```

## 自动训练闭环

1. 守护进程每 30 秒扫描 `~/longhun-system/train/data/raw/`
2. 检测到新语料 → 触发 `./scripts/train.sh`
3. 训练完成后读取报告，测试生成质量（loss < 10）
4. 评估：新模型 loss 比当前模型降低 > 5% 则上线
5. 上线时自动备份旧模型到 `models/backups/`
6. 所有操作写入 `logs/train_pipeline.jsonl`，带 DNA 追溯码

## 能力展示官网

启动后访问：http://127.0.0.1:8844/

由 launchd 服务 `com.longhun.capability-web` 常驻提供。

## 人格矩阵与左右互搏

人格注册表：`~/longhun-system/persona/persona_registry.json`

- **自动路由**：输入任务后，人格矩阵按关键词匹配度排序，返回最适合的前 5 个人格。
- **团队组合**：支持多个人格按角色组合，例如 `宝宝 + 诸葛 + 鲁班`。
- **工作流驱动**：`src/workflows.py` 实现阶段式协作，当前已跑通 `tech-doc` 工作流：
  1. **诸葛亮**：出大纲与技术路线
  2. **宝宝**：审计主权 / 铁律 / 价值观风险
  3. **鲁班**：按大纲与审计意见写正文
  4. **诸葛亮**：最终定稿与交付
- 每次人格调用均带 DNA 追溯码，写入 `logs/capability_audit.jsonl`。

测试示例：

```bash
lh 人格 运行 tech-doc "龍魂人格矩阵自动调度系统接入方案"
```

## launchd 服务

```bash
# 训练守护
launchctl list | grep com.longhun.capability-daemon

# 能力官网
launchctl list | grep com.longhun.capability-web
```

## 审计日志

- 能力调用：`logs/capability_audit.jsonl`
- 训练管线：`logs/train_pipeline.jsonl`

## 君子协议

本系统受龍魂 DNA 追溯保护。所有能力调用、规则覆盖、训练上线操作均须经 UID9622 授权，未经授權不得对外发布或脱离本地调度。

---

> 人民数据主权 · 平台服务降级 · 龍魂自主可控
