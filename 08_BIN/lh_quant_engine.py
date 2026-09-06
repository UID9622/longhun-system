#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🐉 龍魂系统 · 量化引擎 v1.0（GGUF/AWQ/GPTQ 三轨探测·消费级硬件命门）
# DNA: #龍芯⚡️丙午·丁酉·癸未·巳时·QUANT-ENGINE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 立项: D-03 老大拍板(2026-09-06)「追·软件量化绕硬件限制」· 台账 B4 缺口指针
# 功能: 三轨量化探测——
#   GGUF轨: 纯标准库解析 GGUF 文件头+metadata kv(llama.cpp/ollama 实机可跑·CPU)
#   AWQ轨 : 探测 HF 模型目录 config.json 的 quantization_config.quant_method=='awq'
#   GPTQ轨: 同目录法 quant_method=='gptq'
# 用法:
#   python3 08_BIN/lh_quant_engine.py gguf --file <model.gguf>   # 解析单个 GGUF
#   python3 08_BIN/lh_quant_engine.py gguf --ollama [N]         # 扫 ~/.ollama GGUF blobs
#   python3 08_BIN/lh_quant_engine.py dir  --model <dir>        # AWQ/GPTQ/FP16 目录探测
#   python3 08_BIN/lh_quant_engine.py summary                   # 引擎速览
# 原则: 按需触发·用完即沉默·GGUF metadata 全部直读文件实机取证(不臆造)·
#       file_type 编号按 llama.cpp ggml_ftype 惯例近似映射(未知显示编号)
import json
import os
import struct
import sys

GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GGUF_MAGIC = b"GGUF"
MAX_READ = 1 << 20  # metadata 区读取上限 1MB(足够·禁整文件入内存)

# GGUF value_type 编号 → (定长字节, 名称)  (ggml_type 附录惯例·容错解析)
SCALAR = {0: (1, "u8"), 1: (1, "i8"), 2: (2, "u16"), 3: (2, "i16"),
          4: (4, "u32"), 5: (4, "i32"), 6: (4, "f32"), 7: (1, "bool"),
          8: (-1, "string"), 9: (-2, "array"),
          10: (8, "u64"), 11: (8, "i64"), 12: (8, "f64")}

# llama.cpp ggml_ftype 惯例映射(常见子集·未列编号显示原始值不硬猜)
FILE_TYPES = {0: "F32", 1: "F16", 2: "Q4_0", 3: "Q4_1", 6: "Q5_0", 7: "Q5_1",
              8: "Q8_0", 10: "Q2_K", 11: "Q3_K", 12: "Q4_K", 13: "Q5_K",
              14: "Q6_K", 15: "Q8_K", 16: "IQ2_XXS", 17: "IQ2_XS", 18: "IQ3_XXS",
              19: "IQ1_S", 20: "IQ4_NL", 21: "IQ3_S", 22: "IQ2_S", 23: "IQ4_XS"}


def _ftype_name(n):
    return FILE_TYPES.get(n, f"file_type={n}")


def _rs(buf, off):
    """GGUF 字符串: u64 长度前缀 + utf8"""
    (n,) = struct.unpack_from("<Q", buf, off)
    off += 8
    return buf[off:off + n].decode("utf-8", "replace"), off + n


def _read_kv(buf, off):
    """读一个 metadata kv → (key, value, new_off)。标量/string 平铺返回。"""
    key, off = _rs(buf, off)
    (vt,) = struct.unpack_from("<I", buf, off)
    off += 4
    size, name = SCALAR.get(vt, (0, f"type{vt}"))
    if name == "string":
        val, off = _rs(buf, off)
    elif name.startswith("type"):
        val = None
    elif vt == 9:  # array: elem_type u32 + count u64 + items
        (et,) = struct.unpack_from("<I", buf, off)
        off += 4
        (cnt,) = struct.unpack_from("<Q", buf, off)
        off += 8
        items = []
        for _ in range(cnt):
            it, off = _read_elem(buf, off, et)
            items.append(it)
        val = items
    else:  # 定长标量
        (val,) = struct.unpack_from("<" + _fmt(name), buf, off)
        off += size
    return key, val, off


def _read_elem(buf, off, vt):
    size, name = SCALAR.get(vt, (0, f"type{vt}"))
    if name == "string":
        return _rs(buf, off)
    if name.startswith("type"):
        return None, off
    if vt == 9:  # 嵌套 array 少见·取空防死循环
        return [], off
    (val,) = struct.unpack_from("<" + _fmt(name), buf, off)
    return val, off + size


def _fmt(name):
    return {"u8": "B", "i8": "b", "u16": "H", "i16": "h", "u32": "I",
            "i32": "i", "f32": "f", "bool": "B", "u64": "Q", "i64": "q",
            "f64": "d"}[name]


def parse_gguf(path, cap=MAX_READ):
    """解析 GGUF 头部+metadata → (ok, meta_dict|err)"""
    size = os.path.getsize(path)
    if size < 24:
        return False, {"err": "文件过小·非 GGUF"}
    with open(path, "rb") as f:
        buf = f.read(min(size, cap))
    if buf[:4] != GGUF_MAGIC:
        return False, {"err": f"magic 非 GGUF: {buf[:4]!r}"}
    (ver,) = struct.unpack_from("<I", buf, 4)
    (tensors,) = struct.unpack_from("<Q", buf, 8)
    (kv_n,) = struct.unpack_from("<Q", buf, 16)
    off = 24
    meta = {"magic": "GGUF", "version": ver, "tensor_count": tensors,
            "kv_count": kv_n, "bytes": size}
    # 抽感兴趣字段(不 dump 全部·词表数组跳过)
    want_prefix = ("general.", "llama.", "qwen2.", "gemma.", "mistral.",
                   "phi3.", "deepseek", "baichuan")
    for _ in range(kv_n):
        if off >= len(buf) - 8:
            break
        key, val, off = _read_kv(buf, off)
        if key.startswith(want_prefix):
            if isinstance(val, list) and len(val) > 64:
                val = f"<array len={len(val)}>"
            meta[key] = val
    return True, meta


def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return f"{n:.2f} {u}"
        n /= 1024


def _print_gguf(path):
    ok, m = parse_gguf(path)
    if not ok:
        print(f"  🔴 {os.path.basename(path)[:24]}: {m.get('err')}")
        return 0
    arch = m.get("general.architecture", "?")
    name = m.get("general.name", "")
    ft = _ftype_name(m.get("general.file_type", "?")) if m.get("general.file_type") is not None else "?"
    ctx = m.get(f"{arch}.context_length") or m.get("llama.context_length")
    blk = m.get(f"{arch}.block_count") or m.get("llama.block_count")
    line = f"  🟢 GGUF v{m['version']} | {name or os.path.basename(path)[:20]} | {arch} | {ft} | {human(m['bytes'])}"
    extra = []
    if blk:
        extra.append(f"{blk}层")
    if ctx:
        extra.append(f"ctx={ctx}")
    if extra:
        line += " | " + "·".join(extra)
    print(line)
    return 1


def cmd_gguf(args):
    if "--file" in args:
        i = args.index("--file")
        path = args[i + 1] if len(args) > i + 1 else ""
        if not os.path.isfile(path):
            print(f"🔴 文件不存在: {path}")
            return 1
        ok, m = parse_gguf(path)
        if not ok:
            print(f"🔴 解析失败: {m.get('err')}")
            return 1
        print(f"🟢 GGUF 解析成功 v{m['version']} · 张量 {m['tensor_count']} · 元数据 {m['kv_count']} 条")
        for k in sorted(m):
            if k in ("magic", "version", "tensor_count", "kv_count", "bytes"):
                continue
            if "tokenizer.ggml.tokens" in k:
                continue
            print(f"   {k}: {m[k]}")
        print(f"  文件大小: {human(m['bytes'])}")
        return 0
    if "--ollama" in args:
        blob_dir = os.path.expanduser("~/.ollama/models/blobs")
        n_limit = 24
        if "--ollama" in args and len(args) > args.index("--ollama") + 1:
            try:
                n_limit = int(args[args.index("--ollama") + 1])
            except ValueError:
                pass
        if not os.path.isdir(blob_dir):
            print(f"🔴 未找到 ollama blobs: {blob_dir}")
            return 1
        files = [os.path.join(blob_dir, f) for f in os.listdir(blob_dir)]
        hit = 0
        print(f"== ollama blobs GGUF 扫描 ({len(files)} 候选·上限 {n_limit}) ==")
        for p in files:
            try:
                ok, m = parse_gguf(p)
            except Exception:
                continue
            if ok:
                hit += 1
                _print_gguf(p)
                if hit >= n_limit:
                    break
        print(f"命中 GGUF: {hit}")
        return 0
    print("用法: gguf --file <path> | gguf --ollama [N]")
    return 1


def cmd_dir(model_dir):
    if not os.path.isdir(model_dir):
        print(f"🔴 目录不存在: {model_dir}")
        return 1
    cfg = None
    root = model_dir
    for d in (model_dir,):
        c = os.path.join(d, "config.json")
        if os.path.isfile(c):
            cfg = json.load(open(c, encoding="utf-8"))
            root = d
            break
    if cfg is None:
        print(f"🔴 未找到 config.json(AWQ/GPTQ 轨需要 HF 目录结构)")
        return 1
    qc = cfg.get("quantization_config") or {}
    qm = (qc.get("quant_method") or "").lower()
    mt = cfg.get("model_type", "?")
    total = 0
    for fn in os.listdir(root):
        if fn.endswith((".safetensors", ".bin", ".gguf")):
            total += os.path.getsize(os.path.join(root, fn))
    head = f"{mt}"
    if qm == "awq":
        color, tag = "🟢", "AWQ 已量化"
        extra = f"bits={qc.get('bits')} group_size={qc.get('group_size')}"
    elif qm == "gptq":
        color, tag = "🟢", "GPTQ 已量化"
        extra = f"bits={qc.get('bits')} group_size={qc.get('group_size')}"
    else:
        color, tag = "🟡", "未检出量化(FP16/FP32/BF16)"
        extra = f"torch_dtype={cfg.get('torch_dtype')} architectures={cfg.get('architectures')}"
    print(f"{color} {tag} | {head} | 权重总大小 {human(total)}")
    print(f"   {extra}")
    if qm:
        print(f"   method={qm} quant config 直读 config.json (实机取证)")
    return 0


def cmd_summary():
    print("lh_quant_engine v1.0 · GGUF/AWQ/GPTQ 三轨探测")
    print(f"  GGUF轨: 纯 stdlib 解析(ollama/llama.cpp 兼容·CPU 实机)  |  awq/gptq轨: config.json 直读")
    print(f"  DNA: #龍芯⚡️丙午·丁酉·癸未·巳时·QUANT-ENGINE-v1.0-UID9622")
    print(f"  GPG: {GPG}  |  台账: B4 证据指针(D-03·2026-09-06)")
    return 0


def main():
    args = sys.argv[1:]
    if not args:
        return cmd_summary()
    c, rest = args[0], args[1:]
    if c == "gguf":
        return cmd_gguf(rest)
    if c == "dir":
        i = rest.index("--model") if "--model" in rest else -1
        p = rest[i + 1] if i >= 0 and len(rest) > i + 1 else ""
        return cmd_dir(p)
    if c == "summary":
        return cmd_summary()
    print("用法: summary | gguf --file <path> | gguf --ollama [N] | dir --model <dir>")
    return 1


if __name__ == "__main__":
    sys.exit(main())
