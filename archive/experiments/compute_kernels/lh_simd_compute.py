# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂 SIMD 计算内核 · Python ctypes 绑定 + 纯 Python 回退
DNA: #龍芯⚡️2026-07-13-COMPUTE-KERNELS-v1.1

提供 5 个神经网络推理原语：
  SiLU · RMS Norm · Linear (matvec) · RoPE · 统计约束

架构检测: x86-64 → SIMD 汇编 / ARM64 → 纯 Python 回退
"""

import ctypes
import math
import platform
from pathlib import Path
from typing import Optional

__all__ = [
    "lh_silu", "lh_rms_norm", "lh_linear",
    "lh_apply_rope", "lh_stat_constraint",
    "is_available", "get_lib_path", "engine_type",
]

_KERNEL_DIR = Path(__file__).parent
_lib: Optional[ctypes.CDLL] = None
_arch = platform.machine()


def _find_lib() -> Optional[str]:
    candidates = [
        _KERNEL_DIR / "liblh_kernels.dylib",
        _KERNEL_DIR / "liblh_kernels.so",
    ]
    for path in candidates:
        if path.exists():
            return str(path)
    return None


def _load_lib() -> Optional[ctypes.CDLL]:
    global _lib
    if _lib is not None:
        return _lib
    lib_path = _find_lib()
    if lib_path is None:
        return None
    try:
        _lib = ctypes.CDLL(str(lib_path))
    except OSError:
        return None
    try:
        _lib._lh_silu.argtypes = [ctypes.c_float]
        _lib._lh_silu.restype = ctypes.c_float
        _lib._lh_rms_norm.argtypes = [ctypes.c_void_p]*3 + [ctypes.c_int]
        _lib._lh_rms_norm.restype = None
        _lib._lh_linear.argtypes = [ctypes.c_void_p]*3 + [ctypes.c_int, ctypes.c_int]
        _lib._lh_linear.restype = None
        _lib._lh_apply_rope.argtypes = [ctypes.c_void_p]*3 + [ctypes.c_int]
        _lib._lh_apply_rope.restype = None
        _lib._lh_apply_stat_constraint.argtypes = [
            ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p,
            ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_float
        ]
        _lib._lh_apply_stat_constraint.restype = None
    except AttributeError:
        _lib = None
        return None
    return _lib


def _to_ctypes(arr, n):
    """将 list/numpy 转为 ctypes float 数组"""
    if hasattr(arr, '__array_interface__'):
        return (ctypes.c_float * n).from_buffer(arr)
    return (ctypes.c_float * n)(*arr)


def _copyback(dest, src, n):
    """将 ctypes 结果拷贝回 Python list"""
    if not hasattr(dest, '__array_interface__'):
        dest[:] = list(src)


def is_available() -> bool:
    return _load_lib() is not None


def get_lib_path() -> Optional[str]:
    return _find_lib()


def engine_type() -> str:
    """返回当前计算引擎类型"""
    if is_available():
        return f"SIMD (x86-64 AVX/SSE)"
    return f"纯Python ({_arch})"


# ============================================================
# 纯 Python 回退实现
# ============================================================

def _py_silu(x: float) -> float:
    return x / (1.0 + math.exp(-x))


def _py_rms_norm(out, x, weight, n: int):
    rms = math.sqrt(sum(v*v for v in x) / n)
    inv_rms = 1.0 / rms if rms > 1e-8 else 1.0
    for i in range(n):
        out[i] = x[i] * inv_rms * weight[i]


def _py_linear(x, w, out, in_dim: int, out_dim: int):
    for i in range(out_dim):
        s = 0.0
        row_base = i * in_dim
        for j in range(in_dim):
            s += w[row_base + j] * x[j]
        out[i] = s


def _py_apply_rope(x, cos, sin, dim: int):
    half = dim // 2
    for i in range(half):
        a, b = x[i], x[i + half]
        c, s = cos[i], sin[i]
        x[i] = a * c - b * s
        x[i + half] = b * c + a * s


def _py_stat_constraint(x, size: int, mean, std,
                        gamma: float = 0.9, k: float = 3.0,
                        max_norm: float = 100.0, min_norm: float = 0.01):
    # 计算当前范数
    norm_val = math.sqrt(sum(v*v for v in x))
    old_mean = mean[0]
    old_std = std[0]

    # EMA 更新统计量
    new_mean = gamma * old_mean + (1.0 - gamma) * norm_val
    new_std = gamma * old_std + (1.0 - gamma) * abs(norm_val - old_mean)
    mean[0] = new_mean
    std[0] = new_std

    # 自适应约束: norm > mean + k*std → 缩放
    threshold = new_mean + k * new_std
    if norm_val > threshold:
        scale = threshold / norm_val
        for i in range(size):
            x[i] *= scale

    # 硬上限约束
    if norm_val > max_norm:
        scale = max_norm / norm_val
        for i in range(size):
            x[i] *= scale


# ============================================================
# 统一接口 (SIMD 优先 → Python 回退)
# ============================================================

def lh_silu(x: float) -> float:
    lib = _load_lib()
    if lib:
        return lib._lh_silu(ctypes.c_float(x))
    return _py_silu(x)


def lh_rms_norm(out, x, weight, n: int):
    lib = _load_lib()
    if lib:
        _out = _to_ctypes(out, n)
        _x = _to_ctypes(x, n)
        _w = _to_ctypes(weight, n)
        lib._lh_rms_norm(_out, _x, _w, ctypes.c_int(n))
        _copyback(out, _out, n)
        return
    _py_rms_norm(out, x, weight, n)


def lh_linear(x, w, out, in_dim: int, out_dim: int):
    lib = _load_lib()
    if lib:
        _x = _to_ctypes(x, in_dim)
        _w = _to_ctypes(w, in_dim * out_dim)
        _out = _to_ctypes(out, out_dim)
        lib._lh_linear(_x, _w, _out, ctypes.c_int(in_dim), ctypes.c_int(out_dim))
        _copyback(out, _out, out_dim)
        return
    _py_linear(x, w, out, in_dim, out_dim)


def lh_apply_rope(x, cos, sin, dim: int):
    lib = _load_lib()
    if lib:
        _x = _to_ctypes(x, dim)
        _c = _to_ctypes(cos, dim // 2)
        _s = _to_ctypes(sin, dim // 2)
        lib._lh_apply_rope(_x, _c, _s, ctypes.c_int(dim))
        _copyback(x, _x, dim)
        return
    _py_apply_rope(x, cos, sin, dim)


def lh_stat_constraint(x, size: int, mean, std,
                       gamma: float = 0.9, k: float = 3.0,
                       max_norm: float = 100.0, min_norm: float = 0.01):
    lib = _load_lib()
    if lib:
        _x = _to_ctypes(x, size)
        _m = _to_ctypes(mean, 1)
        _s = _to_ctypes(std, 1)
        lib._lh_apply_stat_constraint(
            _x, ctypes.c_int(size), _m, _s,
            ctypes.c_float(gamma), ctypes.c_float(k),
            ctypes.c_float(max_norm), ctypes.c_float(min_norm)
        )
        _copyback(x, _x, size)
        if not hasattr(mean, '__array_interface__'):
            mean[0] = _m[0]
        if not hasattr(std, '__array_interface__'):
            std[0] = _s[0]
        return
    _py_stat_constraint(x, size, mean, std, gamma, k, max_norm, min_norm)
