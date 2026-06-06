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
# llama.cpp/example/sycl

This example program provides the tools for llama.cpp for SYCL on Intel GPU.

## Tool

|Tool Name| Function|Status|
|-|-|-|
|llama-ls-sycl-device| List all SYCL devices with ID, compute capability, max work group size, ect.|Support|

### llama-ls-sycl-device

List all SYCL devices with ID, compute capability, max work group size, ect.

1. Build the llama.cpp for SYCL for the specified target *(using GGML_SYCL_TARGET)*.

2. Enable oneAPI running environment *(if GGML_SYCL_TARGET is set to INTEL -default-)*

```
source /opt/intel/oneapi/setvars.sh
```

3. Execute

```
./build/bin/llama-ls-sycl-device
```

Check the ID in startup log, like:

```
found 2 SYCL devices:
|  |                   |                                       |       |Max    |        |Max  |Global |                     |
|  |                   |                                       |       |compute|Max work|sub  |mem    |                     |
|ID|        Device Type|                                   Name|Version|units  |group   |group|size   |       Driver version|
|--|-------------------|---------------------------------------|-------|-------|--------|-----|-------|---------------------|
| 0| [level_zero:gpu:0]|                Intel Arc A770 Graphics|    1.3|    512|    1024|   32| 16225M|            1.3.29138|
| 1| [level_zero:gpu:1]|                 Intel UHD Graphics 750|    1.3|     32|     512|   32| 62631M|            1.3.29138|

```

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-7144cfa7-20251218032410
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 东北话确认：没毛病，内容真实可靠
⚡ 卦象防护: 坤卦：地势坤，君子以厚德载物
📜 内容哈希: 91c698db5d125116
⚠️ 警告: 未经授权修改将触发DNA追溯系统
