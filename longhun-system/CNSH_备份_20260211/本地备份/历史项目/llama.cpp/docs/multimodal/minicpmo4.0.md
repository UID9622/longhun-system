## MiniCPM-o 4

### Prepare models and code

Download [MiniCPM-o-4](https://huggingface.co/openbmb/MiniCPM-o-4) PyTorch model from huggingface to "MiniCPM-o-4" folder.


### Build llama.cpp
Readme modification time: 20250206

If there are differences in usage, please refer to the official build [documentation](https://github.com/ggerganov/llama.cpp/blob/master/docs/build.md)

Clone llama.cpp:
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
```

Build llama.cpp using `CMake`:
```bash
cmake -B build
cmake --build build --config Release
```


### Usage of MiniCPM-o 4

Convert PyTorch model to gguf files (You can also download the converted [gguf](https://huggingface.co/openbmb/MiniCPM-o-4-gguf) by us)

```bash
python ./tools/mtmd/legacy-models/minicpmv-surgery.py -m ../MiniCPM-o-4
python ./tools/mtmd/legacy-models/minicpmv-convert-image-encoder-to-gguf.py -m ../MiniCPM-o-4 --minicpmv-projector ../MiniCPM-o-4/minicpmv.projector --output-dir ../MiniCPM-o-4/ --minicpmv_version 6
python ./convert_hf_to_gguf.py ../MiniCPM-o-4/model

# quantize int4 version
./build/bin/llama-quantize ../MiniCPM-o-4/model/ggml-model-f16.gguf ../MiniCPM-o-4/model/ggml-model-Q4_K_M.gguf Q4_K_M
```


Inference on Linux or Mac
```bash
# run in single-turn mode
./build/bin/llama-mtmd-cli -m ../MiniCPM-o-4/model/ggml-model-f16.gguf --mmproj ../MiniCPM-o-4/mmproj-model-f16.gguf -c 4096 --temp 0.7 --top-p 0.8 --top-k 100 --repeat-penalty 1.05 --image xx.jpg -p "What is in the image?"

# run in conversation mode
./build/bin/llama-mtmd-cli -m ../MiniCPM-o-4/model/ggml-model-Q4_K_M.gguf --mmproj ../MiniCPM-o-4/mmproj-model-f16.gguf
```

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-1062ae31-20251218032410
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 乾卦：天行健，君子以自强不息
📜 内容哈希: 09abd50f403b9ed4
⚠️ 警告: 未经授权修改将触发DNA追溯系统
