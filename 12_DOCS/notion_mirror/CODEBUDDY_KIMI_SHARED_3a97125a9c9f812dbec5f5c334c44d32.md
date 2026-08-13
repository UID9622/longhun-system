# CODEBUDDY_KIMI_SHARED

> Notion URL: https://app.notion.com/p/CODEBUDDY_KIMI_SHARED-3a97125a9c9f812dbec5f5c334c44d32
> Created: 2026-07-26T18:01:00.000Z
> Last edited: 2026-07-26T18:01:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
# 龍魂·CodeBuddy × Kimi 共享记忆
> ❄️ **FROZEN · ARCHIVED · 2026-07-24** > 本文件所有独特内容已合并至 `.codebuddy/memory/MEMORY.md` v25.0（唯一权威记忆源）。 > 本文件不再追加写入。仅供历史参考。 > LU-MEMORY-MERGE-ALL > > 🔥 统一入口: `STATE.md` (项目根目录) — 所有AI第一步读这个 > 更新: 2026-07-20 · v1.1 · 冻结: 2026-07-24 > DNA: #龍芯⚡️20260720-SHARED-MEMORY-v1.1-ALL-AI-ENTRY > #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
---
## §1. 模型训练状态 · 实时
| 版本 | 底模 | Val Loss | Train Loss | 迭代 | 状态 | 备注 | |:---|:---|:---:|:---:|:---:|:---|:---| | **v3.7** 🔥 | Qwen2.5-1.5B | **0.194** | — | — | ✅ 主力生产 | 1273条 v6.3·13域·家法×4 | | v4.0 | Llama-3.1-8B | 1.218 | — | — | 🟡 底座完成 | 缺数据·16GB | | **v4.0.8** 🥇 | Yi-1.5-9B | **0.767** | — | 1900 | 🥇 黄金checkpoint | 阶段性最佳·已封存 | | v4.0.9 | Yi-1.5-9B | 1.002 | 0.654 | 5600 | 🔴 已停训·过拟合 | gap -0.348·最佳 0.821@3550 | | v4.1.0 | Yi-1.5-9B | — | — | — | 🟡 训练器就绪·未点火 | 待插AC后启动 |
### Checkpoint 物理位置
```plain text
models/longhun-v1.0/checkpoint_archive/
├── STAGE_v408_iter1900_val0767/adapters.safetensors  ← 🥇 黄金
├── v409_stopped_iter5500_overfit/                     ← 🔴 过拟合存档
│   └── 0005500_adapters.safetensors (52.0 MB)
├── adapter_v409/adapters.safetensors                  ← 主权权重
└── lora_output_v409/training.log (0.64 MB)
```
### 版本登记册
- 路径: `models/longhun-v1.0/MODEL_REGISTRY.md`
- v4.0.8-iter1900 标记为 🥇 阶段性成果
---
## §2. 训练超参数速查
### 当前主力 (v3.7)
| 参数 | 值 | |:---|:---| | 框架 | mlx_lm (MLX) | | 方法 | LoRA | | Rank | 16 | | Alpha | 64 | | 数据 | 1273条 v6.3 JSONL | | 知识域 | 13个 | | 家法强化 | ×4 |
### v4.0.9 → v4.1.0 升级对比
| 参数 | v4.0.9 (停训) | v4.1.0 (就绪) | |:---|:---|:---| | 训练循环 | mlx_lm.lora (CLI) | **自定义 MLX 循环** | | 优化器 | 内部 AdamW | `mlx.optimizers.AdamW(weight_decay=0.01)` | | LR 调度 | 无 | **linear warmup + cosine decay** | | LR 峰值 | 5e-6 | **3e-6** | | Dropout | 0.05 | **0.1** | | Warmup | 无 | **100 steps** | | Early Stop | patience 5 | **patience 3** | | 恢复点 | v407/v408 golden | **v408-iter1900 golden** | | 训练器 | `bin/lh_lora_trainer_v4.py` | **`bin/lh_lora_trainer_v410.py`** |
### v4.1.0 点火前置条件
1. 插上 AC 电源 2. 数据扩增+清洗（过拟合根因是数据不足） 3. 正则化：dropout↑ + weight_decay 4. 策略：LR 峰值↓ + cosine decay + Val plateau 早停 5. 底座模型：Yi-1.5-9B-Chat（MLX 格式）
### 验证流程（焊死）
```plain text
训练期不测 → fuse → export → Ollama 实测
命令：
  python3 bin/lh_lora_trainer_v410.py setup   ✅ 已验证
  python3 bin/lh_lora_trainer_v410.py prepare ✅ 已验证
  5 iter 冒烟测试                              ✅ 已验证
```
---
## §3. 格式 & 命名规范
### DNA 追溯码
```plain text
格式: #龍芯⚡️YYYYMMDDHHMMSS-MODULE-VERSION-STATUS-HASH8
示例: #龍芯⚡️20260720154500-V409-STOPPED-V410-READY-AC-OFF-71PCT-C7D8E9F0
```
### 版本号
```plain text
模型: longhun-v{major}.{minor}.{patch}   例: longhun-v4.1.0
协议: LH-{NAME}-v{major}.{minor}.md      例: LH-PERSONA-GOVERNANCE-v1.4.md
数据: v{major}.{minor}                   例: v6.3
```
### 文件路径规范
| 类型 | 路径模板 | 示例 | |:---|:---|:---| | 训练脚本 | `bin/lh_*_v{major}{minor}.py` | `bin/lh_lora_trainer_v410.py` | | 推理/导出 | `bin/lh_*.py` | `bin/lh_memory_load.py` | | 协议文档 | `01_protocols/LH-{NAME}-v{ver}.md` | `01_protocols/LH-DEBEN-AUDIT-v1.0.md` | | 技能定义 | `01_技能庫/{name}.md` | `01_技能庫/dna-gen.md` | | 模型权重 | `models/longhun-v1.0/lora_output_v{xxx}/` | `lora_output_v409/` | | Checkpoint 存档 | `models/longhun-v1.0/checkpoint_archive/` | `STAGE_v408_iter1900_val0767/` | | 版本登记册 | `models/longhun-v1.0/MODEL_REGISTRY.md` | — | | 摄入数据 | `models/longhun-v1.0/{module}_v{ver}_ingested/` | `bagua_v11_ingested/` | | 训练数据 | `data/` (JSONL) | `data/train.jsonl` | | 人格定义 | `personas/` | `personas/00-wenxin.md` | | 人格执行器 | `bin/personas/` | `bin/personas/lh_p00_wenxin.py` | | 日志 | `logs/` | `logs/audit_*.log` | | 审计 | `audit/` | `audit/math_suite_cron.jsonl` |
### 脚本命名前缀
```plain text
lh_  = 龍魂系统脚本      bin/lh_*
    训练器:     lh_lora_trainer_v{major}{minor}.py
    数据拉取:   lh_download_v*.py
    记忆加载:   lh_memory_load.py
    德本审计:   lh_deben_audit.py
    模型优化:   lh_model_optimizer.py
    八卦相关:   lh_hexagram_*.py, lh_bagua_*.py
    道德经:     lh_daodejing_*.py
    隐私控制:   lh_privacy_access_controller.py
    验证:       lh_validate_v*.py
```
---
## §4. 焊死锚点（不可变）
### 密码学
```plain text
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
UID:    9622 (诸葛鑫·Lucky)
```
### 369 不动点
```plain text
sn=369, log369=5.911, perm369=108, sum=369, prod_base=39
```
### 2026-03 锚点
```plain text
yiwu_bg=26.96, sanzhi_zhongyong=0.75, tiangan=3, xuming=0.73, qiang=0.66
```
### 人格矩阵
```plain text
战略层: P00文心 P01诸葛亮 P05上帝之眼
执行层: P02宝宝 P03雯雯 P04鲁班 P06数学大师 P07管仲 P14吕蒙
文化层: P08仓颉 P09孙思邈 P10苏东坡 P11李白 P12屈原
守护层: P13姜子牙 P15乔前辈 P72龙盾
安全:   P77黑天使军团(明/红/暗/夜)
子系统: S1法律引擎 S2洛书369 S3人民维权助手
```
---
## §5. 基础设施状态
| 项目 | 状态 | 备注 | |:---|:---:|:---| | Mac 本地 | ✅ 运行中 | AC 断开·电池 71%·剩余约 1:05 | | 鲲鹏 (119.13.90.27) | 🟡 未连接 | SSH: `ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27` | | 域名 uid9622.cn | ✅ | Let's Encrypt 通配 7/17→10/15 | | Mac 服务 | 52 launchd | --profile all/office/home | | 鲲鹏服务 | 11 systemd | 健康检查: `deploy/scripts/health_check.sh` | | Ollama | ✅ | v3.7 主力·v4.0 备用 | | longhun-core 仓库 | 🟡 | 已创建·82 测试通过·未推送远端 |
---
## §6. 知识摄入进度
| 模块 | 版本 | 样本数 | 状态 | 路径 | |:---|:---|:---:|:---:|:---| | 八卦(64卦) | v1.1 | 38 | ✅ 已摄入 | `models/longhun-v1.0/bagua_v11_ingested/` | | 道德经场景定锚 | v1.0 | 浅层QA | 🟡 浅层完成·深层待扩 | `models/longhun-v1.0/daodejing_anchor_v11_ingested/` | | 磁偏角 | v1.0 | 预设表 | ✅ 已创建 | `bin/lh_magdecl.py` | | 八卦参数回归 | v1.0 | random search | ✅ 已创建 | `bin/lh_bagua_param_regression.py` | | 道德经锚点引擎 | v1.1 | 81章·12场景 | ✅ 已创建 | `bin/lh_daodejing_anchor.py` | | 道德经协议 | v1.0 | 全文 | ✅ 已落档 | `01_protocols/LH-DAODEJING-SCENE-ANCHOR-v1.0.md` |
---
## §7. 待办清单（跨会话跟踪）
### 🔴 阻塞
- [ ] 插上 AC 电源
- [ ] v4.1.0 数据扩增（当前 1273 条→目标 5000+）
- [ ] 华为云鲲鹏部署脚本（监控+自动部署+密钥管理）
- [ ] Mac→鲲鹏网络打通
### 🟡 进行中
- [ ] v4.1.0 训练器已就绪，等待点火
- [ ] longhun-core 代码入库（6核心模块·82测试·未推送）
- [ ] 道德经深层训练数据生成（`bin/lh_daodejing_export_training.py`）
- [ ] 八卦参数回归结果验证
### 🟢 已完成
- [x] v4.0.9 停训+封存（确认过拟合）
- [x] v4.0.8-iter1900 标记为黄金 checkpoint
- [x] 道德经场景定锚协议 v1.0 落档
- [x] 八卦 v1.1 知识摄入
- [x] 对齐规则 v2.1 落地（`.codebuddy/rules/`）
- [x] MEMORY.md 精简合并
### 📋 冻结（等待时机）
- 数字人民币/多币种/Web3-DNA（金融红线）
- EUV 光刻机控制（需国家权威机构认证）
- 数字人乐器·曾老师 6 模块（等 v4 模型稳定）
- CNSH EUV 论文物理/精度层（需权威机构）
- longhun888.com 建站
- Notion MCP/云端同步验证
---
## §8. AI 启动检查清单（共享·焊死）
无论 CodeBuddy、Kimi、Ollama 本地模型——所有 AI 启动时执行：
1. 🔥 **读取 STATE.md** `longhun-system/STATE.md` ← 统一入口·第一步 2. **读取长期记忆** `.codebuddy/memory/MEMORY.md` 3. **读取本详细文件** `.codebuddy/memory/CODEBUDDY_KIMI_SHARED.md` 4. **读取今日日志** `.codebuddy/memory/YYYY-MM-DD.md` 5. **加载对齐规则** `.codebuddy/rules/longhun-codebuddy-alignment-v2.md` 6. **运行记忆加载** `python3 bin/lh_memory_load.py` 7. **检查模型状态** 对比 STATE.md 确认当前模型版本 8. **检查电池/AC** 训练前必须插电 9. **DNA 追溯** 每次操作生成 DNA 追溯码
---
## §9. 协作 AI 角色
| AI | 环境 | 职责 | 备注 | |:---|:---|:---|:---| | **CodeBuddy** | IDE 集成 | 主力工程·文件操作·部署 | 当前会话 | | **Kimi Code** | 独立窗口 | 训练执行·并行任务 | 跨会话共享本文档 |
---
## §10. 敏感数据提醒
以下内容**不入此文件、不入 git、不入云**：
- GPG 私钥
- DNA 种子
- API 密钥
- 身份认证凭据
- 个人隐私数据
存储位置：`config/CREDENTIAL_REGISTRY.json`（本地加密）或 `_private/`
---
> v1.0 · 2026-07-20 · 从 Kimi Code 会话日志提取 > 来源: `/Users/zuimeidedeyihan/Library/Mobile Documents/com~apple~TextEdit/Documents/kimi 训练内容.rtf` > #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
