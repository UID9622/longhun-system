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
  文件: README.md | 标记时间: 2026-06-03T07:46:00+0800
-->
# cvector-generator

This example demonstrates how to generate a control vector using gguf models.

Related PRs:
- [Add support for control vectors](https://github.com/ggml-org/llama.cpp/pull/5970)
- (Issue) [Generate control vector using llama.cpp](https://github.com/ggml-org/llama.cpp/issues/6880)
- [Add cvector-generator example](https://github.com/ggml-org/llama.cpp/pull/7514)

## Examples

```sh
# CPU only
./cvector-generator -m ./llama-3.Q4_K_M.gguf

# With GPU
./cvector-generator -m ./llama-3.Q4_K_M.gguf -ngl 99

# With advanced options
./cvector-generator -m ./llama-3.Q4_K_M.gguf -ngl 99 --pca-iter 2000 --pca-batch 100

# Using mean value instead of PCA
./cvector-generator -m ./llama-3.Q4_K_M.gguf --method mean

# To see help message
./cvector-generator -h
# Then, have a look at "cvector" section
```

## Tips and tricks

If you have multiple lines per prompt, you can escape the newline character (change it to `\n`). For example:

```
<|im_start|>system\nAct like a person who is extremely happy.<|im_end|>
<|im_start|>system\nYou are in a very good mood today<|im_end|>
```

Example to use output file with `llama-cli`:

(Tips: The control vector works better when apply to layers higher than 10)

```sh
./llama-cli -m ./llama-3.Q4_K_M.gguf -p "<|start_header_id|>system<|end_header_id|>\n\nYou are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>\n\nSing a song<|im_end|><|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n" --special --control-vector-scaled ./control_vector.gguf 0.8 --control-vector-layer-range 10 31
```

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-78f24bbb-20251218032410
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 乾卦：天行健，君子以自强不息
📜 内容哈希: 580d4b9585dffc9a
⚠️ 警告: 未经授权修改将触发DNA追溯系统
