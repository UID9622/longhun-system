# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 自动微分

> 创建者: 诸葛鑫（UID9622）
> DNA: #龍芯⚡️2026-07-23-TOPIC-自动微分-v1.0-9c4e1a85
> 协议: CC BY-NC-SA 4.0
> 分类: 哲学与数学基础·L2知识层

---

## 1. 定义

自动微分（Automatic Differentiation, AD）= 基于链式法则的程序化导数计算。深度学习训练的核心。

## 2. 两种模式

| 模式 | 方向 | 复杂度 | 适用 |
|:---|:---|:---|:---|
| 前向模式 | 输入→输出 | O(N)·N=输入维度 | 输入少·输出多 |
| 反向模式 | 输出→输入 | O(M)·M=输出维度 | 输入多·输出少(Loss) |

深度学习用**反向模式**（反向传播），因为参数量(输入)远大于损失函数(输出=1)。

## 3. 龍魂中的自动微分

### 3.1 MLX框架
```python
import mlx.core as mx

def loss_fn(model, x, y):
    logits = model(x)
    return mx.mean(mx.losses.cross_entropy(logits, y))

# MLX自动追踪计算图
loss_and_grad = mx.value_and_grad(model, loss_fn)
loss, grads = loss_and_grad(model, x_batch, y_batch)
```

### 3.2 自定义算子梯度

CNSH自定义算子的梯度定义（如五行注意力·三才损失）：
```python
@mx.custom_grad
def wuxing_attention(query, key, value, element_mask):
    """五行注意力·自定义前向+反向"""
    ...
    def vjp(upstream_grad):
        # 五行生克约束的反向传播
        ...
    return output, vjp
```

## 4. 梯度与龍魂哲学

| 数学概念 | 哲学含义 | 龍魂落点 |
|:---|:---|:---|
| $\nabla L$ | 损失函数梯度 | "知错能改·方向明确" |
| $\nabla L \to 0$ | 梯度消失 | "失去方向·需要重新锚定" |
| $\|\nabla L\|$ 爆炸 | 梯度爆炸 | "过度反应·需要收敛" |
| Adam优化器 | 自适应学习率 | "因材施教·各个突破" |
| 梯度裁剪 | 限制步长 | "过犹不及·中道而行" |

## 5. 三才梯度分解

将总梯度按三才分解：
$$
\nabla L = \nabla_{天}L + \nabla_{地}L + \nabla_{人}L
$$

- $\nabla_{天}$: 语法·逻辑层面的梯度 → 修正形式错误
- $\nabla_{地}$: 物理·约束层面的梯度 → 修正资源问题
- $\nabla_{人}$: 语义·意图层面的梯度 → 修正理解偏差

## 6. 梯度审计

每369步检查梯度统计：

| 检查项 | 阈值 | 动作 |
|:---|:---|:---|
| `grad_norm` | >10 | 梯度裁剪到10 |
| `grad_norm` | <0.001 | 🟡 可能梯度消失·检查lr |
| `param_update / param` | >0.01 | 🟡 更新过大·降低lr |
| `grad_std / grad_mean` | >100 | 🟡 梯度不稳定·检查数据 |

---

> 自动微分·反向传播·MLX·三才梯度
> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
