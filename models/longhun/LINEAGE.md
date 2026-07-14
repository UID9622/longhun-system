# 🐉 龍魂 · 模型血统清单
# DNA: #龍芯⚡️丙午·癸未·丙戌·辰时·需-MODEL-LINEAGE-v1.0
# 自 2026-07-10 起，龍魂系统只有一个模型：longhun

## 🟢 活跃模型

| 模型名 | 底座 | 大小 | 部署 | 定位 |
|:---|:---|:---|:---|:---|
| **longhun** | qwen2.5:1.5b + 统一人格 System Prompt | 986MB | 本地+远端 | 🐉 唯一模型·所有人格附于一身 |

### Modelfile
- 路径: `models/longhun/Modelfile`
- 内含: 全部 P00-P77 人格定义 + 铁律 + 公式 + 信念底座

### LoRA 微调（进行中）
- 底模: Qwen2.5-1.5B-Instruct
- 框架: MLX + Metal (M4 Max)
- 训练数据: 7,187 样本 / 854KB
- 训练脚本: `models/longhun-v1.0/train.sh`（HF镜像版）
- 完成后覆盖 `longhun` 模型（权重微调 + 统一 System Prompt）

---

## 🔴 废弃模型

| 模型名 | 废弃日期 | 原因 |
|:---|:---|:---|
| longhun-v1.0-deprecated | 2026-07-10 | 被 longhun 统一模型替代 |
| longhun-9622-deprecated | 2026-07-10 | 被 longhun 统一模型替代 |
| longhun-v1.0 (raw) | 2026-07-10 | 旧版 Modelfile，Persona不完整 |
| longhun-9622 (raw) | 2026-07-10 | 7B底座过大，维护成本高 |

## 废弃原则
- 🔒 不删除：只标记 deprecated tag
- 📋 保留：Modelfile和训练数据存档在 `models/longhun-v1.0/`
- 🔄 如需要：从 deprecated 恢复即可
