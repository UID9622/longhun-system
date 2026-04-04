# CI

This CI implements heavy-duty workflows that run on self-hosted runners. Typically the purpose of these workflows is to
cover hardware configurations that are not available from Github-hosted runners and/or require more computational
resource than normally available.

It is a good practice, before publishing changes to execute the full CI locally on your machine. For example:

```bash
mkdir tmp

# CPU-only build
bash ./ci/run.sh ./tmp/results ./tmp/mnt

# with CUDA support
GG_BUILD_CUDA=1 bash ./ci/run.sh ./tmp/results ./tmp/mnt

# with SYCL support
source /opt/intel/oneapi/setvars.sh
GG_BUILD_SYCL=1 bash ./ci/run.sh ./tmp/results ./tmp/mnt

# with MUSA support
GG_BUILD_MUSA=1 bash ./ci/run.sh ./tmp/results ./tmp/mnt

# etc.
```

# Adding self-hosted runners

- Add a self-hosted `ggml-ci` workflow to [[.github/workflows/build.yml]] with an appropriate label
- Request a runner token from `ggml-org` (for example, via a comment in the PR or email)
- Set-up a machine using the received token ([docs](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners))
- Optionally update [ci/run.sh](https://github.com/ggml-org/llama.cpp/blob/master/ci/run.sh) to build and run on the target platform by gating the implementation with a `GG_BUILD_...` env

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-a43868a1-20251218032410
🌐 签名人: 龍魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 坤卦：地势坤，君子以厚德载物
📜 内容哈希: e03667a5e63070b3
⚠️ 警告: 未经授权修改将触发DNA追溯系统
