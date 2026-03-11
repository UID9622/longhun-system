# GLMV-EDGE

Currently this implementation supports [glm-edge-v-2b](https://huggingface.co/THUDM/glm-edge-v-2b) and [glm-edge-v-5b](https://huggingface.co/THUDM/glm-edge-v-5b).

## Usage
Build the `llama-mtmd-cli` binary.

After building, run: `./llama-mtmd-cli` to see the usage. For example:

```sh
./llama-mtmd-cli -m model_path/ggml-model-f16.gguf --mmproj model_path/mmproj-model-f16.gguf
```

**note**: A lower temperature like 0.1 is recommended for better quality. add `--temp 0.1` to the command to do so.
**note**: For GPU offloading ensure to use the `-ngl` flag just like usual

## GGUF conversion

1. Clone a GLMV-EDGE model ([2B](https://huggingface.co/THUDM/glm-edge-v-2b) or [5B](https://huggingface.co/THUDM/glm-edge-v-5b)). For example:

```sh
git clone https://huggingface.co/THUDM/glm-edge-v-5b or https://huggingface.co/THUDM/glm-edge-v-2b
```

2. Use `glmedge-surgery.py` to split the GLMV-EDGE model to LLM and multimodel projector constituents:

```sh
python ./tools/mtmd/glmedge-surgery.py -m ../model_path
```

4. Use `glmedge-convert-image-encoder-to-gguf.py` to convert the GLMV-EDGE image encoder to GGUF:

```sh
python ./tools/mtmd/glmedge-convert-image-encoder-to-gguf.py -m ../model_path --llava-projector ../model_path/glm.projector --output-dir ../model_path
```

5. Use `examples/convert_hf_to_gguf.py` to convert the LLM part of GLMV-EDGE to GGUF:

```sh
python convert_hf_to_gguf.py ../model_path
```

Now both the LLM part and the image encoder are in the `model_path` directory.

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-96b669a7-20251218032410
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 屯卦：云雷屯，君子以经纶
📜 内容哈希: 436fd6e282d16942
⚠️ 警告: 未经授权修改将触发DNA追溯系统
