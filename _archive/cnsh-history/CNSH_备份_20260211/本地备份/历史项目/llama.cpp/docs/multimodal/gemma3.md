<!--
  龍魂·六层来源链 / LongHun Six-Layer Source Chain
  1 道统层 Dao           : 曾仕强老师
  2 精神层 Spirit        : Steve Jobs
  3 设备层 Device        : Apple
  4 技术层 Technology    : Open Source
  5 系统层 System        : UID9622
  6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
  DNA追溯码: #龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-v2.0
  铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
  文件: gemma3.md | 标记时间: 2026-06-03T07:46:00+0800
-->
# Gemma 3 vision

> [!IMPORTANT]
>
> This is very experimental, only used for demo purpose.

## Quick started

You can use pre-quantized model from [ggml-org](https://huggingface.co/ggml-org)'s Hugging Face account

```bash
# build
cmake -B build
cmake --build build --target llama-mtmd-cli

# alternatively, install from brew (MacOS)
brew install llama.cpp

# run it
llama-mtmd-cli -hf ggml-org/gemma-3-4b-it-GGUF
llama-mtmd-cli -hf ggml-org/gemma-3-12b-it-GGUF
llama-mtmd-cli -hf ggml-org/gemma-3-27b-it-GGUF

# note: 1B model does not support vision
```

## How to get mmproj.gguf?

Simply to add `--mmproj` in when converting model via `convert_hf_to_gguf.py`:

```bash
cd gemma-3-4b-it
python ../llama.cpp/convert_hf_to_gguf.py --outfile model.gguf --outtype f16 --mmproj .
# output file: mmproj-model.gguf
```

## How to run it?

What you need:
- The text model GGUF, can be converted using `convert_hf_to_gguf.py`
- The mmproj file from step above
- An image file

```bash
# build
cmake -B build
cmake --build build --target llama-mtmd-cli

# run it
./build/bin/llama-mtmd-cli -m {text_model}.gguf --mmproj mmproj.gguf --image your_image.jpg
```

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-cabc982b-20251218032410
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 坤卦：地势坤，君子以厚德载物
📜 内容哈希: 57e49f25cd5363e0
⚠️ 警告: 未经授权修改将触发DNA追溯系统
