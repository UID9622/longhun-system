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
# export-lora

Apply LORA adapters to base model and export the resulting model.

```
usage: llama-export-lora [options]

options:
  -m,    --model                  model path from which to load base model (default '')
         --lora FNAME             path to LoRA adapter  (can be repeated to use multiple adapters)
         --lora-scaled FNAME S    path to LoRA adapter with user defined scaling S  (can be repeated to use multiple adapters)
  -t,    --threads N              number of threads to use during computation (default: 4)
  -o,    --output FNAME           output file (default: 'ggml-lora-merged-f16.gguf')
```

For example:

```bash
./bin/llama-export-lora \
    -m open-llama-3b-v2.gguf \
    -o open-llama-3b-v2-english2tokipona-chat.gguf \
    --lora lora-open-llama-3b-v2-english2tokipona-chat-LATEST.gguf
```

Multiple LORA adapters can be applied by passing multiple `--lora FNAME` or `--lora-scaled FNAME S` command line parameters:

```bash
./bin/llama-export-lora \
    -m your_base_model.gguf \
    -o your_merged_model.gguf \
    --lora-scaled lora_task_A.gguf 0.5 \
    --lora-scaled lora_task_B.gguf 0.5
```

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-95e66795-20251218032410
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 坤卦：地势坤，君子以厚德载物
📜 内容哈希: 229f6864467d8170
⚠️ 警告: 未经授权修改将触发DNA追溯系统
