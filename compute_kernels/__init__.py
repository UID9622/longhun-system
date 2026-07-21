"""
🐉 龍魂计算内核 · 高性能 SIMD 加速层
DNA: #龍芯⚡️2026-07-13-COMPUTE-KERNELS-v1.0

x86-64 AVX/SSE 汇编优化的神经网络推理原语：
  SiLU · RMS Norm · Linear (matvec) · RoPE · 统计约束

编译: cd compute_kernels && make
测试: cd compute_kernels && make test
"""

from .lh_simd_compute import (
    lh_silu,
    lh_rms_norm,
    lh_linear,
    lh_apply_rope,
    lh_stat_constraint,
    is_available,
    get_lib_path,
    engine_type,
)

__all__ = [
    "lh_silu",
    "lh_rms_norm",
    "lh_linear",
    "lh_apply_rope",
    "lh_stat_constraint",
    "is_available",
    "get_lib_path",
    "engine_type",
]
