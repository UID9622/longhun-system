# llama.cpp/example/parallel

Simplified simulation of serving incoming requests in parallel

## Example

Generate 128 client requests (`-ns 128`), simulating 8 concurrent clients (`-np 8`). The system prompt is shared (`-pps`), meaning that it is computed once at the start. The client requests consist of up to 10 junk questions (`--junk 10`) followed by the actual question.

```bash
llama-parallel -m model.gguf -np 8 -ns 128 --top-k 1 -pps --junk 10 -c 16384
```

> [!NOTE]
> It's recommended to use base models with this example. Instruction tuned models might not be able to properly follow the custom chat template specified here, so the results might not be as expected.

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-6a55fcc5-20251218032410
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 坤卦：地势坤，君子以厚德载物
📜 内容哈希: f3c97fc5d4679899
⚠️ 警告: 未经授权修改将触发DNA追溯系统
