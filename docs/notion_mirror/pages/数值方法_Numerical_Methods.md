# 数值方法

> 创建者: 诸葛鑫（UID9622）
> DNA: #龍芯⚡️2026-07-23-TOPIC-数值方法-v1.0-4b8e7d16
> 协议: CC BY-NC-SA 4.0
> 分类: 哲学与数学基础·L2知识层

---

## 1. 定义

数值方法 = 用离散近似求解连续数学问题的算法集合，是深度学习训练的数学底层。

## 2. 龍魂中的数值方法

| 数值方法 | DL应用 | 龍魂落点 |
|:---|:---|:---|
| **梯度下降** | 参数优化 | SGD·AdamW |
| **数值积分** | BatchNorm统计 | running_mean·var |
| **插值** | 图像/序列上采样 | 位置编码插值 |
| **矩阵分解** | LoRA·SVD | rank=16分解 |
| **蒙特卡洛** | Dropout·采样 | 训练随机性 |
| **数值微分** | 梯度检查 | finitediff验证 |

## 3. 优化器的数值稳定性

### 3.1 AdamW
$$
m_t = \beta_1 m_{t-1} + (1-\beta_1) \nabla L
$$
$$
v_t = \beta_2 v_{t-1} + (1-\beta_2)(\nabla L)^2
$$
$$
\hat{m}_t = \frac{m_t}{1-\beta_1^t},\quad \hat{v}_t = \frac{v_t}{1-\beta_2^t}
$$
$$
\theta_t = \theta_{t-1} - \eta \left(\frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon} + \lambda \theta_{t-1}\right)
$$

### 3.2 369锚定数值参数
```python
NUMERICAL_CONFIG = {
    "epsilon": 3.69e-8,        # AdamW ε·防除零
    "beta1": 0.9,              # 一阶动量
    "beta2": 0.999,            # 二阶动量
    "mixed_precision": True,   # bf16/fp32混合
    "gradient_clip": 3.69,     # 梯度裁剪(369对齐)
    "loss_scale": 65536,       # 混合精度缩放(2^16)
}
```

## 4. 数值精度管理

| 精度 | 使用场景 | 范围 | 注意 |
|:---|:---|:---|:---|
| fp32 | 关键参数·权重 | ±3.4e38 | 默认 |
| bf16 | 激活值·梯度 | ±3.4e38(同fp32范围) | 推荐 |
| fp16 | 推理 | ±65504 | 易溢出 |
| int8 | 量化推理 | ±127 | 精度损失 |
| fp64 | 数值验证 | ±1.8e308 | 仅检查用 |

## 5. 条件数与数值稳定性

条件数 $\kappa$ 衡量问题对输入扰动的敏感度：

$$
\kappa = \frac{\lambda_{max}}{\lambda_{min}} \quad (\text{矩阵的条件数})
$$

- $\kappa < 10$: 🟢 良好·稳定训练
- $10 \le \kappa < 100$: 🟡 一般·需监控
- $\kappa \ge 100$: 🔴 病态·可能导致NaN

## 6. 混合精度训练

```python
# MLX混合精度
mx.set_default_dtype(mx.bfloat16)  # 计算用bf16
model = model.astype(mx.float32)   # 权重建模用fp32保持精度
# 前向用bf16·反向自动混合·loss scale自动管理
```

---

> 数值方法·梯度下降·稳定性·混合精度
> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
