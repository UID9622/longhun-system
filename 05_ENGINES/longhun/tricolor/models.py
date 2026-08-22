# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 🐉 龍魂·三色审计 数据模型 v1.1
# DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-TRICOLOR-MODELS-v1.1-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

"""
三色审计 API 数据模型（与 OpenAPI 规范一一对齐）。

所有模型从 engine 模块统一导出，避免定义分叉。
如需独立导入（不依赖完整引擎），直接从此文件导入。
"""

from .engine import (
    Scores,
    EvaluateRequest,
    Verdict,
    AuditRecord,
)

__all__ = ["Scores", "EvaluateRequest", "Verdict", "AuditRecord"]
