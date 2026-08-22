# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-a8a5fdc0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""龍魂信任核心 · 异常定义。"""

from __future__ import annotations


class ConfirmCodeError(PermissionError):
    """确认码不匹配：破坏性操作（回滚/覆盖/清除）被闸门拒绝。"""


class CircuitBreakerTripped(RuntimeError):
    """熔断已触发：字段矛盾计数达到阈值，禁止继续使用该字段。"""
