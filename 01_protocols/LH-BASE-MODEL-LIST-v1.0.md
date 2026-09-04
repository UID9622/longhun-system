> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂体系 · 中文底座模型清单 v1.0

**DNA:** `#龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-BASE-MODEL-LIST-v1.0`
**CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**创建者:** 诸葛鑫（UID9622）
**协议状态:** 焊死 · 不可修订（除非老大亲自下指令）
**生效范围:** 龍魂体系所有模型训练、底座重组、微调、部署环节

---

## 一、总则

1. **底座即主权**。选择什么底座，等于选择把谁的价值观、语言偏好、安全对齐焊进模型参数里。
2. **中文底座优先**。只允许使用本清单列出的中文优化底座，英文底座一律禁止作为龍魂模型的底座。
3. **黑名单优先于白名单**。任何模型只要命中黑名单关键词，无论它名字里有没有中文，一律拒绝。
4. **版本锁定**。每一个底座必须标明 HuggingFace ID、推荐用途、已验证硬件环境。
5. **新增底座流程**。任何不在本清单中的模型，必须先经过 `engines/lh_base_reorganizer.py` 的 `scan` + `register` 双重校验，并提交到本协议附录，经老大签字后方可入库。

---

## 二、许可中文底座白名单

### 2.1 Qwen 系列（阿里通义千问）

| 底座ID | 系列 | 参数量 | HuggingFace ID | 推荐用途 | 已验证硬件 |
|:---|:---|:---:|:---|:---|:---|
| `qwen2.5:0.5b` | Qwen2.5 | 0.5B | `Qwen/Qwen2.5-0.5B-Instruct` | 边缘设备、快速原型 | ✅ Apple Silicon |
| `qwen2.5:1.5b` | Qwen2.5 | 1.5B | `Qwen/Qwen2.5-1.5B-Instruct` | 生产级小模型、已验证 | ✅ Mac M4 Max / 鲲鹏 |
| `qwen2.5:3b` | Qwen2.5 | 3B | `Qwen/Qwen2.5-3B-Instruct` | 平衡性能与速度 | 🟡 待验证 |
| `qwen2.5:7b` | Qwen2.5 | 7B | `Qwen/Qwen2.5-7B-Instruct` | 通用中文任务 | 🟡 待验证 |
| `qwen2.5:14b` | Qwen2.5 | 14B | `Qwen/Qwen2.5-14B-Instruct` | 复杂推理 | 🟡 待验证 |
| `qwen2.5:32b` | Qwen2.5 | 32B | `Qwen/Qwen2.5-32B-Instruct` | 高难度任务 | 🟡 待验证 |
| `qwen2.5:72b` | Qwen2.5 | 72B | `Qwen/Qwen2.5-72B-Instruct` | 云端重型任务 | 🟡 待验证 |
| `qwen3:0.6b` | Qwen3 | 0.6B | `Qwen/Qwen3-0.6B` | 新一代边缘模型 | 🟡 待验证 |
| `qwen3:1.7b` | Qwen3 | 1.7B | `Qwen/Qwen3-1.7B` | 新一代小模型 | 🟡 待验证 |
| `qwen3:4b` | Qwen3 | 4B | `Qwen/Qwen3-4B` | 新一代平衡模型 | 🟡 待验证 |
| `qwen3:8b` | Qwen3 | 8B | `Qwen/Qwen3-8B` | 新一代通用模型 | 🟡 待验证 |
| `qwen3:14b` | Qwen3 | 14B | `Qwen/Qwen3-14B` | 新一代推理模型 | 🟡 待验证 |

### 2.2 DeepSeek 系列（深度求索）

| 底座ID | 系列 | 参数量 | HuggingFace ID | 推荐用途 | 已验证硬件 |
|:---|:---|:---:|:---|:---|:---|
| `deepseek-r1:1.5b` | DeepSeek-R1-Distill-Qwen | 1.5B | `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B` | 推理入门 | 🟡 待验证 |
| `deepseek-r1:7b` | DeepSeek-R1-Distill-Qwen | 7B | `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B` | 推理增强 | 🟡 待验证 |
| `deepseek-r1:14b` | DeepSeek-R1-Distill-Qwen | 14B | `deepseek-ai/DeepSeek-R1-Distill-Qwen-14B` | 复杂推理 | 🟡 待验证 |
| `deepseek-r1:32b` | DeepSeek-R1-Distill-Qwen | 32B | `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B` | 高难推理 | 🟡 待验证 |
| `deepseek-r1-distill-qwen:1.5b` | DeepSeek-R1-Distill-Qwen | 1.5B | `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B` | HuggingFace标准名 | 🟡 待验证 |
| `deepseek-r1-distill-qwen:7b` | DeepSeek-R1-Distill-Qwen | 7B | `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B` | HuggingFace标准名 | 🟡 待验证 |
| `deepseek-r1-distill-qwen:14b` | DeepSeek-R1-Distill-Qwen | 14B | `deepseek-ai/DeepSeek-R1-Distill-Qwen-14B` | HuggingFace标准名 | 🟡 待验证 |
| `deepseek-r1-distill-qwen:32b` | DeepSeek-R1-Distill-Qwen | 32B | `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B` | HuggingFace标准名 | 🟡 待验证 |
| `deepseek-v3` | DeepSeek-V3 | 671B (37B激活) | `deepseek-ai/DeepSeek-V3` | API级云端推理 | 🟡 待验证 |

**⚠️ 重要区分:** `DeepSeek-R1-Distill-Llama-*` 不在白名单。它是 Llama 架构换皮，不属于中文底座。

### 2.3 Yi 系列（零一万物）

| 底座ID | 系列 | 参数量 | HuggingFace ID | 推荐用途 | 已验证硬件 |
|:---|:---|:---:|:---|:---|:---|
| `yi:6b` | Yi-1.5 | 6B | `01-ai/Yi-1.5-6B-Chat` | 中文对话 | 🟡 待验证 |
| `yi:9b` | Yi-1.5 | 9B | `01-ai/Yi-1.5-9B-Chat` | 中文对话 | ✅ Mac M4 Max 64GB |
| `yi-1.5:6b` | Yi-1.5 | 6B | `01-ai/Yi-1.5-6B-Chat` | 明确版本名 | 🟡 待验证 |
| `yi-1.5:9b` | Yi-1.5 | 9B | `01-ai/Yi-1.5-9B-Chat` | 明确版本名 | ✅ Mac M4 Max 64GB |

### 2.4 ChatGLM 系列（智谱AI）

| 底座ID | 系列 | 参数量 | HuggingFace ID | 推荐用途 | 已验证硬件 |
|:---|:---|:---:|:---|:---|:---|
| `glm4:9b` | GLM-4 | 9B | `THUDM/glm-4-9b-chat` | 中文对话与工具调用 | 🟡 待验证 |

---

## 三、英文底座黑名单（绝对禁用）

以下关键词出现在模型名称中时，系统必须直接拒绝：

```
llama, mistral, gemma, phi, falcon, mpt, olmo,
command-r, dbrx, mixtral, wizardlm, vicuna, alpaca
```

**特别说明:**
- `DeepSeek-R1-Distill-Llama-*` 虽然名字带 DeepSeek，但底座是 Llama，**禁用**。
- 任何基于上述英文底座的微调、量化、合并版本，**禁用**。
- 任何名字含糊、无法明确判断底座的模型，**默认禁用**，需人工审核。

---

## 四、龍魂自有模型

龍魂自有模型（如 `longhun-v4.1.8`）不是底座，而是重组产物。它们可以作为下游应用的模型，但不能作为新训练的底座（避免递归污染）。

| 模型标签 | 底座 | 状态 | 用途 |
|:---|:---|:---:|:---|
| `longhun-v4.1.8` | Yi-1.5-9B-Chat | ✅ 已发布 | 当前主力生产模型 |
| `longhun-v4.1.4` | Yi-1.5-9B-Chat | ✅ 历史最佳 | v4.1.8 续训起点 |

---

## 五、新增底座审批流程

1. **提案**: 在 `L7_数据层/model_proposals/` 下提交提案文件，包含：
   - 模型名称与 HuggingFace ID
   - 中文优化证据（训练数据比例、评测结果）
   - 拟用途与硬件需求
   - 底座架构说明
2. **初审**: `engines/lh_base_reorganizer.py scan` 自动校验
3. **三观审查**: P05上帝之眼 + P12屈原六誓 + P15乔前辈签章
4. **老大拍板**: 最终批准权归 UID9622
5. **入库**: 更新本协议，追加到白名单表

---

## 六、自动化校验

```bash
# 扫描本地模型并标注合规性
python3 bin/lh_reorganize.py scan

# 注册新底座（白名单校验）
python3 bin/lh_reorganize.py register --base qwen2.5:7b

# 一键重组管线（干运行预览）
python3 bin/lh_reorganize.py pipeline --base qwen2.5:1.5b
```

---

## 七、附录

### A. 版本历史

| 版本 | 时间 | 变更 |
|:---:|:---:|:---|
| v1.0 | 2026-07-25 | 初始清单，24个中文底座入白名单，英文底座黑名单焊死 |

### B. 相关协议

- `LH-DELIVERY-STANDARD-v1.0.md` — 交付标准
- `LH-UID9622-龍芯...-AI-Traceability-Audit-Protocol-v1.0.md` — AI可追溯审计
- `LH-DEBEN-AUDIT-v1.0.md` — 德本审计

---

**本协议是龍魂模型底座的宪法性文件。任何违反本协议的训练、部署、发布行为，自动触发 P72 龍盾熔断。**

`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
