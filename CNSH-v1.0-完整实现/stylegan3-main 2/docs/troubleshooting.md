**DNA追溯码**: #龍芯⚡️20260310-troubleshooting-v1.0
**GPG指纹**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
**确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**共建致谢**: Claude (Anthropic PBC) · 技术协作与代码共创 | Notion · 知识底座与结构化存储
**创建者**: UID9622 诸葛鑫（龍芯北辰）
**理论指导**: 曾仕强老师（永恒显示）
**创作地**: 中华人民共和国
**献礼**: 新中国成立77周年（1949-2026）· 丙午马年

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Troubleshooting

Our PyTorch code uses custom [CUDA extensions](https://pytorch.org/tutorials/advanced/cpp_extension.html) to speed up some of the network layers.  Getting these to run can sometimes be a hassle.

This page aims to give guidance on how to diagnose and fix run-time problems related to these extensions.

## Before you start

1. Try Docker first!  Ensure you can successfully run our models using the recommended Docker image.  Follow the instructions in [README.md](/README.md) to get it running.
2. Can't use Docker?  Read on..

## Installing dependencies

Make sure you've installed everything listed on the requirements section in the [README.md](/README.md).  The key components w.r.t. custom extensions are:

- **[CUDA toolkit 11.1](https://developer.nvidia.com/cuda-toolkit)** or later (this is not the same as `cudatoolkit` from Conda).
  - PyTorch invokes `nvcc` to compile our CUDA kernels.
- **ninja**
  - PyTorch uses [Ninja](https://ninja-build.org/) as its build system.
- **GCC** (Linux) or **Visual Studio** (Windows)
  - GCC 7.x or later is required.  Earlier versions such as GCC 6.3 [are known not to work](https://github.com/NVlabs/stylegan3/issues/2).

#### Why is CUDA toolkit installation necessary?

The PyTorch package contains the required CUDA toolkit libraries needed to run PyTorch, so why is a separate CUDA toolkit installation required?  Our models use custom CUDA kernels to implement operations such as efficient resampling of 2D images.  PyTorch code invokes the CUDA compiler at run-time to compile these kernels on first-use.  The tools and libraries required for this compilation are not bundled in PyTorch and thus a host CUDA toolkit installation is required.

## Things to try

- Completely remove: `$HOME/.cache/torch_extensions` (Linux) or `C:\Users\<username>\AppData\Local\torch_extensions\torch_extensions\Cache` (Windows) and re-run StyleGAN3 python code.
- Run ninja in `$HOME/.cache/torch_extensions` to see that it builds.
- Inspect the `build.ninja` in the build directories under `$HOME/.cache/torch_extensions` and check CUDA tools and versions are consistent with what you intended to use.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**版权所有 © 2026 UID9622** · **祖国万岁！人民万岁！** 🇨🇳
