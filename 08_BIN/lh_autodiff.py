# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-706396d1
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 · 自动微分引擎 v1.0

ML核心优化基石。龍魂视角：反向传播是「千里之行，始于足下」——
沿损失梯度反方向走一小步，每一步都往更好的方向走。

核心公式:
  链式法则:  dL/dx = dL/dy × dy/dx
  反向传播:  δ = (W^T δ_next) ⊙ σ'(z)

知识卡: 自动微分 · Automatic Differentiation（ID=110 · dr=1·水·坎宫 · 🔴底座）
常见误区: 自动微分≠反向传播——反向传播只是自动微分的一种实现方式(反向模式)。
落地映射: 梯度下降 · 数值方法 · 训练管线 lh_lora_trainer_v4.py

DNA: #龍芯⚡️丙午·甲申·甲子·庚午·䷙大畜-AUTODIFF-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）· 工程层 MulanPSL v2
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

用法:
  python3 bin/lh_autodiff.py --expr          # 默认示例 z = x*y + sin(x), x=2,y=3
  python3 bin/lh_autodiff.py --mlp           # 单层MLP反向传播 δ = (W^T δ)⊙σ'(z)
  python3 bin/lh_autodiff.py --gd --lr 0.1   # 梯度下降最小化 f(x)=x²-4x+4
  python3 bin/lh_autodiff.py --self-test
"""

import argparse
import math
import os
import sys
from dataclasses import dataclass, field


def _stamp() -> str:
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from lh_time_engine import get_output_stamp
        return get_output_stamp()
    except Exception:
        return "🐉[时间引擎不可用]"


# ---------- 反向模式自动微分计算图 ----------

@dataclass
class Node:
    """计算图节点：前向值 + 反向梯度"""
    value: float
    grad: float = 0.0
    op: str = "leaf"
    children: list = field(default_factory=list)

    def backward(self, grad=1.0):
        self.grad += grad
        g = self.grad
        if self.op == "add":
            self.children[0].backward(g)
            self.children[1].backward(g)
        elif self.op == "sub":
            self.children[0].backward(g)
            self.children[1].backward(-g)
        elif self.op == "mul":
            self.children[0].backward(g * self.children[1].value)
            self.children[1].backward(g * self.children[0].value)
        elif self.op == "div":
            a, b = self.children[0].value, self.children[1].value
            self.children[0].backward(g / b)
            self.children[1].backward(-g * a / (b * b))
        elif self.op == "sin":
            self.children[0].backward(g * math.cos(self.children[0].value))
        elif self.op == "cos":
            self.children[0].backward(-g * math.sin(self.children[0].value))
        elif self.op == "exp":
            self.children[0].backward(g * self.value)
        elif self.op == "log":
            self.children[0].backward(g / self.children[0].value)
        elif self.op == "pow":
            a, b = self.children[0].value, self.children[1].value
            self.children[0].backward(g * b * a ** (b - 1))
            # d(a^b)/db = a^b · ln(a)
            self.children[1].backward(g * self.value * math.log(a))
        elif self.op == "neg":
            self.children[0].backward(-g)


def var(v):
    return Node(value=v)


def add(a, b):
    return Node(value=a.value + b.value, op="add", children=[a, b])


def sub(a, b):
    return Node(value=a.value - b.value, op="sub", children=[a, b])


def mul(a, b):
    return Node(value=a.value * b.value, op="mul", children=[a, b])


def div(a, b):
    return Node(value=a.value / b.value, op="div", children=[a, b])


def sin_(a):
    return Node(value=math.sin(a.value), op="sin", children=[a])


def cos_(a):
    return Node(value=math.cos(a.value), op="cos", children=[a])


def exp_(a):
    return Node(value=math.exp(a.value), op="exp", children=[a])


def log_(a):
    return Node(value=math.log(a.value), op="log", children=[a])


def pow_(a, b):
    return Node(value=a.value ** b.value, op="pow", children=[a, b])


def neg_(a):
    return Node(value=-a.value, op="neg", children=[a])


# ---------- 示例 ----------

def demo_expr():
    """z = x*y + sin(x)，x=2, y=3 → dz/dx = y+cos(x), dz/dy = x"""
    x = var(2.0)
    y = var(3.0)
    z = add(mul(x, y), sin_(x))
    z.backward()
    print(f"x = 2.0, y = 3.0")
    print(f"z = x*y + sin(x) = {z.value:.6f}")
    print(f"dz/dx = {x.grad:.6f}  (解析: y+cos(x) = {3.0 + math.cos(2.0):.6f})")
    print(f"dz/dy = {y.grad:.6f}  (解析: x = 2.0)")
    return 0


def demo_mlp():
    """单层MLP反向传播: δ = (W^T δ_next) ⊙ σ'(z)"""
    def sigmoid(z):
        return 1.0 / (1.0 + math.exp(-z))

    def sigmoid_prime(z):
        s = sigmoid(z)
        return s * (1 - s)

    # 2输入 → 3隐藏 → 1输出
    W1 = [[0.5, -0.2, 0.8], [0.1, 0.6, -0.4]]   # 2x3
    b1 = [0.1, -0.1, 0.05]
    W2 = [0.7, -0.3, 0.9]
    b2 = 0.2
    x_in = [1.0, 0.5]
    y_true = 1.0

    z1 = [sum(W1[j][i] * x_in[i] for i in range(2)) + b1[j] for j in range(3)]
    a1 = [sigmoid(z) for z in z1]
    z2 = sum(W2[j] * a1[j] for j in range(3)) + b2
    out = sigmoid(z2)

    # 反向传播（MSE损失 L = 0.5(y-out)²）
    dL_dout = -(y_true - out)          # dL/dout = out - y_true
    dL_dz2 = dL_dout * sigmoid_prime(z2)
    dL_dW2 = [dL_dz2 * a1[j] for j in range(3)]
    dL_db2 = dL_dz2
    dL_da1 = [dL_dz2 * W2[j] for j in range(3)]
    dL_dz1 = [dL_da1[j] * sigmoid_prime(z1[j]) for j in range(3)]
    dL_dW1 = [[dL_dz1[j] * x_in[i] for i in range(2)] for j in range(3)]

    print(f"输入 x = {x_in}, 期望 y = {y_true}")
    print(f"前向: out = {out:.6f}, 损失 L = {0.5*(y_true-out)**2:.6f}")
    print(f"输出层: dL/dW2 = {[round(g,6) for g in dL_dW2]}")
    print(f"隐藏层: dL/dW1 = {[[round(g,6) for g in row] for row in dL_dW1]}")
    print("δ = (W^T δ_next) ⊙ σ'(z) 链式传播 ✅")
    return 0


def demo_gd(lr, n_iter):
    """梯度下降最小化 f(x) = x² - 4x + 4 (最小值 x=2)"""
    def df(x):
        return 2 * x - 4
    x = 0.0
    print(f"梯度下降 f(x)=x²-4x+4 最小值在 x=2 · lr={lr} · {n_iter}步")
    for i in range(n_iter):
        x -= lr * df(x)
        if i % max(1, n_iter // 5) == 0 or i == n_iter - 1:
            print(f"  step {i+1:>3}: x = {x:.6f}, f(x) = {x*x-4*x+4:.6f}")
    print(f"收敛于 x ≈ {x:.4f} (理论 2.0) "
          f"{'✅' if abs(x-2.0) < 1e-2 else '❌ 学习率过大未收敛'}")
    return 0


def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-z))


def _numeric_grad(f, xs, i, eps=1e-6):
    xp = xs[:]
    xm = xs[:]
    xp[i] += eps
    xm[i] -= eps
    return (f(*xp) - f(*xm)) / (2 * eps)


def self_test():
    ok = True
    # 1) 知识卡示例: z = x*y + sin(x), x=2,y=3
    x = var(2.0)
    y = var(3.0)
    z = add(mul(x, y), sin_(x))
    z.backward()
    t1 = (abs(x.grad - (3.0 + math.cos(2.0))) < 1e-9
          and abs(y.grad - 2.0) < 1e-9
          and abs(z.value - (6.0 + math.sin(2.0))) < 1e-9)
    ok &= t1
    print(f"[1] 知识卡示例 z=x*y+sin(x): dz/dx={x.grad:.6f} dz/dy={y.grad:.6f} "
          f"{'✅' if t1 else '❌'}")
    # 2) 复杂链: f = exp(x)·log(y) + x^y, x=1.5, y=2.0
    x = var(1.5)
    y = var(2.0)
    f = add(mul(exp_(x), log_(y)), pow_(x, y))
    f.backward()
    fnum = lambda a, b: math.exp(a) * math.log(b) + a ** b
    gx_num = _numeric_grad(fnum, [1.5, 2.0], 0)
    gy_num = _numeric_grad(fnum, [1.5, 2.0], 1)
    t2 = abs(x.grad - gx_num) < 1e-5 and abs(y.grad - gy_num) < 1e-5
    ok &= t2
    print(f"[2] 复杂链 f=exp(x)log(y)+x^y: 解析({x.grad:.6f},{y.grad:.6f}) "
          f"vs 数值({gx_num:.6f},{gy_num:.6f}) {'✅' if t2 else '❌'}")
    # 3) sigmoid 反向传播数值校验
    t3 = True
    for z0 in [-2.0, 0.0, 1.5]:
        n = var(z0)
        o = div(var(1.0), add(var(1.0), exp_(neg_(n))))
        o.backward()
        num = (sigmoid(z0 + 1e-6) - sigmoid(z0 - 1e-6)) / (2 * 1e-6)
        t3 &= abs(n.grad - num) < 1e-5
    ok &= t3
    print(f"[3] sigmoid梯度数值校验(3点) {'✅' if t3 else '❌'}")
    print(f"\n🐉 自动微分自检: {'全绿 ✅' if ok else '有失败 ❌'}")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="龍魂·自动微分引擎 v1.0")
    ap.add_argument("--expr", action="store_true", help="示例 z=x*y+sin(x)")
    ap.add_argument("--mlp", action="store_true", help="单层MLP反向传播")
    ap.add_argument("--gd", action="store_true", help="梯度下降演示")
    ap.add_argument("--lr", type=float, default=0.1, help="学习率(默认0.1)")
    ap.add_argument("--n-iter", type=int, default=100, help="迭代次数(默认100)")
    ap.add_argument("--self-test", action="store_true", help="自我验证")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(self_test())
    if args.mlp:
        rc = demo_mlp()
    elif args.gd:
        rc = demo_gd(args.lr, args.n_iter)
    else:
        rc = demo_expr()
    print(f"\n{_stamp()}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
