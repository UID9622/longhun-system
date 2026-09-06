#!/usr/bin/env python3
# 🐉 龍魂系统 · 白盒探针引擎 v1.0（GGUF 张量级权重白盒 + LLM 前向层骨架）
# DNA: #龍芯⚡️丙午·丁酉·癸未·午时-WHITEBOX-PROBE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 立项: T2 白盒探针(2026-09-06 午指令)「L1注意力权重分布/L2隐层激活/L3 token归因」
# 铁律: 21层幻觉量化——实机跑通才标🟢·未验证标🟡·不因「理论上可跑」升绿
# 口径: L1=权重层白盒(静态·可重现·与prompt无耦合, prompt仅锚记录)
#       L2/L3=前向推理层(🟡待mlx_lm/llama.cpp前向引擎·见 `llm` 子命令)
# 用法:
#   python3 08_BIN/lh_whitebox_probe.py list    --file <model.gguf> [--tensors N]
#   python3 08_BIN/lh_whitebox_probe.py weights --file <model.gguf> [--prompt 龍魂系统自检] [--layers N|all] [--topk K] [--out <out.json>]
#   python3 08_BIN/lh_whitebox_probe.py llm     [--ollama 0|1] [--prompt ...]
#   python3 08_BIN/lh_whitebox_probe.py summary
import json
import os
import struct
import sys
import time
from typing import Any

GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GGUF_MAGIC = b"GGUF"
GGUF_ALIGN = 32

# GGUF metadata value_type → (bytes, name, struct_fmt)
SCALAR = {0: (1, "u8", "B"), 1: (1, "i8", "b"), 2: (2, "u16", "H"),
          3: (2, "i16", "h"), 4: (4, "u32", "I"), 5: (4, "i32", "i"),
          6: (4, "f32", "f"), 7: (1, "bool", "B"), 8: (-1, "string", ""),
          9: (-2, "array", ""), 10: (8, "u64", "Q"), 11: (8, "i64", "q"),
          12: (8, "f64", "d")}
# 张量 ggml_type 子集 → 每元素字节(未知=量化/稀疏·字节数复杂不硬猜)
TBYTES = {0: 4, 1: 2, 2: None, 3: None, 6: None, 7: None, 8: None,
          10: None, 11: None, 12: None, 13: None, 14: None, 15: None,
          16: None, 17: None, 18: None, 19: None, 20: None, 21: None,
          22: None, 23: None, 24: None, 25: None, 26: None, 27: None,
          28: None, 29: None, 30: None}
TNAME = {0: "F32", 1: "F16", 2: "Q4_0", 3: "Q4_1", 6: "Q5_0", 7: "Q5_1",
         8: "Q8_0", 10: "Q2_K", 11: "Q3_K", 12: "Q4_K", 13: "Q5_K",
         14: "Q6_K", 15: "Q8_K", 30: "IQ4_XS"}


def _rs(buf, off):
    (n,) = struct.unpack_from("<Q", buf, off)
    off += 8
    return buf[off:off + n].decode("utf-8", "replace"), off + n


def _fmt(name):
    return {"u8": "B", "i8": "b", "u16": "H", "i16": "h", "u32": "I",
            "i32": "i", "f32": "f", "bool": "B", "u64": "Q", "i64": "q",
            "f64": "d"}[name]


def _read_elem(buf, off, vt):
    """metadata 数组元素/标量读取 → (val, new_off)"""
    if vt not in SCALAR:
        return None, off
    size, name, fmt = SCALAR[vt]
    if name == "string":
        return _rs(buf, off)
    if name == "array":  # 嵌套数组罕见·不深读
        return None, off
    (val,) = struct.unpack_from("<" + fmt, buf, off)
    return val, off + size


def parse_header(path: str, cap: int = 1 << 26) -> tuple[bool, dict[str, Any]]:
    # 64MB 读窗(词表数组可 >4MB·不足则报需要扩展)
    """读 GGUF 头部+全部 metadata+kv → (ok, info)  info 含 kv/meta 摘要"""
    size = os.path.getsize(path)
    if size < 24:
        return False, {"err": "文件过小"}
    with open(path, "rb") as f:
        head = f.read(min(size, cap))
    if head[:4] != GGUF_MAGIC:
        return False, {"err": "magic 非 GGUF"}
    (ver,) = struct.unpack_from("<I", head, 4)
    (n_tensors,) = struct.unpack_from("<Q", head, 8)
    (n_kv,) = struct.unpack_from("<Q", head, 16)
    off = 24
    meta: dict[str, Any] = {}
    for _ in range(n_kv):
        if os.environ.get("WB_DEBUG"):
            print(f"DBG kv#{_} start_off={off}", file=sys.stderr)
        if off >= len(head) - 8:
            return False, {"err": f"kv 越界 #{_}"}
        key, off = _rs(head, off)
        (vt,) = struct.unpack_from("<I", head, off)
        off += 4
        size_, name, fmt = SCALAR.get(vt, (0, f"type{vt}", ""))
        if name == "string":
            val, off = _rs(head, off)
        elif name == "array":
            (et,) = struct.unpack_from("<I", head, off)
            off += 4
            (cnt,) = struct.unpack_from("<Q", head, off)
            off += 8
            items = []
            for _ in range(cnt):  # 必须全读才能对齐到下一 kv
                if off > len(head) - 16:
                    return False, {"err": f"array 越界 @{key}(cap 不足)"}
                it, off = _read_elem(head, off, et)
                if it is None and et not in SCALAR:
                    return False, {"err": f"array 未知元素类型 {et} @{key}"}
                if len(items) < 8:
                    items.append(it)
            val = items if cnt <= 8 else f"<array len={cnt} 前8:{items}>"
        elif name.startswith("type"):
            return False, {"err": f"未知 vt={vt} @{key}"}
        else:
            (val,) = struct.unpack_from("<" + fmt, head, off)
            off += size_
        meta[key] = val
    # tensor infos 区
    infos = []
    for i in range(n_tensors):
        if off >= len(head) - 8:
            return False, {"err": f"tensor info 越界 #{i}"}
        tname, off = _rs(head, off)
        (nd,) = struct.unpack_from("<I", head, off)
        off += 4
        dims = list(struct.unpack_from("<" + "Q" * nd, head, off))  # GGUF dims=u64
        off += 8 * nd
        (gt,) = struct.unpack_from("<i", head, off)
        off += 4
        (toff,) = struct.unpack_from("<Q", head, off)
        off += 8
        infos.append({"name": tname, "dims": dims, "type": gt, "offset": toff})
    data_start = (off + GGUF_ALIGN - 1) // GGUF_ALIGN * GGUF_ALIGN
    return True, {"version": ver, "tensor_count": n_tensors, "kv_count": n_kv,
                  "bytes": size, "meta": meta, "infos": infos,
                  "data_start": data_start, "head_size": off}


def nelem(dims):
    n = 1
    for d in dims:
        n *= d
    return n


def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return f"{n:.2f} {u}"
        n /= 1024


def _attn_tensors(infos):
    """注意力权重矩阵张量(二维·非 norm·非 bias)"""
    hits = []
    for t in infos:
        nm = t["name"].lower()
        if "norm" in nm or nm.endswith(".bias"):
            continue
        if len(t["dims"]) < 2:
            continue
        if any(k in nm for k in ("attn_qkv", "attn_q", "attn_k", "attn_v",
                                 "attn_output", "attn_out", "self_attn",
                                 "attention.q", "attention.k", "attention.v",
                                 "attention.o", "wq", "wk", "wv", "wo",
                                 ".attn.")):
            hits.append(t)
    return hits


def cmd_list(args):
    path = _arg(args, "--file")
    if not path or not os.path.isfile(path):
        print("🔴 --file 必需且存在")
        return 1
    n_show = int(_arg(args, "--tensors") or "24")
    ok, info = parse_header(path)
    if not ok:
        print(f"🔴 解析失败: {info.get('err')}")
        return 1
    print(f"🟢 GGUF v{info['version']} · {human(info['bytes'])} · 张量 {info['tensor_count']} · KV {info['kv_count']} · data@+{info['data_start']}")
    arch = info["meta"].get("general.architecture", "?")
    print(f"   arch={arch} · name={info['meta'].get('general.name','?')} · file_type={info['meta'].get('general.file_type','?')}")
    for k in sorted(info["meta"]):
        v = info["meta"][k]
        if k.startswith("tokenizer"):
            continue
        if isinstance(v, list):
            v = f"<list len={len(v)}>"
        if str(v).count(" ") > 40:
            v = str(v)[:120] + "…"
        print(f"   {k}: {v}")
    print(f"== 张量前 {n_show} (name | type | dims | off) ==")
    for t in info["infos"][:n_show]:
        print(f"   {t['name']:<46} {TNAME.get(t['type'], t['type'])} {t['dims']} @{t['offset']}")
    return 0


def _load_tensor(path, data_start, t):
    """流式读张量 → np.ndarray[out,in...] float64 | None
    GGUF 列主序(dims[0] 最内层)·numpy reshape(dims[::-1]) 还原 [out,in]
    type: 0=F32 1=F16 2=Q4_0(反量化) 其它量化暂不支持→None"""
    import numpy as np
    if t["type"] == 2:  # Q4_0: 每块 18B=2B f16 scale + 16B nibble(32 权重)
        prod = nelem(t["dims"])
        nblk = prod // 32
        pos = data_start + t["offset"]
        with open(path, "rb") as f:
            f.seek(pos)
            raw = f.read(nblk * 18)
        if len(raw) < nblk * 18:
            return None
        arr = _decode_q4_0(raw, nblk, t["dims"])
    else:
        b = TBYTES.get(t["type"])
        if b is None:
            return None
        dt = np.float16 if t["type"] == 1 else np.float32
        n = nelem(t["dims"])
        pos = data_start + t["offset"]
        with open(path, "rb") as f:
            f.seek(pos)
            raw = f.read(n * b)
        if len(raw) < n * b:
            return None
        a = np.frombuffer(raw, dtype=dt)
        if t["dims"]:
            a = a.reshape(list(reversed(t["dims"])))  # 列主序→[out,...,in]
        return a.astype(np.float64)
    return arr


Q4_LUT = None  # 懒加载(numpy 仅 weights 轨需要·list 轨保持纯 stdlib)


def _q4_lut():
    import numpy as np
    global Q4_LUT
    if Q4_LUT is None:
        lut = np.empty((256, 2), dtype=np.int16)
        for b in range(256):
            hi = (b >> 4) & 0x0F
            lo = b & 0x0F
            lut[b, 0] = lo - 16 if lo & 0x08 else lo
            lut[b, 1] = hi - 16 if hi & 0x08 else hi
        Q4_LUT = lut
    return Q4_LUT


def _decode_q4_0(raw, nblk, dims):
    """Q4_0 反量化(LUT 查表·快) → np.ndarray shape=dims(列主序还原) float64"""
    import numpy as np
    b = np.frombuffer(raw, dtype=np.uint8).reshape(nblk, 18)
    scales = b[:, :2].view(np.float16).astype(np.float64).reshape(nblk, 1)
    s = _q4_lut()[b[:, 2:].ravel()].reshape(nblk, 16, 2)  # (nblk,16,(lo,hi))
    vals = np.empty((nblk, 32), dtype=np.float64)
    vals[:, 0::2] = s[:, :, 0]
    vals[:, 1::2] = s[:, :, 1]
    vals *= scales
    if dims:
        return vals.reshape(-1).reshape(list(reversed(dims)))
    return vals.reshape(-1)


def _layout_note(name):
    """张量物理布局标注(自解释·防黑箱)·phi2 系 attn_qkv=QKV 三投影按行拼接"""
    nm = name.lower()
    if "qkv" in nm:
        return "qkv_stack(行序=q|k|v 三投影拼接·每投影同头数)"
    if "output" in nm or nm.endswith(".wo") or ".o." in nm:
        return "out_proj"
    for tag, lbl in ((".q", "q_proj"), (".k", "k_proj"), (".v", "v_proj")):
        if nm.endswith(tag):
            return lbl
    return "weights"


def _row_slice_heads(arr, head_dim=64):
    """权重 [out,in]→按 head_dim 行段分(每 head 一个 out 段)·支持 [out] 单维"""
    if arr.ndim == 1:
        return {"heads": 1, "rows": [arr]}
    out = arr.shape[0]
    if head_dim and out % head_dim == 0:
        heads = out // head_dim
    else:
        cand = [h for h in (4, 8, 16, 24, 32, 48, 64, 96, 128, 144)
                if out % h == 0]
        heads = cand[-1] if cand else 1
    hs = out // heads
    return {"heads": heads, "rows": [arr[i * hs:(i + 1) * hs] for i in range(heads)]}


def _summ(a):
    m = float(a.mean())
    return {"mean": round(m, 6), "std": round(float(a.std()), 6),
            "l2": round(float(np_l2(a)), 3), "min": round(float(a.min()), 4),
            "max": round(float(a.max()), 4)}


def np_l2(a):
    return float((a * a).sum()) ** 0.5


def _head_heat(arr, topk, head_dim=64):
    """每头段 L2 范数 + 每头绝对峰值 top-k → heatmap 数值矩阵"""
    hh = _row_slice_heads(arr, head_dim)
    heat = []
    tops = []
    for row in hh["rows"]:
        flat = row.ravel()
        heat.append(round(np_l2(flat), 4))
        idx = sorted(range(flat.size), key=lambda i: -abs(flat[i]))[:topk]
        tops.append([int(i) for i in idx])
    return hh["heads"], heat, tops


def cmd_weights(args):
    path = _arg(args, "--file")
    if not path or not os.path.isfile(path):
        print("🔴 --file 必需且存在")
        return 1
    prompt = _arg(args, "--prompt") or "龍魂系统自检"
    layers = _arg(args, "--layers") or "6"      # 默认取前 6 层(节能·可控)
    topk = int(_arg(args, "--topk") or "3")
    out_path = _arg(args, "--out") or ""
    ok, info = parse_header(path)
    if not ok:
        print(f"🔴 解析失败: {info.get('err')}")
        return 1
    attns = _attn_tensors(info["infos"])
    if not attns:
        print("🟡 未匹配到注意力张量(尝试 list --file 看命名)")
        return 1
    # 层分组: blk.N 或 .layer.N 提取编号
    import re
    def _lno(nm):
        m = re.search(r"blk\.(\d+)|\.(\d+)\.[^.]+\.(?:attn|self_attn)", nm)
        if m is None:
            return 0
        return int(m.group(1) or m.group(2) or 0)
    by_layer = {}
    for t in attns:
        by_layer.setdefault(_lno(t["name"]), []).append(t)
    lmax = max(by_layer)
    want_all = layers.lower() in ("all", "")
    try:
        want_n = int(layers)
    except ValueError:
        want_n = lmax + 1
    sel = sorted(by_layer)[:lmax + 1 if want_all else min(want_n, lmax + 1)]
    arch = info["meta"].get("general.architecture", "")
    em = info["meta"].get(f"{arch}.embedding_length")
    hc = info["meta"].get(f"{arch}.attention.head_count")
    head_dim = (em // hc) if (em and hc) else 64
    t0 = time.time()
    mats = []
    for layer_no in sel:
        for t in by_layer[layer_no]:
            a = _load_tensor(path, info["data_start"], t)
            if a is None:
                continue
            heads, heat, tops = _head_heat(a, topk, head_dim)
            mats.append({
                "layer": layer_no, "tensor": t["name"], "shape": t["dims"],
                "ggml_type": TNAME.get(t["type"], t["type"]),
                "heads": heads, "layout": _layout_note(t["name"]),
                "stat": _summ(a),
                "head_l2": heat,                 # heatmap 数值矩阵(n_head)
                "head_top_abs": tops,            # 每头 top-k 绝对峰位(flat)
            })
    out = {
        "_meta": {
            "dna": "#龍芯⚡️丙午·丁酉·癸未·午时-WHITEBOX-PROBE-v1.0-UID9622",
            "engine": "lh_whitebox_probe.py v1.0",
            "model_file": os.path.basename(path),
            "model_bytes": info["bytes"],
            "prompt_input": prompt,
            "layers": sel,
            "topk": topk,
            "scope": "L1 权重层白盒(静态·与prompt无耦合·prompt为锚记录)",
            "deterministic": True,
            "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
            "elapsed_s": round(time.time() - t0, 2),
            "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
        },
        "matrices": mats,
    }
    # 稳定性指纹: 仅矩阵+固定参数(不随 ts/elapsed 变)→ 同参必同哈希 = 真可复现
    stable = json.dumps({"mats": mats, "prompt": prompt, "layers": sel,
                         "topk": topk, "model_file": os.path.basename(path)},
                        ensure_ascii=False, sort_keys=True)
    sha = hashlib_sha256(stable)
    out["_meta"]["sha256"] = sha
    print(f"🟢 L1 权重白盒 · {os.path.basename(path)} · 层 {len(sel)} · 注意力张量 {len(mats)}")
    print(f"   prompt锚=「{prompt}」 · 确定性=True(同参可重现) · {out['_meta']['elapsed_s']}s")
    for m in mats:
        hl = m["head_l2"]
        hh = " ".join(f"{h:.1f}" for h in hl)
        lay = "qkv3×32" if "qkv" in m["layout"] else ""
        print(f"   blk.{m['layer']:<3} {m['tensor'].split('.')[-2]:<11} "
              f"{m['heads']:>3}段{lay:<7} mean={m['stat']['mean']:.4f} "
              f"l2={m['stat']['l2']:.1f} | headL2: {hh}")
    print(f"   SHA256={sha}")
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(out, ensure_ascii=False, indent=1))
        print(f"   → {out_path} ({human(os.path.getsize(out_path))})")
    return 0


def hashlib_sha256(s):
    import hashlib
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def cmd_llm(args):
    """L2/L3 前向层骨架·如实🟡——实机前向需推理引擎(mlx_lm/llama.cpp)"""
    prompt = _arg(args, "--prompt") or "龍魂系统自检"
    print(f"== LLM 前向层探针(L2/L3) · prompt「{prompt}」 ==")
    # ① mlx 前向引擎可用性(真白盒候选: base_models_v4.0/Meta-Llama-3.1-8B-Instruct)
    import importlib.util
    mlx_ok = importlib.util.find_spec("mlx.core") is not None
    print(f"🟡 L2 隐层激活抽样: 需前向(embed→RMSNorm→attn→FFN 中间值)·"
          f"mlx={'可用' if mlx_ok else '不可用'} → 待 mlx 前向轨实机(下棒)")
    # ② ollama logprobs 抽测(零侵入·L3 雏形候选)
    use_ollama = _arg(args, "--ollama") or "1"
    if use_ollama == "1":
        try:
            import urllib.request
            req = urllib.request.Request(
                "http://127.0.0.1:11434/api/tags",
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=3) as r:
                tags = json.loads(r.read())
            has = [m["name"] for m in tags.get("models", [])]
            print(f"   ollama 运行中({len(has)} 模型) → logprobs 抽测候选: "
                  f"{[m for m in has if 'moondream' in m or 'qwen' in m][:3]}")
        except Exception as e:
            print(f"   🟡 ollama 未运行/不可达({type(e).__name__}) → logprobs 抽测跳过·L3 留🟡")
    else:
        print("   --ollama 0 → 跳过 logprobs 抽测")
    print("🟡 L3 token 归因: 需前向 logits(softmax 概率→归因)·待前向轨后逐token实测")
    print("   下一步(前向轨方案): mlx_lm.load(base_models_v4.0/Meta-Llama-3.1-8B-Instruct·4bit) "
          "+ 自定义逐层 forward 钩子取 hidden/attn → L2/L3 升绿候选")
    return 0


def cmd_summary():
    print("lh_whitebox_probe v1.0 · GGUF 张量级白盒 + LLM 前向骨架")
    print("  L1 权重层(🟢可实机): 注意力权重矩阵统计+head热力+SHA256·同参可重现")
    print("  L2/L3 前向层(🟡待前向轨): 隐层激活/token归因需推理引擎实机")
    print("  DNA: #龍芯⚡️丙午·丁酉·癸未·午时-WHITEBOX-PROBE-v1.0-UID9622")
    print(f"  GPG: {GPG} · 台账 T2 证据指针(2026-09-06)")


def _arg(args, flag):
    if flag in args:
        i = args.index(flag)
        return args[i + 1] if len(args) > i + 1 else ""
    return ""


def main():
    args = sys.argv[1:]
    if not args:
        return cmd_summary()
    c, rest = args[0], args[1:]
    if c == "list":
        return cmd_list(rest)
    if c == "weights":
        return cmd_weights(rest)
    if c == "llm":
        return cmd_llm(rest)
    if c == "summary":
        return cmd_summary()
    print("用法: list --file <gguf> | weights --file <gguf> [--prompt] [--layers] [--topk] [--out] | llm | summary")
    return 1


if __name__ == "__main__":
    sys.exit(main())
