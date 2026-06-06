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
  文件: README-MUSA.md | 标记时间: 2026-06-03T07:46:00+0800
-->
## Running MUSA CI in a Docker Container

Assuming `$PWD` is the root of the `llama.cpp` repository, follow these steps to set up and run MUSA CI in a Docker container:

### 1. Create a local directory to store cached models, configuration files and venv:

```bash
mkdir -p $HOME/llama.cpp/ci-cache
```

### 2. Create a local directory to store CI run results:

```bash
mkdir -p $HOME/llama.cpp/ci-results
```

### 3. Start a Docker container and run the CI:

```bash
docker run --privileged -it \
    -v $HOME/llama.cpp/ci-cache:/ci-cache \
    -v $HOME/llama.cpp/ci-results:/ci-results \
    -v $PWD:/ws -w /ws \
    mthreads/musa:rc4.3.0-devel-ubuntu22.04-amd64
```

Inside the container, execute the following commands:

```bash
apt update -y && apt install -y bc cmake ccache git python3.10-venv time unzip wget
git config --global --add safe.directory /ws
GG_BUILD_MUSA=1 bash ./ci/run.sh /ci-results /ci-cache
```

This setup ensures that the CI runs within an isolated Docker environment while maintaining cached files and results across runs.

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-1b8786e8-20251218032410
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 蒙卦：山下出泉，君子以果行育德
📜 内容哈希: ade57e9c5e86c06c
⚠️ 警告: 未经授权修改将触发DNA追溯系统
