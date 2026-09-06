#!/usr/bin/env python3
# 🐉 龍魂系统 · MLX 前向探针引擎 v1.0（L2 隐层激活实机 + L3 token 归因实机）
# DNA: #龍芯⚡️丙午·癸未·甲子·申时-MLX-FORWARD-PROBE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 立项: T2 白盒探针·L2/L3 升绿候选（台账 2026-09-06·白盒探针 v1.0 前向轨）
# 铁律: 21层幻觉量化——实机跑出数据才标🟢·方法学如实标注·不因「能跑」标绿
# 口径:
#   L2 隐层激活 = 真实 MLX 前向·逐层截取 hidden states·统计(范数/稀疏度/层间相似度)
#   L3 token 归因 = leave-one-out(替换干扰)·目标位 logprob 差排序·方法学 v1.0(简单替换·非梯度)
# 载体模型: MLX q8 格式（mlx_lm.convert 产物）·任何 mlx_lm 可载模型均可
# 用法:
#   python3 08_BIN/lh_mlx_forward_probe.py run \
#       --model _work/mlx-qwen1.5b-q8 \
#       --prompt "龍魂系统自检 五行平衡" \
#       --probe-layers 0,7,14,21,27   # 指定层(0起)·默认等比抽 5 层
#       --out reports/xxx.json
import argparse
import json
import sys
import time

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

try:
    import mlx.core as mx
    from mlx_lm.models.base import create_attention_mask
except Exception as e:
    print(f"🔴 依赖不可用: {type(e).__name__}: {e} · 需 mlx+mlx_lm 环境")
    sys.exit(2)


def load_model(path):
    """mlx_lm.load 的轻量替代: 已知架构(qwen2)直读 safetensors。

    mlx_lm.load 返回元组长度随入参浮动(2 或 3)且 MLX 模块为运行时动态类，
    显式只取前两项并以 Any 传递——消除 pyright 对动态模型的推断噪音，
    实机行为不变(Qwen2Model.model 载入后恒非空)。
    """
    from typing import Any, cast

    import mlx_lm
    res = cast(tuple, mlx_lm.load(path))
    return cast(Any, res[0]), cast(Any, res[1])


def layer_stats(h):
    """L2 统计: h=(1,T,H) → 末位向量指标。"""
    last = h[:, -1, :]  # (1,H)
    f = mx.abs(last).sum().item()
    l2 = mx.sqrt(mx.sum(last * last)).item()
    sparsity = (mx.abs(last) < 1e-6).sum().item() / last.shape[-1]
    mean = mx.mean(last).item()
    return {"l2_norm": round(l2, 6), "l1_sum": round(f, 4),
            "sparsity": round(sparsity, 6), "mean": round(mean, 6),
            "max_abs": round(float(mx.max(mx.abs(last))), 6)}


def cosine(a, b):
    a = a.reshape(-1)
    b = b.reshape(-1)
    na = mx.sqrt(mx.sum(a * a))
    nb = mx.sqrt(mx.sum(b * b))
    return float(mx.sum(a * b) / (na * nb + 1e-9))


def forward_hidden(model, ids, probe_layers, collect_all=False):
    """逐层前向·返回 {层idx: hidden(1,T,H)} + 最终 hidden。ids=(1,T)。"""
    m = model.model
    h = m.embed_tokens(ids)
    mask = create_attention_mask(h, None)
    outs = {}
    cache = None  # 纯前向无 cache
    for i, layer in enumerate(m.layers):
        h = layer(h, mask, cache)
        if collect_all or i in probe_layers:
            outs[i] = h
    h = m.norm(h)
    return outs, h


def logits_for(model, h):
    if getattr(model, "lm_head", None) is not None:
        return model.lm_head(h)
    return model.model.embed_tokens.as_linear(h)


def logprob(logits, target_id):
    """target 位置 logprob。logits=(1,T,V)·target 用最后一位置。"""
    z = logits[0, -1, :]
    log_z = z - mx.logsumexp(z)
    return float(log_z[target_id])


def run(args):
    model_path = args.model
    prompt = args.prompt
    probe_layers = [int(x) for x in args.probe_layers.split(",")] if args.probe_layers else None
    out_path = args.out
    t0 = time.time()

    print(f"== MLX 前向探针 · 模型={model_path} · prompt「{prompt}」 ==")
    model, tokenizer = load_model(model_path)
    core = model.model  # Qwen2Model: layers/embed_tokens/norm(Qwen2.5 系·载入后恒非空)
    n_layers = len(core.layers)

    ids = tokenizer.encode(prompt)
    seq = mx.array([ids])  # (1,T)
    h0 = core.embed_tokens(seq)
    hidden = int(h0.shape[-1])  # 运行期实测(兼容混合 embedding: qwen1.5 码表384→前向1536)
    print(f"  架构: {type(model).__name__} · 层数={n_layers} · hidden(实测)={hidden}")
    print(f"  token 数={len(ids)}")

    # 默认等比抽层
    if probe_layers is None:
        k = min(5, n_layers)
        idxs = [round(i * (n_layers - 1) / max(k - 1, 1)) for i in range(k)]
        probe_layers = sorted(set(idxs))

    # ── L2 隐层激活实机 ──
    outs, final_h = forward_hidden(model, seq, set(probe_layers))
    l2_rows = {}
    prev_h = None
    for li in sorted(outs):
        h = outs[li]
        st = layer_stats(h)
        st["cos_to_prev"] = round(cosine(prev_h, h), 6) if prev_h is not None else None
        l2_rows[str(li)] = st
        prev_h = h
    final_stats = layer_stats(final_h)
    l2_rows["final_norm"] = {"l2_norm": final_stats["l2_norm"], "mean": final_stats["mean"]}
    print(f"🟢 L2 隐层激活实机: {len(outs)} 层截取 → {json.dumps(l2_rows, ensure_ascii=False)[:240]}…")

    # ── L3 token 归因 leave-one-out ──
    # 目标位 = prompt 末 token；prefix = prompt[0..n-2]；干扰 token = id 0(中性弱语义)
    prefix_ids = list(ids[:-1])
    target = ids[-1]
    base_emb_seq = mx.array([prefix_ids])
    _, bh = forward_hidden(model, base_emb_seq, set())
    lg = logits_for(model, bh)
    base_lp = logprob(lg, target)
    attr = {}
    for j in range(len(prefix_ids)):
        alt = prefix_ids.copy()
        alt[j] = 0  # 中性干扰 id
        alt_seq = mx.array([alt])
        _, ah = forward_hidden(model, alt_seq, set())
        al = logits_for(model, ah)
        lp = logprob(al, target)
        attr[str(j)] = round(base_lp - lp, 6)  # 越大=该 token 越关键(移除它降幅大)
    sorted_attr = sorted(attr.items(), key=lambda kv: -kv[1])
    top3 = [(f"t{j}={tokenizer.decode([prefix_ids[int(j)]])[:6]!r}",
             f"{v:+.4f}") for j, v in sorted_attr[:3]]
    print(f"🟢 L3 token 归因实机(LOO·方法v1.0): top3 {top3} · base_logp={base_lp:.4f}")

    # ── 输出 ──
    out = {
        "dna": "#龍芯⚡️丙午·癸未·甲子·申时-MLX-FORWARD-PROBE-v1.0-UID9622",
        "model": model_path, "prompt": prompt, "n_tokens": len(ids),
        "architecture": type(model).__name__, "layers": n_layers, "hidden": hidden,
        "L2_layer_stats": l2_rows,
        "L3_attr": attr, "L3_top3": top3, "L3_method": "leave-one-out·replace-id0·v1.0",
        "base_logprob": round(base_lp, 6),
        "duration_sec": round(time.time() - t0, 2),
        "status": "🟢 实机跑通(L2/L3 前向)·方法学 v1.0"
    }
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True) if os.path.dirname(out_path) else None
        with open(out_path, "w") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"  输出 → {out_path}")
    else:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    import os
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run"])
    ap.add_argument("--model", default="_work/mlx-qwen1.5b-q8")
    ap.add_argument("--prompt", default="龍魂系统自检 五行平衡")
    ap.add_argument("--probe-layers", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    sys.exit(run(a))
