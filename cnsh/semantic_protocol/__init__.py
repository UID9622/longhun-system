# -*- coding: utf-8 -*-
"""语义协议模型 v1.0 · Hook 点 Phase 1（意识流插桩烟测）。"""

__all__ = ["hook", "capture_at_moment", "interpret", "compress_record", "persist"]


def __getattr__(name: str):
    if name in __all__:
        from cnsh.semantic_protocol import hook_point as _hp

        return getattr(_hp, name)
    raise AttributeError(name)
