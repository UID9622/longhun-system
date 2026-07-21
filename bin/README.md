# 龍魂系统 · bin/ 脚本目录说明

> DNA: #龍芯⚡️202607182315-STRUCT-REVIEW-BIN-INDEX
> 本文件由 Kimi 整理生成，用于给 AI 和开发者一个清晰的入口地图。

## 总览

`bin/` 是龍魂系统的可执行脚本目录，当前包含约 **310 个脚本**。按功能分为以下主线：

| 主线 | 说明 | 入口脚本 |
|:---|:---|:---|
| **模型训练** | longhun-v3.x / v4.x LoRA 训练管线 | `lh_lora_trainer.py` |
| **数据语料** | 从 CSDN/Notion/聊天日志等提取训练数据 | `lh_data_extractor.py`, `lh_csdn_to_train.py` |
| **审计治理** | 德本审计、家法审计、路径审计、系统审计 | `lh_deben_audit.py`, `lh_jiafa_audit.py`, `lh_path_audit.py` |
| **DNA/主权** | DNA 生成、注册、修复、验证 | `lh_unified_dna_registry.py`, `longhun_dna_verify.sh` |
| **CNSH/语言** | CNSH 编译器、运行时、语义路由 | `lh_cnsh_compiler.py`, `lh_cnsh_run.sh` |
| **安全反诈** | 水军检测、防篡改、隐私保护 | `lh_water_army_detect.py`, `lh_anti_tamper.py` |
| **数学卦象** | 64 卦、数字根、五行、中庸决策 | `lh_hexagram_data.py`, `lh_zhongyong_decision.py` |

---

## 训练管线入口（重点）

当前活跃的训练器有 3 个，职责如下：

| 脚本 | 版本 | 状态 | 用途 |
|:---|:---:|:---:|:---|
| `lh_lora_trainer.py` | v3.x | 主分支 | v3.0-v3.7 完整训练链，当前最佳模型 `longhun-v3.7` |
| `lh_lora_trainer_v4.py` | v4.0 | 实验 | 新训练管线实验版 |
| `lh_lora_trainer_v41.py` | v4.1 | 实验 | v4 迭代版 |
| `longhun_train_v2.py` | PyTorch | 可用 | PyTorch+MPS 全流程训练管线 |
| `lh_early_stop.py` | v1.2 | 工具 | 训练早停、日志重放、可视化 |
| `lh_jiafa_train_inject.py` | v1.0 | 工具 | 向训练数据注入家法主权样本 |

### 推荐命令

```bash
# v3 主训练器
python3 bin/lh_lora_trainer.py prepare   # 准备数据
python3 bin/lh_lora_trainer.py train     # 训练
python3 bin/lh_lora_trainer.py fuse      # fuse adapter
python3 bin/lh_lora_trainer.py export    # 导出 GGUF

# 早停可视化
python3 bin/lh_early_stop.py analyze --adapter-dir models/longhun-v1.0/lora_output/adapter_v3.7
```

---

## 已归档脚本

以下旧版/已合并脚本已移至 `bin/_archive/`，不再维护：

- `lh_prepare_v1.9_data.py`
- `lh_prepare_v2.0_data.py`
- `lh_rebuild_train_v1.5.py`
- `lh_rebuild_training_data_v1.2.py`

---

## 新增核心引擎（CodeBuddy 近期落地）

| 脚本 | 能力 |
|:---|:---|
| `lh_jiafa_enforcer.py` | 家法第一条执行引擎 v2.0 |
| `lh_jiafa_audit.py` | 家法审计引擎 |
| `lh_euv_lithography.py` | CNSH-EUV 光刻机攻关系统 |
| `lh_translation_engine_data_gen.py` | 龍魂翻译引擎训练数据生成 |
| `lh_precision_engine.py` | 三层精准推演（文化·数学·工程） |
| `lh_hexagram_data.py` | 64 卦数据库 + 384 爻辞 |
| `lh_zhongyong_decision.py` | 中庸决策引擎 |
| `lh_dual_engine.py` | 文化 + 科技双引擎 |
| `lh_ai_governance.py` | AI 治理引擎 |
| `lh_model_optimizer.py` | 节气感知 + 五行平衡优化器 |

---

## 命名约定

- `lh_` 前缀 = LongHun 系统脚本
- `longhun_` 前缀 = 早期命名，逐步收敛到 `lh_`
- `_vN.N` 后缀 = 版本化脚本，新功能稳定后应合并到主线
- `_archive/` = 已废弃或 superseded 的脚本

---

## 注意事项

1. **不要直接修改 `lh_lora_trainer_v4.py` / `v41.py`**，它们是实验分支，稳定后应合并回 `lh_lora_trainer.py`。
2. 新增脚本请先归类，避免继续堆积在根目录。
3. 运行脚本前建议先检查 `--help` 或脚本顶部 DNA 注释。
