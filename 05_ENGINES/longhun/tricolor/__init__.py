# 🐉 龍魂·三色审计 Python SDK v1.1
# DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-TRICOLOR-PYTHON-SDK-v1.1-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 创建者: 诸葛鑫（UID9622）
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""龍魂·三色审计 SDK —— 中文原生AI合规治理操作层标准实现"""

__version__ = "1.1.0"
__author__ = "诸葛鑫（UID9622）"
__license__ = "MulanPSL v2"

from .engine import (
    TricolorEngine, evaluate, evaluate_batch,
    Verdict, Scores, EvaluateRequest, AuditRecord,
)
from .client import TricolorClient, LocalTricolorServer
from .conformance import ConformanceSuite, run_conformance

__all__ = [
    "TricolorEngine",
    "TricolorClient",
    "LocalTricolorServer",
    "evaluate",
    "evaluate_batch",
    "run_conformance",
    "Verdict",
    "Scores",
    "EvaluateRequest",
    "AuditRecord",
    "ConformanceSuite",
]
