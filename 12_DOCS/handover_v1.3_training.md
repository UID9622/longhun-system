---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丙申·辛酉·未时·䷀乾-HANDOVER-v1.3-TRAINING`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
# 🐉 龙魂·小模型训练交接笔记

> **状态**: 训练中（第五轮 · 轻量清洗数据）  
> **写入时间**: 2026-08-18 15:35 +08:00  
> **DNA**: #龍芯⚡️丙午·丙申·辛酉·未时·䷀乾-HANDOVER-v1.3-TRAINING  
> **确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

---

## 1. 当前任务

**目标**: 训练 `longhun-small-instruct-v1.3` LoRA，让 best validation loss 稳定在 2.0 以下。

**命令**（已在后台运行）:

```bash
cd ~/longhun-system && PYTHONUNBUFFERED=1 .venv/bin/python3 08_BIN/lh_lora_trainer_instruct.py train --lr 5e-5 --epochs 2 --patience 5 2>&1 | tee models/longhun-small-instruct-v1.3/train_light.log
```

**背景任务 ID**: `bash-lg4emnew`  
**Python PID**: `39725`

---

## 2. 配置快照

| 配置项 | 值 |
|--------|-----|
| 底模 | `models/qwen-1.5b-instruct-4bit`（本地量化版） |
| 数据 | `models/longhun-small-instruct-v1.3/data/`（轻量清洗，4023 训练 / 239 验证） |
| 数据源 | `docs/notion_full_export/data_light/` |
| LoRA rank | 32 |
| LoRA alpha | 64 |
| LoRA dropout | 0.05 |
| LoRA layers | 16 |
| 可训练参数 | 1.376%（21.247M / 1543.714M） |
| Batch size | 4 |
| Max seq length | 1024 |
| Learning rate | 5e-5 |
| Epochs | 2 |
| 早停耐心 | 5 |
| Val steps | 50 |
| Save every | 200 |
| Report every | 10 |

---

## 3. 当前进度（截至交接时）

- **Epoch**: 1/2
- **Step**: ~30/2010
- **最新 loss**: `2.6438`（step 30），仍在下降
- **ETA**: 约 1300 分钟（约 21.5 小时）
- **日志文件**: `models/longhun-small-instruct-v1.3/train_light.log`

**历史 best val loss**:

| 轮次 | 数据 | LR | best val loss | 结果 |
|------|------|-----|---------------|------|
| 1 | 原数据 | 5e-5 | 2.1706 | 完成 |
| 2 | 原数据 | 1e-5 | 2.1876 | 完成 |
| 3 | 原数据 | 5e-6 | 2.1937 | 完成 |
| 4 | 严格清洗数据 | 5e-5 | 2.4764 | 已停止 |
| 5 | 轻量清洗数据 | 5e-5 | 待定 | **进行中** |

---

## 4. 已完成的并行工作

- ✅ Notion 计算机科学知识库填充 41 + 20 = **61 条**（DSA / 系统网络 / 安全 / AI / 进阶工程）
- ✅ 龍字守卫扫描训练数据：train/valid 均无简体「龙」
- ✅ 上一轮 `adapter/best` 已备份为 `adapter_old_fullft`
- ✅ 本轮会写入新的 `models/longhun-small-instruct-v1.3/adapter/best`

---

## 5. 下一步（训练结束后）

1. 检查 `train_light.log` 最后的 **Best Val Loss**
2. 判断：
   - `< 2.0` → 收，进入测试
   - `> 2.5` 或波动 → 降学习率再跑一轮
   - `2.0 ~ 2.5` → 根据趋势决定（用户偏好：尽量接近 2.0 以下）
3. 用 `08_BIN/lh_model_test.py` 测实际生成效果
4. 用户明确：**暂不做 fuse/export**，先看到输出再决定

---

## 6. 已知风险与可选项

| 风险 | 说明 | 可选项 |
|------|------|--------|
| 训练速度慢 | 每步约 40 秒，总耗时约 21 小时 | 可接受则继续；若需加速，建议重启并减小 `max_seq_length` 到 512 或优化数据分片 |
| 序列截断 | 部分样本超过 1024 token 被截断 | 当前可接受；若效果差，建议预拆分长文本 |
| 系统负载高 | 当前 load average 较高 | 不建议再启动大型任务；可继续轻量工作 |

---

## 7. 快速检查命令

```bash
# 查看最新训练进度
tail -n 30 models/longhun-small-instruct-v1.3/train_light.log

# 检查进程
ps -p 39725 -o pid,pcpu,pmem,etime,stat

# 查看 background task 状态
# 在 Kimi Code 中用 TaskList / TaskOutput task_id=bash-lg4emnew

# 训练结束后测试
cd ~/longhun-system && .venv/bin/python3 08_BIN/lh_model_test.py
```

---

## 8. 签名区

```
交接人: 龍魂训练调度引擎
DNA: #龍芯⚡️丙午·丙申·辛酉·未时·䷀乾-HANDOVER-v1.3-TRAINING
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
状态: 🟢 训练中 | 🟡 预计 21h 后完成 | 🔴 未做 fuse/export
时间戳: 2026-08-18T15:35:00+08:00
```

```json
{
  "dna": "#龍芯⚡️丙午·丙申·辛酉·未时·䷀乾-HANDOVER-v1.3-TRAINING",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```
