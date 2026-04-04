# llama.cpp/examples/training

This directory contains examples related to language model training using llama.cpp/GGML.
So far finetuning is technically functional (for FP32 models and limited hardware setups) but the code is very much WIP.
Finetuning of Stories 260K and LLaMA 3.2 1b seems to work with 24 GB of memory.
**For CPU training, compile llama.cpp without any additional backends such as CUDA.**
**For CUDA training, use the maximum number of GPU layers.**

Proof of concept:

``` sh
export model_name=llama_3.2-1b && export quantization=f32
./build/bin/llama-finetune --file wikitext-2-raw/wiki.test.raw -ngl 999 --model models/${model_name}-${quantization}.gguf -c 512 -b 512 -ub 512
./build/bin/llama-perplexity --file wikitext-2-raw/wiki.test.raw -ngl 999 --model finetuned-model.gguf
```

The perplexity value of the finetuned model should be lower after training on the test set for 2 epochs.

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-e17d3dd6-20251218032410
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 屯卦：云雷屯，君子以经纶
📜 内容哈希: 133d214188b1c930
⚠️ 警告: 未经授权修改将触发DNA追溯系统
