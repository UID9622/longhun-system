## Convert llama2.c model to ggml

This example reads weights from project [llama2.c](https://github.com/karpathy/llama2.c) and saves them in ggml compatible format. The vocab that is available in `models/ggml-vocab.bin` is used by default.

To convert the model first download the models from the [llama2.c](https://github.com/karpathy/llama2.c) repository.

```
usage: ./llama-convert-llama2c-to-ggml [options]

options:
  -h, --help                       show this help message and exit
  --copy-vocab-from-model FNAME    path of gguf llama model or llama2.c vocabulary from which to copy vocab (default 'models/7B/ggml-model-f16.gguf')
  --llama2c-model FNAME            [REQUIRED] model path from which to load Karpathy's llama2.c model
  --llama2c-output-model FNAME     model path to save the converted llama2.c model (default ak_llama_model.bin')
```

An example command using a model from [karpathy/tinyllamas](https://huggingface.co/karpathy/tinyllamas) is as follows:

`$ ./llama-convert-llama2c-to-ggml --copy-vocab-from-model llama-2-7b-chat.gguf.q2_K.bin --llama2c-model stories42M.bin --llama2c-output-model stories42M.gguf.bin`

Note: The vocabulary for `stories260K.bin` should be its own tokenizer `tok512.bin` found in [karpathy/tinyllamas/stories260K](https://huggingface.co/karpathy/tinyllamas/tree/main/stories260K).

Now you can use the model with a command like:

`$ ./llama-cli -m stories42M.gguf.bin -p "One day, Lily met a Shoggoth" -n 500 -c 256`

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-de728b89-20251218032410
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 蒙卦：山下出泉，君子以果行育德
📜 内容哈希: 374883b2360b547e
⚠️ 警告: 未经授权修改将触发DNA追溯系统
