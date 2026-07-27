#!/usr/bin/env python3
"""龍魂 v4.1.4 MLX merged → GGUF 导出器（轻量·无需llama.cpp）
DNA: #龍芯⚡️丙午·癸未·丁亥·☲离-EXPORT-GGUF-v4.1.4
用法: python3 bin/lh_export_gguf_v414.py
"""

import json, os, sys, struct, numpy as np
from pathlib import Path
import torch
from safetensors import safe_open
from gguf import GGUFWriter, GGMLQuantizationType

# 必须保持 F32 的张量名模式（norm/embedding 层）
MUST_F32_PATTERNS = [
    "token_embd.weight",
    "output_norm.weight",
    "attn_norm.weight",
    "ffn_norm.weight",
]
from transformers import AutoTokenizer

PROJECT = Path(__file__).resolve().parent.parent
MERGED_DIR = PROJECT / "models" / "longhun-v1.0" / "lora_output_v414" / "merged_v414"
GGUF_DIR = PROJECT / "models" / "longhun-v1.0" / "lora_output_v414" / "gguf_v414"
GGUF_PATH = GGUF_DIR / "longhun-v4.1.4.F16.gguf"

def run():
    GGUF_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. 读 config
    with open(MERGED_DIR / "config.json") as f:
        config = json.load(f)
    
    arch = config.get("model_type", "llama")
    print(f"📋 架构: {arch} | hidden_size={config['hidden_size']} | layers={config['num_hidden_layers']}")
    
    # 2. 读 tokenizer
    tokenizer = AutoTokenizer.from_pretrained(str(MERGED_DIR), local_files_only=True)
    vocab = tokenizer.get_vocab()
    print(f"📝 词表: {len(vocab)} tokens")
    
    # 3. 创建 GGUF writer
    gguf = GGUFWriter(str(GGUF_PATH), arch)
    
    # 写入架构元数据（arch 已在构造函数中设置，无需 add_architecture）
    gguf.add_context_length(config.get("max_position_embeddings", 2048))
    gguf.add_embedding_length(config["hidden_size"])
    gguf.add_block_count(config["num_hidden_layers"])
    gguf.add_feed_forward_length(config.get("intermediate_size", config["hidden_size"] * 8 // 3))
    gguf.add_head_count(config["num_attention_heads"])
    if "num_key_value_heads" in config:
        gguf.add_head_count_kv(config["num_key_value_heads"])
    gguf.add_layer_norm_rms_eps(config.get("rms_norm_eps", 1e-6))
    rope_dim = config.get("hidden_size", 4096) // config.get("num_attention_heads", 32)
    gguf.add_rope_dimension_count(rope_dim)
    gguf.add_rope_freq_base(config.get("rope_theta", 500000.0))
    
    # 词汇表
    gguf.add_tokenizer_model("llama")
    
    # 写入词汇
    tokens = []
    scores = []
    token_types = []
    merges = []
    bos_id = tokenizer.bos_token_id or 1
    eos_id = tokenizer.eos_token_id or 2
    
    for i in range(tokenizer.vocab_size):
        tok = tokenizer.convert_ids_to_tokens(i) or ""
        tokens.append(tok)
        scores.append(0.0)
        token_types.append(1)  # NORMAL
    
    gguf.add_token_list(tokens)
    gguf.add_token_scores(scores)
    gguf.add_token_types(token_types)
    gguf.add_bos_token_id(bos_id)
    gguf.add_eos_token_id(eos_id)
    
    # 4. 加载 safetensors 权重
    idx_path = MERGED_DIR / "model.safetensors.index.json"
    if idx_path.exists():
        with open(idx_path) as f:
            weight_map = json.load(f)["weight_map"]
        shard_files = sorted(set(weight_map.values()))
    else:
        shard_files = sorted(f for f in os.listdir(MERGED_DIR) if f.startswith("model-") and f.endswith(".safetensors"))
    
    print(f"📦 {len(shard_files)} 分片")
    
    from gguf import GGMLQuantizationType
    
    tensor_count = 0
    for shard_name in shard_files:
        shard_path = MERGED_DIR / shard_name
        # bfloat16 → float16: numpy 不原生支持 bf16，用 torch 中转
        with safe_open(str(shard_path), framework="pt") as sf:
            for key in sf.keys():
                tensor_pt = sf.get_tensor(key)
                
                # 转换名称: HF → GGUF
                gguf_name = _hf_to_gguf(key)
                if gguf_name is None:
                    continue
                
                # 判断是否需要 F32（norm/embedding 层必须 F32）
                need_f32 = any(gguf_name.endswith(p) for p in MUST_F32_PATTERNS)
                target_dtype = torch.float32 if need_f32 else torch.float16
                quant_type = GGMLQuantizationType.F32 if need_f32 else GGMLQuantizationType.F16
                
                tensor_np = tensor_pt.to(dtype=target_dtype).numpy()
                
                gguf.add_tensor(gguf_name, tensor_np, raw_dtype=quant_type)
                tensor_count += 1
                if tensor_count <= 10 or tensor_count % 50 == 0:
                    dtype_tag = "F32" if need_f32 else "F16"
                    print(f"  [{tensor_count}] {key} → {gguf_name} ({list(tensor_np.shape)}) [{dtype_tag}]")
    
    # 5. 写入
    print(f"\n💾 写入 GGUF → {GGUF_PATH}")
    gguf.write_header_to_file()
    gguf.write_kv_data_to_file()
    gguf.write_tensors_to_file()
    gguf.close()
    
    size_gb = GGUF_PATH.stat().st_size / 1e9
    print(f"✅ 完成: {GGUF_PATH} ({size_gb:.1f} GB)")


def _hf_to_gguf(hf_name: str):
    """HuggingFace 参数名 → GGUF 参数名"""
    # 映射规则
    mappings = {
        "model.embed_tokens.weight": "token_embd.weight",
        "model.norm.weight": "output_norm.weight",
        "lm_head.weight": "output.weight",
    }
    
    if hf_name in mappings:
        return mappings[hf_name]
    
    # model.layers.N.xxx → blk.N.xxx
    parts = hf_name.split(".")
    if parts[0] == "model" and parts[1] == "layers":
        layer_idx = parts[2]
        sub = ".".join(parts[3:])
        
        layer_map = {
            "input_layernorm.weight": f"blk.{layer_idx}.attn_norm.weight",
            "post_attention_layernorm.weight": f"blk.{layer_idx}.ffn_norm.weight",
            "self_attn.q_proj.weight": f"blk.{layer_idx}.attn_q.weight",
            "self_attn.k_proj.weight": f"blk.{layer_idx}.attn_k.weight",
            "self_attn.v_proj.weight": f"blk.{layer_idx}.attn_v.weight",
            "self_attn.o_proj.weight": f"blk.{layer_idx}.attn_output.weight",
            "mlp.gate_proj.weight": f"blk.{layer_idx}.ffn_gate.weight",
            "mlp.up_proj.weight": f"blk.{layer_idx}.ffn_up.weight",
            "mlp.down_proj.weight": f"blk.{layer_idx}.ffn_down.weight",
        }
        return layer_map.get(sub)
    
    return None


if __name__ == "__main__":
    run()
