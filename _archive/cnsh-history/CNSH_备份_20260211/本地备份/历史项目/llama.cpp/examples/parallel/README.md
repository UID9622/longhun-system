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
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 坤卦：地势坤，君子以厚德载物
📜 内容哈希: f3c97fc5d4679899
⚠️ 警告: 未经授权修改将触发DNA追溯系统
